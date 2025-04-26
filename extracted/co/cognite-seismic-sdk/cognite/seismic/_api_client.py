# Copyright 2019 Cognite AS
import logging
import os
import time
from collections import namedtuple

import certifi
import grpc
from cognite.seismic._api.utility import _backoffs
from cognite.seismic._interceptors import (
    ApiKeyAuth,
    BearerTokenAuth,
    UnaryStreamMetadataInterceptor,
    UnaryUnaryMetadataInterceptor,
)
from grpc import UnaryStreamMultiCallable, UnaryUnaryMultiCallable

if not os.getenv("READ_THE_DOCS"):
    from cognite.seismic._api.file import FileAPI
    from cognite.seismic._api.job import JobAPI
    from cognite.seismic._api.partition import PartitionAPI
    from cognite.seismic._api.seismics import SeismicAPI
    from cognite.seismic._api.seismicstores import SeismicStoreAPI
    from cognite.seismic._api.survey import SurveyAPI
    from cognite.seismic._api.traces import TracesAPI
    from cognite.seismic.data_classes.errors import SeismicServiceError, _from_grpc_error
    from cognite.seismic.protos import ingest_service_pb2_grpc as ingest_serv
    from cognite.seismic.protos import query_service_pb2_grpc as query_serv
    from cognite.seismic.protos.v1 import seismic_service_pb2_grpc as seismic_serv

# The maximum number of call attempts including both the initial call and any retries
_MAX_ATTEMPTS_BY_CODE = {
    grpc.StatusCode.ABORTED: 3,
    grpc.StatusCode.UNAVAILABLE: 5,
    grpc.StatusCode.DEADLINE_EXCEEDED: 5,
}

logger = logging.getLogger(__name__)


def with_retry(f, transactional=False):
    def wraps(*args, **kwargs):
        for attempts, backoff in enumerate(_backoffs()):
            try:
                return f(*args, **kwargs)
            except grpc.RpcError as e:
                code = e.code()

                max_attempts = _MAX_ATTEMPTS_BY_CODE.get(code)
                if max_attempts is None or transactional and code == grpc.StatusCode.ABORTED:
                    raise _from_grpc_error(e)

                if attempts > max_attempts:
                    seismic_error = SeismicServiceError()
                    seismic_error.status = grpc.StatusCode.UNAVAILABLE
                    seismic_error.message = "maximum number of retries exceeded"
                    seismic_error.source = e
                    raise seismic_error

                logger.info("sleeping %r for %r before retrying failed request...", backoff, code)

                time.sleep(backoff)

    return wraps


def decorate_with_retries(*args):
    for obj in args:
        for key, attr in obj.__dict__.items():
            if isinstance(attr, UnaryUnaryMultiCallable):
                setattr(obj, key, with_retry(attr))


class _WrappedStream:
    def __init__(self, stream):
        self.stream = stream

    def __next__(self):
        try:
            return next(self.stream)
        except grpc.RpcError as e:
            raise _from_grpc_error(e) from None

    def __iter__(self):
        return self

    def initial_metadata(self):
        return self.stream.initial_metadata()


def with_wrapped_rpc_errors(f):
    if isinstance(f, UnaryUnaryMultiCallable):

        def wraps(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except grpc.RpcError as e:
                raise _from_grpc_error(e) from None

        return wraps
    elif isinstance(f, UnaryStreamMultiCallable):

        def wraps(*args, **kwargs):
            return _WrappedStream(f(*args, **kwargs))

        return wraps
    else:
        return f


def decorate_with_wrapped_rpc_errors(*args):
    for obj in args:
        for key, attr in obj.__dict__.items():
            setattr(obj, key, with_wrapped_rpc_errors(attr))


ParsedUrl = namedtuple("ParsedUrl", "is_insecure target")


def parse_url_parameter(url) -> ParsedUrl:
    """Parse a provided url, setting the secure/insecure status and standardizing the URL with a port"""
    from urllib.parse import urlparse

    o = urlparse(url)
    # Urllib parsing quirk: if there's no schema, it parses the entire url as a path
    if o.netloc:
        netloc = o.netloc
    else:
        netloc = o.path

    scheme = o.scheme or "https"
    # We're removing any potential port that might exist, esp since it's also provided separately.
    # The rest of the URL (the path and params) are discarded
    base_url = netloc.split(":")[0] or "api.cognitedata.com"
    port = o.port or 443
    full_url = f"{base_url}:{port}"

    return ParsedUrl(scheme == "http", full_url)


class CogniteSeismicClient:
    """
    Main class for the seismic client.


    Args:
        api_key (str, optional): An API key. Equivalent to setting the :code:`COGNITE_API_KEY` environment variable.
        base_url (str, optional): The url to connect to. Defaults to :code:`api.cognitedata.com`.
        port (int, optional): The port to connect to. Defaults to 443.
        custom_root_cert (str, optional):
            A custom root certificate for SSL connections. Should not need to be used by general users.
        project (str): The name of the project to call API endpoints against.
        no_retries (bool): If true, will not automatically retry failed requests.
        max_message_size_MB (int): The max message size of gRPC replies. Defaults to 10.
        oidc_token (str | function() -> str, optional):
            If specified, will attempt to connect to the seismic service using an OIDC token.
            This should be either a string or a callable resolving to a string.
    """

    job: "JobAPI"
    survey: "SurveyAPI"
    traces: "TracesAPI"
    partition: "PartitionAPI"
    seismic: "SeismicAPI"
    seismicstore: "SeismicStoreAPI"
    file: "FileAPI"

    def __init__(
        self,
        api_key=None,
        base_url=None,
        custom_root_cert=None,
        *,
        project=None,
        no_retries=False,
        max_message_size_MB=10,
        oidc_token=None,
    ):
        # configure env
        self.api_key = api_key or os.getenv("COGNITE_API_KEY")
        self.project = project or os.getenv("COGNITE_PROJECT")

        if base_url is not None:
            parsed_url = parse_url_parameter(base_url)
            self.target = parsed_url.target
            self.is_insecure = parsed_url.is_insecure
        else:
            self.target = "api.cognitedata.com:443"
            self.is_insecure = False

        if self.project is None:
            raise ValueError(
                "CDF project name must be supplied. \
                Please set the project name with \
                CogniteSeismicClient(project='') or with an environment \
                variable COGNITE_PROJECT=''"
            )

        if custom_root_cert is None:
            root_certs = certifi.contents().encode()
        else:
            root_certs = custom_root_cert

        if callable(oidc_token):
            auth_plugin = BearerTokenAuth(self.project, oidc_token)
        elif oidc_token is not None:
            auth_plugin = BearerTokenAuth(self.project, lambda: oidc_token)
        elif self.api_key is not None and self.api_key != "":
            auth_plugin = ApiKeyAuth(self.project, self.api_key)
        else:
            raise ValueError(
                """
You must provide at least one of the following:
* An OIDC token (via the argument 'oidc_token')
* An API key (via the argument 'api_key')
* Set the COGNITE_API_KEY environment variable
            """
            )

        if max_message_size_MB > 10:
            logger.warning(
                "Raising the maximum message size above the default of 10MB may result in significant performance costs"
            )
        elif max_message_size_MB < 10:
            raise ValueError("Maximum message size must be at least 10MB")

        # start the connection
        options = [
            ("grpc.max_receive_message_length", max_message_size_MB * 1024 * 1024),
            ("grpc.keepalive_time_ms", 5000),
            ("grpc.keepalive_permit_without_calls", 1),
            ("grpc.http2.max_pings_without_data", 0),
            ("grpc.http2.min_time_between_pings_ms", 5000),
        ]
        if self.is_insecure:
            channel = grpc.insecure_channel(self.target, options=options)
        else:
            credentials = grpc.composite_channel_credentials(
                grpc.ssl_channel_credentials(root_certificates=root_certs), grpc.metadata_call_credentials(auth_plugin)
            )
            channel = grpc.secure_channel(self.target, credentials, options=options)
        channel = grpc.intercept_channel(channel, UnaryUnaryMetadataInterceptor(), UnaryStreamMetadataInterceptor())
        self.query = query_serv.QueryStub(channel)
        self.ingestion = ingest_serv.IngestStub(channel)
        self.seismicstub = seismic_serv.SeismicAPIStub(channel)

        if not no_retries:
            decorate_with_retries(self.query, self.ingestion, self.seismicstub)
        decorate_with_wrapped_rpc_errors(self.query, self.ingestion, self.seismicstub)

        self.job = JobAPI(self.seismicstub)
        self.survey = SurveyAPI(self.seismicstub)
        self.traces = TracesAPI(self.seismicstub, self.ingestion)
        self.partition = PartitionAPI(self.seismicstub, self.ingestion)
        self.seismic = SeismicAPI(self)
        self.seismicstore = SeismicStoreAPI(self)
        self.file = FileAPI(self.seismicstub, self.ingestion)
