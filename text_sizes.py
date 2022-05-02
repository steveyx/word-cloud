import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt


"""
this module is to calculate the text box sizes using matplotlib
"""


def short_title(string):
    _p = "[^\d\.\sa-zA-ZÀ-ÿ]"
    _r = re.findall(_p, string)
    if _r:
        string = string.split(_r[0])[0]
    words = string.split(" ")
    return " ".join(words[:3]).strip()


def calculate_text_size(df_texts):
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
        _txt = ax.text(0.5, 0.5, s_title,
                       horizontalalignment="center", verticalalignment="center", rotation=0, fontsize=size)
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
    _total_area = sum(df_texts["area"])
    print(df_texts[["short_title", "width", "height", "area", "height_pixel"]])
    print("fig size: {}, dpi: {}".format(_fig_size, _dpi))
    print("total area: ", _total_area)
    # ax.cla()
    plt.close(_fig)
    # plt.show()
    return _total_area


def linear_scale(df, max_times=5, col="total ratings"):
    _max = df[col].max()
    _min = df[col].min()
    _cur_times = _max / _min
    print(_max, _min, _cur_times)
    return (df[col] - _min) * (max_times - 1) / (_cur_times - 1) / _min + 1


def log_scale(df, max_times=5, col="total ratings"):
    _max = df[col].max()
    _min = df[col].min()
    _cur_times = _max / _min
    b = np.exp(np.log(_max / _min) / (max_times - 1))
    return np.log(df[col] / _min) / np.log(b) + 1


def get_text_box_sizes(df, base_fontsize=8, max_fontsize_times=5, fontsize_by='total ratings'):
    _max_w = df[fontsize_by].max()
    _min_w = df[fontsize_by].min()
    use_log_scale = True
    if int(_max_w / _min_w) <= max_fontsize_times:
        df["weight"] = np.round(df[fontsize_by] / _min_w * base_fontsize, 1)
    else:
        if use_log_scale:
            _times = log_scale(df, max_times=max_fontsize_times, col=fontsize_by)
        else:
            _times = linear_scale(df, max_times=max_fontsize_times, col=fontsize_by)
        df["weight"] = np.round(_times * base_fontsize, 1)
    _total_area = calculate_text_size(df)
    columns = ["short_title", "weight", "width", "height"]
    df[columns].to_csv("data/top_games.csv", index=False)
    return _total_area


if __name__ == "__main__":
    games = pd.read_csv("data/android-games.csv")
    games.sort_values(by="total ratings", ascending=False, inplace=True)
    games.reset_index(drop=True, inplace=True)
    tn = 150
    games["short_title"] = games["title"].apply(lambda x: short_title(x))
    games = games[games["short_title"].str.len() > 0]
    top_n_games = games.iloc[:tn].copy()
    total_area = get_text_box_sizes(top_n_games, base_fontsize=8, max_fontsize_times=5, fontsize_by='total ratings')
