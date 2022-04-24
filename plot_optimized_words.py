import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud

"""
this module is to 
1) visualize word cloud after solving the 2d bin pack problem
2) visualize using alternate WordCloud library  
"""

n_colors = 100
color_map = plt.get_cmap("jet", n_colors)
colors = [color_map(x) for x in range(n_colors)]
font_families = ['serif', 'sans-serif', 'fantasy', 'monospace']


def load_texts(fn="data/top_games.csv"):
    _df = pd.read_csv(fn)
    return _df


def plot_optimized_texts(fn="data/top_games_results.csv", xlim=1, ylim=1):
    _df = pd.read_csv(fn)
    print(_df)
    _fig = plt.figure(figsize=(8*xlim, 8*ylim))
    ax = _fig.add_axes([0.05, .05, .9, .9])
    ax.set_aspect('equal')
    ax.set_ylim((0, ylim))
    ax.set_xlim((0, xlim))
    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor('black')
    for idx, row in _df.iterrows():
        s_title = row["short_title"]
        size = row["weight"]
        angle = row["vertical"] * 90
        _txt = ax.text(row["cx"], row["cy"], s_title, horizontalalignment="left", verticalalignment="bottom",
                       rotation=angle, fontsize=size,
                       # fontname='Symbol',
                       color=colors[np.random.randint(n_colors)])
    plt.show()


def plot_by_word_cloud():
    _df = load_texts()

    text_dict = {r.short_title: r.weight for r in _df.itertuples()}
    wc = WordCloud(background_color="white", max_words=1000)
    # generate word cloud
    wc.generate_from_frequencies(text_dict)
    # show
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()


if __name__ == "__main__":
    plot_optimized_texts(xlim=1.4, ylim=0.9)
    plot_by_word_cloud()

