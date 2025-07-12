from .config import TypedCoreConfig

from ._state_machine import DEPLOYMENT_READY_CONDITIONS
from .app_config import AppConfig, AppConfigError
from .capsule import CapsuleDeployer, list_and_filter_capsules
from functools import partial
import sys
from typing import Type


class AppDeployer(TypedCoreConfig):
    """ """

    __init__ = TypedCoreConfig.__init__

    _app_config: AppConfig

    _state = {}

    @property
    def app_config(self) -> AppConfig:
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
        name: str = None,
        image: str = None,
    ):
        cls._state["perimeter"] = perimeter
        cls._state["api_url"] = api_url
        cls._state["code_package_url"] = code_package_url
        cls._state["code_package_key"] = code_package_key
        cls._state["name"] = name
        cls._state["image"] = image

    def deploy(
        self,
        readiness_condition=DEPLOYMENT_READY_CONDITIONS.ATLEAST_ONE_RUNNING,
        max_wait_time=600,
        readiness_wait_time=10,
        logger_fn=partial(print, file=sys.stderr),
        status_file=None,
        no_loader=False,
        **kwargs,
    ):
        # Name setting from top level if none is set in the code
        if self.app_config._core_config.name is None:
            self.app_config._core_config.name = self._state["name"]

        self.app_config.commit()

        # Set any state that might have been passed down from the top level
        for k, v in self._state.items():
            if self.app_config.get_state(k) is None:
                self.app_config.set_state(k, v)

        capsule = CapsuleDeployer(
            self.app_config,
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

        force_upgrade = self.app_config.get_state("force_upgrade", False)

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
        return final_status


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
