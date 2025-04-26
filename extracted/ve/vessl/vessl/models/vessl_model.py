import json
import os
import subprocess

import packaging.requirements
import toml
from packaging.specifiers import SpecifierSet

from vessl.service import _load_model_v2, _run_model_server
from vessl.util.constant import API_HOST, VESSL_IGNORE_FILE_PATH
from vessl.util.echo import print_info


class VesslModel:
    """
    This class is used to contain a model.
    You can use this class to create a lockfile, install dependencies, and launch the RunnerBase class models.
    The lockfile contains information about the model, runtime, and dependencies.

    Args:
        type_input (str): The type of model.

        repository_name (str): The name of the repository.

        model_number (str): The number of the model.

        entrypoint (str): The entrypoint of the model.

        python_version (str): The version of Python.

        weight_name_or_path (str): The name or path of the weights.

        requirements_path (str): The path to the requirements file.

        pyproject_path (str): The path to the pyproject file.

        cuda_version (str): The version of CUDA.

        pytorch_version (str): The version of PyTorch.

        tensorflow_version (str): The version of TensorFlow.

        autocreate_repository (bool): Whether to autocreate the repository.

    """

    class Runtime:
        def __init__(
            self,
            python_version=None,
            cuda_version=None,
            framework_type=None,
            pytorch_version=None,
            tensorflow_version=None,
        ):
            self.python_version = python_version
            self.cuda_version = cuda_version
            self.framework_type = framework_type
            self.pytorch_version = pytorch_version
            self.tensorflow_version = tensorflow_version

        def build(self):
            return {
                "python_version": self.python_version,
                "cuda_version": self.cuda_version,
                "framework_type": self.framework_type,
                "pytorch_version": self.pytorch_version,
                "tensorflow_version": self.tensorflow_version,
            }

    class ModelReference:
        def __init__(
            self,
            type_input=None,
            repository_name=None,
            model_number=None,
            weights_path=None,
        ):
            self.type = type_input
            self.model_repository_name = repository_name
            self.model_number = model_number
            self.weights_path = weights_path

        def build(self):
            return {
                "type": self.type,
                "model_repository_name": self.model_repository_name,
                "model_number": self.model_number,
                "weights_path": self.weights_path,
            }

    class Dependency:
        def __init__(
            self,
            requirements_path=None,
            pyproject_path=None,
        ):
            self.requirements_path = requirements_path
            self.pyproject_path = pyproject_path

        def build(self):
            return {
                "requirements_path": self.requirements_path,
                "pyproject_path": self.pyproject_path,
            }

    def __init__(
        self,
        type_input=None,
        repository_name=None,
        model_number=None,
        entrypoint=None,
        python_version=None,
        weight_name_or_path=None,
        requirements_path=None,
        pyproject_path=None,
        cuda_version=None,
        framework_type=None,
        pytorch_version=None,
        tensorflow_version=None,
        autocreate_repository=None,
    ):
        self.type = type_input
        self.repository_name = repository_name
        self.model_number = model_number
        self.entrypoint = entrypoint

        self.weight_name_or_path = weight_name_or_path

        self.python_version = python_version
        self.cuda_version = cuda_version
        self.framework_type = framework_type
        self.pytorch_version = pytorch_version
        self.tensorflow_version = tensorflow_version
        self.autocreate_repository = autocreate_repository

        self.requirements_path = requirements_path
        self.pyproject_path = pyproject_path
        if requirements_path is not None:
            self._validate_from_requirements()
        if pyproject_path is not None:
            self._validate_from_pyproject()

    def _validate_from_requirements(self):
        try:
            with open(self.requirements_path, "r") as f:
                reqs = {}
                for req_line in f:
                    req_line: str = req_line.strip()
                    if not req_line:
                        continue
                    try:
                        req = packaging.requirements.Requirement(req_line)
                    except packaging.requirements.InvalidRequirement:
                        continue
                    reqs[req.name] = req.specifier

                if "torch" in reqs:
                    _validate_version("torch", "requirements", self.pytorch_version, reqs["torch"])
                if "tensorflow" in reqs:
                    _validate_version(
                        "tensorflow", "requirements", self.tensorflow_version, reqs["tensorflow"]
                    )
                if "python" in reqs:
                    _validate_version("python", "requirements", self.python_version, reqs["python"])
        except FileNotFoundError:
            print_info("requirements.txt not found, skipping")
            pass

    def _validate_from_pyproject(self):
        try:
            with open(self.pyproject_path, "r") as f:
                data = toml.load(f)

                # pyproject deps
                deps = data.get("dependencies")
                if deps is not None:
                    deps = {k: SpecifierSet(v) for k, v in deps.items()}
                    if "torch" in deps:
                        _validate_version("torch", "pyproject", self.pytorch_version, deps["torch"])
                    if "tensorflow" in deps:
                        _validate_version(
                            "tensorlow", "pyproject", self.tensorflow_version, deps["tensorflow"]
                        )
                    if "python" in deps:
                        _validate_version(
                            "python", "pyproject", self.python_version, deps["python"]
                        )

                # poetry deps, overrides pyproject deps
                deps = data.get("tool", {}).get("poetry", {}).get("dependencies")
                if deps is not None:
                    deps = {k: SpecifierSet(v) for k, v in deps.items()}
                    if "torch" in deps:
                        _validate_version("torch", "poetry", self.pytorch_version, deps["torch"])
                    if "tensorflow" in deps:
                        _validate_version(
                            "tensorlow", "poetry", self.tensorflow_version, deps["tensorflow"]
                        )
                    if "python" in deps:
                        _validate_version("python", "poetry", self.python_version, deps["python"])
        except FileNotFoundError:
            print_info("pyproject.toml not found, skipping")
            pass

    def build_lockfile(self):
        return json.dumps(
            {
                "_comment": "This file is auto-generated by `vessl model register` command. Do not edit manually.",
                "runtime": VesslModel.Runtime(
                    self.python_version,
                    self.cuda_version,
                    self.framework_type,
                    self.pytorch_version if hasattr(self, "pytorch_version") else None,
                    self.tensorflow_version if hasattr(self, "tensorflow_version") else None,
                ).build(),
                "model": VesslModel.ModelReference(
                    self.type, self.repository_name, self.model_number, self.weight_name_or_path
                ).build(),
                "dependency": VesslModel.Dependency(
                    self.requirements_path, self.pyproject_path
                ).build(),
                "entrypoint": self.entrypoint,
            },
            indent=2,
        )

    @classmethod
    def create(
        cls,
        type: str,
        repository_name: str,
        model_number: str,
        entrypoint: str,
        python_version: str,
        weight_name_or_path: str,
        requirements_path: str,
        pyproject_path: str,
        cuda_version: str,
        framework_type: str,
        pytorch_version: str = None,
        tensorflow_version: str = None,
        autocreate_repository: bool = False,
    ):
        l = cls(
            type,
            repository_name,
            model_number,
            entrypoint,
            python_version,
            weight_name_or_path,
            requirements_path,
            pyproject_path,
            cuda_version,
            framework_type,
            pytorch_version,
            tensorflow_version,
            autocreate_repository,
        )
        return l

    def save_lockfile(self, dest_dir: str = None):
        dest_path = os.path.join(os.getcwd(), ".vessl.model.lock")
        if dest_dir != None:
            dest_path = os.path.join(dest_dir, ".vessl.model.lock")

        with open(dest_path, "w") as f:
            f.write(self.build_lockfile())

    @staticmethod
    def create_ignore_file(dest_dir: str = None):
        dest_path = VESSL_IGNORE_FILE_PATH
        if dest_dir != None:
            dest_path = os.path.join(dest_dir, ".vesslignore")

        if not os.path.exists(dest_path):
            default_vesslignore_list = [
                ".git",
                ".pytest_cache",
                ".venv",
                "__pycache__",
            ]
            with open(dest_path, "w") as f:
                f.write("\n".join(default_vesslignore_list))

    @classmethod
    def from_lockfile(cls, path: str):
        if not os.path.exists(path):
            return None
        with open(path, "r") as f:
            data = json.load(f)
            return cls(
                type_input=data["model"]["type"],
                repository_name=data["model"]["model_repository_name"],
                model_number=data["model"]["model_number"],
                entrypoint=data["entrypoint"],
                python_version=data["runtime"]["python_version"],
                requirements_path=data["dependency"]["requirements_path"],
                pyproject_path=data["dependency"]["pyproject_path"],
                cuda_version=data["runtime"]["cuda_version"],
                framework_type=data["runtime"]["framework_type"],
                pytorch_version=data["runtime"]["pytorch_version"],
                tensorflow_version=data["runtime"]["tensorflow_version"],
            )

    def install_deps(self):
        if self.requirements_path is not None:
            print_info(f"Installing dependencies from {self.requirements_path}")
            command = ["pip", "install", "-r", self.requirements_path]
            # @XXX(seokju) hardcoded for now
            if API_HOST == "https://api.dev.vssl.ai":
                command.extend(
                    [
                        "--index-url",
                        "https://test.pypi.org/simple",
                        "--extra-index-url",
                        "https://pypi.org/simple",
                        "--pre",
                    ]
                )
            subprocess.check_call(command)
        if self.pyproject_path is not None:
            print_info(f"Installing dependencies from {self.pyproject_path}")
            subprocess.check_call(["poetry", "install"])

    def launch_model(self, filename: str, classname: str, remote: bool = True, port: int = 8000):
        model_server, input_type, output_type, pass_type_param = _load_model_v2(filename, classname)

        _run_model_server(
            model_server,
            remote,
            port=port,
            api_name=f"{self.repository_name}-{self.model_number}",
            inputType=input_type if pass_type_param else None,
            outputType=output_type if pass_type_param else None,
        )


def _validate_version(library_name: str, context: str, input_version: str, version: SpecifierSet):
    if input_version is not None:
        if not version.contains(input_version):
            raise ValueError(
                f"There is a mismatch of the {library_name} version between your input({input_version}) and {context}({version})"
            )
