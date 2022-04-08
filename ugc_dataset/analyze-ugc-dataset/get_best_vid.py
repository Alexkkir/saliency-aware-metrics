import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from subjectify_lib import *

TABLE = '../Ugc_dataset/subjective_scores.csv'
df = pd.read_csv(TABLE, sep=';')
names = [*{*df[df['comparison'] == 'ugc']['sequence']}]


def top_3_best_codecs(name):
    TABLE = '../Ugc_dataset/subjective_scores.csv'
    df = pd.read_csv(TABLE, sep=';')
    df = df[df['comparison'] == 'ugc']

    arr = np.array(df[df['sequence'] == name][['codec', 'subjective']])
    arr = sorted(arr, key=lambda row: row[1], reverse=True)
    return arr[:3]

for name in names:
    print(name)
    print(*top_3_best_codecs(name), sep='\n')
    print()
