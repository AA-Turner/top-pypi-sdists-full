from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar, BinaryIO, TextIO, TYPE_CHECKING, Generator

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

from ..models.forge import Forge
from ..models.item_reference_direction import ItemReferenceDirection
from ..models.item_reference_kind import ItemReferenceKind
from ..models.item_reference_relation import ItemReferenceRelation
from ..models.item_reference_state import ItemReferenceState






T = TypeVar("T", bound="ItemReference")



@_attrs_define
class ItemReference:
    """ One issue or pull request that is related to the item whose details were asked for.

        Attributes:
            forge (Forge):
            repo (str): The related item's repository as `owner/name`, which is not always the asked-for item's own.
            number (int):
            title (str): The related item's title, as the forge has it now.
            url (str): The related item's address on the forge.
            page_url (str): The address on this dashboard that opens the related item's pop-up:
                `/pull-requests.html?pr=` or `/issues.html?issue=`, then
                `forge/owner/name/number`. A relative address.
            kind (ItemReferenceKind): What the related number is. A forge shares one number space between the two.
            state (ItemReferenceState): Where the related item stands. Only a pull request is `merged`; `closed` means
                closed without merging.
            direction (ItemReferenceDirection): `incoming` when the related item refers to the asked-for one,
                `outgoing` when the asked-for one refers to it. The `relation` is
                always the referring item's: what the related item does to the
                asked-for one when `incoming`, what the asked-for one does to the
                related item when `outgoing`.
            relation (ItemReferenceRelation): What the referring item does to the referred-to one. `closes`
                closes it when merged (a closing keyword). `refs` references it
                without closing it (`Refs`, `Related to`, `See`). `mentions` only
                names it. An item holds one relation to the asked-for one, the
                strongest it has: `closes`, then `refs`, then `mentions`. The
                forge's timeline does not tell `refs` from `mentions`, so for an
                `incoming` entry the referring item's own description is read for
                a `Refs`, `Related to` or `See` on the asked-for item; a `closes`
                the forge reports is kept.
     """

    forge: Forge
    repo: str
    number: int
    title: str
    url: str
    page_url: str
    kind: ItemReferenceKind
    state: ItemReferenceState
    direction: ItemReferenceDirection
    relation: ItemReferenceRelation
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)





    def to_dict(self) -> dict[str, Any]:
        forge = self.forge.value

        repo = self.repo

        number = self.number

        title = self.title

        url = self.url

        page_url = self.page_url

        kind = self.kind.value

        state = self.state.value

        direction = self.direction.value

        relation = self.relation.value


        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({
            "forge": forge,
            "repo": repo,
            "number": number,
            "title": title,
            "url": url,
            "pageUrl": page_url,
            "kind": kind,
            "state": state,
            "direction": direction,
            "relation": relation,
        })

        return field_dict



    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        forge = Forge(d.pop("forge"))




        repo = d.pop("repo")

        number = d.pop("number")

        title = d.pop("title")

        url = d.pop("url")

        page_url = d.pop("pageUrl")

        kind = ItemReferenceKind(d.pop("kind"))




        state = ItemReferenceState(d.pop("state"))




        direction = ItemReferenceDirection(d.pop("direction"))




        relation = ItemReferenceRelation(d.pop("relation"))




        item_reference = cls(
            forge=forge,
            repo=repo,
            number=number,
            title=title,
            url=url,
            page_url=page_url,
            kind=kind,
            state=state,
            direction=direction,
            relation=relation,
        )


        item_reference.additional_properties = d
        return item_reference

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
