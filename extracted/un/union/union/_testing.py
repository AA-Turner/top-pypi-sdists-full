"""This module contains utils that are useful for development.

Example usage:

```python
import pandas as pd
from flytekit import task, workflow

from union._testing import imagespec_with_local_union

image = imagespec_with_local_union(packages=["pandas"])


@task(container_image=image)
def get_data() -> pd.DataFrame:
    return pd.DataFrame([1, 2, 3])


@task(container_image=image)
def double_df(df: pd.DataFrame) -> pd.DataFrame:
    return 2 * df


@workflow
def main() -> pd.DataFrame:
    df = get_data()
    return double_df(df=df)
```
"""

import os
import sys
from pathlib import Path
from shutil import rmtree
from subprocess import run
from tempfile import mkdtemp
from typing import Optional

import flytekit
from flytekit import ImageSpec
from flytekit.constants import CopyFileDetection

import union


def imagespec_with_local_union(
    *args,
    builder: str,
    packages: Optional[list] = None,
    source_root: Optional[str] = None,
    pull_flytekit_local_dev=False,
    union_extra: Optional[str] = None,
    **kwargs,
) -> Optional[ImageSpec]:
    """Creates an imagespec with local changes."""

    # Do not run during execution time
    execution_id = os.getenv("FLYTE_INTERNAL_EXECUTION_ID", None)
    if execution_id is not None:
        return None

    union_root_path = Path(union.__path__[0]).parent

    assert (union_root_path / "pyproject.toml").exists(), "pyproject.toml needs to exists in root directory"

    if source_root is None:
        tmp_path = Path(mkdtemp())
        source_root = tmp_path / "source_root"
        if source_root.exists():
            rmtree(source_root)
        source_root.mkdir(parents=True)
    else:
        source_root = Path(source_root)

    vendor_path = source_root / ".vendor"
    vendor_path = vendor_path.absolute()

    expected_wheels = 1
    run([sys.executable, "-m", "build", "--outdir", vendor_path, "--wheel"], check=True, cwd=union_root_path)

    if pull_flytekit_local_dev:
        expected_wheels += 1
        flytekit_root_path = Path(flytekit.__path__[0]).parent
        assert (flytekit_root_path / "pyproject.toml").exists(), "pyproject.toml needs to exists in flytekit directory"
        run([sys.executable, "-m", "build", "--outdir", vendor_path, "--wheel"], check=True, cwd=flytekit_root_path)

    wheels = list(vendor_path.iterdir())
    assert len(wheels) == expected_wheels, f"There should be {expected_wheels} wheel in {vendor_path}"
    packages = packages or []

    source_root_absolute = source_root.absolute()

    kwargs["source_copy_mode"] = CopyFileDetection.ALL

    def _process_wheel_name(name: str):
        if union_extra is None or not name.startswith("union-"):
            return name

        return f"{name}[{union_extra}]"

    if builder == "default":
        all_packages = " ".join(f"/root/.vendor/{_process_wheel_name(wheel.name)}" for wheel in wheels)
        if "commands" not in kwargs:
            kwargs["commands"] = []

        kwargs["commands"].insert(
            0,
            "--mount=from=uv,source=/uv,target=/usr/bin/uv uv pip install "
            f"--python /opt/micromamba/envs/runtime/bin/python {all_packages}",
        )
    elif builder == "envd":
        all_packages = " ".join(f"/root/.vendor/{_process_wheel_name(wheel.name)}" for wheel in wheels)
        if "commands" not in kwargs:
            kwargs["commands"] = []

        kwargs["commands"].insert(0, f"pip install {all_packages}")

    elif builder in ("unionai", "union"):
        for wheel in wheels:
            packages.append(f".vendor/{_process_wheel_name(wheel.name)}")
    else:
        raise ValueError("only default and union/unionai builder is supported")

    return ImageSpec(*args, builder=builder, packages=packages, source_root=os.fspath(source_root_absolute), **kwargs)
