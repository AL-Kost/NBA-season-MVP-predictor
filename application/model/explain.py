import pandas as pd
import shap

from application import conf, logger
from application.utils import load


def load_data_and_preprocess():
    """Load necessary data and preprocess for SHAP explanation."""
    model_input = load.load_model_input()
    predictions = load.load_predictions().sort_values(by="PRED_RANK", ascending=True)
    return model_input, predictions


def get_sample_and_population(model_input, predictions, sample_size=10, population_size=100):
    """Extract sample and population from model input and predictions."""
    player_season_team_list = predictions.index.to_list()

    logger.debug(f"SHAP values will be computed for : {sample_size} top players")
    sample = model_input[model_input.index.isin(player_season_team_list[:sample_size])]

    logger.debug(f"Number of players in predictions : {len(player_season_team_list)}")
    # New method : Sample players randomly.
    population = model_input.sample(population_size)
    logger.debug(f"Population size for SHAP : {population_size}")

    return sample, population


def compute_shap_values(model, sample, population):
    """Compute SHAP values for the provided sample."""
    explainer = shap.Explainer(model.predict, population, algorithm="auto")
    return explainer(sample)


def save_shap_values(shap_values, sample, predictions):
    """Save SHAP values to a CSV file."""
    sample["player"] = sample.index
    sample["player"] = sample["player"].map(predictions["PLAYER"])
    sample = sample.reset_index(drop=True)

    shap_df = pd.DataFrame(shap_values.values, columns=shap_values.feature_names, index=sample.player)
    shap_df.to_csv(
        conf.data.shap_values.path,
        sep=conf.data.shap_values.sep,
        encoding=conf.data.shap_values.encoding,
        compression=conf.data.shap_values.compression,
        index=True
    )


def explain_model():
    """Explain model predictions using SHAP values."""
    try:
        model = load.load_model()
        model_input, predictions = load_data_and_preprocess()
        sample, population = get_sample_and_population(model_input, predictions)
        shap_values = compute_shap_values(model, sample, population)
        save_shap_values(shap_values, sample, predictions)
    except Exception as e:
        logger.error(f"Error explaining the model: {e}")
        raise e


if __name__ == "__main__":
    explain_model()
