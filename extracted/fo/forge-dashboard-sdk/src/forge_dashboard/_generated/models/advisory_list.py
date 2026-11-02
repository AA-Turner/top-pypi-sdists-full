from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.advisory_reason import AdvisoryReason
from ..models.advisory_state import AdvisoryState
from ..types import UNSET, Unset
from typing import cast

if TYPE_CHECKING:
  from ..models.advisory_item import AdvisoryItem





T = TypeVar("T", bound="AdvisoryList")



@_attrs_define
class AdvisoryList:
    """ A repository's open dependency advisories in full.

        Attributes:
            state (AdvisoryState): "known" is an answer the forge gave. "unknown" is no answer, and must
                never be shown as zero.
            advisories (list[AdvisoryItem]): Empty when none are open and whenever `state` is "unknown". Highest severity
                first, then newest first.
            reason (AdvisoryReason | Unset): Why `state` is "unknown", when the dashboard can tell. Absent when
                the state is "known". "refused" is a 403: the credential lacks the
                Dependabot alerts permission. "switched_off" is a 404: alerts are off
                for the repository. "throttled" is a rate limit, which clears by
                itself. "failed" is any other error reading the alerts. "too_many" is
                a repository with more open alerts than one read pages through. On a
                Forgejo repository, "not_enabled" is the operator not having switched
                on lockfile checking (it is off by default, since it sends package
                names to a third party), absent when it has no lockfile the dashboard
                reads, and "failed" when one is too big or doesn't parse. A Forgejo
                repository whose advisories have not been read yet, because its first
                read is still running in the background, is "unknown" with no reason.
            partial (bool | Unset): Set on a known Forgejo list that leaves out packages the dashboard may not send to OSV,
                because they may be private. Absent otherwise.
            url (str | Unset): The repository's advisories page on the forge. Absent when none are open or the state is
                unknown, and for Forgejo, which has no page for a whole repository.
     """

    state: AdvisoryState
    advisories: list[AdvisoryItem]
    reason: AdvisoryReason | Unset = UNSET
    partial: bool | Unset = UNSET
    url: str | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        from ..models.advisory_item import AdvisoryItem # noqa: PLC0415
        state = self.state.value

        advisories = []
        for advisories_item_data in self.advisories:
            advisories_item = advisories_item_data.to_dict()
            advisories.append(advisories_item)



        reason: str | Unset = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value


        partial = self.partial

        url = self.url


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "state": state,
            "advisories": advisories,
        })
        if reason is not UNSET:
            field_dict["reason"] = reason
        if partial is not UNSET:
            field_dict["partial"] = partial
        if url is not UNSET:
            field_dict["url"] = url

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.advisory_item import AdvisoryItem # noqa: PLC0415
        d = dict(src_dict)
        state = AdvisoryState(d.pop("state"))




        advisories = []
        _advisories = d.pop("advisories")
        for advisories_item_data in (_advisories):
            advisories_item = AdvisoryItem.from_dict(advisories_item_data)



            advisories.append(advisories_item)


        _reason = d.pop("reason", UNSET)
        reason: AdvisoryReason | Unset
        if isinstance(_reason,  Unset):
            reason = UNSET
        else:
            reason = AdvisoryReason(_reason)




        partial = d.pop("partial", UNSET)

        url = d.pop("url", UNSET)

        advisory_list = cls(
            state=state,
            advisories=advisories,
            reason=reason,
            partial=partial,
            url=url,
        )


        advisory_list.additional_properties = d
        return advisory_list

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
