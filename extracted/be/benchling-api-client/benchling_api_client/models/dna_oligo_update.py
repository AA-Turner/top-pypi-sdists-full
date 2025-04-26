from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.custom_fields import CustomFields
from ..models.dna_annotation import DnaAnnotation
from ..models.fields import Fields
from ..types import UNSET, Unset

T = TypeVar("T", bound="DnaOligoUpdate")


@attr.s(auto_attribs=True, repr=False)
class DnaOligoUpdate:
    """  """

    _annotations: Union[Unset, List[DnaAnnotation]] = UNSET
    _helm: Union[Unset, str] = UNSET
    _custom_notation: Union[Unset, str] = UNSET
    _custom_notation_id: Union[Unset, str] = UNSET
    _aliases: Union[Unset, List[str]] = UNSET
    _author_ids: Union[Unset, List[str]] = UNSET
    _bases: Union[Unset, str] = UNSET
    _custom_fields: Union[Unset, CustomFields] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _folder_id: Union[Unset, str] = UNSET
    _name: Union[Unset, str] = UNSET
    _schema_id: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("annotations={}".format(repr(self._annotations)))
        fields.append("helm={}".format(repr(self._helm)))
        fields.append("custom_notation={}".format(repr(self._custom_notation)))
        fields.append("custom_notation_id={}".format(repr(self._custom_notation_id)))
        fields.append("aliases={}".format(repr(self._aliases)))
        fields.append("author_ids={}".format(repr(self._author_ids)))
        fields.append("bases={}".format(repr(self._bases)))
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("folder_id={}".format(repr(self._folder_id)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("schema_id={}".format(repr(self._schema_id)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "DnaOligoUpdate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        annotations: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._annotations, Unset):
            annotations = []
            for annotations_item_data in self._annotations:
                annotations_item = annotations_item_data.to_dict()

                annotations.append(annotations_item)

        helm = self._helm
        custom_notation = self._custom_notation
        custom_notation_id = self._custom_notation_id
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._aliases, Unset):
            aliases = self._aliases

        author_ids: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._author_ids, Unset):
            author_ids = self._author_ids

        bases = self._bases
        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._custom_fields, Unset):
            custom_fields = self._custom_fields.to_dict()

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        folder_id = self._folder_id
        name = self._name
        schema_id = self._schema_id

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if annotations is not UNSET:
            field_dict["annotations"] = annotations
        if helm is not UNSET:
            field_dict["helm"] = helm
        if custom_notation is not UNSET:
            field_dict["customNotation"] = custom_notation
        if custom_notation_id is not UNSET:
            field_dict["customNotationId"] = custom_notation_id
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if author_ids is not UNSET:
            field_dict["authorIds"] = author_ids
        if bases is not UNSET:
            field_dict["bases"] = bases
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if name is not UNSET:
            field_dict["name"] = name
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_annotations() -> Union[Unset, List[DnaAnnotation]]:
            annotations = []
            _annotations = d.pop("annotations")
            for annotations_item_data in _annotations or []:
                annotations_item = DnaAnnotation.from_dict(annotations_item_data, strict=False)

                annotations.append(annotations_item)

            return annotations

        try:
            annotations = get_annotations()
        except KeyError:
            if strict:
                raise
            annotations = cast(Union[Unset, List[DnaAnnotation]], UNSET)

        def get_helm() -> Union[Unset, str]:
            helm = d.pop("helm")
            return helm

        try:
            helm = get_helm()
        except KeyError:
            if strict:
                raise
            helm = cast(Union[Unset, str], UNSET)

        def get_custom_notation() -> Union[Unset, str]:
            custom_notation = d.pop("customNotation")
            return custom_notation

        try:
            custom_notation = get_custom_notation()
        except KeyError:
            if strict:
                raise
            custom_notation = cast(Union[Unset, str], UNSET)

        def get_custom_notation_id() -> Union[Unset, str]:
            custom_notation_id = d.pop("customNotationId")
            return custom_notation_id

        try:
            custom_notation_id = get_custom_notation_id()
        except KeyError:
            if strict:
                raise
            custom_notation_id = cast(Union[Unset, str], UNSET)

        def get_aliases() -> Union[Unset, List[str]]:
            aliases = cast(List[str], d.pop("aliases"))

            return aliases

        try:
            aliases = get_aliases()
        except KeyError:
            if strict:
                raise
            aliases = cast(Union[Unset, List[str]], UNSET)

        def get_author_ids() -> Union[Unset, List[str]]:
            author_ids = cast(List[str], d.pop("authorIds"))

            return author_ids

        try:
            author_ids = get_author_ids()
        except KeyError:
            if strict:
                raise
            author_ids = cast(Union[Unset, List[str]], UNSET)

        def get_bases() -> Union[Unset, str]:
            bases = d.pop("bases")
            return bases

        try:
            bases = get_bases()
        except KeyError:
            if strict:
                raise
            bases = cast(Union[Unset, str], UNSET)

        def get_custom_fields() -> Union[Unset, CustomFields]:
            custom_fields: Union[Unset, Union[Unset, CustomFields]] = UNSET
            _custom_fields = d.pop("customFields")

            if not isinstance(_custom_fields, Unset):
                custom_fields = CustomFields.from_dict(_custom_fields)

            return custom_fields

        try:
            custom_fields = get_custom_fields()
        except KeyError:
            if strict:
                raise
            custom_fields = cast(Union[Unset, CustomFields], UNSET)

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

        dna_oligo_update = cls(
            annotations=annotations,
            helm=helm,
            custom_notation=custom_notation,
            custom_notation_id=custom_notation_id,
            aliases=aliases,
            author_ids=author_ids,
            bases=bases,
            custom_fields=custom_fields,
            fields=fields,
            folder_id=folder_id,
            name=name,
            schema_id=schema_id,
        )

        dna_oligo_update.additional_properties = d
        return dna_oligo_update

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
    def annotations(self) -> List[DnaAnnotation]:
        """ Annotations on the Oligo. """
        if isinstance(self._annotations, Unset):
            raise NotPresentError(self, "annotations")
        return self._annotations

    @annotations.setter
    def annotations(self, value: List[DnaAnnotation]) -> None:
        self._annotations = value

    @annotations.deleter
    def annotations(self) -> None:
        self._annotations = UNSET

    @property
    def helm(self) -> str:
        """ Representation of the oligo in HELM syntax, including any chemical modifications """
        if isinstance(self._helm, Unset):
            raise NotPresentError(self, "helm")
        return self._helm

    @helm.setter
    def helm(self, value: str) -> None:
        self._helm = value

    @helm.deleter
    def helm(self) -> None:
        self._helm = UNSET

    @property
    def custom_notation(self) -> str:
        """ Representation of the sequence or oligo in the custom notation specified by customNotationId """
        if isinstance(self._custom_notation, Unset):
            raise NotPresentError(self, "custom_notation")
        return self._custom_notation

    @custom_notation.setter
    def custom_notation(self, value: str) -> None:
        self._custom_notation = value

    @custom_notation.deleter
    def custom_notation(self) -> None:
        self._custom_notation = UNSET

    @property
    def custom_notation_id(self) -> str:
        """ ID of the notation used to interpret the string provided in the customNotation field """
        if isinstance(self._custom_notation_id, Unset):
            raise NotPresentError(self, "custom_notation_id")
        return self._custom_notation_id

    @custom_notation_id.setter
    def custom_notation_id(self, value: str) -> None:
        self._custom_notation_id = value

    @custom_notation_id.deleter
    def custom_notation_id(self) -> None:
        self._custom_notation_id = UNSET

    @property
    def aliases(self) -> List[str]:
        """ Aliases to add to the Oligo """
        if isinstance(self._aliases, Unset):
            raise NotPresentError(self, "aliases")
        return self._aliases

    @aliases.setter
    def aliases(self, value: List[str]) -> None:
        self._aliases = value

    @aliases.deleter
    def aliases(self) -> None:
        self._aliases = UNSET

    @property
    def author_ids(self) -> List[str]:
        """ IDs of users to set as the Oligo's authors. """
        if isinstance(self._author_ids, Unset):
            raise NotPresentError(self, "author_ids")
        return self._author_ids

    @author_ids.setter
    def author_ids(self, value: List[str]) -> None:
        self._author_ids = value

    @author_ids.deleter
    def author_ids(self) -> None:
        self._author_ids = UNSET

    @property
    def bases(self) -> str:
        """Base pairs of the oligo."""
        if isinstance(self._bases, Unset):
            raise NotPresentError(self, "bases")
        return self._bases

    @bases.setter
    def bases(self, value: str) -> None:
        self._bases = value

    @bases.deleter
    def bases(self) -> None:
        self._bases = UNSET

    @property
    def custom_fields(self) -> CustomFields:
        if isinstance(self._custom_fields, Unset):
            raise NotPresentError(self, "custom_fields")
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, value: CustomFields) -> None:
        self._custom_fields = value

    @custom_fields.deleter
    def custom_fields(self) -> None:
        self._custom_fields = UNSET

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
        """ID of the folder containing the Oligo."""
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
    def name(self) -> str:
        """Name of the Oligo."""
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
        """ID of the oligo's schema."""
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: str) -> None:
        self._schema_id = value

    @schema_id.deleter
    def schema_id(self) -> None:
        self._schema_id = UNSET
