from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.global_offboard_preview_workspaces_item_preview_executing_on_behalf import (
        GlobalOffboardPreviewWorkspacesItemPreviewExecutingOnBehalf,
    )
    from ..models.global_offboard_preview_workspaces_item_preview_owned import (
        GlobalOffboardPreviewWorkspacesItemPreviewOwned,
    )
    from ..models.global_offboard_preview_workspaces_item_preview_referencing import (
        GlobalOffboardPreviewWorkspacesItemPreviewReferencing,
    )
    from ..models.global_offboard_preview_workspaces_item_preview_tokens_item import (
        GlobalOffboardPreviewWorkspacesItemPreviewTokensItem,
    )


T = TypeVar("T", bound="GlobalOffboardPreviewWorkspacesItemPreview")


@_attrs_define
class GlobalOffboardPreviewWorkspacesItemPreview:
    """
    Attributes:
        owned (GlobalOffboardPreviewWorkspacesItemPreviewOwned): Objects under u/{username}/ that will be reassigned
        executing_on_behalf (GlobalOffboardPreviewWorkspacesItemPreviewExecutingOnBehalf): Objects not under the user's
            path but that execute on behalf of this user (permissioned_as/on_behalf_of will be updated)
        referencing (GlobalOffboardPreviewWorkspacesItemPreviewReferencing): Scripts/flows/apps/resources whose content
            or value references this user's paths (may break after reassignment)
        tokens (List['GlobalOffboardPreviewWorkspacesItemPreviewTokensItem']): Tokens owned by this user (will be
            deleted)
        http_triggers (int): HTTP triggers under the user's path (webhook URLs will change)
        email_triggers (int): Email triggers under the user's path (email addresses will change)
    """

    owned: "GlobalOffboardPreviewWorkspacesItemPreviewOwned"
    executing_on_behalf: "GlobalOffboardPreviewWorkspacesItemPreviewExecutingOnBehalf"
    referencing: "GlobalOffboardPreviewWorkspacesItemPreviewReferencing"
    tokens: List["GlobalOffboardPreviewWorkspacesItemPreviewTokensItem"]
    http_triggers: int
    email_triggers: int
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        owned = self.owned.to_dict()

        executing_on_behalf = self.executing_on_behalf.to_dict()

        referencing = self.referencing.to_dict()

        tokens = []
        for tokens_item_data in self.tokens:
            tokens_item = tokens_item_data.to_dict()

            tokens.append(tokens_item)

        http_triggers = self.http_triggers
        email_triggers = self.email_triggers

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "owned": owned,
                "executing_on_behalf": executing_on_behalf,
                "referencing": referencing,
                "tokens": tokens,
                "http_triggers": http_triggers,
                "email_triggers": email_triggers,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.global_offboard_preview_workspaces_item_preview_executing_on_behalf import (
            GlobalOffboardPreviewWorkspacesItemPreviewExecutingOnBehalf,
        )
        from ..models.global_offboard_preview_workspaces_item_preview_owned import (
            GlobalOffboardPreviewWorkspacesItemPreviewOwned,
        )
        from ..models.global_offboard_preview_workspaces_item_preview_referencing import (
            GlobalOffboardPreviewWorkspacesItemPreviewReferencing,
        )
        from ..models.global_offboard_preview_workspaces_item_preview_tokens_item import (
            GlobalOffboardPreviewWorkspacesItemPreviewTokensItem,
        )

        d = src_dict.copy()
        owned = GlobalOffboardPreviewWorkspacesItemPreviewOwned.from_dict(d.pop("owned"))

        executing_on_behalf = GlobalOffboardPreviewWorkspacesItemPreviewExecutingOnBehalf.from_dict(
            d.pop("executing_on_behalf")
        )

        referencing = GlobalOffboardPreviewWorkspacesItemPreviewReferencing.from_dict(d.pop("referencing"))

        tokens = []
        _tokens = d.pop("tokens")
        for tokens_item_data in _tokens:
            tokens_item = GlobalOffboardPreviewWorkspacesItemPreviewTokensItem.from_dict(tokens_item_data)

            tokens.append(tokens_item)

        http_triggers = d.pop("http_triggers")

        email_triggers = d.pop("email_triggers")

        global_offboard_preview_workspaces_item_preview = cls(
            owned=owned,
            executing_on_behalf=executing_on_behalf,
            referencing=referencing,
            tokens=tokens,
            http_triggers=http_triggers,
            email_triggers=email_triggers,
        )

        global_offboard_preview_workspaces_item_preview.additional_properties = d
        return global_offboard_preview_workspaces_item_preview

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
