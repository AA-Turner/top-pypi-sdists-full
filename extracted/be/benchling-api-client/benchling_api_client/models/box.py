import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Box")


@attr.s(auto_attribs=True, repr=False)
class Box:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _available_capacity: Union[Unset, int] = UNSET
    _barcode: Union[Unset, None, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _creator: Union[Unset, UserSummary] = UNSET
    _empty_containers: Union[Unset, int] = UNSET
    _empty_positions: Union[Unset, int] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _filled_positions: Union[Unset, int] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _name: Union[Unset, str] = UNSET
    _occupied_capacity: Union[Unset, int] = UNSET
    _parent_storage_id: Union[Unset, None, str] = UNSET
    _project_id: Union[Unset, None, str] = UNSET
    _schema: Union[Unset, None, SchemaSummary] = UNSET
    _size: Union[Unset, int] = UNSET
    _total_capacity: Union[Unset, int] = UNSET
    _web_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("available_capacity={}".format(repr(self._available_capacity)))
        fields.append("barcode={}".format(repr(self._barcode)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creator={}".format(repr(self._creator)))
        fields.append("empty_containers={}".format(repr(self._empty_containers)))
        fields.append("empty_positions={}".format(repr(self._empty_positions)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("filled_positions={}".format(repr(self._filled_positions)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("occupied_capacity={}".format(repr(self._occupied_capacity)))
        fields.append("parent_storage_id={}".format(repr(self._parent_storage_id)))
        fields.append("project_id={}".format(repr(self._project_id)))
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("size={}".format(repr(self._size)))
        fields.append("total_capacity={}".format(repr(self._total_capacity)))
        fields.append("web_url={}".format(repr(self._web_url)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Box({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        available_capacity = self._available_capacity
        barcode = self._barcode
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creator, Unset):
            creator = self._creator.to_dict()

        empty_containers = self._empty_containers
        empty_positions = self._empty_positions
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        filled_positions = self._filled_positions
        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        name = self._name
        occupied_capacity = self._occupied_capacity
        parent_storage_id = self._parent_storage_id
        project_id = self._project_id
        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._schema, Unset):
            schema = self._schema.to_dict() if self._schema else None

        size = self._size
        total_capacity = self._total_capacity
        web_url = self._web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if available_capacity is not UNSET:
            field_dict["availableCapacity"] = available_capacity
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if empty_containers is not UNSET:
            field_dict["emptyContainers"] = empty_containers
        if empty_positions is not UNSET:
            field_dict["emptyPositions"] = empty_positions
        if fields is not UNSET:
            field_dict["fields"] = fields
        if filled_positions is not UNSET:
            field_dict["filledPositions"] = filled_positions
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if occupied_capacity is not UNSET:
            field_dict["occupiedCapacity"] = occupied_capacity
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if size is not UNSET:
            field_dict["size"] = size
        if total_capacity is not UNSET:
            field_dict["totalCapacity"] = total_capacity
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any], strict: bool = False) -> T:
        d = src_dict.copy()

        def get_archive_record() -> Union[Unset, None, ArchiveRecord]:
            archive_record = None
            _archive_record = d.pop("archiveRecord")

            if _archive_record is not None and not isinstance(_archive_record, Unset):
                archive_record = ArchiveRecord.from_dict(_archive_record)

            return archive_record

        try:
            archive_record = get_archive_record()
        except KeyError:
            if strict:
                raise
            archive_record = cast(Union[Unset, None, ArchiveRecord], UNSET)

        def get_available_capacity() -> Union[Unset, int]:
            available_capacity = d.pop("availableCapacity")
            return available_capacity

        try:
            available_capacity = get_available_capacity()
        except KeyError:
            if strict:
                raise
            available_capacity = cast(Union[Unset, int], UNSET)

        def get_barcode() -> Union[Unset, None, str]:
            barcode = d.pop("barcode")
            return barcode

        try:
            barcode = get_barcode()
        except KeyError:
            if strict:
                raise
            barcode = cast(Union[Unset, None, str], UNSET)

        def get_created_at() -> Union[Unset, datetime.datetime]:
            created_at: Union[Unset, datetime.datetime] = UNSET
            _created_at = d.pop("createdAt")
            if _created_at is not None and not isinstance(_created_at, Unset):
                created_at = isoparse(cast(str, _created_at))

            return created_at

        try:
            created_at = get_created_at()
        except KeyError:
            if strict:
                raise
            created_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_creator() -> Union[Unset, UserSummary]:
            creator: Union[Unset, Union[Unset, UserSummary]] = UNSET
            _creator = d.pop("creator")

            if not isinstance(_creator, Unset):
                creator = UserSummary.from_dict(_creator)

            return creator

        try:
            creator = get_creator()
        except KeyError:
            if strict:
                raise
            creator = cast(Union[Unset, UserSummary], UNSET)

        def get_empty_containers() -> Union[Unset, int]:
            empty_containers = d.pop("emptyContainers")
            return empty_containers

        try:
            empty_containers = get_empty_containers()
        except KeyError:
            if strict:
                raise
            empty_containers = cast(Union[Unset, int], UNSET)

        def get_empty_positions() -> Union[Unset, int]:
            empty_positions = d.pop("emptyPositions")
            return empty_positions

        try:
            empty_positions = get_empty_positions()
        except KeyError:
            if strict:
                raise
            empty_positions = cast(Union[Unset, int], UNSET)

        def get_fields() -> Union[Unset, Fields]:
            fields: Union[Unset, Union[Unset, Fields]] = UNSET
            _fields = d.pop("fields")

            if not isinstance(_fields, Unset):
                fields = Fields.from_dict(_fields)

            return fields

        try:
            fields = get_fields()
        except KeyError:
            if strict:
                raise
            fields = cast(Union[Unset, Fields], UNSET)

        def get_filled_positions() -> Union[Unset, int]:
            filled_positions = d.pop("filledPositions")
            return filled_positions

        try:
            filled_positions = get_filled_positions()
        except KeyError:
            if strict:
                raise
            filled_positions = cast(Union[Unset, int], UNSET)

        def get_id() -> Union[Unset, str]:
            id = d.pop("id")
            return id

        try:
            id = get_id()
        except KeyError:
            if strict:
                raise
            id = cast(Union[Unset, str], UNSET)

        def get_modified_at() -> Union[Unset, datetime.datetime]:
            modified_at: Union[Unset, datetime.datetime] = UNSET
            _modified_at = d.pop("modifiedAt")
            if _modified_at is not None and not isinstance(_modified_at, Unset):
                modified_at = isoparse(cast(str, _modified_at))

            return modified_at

        try:
            modified_at = get_modified_at()
        except KeyError:
            if strict:
                raise
            modified_at = cast(Union[Unset, datetime.datetime], UNSET)

        def get_name() -> Union[Unset, str]:
            name = d.pop("name")
            return name

        try:
            name = get_name()
        except KeyError:
            if strict:
                raise
            name = cast(Union[Unset, str], UNSET)

        def get_occupied_capacity() -> Union[Unset, int]:
            occupied_capacity = d.pop("occupiedCapacity")
            return occupied_capacity

        try:
            occupied_capacity = get_occupied_capacity()
        except KeyError:
            if strict:
                raise
            occupied_capacity = cast(Union[Unset, int], UNSET)

        def get_parent_storage_id() -> Union[Unset, None, str]:
            parent_storage_id = d.pop("parentStorageId")
            return parent_storage_id

        try:
            parent_storage_id = get_parent_storage_id()
        except KeyError:
            if strict:
                raise
            parent_storage_id = cast(Union[Unset, None, str], UNSET)

        def get_project_id() -> Union[Unset, None, str]:
            project_id = d.pop("projectId")
            return project_id

        try:
            project_id = get_project_id()
        except KeyError:
            if strict:
                raise
            project_id = cast(Union[Unset, None, str], UNSET)

        def get_schema() -> Union[Unset, None, SchemaSummary]:
            schema = None
            _schema = d.pop("schema")

            if _schema is not None and not isinstance(_schema, Unset):
                schema = SchemaSummary.from_dict(_schema)

            return schema

        try:
            schema = get_schema()
        except KeyError:
            if strict:
                raise
            schema = cast(Union[Unset, None, SchemaSummary], UNSET)

        def get_size() -> Union[Unset, int]:
            size = d.pop("size")
            return size

        try:
            size = get_size()
        except KeyError:
            if strict:
                raise
            size = cast(Union[Unset, int], UNSET)

        def get_total_capacity() -> Union[Unset, int]:
            total_capacity = d.pop("totalCapacity")
            return total_capacity

        try:
            total_capacity = get_total_capacity()
        except KeyError:
            if strict:
                raise
            total_capacity = cast(Union[Unset, int], UNSET)

        def get_web_url() -> Union[Unset, str]:
            web_url = d.pop("webURL")
            return web_url

        try:
            web_url = get_web_url()
        except KeyError:
            if strict:
                raise
            web_url = cast(Union[Unset, str], UNSET)

        box = cls(
            archive_record=archive_record,
            available_capacity=available_capacity,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            empty_containers=empty_containers,
            empty_positions=empty_positions,
            fields=fields,
            filled_positions=filled_positions,
            id=id,
            modified_at=modified_at,
            name=name,
            occupied_capacity=occupied_capacity,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema=schema,
            size=size,
            total_capacity=total_capacity,
            web_url=web_url,
        )

        box.additional_properties = d
        return box

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
    def archive_record(self) -> Optional[ArchiveRecord]:
        if isinstance(self._archive_record, Unset):
            raise NotPresentError(self, "archive_record")
        return self._archive_record

    @archive_record.setter
    def archive_record(self, value: Optional[ArchiveRecord]) -> None:
        self._archive_record = value

    @archive_record.deleter
    def archive_record(self) -> None:
        self._archive_record = UNSET

    @property
    def available_capacity(self) -> int:
        """ The number of available positions in the box. """
        if isinstance(self._available_capacity, Unset):
            raise NotPresentError(self, "available_capacity")
        return self._available_capacity

    @available_capacity.setter
    def available_capacity(self, value: int) -> None:
        self._available_capacity = value

    @available_capacity.deleter
    def available_capacity(self) -> None:
        self._available_capacity = UNSET

    @property
    def barcode(self) -> Optional[str]:
        if isinstance(self._barcode, Unset):
            raise NotPresentError(self, "barcode")
        return self._barcode

    @barcode.setter
    def barcode(self, value: Optional[str]) -> None:
        self._barcode = value

    @barcode.deleter
    def barcode(self) -> None:
        self._barcode = UNSET

    @property
    def created_at(self) -> datetime.datetime:
        if isinstance(self._created_at, Unset):
            raise NotPresentError(self, "created_at")
        return self._created_at

    @created_at.setter
    def created_at(self, value: datetime.datetime) -> None:
        self._created_at = value

    @created_at.deleter
    def created_at(self) -> None:
        self._created_at = UNSET

    @property
    def creator(self) -> UserSummary:
        if isinstance(self._creator, Unset):
            raise NotPresentError(self, "creator")
        return self._creator

    @creator.setter
    def creator(self, value: UserSummary) -> None:
        self._creator = value

    @creator.deleter
    def creator(self) -> None:
        self._creator = UNSET

    @property
    def empty_containers(self) -> int:
        """ The number of containers in the box that have no contents. """
        if isinstance(self._empty_containers, Unset):
            raise NotPresentError(self, "empty_containers")
        return self._empty_containers

    @empty_containers.setter
    def empty_containers(self, value: int) -> None:
        self._empty_containers = value

    @empty_containers.deleter
    def empty_containers(self) -> None:
        self._empty_containers = UNSET

    @property
    def empty_positions(self) -> int:
        """ The number of empty positions for adding additional containers in the box. """
        if isinstance(self._empty_positions, Unset):
            raise NotPresentError(self, "empty_positions")
        return self._empty_positions

    @empty_positions.setter
    def empty_positions(self, value: int) -> None:
        self._empty_positions = value

    @empty_positions.deleter
    def empty_positions(self) -> None:
        self._empty_positions = UNSET

    @property
    def fields(self) -> Fields:
        if isinstance(self._fields, Unset):
            raise NotPresentError(self, "fields")
        return self._fields

    @fields.setter
    def fields(self, value: Fields) -> None:
        self._fields = value

    @fields.deleter
    def fields(self) -> None:
        self._fields = UNSET

    @property
    def filled_positions(self) -> int:
        """ The number of containers currently in the box. """
        if isinstance(self._filled_positions, Unset):
            raise NotPresentError(self, "filled_positions")
        return self._filled_positions

    @filled_positions.setter
    def filled_positions(self, value: int) -> None:
        self._filled_positions = value

    @filled_positions.deleter
    def filled_positions(self) -> None:
        self._filled_positions = UNSET

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
    def modified_at(self) -> datetime.datetime:
        if isinstance(self._modified_at, Unset):
            raise NotPresentError(self, "modified_at")
        return self._modified_at

    @modified_at.setter
    def modified_at(self, value: datetime.datetime) -> None:
        self._modified_at = value

    @modified_at.deleter
    def modified_at(self) -> None:
        self._modified_at = UNSET

    @property
    def name(self) -> str:
        if isinstance(self._name, Unset):
            raise NotPresentError(self, "name")
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @name.deleter
    def name(self) -> None:
        self._name = UNSET

    @property
    def occupied_capacity(self) -> int:
        """ The number of containers currently in the box. """
        if isinstance(self._occupied_capacity, Unset):
            raise NotPresentError(self, "occupied_capacity")
        return self._occupied_capacity

    @occupied_capacity.setter
    def occupied_capacity(self, value: int) -> None:
        self._occupied_capacity = value

    @occupied_capacity.deleter
    def occupied_capacity(self) -> None:
        self._occupied_capacity = UNSET

    @property
    def parent_storage_id(self) -> Optional[str]:
        if isinstance(self._parent_storage_id, Unset):
            raise NotPresentError(self, "parent_storage_id")
        return self._parent_storage_id

    @parent_storage_id.setter
    def parent_storage_id(self, value: Optional[str]) -> None:
        self._parent_storage_id = value

    @parent_storage_id.deleter
    def parent_storage_id(self) -> None:
        self._parent_storage_id = UNSET

    @property
    def project_id(self) -> Optional[str]:
        if isinstance(self._project_id, Unset):
            raise NotPresentError(self, "project_id")
        return self._project_id

    @project_id.setter
    def project_id(self, value: Optional[str]) -> None:
        self._project_id = value

    @project_id.deleter
    def project_id(self) -> None:
        self._project_id = UNSET

    @property
    def schema(self) -> Optional[SchemaSummary]:
        if isinstance(self._schema, Unset):
            raise NotPresentError(self, "schema")
        return self._schema

    @schema.setter
    def schema(self, value: Optional[SchemaSummary]) -> None:
        self._schema = value

    @schema.deleter
    def schema(self) -> None:
        self._schema = UNSET

    @property
    def size(self) -> int:
        """ The size of the box (i.e. how many containers it can store). """
        if isinstance(self._size, Unset):
            raise NotPresentError(self, "size")
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        self._size = value

    @size.deleter
    def size(self) -> None:
        self._size = UNSET

    @property
    def total_capacity(self) -> int:
        """ The total capacity of the box (i.e. how many containers it can store). """
        if isinstance(self._total_capacity, Unset):
            raise NotPresentError(self, "total_capacity")
        return self._total_capacity

    @total_capacity.setter
    def total_capacity(self, value: int) -> None:
        self._total_capacity = value

    @total_capacity.deleter
    def total_capacity(self) -> None:
        self._total_capacity = UNSET

    @property
    def web_url(self) -> str:
        if isinstance(self._web_url, Unset):
            raise NotPresentError(self, "web_url")
        return self._web_url

    @web_url.setter
    def web_url(self, value: str) -> None:
        self._web_url = value

    @web_url.deleter
    def web_url(self) -> None:
        self._web_url = UNSET
