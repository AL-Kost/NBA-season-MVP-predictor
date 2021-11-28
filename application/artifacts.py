from datetime import datetime
import os
import requests
from application import conf, logger


def get_artifacts():
    """Gets the artifacts from the GitHub project.

    Returns:
        dict: Artifacts dictionary
    """
    github_repo = conf.web.github_repo
    url = f"https://api.github.com/repos/{github_repo}/actions/artifacts?per_page=100"
    artifacts = load_json_from_url(url)
    return artifacts


def load_json_from_url(url: str):
    """Loads a JSON file into memory from URL

    Args:
        url (str): URL of the file

    Returns:
         dict: Dictionary from the JSON file
    """
    response = requests.get(url)
    if response.status_code == 403:
        raise Exception(f"Error 403 when requesting {url} : {response.content}")
    return response.json()


def get_github_auth():
    """Gets an authentication tuple for the GitHub API.

    Returns:
        (str, str): Tuple (user, token) to use when making API calls
    """
    username = os.environ["GITHUB_USERNAME"]
    token = os.environ["GITHUB_TOKEN"]
    return username, token


def get_last_artifact(artifact_name: str):
    """Gets the last available artifact.

    Params:
        artifact_name: Name of the searched artifact

    Returns:
        dict: Last available artifact (date:url)
    """
    artifacts = get_artifacts()
    num_artifacts = artifacts.get("total_count")
    logger.debug(f"{num_artifacts} artifacts available on the project")
    if num_artifacts > 100:
        logger.warning(
            "Some artifacts were not retrieved due to GitHub artifact pagination"
        )
    artifacts = [
        a
        for a in artifacts.get("artifacts")
        if a.get("name") == artifact_name and a.get("expired") == False
    ]
    logger.debug(f"{len(artifacts)} artifacts with the name {artifact_name}")
    results = dict()
    for artifact in artifacts:
        artifact_datetime = artifact.get("created_at")
        artifact_url = artifact.get("archive_download_url")
        artifact_datetime = datetime.strptime(artifact_datetime, "%Y-%m-%dT%H:%M:%SZ")
        results[artifact_datetime] = artifact_url
    last_result = sorted(results.items(), reverse=True)[0]
    logger.debug(f"Last available artifact: {last_result}")
    return last_result
