from __future__ import annotations

from typing import Optional

from requests import HTTPError

from pycarlo.common import get_logger
from pycarlo.common.errors import InvalidSessionError
from pycarlo.core import Client
from pycarlo.features.ingestion.exceptions import IngestionError
from pycarlo.features.ingestion.models import RelationalAsset, build_metadata_payload

logger = get_logger(__name__)

_METADATA_PATH = "/ingest/v1/metadata"


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

    def _post_metadata(self, payload: dict) -> dict | None:
        try:
            return self._client.make_request(
                path=_METADATA_PATH,
                method="POST",
                body=payload,
            )
        except HTTPError as exc:
            response_body = ""
            if exc.response is not None:
                try:
                    response_body = exc.response.text
                except Exception:
                    pass
            raise IngestionError(
                f"Metadata ingestion request failed: {exc}. Response: {response_body}"
            ) from exc
