import datetime
from typing import Any, cast, Dict, List, Optional, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..extensions import NotPresentError, UnknownType
from ..models.archive_record import ArchiveRecord
from ..models.checkout_record import CheckoutRecord
from ..models.container_content import ContainerContent
from ..models.container_quantity import ContainerQuantity
from ..models.deprecated_container_volume_for_response import DeprecatedContainerVolumeForResponse
from ..models.experimental_well_role import ExperimentalWellRole
from ..models.fields import Fields
from ..models.sample_restriction_status import SampleRestrictionStatus
from ..models.schema_summary import SchemaSummary
from ..models.team_summary import TeamSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset

T = TypeVar("T", bound="Container")


@attr.s(auto_attribs=True, repr=False)
class Container:
    """  """

    _archive_record: Union[Unset, None, ArchiveRecord] = UNSET
    _barcode: Union[Unset, None, str] = UNSET
    _checkout_record: Union[Unset, CheckoutRecord] = UNSET
    _contents: Union[Unset, List[ContainerContent]] = UNSET
    _created_at: Union[Unset, datetime.datetime] = UNSET
    _creator: Union[Unset, UserSummary] = UNSET
    _expiration_date: Union[Unset, None, str] = UNSET
    _expiration_date_override: Union[Unset, None, str] = UNSET
    _fields: Union[Unset, Fields] = UNSET
    _freeze_thaw_count: Union[Unset, None, int] = UNSET
    _id: Union[Unset, str] = UNSET
    _modified_at: Union[Unset, datetime.datetime] = UNSET
    _name: Union[Unset, str] = UNSET
    _parent_storage_id: Union[Unset, None, str] = UNSET
    _parent_storage_schema: Union[Unset, None, SchemaSummary] = UNSET
    _project_id: Union[Unset, None, str] = UNSET
    _quantity: Union[Unset, ContainerQuantity] = UNSET
    _restricted_sample_parties: Union[Unset, List[Union[UserSummary, TeamSummary, UnknownType]]] = UNSET
    _restriction_status: Union[Unset, SampleRestrictionStatus] = UNSET
    _role: Union[Unset, None, ExperimentalWellRole] = UNSET
    _sample_owners: Union[Unset, List[Union[UserSummary, TeamSummary, UnknownType]]] = UNSET
    _schema: Union[Unset, None, SchemaSummary] = UNSET
    _volume: Union[Unset, DeprecatedContainerVolumeForResponse] = UNSET
    _web_url: Union[Unset, str] = UNSET
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    def __repr__(self):
        fields = []
        fields.append("archive_record={}".format(repr(self._archive_record)))
        fields.append("barcode={}".format(repr(self._barcode)))
        fields.append("checkout_record={}".format(repr(self._checkout_record)))
        fields.append("contents={}".format(repr(self._contents)))
        fields.append("created_at={}".format(repr(self._created_at)))
        fields.append("creator={}".format(repr(self._creator)))
        fields.append("expiration_date={}".format(repr(self._expiration_date)))
        fields.append("expiration_date_override={}".format(repr(self._expiration_date_override)))
        fields.append("fields={}".format(repr(self._fields)))
        fields.append("freeze_thaw_count={}".format(repr(self._freeze_thaw_count)))
        fields.append("id={}".format(repr(self._id)))
        fields.append("modified_at={}".format(repr(self._modified_at)))
        fields.append("name={}".format(repr(self._name)))
        fields.append("parent_storage_id={}".format(repr(self._parent_storage_id)))
        fields.append("parent_storage_schema={}".format(repr(self._parent_storage_schema)))
        fields.append("project_id={}".format(repr(self._project_id)))
        fields.append("quantity={}".format(repr(self._quantity)))
        fields.append("restricted_sample_parties={}".format(repr(self._restricted_sample_parties)))
        fields.append("restriction_status={}".format(repr(self._restriction_status)))
        fields.append("role={}".format(repr(self._role)))
        fields.append("sample_owners={}".format(repr(self._sample_owners)))
        fields.append("schema={}".format(repr(self._schema)))
        fields.append("volume={}".format(repr(self._volume)))
        fields.append("web_url={}".format(repr(self._web_url)))
        fields.append("additional_properties={}".format(repr(self.additional_properties)))
        return "Container({})".format(", ".join(fields))

    def to_dict(self) -> Dict[str, Any]:
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._archive_record, Unset):
            archive_record = self._archive_record.to_dict() if self._archive_record else None

        barcode = self._barcode
        checkout_record: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._checkout_record, Unset):
            checkout_record = self._checkout_record.to_dict()

        contents: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._contents, Unset):
            contents = []
            for contents_item_data in self._contents:
                contents_item = contents_item_data.to_dict()

                contents.append(contents_item)

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self._created_at, Unset):
            created_at = self._created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._creator, Unset):
            creator = self._creator.to_dict()

        expiration_date = self._expiration_date
        expiration_date_override = self._expiration_date_override
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._fields, Unset):
            fields = self._fields.to_dict()

        freeze_thaw_count = self._freeze_thaw_count
        id = self._id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self._modified_at, Unset):
            modified_at = self._modified_at.isoformat()

        name = self._name
        parent_storage_id = self._parent_storage_id
        parent_storage_schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._parent_storage_schema, Unset):
            parent_storage_schema = (
                self._parent_storage_schema.to_dict() if self._parent_storage_schema else None
            )

        project_id = self._project_id
        quantity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._quantity, Unset):
            quantity = self._quantity.to_dict()

        restricted_sample_parties: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._restricted_sample_parties, Unset):
            restricted_sample_parties = []
            for restricted_sample_parties_item_data in self._restricted_sample_parties:
                if isinstance(restricted_sample_parties_item_data, UnknownType):
                    restricted_sample_parties_item = restricted_sample_parties_item_data.value
                elif isinstance(restricted_sample_parties_item_data, UserSummary):
                    restricted_sample_parties_item = restricted_sample_parties_item_data.to_dict()

                else:
                    restricted_sample_parties_item = restricted_sample_parties_item_data.to_dict()

                restricted_sample_parties.append(restricted_sample_parties_item)

        restriction_status: Union[Unset, int] = UNSET
        if not isinstance(self._restriction_status, Unset):
            restriction_status = self._restriction_status.value

        role: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._role, Unset):
            role = self._role.to_dict() if self._role else None

        sample_owners: Union[Unset, List[Any]] = UNSET
        if not isinstance(self._sample_owners, Unset):
            sample_owners = []
            for sample_owners_item_data in self._sample_owners:
                if isinstance(sample_owners_item_data, UnknownType):
                    sample_owners_item = sample_owners_item_data.value
                elif isinstance(sample_owners_item_data, UserSummary):
                    sample_owners_item = sample_owners_item_data.to_dict()

                else:
                    sample_owners_item = sample_owners_item_data.to_dict()

                sample_owners.append(sample_owners_item)

        schema: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self._schema, Unset):
            schema = self._schema.to_dict() if self._schema else None

        volume: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self._volume, Unset):
            volume = self._volume.to_dict()

        web_url = self._web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        # Allow the model to serialize even if it was created outside of the constructor, circumventing validation
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if checkout_record is not UNSET:
            field_dict["checkoutRecord"] = checkout_record
        if contents is not UNSET:
            field_dict["contents"] = contents
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if expiration_date is not UNSET:
            field_dict["expirationDate"] = expiration_date
        if expiration_date_override is not UNSET:
            field_dict["expirationDateOverride"] = expiration_date_override
        if fields is not UNSET:
            field_dict["fields"] = fields
        if freeze_thaw_count is not UNSET:
            field_dict["freezeThawCount"] = freeze_thaw_count
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if parent_storage_schema is not UNSET:
            field_dict["parentStorageSchema"] = parent_storage_schema
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if quantity is not UNSET:
            field_dict["quantity"] = quantity
        if restricted_sample_parties is not UNSET:
            field_dict["restrictedSampleParties"] = restricted_sample_parties
        if restriction_status is not UNSET:
            field_dict["restrictionStatus"] = restriction_status
        if role is not UNSET:
            field_dict["role"] = role
        if sample_owners is not UNSET:
            field_dict["sampleOwners"] = sample_owners
        if schema is not UNSET:
            field_dict["schema"] = schema
        if volume is not UNSET:
            field_dict["volume"] = volume
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

        def get_barcode() -> Union[Unset, None, str]:
            barcode = d.pop("barcode")
            return barcode

        try:
            barcode = get_barcode()
        except KeyError:
            if strict:
                raise
            barcode = cast(Union[Unset, None, str], UNSET)

        def get_checkout_record() -> Union[Unset, CheckoutRecord]:
            checkout_record: Union[Unset, Union[Unset, CheckoutRecord]] = UNSET
            _checkout_record = d.pop("checkoutRecord")

            if not isinstance(_checkout_record, Unset):
                checkout_record = CheckoutRecord.from_dict(_checkout_record)

            return checkout_record

        try:
            checkout_record = get_checkout_record()
        except KeyError:
            if strict:
                raise
            checkout_record = cast(Union[Unset, CheckoutRecord], UNSET)

        def get_contents() -> Union[Unset, List[ContainerContent]]:
            contents = []
            _contents = d.pop("contents")
            for contents_item_data in _contents or []:
                contents_item = ContainerContent.from_dict(contents_item_data, strict=False)

                contents.append(contents_item)

            return contents

        try:
            contents = get_contents()
        except KeyError:
            if strict:
                raise
            contents = cast(Union[Unset, List[ContainerContent]], UNSET)

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

        def get_expiration_date() -> Union[Unset, None, str]:
            expiration_date = d.pop("expirationDate")
            return expiration_date

        try:
            expiration_date = get_expiration_date()
        except KeyError:
            if strict:
                raise
            expiration_date = cast(Union[Unset, None, str], UNSET)

        def get_expiration_date_override() -> Union[Unset, None, str]:
            expiration_date_override = d.pop("expirationDateOverride")
            return expiration_date_override

        try:
            expiration_date_override = get_expiration_date_override()
        except KeyError:
            if strict:
                raise
            expiration_date_override = cast(Union[Unset, None, str], UNSET)

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

        def get_freeze_thaw_count() -> Union[Unset, None, int]:
            freeze_thaw_count = d.pop("freezeThawCount")
            return freeze_thaw_count

        try:
            freeze_thaw_count = get_freeze_thaw_count()
        except KeyError:
            if strict:
                raise
            freeze_thaw_count = cast(Union[Unset, None, int], UNSET)

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

        def get_parent_storage_id() -> Union[Unset, None, str]:
            parent_storage_id = d.pop("parentStorageId")
            return parent_storage_id

        try:
            parent_storage_id = get_parent_storage_id()
        except KeyError:
            if strict:
                raise
            parent_storage_id = cast(Union[Unset, None, str], UNSET)

        def get_parent_storage_schema() -> Union[Unset, None, SchemaSummary]:
            parent_storage_schema = None
            _parent_storage_schema = d.pop("parentStorageSchema")

            if _parent_storage_schema is not None and not isinstance(_parent_storage_schema, Unset):
                parent_storage_schema = SchemaSummary.from_dict(_parent_storage_schema)

            return parent_storage_schema

        try:
            parent_storage_schema = get_parent_storage_schema()
        except KeyError:
            if strict:
                raise
            parent_storage_schema = cast(Union[Unset, None, SchemaSummary], UNSET)

        def get_project_id() -> Union[Unset, None, str]:
            project_id = d.pop("projectId")
            return project_id

        try:
            project_id = get_project_id()
        except KeyError:
            if strict:
                raise
            project_id = cast(Union[Unset, None, str], UNSET)

        def get_quantity() -> Union[Unset, ContainerQuantity]:
            quantity: Union[Unset, Union[Unset, ContainerQuantity]] = UNSET
            _quantity = d.pop("quantity")

            if not isinstance(_quantity, Unset):
                quantity = ContainerQuantity.from_dict(_quantity)

            return quantity

        try:
            quantity = get_quantity()
        except KeyError:
            if strict:
                raise
            quantity = cast(Union[Unset, ContainerQuantity], UNSET)

        def get_restricted_sample_parties() -> Union[
            Unset, List[Union[UserSummary, TeamSummary, UnknownType]]
        ]:
            restricted_sample_parties = []
            _restricted_sample_parties = d.pop("restrictedSampleParties")
            for restricted_sample_parties_item_data in _restricted_sample_parties or []:

                def _parse_restricted_sample_parties_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[UserSummary, TeamSummary, UnknownType]:
                    restricted_sample_parties_item: Union[UserSummary, TeamSummary, UnknownType]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        restricted_sample_parties_item = UserSummary.from_dict(data, strict=True)

                        return restricted_sample_parties_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        restricted_sample_parties_item = TeamSummary.from_dict(data, strict=True)

                        return restricted_sample_parties_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                restricted_sample_parties_item = _parse_restricted_sample_parties_item(
                    restricted_sample_parties_item_data
                )

                restricted_sample_parties.append(restricted_sample_parties_item)

            return restricted_sample_parties

        try:
            restricted_sample_parties = get_restricted_sample_parties()
        except KeyError:
            if strict:
                raise
            restricted_sample_parties = cast(
                Union[Unset, List[Union[UserSummary, TeamSummary, UnknownType]]], UNSET
            )

        def get_restriction_status() -> Union[Unset, SampleRestrictionStatus]:
            restriction_status = UNSET
            _restriction_status = d.pop("restrictionStatus")
            if _restriction_status is not None and _restriction_status is not UNSET:
                try:
                    restriction_status = SampleRestrictionStatus(_restriction_status)
                except ValueError:
                    restriction_status = SampleRestrictionStatus.of_unknown(_restriction_status)

            return restriction_status

        try:
            restriction_status = get_restriction_status()
        except KeyError:
            if strict:
                raise
            restriction_status = cast(Union[Unset, SampleRestrictionStatus], UNSET)

        def get_role() -> Union[Unset, None, ExperimentalWellRole]:
            role = None
            _role = d.pop("role")

            if _role is not None and not isinstance(_role, Unset):
                role = ExperimentalWellRole.from_dict(_role)

            return role

        try:
            role = get_role()
        except KeyError:
            if strict:
                raise
            role = cast(Union[Unset, None, ExperimentalWellRole], UNSET)

        def get_sample_owners() -> Union[Unset, List[Union[UserSummary, TeamSummary, UnknownType]]]:
            sample_owners = []
            _sample_owners = d.pop("sampleOwners")
            for sample_owners_item_data in _sample_owners or []:

                def _parse_sample_owners_item(
                    data: Union[Dict[str, Any]]
                ) -> Union[UserSummary, TeamSummary, UnknownType]:
                    sample_owners_item: Union[UserSummary, TeamSummary, UnknownType]
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        sample_owners_item = UserSummary.from_dict(data, strict=True)

                        return sample_owners_item
                    except:  # noqa: E722
                        pass
                    try:
                        if not isinstance(data, dict):
                            raise TypeError()
                        sample_owners_item = TeamSummary.from_dict(data, strict=True)

                        return sample_owners_item
                    except:  # noqa: E722
                        pass
                    return UnknownType(data)

                sample_owners_item = _parse_sample_owners_item(sample_owners_item_data)

                sample_owners.append(sample_owners_item)

            return sample_owners

        try:
            sample_owners = get_sample_owners()
        except KeyError:
            if strict:
                raise
            sample_owners = cast(Union[Unset, List[Union[UserSummary, TeamSummary, UnknownType]]], UNSET)

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

        def get_volume() -> Union[Unset, DeprecatedContainerVolumeForResponse]:
            volume: Union[Unset, Union[Unset, DeprecatedContainerVolumeForResponse]] = UNSET
            _volume = d.pop("volume")

            if not isinstance(_volume, Unset):
                volume = DeprecatedContainerVolumeForResponse.from_dict(_volume)

            return volume

        try:
            volume = get_volume()
        except KeyError:
            if strict:
                raise
            volume = cast(Union[Unset, DeprecatedContainerVolumeForResponse], UNSET)

        def get_web_url() -> Union[Unset, str]:
            web_url = d.pop("webURL")
            return web_url

        try:
            web_url = get_web_url()
        except KeyError:
            if strict:
                raise
            web_url = cast(Union[Unset, str], UNSET)

        container = cls(
            archive_record=archive_record,
            barcode=barcode,
            checkout_record=checkout_record,
            contents=contents,
            created_at=created_at,
            creator=creator,
            expiration_date=expiration_date,
            expiration_date_override=expiration_date_override,
            fields=fields,
            freeze_thaw_count=freeze_thaw_count,
            id=id,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            parent_storage_schema=parent_storage_schema,
            project_id=project_id,
            quantity=quantity,
            restricted_sample_parties=restricted_sample_parties,
            restriction_status=restriction_status,
            role=role,
            sample_owners=sample_owners,
            schema=schema,
            volume=volume,
            web_url=web_url,
        )

        container.additional_properties = d
        return container

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
    def checkout_record(self) -> CheckoutRecord:
        """
        *assignee field* is set if status is "RESERVED" or "CHECKED_OUT", or null if status is "AVAILABLE".

        *comment field* is set when container was last reserved, checked out, or checked into.

        *modifiedAt field* is the date and time when container was last checked out, checked in, or reserved
        """
        if isinstance(self._checkout_record, Unset):
            raise NotPresentError(self, "checkout_record")
        return self._checkout_record

    @checkout_record.setter
    def checkout_record(self, value: CheckoutRecord) -> None:
        self._checkout_record = value

    @checkout_record.deleter
    def checkout_record(self) -> None:
        self._checkout_record = UNSET

    @property
    def contents(self) -> List[ContainerContent]:
        if isinstance(self._contents, Unset):
            raise NotPresentError(self, "contents")
        return self._contents

    @contents.setter
    def contents(self, value: List[ContainerContent]) -> None:
        self._contents = value

    @contents.deleter
    def contents(self) -> None:
        self._contents = UNSET

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
    def expiration_date(self) -> Optional[str]:
        if isinstance(self._expiration_date, Unset):
            raise NotPresentError(self, "expiration_date")
        return self._expiration_date

    @expiration_date.setter
    def expiration_date(self, value: Optional[str]) -> None:
        self._expiration_date = value

    @expiration_date.deleter
    def expiration_date(self) -> None:
        self._expiration_date = UNSET

    @property
    def expiration_date_override(self) -> Optional[str]:
        if isinstance(self._expiration_date_override, Unset):
            raise NotPresentError(self, "expiration_date_override")
        return self._expiration_date_override

    @expiration_date_override.setter
    def expiration_date_override(self, value: Optional[str]) -> None:
        self._expiration_date_override = value

    @expiration_date_override.deleter
    def expiration_date_override(self) -> None:
        self._expiration_date_override = UNSET

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
    def freeze_thaw_count(self) -> Optional[int]:
        if isinstance(self._freeze_thaw_count, Unset):
            raise NotPresentError(self, "freeze_thaw_count")
        return self._freeze_thaw_count

    @freeze_thaw_count.setter
    def freeze_thaw_count(self, value: Optional[int]) -> None:
        self._freeze_thaw_count = value

    @freeze_thaw_count.deleter
    def freeze_thaw_count(self) -> None:
        self._freeze_thaw_count = UNSET

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
    def parent_storage_schema(self) -> Optional[SchemaSummary]:
        if isinstance(self._parent_storage_schema, Unset):
            raise NotPresentError(self, "parent_storage_schema")
        return self._parent_storage_schema

    @parent_storage_schema.setter
    def parent_storage_schema(self, value: Optional[SchemaSummary]) -> None:
        self._parent_storage_schema = value

    @parent_storage_schema.deleter
    def parent_storage_schema(self) -> None:
        self._parent_storage_schema = UNSET

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
    def quantity(self) -> ContainerQuantity:
        """ Quantity of a container, well, or transfer. Supports mass, volume, and other quantities. """
        if isinstance(self._quantity, Unset):
            raise NotPresentError(self, "quantity")
        return self._quantity

    @quantity.setter
    def quantity(self, value: ContainerQuantity) -> None:
        self._quantity = value

    @quantity.deleter
    def quantity(self) -> None:
        self._quantity = UNSET

    @property
    def restricted_sample_parties(self) -> List[Union[UserSummary, TeamSummary, UnknownType]]:
        if isinstance(self._restricted_sample_parties, Unset):
            raise NotPresentError(self, "restricted_sample_parties")
        return self._restricted_sample_parties

    @restricted_sample_parties.setter
    def restricted_sample_parties(self, value: List[Union[UserSummary, TeamSummary, UnknownType]]) -> None:
        self._restricted_sample_parties = value

    @restricted_sample_parties.deleter
    def restricted_sample_parties(self) -> None:
        self._restricted_sample_parties = UNSET

    @property
    def restriction_status(self) -> SampleRestrictionStatus:
        if isinstance(self._restriction_status, Unset):
            raise NotPresentError(self, "restriction_status")
        return self._restriction_status

    @restriction_status.setter
    def restriction_status(self, value: SampleRestrictionStatus) -> None:
        self._restriction_status = value

    @restriction_status.deleter
    def restriction_status(self) -> None:
        self._restriction_status = UNSET

    @property
    def role(self) -> Optional[ExperimentalWellRole]:
        if isinstance(self._role, Unset):
            raise NotPresentError(self, "role")
        return self._role

    @role.setter
    def role(self, value: Optional[ExperimentalWellRole]) -> None:
        self._role = value

    @role.deleter
    def role(self) -> None:
        self._role = UNSET

    @property
    def sample_owners(self) -> List[Union[UserSummary, TeamSummary, UnknownType]]:
        if isinstance(self._sample_owners, Unset):
            raise NotPresentError(self, "sample_owners")
        return self._sample_owners

    @sample_owners.setter
    def sample_owners(self, value: List[Union[UserSummary, TeamSummary, UnknownType]]) -> None:
        self._sample_owners = value

    @sample_owners.deleter
    def sample_owners(self) -> None:
        self._sample_owners = UNSET

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
    def volume(self) -> DeprecatedContainerVolumeForResponse:
        if isinstance(self._volume, Unset):
            raise NotPresentError(self, "volume")
        return self._volume

    @volume.setter
    def volume(self, value: DeprecatedContainerVolumeForResponse) -> None:
        self._volume = value

    @volume.deleter
    def volume(self) -> None:
        self._volume = UNSET

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
