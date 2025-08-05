from .config import TypedCoreConfig, TypedDict
from .perimeters import PerimeterExtractor
from .capsule import CapsuleApi
import json
from ._state_machine import DEPLOYMENT_READY_CONDITIONS, LogLine
from .app_config import AppConfig, AppConfigError
from .capsule import CapsuleDeployer, list_and_filter_capsules
from functools import partial
import sys
import uuid
from typing import Type, Dict, List
from datetime import datetime


class AppDeployer(TypedCoreConfig):
    """ """

    __init__ = TypedCoreConfig.__init__

    _app_config: AppConfig

    _state = {}

    __state_items = [
        "perimeter",
        "api_url",
        "code_package_url",
        "code_package_key",
        "image",
        "project",
        "branch",
    ]

    @property
    def _deploy_config(self) -> AppConfig:
        if not hasattr(self, "_app_config"):
            self._app_config = AppConfig(self._config)
        return self._app_config

    # Things that need to be set before deploy
    @classmethod
    def _set_state(
        cls,
        perimeter: str,
        api_url: str,
        code_package_url: str = None,
        code_package_key: str = None,
        name_prefix: str = None,
        image: str = None,
        max_entropy: int = 4,
        default_tags: List[Dict[str, str]] = None,
        project: str = None,
        branch: str = None,
    ):
        cls._state["perimeter"] = perimeter
        cls._state["api_url"] = api_url
        cls._state["code_package_url"] = code_package_url
        cls._state["code_package_key"] = code_package_key
        cls._state["name_prefix"] = name_prefix
        cls._state["image"] = image
        cls._state["max_entropy"] = max_entropy
        cls._state["default_tags"] = default_tags
        cls._state["project"] = project
        cls._state["branch"] = branch

        assert (
            max_entropy > 0
        ), "max_entropy must be greater than 0. Since AppDeployer's deploy fn can be called many time inside a step itself."

    def deploy(
        self,
        readiness_condition=DEPLOYMENT_READY_CONDITIONS.ATLEAST_ONE_RUNNING,
        max_wait_time=600,
        readiness_wait_time=10,
        logger_fn=partial(print, file=sys.stderr),
        status_file=None,
        no_loader=False,
        **kwargs,
    ) -> "DeployedApp":

        # Name setting from top level if none is set in the code
        if self._deploy_config._core_config.name is None:
            name = self._state[
                "name_prefix"
            ]  # for now the name-prefix cannot be very large.
            entropy = uuid.uuid4().hex[: self._state["max_entropy"]]
            self._deploy_config._core_config.name = f"{name}-{entropy}"

        if len(self._state["default_tags"]) > 0:
            self._deploy_config._core_config.tags = (
                self._deploy_config._core_config.tags or []
            ) + self._state["default_tags"]

        self._deploy_config.commit()
        # Set any state that might have been passed down from the top level
        for k in self.__state_items:
            if self._deploy_config.get_state(k) is None:
                self._deploy_config.set_state(k, self._state[k])

        capsule = CapsuleDeployer(
            self._deploy_config,
            self._state["api_url"],
            create_timeout=max_wait_time,
            debug_dir=None,
            success_terminal_state_condition=readiness_condition,
            readiness_wait_time=readiness_wait_time,
            logger_fn=logger_fn,
        )

        currently_present_capsules = list_and_filter_capsules(
            capsule.capsule_api,
            None,
            None,
            capsule.name,
            None,
            None,
            None,
        )

        force_upgrade = self._deploy_config.get_state("force_upgrade", False)

        if len(currently_present_capsules) > 0:
            # Only update the capsule if there is no upgrade in progress
            # Only update a "already updating" capsule if the `--force-upgrade` flag is provided.
            _curr_cap = currently_present_capsules[0]
            this_capsule_is_being_updated = _curr_cap.get("status", {}).get(
                "updateInProgress", False
            )

            if this_capsule_is_being_updated and not force_upgrade:
                _upgrader = _curr_cap.get("metadata", {}).get("lastModifiedBy", None)
                message = f"{capsule.capsule_type} is currently being upgraded"
                if _upgrader:
                    message = (
                        f"{capsule.capsule_type} is currently being upgraded. Upgrade was launched by {_upgrader}. "
                        "If you wish to force upgrade, you can do so by providing the `--force-upgrade` flag."
                    )
                raise AppConfigError(message)

            logger_fn(
                f"🚀 {'' if not force_upgrade else 'Force'} Upgrading {capsule.capsule_type.lower()} `{capsule.name}`....",
            )
        else:
            logger_fn(
                f"🚀 Deploying {capsule.capsule_type.lower()} `{capsule.name}`....",
            )

        capsule.create()
        final_status = capsule.wait_for_terminal_state()
        return DeployedApp(
            final_status["id"],
            final_status["auth_type"],
            final_status["public_url"],
            final_status["name"],
            final_status["deployed_version"],
            final_status["deployed_at"],
        )


class DeployedApp:
    def __init__(
        self,
        _id: str,
        capsule_type: str,
        public_url: str,
        name: str,
        deployed_version: str,
        deployed_at: str,
    ):
        self._id = _id
        self._capsule_type = capsule_type
        self._public_url = public_url
        self._name = name
        self._deployed_version = deployed_version
        self._deployed_at = deployed_at

    def _get_capsule_api(self) -> CapsuleApi:
        perimeter, api_server = PerimeterExtractor.during_metaflow_execution()
        return CapsuleApi(api_server, perimeter)

    def logs(self, previous=False) -> Dict[str, List[LogLine]]:
        """
        Returns a dictionary of worker_id to logs.
        If `previous` is True, it will return the logs from the previous execution of the workers. Useful when debugging a crashlooping worker.
        """
        capsule_api = self._get_capsule_api()
        # extract workers from capsule
        workers = capsule_api.get_workers(self._id)
        # get logs from workers
        logs = {
            # worker_id: logs
        }
        for worker in workers:
            # TODO: Handle exceptions better over here.
            logs[worker["workerId"]] = capsule_api.logs(
                self._id, worker["workerId"], previous=previous
            )
        return logs

    def info(self) -> dict:
        """
        Returns a dictionary representing the deployed app.
        """
        capsule_api = self._get_capsule_api()
        capsule = capsule_api.get(self._id)
        return capsule

    def replicas(self):
        capsule_api = self._get_capsule_api()
        return capsule_api.get_workers(self._id)

    def scale_to_zero(self):
        """
        Scales the DeployedApp to 0 replicas.
        """
        capsule_api = self._get_capsule_api()
        return capsule_api.patch(
            self._id,
            {
                "autoscalingConfig": {
                    "minReplicas": 0,
                    "maxReplicas": 0,
                }
            },
        )

    def delete(self):
        """
        Deletes the DeployedApp.
        """
        capsule_api = self._get_capsule_api()
        return capsule_api.delete(self._id)

    @property
    def id(self) -> str:
        return self._id

    @property
    def auth_style(self) -> str:
        # TODO : Fix naming here.
        return self._capsule_type

    @property
    def public_url(self) -> str:
        return self._public_url

    @property
    def name(self) -> str:
        return self._name

    @property
    def deployed_version(self) -> str:
        return self._deployed_version

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "auth_style": self.auth_style,  # TODO : Fix naming here.
            "public_url": self._public_url,
            "name": self._name,
            "deployed_version": self._deployed_version,
            "deployed_at": self._deployed_at,
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            _id=data["id"],
            capsule_type=data["capsule_type"],
            public_url=data["public_url"],
            name=data["name"],
            deployed_version=data["deployed_version"],
            deployed_at=data["deployed_at"],
        )

    @property
    def deployed_at(self) -> datetime:
        return datetime.fromisoformat(self._deployed_at)

    def __repr__(self) -> str:
        return (
            f"DeployedApp(id='{self._id}', "
            f"name='{self._name}', "
            f"public_url='{self._public_url}', "
            f"deployed_version='{self._deployed_version}')"
        )


class apps:

    _name_prefix = None

    @classmethod
    def set_name_prefix(cls, name_prefix: str):
        cls._name_prefix = name_prefix

    @property
    def name_prefix(self) -> str:
        return self._name_prefix

    @property
    def Deployer(self) -> Type[AppDeployer]:
        return AppDeployer
