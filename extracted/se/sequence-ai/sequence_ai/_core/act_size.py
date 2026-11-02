"""
A robot's observation: warned once a session when it is big.

In one sentence: the size of each observation as it goes up (its msgpack frame, observe_stream.ObserveStream.put) → past
1 MB, one warning a session (DirectConnection): how big it was, and how camera frames go smaller. Nothing is refused or
changed: it goes as it is.
WHY on the robot: an observation's upload grows with its size - each pays it, on every step - and nothing else says so;
the robot knows the number before it sends.



An observation's says too what a robot can do now to send camera frames smaller, sequence_ai.Video, and nothing of what
the platform may do with observations later.

WHY one threshold: a policy's inputs are its own (the robot-arm preset and the cameras it declared went with train bt),
so nothing declares what a policy reads of them to hold one to.

"""
from __future__ import annotations

from .warn import warn


OWN_INPUTS_BYTES = 1024 * 1024


def size_words(n: float) -> str:
    """A size as a reader takes it in: "2.4 MB", "160 KB", "900 bytes"."""
    if n >= 1024 * 1024:
        return f"{n / 1024 / 1024:.1f} MB"
    if n >= 1024:
        return f"{n / 1024:.0f} KB"
    return f"{int(n)} bytes"


class Observations:
    """A session's observations held to OWN_INPUTS_BYTES as each goes up: the first past it said, once a session, on the
    robot's own thread (observe() hands each to the stream there). It holds nothing of the connection - a stream's thread
    holds it, and a connection the robot dropped must still be collected - and goes with the session to each stream it
    makes, so a reconnect does not say it again."""

    def __init__(self, model: str) -> None:
        self.model = model
        self.said = False

    def __call__(self, sent: int) -> None:
        if self.said or sent <= OWN_INPUTS_BYTES:
            return
        self.said = True
        warn(f"{self.model}: an observation sent {size_words(sent)}, past {size_words(OWN_INPUTS_BYTES)} - to send "
             "camera frames smaller, wrap each in sequence_ai.Video, which sends them as compressed video "
             '(pip install -U "sequence-ai[observe]")')
