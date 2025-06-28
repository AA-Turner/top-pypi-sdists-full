import copy
from dataclasses import replace
import pathlib
from typing import Any, Dict, List, Optional, Tuple, Union

from anyscale._private.anyscale_client import (
    AnyscaleClientInterface,
    WORKSPACE_CLUSTER_NAME_PREFIX,
)
from anyscale._private.sdk.base_sdk import BaseSDK, Timer
from anyscale.cli_logger import BlockLogger
from anyscale.compute_config._private.compute_config_sdk import PrivateComputeConfigSDK
from anyscale.compute_config.models import ComputeConfig
from anyscale.image._private.image_sdk import PrivateImageSDK
from anyscale.utils.runtime_env import is_dir_remote_uri, parse_requirements_file


class WorkloadSDK(BaseSDK):
    """Shared parent class for job and service SDKs."""

    def __init__(
        self,
        *,
        logger: Optional[BlockLogger] = None,
        client: Optional[AnyscaleClientInterface] = None,
        timer: Optional[Timer] = None,
    ):
        super().__init__(logger=logger, client=client, timer=timer)
        self._compute_config_sdk = PrivateComputeConfigSDK(
            logger=self.logger, client=self.client,
        )
        self._image_sdk = PrivateImageSDK(logger=self.logger, client=self.client)

    @property
    def image_sdk(self) -> PrivateImageSDK:
        return self._image_sdk

    def update_env_vars(
        self,
        runtime_envs: List[Dict[str, Any]],
        *,
        env_vars_updates: Optional[Dict[str, str]],
    ) -> List[Dict[str, Any]]:
        """Replaces 'env_vars' fields in runtime_envs with the override."""
        new_runtime_envs = copy.deepcopy(runtime_envs)

        if env_vars_updates:
            for runtime_env in new_runtime_envs:
                if "env_vars" in runtime_env:
                    # the precedence should be config > runtime_env
                    runtime_env["env_vars"].update(env_vars_updates)
                else:
                    runtime_env["env_vars"] = env_vars_updates

        return new_runtime_envs

    def override_and_load_requirements_files(
        self,
        runtime_envs: List[Dict[str, Any]],
        *,
        requirements_override: Union[None, str, List[str]],
        workspace_requirements_path: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Replaces 'pip' fields in runtime_envs with their parsed file contents.

        The precedence for overrides is: explicit overrides passed in > fields in the existing
        runtime_envs > workspace defaults (if `autopopulate_in_workspace == True`).
        """
        new_runtime_envs = copy.deepcopy(runtime_envs)

        local_path_to_parsed_requirements: Dict[str, List[str]] = {}

        def _load_requirements_file_memoized(
            target: Union[str, List[str]]
        ) -> List[str]:
            if isinstance(target, list):
                return target
            elif target in local_path_to_parsed_requirements:
                return local_path_to_parsed_requirements[target]
            elif isinstance(target, str):
                parsed_requirements = parse_requirements_file(target)
                if parsed_requirements is None:
                    raise FileNotFoundError(
                        f"Requirements file {target} does not exist."
                    )
                local_path_to_parsed_requirements[target] = parsed_requirements
                return parsed_requirements
            else:
                raise TypeError("pip field in runtime_env must be a list or string.")

        for runtime_env in new_runtime_envs:
            if requirements_override is not None:
                # Explicitly-specified override from the user.
                runtime_env["pip"] = requirements_override
            elif (
                workspace_requirements_path is not None
                and "pip" not in runtime_env
                and "conda" not in runtime_env
            ):
                self.logger.info("Including workspace-managed pip dependencies.")
                runtime_env["pip"] = workspace_requirements_path

            if runtime_env.get("pip", None) is not None:
                # Load requirements from the file if necessary.
                runtime_env["pip"] = _load_requirements_file_memoized(
                    runtime_env["pip"]
                )

        return new_runtime_envs

    def override_and_upload_local_dirs(
        self,
        runtime_envs: List[Dict[str, Any]],
        *,
        working_dir_override: Optional[str],
        excludes_override: Optional[List[str]],
        cloud_id: Optional[str] = None,
        autopopulate_in_workspace: bool = True,
        additional_py_modules: Optional[List[str]] = None,
        py_executable_override: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """Returns modified runtime_envs with all local dirs converted to remote URIs.

        The precedence for overrides is: explicit overrides passed in > fields in the existing
        runtime_envs > workspace defaults (if `autopopulate_in_workspace == True`).

        Each unique local directory across these fields will be uploaded once to cloud storage,
        then all occurrences of it in the config will be replaced with the corresponding remote URI.
        """
        new_runtime_envs = copy.deepcopy(runtime_envs)

        local_path_to_uri: Dict[str, str] = {}

        def _upload_dir_memoized(target: str, *, excludes: Optional[List[str]]) -> str:
            if is_dir_remote_uri(target):
                return target
            if target in local_path_to_uri:
                return local_path_to_uri[target]

            self.logger.info(f"Uploading local dir '{target}' to cloud storage.")
            assert cloud_id is not None
            uri = self._client.upload_local_dir_to_cloud_storage(
                target, cloud_id=cloud_id, excludes=excludes,
            )
            local_path_to_uri[target] = uri
            return uri

        for runtime_env in new_runtime_envs:
            # Extend, don't overwrite, excludes if it's provided.
            if excludes_override is not None:
                existing_excludes = runtime_env.get("excludes", None) or []
                runtime_env["excludes"] = existing_excludes + excludes_override

            final_excludes = runtime_env.get("excludes", [])

            new_working_dir = None
            if working_dir_override is not None:
                new_working_dir = working_dir_override
            elif "working_dir" in runtime_env:
                new_working_dir = runtime_env["working_dir"]
            elif autopopulate_in_workspace and self._client.inside_workspace():
                new_working_dir = "."

            if new_working_dir is not None:
                runtime_env["working_dir"] = _upload_dir_memoized(
                    new_working_dir, excludes=final_excludes
                )

            if additional_py_modules:
                existing_py_modules = runtime_env.get("py_modules", [])
                runtime_env["py_modules"] = existing_py_modules + additional_py_modules

            final_py_modules = runtime_env.get("py_modules", None)
            if final_py_modules is not None:
                runtime_env["py_modules"] = [
                    _upload_dir_memoized(py_module, excludes=final_excludes)
                    for py_module in final_py_modules
                ]

            if py_executable_override:
                runtime_env["py_executable"] = py_executable_override

        return new_runtime_envs

    def _resolve_compute_config_id(
        self, compute_config: Union[str, ComputeConfig], cloud: Optional[str] = None,
    ) -> str:
        """Resolve the passed compute config to its ID.

        Accepts either:
            - A string of the form: '<name>[:<version>]'.
            - A dictionary from which an anonymous compute config will be built.

        Returns compute_config_id.
        """
        if isinstance(compute_config, str):
            compute_config_id = self._client.get_compute_config_id(
                compute_config_name=compute_config, cloud=cloud,
            )
            if compute_config_id is None:
                raise ValueError(
                    f"The compute config '{compute_config}' does not exist."
                )
        else:
            _, compute_config_id = self._compute_config_sdk.create_compute_config(
                compute_config
            )

        return compute_config_id

    def resolve_compute_config_and_cloud_id(
        self,
        *,
        compute_config: Union[ComputeConfig, Dict, str, None],
        cloud: Union[None, str],
    ) -> Tuple[str, str]:
        """Resolve the passed compute config to its ID and corresponding cloud ID.

        Accepts either:
            - A string of the form: '<name>[:<version>]'.
            - A dictionary from which an anonymous compute config will be built.

        Returns (compute_config_id, cloud_id).
        """
        if compute_config is None and cloud is None:
            compute_config_id = self._client.get_compute_config_id()
            assert compute_config_id is not None
            return (
                compute_config_id,
                self.client.get_cloud_id(compute_config_id=compute_config_id),
            )
        elif compute_config is None:
            cloud_id = self.client.get_cloud_id(cloud_name=cloud)  # type: ignore
            compute_config_id = self._client.get_default_compute_config(
                cloud_id=cloud_id
            ).id
            return (compute_config_id, cloud_id)  # type: ignore
        elif cloud is None:
            compute_config_id = self._resolve_compute_config_id(
                compute_config=compute_config  # type: ignore
            )
            return (
                compute_config_id,
                self.client.get_cloud_id(compute_config_id=compute_config_id),
            )
        else:
            # If we are creating a new compute config, ensure cloud is set accordingly
            if (
                isinstance(compute_config, ComputeConfig)
                and compute_config.cloud is None
            ):
                compute_config = replace(compute_config, cloud=cloud)

            compute_config_id = self._resolve_compute_config_id(
                compute_config=compute_config,  # type: ignore
                cloud=cloud,
            )
            cloud_id_from_cc = self.client.get_cloud_id(
                compute_config_id=compute_config_id
            )
            cloud_id_from_cloud = self.client.get_cloud_id(cloud_name=cloud)  # type: ignore
            if cloud_id_from_cc != cloud_id_from_cloud:
                raise ValueError(
                    "Cloud does not match from provided `cloud` and `compute_config`. Either pass one of these or ensure they match."
                )
            else:
                return (compute_config_id, cloud_id_from_cc)

    def get_current_workspace_name(self) -> Optional[str]:
        """Get the name of the curernt workspace if running inside one."""
        if not self._client.inside_workspace():
            return None

        workspace = self._client.get_current_workspace_cluster()
        assert workspace is not None
        name = workspace.name
        # Defensively default to the workspace cluster name as-is if it doesn't
        # start with the expected prefix.
        if name.startswith(WORKSPACE_CLUSTER_NAME_PREFIX):
            name = name[len(WORKSPACE_CLUSTER_NAME_PREFIX) :]

        return name

    def get_containerfile_contents(self, path: str) -> str:
        """Get the full content of the containerfile as a string."""
        containerfile_path = pathlib.Path(path)
        if not containerfile_path.exists():
            raise FileNotFoundError(
                f"Containerfile '{containerfile_path}' does not exist."
            )
        if not containerfile_path.is_file():
            raise ValueError(f"Containerfile '{containerfile_path}' must be a file.")

        return containerfile_path.read_text()

    def _strip_none_values_from_dict(self, d: Dict) -> Dict:
        """Return a copy of the dictionary without any keys whose values are None.

        Recursively calls into any dictionary values.
        """
        result = {}
        for k, v in d.items():
            if isinstance(v, dict):
                result[k] = self._strip_none_values_from_dict(v)
            elif v is not None:
                result[k] = v

        return result

    def get_user_facing_compute_config(
        self, compute_config_id: str,
    ) -> Union[str, ComputeConfig]:
        """Get the compute config in a format to be displayed in a user-facing status.

        If the compute config refers to an anonymous compute config, its config
        object will be returned. Else the name of the compute config will be
        returned in the form: '<name>:<version>'.
        """
        compute_config = self._client.get_compute_config(compute_config_id)
        if compute_config is None:
            raise RuntimeError(
                f"Failed to get compute config for ID {compute_config_id}."
            )

        compute_config_name = compute_config.name
        if compute_config.version is not None:
            compute_config_name += f":{compute_config.version}"

        if not compute_config.anonymous:
            return compute_config_name

        return self._compute_config_sdk._convert_api_model_to_compute_config_version(  # noqa: SLF001
            compute_config
        ).config
