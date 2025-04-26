from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..models.custom_notation_create_use_shared_delimiter import CustomNotationCreateUseSharedDelimiter
from ..models.custom_notation_prefilter_terminals import CustomNotationPrefilterTerminals
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotationCreate")


@attr.s(auto_attribs=True, repr=False)
class CustomNotationCreate:
    """  """

    _is_case_sensitive: Union[Unset, bool] = UNSET
    _name: Union[Unset, str] = UNSET
    _nullify_end_phosphate: Union[Unset, bool] = UNSET
    _prefilter_terminals: Union[Unset, CustomNotationPrefilterTerminals] = UNSET
    _use_shared_delimiter: Union[Unset, CustomNotationCreateUseSharedDelimiter] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("is_case_sensitive={}".format(repr(self._is_case_sensitive)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("nullify_end_phosphate={}".format(repr(self._nullify_end_phosphate)))
        fields.append("prefilter_terminals={}".format(repr(self._prefilter_terminals)))
        fields.append("use_shared_delimiter={}".format(repr(self._use_shared_delimiter)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CustomNotationCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        is_case_sensitive = self._is_case_sensitive
        name = self._name
        nullify_end_phosphate = self._nullify_end_phosphate
        prefilter_terminals: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._prefilter_terminals, Unset):
            prefilter_terminals = self._prefilter_terminals.to_dict()

        use_shared_delimiter: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._use_shared_delimiter, Unset):
            use_shared_delimiter = self._use_shared_delimiter.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if is_case_sensitive is not UNSET:
            field_dict["isCaseSensitive"] = is_case_sensitive
        if name is not UNSET:
            field_dict["name"] = name
        if nullify_end_phosphate is not UNSET:
            field_dict["nullifyEndPhosphate"] = nullify_end_phosphate
        if prefilter_terminals is not UNSET:
            field_dict["prefilterTerminals"] = prefilter_terminals
        if use_shared_delimiter is not UNSET:
            field_dict["useSharedDelimiter"] = use_shared_delimiter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_is_case_sensitive() -> Union[Unset, bool]:
            is_case_sensitive = d.pop("isCaseSensitive")
            return is_case_sensitive

        try:
            is_case_sensitive = get_is_case_sensitive()
        except KeyError:
            if strict:
                raise
            is_case_sensitive = cast(Union[Unset, bool], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_nullify_end_phosphate() -> Union[Unset, bool]:
            nullify_end_phosphate = d.pop("nullifyEndPhosphate")
            return nullify_end_phosphate

        try:
            nullify_end_phosphate = get_nullify_end_phosphate()
        except KeyError:
            if strict:
                raise
            nullify_end_phosphate = cast(Union[Unset, bool], UNSET)

        def get_prefilter_terminals() -> Union[Unset, CustomNotationPrefilterTerminals]:
            prefilter_terminals: Union[Unset, Union[Unset, CustomNotationPrefilterTerminals]] = UNSET
            _prefilter_terminals = d.pop("prefilterTerminals")

            if not isinstance(_prefilter_terminals, Unset):
                prefilter_terminals = CustomNotationPrefilterTerminals.from_dict(_prefilter_terminals)

            return prefilter_terminals

        try:
            prefilter_terminals = get_prefilter_terminals()
        except KeyError:
            if strict:
                raise
            prefilter_terminals = cast(Union[Unset, CustomNotationPrefilterTerminals], UNSET)

        def get_use_shared_delimiter() -> Union[Unset, CustomNotationCreateUseSharedDelimiter]:
            use_shared_delimiter: Union[Unset, Union[Unset, CustomNotationCreateUseSharedDelimiter]] = UNSET
            _use_shared_delimiter = d.pop("useSharedDelimiter")

            if not isinstance(_use_shared_delimiter, Unset):
                use_shared_delimiter = CustomNotationCreateUseSharedDelimiter.from_dict(_use_shared_delimiter)

            return use_shared_delimiter

        try:
            use_shared_delimiter = get_use_shared_delimiter()
        except KeyError:
            if strict:
                raise
            use_shared_delimiter = cast(Union[Unset, CustomNotationCreateUseSharedDelimiter], UNSET)

        custom_notation_create = cls(
            is_case_sensitive=is_case_sensitive,
            name=name,
            nullify_end_phosphate=nullify_end_phosphate,
            prefilter_terminals=prefilter_terminals,
            use_shared_delimiter=use_shared_delimiter,
        )

        custom_notation_create.additional_properties = d
        return custom_notation_create

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
    def is_case_sensitive(self) -> bool:
        """ Whether the custom notation is case sensitive. """
        if isinstance(self._is_case_sensitive, Unset):
            raise NotPresentError(self, "is_case_sensitive")
        return self._is_case_sensitive

    @is_case_sensitive.setter
    def is_case_sensitive(self, value: bool) -> None:
        self._is_case_sensitive = value

    @is_case_sensitive.deleter
    def is_case_sensitive(self) -> None:
        self._is_case_sensitive = UNSET

    @property
    def name(self) -> str:
        """ Name of custom notation """
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
    def nullify_end_phosphate(self) -> bool:
        """ When enabled, the parser will emit a null phosphate for any token mapped to a natural phosphate when it occurs as the final 3' nucleotide in a sequence. """
        if isinstance(self._nullify_end_phosphate, Unset):
            raise NotPresentError(self, "nullify_end_phosphate")
        return self._nullify_end_phosphate

    @nullify_end_phosphate.setter
    def nullify_end_phosphate(self, value: bool) -> None:
        self._nullify_end_phosphate = value

    @nullify_end_phosphate.deleter
    def nullify_end_phosphate(self) -> None:
        self._nullify_end_phosphate = UNSET

    @property
    def prefilter_terminals(self) -> CustomNotationPrefilterTerminals:
        """ Configuration for an optional feature where unrecognized tokens at the 5'/3' terminal ends of an input sequence can be stripped and output to schema fields. """
        if isinstance(self._prefilter_terminals, Unset):
            raise NotPresentError(self, "prefilter_terminals")
        return self._prefilter_terminals

    @prefilter_terminals.setter
    def prefilter_terminals(self, value: CustomNotationPrefilterTerminals) -> None:
        self._prefilter_terminals = value

    @prefilter_terminals.deleter
    def prefilter_terminals(self) -> None:
        self._prefilter_terminals = UNSET

    @property
    def use_shared_delimiter(self) -> CustomNotationCreateUseSharedDelimiter:
        """ By default the system assumes that all delimiters "belong" to a single token (such as in a notation like "[A][B][C]"). This setting allows specifying a single "shared" delimiter instead, e.g. the commas in "A,B,C". """
        if isinstance(self._use_shared_delimiter, Unset):
            raise NotPresentError(self, "use_shared_delimiter")
        return self._use_shared_delimiter

    @use_shared_delimiter.setter
    def use_shared_delimiter(self, value: CustomNotationCreateUseSharedDelimiter) -> None:
        self._use_shared_delimiter = value

    @use_shared_delimiter.deleter
    def use_shared_delimiter(self) -> None:
        self._use_shared_delimiter = UNSET
