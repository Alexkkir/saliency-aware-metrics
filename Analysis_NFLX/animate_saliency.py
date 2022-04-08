import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from skimage import io
from skimage.transform import resize
from PIL import Image
from tqdm import tqdm
import os

NAME = 'BirdsInCage_30fps'
DIRECTORY_SRC = f'datasets/NFLX/{NAME}/'
DIRECTORY_ORIG = DIRECTORY_SRC + 'orig/'
DIRECTORY_SAL = DIRECTORY_SRC + 'sal/'
DIRECTORY_TMP = DIRECTORY_SRC + 'tmp/'

mpl.rcParams['animation.ffmpeg_path'] = r'C:\\ffmpeg\\bin\\ffmpeg.exe'

def animate_pil(i):
    name1 = "%04d.jpg" % (i + 1)
    name2 = "%04d.jpg" % (i + 1)
    image1 = io.imread(DIRECTORY_ORIG + name1)
    image2 = io.imread(DIRECTORY_SAL + name2)

    image1 = np.rint(resize(image1, (216, 384, 3)) * 256).astype('uint8')
    image2 = resize(image2, image1.shape)

    red = np.zeros_like(image1)
    red[:, :, 0] += 255

    image3 = image1 * (1 - image2) + red * image2
    image3 = np.rint(image3).astype('int')

    image2 = plt.get_cmap('viridis')(image2[:, :, 0])[:, :, :3] * 255

    image1 = Image.fromarray(image1.astype('uint8'))
    image2 = Image.fromarray(image2.astype('uint8'))
    image3 = Image.fromarray(image3.astype('uint8'))

    result = Image.new('RGB', (2 * image1.size[0] + 20, 2 * image1.size[1] + 20), (250, 250, 250))
    result.paste(image1, (0, 0))
    result.paste(image2, (image1.size[0] + 20, 0))
    result.paste(image3, (0, image1.size[1] + 20))
    # result.show()
    return result


if not os.path.exists(DIRECTORY_ORIG):
    os.mkdir(DIRECTORY_ORIG)
if not os.path.exists(DIRECTORY_SAL):
    os.mkdir(DIRECTORY_SAL)
if not os.path.exists(DIRECTORY_TMP):
    os.mkdir(DIRECTORY_TMP)

os.system(f'ffmpeg -i {DIRECTORY_SRC + NAME + ".mp4"} -q 0 {DIRECTORY_ORIG}%04d.jpg')
os.system(f'ffmpeg -i {DIRECTORY_SRC + NAME + "_saliency.mp4"} -q 0 {DIRECTORY_SAL}%04d.jpg')

n_frames = len(os.listdir(DIRECTORY_ORIG))
for i in tqdm(range(n_frames)):
    frame = animate_pil(i)
    frame.save(f'{DIRECTORY_TMP}%04d.jpg' % (i + 1), 'JPEG')

os.system(f'ffmpeg -i {DIRECTORY_TMP}%04d.jpg -b 10M {DIRECTORY_SRC}saliency_vis.mp4')