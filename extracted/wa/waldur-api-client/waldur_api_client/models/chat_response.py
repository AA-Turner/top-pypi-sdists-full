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
        k (Union[Unset, str]): Component key (e.g. 'markdown', 'code', 'table', 'vm_order').
        c (Union[Unset, str]): Content payload.
        t (Union[Unset, str]): Tag or language for dynamic blocks.
        e (Union[Unset, str]): Error message.
        h (Union[Unset, list[Any]]): Table headers.
        r (Union[Unset, list[Any]]): Table rows.
        n (Union[Unset, int]): Total row count.
        m (Union[Unset, ChatResponseM]): System metadata (thread_uuid, message UUIDs).
        w (Union[Unset, str]): PII detection warning message.
        status (Union[Unset, str]): vm_order status: 'form' | 'project_form' | 'preview' | 'success' | 'error'.
        name (Union[Unset, str]): VM name.
        flavor (Union[Unset, str]): Flavor display string (e.g. 'm1.small (2 vCPU, 4GB RAM)').
        image (Union[Unset, str]): Image name.
        content (Union[Unset, str]): Intro text or form instructions.
        project (Union[Unset, str]): Project name.
        organization (Union[Unset, str]): Organization/customer name.
        project_uuid (Union[Unset, str]): Project UUID.
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
    """

    k: Union[Unset, str] = UNSET
    c: Union[Unset, str] = UNSET
    t: Union[Unset, str] = UNSET
    e: Union[Unset, str] = UNSET
    h: Union[Unset, list[Any]] = UNSET
    r: Union[Unset, list[Any]] = UNSET
    n: Union[Unset, int] = UNSET
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
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        k = self.k

        c = self.c

        t = self.t

        e = self.e

        h: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.h, Unset):
            h = self.h

        r: Union[Unset, list[Any]] = UNSET
        if not isinstance(self.r, Unset):
            r = self.r

        n = self.n

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
        if h is not UNSET:
            field_dict["h"] = h
        if r is not UNSET:
            field_dict["r"] = r
        if n is not UNSET:
            field_dict["n"] = n
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

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.chat_response_m import ChatResponseM

        d = dict(src_dict)
        k = d.pop("k", UNSET)

        c = d.pop("c", UNSET)

        t = d.pop("t", UNSET)

        e = d.pop("e", UNSET)

        h = cast(list[Any], d.pop("h", UNSET))

        r = cast(list[Any], d.pop("r", UNSET))

        n = d.pop("n", UNSET)

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

        chat_response = cls(
            k=k,
            c=c,
            t=t,
            e=e,
            h=h,
            r=r,
            n=n,
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
