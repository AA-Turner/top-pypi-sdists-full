"""The server must never resolve a credential from a store that is not tenant-scoped.

Per-tenant secrets live in Supabase Vault; app-level config lives in process env.
Two different stores break that rule, in opposite directions, and this gate covers
both:

**Local state (#525/#536) yields nothing.** A deployed server has no
``~/.innoday/config.json`` and no OS keyring, and ``CredentialProvider`` -- the
442-line service that read them, deleted in #525 phase 5 -- returned ``None``
there **silently**. So a server-side read of local state is not a fallback, it is
a path that yields nothing in production while working on a developer's machine.
That divergence already caused an outage:
``org_credential_service``'s own docstring records that "every server-side GitHub
call used to fail with 'No GitHub connection found for organization'".

**Process env (#554) yields the operator's credential.** ``GITHUB_TOKEN`` is one
value shared by every tenant in the process. A server-side
``x_integration_token or os.getenv("GITHUB_TOKEN")`` therefore **fails open**: a
tenant with no credential of its own silently proceeds on the operator's, reading
(and writing) against a GitHub account it was never granted. Worse, the value is
not even type-checked at the boundary -- ``POST /integrations/trello/sync`` used to
hand it to ``TrelloAPI``, which puts its credentials in the query string, so the
operator's GitHub PAT reached ``api.trello.com``'s request logs.

Same mechanism gates both: the store is not keyed by tenant, and the failure is
invisible either way.

**Why this is a separate gate from an import-layer rule.** The coupling here is
filesystem-, OS- and environment-mediated, not an import edge -- ``slack_tools``
used to reach the keyring by calling ``get_credential_provider()``, and the
provider reached ``Path.home()`` internally. A layer test that maps
module-to-module imports would have passed the whole time that coupling stood.
This asserts the four concrete vectors instead:

  1. importing ``keyring`` from a server layer,
  2. reading ``Path.home()`` from a server layer,
  3. importing ``credential_provider``, which does both on the caller's behalf,
  4. reading a ``SHARED_CREDENTIAL_ENV`` name out of the process environment.

**The ``env:`` class covers GitHub and board credentials.** It held two names,
both GitHub's, until #611 added the board ones. The gap that made that necessary
is worth keeping in view: ``src/mcp/`` was in **neither** this gate's scope (a
named-layer allowlist until #622) nor #610's client-side twin, and it was the one component still
building ``X-Integration-Token`` out of the process environment. A supplied
header **wins over** Vault at every sync endpoint, so that was never a fallback
for a board with nothing stored -- it silently replaced the board's own
credential with the operator's, for every tenant the process served.

Board names satisfy the entry criterion this list is judged by ("where would a
correct value come from, and who can put it there?"): Vault's
``board_credentials``, written at ``register_board`` time or rotated with
``innoday board set-credential``. That is a real writer, which is exactly what
``SLACK_BOT_TOKEN`` still lacks.

Two names are deliberately **not** here, for the ``GITHUB_ORG`` reason -- they
are the non-secret half of a pair: ``BOARD_API_EMAIL`` (a Jira username; the
``email:token`` secret is the token) and ``TRELLO_API_KEY`` (identifies the
application, not the user). Neither authorizes anything on its own, and the half
that does is covered.

The process-env-credential-fallback shape lives at **one** remaining place this
gate does not catch:

  * ``src/api/slack_api.py:65-66`` -- ``SlackAPI.__init__``'s own defaults,
    ``token or os.getenv("SLACK_BOT_TOKEN")`` and the same for
    ``SLACK_WEBHOOK_URL``. ``src/api/`` **is** scanned; what this
    gate misses is the env *name*, not the location.

    **Latent, not live: that constructor default has no reachable caller.** Every
    caller passes an explicit ``token`` -- since #571 that is only
    ``src/cli/commands/config.py``, which is client-side -- so the only thing that
    reaches the ``or os.getenv(...)`` branch today is ``tests/test_slack_api.py``.
    Removing those defaults belongs with #525 phase 6 (**#605** -- #572 was
    rescoped to the org-credential lifecycle on 2026-08-13 with Slack dropped);
    doing it here would be an unrelated behaviour change. Do **not** add
    ``SLACK_BOT_TOKEN`` to ``SHARED_CREDENTIAL_ENV`` before then -- see the next paragraph for why the
    gate cannot pass with it.

    (This list named ``src/tools/slack_tools.py`` as a second site until #571
    deleted ``src/tools/`` outright -- an unreachable prototype layer written
    against an ``agent`` host that never existed here. Its ``SLACK_BOT_TOKEN``
    read went with it, and so did the only server-side Slack code of any kind.)

**What blocks adding that name is a writer, not a reader.** #525 phase 4 gave
Slack a Vault reader, and that changed nothing here: nothing in ``src/``,
``scripts/`` or the CLI writes a ``slack`` row -- ``set_org_credential`` is generic
and has no Slack caller -- so no tenant has a supported way to store one. A
tenant-scoped read with no writer behind it is not somewhere a credential can come
from, so adding ``SLACK_BOT_TOKEN`` today would fail the gate with no fix
available to anybody. **The gate can gain ``SLACK_BOT_TOKEN`` once a tenant is able
to STORE a Slack credential** -- #525 phase 6, tracked as **#605**.

That reader is gone too, and deliberately: #571 deleted its only caller, and this
change then deleted ``org_credential_service.get_slack_bot_token`` itself rather
than leave a function with no caller and no test. Keeping it would have recreated,
inside the very commit that removes 2,900 lines of unreachable code, the thing that
made those lines expensive -- code that reads as live infrastructure and is not.
Phase 6 should add a reader where Slack is actually used, and today that is
nowhere server-side.

Separately, and not a reason to relax the rule: the remaining site has no caller
that reaches it in the deployed server today -- every ``SlackAPI`` construction
passes an explicit token, and the one that does so is in the CLI. The gate is
about what the code would do, not about who is currently reaching it.

An earlier revision of this paragraph said to add the name "in the same change
that gives Slack a Vault reader". That was the wrong blocker: following it would
have failed the gate on the only path that actually works. A reader is necessary
and not sufficient; the question to ask of any entry here is "where would a
correct value come from, and who can put it there?".

Do not read this module as "the server reads no shared credential from env" -- it
asserts that for GitHub and board credentials, and for the names in
``SHARED_CREDENTIAL_ENV`` only. The *scope* is now all of ``src/`` bar
``EXCLUDED_SUBTREES``; it is the vocabulary that is partial, not the walk.

``ALLOWLIST`` is a **shrink-only** record of what stood when this landed. Adding
to it is a deliberate act that has to survive review; removing from it is the work
tracked in #525. The point of freezing the list rather than skipping the check is
that a NEW violation fails immediately, while the known ones are worked off in
order. The ``env:`` symbol class has **no** allowlist entries and must not gain
any: #554 removed every server-side read, so there is no legacy to work off.
"""

import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"

# This gate scans **all of `src/`** except the subtrees named here. `src/cli/` is
# the only exclusion: the CLI owns ~/.innoday and the keyring, and reading them
# there is correct.
#
# It used to be the other way round -- an allowlist,
# `SERVER_LAYERS = ("api", "routers", "services", "adapters", "mcp")` -- and that
# shape leaked twice, in the same way both times:
#
#   * #611: `src/mcp/` was in neither this gate's list nor #610's client-side
#     twin, and it was the one component still building `X-Integration-Token`
#     out of the process environment. Adding the layer closed that instance.
#   * #622: `src/ticket_manager.py` read `BOARD_API_TOKEN`/`TRELLO_TOKEN` from
#     `src/` **root** -- in no layer at all -- while being imported *from* a
#     scanned one (`routers/tickets.py`). Naming layers meant a credential read
#     was invisible simply by not living in a directory somebody had listed.
#
# Both escapes are the default: under an allowlist new code is uncovered until
# somebody remembers it. Inverted, a new package -- or a module at `src/` root --
# is covered the day it is written, and *dropping* coverage now takes a
# deliberate edit here that review can see.
#
# `src/mcp/` deserves its old note: it reaches ~/.innoday through `CLIConfig`, so
# the `keyring`/`Path.home`/`credential_provider` classes pass there by
# indirection rather than by the code touching no local state. That is
# deliberate -- going through CLIConfig is how MCP is supposed to read local
# state, and a direct `Path.home()` there would be a divergent second copy of
# profile resolution, worth failing on. The class that carries the weight for
# that package is `env:`.
EXCLUDED_SUBTREES = ("cli",)

# Process-env names holding a credential shared by every tenant in the process:
# GitHub's, and the board tokens #611 removed from `src/mcp/`. See the module
# docstring for why the board names qualify (Vault, with a real writer behind
# it) and why `BOARD_API_EMAIL`/`TRELLO_API_KEY` are excluded.
#
# `GITHUB_ORG` is deliberately absent: it is non-secret config, not a credential,
# and `WorkspaceOnboardService.github_org` documents it as a last-resort fallback.
SHARED_CREDENTIAL_ENV = {
    "GITHUB_TOKEN",
    "GH_TOKEN",
    "BOARD_API_TOKEN",
    "TRELLO_TOKEN",
    "JIRA_TOKEN",
    "LINEAR_API_KEY",
    "LINEAR_TOKEN",
    "NOTION_TOKEN",
}

# (path relative to src/, symbol) pairs that existed when this gate landed.
# Every entry is tracked in #525. Do not add without a written reason.
ALLOWLIST = {
    # #525's local-credential removals (phases 1-5) are done -- phase 6, the
    # tenant-facing credential store, is still open -- and the list is down to one
    # unrelated entry. Gone:
    # `api/_base.py` (phase 2), `services/board_ticket_creation_service.py`
    # (phase 3), `tools/slack_tools.py` (phase 4 -- a `slack` row in
    # `org_credentials`, then SLACK_BOT_TOKEN; that module has since been deleted
    # outright by #571, along with the rest of `src/tools/`), and both
    # `services/credential_provider.py` entries, the module itself having been
    # deleted in phase 5. `TestTheProviderIsDeleted` keeps it that way.
    #
    # `InnoServiceManager` writes ~/.innoday/config.toml and ~/.innoday/data --
    # correct behaviour for a local service manager, and NOT a credential read.
    # It sits under services/ only because of where it was first written; it has
    # exactly one consumer, `src/cli/commands/services.py`. Relocating it to
    # src/cli/ is tracked in #521, and this entry disappears when that happens.
    ("services/manager.py", "Path.home"),
}


def _server_files():
    for path in sorted(SRC.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        if path.relative_to(SRC).parts[0] in EXCLUDED_SUBTREES:
            continue
        yield path


def _const_str(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _is_environ(node):
    """``os.environ`` (attribute) or a bare ``environ`` (from-imported)."""
    if isinstance(node, ast.Attribute):
        return node.attr == "environ"
    return isinstance(node, ast.Name) and node.id == "environ"


def _env_credential_name(node):
    """The shared-credential env name this node READS, or None.

    Covers the three shapes a process-env read takes: ``os.getenv(NAME)``,
    ``os.environ.get(NAME)`` and ``os.environ[NAME]`` (plus their from-imported
    equivalents).

    Matching the AST rather than grepping is what makes two deliberate,
    legitimate occurrences free rather than something to allowlist:
    `container_guardrails.py`'s ``"GITHUB_TOKEN"`` is a string in a secret-scan
    *pattern list* and `api/app.py`'s is prose in a docstring -- neither is a
    read, and neither appears here.
    """
    if isinstance(node, ast.Call):
        func = node.func
        name = None
        if isinstance(func, ast.Attribute) and func.attr == "getenv":
            name = _const_str(node.args[0]) if node.args else None
        elif isinstance(func, ast.Name) and func.id == "getenv":
            name = _const_str(node.args[0]) if node.args else None
        elif (
            isinstance(func, ast.Attribute)
            and func.attr == "get"
            and _is_environ(func.value)
        ):
            name = _const_str(node.args[0]) if node.args else None
        if name in SHARED_CREDENTIAL_ENV:
            return name
    elif isinstance(node, ast.Subscript) and _is_environ(node.value):
        name = _const_str(node.slice)
        if name in SHARED_CREDENTIAL_ENV:
            return name
    return None


def _violations_in(path: Path):
    """Every (symbol) this file uses to reach a non-tenant-scoped credential store.

    Walks the AST rather than grepping so that a function-level import counts --
    four of `slack_tools`' five uses are inside functions, and a grep for
    top-of-file imports would report the file as clean.
    """
    tree = ast.parse(path.read_text())
    found = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                root = alias.name.split(".")[0]
                if root == "keyring":
                    found.add("keyring")
                if "credential_provider" in alias.name:
                    found.add("credential_provider")
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.split(".")[0] == "keyring":
                found.add("keyring")
            if "credential_provider" in module:
                found.add("credential_provider")
        elif isinstance(node, ast.Call):
            # Path.home() -- an attribute call, so match on the attribute chain
            # rather than a bare name.
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "home"
                and isinstance(func.value, ast.Name)
                and func.value.id == "Path"
            ):
                found.add("Path.home")

        env_name = _env_credential_name(node)
        if env_name:
            found.add(f"env:{env_name}")

    return found


def _current():
    current = set()
    for path in _server_files():
        rel = path.relative_to(SRC).as_posix()
        for symbol in _violations_in(path):
            current.add((rel, symbol))
    return current


class TestNoNewLocalCredentialReads:
    def test_no_violation_outside_the_allowlist(self):
        """A NEW server-side read of local credential state fails here."""
        unexpected = _current() - ALLOWLIST
        assert not unexpected, (
            "server code must not read local credential state "
            "(~/.innoday or the OS keyring) -- per-tenant secrets belong in "
            f"Vault. New violations: {sorted(unexpected)}"
        )

    def test_allowlist_shrinks_and_never_goes_stale(self):
        """An allowlisted entry that no longer exists must be deleted.

        Without this the list silently becomes a description of the past, and the
        next reader cannot tell which entries are real work outstanding. This is
        the half that makes it a ratchet rather than a suppression list.
        """
        stale = ALLOWLIST - _current()
        assert not stale, (
            "these ALLOWLIST entries no longer exist -- delete them, the "
            f"violation is fixed: {sorted(stale)}"
        )

    def test_every_excluded_subtree_exists(self):
        """An exclusion naming a directory that is gone is a lie about scope.

        Harmless to the *scan* -- excluding a package that does not exist removes
        nothing -- but it tells the next reader that some part of `src/` is
        deliberately unwatched when nothing is. #571 left `"tools"` in the old
        allowlist after deleting `src/tools/`, where the same rot was actively
        dangerous (a named layer that scanned nothing read as coverage). Keep the
        list honest in the direction that is left.
        """
        missing = [name for name in EXCLUDED_SUBTREES if not (SRC / name).is_dir()]
        assert not missing, (
            f"EXCLUDED_SUBTREES names directories that do not exist: {missing}"
        )

    def test_the_gate_actually_scans_what_it_claims_to(self):
        """Vacuity guard: an empty walk passes every assertion in this module.

        `_current()` must still find the one known violation. If it returned an
        empty set -- a broken walker, an `EXCLUDED_SUBTREES` that swallowed
        `src/` -- then `test_no_violation_outside_the_allowlist` would pass on
        nothing, and `test_allowlist_shrinks_and_never_goes_stale` is the only
        thing that notices. Assert it directly rather than relying on that side
        effect.
        """
        assert ("services/manager.py", "Path.home") in _current()

    def test_the_cli_is_not_covered_by_this_gate(self):
        """Guards the gate's own scope.

        The CLI legitimately owns ~/.innoday and the keyring. If `cli` ever drops
        out of the exclusions the gate starts reporting correct code as broken,
        and the natural response is to widen the ALLOWLIST -- which would hollow
        it out.
        """
        assert "cli" in EXCLUDED_SUBTREES

    def test_the_mcp_package_is_actually_walked(self):
        """#611: the package neither gate watched was the one still offending.

        `src/mcp/` sat outside this gate *and* outside #610's client-side twin,
        and that is precisely where the surviving `BOARD_API_TOKEN` override was
        found. Asserted on the *walk* rather than on the constant, because being
        in scope on paper is not being scanned.
        """
        scanned = {path.relative_to(SRC).as_posix() for path in _server_files()}
        assert "mcp/server.py" in scanned

    def test_a_module_at_src_root_is_walked(self):
        """#622: the read that escaped lived in no package at all.

        `src/ticket_manager.py` sat at `src/` root, outside every named layer,
        and read `BOARD_API_TOKEN` while `routers/tickets.py` imported it. Under
        the old allowlist the gate could not see it. This is the assertion that
        fails if anyone narrows the walk back to a set of directories.
        """
        scanned = {path.relative_to(SRC).as_posix() for path in _server_files()}
        assert "main.py" in scanned, "modules at src/ root are not being scanned"

    def test_packages_outside_the_old_server_layers_are_walked(self):
        """The same widening, for packages rather than root modules.

        None of these was in the pre-#622 allowlist
        (`api`/`routers`/`services`/`adapters`/`mcp`), and each holds code that
        could plausibly reach for a credential.
        """
        scanned = {path.relative_to(SRC).as_posix() for path in _server_files()}
        for expected in (
            "utils/time_windows.py",
            "domain/board.py",
            "middleware/__init__.py",
            "integrations/__init__.py",
            "config/schema.py",
        ):
            assert expected in scanned, f"{expected} is not being scanned"

    def test_the_cli_really_is_skipped(self):
        """The exclusion has to bite, or `ALLOWLIST` would need CLI entries.

        `src/cli/config.py` imports keyring at module scope; if the walk stopped
        honouring `EXCLUDED_SUBTREES` this gate would fail on correct code.
        """
        scanned = {path.relative_to(SRC).as_posix() for path in _server_files()}
        assert not [rel for rel in scanned if rel.startswith("cli/")]
        assert (SRC / "cli" / "config.py").exists()


class TestTheProviderIsDeleted:
    """#525 phase 5: `CredentialProvider` has no server-side consumer left.

    Asserting the *file* is gone, not just that nothing imports it. A module with
    no importers is not retired, it is dormant -- and this one is a 442-line
    keyring reader with a module-level singleton, which is exactly the thing
    somebody re-wires because it looks like existing infrastructure.
    """

    def test_the_module_no_longer_exists(self):
        assert not (SRC / "services" / "credential_provider.py").exists()

    def test_no_server_file_imports_it(self):
        offenders = sorted(
            rel for rel, symbol in _current() if symbol == "credential_provider"
        )
        assert not offenders, offenders

    def test_the_allowlist_holds_no_entry_for_it(self):
        """The specific shrink this list was built for.

        Checked separately from `test_allowlist_shrinks_and_never_goes_stale`,
        which only proves entries are not *stale* -- an entry for a file that
        still existed and still violated would satisfy that test forever. This
        asserts the entries are absent because the work is done.
        """
        remaining = [
            entry
            for entry in ALLOWLIST
            if "credential_provider" in entry[0] or entry[1] == "credential_provider"
        ]
        assert remaining == []

    def test_the_detector_would_still_catch_a_reintroduction(self, tmp_path):
        """Vacuity guard: the three assertions above all pass on an empty repo.

        Nothing here proves the gate can still see this symbol -- a detector that
        silently stopped matching would leave them green forever. So exercise it
        on a probe, in both the module and the from-import form.
        """
        for source in (
            "from src.services.credential_provider import get_credential_provider\n",
            "import src.services.credential_provider\n",
        ):
            probe = tmp_path / "probe.py"
            probe.write_text(source)
            assert "credential_provider" in _violations_in(probe), source

    def test_keyring_stays_a_dependency_because_the_cli_needs_it(self):
        """Why phase 5 deletes the module but NOT the `keyring` requirement.

        #525 phase 5 says to "drop `keyring` from the server's dependency
        surface". There is no such surface to drop it from: `pyproject.toml` has a
        single `[project] dependencies` list shipping both the API image and the
        `innoday` console script, and `src/cli/config.py` imports keyring at
        module scope to store the CLI auth token. Removing the line would
        `ImportError` the CLI on startup.

        Pinned as a test rather than left as a comment because "nothing
        server-side imports keyring" is true and reads like permission to remove
        it. Splitting server and CLI dependency sets is #521's work, not this
        gate's.
        """
        root = SRC.parent
        pyproject = (root / "pyproject.toml").read_text()
        assert "keyring>=" in pyproject

        cli_config = (SRC / "cli" / "config.py").read_text()
        assert "import keyring" in cli_config
        # The CLI ships from this same dependency list.
        assert 'innoday = "src.cli.main:main"' in pyproject


def _imports_module(path: Path, module_name: str) -> bool:
    """Does this file import ``module_name`` (as a module or a from-import)?"""
    tree = ast.parse(path.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            if any(module_name in alias.name.split(".") for alias in node.names):
                return True
        elif isinstance(node, ast.ImportFrom):
            if module_name in (node.module or "").split("."):
                return True
    return False


class TestTheTicketManagerIsDeleted:
    """#622: `src/ticket_manager.py` was the read this gate could not see.

    Same reasoning as `TestTheProviderIsDeleted`: assert the *file* is gone, not
    only that nothing imports it. It was a Trello client that resolved
    `TRELLO_API_KEY` and `BOARD_API_TOKEN`/`TRELLO_TOKEN` from process env in its
    constructor, reachable only through `get_ticket_manager()` in
    `routers/tickets.py`, which had no callers at all. A module with no importers
    is not retired, it is dormant -- and this one reads like a working sync path.
    """

    def test_the_module_no_longer_exists(self):
        assert not (SRC / "ticket_manager.py").exists()

    def test_no_scanned_file_imports_it(self):
        offenders = [
            path.relative_to(SRC).as_posix()
            for path in _server_files()
            if _imports_module(path, "ticket_manager")
        ]
        assert not offenders, offenders

    def test_its_entry_point_is_gone_too(self):
        """`get_ticket_manager()` was the whole reachable surface.

        Leaving the factory behind after deleting the module would be an
        ImportError at startup; leaving the factory *and* the module would put
        the env reads straight back.
        """
        offenders = [
            path.relative_to(SRC).as_posix()
            for path in _server_files()
            if "get_ticket_manager" in path.read_text()
        ]
        assert not offenders, offenders

    def test_the_import_detector_would_catch_a_reintroduction(self, tmp_path):
        """Vacuity guard: both assertions above pass on an empty repo."""
        for source in (
            "from src.ticket_manager import TicketManager\n",
            "import src.ticket_manager\n",
        ):
            probe = tmp_path / "probe.py"
            probe.write_text(source)
            assert _imports_module(probe, "ticket_manager"), source
        probe = tmp_path / "probe.py"
        probe.write_text("from src.services.manager import InnoServiceManager\n")
        assert not _imports_module(probe, "ticket_manager")


class TestNoSharedCredentialEnvReads:
    """#554/#611: no scanned layer may resolve a credential from process env.

    GitHub's names (#554) and the board ones (#611). The allowlist for this
    symbol class is empty and must stay empty -- unlike the local-state classes
    above there is no legacy to work off, so any entry would be a new fail-open.
    """

    def test_no_server_file_reads_a_shared_credential_from_env(self):
        offenders = sorted(
            (rel, symbol) for rel, symbol in _current() if symbol.startswith("env:")
        )
        assert not offenders, (
            "scanned code must resolve a credential per tenant -- GitHub via "
            "x_integration_token, else get_github_credentials(session, org_id); "
            "a board via resolve_board_sync_credential (Vault). A process-env "
            "read hands every tenant the operator's token. "
            f"Violations: {offenders}"
        )

    def test_the_env_symbol_class_has_no_allowlist_entries(self):
        """Guards the fix itself: allowlisting one of these re-opens #554."""
        assert not [entry for entry in ALLOWLIST if entry[1].startswith("env:")]

    def test_github_org_is_not_a_credential_and_is_not_reported(self):
        """`GITHUB_ORG` is non-secret config, documented as a last-resort fallback.

        Without this, the first person whose legitimate `GITHUB_ORG` read got
        flagged would widen the gate -- or the allowlist -- and hollow it out.
        """
        assert "GITHUB_ORG" not in SHARED_CREDENTIAL_ENV
        onboard_py = SRC / "services" / "workspace_onboard.py"
        # Vacuity guard: this only asserts something while that read still exists.
        assert "GITHUB_ORG" in onboard_py.read_text()
        # Assert on the symbol, not on "no env: violation at all" in this file --
        # otherwise an unrelated GITHUB_TOKEN read fails a test named for
        # GITHUB_ORG, and sends whoever reads the failure to the wrong variable.
        assert "env:GITHUB_ORG" not in _violations_in(onboard_py)

    def test_a_string_literal_naming_the_variable_is_not_a_read(self):
        """`container_guardrails.py` lists "GITHUB_TOKEN" as a secret-scan pattern.

        It never reads the variable. This is the case that makes AST-over-grep
        load-bearing rather than a stylistic preference.
        """
        guardrails = SRC / "services" / "container_guardrails.py"
        assert "GITHUB_TOKEN" in guardrails.read_text()
        assert not [s for s in _violations_in(guardrails) if s.startswith("env:")]

    def test_the_detector_catches_every_env_read_shape(self, tmp_path):
        """The gate's own detector, exercised directly.

        A gate whose matcher silently stopped matching would pass forever. The
        first three are the exact forms the four #554 sites used between them;
        the fourth is the `from os import environ` alias, which no site used but
        which would otherwise be a silent way back in.
        """
        for source in (
            'import os\nx = os.getenv("GITHUB_TOKEN")\n',
            'import os\nx = os.environ.get("GITHUB_TOKEN", "")\n',
            'import os\nx = os.environ["GH_TOKEN"]\n',
            'from os import environ\nx = environ.get("GITHUB_TOKEN")\n',
        ):
            probe = tmp_path / "probe.py"
            probe.write_text(source)
            found = _violations_in(probe)
            assert [s for s in found if s.startswith("env:")], source

    def test_a_reintroduced_board_token_read_in_mcp_is_caught(self, tmp_path):
        """#611's own regression, in the layer and the shape it happened in.

        The probe is `sync_board`'s removed body, near enough: the pair read,
        joined into `email:token`, sent as `X-Integration-Token`. Anyone putting
        it back writes something this detector must see -- so exercise the
        detector on it directly, rather than trusting that a whole-tree scan of
        code that no longer contains it proves the matcher still works.
        """
        probe = tmp_path / "probe.py"
        probe.write_text(
            "import os\n"
            'email = os.getenv("BOARD_API_EMAIL")\n'
            'token = os.getenv("BOARD_API_TOKEN")\n'
            'headers = {"X-Integration-Token": f"{email}:{token}"}\n'
        )
        assert "env:BOARD_API_TOKEN" in _violations_in(probe)
        # The email half is not a credential and is deliberately not reported;
        # if it ever is, the docstring's stated reason has silently changed.
        assert "env:BOARD_API_EMAIL" not in _violations_in(probe)

    def test_every_board_type_this_repo_supports_has_a_covered_env_name(self):
        """`register_board`'s per-type fallback was a map, so one gap is enough.

        It resolved a token by board type; a type whose env name is missing from
        `SHARED_CREDENTIAL_ENV` is a reintroduction the gate would wave through
        while reporting the other four. Board types come from the enum rather
        than a hand-typed list -- a sixth BoardType then fails here instead of
        being silently uncovered.
        """
        from src.domain.board import BoardType

        # `github` is absent on purpose: `BoardType` has four members and never
        # had a GITHUB one, though the removed MCP fallback offered a `github`
        # branch resolving `GH_TOKEN`/`GITHUB_TOKEN`. Those two names are covered
        # regardless -- by #554, as GitHub credentials.
        covered = {
            BoardType.TRELLO: {"TRELLO_TOKEN", "BOARD_API_TOKEN"},
            BoardType.JIRA: {"JIRA_TOKEN", "BOARD_API_TOKEN"},
            BoardType.LINEAR: {"LINEAR_API_KEY", "LINEAR_TOKEN", "BOARD_API_TOKEN"},
            BoardType.NOTION: {"NOTION_TOKEN", "BOARD_API_TOKEN"},
        }
        assert set(BoardType) == set(covered), (
            "a board type has no entry here -- decide which env name(s) would "
            "carry its credential and cover them, or the gate has a blind spot"
        )
        for board_type, names in covered.items():
            assert names <= SHARED_CREDENTIAL_ENV, board_type

    def test_a_board_token_literal_in_the_secret_scanner_is_not_a_read(self):
        """`container_guardrails.py` lists board names as scan patterns too.

        Same point as the GITHUB_TOKEN case above, now load-bearing for a second
        symbol: adding `BOARD_API_TOKEN` to the gate must not flag the file whose
        job is to *name* it.
        """
        guardrails = SRC / "services" / "container_guardrails.py"
        assert "BOARD_API_TOKEN" in guardrails.read_text()
        assert not [s for s in _violations_in(guardrails) if s.startswith("env:")]
