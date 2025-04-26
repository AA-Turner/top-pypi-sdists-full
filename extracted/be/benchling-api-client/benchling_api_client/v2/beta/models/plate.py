import datetime
from typing import Any, cast, Dict, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError
from ..models.archive_record import ArchiveRecord
from ..models.fields import Fields
from ..models.plate_type import PlateType
from ..models.plate_wells import PlateWells
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Plate")


@attr.s(auto_attribs=True, repr=False)
class Plate:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _available_capacity: Union[Unset, None, int] = UNSET
    _barcode: Union[Unset, None, str] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _creator: Union[Unset, UserSummary] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _name: Union[Unset, str] = UNSET
    _occupied_capacity: Union[Unset, None, int] = UNSET
    _parent_storage_id: Union[Unset, None, str] = UNSET
    _project_id: Union[Unset, None, str] = UNSET
    _schema: Union[Unset, None, SchemaSummary] = UNSET
    _total_capacity: Union[Unset, None, int] = UNSET
    _type: Union[Unset, PlateType] = UNSET
    _web_url: Union[Unset, str] = UNSET
    _wells: Union[Unset, PlateWells] = UNSET

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("available_capacity={}".format(repr(self._available_capacity)))
        fields.append("barcode={}".format(repr(self._barcode)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creator={}".format(repr(self._creator)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("occupied_capacity={}".format(repr(self._occupied_capacity)))
        fields.append("parent_storage_id={}".format(repr(self._parent_storage_id)))
        fields.append("project_id={}".format(repr(self._project_id)))
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("total_capacity={}".format(repr(self._total_capacity)))
        fields.append("type={}".format(repr(self._type)))
        fields.append("web_url={}".format(repr(self._web_url)))
        fields.append("wells={}".format(repr(self._wells)))
        return "Plate({})".format(", ".join(fields))

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

        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

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

        total_capacity = self._total_capacity
        type: Union[Unset, int] = UNSET
        if not isinstance(self._type, Unset):
            type = self._type.value

        web_url = self._web_url
        wells: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._wells, Unset):
            wells = self._wells.to_dict()

        field_dict: Dict[str, Any] = {}
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
        if fields is not UNSET:
            field_dict["fields"] = fields
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
        if total_capacity is not UNSET:
            field_dict["totalCapacity"] = total_capacity
        if type is not UNSET:
            field_dict["type"] = type
        if web_url is not UNSET:
            field_dict["webURL"] = web_url
        if wells is not UNSET:
            field_dict["wells"] = wells

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

        def get_available_capacity() -> Union[Unset, None, int]:
            available_capacity = d.pop("availableCapacity")
            return available_capacity

        try:
            available_capacity = get_available_capacity()
        except KeyError:
            if strict:
                raise
            available_capacity = cast(Union[Unset, None, int], UNSET)

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

        def get_occupied_capacity() -> Union[Unset, None, int]:
            occupied_capacity = d.pop("occupiedCapacity")
            return occupied_capacity

        try:
            occupied_capacity = get_occupied_capacity()
        except KeyError:
            if strict:
                raise
            occupied_capacity = cast(Union[Unset, None, int], UNSET)

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

        def get_total_capacity() -> Union[Unset, None, int]:
            total_capacity = d.pop("totalCapacity")
            return total_capacity

        try:
            total_capacity = get_total_capacity()
        except KeyError:
            if strict:
                raise
            total_capacity = cast(Union[Unset, None, int], UNSET)

        def get_type() -> Union[Unset, PlateType]:
            type = UNSET
            _type = d.pop("type")
            if _type is not None and _type is not UNSET:
                try:
                    type = PlateType(_type)
                except ValueError:
                    type = PlateType.of_unknown(_type)

            return type

        try:
            type = get_type()
        except KeyError:
            if strict:
                raise
            type = cast(Union[Unset, PlateType], UNSET)

        def get_web_url() -> Union[Unset, str]:
            web_url = d.pop("webURL")
            return web_url

        try:
            web_url = get_web_url()
        except KeyError:
            if strict:
                raise
            web_url = cast(Union[Unset, str], UNSET)

        def get_wells() -> Union[Unset, PlateWells]:
            wells: Union[Unset, Union[Unset, PlateWells]] = UNSET
            _wells = d.pop("wells")

            if not isinstance(_wells, Unset):
                wells = PlateWells.from_dict(_wells)

            return wells

        try:
            wells = get_wells()
        except KeyError:
            if strict:
                raise
            wells = cast(Union[Unset, PlateWells], UNSET)

        plate = cls(
            archive_record=archive_record,
            available_capacity=available_capacity,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            fields=fields,
            id=id,
            modified_at=modified_at,
            name=name,
            occupied_capacity=occupied_capacity,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema=schema,
            total_capacity=total_capacity,
            type=type,
            web_url=web_url,
            wells=wells,
        )

        return plate

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
    def available_capacity(self) -> Optional[int]:
        """The number of available positions in a matrix plate. Null for well plates."""
        if isinstance(self._available_capacity, Unset):
            raise NotPresentError(self, "available_capacity")
        return self._available_capacity

    @available_capacity.setter
    def available_capacity(self, value: Optional[int]) -> None:
        self._available_capacity = value

    @available_capacity.deleter
    def available_capacity(self) -> None:
        self._available_capacity = UNSET

    @property
    def barcode(self) -> Optional[str]:
        """ Barcode of the plate """
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
        """ DateTime the container was created """
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
    def id(self) -> str:
        """ ID of the plate """
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
        """ DateTime the plate was last modified """
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
        """ Name of the plate, defaults to barcode if name is not provided. """
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
    def occupied_capacity(self) -> Optional[int]:
        """The number of containers currently in a matrix plate. Null for well plates."""
        if isinstance(self._occupied_capacity, Unset):
            raise NotPresentError(self, "occupied_capacity")
        return self._occupied_capacity

    @occupied_capacity.setter
    def occupied_capacity(self, value: Optional[int]) -> None:
        self._occupied_capacity = value

    @occupied_capacity.deleter
    def occupied_capacity(self) -> None:
        self._occupied_capacity = UNSET

    @property
    def parent_storage_id(self) -> Optional[str]:
        """ ID of containing parent inventory (e.g. loc_k2lNspzS). """
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
        """ ID of the project if set """
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
    def total_capacity(self) -> Optional[int]:
        """The total capacity of a matrix plate (i.e. how many containers it can store). Null for well plates."""
        if isinstance(self._total_capacity, Unset):
            raise NotPresentError(self, "total_capacity")
        return self._total_capacity

    @total_capacity.setter
    def total_capacity(self, value: Optional[int]) -> None:
        self._total_capacity = value

    @total_capacity.deleter
    def total_capacity(self) -> None:
        self._total_capacity = UNSET

    @property
    def type(self) -> PlateType:
        if isinstance(self._type, Unset):
            raise NotPresentError(self, "type")
        return self._type

    @type.setter
    def type(self, value: PlateType) -> None:
        self._type = value

    @type.deleter
    def type(self) -> None:
        self._type = UNSET

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

    @property
    def wells(self) -> PlateWells:
        """ Well contents of the plate, keyed by position string (eg. "A1"). """
        if isinstance(self._wells, Unset):
            raise NotPresentError(self, "wells")
        return self._wells

    @wells.setter
    def wells(self, value: PlateWells) -> None:
        self._wells = value

    @wells.deleter
    def wells(self) -> None:
        self._wells = UNSET
