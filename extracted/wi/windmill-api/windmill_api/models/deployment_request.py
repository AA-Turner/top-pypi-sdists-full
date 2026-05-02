import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.deployment_request_assignees_item import DeploymentRequestAssigneesItem
    from ..models.deployment_request_comments_item import DeploymentRequestCommentsItem


T = TypeVar("T", bound="DeploymentRequest")


@_attrs_define
class DeploymentRequest:
    """
    Attributes:
        id (int):
        source_workspace_id (str):
        fork_workspace_id (str):
        requested_by (str):
        requested_by_email (str):
        requested_at (datetime.datetime):
        assignees (List['DeploymentRequestAssigneesItem']):
        comments (List['DeploymentRequestCommentsItem']):
    """

    id: int
    source_workspace_id: str
    fork_workspace_id: str
    requested_by: str
    requested_by_email: str
    requested_at: datetime.datetime
    assignees: List["DeploymentRequestAssigneesItem"]
    comments: List["DeploymentRequestCommentsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        source_workspace_id = self.source_workspace_id
        fork_workspace_id = self.fork_workspace_id
        requested_by = self.requested_by
        requested_by_email = self.requested_by_email
        requested_at = self.requested_at.isoformat()

        assignees = []
        for assignees_item_data in self.assignees:
            assignees_item = assignees_item_data.to_dict()

            assignees.append(assignees_item)

        comments = []
        for comments_item_data in self.comments:
            comments_item = comments_item_data.to_dict()

            comments.append(comments_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "source_workspace_id": source_workspace_id,
                "fork_workspace_id": fork_workspace_id,
                "requested_by": requested_by,
                "requested_by_email": requested_by_email,
                "requested_at": requested_at,
                "assignees": assignees,
                "comments": comments,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.deployment_request_assignees_item import DeploymentRequestAssigneesItem
        from ..models.deployment_request_comments_item import DeploymentRequestCommentsItem

        d = src_dict.copy()
        id = d.pop("id")

        source_workspace_id = d.pop("source_workspace_id")

        fork_workspace_id = d.pop("fork_workspace_id")

        requested_by = d.pop("requested_by")

        requested_by_email = d.pop("requested_by_email")

        requested_at = isoparse(d.pop("requested_at"))

        assignees = []
        _assignees = d.pop("assignees")
        for assignees_item_data in _assignees:
            assignees_item = DeploymentRequestAssigneesItem.from_dict(assignees_item_data)

            assignees.append(assignees_item)

        comments = []
        _comments = d.pop("comments")
        for comments_item_data in _comments:
            comments_item = DeploymentRequestCommentsItem.from_dict(comments_item_data)

            comments.append(comments_item)

        deployment_request = cls(
            id=id,
            source_workspace_id=source_workspace_id,
            fork_workspace_id=fork_workspace_id,
            requested_by=requested_by,
            requested_by_email=requested_by_email,
            requested_at=requested_at,
            assignees=assignees,
            comments=comments,
        )

        deployment_request.additional_properties = d
        return deployment_request

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
