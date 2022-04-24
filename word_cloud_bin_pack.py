import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from bin_pack_2d import bin_pack_2d
from plot_optimized_words import plot_optimized_texts

"""
given for a list of texts:
   each text has: width, height, vertical or not (optional)
this module is to optimize word positions (x, y) and vertical (0, or 1)
"""


def load_texts(fn="data/top_games.csv"):
    _df = pd.read_csv(fn).iloc[:]
    return _df


def get_text_size(fn="data/top_games_results.csv"):
    _df = pd.read_csv(fn)
    _fig = plt.figure(figsize=(10, 8))
    ax = _fig.add_axes([0.1, .1, .8, .8])
    ax.set_ylim((0, 1))
    ax.set_xlim((0, 1))
    for _idx, _r in _df.iterrows():
        s_title = _r["short_title"]
        size = _r["weight"]
        angle = _r["vertical"] * 90
        _txt = ax.text(_r["cx"], _r["cy"], s_title, horizontalalignment="center", verticalalignment="center",
                       rotation=angle, fontsize=size,
                       # family='fantasy'
                       )
    plt.show()


if __name__ == "__main__":
    np.random.RandomState(seed=10)
    df = load_texts()
    df["vertical"] = 0
    words = [(r["width"], r["height"], idx) if r["vertical"] == 0 else (r["height"], r["width"], idx)
             for idx, r in df.iterrows()]
    x_limit, y_limit = 1.31, 0.89
    ratio = 10000
    packed, unpacked = bin_pack_2d(words, xlim=x_limit, ylim=y_limit, ratio=ratio, rotation=False)
    df["cx"] = 0
    df["cy"] = 0
    for r in packed:
        df.loc[r["rid"], "cx"] = r["x"]/ratio
        df.loc[r["rid"], "cy"] = r["y"]/ratio
        df.loc[r["rid"], "vertical"] = r["vertical"]
        df.to_csv("data/top_games_results.csv", index=False)
    print("unpacked rectangles: ", unpacked)
    plot_optimized_texts(xlim=x_limit, ylim=y_limit)




