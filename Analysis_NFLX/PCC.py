import pandas as pd
import numpy as np

RESULTS = 'results_psnr_vmaf_9_subj.csv'

data = pd.read_csv(RESULTS)
names = sorted([*{*data['Reference']}])[:-1]
metrics = sorted([*{*data['Metric']}])

PCC_final = pd.DataFrame(columns=metrics)
for mask in [False, True]:
    PCC = dict()
    for name in names:
        vid = data[(data['Reference'] == name) & (data['Mask'] == mask)]
        M = [vid[vid['Metric'].str.match(metrics[0])]['Subjective']]
        for metric in metrics:
            M.append(vid[vid['Metric'].str.match(metric)]['Metric_val'].reset_index(drop=True))

        M = np.array(M)
        rho = np.corrcoef(M)[0, 1:]
        PCC[name] = rho

    PCC_mean = dict()
    for metric, i in zip(metrics, range(len(metrics))):
        val = 0
        for vid in PCC.values():
            val += vid[i]
        val /= len(PCC)
        PCC_mean[metric] = val
    df = pd.DataFrame(PCC_mean, index=[f'Mask={mask}'])
    PCC_final = pd.concat([PCC_final, df])

print(PCC_final)
# with open('Analysis_NFLX/PCC.csv', 'w') as f:
#     f.write(str(PCC_final))



