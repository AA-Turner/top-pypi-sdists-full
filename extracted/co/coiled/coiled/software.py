import pathlib
import platform
import re
from logging import getLogger
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, List, Tuple, Union

from pip_requirements_parser import RequirementsFile
from yaml import safe_load

from coiled.pypi_conda_map import CONDA_TO_PYPI
from coiled.software_utils import get_index_urls
from coiled.types import CondaEnvSchema, PackageSchema, SoftwareEnvSpec

logger = getLogger(__file__)


def parse_env_yaml(env_path: Path) -> CondaEnvSchema:
    try:
        with env_path.open("rt") as env_file:
            conda_data = safe_load(env_file)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Unable to find file '{env_path}', please make sure it exists "
            "and the path is correct. If you are trying to create a "
            "software environment by specifying dependencies, you can "
            "do so by passing a list of dependencies or a dictionary. For example:\n"
            "\tcoiled.create_software_environment(\n"
            "\t    name='my-env', conda={'channels': ['conda-forge'], 'dependencies': ['coiled']}\n"
            "\t)"
        ) from None
    return {
        "channels": conda_data["channels"],
        "dependencies": conda_data["dependencies"],
    }


def parse_conda(
    conda: Union[CondaEnvSchema, str, pathlib.Path, list],
) -> Tuple[List[PackageSchema], CondaEnvSchema, List[str]]:
    if isinstance(conda, (str, pathlib.Path)):
        logger.info(f"Attempting to load environment file {conda}")
        schema = parse_env_yaml(Path(conda))
    elif isinstance(conda, list):
        schema = {"dependencies": conda}
    else:
        schema = conda
    if "channels" not in schema:
        schema["channels"] = ["conda-forge"]
    if "dependencies" not in schema:
        raise TypeError("No dependencies in conda spec")
    raw_conda: CondaEnvSchema = {
        "channels": schema["channels"],
        "dependencies": schema["dependencies"],
    }
    packages: List[PackageSchema] = []
    raw_pip: List[str] = []
    deps: List[Union[str, Dict[str, List[str]]]] = []
    for dep in raw_conda["dependencies"]:
        if isinstance(dep, dict) and "pip" in dep:
            raw_pip.extend(dep["pip"])
            continue
        deps.append(dep)
        if isinstance(dep, str):
            channel, dep = dep.split("::") if "::" in dep else (None, dep)
            match = re.match("^([a-zA-Z0-9_.-]+)(.*)$", dep)
            if not match:
                continue
            dep, specifier = match.groups()
            packages.append({
                "name": CONDA_TO_PYPI.get(dep, dep),
                "source": "conda",
                "channel": channel,
                "conda_name": dep,
                "client_version": None,
                "include": True,
                "specifier": specifier or "",
                "file": None,
            })

    raw_conda["dependencies"] = deps
    return packages, raw_conda, raw_pip


def parse_pip(pip: Union[List[str], str, Path]) -> Tuple[List[PackageSchema], List[str]]:
    if isinstance(pip, (str, Path)):
        try:
            reqs = RequirementsFile.from_file(str(pip), include_nested=True)
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Unable to find file '{pip}', please make sure it exists "
                "and the path is correct. If you are trying to create a "
                "software environment by specifying dependencies, you can "
                "do so by passing a list of dependencies. For example:\n"
                "\tcoiled.create_software_environment(\n"
                "\t    name='my-env', pip=['coiled']\n"
                "\t)"
            ) from None
    else:
        with NamedTemporaryFile("wt") as f:
            f.write("\n".join(pip))
            f.flush()
            reqs = RequirementsFile.from_file(f.name, include_nested=True)

    reqs_dict = reqs.to_dict()
    parsed_reqs: List[PackageSchema] = []
    raw_pip: List[str] = []
    for option in reqs_dict["options"]:
        raw_pip.append(option["line"])
    for req in reqs_dict["requirements"]:
        raw_line = req["requirement_line"].get("line")
        if req["is_editable"]:
            logger.warning(f"Editable requirement {raw_line!r} is not supported and will be ignored")
            continue
        if req["is_vcs_url"]:
            raw_pip.append(raw_line)
            continue
        raw_pip.append(raw_line)
        parsed_reqs.append({
            "name": req["name"],
            "source": "pip",
            "channel": None,
            "conda_name": None,
            "client_version": None,
            "include": True,
            "specifier": ",".join(req["specifier"]),
            "file": None,
        })

    return parsed_reqs, raw_pip


async def create_env_spec(
    conda: Union[CondaEnvSchema, str, Path, list, None] = None,
    pip: Union[List[str], str, Path, None] = None,
) -> SoftwareEnvSpec:
    if not conda and not pip:
        raise TypeError("Either or both of conda/pip kwargs must be specified")
    spec: SoftwareEnvSpec = {"packages": [], "raw_conda": None, "raw_pip": None}
    if conda:
        packages, raw_conda, raw_pip = parse_conda(conda)
        spec["raw_conda"] = raw_conda
        spec["raw_pip"] = raw_pip
        spec["packages"].extend(packages)
    if not conda:
        python_version = platform.python_version()
        spec["raw_conda"] = {"channels": ["conda-forge", "pkgs/main"], "dependencies": [f"python=={python_version}"]}
        spec["packages"].append({
            "name": "python",
            "source": "conda",
            "channel": None,
            "conda_name": "python",
            "client_version": None,
            "include": True,
            "specifier": f"=={python_version}",
            "file": None,
        })

    if pip:
        packages, raw_pip = parse_pip(pip)
        spec["packages"].extend(packages)
        if spec["raw_pip"] is None:
            spec["raw_pip"] = raw_pip
        else:
            spec["raw_pip"].extend(raw_pip)
        raw_index_urls = [
            re.split(r"[ =]", line.strip(), maxsplit=1)[1]
            for line in spec["raw_pip"]
            if line.startswith("--index-url") or line.startswith("--extra-index-url")
        ]
        index_urls = get_index_urls()
        if index_urls:
            raw_pip_no_index_urls = [
                line
                for line in spec["raw_pip"]
                if not line.startswith("--index-url") and not line.startswith("--extra-index-url")
            ]
            index_url, *extra_index_urls = list(set(index_urls + raw_index_urls))
            spec["raw_pip"] = [f"--index-url {index_url}"]
            for extra_index_url in extra_index_urls:
                spec["raw_pip"].append(f"--extra-index-url {extra_index_url}")
            spec["raw_pip"].extend(raw_pip_no_index_urls)

    conda_installed_pip = any(p for p in spec["packages"] if p["name"] == "pip" and p["source"] == "conda")
    has_pip_installed_package = any(p for p in spec["packages"] if p["source"] == "pip")
    if not conda_installed_pip and has_pip_installed_package:
        if not spec["raw_conda"]:
            spec["raw_conda"] = {"channels": ["conda-forge", "pkgs/main"], "dependencies": ["pip"]}
        else:
            assert "dependencies" in spec["raw_conda"]  # make pyright happy
            assert "channels" in spec["raw_conda"]
            spec["raw_conda"]["dependencies"].append("pip")
            if "pkgs/main" not in spec["raw_conda"]["channels"] and "conda-forge" not in spec["raw_conda"]["channels"]:
                spec["raw_conda"]["channels"].append("pkgs/main")
        spec["packages"].append({
            "name": "pip",
            "source": "conda",
            "channel": None,
            "conda_name": "pip",
            "client_version": None,
            "include": True,
            "specifier": "",
            "file": None,
        })
    return spec
