"""Base verifier class."""

from __future__ import annotations

import logging
from abc import abstractmethod
from typing import Any, ClassVar, Generic, TypeVar, get_args

from plato.chronos.sdk import AsyncChronos

from .config import VerifierConfig
from .models import SessionData, VerifierResult

logger = logging.getLogger(__name__)

ConfigT = TypeVar("ConfigT", bound=VerifierConfig)


class BaseVerifier(Generic[ConfigT]):
    """Base class for all verifiers.

    Subclasses must implement :meth:`verify` and can optionally override
    :meth:`reset` for setup logic.

    Usage::

        @register_verifier("my-verifier")
        class MyVerifier(BaseVerifier[MyConfig]):
            description = "Checks something"

            async def verify(self, session_data: SessionData) -> VerifierResult:
                ...
    """

    name: ClassVar[str] = ""
    description: ClassVar[str] = ""

    def __init__(self) -> None:
        self.config: ConfigT = None  # type: ignore[assignment]
        self._chronos: AsyncChronos | None = None
        self.world: Any = None  # BaseWorld instance, set by caller for agent/workspace access

    @classmethod
    def get_config_class(cls) -> type[ConfigT]:
        """Resolve the config type parameter from the class hierarchy."""
        for base in getattr(cls, "__orig_bases__", ()):
            args = get_args(base)
            if args and isinstance(args[0], type) and issubclass(args[0], VerifierConfig):
                return args[0]  # type: ignore[return-value]
        return VerifierConfig  # type: ignore[return-value]

    @abstractmethod
    async def verify(self) -> VerifierResult:
        """Run verification.

        Must return a :class:`VerifierResult` with an overall signal,
        summary, and zero or more findings.
        """
        ...

    async def run(self, config: ConfigT) -> VerifierResult:
        """Full lifecycle: fetch data -> reset -> verify -> publish.

        This is called by the runner CLI and orchestrates the entire
        verification flow.
        """
        self.config = config
        self._chronos = AsyncChronos(
            base_url=config.chronos_base_url,
            api_key=config.plato_api_key,
        )
        try:
            logger.info(
                "Verifier '%s' starting for session %s",
                self.name,
                config.session_id,
            )

            result = await self.verify()

            logger.info(
                "Verifier '%s' completed: signal=%s, %d findings",
                self.name,
                result.signal.value,
                len(result.findings),
            )

            await self._publish_results(result)
            return result
        except Exception:
            logger.exception("Verifier '%s' failed", self.name)
            raise
        finally:
            if self._chronos:
                await self._chronos.close()
                self._chronos = None

    async def _fetch_session_data(self) -> SessionData:
        """Fetch all relevant data for the target session from Chronos."""
        await self._ensure_chronos()
        assert self._chronos is not None
        cfg = self.config
        sid = cfg.session_id

        logger.info("Fetching session data for %s", sid)

        session = await self._chronos.get_session(sid)
        trajectory = await self._chronos.get_trajectory(sid)
        logs = await self._chronos.get_logs(sid)

        # Fetch existing annotations
        annotations: list[Any] = []
        try:
            resp = await self._chronos._client.request(
                method="GET",
                url="/api/annotations",
                params={"session_id": sid},
            )
            if resp.status_code == 200:
                data = resp.json()
                annotations = data.get("annotations", [])
        except Exception:
            logger.warning("Failed to fetch annotations for %s", sid, exc_info=True)

        result = None
        if hasattr(session, "result") and session.result:
            result = session.result if isinstance(session.result, dict) else {}

        logger.info(
            "Fetched: session=%s, trajectory agents=%d, annotations=%d",
            session.status,
            len(trajectory.agents or []),
            len(annotations),
        )

        return SessionData(
            session_id=sid,
            session=session,
            trajectory=trajectory,
            logs=logs,
            annotations=annotations,
            result=result,
        )

    async def _ensure_chronos(self) -> AsyncChronos:
        """Get or create the Chronos client."""
        if self._chronos is None:
            self._chronos = AsyncChronos(
                base_url=self.config.chronos_base_url,
                api_key=self.config.plato_api_key,
            )
        return self._chronos

    async def _publish_results(self, result: VerifierResult) -> None:
        """Publish verifier results as annotations on the target session."""
        await self._ensure_chronos()
        cfg = self.config
        verifier_sid = cfg.verifier_session_id or "unknown"

        review_id = cfg.review_id

        # Build review name: "Session Verifier (verifier_session → target_session)"
        review_name = f"Session Verifier ({verifier_sid[:8]} → {cfg.session_id[:8]})"

        # Common tags for all annotations
        base_tags = [
            "session_verifier",
            f"verifier.{self.name}",
            f"verifier_session.{verifier_sid}",
            *cfg.annotation_tags,
        ]

        # Create a review if none provided
        if not review_id:
            try:
                resp = await self._chronos._client.request(
                    method="POST",
                    url="/api/reviews",
                    json={
                        "session_id": cfg.session_id,
                        "name": review_name,
                        "description": f"{result.signal.value.upper()}: {result.summary}",
                        "tags": [*base_tags, f"signal.{result.signal.value}"],
                        "author_type": "agent",
                    },
                )
                resp.raise_for_status()
                review_id = resp.json()["public_id"]
                logger.info("Created review %s: %s", review_id, review_name)
            except Exception:
                logger.warning("Failed to create review, publishing annotations without review_id", exc_info=True)

        # Publish individual findings
        for finding in result.findings:
            content = f"{finding.title}\n{finding.description}" if finding.description else finding.title
            await self._create_annotation(
                review_id=review_id,
                content=content,
                tags=[*base_tags, *finding.tags],
                span_ids=finding.span_ids,
                signal=finding.signal.value,
                data=finding.data.model_dump() if finding.data else None,
            )

        logger.info(
            "Published %d annotations to session %s",
            len(result.findings),
            cfg.session_id,
        )

    async def _create_annotation(
        self,
        review_id: str | None,
        content: str,
        tags: list[str],
        span_ids: list[str],
        signal: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        """Create a single annotation on the target session."""
        assert self._chronos is not None
        targets = [{"type": "span", "span_id": sid} for sid in span_ids]
        body: dict[str, Any] = {
            "session_id": self.config.session_id,
            "kind": "observation",
            "content": content,
            "tags": tags,
            "targets": targets,
            "author_type": "agent",
        }
        if review_id:
            body["review_id"] = review_id
        if signal:
            body["signal"] = signal
        if data:
            body["data"] = data
        try:
            resp = await self._chronos._client.request(
                method="POST",
                url="/api/annotations",
                json=body,
            )
            resp.raise_for_status()
        except Exception:
            logger.warning("Failed to create annotation: %s", content[:80], exc_info=True)
