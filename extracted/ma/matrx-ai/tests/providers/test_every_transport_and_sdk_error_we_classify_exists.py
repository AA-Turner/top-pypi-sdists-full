"""Every error class the classifiers match on exists in the INSTALLED libraries.

THE CLASS (2026-10-30, found while planning the SDK upgrade campaign). The transport
branch of ``classify_common_error`` and the billed-call test ``wire_was_engaged`` named
``httpx.<Error>`` directly. ``anthropic`` has run on ``httpx2`` since 1.0 and ``openai``
moves to it in 3.0; ``httpx2``'s classes are unrelated to ``httpx``'s (not equal, not
subclasses). A Claude stream dropped mid-body raised ``httpx2.RemoteProtocolError``, the
typed branch never matched, and the failure was left to string guessing — and
``wire_was_engaged`` called a mid-flight ``httpx2.ReadTimeout`` "never billed".

The sibling: ``_resolve_exc`` returns ``None`` when an SDK renames an exception class, and
a direct ``sdk.FooError`` raises ``AttributeError`` mid-classify. Either way an SDK bump
silently changes what an error means. Both layers below fail the build instead:

  1. behavior — real httpx2 exceptions classify exactly like their httpx twins;
  2. existence — every ``<sdk>.<Name>`` / ``_resolve_exc(<sdk>, "<Name>")`` /
     ``from <sdk>.errors import <Name>`` the classifiers reference resolves on the
     installed SDK, and every httpx flavor exports every transport name we ask for.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

import httpx
import pytest

from matrx_ai.providers import errors as errors_module
from matrx_ai.providers.device.classify import device_error_for
from matrx_ai.providers.errors import (
    classify_anthropic_error,
    classify_common_error,
    classify_openai_error,
    wire_was_engaged,
)
from matrx_ai.providers.http_flavors import HTTPX_FLAVORS, missing_transport_names

httpx2 = pytest.importorskip("httpx2")

_PROVIDERS_DIR = Path(errors_module.__file__).parent
_CLASSIFIER_SOURCES = (
    _PROVIDERS_DIR / "errors.py",
    _PROVIDERS_DIR / "device" / "classify.py",
)
_SDK_MODULES = frozenset(
    {
        "anthropic",
        "openai",
        "groq",
        "together",
        "cerebras_cloud_sdk",
        "xai_sdk",
        "elevenlabs",
        "cohere",
    }
)


# --- 1. behavior: httpx2 is classified exactly like httpx ---------------------------


@pytest.mark.parametrize("flavor", [httpx, httpx2], ids=lambda m: m.__name__)
def test_a_truncated_stream_is_an_incomplete_response_on_every_flavor(flavor) -> None:
    exc = flavor.RemoteProtocolError("peer closed connection without sending complete message body")
    info = classify_anthropic_error(exc)
    assert info.error_type == "incomplete_response", info
    assert info.is_retryable is True, info
    assert info.details["transport_exception"].startswith(f"{flavor.__name__}."), info.details


@pytest.mark.parametrize("flavor", [httpx, httpx2], ids=lambda m: m.__name__)
def test_a_read_timeout_is_a_timeout_on_every_flavor(flavor) -> None:
    info = classify_common_error(flavor.ReadTimeout(""), "Anthropic")
    assert info is not None and info.error_type == "provider_timeout", info
    assert info.is_retryable is True, info


@pytest.mark.parametrize("flavor", [httpx, httpx2], ids=lambda m: m.__name__)
def test_a_dropped_connection_is_a_connection_error_on_every_flavor(flavor) -> None:
    info = classify_openai_error(flavor.ReadError(""))
    assert info.error_type == "connection_error", info
    assert info.is_retryable is True, info


@pytest.mark.parametrize("flavor", [httpx, httpx2], ids=lambda m: m.__name__)
def test_billing_judgement_is_the_same_on_every_flavor(flavor) -> None:
    # Never reached a server: nothing billed. Mid-flight timeout: may have been billed.
    assert wire_was_engaged(flavor.ConnectError("refused")) is False
    assert wire_was_engaged(flavor.ReadTimeout("")) is True


@pytest.mark.parametrize("flavor", [httpx, httpx2], ids=lambda m: m.__name__)
def test_the_device_relay_reads_every_flavor(flavor) -> None:
    timeout = device_error_for(flavor.ReadTimeout("")).error_info
    offline = device_error_for(flavor.ConnectError("refused")).error_info
    assert timeout.error_type != offline.error_type
    assert "timed out" in timeout.message, timeout
    assert "could not be reached" in offline.message, offline


def test_the_classifier_does_not_grade_its_own_homework() -> None:
    # Independent of every tuple the module built: the raw httpx2 class must be one
    # the module's never-sent / transport tuples contain.
    assert httpx2.ConnectError in errors_module._NEVER_SENT_EXC
    assert httpx2.TransportError in errors_module._HTTPX_TRANSPORT
    assert httpx2.TimeoutException in errors_module._HTTPX_TIMEOUT


# --- 2. existence: every name we match on resolves on the installed library ----------


def test_every_httpx_flavor_exports_every_transport_name_we_match() -> None:
    assert {m.__name__ for m in HTTPX_FLAVORS} >= {"httpx", "httpx2"}
    names = (*errors_module._NEVER_SENT_HTTPX_NAMES, *errors_module._HTTPX_TRANSPORT_NAMES)
    assert missing_transport_names(*names) == []


def _referenced_sdk_names() -> set[tuple[str, str]]:
    found: set[tuple[str, str]] = set()
    for source in _CLASSIFIER_SOURCES:
        tree = ast.parse(source.read_text(), filename=str(source))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id in _SDK_MODULES
                and node.attr[:1].isupper()
            ):
                found.add((node.value.id, node.attr))
            elif (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "_resolve_exc"
                and len(node.args) == 2
                and isinstance(node.args[0], ast.Name)
                and isinstance(node.args[1], ast.Constant)
            ):
                found.add((node.args[0].id, node.args[1].value))
            elif (
                isinstance(node, ast.ImportFrom)
                and node.module
                and node.module.split(".")[0]
                in {
                    *_SDK_MODULES,
                    "google",
                }
            ):
                found.update((node.module, alias.name) for alias in node.names)
    return found


def test_the_scan_sees_the_classifiers() -> None:
    # A scan that finds nothing passes everything; prove it reads real references.
    names = _referenced_sdk_names()
    assert ("anthropic", "OverloadedError") in names
    assert ("anthropic", "AuthenticationError") in names
    assert ("openai", "RateLimitError") in names
    assert ("google.genai.errors", "ClientError") in names


def test_every_sdk_error_the_classifiers_name_exists_on_the_installed_sdk() -> None:
    missing: list[str] = []
    for module_name, attr in sorted(_referenced_sdk_names()):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            missing.append(f"{module_name} (not importable)")
            continue
        if errors_module._resolve_exc(module, attr) is None:
            missing.append(f"{module_name}.{attr}")
    assert missing == [], (
        "An installed provider SDK no longer exports an error class the classifiers match on. "
        "Find its new name in the SDK's changelog and update providers/errors.py: "
        f"{missing}"
    )


def test_no_sdk_flavored_client_catches_a_named_httpx_error() -> None:
    # A file that builds its client on the SDK's own flavor (``make_capture_http_client``)
    # receives that flavor's errors; naming ``httpx.<Error>`` there misses httpx2's.
    offenders: list[str] = []
    for source in sorted(_PROVIDERS_DIR.rglob("*.py")):
        if source.name == "outbound_capture.py" or "/tests/" in source.as_posix():
            continue
        text = source.read_text()
        if "make_capture_http_client" not in text:
            continue
        for node in ast.walk(ast.parse(text, filename=str(source))):
            if (
                isinstance(node, ast.Attribute)
                and isinstance(node.value, ast.Name)
                and node.value.id == "httpx"
                and node.attr.endswith(("Error", "Exception", "Timeout"))
            ):
                offenders.append(f"{source.relative_to(_PROVIDERS_DIR)}:{node.lineno} httpx.{node.attr}")
    assert offenders == [], f"use http_flavors.transport_classes(...): {offenders}"
