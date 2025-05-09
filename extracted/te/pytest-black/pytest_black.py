# -*- coding: utf-8 -*-

# stdlib imports
import subprocess
import re
import sys

# third-party imports
import pytest
import toml


HISTKEY = "black/mtimes"


def pytest_addoption(parser):
    group = parser.getgroup("general")
    group.addoption(
        "--black", action="store_true", help="enable format checking with black"
    )


def pytest_collect_file(file_path, path, parent):
    config = parent.config
    if config.option.black and path.ext in [".py", ".pyi"]:
        return BlackFile.from_parent(parent, path=file_path)


def pytest_configure(config):
    # load cached mtimes at session startup
    if config.option.black and hasattr(config, "cache"):
        config._blackmtimes = config.cache.get(HISTKEY, {})
    config.addinivalue_line("markers", "black: enable format checking with black")


def pytest_unconfigure(config):
    # save cached mtimes at end of session
    if hasattr(config, "_blackmtimes"):
        config.cache.set(HISTKEY, config._blackmtimes)


class BlackFile(pytest.File):
    def collect(self):
        """ returns a list of children (items and collectors)
            for this collection node.
        """
        yield BlackItem.from_parent(self, name="black")


class BlackItem(pytest.Item):
    def __init__(self, **kwargs):
        super(BlackItem, self).__init__(**kwargs)
        self.add_marker("black")
        try:
            with open("pyproject.toml") as toml_file:
                settings = toml.load(toml_file)["tool"]["black"]
            if "include" in settings.keys():
                settings["include"] = self._re_fix_verbose(settings["include"])
            if "exclude" in settings.keys():
                settings["exclude"] = self._re_fix_verbose(settings["exclude"])
            self.pyproject = settings
        except Exception:
            self.pyproject = {}

    def setup(self):
        pytest.importorskip("black")
        mtimes = getattr(self.config, "_blackmtimes", {})
        self._blackmtime = self.path.stat().st_mtime
        old = mtimes.get(str(self.path), 0)
        if self._blackmtime == old:
            pytest.skip("file(s) previously passed black format checks")

        if self._skip_test():
            pytest.skip("file(s) excluded by pyproject.toml")

    def runtest(self):
        cmd = [sys.executable, "-m", "black", "--check", "--diff", "--quiet", str(self.path)]
        try:
            subprocess.run(
                cmd, check=True, stdout=subprocess.PIPE, universal_newlines=True
            )
        except subprocess.CalledProcessError as e:
            raise BlackError(e)

        mtimes = getattr(self.config, "_blackmtimes", {})
        mtimes[str(self.path)] = self._blackmtime

    def repr_failure(self, excinfo):
        if excinfo.errisinstance(BlackError):
            return excinfo.value.args[0].stdout
        return super(BlackItem, self).repr_failure(excinfo)

    def reportinfo(self):
        return (self.path, -1, "Black format check")

    def _skip_test(self):
        return self._excluded() or (not self._included())

    def _included(self):
        if "include" not in self.pyproject:
            return True
        return re.search(self.pyproject["include"], str(self.path))

    def _excluded(self):
        if "exclude" not in self.pyproject:
            return False
        return re.search(self.pyproject["exclude"], str(self.path))

    def _re_fix_verbose(self, regex):
        if "\n" in regex:
            regex = "(?x)" + regex
        return re.compile(regex)


class BlackError(Exception):
    pass
