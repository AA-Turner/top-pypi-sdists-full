from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.container_v2_resources import ContainerV2Resources
    from ..models.container_v2_spec_environment import ContainerV2SpecEnvironment


T = TypeVar("T", bound="ContainerV2Spec")


@_attrs_define
class ContainerV2Spec:
    """
    Attributes:
        image (str): Image name with an optional tag or sha256 digest. The default tag is latest. Worker resolves tags
            once at creation and keeps the same image for later starts. Example: alpine:3.22.
        resources (ContainerV2Resources):
        command (list[str] | Unset):
        args (list[str] | Unset):
        working_directory (str | Unset):
        username (str | Unset):
        uid (int | Unset):
        group_name (str | Unset):
        gid (int | Unset):
        environment (ContainerV2SpecEnvironment | Unset):
    """

    image: str
    resources: ContainerV2Resources
    command: list[str] | Unset = UNSET
    args: list[str] | Unset = UNSET
    working_directory: str | Unset = UNSET
    username: str | Unset = UNSET
    uid: int | Unset = UNSET
    group_name: str | Unset = UNSET
    gid: int | Unset = UNSET
    environment: ContainerV2SpecEnvironment | Unset = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        image = self.image

        resources = self.resources.to_dict()

        command: list[str] | Unset = UNSET
        if not isinstance(self.command, Unset):
            command = self.command

        args: list[str] | Unset = UNSET
        if not isinstance(self.args, Unset):
            args = self.args

        working_directory = self.working_directory

        username = self.username

        uid = self.uid

        group_name = self.group_name

        gid = self.gid

        environment: dict[str, Any] | Unset = UNSET
        if not isinstance(self.environment, Unset):
            environment = self.environment.to_dict()

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "image": image,
                "resources": resources,
            }
        )
        if command is not UNSET:
            field_dict["command"] = command
        if args is not UNSET:
            field_dict["args"] = args
        if working_directory is not UNSET:
            field_dict["working_directory"] = working_directory
        if username is not UNSET:
            field_dict["username"] = username
        if uid is not UNSET:
            field_dict["uid"] = uid
        if group_name is not UNSET:
            field_dict["group_name"] = group_name
        if gid is not UNSET:
            field_dict["gid"] = gid
        if environment is not UNSET:
            field_dict["environment"] = environment

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.container_v2_resources import ContainerV2Resources
        from ..models.container_v2_spec_environment import ContainerV2SpecEnvironment

        d = dict(src_dict)
        image = d.pop("image")

        resources = ContainerV2Resources.from_dict(d.pop("resources"))

        command = cast(list[str], d.pop("command", UNSET))

        args = cast(list[str], d.pop("args", UNSET))

        working_directory = d.pop("working_directory", UNSET)

        username = d.pop("username", UNSET)

        uid = d.pop("uid", UNSET)

        group_name = d.pop("group_name", UNSET)

        gid = d.pop("gid", UNSET)

        _environment = d.pop("environment", UNSET)
        environment: ContainerV2SpecEnvironment | Unset
        if isinstance(_environment, Unset):
            environment = UNSET
        else:
            environment = ContainerV2SpecEnvironment.from_dict(_environment)

        container_v2_spec = cls(
            image=image,
            resources=resources,
            command=command,
            args=args,
            working_directory=working_directory,
            username=username,
            uid=uid,
            group_name=group_name,
            gid=gid,
            environment=environment,
        )

        container_v2_spec.additional_properties = d
        return container_v2_spec

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
