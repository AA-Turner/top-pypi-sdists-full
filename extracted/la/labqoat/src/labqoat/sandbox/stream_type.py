"""Where a sandbox process's standard streams go."""

import enum


class StreamType(enum.Enum):
    """A stream piped to the caller, merged into standard output, or discarded.

    ``PIPE`` is every stream's default: standard input takes what the caller writes and the outputs are kept
    for the caller to read. ``STDOUT`` sends standard error into standard output, in the order written.
    ``DEVNULL`` gives standard input nothing to read, or discards an output.
    """

    PIPE = "pipe"
    STDOUT = "stdout"
    DEVNULL = "devnull"
