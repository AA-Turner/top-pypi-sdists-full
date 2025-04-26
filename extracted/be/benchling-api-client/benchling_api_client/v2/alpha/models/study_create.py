from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.entry_create import EntryCreate
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="StudyCreate")


@attr.s(auto_attribs=True, repr=False)
class StudyCreate:
    """  """

    _entry_information: EntryCreate
    _fields: Fields
    _folder_id: str
    _name: str
    _study_schema_id: str
    _description: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("entry_information={}".format(repr(self._entry_information)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("study_schema_id={}".format(repr(self._study_schema_id)))
        fields.append("description={}".format(repr(self._description)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "StudyCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        entry_information = self._entry_information.to_dict()

        fields = self._fields.to_dict()

        folder_id = self._folder_id
        name = self._name
        study_schema_id = self._study_schema_id
        description = self._description

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if entry_information is not UNSET:
            field_dict["entryInformation"] = entry_information
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if study_schema_id is not UNSET:
            field_dict["studySchemaId"] = study_schema_id
        if description is not UNSET:
            field_dict["description"] = description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_entry_information() -> EntryCreate:
            entry_information = EntryCreate.from_dict(d.pop("entryInformation"), strict=False)

            return entry_information

        try:
            entry_information = get_entry_information()
        except KeyError:
            if strict:
                raise
            entry_information = cast(EntryCreate, UNSET)

        def get_fields() -> Fields:
            fields = Fields.from_dict(d.pop("fields"), strict=False)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Fields, UNSET)

        def get_folder_id() -> str:
            folder_id = d.pop("folderId")
            return folder_id

        try:
            folder_id = get_folder_id()
        except KeyError:
            if strict:
                raise
            folder_id = cast(str, UNSET)

        def get_name() -> str:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(str, UNSET)

        def get_study_schema_id() -> str:
            study_schema_id = d.pop("studySchemaId")
            return study_schema_id

        try:
            study_schema_id = get_study_schema_id()
        except KeyError:
            if strict:
                raise
            study_schema_id = cast(str, UNSET)

        def get_description() -> Union[Unset, str]:
            description = d.pop("description")
            return description

        try:
            description = get_description()
        except KeyError:
            if strict:
                raise
            description = cast(Union[Unset, str], UNSET)

        study_create = cls(
            entry_information=entry_information,
            fields=fields,
            folder_id=folder_id,
            name=name,
            study_schema_id=study_schema_id,
            description=description,
        )

        study_create.additional_properties = d
        return study_create

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
    def entry_information(self) -> EntryCreate:
        if isinstance(self._entry_information, Unset):
            raise NotPresentError(self, "entry_information")
        return self._entry_information

    @entry_information.setter
    def entry_information(self, value: EntryCreate) -> None:
        self._entry_information = value

    @property
    def fields(self) -> Fields:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: Fields) -> None:
        self._fields = value

    @property
    def folder_id(self) -> str:
        """ ID of the folder that contains the Study. """
        if isinstance(self._folder_id, Unset):
            raise NotPresentError(self, "folder_id")
        return self._folder_id

    @folder_id.setter
    def folder_id(self, value: str) -> None:
        self._folder_id = value

    @property
    def name(self) -> str:
        """ Name of the Study. """
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def study_schema_id(self) -> str:
        """ The ID of the Study's schema. """
        if isinstance(self._study_schema_id, Unset):
            raise NotPresentError(self, "study_schema_id")
        return self._study_schema_id

    @study_schema_id.setter
    def study_schema_id(self, value: str) -> None:
        self._study_schema_id = value

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
