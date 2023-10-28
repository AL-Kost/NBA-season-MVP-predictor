import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt


def get_columns_with_inter_correlations_under(dataframe, threshold):
    """
    Remove columns that have correlation above a specified threshold.

    :param dataframe: Input DataFrame
    :param threshold: Correlation threshold
    :return: Remaining columns after removal
    """
    data_copy = dataframe.copy()
    initial_num_cols = len(data_copy.columns)

    high_correlation_pairs = get_column_pairs_correlation_above_threshold(data_copy, threshold)

    while high_correlation_pairs:
        col_to_drop = high_correlation_pairs[0][1]
        print(f"Dropping {col_to_drop} which is correlated with {high_correlation_pairs[0][0]}")
        data_copy.drop(col_to_drop, axis="columns", inplace=True)
        high_correlation_pairs = get_column_pairs_correlation_above_threshold(data_copy, threshold)

    remaining_cols = data_copy.columns
    print(f"Reduced number of columns from {initial_num_cols} to {len(remaining_cols)}")

    return remaining_cols


def get_column_pairs_correlation_above_threshold(dataframe, threshold):
    """
    Get pairs of columns that have a correlation above the given threshold.

    :param dataframe: Input DataFrame
    :param threshold: Correlation threshold
    :return: Pairs of columns with high correlation
    """
    correlations = dataframe.corr().abs()
    sorted_correlations = correlations.unstack().sort_values(ascending=False)
    filtered_correlations = sorted_correlations[(sorted_correlations < 1.0) & (sorted_correlations > threshold)]

    return filtered_correlations.index.tolist()


def get_columns_correlation_with_target(dataframe, target_column, method="pearson"):
    """
    Get column correlations with a specified target column.

    :param dataframe: Input DataFrame
    :param target_column: Target column
    :param method: Correlation method (default is "pearson")
    :return: Sorted series of column correlations with the target column
    """
    correlations_with_target = dataframe.corr(method=method)[target_column]
    return correlations_with_target[correlations_with_target < 1.0].abs().sort_values(ascending=False)


def pairplot_columns(dataframe, columns, color_by):
    """
    Create pairplots of specified columns.

    :param dataframe: Input DataFrame
    :param columns: Columns to plot
    :param color_by: Column to color by
    """
    sns.pairplot(dataframe, hue=color_by, x_vars=columns, y_vars=columns, corner=True)


def plot_columns_against_target(dataframe, columns, target_column):
    """
    Plot specified columns against a target column.

    :param dataframe: Input DataFrame
    :param columns: Columns to plot
    :param target_column: Target column
    """
    sns.pairplot(dataframe, x_vars=[target_column], y_vars=columns, corner=True)


def plot_correlation_heatmap(dataframe, corner=True, method="pearson"):
    """
    Plot a correlation heatmap of the dataframe.

    :param dataframe: Input DataFrame
    :param corner: If True, only plot the lower triangle of the heatmap
    :param method: Correlation method (default is "pearson")
    """
    corr_matrix = dataframe.corr(method=method)
    mask = np.triu(np.ones_like(corr_matrix, dtype=bool)) if corner else None
    cmap = sns.diverging_palette(240, 10, as_cmap=True)

    sns.heatmap(
        corr_matrix,
        mask=mask,
        cmap=cmap,
        vmax=0.3,
        center=0,
        square=True,
        linewidths=0.5,
        cbar_kws={"shrink": 0.5},
        annot=True,
        fmt=".2f"
    )

    plt.title(method)
