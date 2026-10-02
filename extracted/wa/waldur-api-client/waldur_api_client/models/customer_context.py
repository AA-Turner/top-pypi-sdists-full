from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.caller_context import CallerContext
    from ..models.recent_ticket import RecentTicket
    from ..models.resource_context import ResourceContext


T = TypeVar("T", bound="CustomerContext")


@_attrs_define
class CustomerContext:
    """
    Attributes:
        caller (CallerContext):
        resource (Union['ResourceContext', None]):
        recent_tickets (list['RecentTicket']):
    """

    caller: "CallerContext"
    resource: Union["ResourceContext", None]
    recent_tickets: list["RecentTicket"]
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.resource_context import ResourceContext

        caller = self.caller.to_dict()

        resource: Union[None, dict[str, Any]]
        if isinstance(self.resource, ResourceContext):
            resource = self.resource.to_dict()
        else:
            resource = self.resource

        recent_tickets = []
        for recent_tickets_item_data in self.recent_tickets:
            recent_tickets_item = recent_tickets_item_data.to_dict()
            recent_tickets.append(recent_tickets_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "caller": caller,
                "resource": resource,
                "recent_tickets": recent_tickets,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.caller_context import CallerContext
        from ..models.recent_ticket import RecentTicket
        from ..models.resource_context import ResourceContext

        d = dict(src_dict)
        caller = CallerContext.from_dict(d.pop("caller"))

        def _parse_resource(data: object) -> Union["ResourceContext", None]:
            if data is None:
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                resource_type_1 = ResourceContext.from_dict(data)

                return resource_type_1
            except:  # noqa: E722
                pass
            return cast(Union["ResourceContext", None], data)

        resource = _parse_resource(d.pop("resource"))

        recent_tickets = []
        _recent_tickets = d.pop("recent_tickets")
        for recent_tickets_item_data in _recent_tickets:
            recent_tickets_item = RecentTicket.from_dict(recent_tickets_item_data)

            recent_tickets.append(recent_tickets_item)

        customer_context = cls(
            caller=caller,
            resource=resource,
            recent_tickets=recent_tickets,
        )

        customer_context.additional_properties = d
        return customer_context

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
