from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.main_arg_signature_type import MainArgSignatureType
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.main_arg_signature_args_item import MainArgSignatureArgsItem


T = TypeVar("T", bound="MainArgSignature")


@_attrs_define
class MainArgSignature:
    """
    Attributes:
        type (MainArgSignatureType):
        error (str):
        star_args (bool):
        args (List['MainArgSignatureArgsItem']):
        star_kwargs (Union[Unset, bool]):
        no_main_func (Optional[bool]):
        has_preprocessor (Optional[bool]):
    """

    type: MainArgSignatureType
    error: str
    star_args: bool
    args: List["MainArgSignatureArgsItem"]
    no_main_func: Optional[bool]
    has_preprocessor: Optional[bool]
    star_kwargs: Union[Unset, bool] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        type = self.type.value

        error = self.error
        star_args = self.star_args
        args = []
        for args_item_data in self.args:
            args_item = args_item_data.to_dict()

            args.append(args_item)

        star_kwargs = self.star_kwargs
        no_main_func = self.no_main_func
        has_preprocessor = self.has_preprocessor

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "type": type,
                "error": error,
                "star_args": star_args,
                "args": args,
                "no_main_func": no_main_func,
                "has_preprocessor": has_preprocessor,
            }
        )
        if star_kwargs is not UNSET:
            field_dict["star_kwargs"] = star_kwargs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.main_arg_signature_args_item import MainArgSignatureArgsItem

        d = src_dict.copy()
        type = MainArgSignatureType(d.pop("type"))

        error = d.pop("error")

        star_args = d.pop("star_args")

        args = []
        _args = d.pop("args")
        for args_item_data in _args:
            args_item = MainArgSignatureArgsItem.from_dict(args_item_data)

            args.append(args_item)

        star_kwargs = d.pop("star_kwargs", UNSET)

        no_main_func = d.pop("no_main_func")

        has_preprocessor = d.pop("has_preprocessor")

        main_arg_signature = cls(
            type=type,
            error=error,
            star_args=star_args,
            args=args,
            star_kwargs=star_kwargs,
            no_main_func=no_main_func,
            has_preprocessor=has_preprocessor,
        )

        main_arg_signature.additional_properties = d
        return main_arg_signature

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
