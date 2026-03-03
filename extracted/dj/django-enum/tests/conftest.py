import inspect
import json
import os
import subprocess
import sys
from importlib.metadata import distributions

import pytest
import django
from packaging.version import parse as parse_version


def pytest_addoption(parser):
    parser.addoption(
        "--record-screenshots",
        action="store_true",
        default=False,
        help="Record screenshots for the documentation",
    )
    parser.addoption(
        "--log-env",
        action="store_true",
        default=False,
        help="Log the installed environment to requirements-test-N.txt",
    )


def pytest_sessionstart(session: pytest.Session) -> None:
    if os.getenv("GITHUB_ACTIONS") == "true" or session.config.getoption("--log-env"):

        def freeze():
            lines = []
            for dist in distributions():
                name = dist.metadata["Name"]
                version = dist.version
                direct_url = dist.read_text("direct_url.json")
                if direct_url:
                    data = json.loads(direct_url)
                    if "url" in data:
                        lines.append(f"{name} @ {data['url']}")
                        continue
                lines.append(f"{name}=={version}")
            return sorted(lines)

        def write_reqs(number: int) -> bool:
            try:
                with open(
                    f"requirements-test-{number}.txt", "x", encoding="utf-8"
                ) as f:
                    f.write("\n".join(freeze()) + "\n")
                return True
            except FileExistsError:
                return False

        run = 0
        while not write_reqs(run):
            run += 1


@pytest.fixture(autouse=True)
def inject_pytest_options(pytestconfig, request):
    # Only apply to tests marked with @pytest.mark.screenshots
    if (
        request.cls is not None
        and request.node.get_closest_marker("screenshots") is not None
    ):
        request.cls.record_screenshots = pytestconfig.getoption("--record-screenshots")


def pytest_configure(config: pytest.Config) -> None:
    # stash it somewhere global-ish
    import tests

    tests.HEADLESS = not config.getoption("--headed")


def first_breakable_line(obj) -> tuple[str, int]:
    """
    Return the absolute line number of the first executable statement
    in a function or bound method.
    """
    import ast
    import textwrap

    func = obj.__func__ if inspect.ismethod(obj) else obj

    source = inspect.getsource(func)
    source = textwrap.dedent(source)
    filename = inspect.getsourcefile(func)
    assert filename
    _, start_lineno = inspect.getsourcelines(func)

    tree = ast.parse(source)

    for node in tree.body[0].body:
        if (
            isinstance(node, ast.Expr)
            and isinstance(node.value, ast.Constant)
            and isinstance(node.value.value, str)
        ):
            continue

        return filename, start_lineno + node.lineno - 1

    # fallback: just return the line after the def
    return filename, start_lineno + 1


def pytest_runtest_call(item):
    # --trace cli option does not work for unittest style tests so we implement it here
    test = getattr(item, "obj", None)
    if item.config.option.trace and inspect.ismethod(test):
        from IPython.terminal.debugger import TerminalPdb

        try:
            file = inspect.getsourcefile(test)
            assert file
            dbg = TerminalPdb()
            dbg.set_break(*first_breakable_line(test))
            dbg.cmdqueue.append("continue")
            dbg.set_trace()
        except (OSError, AssertionError):
            pass


def _install_playwright_browsers() -> None:
    cmd = [sys.executable, "-m", "playwright", "install", "chromium"]
    subprocess.run(cmd, check=True)


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    any_ui = any(item.get_closest_marker("ui") is not None for item in items)

    if any_ui and not getattr(config, "_did_install_playwright", False):
        setattr(config, "_did_install_playwright", True)
        _install_playwright_browsers()


@pytest.fixture(scope="session", autouse=True)
def require_db_version(django_db_setup, django_db_blocker):
    from django.db import connection

    if os.getenv("GITHUB_ACTIONS") == "true":
        rdbms = os.environ["RDBMS"]
        expected_python = os.environ["TEST_PYTHON_VERSION"]
        expected_django = os.environ.get("TEST_DJANGO_VERSION", "").removeprefix("dj")
        if expected_django.isdigit():
            expected_django = ".".join(expected_django)
        expected_db_ver = os.environ.get("TEST_DATABASE_VERSION", None)
        expected_client = os.environ.get("TEST_DATABASE_CLIENT_VERSION", None)

        expected_python = parse_version(expected_python)
        if sys.version_info[:2] != (expected_python.major, expected_python.minor):
            pytest.fail(
                f"Python Version Mismatch: {sys.version_info[:2]} != {expected_python}"
            )

        try:
            dj_actual = django.VERSION[:2]
            expected_django = parse_version(expected_django)
            dj_expected = (expected_django.major, expected_django.minor)
            if dj_actual != dj_expected:
                pytest.fail(
                    f"Django Version Mismatch: {dj_actual} != {expected_django}"
                )
        except ValueError:
            pytest.fail(f"Invalid Django version format: {expected_django}")

        def get_postgresql_version():
            with django_db_blocker.unblock():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()
                    db, ver = version[0].split(" ")[:2]
                    assert db == "PostgreSQL"
                    return tuple(int(v) for v in ver.split(".")[:2] if v)

        def get_mysql_version():
            with django_db_blocker.unblock():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT VERSION();")
                    version = cursor.fetchone()
                    return version[0]

        if expected_db_ver:
            if rdbms == "postgres":
                if expected_db_ver == "latest":
                    get_postgresql_version()  # verify accessible and is PostgreSQL
                else:
                    expected_version = tuple(
                        int(v) for v in expected_db_ver.split(".") if v
                    )
                    if (
                        expected_version
                        != get_postgresql_version()[: len(expected_version)]
                    ):
                        pytest.fail(
                            f"Unexpected PostgreSQL version: got {get_postgresql_version()[: len(expected_version)]}, expected {expected_version}",
                            pytrace=False,
                        )
                if expected_client == "psycopg3":
                    import psycopg

                    if not psycopg.__version__[0] == "3":
                        pytest.fail(
                            f"Unexpected psycopg version: got {psycopg.__version__}, "
                            f" expected 3.x",
                            pytrace=False,
                        )
                else:
                    import psycopg2

                    if not psycopg2.__version__[0] == "2":
                        pytest.fail(
                            f"Unexpected psycopg version: got {psycopg2.__version__}, "
                            f" expected 2.x",
                            pytrace=False,
                        )
            elif rdbms == "mysql":
                if expected_db_ver != "latest":
                    mysql_ver = get_mysql_version()
                    actual = tuple(
                        int(v) for v in mysql_ver.split(".")[:2] if v.isdigit()
                    )
                    expected = tuple(
                        int(v) for v in expected_db_ver.split(".") if v.isdigit()
                    )
                    if actual[: len(expected)] != expected:
                        pytest.fail(
                            f"Unexpected MySQL version: got {mysql_ver}, expected {expected_db_ver}",
                            pytrace=False,
                        )
                if expected_client == "mysqlclient2x":
                    import MySQLdb

                    if MySQLdb.version_info[0] != 2:
                        pytest.fail(
                            f"Unexpected mysqlclient version: got {MySQLdb.version_info},"
                            f" expected 2.x",
                            pytrace=False,
                        )
            elif rdbms == "mariadb":
                if expected_db_ver != "latest":
                    mariadb_ver = get_mysql_version()
                    ver_str = mariadb_ver.split("-")[0]  # strip "-MariaDB" suffix
                    actual = tuple(
                        int(v) for v in ver_str.split(".")[:2] if v.isdigit()
                    )
                    expected = tuple(
                        int(v) for v in expected_db_ver.split(".") if v.isdigit()
                    )
                    if actual[: len(expected)] != expected:
                        pytest.fail(
                            f"Unexpected MariaDB version: got {mariadb_ver}, expected {expected_db_ver}",
                            pytrace=False,
                        )
                if expected_client == "mysqlclient2x":
                    import MySQLdb

                    if MySQLdb.version_info[0] != 2:
                        pytest.fail(
                            f"Unexpected mysqlclient version: got {MySQLdb.version_info},"
                            f" expected 2.x",
                            pytrace=False,
                        )
            elif rdbms == "sqlite":
                pass  # no server version to verify for SQLite
            elif rdbms == "oracle":
                # expected_db_ver is the image tag, e.g. 'oracle-xe:21' or 'oracle-free:latest'
                tag = (
                    expected_db_ver.split(":")[-1]
                    if ":" in expected_db_ver
                    else expected_db_ver
                )
                if tag != "latest":
                    with django_db_blocker.unblock():
                        actual_ver = connection.connection.version  # e.g. "21.3.0.0.0"
                    actual_major = int(actual_ver.split(".")[0])
                    expected_major = int(tag)
                    if actual_major != expected_major:
                        pytest.fail(
                            f"Unexpected Oracle version: got {actual_ver},"
                            f" expected {expected_major}c",
                            pytrace=False,
                        )
