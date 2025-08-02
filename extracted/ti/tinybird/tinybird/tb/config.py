import json
from os import environ, getcwd
from pathlib import Path
from typing import Any, Dict, Optional

import click

from tinybird.tb import __cli__
from tinybird.tb.modules.feedback_manager import FeedbackManager

try:
    from tinybird.tb.__cli__ import __revision__
except Exception:
    __revision__ = ""

DEFAULT_LOCALHOST = "http://localhost:8001"
CURRENT_VERSION = f"{__cli__.__version__}"
VERSION = f"{__cli__.__version__} (rev {__revision__})"
DEFAULT_UI_HOST = "https://cloud.tinybird.co"
DEFAULT_API_HOST = "https://api.europe-west2.gcp.tinybird.co"
SUPPORTED_CONNECTORS = ["bigquery", "snowflake"]
PROJECT_PATHS = ["datasources", "datasources/fixtures", "endpoints", "pipes", "tests", "scripts", "deploy"]
DEPRECATED_PROJECT_PATHS = ["endpoints"]
MIN_WORKSPACE_ID_LENGTH = 36

CLOUD_HOSTS = {
    "https://api.tinybird.co": "https://cloud.tinybird.co/gcp/europe-west3",
    "https://api.us-east.tinybird.co": "https://cloud.tinybird.co/gcp/us-east4",
    "https://api.us-east.aws.tinybird.co": "https://cloud.tinybird.co/aws/us-east-1",
    "https://api.us-west-2.aws.tinybird.co": "https://cloud.tinybird.co/aws/us-west-2",
    "https://api.eu-central-1.aws.tinybird.co": "https://cloud.tinybird.co/aws/eu-central-1",
    "https://api.eu-west-1.aws.tinybird.co": "https://cloud.tinybird.co/aws/eu-west-1",
    "https://api.europe-west2.gcp.tinybird.co": "https://cloud.tinybird.co/gcp/europe-west2",
    "https://api.ap-east.aws.tinybird.co": "https://cloud.tinybird.co/aws/ap-east",
    "https://ui.tinybird.co": "https://cloud.tinybird.co/gcp/europe-west3",
    "https://ui.us-east.tinybird.co": "https://cloud.tinybird.co/gcp/us-east4",
    "https://ui.us-east.aws.tinybird.co": "https://cloud.tinybird.co/aws/us-east-1",
    "https://ui.us-west-2.aws.tinybird.co": "https://cloud.tinybird.co/aws/us-west-2",
    "https://ui.eu-central-1.aws.tinybird.co": "https://cloud.tinybird.co/aws/eu-central-1",
    "https://ui.europe-west2.gcp.tinybird.co": "https://cloud.tinybird.co/gcp/europe-west2",
}


def get_config(
    host: Optional[str], token: Optional[str], semver: Optional[str] = None, config_file: Optional[str] = None
) -> Dict[str, Any]:
    if host:
        host = host.rstrip("/")

    config = {}
    try:
        with open(config_file or Path(getcwd()) / ".tinyb") as file:
            res = file.read()
            config = json.loads(res)
    except OSError:
        pass
    except json.decoder.JSONDecodeError:
        click.echo(FeedbackManager.error_load_file_config(config_file=config_file))
        return config

    config["token_passed"] = token
    config["token"] = token or config.get("token", None)
    config["semver"] = semver or config.get("semver", None)
    config["host"] = host or config.get("host", DEFAULT_API_HOST)
    config["workspaces"] = config.get("workspaces", [])
    config["cwd"] = config.get("cwd", getcwd())
    config["user_email"] = config.get("user_email", None)
    config["user_id"] = config.get("user_id", None)
    config["workspace_id"] = config.get("id", None)
    config["workspace_name"] = config.get("name", None)
    return config


def write_config(config: Dict[str, Any], dest_file: str = ".tinyb") -> None:
    config_file = Path(getcwd()) / dest_file
    with open(config_file, "w") as file:
        file.write(json.dumps(config, indent=4, sort_keys=True))


def get_display_cloud_host(api_host: str) -> str:
    is_local = "localhost" in api_host
    if is_local:
        port = api_host.split(":")[-1]
        return f"http://cloud.tinybird.co/local/{port}"
    return CLOUD_HOSTS.get(api_host, api_host)


class FeatureFlags:
    @classmethod
    def ignore_sql_errors(cls) -> bool:  # Context: #1155
        return "TB_IGNORE_SQL_ERRORS" in environ

    @classmethod
    def is_localhost(cls) -> bool:
        return "SET_LOCALHOST" in environ

    @classmethod
    def enable_snowflake_connector_command(cls) -> bool:
        return "ENABLE_SNOWFLAKE_CONNECTOR_COMMAND" in environ
