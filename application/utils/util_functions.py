import yaml
from box import Box


def get_dict_from_yaml(yaml_path: str) -> Box:
    """
    Load a YAML file from a given path and return its content as a Box object.

    Args:
        yaml_path (str): The path to the YAML file to be loaded.

    Returns:
        Box: The YAML content loaded into a Box object.
    """

    with open(yaml_path, "r", encoding="utf-8") as f:
        conf_dict = yaml.safe_load(f)

    return Box(conf_dict, default_box=True, default_box_attr=None)
