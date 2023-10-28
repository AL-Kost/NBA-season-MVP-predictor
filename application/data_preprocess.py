import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler


def standardize(dataframe: pd.DataFrame, fit_on: pd.DataFrame = None,
                fit_per_values_of: pd.Series = None, min_max_scaler: bool = False) -> pd.DataFrame:
    """
    Standardize the dataframe using MinMaxScaler or StandardScaler.

    Args:
        dataframe: Input dataframe to standardize.
        fit_on: Dataframe to fit the scaler on.
        fit_per_values_of: Series to fit the scaler on unique values.
        min_max_scaler: Use MinMaxScaler if True, otherwise StandardScaler.

    Returns:
        A standardized dataframe.
    """
    scaler = MinMaxScaler() if min_max_scaler else StandardScaler(with_mean=True, with_std=True)

    if fit_on is not None and fit_per_values_of is not None:
        raise NotImplementedError

    scaled = dataframe.copy()
    fit_on = fit_on or dataframe.copy()

    if fit_per_values_of is not None:
        for unique in fit_per_values_of.unique():
            curr_index = fit_per_values_of[fit_per_values_of == unique].index
            df_subset = dataframe.loc[curr_index, :]
            scaler.fit(df_subset)
            scaled.loc[curr_index, :] = scaler.transform(df_subset)
    else:
        scaler.fit(fit_on)
        scaled = scaler.transform(dataframe)

    return pd.DataFrame(scaled, columns=dataframe.columns)


def get_numerical_columns(dataframe: pd.DataFrame) -> list:
    """
    Get numerical columns from the dataframe.

    Args:
        dataframe: Input dataframe.

    Returns:
        List of numerical column names.
    """
    return dataframe.select_dtypes(include="number").columns.tolist()


def get_categorical_columns(dataframe: pd.DataFrame) -> list:
    """
    Get non-numerical columns from the dataframe.

    Args:
        dataframe: Input dataframe.

    Returns:
        List of non-numerical column names.
    """
    return dataframe.select_dtypes(exclude="number").columns.tolist()


def natural_log_transform(series: pd.Series) -> pd.Series:
    """
    Perform natural log transformation on the series.

    Args:
        series: Input series.

    Returns:
        Transformed series.
    """
    return np.log(series + 1)


def exp_transform(series: pd.Series) -> pd.Series:
    """
    Perform exponential transformation on the series.

    Args:
        series: Input series.

    Returns:
        Transformed series.
    """
    return np.exp(series)


def select_random_unique_values(series: pd.Series, share: float) -> list:
    """
    Select a random set of unique values from the series.

    Args:
        series: Input series.
        share: Fraction of unique values to select.

    Returns:
        List of unique values.
    """
    share_int = int(share * len(series.unique()))
    return series.sample(share_int).tolist()


def scale_per_value_of(data: pd.DataFrame, selected_cat_features: list, selected_num_features: list,
                       fit_per_value_of: pd.Series, min_max_scaler: bool = True) -> tuple:
    """
    Scale dataframe values based on specified categorical and numerical features.

    Args:
        data: Input dataframe.
        selected_cat_features: List of categorical features.
        selected_num_features: List of numerical features.
        fit_per_value_of: Series to fit the scaler on unique values.
        min_max_scaler: Use MinMaxScaler if True, otherwise StandardScaler.

    Returns:
        Tuple containing processed dataframe and raw data.
    """
    if not selected_num_features:
        raise NotImplementedError("Need at least 1 numerical feature")

    processed_num_data = standardize(
        data[selected_num_features], fit_on=None, fit_per_values_of=fit_per_value_of, min_max_scaler=min_max_scaler
    )

    if selected_cat_features:
        processed_cat_data = pd.get_dummies(data[selected_cat_features])
        processed_data = pd.concat([processed_num_data, processed_cat_data], axis=1)
        raw_data = data[selected_num_features + selected_cat_features]
    else:
        processed_data = processed_num_data
        raw_data = data[selected_num_features]

    return processed_data, raw_data
