import importlib.util
import os
import shutil
import subprocess  # nosec
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from qwak.inner.build_logic.constants.temp_dir import TEMP_LOCAL_MODEL_DIR
from qwak.inner.build_logic.dependency_manager_type import DependencyManagerType

from qwak.inner.build_logic.interface.step_inteface import Step
from qwak.exceptions import QwakSuggestionException
from qwak.inner.build_logic.tools.dependencies_tools import find_dependency_files

TEMP_LOCAL_EDITABLE_FOLDER = "editable"


@dataclass
class DependencyFileObject:
    dep_file_name: List[str]
    lock_file_name: str = field(default="")


DEPS_MANAGER_FILE_MAP = {
    DependencyManagerType.PIP: DependencyFileObject(dep_file_name=["requirements.txt"]),
    DependencyManagerType.POETRY: DependencyFileObject(
        dep_file_name=["pyproject.toml"], lock_file_name="poetry.lock"
    ),
    DependencyManagerType.CONDA: DependencyFileObject(
        dep_file_name=["conda.yml", "conda.yaml"]
    ),
}


class PostFetchValidationStep(Step):
    STEP_DESCRIPTION = "Post model fetch validation"

    def description(self) -> str:
        return self.STEP_DESCRIPTION

    def execute(self) -> None:
        self.validate_dependencies()
        self.configure_base_docker_image()
        self.create_development_wheels()

    def validate_dependencies(self):
        if (
            not Path(self.config.build_properties.model_uri.uri).is_dir()
            or self.config.build_env.python_env.dependency_file_path
        ):
            self.build_logger.debug("Validating dependency file exists")
            model_uri, main_dir = (
                self.context.host_temp_local_build_dir / TEMP_LOCAL_MODEL_DIR,
                self.config.build_properties.model_uri.main_dir,
            )
            (
                self.context.dependency_manager_type,
                self.context.model_relative_dependency_file,
                self.context.model_relative_dependency_lock_file,
            ) = find_dependency_files(model_uri, main_dir, self.build_logger)

            if (
                self.context.dependency_manager_type
                and self.context.model_relative_dependency_file
            ):
                return

            self.build_logger.error("Dependency file wasn't found, failing...")
            raise QwakSuggestionException(
                message="Dependency file isn't found",
                suggestion="Make sure your model include one of dependencies manager: pip/poetry/conda",
            )

    def configure_base_docker_image(self):
        base_image = self.config.build_env.docker.base_image
        if (not base_image) and self.config.build_env.remote.resources.gpu_type:
            base_image = "qwakai/qwak:gpu-py39"
        self.context.base_image = base_image

    def create_development_wheels(self):
        if not os.getenv("QWAK_DEBUG"):
            return

        (module_location,) = importlib.util.find_spec(
            "qwak_sdk"
        ).submodule_search_locations
        source_dir = Path(module_location).parent
        pyproject_toml = source_dir / "pyproject.toml"

        if pyproject_toml.is_file():
            self.build_logger.info(
                "Detected non-PyPI-released qwak-sdk installed, creating local qwak-runtime "
                "and qwak-core wheel files to pass to build process"
            )
            runtime_dir = source_dir.parent / "qwak-runtime"
            core_dir = source_dir.parent / "qwak-core"
            target_path = self.context.host_temp_local_build_dir
            self.context.custom_runtime_wheel = self._create_wheel(
                runtime_dir, target_path
            )
            self.context.custom_core_wheel = self._create_wheel(core_dir, target_path)

    def _create_wheel(self, package_dir, target_path):
        dist_dir = package_dir / "dist"
        shutil.rmtree(dist_dir, ignore_errors=True)
        output = subprocess.check_output(["make", "sync"], cwd=package_dir)  # nosec
        for line in output.decode().split("\n"):
            self.build_logger.debug(f">>> {line}")
        output = subprocess.check_output(["poetry", "build"], cwd=package_dir)  # nosec
        for line in output.decode().split("\n"):
            self.build_logger.debug(f">>> {line}")
        wheel_file = next(dist_dir.glob("*.whl"), None)
        editable_folder = target_path / TEMP_LOCAL_EDITABLE_FOLDER
        editable_folder.mkdir(exist_ok=True)
        copied_wheel_file = shutil.move(wheel_file, editable_folder / wheel_file.name)
        shutil.rmtree(dist_dir, ignore_errors=True)
        self.build_logger.info(f"Created wheel for {package_dir} successfully")
        return copied_wheel_file


def find_file_location(model_uri, main_dir, filename) -> Path:
    file_locations: List[Path] = [
        model_uri / filename,
        model_uri / main_dir / filename,
    ]
    for file in file_locations:
        if file.is_file():
            return file


def get_possible_dependency_lock_paths(dependency_path: Path):
    paths = []
    for _, dependency_file_object in DEPS_MANAGER_FILE_MAP.items():
        if dependency_file_object.lock_file_name:
            lock_file_path = (
                dependency_path.parent / dependency_file_object.lock_file_name
            )
            paths.append(lock_file_path)
    return paths
