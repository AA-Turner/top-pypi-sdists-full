from pathlib import Path
from os import PathLike
from setuptools import Command
from setuptools.command.build import build
from typing import Any, Callable, Dict, List, Union
from warnings import warn

from importlib_resources import Package, files
from importlib_resources.abc import Traversable

try:
    PathType = str | PathLike[Any]
except TypeError:
    # `PathLike[Any]` not supported until 3.9
    # `str | None` syntax not supported until 3.10
    PathType = Union[str, PathLike]

Builder = Callable[[Path], None]


DEFAULT_FN = "runtime_build"


def load_python_config(
    config_file_path: Traversable, local_variable_name: str = "BUILD_ARGUMENTS"
) -> Dict:
    config_file_contents = config_file_path.read_text()
    context: Dict[str, Any] = dict(__file__=str(config_file_path.resolve()))
    exec(config_file_contents, context)
    return context.get(local_variable_name, {})


def build_item(
    package_base: Traversable,
    base_name: PathType,
    builder: Builder,
) -> Path:
    target_path = package_base / base_name
    builder(target_path)
    return target_path


def build_on_demand(
    package: Package,
    base_name: PathType,
    build_file_name: PathType = DEFAULT_FN,
):
    fp = files(package)
    build_path = fp / build_file_name
    try:
        build_args = load_python_config(build_path)
    except FileNotFoundError:
        warn(f"can't find {build_path}, runtime build skipped", RuntimeWarning)
        return None
    builder = build_args.get(base_name)
    if builder is None:
        raise ValueError(f"unknown resource {base_name}")
    try:
        return build_item(files(package), base_name, builder)
    except FileNotFoundError:
        warn(
            f"can't find source file {base_name}, runtime build skipped", RuntimeWarning
        )


def build_all_items_for_package(
    package: str, package_dir: Dict[str, str] = {}
) -> List[Path]:
    package_base = package_base_for_package(package, package_dir)
    return build_all_items_for_package_base(package_base)


def build_all_items_for_package_base(
    package_base: Traversable,
    build_file_name: PathType = DEFAULT_FN,
) -> List[Path]:
    build_args = load_python_config(package_base / build_file_name)
    return [
        build_item(package_base, base_name, builder)
        for base_name, builder in build_args.items()
    ]


def build_runtime_setuptools(*all_packages: List[str]) -> Command:
    """
    Use this in `setup.py` as follows:

    ```python
    from runtime_builder import build_runtime_setuptools

    RUNTIME_BUILD_PACKAGE_LIST = ["package.foo", "package.bar", ...]
    # list of packages containing `runtime_build` files (so there is one
    # at `package/foo/runtime_build` and one at `package/bar/runtime_build`)

    setup(
        ...
        include_package_data=True,
        cmdclass={
            "build_runtime_builder_artifacts": build_runtime_setuptools(RUNTIME_BUILD_PACKAGE_LIST),
        },
    )
    ```
    This example invokes `build_all_items_for_package` at just the right time.

    Using `setuptools` to do this build isn't as satisfying as `enscons`, as I've not been able
    to figure out a way to only include source files in the sdist. This is a consequence of
    `setuptools` being a really terrible legacy mess.
    """
    build.sub_commands.insert(0, ("build_runtime_builder_artifacts", lambda x: 1))

    class BuildRuntimeBuilderArtifactsCommand(Command):
        description = "Build runtime_builder artifacts files"
        user_options = []

        def initialize_options(self):
            pass

        def finalize_options(self):
            pass

        def run(self):
            # Custom code to generate the .hex files
            package_dir = self.distribution.package_dir
            for package in all_packages:
                package_base = package_base_for_package(package, package_dir)
                _built_items = build_all_items_for_package_base(package_base)

    return BuildRuntimeBuilderArtifactsCommand


def package_base_for_package(
    package: str, package_dir: Dict[str, PathType]
) -> Traversable:
    components = package.split(".")
    loop = list(components)
    base = Path(package_dir.get("", "."))
    suffix = Path(*components)
    while loop:
        prefix = ".".join(loop)
        if prefix in package_dir:
            raise ValueError(
                'package_dir mappings besides {"" : SOME_PATH} not yet supported'
            )
        loop.pop()
    return base / suffix
