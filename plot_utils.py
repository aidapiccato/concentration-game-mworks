from scipy.stats import linregress
import pandas as pd

def prettify(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.title.set_style('italic')
    ax.title.set_size(20)


def hline(ax, y):
    ax.axhline(y, linestyle='--', linewidth=1, color='black')


def fit_line(ax, x, y):
    if type(y) is pd.Series:
        is_nan = y.isnull()
        y = y[~is_nan]
        x = x[~is_nan]
    slope, intercept, r_value, p_value, std_err = linregress(x, y)
    y_fit = intercept + slope * x
    ax.plot(x, y_fit, 'r--', linewidth=1)
    return r_value, p_value, std_err

