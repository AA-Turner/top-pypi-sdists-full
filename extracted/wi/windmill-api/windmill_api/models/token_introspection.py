import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..models.token_introspection_kind import TokenIntrospectionKind
from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.token_introspection_route import TokenIntrospectionRoute
    from ..models.token_introspection_workspace import TokenIntrospectionWorkspace


T = TypeVar("T", bound="TokenIntrospection")


@_attrs_define
class TokenIntrospection:
    """
    Attributes:
        kind (TokenIntrospectionKind):
        email (str):
        username (str):
        read_only (bool):
        admin_withheld (bool): the token does not carry its owner's workspace admin rights; the rights it does hold
            in a workspace are in `workspace`
        super_admin (bool): whether the token reaches superadmin routes: its owner is a superadmin, and it is
            neither a job token nor one that withholds those rights
        label (Union[Unset, str]):
        token_prefix (Union[Unset, str]):
        created_at (Union[Unset, datetime.datetime]):
        expiration (Union[Unset, datetime.datetime]):
        workspace_id (Union[Unset, str]): the one workspace the token is bound to; absent when it is not bound
        workspace_ids (Union[Unset, List[str]]): the workspaces a signed token is bound to, when it names several
        scopes (Union[Unset, List[str]]): absent when the token is unrestricted
        allowed_ips (Union[Unset, List[str]]):
        job_id (Union[Unset, str]):
        workspace (Union[Unset, TokenIntrospectionWorkspace]):
        route (Union[Unset, TokenIntrospectionRoute]):
    """

    kind: TokenIntrospectionKind
    email: str
    username: str
    read_only: bool
    admin_withheld: bool
    super_admin: bool
    label: Union[Unset, str] = UNSET
    token_prefix: Union[Unset, str] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    expiration: Union[Unset, datetime.datetime] = UNSET
    workspace_id: Union[Unset, str] = UNSET
    workspace_ids: Union[Unset, List[str]] = UNSET
    scopes: Union[Unset, List[str]] = UNSET
    allowed_ips: Union[Unset, List[str]] = UNSET
    job_id: Union[Unset, str] = UNSET
    workspace: Union[Unset, "TokenIntrospectionWorkspace"] = UNSET
    route: Union[Unset, "TokenIntrospectionRoute"] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        kind = self.kind.value

        email = self.email
        username = self.username
        read_only = self.read_only
        admin_withheld = self.admin_withheld
        super_admin = self.super_admin
        label = self.label
        token_prefix = self.token_prefix
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        expiration: Union[Unset, str] = UNSET
        if not isinstance(self.expiration, Unset):
            expiration = self.expiration.isoformat()

        workspace_id = self.workspace_id
        workspace_ids: Union[Unset, List[str]] = UNSET
        if not isinstance(self.workspace_ids, Unset):
            workspace_ids = self.workspace_ids

        scopes: Union[Unset, List[str]] = UNSET
        if not isinstance(self.scopes, Unset):
            scopes = self.scopes

        allowed_ips: Union[Unset, List[str]] = UNSET
        if not isinstance(self.allowed_ips, Unset):
            allowed_ips = self.allowed_ips

        job_id = self.job_id
        workspace: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.workspace, Unset):
            workspace = self.workspace.to_dict()

        route: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.route, Unset):
            route = self.route.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "kind": kind,
                "email": email,
                "username": username,
                "read_only": read_only,
                "admin_withheld": admin_withheld,
                "super_admin": super_admin,
            }
        )
        if label is not UNSET:
            field_dict["label"] = label
        if token_prefix is not UNSET:
            field_dict["token_prefix"] = token_prefix
        if created_at is not UNSET:
            field_dict["created_at"] = created_at
        if expiration is not UNSET:
            field_dict["expiration"] = expiration
        if workspace_id is not UNSET:
            field_dict["workspace_id"] = workspace_id
        if workspace_ids is not UNSET:
            field_dict["workspace_ids"] = workspace_ids
        if scopes is not UNSET:
            field_dict["scopes"] = scopes
        if allowed_ips is not UNSET:
            field_dict["allowed_ips"] = allowed_ips
        if job_id is not UNSET:
            field_dict["job_id"] = job_id
        if workspace is not UNSET:
            field_dict["workspace"] = workspace
        if route is not UNSET:
            field_dict["route"] = route

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.token_introspection_route import TokenIntrospectionRoute
        from ..models.token_introspection_workspace import TokenIntrospectionWorkspace

        d = src_dict.copy()
        kind = TokenIntrospectionKind(d.pop("kind"))

        email = d.pop("email")

        username = d.pop("username")

        read_only = d.pop("read_only")

        admin_withheld = d.pop("admin_withheld")

        super_admin = d.pop("super_admin")

        label = d.pop("label", UNSET)

        token_prefix = d.pop("token_prefix", UNSET)

        _created_at = d.pop("created_at", UNSET)
        created_at: Union[Unset, datetime.datetime]
        if isinstance(_created_at, Unset):
            created_at = UNSET
        else:
            created_at = isoparse(_created_at)

        _expiration = d.pop("expiration", UNSET)
        expiration: Union[Unset, datetime.datetime]
        if isinstance(_expiration, Unset):
            expiration = UNSET
        else:
            expiration = isoparse(_expiration)

        workspace_id = d.pop("workspace_id", UNSET)

        workspace_ids = cast(List[str], d.pop("workspace_ids", UNSET))

        scopes = cast(List[str], d.pop("scopes", UNSET))

        allowed_ips = cast(List[str], d.pop("allowed_ips", UNSET))

        job_id = d.pop("job_id", UNSET)

        _workspace = d.pop("workspace", UNSET)
        workspace: Union[Unset, TokenIntrospectionWorkspace]
        if isinstance(_workspace, Unset):
            workspace = UNSET
        else:
            workspace = TokenIntrospectionWorkspace.from_dict(_workspace)

        _route = d.pop("route", UNSET)
        route: Union[Unset, TokenIntrospectionRoute]
        if isinstance(_route, Unset):
            route = UNSET
        else:
            route = TokenIntrospectionRoute.from_dict(_route)

        token_introspection = cls(
            kind=kind,
            email=email,
            username=username,
            read_only=read_only,
            admin_withheld=admin_withheld,
            super_admin=super_admin,
            label=label,
            token_prefix=token_prefix,
            created_at=created_at,
            expiration=expiration,
            workspace_id=workspace_id,
            workspace_ids=workspace_ids,
            scopes=scopes,
            allowed_ips=allowed_ips,
            job_id=job_id,
            workspace=workspace,
            route=route,
        )

        token_introspection.additional_properties = d
        return token_introspection

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
