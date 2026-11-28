"""
sequence_ai: SequenceLink, open source. Serve a robot policy from a GPU, and connect a robot to it.

A policy is a class with @seq.policy, @seq.sample and @seq.infer, which `seq serve` serves from a GPU. On the robot,
connect() opens one connection to it and hands back a Policy: your robot hands it what it observes (observe), asks for
the next action chunk when your own code says so (act), and plays the chunk its own way, at its own rate.

    import sequence_ai

    with sequence_ai.connect("http://your-gpu:8000") as policy_user:   # the GPU where `seq serve` runs
        policy_user.wait_until_ready()                                 # once, before the robot moves
        policy_user.observe(observation_user)                          # as the robot makes it; never blocks
        actions_user = policy_user.act()["actions"]                    # the next chunk; its first dimension is time
        for step_user in actions_user:                                 # played by your code, at your rate
            robot_user.apply(step_user)

Two brains, one string between them
A VLM looks at a snapshot, decides *what* to do next, and says it in a sentence. This package is
the *how*. The two halves run at completely different speeds (the brain thinks between
subtasks, the arm needs a chunk of motion every second), and that sentence is their entire
interface: the robot hands it to its policy with what it observes, as any input,
policy.observe({"instruction": ..., ...}), so the brain's clock never holds the arm's, and
`interrupt()` lets the brain change its mind mid-wait.

    slow brain   sequence_ai.chat()          messages in, one message out
    fast brain   this package                policy.observe(x); policy.act()

Wiring the two together (retries, failure detection, choosing the next sub-goal) is yours. This
package provides inference, not orchestration.

What it does for you
Three things, each of them work a loop written straight against the HTTP endpoints has to get
right before it behaves properly on a robot:

    keeps the connection open      184.9 ms of handshake otherwise paid on every call,
                                   60% of a bare request  (see _transport.py)
    classifies errors              `warming` with a retry_after_s is "wait 118 s"; a plain
                                   Unavailable is "stop": opposite instructions (see errors)
    one driver per Policy          two threads acting through one handle interleave its
                                   episodes (see Policy._driving)

And `interrupt()` cuts through an act waiting on a starting worker or a slow answer, so stop
latency is never a property of the service (see Policy.interrupt).

Each was measured, and the cited modules carry the measurements.

Safety
An action returned by any model is model output, not a safe robot command. This library does
not check joint limits, reachability, collisions, velocity, or anything else. Bounds
checking and an e-stop belong between this library and your motors. connect(on_stale=) is told
the moment the arm runs out of answer, so that you can hold it; it is no emergency stop, which stays physical.

Teleoperation
A person drives a robot from a console, straight to it: `seq teleop serve` pairs the two, on the robot's machine or one
both can reach - the robot connects to its address, connect("http://<that machine>:8200", token=...), and a console
with teleop("http://<that machine>:8200", token=...) or the page it serves. Needs sequence-ai[teleop].

── On GS's platform ──────────────────────────────────────────────────
A deployment by its name - connect("my_policy_user") - a robot paired through the platform by its key
(connect("teleop"), teleop(key=...)), the platform's recorder, models - its text to speech among them, speech() -
your account, GPUs, billing and usage are
sequence-cloud's, GS's client for its platform, which `pip install sequence-ai` installs with it on Python 3.10 or
later, your key in SEQUENCES_API_KEY.
"""

from __future__ import annotations

import importlib.util
import re
import types
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Iterator




from ._core.direct import DirectConnection
from ._core.encode import DEFAULT_JPEG_QUALITY, encode, image_size, resize_image
from ._core.plugins import INSTALL, first, needs_cloud
from ._core.recorder import Recorder
from ._core.stale import Stale
from .act import Interrupted, Policy, Ready
from .chat import ChatResult, ChatStream, Conversation, cached, chat, image

from .markers import Depth, Tactile, Video

if TYPE_CHECKING:
    from ._core.teleop import Teleop
    from .act.teleop_handle import TeleopHandle

from .errors import (
    AuthError,
    CertPinError,
    Conflict,
    NewVersion,
    Gone,
    InternalError,
    InvalidRequest,
    MissingPackage,
    NotFound,
    OutOfCredit,
    PermissionDenied,
    PolicyError,
    SequencesError,
    StreamRefused,
    Unavailable,
    from_response,
)

__all__ = [
    "connect",
    "teleop",
    "Teleop",
    "TeleopHandle",
    "read_record",
    "Recorder",
    "Video",
    "Depth",
    "Tactile",
    "chat",
    "Conversation",
    "image",
    "cached",
    "encode",
    "resize_image",
    "image_size",
    "DEFAULT_JPEG_QUALITY",
    "Policy",
    "Interrupted",
    "Ready",
    "Stale",
    "ChatResult",
    "ChatStream",
    "SequencesError",
    "InvalidRequest",
    "AuthError",
    "PermissionDenied",
    "OutOfCredit",
    "NotFound",
    "Conflict",
    "NewVersion",
    "Gone",
    "Unavailable",
    "PolicyError",
    "InternalError",
    "CertPinError",
    "StreamRefused",
    "MissingPackage",
    "from_response",
]


_CLOUD_NAMES = frozenset((
        "record", "models", "account", "gpu", "gpus", "billing", "usage", "fleet", "decide", "DecideResult", "Model",
        "speech", "SpeechResult",
        "GpuBadRequest", "GpuOverLimit", "GpuNoCard", "DEFAULT_BASE_URL", "Transport",
))

_ASK_S = 3.0











try:
    from importlib.metadata import version as _pkg_version

    __version__ = _pkg_version("sequence-ai")
except Exception:


    __version__ = "dev"


def connect(
    model: str,
    *more: str,
    api_key: str | None = None,
    base_url: str | None = None,
    timeout_s: float | None = None,
    startup_timeout_s: float | None = None,
    token: str | None = None,
    follow: str | None = None,
    on_warming: Callable[[float, float], None] | None = None,
    on_queue: Callable[[Any, Any, float, Any], None] | None = None,
    on_stale: Callable[[Stale], None] | None = None,
    on_resume: Callable[[Stale], None] | None = None,
    hold: Any = None,
    lines: list[str] | dict[str, str] | None = None,
    pictures: str = "keyframes",
) -> Policy | Any:
    """
    Open the robot's connection to a policy server of your own - `seq serve` - by its address:
    connect("http://your-gpu:8000"). What comes back is a Policy: observe() hands it what the robot observes as it makes
    it, a sequence_ai.Video item as video, and act() asks what to do when your code says so - on one stream straight to
    that server, nothing in between: no key, no account, nothing billed.

    What act() returns is what the policy's own act function returned: nothing converts it. What it means - joint
    velocities, deltas, absolute targets - is the policy's own, and the robot's code turns it into commands.


    model       the server's address, http:// or https:// (an address written without it is refused: as a name, it would
                go to GS's platform) - a policy server's (seq serve), or a teleop server's (seq teleop serve): asked
                which as connect() is called (its GET /ping, 3 s at most), and taken for a policy server's while it
                does not answer
    token       the server's token (seq serve --token, seq teleop serve --token), sent with each request to it; only as
                given here: nothing reads it from the environment
    hold        a teleop server's robot: what act() hands back while no person drives it, or one stopped it (None
                unset); a policy server's has no use for it
    timeout_s   how long one request waits for its answer, in seconds
    startup_timeout_s, on_warming, on_stale, on_resume
                how long an act waits for a server that is starting, and what it is told as it waits or as the answer the
                robot plays runs out and the next comes
    lines       the robot's uplinks, two or more, by network interface - a satellite terminal's and a cellular modem's,
                say: lines=["eth0", "wwan0"]. Its stream goes over each, each observation and act on every one, and
                an act's first answer is the one used; a line that drops leaves everything to the others while it
                opens again. Every line carries the whole upload. To a server of your own, a dict gives each line its
                own address of it: {"eth0": "http://[2001:db8::7]:8000", "wwan0": "http://203.0.113.7:8000"}. Each
                line's numbers are in stats()["lines"]. Linux 5.7 or later, or macOS
    pictures    what observe() does with a camera picture you did not mark (an HxWx3 uint8 array, each side 32 pixels
                or more): "keyframes", the default - each one sent as a video keyframe of its own, lossy, a small part
                of its bytes - or "exact", every byte as it is. A marked item goes as its marker says
                (sequence_ai.Video, Depth, Tactile); sending a picture as video needs Python 3.10 or later
                (3.11 on Windows ARM64), and without it it goes as it is, said once
    follow, base_url
                a GPU rented on GS's platform: its follow token and the platform's address (sequence-cloud's)
    *more, api_key, on_queue
                a deployment on GS's platform by its name, connect("my_policy_user"), and its options: sequence-cloud's,
                which comes with sequence-ai on Python 3.10 or later (sequence_cloud.api.by_name says them all)

    Use it as a context manager: a Policy that is never closed leaks a socket.

        with sequence_ai.connect("http://my-gpu_user:8000") as policy_user:
            policy_user.observe(frame_user)
            actions_user = policy_user.act()

    connect() asks the address what it serves, and nothing more: the first observe() or act() opens the stream, and
    wait_until_ready() waits for a server that is still starting. A robot names nothing of the policy's: its control
    rate, how many steps of an answer are valid and when the next is asked for are the policy's to declare
    (@seq.policy(hz=, action_chunk_valid_len=, action_chunk_replan_at=)), and what differs between robots goes in their
    observations.

    At a teleop server's address, what comes back is a TeleopHandle - the robot's own handle while a person drives it,
    with no policy behind it: observe() sends each step to the consoles connected, and act() hands back the newest chunk
    its person sent, once, or `hold`. The same robot code runs paired through GS's platform, connect("teleop",
    api_key=...) with sequence-cloud, this one line changed.

        with sequence_ai.connect("http://robot-box_user:8200", token=TOKEN_user) as robot_user:
            robot_user.wait_until_ready()
            robot_user.observe(frame_user)
            chunk_user = robot_user.act()          # a person's newest chunk, or None while no one drives it
    """
    for name in (model, *more):
        _not_an_address(name)
    if lines is not None:
        lines = _lines_of(lines, address="://" in model)
    from ._core.marked_observe import PICTURES

    if pictures not in PICTURES:
        raise InvalidRequest(f"pictures= is one of {', '.join(map(repr, PICTURES))}, not {pictures!r}")
    if "://" in model:

        unused = [name for name, given in (("api_key", api_key), ("on_queue", on_queue)) if given is not None]
        if unused:
            raise InvalidRequest(f"{unused[0]}= is the platform's, and {model} is a server of your own: it is reached "
                                 "with its token= (seq serve --token), and it has no line to wait in")
        return _own_server(model, more, timeout_s, token, follow=follow, base_url=base_url, lines=lines,
                           pictures=pictures, startup_timeout_s=startup_timeout_s, on_warming=on_warming,
                           on_stale=on_stale, on_resume=on_resume, hold=hold)
    api = first("sequence_ai.api")
    if api is None:
        raise MissingPackage(f"connect({model!r}) names a deployment on GS's platform: an address of a server of your "
                             "own is http://... - a name is sequence-cloud's, GS's client for its platform",
                             hint=INSTALL)
    return api.by_name(model, *more, api_key=api_key, base_url=base_url, timeout_s=timeout_s,
                       startup_timeout_s=startup_timeout_s, token=token, follow=follow, on_warming=on_warming,
                       on_queue=on_queue, on_stale=on_stale, on_resume=on_resume, hold=hold, lines=lines,
                       pictures=pictures)


def _own_server(url: str, more: tuple, timeout_s: float | None, token: str | None = None, *,
                follow: str | None = None, base_url: str | None = None,
                lines: list[str] | dict[str, str] | None = None, pictures: str = "keyframes",
                startup_timeout_s: float | None = None, on_warming: Callable[[float, float], None] | None = None,
                on_stale: Callable[[Stale], None] | None = None,
                on_resume: Callable[[Stale], None] | None = None, hold: Any = None) -> Policy | Any:
    """connect()'s way to a server of your own - a teleop server's address, what it says it is (_served), to
    _own_teleop - and to a policy server of your own: the platform's own Policy on its address - the same robot's stream,
    its control plane answered here (_core/own_server.OwnGateway) - and nothing of the platform asked or told: `token`,
    given, is sent to it (serve(token=...)), never an api_key - a script whose address is changed to another's server
    would hand that server the account's key. Its follow token (`follow`, else $SEQUENCES_FOLLOW_TOKEN), where it has
    one, goes to the platform's gateway alone, before the connection: the robot's own address let into the GPU's allow
    list (sequence-cloud's api.follow), and again as the robot connects anew after the GPU stopped answering it.
    
"""
    if more:
        raise InvalidRequest(f"a policy server of your own is connected to alone: connect({url!r}) takes no other name")
    from urllib.parse import urlsplit, urlunsplit

    from ._core.warn import warn

    parts = urlsplit(url)
    if parts.path not in ("", "/") or parts.query or parts.fragment:

        bare = urlunsplit((parts.scheme, parts.netloc, "", "", ""))
        warn(f"connect(): {url} has a path, which a server's address does not take: connecting to {bare}")
        url = bare
    teleop_server, pinged = _served(url, token, timeout_s)
    if teleop_server:
        if lines is not None or follow:
            what = "lines=" if lines is not None else "follow="
            raise InvalidRequest(f"{what} goes with a policy server: {url} is a teleop server's (seq teleop serve), "
                                 "whose robot is reached on one line, as its console reaches it")
        return _own_teleop(url, token, hold)
    if hold is not None:
        raise InvalidRequest(f"hold= is what act() hands back while no person drives the robot: it goes with a teleop "
                             f"server's address (seq teleop serve), and {url} is a policy server's")
    from ._core.own_server import OwnGateway



    api = first("sequence_ai.api")
    if api is None and follow:
        raise MissingPackage("follow= lets this robot into a GPU rented on GS's platform: sequence-cloud's, "
                             "GS's client for its platform", hint=INSTALL)
    on_reconnect = api.follow(follow, url, base_url, lines) if api is not None else None
    name = _named(pinged) or _name_of(url)
    gateway = OwnGateway(url, token=token, on_reconnect=on_reconnect, pinged=pinged)
    return Policy(DirectConnection(gateway, model=name, timeout_s=timeout_s, lines=lines, pictures=pictures),
                  model=name, startup_timeout_s=startup_timeout_s, on_warming=on_warming, on_stale=on_stale,
                  on_resume=on_resume)


def _served(url: str, token: str | None, timeout_s: float | None) -> tuple[bool, Any]:
    """What the server at `url` serves, as its GET /ping says it within _ASK_S: (True, None) for a teleop server's (seq
    teleop serve says X-Seq-Teleop), else (False, the answer) - a policy server's, or None where nothing answered:
    taken for a policy server that is starting, as connect() always took an address."""
    import httpx

    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        answer = httpx.get(f"{url}/ping", headers=headers, timeout=min(_ASK_S, timeout_s or _ASK_S))
    except httpx.HTTPError:
        return False, None
    return ("x-seq-teleop" in answer.headers), (None if "x-seq-teleop" in answer.headers else answer)


def _own_teleop(url: str, token: str | None, hold: Any) -> Any:
    """connect()'s way to a teleop server of your own (seq teleop serve): the robot's handle while a person drives it,
    its link to the server the one the platform's pairing takes (teleop_link.RobotLink), its token as given and nothing
    of an account's."""
    from ._core import teleop_direct, teleop_link, teleop_robot
    from .act.teleop_handle import TeleopHandle

    teleop_direct.require()
    driven = teleop_robot.Driven() if hold is None else teleop_robot.Driven(hold)
    link = teleop_link.RobotLink(token, url, driven, own=True)
    handle = TeleopHandle(driven, link)
    link.start()
    return handle


def teleop(url: str | None = None, *, token: str | None = None, key: str | None = None, operator: str | None = None,
           base_url: str | None = None, timeout_s: float | None = None, direct_only: bool = False,
           via: str = "webrtc") -> "Teleop":
    """
    A person's console for one robot: watch it, take it, drive it with action chunks, hand it back, stop it - connected
    straight to the robot, its pictures and commands reaching no server.

        with sequence_ai.teleop("http://robot-box_user:8200", token=TOKEN_user, operator="alice_user") as op_user:
            for step_user in op_user.stream():     # the robot's newest view: {"episode", "seq", "observation", "t_us"}
                ...
            op_user.take()                         # one person at a time: Conflict while another drives it
            op_user.send({"actions": chunk_user})  # the robot's next act() hands it back, at once
            op_user.release()                      # back to its model; op_user.stop() stops it where it is

    url         the teleop server the robot connected to (seq teleop serve): `token` its token, as given
    key, base_url
                a robot paired through GS's platform instead, by its own key (sequence-cloud's): `key` defaults to
                $SEQUENCES_API_KEY, `base_url` to $SEQUENCES_BASE_URL, then the platform's
    operator    the name this console goes by: who drives, in the robot's audit trail
    timeout_s   how long its server's answers may take, 10 s unset; meeting the robot takes 15 s at least
    direct_only no relay: where the two cannot meet directly, Unavailable rather than through a TURN server its teleop
                server names (seq teleop serve --turn); op.path says which way a connection went, "direct" or "relay"
    via         "webrtc" (the default): straight to the robot, to watch it and drive it. "moq": to watch it alone,
                through the MoQ relay its teleop server names (seq teleop serve --moq-port), the robot uploading once
                however many watch - stream(), states() and metrics() as below, and nothing to take or send;
                sequence-ai[moq], Python 3.10 or later

    It needs sequence-ai[teleop] (Python 3.11 or later): pip install 'sequence-ai[teleop]'. Conflict while the robot is
    not connected (details.reason "robot_not_connected"); Unavailable, saying why, where the two cannot reach each other
    (details.reason "direct_failed": both behind symmetric NAT, a network that lets no UDP out...): nothing goes any
    other way in its place. A console that drives the robot and goes - closed, or silent for 3 s - stops it; one that
    only watches changes nothing by going. stream() hands on the robot's newest view each time something new comes: at
    most 8 cameras are sent, in the order the robot first observes them, and a camera's frame may be a few steps from the
    arrays beside it, behind them or ahead. op.driver is who drives as the robot last said it - {"driver": "model",
    "human" or "stopped", "by": who, "since": its epoch second}. metrics() says how late its commands and the robot's
    steps were: p50, p95 and p99 of each, in microseconds.
    """
    if via not in ("webrtc", "moq"):
        raise InvalidRequest(f"via= is \"webrtc\" (straight to the robot) or \"moq\" (watching through a relay), not "
                             f"{via!r}")
    if via == "moq":
        unused = [name for name, given in (("operator", operator), ("direct_only", direct_only or None)) if given]
        if url is None:
            raise InvalidRequest("via=\"moq\" watches through the MoQ relay a teleop server of your own names (seq "
                                 "teleop serve --moq-port): teleop(\"http://ADDRESS:8200\", token=..., via=\"moq\")")
        if unused:
            raise InvalidRequest(f"{unused[0]}= is a driving console's: one watching through the relay is told to no "
                                 "one and goes no way but the relay's")
    if url is None:
        if token is not None:
            raise InvalidRequest("token= is a teleop server of your own's, given with its address: "
                                 "teleop(\"http://ADDRESS:8200\", token=...)")
        api = first("sequence_ai.api")
        if api is None:
            raise MissingPackage("teleop() with no address pairs through GS's platform, by the robot's key: "
                                 "sequence-cloud's, GS's client for its platform; a teleop server of your own is "
                                 "teleop(\"http://ADDRESS:8200\", token=...)", hint=INSTALL)
        return api.teleop_console(key=key, operator=operator, base_url=base_url, timeout_s=timeout_s,
                                  **({"direct_only": True} if direct_only else {}))
    if key is not None or base_url is not None:
        raise InvalidRequest(f"{'key=' if key is not None else 'base_url='} is the platform's, and {url} is a teleop "
                             "server of your own: it is reached with its token= (seq teleop serve --token)")
    _not_an_address(url)
    if "://" not in url:
        raise InvalidRequest(f"teleop() takes a teleop server's URL, http://... or https://..., not {url!r}")
    from ._core import teleop as _teleop
    from ._core import teleop_direct
    from ._core.transport import Transport

    if via == "moq":
        from ._core import teleop_moq

        teleop_moq.require()
        gateway = Transport(api_key=token, base_url=url.rstrip("/"), own=True, timeout_s=timeout_s or 10.0)
        try:
            return teleop_moq.Watch(gateway, timeout_s=timeout_s or 10.0)
        finally:
            gateway.close()
    teleop_direct.require()

    gateway = Transport(api_key=token, base_url=url.rstrip("/"), own=True,
                        timeout_s=max(timeout_s or 10.0, _teleop.PAIRING_WAIT_S + 10.0))
    try:
        return _teleop.Teleop(gateway, operator=operator, timeout_s=timeout_s or 10.0, direct_only=direct_only)
    finally:
        gateway.close()



_SCHEMELESS = re.compile(r"[^/]*:\d{1,5}|\d{1,3}(\.\d{1,3}){3}|localhost|\[[0-9a-fA-F:.]+\](:\d{1,5})?")


def _not_an_address(name: Any) -> None:
    """InvalidRequest for a name that is an address written without http://, before anything is asked of the
    platform: taken for a policy's name, it would go to the platform's gateway with the account's key."""
    if isinstance(name, str) and "://" not in name and _SCHEMELESS.fullmatch(name.strip()):
        raise InvalidRequest(f"{name!r} is an address, not a policy's name: did you mean "
                             f"connect(\"http://{name.strip()}\")? A policy server of your own is reached by its URL")


def _lines_of(lines: Any, *, address: bool) -> list[str] | dict[str, str]:
    """connect()'s `lines`, checked before anything opens: two or more network interfaces this machine has - a list, or,
    to a server of your own (`address`), a dict of each one's own address of it. InvalidRequest naming what is wrong.
    With "teleop" among the names, sequence-cloud's by_name refuses them: a console reaches its robot on one line."""
    from .network import bind as _bind

    if isinstance(lines, dict) and not address:
        raise InvalidRequest("lines= as a dict gives each line its own address of a server of your own; a policy "
                             "reached by its name is reached at the address the platform gives: "
                             "lines=[\"eth0\", \"wwan0\"]")
    names = list(lines)
    if len(names) < 2 or not all(isinstance(n, str) and n for n in names):
        raise InvalidRequest(f"lines= names two or more of this machine's network interfaces, and {lines!r} does not")
    for name in names:
        try:
            _bind.check(name)
        except OSError as e:
            raise InvalidRequest(f"lines=: {e}") from None
    if isinstance(lines, dict):
        bad = [n for n, to in lines.items() if not isinstance(to, str) or "://" not in to]
        if bad:
            raise InvalidRequest(f"lines=: each line's address is a URL, as connect()'s is; {bad[0]!r} has "
                                 f"{lines[bad[0]]!r}")
        return {n: to.rstrip("/") for n, to in lines.items()}
    return names


def _named(pinged: Any) -> str | None:
    """The policy a server of one's own names on its /ping (serve()'s "policy": seq serve's class and act function), as a
    name is written - the name its Policy goes by; None where its /ping did not answer 200, or named none."""
    try:
        said = pinged.json() if pinged is not None and pinged.status_code == 200 else None
    except ValueError:
        return None
    policy = said.get("policy") if isinstance(said, dict) else None
    if not isinstance(policy, str):
        return None
    return re.sub(r"[^A-Za-z0-9._-]+", "-", policy).strip("-._")[:64] or None


def _name_of(url: str) -> str:
    """The name a Policy on a server of one's own goes by where its /ping names no policy: its host and port, as a name
    is written ("10.0.0.5-8000")."""
    from urllib.parse import urlsplit

    parts = urlsplit(url)
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", f"{parts.hostname or 'server'}-{parts.port or ''}").strip("-._")
    return (name or "server")[:64]


def read_record(path: str) -> Iterator[dict[str, Any]]:
    """
    The items a recording file holds - what `seq robot record` wrote - in order, each as Recorder.steps() gave it: one
    msgpack map after another, which any msgpack reader reads too (its first map the file's header, "kind"
    "recording"). Read a chunk at a time, so a file of hours is never held whole.
    """
    from ._core import recorder as _recorder

    return _recorder.read(path)


def __getattr__(name: str) -> Any:
    """`sequence_ai.network` and `sequence_ai.engine` are imported when first used, so a robot that only connects loads
    neither; Teleop and TeleopHandle are loaded as first used too; and the platform's names (models, account, gpu, ...)
    are sequence-cloud's, there once it is installed.
    `serve` is none of them: `seq serve` serves a @seq.policy class, and runs sequence_ai.engine.serve to do it.
    """
    if name in ("network", "engine"):
        return importlib.import_module(f".{name}", __name__)
    if name == "Teleop":
        return importlib.import_module("._core.teleop", __name__).Teleop
    if name == "TeleopHandle":
        return importlib.import_module(".act.teleop_handle", __name__).TeleopHandle


    if name in _CLOUD_NAMES:
        api = first("sequence_ai.api")
        if api is not None and name in getattr(api, "__all__", ()):
            return getattr(api, name)
        raise AttributeError(needs_cloud(f"sequence_ai.{name}"))



    spec = None if name.startswith("__") else importlib.util.find_spec(f"{__name__}.{name}")
    if name.startswith("__") or (spec is not None and spec.origin is not None):
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    api = first("sequence_ai.api")
    if api is not None and name in getattr(api, "__all__", ()):
        return getattr(api, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__() -> list[str]:
    """What `dir(sequence_ai)` lists: the names it exports and its subpackages - with sequence-cloud installed, the
    platform's names it adds."""
    api = first("sequence_ai.api")
    modules = {n for n, v in globals().items() if isinstance(v, types.ModuleType) and not n.startswith("_")}
    added = set(getattr(api, "__all__", ())) if api is not None else set()
    return sorted(set(__all__) | modules | {"__version__"} | added)
