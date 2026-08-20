import time
import typing as t

from loguru import logger
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from requests import Session

from dreadnode.core.tls import create_platform_http_session
from dreadnode.version import VERSION


class CustomOTLPSpanExporter(OTLPSpanExporter):
    """A custom OTLP exporter that injects our SDK version into the User-Agent."""

    _BILLING_WARNING_INTERVAL_SECONDS = 60.0

    def __init__(self, *, session: Session | None = None, **kwargs: t.Any) -> None:
        super().__init__(session=session or create_platform_http_session(), **kwargs)
        self._last_billing_warning_monotonic = 0.0

        otlp_user_agent = self._session.headers.get("User-Agent")
        if isinstance(otlp_user_agent, bytes):
            otlp_user_agent = otlp_user_agent.decode("utf-8")

        if otlp_user_agent:
            combined_user_agent = f"dreadnode/{VERSION} {otlp_user_agent}"
            self._session.headers["User-Agent"] = combined_user_agent
        else:
            # Fallback if somehow OTel didn't set a User-Agent
            self._session.headers["User-Agent"] = f"dreadnode/{VERSION}"

    def _export(self, serialized_data: bytes) -> t.Any:
        """Export serialized spans and warn clearly on billing-related 429s."""
        response = super()._export(serialized_data)

        if response.status_code == 429:
            detail = self._extract_detail_from_response(response)
            message = (
                detail or "Insufficient credits for span ingestion — purchase credits to continue"
            )

            if self._should_emit_billing_warning():
                logger.warning(message)

        return response

    def _should_emit_billing_warning(self) -> bool:
        now = time.monotonic()
        if now - self._last_billing_warning_monotonic < self._BILLING_WARNING_INTERVAL_SECONDS:
            return False
        self._last_billing_warning_monotonic = now
        return True

    @staticmethod
    def _extract_detail_from_response(response: t.Any) -> str | None:
        try:
            payload = response.json()
        except Exception:
            return None

        if isinstance(payload, dict):
            detail = payload.get("detail")
            if detail is None:
                return None
            if isinstance(detail, str):
                return detail
            return str(detail)
        return None
