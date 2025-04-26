import datetime
from typing import Any, cast, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.form_definition_version import FormDefinitionVersion
from ..types import UNSET, Unset

T = TypeVar("T", bound="FormDefinition")


@attr.s(auto_attribs=True, repr=False)
class FormDefinition:
    """  """

    _id: Union[Unset, str] = UNSET
    _latest_version: Union[Unset, FormDefinitionVersion] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _name: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("id={}".format(repr(self._id)))
        fields.append("latest_version={}".format(repr(self._latest_version)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name={}".format(repr(self._name)))
        return "FormDefinition({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        id = self._id
        latest_version: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._latest_version, Unset):
            latest_version = self._latest_version.to_dict()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        name = self._name

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if id is not UNSET:
            field_dict["id"] = id
        if latest_version is not UNSET:
            field_dict["latestVersion"] = latest_version
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_latest_version() -> Union[Unset, FormDefinitionVersion]:
            latest_version: Union[Unset, Union[Unset, FormDefinitionVersion]] = UNSET
            _latest_version = d.pop("latestVersion")

            if not isinstance(_latest_version, Unset):
                latest_version = FormDefinitionVersion.from_dict(_latest_version)

            return latest_version

        try:
            latest_version = get_latest_version()
        except KeyError:
            if strict:
                raise
            latest_version = cast(Union[Unset, FormDefinitionVersion], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        form_definition = cls(
            id=id,
            latest_version=latest_version,
            modified_at=modified_at,
            name=name,
        )

        return form_definition

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def latest_version(self) -> FormDefinitionVersion:
        if isinstance(self._latest_version, Unset):
            raise NotPresentError(self, "latest_version")
        return self._latest_version

    @latest_version.setter
    def latest_version(self, value: FormDefinitionVersion) -> None:
        self._latest_version = value

    @latest_version.deleter
    def latest_version(self) -> None:
        self._latest_version = UNSET

    @property
    def modified_at(self) -> datetime.datetime:
        """ Time when the definition was last modified. Will be updated when a new version becomes the default """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET
