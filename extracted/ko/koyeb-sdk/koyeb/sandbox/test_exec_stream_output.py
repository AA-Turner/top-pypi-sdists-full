import unittest

from koyeb.sandbox.test_exec_raise_on_error import (
    FakeAsyncClient,
    FakeSyncClient,
    _exec,
    _exec_async,
)


def _out(data, **extra):
    return {"stream": "stdout", "data": data, **extra}


def _err(data, **extra):
    return {"stream": "stderr", "data": data, **extra}


class TestStreamedOutputKeepsLineBreaks(unittest.TestCase):
    """Buffered stdout/stderr from /run_streaming match what /run returns.

    The executor sends one event per line without its line ending, so the
    fold puts it back: the event's "eol" if present, "\\n" otherwise."""

    def run_both(self, events):
        sync = _exec(FakeSyncClient(events=events))
        async_ = _exec_async(FakeAsyncClient(events=events))
        self.assertEqual(
            (sync.stdout, sync.stderr, sync.exit_code),
            (async_.stdout, async_.stderr, async_.exit_code),
        )
        return sync

    def test_lines(self):
        result = self.run_both([_out("a"), _out("b"), _out("c"), {"code": 0}])
        self.assertEqual(result.stdout, "a\nb\nc\n")

    def test_blank_lines(self):
        result = self.run_both([_out("a"), _out(""), _out("b"), {"code": 0}])
        self.assertEqual(result.stdout, "a\n\nb\n")

    def test_no_trailing_newline_without_eol_gets_one(self):
        # Today's executors don't say whether the last line ended with "\n".
        result = self.run_both([_out("no newline at end"), {"code": 0}])
        self.assertEqual(result.stdout, "no newline at end\n")

    def test_stderr(self):
        result = self.run_both([_out("out"), _err("err"), _err("err2"), {"code": 3}])
        self.assertEqual(result.stdout, "out\n")
        self.assertEqual(result.stderr, "err\nerr2\n")
        self.assertEqual(result.exit_code, 3)

    def test_eol_is_used_when_sent(self):
        result = self.run_both(
            [
                _out("10%", eol="\r"),
                _out("20%", eol="\r"),
                _out("30% done", eol="\n"),
                _out("a", eol="\r\n"),
                _out("no newline at end", eol=""),
                _err("err", eol=""),
                {"code": 0},
            ]
        )
        self.assertEqual(result.stdout, "10%\r20%\r30% done\na\r\nno newline at end")
        self.assertEqual(result.stderr, "err")

    def test_callbacks_get_data_without_line_ending(self):
        events = [_out("a"), _out(""), _err("e", eol="\r"), {"code": 0}]
        calls = []
        result = _exec(
            FakeSyncClient(events=events),
            on_stdout=lambda d: calls.append(("out", d)),
            on_stderr=lambda d: calls.append(("err", d)),
        )
        self.assertEqual(calls, [("out", "a"), ("out", ""), ("err", "e")])
        self.assertEqual((result.stdout, result.stderr), ("", ""))


if __name__ == "__main__":
    unittest.main()
