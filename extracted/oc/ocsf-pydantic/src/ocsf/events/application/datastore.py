from enum import Enum

from ocsf.objects.network_endpoint import NetworkEndpoint
from ocsf.objects.http_request import HTTPRequest
from ocsf.objects.query_info import QueryInformation
from ocsf.objects.actor import Actor
from ocsf.objects.database import Database
from ocsf.objects.databucket import Databucket
from ocsf.objects.table import Table

from .application import Application

class DatastoreActivityActivityId(Enum):
    Read: int = 1
    Update: int = 2
    Connect: int = 3
    Query: int = 4
    Write: int = 5
    Create: int = 6
    Delete: int = 7
    List: int = 8
    Encrypt: int = 9
    Decrypt: int = 10

class DatastoreActivityTypeId(Enum):
    """
    The normalized datastore resource type identifier.
    """
    Other: int = 99 # The datastore resource type is not mapped.
    Unknown: int = 0 # The datastore resource type is unknown.
    Database: int = 1
    Databucket: int = 2
    Table: int = 3

class DatastoreActivity(Application):
    """
    Datastore events describe general activities (Read, Update, Query, Delete, etc.)
    which affect datastores or data within those datastores, e.g. (AWS RDS, AWS S3).
    """
    class_uid: int = 6005
    class_name: str = 'Datastore Activity'

    actor: Actor
    src_endpoint: NetworkEndpoint # Details about the source of the activity.

    # Recommended:
    database: Database | None = None
    databucket: Databucket | None = None
    table: Table | None = None
    type_id: DatastoreActivityTypeId | None = None # The normalized datastore resource type identifier.
    query_info: QueryInformation | None = None
    dst_endpoint: NetworkEndpoint | None = None # Details about the endpoint hosting the datastore
                                                # application or service.
    http_request: HTTPRequest | None = None # Details about the underlying http request.

    # Optional:
    activity_id: DatastoreActivityActivityId | None = None
    type: str | None = None # The datastore resource type (e.g. database, datastore, or table).
