#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2025.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import logging
import json
from functools import reduce
from concurrent.futures import ThreadPoolExecutor
from typing import Optional, Iterable, Any

import pandas as pd

from ibm_watsonx_ai import APIClient

from .utils.flight_utils import (
    SimplyCallback,
    CallbackSchema,
    HeaderMiddlewareFactory,
    _flight_retry,
)

from pyarrow import flight

logger = logging.getLogger(__name__)


class FlightSQLClient:
    """FlightSQLClient object unify the work for data reading from different types of data sources,
    including databases. It uses a Flight Service and `pyarrow` library to connect and transfer the data.

    :param connection_id: ID of db connection asset
    :type connection_id: str

    :param api_client: initialized APIClient object.
    :type api_client: APIClient

    :param project_id: ID of project
    :type project_id: str, optional

    :param space_id: ID of space
    :type space_id: str, optional

    :param callback: required for sending messages
    :type callback: StatusCallback, optional

    :param flight_parameters: pure unchanged flight service parameters that need to be passed to the service
    :type flight_parameters: dict, optional

    :param extra_interaction_properties: extra interaction properties passed in flight params
    :type extra_interaction_properties: dict, optional

    :param max_retry_time: maximal time for retrying in seconds (the whole retrying process should take less than max_retry_time)
    :type max_retry_time: int, optional

    """

    def __init__(
        self,
        connection_id: str,
        api_client: APIClient,
        space_id: Optional[str] = None,
        project_id: Optional[str] = None,
        callback: Optional[CallbackSchema] = None,
        flight_parameters: Optional[dict] = None,
        extra_interaction_properties: Optional[dict] = None,
        max_retry_time: int = 200,
    ) -> None:

        # callback is used in the backend to send status messages
        self.callback = (
            callback if callback is not None else SimplyCallback(logger=logger)
        )
        self._max_retry_time = max_retry_time

        self.connection_id = connection_id

        self.flight_parameters = (
            flight_parameters if flight_parameters is not None else {}
        )

        if space_id is None and project_id is None:
            raise ValueError("Either space_id or project_id is required.")

        self._api_client = api_client

        self.additional_connection_args = {}
        if os.environ.get("TLS_ROOT_CERTS_PATH"):
            self.additional_connection_args["tls_root_certs"] = os.environ.get(
                "TLS_ROOT_CERTS_PATH"
            )

        self.extra_interaction_properties = extra_interaction_properties

        # Set flight location and port
        self.flight_location = None
        self.flight_port = None
        self._set_default_flight_location()

        self._base_command = {}

        if space_id is not None:
            self._base_command["space_id"] = space_id
        else:
            self._base_command["project_id"] = project_id

        self._base_command["asset_id"] = self.connection_id

        # Need in external retry
        self._logger = logger

    @property
    def _flight_client(self) -> flight.FlightClient:
        return flight.FlightClient(
            location=f"grpc+tls://{self.flight_location}:{self.flight_port}",
            disable_server_verification=True,
            override_hostname=self.flight_location,
            middleware=[
                HeaderMiddlewareFactory(headers=self._api_client.get_headers())
            ],
            **self.additional_connection_args,
        )

    def _set_default_flight_location(self) -> None:
        """Try to set default flight location and port from WS."""
        if (
            not os.environ.get("FLIGHT_SERVICE_LOCATION")
            and self._api_client
            and self._api_client.CLOUD_PLATFORM_SPACES
        ):
            try:
                flight_location = self._api_client.PLATFORM_URLS_MAP[
                    self._api_client.credentials.url
                ].replace("https://", "")
            except KeyError as e:
                if (
                    self._api_client.credentials.url
                    in self._api_client.PLATFORM_URLS_MAP.values()
                ):
                    flight_location = self._api_client.credentials.url.replace(
                        "https://", ""
                    )
                else:
                    raise e
            flight_port = 443
        else:
            host = os.environ.get(
                "ASSET_API_SERVICE_HOST", os.environ.get("CATALOG_API_SERVICE_HOST")
            )

            if host is None or "api." not in host:
                default_service_url = os.environ.get(
                    "RUNTIME_FLIGHT_SERVICE_URL", "grpc+tls://wdp-connect-flight:443"
                )
                default_service_url = default_service_url.split("//")[-1]
                flight_location = os.environ.get("FLIGHT_SERVICE_LOCATION")
                flight_port = os.environ.get("FLIGHT_SERVICE_PORT")

                if flight_location is None or flight_location == "":
                    flight_location = default_service_url.split(":")[0]
                elif flight_location.startswith("https://"):
                    flight_location = flight_location.replace("https://", "")

                if flight_port is None or flight_port == "":
                    flight_port = default_service_url.split(":")[-1]

            else:
                flight_location = host
                flight_port = "443"

        self.flight_location = flight_location
        self.flight_port = flight_port

        logger.debug(f"Flight location: {self.flight_location}")
        logger.debug(f"Flight port: {self.flight_port}")

    def _get_source_command(
        self, select_statement: str | None = None, **kwargs: Any
    ) -> str:
        """Get source command for flight service."""

        command = self._base_command.copy()

        if self.flight_parameters is not None:
            command |= self.flight_parameters

        if self.extra_interaction_properties is not None:
            command["interaction_properties"] = self.extra_interaction_properties

        if select_statement is not None:
            if command.get("interaction_properties") is None:
                command["interaction_properties"] = {
                    "select_statement": select_statement
                }
            else:
                command["interaction_properties"]["select_statement"] = select_statement

        for key, value in kwargs.items():
            command[key] = value

        return json.dumps(command)

    @_flight_retry()
    def _get_endpoints(
        self, select_statement: str | None = None
    ) -> Iterable["flight.FlightEndpoint"]:
        """Listing all available Flight Service endpoints (one endpoint corresponds to one batch)"""
        source_command = self._get_source_command(select_statement=select_statement)

        with self._flight_client as flight_client:
            info = flight_client.get_flight_info(
                flight.FlightDescriptor.for_command(source_command)
            )
            return info.endpoints

    @_flight_retry()
    def execute(self, query: str) -> pd.DataFrame:
        """Execute a query on the data source.

        :param query: query to execute
        :type query: str

        :return: query result
        :rtype: str
        """

        endpoints = self._get_endpoints(select_statement=query)

        def read_thread(
            flight_client: flight.FlightClient, endpoint: flight.FlightEndpoint
        ) -> pd.DataFrame:
            reader = flight_client.do_get(endpoint.ticket)
            return reader.read_pandas()

        with self._flight_client as flight_client:
            # Limit max concurrent threads to 10
            with ThreadPoolExecutor(max_workers=10) as executor:
                df_list = list(
                    executor.map(
                        read_thread, [flight_client] * len(endpoints), endpoints
                    )
                )

        return pd.concat(df_list)

    @_flight_retry()
    def get_tables(self, schema: str) -> list[dict]:
        """Get list of tables in the schema.

        :param schema: Schema name
        :type schema: str

        :return: List of tables in the schema
        :rtype: list[dict]
        """
        tables = []
        additional_params = {
            "path": f"/{schema}",
            "discovery_filters": {
                "include_system": "false",
                "include_table": "true",
                "include_view": "true",
            },
            "context": "source",
        }

        command = self._get_source_command(**additional_params)
        action = flight.Action("discovery", command.encode("utf-8"))

        with self._flight_client as flight_client:
            action_res = flight_client.do_action(action)
            # Retrieve first chunk to read a schema
            first_chunk = json.loads(next(action_res).body.to_pybytes())
            tables = reduce(
                lambda left_chunk, right_chunk: self._reduce_discovery_chunks(
                    left_chunk,
                    json.loads(right_chunk.body.to_pybytes()),
                    reduce_fields=["assets", "total_count"],
                ),
                action_res,
                first_chunk,
            )

        return tables

    @_flight_retry()
    def get_table_info(self, schema: str, table_name: str, **kwargs: Any) -> dict:
        """Get info about table from given schema."""

        extended_metadata = kwargs.get("extended_metadata", False)
        interaction_properties = kwargs.get("interaction_properties", False)

        fetch = "metadata"
        if extended_metadata:
            fetch += ",extended_metadata"
        if interaction_properties:
            fetch += ",interaction"

        additional_params = {
            "path": f"/{schema}/{table_name}",
            "detail": "true",
            "fetch": fetch,
            "context": "source",
        }

        command = self._get_source_command(**additional_params)
        action = flight.Action("discovery", command.encode("utf-8"))

        with self._flight_client as flight_client:
            action_res = flight_client.do_action(action)
            table_info_raw = next(action_res)
            table_info = json.loads(table_info_raw.body.to_pybytes())

        return table_info

    @_flight_retry()
    def get_schemas(self) -> list[dict]:
        """Get list of schemas.

        :return: List of schemas
        :rtype: list[dict]
        """

        schemas = []
        additional_params = {"path": "/", "detail": "true", "context": "source"}

        command = self._get_source_command(**additional_params)
        action = flight.Action("discovery", command.encode("utf-8"))

        with self._flight_client as flight_client:
            action_res = flight_client.do_action(action)

            # Retrieve first chunk to read a schema
            first_chunk = json.loads(next(action_res).body.to_pybytes())
            schemas = reduce(
                lambda left_chunk, right_chunk: self._reduce_discovery_chunks(
                    left_chunk,
                    json.loads(right_chunk.body.to_pybytes()),
                    reduce_fields=["assets", "totalCount"],
                ),
                action_res,
                first_chunk,
            )

        return schemas

    def _reduce_discovery_chunks(
        self, left_chunk, right_chunk, reduce_fields: list[str]
    ):
        for field in reduce_fields:
            if field in right_chunk and field in left_chunk:
                left_chunk[field] += right_chunk[field]

        return left_chunk
