from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.canned_response_render_request_context import CannedResponseRenderRequestContext


T = TypeVar("T", bound="CannedResponseRenderRequest")


@_attrs_define
class CannedResponseRenderRequest:
    """
    Attributes:
        context (Union[Unset, CannedResponseRenderRequestContext]):
    """

    context: Union[Unset, "CannedResponseRenderRequestContext"] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        context: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.context, Unset):
            context = self.context.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if context is not UNSET:
            field_dict["context"] = context

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.canned_response_render_request_context import CannedResponseRenderRequestContext

        d = dict(src_dict)
        _context = d.pop("context", UNSET)
        context: Union[Unset, CannedResponseRenderRequestContext]
        if isinstance(_context, Unset):
            context = UNSET
        else:
            context = CannedResponseRenderRequestContext.from_dict(_context)

        canned_response_render_request = cls(
            context=context,
        )

        canned_response_render_request.additional_properties = d
        return canned_response_render_request

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
