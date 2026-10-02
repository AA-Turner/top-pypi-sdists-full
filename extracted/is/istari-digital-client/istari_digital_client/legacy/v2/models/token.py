from __future__ import annotations
import pprint
import re  # noqa: F401
import json
import uuid

import datetime
from pydantic import BaseModel, ConfigDict, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Set
from typing_extensions import Self

from istari_digital_client.legacy.log_utils import log_method

import istari_digital_core


class Token(BaseModel):
    """
    Represents a cryptographic token used for verifying the integrity of binary content.

    A token encapsulates the SHA digest and salt used to verify the contents of a file.
    It is generated and validated using core functionality from ``istari_digital_core``.
    """

    id: StrictStr
    created: datetime.datetime
    sha: StrictStr
    salt: StrictStr
    created_by_id: Optional[StrictStr] = None
    __properties: ClassVar[List[str]] = [
        "id",
        "created",
        "sha",
        "salt",
        "created_by_id",
    ]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )

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
        # set to None if created_by_id (nullable) is None
        # and model_fields_set contains the field
        if self.created_by_id is None and "created_by_id" in self.model_fields_set:
            _dict["created_by_id"] = None

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
                "sha": obj.get("sha"),
                "salt": obj.get("salt"),
                "created_by_id": obj.get("created_by_id"),
            }
        )
        return _obj

    @classmethod
    @log_method
    def from_storage_token(
        cls,
        storage_token: istari_digital_core.Token,
    ) -> Self:
        """
        Create a :class:`Token` instance from a core :class:`istari_digital_core.Token`.

        This assigns a new UUID and sets the current UTC timestamp for ``created``.

        :param storage_token: A token object from the istari core package.
        """
        return cls(
            id=str(uuid.uuid4()),
            created=datetime.datetime.now(datetime.timezone.utc),
            sha=storage_token.sha,
            salt=storage_token.salt,
        )

    @classmethod
    @log_method
    def compare_token(
        cls,
        sha: str,
        salt: str,
        data: bytes,
    ) -> None:
        """
        Verify the integrity of a token against a given binary payload.

        Raises a ``ValueError`` if the SHA+salt digest does not match the provided data.

        :param sha: The expected SHA digest.
        :param salt: The salt used during hashing.
        :param data: The raw bytes to verify.
        :raises ValueError: If the provided data does not match the token hash.
        """
        try:
            istari_digital_core.Token.compare_token(sha, salt, data)
        except ValueError as e:
            raise ValueError("Token does not match the data") from e

    @classmethod
    @log_method
    def from_bytes(
        cls,
        data: bytes,
        salt: str | None = None,
    ) -> Self:
        """
        Create a token from a byte string and an optional salt.

        Internally computes the SHA digest and wraps the result in a new Token instance.

        :param data: The content to hash.
        :param salt: Optional salt to apply during hashing.
        """
        return cls.from_storage_token(istari_digital_core.Token.from_bytes(data, salt))
