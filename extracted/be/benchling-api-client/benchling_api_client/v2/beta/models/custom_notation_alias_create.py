from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError
from ..types import UNSET, Unset

T = TypeVar("T", bound="CustomNotationAliasCreate")


@attr.s(auto_attribs=True, repr=False)
class CustomNotationAliasCreate:
    """  """

    _base_monomer_id: str
    _custom_notation_id: str
    _sugar_monomer_id: str
    _token: str
    _phosphate_monomer_id: Optional[str]
    _rank: Union[Unset, None, float] = 1.0
    _token_variant_end: Union[Unset, None, str] = UNSET
    _token_variant_start: Union[Unset, None, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("base_monomer_id={}".format(repr(self._base_monomer_id)))
        fields.append("custom_notation_id={}".format(repr(self._custom_notation_id)))
        fields.append("sugar_monomer_id={}".format(repr(self._sugar_monomer_id)))
        fields.append("token={}".format(repr(self._token)))
        fields.append("phosphate_monomer_id={}".format(repr(self._phosphate_monomer_id)))
        fields.append("rank={}".format(repr(self._rank)))
        fields.append("token_variant_end={}".format(repr(self._token_variant_end)))
        fields.append("token_variant_start={}".format(repr(self._token_variant_start)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "CustomNotationAliasCreate({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        base_monomer_id = self._base_monomer_id
        custom_notation_id = self._custom_notation_id
        sugar_monomer_id = self._sugar_monomer_id
        token = self._token
        phosphate_monomer_id = self._phosphate_monomer_id
        rank = self._rank
        token_variant_end = self._token_variant_end
        token_variant_start = self._token_variant_start

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if base_monomer_id is not UNSET:
            field_dict["baseMonomerId"] = base_monomer_id
        if custom_notation_id is not UNSET:
            field_dict["customNotationId"] = custom_notation_id
        if sugar_monomer_id is not UNSET:
            field_dict["sugarMonomerId"] = sugar_monomer_id
        if token is not UNSET:
            field_dict["token"] = token
        if phosphate_monomer_id is not UNSET:
            field_dict["phosphateMonomerId"] = phosphate_monomer_id
        if rank is not UNSET:
            field_dict["rank"] = rank
        if token_variant_end is not UNSET:
            field_dict["tokenVariantEnd"] = token_variant_end
        if token_variant_start is not UNSET:
            field_dict["tokenVariantStart"] = token_variant_start

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_base_monomer_id() -> str:
            base_monomer_id = d.pop("baseMonomerId")
            return base_monomer_id

        try:
            base_monomer_id = get_base_monomer_id()
        except KeyError:
            if strict:
                raise
            base_monomer_id = cast(str, UNSET)

        def get_custom_notation_id() -> str:
            custom_notation_id = d.pop("customNotationId")
            return custom_notation_id

        try:
            custom_notation_id = get_custom_notation_id()
        except KeyError:
            if strict:
                raise
            custom_notation_id = cast(str, UNSET)

        def get_sugar_monomer_id() -> str:
            sugar_monomer_id = d.pop("sugarMonomerId")
            return sugar_monomer_id

        try:
            sugar_monomer_id = get_sugar_monomer_id()
        except KeyError:
            if strict:
                raise
            sugar_monomer_id = cast(str, UNSET)

        def get_token() -> str:
            token = d.pop("token")
            return token

        try:
            token = get_token()
        except KeyError:
            if strict:
                raise
            token = cast(str, UNSET)

        def get_phosphate_monomer_id() -> Optional[str]:
            phosphate_monomer_id = d.pop("phosphateMonomerId")
            return phosphate_monomer_id

        try:
            phosphate_monomer_id = get_phosphate_monomer_id()
        except KeyError:
            if strict:
                raise
            phosphate_monomer_id = cast(Optional[str], UNSET)

        def get_rank() -> Union[Unset, None, float]:
            rank = d.pop("rank")
            return rank

        try:
            rank = get_rank()
        except KeyError:
            if strict:
                raise
            rank = cast(Union[Unset, None, float], UNSET)

        def get_token_variant_end() -> Union[Unset, None, str]:
            token_variant_end = d.pop("tokenVariantEnd")
            return token_variant_end

        try:
            token_variant_end = get_token_variant_end()
        except KeyError:
            if strict:
                raise
            token_variant_end = cast(Union[Unset, None, str], UNSET)

        def get_token_variant_start() -> Union[Unset, None, str]:
            token_variant_start = d.pop("tokenVariantStart")
            return token_variant_start

        try:
            token_variant_start = get_token_variant_start()
        except KeyError:
            if strict:
                raise
            token_variant_start = cast(Union[Unset, None, str], UNSET)

        custom_notation_alias_create = cls(
            base_monomer_id=base_monomer_id,
            custom_notation_id=custom_notation_id,
            sugar_monomer_id=sugar_monomer_id,
            token=token,
            phosphate_monomer_id=phosphate_monomer_id,
            rank=rank,
            token_variant_end=token_variant_end,
            token_variant_start=token_variant_start,
        )

        custom_notation_alias_create.additional_properties = d
        return custom_notation_alias_create

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
    def base_monomer_id(self) -> str:
        """ The API identifier of the base monomer represented in this token. """
        if isinstance(self._base_monomer_id, Unset):
            raise NotPresentError(self, "base_monomer_id")
        return self._base_monomer_id

    @base_monomer_id.setter
    def base_monomer_id(self, value: str) -> None:
        self._base_monomer_id = value

    @property
    def custom_notation_id(self) -> str:
        """ The API identifier of the custom notation with which to associate this alias. """
        if isinstance(self._custom_notation_id, Unset):
            raise NotPresentError(self, "custom_notation_id")
        return self._custom_notation_id

    @custom_notation_id.setter
    def custom_notation_id(self, value: str) -> None:
        self._custom_notation_id = value

    @property
    def sugar_monomer_id(self) -> str:
        """ The API identifier of the sugar monomer represented in this token. """
        if isinstance(self._sugar_monomer_id, Unset):
            raise NotPresentError(self, "sugar_monomer_id")
        return self._sugar_monomer_id

    @sugar_monomer_id.setter
    def sugar_monomer_id(self, value: str) -> None:
        self._sugar_monomer_id = value

    @property
    def token(self) -> str:
        """ An arbitrary string token to represent this modified nucleotide. """
        if isinstance(self._token, Unset):
            raise NotPresentError(self, "token")
        return self._token

    @token.setter
    def token(self, value: str) -> None:
        self._token = value

    @property
    def phosphate_monomer_id(self) -> Optional[str]:
        """ The API identifier of the phosphate monomer represented in this token. """
        if isinstance(self._phosphate_monomer_id, Unset):
            raise NotPresentError(self, "phosphate_monomer_id")
        return self._phosphate_monomer_id

    @phosphate_monomer_id.setter
    def phosphate_monomer_id(self, value: Optional[str]) -> None:
        self._phosphate_monomer_id = value

    @property
    def rank(self) -> Optional[float]:
        """The rank of the token. It is possible to configure multiple aliases for the same monomers,
        in which case rank determines precedence when generating custom notation from a Benchling
        sequence. Lower ranks denote higher priority.
        """
        if isinstance(self._rank, Unset):
            raise NotPresentError(self, "rank")
        return self._rank

    @rank.setter
    def rank(self, value: Optional[float]) -> None:
        self._rank = value

    @rank.deleter
    def rank(self) -> None:
        self._rank = UNSET

    @property
    def token_variant_end(self) -> Optional[str]:
        """ Optional variant form of alias token, only valid for the last 3' nucleotide on a modified sequence. """
        if isinstance(self._token_variant_end, Unset):
            raise NotPresentError(self, "token_variant_end")
        return self._token_variant_end

    @token_variant_end.setter
    def token_variant_end(self, value: Optional[str]) -> None:
        self._token_variant_end = value

    @token_variant_end.deleter
    def token_variant_end(self) -> None:
        self._token_variant_end = UNSET

    @property
    def token_variant_start(self) -> Optional[str]:
        """ Optional variant form of alias token, only valid for the first 5' nucleotide on a modified sequence. """
        if isinstance(self._token_variant_start, Unset):
            raise NotPresentError(self, "token_variant_start")
        return self._token_variant_start

    @token_variant_start.setter
    def token_variant_start(self, value: Optional[str]) -> None:
        self._token_variant_start = value

    @token_variant_start.deleter
    def token_variant_start(self) -> None:
        self._token_variant_start = UNSET
