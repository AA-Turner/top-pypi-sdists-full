from typing import Any

import yaml
from airflow.models.connection import Connection


def _get_connections(yaml_dict: dict[str, Any]) -> dict[str, Connection]:
    connections = {}
    for i in yaml_dict["connections"]:
        parsed_yaml_dict = {
            (k.replace("conn_", "") if k not in ["conn_id", "conn_type"] else k): v for k, v in i.items()
        }
        connections[parsed_yaml_dict["conn_id"]] = Connection(**parsed_yaml_dict)
    return connections


def _get_variables(yaml_dict: dict[str, Any]) -> dict[str, str]:
    variables = {}
    for i in yaml_dict["variables"]:
        variables[i["variable_name"]] = i["variable_value"]
    return variables


def parse_settings_file(
    file_path: str,
) -> tuple[dict[str, Connection], dict[str, str]]:
    """
    This function parses an astronomer-style settings.yaml file and returns created connections and variables.

    Files are expected in this format:

    ```
    airflow:
     connections:
       - conn_id:
         conn_type:
         conn_host:
         conn_schema:
         conn_login:
         conn_password:
         conn_port:
         conn_extra:
           extra__field_1:
           extra__field_2:
     pools:
       - pool_name:
         pool_slot:
         pool_description:
     variables:
       - variable_name:
         variable_value:
    ```

    :param file_path: file path of airflow_settings.yaml file
    :return: Connections and Variables that can be pushed into a run_dag function.
    """
    with open(file_path) as file_stream:
        parsed_yaml = yaml.safe_load(file_stream)["airflow"]
        return _get_connections(parsed_yaml), _get_variables(parsed_yaml)
