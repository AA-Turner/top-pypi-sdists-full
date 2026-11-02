"""What a sandbox host reports about one sandbox."""

from dataclasses import dataclass, field

from labqoat.json_document import JsonDocument


@dataclass(frozen=True)
class SandboxState:
    """A sandbox's name, tags and stage, and once it finished, its exit code and why it ended.

    ``state`` is ``starting``, ``running`` or ``finished``. Only a finished sandbox has an ``exit_code``: its
    entrypoint's own when ``reason`` is ``exited``, 124 when its ``timeout`` or ``idle_timeout`` ended it, and
    137 when it was terminated or lost. ``ready`` turns true once its readiness probe passed, or as soon as it
    runs when it has none.
    """

    id: str
    name: str | None = None
    tags: dict[str, str] = field(default_factory=dict)
    state: str = "running"
    ready: bool = False
    exit_code: int | None = None
    reason: str | None = None

    @staticmethod
    def decode(document: JsonDocument) -> "SandboxState":
        """Read a sandbox document; a host's listing leaves out what only a finished sandbox has."""
        tags = JsonDocument.expect_dict(document["tags"])
        state = SandboxState(
            JsonDocument.expect_scalar(document["id"], str),
            JsonDocument.expect_optional_scalar(document["name"], str),
            {key: JsonDocument.expect_scalar(value, str) for key, value in tags.items()},
            JsonDocument.expect_scalar(document["state"], str),
            JsonDocument.expect_scalar(document.get("ready", False), bool),
            JsonDocument.expect_optional_scalar(document.get("exit_code"), int),
            JsonDocument.expect_optional_scalar(document.get("reason"), str),
        )
        if (state.state == "finished") == (state.exit_code is None):
            raise ValueError(f"a sandbox that is {state.state!r} cannot have exit code {state.exit_code!r}")
        return state

    @staticmethod
    def listed(document: JsonDocument) -> tuple["SandboxState", ...]:
        """Read every sandbox a host's capacity document lists."""
        listed = JsonDocument.expect_list(document["sandboxes"])
        return tuple(SandboxState.decode(JsonDocument.expect_dict(item)) for item in listed)
