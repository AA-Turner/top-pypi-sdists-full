"""Classify an UNHANDLED task exception before it is streamed to a client.

Every stream in the platform funnels its crash through
``create_streaming_response``. Until 2026-08-17 that path did three things
wrong for any exception the provider layer had not already classified:

1. ``error_type = f"{debug_label.lower()}_error"`` — and debug labels carry
   per-run identifiers (``VisionInterview:72175649``), so the emitted type was
   ``visioninterview:72175649_error``: a NEW error type for every session.
   Nothing can group, count, or alert on that, and the Error Inspector shows
   ``operation: unknown``.
2. ``user_message`` was always "…failed unexpectedly. Please try again or
   adjust your settings." — which tells a non-technical user to go change
   settings they did not break, when the truth was that the server could not
   reach a renamed database table.
3. ``message = str(e)`` shipped the raw operator diagnostic verbatim —
   including ANSI color escapes the browser renders as ``\\u001b[91m``.

The live incident: ``agent.slot_definition`` was renamed to ``agent.mandate``
in the shared database while the running build still queried the old name.
Every mandate resolution platform-wide raised ``SchemaMismatchError``; the one
a user saw arrived as ``visioninterview:72175649_error`` telling them to adjust
their settings.

The 2026-08-27 repeat, same three symptoms one family over: every
``pdf.content_cleaner`` run refused on a broken Provision promise and arrived
as ``pdfclean_error`` — one error type per ROUTE for one failure class —
telling the user to adjust settings that could not possibly fix a code-side
contract disagreement. The mandate family is classified below.

Classification is by exception CLASS NAME on purpose: matrx-connect does not
depend on matrx-orm (or asyncpg), and it must not grow that dependency to
recognize a database error. Names are matched against the raised exception and
its whole ``__mro__``/``__cause__`` chain, so a wrapper around the real cause
still classifies.
"""

from __future__ import annotations

import re
from typing import NamedTuple

# Matches CSI sequences (color, cursor moves). vcprint wraps operator banners
# in these; they are meaningless to a browser and render as literal escapes.
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")

# Segments of a debug label that identify ONE run rather than the KIND of work:
# a uuid, a uuid prefix, or any long hex/digit run. Stripping them is what turns
# `visioninterview:72175649_error` into the groupable `visioninterview_error`.
# A uuid split on its dashes yields short groups (`1e92`, `4bef`), so matching
# only long runs leaves half the uuid in the type — the exact bug the first cut
# of this regex had. A segment is an identifier when it is hex-only, at least 4
# characters, and contains a digit: that catches every uuid group and numeric id
# while leaving real words ("research", "seo", "chat") alone, since they carry
# letters outside a-f.
_ID_SEGMENT_RE = re.compile(
    r"""(?ix)
    ^(
        [0-9a-f]{8,}                          # long hex run: uuid group / id
      | (?=[0-9a-f]{4,7}$)[0-9a-f]*\d[0-9a-f]*  # short uuid group (has a digit)
      | \d{4,}                                # long numeric id
    )$
    """
)

_LABEL_SPLIT_RE = re.compile(r"[^a-z0-9]+")


#: What a person reads when a stream crashes for a reason nothing classified. No route label, no
#: exception class name, no "adjust your settings": the class and the request id ride in the error's
#: ``details`` and the durable system_error record.
GENERIC_CRASH_MESSAGE = "Something went wrong on our side and this did not finish. Please try again."


class FailureClass(NamedTuple):
    """A recognized infrastructure failure — stable type + honest message."""

    error_type: str
    user_message: str


# The user message never blames the user and never asks them to change a
# setting: for every entry here the cause is on our side of the wire.
_INFRASTRUCTURE_CLASSES: tuple[tuple[frozenset[str], FailureClass], ...] = (
    (
        frozenset(
            {
                "SchemaMismatchError",
                "UndefinedTableError",
                "UndefinedColumnError",
                "UndefinedObjectError",
                "UndefinedFunctionError",
                "InvalidSchemaNameError",
            }
        ),
        FailureClass(
            error_type="database_schema_mismatch",
            user_message=(
                "Something on our side is out of date and this could not run. "
                "Nothing you did caused it and your work is saved — we have "
                "been alerted."
            ),
        ),
    ),
    (
        frozenset(
            {
                "ConnectionDoesNotExistError",
                "CannotConnectNowError",
                "TooManyConnectionsError",
                "InterfaceError",
                "PostgresConnectionError",
            }
        ),
        FailureClass(
            error_type="database_unavailable",
            user_message=(
                "We could not reach the database just now. Nothing you did "
                "caused it and your work is saved — please try again in a "
                "moment."
            ),
        ),
    ),
    (
        # THE MANDATE CONTRACT FAMILY (added 2026-08-27). A mandated run that
        # refuses because its Provision promise is broken, or because the
        # platform cannot say WHICH agent holds the mandate, is a defect on our
        # side of the wire: a declaration and a call site disagree, or no
        # resolver/binding is reachable. It reached users as
        # ``pdfclean_error`` / "Please try again or adjust your settings." —
        # a NEW error type per route for ONE failure class, telling a user to
        # change settings that cannot possibly fix it (live incident: every
        # ``pdf.content_cleaner`` run, request a89b3d83).
        #
        # Matched by class NAME, like every entry here — matrx-connect neither
        # imports nor depends on matrx-ai or aidream.
        frozenset(
            {
                "BrokenOfferPromise",  # matrx_ai.mandates
                "ProvisionInputError",  # aidream.services.mandates.provisions
            }
        ),
        FailureClass(
            error_type="mandate_contract_broken",
            user_message=(
                "This step could not run because two parts of our system "
                "disagree about what it was given. Nothing you did caused it "
                "and your work is saved — we have been alerted."
            ),
        ),
    ),
    (
        frozenset(
            {
                "MandateResolutionUnavailable",  # matrx_ai.mandates
                "MandateResolutionError",  # aidream.services.mandates.service
            }
        ),
        FailureClass(
            error_type="mandate_unresolved",
            user_message=(
                "We could not determine which AI agent should run this step, "
                "so nothing was run or charged. Nothing you did caused it and "
                "your work is saved — we have been alerted."
            ),
        ),
    ),
    (
        frozenset({"InsufficientPrivilegeError"}),
        FailureClass(
            error_type="database_permission_denied",
            user_message=(
                "The server was refused access to something it needed. "
                "Nothing you did caused it and your work is saved — we have "
                "been alerted."
            ),
        ),
    ),
)


def strip_ansi(text: str) -> str:
    """Remove terminal color escapes from anything bound for a client."""
    return _ANSI_RE.sub("", text)


def stable_error_type(debug_label: str) -> str:
    """Derive a GROUPABLE error type from a run's debug label.

    ``VisionInterview:72175649`` → ``visioninterview_error``. Per-run
    identifiers are dropped so one failure class is one error type, however
    many sessions hit it.
    """
    parts = [p for p in _LABEL_SPLIT_RE.split(debug_label.lower()) if p]
    kept = [p for p in parts if not _ID_SEGMENT_RE.match(p)]
    # A label made ENTIRELY of identifiers still needs a name; fall back to the
    # raw (sanitised) label rather than emitting a bare "_error".
    slug = "_".join(kept or parts) or "stream"
    return f"{slug}_error"


def classify_infrastructure_failure(exc: BaseException) -> FailureClass | None:
    """Recognize a server-side infrastructure failure, or None if unknown.

    Walks the exception's class hierarchy AND its ``__cause__``/``__context__``
    chain: a service that wraps a DB error in its own type must still classify,
    or the wrapper silently reintroduces the anonymous failure.
    """
    for candidate in _exception_chain(exc):
        names = {klass.__name__ for klass in type(candidate).__mro__}
        for recognized, failure in _INFRASTRUCTURE_CLASSES:
            if names & recognized:
                return failure
    return None


def _exception_chain(exc: BaseException, *, limit: int = 10) -> list[BaseException]:
    chain: list[BaseException] = []
    seen: set[int] = set()
    current: BaseException | None = exc
    while current is not None and len(chain) < limit and id(current) not in seen:
        seen.add(id(current))
        chain.append(current)
        current = current.__cause__ or current.__context__
    return chain
