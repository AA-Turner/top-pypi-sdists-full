from typing import Optional, Union

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.compute_config._private.compute_config_sdk import PrivateComputeConfigSDK
from anyscale.compute_config.commands import (
    _ARCHIVE_ARG_DOCSTRINGS,
    _ARCHIVE_EXAMPLE,
    _CREATE_ARG_DOCSTRINGS,
    _CREATE_EXAMPLE,
    _GET_ARG_DOCSTRINGS,
    _GET_EXAMPLE,
    archive,
    create,
    get,
)
from anyscale.compute_config.models import (
    ComputeConfig,
    ComputeConfigVersion,
    HeadNodeConfig,
    WorkerNodeGroupConfig,
)


class ComputeConfigSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateComputeConfigSDK(
            client=client, logger=logger, timer=timer
        )

    @sdk_docs(
        doc_py_example=_CREATE_EXAMPLE, arg_docstrings=_CREATE_ARG_DOCSTRINGS,
    )
    def create(  # noqa: F811
        self, config: ComputeConfig, *, name: Optional[str],
    ) -> str:
        """Create a new version of a compute config.

        Returns the full name of the registered compute config, including the version.
        """
        full_name, _ = self._private_sdk.create_compute_config(config, name=name)
        return full_name

    @sdk_docs(
        doc_py_example=_GET_EXAMPLE, arg_docstrings=_GET_ARG_DOCSTRINGS,
    )
    def get(  # noqa: F811
        self, name: str, *, include_archived: bool = False, _id: Optional[str] = None,
    ) -> ComputeConfigVersion:
        """Get the compute config with the specified name.

        The name can contain an optional version tag, i.e., 'name:version'.
        If no version is provided, the latest one will be returned.
        """
        # NOTE(edoakes): I want to avoid exposing fetching by ID in the public API,
        # but it's needed for parity with the existing CLI. Therefore I am adding it
        # as a hidden private API that can be used like: (`name="", _id=id`).
        return self._private_sdk.get_compute_config(
            name=name or None, id=_id, include_archived=include_archived
        )

    @sdk_docs(
        doc_py_example=_ARCHIVE_EXAMPLE, arg_docstrings=_ARCHIVE_ARG_DOCSTRINGS,
    )
    def archive(self, name: str, *, _id: Optional[str] = None):  # noqa: F811
        """Archive a compute config and all of its versions.

        The name can contain an optional version, e.g., 'name:version'.
        If no version is provided, the latest one will be archived.

        Once a compute config is archived, its name will no longer be usable in the organization.
        """
        # NOTE(edoakes): I want to avoid exposing fetching by ID in the public API,
        # but it's needed for parity with the existing CLI. Therefore I am adding it
        # as a hidden private API that can be used like: (`name="", _id=id`).
        return self._private_sdk.archive_compute_config(name=name or None, id=_id,)
