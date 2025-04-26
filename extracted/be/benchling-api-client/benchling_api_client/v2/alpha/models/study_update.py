from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.fields import Fields
from ..models.study_update_phase import StudyUpdatePhase
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudyUpdate")


@attr.s(auto_attribs=True, repr=False)
class StudyUpdate:
    """  """

    _archive_reason: Union[Unset, str] = UNSET
    _description: Union[Unset, str] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _folder_id: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _is_archived: Union[Unset, bool] = UNSET
    _name: Union[Unset, str] = UNSET
    _phase: Union[Unset, StudyUpdatePhase] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_reason={}".format(repr(self._archive_reason)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("is_archived={}".format(repr(self._is_archived)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("phase={}".format(repr(self._phase)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "StudyUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_reason = self._archive_reason
        description = self._description
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        folder_id = self._folder_id
        id = self._id
        is_archived = self._is_archived
        name = self._name
        phase: Union[Unset, int] = UNSET
        if not isinstance(self._phase, Unset):
            phase = self._phase.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_reason is not UNSET:
            field_dict["archiveReason"] = archive_reason
        if description is not UNSET:
            field_dict["description"] = description
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if id is not UNSET:
            field_dict["id"] = id
        if is_archived is not UNSET:
            field_dict["isArchived"] = is_archived
        if name is not UNSET:
            field_dict["name"] = name
        if phase is not UNSET:
            field_dict["phase"] = phase

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_archive_reason() -> Union[Unset, str]:
            archive_reason = d.pop("archiveReason")
            return archive_reason

        try:
            archive_reason = get_archive_reason()
        except KeyError:
            if strict:
                raise
            archive_reason = cast(Union[Unset, str], UNSET)

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, str], UNSET)

        def get_fields() -> Union[Unset, Fields]:
            fields: Union[Unset, Union[Unset, Fields]] = UNSET
            _fields = d.pop("fields")

            if not isinstance(_fields, Unset):
                fields = Fields.from_dict(_fields)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, Fields], UNSET)

        def get_folder_id() -> Union[Unset, str]:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_is_archived() -> Union[Unset, bool]:
            is_archived = d.pop("isArchived")
            return is_archived

        try:
            is_archived = get_is_archived()
        except KeyError:
            if strict:
                raise
            is_archived = cast(Union[Unset, bool], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_phase() -> Union[Unset, StudyUpdatePhase]:
            phase = UNSET
            _phase = d.pop("phase")
            if _phase is not None and _phase is not UNSET:
                try:
                    phase = StudyUpdatePhase(_phase)
                except ValueError:
                    phase = StudyUpdatePhase.of_unknown(_phase)

            return phase

        try:
            phase = get_phase()
        except KeyError:
            if strict:
                raise
            phase = cast(Union[Unset, StudyUpdatePhase], UNSET)

        study_update = cls(
            archive_reason=archive_reason,
            description=description,
            fields=fields,
            folder_id=folder_id,
            id=id,
            is_archived=is_archived,
            name=name,
            phase=phase,
        )

        study_update.additional_properties = d
        return study_update

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties

    def get(self, key, default=None) -> Optional[Any]:
        return self.additional_properties.get(key, default)

    @property
    def archive_reason(self) -> str:
        if isinstance(self._archive_reason, Unset):
            raise NotPresentError(self, "archive_reason")
        return self._archive_reason

    @archive_reason.setter
    def archive_reason(self, value: str) -> None:
        self._archive_reason = value

    @archive_reason.deleter
    def archive_reason(self) -> None:
        self._archive_reason = UNSET

    @property
    def description(self) -> str:
        """ The description of the Study. """
        if isinstance(self._description, Unset):
            raise NotPresentError(self, "description")
        return self._description

    @description.setter
    def description(self, value: str) -> None:
        self._description = value

    @description.deleter
    def description(self) -> None:
        self._description = UNSET

    @property
    def fields(self) -> Fields:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: Fields) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def folder_id(self) -> str:
        """ ID of the folder that contains the Study. """
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: str) -> None:
        self._folder_id = value

    @folder_id.deleter
    def folder_id(self) -> None:
        self._folder_id = UNSET

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
    def is_archived(self) -> bool:
        if isinstance(self._is_archived, Unset):
            raise NotPresentError(self, "is_archived")
        return self._is_archived

    @is_archived.setter
    def is_archived(self, value: bool) -> None:
        self._is_archived = value

    @is_archived.deleter
    def is_archived(self) -> None:
        self._is_archived = UNSET

    @property
    def name(self) -> str:
        """ Name of the Study. """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def phase(self) -> StudyUpdatePhase:
        """ The phase of the Study. """
        if isinstance(self._phase, Unset):
            raise NotPresentError(self, "phase")
        return self._phase

    @phase.setter
    def phase(self, value: StudyUpdatePhase) -> None:
        self._phase = value

    @phase.deleter
    def phase(self) -> None:
        self._phase = UNSET
