"""Tests for _stream_subprocess_output."""

import io

from agentic_devtools.cli.setup.script_generators.required_setup import _stream_subprocess_output


class TestStreamSubprocessOutput:
    """Tests for _stream_subprocess_output."""

    def test_ignores_missing_stream(self) -> None:
        """A missing pipe is ignored without touching the sink or chunks."""
        sink = io.StringIO()
        chunks: list[str] = []

        _stream_subprocess_output(None, sink, chunks)

        assert sink.getvalue() == ""
        assert chunks == []

    def test_streams_content_to_sink_and_chunks(self) -> None:
        """A present stream is mirrored to the sink and captured in order."""
        stream = io.StringIO("line 1\nline 2\n")
        sink = io.StringIO()
        chunks: list[str] = []

        _stream_subprocess_output(stream, sink, chunks)

        assert sink.getvalue() == "line 1\nline 2\n"
        assert chunks == ["line 1\n", "line 2\n"]
        assert stream.closed is True
