import json
import os
import shutil
import subprocess
from datetime import datetime

import click

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"], "show_default": True}


def fix_path_for_upload(local_path, specified_root=None):
    cwd = os.path.abspath(os.path.curdir)
    base = os.path.basename(local_path)
    is_under_cwd = os.path.commonpath((os.path.abspath(local_path), cwd)) == cwd

    if is_under_cwd:
        relative_to = os.path.curdir
    elif specified_root:
        relative_to = specified_root
    else:
        relative_to = None

    if relative_to:
        # For file that's inside cwd, keep the relative path.
        # Note that this could be different from how you specified the path, for example
        #   cwd=/foo/bar
        #   coiled run --file /foo/bar/nested/path.txt
        # file will be copied to /scratch/nested/path.txt
        # which is a little confusing, but means it's equivalent to
        #   coiled run --file ~/nested/path.txt
        # which does feel natural.

        # For file that's not inside cwd, keep path relative if the user specified a directory for upload.
        # For example, if user specified `--file /absolute/subdir/`, then preserve path structure relative
        # to `/absolute/subdir/`, so `/absolute/subdir/foo/bar.txt` would go to `/scratch/subdir/foo/bar.txt`.
        specified_path_dir = os.path.dirname(os.path.relpath(local_path, relative_to))
        specified_path_dir = f"{specified_path_dir}/" if specified_path_dir else ""
    else:
        specified_path_dir = ""

    return specified_path_dir, base


def conda_command():
    return shutil.which(os.environ.get("CONDA_EXE", "conda")) or "conda"


def parse_conda_command(cmd: list):
    if not any("json" in i for i in cmd):
        raise ValueError("Attempting to parse conda command output with no json options specified")
    output = subprocess.check_output(cmd)
    result = json.loads(output)
    return result


def conda_package_versions(name: str) -> dict:
    """Return pacakge name and version for each conda installed pacakge

    Parameters
    ----------
    name
        Name of conda environment

    Returns
    -------
    results
        Mapping that contains the name and version of each installed package
        in the environment
    """
    cmd = [conda_command(), "env", "export", "-n", name, "--no-build", "--json"]
    output = parse_conda_command(cmd)
    output = output.get("dependencies", [])
    results = {}
    for i in output:
        if isinstance(i, str):
            package, version = i.split("=")
            results[package] = version
        else:
            # TODO: Use pip installed package information which is currently ignored
            assert isinstance(i, dict), type(i)
            assert list(i.keys()) == ["pip"], list(i.keys())
    return results


class Environ(click.ParamType):
    name = "key=value"

    def convert(self, value, param, ctx):
        env_name, env_value = value.split("=")

        if not all([env_name, env_value]):
            self.fail(
                f"{value} is not a key=value mapping",
                param,
                ctx,
            )

        return (env_name, env_value)


ENVIRON = Environ()


def format_dt(dt):
    if not dt:
        return ""
    dt = datetime.fromisoformat(dt)

    if dt.date() == datetime.today().date():
        return dt.time().strftime("%H:%M:%S")
    else:
        return dt.strftime("%Y-%m-%d %H:%M:%S")
