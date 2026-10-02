from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.link_request import LinkRequest


T = TypeVar("T", bound="SetLinksRequest")


@_attrs_define
class SetLinksRequest:
    """
    Attributes:
        award (Union['LinkRequest', None, Unset]):
        call (Union['LinkRequest', None, Unset]):
        project_link (Union['LinkRequest', None, Unset]):
        renewal (Union['LinkRequest', None, Unset]):
    """

    award: Union["LinkRequest", None, Unset] = UNSET
    call: Union["LinkRequest", None, Unset] = UNSET
    project_link: Union["LinkRequest", None, Unset] = UNSET
    renewal: Union["LinkRequest", None, Unset] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        from ..models.link_request import LinkRequest

        award: Union[None, Unset, dict[str, Any]]
        if isinstance(self.award, Unset):
            award = UNSET
        elif isinstance(self.award, LinkRequest):
            award = self.award.to_dict()
        else:
            award = self.award

        call: Union[None, Unset, dict[str, Any]]
        if isinstance(self.call, Unset):
            call = UNSET
        elif isinstance(self.call, LinkRequest):
            call = self.call.to_dict()
        else:
            call = self.call

        project_link: Union[None, Unset, dict[str, Any]]
        if isinstance(self.project_link, Unset):
            project_link = UNSET
        elif isinstance(self.project_link, LinkRequest):
            project_link = self.project_link.to_dict()
        else:
            project_link = self.project_link

        renewal: Union[None, Unset, dict[str, Any]]
        if isinstance(self.renewal, Unset):
            renewal = UNSET
        elif isinstance(self.renewal, LinkRequest):
            renewal = self.renewal.to_dict()
        else:
            renewal = self.renewal

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if award is not UNSET:
            field_dict["award"] = award
        if call is not UNSET:
            field_dict["call"] = call
        if project_link is not UNSET:
            field_dict["project_link"] = project_link
        if renewal is not UNSET:
            field_dict["renewal"] = renewal

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.link_request import LinkRequest

        d = dict(src_dict)

        def _parse_award(data: object) -> Union["LinkRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                award_type_1 = LinkRequest.from_dict(data)

                return award_type_1
            except:  # noqa: E722
                pass
            return cast(Union["LinkRequest", None, Unset], data)

        award = _parse_award(d.pop("award", UNSET))

        def _parse_call(data: object) -> Union["LinkRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                call_type_1 = LinkRequest.from_dict(data)

                return call_type_1
            except:  # noqa: E722
                pass
            return cast(Union["LinkRequest", None, Unset], data)

        call = _parse_call(d.pop("call", UNSET))

        def _parse_project_link(data: object) -> Union["LinkRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                project_link_type_1 = LinkRequest.from_dict(data)

                return project_link_type_1
            except:  # noqa: E722
                pass
            return cast(Union["LinkRequest", None, Unset], data)

        project_link = _parse_project_link(d.pop("project_link", UNSET))

        def _parse_renewal(data: object) -> Union["LinkRequest", None, Unset]:
            if data is None:
                return data
            if isinstance(data, Unset):
                return data
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                renewal_type_1 = LinkRequest.from_dict(data)

                return renewal_type_1
            except:  # noqa: E722
                pass
            return cast(Union["LinkRequest", None, Unset], data)

        renewal = _parse_renewal(d.pop("renewal", UNSET))

        set_links_request = cls(
            award=award,
            call=call,
            project_link=project_link,
            renewal=renewal,
        )

        set_links_request.additional_properties = d
        return set_links_request

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
