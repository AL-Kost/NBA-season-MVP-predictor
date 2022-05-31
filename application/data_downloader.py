from typing import List
import requests
from application import conf, logger
from application import data_scrapper


def download_data(
    seasons: List[int] = None,
    scrapper: data_scrapper.Scrapper = data_scrapper.BasketballReferenceScrapper()
):
    logger.info("Downloading player stats...")
    try:
        download_player_stats(seasons=seasons, scrapper=scrapper)
    except Exception as e:
        logger.error(f"Downloading player stats failed : {e}")
    logger.info("Downloading MVP votes...")
    try:
        download_mvp_votes(seasons=seasons, scrapper=scrapper)
    except Exception as e:
        logger.error(f"Downloading MVP votes failed : {e}")
    logger.info("Downloading team standings...")
    try:
        download_team_standings(seasons=seasons, scrapper=scrapper)
    except Exception as e:
        logger.error(f"Downloading team standings failed : {e}")


def download_player_stats(seasons: List[int], scrapper: data_scrapper.Scrapper):
    # We don't retrieve totals stats since we want to be able to predict at any moment in the season, no matter what
    data = scrapper.get_player_stats(
        subset_by_seasons=seasons,
        subset_by_stat_types=["per_game", "per_36min", "per_100poss", "advanced"]
    )
    data.to_csv(
        conf.data.player_stats.path,
        sep=conf.data.player_stats.sep,
        encoding=conf.data.player_stats.encoding,
        compression=conf.data.player_stats.compression,
        index=True
    )


def download_mvp_votes(seasons: List[int], scrapper: data_scrapper.Scrapper):
    data = scrapper.get_mvp(
        subset_by_seasons=seasons
    )
    data.to_csv(
        conf.data.mvp_votes.path,
        sep=conf.data.mvp_votes.sep,
        encoding=conf.data.mvp_votes.encoding,
        compression=conf.data.mvp_votes.compression,
        index=True
    )


def download_team_standings(seasons: List[int], scrapper: data_scrapper.Scrapper):
    data = scrapper.get_team_standings(
        subset_by_seasons=seasons
    )
    data.to_csv(
        conf.data.team_standings.path,
        sep=conf.data.team_standings.sep,
        encoding=conf.data.team_standings.encoding,
        compression=conf.data.team_standings.compression,
        index=True
    )


def download_data_from_url_to_file(
    url: str, path: str, stream: bool = True, auth=None, headers=None
):
    """Download data file from URL.

    Args:
        url (str): URL of file to download
        path (str): Path to a local file
        stream (bool, optional): Whether data should be streamed (recommended for super large files). Default is True
    """
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
