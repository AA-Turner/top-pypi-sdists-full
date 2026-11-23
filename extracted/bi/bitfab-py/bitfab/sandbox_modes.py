from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from bitfab.github_sandbox import GITHUB_SANDBOX_NAME, github_sandbox
from bitfab.gmail_live import (
    READ_REAL_WRITE_FAKE,
    GmailCredentials,
    LiveGmail,
    Transport,
    answer_live_gmail_call,
    start_live,
)
from bitfab.gmail_sandbox import (
    GMAIL_SANDBOX_NAME,
    answer_gmail_call,
    as_mailboxes,
    is_gmail_call,
    mailbox_from_recorded_calls,
)
from bitfab.mock_override import MockOverrideCtx
from bitfab.sandbox import (
    Sandbox,
    SandboxStartCtx,
    combine_sandboxes,
    without_sandbox,
)
from bitfab.slack_calls import install as install_slack_interception
from bitfab.slack_sandbox import (
    SLACK_SANDBOX_NAME,
    build_slack_sandbox,
    urllib_transport,
)
from bitfab.slack_sandbox import Transport as SlackTransport

RECORDED = "recorded"
SandboxModeSetting = bool | str


def _stored_mode(value: Any) -> str:
    if isinstance(value, dict) and value.get("mode") == READ_REAL_WRITE_FAKE:
        return READ_REAL_WRITE_FAKE
    return RECORDED


def _refuse_other_mode(value: Any, mode: str) -> None:
    stored = _stored_mode(value)
    if stored != mode:
        raise ValueError(
            f'The sandbox store holds a Gmail mailbox from mode="{stored}", and '
            f'this replay runs the Gmail sandbox in mode="{mode}". Replay in '
            f'mode="{stored}", or seed the store\'s Gmail entry again.'
        )


def _load_live(_ctx: SandboxStartCtx, value: Any) -> Any:
    _refuse_other_mode(value, READ_REAL_WRITE_FAKE)
    return value


def _load_recorded(ctx: SandboxStartCtx, value: Any) -> Any:
    _refuse_other_mode(value, RECORDED)
    return as_mailboxes(ctx, value)


def gmail_sandbox(
    start: Callable[[SandboxStartCtx], Any] | None = None,
    account: Callable[[Any], str | None] | None = None,
    mode: str = RECORDED,
    credentials: GmailCredentials | None = None,
    _transport: Transport | None = None,
) -> Sandbox:
    """The Gmail sandbox: answers Gmail API calls during replay, never sending one to Google.

    It answers calls made through Google's Python client
    (``googleapiclient``), keeping sends, drafts and label changes in the
    sandbox for the rest of the replay item, along with trashed, deleted
    and relabeled messages and threads. It is on by default in
    ``"recorded"`` mode; pass it to change its mode or where its mailbox
    comes from, or turn its mode on with
    ``replay(sandbox_modes={"gmail": True})``.

    Args:
        start: ``"recorded"`` mode only. Builds the mailbox for one replay
            item from a ``SandboxStartCtx``. Return a list of messages, or
            ``{"messages": [...], "emailAddress": ..., "drafts": [...],
            "labels": [...], "sendAs": [...]}``. ``labels`` are the account's
            own labels, each a Gmail label or a name; ``sendAs`` are Gmail
            send-as entries (``sendAsEmail``, ``displayName``, ``signature``,
            ...). Without ``sendAs``, the account's address is listed with no
            signature.
            ``clock`` (ISO 8601) is where the mailbox's time starts, in place
            of the original trace's start time.
            Each message is a Gmail API message or plain fields as
            ``gmail_message`` takes them; a plain ``account`` field puts the
            message in that account's mailbox. Each draft is
            ``{"id": ..., "message": ...}``, where the message is a Gmail API
            message (as ``drafts.get`` returns it, ``raw`` included), plain
            fields, or only the ``id`` of a message in ``messages``. For several accounts, return
            ``{"mailboxes": [{"emailAddress": ..., "messages": [...]}]}``.
            ``None`` uses ``mailbox_from_recorded_calls``.
        account: With several mailboxes, names the account a call is for
            from the Google credentials it was made with, returning the
            account's address. ``None`` routes by a ``userId`` that is an
            address, then by the credential the original calls used, then
            to the only mailbox; a call it cannot place fails the item.
        mode: ``"recorded"`` (default) answers every call from a mailbox
            built from the original trace. ``"read-real-write-fake"`` reads
            the account's real mailbox as it stood when the original trace
            started (searches get a ``before:`` that time, newer messages are
            hidden, and relative dates such as ``newer_than:2d`` count back
            from it) and keeps every write in the sandbox, shown on later
            reads. Each mailbox's ``liveReads`` on the replay trace lists the
            reads that went to Gmail. A call for an account with no
            credential, or one Google refuses, fails the replay item, even
            when the replayed code catches the error.
        credentials: ``"read-real-write-fake"`` mode only. The OAuth refresh
            token for each mailbox, as a mapping from address to credential
            or a function taking an address and returning one (``None`` when
            it has none). A credential is a refresh token, a mapping or
            object with ``refresh_token``, ``client_id``, ``client_secret``
            and optional ``token_uri`` (a ``google.oauth2.credentials.
            Credentials`` works), and needs the ``gmail.readonly`` scope. A
            bare token takes its client from ``BITFAB_GMAIL_CLIENT_ID`` and
            ``BITFAB_GMAIL_CLIENT_SECRET``. ``None`` reads the
            ``BITFAB_GMAIL_CREDENTIALS`` environment variable, a JSON object
            mapping address to credential. Credentials and access tokens are
            never written to spans, sandbox state, or the replay trace.
    """
    if mode == READ_REAL_WRITE_FAKE:
        if start is not None:
            raise ValueError(
                f'gmail_sandbox(start=...) builds a recorded mailbox; mode="'
                f'{READ_REAL_WRITE_FAKE}" reads the real one instead. Pass one '
                "or the other."
            )
        live = LiveGmail(credentials, _transport)
        return Sandbox(
            name=GMAIL_SANDBOX_NAME,
            match=is_gmail_call,
            handle=lambda state, call: answer_live_gmail_call(
                state, call, account, live
            ),
            start=start_live(live),
            integration="gmail",
            mode=READ_REAL_WRITE_FAKE,
            load=_load_live,
            is_write=is_gmail_write,
        )
    if mode != RECORDED:
        raise ValueError(
            f"The Gmail sandbox has no mode {mode!r}. Its modes are "
            f"{', '.join(repr(m) for m in GMAIL_MODES)}."
        )
    if credentials is not None:
        raise ValueError(
            f'gmail_sandbox(credentials=...) is for mode="{READ_REAL_WRITE_FAKE}"; '
            f'mode="{RECORDED}" never reads the real mailbox.'
        )
    chosen = start or mailbox_from_recorded_calls
    return Sandbox(
        name=GMAIL_SANDBOX_NAME,
        match=is_gmail_call,
        handle=lambda state, call: answer_gmail_call(state, call, account),
        start=lambda ctx: as_mailboxes(ctx, chosen(ctx)),
        integration="gmail",
        mode=RECORDED,
        load=_load_recorded,
        is_write=is_gmail_write,
    )


GMAIL_MODES = (READ_REAL_WRITE_FAKE, RECORDED)
GMAIL_READ_VERBS = frozenset({"get", "list", "getProfile"})


def is_gmail_write(call: MockOverrideCtx) -> bool:
    return call.node.trace_function_key.rsplit(".", 1)[-1] not in GMAIL_READ_VERBS


def slack_sandbox(
    token: str | None = None,
    api_url: str | None = None,
    mode: str = READ_REAL_WRITE_FAKE,
    start: Callable[[SandboxStartCtx], Any] | None = None,
    _transport: SlackTransport | None = None,
) -> Sandbox:
    """The Slack sandbox: answers Slack Web API calls during replay, never sending a write to Slack.

    It answers calls made through ``slack_sdk``'s ``WebClient`` and
    ``AsyncWebClient`` and calls made with ``requests`` to ``slack.com/api``.
    Reads go to the real workspace as it stood when the original trace
    started: channel history and thread replies stop at that time, and search
    results after it are dropped. Messages, edits, deletions, reactions, new
    conversations and file uploads stay in the sandbox for the rest of the
    replay item and show on later reads. A method it does not know is refused,
    and a missing or refused token fails the replay item, even when the
    replayed code catches the error.

    It is off until a replay asks for it, with
    ``replay(sandbox_modes={"slack": True})`` or by passing
    ``slack_sandbox(...)`` in ``sandboxes``.

    Args:
        token: ``"read-real-write-fake"`` mode only. The Slack token that
            reads the real workspace. ``None`` uses the ``BITFAB_SLACK_TOKEN``
            environment variable, and without that the token each replayed
            call was made with. It is never written to a span, the sandbox's
            state, or the replay trace.
        api_url: ``"read-real-write-fake"`` mode only. Where reads are sent.
            ``None`` reads from the URL each replayed call's client points
            at, which is ``https://slack.com/api/`` unless the client was
            given another.
        mode: ``"read-real-write-fake"`` (default) reads the real workspace
            as described above. ``"recorded"`` never reaches Slack and needs
            no token: it answers reads from the Slack calls the original
            trace recorded. Channel history and thread replies come from the
            messages the original run read, so a replay that reads them in a
            new way is still answered; any other read gets the recorded reply
            to the same call. A read the trace has nothing for fails the
            replay item. Writes stay in the sandbox in both modes.
        start: ``"recorded"`` mode only. Builds the workspace for one replay
            item from a ``SandboxStartCtx``. Return
            ``{"recordedChannels": {channel_id: [message, ...]},
            "recordedReads": [{"method": ..., "params": {...},
            "response": {...}}]}``; either key may be left out. ``None`` uses
            ``recorded_start_state``. A sandbox store's Slack entry takes the
            same shape.
    """
    if mode == RECORDED and (token is not None or api_url is not None):
        raise ValueError(
            f'slack_sandbox(token=..., api_url=...) are for mode="{READ_REAL_WRITE_FAKE}"; '
            f'mode="{RECORDED}" never reads the real workspace.'
        )
    if mode != RECORDED and start is not None:
        raise ValueError(
            f'slack_sandbox(start=...) builds a recorded workspace; mode="'
            f'{READ_REAL_WRITE_FAKE}" reads the real one instead. Pass one or the other.'
        )
    install_slack_interception()
    return build_slack_sandbox(
        token, api_url, _transport or urllib_transport, mode, start
    )


@dataclass(frozen=True)
class ServiceModes:
    sandbox_name: str
    default_mode: str
    modes: Mapping[str, Callable[[], Sandbox]]


SERVICE_MODES: dict[str, ServiceModes] = {
    "gmail": ServiceModes(
        sandbox_name=GMAIL_SANDBOX_NAME,
        default_mode=READ_REAL_WRITE_FAKE,
        modes={
            READ_REAL_WRITE_FAKE: lambda: gmail_sandbox(mode=READ_REAL_WRITE_FAKE),
            RECORDED: lambda: gmail_sandbox(mode=RECORDED),
        },
    ),
    "github": ServiceModes(
        sandbox_name=GITHUB_SANDBOX_NAME,
        default_mode=READ_REAL_WRITE_FAKE,
        modes={READ_REAL_WRITE_FAKE: github_sandbox},
    ),
    "slack": ServiceModes(
        sandbox_name=SLACK_SANDBOX_NAME,
        default_mode=READ_REAL_WRITE_FAKE,
        modes={
            READ_REAL_WRITE_FAKE: slack_sandbox,
            RECORDED: lambda: slack_sandbox(mode=RECORDED),
        },
    ),
}


def default_sandboxes() -> list[Sandbox]:
    return [gmail_sandbox(), github_sandbox()]


def _configured(service: str, setting: Any) -> Sandbox:
    found = SERVICE_MODES.get(service)
    if found is None:
        raise ValueError(
            f"sandbox_modes has no service {service!r}. Its services are "
            f"{', '.join(repr(s) for s in SERVICE_MODES)}."
        )
    if setting is False:
        return without_sandbox(found.sandbox_name)
    if setting is True:
        return found.modes[found.default_mode]()
    if not isinstance(setting, str):
        raise TypeError(
            f"sandbox_modes[{service!r}] must be True, False, or a mode name, "
            f"not {type(setting).__name__}."
        )
    build = found.modes.get(setting)
    if build is None:
        raise ValueError(
            f"The {found.sandbox_name} sandbox has no mode {setting!r}. Its modes "
            f"are {', '.join(repr(m) for m in found.modes)}."
        )
    return build()


def resolve_sandboxes(
    sandboxes: Sequence[Sandbox] | None,
    sandbox_modes: Mapping[str, SandboxModeSetting] | None,
) -> list[Sandbox]:
    configured = [
        _configured(service, setting)
        for service, setting in (sandbox_modes or {}).items()
    ]
    passed = {sandbox.name for sandbox in sandboxes or []}
    both = sorted(passed & {sandbox.name for sandbox in configured})
    if both:
        raise ValueError(
            f"The {', '.join(both)} sandbox is set in both sandboxes and "
            "sandbox_modes; set it in one of them."
        )
    return combine_sandboxes([*(sandboxes or []), *configured], default_sandboxes())
