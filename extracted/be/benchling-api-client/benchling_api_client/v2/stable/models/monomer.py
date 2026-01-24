import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.monomer_polymer_type import MonomerPolymerType
from ..models.monomer_type import MonomerType
from ..models.monomer_visual_symbol import MonomerVisualSymbol
from ..types import UNSET, Unset

T = TypeVar("T", bound="Monomer")


@attr.s(auto_attribs=True, repr=False)
class Monomer:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _attachment_points: Union[Unset, List[str]] = UNSET
    _calculated_molecular_weight: Union[Unset, float] = UNSET
    _canonical_smiles: Union[Unset, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _custom_molecular_weight: Union[Unset, None, float] = UNSET
    _exact_molecular_weight: Union[Unset, float] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _monomer_type: Union[Unset, MonomerType] = UNSET
    _name: Union[Unset, str] = UNSET
    _natural_analog: Union[Unset, str] = UNSET
    _original_smiles: Union[Unset, None, str] = UNSET
    _polymer_type: Union[Unset, MonomerPolymerType] = UNSET
    _symbol: Union[Unset, str] = UNSET
    _visual_color: Union[Unset, None, str] = UNSET
    _visual_symbol: Union[Unset, None, MonomerVisualSymbol] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("attachment_points={}".format(repr(self._attachment_points)))
        fields.append("calculated_molecular_weight={}".format(repr(self._calculated_molecular_weight)))
        fields.append("canonical_smiles={}".format(repr(self._canonical_smiles)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("custom_molecular_weight={}".format(repr(self._custom_molecular_weight)))
        fields.append("exact_molecular_weight={}".format(repr(self._exact_molecular_weight)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("monomer_type={}".format(repr(self._monomer_type)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("natural_analog={}".format(repr(self._natural_analog)))
        fields.append("original_smiles={}".format(repr(self._original_smiles)))
        fields.append("polymer_type={}".format(repr(self._polymer_type)))
        fields.append("symbol={}".format(repr(self._symbol)))
        fields.append("visual_color={}".format(repr(self._visual_color)))
        fields.append("visual_symbol={}".format(repr(self._visual_symbol)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Monomer({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        attachment_points: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._attachment_points, Unset):
            attachment_points = self._attachment_points

        calculated_molecular_weight = self._calculated_molecular_weight
        canonical_smiles = self._canonical_smiles
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        custom_molecular_weight = self._custom_molecular_weight
        exact_molecular_weight = self._exact_molecular_weight
        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        monomer_type: Union[Unset, int] = UNSET
        if not isinstance(self._monomer_type, Unset):
            monomer_type = self._monomer_type.value

        name = self._name
        natural_analog = self._natural_analog
        original_smiles = self._original_smiles
        polymer_type: Union[Unset, int] = UNSET
        if not isinstance(self._polymer_type, Unset):
            polymer_type = self._polymer_type.value

        symbol = self._symbol
        visual_color = self._visual_color
        visual_symbol: Union[Unset, None, int] = UNSET
        if not isinstance(self._visual_symbol, Unset):
            visual_symbol = self._visual_symbol.value if self._visual_symbol else None

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if attachment_points is not UNSET:
            field_dict["attachmentPoints"] = attachment_points
        if calculated_molecular_weight is not UNSET:
            field_dict["calculatedMolecularWeight"] = calculated_molecular_weight
        if canonical_smiles is not UNSET:
            field_dict["canonicalSmiles"] = canonical_smiles
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if custom_molecular_weight is not UNSET:
            field_dict["customMolecularWeight"] = custom_molecular_weight
        if exact_molecular_weight is not UNSET:
            field_dict["exactMolecularWeight"] = exact_molecular_weight
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if monomer_type is not UNSET:
            field_dict["monomerType"] = monomer_type
        if name is not UNSET:
            field_dict["name"] = name
        if natural_analog is not UNSET:
            field_dict["naturalAnalog"] = natural_analog
        if original_smiles is not UNSET:
            field_dict["originalSmiles"] = original_smiles
        if polymer_type is not UNSET:
            field_dict["polymerType"] = polymer_type
        if symbol is not UNSET:
            field_dict["symbol"] = symbol
        if visual_color is not UNSET:
            field_dict["visualColor"] = visual_color
        if visual_symbol is not UNSET:
            field_dict["visualSymbol"] = visual_symbol

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_archive_record() -> Union[Unset, None, ArchiveRecord]:
            archive_record = None
            _archive_record = d.pop("archiveRecord")

            if _archive_record is not None and not isinstance(_archive_record, Unset):
                archive_record = ArchiveRecord.from_dict(_archive_record)

            return archive_record

        try:
            archive_record = get_archive_record()
        except KeyError:
            if strict:
                raise
            archive_record = cast(Union[Unset, None, ArchiveRecord], UNSET)

        def get_attachment_points() -> Union[Unset, List[str]]:
            attachment_points = cast(List[str], d.pop("attachmentPoints"))

            return attachment_points

        try:
            attachment_points = get_attachment_points()
        except KeyError:
            if strict:
                raise
            attachment_points = cast(Union[Unset, List[str]], UNSET)

        def get_calculated_molecular_weight() -> Union[Unset, float]:
            calculated_molecular_weight = d.pop("calculatedMolecularWeight")
            return calculated_molecular_weight

        try:
            calculated_molecular_weight = get_calculated_molecular_weight()
        except KeyError:
            if strict:
                raise
            calculated_molecular_weight = cast(Union[Unset, float], UNSET)

        def get_canonical_smiles() -> Union[Unset, str]:
            canonical_smiles = d.pop("canonicalSmiles")
            return canonical_smiles

        try:
            canonical_smiles = get_canonical_smiles()
        except KeyError:
            if strict:
                raise
            canonical_smiles = cast(Union[Unset, str], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_custom_molecular_weight() -> Union[Unset, None, float]:
            custom_molecular_weight = d.pop("customMolecularWeight")
            return custom_molecular_weight

        try:
            custom_molecular_weight = get_custom_molecular_weight()
        except KeyError:
            if strict:
                raise
            custom_molecular_weight = cast(Union[Unset, None, float], UNSET)

        def get_exact_molecular_weight() -> Union[Unset, float]:
            exact_molecular_weight = d.pop("exactMolecularWeight")
            return exact_molecular_weight

        try:
            exact_molecular_weight = get_exact_molecular_weight()
        except KeyError:
            if strict:
                raise
            exact_molecular_weight = cast(Union[Unset, float], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

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

        def get_monomer_type() -> Union[Unset, MonomerType]:
            monomer_type = UNSET
            _monomer_type = d.pop("monomerType")
            if _monomer_type is not None and _monomer_type is not UNSET:
                try:
                    monomer_type = MonomerType(_monomer_type)
                except ValueError:
                    monomer_type = MonomerType.of_unknown(_monomer_type)

            return monomer_type

        try:
            monomer_type = get_monomer_type()
        except KeyError:
            if strict:
                raise
            monomer_type = cast(Union[Unset, MonomerType], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_natural_analog() -> Union[Unset, str]:
            natural_analog = d.pop("naturalAnalog")
            return natural_analog

        try:
            natural_analog = get_natural_analog()
        except KeyError:
            if strict:
                raise
            natural_analog = cast(Union[Unset, str], UNSET)

        def get_original_smiles() -> Union[Unset, None, str]:
            original_smiles = d.pop("originalSmiles")
            return original_smiles

        try:
            original_smiles = get_original_smiles()
        except KeyError:
            if strict:
                raise
            original_smiles = cast(Union[Unset, None, str], UNSET)

        def get_polymer_type() -> Union[Unset, MonomerPolymerType]:
            polymer_type = UNSET
            _polymer_type = d.pop("polymerType")
            if _polymer_type is not None and _polymer_type is not UNSET:
                try:
                    polymer_type = MonomerPolymerType(_polymer_type)
                except ValueError:
                    polymer_type = MonomerPolymerType.of_unknown(_polymer_type)

            return polymer_type

        try:
            polymer_type = get_polymer_type()
        except KeyError:
            if strict:
                raise
            polymer_type = cast(Union[Unset, MonomerPolymerType], UNSET)

        def get_symbol() -> Union[Unset, str]:
            symbol = d.pop("symbol")
            return symbol

        try:
            symbol = get_symbol()
        except KeyError:
            if strict:
                raise
            symbol = cast(Union[Unset, str], UNSET)

        def get_visual_color() -> Union[Unset, None, str]:
            visual_color = d.pop("visualColor")
            return visual_color

        try:
            visual_color = get_visual_color()
        except KeyError:
            if strict:
                raise
            visual_color = cast(Union[Unset, None, str], UNSET)

        def get_visual_symbol() -> Union[Unset, None, MonomerVisualSymbol]:
            visual_symbol = UNSET
            _visual_symbol = d.pop("visualSymbol")
            if _visual_symbol is not None and _visual_symbol is not UNSET:
                try:
                    visual_symbol = MonomerVisualSymbol(_visual_symbol)
                except ValueError:
                    visual_symbol = MonomerVisualSymbol.of_unknown(_visual_symbol)

            return visual_symbol

        try:
            visual_symbol = get_visual_symbol()
        except KeyError:
            if strict:
                raise
            visual_symbol = cast(Union[Unset, None, MonomerVisualSymbol], UNSET)

        monomer = cls(
            archive_record=archive_record,
            attachment_points=attachment_points,
            calculated_molecular_weight=calculated_molecular_weight,
            canonical_smiles=canonical_smiles,
            created_at=created_at,
            custom_molecular_weight=custom_molecular_weight,
            exact_molecular_weight=exact_molecular_weight,
            id=id,
            modified_at=modified_at,
            monomer_type=monomer_type,
            name=name,
            natural_analog=natural_analog,
            original_smiles=original_smiles,
            polymer_type=polymer_type,
            symbol=symbol,
            visual_color=visual_color,
            visual_symbol=visual_symbol,
        )

        monomer.additional_properties = d
        return monomer

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
    def archive_record(self) -> Optional[ArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[ArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

    @property
    def attachment_points(self) -> List[str]:
        """ A list of the capping group present at each location where the monomer can form a bond with other monomers """
        if isinstance(self._attachment_points, Unset):
            raise NotPresentError(self, "attachment_points")
        return self._attachment_points

    @attachment_points.setter
    def attachment_points(self, value: List[str]) -> None:
        self._attachment_points = value

    @attachment_points.deleter
    def attachment_points(self) -> None:
        self._attachment_points = UNSET

    @property
    def calculated_molecular_weight(self) -> float:
        """ The molecular weight of the monomer as calculated by RDKit based on the monomer chemical structure """
        if isinstance(self._calculated_molecular_weight, Unset):
            raise NotPresentError(self, "calculated_molecular_weight")
        return self._calculated_molecular_weight

    @calculated_molecular_weight.setter
    def calculated_molecular_weight(self, value: float) -> None:
        self._calculated_molecular_weight = value

    @calculated_molecular_weight.deleter
    def calculated_molecular_weight(self) -> None:
        self._calculated_molecular_weight = UNSET

    @property
    def canonical_smiles(self) -> str:
        """ The canonicalized chemical structure in SMILES format. """
        if isinstance(self._canonical_smiles, Unset):
            raise NotPresentError(self, "canonical_smiles")
        return self._canonical_smiles

    @canonical_smiles.setter
    def canonical_smiles(self, value: str) -> None:
        self._canonical_smiles = value

    @canonical_smiles.deleter
    def canonical_smiles(self) -> None:
        self._canonical_smiles = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        """ DateTime the monomer was created. """
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def custom_molecular_weight(self) -> Optional[float]:
        """ Optional molecular weight value that the user can provide to override the calculated molecular weight """
        if isinstance(self._custom_molecular_weight, Unset):
            raise NotPresentError(self, "custom_molecular_weight")
        return self._custom_molecular_weight

    @custom_molecular_weight.setter
    def custom_molecular_weight(self, value: Optional[float]) -> None:
        self._custom_molecular_weight = value

    @custom_molecular_weight.deleter
    def custom_molecular_weight(self) -> None:
        self._custom_molecular_weight = UNSET

    @property
    def exact_molecular_weight(self) -> float:
        """ The exact molecular weight of the monomer as calculated by RDKit based on the monomer chemical structure """
        if isinstance(self._exact_molecular_weight, Unset):
            raise NotPresentError(self, "exact_molecular_weight")
        return self._exact_molecular_weight

    @exact_molecular_weight.setter
    def exact_molecular_weight(self, value: float) -> None:
        self._exact_molecular_weight = value

    @exact_molecular_weight.deleter
    def exact_molecular_weight(self) -> None:
        self._exact_molecular_weight = UNSET

    @property
    def id(self) -> str:
        """ ID of the monomer """
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
    def modified_at(self) -> datetime.datetime:
        """ DateTime the monomer was last modified. """
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
    def monomer_type(self) -> MonomerType:
        """ The part of the nucleotide structure that the monomer fits into, i.e. backbone or branch """
        if isinstance(self._monomer_type, Unset):
            raise NotPresentError(self, "monomer_type")
        return self._monomer_type

    @monomer_type.setter
    def monomer_type(self, value: MonomerType) -> None:
        self._monomer_type = value

    @monomer_type.deleter
    def monomer_type(self) -> None:
        self._monomer_type = UNSET

    @property
    def name(self) -> str:
        """ Name of the monomer """
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
    def natural_analog(self) -> str:
        """ Symbol for the natural equivalent of the monomer. Acceptable natural analog values include IUPAC bases, r, and p. """
        if isinstance(self._natural_analog, Unset):
            raise NotPresentError(self, "natural_analog")
        return self._natural_analog

    @natural_analog.setter
    def natural_analog(self, value: str) -> None:
        self._natural_analog = value

    @natural_analog.deleter
    def natural_analog(self) -> None:
        self._natural_analog = UNSET

    @property
    def original_smiles(self) -> Optional[str]:
        """ The original chemical structure supplied by the user in SMILES format. Null if the user did not originally supply SMILES. """
        if isinstance(self._original_smiles, Unset):
            raise NotPresentError(self, "original_smiles")
        return self._original_smiles

    @original_smiles.setter
    def original_smiles(self, value: Optional[str]) -> None:
        self._original_smiles = value

    @original_smiles.deleter
    def original_smiles(self) -> None:
        self._original_smiles = UNSET

    @property
    def polymer_type(self) -> MonomerPolymerType:
        """ The polymer type of the monomer. Currently only RNA monomers are supported. """
        if isinstance(self._polymer_type, Unset):
            raise NotPresentError(self, "polymer_type")
        return self._polymer_type

    @polymer_type.setter
    def polymer_type(self, value: MonomerPolymerType) -> None:
        self._polymer_type = value

    @polymer_type.deleter
    def polymer_type(self) -> None:
        self._polymer_type = UNSET

    @property
    def symbol(self) -> str:
        """ User-defined identifier of the monomer, unique on the monomer type. """
        if isinstance(self._symbol, Unset):
            raise NotPresentError(self, "symbol")
        return self._symbol

    @symbol.setter
    def symbol(self, value: str) -> None:
        self._symbol = value

    @symbol.deleter
    def symbol(self) -> None:
        self._symbol = UNSET

    @property
    def visual_color(self) -> Optional[str]:
        """ The hex color code of the monomer visual symbol """
        if isinstance(self._visual_color, Unset):
            raise NotPresentError(self, "visual_color")
        return self._visual_color

    @visual_color.setter
    def visual_color(self, value: Optional[str]) -> None:
        self._visual_color = value

    @visual_color.deleter
    def visual_color(self) -> None:
        self._visual_color = UNSET

    @property
    def visual_symbol(self) -> Optional[MonomerVisualSymbol]:
        """ The shape of the monomer visual symbol. """
        if isinstance(self._visual_symbol, Unset):
            raise NotPresentError(self, "visual_symbol")
        return self._visual_symbol

    @visual_symbol.setter
    def visual_symbol(self, value: Optional[MonomerVisualSymbol]) -> None:
        self._visual_symbol = value

    @visual_symbol.deleter
    def visual_symbol(self) -> None:
        self._visual_symbol = UNSET
