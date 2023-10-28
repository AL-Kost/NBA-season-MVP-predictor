import argparse
import sys

import streamlit.cli

from application import data_downloader
from application.model import train, predict, explain


def download_data(args):
    """Download data for the specified seasons."""
    data_downloader.download_data(args.seasons)


def train_model():
    """Train a model on downloaded data."""
    train.train_model()


def make_predictions():
    """Make predictions with the trained model."""
    predict.make_predictions()


def explain_model():
    """Provide explanations for model decisions."""
    explain.explain_model()


def run_webapp():
    """Initialize and run the web application."""
    sys.argv = ["0", "run", "./streamlit_app.py"]
    streamlit.cli.main()


def get_parser():
    """Set up the CLI argument parser."""

    parser = argparse.ArgumentParser(description="CLI for data operations and model training/predictions.")

    subparsers = parser.add_subparsers(dest="command")

    # Web application command
    subparsers.add_parser("web", help="Run the web application showing predictions")

    # Data download command
    download_parser = subparsers.add_parser("download", help="Download data")
    download_parser.add_argument(
        "--seasons",
        required=False,
        nargs="+",
        type=int,
        help="Seasons to download data for"
    )

    # Model-related commands
    subparsers.add_parser("train", help="Train a model on downloaded data")
    subparsers.add_parser("predict", help="Make predictions with the trained model")
    subparsers.add_parser("explain", help="Explain the predictions made by the model")

    return parser


def run(args=None):
    """Main CLI entry point."""

    parser = get_parser()
    parsed_args = parser.parse_args(args)

    commands = {
        "web": run_webapp,
        "download": download_data,
        "train": train_model,
        "predict": make_predictions,
        "explain": explain_model
    }

    if parsed_args.command in commands:
        commands[parsed_args.command](parsed_args)


if __name__ == "__main__":
    run()
