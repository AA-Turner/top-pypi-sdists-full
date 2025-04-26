from typing import Any, cast, Dict, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.monomer_visual_symbol import MonomerVisualSymbol
from ..types import UNSET, Unset

T = TypeVar("T", bound="MonomerCreate")


@attr.s(auto_attribs=True, repr=False)
class MonomerCreate:
    """  """

    _natural_analog: str
    _color: Union[Unset, None, str] = UNSET
    _custom_molecular_weight: Union[Unset, None, float] = UNSET
    _name: Union[Unset, str] = UNSET
    _smiles: Union[Unset, str] = UNSET
    _symbol: Union[Unset, str] = UNSET
    _visual_symbol: Union[Unset, MonomerVisualSymbol] = UNSET

    def __repr__(self):
        fields = []
        fields.append("natural_analog={}".format(repr(self._natural_analog)))
        fields.append("color={}".format(repr(self._color)))
        fields.append("custom_molecular_weight={}".format(repr(self._custom_molecular_weight)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("smiles={}".format(repr(self._smiles)))
        fields.append("symbol={}".format(repr(self._symbol)))
        fields.append("visual_symbol={}".format(repr(self._visual_symbol)))
        return "MonomerCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        natural_analog = self._natural_analog
        color = self._color
        custom_molecular_weight = self._custom_molecular_weight
        name = self._name
        smiles = self._smiles
        symbol = self._symbol
        visual_symbol: Union[Unset, int] = UNSET
        if not isinstance(self._visual_symbol, Unset):
            visual_symbol = self._visual_symbol.value

        field_dict: Dict[str, Any] = {}
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if natural_analog is not UNSET:
            field_dict["naturalAnalog"] = natural_analog
        if color is not UNSET:
            field_dict["color"] = color
        if custom_molecular_weight is not UNSET:
            field_dict["customMolecularWeight"] = custom_molecular_weight
        if name is not UNSET:
            field_dict["name"] = name
        if smiles is not UNSET:
            field_dict["smiles"] = smiles
        if symbol is not UNSET:
            field_dict["symbol"] = symbol
        if visual_symbol is not UNSET:
            field_dict["visualSymbol"] = visual_symbol

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_natural_analog() -> str:
            natural_analog = d.pop("naturalAnalog")
            return natural_analog

        try:
            natural_analog = get_natural_analog()
        except KeyError:
            if strict:
                raise
            natural_analog = cast(str, UNSET)

        def get_color() -> Union[Unset, None, str]:
            color = d.pop("color")
            return color

        try:
            color = get_color()
        except KeyError:
            if strict:
                raise
            color = cast(Union[Unset, None, str], UNSET)

        def get_custom_molecular_weight() -> Union[Unset, None, float]:
            custom_molecular_weight = d.pop("customMolecularWeight")
            return custom_molecular_weight

        try:
            custom_molecular_weight = get_custom_molecular_weight()
        except KeyError:
            if strict:
                raise
            custom_molecular_weight = cast(Union[Unset, None, float], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_smiles() -> Union[Unset, str]:
            smiles = d.pop("smiles")
            return smiles

        try:
            smiles = get_smiles()
        except KeyError:
            if strict:
                raise
            smiles = cast(Union[Unset, str], UNSET)

        def get_symbol() -> Union[Unset, str]:
            symbol = d.pop("symbol")
            return symbol

        try:
            symbol = get_symbol()
        except KeyError:
            if strict:
                raise
            symbol = cast(Union[Unset, str], UNSET)

        def get_visual_symbol() -> Union[Unset, MonomerVisualSymbol]:
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
            visual_symbol = cast(Union[Unset, MonomerVisualSymbol], UNSET)

        monomer_create = cls(
            natural_analog=natural_analog,
            color=color,
            custom_molecular_weight=custom_molecular_weight,
            name=name,
            smiles=smiles,
            symbol=symbol,
            visual_symbol=visual_symbol,
        )

        return monomer_create

    @property
    def natural_analog(self) -> str:
        """ Symbol for the natural equivalent of the monomer. Acceptable natural analog values include IUPAC bases, r, and p. """
        if isinstance(self._natural_analog, Unset):
            raise NotPresentError(self, "natural_analog")
        return self._natural_analog

    @natural_analog.setter
    def natural_analog(self, value: str) -> None:
        self._natural_analog = value

    @property
    def color(self) -> Optional[str]:
        """ The hex color code of the monomer visual symbol """
        if isinstance(self._color, Unset):
            raise NotPresentError(self, "color")
        return self._color

    @color.setter
    def color(self, value: Optional[str]) -> None:
        self._color = value

    @color.deleter
    def color(self) -> None:
        self._color = UNSET

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
    def smiles(self) -> str:
        """ The chemical structure in SMILES format. """
        if isinstance(self._smiles, Unset):
            raise NotPresentError(self, "smiles")
        return self._smiles

    @smiles.setter
    def smiles(self, value: str) -> None:
        self._smiles = value

    @smiles.deleter
    def smiles(self) -> None:
        self._smiles = UNSET

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
    def visual_symbol(self) -> MonomerVisualSymbol:
        """ The shape of the monomer visual symbol. """
        if isinstance(self._visual_symbol, Unset):
            raise NotPresentError(self, "visual_symbol")
        return self._visual_symbol

    @visual_symbol.setter
    def visual_symbol(self, value: MonomerVisualSymbol) -> None:
        self._visual_symbol = value

    @visual_symbol.deleter
    def visual_symbol(self) -> None:
        self._visual_symbol = UNSET
