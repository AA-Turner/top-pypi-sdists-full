# Until https://github.com/astral-sh/uv/issues/6794

import json
import subprocess
import tomllib
from collections import defaultdict
from pathlib import Path

from packaging.requirements import Requirement

pyproject = tomllib.loads((Path(__file__).parent.parent / "pyproject.toml").read_text())

dependencies: dict[str, list[str]] = defaultdict(list)
dependencies["main"].extend(Requirement(dep).name for dep in pyproject.get("project", {}).get("dependencies", []))

for group, group_deps in pyproject.get("dependency-groups", {}).items():
    dependencies[group].extend(Requirement(dep).name for dep in group_deps)

outdated_packages = json.loads(subprocess.check_output(["uv", "pip", "list", "--outdated", "--format=json"], text=True))
latest_by_name = {pkg["name"]: pkg["latest_version"] for pkg in outdated_packages}

for group, names in dependencies.items():
    for name in names:
        if latest_version := latest_by_name.get(name):
            print(f"Updating {name} in group '{group}' to version {latest_version}...")
            group_arg = ["--group", group] if group != "main" else []
            subprocess.run(["uv", "add", *group_arg, f"{name}=={latest_version}"], check=False)

if outdated_packages:
    subprocess.run(["uv", "sync"], check=True)
    subprocess.run(["uv", "lock", "--upgrade"], check=True)
