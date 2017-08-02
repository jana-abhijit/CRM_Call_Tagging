import matplotlib
matplotlib.use('agg')
matplotlib.rcParams['font.size'] = 8.0
import numpy as np
import matplotlib.pyplot as plt


def generate_pie_chart(labels, sizes, title, path):
    ax1 = plt.subplots()[1]
    axpie = ax1.pie(sizes, autopct='%1.1f%%', pctdistance=1.1)
    ax1.axis('equal')
    plt.title(title)
    plt.legend(axpie[0], labels, loc='lower center', bbox_to_anchor=(0.5, -0.4))
    plt.savefig(path,  bbox_inches='tight')


def generate_bar_chart(labels, sizes, title, path):
    ind = np.arange(len(labels))
    width = 0.35

    ax = plt.subplots()[1]
    ax.bar(ind, sizes)

    ax2 = ax.twinx()
    vals = ax2.get_yticks()
    ax2.set_yticklabels(['{:3.0f}%'.format(x*100) for x in vals])
    ax2.set_ylim(ymax=100)

    ax.set_title(title)
    ax.set_xticks(ind + width / 2)
    ax.set_xticklabels(labels, rotation=-65)

    plt.tight_layout()
    plt.savefig(path, bbox_inches='tight')
