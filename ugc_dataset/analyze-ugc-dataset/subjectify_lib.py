import matplotlib.pyplot as plt
from time import time
import csv

import pandas
from tqdm import tqdm
import pandas as pd


def get_subjective_score(df: pandas.DataFrame, name, codec, crf, method):
    x = df[(df['comparison'] == 'ugc') & (df['sequence'] == name) & (df['crf'] == int(crf)) & (df['codec'] == codec) & (
            df['preset'] == method)]
    x = x['subjective']

    if len(x) == 1:
        x = float(x)
    else:
        x = None
    return x


def parse(name: str) -> dict[str]:
    out = dict()
    name = name.split('.')[0]
    name = name.split('enc_res_')[1]

    str1 = '_mv_offline_2k_v1_'
    str2 = '_mv_offline_2k_'

    if name.find(str1) >= 0:
        method = 'mv_offline_2k_v1'
        name = name.split(str1)
    else:
        method = 'mv_offline_2k'
        name = name.split(str2)

    out['method'] = method

    out['codec'] = name[0]

    name = name[1]
    name = name.split('_')
    out['crf'] = int(name[-1])

    name = '_'.join(name[0:-1])
    out['name'] = name

    return out


def add_subjective(data_csv,
                   modified_csv,
                   subjective_csv=r'../subjective_scores.csv'):
    subj = pandas.read_csv(subjective_csv, sep=';')

    print(get_subjective_score(subj, 'blue_hair', 'svt_av1', '48', 'mv_offline_2k'))  # 5.40818

    met = pandas.read_csv(data_csv)
    met['Subjective'] = float(0)

    new_df = pd.DataFrame(columns=met.columns)

    excluded_cnt = 0
    for index in met.index:
        try:
            dis = met.loc[index, 'Distorted']
            prop = parse(dis)
            subj_score = get_subjective_score(subj, **prop)
            if subj_score == None:
                print('EXCLUDED', index, met.loc[index, 'Distorted'])
                excluded_cnt += 1
            else:
                tmp_ser = met.loc[index]
                tmp_ser['Subjective'] = subj_score
                new_df = new_df.append(tmp_ser)
        except:
            print('ERROR', index, met.loc[index, 'Distorted'])

    print(f'Totally excluded {excluded_cnt} videos')
    new_df.to_csv(modified_csv)

