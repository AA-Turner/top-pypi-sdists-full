#
# Copyright 2024 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
from datetime import datetime
import sys
import types
from typing import Optional

from databricks.connect import DatabricksSession
import trafaret as t

from datarobot import DataStore as BaseDataStore
from datarobot._compat import String
from datarobot.models.data_store import _data_store_params_converter, DataStoreParameters
from datarobot.utils import parse_time

DATABRICKS_DRIVER_CLASS = "databricks-v1"
SPARK_CONNECT_USER_AGENT = "DataRobot/10.1"


# databricks-connect==13.0 fails in _from_sdkconfig for py<3.9. workaround for that
def _get_connection_string(host: str, token: str, cluster_id: str) -> str:
    """
    Returns formated connection string for spark session compatible with python version < 3.9 for databricks-connect==13
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
        session_builder = DatabricksSession.Builder()
        session_builder.host(db_host)
        session_builder.token(db_token)
        session_builder.clusterId(db_cluster_id)
    else:
        conn_string = _get_connection_string(db_host, db_token, db_cluster_id)
        session_builder = DatabricksSession.Builder().remote(conn_string)

    try:
        session_builder.userAgent(SPARK_CONNECT_USER_AGENT)
    except AttributeError:
        # databricks-connect<13.1
        pass

    return session_builder.getOrCreate()


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

    _converter = t.Dict(
        {
            t.Key("id", optional=True) >> "data_store_id": String(),
            t.Key("type") >> "data_store_type": String(),
            t.Key("canonical_name"): String(),
            t.Key("creator"): String(),
            t.Key("params"): _data_store_params_converter,
            t.Key("updated"): parse_time,
            t.Key("role"): String(),
            t.Key("driver_class_type", optional=True): String(),
        }
    ).ignore_extra("*")

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
            data_store_id, data_store_type, canonical_name, creator, updated, params, role
        )
        print("")
        if driver_class_type == DATABRICKS_DRIVER_CLASS:
            self.get_spark_session = types.MethodType(get_spark_session, self)
