#  Copyright 2025 DataRobot, Inc. and its affiliates.
#
#  All rights reserved.
#
#  DataRobot, Inc. Confidential.
#
#  This is unpublished proprietary source code of DataRobot, Inc.
#  and its affiliates.
#
#  The copyright notice above does not evidence any actual or intended
#  publication of such source code.


"""That's a non-public extension of GA Files model."""
from __future__ import annotations

from io import IOBase
import os
from typing import Iterable, List, Optional, cast

import trafaret as t

from datarobot._compat import String
from datarobot.enums import DEFAULT_MAX_WAIT, DEFAULT_TIMEOUT
from datarobot.models.api_object import APIObject
from datarobot.models.files import Files
from datarobot.models.user_blueprints.models import HumanReadable
from datarobot.utils.waiters import wait_for_async_resolution

_files_stage_schema = t.Dict({"catalog_id": String, "stage_id": String}).ignore_extra("*")


class FilesExperimental(Files):
    """A not yet documented extension for an existing `Files` entity."""

    def clone(
        self,
        *,
        omit: str | List[str] | None = None,
        wait_for_completion: bool = True,
        max_wait: int = DEFAULT_MAX_WAIT,
    ) -> Files:
        """Duplicate the files container.

        Parameters
        ----------
        omit:
            Don't duplicate some files.
        wait_for_completion:
            Set to *False* if you don't want to wait for the operation completion.
        max_wait:
            Raise AsyncTimeoutError if wait_for_completion=True
            and the operation took more than this number of seconds.
        """
        url = f"files/{self.id}/clone/"

        if isinstance(omit, str):
            omit = [omit]

        response = self._client.post(url, data={"omit": omit})
        return self._get_files_from_async(
            response, wait_for_completion=wait_for_completion, max_wait=max_wait
        )

    def create_stage(self) -> "FilesStage":
        """Create a new `FilesStage` for this files container."""
        response = self._client.post(f"files/{self.id}/stages/")
        return FilesStage.from_server_data(response.json())

    def apply_stage(self, stage: "FilesStage") -> None:
        file = stage.apply()
        self.num_files = file.num_files

    def copy(
        self,
        source_path: str | Iterable[str],
        *,
        target: str | None = None,
        target_files: Optional["Files"] = None,
        max_wait: int = DEFAULT_MAX_WAIT,
        wait_for_completion: bool = True,
    ) -> "Files":
        """Copy file(s) and/or folder(s) within the same or into another files container.

        Parameters
        ----------
        source_path
            file(s) and/or folder(s) to copy.
        target
            Either a folder to copy file(s) into
            or a new file name if only one file is being copied.
        target_files
            Files collection to copy files into.
        max_wait
             Raise TimeoutError if the operation took more than this number of seconds to complete.
        """
        if isinstance(source_path, str):
            sources = [source_path]
        elif isinstance(source_path, Iterable):
            sources = list(source_path)
        else:
            raise ValueError(source_path)

        url = f"files/{self.id}/copyBatch/"
        response = self._client.post(
            url,
            json={
                "sources": sources,
                "target": target,
                "targetCatalogId": target_files and target_files.id,
            },
        )
        return self._get_files_from_async(
            response, max_wait=max_wait, wait_for_completion=wait_for_completion
        )

    def wait_for_completion(self) -> None:
        """Wait for initial upload completion."""
        if self._async_status_location is None:
            return

        catalog_item_data = wait_for_async_resolution(self._client, self._async_status_location)

        new_file = Files.from_server_data(catalog_item_data)
        self.num_files = new_file.num_files
        self.from_archive = new_file.from_archive
        self._async_status_location = None


class FilesStage(APIObject, HumanReadable):
    """A place to accumulate multiple uploaded files
    before they're added into corresponding files container.

    .. versionadded:: v3.9

    Attributes
    ----------
    catalog_id: str
        The unique identifier for the files container.
        The `FilesStage` can be applied only to that files container.
    stage_id: str
        The unique identifier for the `FilesStage` object.
    """

    _converter = _files_stage_schema

    def __init__(self, catalog_id: str, stage_id: str):
        self.catalog_id = catalog_id
        self.stage_id = stage_id

    def apply(self) -> Files:
        """Add the files uploaded into this `FilesStage` into the corresponding files container.
        You can call this method only once for a particular `FilesStage`.
        """
        url = f"files/{self.catalog_id}/fromStage/"
        response = self._client.post(url, json={"stageId": self.stage_id})
        return Files.get(response.json()["catalogId"])

    def upload(self, source: str | IOBase, file_name: str | None = None) -> None:
        """Upload a file into the `FilesStage`.

        Parameters
        ----------
        source: str | IOBase
            Local file path or a file-like object to upload.
        file_name: str
            The file name to apply on the server side.
        """
        url = f"files/{self.catalog_id}/stages/{self.stage_id}/upload/"

        if isinstance(source, str):
            fname = file_name or os.path.basename(source)
            self._client.build_request_with_file(
                method="post",
                url=url,
                fname=fname,
                file_path=source,
                read_timeout=DEFAULT_TIMEOUT.UPLOAD,
            )
        else:
            fname = cast(str, getattr(source, "name", file_name))
            self._client.build_request_with_file(
                method="post",
                url=url,
                fname=fname,
                filelike=source,
                read_timeout=DEFAULT_TIMEOUT.UPLOAD,
            )
