# btrdb.conn
# Connection related objects for the BTrDB library
#
# Author:   PingThings
# Created:  Fri Dec 21 14:57:30 2018 -0500
#
# For license information, see LICENSE.txt
# ID: conn.py [] allen@pingthings.io $

"""
Connection related objects for the BTrDB library
"""

##########################################################################
## Imports
##########################################################################

import importlib.metadata
import json
import logging
import os
import re
import uuid as uuidlib
from concurrent.futures import ThreadPoolExecutor
from typing import List, Tuple, Union
from warnings import warn

import certifi
import grpc
from grpc._cython.cygrpc import CompressionAlgorithm

from btrdb.exceptions import BTrDBError, InvalidOperation, StreamNotFoundError, retry
from btrdb.stream import Stream, StreamSet
from btrdb.utils.conversion import to_uuid
from btrdb.utils.general import unpack_stream_descriptor

##########################################################################
## Module Variables
##########################################################################

MIN_TIME = -(16 << 56)
MAX_TIME = 48 << 56
MAX_POINTWIDTH = 63


##########################################################################
## Classes
##########################################################################
logger = logging.getLogger(__name__)


class Connection(object):
    def __init__(self, addrportstr, apikey=None):
        """
        Connects to a BTrDB server

        Parameters
        ----------
        addrportstr : str, required
            The address of the cluster to connect to, e.g 123.123.123:4411
        apikey : str, optional
            The optional API key to authenticate requests

        Notes
        -----
        The ``btrdb.connect`` method is a helper function to make connecting to the platform easier
            usually that will be sufficient for most users.
        """
        # 4 Is a magic number to make sure the error propagates where btrdb.connect is called.
        warn(
            "This API is deprecated in favor of the pingthings_api, refer to your hub landing page for further documentation.",
            FutureWarning,
            stacklevel=4,
        )
        addrport = addrportstr.split(":", 2)
        # 100MB size limit ~ 2500 streams for 5000 points with each point being 64bit
        # 500MB size limit ~ 13K streams for 5000 points
        # -1 size limit = no limit of size to send
        chan_ops = [("grpc.max_receive_message_length", -1)]

        if len(addrport) != 2:
            raise ValueError("expecting address:port")

        if addrport[1] == "4411":
            # grpc bundles its own CA certs which will work for all normal SSL
            # certificates but will fail for custom CA certs. Allow the user
            # to specify a CA bundle via env var to overcome this
            env_bundle = os.getenv("BTRDB_CA_BUNDLE", "")

            # certifi certs are provided as part of this package install
            # https://github.com/certifi/python-certifi
            lib_certs = certifi.where()

            ca_bundle = env_bundle

            if ca_bundle == "":
                ca_bundle = lib_certs
            try:
                with open(ca_bundle, "rb") as f:
                    contents = f.read()
            except Exception:
                if env_bundle != "":
                    # The user has given us something but we can't use it, we need to make noise
                    raise Exception(
                        "BTRDB_CA_BUNDLE(%s) env is defined but could not read file"
                        % ca_bundle
                    )
                else:
                    contents = None

            if apikey is None:
                self.channel = grpc.secure_channel(
                    addrportstr,
                    grpc.ssl_channel_credentials(contents),
                    options=chan_ops,
                )
            else:
                self.channel = grpc.secure_channel(
                    addrportstr,
                    grpc.composite_channel_credentials(
                        grpc.ssl_channel_credentials(contents),
                        grpc.access_token_call_credentials(apikey),
                    ),
                    options=chan_ops,
                )
        else:
            self.channel = grpc.insecure_channel(addrportstr, chan_ops)
            if apikey is not None:

                class AuthCallDetails(grpc.ClientCallDetails):
                    def __init__(self, apikey, client_call_details):
                        metadata = []
                        if client_call_details.metadata is not None:
                            metadata = list(client_call_details.metadata)
                        metadata.append(("authorization", "Bearer " + apikey))
                        version = "unknown"
                        try:
                            version = importlib.metadata.version("btrdb")
                        except Exception:
                            pass
                        metadata.append(
                            (
                                "x-api-client",
                                "btrdbpy-" + version,
                            )
                        )
                        self.method = client_call_details.method
                        self.timeout = client_call_details.timeout
                        self.credentials = client_call_details.credentials
                        self.wait_for_ready = client_call_details.wait_for_ready
                        self.compression = client_call_details.compression
                        self.metadata = metadata

                class AuthorizationInterceptor(
                    grpc.UnaryUnaryClientInterceptor,
                    grpc.UnaryStreamClientInterceptor,
                    grpc.StreamUnaryClientInterceptor,
                    grpc.StreamStreamClientInterceptor,
                ):
                    def __init__(self, apikey):
                        self.apikey = apikey

                    def intercept_unary_unary(
                        self, continuation, client_call_details, request
                    ):
                        return continuation(
                            AuthCallDetails(self.apikey, client_call_details), request
                        )

                    def intercept_unary_stream(
                        self, continuation, client_call_details, request
                    ):
                        return continuation(
                            AuthCallDetails(self.apikey, client_call_details), request
                        )

                    def intercept_stream_unary(
                        self, continuation, client_call_details, request_iterator
                    ):
                        return continuation(
                            AuthCallDetails(self.apikey, client_call_details),
                            request_iterator,
                        )

                    def intercept_stream_stream(
                        self, continuation, client_call_details, request_iterator
                    ):
                        return continuation(
                            AuthCallDetails(self.apikey, client_call_details),
                            request_iterator,
                        )

                self.channel = grpc.intercept_channel(
                    self.channel,
                    AuthorizationInterceptor(apikey),
                )


def _is_arrow_enabled(info):
    info = {
        "majorVersion": info.majorVersion,
        "minorVersion": info.minorVersion,
    }
    major = info.get("majorVersion", -1)
    minor = info.get("minorVersion", -1)
    if logger.isEnabledFor(logging.DEBUG):
        logger.debug(f"major version: {major}")
        logger.debug(f"minor version: {minor}")
    if major >= 5 and minor >= 30:
        return True
    else:
        return False


class BTrDB(object):
    """
    The primary server connection object for communicating with a BTrDB server.
    """

    def __init__(self, endpoint):
        self.ep = endpoint
        try:
            _ = self.ep.info()
        except Exception as err:
            raise BTrDBError(f"Could not connect to the database, error message: {err}")
        self._executor = ThreadPoolExecutor()
        try:
            self._ARROW_ENABLED = _is_arrow_enabled(self.ep.info())
        except Exception:
            self._ARROW_ENABLED = False
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"ARROW ENABLED: {self._ARROW_ENABLED}")

    @retry
    def query(
        self,
        stmt: str,
        params: Union[Tuple[str], List[str]] = None,
        auto_retry=False,
        retries=5,
        retry_delay=3,
        retry_backoff=4,
    ):
        """
        Performs a SQL query on the database metadata and returns a list of
        dictionaries from the resulting cursor.

        Parameters
        ----------
        stmt : str
            a SQL statement to be executed on the BTrDB metadata.  Available
            tables are noted below.  To sanitize inputs use a `$1` style parameter such as
            `select * from streams where name = $1 or name = $2`.
        params : list or tuple
            a list of parameter values to be sanitized and interpolated into the
            SQL statement. Using parameters forces value/type checking and is
            considered a best practice at the very least.
        auto_retry : bool, default: False
            Whether to retry this request in the event of an error
        retries : int, default: 5
            Number of times to retry this request if there is an error. Will
            be ignored if auto_retry is False
        retry_delay : int, default: 3
            initial time to wait before retrying function call if there is an error.
            Will be ignored if auto_retry is False
        retry_backoff : int, default: 4
            Exponential factor by which the backoff increases between retries.
            Will be ignored if auto_retry is False

        Returns
        -------
        list
            a list of dictionary object representing the cursor results.


        Notes
        -------
        Parameters will be inserted into the SQL statement as noted by the
        parameter number such as `$1`, `$2`, or `$3`.  The `streams` table is
        available for `SELECT` statements only.

        See https://btrdb.readthedocs.io/en/latest/ for more info.

        The following are the queryable columns in the postgres ``streams`` table.

        +------------------+------------------------+-----------+
        |      Column      |          Type          | Nullable  |
        +==================+========================+===========+
        | uuid             | uuid                   | not null  |
        +------------------+------------------------+-----------+
        | collection       | character varying(256) | not null  |
        +------------------+------------------------+-----------+
        | name             | character varying(256) | not null  |
        +------------------+------------------------+-----------+
        | unit             | character varying(256) | not null  |
        +------------------+------------------------+-----------+
        | ingress          | character varying(256) | not null  |
        +------------------+------------------------+-----------+
        | property_version | bigint                 | not null  |
        +------------------+------------------------+-----------+
        | annotations      | hstore                 |           |
        +------------------+------------------------+-----------+

        Examples
        --------
        Count all streams in the platform.

        >>> conn = btrdb.connect()
        >>> conn.query("SELECT COUNT(uuid) FROM streams")
        [{'count': ...}]

        Count all streams in the collection ``foo/bar`` by passing in the variable as a parameter.

        >>> conn.query("SELECT COUNT(uuid) FROM streams WHERE collection=$1::text", params=["foo/bar"])
        [{'count': ...}]

        Count all streams in the platform that has a non-null entry for the metadata annotation ``foo``.

        >>> conn.query("SELECT COUNT(uuid) FROM streams WHERE annotations->$1::text IS NOT NULL", params=["foo"])
        [{'count': ...}]
        """
        if params is None:
            params = list()
        return [
            json.loads(row.decode("utf-8"))
            for page in self.ep.sql_query(stmt, params)
            for row in page
        ]

    def streams(self, *identifiers, versions=None, is_collection_prefix=False):
        """
        Returns a StreamSet object with BTrDB streams from the supplied
        identifiers.  If any streams cannot be found matching the identifier
        then a ``StreamNotFoundError`` will be returned.

        Parameters
        ----------
        identifiers : str or UUID
            a single item or iterable of items which can be used to query for
            streams. Identifiers are expected to be UUID as string, UUID as UUID,
            or collection/name string.

        versions : list[int]
            a single or iterable of version numbers to match the identifiers

        is_collection_prefix : bool, default=False
            If providing a collection string, is that string just a prefix, or the entire collection name?
            This will impact how many streams are returned.


        Returns
        -------
        :class:`StreamSet`
            Collection of streams.

        Examples
        --------
        With a sequence of uuids.

        >>> conn = btrdb.connect()
        >>> conn.streams(identifiers=list_of_uuids)
        <btrdb.stream.StreamSet at 0x...>

        With a sequence of uuids and version numbers.
        Here we are using version 0 to use the latest data points.

        >>> conn.streams(identifiers=list_of_uuids, versions=[0 for _ in list_of_uuids])
        <btrdb.stream.StreamSet at 0x...>

        Filtering by ``collection`` prefix ``"foo"`` where multiple collections exist like the following:
        ``foo/bar``, ``foo/baz``, ``foo/bar/new``, and ``foo``.
        If we set `is_collection_prefix`` to ``True``, this will return all streams that exist in the collections defined above.
        It is similar to a regex pattern ``^foo.*`` for matching purposes.

        >>> conn.streams(identifiers="foo", is_collection_prefix=True)
        <btrdb.stream.StreamSet at 0x...>

        If you set ``is_collection_prefix`` to ``False``, this will assume that the string identifier you provide is the full collection name.
        Matching like the regex here: ``^foo``

        >>> conn.streams(identifiers="foo", is_collection_prefix=False)
        <btrdb.stream.StreamSet at 0x...>

        """
        if versions is not None and not isinstance(versions, list):
            raise TypeError("versions argument must be of type list")

        if versions and len(versions) != len(identifiers):
            raise ValueError("number of versions does not match identifiers")
        streams: List[Stream] = []
        for ident in identifiers:
            if isinstance(ident, uuidlib.UUID):
                streams.append(self.stream_from_uuid(ident))
                continue

            if isinstance(ident, str):
                # attempt UUID lookup
                pattern = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"
                if re.match(pattern, ident):
                    streams.append(self.stream_from_uuid(ident))
                    continue

                # attempt collection/name lookup
                if "/" in ident:
                    parts = ident.split("/")
                    found = self.streams_in_collection(
                        "/".join(parts[:-1]),
                        is_collection_prefix=is_collection_prefix,
                        tags={"name": parts[-1]},
                    )
                    if isinstance(found, Stream):
                        streams.append(found)
                        continue
                    if isinstance(found, list) and len(found) == 1:
                        streams.append(found[0])
                        continue
                    raise StreamNotFoundError(f"Could not identify stream `{ident}`")

            raise ValueError(
                f"Could not identify stream based on `{ident}`.  Identifier must be UUID or collection/name."
            )

        obj = StreamSet(streams)

        if versions:
            version_dict = {
                streams[idx].uuid: versions[idx] for idx in range(len(versions))
            }
            obj.pin_versions(version_dict)

        return obj

    def stream_from_uuid(self, uuid):
        """
        Creates a stream handle to the BTrDB stream with the UUID `uuid`. This
        method does not check whether a stream with the specified UUID exists.
        It is always good form to check whether the stream existed using
        `stream.exists()`.


        Parameters
        ----------
        uuid : UUID
            The uuid of the requested stream.

        Returns
        -------
        Stream
            instance of Stream class or None

        Examples
        --------

        >>> import btrdb
        >>> conn = btrdb.connect()
        >>> uuid = "f98f4b4e-9fab-46b5-8a80-f282059d69b1"
        >>> stream = conn.stream_from_uuid(uuid)
        >>> stream
        <Stream collection=foo/test name=test_stream>

        """
        return Stream(self, to_uuid(uuid))

    @retry
    def create(
        self,
        uuid,
        collection,
        tags=None,
        annotations=None,
        auto_retry=False,
        retries=5,
        retry_delay=3,
        retry_backoff=4,
    ):
        """
        Tells BTrDB to create a new stream with UUID `uuid` in `collection` with specified `tags` and `annotations`.

        Parameters
        ----------
        uuid : UUID, required
            The uuid of the requested stream.
        collection : str, required
            The collection string prefix that the stream will belong to.
        tags : dict, required
            The tags-level metadata key:value pairs.
        annotations : dict, optional
            The mutable metadata of the stream, key:value pairs
        auto_retry : bool, default: False
            Whether to retry this request in the event of an error
        retries : int, default: 5
            Number of times to retry this request if there is an error. Will
            be ignored if auto_retry is False
        retry_delay : int, default: 3
            initial time to wait before retrying function call if there is an error.
            Will be ignored if auto_retry is False
        retry_backoff : int, default: 4
            Exponential factor by which the backoff increases between retries.
            Will be ignored if auto_retry is False

        Returns
        -------
        Stream
            instance of Stream class


        Examples
        --------
        >>> import btrdb
        >>> from uuid import uuid4 # this generates a random uuid
        >>> conn = btrdb.connect()
        >>> collection = "new/stream/collection"
        >>> tags = {"name":"foo", "unit":"V"}
        >>> annotations = {"bar": "baz"}
        >>> s = conn.create(uuid=uuid4(), tags=tags, annotations=annotations, collection=collection)
        <Stream collection=new/stream/collection name=foo>
        """

        if tags is None:
            tags = {}

        if annotations is None:
            annotations = {}

        self.ep.create(uuid, collection, tags, annotations)
        return Stream(
            self,
            uuid,
            known_to_exist=True,
            collection=collection,
            tags=tags.copy(),
            annotations=annotations.copy(),
            property_version=1,
        )

    def info(self):
        """
        Returns information about the platform proxy server.

        Returns
        -------
        dict
            Proxy server connection and status information

        Examples
        --------
        >>> conn = btrdb.connect()
        >>> conn.info()
        {
        ..        'majorVersion': 5,
        ..        'minorVersion': 8,
        ..        'build': ...,
        ..        'proxy': ...,
        }

        """
        info = self.ep.info()
        return {
            "majorVersion": info.majorVersion,
            "minorVersion": info.minorVersion,
            "build": info.build,
            "proxy": {"proxyEndpoints": [ep for ep in info.proxy.proxyEndpoints]},
        }

    def list_collections(self, starts_with=""):
        """
        Returns a list of collection paths using the `starts_with` argument for
        filtering.

        Parameters
        ----------
        starts_with : str, optional, default: ''
            Filter collections that start with the string provided, if none passed, will list all collections.

        Returns
        -------
        collections: List[str]

        Examples
        --------

        Assuming we have the following collections in the platform:
        ``foo``, ``bar``, ``foo/baz``, ``bar/baz``

        >>> conn = btrdb.connect()
        >>> conn.list_collections().sort()
        ["bar", "bar/baz", "foo", "foo/bar"]

        >>> conn.list_collections(starts_with="foo")
        ["foo", "foo/bar"]


        """
        return [c for some in self.ep.listCollections(starts_with) for c in some]

    def _list_unique_tags_annotations(self, key, collection):
        """
        Returns a SQL statement and parameters to get list of tags or annotations.
        """
        if key == "annotations":
            query = "select distinct({}) as {} from streams".format(
                "skeys(annotations)", "annotations"
            )
        else:
            query = "select distinct({}) as {} from streams".format(key, key)
        params = []
        if isinstance(collection, str):
            params.append("{}%".format(collection))
            query = " where ".join([query, """collection like $1"""])
        return [metadata[key] for metadata in self.query(query, params)]

    def list_unique_annotations(self, collection=None):
        """
        Returns a list of annotation keys used in a given collection prefix.

        Parameters
        ----------
        collection : str
            Prefix of the collection to filter.

        Returns
        -------
        annotations : list[str]

        Notes
        -----
        This query treats the ``collection`` string as a prefix, so ``collection="foo"`` will match with the following wildcard syntax ``foo%``.
        If you only want to filter for a single collection, you will need to provide the full collection, if there are other collections
        that match the ``foo%`` pattern, you might need to use a custom SQL query using ``conn.query``.

        Examples
        --------
        >>> conn.list_unique_annotations(collection="sunshine/PMU1")
        ['foo', 'location', 'impedance']

        """
        return self._list_unique_tags_annotations("annotations", collection)

    def list_unique_names(self, collection=None):
        """
        Returns a list of names used in a given collection prefix.

        Parameters
        ----------
        collection : str
            Prefix of the collection to filter.

        Returns
        -------
        names : list[str]

        Examples
        --------
        Can specify a full ``collection`` name.

        >>> conn.list_unique_names(collection="sunshine/PMU1")
        ['C1ANG', 'C1MAG', 'C2ANG', 'C2MAG', 'C3ANG', 'C3MAG', 'L1ANG', 'L1MAG', 'L2ANG', 'L2MAG', 'L3ANG', 'L3MAG', 'LSTATE']

        And also provide a ``collection`` prefix.

        >>> conn.list_unique_names(collection="sunshine/")
        ['C1ANG', 'C1MAG', 'C2ANG', 'C2MAG', 'C3ANG', 'C3MAG', 'L1ANG', 'L1MAG', 'L2ANG', 'L2MAG', 'L3ANG', 'L3MAG', 'LSTATE']



        """
        return self._list_unique_tags_annotations("name", collection)

    def list_unique_units(self, collection=None):
        """
        Returns a list of units used in a given collection prefix.

        Parameters
        ----------
        collection : str
            Prefix of the collection to filter.

        Returns
        -------
        units : list[str]


        Examples
        --------

        >>> conn.list_unique_units(collection="sunshine/PMU1")
        ['amps', 'deg', 'mask', 'volts']

        """
        return self._list_unique_tags_annotations("unit", collection)

    @retry
    def streams_in_collection(
        self,
        *collection,
        is_collection_prefix=True,
        tags=None,
        annotations=None,
        auto_retry=False,
        retries=5,
        retry_delay=3,
        retry_backoff=4,
    ):
        """
        Search for streams matching given parameters

        This function allows for searching

        Parameters
        ----------
        collection : str
            collections to use when searching for streams, case sensitive.
        is_collection_prefix : bool
            Whether the collection is a prefix.
        tags : Dict[str, str]
            The tags to identify the stream.
        annotations : Dict[str, str]
            The annotations to identify the stream.
        auto_retry : bool, default: False
            Whether to retry this request in the event of an error
        retries : int, default: 5
            Number of times to retry this request if there is an error. Will
            be ignored if auto_retry is False
        retry_delay : int, default: 3
            initial time to wait before retrying function call if there is an error.
            Will be ignored if auto_retry is False
        retry_backoff : int, default: 4
            Exponential factor by which the backoff increases between retries.
            Will be ignored if auto_retry is False

        Returns
        ------
        list[Stream]
            A list of ``Stream`` objects found with the provided search arguments.


        .. note::

            In a future release, the default return value of this function will be a ``StreamSet``

        Examples
        --------

        >>> conn = btrdb.connect()
        >>> conn.streams_in_collection(collection="foo", is_collection_prefix=True)
        [<Stream collection=foo name=test1>, <Stream collection=foo name=test2,
        ... <Stream collection=foo/bar, name=testX>, <Stream collection=foo/baz/bar name=testY>]

        >>> conn.streams_in_collection(collection="foo", is_collection_prefix=False)
        [<Stream collection=foo, name=test1>, <Stream collection=foo, name=test2>]

        >>> conn.streams_in_collection(collection="foo",
        ...  is_collection_prefix=False, tags={"unit":"Volts"})
        [<Stream collection=foo, name=test1>]

        >>> conn.streams_in_collection(collection="foo",
        ...  is_collection_prefix=False, tags={"unit":"UNKNOWN"})
        []
        """
        result = []

        if tags is None:
            tags = {}

        if annotations is None:
            annotations = {}

        if not collection:
            collection = [None]

        for item in collection:
            streams = self.ep.lookupStreams(
                item, is_collection_prefix, tags, annotations
            )
            for desclist in streams:
                for desc in desclist:
                    tagsanns = unpack_stream_descriptor(desc)
                    result.append(
                        Stream(
                            self,
                            uuidlib.UUID(bytes=desc.uuid),
                            known_to_exist=True,
                            collection=desc.collection,
                            tags=tagsanns[0],
                            annotations=tagsanns[1],
                            property_version=desc.propertyVersion,
                        )
                    )
        # TODO: In future release update this method to return a streamset object.
        warn(
            "StreamSet will be the default return object for ``streams_in_collection`` in a future release.",
            FutureWarning,
            stacklevel=2,
        )
        return result

    @retry
    def collection_metadata(
        self,
        prefix,
        auto_retry=False,
        retries=5,
        retry_delay=3,
        retry_backoff=4,
    ):
        """
        Gives statistics about metadata for collections that match a
        ``prefix``.

        Parameters
        ----------
        prefix : str, required
            A prefix of the collection names to look at
        auto_retry : bool, default: False
            Whether to retry this request in the event of an error
        retries : int, default: 5
            Number of times to retry this request if there is an error. Will
            be ignored if auto_retry is False
        retry_delay : int, default: 3
            initial time to wait before retrying function call if there is an error.
            Will be ignored if auto_retry is False
        retry_backoff : int, default: 4
            Exponential factor by which the backoff increases between retries.
            Will be ignored if auto_retry is False

        Returns
        -------
        tuple
            A tuple of dictionaries containing metadata on the streams in the
            provided collection.

        Examples
        --------
        >>> conn.collection_metadata("sunshine/PMU1")
        ({'name': 0, 'unit': 0, 'ingress': 0, 'distiller': 0},
        .. {'foo': 1, 'impedance': 12, 'location': 12})

        >>> conn.collection_metadata("sunshine/")
        ({'name': 0, 'unit': 0, 'ingress': 0, 'distiller': 0},
        .. {'foo': 1, 'impedance': 72, 'location': 72})

        """
        ep = self.ep
        tags, annotations = ep.getMetadataUsage(prefix)
        pyTags = {tag.key: tag.count for tag in tags}
        pyAnn = {ann.key: ann.count for ann in annotations}
        return pyTags, pyAnn

    def __reduce__(self):
        raise InvalidOperation("BTrDB object cannot be reduced.")
