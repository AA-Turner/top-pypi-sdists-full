"""Dev utilities for constructing models from CSV files"""

import re
import yaml
import requests
import pandas as pd
from pathlib import Path


def to_class_name_underscored(name: str) -> str:
    """Convert a name to a class name by capitalizing and removing non-alphanumeric characters.

    Always prefixes the string with an underscore."""
    name = str(name)
    return "_" + re.sub(r"\W+", "_", name.title()).replace(" ", "")


def to_class_name(name: str) -> str:
    """Convert a name to a valid class name by capitalizing and removing non-alphanumeric characters.

    Replace any non alphanumeric characters at the beginning of the string with a single _."""
    name = str(name)
    return re.sub(r"\W|^(?=\d)", "_", name.title()).replace(" ", "")


def update_harp_types(
    url: str = "https://raw.githubusercontent.com/harp-tech/whoami/refs/heads/main/whoami.yml",
):
    """Pull the latest harp types from the whoami.yml file and save them to a CSV file."""
    response = requests.get(url, allow_redirects=True, timeout=5)
    content = response.content.decode("utf-8")
    content = yaml.safe_load(content)

    devices = content["devices"]
    data = [{"name": device["name"], "whoami": str(whoami)} for whoami, device in devices.items()]

    df = pd.DataFrame(data)

    current_dir = Path(__file__).parent.resolve()
    df.to_csv(current_dir / "models/harp_types.csv", index=False)
