from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from typing import cast

if TYPE_CHECKING:
  from ..models.managed_agents_pull_request_summary import ManagedAgentsPullRequestSummary





T = TypeVar("T", bound="ManagedAgentsPullRequests")



@_attrs_define
class ManagedAgentsPullRequests:
    """ One page of pull requests in a GitHub repository reachable through an integration connection. Returned to populate a
    pull request picker.

        Example:
            {'page': 1, 'pull_requests': [{'draft': True, 'head_sha': 'example', 'number': 1, 'title': 'example'}]}

        Attributes:
            page (int): 1-based page this response covers. Defaults to 1 when the request omits or under-specifies it.
            pull_requests (list[ManagedAgentsPullRequestSummary] | None): Pull requests reachable on this page, up to 100
                per page.
     """

    page: int
    pull_requests: list[ManagedAgentsPullRequestSummary] | None
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.managed_agents_pull_request_summary import ManagedAgentsPullRequestSummary # noqa: PLC0415
        page = self.page

        pull_requests: list[dict[str, Any]] | None
        if isinstance(self.pull_requests, list):
            pull_requests = []
            for pull_requests_type_0_item_data in self.pull_requests:
                pull_requests_type_0_item = pull_requests_type_0_item_data.to_dict()
                pull_requests.append(pull_requests_type_0_item)


        else:
            pull_requests = self.pull_requests


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "page": page,
            "pull_requests": pull_requests,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.managed_agents_pull_request_summary import ManagedAgentsPullRequestSummary # noqa: PLC0415
        d = dict(src_dict)
        page = d.pop("page")

        def _parse_pull_requests(data: object) -> list[ManagedAgentsPullRequestSummary] | None:
            if data is None:
                return data
            try:
                if not isinstance(data, list):
                    raise TypeError()
                pull_requests_type_0 = []
                _pull_requests_type_0 = data
                for pull_requests_type_0_item_data in (_pull_requests_type_0):
                    pull_requests_type_0_item = ManagedAgentsPullRequestSummary.from_dict(pull_requests_type_0_item_data)



                    pull_requests_type_0.append(pull_requests_type_0_item)

                return pull_requests_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            return cast(list[ManagedAgentsPullRequestSummary] | None, data)

        pull_requests = _parse_pull_requests(d.pop("pull_requests"))


        managed_agents_pull_requests = cls(
            page=page,
            pull_requests=pull_requests,
        )


        managed_agents_pull_requests.additional_properties = d
        return managed_agents_pull_requests

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
