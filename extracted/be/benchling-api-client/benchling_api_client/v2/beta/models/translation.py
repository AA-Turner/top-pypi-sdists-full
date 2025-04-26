from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.sequence_feature_custom_field import SequenceFeatureCustomField
from ..models.translation_genetic_code import TranslationGeneticCode
from ..models.translation_regions_item import TranslationRegionsItem
from ..types import UNSET, Unset

T = TypeVar("T", bound="Translation")


@attr.s(auto_attribs=True, repr=False)
class Translation:
    """  """

    _amino_acids: Union[Unset, str] = UNSET
    _coerce_start_codon_to_methionine: Union[Unset, bool] = False
    _end: Union[Unset, int] = UNSET
    _genetic_code: Union[Unset, TranslationGeneticCode] = TranslationGeneticCode.STANDARD
    _regions: Union[Unset, List[TranslationRegionsItem]] = UNSET
    _start: Union[Unset, int] = UNSET
    _strand: Union[Unset, int] = UNSET
    _color: Union[Unset, str] = UNSET
    _custom_fields: Union[Unset, List[SequenceFeatureCustomField]] = UNSET
    _name: Union[Unset, str] = UNSET
    _notes: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("amino_acids={}".format(repr(self._amino_acids)))
        fields.append(
            "coerce_start_codon_to_methionine={}".format(repr(self._coerce_start_codon_to_methionine))
        )
        fields.append("end={}".format(repr(self._end)))
        fields.append("genetic_code={}".format(repr(self._genetic_code)))
        fields.append("regions={}".format(repr(self._regions)))
        fields.append("start={}".format(repr(self._start)))
        fields.append("strand={}".format(repr(self._strand)))
        fields.append("color={}".format(repr(self._color)))
        fields.append("custom_fields={}".format(repr(self._custom_fields)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("notes={}".format(repr(self._notes)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Translation({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        amino_acids = self._amino_acids
        coerce_start_codon_to_methionine = self._coerce_start_codon_to_methionine
        end = self._end
        genetic_code: Union[Unset, int] = UNSET
        if not isinstance(self._genetic_code, Unset):
            genetic_code = self._genetic_code.value

        regions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._regions, Unset):
            regions = []
            for regions_item_data in self._regions:
                regions_item = regions_item_data.to_dict()

                regions.append(regions_item)

        start = self._start
        strand = self._strand
        color = self._color
        custom_fields: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._custom_fields, Unset):
            custom_fields = []
            for custom_fields_item_data in self._custom_fields:
                custom_fields_item = custom_fields_item_data.to_dict()

                custom_fields.append(custom_fields_item)

        name = self._name
        notes = self._notes

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if amino_acids is not UNSET:
            field_dict["aminoAcids"] = amino_acids
        if coerce_start_codon_to_methionine is not UNSET:
            field_dict["coerceStartCodonToMethionine"] = coerce_start_codon_to_methionine
        if end is not UNSET:
            field_dict["end"] = end
        if genetic_code is not UNSET:
            field_dict["geneticCode"] = genetic_code
        if regions is not UNSET:
            field_dict["regions"] = regions
        if start is not UNSET:
            field_dict["start"] = start
        if strand is not UNSET:
            field_dict["strand"] = strand
        if color is not UNSET:
            field_dict["color"] = color
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if name is not UNSET:
            field_dict["name"] = name
        if notes is not UNSET:
            field_dict["notes"] = notes

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_amino_acids() -> Union[Unset, str]:
            amino_acids = d.pop("aminoAcids")
            return amino_acids

        try:
            amino_acids = get_amino_acids()
        except KeyError:
            if strict:
                raise
            amino_acids = cast(Union[Unset, str], UNSET)

        def get_coerce_start_codon_to_methionine() -> Union[Unset, bool]:
            coerce_start_codon_to_methionine = d.pop("coerceStartCodonToMethionine")
            return coerce_start_codon_to_methionine

        try:
            coerce_start_codon_to_methionine = get_coerce_start_codon_to_methionine()
        except KeyError:
            if strict:
                raise
            coerce_start_codon_to_methionine = cast(Union[Unset, bool], UNSET)

        def get_end() -> Union[Unset, int]:
            end = d.pop("end")
            return end

        try:
            end = get_end()
        except KeyError:
            if strict:
                raise
            end = cast(Union[Unset, int], UNSET)

        def get_genetic_code() -> Union[Unset, TranslationGeneticCode]:
            genetic_code = UNSET
            _genetic_code = d.pop("geneticCode")
            if _genetic_code is not None and _genetic_code is not UNSET:
                try:
                    genetic_code = TranslationGeneticCode(_genetic_code)
                except ValueError:
                    genetic_code = TranslationGeneticCode.of_unknown(_genetic_code)

            return genetic_code

        try:
            genetic_code = get_genetic_code()
        except KeyError:
            if strict:
                raise
            genetic_code = cast(Union[Unset, TranslationGeneticCode], UNSET)

        def get_regions() -> Union[Unset, List[TranslationRegionsItem]]:
            regions = []
            _regions = d.pop("regions")
            for regions_item_data in _regions or []:
                regions_item = TranslationRegionsItem.from_dict(regions_item_data, strict=False)

                regions.append(regions_item)

            return regions

        try:
            regions = get_regions()
        except KeyError:
            if strict:
                raise
            regions = cast(Union[Unset, List[TranslationRegionsItem]], UNSET)

        def get_start() -> Union[Unset, int]:
            start = d.pop("start")
            return start

        try:
            start = get_start()
        except KeyError:
            if strict:
                raise
            start = cast(Union[Unset, int], UNSET)

        def get_strand() -> Union[Unset, int]:
            strand = d.pop("strand")
            return strand

        try:
            strand = get_strand()
        except KeyError:
            if strict:
                raise
            strand = cast(Union[Unset, int], UNSET)

        def get_color() -> Union[Unset, str]:
            color = d.pop("color")
            return color

        try:
            color = get_color()
        except KeyError:
            if strict:
                raise
            color = cast(Union[Unset, str], UNSET)

        def get_custom_fields() -> Union[Unset, List[SequenceFeatureCustomField]]:
            custom_fields = []
            _custom_fields = d.pop("customFields")
            for custom_fields_item_data in _custom_fields or []:
                custom_fields_item = SequenceFeatureCustomField.from_dict(
                    custom_fields_item_data, strict=False
                )

                custom_fields.append(custom_fields_item)

            return custom_fields

        try:
            custom_fields = get_custom_fields()
        except KeyError:
            if strict:
                raise
            custom_fields = cast(Union[Unset, List[SequenceFeatureCustomField]], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_notes() -> Union[Unset, str]:
            notes = d.pop("notes")
            return notes

        try:
            notes = get_notes()
        except KeyError:
            if strict:
                raise
            notes = cast(Union[Unset, str], UNSET)

        translation = cls(
            amino_acids=amino_acids,
            coerce_start_codon_to_methionine=coerce_start_codon_to_methionine,
            end=end,
            genetic_code=genetic_code,
            regions=regions,
            start=start,
            strand=strand,
            color=color,
            custom_fields=custom_fields,
            name=name,
            notes=notes,
        )

        translation.additional_properties = d
        return translation

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
    def amino_acids(self) -> str:
        if isinstance(self._amino_acids, Unset):
            raise NotPresentError(self, "amino_acids")
        return self._amino_acids

    @amino_acids.setter
    def amino_acids(self, value: str) -> None:
        self._amino_acids = value

    @amino_acids.deleter
    def amino_acids(self) -> None:
        self._amino_acids = UNSET

    @property
    def coerce_start_codon_to_methionine(self) -> bool:
        """ Whether to override the translation of the start codon to Methionine. Has no effect when the start codon already translates to Methionine. """
        if isinstance(self._coerce_start_codon_to_methionine, Unset):
            raise NotPresentError(self, "coerce_start_codon_to_methionine")
        return self._coerce_start_codon_to_methionine

    @coerce_start_codon_to_methionine.setter
    def coerce_start_codon_to_methionine(self, value: bool) -> None:
        self._coerce_start_codon_to_methionine = value

    @coerce_start_codon_to_methionine.deleter
    def coerce_start_codon_to_methionine(self) -> None:
        self._coerce_start_codon_to_methionine = UNSET

    @property
    def end(self) -> int:
        """ 0-based exclusive end index. The end of the sequence is always represented as 0. """
        if isinstance(self._end, Unset):
            raise NotPresentError(self, "end")
        return self._end

    @end.setter
    def end(self, value: int) -> None:
        self._end = value

    @end.deleter
    def end(self) -> None:
        self._end = UNSET

    @property
    def genetic_code(self) -> TranslationGeneticCode:
        """ The genetic code to use when translating the nucleotide sequence into amino acids. """
        if isinstance(self._genetic_code, Unset):
            raise NotPresentError(self, "genetic_code")
        return self._genetic_code

    @genetic_code.setter
    def genetic_code(self, value: TranslationGeneticCode) -> None:
        self._genetic_code = value

    @genetic_code.deleter
    def genetic_code(self) -> None:
        self._genetic_code = UNSET

    @property
    def regions(self) -> List[TranslationRegionsItem]:
        if isinstance(self._regions, Unset):
            raise NotPresentError(self, "regions")
        return self._regions

    @regions.setter
    def regions(self, value: List[TranslationRegionsItem]) -> None:
        self._regions = value

    @regions.deleter
    def regions(self) -> None:
        self._regions = UNSET

    @property
    def start(self) -> int:
        """ 0-based inclusive start index. """
        if isinstance(self._start, Unset):
            raise NotPresentError(self, "start")
        return self._start

    @start.setter
    def start(self, value: int) -> None:
        self._start = value

    @start.deleter
    def start(self) -> None:
        self._start = UNSET

    @property
    def strand(self) -> int:
        if isinstance(self._strand, Unset):
            raise NotPresentError(self, "strand")
        return self._strand

    @strand.setter
    def strand(self, value: int) -> None:
        self._strand = value

    @strand.deleter
    def strand(self) -> None:
        self._strand = UNSET

    @property
    def color(self) -> str:
        """ Hex color code used when displaying this feature in the UI. """
        if isinstance(self._color, Unset):
            raise NotPresentError(self, "color")
        return self._color

    @color.setter
    def color(self, value: str) -> None:
        self._color = value

    @color.deleter
    def color(self) -> None:
        self._color = UNSET

    @property
    def custom_fields(self) -> List[SequenceFeatureCustomField]:
        if isinstance(self._custom_fields, Unset):
            raise NotPresentError(self, "custom_fields")
        return self._custom_fields

    @custom_fields.setter
    def custom_fields(self, value: List[SequenceFeatureCustomField]) -> None:
        self._custom_fields = value

    @custom_fields.deleter
    def custom_fields(self) -> None:
        self._custom_fields = UNSET

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

    @property
    def notes(self) -> str:
        if isinstance(self._notes, Unset):
            raise NotPresentError(self, "notes")
        return self._notes

    @notes.setter
    def notes(self, value: str) -> None:
        self._notes = value

    @notes.deleter
    def notes(self) -> None:
        self._notes = UNSET
