from typing import Any, cast, Dict, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="EntryTemplateUpdate")


@attr.s(auto_attribs=True, repr=False)
class EntryTemplateUpdate:
    """  """

    _fields: Union[Unset, Fields] = UNSET
    _modified_at: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _schema_id: Union[Unset, str] = UNSET
    _template_collection_id: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("schema_id={}".format(repr(self._schema_id)))
        fields.append("template_collection_id={}".format(repr(self._template_collection_id)))
        return "EntryTemplateUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        modified_at = self._modified_at
        name = self._name
        schema_id = self._schema_id
        template_collection_id = self._template_collection_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if fields is not UNSET:
            field_dict["fields"] = fields
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
        if template_collection_id is not UNSET:
            field_dict["templateCollectionId"] = template_collection_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

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

        def get_modified_at() -> Union[Unset, str]:
            modified_at = d.pop("modifiedAt")
            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, str], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_schema_id() -> Union[Unset, str]:
            schema_id = d.pop("schemaId")
            return schema_id

        try:
            schema_id = get_schema_id()
        except KeyError:
            if strict:
                raise
            schema_id = cast(Union[Unset, str], UNSET)

        def get_template_collection_id() -> Union[Unset, str]:
            template_collection_id = d.pop("templateCollectionId")
            return template_collection_id

        try:
            template_collection_id = get_template_collection_id()
        except KeyError:
            if strict:
                raise
            template_collection_id = cast(Union[Unset, str], UNSET)

        entry_template_update = cls(
            fields=fields,
            modified_at=modified_at,
            name=name,
            schema_id=schema_id,
            template_collection_id=template_collection_id,
        )

        return entry_template_update

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
    def modified_at(self) -> str:
        """ DateTime the template was last modified """
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: str) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def name(self) -> str:
        """ Title of the template """
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
    def schema_id(self) -> str:
        """ ID of the schema for the entry """
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: str) -> None:
        self._schema_id = value

    @schema_id.deleter
    def schema_id(self) -> None:
        self._schema_id = UNSET

    @property
    def template_collection_id(self) -> str:
        """ ID of the collection that contains the template """
        if isinstance(self._template_collection_id, Unset):
            raise NotPresentError(self, "template_collection_id")
        return self._template_collection_id

    @template_collection_id.setter
    def template_collection_id(self, value: str) -> None:
        self._template_collection_id = value

    @template_collection_id.deleter
    def template_collection_id(self) -> None:
        self._template_collection_id = UNSET
