#
# Copyright 2021-2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

import trafaret as t

from datarobot._compat import String, TypedDict
from datarobot.enums import DATA_STORE_TABLE_TYPE, DataStoreListTypes, DataStoreTypes, DataTypes
from datarobot.errors import CredentialsError
from datarobot.models.api_object import APIObject, ServerDataType
from datarobot.models.credential import CredentialDataSchema
from datarobot.models.jdbc_data_preview import JdbcPreviewData
from datarobot.models.sharing import SharingRole
from datarobot.utils import from_api, parse_time, to_api
from datarobot.utils.pagination import unpaginate

field_converter = t.Dict({t.Key("id"): String(), t.Key("name"): String(), t.Key("value"): String()}).ignore_extra("*")
_data_store_params_converter = t.Dict({
    t.Key("driver_id", optional=True): t.Or(String(), t.Null()),
    t.Key("connector_id", optional=True): t.Or(String(), t.Null()),
    t.Key("jdbc_url", optional=True): t.Or(String(), t.Null()),
    t.Key("fields", optional=True): t.Or(t.List(field_converter), t.Null()),
}).ignore_extra("*")


class TestResponse(TypedDict):
    """The result of testing a data store's connection.

    Attributes
    ----------
    message : str
        A human-readable description of the test result.
    """

    message: str


class SchemasResponse(TypedDict):
    """The schemas and catalogs available through a data store.

    Attributes
    ----------
    schemas : list[str]
        The names of the schemas available in the ``catalog``.
    catalogs : list[str] or None
        The names of the catalogs available on the data store, if applicable.
    catalog : str
        The catalog that ``schemas`` belongs to.
    """

    schemas: List[str]
    catalogs: Optional[List[str]]
    catalog: str


class TableDescription(TypedDict):
    """Metadata describing a single table available through a data store.

    Attributes
    ----------
    catalog : str or None
        The catalog the table belongs to, if applicable.
    name : str
        The name of the table.
    schema : str or None
        The schema the table belongs to, if applicable.
    type : DATA_STORE_TABLE_TYPE
        The type of the table. One of :class:`datarobot.enums.DATA_STORE_TABLE_TYPE`.
    """

    catalog: Optional[str]
    name: str
    schema: Optional[str]
    type: DATA_STORE_TABLE_TYPE


class TablesResponse(TypedDict):
    """The tables available through a data store.

    Attributes
    ----------
    catalog : str
        The catalog that ``tables`` belongs to.
    tables : list[TableDescription]
        The tables available in ``catalog``.
    """

    catalog: str
    tables: List[TableDescription]


class DataStoreParameters:
    """A data store's parameters'

    Attributes
    ----------
    driver_id : str
        Optional. The identifier of the data driver if the type is one of DataStoreTypes.DR_DATABASE_V1
        or DataStoreTypes.JDBC.
    jdbc_url : str
        Optional. The full JDBC URL (for example: `jdbc:postgresql://my.dbaddress.org:5432/my_db`).
    fields: list
        Optional. If the type is `dr-database-v1`, then the fields specify the configuration.
    connector_id: str
        Optional. The connector identifier if the type is DataStoreTypes.DR_CONNECTOR_V1.
    """

    def __init__(
        self,
        driver_id: Optional[str],
        jdbc_url: Optional[str],
        fields: Optional[List[Dict[str, str]]] = None,
        connector_id: Optional[str] = None,
    ):
        _data_store_params_converter.check({
            "driver_id": driver_id,
            "jdbc_url": jdbc_url,
            "fields": fields,
            "connector_id": connector_id,
        })
        self.driver_id = driver_id
        self.connector_id = connector_id
        self.jdbc_url = jdbc_url
        self.fields = fields

    def collect_payload(self) -> Dict[str, Any]:
        """Build a dict of the parameters to send to the server"""
        dat: Dict[str, Any] = {}
        if self.driver_id is not None:
            dat["driver_id"] = self.driver_id
        if self.connector_id is not None:
            dat["connector_id"] = self.connector_id
        if self.jdbc_url is not None:
            dat["jdbc_url"] = self.jdbc_url
        if self.fields is not None:
            dat["fields"] = self.fields
        return dat


class DataStore(APIObject):
    """A data store. Represents a database.

    Attributes
    ----------
    id : str
        The ID of the data store.
    data_store_type : str
        The data store type.
    canonical_name : str
        The user-friendly name of the data store.
    creator : str
        The ID of the user who created the data store.
    updated : datetime.datetime
        The time of the last update.
    params : DataStoreParameters
        The data store parameters.
    role : str
        Your access role for this data store.
    """

    _path = "externalDataStores/"
    _converter = t.Dict({
        t.Key("id", optional=True) >> "data_store_id": String(),
        t.Key("type") >> "data_store_type": String(),
        t.Key("canonical_name"): String(),
        t.Key("creator"): String(),
        t.Key("params"): _data_store_params_converter,
        t.Key("updated"): parse_time,
        t.Key("role"): String(),
        t.Key("driver_class_type", optional=True): t.Or(String(), t.Null()),
    }).ignore_extra("*")

    def __init__(
        self,
        data_store_id: Optional[str] = None,
        data_store_type: Optional[str] = None,
        canonical_name: Optional[str] = None,
        creator: Optional[str] = None,
        updated: Optional[datetime] = None,
        params: Optional[DataStoreParameters] = None,
        role: Optional[str] = None,
        driver_class_type: Optional[str] = None,
    ):
        self._id = data_store_id
        self._type = data_store_type
        self.canonical_name = canonical_name
        self._creator = creator
        self._driver_class_type = driver_class_type
        self._updated = updated
        self.params = params
        self.role = role

    @classmethod
    def list(
        cls,
        typ: Optional[Union[str, DataStoreListTypes]] = None,
        name: Optional[str] = None,
        substitute_url_parameters: Optional[bool] = False,
        data_type: Optional[DataTypes] = None,
    ) -> List[DataStore]:
        """
        Returns a list of available data stores.

        Parameters
        ----------
        typ : str
            If specified, filters by the specified data store type. If not specified, the default
            is ``DataStoreListTypes.JDBC``.
        name: str
            If specified, filters by data store names that match or contain this name.
            The search is case-insensitive.
        substitute_url_parameters: bool
            If specified, substitutes dynamic parameters in the URL.
        data_type : DataTypes
            If specified, filters data stores that support the specified data type. If not
            specified, defaults to ``DataTypes.ALL``.

        Returns
        -------
        data_stores : list of DataStore instances
            Contains a list of available data stores.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_stores = dr.DataStore.list()
            >>> data_stores
            [DataStore('Demo'), DataStore('Airlines')]
        """
        params = {}
        if typ:
            params["type"] = typ
        if name:
            params["name"] = name
        if substitute_url_parameters:
            params["substituteUrlParameters"] = "True"
        if data_type is not None:
            params["dataType"] = str(data_type)

        if params:
            r_data = cls._client.get(cls._path, params=params).json()
        else:
            r_data = cls._client.get(cls._path).json()
        return [cls.from_server_data(item) for item in r_data["data"]]

    @classmethod
    def get(cls, data_store_id: str, substitute_url_parameters: Optional[bool] = False) -> DataStore:
        """
        Returns the data store.

        Parameters
        ----------
        data_store_id : str
            The identifier of the data store.
        substitute_url_parameters: bool
            If specified, substitutes dynamic parameters in the URL.

        Returns
        -------
        data_store : DataStore
            The required data store.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_store = dr.DataStore.get('5a8ac90b07a57a0001be501e')
            >>> data_store
            DataStore('Demo')
        """
        if substitute_url_parameters:
            params = {"substituteUrlParameters": "True"}
        else:
            params = None
        return cls.from_location(f"{cls._path}{data_store_id}/", params=params)

    @classmethod
    def create(
        cls,
        data_store_type: Union[str, DataStoreTypes],
        canonical_name: str,
        driver_id: Optional[str] = None,
        jdbc_url: Optional[str] = None,
        fields: Optional[List[Dict[str, str]]] = None,
        connector_id: Optional[str] = None,
    ) -> DataStore:
        """
        Creates the data store.

        Parameters
        ----------
        data_store_type : str or DataStoreTypes
            The data store type.
        canonical_name : str
            The user-friendly name of the data store.
        driver_id : str
            Optional. The identifier of the DataDriver when ``data_store_type`` is
            ``DataStoreListTypes.JDBC`` or ``DataStoreListTypes.DR_DATABASE_V1``.
        jdbc_url : str
            Optional. The full JDBC URL (for example: `jdbc:postgresql://my.dbaddress.org:5432/my_db`).
        fields: list
            Optional. If the type is `dr-database-v1`, then the fields specify the configuration.
        connector_id: str
            Optional. The identifier of the Connector when ``data_store_type`` is
            ``DataStoreListTypes.DR_CONNECTOR_V1``.
        Returns
        -------
        data_store : DataStore
            The created data store.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_store = dr.DataStore.create(
            ...     data_store_type='jdbc',
            ...     canonical_name='Demo DB',
            ...     driver_id='5a6af02eb15372000117c040',
            ...     jdbc_url='jdbc:postgresql://my.db.address.org:5432/perftest'
            ... )
            >>> data_store
            DataStore('Demo DB')
        """
        payload = {
            "type": str(data_store_type),
            "canonicalName": canonical_name,
            "params": DataStoreParameters(
                driver_id=driver_id, jdbc_url=jdbc_url, fields=fields, connector_id=connector_id
            ).collect_payload(),
        }
        return cls.from_server_data(cls._client.post(cls._path, data=payload).json())

    def update(
        self,
        canonical_name: Optional[str] = None,
        driver_id: Optional[str] = None,
        connector_id: Optional[str] = None,
        jdbc_url: Optional[str] = None,
        fields: Optional[List[Dict[str, str]]] = None,
    ) -> None:
        """
        Updates the data store.

        Parameters
        ----------
        canonical_name : str
            Optional; the user-friendly name of the data store.
        driver_id : str
            Optional. The identifier of the DataDriver. if the type is one of DataStoreTypes.DR_DATABASE_V1
            or DataStoreTypes.JDBC.
        connector_id : str
            Optional. The identifier of the Connector. if the type is DataStoreTypes.DR_CONNECTOR_V1.
        jdbc_url : str
            Optional. The full JDBC URL (for example: `jdbc:postgresql://my.dbaddress.org:5432/my_db`).
        fields: list
            Optional. If the type is `dr-database-v1`, then the fields specify the configuration.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_store = dr.DataStore.get('5ad5d2afef5cd700014d3cae')
            >>> data_store
            DataStore('Demo DB')
            >>> data_store.update(canonical_name='Demo DB updated')
            >>> data_store
            DataStore('Demo DB updated')
        """
        params = DataStoreParameters(
            driver_id=driver_id or self.params.driver_id,  # type: ignore[union-attr]
            connector_id=connector_id or self.params.connector_id,  # type: ignore[union-attr]
            jdbc_url=jdbc_url or self.params.jdbc_url,  # type: ignore[union-attr]
            fields=fields or self.params.fields,  # type: ignore[union-attr]
        ).collect_payload()
        # if we are updating fields, then we cannot include driver_id or connector_id
        if params.get("fields"):
            params.pop("driver_id", None)
            params.pop("connector_id", None)

        payload = {
            "canonicalName": canonical_name or self.canonical_name,
            "params": params,
        }
        r_data = self._client.patch(f"{self._path}{self.id}/", data=payload).json()
        self.canonical_name = r_data["canonicalName"]
        self.params = DataStoreParameters(
            r_data["params"].get("driverId"),
            r_data["params"].get("jdbcUrl"),
            r_data["params"].get("fields"),
            r_data["params"].get("connectorId"),
        )

    def delete(self) -> None:
        """Removes the DataStore"""
        self._client.delete(f"{self._path}{self.id}/")

    def test(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        credential_id: Optional[str] = None,
        use_kerberos: Optional[bool] = None,
        credential_data: Optional[Dict[str, str]] = None,
        set_default_credential: bool = False,
    ) -> TestResponse:
        """
        Tests database connection.

        .. versionchanged:: v3.2
           Added ``credential_id``, ``use_kerberos``, and ``credential_data`` optional parameters and made
           ``username`` and ``password`` optional.
        .. versionchanged:: v3.9
           When you provide ``credential_id`` and set ``set_default_credential`` to True and the connection test
           succeeds, DataRobot sets the credential as the default for this data store.

        Parameters
        ----------
        username : str
            Optional. The username for database authentication.
        password : str
            Optional. The password for database authentication. The server encrypts the password
            during the request and never saves or stores it.
        credential_id : str
            Optional. The ID of the credentials to use instead of username and password.
        use_kerberos : bool
            Optional. Whether to use Kerberos for data store authentication.
        credential_data : dict
            Optional. The credentials to authenticate with the database, to use instead of
            username/password or credential ID.
        set_default_credential: bool
            Optional. If True and you provide ``credential_id``, sets the credential as the default for this data
            store. Defaults to False.

        Returns
        -------
        message : dict
            Message with status.

        Raises
        ------
        CredentialsError
            If unable to set the provided ``credential_id`` as default for this data store.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_store = dr.DataStore.get('5ad5d2afef5cd700014d3cae')
            >>> data_store.test(username='db_username', password='db_password')
            {'message': 'Connection successful'}
        """
        payload = {
            "user": username,
            "password": password,
            "credential_id": credential_id,
            "use_kerberos": use_kerberos,
        }
        if credential_data:
            payload["credential_data"] = CredentialDataSchema(credential_data)
        response = self._client.post(f"{self._path}{self.id}/test/", data=to_api(payload))
        if set_default_credential and response.status_code == 200 and credential_id is not None:
            cred_assoc_resp = self._client.put(
                f"credentials/{credential_id}/associations/dataconnection:{self.id}/",
                json={"isDefault": True},
            )
            if cred_assoc_resp.status_code not in {200, 201}:
                raise CredentialsError(f"Unable to set {credential_id} as default credential")
        return response.json()  # type: ignore[no-any-return] # noqa: E501

    def schemas(self, username: str, password: str) -> SchemasResponse:
        """
        Returns a list of available schemas.

        Parameters
        ----------
        username : str
            The username for database authentication.
        password : str
            The password for database authentication. The server encrypts the password during the
            request and never saves or stores it.

        Returns
        -------
        response : dict
            A dictionary with the database name and a list of available schemas.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_store = dr.DataStore.get('5ad5d2afef5cd700014d3cae')
            >>> data_store.schemas(username='db_username', password='db_password')
            {'catalog': 'perftest', 'schemas': ['demo', 'information_schema', 'public']}
        """
        payload = {"user": username, "password": password}
        return self._client.post(f"{self._path}{self.id}/schemas/", data=payload).json()  # type: ignore[no-any-return]

    def tables(self, username: str, password: str, schema: Optional[str] = None) -> TablesResponse:
        """
        Returns a list of available tables in a schema.

        Parameters
        ----------
        username : str
            Optional. The username for database authentication.
        password : str
            Optional. The password for database authentication. The server encrypts the password
            during the request and never saves or stores it.
        schema : str
            Optional. The schema name.

        Returns
        -------
        response : dict
            A dictionary with the catalog name and table information.

        Examples
        --------
        .. code-block:: python

            >>> import datarobot as dr
            >>> data_store = dr.DataStore.get('5ad5d2afef5cd700014d3cae')
            >>> data_store.tables(username='db_username', password='db_password', schema='demo')
            {'tables': [{'type': 'TABLE', 'name': 'diagnosis', 'schema': 'demo'}, {'type': 'TABLE',
            'name': 'kickcars', 'schema': 'demo'}, {'type': 'TABLE', 'name': 'patient',
            'schema': 'demo'}, {'type': 'TABLE', 'name': 'transcript', 'schema': 'demo'}],
            'catalog': 'perftest'}
        """
        payload = {"schema": schema, "user": username, "password": password}
        return self._client.post(f"{self._path}{self.id}/tables/", data=payload).json()  # type: ignore[no-any-return]

    @classmethod
    def from_server_data(  # type: ignore[override]
        cls, data: ServerDataType, keep_attrs: Optional[List[str]] = None
    ) -> DataStore:
        converted_data = cls._converter.check(from_api(data))
        params = converted_data.pop("params")
        converted_data["params"] = DataStoreParameters(
            params.get("driver_id"),
            params.get("jdbc_url"),
            params.get("fields"),
            params.get("connector_id"),
        )
        return cls(**converted_data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.canonical_name or self.id}')"

    @property
    def id(self) -> Optional[str]:
        return self._id

    @property
    def creator(self) -> Optional[str]:
        return self._creator

    @property
    def type(self) -> Optional[str]:
        return self._type

    @property
    def updated(self) -> Optional[datetime]:
        return self._updated

    @property
    def driver_class_type(self) -> Optional[str]:
        return self._driver_class_type

    def get_shared_roles(self) -> List[SharingRole]:
        """Retrieve what users have access to this data store

        .. versionadded:: v3.2

        Returns
        -------
        list of :class:`SharingRole <datarobot.models.sharing.SharingRole>`
        """
        url = f"{self._path}{self.id}/sharedRoles/"
        return [SharingRole.from_server_data(datum) for datum in unpaginate(url, {}, self._client)]

    def share(self, access_list: List[SharingRole]) -> None:
        """Modify the ability of users to access this data store

        .. versionadded:: v2.14

        Parameters
        ----------
        access_list : list of :class:`SharingRole <datarobot.models.sharing.SharingRole>`
            The modifications to make.

        Returns
        -------
        None

        Raises
        ------
        datarobot.ClientError :
            if you do not have permission to share this data store, if the user you're sharing with
            doesn't exist, if the same user appears multiple times in the access_list, or if these
            changes would leave the data store without an owner.

        Examples
        --------
        The :class:`SharingRole <datarobot.models.sharing.SharingRole>` class is needed in order to
        share a Data Store with one or more users.

        For example, suppose you had a list of user IDs you wanted to share this DataStore with. You could use
        a loop to generate a list of :class:`SharingRole <datarobot.models.sharing.SharingRole>` objects for them,
        and bulk share this Data Store.

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.sharing import SharingRole
            >>> from datarobot.enums import SHARING_ROLE, SHARING_RECIPIENT_TYPE
            >>>
            >>> user_ids = ["60912e09fd1f04e832a575c1", "639ce542862e9b1b1bfa8f1b", "63e185e7cd3a5f8e190c6393"]
            >>> sharing_roles = []
            >>> for user_id in user_ids:
            ...     new_sharing_role = SharingRole(
            ...         role=SHARING_ROLE.CONSUMER,
            ...         share_recipient_type=SHARING_RECIPIENT_TYPE.USER,
            ...         id=user_id,
            ...         can_share=True,
            ...     )
            ...     sharing_roles.append(new_sharing_role)
            >>> dr.DataStore.get('my-data-store-id').share(access_list)

        Similarly, a :class:`SharingRole <datarobot.models.sharing.SharingRole>` instance can be used to
        remove a user's access if the ``role`` is set to ``SHARING_ROLE.NO_ROLE``, like in this example:

        .. code-block:: python

            >>> import datarobot as dr
            >>> from datarobot.models.sharing import SharingRole
            >>> from datarobot.enums import SHARING_ROLE, SHARING_RECIPIENT_TYPE
            >>>
            >>> user_to_remove = "foo.bar@datarobot.com"
            ... remove_sharing_role = SharingRole(
            ...     role=SHARING_ROLE.NO_ROLE,
            ...     share_recipient_type=SHARING_RECIPIENT_TYPE.USER,
            ...     username=user_to_remove,
            ...     can_share=False,
            ... )
            >>> dr.DataStore.get('my-data-store-id').share(roles=[remove_sharing_role])
        """
        formatted_roles = [access.collect_payload() for access in access_list]
        payload = {"roles": formatted_roles, "operation": "updateRoles"}
        self._client.patch(f"{self._path}{self.id}/sharedRoles/", data=payload)

    def preview_table(
        self,
        table_name: str,
        *,
        max_rows: Optional[int] = 100,
        catalog: Optional[str] = None,
        schema: Optional[str] = None,
        credential_id: Optional[str] = None,
        use_kerberos: Optional[bool] = None,
    ) -> JdbcPreviewData:
        """
        Preview data from a table in the data store.

        Parameters
        ----------
        table_name:
            Name of the table to preview.
        max_rows:
            Maximum number of rows to preview.
        catalog:
            Catalog of the table to preview.
        schema:
            Schema of the table to preview.
        credential_id:
            ID of the credential to use instead of default credentials.
        use_kerberos:
            Whether to use Kerberos for authentication.

        Returns
        -------
        JdbcPreviewData:
            Object with preview data and result schema.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.models.data_store import DataStore
            >>> data_store = DataStore.get("my_data_store_id")
            >>> credential_id = "my_credential_id"
            >>> preview = data_store.preview_table(
            ...     "my_table_name",
            ...     credential_id=credential_id,
            ...     schema="my_schema",
            ...     catalog="my_catalog",
            ...     max_rows=10,
            ... )
            >>> preview.columns
            ['id', 'name', 'email']
            >>> preview.records
            [
                {'id': 1, 'name': 'John Doe', 'email': 'john.doe@example.com'},
                {'id': 2, 'name': 'Jane Doe', 'email': 'jane.doe@example.com'},
            ]
            >>> preview.df.head()
                id  name  email
            0   1   John  john.doe@example.com
            1   2   Jane  jane.doe@example.com

        """
        payload = {
            "table": table_name,
            "max_rows": max_rows,
            "catalog": catalog,
            "schema": schema,
            "credential_id": credential_id,
            "use_kerberos": use_kerberos,
        }
        resp = self._client.post(f"{self._path}{self.id}/preview/", data=to_api(payload))
        return JdbcPreviewData.from_server_data(resp.json())

    def preview_query(
        self,
        sql: str,
        *,
        max_rows: Optional[int] = 100,
        credential_id: Optional[str] = None,
        bind_parameters: Optional[List[Optional[Union[str, int, float, bool, datetime, date]]]] = None,
        read_timeout: int = 300,
    ) -> JdbcPreviewData:
        """
        Execute a SQL query statement against a data store and return a preview of the results.

        Parameters
        ----------
        sql:
            The SQL query statement to execute.
        max_rows:
            The maximum number of rows to return.
        credential_id:
            The ID of the credential to use. If not provided, the default credential will be used.
        bind_parameters:
            List of values to bind to the SQL statement. Each value is bound to
            a `?` placeholder in the SQL statement. Binding is in-order.
        read_timeout:
            Seconds to wait for the response from the server.

        Returns
        -------
        JdbcPreviewData:
            Object with preview data and result schema.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.models.data_store import DataStore
            >>> data_store = DataStore.get("my_data_store_id")
            >>> preview = data_store.preview_query(
            ...     "SELECT * FROM my_catalog.my_schema.my_table WHERE name LIKE ?",
            ...     credential_id="my_credential_id",
            ...     max_rows=10,
            ...     bind_parameters=['%Doe%'],
            ... )
            >>> preview.columns
            ['id', 'name', 'email']
            >>> preview.records
            [
                {'id': 1, 'name': 'John Doe', 'email': 'john.doe@example.com'},
                {'id': 2, 'name': 'Jane Doe', 'email': 'jane.doe@example.com'},
            ]
            >>> preview.df.head()
                id  name      email
            0   1   John Doe  john.doe@example.com
            1   2   Jane Doe  jane.doe@example.com
        """
        payload = {
            "sql": sql,
            "max_rows": max_rows,
            "credential_id": credential_id,
            "bind_params": bind_parameters,
        }
        resp = self._client.post(
            f"{self._path}{self.id}/previewQuery/",
            data=to_api(payload),
            timeout=(self._client.connect_timeout, read_timeout),
        )
        return JdbcPreviewData.from_server_data(resp.json())

    def execute_update(
        self,
        sql: str,
        *,
        credential_id: Optional[str] = None,
        bind_parameters: Optional[List[Optional[Union[str, int, float, bool, datetime, date]]]] = None,
        read_timeout: int = 300,
    ) -> str:
        """
        Execute a SQL update statement against a data store. Returns the message from the server.

        Parameters
        ----------
        sql:
            The SQL update statement to execute.
        credential_id:
            The ID of the credential to use. If not provided, the default credential will be used.
        bind_parameters:
            List of values to bind to the SQL statement. Each value is bound to
            a `?` placeholder in the SQL statement. Binding is in-order.
        read_timeout:
            Seconds to wait for the response from the server.

        Returns
        -------
        str:
            The message from the server. Returns "OK" if successful.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.models.data_store import DataStore
            >>> data_store = DataStore.get("my_data_store_id")
            >>> data_store.execute_update(
            ...     "UPDATE my_table SET name = ? WHERE id = ?",
            ...     credential_id="my_credential_id",
            ...     bind_parameters=['John', 1],
            ... )
            "OK"
        """
        payload = {
            "sql": sql,
            "credential_id": credential_id,
            "bind_params": bind_parameters,
        }
        resp = self._client.post(
            f"{self._path}{self.id}/executeUpdate/",
            data=to_api(payload),
            timeout=(self._client.connect_timeout, read_timeout),
        )
        return resp.json().get("message") or ""

    @classmethod
    def is_execute_update_success(cls, message: str) -> bool:
        """
        Check if the message from the server indicates a successful execute update.

        Parameters
        ----------
        message:
            The message from the server.

        Returns
        -------
        bool:
            True if the message indicates a successful execute update, False otherwise.

        Examples
        --------
        .. code-block:: python

            >>> from datarobot.models.data_store import DataStore
            >>> ds = DataStore.get("my_data_store_id")
            >>> DataStore.is_execute_update_success(
            ...     ds.execute_update("UPDATE my_table SET name = 'John Doe' WHERE id = 1")
            ... )
            True
        """
        return message == "OK"
