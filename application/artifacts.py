import os
import requests
from datetime import datetime
from application import conf, logger

GITHUB_DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
MAX_ARTIFACTS_PER_PAGE = 100


def get_artifacts() -> dict:
    """
    Fetch artifacts from the specified GitHub repository.

    Returns:
        dict: Artifacts information.
    """
    github_repo = conf.web.github_repo
    url = f"https://api.github.com/repos/{github_repo}/actions/artifacts?per_page={MAX_ARTIFACTS_PER_PAGE}"
    auth = get_github_auth()
    return _load_json_from_url(url, auth)


def _load_json_from_url(url: str, auth=None) -> dict:
    """
    Fetch a JSON object from a given URL.

    Args:
        url: Target URL.
        auth: Authentication tuple.

    Returns:
        dict: Parsed JSON content.

    Raises:
        Exception: If the request returns a 403 Forbidden status.
    """
    response = requests.get(url, auth=auth)
    response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

    if response.status_code == 403:
        raise Exception(f"Error 403 when requesting {url} : {response.content}")
    return response.json()


def get_github_auth() -> tuple:
    """
    Retrieve GitHub authentication details from the environment.

    Returns:
        tuple: (username, token).
    """
    return os.environ["GITHUB_USERNAME"], os.environ["GITHUB_TOKEN"]


def get_last_artifact(artifact_name: str) -> dict:
    """
    Retrieve the most recent artifact matching the provided name.

    Args:
        artifact_name: Name of the artifact.

    Returns:
        dict: Dictionary containing the date and URL of the last available artifact.

    Raises:
        IOError: If no matching artifact is found.
    """
    artifacts = get_artifacts()
    _log_artifacts_info(artifacts, artifact_name)
    relevant_artifacts = _filter_relevant_artifacts(artifacts, artifact_name)

    last_result = _find_last_artifact(relevant_artifacts)
    if not last_result:
        raise IOError(f"No artifact found with name {artifact_name}")

    logger.debug(f"Last available artifact: {last_result}")
    return last_result


def _log_artifacts_info(artifacts: dict, artifact_name: str):
    """Log information about the fetched artifacts."""
    num_artifacts = artifacts.get("total_count", 0)
    logger.debug(f"{num_artifacts} artifacts available on the project")

    if num_artifacts > MAX_ARTIFACTS_PER_PAGE:
        logger.warning("Some artifacts were not retrieved due to GitHub artifact pagination")


def _filter_relevant_artifacts(artifacts: dict, artifact_name: str) -> list:
    """Filter out artifacts based on given criteria."""
    return [
        artifact
        for artifact in artifacts.get("artifacts", [])
        if artifact.get("name") == artifact_name and not artifact.get("expired")
    ]


def _find_last_artifact(artifacts: list) -> dict:
    """Find the most recent artifact from the list."""
    results = {
        datetime.strptime(artifact.get("created_at"), GITHUB_DATE_FORMAT): artifact.get("archive_download_url")
        for artifact in artifacts
    }

    return sorted(results.items(), key=lambda x: x[0], reverse=True)[0] if results else None
