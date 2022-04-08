#! python
import os
import numpy as np
import matplotlib.pyplot as plt
from time import time
import csv
from tqdm import tqdm

METRICS = ['niqe']
INTERVAL = None

TMP_FILE = 'tmp_file.txt'
DISTORTED = '../sequences'
REFERENCES = '../references'
RESULTS = 'results_niqe.csv'
MASKS = '../masks_mod'
ERRORS = 'errors.txt'


def calc_metric_for_video(ref: str, dis: str, metric: str, mask_path=None) -> float:
    cmd = "../../vqmt "
    if ref is not None:
        cmd += f"-orig {ref} 1920x1080 YUV420p "
    cmd += f"-in {dis} "
    if mask_path is not None:
        cmd += f"-mask {mask_path}  -mask-type 8bit black "
    cmd += f"-metr {metric} over Y -resize to orig | grep mean > {TMP_FILE} "

    os.system(cmd)
    with open(TMP_FILE) as tmp_file:
        line = tmp_file.readline()
        metric_value = float(line.split()[-1])
    return metric_value


HEADERS = 'Reference,Distorted,Metric,Metric_val,Mask'.split(',')


class MyWriter:
    def __init__(self, f):
        self.filename = f
        if not os.path.exists(self.filename):
            os.open(self.filename, os.O_CREAT)

    def write_row(self, row):
        with open(self.filename, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(row)
            print("%5s%-55s%-90s%-20s%-20s%-10s" % tuple([''] + row))

    def write_text(self, text):
        with open(self.filename, 'a') as f:
            f.write(text)
            print(text)


writer_results = MyWriter(RESULTS)
writer_errors = MyWriter(ERRORS)

writer_results.write_row(HEADERS)

# assumed, that files in folders DISTORTED, REFERENCES, MASKS go in the same order
dis_sequences = [x for x in os.listdir(DISTORTED) if os.path.isdir(f'{DISTORTED}/{x}')]
dis_sequences.sort()

references = [x for x in os.listdir(REFERENCES)]
references.sort()

masks_map = [x for x in os.listdir(MASKS)]
masks_map.sort()

for folder, ref, mask_map in [*zip(dis_sequences, references, masks_map)][:1]:
    for metric in METRICS:
        for mask_mode in [False, True]:
            try:
                distorted_seq = f'{DISTORTED}/{folder}'
                videos = os.listdir(distorted_seq)
                # videos = [x for x in videos if x.find('x265') >= 0]
                # scores = [v.split('.')[0].split('_')[-1] for v in videos]
                # ref = videos[np.argmin(scores)]

                # dis_list = [x for x in os.listdir(cur_dir) if x != ref]
                dis_list = [x for x in os.listdir(distorted_seq)]

                time_start_sequence = time()
                for dis in dis_list:
                    time_start_video = time()
                    ref_path = f'{REFERENCES}/{ref}'
                    dis_path = f'{distorted_seq}/{dis}'
                    mask_path = f'{MASKS}/{mask_map}' if mask_mode is True else None

                    ref_path = None

                    metric_val = calc_metric_for_video(ref_path, dis_path, metric, mask_path)

                    row = (ref, dis, metric, metric_val, mask_mode)
                    writer_results.write_row(row)
                    print('time for video:', f'{int(time() - time_start_video)} sec')
                time_for_seq = int(time() - time_start_sequence)
                print('>>> time for sequence:', f'{time_for_seq // 60} min, {time_for_seq % 60} sec')
            except:
                try:
                    writer_errors.write_text(f'ERROR:  {folder}, {metric}, {mask_mode}')
                except:
                    print(f'ERROR WHILE LOGGING ERROR')
