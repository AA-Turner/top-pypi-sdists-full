from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.chat_response_m import ChatResponseM


T = TypeVar("T", bound="ChatResponse")


@_attrs_define
class ChatResponse:
    """
    Attributes:
        k (Union[Unset, str]): Component key (e.g. 'markdown', 'code', 'vm_order', 'resource_list').
        c (Union[Unset, str]): Content payload.
        t (Union[Unset, str]): Tag or language for dynamic blocks.
        e (Union[Unset, str]): Error message.
        m (Union[Unset, ChatResponseM]): System metadata (thread_uuid, message UUIDs).
        w (Union[Unset, str]): PII detection warning message.
        status (Union[Unset, str]): vm_order status: 'form' | 'project_form' | 'preview' | 'success' | 'error'.
        name (Union[Unset, str]): VM name.
        flavor (Union[Unset, str]): Flavor display string (e.g. 'm1.small (2 vCPU, 4GB RAM)').
        image (Union[Unset, str]): Image name.
        content (Union[Unset, str]): Intro text or form instructions.
        project (Union[Unset, str]): Project name.
        organization (Union[Unset, str]): Organization/customer name.
        project_uuid (Union[Unset, str]): Project UUID. Present when k='vm_order' or k='resource_list'.
        order_id (Union[Unset, str]): Order UUID (present on success).
        message (Union[Unset, str]): Success message (present on success).
        error (Union[Unset, str]): Error detail (present on error).
        flavors (Union[Unset, list[Any]]): Available flavor options [{name, cores, ram}]. Present when status='form'.
        images (Union[Unset, list[Any]]): Available image options [{name, min_disk, min_ram}]. Present when
            status='form'.
        projects (Union[Unset, list[Any]]): Available project options [{name, organization, uuid}]. Present when
            status='project_form'.
        offerings (Union[Unset, list[Any]]): Available offering options [{uuid, name}]. Present when
            status='offering_form'.
        network (Union[Unset, str]): Network name (e.g. 'default'). Present when status='preview'.
        ssh_key_name (Union[Unset, str]): SSH key name. Present when status='preview'.
        system_volume_size (Union[Unset, int]): System volume size in GB. Present when status='preview'.
        customer_uuid (Union[Unset, str]): Customer/organization UUID filter hint. Present when k='resource_list'.
        category_uuid (Union[Unset, str]): Category UUID filter hint. Present when k='resource_list'.
        state (Union[Unset, list[Any]]): State display name filters (e.g. ['OK', 'Erred']). Present when
            k='resource_list'.
    """

    k: Union[Unset, str] = UNSET
    c: Union[Unset, str] = UNSET
    t: Union[Unset, str] = UNSET
    e: Union[Unset, str] = UNSET
    m: Union[Unset, "ChatResponseM"] = UNSET
    w: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    flavor: Union[Unset, str] = UNSET
    image: Union[Unset, str] = UNSET
    content: Union[Unset, str] = UNSET
    project: Union[Unset, str] = UNSET
    organization: Union[Unset, str] = UNSET
    project_uuid: Union[Unset, str] = UNSET
    order_id: Union[Unset, str] = UNSET
    message: Union[Unset, str] = UNSET
    error: Union[Unset, str] = UNSET
    flavors: Union[Unset, list[Any]] = UNSET
    images: Union[Unset, list[Any]] = UNSET
    projects: Union[Unset, list[Any]] = UNSET
    offerings: Union[Unset, list[Any]] = UNSET
    network: Union[Unset, str] = UNSET
    ssh_key_name: Union[Unset, str] = UNSET
    system_volume_size: Union[Unset, int] = UNSET
    customer_uuid: Union[Unset, str] = UNSET
    category_uuid: Union[Unset, str] = UNSET
    state: Union[Unset, list[Any]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        k = self.k

        c = self.c

        t = self.t

        e = self.e

        m: Union[Unset, dict[str, Any]] = UNSET
        if not isinstance(self.m, Unset):
            m = self.m.to_dict()

        w = self.w

        status = self.status

        name = self.name

        flavor = self.flavor

        image = self.image

        content = self.content

        project = self.project

        organization = self.organization

        project_uuid = self.project_uuid

        order_id = self.order_id

        message = self.message

        error = self.error

        flavors: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.flavors, Unset):
            flavors = self.flavors

        images: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.images, Unset):
            images = self.images

        projects: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.projects, Unset):
            projects = self.projects

        offerings: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.offerings, Unset):
            offerings = self.offerings

        network = self.network

        ssh_key_name = self.ssh_key_name

        system_volume_size = self.system_volume_size

        customer_uuid = self.customer_uuid

        category_uuid = self.category_uuid

        state: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if k is not UNSET:
            field_dict["k"] = k
        if c is not UNSET:
            field_dict["c"] = c
        if t is not UNSET:
            field_dict["t"] = t
        if e is not UNSET:
            field_dict["e"] = e
        if m is not UNSET:
            field_dict["m"] = m
        if w is not UNSET:
            field_dict["w"] = w
        if status is not UNSET:
            field_dict["status"] = status
        if name is not UNSET:
            field_dict["name"] = name
        if flavor is not UNSET:
            field_dict["flavor"] = flavor
        if image is not UNSET:
            field_dict["image"] = image
        if content is not UNSET:
            field_dict["content"] = content
        if project is not UNSET:
            field_dict["project"] = project
        if organization is not UNSET:
            field_dict["organization"] = organization
        if project_uuid is not UNSET:
            field_dict["project_uuid"] = project_uuid
        if order_id is not UNSET:
            field_dict["order_id"] = order_id
        if message is not UNSET:
            field_dict["message"] = message
        if error is not UNSET:
            field_dict["error"] = error
        if flavors is not UNSET:
            field_dict["flavors"] = flavors
        if images is not UNSET:
            field_dict["images"] = images
        if projects is not UNSET:
            field_dict["projects"] = projects
        if offerings is not UNSET:
            field_dict["offerings"] = offerings
        if network is not UNSET:
            field_dict["network"] = network
        if ssh_key_name is not UNSET:
            field_dict["ssh_key_name"] = ssh_key_name
        if system_volume_size is not UNSET:
            field_dict["system_volume_size"] = system_volume_size
        if customer_uuid is not UNSET:
            field_dict["customer_uuid"] = customer_uuid
        if category_uuid is not UNSET:
            field_dict["category_uuid"] = category_uuid
        if state is not UNSET:
            field_dict["state"] = state

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chat_response_m import ChatResponseM

        d = dict(src_dict)
        k = d.pop("k", UNSET)

        c = d.pop("c", UNSET)

        t = d.pop("t", UNSET)

        e = d.pop("e", UNSET)

        _m = d.pop("m", UNSET)
        m: Union[Unset, ChatResponseM]
        if isinstance(_m, Unset):
            m = UNSET
        else:
            m = ChatResponseM.from_dict(_m)

        w = d.pop("w", UNSET)

        status = d.pop("status", UNSET)

        name = d.pop("name", UNSET)

        flavor = d.pop("flavor", UNSET)

        image = d.pop("image", UNSET)

        content = d.pop("content", UNSET)

        project = d.pop("project", UNSET)

        organization = d.pop("organization", UNSET)

        project_uuid = d.pop("project_uuid", UNSET)

        order_id = d.pop("order_id", UNSET)

        message = d.pop("message", UNSET)

        error = d.pop("error", UNSET)

        flavors = cast(list[Any], d.pop("flavors", UNSET))

        images = cast(list[Any], d.pop("images", UNSET))

        projects = cast(list[Any], d.pop("projects", UNSET))

        offerings = cast(list[Any], d.pop("offerings", UNSET))

        network = d.pop("network", UNSET)

        ssh_key_name = d.pop("ssh_key_name", UNSET)

        system_volume_size = d.pop("system_volume_size", UNSET)

        customer_uuid = d.pop("customer_uuid", UNSET)

        category_uuid = d.pop("category_uuid", UNSET)

        state = cast(list[Any], d.pop("state", UNSET))

        chat_response = cls(
            k=k,
            c=c,
            t=t,
            e=e,
            m=m,
            w=w,
            status=status,
            name=name,
            flavor=flavor,
            image=image,
            content=content,
            project=project,
            organization=organization,
            project_uuid=project_uuid,
            order_id=order_id,
            message=message,
            error=error,
            flavors=flavors,
            images=images,
            projects=projects,
            offerings=offerings,
            network=network,
            ssh_key_name=ssh_key_name,
            system_volume_size=system_volume_size,
            customer_uuid=customer_uuid,
            category_uuid=category_uuid,
            state=state,
        )

        chat_response.additional_properties = d
        return chat_response

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
