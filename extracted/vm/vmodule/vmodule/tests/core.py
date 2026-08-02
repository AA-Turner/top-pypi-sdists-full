import io
import logging
import re
import unittest

import vmodule

LOG_LINE_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} ", re.M)
LOG_LINE_NUMERIC_LINE_RE = re.compile(r"^([A-Z0-9_]+\s+[a-z_.]+:)\d+(?= )", re.M)


def log_some_messages() -> None:
    logging.getLogger("a.b.c").warning("Warn")
    logging.getLogger("a.b.c").info("Info")
    logging.getLogger("a.b.c").debug("Debug")
    logging.getLogger("x.y.z").log(vmodule.VLOG_1, "Vlog %d", 1)
    logging.getLogger("x.y.z").log(vmodule.VLOG_2, "Vlog %d", 2)


class CoreTest(unittest.TestCase):
    def test_defaults(self) -> None:
        # let basicConfig do its work
        del logging.root.handlers[:]
        # clear out anything that might have leaked in from another test
        logging.Logger.manager.loggerDict = {}

        stream = io.StringIO()
        vmodule.vmodule_init(None, "", stream=stream)

        log_some_messages()

        output = LOG_LINE_TIMESTAMP_RE.sub("", stream.getvalue())
        output = LOG_LINE_NUMERIC_LINE_RE.sub(lambda m: (m.group(1) + "<n>"), output)
        self.assertEqual(
            """\
WARNING  a.b.c:<n> Warn
""",
            output,
        )

    def test_root_verbosity_zero_is_info(self) -> None:
        # let basicConfig do its work
        del logging.root.handlers[:]
        # clear out anything that might have leaked in from another test
        logging.Logger.manager.loggerDict = {}

        stream = io.StringIO()
        vmodule.vmodule_init(0, "", stream=stream)

        log_some_messages()

        output = LOG_LINE_TIMESTAMP_RE.sub("", stream.getvalue())
        output = LOG_LINE_NUMERIC_LINE_RE.sub(lambda m: (m.group(1) + "<n>"), output)
        self.assertEqual(
            """\
WARNING  a.b.c:<n> Warn
INFO     a.b.c:<n> Info
""",
            output,
        )

    def test_root_verbosity(self) -> None:
        # let basicConfig do its work
        del logging.root.handlers[:]
        # clear out anything that might have leaked in from another test
        logging.Logger.manager.loggerDict = {}

        stream = io.StringIO()
        vmodule.vmodule_init(1, "", stream=stream)

        log_some_messages()

        output = LOG_LINE_TIMESTAMP_RE.sub("", stream.getvalue())
        output = LOG_LINE_NUMERIC_LINE_RE.sub(lambda m: (m.group(1) + "<n>"), output)
        self.assertEqual(
            """\
WARNING  a.b.c:<n> Warn
INFO     a.b.c:<n> Info
VLOG_1   x.y.z:<n> Vlog 1
""",
            output,
        )

    def test_vmodule_verbosity(self) -> None:
        # let basicConfig do its work
        del logging.root.handlers[:]
        # clear out anything that might have leaked in from another test
        logging.Logger.manager.loggerDict = {}

        stream = io.StringIO()
        vmodule.vmodule_init(None, "x.y.z=1", stream=stream)

        log_some_messages()

        output = LOG_LINE_TIMESTAMP_RE.sub("", stream.getvalue())
        output = LOG_LINE_NUMERIC_LINE_RE.sub(lambda m: (m.group(1) + "<n>"), output)
        self.assertEqual(
            """\
WARNING  a.b.c:<n> Warn
VLOG_1   x.y.z:<n> Vlog 1
""",
            output,
        )

    def test_debug_is_ten(self) -> None:
        # let basicConfig do its work
        del logging.root.handlers[:]
        # clear out anything that might have leaked in from another test
        logging.Logger.manager.loggerDict = {}

        stream = io.StringIO()
        vmodule.vmodule_init(10, "", stream=stream)

        log_some_messages()

        output = LOG_LINE_TIMESTAMP_RE.sub("", stream.getvalue())
        output = LOG_LINE_NUMERIC_LINE_RE.sub(lambda m: (m.group(1) + "<n>"), output)
        self.assertEqual(
            """\
WARNING  a.b.c:<n> Warn
INFO     a.b.c:<n> Info
DEBUG    a.b.c:<n> Debug
VLOG_1   x.y.z:<n> Vlog 1
VLOG_2   x.y.z:<n> Vlog 2
""",
            output,
        )
