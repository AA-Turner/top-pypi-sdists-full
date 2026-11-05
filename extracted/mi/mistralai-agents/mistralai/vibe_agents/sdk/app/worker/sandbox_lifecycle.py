"""Optional worker-owned durability, independent of provider and Session lifetime."""

from collections.abc import Callable, Mapping
from typing import Protocol

from pydantic import JsonValue

from mistralai.vibe.harness.runtime.hosts.workflows.sandbox_definitions import SandboxDriver
from mistralai.vibe_agents import session_workflow as wire


class SandboxLifecycle(Protocol):
    @property
    def workspace_attempts(self) -> int:
        """Fresh sandboxes the workspace provisioning step may use."""
        ...

    def activity(self) -> None: ...

    def expired(self, provider_state: Mapping[str, JsonValue]) -> bool:
        """Whether a ready sandbox must be replaced before new work reaches it; pure."""
        ...

    def lost(self) -> None:
        """Record that the ready sandbox was marked lost, before activity() for the same command."""
        ...

    def reattach(self, driver: SandboxDriver) -> None:
        """Bind a sandbox carried through Continue-As-New, without I/O."""
        ...

    async def provision(self, driver: SandboxDriver) -> None:
        """Prepare the workspace of a new sandbox, as its workspace provisioning step."""
        ...

    async def checkpoint(self, is_idle: Callable[[], bool]) -> None: ...

    def notice(self) -> str | None:
        """Model context the next Start, Steer, or Send Message must carry."""
        ...

    def notice_delivered(self, notice: str) -> None: ...

    def continuation(self) -> dict[str, JsonValue]: ...


# Called with the start input, the attested caller (None for a Session that runs for no user), and
# the lifecycle state carried across Continue-As-New.
type SandboxLifecycleFactory = Callable[
    [wire.SessionWorkflowStartInput, wire.Principal | None, dict[str, JsonValue] | None], SandboxLifecycle | None
]
