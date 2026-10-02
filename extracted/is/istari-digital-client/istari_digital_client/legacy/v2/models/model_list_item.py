from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List
from typing import Optional, Set, TYPE_CHECKING
from typing_extensions import Self

from istari_digital_client.legacy.v2.models.file_having import FileHaving
from istari_digital_client.legacy.mixin import ClientHaving
from istari_digital_client.legacy.v2.models.file import File
from istari_digital_client.legacy.log_utils import log_method

if TYPE_CHECKING:
    from istari_digital_client.legacy.v2.models.model import Model
    from istari_digital_client.legacy.v2.models.page_artifact import PageArtifact
    from istari_digital_client.legacy.v2.models.page_comment import PageComment
    from istari_digital_client.legacy.v2.models.page_job import PageJob


class ModelListItem(FileHaving, ClientHaving):
    """
    Model class representing a simplified summary of a Model.

    This class contains only UUID references for related sub-resources such as
    comments, artifacts, and jobs. Use the ``model``, ``comments``, ``artifacts``,
    and ``jobs`` properties to resolve full objects via the client.
    """

    id: StrictStr
    created: datetime
    file: File
    archive_status: StrictStr
    created_by_id: StrictStr
    comment_ids: Optional[List[StrictStr]] = None
    artifact_ids: Optional[List[StrictStr]] = None
    job_ids: Optional[List[StrictStr]] = None
    __client_fields__: ClassVar[List[str]] = ["file"]
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "file",
        "archive_status",
        "created_by_id",
        "comment_ids",
        "artifact_ids",
        "job_ids",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

    @property
    @log_method
    def model(self) -> Optional["Model"]:
        """
        Retrieve the full :class:`Model` instance corresponding to this list item.

        :raises ValueError: If the client is not set.
        """

        if not self.client:
            return None
        return self.client.get_model(self.id)

    @property
    @log_method
    def comments(self) -> Optional[PageComment]:
        """
        Retrieve the paginated list of model comments.

        This requires that ``comment_ids`` is not empty and that the client is set.

        """

        if not self.comment_ids or not self.client:
            return None
        return self.client.list_model_comments(self.id)

    @property
    @log_method
    def artifacts(self) -> Optional[PageArtifact]:
        """
        Retrieve the paginated list of artifacts for this model.

        This requires that ``artifact_ids`` is not empty and that the client is set.
        """
        if not self.artifact_ids or not self.client:
            return None
        return self.client.list_model_artifacts(self.id)

    @property
    @log_method
    def jobs(self) -> Optional[PageJob]:
        """
        Retrieve the paginated list of jobs associated with this model.

        This requires that ``job_ids`` is not empty and that the client is set.
        """
        if not self.job_ids or not self.client:
            return None
        return self.client.list_model_jobs(self.id)

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
                "archive_status": obj.get("archive_status"),
                "created_by_id": obj.get("created_by_id"),
                "comment_ids": obj.get("comment_ids"),
                "artifact_ids": obj.get("artifact_ids"),
                "job_ids": obj.get("job_ids"),
            }
        )
        return _obj
