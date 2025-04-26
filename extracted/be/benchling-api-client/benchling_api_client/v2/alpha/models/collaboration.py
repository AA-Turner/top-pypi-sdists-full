from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr

from ..extensions import NotPresentError, UnknownType
from ..models.access_policy import AccessPolicy
from ..models.app_collaborator import AppCollaborator
from ..models.org_membership_collaborator import OrgMembershipCollaborator
from ..models.team_membership_collaborator import TeamMembershipCollaborator
from ..models.user_collaborator import UserCollaborator
from ..types import UNSET, Unset

T = TypeVar("T", bound="Collaboration")


@attr.s(auto_attribs=True, repr=False)
class Collaboration:
    """  """

    _access_policy: Union[Unset, AccessPolicy] = UNSET
    _collaborator: Union[
        Unset,
        OrgMembershipCollaborator,
        TeamMembershipCollaborator,
        UserCollaborator,
        AppCollaborator,
        UnknownType,
    ] = UNSET
    _created_at: Union[Unset, str] = UNSET
    _id: Union[Unset, str] = UNSET
    _item_id: Union[Unset, str] = UNSET
    _item_type: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("access_policy={}".format(repr(self._access_policy)))
        fields.append("collaborator={}".format(repr(self._collaborator)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("item_id={}".format(repr(self._item_id)))
        fields.append("item_type={}".format(repr(self._item_type)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Collaboration({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        access_policy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._access_policy, Unset):
            access_policy = self._access_policy.to_dict()

        collaborator: Union[Unset, Dict[str, Any]]
        if isinstance(self._collaborator, Unset):
            collaborator = UNSET
        elif isinstance(self._collaborator, UnknownType):
            collaborator = self._collaborator.value
        elif isinstance(self._collaborator, OrgMembershipCollaborator):
            collaborator = UNSET
            if not isinstance(self._collaborator, Unset):
                collaborator = self._collaborator.to_dict()

        elif isinstance(self._collaborator, TeamMembershipCollaborator):
            collaborator = UNSET
            if not isinstance(self._collaborator, Unset):
                collaborator = self._collaborator.to_dict()

        elif isinstance(self._collaborator, UserCollaborator):
            collaborator = UNSET
            if not isinstance(self._collaborator, Unset):
                collaborator = self._collaborator.to_dict()

        else:
            collaborator = UNSET
            if not isinstance(self._collaborator, Unset):
                collaborator = self._collaborator.to_dict()

        created_at = self._created_at
        id = self._id
        item_id = self._item_id
        item_type = self._item_type
        modified_at = self._modified_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if access_policy is not UNSET:
            field_dict["accessPolicy"] = access_policy
        if collaborator is not UNSET:
            field_dict["collaborator"] = collaborator
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if id is not UNSET:
            field_dict["id"] = id
        if item_id is not UNSET:
            field_dict["itemId"] = item_id
        if item_type is not UNSET:
            field_dict["itemType"] = item_type
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_access_policy() -> Union[Unset, AccessPolicy]:
            access_policy: Union[Unset, Union[Unset, AccessPolicy]] = UNSET
            _access_policy = d.pop("accessPolicy")

            if not isinstance(_access_policy, Unset):
                access_policy = AccessPolicy.from_dict(_access_policy)

            return access_policy

        try:
            access_policy = get_access_policy()
        except KeyError:
            if strict:
                raise
            access_policy = cast(Union[Unset, AccessPolicy], UNSET)

        def get_collaborator() -> Union[
            Unset,
            OrgMembershipCollaborator,
            TeamMembershipCollaborator,
            UserCollaborator,
            AppCollaborator,
            UnknownType,
        ]:
            collaborator: Union[
                Unset,
                OrgMembershipCollaborator,
                TeamMembershipCollaborator,
                UserCollaborator,
                AppCollaborator,
                UnknownType,
            ]
            _collaborator = d.pop("collaborator")

            if not isinstance(_collaborator, Unset):
                discriminator = _collaborator["type"]
                if discriminator == "APP":
                    collaborator = AppCollaborator.from_dict(_collaborator)
                elif discriminator == "ORGANIZATION_MEMBER":
                    collaborator = OrgMembershipCollaborator.from_dict(_collaborator)
                elif discriminator == "TEAM_MEMBER":
                    collaborator = TeamMembershipCollaborator.from_dict(_collaborator)
                elif discriminator == "USER":
                    collaborator = UserCollaborator.from_dict(_collaborator)
                else:
                    collaborator = UnknownType(value=_collaborator)

            return collaborator

        try:
            collaborator = get_collaborator()
        except KeyError:
            if strict:
                raise
            collaborator = cast(
                Union[
                    Unset,
                    OrgMembershipCollaborator,
                    TeamMembershipCollaborator,
                    UserCollaborator,
                    AppCollaborator,
                    UnknownType,
                ],
                UNSET,
            )

        def get_created_at() -> Union[Unset, str]:
            created_at = d.pop("createdAt")
            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, str], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_item_id() -> Union[Unset, str]:
            item_id = d.pop("itemId")
            return item_id

        try:
            item_id = get_item_id()
        except KeyError:
            if strict:
                raise
            item_id = cast(Union[Unset, str], UNSET)

        def get_item_type() -> Union[Unset, str]:
            item_type = d.pop("itemType")
            return item_type

        try:
            item_type = get_item_type()
        except KeyError:
            if strict:
                raise
            item_type = cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, str]:
            modified_at = d.pop("modifiedAt")
            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, str], UNSET)

        collaboration = cls(
            access_policy=access_policy,
            collaborator=collaborator,
            created_at=created_at,
            id=id,
            item_id=item_id,
            item_type=item_type,
            modified_at=modified_at,
        )

        collaboration.additional_properties = d
        return collaboration

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
    def access_policy(self) -> AccessPolicy:
        if isinstance(self._access_policy, Unset):
            raise NotPresentError(self, "access_policy")
        return self._access_policy

    @access_policy.setter
    def access_policy(self, value: AccessPolicy) -> None:
        self._access_policy = value

    @access_policy.deleter
    def access_policy(self) -> None:
        self._access_policy = UNSET

    @property
    def collaborator(
        self,
    ) -> Union[
        OrgMembershipCollaborator, TeamMembershipCollaborator, UserCollaborator, AppCollaborator, UnknownType
    ]:
        if isinstance(self._collaborator, Unset):
            raise NotPresentError(self, "collaborator")
        return self._collaborator

    @collaborator.setter
    def collaborator(
        self,
        value: Union[
            OrgMembershipCollaborator,
            TeamMembershipCollaborator,
            UserCollaborator,
            AppCollaborator,
            UnknownType,
        ],
    ) -> None:
        self._collaborator = value

    @collaborator.deleter
    def collaborator(self) -> None:
        self._collaborator = UNSET

    @property
    def created_at(self) -> str:
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: str) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def id(self) -> str:
        if isinstance(self._id, Unset):
            raise NotPresentError(self, "id")
        return self._id

    @id.setter
    def id(self, value: str) -> None:
        self._id = value

    @id.deleter
    def id(self) -> None:
        self._id = UNSET

    @property
    def item_id(self) -> str:
        if isinstance(self._item_id, Unset):
            raise NotPresentError(self, "item_id")
        return self._item_id

    @item_id.setter
    def item_id(self, value: str) -> None:
        self._item_id = value

    @item_id.deleter
    def item_id(self) -> None:
        self._item_id = UNSET

    @property
    def item_type(self) -> str:
        if isinstance(self._item_type, Unset):
            raise NotPresentError(self, "item_type")
        return self._item_type

    @item_type.setter
    def item_type(self, value: str) -> None:
        self._item_type = value

    @item_type.deleter
    def item_type(self) -> None:
        self._item_type = UNSET

    @property
    def modified_at(self) -> str:
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: str) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET
