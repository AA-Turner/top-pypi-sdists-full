"""control_plane package — proto firewall seam (ADR §3.7).

Only codec.py and stub_server.py may import _pb directly.
client.py is proto-free: use make_client() to wire codec into it.
"""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import Any

from aigie.autonomous.control_plane.client import ControlStreamClient, _CodecInterface
from aigie.autonomous.control_plane.codec import (
    CodecError,
    outcome_to_proto,
    pb,
    pb_grpc,
    proto_to_directive,
)
from aigie.autonomous.directives import Directive
from aigie.autonomous.outcome import OutcomeReport


def _make_hello_envelope(
    sdk_version: str,
    sdk_language: str,
    customer_id: str,
    rule_cache_version_provider: Callable[[], str],
) -> Any:
    hello = pb.Hello(
        sdk_version=sdk_version,
        sdk_language=sdk_language,
        customer_id=customer_id,
        rule_cache_version=rule_cache_version_provider(),
    )
    return pb.ClientEnvelope(hello=hello)


def _make_outcome_envelope(outcome: OutcomeReport) -> Any:
    return pb.ClientEnvelope(outcome=outcome_to_proto(outcome))


def _make_ping_envelope() -> Any:
    return pb.ClientEnvelope(ping=pb.Ping(sent_unix_ms=int(time.time() * 1000)))


def _build_codec_interface() -> _CodecInterface:
    """Build a _CodecInterface wired to the real codec functions."""
    return _CodecInterface(
        outcome_to_proto=outcome_to_proto,
        proto_to_directive=proto_to_directive,
        make_hello_envelope=_make_hello_envelope,
        make_outcome_envelope=_make_outcome_envelope,
        make_ping_envelope=_make_ping_envelope,
        stub_cls=pb_grpc.ControlPlaneStub,
        codec_error_cls=CodecError,
    )


def make_client(
    endpoint: str,
    api_key: str | None,
    on_directive: Callable[[Directive], None],
    sdk_version: str = "0.2.40",
    sdk_language: str = "python",
    customer_id: str = "",
    rule_cache_version_provider: Callable[[], str] = lambda: "",
) -> ControlStreamClient:
    """Factory: build a ControlStreamClient wired to the real codec.

    This is the canonical way to create a ControlStreamClient outside of tests.
    The _CodecInterface injection keeps client.py free of any _pb import.
    """
    return ControlStreamClient(
        endpoint=endpoint,
        api_key=api_key,
        on_directive=on_directive,
        codec=_build_codec_interface(),
        sdk_version=sdk_version,
        sdk_language=sdk_language,
        customer_id=customer_id,
        rule_cache_version_provider=rule_cache_version_provider,
    )


__all__ = ["ControlStreamClient", "make_client", "_build_codec_interface", "_CodecInterface"]
