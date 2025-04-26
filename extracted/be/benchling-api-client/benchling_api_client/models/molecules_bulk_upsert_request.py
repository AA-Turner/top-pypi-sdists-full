from typing import Any, cast, Dict, List, Type, TypeVar

import attr

from ..extensions import NotPresentError
from ..models.molecule_bulk_upsert_request import MoleculeBulkUpsertRequest
from ..types import UNSET, Unset

T = TypeVar("T", bound="MoleculesBulkUpsertRequest")


@attr.s(auto_attribs=True, repr=False)
class MoleculesBulkUpsertRequest:
    """  """

    _molecules: List[MoleculeBulkUpsertRequest]

    def __repr__(self):
        fields = []
        fields.append("molecules={}".format(repr(self._molecules)))
        return "MoleculesBulkUpsertRequest({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        molecules = []
        for molecules_item_data in self._molecules:
            molecules_item = molecules_item_data.to_dict()

            molecules.append(molecules_item)

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if molecules is not UNSET:
            field_dict["molecules"] = molecules

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_molecules() -> List[MoleculeBulkUpsertRequest]:
            molecules = []
            _molecules = d.pop("molecules")
            for molecules_item_data in _molecules:
                molecules_item = MoleculeBulkUpsertRequest.from_dict(molecules_item_data, strict=False)

                molecules.append(molecules_item)

            return molecules

        try:
            molecules = get_molecules()
        except KeyError:
            if strict:
                raise
            molecules = cast(List[MoleculeBulkUpsertRequest], UNSET)

        molecules_bulk_upsert_request = cls(
            molecules=molecules,
        )

        return molecules_bulk_upsert_request

    @property
    def molecules(self) -> List[MoleculeBulkUpsertRequest]:
        if isinstance(self._molecules, Unset):
            raise NotPresentError(self, "molecules")
        return self._molecules

    @molecules.setter
    def molecules(self, value: List[MoleculeBulkUpsertRequest]) -> None:
        self._molecules = value
