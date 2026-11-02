"""
seq.port's error, in a module of its own: the porting commands raise it without importing numpy, which
seq.port.mujoco imports at its top - a command that stops for its arguments says why on a machine without numpy, where
importing the error with the engines had asked for all of sequence-ai[port] first.
"""
from __future__ import annotations

from seq.errors import SeqAuthoringError


class PortError(SeqAuthoringError, RuntimeError):
    """The benchmark cannot be exported, checked or scaffolded as asked; the message says why and what to do. An
    authoring error, so a command says it in one line and exits 2, not with a traceback."""
