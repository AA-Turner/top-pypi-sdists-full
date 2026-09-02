import json
import os.path
import sys
from collections import defaultdict

from coverage import CoverageData

from pytest_circleci_coverage._import_graph import import_edges, reachable_from

# Nodeids of the tests that reached their call phase.
_executed_nodeids = {}


def _format_context(context):
    # context: "nodeid|phase" e.g. "src/foo.py::TestClass::test_fn[p]|run"
    # output:  "src/foo.py!!src/foo.py::TestClass!!src/foo.py::TestClass::test_fn[p]|run"
    nodeid, phase = context.rsplit("|", 1)
    parts = nodeid.split("::")
    key = "!!".join("::".join(parts[: i + 1]) for i in range(len(parts)))
    return f"{key}|{phase}"


def pytest_addoption(parser):
    parser.addoption("--circleci-coverage", dest="circleci-coverage")


def _restart_monitoring_events(config):
    # coverage.py's sys.monitoring core (default on Python 3.14+) returns
    # DISABLE from its LINE callback, which silences each (code, lineno) after
    # the first hit. Re-enable events at each test setup so that all context
    # are recorded.
    if not config.getoption("circleci-coverage", default=None):
        return
    monitoring = getattr(sys, "monitoring", None)
    if monitoring is not None:
        monitoring.restart_events()


def pytest_sessionstart():
    _executed_nodeids.clear()


def pytest_runtest_setup(item):
    _restart_monitoring_events(item.config)


def pytest_runtest_logreport(report):
    # A project whose measured sources are all declarations records no context at
    # all, so the tests that ran cannot be recovered from the coverage data.
    # Gating on the call phase keeps skipped tests out.
    if report.when == "call":
        _executed_nodeids[report.nodeid] = True


def pytest_sessionfinish(session):
    try:
        output_path = session.config.getoption("circleci-coverage")
        if not output_path:
            # If the flag is not set, noop skip coverage reporting.
            return

        print("Generating CircleCI coverage JSON...")

        data = CoverageData()
        data.read()
        files = data.measured_files()

        if not files:
            print(
                "No coverage data found. "
                + "Ensure pytest is run with --cov and --cov-context=test flags.",
                file=sys.stderr,
            )
            return

        importers = {}
        if session.config.getoption("cov_context", default=None):
            importers = _importing_tests(data, files, session.config)

        has_contexts = False
        tests = {}
        for filename in files:
            contexts = data.contexts_by_lineno(filename=filename)

            rev = {}
            for lineno, contexts in contexts.items():
                for context in contexts:
                    if context and context.endswith("|run"):
                        key = _format_context(context)
                        rev.setdefault(key, []).append(lineno)
                        has_contexts = True

            # Coverage cannot credit a declaration to any test: it runs once, while
            # its module is imported, before the first test starts. Reading import
            # statements is the only way to tell which tests depend on one.
            for key in importers.get(os.path.abspath(filename), ()):
                rev.setdefault(key, [1])

            if rev:
                name = os.path.relpath(filename)
                tests[name] = rev

        if not has_contexts and not importers:
            print(
                "No coverage context data found. "
                + "Ensure pytest is run with --cov-context=test to enable context tracking.",
                file=sys.stderr,
            )
            with open(output_path, "w") as f:
                json.dump({}, f)

            print(f"Empty coverage data written to {output_path}")
            return

        with open(output_path, "w") as f:
            json.dump(tests, f)

        print(f"Coverage data written to {output_path}")

    except Exception as e:
        print(f"Unexpected error generating coverage data: {e}", file=sys.stderr)


def _importing_tests(data, files, config):
    """{file: the test keys that depend on it by importing it}.

    A test that only reads a constant or a model out of a module runs none of its
    lines, so importing it is the only evidence of the dependency.
    """
    keys_by_test_file, test_file_of = {}, {}
    for nodeid in _executed_nodeids:
        path = os.path.abspath(config.rootpath / nodeid.split("::")[0])
        keys_by_test_file.setdefault(path, []).append(_format_context(f"{nodeid}|run"))
        test_file_of[nodeid] = path
    if not keys_by_test_file:
        return {}

    conftests = _loaded_conftests(config)
    measured = {os.path.abspath(f) for f in files}
    edges = import_edges(measured | set(keys_by_test_file) | set(conftests))
    followed, reportable = _lines_run(data, files, edges, test_file_of)

    # Coverage says which edges a test ran into, but only for the files it
    # measured. A test file or conftest.py outside the --cov scope has no
    # coverage at all, and nothing else here is outside it, every other path
    # having come from the coverage data, so take every edge out of one.
    outside_scope = {
        path: set().union(*by_line.values())
        for path, by_line in edges.items()
        if path not in measured
    }

    importers = {}
    for test_file, keys in keys_by_test_file.items():
        # A conftest.py is imported by pytest rather than by the test, so it is
        # both a dependency of the tests it applies to and a place to walk from.
        starts = [test_file] + _conftests_for(test_file, conftests)
        executed = {**outside_scope, **followed.get(test_file, {})}
        for path in reachable_from(starts, executed) & reportable:
            importers.setdefault(path, []).extend(keys)

    return importers


def _lines_run(data, files, edges, test_file_of):
    """(the edges each test file ran into, files worth reporting).

    Setup and teardown count towards the first even though they are not
    reported: a fixture body referencing an import is a dependency of the test
    being set up.
    """
    followed = defaultdict(lambda: defaultdict(set))
    reportable = set()
    for filename in files:
        absolute = os.path.abspath(filename)
        by_line = edges.get(absolute, {})
        for lineno, contexts in data.contexts_by_lineno(filename=filename).items():
            # Line 0 is what coverage records for a file holding no statements,
            # which is nothing an importer could depend on.
            if lineno > 0:
                reportable.add(absolute)
            targets = by_line.get(lineno)
            if not targets:
                continue
            for context in contexts:
                if not context or "|" not in context:
                    continue
                test_file = test_file_of.get(context.rsplit("|", 1)[0])
                if test_file is not None:
                    followed[test_file][absolute] |= targets
    return followed, reportable


def _loaded_conftests(config):
    """Every conftest.py pytest loaded for this run."""
    paths = []
    for plugin in config.pluginmanager.get_plugins():
        path = getattr(plugin, "__file__", "") or ""
        if os.path.basename(path) == "conftest.py":
            paths.append(os.path.abspath(path))
    return paths


def _conftests_for(test_file, conftests):
    """The conftest.py files pytest applies to a test file: its own directory
    and every directory above it."""
    directory = os.path.dirname(test_file)
    applies = []
    for conftest in conftests:
        above = os.path.dirname(conftest)
        if directory == above or directory.startswith(above + os.sep):
            applies.append(conftest)
    return applies
