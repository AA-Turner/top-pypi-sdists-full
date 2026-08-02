# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

import attrs
import emoji
from lance_namespace import DescribeTableRequest

from geneva import DEFAULT_UPLOAD_DIR
from geneva.config import ConfigBase
from geneva.tqdm import tqdm

if TYPE_CHECKING:
    from pathlib import Path

    from geneva.db import NamespaceConfig

_LOG = logging.getLogger(__name__)


def make_upload_path(filename: str) -> str:
    """Make the remote path for uploading a file via namespace file session.

    When using ds.new_file_session(), the session is rooted at the dataset
    directory. This function constructs the path including the _geneva_uploads
    subdirectory.
    """
    return f"{DEFAULT_UPLOAD_DIR}/{filename}"


# Suppress verbose Azure SDK HTTP logging
logging.getLogger("azure.core.pipeline.policies.http_logging_policy").setLevel(
    logging.WARNING
)


@attrs.define
class Uploader(ConfigBase):
    """
    This class is used to upload files to a specified directory.

    Uploads are always performed through ``LanceFileSession`` so namespace
    credential vending is the single storage access path.

    Upload directories are automatically derived to be table-specific:
    - For namespace tables: {table_location}/_geneva_uploads
    """

    upload_dir: Optional[str] = attrs.field(default=None)
    namespace_config: Optional[NamespaceConfig] = attrs.field(default=None)
    table_id: Optional[list[str]] = attrs.field(default=None)
    storage_options: Optional[dict[str, str]] = attrs.field(default=None, repr=False)

    # Cached namespace resources (initialized lazily in __attrs_post_init__)
    _file_session: Any = attrs.field(default=None, init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        ns = self.namespace_config
        if self.upload_dir is not None:
            raise ValueError(
                "upload_dir cannot be specified. Uploads automatically use the "
                "_geneva_uploads folder inside the table location via file session."
            )
        if not (
            ns
            and ns.namespace_client_impl
            and ns.namespace_client_properties
            and self.table_id
        ):
            raise ValueError("Uploader requires table_id and namespace credentials")

        namespace_client = ns.connect_namespace_client()
        assert namespace_client is not None
        response = namespace_client.describe_table(
            DescribeTableRequest(id=self.table_id)
        )
        if response.location is None:
            raise ValueError(f"Table location is None for table {self.table_id}")

        location = response.location.rstrip("?").rstrip("/")
        self.upload_dir = f"{location}/{DEFAULT_UPLOAD_DIR}"
        _LOG.info(f"Derived namespace table upload_dir: {self.upload_dir}")

        from geneva.db import open_lance_dataset

        vended_storage_options = getattr(response, "storage_options", None)
        effective_storage_options = vended_storage_options or self.storage_options
        ds = open_lance_dataset(
            namespace_client=namespace_client,
            table_id=self.table_id,
            storage_options=effective_storage_options,
        )
        self._file_session = ds.new_file_session()

    @classmethod
    def name(cls) -> str:
        return "uploader"

    def _make_upload_path(self, filename: str) -> str:
        """Make the remote path for uploading a file via namespace file session."""
        return make_upload_path(filename)

    def _file_exists(self, f: Path) -> bool:
        try:
            return self._file_session.contains(self._make_upload_path(f.name))
        except Exception:
            _LOG.exception(f"Failed to check if file exists: {f.name}")
            return False

    def _upload_lance_session(self, f: Path) -> str:
        """
        Upload using dataset's file session (with automatic multi-part upload support).

        Uses the cached file session initialized in __attrs_post_init__ which
        inherits the dataset's storage configuration.
        """
        assert self._file_session is not None, "file_session must be initialized"
        assert self.upload_dir is not None, "upload_dir must be set"

        remote_path = self._make_upload_path(f.name)

        # Upload with progress bar
        with tqdm(
            total=f.stat().st_size, unit="B", unit_scale=True, unit_divisor=1024
        ) as pbar:
            pbar.set_description(
                emoji.emojize(f":cloud: uploading {f.name} to {self.upload_dir}")
            )

            # Upload the file - multi-part upload happens automatically for files > 5MB
            self._file_session.upload_file(str(f), remote_path)
            pbar.update(f.stat().st_size)
        return f"{self.upload_dir}/{f.name}"

    def upload(self, f: Path) -> str:
        """
        Upload a file to the specified directory.

        The name of the object will be in the form of
        <path_to_upload_dir>/<name_of_file>
        """
        if self._file_exists(f):
            _LOG.debug(
                f"File {f.name} already exists in {self.upload_dir}, skipping upload"
            )
            return f"{self.upload_dir}/{f.name}"

        return self._upload_lance_session(f)
