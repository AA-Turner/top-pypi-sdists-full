from typing import Any, cast, Dict, List, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="AaSequencesFindMatchingRegion")


@attr.s(auto_attribs=True, repr=False)
class AaSequencesFindMatchingRegion:
    """  """

    _schema_id: str
    _target_aa_sequence_ids: List[str]
    _registry_id: Union[Unset, str] = UNSET

    def __repr__(self):
        fields = []
        fields.append("schema_id={}".format(repr(self._schema_id)))
        fields.append("target_aa_sequence_ids={}".format(repr(self._target_aa_sequence_ids)))
        fields.append("registry_id={}".format(repr(self._registry_id)))
        return "AaSequencesFindMatchingRegion({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        schema_id = self._schema_id
        target_aa_sequence_ids = self._target_aa_sequence_ids

        registry_id = self._registry_id

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if schema_id is not UNSET:
            field_dict["schemaId"] = schema_id
        if target_aa_sequence_ids is not UNSET:
            field_dict["targetAASequenceIds"] = target_aa_sequence_ids
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_schema_id() -> str:
            schema_id = d.pop("schemaId")
            return schema_id

        try:
            schema_id = get_schema_id()
        except KeyError:
            if strict:
                raise
            schema_id = cast(str, UNSET)

        def get_target_aa_sequence_ids() -> List[str]:
            target_aa_sequence_ids = cast(List[str], d.pop("targetAASequenceIds"))

            return target_aa_sequence_ids

        try:
            target_aa_sequence_ids = get_target_aa_sequence_ids()
        except KeyError:
            if strict:
                raise
            target_aa_sequence_ids = cast(List[str], UNSET)

        def get_registry_id() -> Union[Unset, str]:
            registry_id = d.pop("registryId")
            return registry_id

        try:
            registry_id = get_registry_id()
        except KeyError:
            if strict:
                raise
            registry_id = cast(Union[Unset, str], UNSET)

        aa_sequences_find_matching_region = cls(
            schema_id=schema_id,
            target_aa_sequence_ids=target_aa_sequence_ids,
            registry_id=registry_id,
        )

        return aa_sequences_find_matching_region

    @property
    def schema_id(self) -> str:
        """ Schema ID for the type of AA to match to the source sequence """
        if isinstance(self._schema_id, Unset):
            raise NotPresentError(self, "schema_id")
        return self._schema_id

    @schema_id.setter
    def schema_id(self, value: str) -> None:
        self._schema_id = value

    @property
    def target_aa_sequence_ids(self) -> List[str]:
        """ API IDs of the AA sequences which matching regions will be found for """
        if isinstance(self._target_aa_sequence_ids, Unset):
            raise NotPresentError(self, "target_aa_sequence_ids")
        return self._target_aa_sequence_ids

    @target_aa_sequence_ids.setter
    def target_aa_sequence_ids(self, value: List[str]) -> None:
        self._target_aa_sequence_ids = value

    @property
    def registry_id(self) -> str:
        """ An optional Registry ID to restrict the region search to """
        if isinstance(self._registry_id, Unset):
            raise NotPresentError(self, "registry_id")
        return self._registry_id

    @registry_id.setter
    def registry_id(self, value: str) -> None:
        self._registry_id = value

    @registry_id.deleter
    def registry_id(self) -> None:
        self._registry_id = UNSET
