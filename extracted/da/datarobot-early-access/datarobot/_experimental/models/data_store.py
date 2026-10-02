#
# Copyright 2024-2025 DataRobot, Inc. and its affiliates.
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

from datetime import datetime
import sys
import types
from typing import Any, Dict, List, Optional

from databricks.connect import DatabricksSession
import trafaret as t

from datarobot import DataStore as BaseDataStore
from datarobot._compat import String, TypedDict
from datarobot.models.data_store import DataStoreParameters, _data_store_params_converter
from datarobot.rest import RESTClientObject
from datarobot.utils import from_api, parse_time, to_api

DATABRICKS_DRIVER_CLASS = "databricks-v1"
SPARK_CONNECT_USER_AGENT = "DataRobot/10.1"


# databricks-connect==13.0 fails in _from_sdkconfig for py<3.9. workaround for that
def _get_connection_string(host: str, token: str, cluster_id: str) -> str:
    """
    Return a formatted connection string for a Spark session compatible with
    Python < 3.9 (databricks-connect==13).
    """
    if cluster_id is None:
        # host and token presence are validated by the SDK. cluster id is not.
        raise Exception("Cluster id is required but was not specified.")

    if host.startswith("http://"):
        host = host[len("http://") :]
    if host.startswith("https://"):
        host = host[len("https://") :]

    return f"sc://{host}:443/;token={token};x-databricks-cluster-id={cluster_id}"


def get_spark_session(self, db_token: str):  # type: ignore[no-untyped-def]
    """
    Returns a Spark session

    Parameters
    ----------
    db_token : str
        A personal access token.

    Returns
    -------
    SparkSession
            A spark session initialized with connection parameters taken from DataStore and provided `db_token`.

    Examples
    --------
    .. code-block:: python

        >>> from datarobot._experimental.models.data_store import DataStore
        >>> data_stores = DataStore.list(typ=DataStoreListTypes.DR_DATABASE_V1)
        >>> data_stores
        [DataStore('my_databricks_store_1')]
        >>> db_connection = data_stores[0].get_spark_session('<token>')
        >>> db_connection
        <pyspark.sql.connect.session.SparkSession at 0x7f386068fbb0>
        >>> df = session.read.table("samples.nyctaxi.trips")
        >>> df.show()
    """
    data = self.params.fields
    http_path = next(item["value"] for item in data if item["id"] == "dbx.http_path")
    server_hostname = next(item["value"] for item in data if item["id"] == "dbx.server_hostname")

    # Extracting cluster ID from HTTP path
    db_cluster_id = http_path.split("/")[-1]

    # Constructing the db_host URL
    db_host = f"https://{server_hostname}"

    if sys.version_info >= (3, 9, 0):
        session_builder = DatabricksSession.Builder()  # type: ignore[no-untyped-call]
        session_builder.host(db_host)
        session_builder.token(db_token)
        session_builder.clusterId(db_cluster_id)
    else:
        conn_string = _get_connection_string(db_host, db_token, db_cluster_id)
        session_builder = DatabricksSession.Builder().remote(conn_string)  # type: ignore[no-untyped-call]

    try:
        session_builder.userAgent(SPARK_CONNECT_USER_AGENT)
    except AttributeError:
        # databricks-connect<13.1
        pass

    return session_builder.getOrCreate()


class BrowseConnectionItem(TypedDict, total=False):
    """A single item returned by browse_connection."""

    name: str
    metadata: Optional[Dict[str, Any]]
    is_folder: Optional[bool]


class BrowseConnectionPaginator:
    """
    Paginated browse_connection response with helpers to fetch next/previous pages.
    """

    def __init__(
        self,
        *,
        client: RESTClientObject,
        path: str,
        count: int,
        next_url: Optional[str],
        previous_url: Optional[str],
        total_count: Optional[int],
        data: List[BrowseConnectionItem],
        credential_id: Optional[str] = None,
        use_kerberos: Optional[bool] = None,
        filter: Optional[str] = None,
    ):
        self.client = client
        self.count = count
        self.path = path
        self.next_url = next_url
        self.previous_url = previous_url
        self.total_count = total_count
        self.data = data
        self.credential_id = credential_id
        self.use_kerberos = use_kerberos
        self.filter = filter

    def _fetch(self, url: str) -> "BrowseConnectionPaginator":
        payload: Dict[str, Any] = {
            "path": self.path,
            "credential_id": self.credential_id,
            "use_kerberos": self.use_kerberos,
            "filter": self.filter,
        }
        payload_api = to_api(payload)
        resp = self.client.post(url, data=payload_api).json()  # type: ignore[arg-type]
        parsed = from_api(resp, keep_null_keys=True)
        return BrowseConnectionPaginator(
            client=self.client,
            path=self.path,
            count=parsed.get("count", 0),  # type: ignore[union-attr]
            next_url=parsed.get("next"),  # type: ignore[union-attr]
            previous_url=parsed.get("previous"),  # type: ignore[union-attr]
            total_count=parsed.get("total_count"),  # type: ignore[union-attr]
            data=parsed.get("data") or [],  # type: ignore[union-attr]
            credential_id=self.credential_id,
            use_kerberos=self.use_kerberos,
            filter=self.filter,
        )

    def next(self) -> Optional["BrowseConnectionPaginator"]:
        if not self.next_url:
            return None
        return self._fetch(self.next_url)

    def previous(self) -> Optional["BrowseConnectionPaginator"]:
        if not self.previous_url:
            return None
        return self._fetch(self.previous_url)


class DataStore(BaseDataStore):
    """A data store. Represents database

    Attributes
    ----------
    id : str
        The ID of the data store.
    data_store_type : str
        The type of data store.
    canonical_name : str
        The user-friendly name of the data store.
    creator : str
        The ID of the user who created the data store.
    updated : datetime.datetime
        The time of the last update.
    params : DataStoreParameters
        A list specifying data store parameters.
    role : str
        Your access role for this data store.
    driver_class_type : str
        Your access role for this data store.
    """

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
        super().__init__(
            data_store_id=data_store_id,
            data_store_type=data_store_type,
            canonical_name=canonical_name,
            creator=creator,
            updated=updated,
            params=params,
            role=role,
            driver_class_type=driver_class_type,
        )

        if driver_class_type == DATABRICKS_DRIVER_CLASS:
            self.get_spark_session = types.MethodType(get_spark_session, self)

    def browse_connection(
        self,
        path: str,
        *,
        credential_id: Optional[str] = None,
        use_kerberos: Optional[bool] = None,
        filter: Optional[str] = None,
        offset: Optional[int] = 0,
        limit: Optional[int] = 100,
        search: Optional[str] = None,
        sort: Optional[str] = None,
    ) -> BrowseConnectionPaginator:
        """
        Browse objects in a data store connection.

        Parameters
        ----------
        path : str
            Path to browse within the data store.
        credential_id : str, optional
            Identifier of stored credentials to use instead of default credentials.
        use_kerberos : bool, optional
            Whether to use Kerberos for authentication.
        filter : str, optional
            Filter string, only applicable to some connection types such as Jira (when provided, path is
            ignored server-side).
        offset : int, optional
            Pagination offset. Defaults to 0.
        limit : int, optional
            Pagination limit. Defaults to 100.
        search : str, optional
            Optional search string for supported connectors.
        sort : str, optional
            Optional sort field for supported connectors.

        Returns
        -------
        BrowseConnectionPaginator
            Paginated listing of connection items with helpers for next/previous.
        """
        payload: Dict[str, Any] = {
            "path": path,
            "credential_id": credential_id,
            "use_kerberos": use_kerberos,
            "filter": filter,
        }
        params = {
            k: v
            for k, v in {
                "offset": offset,
                "limit": limit,
                "search": search,
                "sort": sort,
            }.items()
            if v is not None
        }

        url = f"{self._path}{self.id}/browseConnection/"
        payload_api = to_api(payload)
        resp = self._client.post(url, data=payload_api, params=params).json()
        parsed = from_api(resp, keep_null_keys=True)
        return BrowseConnectionPaginator(
            client=self._client,
            path=path,
            count=parsed.get("count", 0),  # type: ignore[union-attr]
            next_url=parsed.get("next"),  # type: ignore[union-attr]
            previous_url=parsed.get("previous"),  # type: ignore[union-attr]
            total_count=parsed.get("total_count"),  # type: ignore[union-attr]
            data=parsed.get("data") or [],  # type: ignore[union-attr]
            credential_id=credential_id,
            use_kerberos=use_kerberos,
            filter=filter,
        )
