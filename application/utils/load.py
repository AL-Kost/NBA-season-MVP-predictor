import joblib
import json
import pandas as pd
from application import conf
from typing import Optional


def load_model():
    """Load the model."""
    return joblib.load(conf.data.model.path)


def _read_csv_from_conf(conf_data: dict, nrows: Optional[int] = None) -> pd.DataFrame:
    """Helper function to read CSV data from configuration."""
    return pd.read_csv(
        conf_data.path,
        sep=conf_data.sep,
        encoding=conf_data.encoding,
        compression=conf_data.compression,
        index_col=0,
        nrows=nrows
    )


def load_player_stats(nrows: Optional[int] = None) -> pd.DataFrame:
    return _read_csv_from_conf(conf.data.player_stats, nrows)


def load_mvp_votes(nrows: Optional[int] = None) -> pd.DataFrame:
    return _read_csv_from_conf(conf.data.mvp_votes, nrows)


def load_team_standings(nrows: Optional[int] = None) -> pd.DataFrame:
    return _read_csv_from_conf(conf.data.team_standings, nrows)


def load_bronze_data(nrows: Optional[int] = None) -> pd.DataFrame:
    return _read_csv_from_conf(conf.data.bronze, nrows)


def load_silver_data(nrows: Optional[int] = None) -> pd.DataFrame:
    return _read_csv_from_conf(conf.data.silver, nrows)


def load_gold_data(nrows: Optional[int] = None) -> pd.DataFrame:
    return _read_csv_from_conf(conf.data.gold, nrows)


def load_predictions(nrows: Optional[int] = None) -> pd.DataFrame:
    return pd.read_csv(
        conf.data.predictions.path,
        sep=conf.data.predictions.sep,
        encoding=conf.data.predictions.encoding,
        compression=conf.data.predictions.compression,
        index_col=0,
        nrows=nrows,
        dtype={}
    )


def load_history(nrows: Optional[int] = None) -> pd.DataFrame:
    return pd.read_csv(
        conf.data.history.path,
        sep=conf.data.history.sep,
        encoding=conf.data.history.encoding,
        compression=conf.data.history.compression,
        index_col=False,
        nrows=nrows,
        dtype={}
    )


def load_features() -> dict:
    with open(conf.data.features.path, encoding=conf.data.features.encoding) as json_file:
        return json.load(json_file)


def load_model_input(nrows: Optional[int] = None) -> pd.DataFrame:
    return pd.read_csv(
        conf.data.model_input.path,
        sep=conf.data.model_input.sep,
        encoding=conf.data.model_input.encoding,
        compression=conf.data.model_input.compression,
        index_col=0,
        nrows=nrows,
        dtype={}
    )


def load_shap_values(nrows: Optional[int] = None) -> pd.DataFrame:
    return pd.read_csv(
        conf.data.shap_values.path,
        sep=conf.data.shap_values.sep,
        encoding=conf.data.shap_values.encoding,
        compression=conf.data.shap_values.compression,
        index_col=0,
        nrows=nrows,
        dtype={}
    )
