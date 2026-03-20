"""Base review world for Plato.

A review world is a world that reviews another session — producing
annotations (findings) about that session.  Every review world:

- takes a ``target_session_id`` in its config
- declares ``output_models`` it produces (wired into ``review_models`` for schema)
- optionally declares a ``default_review`` spec for how *it* should be reviewed

Identity is structural: a session is a review session if its world is a
:class:`BaseReviewWorld` subclass.  No tags or markers needed.

Review worlds support two execution modes:

Inline
    Called from a parent world via :meth:`run_inline`, sharing the parent's
    workspaces, agents, and services.  No new Chronos session is created.

Standalone
    Launched as its own Chronos session (typically as a child of the target
    session).  Restores workspaces and starts services independently.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from pydantic import Field
from typing_extensions import TypeVar

from plato.agents.runner import AgentRunner
from plato.llm import LLMClient
from plato.worlds.base import BaseWorld
from plato.worlds.config import AgentConfig, LLMConfig, RunConfig
from plato.worlds.models import StepResult
from plato.worlds.review.data import ReviewData
from plato.worlds.review.spec import ReviewSpec
from plato.worlds.workspace import Workspace

if TYPE_CHECKING:
    from plato.worlds.result_store import ResultStore

ReviewConfigT = TypeVar("ReviewConfigT", bound="ReviewWorldConfig")


class ReviewWorldConfig(RunConfig):
    """Base configuration for all review worlds."""

    target_session_id: str = Field(
        default="${TARGET_SESSION_ID}",
        description="Session ID being reviewed",
    )


class BaseReviewWorld(BaseWorld[ReviewConfigT]):
    """Base class for worlds that review other sessions.

    Subclass this, implement :meth:`reset` and :meth:`step`, and register
    with ``@register_world``.

    Example::

        @register_world("my-review")
        class MyReviewWorld(BaseReviewWorld[MyReviewConfig]):
            output_models = [MyFindingModel]
            default_review = None  # humans review this

            async def reset(self) -> Observation:
                ...
            async def step(self) -> StepResult:
                ...
    """

    world_type: ClassVar[str] = "review"

    # Review models this reviewer produces.
    # Automatically wired into BaseWorld.review_models for schema generation.
    output_models: ClassVar[list[type[ReviewData]]] = []

    # Default ReviewSpec for reviewing THIS reviewer (recursive).
    # None means human feedback is the ground truth.
    default_review: ClassVar[ReviewSpec | None] = None

    # Set when running inline within a host world
    _host: BaseWorld | None = None

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Wire output_models into review_models so schema generation picks them up.
        # Check __dict__ to distinguish "explicitly set on this class" from inherited.
        if cls.output_models and "review_models" not in cls.__dict__:
            cls.review_models = list(cls.output_models)

    def __init__(self) -> None:
        super().__init__()
        self._host = None

    # ------------------------------------------------------------------
    # Inline execution
    # ------------------------------------------------------------------

    async def run_inline(self, host_world: BaseWorld) -> StepResult:
        """Run this review inline within a host world, sharing its resources.

        No new Chronos session is created.  The review world shares the
        host's workspaces, agents, and services.

        Args:
            host_world: The parent world whose resources to share.

        Returns:
            The :class:`StepResult` from :meth:`step`.
        """
        self._host = host_world
        self._session_id = host_world._session_id
        self.plato_session = host_world.plato_session
        self.logger = host_world.logger.getChild(self.name)
        await self.reset()
        return await self.step()

    # ------------------------------------------------------------------
    # Resource delegation
    # ------------------------------------------------------------------

    def workspace(self, name: str) -> Workspace:
        """Return a workspace, delegating to the host world if running inline."""
        if self._host is not None:
            return self._host.workspace(name)
        return super().workspace(name)

    def agent(
        self,
        config: AgentConfig,
        display_name: str | None = None,
        workspaces: list[Workspace] | None = None,
    ) -> AgentRunner:
        """Create an agent runner, delegating to the host world if running inline."""
        if self._host is not None:
            return self._host.agent(config=config, display_name=display_name, workspaces=workspaces)
        return super().agent(config=config, display_name=display_name, workspaces=workspaces)

    def llm(self, config: LLMConfig, store: ResultStore | None = None) -> LLMClient:
        """Create an LLM client, delegating to the host world if running inline."""
        if self._host is not None:
            return self._host.llm(config, store=store)
        return super().llm(config, store=store)
