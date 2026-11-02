"""How a sandbox host tells that a sandbox's server is ready."""

from dataclasses import dataclass

from labqoat.json_document import JsonValue


@dataclass(frozen=True)
class Probe:
    """A readiness check the host repeats until it passes: a listening TCP port, or a command that exits 0.

    Build one with ``Probe.with_tcp`` or ``Probe.with_exec`` and pass it to ``create(readiness_probe=...)``;
    ``Sandbox.wait_until_ready`` then returns once the check has passed.
    """

    tcp_port: int | None = None
    command: tuple[str, ...] = ()
    interval_ms: int = 100

    @classmethod
    def with_tcp(cls, port: int, *, interval_ms: int = 100) -> "Probe":
        """Ready once something in the sandbox listens on ``port``."""
        if not 0 < port < 65536:
            raise ValueError(f"a TCP port is between 1 and 65535, not {port}")
        return cls(tcp_port=port, interval_ms=interval_ms)

    @classmethod
    def with_exec(cls, *argv: str, interval_ms: int = 100) -> "Probe":
        """Ready once the command ``argv`` exits 0 inside the sandbox."""
        if not argv or not all(isinstance(argument, str) for argument in argv):
            raise TypeError("a probe command is one or more strings: Probe.with_exec('test', '-f', '/ready')")
        return cls(command=argv, interval_ms=interval_ms)

    def document(self) -> dict[str, JsonValue]:
        """Describe the check as the host reads it."""
        check: dict[str, JsonValue] = (
            {"exec": list(self.command)} if self.tcp_port is None else {"tcp_port": self.tcp_port}
        )
        return {**check, "interval_ms": self.interval_ms}
