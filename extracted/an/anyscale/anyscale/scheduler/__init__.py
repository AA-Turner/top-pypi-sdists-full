"""Alpha SDK for the Anyscale Global Resource Scheduler.

Exposed as ``anyscale.scheduler`` and ``Anyscale().scheduler``.
"""
from typing import Any, Dict, List, Optional, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.scheduler._private.scheduler_sdk import PrivateSchedulerSDK
from anyscale.scheduler.commands import (
    _APPLY_CONFIG_DOCSTRINGS,
    _APPLY_CONFIG_EXAMPLE,
    _GET_CONFIG_DOCSTRINGS,
    _GET_CONFIG_EXAMPLE,
    _LIST_CONFIG_VERSIONS_DOCSTRINGS,
    _LIST_CONFIG_VERSIONS_EXAMPLE,
    apply_config as apply_config,
    get_config as get_config,
    list_config_versions as list_config_versions,
)
from anyscale.scheduler.models import (
    SchedulerConfig,
    SchedulerConfigVersion,
    SchedulerConfigVersionSummary,
)


class SchedulerSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateSchedulerSDK(
            client=client, logger=logger, timer=timer,
        )

    @sdk_docs(
        doc_py_example=_APPLY_CONFIG_EXAMPLE, arg_docstrings=_APPLY_CONFIG_DOCSTRINGS,
    )
    def apply_config(  # noqa: F811
        self, config: Union[SchedulerConfig, Dict[str, Any]],
    ) -> int:
        """Apply a scheduler config (creates a new active version). Returns the new version number."""
        return self._private_sdk.apply_config(config)

    @sdk_docs(
        doc_py_example=_GET_CONFIG_EXAMPLE, arg_docstrings=_GET_CONFIG_DOCSTRINGS,
    )
    def get_config(  # noqa: F811
        self, version: Optional[int] = None,
    ) -> SchedulerConfigVersion:
        """Get the active scheduler config (or a specific version)."""
        return self._private_sdk.get_config(version=version)

    @sdk_docs(
        doc_py_example=_LIST_CONFIG_VERSIONS_EXAMPLE,
        arg_docstrings=_LIST_CONFIG_VERSIONS_DOCSTRINGS,
    )
    def list_config_versions(  # noqa: F811
        self, max_items: int = 10,
    ) -> List[SchedulerConfigVersionSummary]:
        """List scheduler config version history (newest first)."""
        return self._private_sdk.list_config_versions(max_items=max_items)
