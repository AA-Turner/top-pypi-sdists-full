from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.constraint_create_fields_item import ConstraintCreateFieldsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="ConstraintCreate")


@attr.s(auto_attribs=True, repr=False)
class ConstraintCreate:
    """  """

    _are_unique_residues_case_sensitive: Union[Unset, bool] = UNSET
    _fields: Union[Unset, List[ConstraintCreateFieldsItem]] = UNSET
    _has_unique_canonical_smiles: Union[Unset, bool] = UNSET
    _has_unique_residues: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append(
            "are_unique_residues_case_sensitive={}".format(repr(self._are_unique_residues_case_sensitive))
        )
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("has_unique_canonical_smiles={}".format(repr(self._has_unique_canonical_smiles)))
        fields.append("has_unique_residues={}".format(repr(self._has_unique_residues)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "ConstraintCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        are_unique_residues_case_sensitive = self._are_unique_residues_case_sensitive
        fields: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = []
            for fields_item_data in self._fields:
                fields_item = fields_item_data.to_dict()

                fields.append(fields_item)

        has_unique_canonical_smiles = self._has_unique_canonical_smiles
        has_unique_residues = self._has_unique_residues

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if are_unique_residues_case_sensitive is not UNSET:
            field_dict["areUniqueResiduesCaseSensitive"] = are_unique_residues_case_sensitive
        if fields is not UNSET:
            field_dict["fields"] = fields
        if has_unique_canonical_smiles is not UNSET:
            field_dict["hasUniqueCanonicalSmiles"] = has_unique_canonical_smiles
        if has_unique_residues is not UNSET:
            field_dict["hasUniqueResidues"] = has_unique_residues

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_are_unique_residues_case_sensitive() -> Union[Unset, bool]:
            are_unique_residues_case_sensitive = d.pop("areUniqueResiduesCaseSensitive")
            return are_unique_residues_case_sensitive

        try:
            are_unique_residues_case_sensitive = get_are_unique_residues_case_sensitive()
        except KeyError:
            if strict:
                raise
            are_unique_residues_case_sensitive = cast(Union[Unset, bool], UNSET)

        def get_fields() -> Union[Unset, List[ConstraintCreateFieldsItem]]:
            fields = []
            _fields = d.pop("fields")
            for fields_item_data in _fields or []:
                fields_item = ConstraintCreateFieldsItem.from_dict(fields_item_data, strict=False)

                fields.append(fields_item)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, List[ConstraintCreateFieldsItem]], UNSET)

        def get_has_unique_canonical_smiles() -> Union[Unset, bool]:
            has_unique_canonical_smiles = d.pop("hasUniqueCanonicalSmiles")
            return has_unique_canonical_smiles

        try:
            has_unique_canonical_smiles = get_has_unique_canonical_smiles()
        except KeyError:
            if strict:
                raise
            has_unique_canonical_smiles = cast(Union[Unset, bool], UNSET)

        def get_has_unique_residues() -> Union[Unset, bool]:
            has_unique_residues = d.pop("hasUniqueResidues")
            return has_unique_residues

        try:
            has_unique_residues = get_has_unique_residues()
        except KeyError:
            if strict:
                raise
            has_unique_residues = cast(Union[Unset, bool], UNSET)

        constraint_create = cls(
            are_unique_residues_case_sensitive=are_unique_residues_case_sensitive,
            fields=fields,
            has_unique_canonical_smiles=has_unique_canonical_smiles,
            has_unique_residues=has_unique_residues,
        )

        constraint_create.additional_properties = d
        return constraint_create

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
    def are_unique_residues_case_sensitive(self) -> bool:
        if isinstance(self._are_unique_residues_case_sensitive, Unset):
            raise NotPresentError(self, "are_unique_residues_case_sensitive")
        return self._are_unique_residues_case_sensitive

    @are_unique_residues_case_sensitive.setter
    def are_unique_residues_case_sensitive(self, value: bool) -> None:
        self._are_unique_residues_case_sensitive = value

    @are_unique_residues_case_sensitive.deleter
    def are_unique_residues_case_sensitive(self) -> None:
        self._are_unique_residues_case_sensitive = UNSET

    @property
    def fields(self) -> List[ConstraintCreateFieldsItem]:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: List[ConstraintCreateFieldsItem]) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def has_unique_canonical_smiles(self) -> bool:
        if isinstance(self._has_unique_canonical_smiles, Unset):
            raise NotPresentError(self, "has_unique_canonical_smiles")
        return self._has_unique_canonical_smiles

    @has_unique_canonical_smiles.setter
    def has_unique_canonical_smiles(self, value: bool) -> None:
        self._has_unique_canonical_smiles = value

    @has_unique_canonical_smiles.deleter
    def has_unique_canonical_smiles(self) -> None:
        self._has_unique_canonical_smiles = UNSET

    @property
    def has_unique_residues(self) -> bool:
        if isinstance(self._has_unique_residues, Unset):
            raise NotPresentError(self, "has_unique_residues")
        return self._has_unique_residues

    @has_unique_residues.setter
    def has_unique_residues(self, value: bool) -> None:
        self._has_unique_residues = value

    @has_unique_residues.deleter
    def has_unique_residues(self) -> None:
        self._has_unique_residues = UNSET
