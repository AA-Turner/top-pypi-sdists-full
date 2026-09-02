from typing import Optional

from benedict import benedict

from dealcloud_sdk.models.factory_models import DealCloudFactoryArgs


def dc_from_yaml_config(
    yaml_file_path: str, yaml_path_to_credentials: Optional[str] = None
) -> DealCloudFactoryArgs:
    """
    Create a DealCloud object from a YAML Config file
    Args:
        yaml_file_path (str): the path to the yaml config file
        yaml_path_to_credentials (str): YAML path to credentials in the document

    Returns:
        DealCloudFactoryArgs: the DealCloud class arguments.
    """

    dc_config = benedict(yaml_file_path, format="yaml")

    if yaml_path_to_credentials:
        dc_config = dc_config.find([yaml_path_to_credentials])

    dc = DealCloudFactoryArgs(**dc_config)

    return dc
