from __future__ import annotations

from typing import Optional

from requests import HTTPError

from pycarlo.common import get_logger
from pycarlo.common.errors import InvalidSessionError
from pycarlo.core import Client
from pycarlo.features.ingestion.etl import (
    EtlAsset,
    EtlRunEvent,
    build_etl_metadata_payload,
    build_etl_runs_payload,
)
from pycarlo.features.ingestion.exceptions import IngestionError
from pycarlo.features.ingestion.models import (
    LineageEvent,
    LineageEventType,
    QueryLogEntry,
    RelationalAsset,
    build_lineage_payload,
    build_metadata_payload,
    build_query_log_payload,
)

logger = get_logger(__name__)

_METADATA_PATH = "/ingest/v1/metadata"
_LINEAGE_PATH = "/ingest/v1/lineage"
_QUERY_LOG_PATH = "/ingest/v1/querylogs"
_ETL_METADATA_PATH = "/ingest/v1/etl/metadata"
_ETL_RUNS_PATH = "/ingest/v1/etl/runs"


class IngestionService:
    """
    Send observability data to Monte Carlo via the Ingest API.

    The ``Client`` used to initialise this service **must** be created with a
    ``Session`` that has ``scope="Ingestion"`` and credentials for an
    integration key with the *Ingestion* scope.

    Example::

        from pycarlo.core import Client, Session
        from pycarlo.features.ingestion import IngestionService
        from pycarlo.features.ingestion.models import (
            RelationalAsset, AssetMetadata, AssetField,
        )

        client = Client(session=Session(
            mcd_id="<key-id>",
            mcd_token="<key-token>",
            scope="Ingestion",
        ))
        svc = IngestionService(mc_client=client)

        svc.send_metadata(
            resource_uuid="<uuid>",
            resource_type="snowflake",
            events=[
                RelationalAsset(
                    type="TABLE",
                    metadata=AssetMetadata(
                        name="orders",
                        database="analytics",
                        schema="public",
                    ),
                ),
            ],
        )
    """

    def __init__(self, mc_client: Optional[Client] = None):
        """
        :param mc_client: A ``Client`` whose session has ``scope`` set
            (e.g. ``"Ingestion"``).  If omitted a default ``Client()`` is
            created, but it will fail at request time unless the default
            session already carries a scope.
        """
        self._client = mc_client or Client()
        if not self._client.session_scope:
            raise InvalidSessionError(
                "IngestionService requires a Client with scope set "
                '(e.g. Session(scope="Ingestion")).'
            )

    def send_metadata(
        self,
        resource_uuid: str,
        resource_type: str,
        events: list[RelationalAsset],
    ) -> dict | None:
        """
        Send relational-asset metadata to Monte Carlo.

        :param resource_uuid: UUID of the Monte Carlo resource (warehouse/lake).
        :param resource_type: Resource type identifier, e.g. ``"snowflake"``,
            ``"bigquery"`` (lowercase).
        :param events: One or more :class:`RelationalAsset` objects describing
            the tables/views to ingest.
        :return: The JSON response from the API, or ``None`` if the response
            body was empty.
        :raises IngestionError: If the API returns an HTTP error.
        """
        if not events:
            raise ValueError("At least one RelationalAsset event is required.")

        payload = build_metadata_payload(
            resource_uuid=resource_uuid,
            resource_type=resource_type,
            events=events,
        )
        return self._post_metadata(payload)

    @staticmethod
    def extract_invocation_id(response: dict | None) -> str | None:
        """
        Extract the invocation ID returned by the ingest API.

        The Integration Gateway returns ``{"invocation_id": "<uuid>"}`` for
        successful ingest metadata, query-log, and lineage requests. This helper keeps SDK
        callers from needing to reach into the raw response payload directly.

        :param response: The JSON response returned by one of the public send
            methods on this service.
        :return: The invocation ID when present, otherwise ``None``.
        """
        if not isinstance(response, dict):
            return None

        invocation_id = response.get("invocation_id")
        return invocation_id if isinstance(invocation_id, str) else None

    def send_metadata_raw(self, payload: dict) -> dict | None:
        """
        Send a raw metadata payload dictionary to the ingest API.

        Use this when you already have a pre-built payload that conforms to the
        ``POST /ingest/v1/metadata`` schema.

        :param payload: The full request body as a dictionary.
        :return: The JSON response from the API, or ``None``.
        :raises IngestionError: If the API returns an HTTP error.
        """
        return self._post_metadata(payload)

    # ------------------------------------------------------------------
    # Lineage
    # ------------------------------------------------------------------

    def send_lineage(
        self,
        resource_uuid: str | None = None,
        resource_type: str | None = None,
        events: list[LineageEvent] | None = None,
        event_type: LineageEventType | str | None = None,
    ) -> dict | None:
        """
        Send lineage data to Monte Carlo.

        :param resource_uuid: UUID of the Monte Carlo resource (warehouse/lake)
            for same-warehouse lineage. Omit it for **cross-warehouse** lineage,
            in which case every :class:`LineageAssetRef` must carry its own
            ``resource_uuid`` / ``resource_type`` instead.
        :param resource_type: Resource type identifier, e.g. ``"snowflake"``,
            ``"bigquery"`` (lowercase). Provide alongside ``resource_uuid``.
        :param events: One or more :class:`LineageEvent` objects describing
            the data-flow relationships to ingest.
        :param event_type: Explicit event type (``"LINEAGE"`` or
            ``"COLUMN_LINEAGE"``).  When *None* the type is auto-detected:
            ``"COLUMN_LINEAGE"`` if any event contains ``fields``, otherwise
            ``"LINEAGE"``.
        :return: The JSON response from the API, or ``None`` if the response
            body was empty.
        :raises IngestionError: If the API returns an HTTP error.
        """
        if not events:
            raise ValueError("At least one LineageEvent is required.")

        payload = build_lineage_payload(
            resource_uuid=resource_uuid,
            resource_type=resource_type,
            events=events,
            event_type=event_type,
        )
        return self._post_lineage(payload)

    def send_lineage_raw(self, payload: dict) -> dict | None:
        """
        Send a raw lineage payload dictionary to the ingest API.

        Use this when you already have a pre-built payload that conforms to the
        ``POST /ingest/v1/lineage`` schema.

        :param payload: The full request body as a dictionary.
        :return: The JSON response from the API, or ``None``.
        :raises IngestionError: If the API returns an HTTP error.
        """
        return self._post_lineage(payload)

    # ------------------------------------------------------------------
    # Query logs
    # ------------------------------------------------------------------

    def send_query_logs(
        self,
        resource_uuid: str,
        log_type: str,
        events: list[QueryLogEntry],
    ) -> dict | None:
        """
        Send query log events to Monte Carlo.

        :param resource_uuid: UUID of the Monte Carlo resource (warehouse/lake).
        :param log_type: The log/connection type, e.g. ``"snowflake"``,
            ``"bigquery"`` (lowercase). This is the customer-facing name for the
            internal connection/warehouse type used by the Monte Carlo pipeline.
        :param events: One or more :class:`QueryLogEntry` objects describing
            the queries to ingest.
        :return: The JSON response from the API, or ``None`` if the response
            body was empty.
        :raises IngestionError: If the API returns an HTTP error.
        """
        if not events:
            raise ValueError("At least one QueryLogEntry event is required.")

        payload = build_query_log_payload(
            resource_uuid=resource_uuid,
            log_type=log_type,
            events=events,
        )
        return self._post_query_logs(payload)

    def send_query_logs_raw(self, payload: dict) -> dict | None:
        """
        Send a raw query log payload dictionary to the ingest API.

        Use this when you already have a pre-built payload that conforms to the
        ``POST /ingest/v1/querylogs`` schema.

        :param payload: The full request body as a dictionary.
        :return: The JSON response from the API, or ``None``.
        :raises IngestionError: If the API returns an HTTP error.
        """
        return self._post_query_logs(payload)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _post_metadata(self, payload: dict) -> dict | None:
        return self._post(
            path=_METADATA_PATH,
            payload=payload,
            label="Metadata",
        )

    def _post_lineage(self, payload: dict) -> dict | None:
        return self._post(
            path=_LINEAGE_PATH,
            payload=payload,
            label="Lineage",
        )

    def _post(self, path: str, payload: dict, label: str) -> dict | None:
        try:
            return self._client.make_request(
                path=path,
                method="POST",
                body=payload,
            )
        except HTTPError as exc:
            response_body = ""
            if exc.response is not None:
                try:
                    response_body = exc.response.text[:500]
                except Exception:
                    pass
            raise IngestionError(
                f"{label} ingestion request failed: {exc}. Response: {response_body}"
            ) from exc

    def _post_query_logs(self, payload: dict) -> dict | None:
        return self._post(
            path=_QUERY_LOG_PATH,
            payload=payload,
            label="Query log",
        )

    # ------------------------------------------------------------------
    # ETL — metadata
    # ------------------------------------------------------------------

    def send_etl_metadata(
        self,
        resource_uuid: str,
        resource_type: str,
        events: list[EtlAsset],
    ) -> dict | None:
        """
        Send declarative ETL job/group definitions to Monte Carlo.

        Maps to ``POST /ingest/v1/etl/metadata``.

        :param resource_uuid: UUID of the Monte Carlo resource.
        :param resource_type: Resource type identifier, e.g. ``"airflow"``,
            ``"dbt"`` (lowercase).
        :param events: One or more :class:`EtlAsset` objects describing the
            ETL jobs to register. Batch size: 1–100.
        :return: The JSON response from the API, or ``None`` if the response
            body was empty.
        :raises IngestionError: If the API returns an HTTP error.
        :raises ValueError: If the batch is empty or exceeds 100 events.
        """
        payload = build_etl_metadata_payload(
            resource_uuid=resource_uuid,
            resource_type=resource_type,
            events=events,
        )
        return self._post_etl_metadata(payload)

    def send_etl_metadata_raw(self, payload: dict) -> dict | None:
        """
        Send a raw ETL metadata payload dictionary to the ingest API.

        Use this when you already have a pre-built payload that conforms to the
        ``POST /ingest/v1/etl/metadata`` schema.

        :param payload: The full request body as a dictionary.
        :return: The JSON response from the API, or ``None``.
        :raises IngestionError: If the API returns an HTTP error.
        :raises ValueError: If the payload fails shape or batch-size validation.
        """
        self._validate_etl_raw_payload(payload, expected_event_type="ETL_METADATA")
        return self._post_etl_metadata(payload)

    # ------------------------------------------------------------------
    # ETL — runs
    # ------------------------------------------------------------------

    def send_etl_runs(
        self,
        resource_uuid: str,
        resource_type: str,
        events: list[EtlRunEvent],
        event_time: Optional[str] = None,
    ) -> dict | None:
        """
        Send ETL run state-transition events to Monte Carlo.

        Maps to ``POST /ingest/v1/etl/runs``.

        :param resource_uuid: UUID of the Monte Carlo resource. Identifies the
            owning ETL container for every event in the batch.
        :param resource_type: Resource type identifier, e.g. ``"airflow"``,
            ``"dbt"`` (lowercase).
        :param events: One or more :class:`EtlRunEvent` objects. Batch size:
            1–100.
        :param event_time: Optional batch-level ISO8601 timestamp.
        :return: The JSON response from the API, or ``None`` if the response
            body was empty.
        :raises IngestionError: If the API returns an HTTP error.
        :raises ValueError: If the batch is empty or exceeds 100 events.
        """
        payload = build_etl_runs_payload(
            resource_uuid=resource_uuid,
            resource_type=resource_type,
            events=events,
            event_time=event_time,
        )
        return self._post_etl_runs(payload)

    def send_etl_runs_raw(self, payload: dict) -> dict | None:
        """
        Send a raw ETL runs payload dictionary to the ingest API.

        Use this when you already have a pre-built payload that conforms to the
        ``POST /ingest/v1/etl/runs`` schema.

        :param payload: The full request body as a dictionary.
        :return: The JSON response from the API, or ``None``.
        :raises IngestionError: If the API returns an HTTP error.
        :raises ValueError: If the payload fails shape or batch-size validation.
        """
        self._validate_etl_raw_payload(payload, expected_event_type="ETLRUN")
        return self._post_etl_runs(payload)

    @staticmethod
    def _validate_etl_raw_payload(payload: dict, expected_event_type: str) -> None:
        """
        Validate the shape of a raw ETL payload before posting.

        :param payload: The raw payload dict to validate.
        :param expected_event_type: The ``event_type`` value the payload must
            carry (e.g. ``"ETL_METADATA"`` or ``"ETLRUN"``).
        :raises ValueError: If the payload fails any validation check.
        """
        if not isinstance(payload, dict):
            raise ValueError(f"payload must be a dict, got {type(payload).__name__!r}.")

        actual_event_type = payload.get("event_type")
        if actual_event_type != expected_event_type:
            raise ValueError(
                f"payload['event_type'] must be {expected_event_type!r}, got {actual_event_type!r}."
            )

        resource = payload.get("resource")
        if not isinstance(resource, dict):
            raise ValueError(
                f"payload['resource'] must be a dict, got {type(resource).__name__!r}."
            )

        events = payload.get("events")
        if not isinstance(events, list):
            raise ValueError(f"payload['events'] must be a list, got {type(events).__name__!r}.")
        if not (1 <= len(events) <= 100):
            raise ValueError(
                f"payload['events'] must contain between 1 and 100 items, got {len(events)}."
            )

    def _post_etl_metadata(self, payload: dict) -> dict | None:
        return self._post(
            path=_ETL_METADATA_PATH,
            payload=payload,
            label="ETL metadata",
        )

    def _post_etl_runs(self, payload: dict) -> dict | None:
        return self._post(
            path=_ETL_RUNS_PATH,
            payload=payload,
            label="ETL runs",
        )
