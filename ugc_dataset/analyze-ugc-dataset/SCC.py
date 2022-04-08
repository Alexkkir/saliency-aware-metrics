import sys
from subjectify_lib import parse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from io import StringIO

data = pd.read_csv('results_psnr_vmaf_9_subj.csv')
names = sorted([*{*data['Reference']}])[:-1]
metrics = sorted([*{*data['Metric']}])

tables_str = {metric: dict() for metric in metrics}
tables_val = {metric: {False: [], True: []} for metric in metrics}


def format3f(x):
    return '%.3f' % x


for metric in metrics:
    for name in names:
        ba = []
        tables_str[metric][name] = pd.Series()
        for mask in [False, True]:
            vid = data[(data['Reference'] == name) & (data['Mask'] == mask)]
            exact = vid[vid['Metric'] == metric]

            bad_exp = []
            for i in exact.index:
                s = exact.loc[i, 'Distorted']
                codec = parse(s)['codec']
                if codec == 'kingsoft_v2':
                    bad_exp.append(i)
            exact = exact.drop(bad_exp, axis=0)

            exact = exact[['Subjective', 'Metric_val']]

            rho = exact.corr(method='spearman')
            rho = np.array(rho)[0][1]
            tables_val[metric][mask].append(rho)
            tables_str[metric][name][f'Mask={mask}'] = format3f(rho)

sys.stdout

means = {met: {f'Mask={mask}': format3f(np.mean(c)) for mask, c in by_mask.items()} for met, by_mask in
         tables_val.items()}

with open('SCC.txt', 'w') as f:
    sys.stdout = f
    print(pd.DataFrame(means))
    print()

    for m, df in tables_str.items():
        print(f'Metric={m}:')
        print(pd.DataFrame(df).to_string())
        print()
