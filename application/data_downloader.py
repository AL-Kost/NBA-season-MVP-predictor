from typing import List, Optional, Any
import requests

from application import conf, logger
from application import data_scrapper as ds


def download_data(
        seasons: Optional[List[int]] = None,
        scrapper: Optional[ds.Scrapper] = None
) -> None:
    """Central function to download multiple types of basketball data."""
    if scrapper is None:
        scrapper = ds.BasketballReferenceScrapper()

    _download_with_logging(
        "player stats",
        download_player_stats,
        seasons=seasons,
        scrapper=scrapper
    )
    _download_with_logging(
        "MVP votes",
        download_mvp_votes,
        seasons=seasons,
        scrapper=scrapper
    )
    _download_with_logging(
        "team standings",
        download_team_standings,
        seasons=seasons,
        scrapper=scrapper
    )


def _download_with_logging(desc: str, func: Any, **kwargs) -> None:
    """Helper function to log the download status and handle exceptions."""
    logger.info(f"Downloading {desc}...")
    try:
        func(**kwargs)
    except Exception as e:
        logger.error(f"Downloading {desc} failed: {e}")


def download_player_stats(seasons: List[int], scrapper: ds.Scrapper) -> None:
    """Download player statistics and save to CSV."""
    data = scrapper.get_player_stats(
        subset_by_seasons=seasons,
        subset_by_stat_types=["per_game", "per_36min", "per_100poss", "advanced"]
    )
    _save_to_csv(data, conf.data.player_stats)


def download_mvp_votes(seasons: List[int], scrapper: ds.Scrapper) -> None:
    """Download MVP votes and save to CSV."""
    data = scrapper.get_mvp(subset_by_seasons=seasons)
    _save_to_csv(data, conf.data.mvp_votes)


def download_team_standings(seasons: List[int], scrapper: ds.Scrapper) -> None:
    """Download team standings and save to CSV."""
    data = scrapper.get_team_standings(subset_by_seasons=seasons)
    _save_to_csv(data, conf.data.team_standings)


def _save_to_csv(data: Any, config: Any) -> None:
    """Helper function to save data to a CSV file."""
    data.to_csv(
        config.path,
        sep=config.sep,
        encoding=config.encoding,
        compression=config.compression,
        index=True
    )


def download_data_from_url_to_file(
        url: str,
        path: str,
        stream: bool = True,
        auth: Optional[Any] = None,
        headers: Optional[Any] = None
) -> None:
    """Download data file from a given URL."""
    response = requests.get(
        url,
        allow_redirects=True,
        verify=True,
        stream=stream,
        auth=auth,
        headers=headers
    )
    with open(path, "wb") as file_writer:
        if stream:
            for chunk in response.iter_content(chunk_size=4096):
                file_writer.write(chunk)
        else:
            file_writer.write(response.content)
