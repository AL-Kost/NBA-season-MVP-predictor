import joblib
import json
import pandas as pd
from application import conf
from typing import Optional


def load_model():
    """Load the model from the path specified in the configuration.

    Returns:
        joblib: The model loaded from disk.
    """
    return joblib.load(conf.data.model.path)


def load_csv_data(path: str, sep: str, encoding: str, compression: str,
                  index_col: Optional[int] = 0, nrows: Optional[int] = None,
                  dtype: Optional[dict] = None) -> pd.DataFrame:
    """Load data from a CSV file.

    Args:
        path (str): The path to the CSV file.
        sep (str): The delimiter used in the CSV file.
        encoding (str): The encoding used in the CSV file.
        compression (str): The compression format used in the CSV file.
        index_col (int, optional): The index column in the CSV file. Defaults to 0.
        nrows (int, optional): The number of rows to read from the CSV file. Reads all rows by default.
        dtype (dict, optional): Dictionary specifying the data types for columns.

    Returns:
        pd.DataFrame: The data loaded from the CSV file.
    """
    return pd.read_csv(
        path, sep=sep, encoding=encoding, compression=compression,
        index_col=index_col, nrows=nrows, dtype=dtype
    )


def load_player_stats(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data.player_stats, nrows=nrows)


def load_mvp_votes(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data.mvp_votes, nrows=nrows)


def load_team_standings(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data.team_standings, nrows=nrows)


def load_medal_data(medal_type: str, nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data[medal_type], nrows=nrows)


def load_predictions(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data.predictions, nrows=nrows)


def load_history(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data.history, nrows=nrows)


def load_features() -> dict:
    """Load feature data from a JSON file.

    Returns:
        dict: The feature data loaded from the JSON file.
    """
    with open(conf.data.features.path, encoding=conf.data.features.encoding) as json_file:
        return json.load(json_file)


def load_model_input(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data.model_input, nrows=nrows)


def load_shap_values(nrows: Optional[int] = None) -> pd.DataFrame:
    return load_csv_data(**conf.data.shap_values, nrows=nrows)
