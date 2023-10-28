import json
from datetime import datetime
import pandas as pd
from application import conf, logger, data_preprocess
from application.utils import load
from application.model import train


def get_current_season():
    """Return the current season based on the month."""
    now = datetime.now()
    return now.year + 1 if now.month > 9 else now.year


def load_features_from_json():
    """Load and return categories, numbers, and features from the JSON file."""
    with open("data/features.json") as json_file:
        features_dict = json.load(json_file)
    return features_dict["cat"], features_dict["num"], features_dict["model"]


def save_to_csv(df, config):
    """Utility function to save dataframe to a CSV."""
    df.to_csv(
        config.path,
        sep=config.sep,
        encoding=config.encoding,
        compression=config.compression,
        index=True
    )


def process_and_save_predictions(data, model, features, max_n):
    """Process and save the predictions."""
    X = data[features]
    predictions = model.predict(X)
    data.loc[:, "PRED"] = predictions
    data.loc[:, "PRED_RANK"] = data["PRED"].rank(ascending=False)
    data = data.sort_values(by="PRED", ascending=False).head(max_n)
    data = data[data["PRED"] > 0.0]
    save_to_csv(data, conf.data.predictions)


def update_prediction_history(data):
    """Update the prediction history CSV with the latest predictions."""
    try:
        history = load.load_history()
        logger.debug(f"History found - {history.DATE.nunique()} entries")
    except FileNotFoundError:
        history = pd.DataFrame(columns=["DATE", "PLAYER", "PRED"])
        logger.warning("No history found")

    today = datetime.now().date().strftime("%d-%m-%Y")
    data["DATE"] = today
    data = data[["DATE", "PLAYER", "PRED"]]

    if today not in history.DATE.unique():
        history = history.append(data, ignore_index=True)
        history.to_csv(
            conf.data.history.path,
            sep=conf.data.history.sep,
            encoding=conf.data.history.encoding,
            compression=conf.data.history.compression,
            index=False
        )
    else:
        logger.warning("Predictions already made for today")


def load_model_and_make_predictions(max_n=50):
    """Make predictions and save them."""
    model = load.load_model()
    data = load.load_silver_data().fillna(0.0)
    data = data[data.SEASON == get_current_season()]
    cat, num, features = load_features_from_json()
    min_max_scaling = False
    data_processed, _ = data_preprocess.scale_per_value_of(
        data, cat, num, data["SEASON"], min_max_scaler=min_max_scaling
    )
    process_and_save_predictions(data_processed, model, features, max_n)
    update_prediction_history(data_processed)


def make_predictions():
    """Main function to initiate the prediction process."""
    try:
        train.make_bronze_data()
        train.make_silver_data()
        load_model_and_make_predictions()
    except Exception as e:
        logger.error(f"Predicting failed: {e}", exc_info=True)
