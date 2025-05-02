import calendar
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

import yaml
from dynamic_yaml import dump as ddump
from dynamic_yaml import load as dload

from .exceptions import NotSupported

today = datetime.today()
RUNTIME_DEFAULTS = {
    "FIRST_DAY_MONTH": today.replace(day=1).day,
    "LAST_DAY_MONTH": calendar.monthrange(today.year, today.month)[1],
    "YEAR": today.year,
    "MONTH": today.month,
    "DAY": today.day,
}

OUTPUT_FOLDER = f"output-meta/{today.day}-{today.month}-{today.year}"

refresh = lambda data: yaml.safe_load(ddump(dload(ddump(data))))


def load_yaml(name: str, dynamic=True) -> dict:
    """Loads yaml and injects dynamic runtime if dynamic is true

    param :name, str: File to load
    param :dyanmic, bool, true: Use dynamic replacement
    Returns :dict: Dictionary with the dynamic variables updated
    """
    with open(name) as f:
        config = yaml.safe_load(f)

    if dynamic:
        config.update(RUNTIME_DEFAULTS)
        config = refresh(config)
    return config


def file_information(file_name: str, output_location: str) -> None:
    """Saves file metadata

    param :file_name, str: Output location of target file
    param :output-location, str: Output location
    """
    fn, ft = os.path.splitext(os.path.basename(file_name))
    exists = os.path.exists(file_name)
    information = {
        "Size": os.path.getsize(file_name) if exists else None,
        "Date": os.path.getmtime(file_name) if exists else None,
        "Type": str(subprocess.check_output(["file", "-i", "-s", file_name]))
        if exists
        else None,
        "Columns": None,
        "Count": None,
    }

    if ft == ".parquet" and exists:
        raise NotImplementedError("HDF5 isn't implemented yet")
    elif ft == ".csv" and exists:
        information["Count"] = str(subprocess.check_output(["wc", "-l", file_name]))
        information["Columns"] = str(
            subprocess.check_output(["head", "-n1", file_name])
        )
    elif ft == ".hdf5" and exists:
        raise NotImplementedError("HDF5 isn't implemented yet")

    print("saving metadata...")
    out = Path(f"{output_location}/{OUTPUT_FOLDER}/{fn}{ft}.info")
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w") as f:
        json.dump(information, f, indent=4)
