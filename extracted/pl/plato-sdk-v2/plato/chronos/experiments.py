"""High-level Chronos experiments client.

Provides a clean interface for managing experiment files, versions, and
launching sessions from experiments. Used by hillclimb and other automation
that needs to interact with the experiments system.
"""

from __future__ import annotations

import logging
from typing import Any

import httpx

from plato.chronos.api.experiments import (
    attach_session_to_experiment_version,
    create_experiment_file,
    create_experiment_file_version,
    detach_session_from_experiment_version,
    list_experiment_files,
    update_experiment_file,
)
from plato.chronos.api.jobs import launch_experiment
from plato.chronos.models import (
    ExperimentFileCreateRequest,
    ExperimentFileResponse,
    ExperimentFileUpdateRequest,
    ExperimentFileVersionCreateRequest,
    LaunchExperimentRequest,
    LaunchJobResponse,
    TargetReviewSpec,
)

logger = logging.getLogger(__name__)


class AsyncExperiments:
    """Async client for the Chronos experiments API.

    Usage::

        from plato.chronos.experiments import AsyncExperiments

        experiments = AsyncExperiments(base_url="https://chronos.plato.so", api_key="pk_...")

        # Create an experiment file
        file = await experiments.create_file(name="my-experiment", config_json={...})

        # Get an experiment file
        file = await experiments.get_file("file-public-id")

        # Get target reviews for an experiment
        reviews = await experiments.get_target_reviews("file-public-id")

        # Create a new version
        file = await experiments.create_version(
            file_id="file-public-id",
            config_json={...},
            notes="Updated config",
        )

        # Launch a session from an experiment version
        result = await experiments.launch(version_id="version-public-id")

        # Attach/detach sessions
        await experiments.attach_session(version_id="...", session_id="...")
        await experiments.detach_session(version_id="...", session_id="...")
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        client: httpx.AsyncClient | None = None,
    ):
        if client is not None:
            self._client = client
            self._owns_client = False
        else:
            import os

            resolved_url = (base_url or os.environ.get("CHRONOS_URL", "https://chronos.plato.so")).rstrip("/")
            resolved_key = api_key or os.environ.get("PLATO_API_KEY", "")
            headers = {"X-API-Key": resolved_key} if resolved_key else {}
            self._client = httpx.AsyncClient(
                base_url=resolved_url,
                headers=headers,
                timeout=60.0,
            )
            self._owns_client = True

    async def close(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def __aenter__(self) -> AsyncExperiments:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.close()

    # -----------------------------------------------------------------------
    # Experiment files
    # -----------------------------------------------------------------------

    async def list_files(self) -> list[ExperimentFileResponse]:
        """List all experiment files for the current org."""
        response = await list_experiment_files.asyncio(self._client)
        return list(response.files)

    async def get_file(self, file_id: str) -> ExperimentFileResponse:
        """Get an experiment file by public ID."""
        response = await list_experiment_files.asyncio(self._client)
        for f in response.files:
            if f.public_id == file_id:
                return f
        raise ValueError(f"Experiment file '{file_id}' not found")

    async def create_file(
        self,
        *,
        name: str,
        description: str | None = None,
        world_key: str = "webclone",
        tags: list[str] | None = None,
        notes: str | None = None,
        config_json: dict[str, Any] | None = None,
        target_reviews: list[dict[str, Any]] | None = None,
        git_link: str | None = None,
    ) -> ExperimentFileResponse:
        """Create a new experiment file with an initial version."""
        return await create_experiment_file.asyncio(
            self._client,
            body=ExperimentFileCreateRequest(
                name=name,
                description=description,
                world_key=world_key,
                tags=tags or [],
                notes=notes,
                config_json=config_json or {},
                target_reviews=target_reviews or [],
                git_link=git_link,
            ),
        )

    async def update_file(
        self,
        file_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        target_reviews: list[dict[str, Any]] | None = None,
    ) -> ExperimentFileResponse:
        """Update experiment file metadata."""
        kwargs: dict[str, Any] = {}
        if name is not None:
            kwargs["name"] = name
        if description is not None:
            kwargs["description"] = description
        if target_reviews is not None:
            kwargs["target_reviews"] = target_reviews
        return await update_experiment_file.asyncio(
            self._client,
            public_id=file_id,
            body=ExperimentFileUpdateRequest(**kwargs),
        )

    # -----------------------------------------------------------------------
    # Target reviews
    # -----------------------------------------------------------------------

    async def get_target_reviews(self, file_id: str) -> list[TargetReviewSpec]:
        """Get target review specs for an experiment file."""
        file = await self.get_file(file_id)
        return list(file.target_reviews or [])

    # -----------------------------------------------------------------------
    # Versions
    # -----------------------------------------------------------------------

    async def create_version(
        self,
        *,
        file_id: str,
        config_json: dict[str, Any],
        notes: str = "",
        tags: list[str] | None = None,
        git_link: str | None = None,
    ) -> ExperimentFileResponse:
        """Create a new version of an experiment file."""
        return await create_experiment_file_version.asyncio(
            self._client,
            public_id=file_id,
            body=ExperimentFileVersionCreateRequest(
                config_json=config_json,
                notes=notes,
                tags=tags or [],
                git_link=git_link,
            ),
        )

    # -----------------------------------------------------------------------
    # Launch
    # -----------------------------------------------------------------------

    async def launch(self, *, version_id: str) -> LaunchJobResponse:
        """Launch a session from an experiment version.

        The backend pulls the full config from the version's config_json,
        resolves env var placeholders, and auto-links the session to the version.
        """
        return await launch_experiment.asyncio(
            self._client,
            version_public_id=version_id,
            body=LaunchExperimentRequest(),
        )

    # -----------------------------------------------------------------------
    # Session linking
    # -----------------------------------------------------------------------

    async def attach_session(self, *, version_id: str, session_id: str) -> None:
        """Attach an existing session to an experiment version."""
        await attach_session_to_experiment_version.asyncio(
            self._client,
            public_id=version_id,
            session_public_id=session_id,
        )

    async def detach_session(self, *, version_id: str, session_id: str) -> None:
        """Detach a session from an experiment version."""
        await detach_session_from_experiment_version.asyncio(
            self._client,
            public_id=version_id,
            session_public_id=session_id,
        )


class Experiments:
    """Synchronous client for the Chronos experiments API.

    Usage::

        from plato.chronos.experiments import Experiments

        experiments = Experiments(base_url="https://chronos.plato.so", api_key="pk_...")
        file = experiments.get_file("file-public-id")
        reviews = experiments.get_target_reviews("file-public-id")
    """

    def __init__(
        self,
        *,
        base_url: str | None = None,
        api_key: str | None = None,
        client: httpx.Client | None = None,
    ):
        if client is not None:
            self._client = client
            self._owns_client = False
        else:
            import os

            resolved_url = (base_url or os.environ.get("CHRONOS_URL", "https://chronos.plato.so")).rstrip("/")
            resolved_key = api_key or os.environ.get("PLATO_API_KEY", "")
            headers = {"X-API-Key": resolved_key} if resolved_key else {}
            self._client = httpx.Client(
                base_url=resolved_url,
                headers=headers,
                timeout=60.0,
            )
            self._owns_client = True

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> Experiments:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def list_files(self) -> list[ExperimentFileResponse]:
        response = list_experiment_files.sync(self._client)
        return list(response.files)

    def get_file(self, file_id: str) -> ExperimentFileResponse:
        response = list_experiment_files.sync(self._client)
        for f in response.files:
            if f.public_id == file_id:
                return f
        raise ValueError(f"Experiment file '{file_id}' not found")

    def create_file(
        self,
        *,
        name: str,
        description: str | None = None,
        world_key: str = "webclone",
        tags: list[str] | None = None,
        notes: str | None = None,
        config_json: dict[str, Any] | None = None,
        target_reviews: list[dict[str, Any]] | None = None,
        git_link: str | None = None,
    ) -> ExperimentFileResponse:
        return create_experiment_file.sync(
            self._client,
            body=ExperimentFileCreateRequest(
                name=name,
                description=description,
                world_key=world_key,
                tags=tags or [],
                notes=notes,
                config_json=config_json or {},
                target_reviews=target_reviews or [],
                git_link=git_link,
            ),
        )

    def update_file(
        self,
        file_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        target_reviews: list[dict[str, Any]] | None = None,
    ) -> ExperimentFileResponse:
        kwargs: dict[str, Any] = {}
        if name is not None:
            kwargs["name"] = name
        if description is not None:
            kwargs["description"] = description
        if target_reviews is not None:
            kwargs["target_reviews"] = target_reviews
        return update_experiment_file.sync(
            self._client,
            public_id=file_id,
            body=ExperimentFileUpdateRequest(**kwargs),
        )

    def get_target_reviews(self, file_id: str) -> list[TargetReviewSpec]:
        file = self.get_file(file_id)
        return list(file.target_reviews or [])

    def create_version(
        self,
        *,
        file_id: str,
        config_json: dict[str, Any],
        notes: str = "",
        tags: list[str] | None = None,
        git_link: str | None = None,
    ) -> ExperimentFileResponse:
        return create_experiment_file_version.sync(
            self._client,
            public_id=file_id,
            body=ExperimentFileVersionCreateRequest(
                config_json=config_json,
                notes=notes,
                tags=tags or [],
                git_link=git_link,
            ),
        )

    def launch(self, *, version_id: str) -> LaunchJobResponse:
        return launch_experiment.sync(
            self._client,
            version_public_id=version_id,
            body=LaunchExperimentRequest(),
        )

    def attach_session(self, *, version_id: str, session_id: str) -> None:
        attach_session_to_experiment_version.sync(
            self._client,
            public_id=version_id,
            session_public_id=session_id,
        )

    def detach_session(self, *, version_id: str, session_id: str) -> None:
        detach_session_from_experiment_version.sync(
            self._client,
            public_id=version_id,
            session_public_id=session_id,
        )
