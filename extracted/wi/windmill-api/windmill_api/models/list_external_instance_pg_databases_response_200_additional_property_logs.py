from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_created_database import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsCreatedDatabase,
)
from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_database_credentials import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDatabaseCredentials,
)
from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_db_connect import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDbConnect,
)
from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_grant_permissions import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsGrantPermissions,
)
from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_replication_user import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsReplicationUser,
)
from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_super_admin import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsSuperAdmin,
)
from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_user_connect import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsUserConnect,
)
from ..models.list_external_instance_pg_databases_response_200_additional_property_logs_valid_dbname import (
    ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsValidDbname,
)
from ..types import UNSET, Unset

T = TypeVar("T", bound="ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogs")


@_attrs_define
class ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogs:
    """
    Attributes:
        super_admin (Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsSuperAdmin]):
        database_credentials (Union[Unset,
            ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDatabaseCredentials]):
        valid_dbname (Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsValidDbname]):
        created_database (Union[Unset,
            ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsCreatedDatabase]):
        db_connect (Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDbConnect]):
        grant_permissions (Union[Unset,
            ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsGrantPermissions]):
        replication_user (Union[Unset,
            ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsReplicationUser]):
        replication_user_error (Union[Unset, str]):
        user_connect (Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsUserConnect]):
    """

    super_admin: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsSuperAdmin] = UNSET
    database_credentials: Union[
        Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDatabaseCredentials
    ] = UNSET
    valid_dbname: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsValidDbname] = UNSET
    created_database: Union[
        Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsCreatedDatabase
    ] = UNSET
    db_connect: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDbConnect] = UNSET
    grant_permissions: Union[
        Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsGrantPermissions
    ] = UNSET
    replication_user: Union[
        Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsReplicationUser
    ] = UNSET
    replication_user_error: Union[Unset, str] = UNSET
    user_connect: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsUserConnect] = UNSET
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

        replication_user: Union[Unset, str] = UNSET
        if not isinstance(self.replication_user, Unset):
            replication_user = self.replication_user.value

        replication_user_error = self.replication_user_error
        user_connect: Union[Unset, str] = UNSET
        if not isinstance(self.user_connect, Unset):
            user_connect = self.user_connect.value

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
        if replication_user is not UNSET:
            field_dict["replication_user"] = replication_user
        if replication_user_error is not UNSET:
            field_dict["replication_user_error"] = replication_user_error
        if user_connect is not UNSET:
            field_dict["user_connect"] = user_connect

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _super_admin = d.pop("super_admin", UNSET)
        super_admin: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsSuperAdmin]
        if isinstance(_super_admin, Unset):
            super_admin = UNSET
        else:
            super_admin = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsSuperAdmin(_super_admin)

        _database_credentials = d.pop("database_credentials", UNSET)
        database_credentials: Union[
            Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDatabaseCredentials
        ]
        if isinstance(_database_credentials, Unset):
            database_credentials = UNSET
        else:
            database_credentials = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDatabaseCredentials(
                _database_credentials
            )

        _valid_dbname = d.pop("valid_dbname", UNSET)
        valid_dbname: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsValidDbname]
        if isinstance(_valid_dbname, Unset):
            valid_dbname = UNSET
        else:
            valid_dbname = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsValidDbname(_valid_dbname)

        _created_database = d.pop("created_database", UNSET)
        created_database: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsCreatedDatabase]
        if isinstance(_created_database, Unset):
            created_database = UNSET
        else:
            created_database = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsCreatedDatabase(
                _created_database
            )

        _db_connect = d.pop("db_connect", UNSET)
        db_connect: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDbConnect]
        if isinstance(_db_connect, Unset):
            db_connect = UNSET
        else:
            db_connect = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsDbConnect(_db_connect)

        _grant_permissions = d.pop("grant_permissions", UNSET)
        grant_permissions: Union[
            Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsGrantPermissions
        ]
        if isinstance(_grant_permissions, Unset):
            grant_permissions = UNSET
        else:
            grant_permissions = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsGrantPermissions(
                _grant_permissions
            )

        _replication_user = d.pop("replication_user", UNSET)
        replication_user: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsReplicationUser]
        if isinstance(_replication_user, Unset):
            replication_user = UNSET
        else:
            replication_user = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsReplicationUser(
                _replication_user
            )

        replication_user_error = d.pop("replication_user_error", UNSET)

        _user_connect = d.pop("user_connect", UNSET)
        user_connect: Union[Unset, ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsUserConnect]
        if isinstance(_user_connect, Unset):
            user_connect = UNSET
        else:
            user_connect = ListExternalInstancePgDatabasesResponse200AdditionalPropertyLogsUserConnect(_user_connect)

        list_external_instance_pg_databases_response_200_additional_property_logs = cls(
            super_admin=super_admin,
            database_credentials=database_credentials,
            valid_dbname=valid_dbname,
            created_database=created_database,
            db_connect=db_connect,
            grant_permissions=grant_permissions,
            replication_user=replication_user,
            replication_user_error=replication_user_error,
            user_connect=user_connect,
        )

        list_external_instance_pg_databases_response_200_additional_property_logs.additional_properties = d
        return list_external_instance_pg_databases_response_200_additional_property_logs

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
