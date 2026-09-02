"""No sync path may resolve a board credential from local state (#609).

This is the client-side twin of ``tests/test_server_reads_no_local_credentials.py``,
and the gap between the two is what allowed the leak it closes.

That gate opens "the server must never resolve a credential from a store that is
not tenant-scoped", and it is enforced -- ``CredentialProvider`` was deleted in
#525 for breaking it. But it deliberately excludes ``src/cli/``, because the CLI
legitimately owns ``~/.innoday`` and the keyring (it holds the user's own auth
token there). **The CLI reading a board credential out of that same file and
POSTing it achieves the identical outcome and passes the server gate**, because
the read happens client-side. That is exactly what was happening.

The concrete hazard it left standing: ``BoardCommands._handle_sync`` looped over
``("linear", "jira", "trello", "notion")``, took the **first** locally-configured
credential and set ``X-Integration-Token`` -- **without checking it matched the
board's type**. So an operator with a saved Jira credential syncing a *Linear*
board sent their Jira email and API token to the server, which forwarded it to
``api.linear.app``. Same shape as #562, where a GitHub PAT reached
``api.trello.com``. There was no ``--token`` flag on ``board sync`` either, so
this was not a fallback behind a deliberate option: it was the only way a
credential was ever attached, and it was silent.

**What this gate asserts, and what it deliberately does not.** It is not "the CLI
never touches the keyring" -- it must, for the CLI auth token. It is narrower and
therefore checkable:

  1. ``get_organization_integration`` no longer exists anywhere. It was the one
     reader of a stored *board* credential, all five of its callers were the
     sites this issue removed, and it is deleted rather than left callerless.
  2. The four sync entry points reach no local credential store at all -- no
     keyring call, no ``["integrations"]`` traversal, no credential getter.
  3. ``board register`` and ``board set-cred`` take a credential only from
     explicit flags. They are excluded from (2) by name, with a reason.

**Why AST rather than grep.** The reads being guarded against are ordinary method
calls on a `config` object, and two of the four sites reached the token builder
through a *function-level* import (``from src.cli.commands.boards import
BoardCommands`` inside the function body). A grep for top-of-file imports would
have reported both files clean the whole time.

`board register` supplying a credential is the one legitimate case and stays
legitimate: it is how a credential reaches Vault, which is where every sync now
resolves one from. `X-Integration-Token` also remains a real server contract for
a caller who genuinely has a one-off credential -- what was removed is the CLI
silently populating it from disk.
"""

import ast
from pathlib import Path

CLI = Path(__file__).resolve().parents[1] / "src" / "cli"

# Every command that triggers a sync, as `module.py::Class.function`. These are
# the paths a credential must never be attached to from local state -- the
# server resolves each one's credential from Vault.
SYNC_ENTRY_POINTS = {
    ("commands/sync.py", "_sync_board"),
    ("commands/sync.py", "_handle_ticket_sync"),
    ("commands/boards.py", "_handle_sync"),
    ("commands/scopes.py", "_handle_generate"),
}

# Functions that may legitimately hold a credential: the operator typed one on
# the command line. Listed so the exemption is a named decision rather than an
# accident of which functions the gate happens to look at.
CREDENTIAL_SUPPLY_POINTS = {
    ("commands/boards.py", "_handle_register"),
    ("commands/boards.py", "_handle_set_credential"),
}

# Call names that read a credential out of local state.
LOCAL_CREDENTIAL_READERS = {
    "get_organization_integration",
    "get_credential",
    "get_password",
}


def _cli_files():
    for path in sorted(CLI.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        yield path


def _rel(path: Path) -> str:
    return path.relative_to(CLI).as_posix()


def _functions(tree):
    """Yield (name, node) for every function, including methods."""
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node.name, node


def _local_credential_reads(node) -> set:
    """Every way this subtree reaches a locally-stored credential.

    Three shapes, all of which occurred at the removed sites:
      * ``config.get_organization_integration(...)`` -- a method call,
      * ``keyring.get_password(...)`` / a bare ``get_credential(...)``,
      * ``...["organizations"][alias]["integrations"]`` -- reading the config
        dict directly, which is how the wizard displays them and would be the
        obvious way to reintroduce the read without naming the getter.
    """
    found = set()
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            func = child.func
            name = None
            if isinstance(func, ast.Attribute):
                name = func.attr
            elif isinstance(func, ast.Name):
                name = func.id
            if name in LOCAL_CREDENTIAL_READERS:
                found.add(name)
        elif isinstance(child, ast.Subscript):
            key = child.slice
            if isinstance(key, ast.Constant) and key.value == "integrations":
                found.add('["integrations"]')
    return found


def _violations_in(path: Path, wanted_functions=None) -> set:
    """(function, symbol) pairs. With `wanted_functions`, only those; without,
    the whole module (used for the probe and the whole-tree scans)."""
    tree = ast.parse(path.read_text())
    found = set()
    for name, node in _functions(tree):
        if wanted_functions is not None and name not in wanted_functions:
            continue
        for symbol in _local_credential_reads(node):
            found.add((name, symbol))
    return found


class TestNoSyncPathReadsALocalCredential:
    def test_every_sync_entry_point_is_clean(self):
        offenders = set()
        for rel_path, function in sorted(SYNC_ENTRY_POINTS):
            path = CLI / rel_path
            for name, symbol in _violations_in(path, {function}):
                offenders.add((rel_path, name, symbol))

        assert not offenders, (
            "a sync path is reading a board credential from local state "
            "(~/.innoday/config.json or the OS keyring). The server resolves "
            "the board's own credential from Vault -- sending one from this "
            f"machine overrides it, possibly with another vendor's. {sorted(offenders)}"
        )

    def test_the_named_sync_entry_points_all_exist(self):
        """Vacuity guard on the gate's own scope.

        `_violations_in` scans nothing for a function that is not there and
        reports clean -- indistinguishable from real coverage. A rename would
        silently empty this gate, which is precisely the failure mode the
        server-side gate's `test_every_server_layer_is_a_directory_that_exists`
        was added for after #571 left a stale entry behind.
        """
        missing = []
        for rel_path, function in sorted(SYNC_ENTRY_POINTS):
            path = CLI / rel_path
            if not path.exists():
                missing.append((rel_path, function, "file"))
                continue
            names = {name for name, _ in _functions(ast.parse(path.read_text()))}
            if function not in names:
                missing.append((rel_path, function, "function"))

        assert not missing, (
            "SYNC_ENTRY_POINTS names something that does not exist -- the gate "
            f"scans nothing for it and reports clean: {missing}"
        )

    def test_the_detector_catches_every_read_shape(self, tmp_path):
        """The other half of the vacuity guard: exercise the matcher itself.

        A detector that silently stopped matching would leave the assertions
        above green forever. The first two are the exact forms the four removed
        sites used; the third is the direct-dict read, which no site used but
        which is the obvious way back in without naming the getter.
        """
        for source in (
            "async def f(config):\n"
            "    return config.get_organization_integration(org, 'jira')\n",
            "import keyring\n"
            "def f():\n"
            "    return keyring.get_password('innoday-cli', 'k')\n",
            "def f(config):\n"
            "    return config._config['organizations']['bp']['integrations']\n",
        ):
            probe = tmp_path / "probe.py"
            probe.write_text(source)
            assert _violations_in(probe), source

    def test_a_sync_path_that_reintroduces_the_read_is_caught(self, tmp_path):
        """The gate, run against the code as it stood before #609.

        `test_every_sync_entry_point_is_clean` passes on an empty function; this
        proves it would fail on the real thing. The body is the loop that was in
        `BoardCommands._handle_sync`.
        """
        probe = tmp_path / "boards.py"
        probe.write_text(
            "class BoardCommands:\n"
            "    async def _handle_sync(args, client, config):\n"
            "        headers = {}\n"
            "        for board_type in ('linear', 'jira', 'trello', 'notion'):\n"
            "            i = config.get_organization_integration(org, board_type)\n"
            "            if i:\n"
            "                headers['X-Integration-Token'] = i['token']\n"
            "                break\n"
        )
        assert _violations_in(probe, {"_handle_sync"}) == {
            ("_handle_sync", "get_organization_integration")
        }


class TestTheBoardCredentialReaderIsGone:
    """`CLIConfig.get_organization_integration` decrypted a stored board
    credential out of the keyring. Every one of its five callers was a
    sync/register path, so removing them left it with none -- and a callerless
    credential reader is not retired, it is dormant. Asserting the *symbol* is
    gone, not merely that nothing calls it, for the same reason the server gate
    asserts `credential_provider.py` no longer exists.
    """

    def test_nothing_in_the_cli_calls_it(self):
        offenders = sorted(
            (_rel(path), function)
            for path in _cli_files()
            for function, symbol in _violations_in(path)
            if symbol == "get_organization_integration"
        )
        assert not offenders, offenders

    def test_the_method_no_longer_exists(self):
        from src.cli.config import CLIConfig

        assert not hasattr(CLIConfig, "get_organization_integration")

    def test_the_source_no_longer_defines_it(self):
        """Belt and braces on the one above: `hasattr` is also False for a
        method that was renamed, and this says which outcome is intended."""
        source = (CLI / "config.py").read_text()
        assert "def get_organization_integration" not in source


class TestCredentialsAreSuppliedByFlagOnly:
    """The two commands that may hold a credential, and the shape they take it
    in. Without this, "no sync path reads local config" is satisfiable by a
    `register` that still does."""

    def test_register_and_set_cred_read_no_local_credential_either(self):
        offenders = set()
        for rel_path, function in sorted(CREDENTIAL_SUPPLY_POINTS):
            for name, symbol in _violations_in(CLI / rel_path, {function}):
                offenders.add((rel_path, name, symbol))

        assert not offenders, (
            "a credential must be typed on the command line, not found on "
            f"this machine: {sorted(offenders)}"
        )

    def test_they_build_the_token_from_the_flags(self):
        """Both go through `_integration_token_from_args`, which reads only
        `args`. Pinned so the shared helper cannot quietly gain a config
        argument."""
        source = (CLI / "commands" / "boards.py").read_text()
        tree = ast.parse(source)
        helper = next(
            node
            for name, node in _functions(tree)
            if name == "_integration_token_from_args"
        )
        parameters = {a.arg for a in helper.args.args}
        assert parameters == {"board_type", "args"}, parameters

    def test_the_supply_points_exist(self):
        """Vacuity guard, as above."""
        for rel_path, function in sorted(CREDENTIAL_SUPPLY_POINTS):
            names = {
                name for name, _ in _functions(ast.parse((CLI / rel_path).read_text()))
            }
            assert function in names, (rel_path, function)


class TestTheServerSideGateStillExcludesTheCli:
    def test_the_two_gates_do_not_overlap(self):
        """This file exists because the server-side gate deliberately does not
        cover `src/cli/`. If that ever changes, the CLI's legitimate keyring use
        (the user's own auth token) starts failing there, and the natural
        response is to widen that allowlist -- which would hollow it out. The
        split is the design; this pins it.
        """
        from tests.test_server_reads_no_local_credentials import (
            EXCLUDED_SUBTREES,
            _server_files,
        )

        assert "cli" in EXCLUDED_SUBTREES
        # `src/cli/` is the whole of this gate's scope, so "no overlap" is that
        # one assertion. This line used to also require `mcp` to be outside the
        # server gate -- which made "neither gate watches src/mcp/" a pinned
        # property of the pair rather than an oversight either could correct.
        # It was where #611's BOARD_API_TOKEN override survived both fixes.
        # #611 put `mcp` in the server gate; this file never scanned it.
        #
        # Asserted on that gate's walk rather than on its constant: since #622 it
        # scans all of `src/` bar `EXCLUDED_SUBTREES`, so there is no list of
        # covered packages to read `mcp` out of -- and "is it actually scanned"
        # was the better question all along.
        scanned = {path.as_posix() for path in _server_files()}
        assert any(path.endswith("/src/mcp/server.py") for path in scanned)
        assert not any("/src/cli/" in path for path in scanned)
        assert CLI.name == "cli"
