import os

from moviepy.editor import VideoFileClip
import moviepy.video.fx.all as vfx

for file in os.listdir('masks'):
    clip = VideoFileClip(f'masks/{file}')
    clip2 = clip.fx(vfx.lum_contrast, lum=64, contrast=-0.25, contrast_thr=0)
    clip2.write_videofile(f'masks_mod/{file}')
