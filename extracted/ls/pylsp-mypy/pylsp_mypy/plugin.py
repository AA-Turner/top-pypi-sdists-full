# -*- coding: utf-8 -*-
"""
File that contains the python-lsp-server plugin pylsp-mypy.

Created on Fri Jul 10 09:53:57 2020

@author: Richard Kellnberger
"""

import ast
import collections
import os
import os.path
import re
import tempfile
from configparser import ConfigParser
from pathlib import Path
from typing import IO, Any, Optional

from pylsp_mypy.hover import hover
from pylsp_mypy.util import get_cmd

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib

from pylsp import hookimpl
from pylsp.config.config import Config
from pylsp.workspace import Document, Workspace

from pylsp_mypy import log
from pylsp_mypy.backend import (
    Backend,
    DmypyAPIBackend,
    DmypyCommandBackend,
    MypyAPIBackend,
    MypyCommandBackend,
)

line_pattern = re.compile(
    (
        r"^(?P<file>.+):(?P<start_line>\d+):(?P<start_col>\d*):(?P<end_line>\d*):(?P<end_col>\d*): "
        r"(?P<severity>\w+): (?P<message>.+?)(?: +\[(?P<code>.+)\])?$"
    )
)

whole_line_pattern = re.compile(  # certain mypy warnings do not report start-end ranges
    (
        r"^(?P<file>.+):(?P<start_line>\d+): "
        r"(?P<severity>\w+): (?P<message>.+?)(?: +\[(?P<code>.+)\])?$"
    )
)


# A mapping from workspace path to config file path
mypyConfigFileMap: dict[str, Optional[str]] = {}

settingsCache: dict[str, dict[str, Any]] = {}

tmpFile: Optional[IO[bytes]] = None

# In non-live-mode the file contents aren't updated.
# Returning an empty diagnostic clears the diagnostic result,
# so store a cache of last diagnostics for each file a-la the pylint plugin,
# so we can return some potentially-stale diagnostics.
# https://github.com/python-lsp/python-lsp-server/blob/v1.0.1/pylsp/plugins/pylint_lint.py#L55-L62
last_diagnostics: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)


def parse_line(line: str, document: Optional[Document] = None) -> Optional[dict[str, Any]]:
    """
    Return a language-server diagnostic from a line of the Mypy error report.

    optionally, use the whole document to provide more context on it.


    Parameters
    ----------
    line : str
        Line of mypy output to be analysed.
    document : Optional[Document], optional
        Document in wich the line is found. The default is None.

    Returns
    -------
    Optional[Dict[str, Any]]
        The dict with the lint data.

    """
    result = line_pattern.match(line) or whole_line_pattern.match(line)

    if not result:
        return None

    file_path = result["file"]
    if file_path != "<string>":  # live mode
        # results from other files can be included, but we cannot return
        # them.
        if document and document.path and not document.path.endswith(file_path):
            log.warning("discarding result for %s against %s", file_path, document.path)
            return None

    lineno = int(result["start_line"]) - 1  # 0-based line number
    offset = int(result.groupdict().get("start_col", 1)) - 1  # 0-based offset
    end_lineno = int(result.groupdict().get("end_line", lineno + 1)) - 1
    end_offset = int(result.groupdict().get("end_col", 1))  # end is exclusive

    severity = result["severity"]
    if severity not in ("error", "note"):
        log.warning(f"invalid error severity '{severity}'")
    errno = 1 if severity == "error" else 3

    diag = {
        "source": "mypy",
        "range": {
            "start": {"line": lineno, "character": offset},
            "end": {"line": end_lineno, "character": end_offset},
        },
        "message": result["message"],
        "severity": errno,
    }

    if result["code"]:
        diag["code"] = result["code"]

    return diag


def apply_overrides(args: list[str], overrides: list[Any]) -> list[str]:
    """Replace or combine default command-line options with overrides."""
    overrides_iterator = iter(overrides)
    if True not in overrides_iterator:
        return overrides
    # If True is in the list, the if above leaves the iterator at the element after True,
    # therefore, the list below only contains the elements after the True
    rest = list(overrides_iterator)
    # slice of the True and the rest, add the args, add the rest
    return overrides[: -(len(rest) + 1)] + args + rest


def didSettingsChange(workspace: str, settings: dict[str, Any]) -> None:
    """Handle relevant changes to the settings between runs."""
    # TODO potentially clean up dmypy
    configSubPaths = settings.get("config_sub_paths", [])
    if settingsCache[workspace].get("config_sub_paths", []) != configSubPaths:
        mypyConfigFile = findConfigFile(
            workspace,
            configSubPaths,
            ["mypy.ini", ".mypy.ini", "pyproject.toml", "setup.cfg"],
            True,
        )
        mypyConfigFileMap[workspace] = mypyConfigFile
        settingsCache[workspace] = settings.copy()


def match_exclude_patterns(document_path: str, exclude_patterns: list[str]) -> bool:
    """Check if the current document path matches any of the configures exlude patterns."""
    document_path = document_path.replace(os.sep, "/")

    for pattern in exclude_patterns:
        try:
            if re.search(pattern, document_path):
                log.debug(f"{document_path} matches " f"exclude pattern '{pattern}'")
                return True
        except re.error as e:
            log.error(f"pattern {pattern} is not a valid regular expression: {e}")

    return False


@hookimpl
def pylsp_lint(
    config: Config, workspace: Workspace, document: Document, is_saved: bool
) -> list[dict[str, Any]]:
    """
    Call the linter.

    Parameters
    ----------
    config : Config
        The pylsp config.
    workspace : Workspace
        The pylsp workspace.
    document : Document
        The document to be linted.
    is_saved : bool
        Weather the document is saved.

    Returns
    -------
    List[Dict[str, Any]]
        List of the linting data.

    """
    settings = config.plugin_settings("pylsp_mypy")

    didSettingsChange(workspace.root_path, settings)

    # Running mypy with a single file (document) ignores any exclude pattern
    # configured with mypy. We can now add our own exclude section like so:
    # [tool.pylsp-mypy]
    # exclude = ["tests/*"]
    exclude_patterns = settings.get("exclude", [])

    if match_exclude_patterns(document_path=document.path, exclude_patterns=exclude_patterns):
        log.debug(
            f"Not running because {document.path} matches " f"exclude patterns '{exclude_patterns}'"
        )
        return []

    if settings.get("report_progress", False):
        with workspace.report_progress("lint: mypy"):
            return get_diagnostics(workspace, document, settings, is_saved)
    else:
        return get_diagnostics(workspace, document, settings, is_saved)


def get_diagnostics(
    workspace: Workspace,
    document: Document,
    settings: dict[str, Any],
    is_saved: bool,
) -> list[dict[str, Any]]:
    """
    Lints.

    Parameters
    ----------
    workspace : Workspace
        The pylsp workspace.
    document : Document
        The document to be linted.
    is_saved : bool
        Whether the document is saved.

    Returns
    -------
    List[Dict[str, Any]]
        List of the linting data.

    """
    log.info(
        "lint settings = %s document.path = %s is_saved = %s",
        settings,
        document.path,
        is_saved,
    )

    live_mode = settings.get("live_mode", True)
    dmypy = settings.get("dmypy", False)

    if dmypy and live_mode:
        # dmypy can only be efficiently run on files that have been saved, see:
        # https://github.com/python/mypy/issues/9309
        log.warning("live_mode is not supported with dmypy, disabling")
        live_mode = False

    if dmypy:
        dmypy_status_file = settings.get("dmypy_status_file", ".dmypy.json")

    args = ["--show-error-end", "--no-error-summary", "--no-pretty"]

    global tmpFile
    if live_mode and not is_saved:
        if tmpFile:
            tmpFile = open(tmpFile.name, "wb")
        else:
            tmpFile = tempfile.NamedTemporaryFile("wb", delete=False)
        log.info("live_mode tmpFile = %s", tmpFile.name)
        tmpFile.write(bytes(document.source, "utf-8"))
        tmpFile.close()
        args.extend(["--shadow-file", document.path, tmpFile.name])
    elif not is_saved and document.path in last_diagnostics:
        # On-launch the document isn't marked as saved, so fall through and run
        # the diagnostics anyway even if the file contents may be out of date.
        log.info(
            "non-live, returning cached diagnostics len(cached) = %s",
            last_diagnostics[document.path],
        )
        return last_diagnostics[document.path]

    mypyConfigFile = mypyConfigFileMap.get(workspace.root_path)
    if mypyConfigFile:
        args.append("--config-file")
        args.append(mypyConfigFile)

    args.append(document.path)

    if settings.get("strict", False):
        args.append("--strict")

    overrides = settings.get("overrides", [True])
    exit_status = 0

    backend: Backend

    if not dmypy:
        args.extend(["--incremental", "--follow-imports", settings.get("follow-imports", "silent")])
        args = apply_overrides(args, overrides)

        command = get_cmd(settings, "mypy")

        if command:
            # mypy exists on PATH or was provided by settings
            # -> use this mypy
            backend = MypyCommandBackend()
        else:
            # mypy does not exist on PATH and was not provided by settings,
            # but must exist in the env pylsp-mypy is installed in
            # -> use mypy via api
            backend = MypyAPIBackend()
    else:
        command = get_cmd(settings, "dmypy")

        args = [
            "--status-file",
            dmypy_status_file,
            "run",
            "--export-types",
            "--",
        ] + apply_overrides(args, overrides)

        if command:
            # dmypy exists on PATH or was provided by settings
            # -> use this dmypy
            backend = DmypyCommandBackend()
        else:
            # dmypy does not exist on PATH and was not provided by settings,
            # but must exist in the env pylsp-mypy is installed in
            # -> use dmypy via api
            backend = DmypyAPIBackend()

    report, errors, exit_status = backend.run(command, args)

    log.debug(f"report:\n{report}")
    log.debug(f"errors:\n{errors}")

    diagnostics = []

    # Expose generic mypy error on the first line.
    if errors:
        diagnostics.append(
            {
                "source": "mypy",
                "range": {
                    "start": {"line": 0, "character": 0},
                    # Client is supposed to clip end column to line length.
                    "end": {"line": 0, "character": 1000},
                },
                "message": errors,
                "severity": 1 if exit_status != 0 else 2,  # Error if exited with error or warning.
            }
        )

    for line in report.splitlines():
        log.debug("parsing: line = %r", line)
        diag = parse_line(line, document)
        if diag:
            diagnostics.append(diag)

    log.info("pylsp-mypy len(diagnostics) = %s", len(diagnostics))

    last_diagnostics[document.path] = diagnostics
    return diagnostics


@hookimpl
def pylsp_settings(config: Config) -> dict[str, dict[str, dict[str, str]]]:
    """
    Read the settings.

    Parameters
    ----------
    config : Config
        The pylsp config.

    Returns
    -------
    Dict[str, Dict[str, Dict[str, str]]]
        The config dict.

    """
    configuration = init(config._root_path)
    return {"plugins": {"pylsp_mypy": configuration}}


def init(workspace: str) -> dict[str, str]:
    """
    Find plugin and mypy config files and creates the temp file should it be used.

    Parameters
    ----------
    workspace : str
        The path to the current workspace.

    Returns
    -------
    Dict[str, str]
        The plugin config dict.

    """
    log.info("init workspace = %s", workspace)

    configuration = {}
    path = findConfigFile(workspace, [], ["pylsp-mypy.cfg", "pyproject.toml"], False)
    if path:
        if "pyproject.toml" in path:
            with open(path, "rb") as file:
                configuration = tomllib.load(file).get("tool").get("pylsp-mypy")
        else:
            with open(path) as file:
                configuration = ast.literal_eval(file.read())

    configSubPaths = configuration.get("config_sub_paths", [])
    mypyConfigFile = findConfigFile(
        workspace, configSubPaths, ["mypy.ini", ".mypy.ini", "pyproject.toml", "setup.cfg"], True
    )
    mypyConfigFileMap[workspace] = mypyConfigFile
    settingsCache[workspace] = configuration.copy()

    log.info("mypyConfigFile = %s configuration = %s", mypyConfigFile, configuration)
    return configuration


def findConfigFile(
    path: str, configSubPaths: list[str], names: list[str], mypy: bool
) -> Optional[str]:
    """
    Search for a config file.

    Search for a file of a given name from the directory specifyed by path through all parent
    directories. The first file found is selected.

    Parameters
    ----------
    path : str
        The path where the search starts.
    configSubPaths : List[str]
        Additional sub search paths in which mypy configs might be located
    names : List[str]
        The file to be found (or alternative names).
    mypy : bool
        whether the config file searched is for mypy (plugin otherwise)

    Returns
    -------
    Optional[str]
        The path where the file has been found or None if no matching file has been found.

    """
    start = Path(path).joinpath(names[0])  # the join causes the parents to include path
    for parent in start.parents:
        for name in names:
            for subPath in [""] + configSubPaths:
                file = parent.joinpath(subPath).joinpath(name)
                if file.is_file():
                    if file.name in ["pylsp-mypy.cfg"]:
                        raise DeprecationWarning(
                            f"{str(file)}: {file.name} is no longer supported, you should use a"
                            "pyproject.toml instead."
                        )
                    if file.name == "pyproject.toml":
                        with open(file, "rb") as fileO:
                            configPresent = (
                                tomllib.load(fileO)
                                .get("tool", {})
                                .get("mypy" if mypy else "pylsp-mypy")
                                is not None
                            )
                        if not configPresent:
                            continue
                    if file.name == "setup.cfg":
                        config = ConfigParser()
                        config.read(str(file))
                        if "mypy" not in config:
                            continue
                    return str(file)
    # No config file found in the whole directory tree
    # -> check mypy default locations for mypy config
    if mypy:
        defaultPaths = ["~/.config/mypy/config", "~/.mypy.ini"]
        XDG_CONFIG_HOME = os.environ.get("XDG_CONFIG_HOME")
        if XDG_CONFIG_HOME:
            defaultPaths.insert(0, f"{XDG_CONFIG_HOME}/mypy/config")
        for path in defaultPaths:
            if Path(path).expanduser().exists():
                return str(Path(path).expanduser())
    return None


@hookimpl(tryfirst=True)
def pylsp_hover(
    config: Config, workspace: Workspace, document: Document, position: dict[str, int]
) -> dict[str, str]:
    # TODO docstring
    return hover(config, document, position)


@hookimpl
def pylsp_code_actions(
    config: Config,
    workspace: Workspace,
    document: Document,
    range: dict[str, Any],
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Provide code actions to ignore errors.

    Parameters
    ----------
    config : pylsp.config.config.Config
        Current config.
    workspace : pylsp.workspace.Workspace
        Current workspace.
    document : pylsp.workspace.Document
        Document to apply code actions on.
    range : Dict
        Range argument given by pylsp.
    context : Dict
        CodeActionContext given as dict.

    Returns
    -------
      List of dicts containing the code actions.
    """
    actions = []
    # Code actions based on diagnostics
    for diagnostic in context.get("diagnostics", []):
        if diagnostic["source"] != "mypy":
            continue
        if "code" not in diagnostic:
            continue
        code = diagnostic["code"]
        lineNumberEnd = diagnostic["range"]["end"]["line"]
        line = document.lines[lineNumberEnd]
        endOfLine = len(line) - 1
        start = {"line": lineNumberEnd, "character": endOfLine}
        edit_range = {"start": start, "end": start}
        edit = {"range": edit_range, "newText": f"  # type: ignore[{code}]"}

        action = {
            "title": f"# type: ignore[{code}]",
            "kind": "quickfix",
            "diagnostics": [diagnostic],
            "edit": {"changes": {document.uri: [edit]}},
        }
        actions.append(action)
    if context.get("diagnostics", []) != []:
        return actions

    # Code actions based on current selected range
    for diagnostic in last_diagnostics[document.path]:
        lineNumberStart = diagnostic["range"]["start"]["line"]
        lineNumberEnd = diagnostic["range"]["end"]["line"]
        rStart = range["start"]["line"]
        rEnd = range["end"]["line"]
        if (rStart <= lineNumberStart and rEnd >= lineNumberStart) or (
            rStart <= lineNumberEnd and rEnd >= lineNumberEnd
        ):
            code = diagnostic["code"]
            line = document.lines[lineNumberEnd]
            endOfLine = len(line) - 1
            start = {"line": lineNumberEnd, "character": endOfLine}
            edit_range = {"start": start, "end": start}
            edit = {"range": edit_range, "newText": f"  # type: ignore[{code}]"}
            action = {
                "title": f"# type: ignore[{code}]",
                "kind": "quickfix",
                "edit": {"changes": {document.uri: [edit]}},
            }
            actions.append(action)

    return actions


def close_tmpfile() -> None:
    """
    Delete the tmpFile should it exist.

    Returns
    -------
    None.

    """
    if tmpFile and tmpFile.name:
        os.unlink(tmpFile.name)


def dmypy_stop(settings: dict[str, Any]) -> None:
    """Possibly stop dmypy."""
    dmypy = settings.get("dmypy", False)
    if not dmypy:
        return

    status_file = settings.get("dmypy_status_file", ".dmypy.json")
    if not os.path.exists(status_file):
        return

    command: list[str] = get_cmd(settings, "dmypy")
    backend: Backend

    if command:
        # dmypy exists on PATH or was provided by settings
        # -> use this dmypy
        backend = DmypyCommandBackend()
    else:
        # dmypy does not exist on PATH and was not provided by settings,
        # but must exist in the env pylsp-mypy is installed in
        # -> use dmypy via api
        backend = DmypyAPIBackend()
    backend.stop(command, status_file)


@hookimpl
def pylsp_shutdown(config: Config, workspace: Workspace) -> None:
    log.info("shutdown requested")
    close_tmpfile()
    dmypy_stop(config.plugin_settings("pylsp_mypy"))
