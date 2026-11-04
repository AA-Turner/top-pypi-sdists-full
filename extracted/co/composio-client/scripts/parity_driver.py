"""One Python lane of the live parity harness, as a subprocess.

``packages/parity`` compares two clients by running the same scenario set
through both and diffing what went on the wire. The TypeScript lanes construct
their clients in-process; the Python lanes cannot, because the pinned Stainless
distribution and this repo's package both import as ``composio_client`` and so
cannot coexist in one interpreter — the same collision
``capture_stainless_oracle.py`` already works around. Each Python lane is
therefore its own isolated interpreter, and this module is what runs in it::

    uv run --isolated --no-project --with composio-client==1.43.0 \\
        python scripts/parity_driver.py --lane stainless
    uv run --isolated --no-project --with ./dist/composio_client-<v>.whl \\
        python scripts/parity_driver.py --lane owned

It speaks one JSON object per line on stdin and stdout, and it implements the
adapter contract in ``packages/parity/src/adapters/adapter.ts`` and nothing
else: turn an invocation into a real HTTP exchange, and report what went on the
wire. Every message carries a ``seq`` and every frame echoes the one it answers,
so the adapter correlates a request with its answer by number rather than by
arrival order — a late answer would otherwise shift every later scenario onto
its predecessor's capture, and the cleanup ledger is built from those captures.

## The capture sits below the client, not around it

An ``httpx`` transport, for the reason the TypeScript adapter wraps ``fetch``:
a client's return value is what it *decided* the exchange meant — an exception
on an error status, a parsed model on success, with the bytes gone. Both
clients are allowed to differ in that layer, and a harness reading return values
would never see it. Below the transport, what is compared is the HTTP.

Captures are verbatim. Nothing here rewrites what it saw, so a capture carries
the API key the run authenticated with and every credential the API returned.
The artifact directory is gitignored and is secret-bearing.

## One Python calling convention

The scenarios use the Stainless Python convention: the last path parameter is
positional, while every leading path parameter, body field, query field, and
declared header is a flat keyword. Both the pinned and owned lanes now receive
that same invocation. The spelling rules come from ``wire_corpus.oracle_call``,
which also captured the offline fixture.

## What this module refuses to guess

A scenario whose accessor the client does not expose, an argument shape the
convention does not describe, a body property that matches no declared
parameter and no request schema — each is an error, not a best effort. A lane
that quietly dropped an argument would produce a capture that compares equal to
the other lane's for a reason that has nothing to do with either client.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from importlib.metadata import version as distribution_version
from typing import Any

import httpx

# `wire_corpus` sits next to this file, so a flat import works under the
# isolated interpreter without any sys.path surgery — the same arrangement
# `capture_stainless_oracle.py` relies on, and the reason `tests/conftest.py`
# puts `scripts/` on the path rather than importing these two as a package.
from wire_corpus import (
    COVERAGE_PATH,
    ORACLE_KWARG_RENAMES,
    ORACLE_VERSION,
    is_ignored_header,
    oracle_location,
    resolve_accessor,
    snake_case,
)

#: Bumped alongside `PROTOCOL_VERSION` in
#: `packages/parity/src/adapters/python.ts` when the framing changes, and
#: alongside `BUNDLE_VERSION` in `packages/parity/src/core/bundle.ts` when the
#: exchange shape does. The handshake is refused outright on a mismatch, so a
#: driver built against an older contract fails at startup rather than
#: contributing captures the comparator reads wrong.
#:
#: v2 added `seq`. Every frame this module emits echoes the `seq` of the message
#: it answers, because position alone is not correlation: an answer that arrives
#: late shifts every later scenario onto its predecessor's capture, and the
#: adapter cannot notice unless the frames say what they are answering.
PROTOCOL_VERSION = 2

LANES = ("stainless", "owned")

#: The methods `packages/parity`'s inventory models. A method outside it has no
#: place in a capture that will be compared as if it did.
HTTP_METHODS = ("GET", "POST", "PUT", "PATCH", "DELETE")

#: Response headers the comparison reads, matching `CAPTURED_RESPONSE_HEADERS`.
CAPTURED_RESPONSE_HEADERS = ("content-type", "content-encoding")


# ---------------------------------------------------------------------------
# capture
# ---------------------------------------------------------------------------


class CapturingTransport(httpx.BaseTransport):
    """Records each exchange verbatim and passes the response through untouched.

    The response is read into memory (``httpx.Response.read()``) so the bytes
    can be recorded without consuming the stream the client is about to parse —
    the transport-level equivalent of the TypeScript adapter cloning the
    response before reading it.
    """

    def __init__(self) -> None:
        self._inner = httpx.HTTPTransport(retries=0)
        self.recorded: list[dict[str, Any]] = []

    def handle_request(self, request: httpx.Request) -> httpx.Response:
        captured = _request_capture(request)
        try:
            response = self._inner.handle_request(request)
        except Exception as exc:  # noqa: BLE001 - a transport failure is a result
            self.recorded.append(
                {"request": captured, "response": None, "transportError": f"{type(exc).__name__}: {exc}"}
            )
            raise
        response.read()
        self.recorded.append(
            {
                "request": captured,
                "response": {
                    "status": response.status_code,
                    "headers": {
                        name: response.headers[name]
                        for name in CAPTURED_RESPONSE_HEADERS
                        if name in response.headers
                    },
                    "bodyText": response.text,
                },
                "transportError": None,
            }
        )
        return response

    def take(self) -> list[dict[str, Any]]:
        """Returns and clears what was recorded since the last call."""
        taken = self.recorded
        self.recorded = []
        return taken

    def close(self) -> None:
        self._inner.close()


def _request_capture(request: httpx.Request) -> dict[str, Any]:
    """The request as it goes out, in the shape `RequestCaptureSchema` declares.

    Header filtering is ``wire_corpus.is_ignored_header``, which already draws
    the line this needs: generator identity (``x-stainless-*``, ``user-agent``)
    and transport artifacts (``content-length``, ``accept-encoding``,
    ``connection``). The last two matter more here than in the offline fixture —
    the two lanes resolve their own httpx, and a version difference must not
    read as the clients disagreeing.
    """
    method = request.method.upper()
    if method not in HTTP_METHODS:
        raise ValueError(f"parity driver: unsupported HTTP method {method} on {request.url.path}")

    raw_target = request.url.raw_path.decode("ascii")
    raw_path, _, raw_query = raw_target.partition("?")
    content = request.content
    body_text = content.decode("utf-8", errors="replace") if content else ""
    try:
        body = json.loads(content) if content else None
    except ValueError:
        body = None

    return {
        "method": method,
        "path": raw_path,
        "query": raw_query,
        "headers": {
            name.lower(): value for name, value in request.headers.items() if not is_ignored_header(name)
        },
        "body": body,
        # Set only when a body went out that is not JSON, so the bytes stay
        # comparable; an empty body is neither.
        "bodyText": None if body is not None or body_text == "" else body_text,
    }


# ---------------------------------------------------------------------------
# the covered operations
# ---------------------------------------------------------------------------


class Operations:
    """The generated coverage map, indexed the two ways a lane asks.

    By **chain**, because that is all an ``Invocation`` carries — the adapter
    contract passes a dotted client chain and its arguments, and nothing else.
    ``surface-coverage.json`` records the TypeScript chain as ``location``
    beside the Python ``accessor``, and those chains are unique across the
    covered surface, so the bridge between the two languages is a file the
    generator already writes rather than a table kept by hand here.

    By **(method, normalized path)** as well, because that is the identity the
    harness inventory and the spec share. Parameter *names* differ between them
    (``{sessionID}`` against ``{session_id}``) and only their positions matter,
    so the name is erased before indexing.
    """

    def __init__(self) -> None:
        coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
        self._by_key: dict[tuple[str, str], dict[str, Any]] = {}
        self._by_chain: dict[str, dict[str, Any]] = {}

        for entry in coverage["operations"]:
            method, path = str(entry["key"]).split(" ", 1)
            accessor = tuple(entry["accessor"])
            record = {
                "accessor": accessor,
                # The pinned oracle has no `_internal`: the operations the spec
                # tags `x-internal` sit at its root, where the scenarios name them.
                "oracleAccessor": oracle_location(accessor),
                "pathNames": tuple(
                    segment[1:-1]
                    for segment in path.split("/")
                    if segment.startswith("{") and segment.endswith("}")
                ),
                # Keyed by wire name, so this is read *before* snake_case erases
                # the distinction it exists to preserve.
                "renames": ORACLE_KWARG_RENAMES.get(f"{method.lower()} {path}", {}),
            }
            chain = ".".join(oracle_location(tuple(entry["location"])))
            if chain in self._by_chain:
                raise ValueError(
                    f"parity driver: two covered operations both answer to the chain {chain}; "
                    "an invocation naming it could not say which one it meant"
                )
            self._by_key[(method.lower(), _normalize_path(path))] = record
            self._by_chain[chain] = record

    def for_key(self, key: str) -> dict[str, Any]:
        method, path = key.split(" ", 1)
        found = self._by_key.get((method.lower(), _normalize_path(path)))
        if found is None:
            raise KeyError(
                f"parity driver: no covered operation for {key}; "
                "surface-coverage.json and the harness inventory disagree"
            )
        return found

    def for_chain(self, chain: str) -> dict[str, Any]:
        found = self._by_chain.get(chain)
        if found is None:
            raise KeyError(
                f"parity driver: no covered operation is reached by {chain}; "
                "the scenario names a chain surface-coverage.json does not record"
            )
        return found


def _normalize_path(path: str) -> str:
    """A path template with its parameter names erased, keeping their positions."""
    out: list[str] = []
    for segment in path.split("/"):
        out.append("{}" if segment.startswith("{") and segment.endswith("}") else segment)
    return "/".join(out)


# ---------------------------------------------------------------------------
# shared invocation
# ---------------------------------------------------------------------------


def _snake_keys(value: Any) -> Any:
    """Every mapping key in a payload, respelled the way both clients take it.

    Recursive because a nested object's keys are keyword-free but still aliased:
    both clients accept the pythonic spelling anywhere and rename it to the
    wire's on the way out, and the committed oracle fixture is the evidence that
    the two agree about the result.
    """
    if isinstance(value, Mapping):
        return {snake_case(str(key)): _snake_keys(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_snake_keys(item) for item in value]
    return value


def _split_arguments(
    invocation: Mapping[str, Any], operation: Mapping[str, Any]
) -> tuple[Any, dict[str, Any]]:
    """A chain invocation's arguments as ``(last path argument, flat bag)``.

    The convention both Stainless generators emit: exactly one positional
    argument when the operation has any path parameter at all, and one optional
    options object after it. Anything else is refused rather than interpreted —
    a driver guessing at an argument shape produces a capture whose agreement
    with the other lane means nothing.
    """
    args = list(invocation.get("args") or [])
    expects_positional = 1 if operation["pathNames"] else 0

    positional = args[:expects_positional]
    rest = args[expects_positional:]

    if len(positional) != expects_positional:
        raise ValueError(
            f"parity driver: {invocation['chain']} declares {len(operation['pathNames'])} path parameter(s) "
            f"but the scenario passed {len(args)} argument(s)"
        )
    if len(rest) > 1:
        raise ValueError(
            f"parity driver: {invocation['chain']} passed {len(rest)} arguments after the path parameter; "
            "the calling convention allows one options object"
        )
    bag = rest[0] if rest else None
    if bag is not None and not isinstance(bag, Mapping):
        raise ValueError(
            f"parity driver: {invocation['chain']} passed a {type(bag).__name__} where the calling "
            "convention expects an options object"
        )

    return (positional[0] if positional else None, dict(bag or {}))


def oracle_chain_call(client: Any, invocation: Mapping[str, Any], operation: Mapping[str, Any]) -> Any:
    """Pass the shared Stainless invocation to either Python client.

    Nearly a pass-through: the scenarios are already written this way, since the
    TypeScript client the harness was built against is the same generator's
    output. Only the keys are respelled, because a TypeScript options key is the
    wire name and a Python keyword argument is the snake_case one.
    """
    method = resolve_accessor(client, operation["accessor"])
    if method is None:
        raise ValueError(
            f"parity driver: the stainless client exposes no {'.'.join(operation['accessor'])}; "
            "a scenario that cannot be spelled on this lane must declare the raw escape hatch"
        )
    last, bag = _split_arguments(invocation, operation)
    renames = operation["renames"]
    kwargs = {renames.get(str(key)) or snake_case(str(key)): _snake_keys(value) for key, value in bag.items()}
    missing = [snake_case(name) for name in operation["pathNames"][:-1] if snake_case(name) not in kwargs]
    if missing:
        raise ValueError(
            f"parity driver: {invocation['chain']} needs path parameter(s) {', '.join(missing)}, "
            "which the scenario's options object does not carry"
        )
    return method(*([last] if last is not None else []), **kwargs)


def owned_chain_call(client: Any, invocation: Mapping[str, Any], operation: Mapping[str, Any]) -> Any:
    """Compatibility alias retained for callers of the driver helper."""
    return oracle_chain_call(client, invocation, operation)


def oracle_raw_call(client: Any, invocation: Mapping[str, Any]) -> Any:
    """The pinned client's escape hatch: ``cast_to`` required, query in ``options``."""
    verb = getattr(client, invocation["method"].lower())
    options = {"params": invocation["query"]} if invocation.get("query") else {}
    kwargs: dict[str, Any] = {"cast_to": object, "options": options}
    if invocation.get("body") is not None:
        kwargs["body"] = invocation["body"]
    return verb(invocation["path"], **kwargs)


def owned_raw_call(client: Any, invocation: Mapping[str, Any]) -> Any:
    """Compatibility alias: the owned raw verbs accept the Stainless form."""
    return oracle_raw_call(client, invocation)


# ---------------------------------------------------------------------------
# the lane
# ---------------------------------------------------------------------------


def build_client(lane: str, api_key: str, base_url: str, transport: CapturingTransport) -> tuple[Any, str]:
    """One client, with retries off and the capture underneath it.

    Retries are not left at the default: disabled. A retried mutation is not the
    same mutation twice, and two lanes stop being comparable the moment one
    retries and the other does not.
    """
    import composio_client

    installed = distribution_version("composio-client")
    if lane == "stainless" and installed != ORACLE_VERSION:
        raise SystemExit(
            f"parity driver: --lane stainless expects the pinned oracle {ORACLE_VERSION}, "
            f"but this interpreter has composio-client {installed}"
        )
    if lane == "owned" and installed == ORACLE_VERSION:
        raise SystemExit(
            f"parity driver: --lane owned is running the pinned oracle {ORACLE_VERSION}; "
            "the isolated environment was built from the wrong distribution"
        )

    # The pinned oracle spells the credential `api_key=`; the owned client has
    # taken `auth` since 2.0.0-rc.18, and `ProjectAuth` sends the same
    # `x-api-key` on every request that `api_key=` alone did.
    credentials: dict[str, Any] = (
        {"api_key": api_key} if lane == "stainless" else {"auth": composio_client.ProjectAuth(api_key)}
    )
    client = composio_client.Composio(
        **credentials,
        base_url=base_url,
        max_retries=0,
        http_client=httpx.Client(transport=transport, follow_redirects=False),
    )
    return client, f"composio-client@{installed}"


def execute(
    lane: str,
    client: Any,
    transport: CapturingTransport,
    operations: Operations,
    message: Mapping[str, Any],
) -> dict[str, Any]:
    """One invocation, folded into the exchange the comparison consumes.

    The client's own error is swallowed on purpose: an HTTP 404 is a *result*
    here, and the capture below the transport already holds everything the
    comparison needs. A failure with no exchange at all is the one reported,
    because it means the request never reached the API.
    """
    transport.take()
    invocation = message["invocation"]
    thrown: str | None = None

    try:
        if invocation["kind"] == "raw":
            oracle_raw_call(client, invocation)
        else:
            operation = operations.for_chain(invocation["chain"])
            if lane == "stainless":
                operation = {**operation, "accessor": operation["oracleAccessor"]}
            oracle_chain_call(client, invocation, operation)
    except Exception as exc:  # noqa: BLE001 - an error status is a result, not a failure
        thrown = f"{type(exc).__name__}: {exc}"

    exchanges = transport.take()
    if not exchanges:
        return {
            "request": None,
            "response": None,
            "transportError": thrown or "the client returned without issuing a request",
            "exchangeCount": 0,
        }

    first = exchanges[0]
    return {
        "request": first["request"],
        "response": first["response"],
        "transportError": first["transportError"],
        "exchangeCount": len(exchanges),
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lane", choices=LANES, required=True)
    args = parser.parse_args(argv)

    handshake = json.loads(sys.stdin.readline())
    if handshake.get("protocolVersion") != PROTOCOL_VERSION:
        raise SystemExit(
            f"parity driver: the adapter speaks protocol v{handshake.get('protocolVersion')} "
            f"and this driver speaks v{PROTOCOL_VERSION}"
        )

    transport = CapturingTransport()
    client, client_version = build_client(args.lane, handshake["apiKey"], handshake["baseUrl"], transport)
    operations = Operations()

    _emit({"seq": handshake.get("seq"), "ready": True, "lane": args.lane, "clientVersion": client_version})

    for line in sys.stdin:
        if not line.strip():
            continue
        message = json.loads(line)
        if message.get("shutdown"):
            break
        # Echoed on the fault frame too: a driver fault is still this request's
        # answer, and an answer the adapter cannot place is one it must refuse.
        seq = message.get("seq")
        try:
            _emit({"seq": seq, "exchange": execute(args.lane, client, transport, operations, message)})
        except Exception as exc:  # noqa: BLE001 - a driver fault is reported, not crashed on
            _emit({"seq": seq, "error": f"{type(exc).__name__}: {exc}"})

    transport.close()
    return 0


def _emit(payload: Mapping[str, Any]) -> None:
    """One JSON object, one line, flushed — the adapter reads line by line."""
    sys.stdout.write(json.dumps(payload) + "\n")
    sys.stdout.flush()


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
