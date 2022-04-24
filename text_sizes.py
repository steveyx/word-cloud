import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


def short_title(string):
    _p = "[^\d\.\sa-zA-ZÀ-ÿ]"
    _r = re.findall(_p, string)
    if _r:
        string = string.split(_r[0])[0]
    words = string.split(" ")
    return " ".join(words[:3]).strip()


def get_text_size(df_texts):
    x_size, y_size = 8, 8
    _fig = plt.figure(figsize=(x_size, y_size))
    ax = _fig.add_axes([0.05, .05, .9, .9])
    ax.set_aspect('equal')
    x_min, x_max = 0, 1
    y_min, y_max = 0, 1
    ax.set_xlim((x_min, x_max))
    ax.set_ylim((y_min, y_max))
    rd = _fig.canvas.get_renderer()
    df_texts["width"] = 0
    df_texts["height"] = 0

    for idx, row in df_texts.iterrows():
        s_title = row["short_title"]
        size = row["weight"]
        _txt = ax.text(0.5, 0.05, s_title, horizontalalignment="center", verticalalignment="center", rotation=0,
                       fontsize=size)
        _bb = _txt.get_window_extent(renderer=rd)
        _points = ax.transData.inverted().transform(_bb)
        w = _points[1, 0] - _points[0, 0]
        h = _points[1, 1] - _points[0, 1]
        df_texts.loc[idx, "width"] = w
        df_texts.loc[idx, "height"] = h
    df_texts["area"] = df_texts["width"] * df_texts["height"]
    _fig_size = _fig.get_size_inches()
    _dpi = _fig.dpi
    df_texts["height_pixel"] = df_texts["height"] / (y_max-y_min) * 0.8 * y_size * _dpi
    print(df_texts[["short_title", "width", "height", "area", "height_pixel"]])
    print("fig size: {}, dpi: {}".format(_fig_size, _dpi))
    print("total area: ", sum(df_texts["area"]))
    # ax.cla()
    # plt.close(_fig)
    # plt.show()


if __name__ == "__main__":
    games = pd.read_csv("data/android-games.csv")
    games.sort_values(by="total ratings", ascending=False, inplace=True)
    games.reset_index(drop=True, inplace=True)
    tn = 150
    games["short_title"] = games["title"].apply(lambda x: short_title(x))
    games = games[games["short_title"].str.len() > 0]
    top_n_games = games.iloc[:tn].copy()
    max_w = top_n_games["total ratings"].max()
    min_w = top_n_games["total ratings"].min()
    max_times = 9 if int(max_w/min_w) > 9 else int(max_w/min_w)
    top_n_games["weight"] = np.int32(np.log2(1 + top_n_games["total ratings"]/min_w) * max_times)

    get_text_size(top_n_games)
    columns = ["short_title", "weight", "width", "height"]
    top_n_games[columns].to_csv("data/top_games.csv", index=False)