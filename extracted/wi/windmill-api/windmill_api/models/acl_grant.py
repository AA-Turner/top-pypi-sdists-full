from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.acl_grant_object import AclGrantObject
    from ..models.acl_grant_sources_item import AclGrantSourcesItem


T = TypeVar("T", bound="AclGrant")


@_attrs_define
class AclGrant:
    """
    Attributes:
        grantee (str):
        privileges (List[str]):
        sources (List['AclGrantSourcesItem']): the roles the grant comes from, each once — who granted it, or for a
            default privilege the role whose future objects it covers. A revoke of some of the grant's privileges takes them
            back from every source that gave them.
        object_ (Union[Unset, AclGrantObject]):
        future (Union[Unset, str]): set for a default privilege, naming the kind of object it covers (TABLES, SEQUENCES,
            FUNCTIONS, TYPES, or SCHEMAS). On a schema, the defaults set in that schema; on the database, the ones set
            database-wide, which apply in every schema and which no schema's own defaults take back.
    """

    grantee: str
    privileges: List[str]
    sources: List["AclGrantSourcesItem"]
    object_: Union[Unset, "AclGrantObject"] = UNSET
    future: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        grantee = self.grantee
        privileges = self.privileges

        sources = []
        for sources_item_data in self.sources:
            sources_item = sources_item_data.to_dict()

            sources.append(sources_item)

        object_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.object_, Unset):
            object_ = self.object_.to_dict()

        future = self.future

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "grantee": grantee,
                "privileges": privileges,
                "sources": sources,
            }
        )
        if object_ is not UNSET:
            field_dict["object"] = object_
        if future is not UNSET:
            field_dict["future"] = future

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.acl_grant_object import AclGrantObject
        from ..models.acl_grant_sources_item import AclGrantSourcesItem

        d = src_dict.copy()
        grantee = d.pop("grantee")

        privileges = cast(List[str], d.pop("privileges"))

        sources = []
        _sources = d.pop("sources")
        for sources_item_data in _sources:
            sources_item = AclGrantSourcesItem.from_dict(sources_item_data)

            sources.append(sources_item)

        _object_ = d.pop("object", UNSET)
        object_: Union[Unset, AclGrantObject]
        if isinstance(_object_, Unset):
            object_ = UNSET
        else:
            object_ = AclGrantObject.from_dict(_object_)

        future = d.pop("future", UNSET)

        acl_grant = cls(
            grantee=grantee,
            privileges=privileges,
            sources=sources,
            object_=object_,
            future=future,
        )

        acl_grant.additional_properties = d
        return acl_grant

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
