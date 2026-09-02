from typing import Optional

from benedict import benedict

from dealcloud_sdk.models.factory_models import DealCloudFactoryArgs


def dc_from_json_config(
    json_file_path: str, json_path_to_credentials: Optional[str] = None
) -> DealCloudFactoryArgs:
    """
    Create a DealCloud object from a JSON Config file
    Args:
        json_file_path (str): the path to the JSON config file
        json_path_to_credentials (Optional[str]): a JSONPath string

    Returns:
        DealCloudFactoryArgs: the DealCloud class arguments.
    """
    dc_config = benedict(json_file_path, format="json")

    if json_path_to_credentials:
        dc_config = dc_config.find([json_path_to_credentials])

    dc = DealCloudFactoryArgs(**dc_config)

    return dc
