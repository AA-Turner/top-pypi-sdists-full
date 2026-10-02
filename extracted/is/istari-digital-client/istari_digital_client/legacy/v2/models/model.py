from __future__ import annotations

import os
import pprint
import re  # noqa: F401
import json

from pathlib import Path
from datetime import datetime
from pydantic import ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set, Union, TypeAlias
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.control_tag import ControlTag
from istari_digital_client.legacy.v2.models.artifact import Artifact
from istari_digital_client.legacy.v2.models.comment import Comment
from istari_digital_client.legacy.v2.models.file import File
from istari_digital_client.legacy.v2.models.job import Job
from istari_digital_client.legacy.v2.models.resource_archive_status import (
    ResourceArchiveStatus,
)
from istari_digital_client.legacy.v2.models.shareable import Shareable
from istari_digital_client.legacy.v2.models.file_having import FileHaving
from istari_digital_client.legacy.v2.models.archivable import Archivable
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.v2.models.new_credential_binding import NewCredentialBinding
from istari_digital_client.legacy.v2.models.new_source import NewSource
from istari_digital_client.legacy.v2.models.os import OS
from istari_digital_client.legacy.log_utils import log_method

PathLike = Union[str, os.PathLike, Path]
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None


class Model(FileHaving, ClientHaving, Shareable, Archivable):
    """
    Represents a model resource that includes associated files, artifacts, jobs, and metadata.

    This class supports archive functionality, job association, and client interactions.
    """

    id: StrictStr
    created: datetime
    file: File
    comments: List[Comment]
    archive_status_history: List[ResourceArchiveStatus]
    created_by_id: StrictStr
    artifacts: List[Artifact]
    jobs: Optional[List[Job]] = None
    control_tags: Optional[List[ControlTag]] = None
    __client_fields__: ClassVar[List[str]] = ["file", "comments", "artifacts", "jobs"]
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "file",
        "comments",
        "archive_status_history",
        "created_by_id",
        "artifacts",
        "jobs",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @log_method
    def add_job(
        self,
        function: str,
        *,
        parameters: JSON | None = None,
        parameters_file: PathLike | None = None,
        tool_name: str | None = None,
        tool_version: str | None = None,
        operating_system: OS | None = None,
        assigned_agent_id: str | None = None,
        assigned_agent_pool_id: str | None = None,
        agent_id: str | None = None,
        auth_bindings: list[NewCredentialBinding] | None = None,
        sources: list[NewSource | str] | None = None,
        description: str | None = None,
        version_name: str | None = None,
        external_identifier: str | None = None,
        display_name: str | None = None,
        **kwargs,
    ) -> Job:
        """
        Add a job associated with this model.

        This method wraps the client's ``add_job`` functionality, linking the job to the model's ID
        and optionally configuring parameters, tools, sources, and metadata.

        :param function: The function to run in the job.
        :type function: str
        :param parameters: Input parameters for the job (JSON-serializable), optional.
        :type parameters: JSON or None
        :param parameters_file: Path to a file containing parameters, optional.
        :type parameters_file: PathLike or None
        :param tool_name: The tool to execute, optional.
        :type tool_name: str or None
        :param tool_version: The version of the tool, optional.
        :type tool_version: str or None
        :param operating_system: Target OS for job execution, optional.
        :type operating_system: OS or None
        :param assigned_agent_id: Specific agent ID to assign the job, optional.
        :type assigned_agent_id: str or None
        :param assigned_agent_pool_id: Specific agent pool ID to assign the job, optional.
        :type assigned_agent_pool_id: str or None
        :param agent_id: Agent ID for the agent that created the job, optional.
        :type agent_id: str or None
        :param auth_bindings: Credential bindings for the function's ``auth_info`` inputs,
            optional. Each binding names a function input and the stored credential that
            will feed it when the job is claimed.
        :type auth_bindings: list[NewCredentialBinding] or None
        :param sources: Source revisions or new source definitions, optional.
        :type sources: list[NewSource or str] or None
        :param description: Job description, optional.
        :type description: str or None
        :param version_name: Version name for tracking, optional.
        :type version_name: str or None
        :param external_identifier: External ID for cross-referencing, optional.
        :type external_identifier: str or None
        :param display_name: Human-friendly name for the job, optional.
        :type display_name: str or None
        :param kwargs: Additional client arguments.
        :raises ValueError: If client is not set.
        """

        if not self.client:
            raise ValueError("Client is not set. Please set the client before calling this method.")

        return self.client.add_job(
            self.id,
            function,
            parameters=parameters,
            parameters_file=parameters_file,
            tool_name=tool_name,
            tool_version=tool_version,
            operating_system=operating_system,
            assigned_agent_id=assigned_agent_id,
            assigned_agent_pool_id=assigned_agent_pool_id,
            agent_id=agent_id,
            auth_bindings=auth_bindings,
            sources=sources,
            description=description,
            version_name=version_name,
            external_identifier=external_identifier,
            display_name=display_name,
            **kwargs,
        )

    @property
    @log_method
    def archive_status(self) -> ResourceArchiveStatus:
        """
        Get the current archive status of the artifact.

        This is derived from the last entry in the ``archive_status_history`` list.
        """

        return self.archive_status_history[-1]

    def to_str(self) -> str:
        """
        Return the string representation of the model using field aliases.

        This method serializes the model to a JSON-formatted string, respecting any defined aliases
        for fields instead of their original attribute names.
        """
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """
        Return the JSON string representation of the model using field aliases.

        This method serializes the model into a JSON-formatted string, using aliases for field names
        where defined instead of their raw attribute names.
        """
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """
        Create an instance of the model from a JSON string.

        This method deserializes the given JSON string into a model instance. It expects the
        string to match the model's schema, using field aliases where applicable.

        :param json_str: JSON string representing the model.
        :type json_str: str
        """
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """
        Return the dictionary representation of the model using field aliases.

        This method differs from calling `self.model_dump(by_alias=True)` in the following way:

        - Fields with a value of `None` are included in the output only if they are nullable and
          were explicitly set during model initialization. All other `None` fields are omitted.
        """
        excluded_fields: Set[str] = set([])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of file
        if self.file:
            _dict["file"] = self.file.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in comments (list)
        _items = []
        if self.comments:
            for _item_comments in self.comments:
                if _item_comments:
                    _items.append(_item_comments.to_dict())
            _dict["comments"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in archive_status_history (list)
        _items = []
        if self.archive_status_history:
            for _item_archive_status_history in self.archive_status_history:
                if _item_archive_status_history:
                    _items.append(_item_archive_status_history.to_dict())
            _dict["archive_status_history"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in artifacts (list)
        _items = []
        if self.artifacts:
            for _item_artifacts in self.artifacts:
                if _item_artifacts:
                    _items.append(_item_artifacts.to_dict())
            _dict["artifacts"] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in jobs (list)
        _items = []
        if self.jobs:
            for _item_jobs in self.jobs:
                if _item_jobs:
                    _items.append(_item_jobs.to_dict())
            _dict["jobs"] = _items

        # override the default output from pydantic by calling `to_dict()` of each item in control_tags (list)
        _items = []
        if self.control_tags:
            for _item_control_tags in self.control_tags:
                if _item_control_tags:
                    _items.append(_item_control_tags.to_dict())
            _dict["control_tags"] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """
        Create an instance of the model from a dictionary.

        This method deserializes a dictionary into a model instance. The input should use
        field aliases where applicable.

        :param obj: Dictionary representing the model.
        :type obj: Optional[Dict[str, Any]]
        """
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "id": obj.get("id"),
                "created": obj.get("created"),
                "file": File.from_dict(obj["file"])
                if obj.get("file") is not None
                else None,
                "comments": [Comment.from_dict(_item) for _item in obj["comments"]]
                if obj.get("comments") is not None
                else None,
                "archive_status_history": [
                    ResourceArchiveStatus.from_dict(_item)
                    for _item in obj["archive_status_history"]
                ]
                if obj.get("archive_status_history") is not None
                else None,
                "created_by_id": obj.get("created_by_id"),
                "artifacts": [Artifact.from_dict(_item) for _item in obj["artifacts"]]
                if obj.get("artifacts") is not None
                else None,
                "jobs": [Job.from_dict(_item) for _item in obj["jobs"]]
                if obj.get("jobs") is not None
                else None,
                "control_tags": [
                    ControlTag.from_dict(_item) for _item in obj["control_tags"]
                ]
                if obj.get("control_tags") is not None
                else None,
            }
        )
        return _obj
