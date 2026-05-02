from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_custom_instance_dbs_response_200_additional_property_logs_created_database import (
    ListCustomInstanceDbsResponse200AdditionalPropertyLogsCreatedDatabase,
)
from ..models.list_custom_instance_dbs_response_200_additional_property_logs_database_credentials import (
    ListCustomInstanceDbsResponse200AdditionalPropertyLogsDatabaseCredentials,
)
from ..models.list_custom_instance_dbs_response_200_additional_property_logs_db_connect import (
    ListCustomInstanceDbsResponse200AdditionalPropertyLogsDbConnect,
)
from ..models.list_custom_instance_dbs_response_200_additional_property_logs_grant_permissions import (
    ListCustomInstanceDbsResponse200AdditionalPropertyLogsGrantPermissions,
)
from ..models.list_custom_instance_dbs_response_200_additional_property_logs_super_admin import (
    ListCustomInstanceDbsResponse200AdditionalPropertyLogsSuperAdmin,
)
from ..models.list_custom_instance_dbs_response_200_additional_property_logs_valid_dbname import (
    ListCustomInstanceDbsResponse200AdditionalPropertyLogsValidDbname,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListCustomInstanceDbsResponse200AdditionalPropertyLogs")


@_attrs_define
class ListCustomInstanceDbsResponse200AdditionalPropertyLogs:
    """
    Attributes:
        super_admin (Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsSuperAdmin]):
        database_credentials (Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsDatabaseCredentials]):
        valid_dbname (Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsValidDbname]):
        created_database (Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsCreatedDatabase]):
        db_connect (Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsDbConnect]):
        grant_permissions (Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsGrantPermissions]):
    """

    super_admin: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsSuperAdmin] = UNSET
    database_credentials: Union[
        Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsDatabaseCredentials
    ] = UNSET
    valid_dbname: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsValidDbname] = UNSET
    created_database: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsCreatedDatabase] = UNSET
    db_connect: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsDbConnect] = UNSET
    grant_permissions: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsGrantPermissions] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        super_admin: Union[Unset, str] = UNSET
        if not isinstance(self.super_admin, Unset):
            super_admin = self.super_admin.value

        database_credentials: Union[Unset, str] = UNSET
        if not isinstance(self.database_credentials, Unset):
            database_credentials = self.database_credentials.value

        valid_dbname: Union[Unset, str] = UNSET
        if not isinstance(self.valid_dbname, Unset):
            valid_dbname = self.valid_dbname.value

        created_database: Union[Unset, str] = UNSET
        if not isinstance(self.created_database, Unset):
            created_database = self.created_database.value

        db_connect: Union[Unset, str] = UNSET
        if not isinstance(self.db_connect, Unset):
            db_connect = self.db_connect.value

        grant_permissions: Union[Unset, str] = UNSET
        if not isinstance(self.grant_permissions, Unset):
            grant_permissions = self.grant_permissions.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if super_admin is not UNSET:
            field_dict["super_admin"] = super_admin
        if database_credentials is not UNSET:
            field_dict["database_credentials"] = database_credentials
        if valid_dbname is not UNSET:
            field_dict["valid_dbname"] = valid_dbname
        if created_database is not UNSET:
            field_dict["created_database"] = created_database
        if db_connect is not UNSET:
            field_dict["db_connect"] = db_connect
        if grant_permissions is not UNSET:
            field_dict["grant_permissions"] = grant_permissions

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _super_admin = d.pop("super_admin", UNSET)
        super_admin: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsSuperAdmin]
        if isinstance(_super_admin, Unset):
            super_admin = UNSET
        else:
            super_admin = ListCustomInstanceDbsResponse200AdditionalPropertyLogsSuperAdmin(_super_admin)

        _database_credentials = d.pop("database_credentials", UNSET)
        database_credentials: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsDatabaseCredentials]
        if isinstance(_database_credentials, Unset):
            database_credentials = UNSET
        else:
            database_credentials = ListCustomInstanceDbsResponse200AdditionalPropertyLogsDatabaseCredentials(
                _database_credentials
            )

        _valid_dbname = d.pop("valid_dbname", UNSET)
        valid_dbname: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsValidDbname]
        if isinstance(_valid_dbname, Unset):
            valid_dbname = UNSET
        else:
            valid_dbname = ListCustomInstanceDbsResponse200AdditionalPropertyLogsValidDbname(_valid_dbname)

        _created_database = d.pop("created_database", UNSET)
        created_database: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsCreatedDatabase]
        if isinstance(_created_database, Unset):
            created_database = UNSET
        else:
            created_database = ListCustomInstanceDbsResponse200AdditionalPropertyLogsCreatedDatabase(_created_database)

        _db_connect = d.pop("db_connect", UNSET)
        db_connect: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsDbConnect]
        if isinstance(_db_connect, Unset):
            db_connect = UNSET
        else:
            db_connect = ListCustomInstanceDbsResponse200AdditionalPropertyLogsDbConnect(_db_connect)

        _grant_permissions = d.pop("grant_permissions", UNSET)
        grant_permissions: Union[Unset, ListCustomInstanceDbsResponse200AdditionalPropertyLogsGrantPermissions]
        if isinstance(_grant_permissions, Unset):
            grant_permissions = UNSET
        else:
            grant_permissions = ListCustomInstanceDbsResponse200AdditionalPropertyLogsGrantPermissions(
                _grant_permissions
            )

        list_custom_instance_dbs_response_200_additional_property_logs = cls(
            super_admin=super_admin,
            database_credentials=database_credentials,
            valid_dbname=valid_dbname,
            created_database=created_database,
            db_connect=db_connect,
            grant_permissions=grant_permissions,
        )

        list_custom_instance_dbs_response_200_additional_property_logs.additional_properties = d
        return list_custom_instance_dbs_response_200_additional_property_logs

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
