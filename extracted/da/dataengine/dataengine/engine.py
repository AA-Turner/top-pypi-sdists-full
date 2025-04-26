"""
This is the main module for Data Engine.
"""
import os
import re
import copy
import yaml
from typing import List, Dict, Union, Any
import datetime
import logging
from . import assets, database, dataset, query


def generate_query_log_message(
    query_name: str, 
    query_object: query.Query, 
    query: str, 
    dependencies: dict
) -> str:
    """
    Generate a neatly formatted log message for a query.

    Args:
        query_name (str): The name of the query.
        query_object (query.Query): The query object instance.
        query (str): The query string.
        dependencies (dict): A dictionary mapping dependencies.

    Returns:
        A formatted log message.
    """
    intro = [f"Beginning execution of {query_name}\n"]
    dependency_list = [
        f"Dependencies:\n" +
        "\n".join(
            f"    {key}:\n        {value}"
            for key, value in dependencies.items())]
    intermittent_tables = query_object.intermittent_tables
    if intermittent_tables:
        it_list = [
            "Intermittent Tables:\n" +
            "\n".join(
                f"    {itable['table_name']}:\n" +
                "\n".join(f"        {line}" for line in itable["sql"].splitlines())
                for itable in intermittent_tables)]
    else:
        it_list = []
    query_list = [
        "Query:\n" +
        "\n".join(f"    {line}" for line in query.splitlines())]

    return "\n".join(intro + dependency_list + it_list + query_list) + "\n"


def load_asset_config_files(
        asset_config_path_list: List[str]
    ) -> Dict[str, Union[str, int, float, bool, list, dict]]:
    """
    Load asset configuration files from a list of file paths and merge them
    into a single dictionary.
    
    Args:
        asset_config_path_list (List[str]):
            A list of file paths to asset configuration files in YAML format.
    
    Returns:
        Dict[str, Union[str, int, float, bool, list, dict]]:
            A dictionary containing the merged asset configurations.
        
    Example:
        >>> load_asset_config_files(
        >>>    ["path/to/config1.yaml", "path/to/config2.yaml"])
        {'key1': 'value1', 'key2': 'value2'}
    """
    assets_config = {}
    # Iterate over input asset configuration paths
    for path in asset_config_path_list:
        # Pull dirname from asset config file
        dirname = os.path.dirname(os.path.realpath(path))
        basename = os.path.basename(path)
        # Use a context manager for file I/O
        with open(path, "r") as f:
            config = yaml.safe_load(f)
            # Add the file dirname for each and add basename if the asset is
            # a base_query
            current_asset_config = {} 
            for key, values in config.items():
                asset_name = key
                if (
                    ("asset_type" in values) and
                    values["asset_type"] == "base_query"
                ):
                    asset_name = f"{basename.split('.yaml')[0]}.{key}"
                # Fill values
                current_asset_config[asset_name] = {
                    "dirname": dirname, "basename": basename,
                    **values}
            # Update asset config with new assets
            assets_config.update(current_asset_config)

    return assets_config


def load_assets(
        asset_config: Dict[str, Dict[str, Union[str, int, float, bool]]]
    ) -> Dict[str, Dict[str, Any]]:
    """
    Load assets from a configuration dictionary and organize them into
    different types.

    Args:
        asset_config (Dict[str, Dict[str, Union[str, int, float, bool]]]):
            A dictionary containing asset names as keys and another dictionary
            as values. The inner dictionary contains asset parameters including
            the asset type ('database', 'bucket', 'base_dataset') and other
            configurations.

    Returns:
        Dict[str, Dict[str, Any]]:
            A dictionary containing loaded assets organized into 'buckets',
            'base_datasets', and 'databases'.
    """
    # Initialize asset map
    asset_map = {
        "buckets": {}, "base_datasets": {}, "databases": {},
        "base_queries": {}}
    # Iterate over each asset and load it accordingly
    for asset_name, parameters in asset_config.items():
        # Assume asset is base dataset
        # TODO: Replace this when base datasets are updated
        if "asset_type" not in parameters:
            asset_type = "base_dataset"
        else:
            asset_type = parameters["asset_type"]
        config = {"asset_name": asset_name}
        # Iterate over config parameters and organize them accordingly
        for key, value in parameters.items():
            if key in ("asset_type", "basename"):
                continue
            # Determine whether config parameter is an environment variable
            # and if it is pull the value from the environment
            match = re.compile(r"\{\{(.+?)\}\}").fullmatch(str(value))
            if match:
                value = os.getenv(match.group(1))
            # If the input value is a port cast it to an integer
            if key == "port":
                if re.fullmatch(r"[0-9]+", str(value)):
                    value = int(value)
                else:
                    value = 0
            # If the value is still None cast it to an empty string
            if value is None:
                value = ""
            # Setup sql info properly if applicable
            if asset_type == "base_query" and key == "sql_info":
                sql_info = copy.deepcopy(value)
                # Convert to a list if it isn't one
                if not isinstance(sql_info, list):
                    sql_info = [sql_info]
                # Iterate over the info values and replace the filenames with
                # the full path
                for i, info_value in enumerate(sql_info):
                    primary_filepath_list = info_value["filename"]
                    if isinstance(primary_filepath_list, str):
                        primary_filepath_list = [primary_filepath_list]
                    sql_info[i]["filename"] = [
                        os.path.realpath(
                            os.path.join(parameters["dirname"], filepath)
                        ) for filepath in primary_filepath_list]
                    if "intermittent_tables" in info_value:
                        for j, list_value in enumerate(
                            info_value["intermittent_tables"]
                        ):
                            sql_info[i]["intermittent_tables"][j][
                                "filename"] = os.path.realpath(os.path.join(
                                    parameters["dirname"], list_value["filename"]))
                # Reset sql info value
                value = sql_info
            # Set the final config value
            config[key] = value
        # Load asset
        if asset_type == "database":
            asset_map["databases"][asset_name] = database.DatabaseSchema().load(config)
        elif asset_type == "bucket":
            asset_map["buckets"][asset_name] = assets.BucketSchema().load(config)
        elif asset_type == "base_dataset":
            asset_map["base_datasets"][asset_name] = assets.BaseDatasetSchema().load(
                config)
        elif asset_type == "base_query":
            asset_map["base_queries"][asset_name] = query.BaseQuerySchema().load(config)
    # Setup linkage between buckets and datasets
    # TODO: Setup bucket / base_dataset linkage here

    return asset_map


class Engine:
    """
    This class will function as the primary class for Data Engine.
    """
    def __init__(
            self,
            asset_config_path_list: list
    ):
        # Load assets
        self.assets = load_assets(
            load_asset_config_files(asset_config_path_list))

    def load_dataset(
            self, spark, base_dataset, dt=datetime.datetime.utcnow(),
            hour="*", bucket=None, format_args={}, time_delta={},
            timestamp_conversion=[], dt_delta={}, exclude_hours=[],
            file_path=None, rename={}, check_path=True, **kwargs):
        """
        This method will load a Dataset object from the available base
        datasets in this engine.
        """
        dataset_obj = None
        load_success = False
        if base_dataset in self.assets["base_datasets"]:
            # TODO: Add file path override here
            try:
                dataset_obj = dataset.Dataset.from_base_dataset(
                    self.assets["base_datasets"][base_dataset], spark=spark,
                    dt=dt, hour=str(hour), bucket=bucket,
                    format_args=format_args, time_delta=time_delta,
                    dt_delta=dt_delta, rename=rename,
                    exclude_hours=exclude_hours, check_path=check_path,
                    timestamp_conversion=timestamp_conversion)
                load_success = True
            except Exception as e:
                logging.error(f"Error loading dataset {base_dataset}:\n{e}\n")
        else:
            logging.error(f"Invalid base dataset provided: {base_dataset}\n")

        return dataset_obj, load_success
    
    def load_query(
            self, base_query, dt=datetime.datetime.utcnow(),
            hour="*", **kwargs
        ):
        """
        This method will load a query provided it's part of the available
        options.
        """
        query_object = None
        load_success = False
        if base_query in self.assets["base_queries"]:
            try:
                query_object = query.Query.from_base_query(
                    self.assets["base_queries"][base_query],
                    dt=dt, hour=hour, **kwargs)
                load_success = True
            except Exception as e:
                logging.error(f"Error loading query {base_query}:\n{e}\n")
        else:
            logging.error(f"Invalid base query provided: {base_query}\n")
        
        return query_object, load_success
