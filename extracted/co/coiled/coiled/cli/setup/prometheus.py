import os
import re
from typing import Optional

import click

import coiled

from ..utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option(
    "--account",
    "--workspace",
    default=None,
    help="Coiled workspace (uses default workspace if not specified)."
    " Note: --account is deprecated, please use --workspace instead.",
)
@click.option("--dir", default="datasources")
@click.option(
    "--export",
    default="yaml",
    type=click.Choice(["text", "yaml"]),
)
def get_prometheus_read_creds(account: Optional[str], dir: Optional[str], export: str):
    with coiled.Cloud() as cloud:
        account = account or cloud.default_workspace
        route = f"/api/v2/user/account/{account}/prometheus-read-credentials"
        read_creds = cloud._sync_request(route, json_result=True)

    if export == "yaml":
        if dir:
            os.makedirs(dir, exist_ok=True)

        for creds in read_creds:
            if creds["sigv4_key"]:
                datasource_file(creds, dir)
    else:
        for creds in read_creds:
            print_creds(creds)


def print_creds(creds):
    output = f"""
name:\t{creds["name"]}
url:\t{creds["endpoint"]}
region:\t{creds["region"]}
auth:\t{creds["auth_type"]}
key:\t{creds["sigv4_key"]}
secret:\t{creds["sigv4_secret"]}"""
    print(output)


def datasource_file(creds, dir):
    datasource_name = datasource_name_format(creds["name"])
    yaml_string = f"""apiVersion: 1

datasources:
  - name: {datasource_name}
    type: prometheus
    access: proxy
    url: {creds["endpoint"]}
    jsonData:
      timeInterval: 5s
      httpMethod: POST
      prometheusType: Prometheus
      sigV4Auth: true
      sigV4AuthType: keys
      sigV4Region: {creds["region"]}
    secureJsonData:
      sigV4AccessKey: {creds["sigv4_key"]}
      sigV4SecretKey: {creds["sigv4_secret"]}
"""
    filename = re.sub(r"[^\w]+", "-", creds["name"])
    filename = f"{filename}.yaml"

    if dir:
        filename = os.path.join(dir, filename)

    with open(filename, "w") as f:
        f.write(yaml_string)
    print(f"saved yaml as {filename}")


def datasource_name_format(storage_name):
    return storage_name if storage_name and storage_name != "default" else "Prometheus"
