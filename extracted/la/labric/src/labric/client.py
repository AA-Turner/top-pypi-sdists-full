"""Labric and AsyncLabric: the SDK clients used by everyone importing this package."""

# Hand-written and listed in `.fernignore`, so Fern regeneration leaves this file alone.
# That's what lets the helpers below be reached as `client.write_labric_table(...)`
# rather than `write_labric_table(client, ...)`.

from .base_client import AsyncBaseLabric, BaseLabric
from .read_wrappers import ReadWrappers
from .step_recording import StepRecording
from .write_wrappers import WriteWrappers


class Labric(ReadWrappers, StepRecording, WriteWrappers, BaseLabric):
    """Synchronous client: the generated API plus read, write, and step-recording helpers."""

    # WriteWrappers is listed explicitly even though StepRecording already inherits
    # from it, so every mixin backing this client is visible here.


class AsyncLabric(AsyncBaseLabric):
    """Asynchronous client. The hand-written helpers above are synchronous only and not included here."""
