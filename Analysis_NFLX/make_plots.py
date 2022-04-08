import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors

RESULTS = 'results_no_mask.csv'

data = pd.read_csv(RESULTS)
names = [*{*data['Reference']}]

for name in names:

    fig, ax = plt.subplots()
    ax.set_title(name)
    axs = [ax, ax.twinx(), ax.twinx()]
    colors = mcolors.TABLEAU_COLORS.values()
    legend = []

    i = 0
    for metric, color, ax in zip(['ssim', 'psnr', 'vmaf'], colors, axs):
        exact = data[(data['Reference'].str.match(name)) & (data['Metric'].str.match(metric))]
        if i > 0:
            ax.spines['right'].set_position(('axes', 1 + 1 * (i - 1)))
        ax.plot(exact['Subjective'], exact['Metric_val'], color=color, label=metric)
        ax.set_yticks([])
        legend += [ax.get_legend_handles_labels()]
        i += 1

    legend = np.array(legend).squeeze()
    plt.legend(legend[:, 0], legend[:, 1])
    # plt.savefig(f'datasets/NFLX/Analysis/{name.split("_")[0]}_compare_metrics.jpg')
    plt.show()