from datetime import datetime
import json

import pandas as pd

from application import conf, logger, data_preprocess
from application.utils import load
from application.model import train


def get_current_season():
    """Return the current season based on the current month."""
    if datetime.now().month > 9:
        return datetime.now().year + 1
    return datetime.now().year


def load_and_preprocess_data(current_season):
    """Load and preprocess data for the current season."""
    data = load.load_silver_data().fillna(0.0)
    data = data[data.SEASON == current_season]
    with open("data/features.json") as json_file:
        features_dict = json.load(json_file)
    cat, num, features = features_dict["cat"], features_dict["num"], features_dict["model"]
    data_processed_features_only, _ = data_preprocess.scale_per_value_of(
        data, cat, num, data["SEASON"], min_max_scaler=False
    )
    return data_processed_features_only[features]


def append_history(data, history):
    """Append the predictions to the history."""
    today = datetime.now().date().strftime("%d-%m-%Y")
    data["DATE"] = today
    data = data[["DATE", "PLAYER", "PRED"]]
    if today in history.DATE.unique():
        logger.warning("Predictions already made for today")
    else:
        history = history.append(data, ignore_index=True)
        history.to_csv(
            conf.data.history.path,
            sep=conf.data.history.sep,
            encoding=conf.data.history.encoding,
            compression=conf.data.history.compression,
            index=False
        )


def load_model_make_predictions(max_n=50):
    """Load the trained model, make predictions and update the history."""
    model = load.load_model()
    current_season = get_current_season()
    logger.debug(f"Current season: {current_season}")

    # Load and preprocess data
    original_data = load.load_silver_data().fillna(0.0)
    original_data = original_data[original_data.SEASON == current_season]
    X = load_and_preprocess_data(current_season)
    X.to_csv(
        conf.data.model_input.path,
        sep=conf.data.model_input.sep,
        encoding=conf.data.model_input.encoding,
        compression=conf.data.model_input.compression,
        index=True
    )

    predictions = model.predict(X)
    original_data.loc[:, "PRED"] = predictions
    original_data.loc[:, "PRED_RANK"] = original_data["PRED"].rank(ascending=False)
    original_data = original_data[original_data["PRED"] > 0.0].sort_values(by="PRED", ascending=False).head(max_n)
    original_data.to_csv(
        conf.data.predictions.path,
        sep=conf.data.predictions.sep,
        encoding=conf.data.predictions.encoding,
        compression=conf.data.predictions.compression,
        index=True
    )

    try:
        history = load.load_history()
        logger.debug(f"History found - {history.DATE.nunique()} entries")
    except FileNotFoundError:
        history = pd.DataFrame(columns=["DATE", "PLAYER", "PRED"])
        logger.warning("No history found")
    append_history(original_data, history)


def make_predictions():
    """Main function to make predictions using the trained model."""
    try:
        train.make_bronze_data()
        train.make_silver_data()
        load_model_make_predictions()
    except Exception as e:
        logger.error(f"Predicting failed: {e}", exc_info=True)
