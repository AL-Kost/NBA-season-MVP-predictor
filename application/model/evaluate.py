import numpy as np
from pandas import Series


def softmax(series: Series) -> Series:
    """
    Compute softmax values for each set of scores in the series.

    Args:
        series (Series): Input values.

    Returns:
        Series: Softmax-transformed values (total is 1).
    """
    exp_values = np.exp(series - np.max(series))
    return exp_values / exp_values.sum()


def share(series: Series) -> Series:
    """
    Compute the share of each value in the series based on its proportion of the series total.

    Args:
        series (Series): Input values.

    Returns:
        Series: Series of shares (total is 1).
    """
    return series / series.sum()
