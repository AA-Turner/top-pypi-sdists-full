# ---------------------------------------------------------------------------
# WHICH `probe` COMMANDS WRITE. One list, read by the plugin's guard hook and by
# the CLI's own write gate (`probe.cli.write_gate`), so the two can never
# disagree about what a command IS. Moved here from `tracking_guard.py`, which
# re-exports the names.
# ---------------------------------------------------------------------------

#: Top-level probe commands that record research content whatever follows them.
#: `flush` is deliberately absent: draining an outbox delivers writes recorded
#: BEFORE the researcher flipped the switch, and honouring the pre-off record is
#: what "off deletes nothing" means.
TOP_LEVEL_WRITES = frozenset(
    {"log", "link", "snapshot", "exec", "backfill", "import"}
)

#: Command groups whose verbs write research content unless the verb is a read.
#: `session` is deliberately absent (it is the switch itself -- refusing
#: `probe session track` would wall the researcher out of the un-mute), and so
#: are the read groups and the machine-plumbing groups (context, token, mcp,
#: workspace, shared, outbox, companion).
WRITE_GROUPS = frozenset(
    {
        "project",
        "experiment",
        "run",
        "artifact",
        "notes",
        "span",
        "group",
        "edge",
        "trial",
        "views",
        "paper",
        "wandb",
        # `probe version create` mints an experiment version (a recorder's
        # write, track-work reference; `version list` reads). Missing here, the
        # write gate and the daemon profile's guard both let it through (live
        # T13 on the released 0.111.2 plugin, 2026-09-29).
        "version",
        # The data catalog (data-catalog C5): `source add`, `dataset add|use`
        # and `checkpoint use` record; `list`, `show` and `download` read.
        "source",
        "dataset",
        "checkpoint",
        # A project's or experiment's summary and its Metrics-center visuals,
        # kept by the recorder (writer-owns-summary): `summary push` and
        # `visuals set` record; `summary checkout` and `visuals options` read.
        "summary",
        "visuals",
    }
)

#: Every subgroup inside a write group, and `session home`. Its OWN verb decides,
#: so `project code list` reads while `project code attach` writes; read two words
#: deep, every `project code` command looked like one write. Keys in the tables
#: below name the three words (`wandb key set`); a bare subgroup key never matches.
SUBGROUPS = frozenset({"project code", "project reference", "run input", "wandb key", "session home"})

#: Commands that only read unless given one of these flags: bare
#: `project contributors` lists who is credited, `--add`/`--remove` change it.
#: An argument the shell has not expanded yet (the guard hook reads the command
#: TEXT) could be one of them, so it counts as a write too.
READ_UNLESS_FLAGS = {"project contributors": frozenset({"--add", "--remove"})}

#: Characters that mark a word the shell still expands (`$F`, `$(...)`, `--{add,x}`).
#: Glob characters count only in an option's NAME (`--a[d]d`): a literal `[::1]`
#: in a `--base-url` value is common.
_SHELL_EXPANSION_CHARS = frozenset("$`{")
_GLOB_CHARS = frozenset("*?[")

#: Verbs inside a write group that only read. Unknown verbs count as writes --
#: the group already said "research content".
READ_VERBS = frozenset(
    {
        "show",
        "list",
        "get",
        "status",
        "versions",
        "cat",
        "diff",
        "search",
        "events",
        "coordinates",
        "download",
        "help",
        # `probe notes team` PRINTS the team note.
        "team",
        "check",
        "reproduce",
        # `probe notes checkout` pulls a note into a local file; the edit lands
        # later through `push`. `audit-advisory` prints the note-size nudge the
        # `note_audit` hook shows.
        "checkout",
        "audit-advisory",
        # Print what is already recorded: `artifact tree|pin-impact`,
        # `experiment|paper edges`, `run metrics|series`, `views data|preview`
        # (a preview evaluates a spec without saving it).
        "tree",
        "pin-impact",
        "edges",
        "metrics",
        "series",
        "data",
        "preview",
        # `run inputs|upstream`: what a run read and built on (lineage plan L5).
        "inputs",
        "upstream",
        # `experiment|project lineage`: the entity's own links in and out.
        "lineage",
        # `experiment inherited`: what a fork reads live from its source.
        "inherited",
        # `project branches`, `experiment branch`: the lines of work.
        "branches",
        "branch",
        # `paper citations|graph`: the citation links the server read from
        # bibliographies (citation graph, Track C).
        "citations",
        "graph",
        # `paper find`: the research literature (the MCP's `find_papers`), an
        # outside index; it adds nothing to the team's records.
        "find",
        # `visuals options`: what a summary's tables and charts may name.
        "options",
    }
)

#: Verbs inside a write group that REMOVE research rather than record it. Never
#: refused: cleanup must stay possible in every state.
REMOVAL_VERBS = frozenset({"delete", "remove", "rm", "prune", "purge"})

#: "group verb" pairs (three words under a `SUBGROUPS` entry) inside a write
#: group that are machine plumbing, not a
#: record of the work, so no state refuses them. `notes sync` is the team note's
#: own sync, which hooks run in the background and which the switch has never
#: governed (see `version_check._spawn_session_maintenance`); `project use` only sets the
#: local default project. `wandb discover` scans a local folder and `wandb key
#: set|status` store or check a local credential: none of them talks to Probe.
UNGATED_COMMANDS = frozenset(
    {"notes sync", "project use", "wandb discover", "wandb key set", "wandb key status"}
)

#: `probe companion feedback` steers the daemon (its note reaches the model as
#: the researcher's correction), so from an agent session it is only admitted
#: with `--directed`, in every state.
DIRECTED_ONLY = frozenset({"companion feedback"})

#: Root `probe` options that take a VALUE (the root callback in `cli/main.py`).
#: Their value is not a command word: `probe --base-url URL notes push` runs
#: `notes push`, and reading the URL as the command waved that write through.
ROOT_VALUE_OPTIONS = frozenset({"--base-url", "--spool-dir"})

#: The only help flag the CLI has (`-h` is not registered: click refuses it).
HELP_FLAG = "--help"

#: Groups whose whole job is READING research content. Refused only under `off`.
#: `docs` reads Probe's own docs, not the team's record: a read so that `off`
#: refuses it as it refuses `paper find`.
READ_GROUPS = frozenset(
    {"metrics", "series", "get", "bundle", "events", "coordinates", "shared", "provenance", "docs"}
)

#: Commands inside a `READ_GROUPS` group that record rather than print:
#: `metrics backfill` stores a derived curve, `shared add` uploads into the
#: team's Shared folder, `shared share|unshare` move a file into or out of it.
#: Read as reads, `read` let them through.
READ_GROUP_WRITES = frozenset({"metrics backfill", "shared add", "shared share", "shared unshare"})

#: ...and the ones that remove: cleanup, never refused, as `REMOVAL_VERBS` is in
#: a write group. Read as reads, `off` refused them.
READ_GROUP_REMOVALS = frozenset({"metrics delete", "shared delete"})

#: Commands of a plumbing group (not in WRITE_GROUPS) that record research
#: content: `workspace set` picks the workspace's best experiment, `session home
#: set|clear` where the session's runs go (the daemon's: not in DAEMON_AGENT_WRITES).
PLUMBING_GROUP_WRITES = frozenset({"workspace set", "session home set", "session home clear"})

#: WHAT THE AGENT STILL WRITES IN THE `daemon` STATE, without `--directed`: the
#: launch of a run, the run's own data -- the `instrument-code` surface the
#: daemon never authors -- and the project a run needs when none fits (daemon v2,
#: D2 / S11; every run has a project since floating runs retired). The
#: experiment and sweep group a run belongs in, and renaming or moving projects
#: and runs, stay the DAEMON's. Keys are "group verb" (three
#: words under a `SUBGROUPS` entry), or the bare top-level command.
#: `probe session status` prints this list as `daemon.agent_writes`, and
#: `DAEMON_CONTEXT` below says the same thing in words.
#: `run token` mints, extends or revokes the one-run token a remote job records
#: with: part of the launch (`probe exec --detached-launcher` mints one), and
#: the run's expiry alert tells the agent to `--extend` it.
DAEMON_AGENT_WRITES = frozenset(
    {
        "exec",
        "log",
        "snapshot",
        "project create",
        "run start",
        "run child",
        "run fork",
        "run end",
        "run token",
        "span add",
        "trial add",
        "trial stage",
        "trial export",
        "trial drain",
        "trial watch",
        "trial reconcile",
        "trial expand",
    }
)

#: Writes that are the run's OWN data only when a run makes them: inside a
#: `probe exec` job or an SDK script (`PROBE_RUN_ID` set), a `probe artifact add`
#: attaches the run's file, the same write the SDK's `log_artifact` makes there
#: ungated. From the agent's own shell it is the daemon's (an artifact the
#: session made), so it stays out of `DAEMON_AGENT_WRITES`. The CLI's write gate
#: admits it only anchored to the run (no `--project`, `--experiment`,
#: `--workspace`, `--shared` or `--from-manifest`).
DAEMON_RUN_WRITES = frozenset({"artifact add"})

#: The flag that marks a write the researcher asked for. The CLI strips it
#: before parsing (it may appear anywhere after `probe`), and the gate lets a
#: marked write through the `daemon` state; the daemon sees it in the transcript
#: and does not repeat it.
DIRECTED_FLAG = "--directed"

#: What a refusal tells the agent about `DIRECTED_FLAG`: the `daemon` state's
#: (`DENY_REASON_DAEMON`) and the daemon profile's, for a write
#: (`DAEMON_PROFILE_DENY_WRITE`).
DIRECTED_RETRY = "If the researcher asked for exactly this, run it again with `--directed`."
#: ...and the daemon-profile agent's other way to a write (Richard's approved
#: text, 2026-10-13): a request to the daemon's writer (`probe ask --writer`).
WRITER_RETRY = 'Otherwise ask the daemon\'s writer: `probe ask --writer "<request>"`.'


def carries_directed(args: "list[str]") -> bool:
    """Do these args (after `probe`) carry `DIRECTED_FLAG` where the CLI reads it?

    Before a standalone `--` only, as `write_gate.split_directed` strips it:
    after that it belongs to the command `probe exec` launches.
    """
    own = args[: args.index("--")] if "--" in args else args
    return DIRECTED_FLAG in own


def command_words(args: "list[str]") -> "list[str]":
    """The (at most three) words click dispatches on, from the args after `probe`.

    The classifier treats the third as a command word only under a `SUBGROUPS`
    entry; anywhere else it is the command's first argument, and is ignored.
    Mirrors click's own resolution closely enough for a gate: options are
    skipped, and so is the VALUE of a root option that takes one; a `--` before
    the command words is skipped too (click still dispatches the command after
    it), while after `exec` everything past `--` is the launched command.
    """
    words: "list[str]" = []
    skip_value = False
    for token in args:
        if skip_value:
            skip_value = False
            continue
        if token == "--":
            if words[:1] == ["exec"]:
                break
            continue
        if token.startswith("-"):
            if not words and token in ROOT_VALUE_OPTIONS:
                skip_value = True
            continue
        words.append(token)
        if len(words) == 3:
            break
    return words


def classify_probe_args(args: "list[str]") -> "tuple[str | None, str]":
    """`(kind, matched)` for the args after `probe`; kind is write/read/None.

    `matched` is `probe <head>` or `probe <head> <verb>`, the words a refusal
    names; under a `SUBGROUPS` entry `<head>` is the subgroup's two words. The
    ONE classifier: the CLI's write gate and the plugin's guard hook both call it.
    """
    words = command_words(args)
    if not words:
        return (None, "")
    group = head = words[0]
    verb = words[1] if len(words) > 1 else ""
    if head + " " + verb in SUBGROUPS:
        head, verb = head + " " + verb, words[2] if len(words) > 2 else ""
    command = head + " " + verb
    if command in UNGATED_COMMANDS:
        return (None, "probe " + command)
    if head in TOP_LEVEL_WRITES:
        return ("write", "probe " + head)
    if command in READ_GROUP_WRITES or command in PLUMBING_GROUP_WRITES:
        return ("write", "probe " + command)
    if command in READ_GROUP_REMOVALS:
        return (None, "probe " + head)
    if head in READ_GROUPS:
        return ("read", "probe " + head)
    if command in DIRECTED_ONLY:
        return ("write", "probe " + command)
    if command in READ_UNLESS_FLAGS:
        writes = _flag_writes(args, READ_UNLESS_FLAGS[command])
        return ("write" if writes else "read", "probe " + command)
    if group in WRITE_GROUPS:
        if verb in READ_VERBS:
            return ("read", "probe " + command)
        if verb and verb not in REMOVAL_VERBS:
            return ("write", "probe " + command)
    return (None, "probe " + head)


def daemon_allows_agent(matched: str) -> bool:
    """Does the `daemon` state leave this write to the agent? (`matched` from
    `classify_probe_args`.)"""
    key = matched[len("probe "):] if matched.startswith("probe ") else matched
    return key in DAEMON_AGENT_WRITES


#: THE DAEMON PROFILE (daemon reads): the machine installed the lean
#: `probe-research-daemon` plugin, so the daemon records AND reads, and the main
#: agent's `probe` is `ask`, `exec`, its runs' own data (`DAEMON_AGENT_WRITES`),
#: reads of one run (`DAEMON_PROFILE_RUN_READS`), `session status` and Probe's
#: own upkeep (`DAEMON_PROFILE_ALLOWED`). The guard in that
#: plugin refuses every other `probe` command, reads included, with
#: `DAEMON_PROFILE_DENY` (the approved text, pinned by `test_daemon_profile.py`:
#: `agent/tests/fixtures/daemon_prompts/reads/agent-facing/guard-refusal.NEW.md`), except a write
#: the researcher asked for (`--directed`), which runs as in the `daemon` state.
#: `probe --version` needs no entry (no command words); `probe version` is the
#: experiment-versions group, a write. While the researcher has Probe inline
#: (`is_inline`) the guard refuses only `RESEARCHER_SWITCH`.
#: `paper find` reads the research literature, an outside index, not the team's
#: records, so the agent runs it itself (Richard 2026-10-12: "just the tools
#: where it makes sense for the agent to call it directly"). `docs` searches
#: Probe's own docs, an outside source too and not the team's records: the same
#: rule, and the only way this profile reaches them (it has no MCP). `feedback send`
#: holds feedback for the Probe team as a question for the researcher
#: (`probe.feedback`); nothing leaves without their yes. `approvals` lists the
#: questions the daemon holds for the researcher: in an agent's shell the CLI
#: only lists them and answers nothing (`daemon_cli.approvals_cmd`). Never
#: `deny`: a no is the researcher's.
#: The rest, none a listing of the team's work: what Probe's own messages send
#: the agent to -- `outbox status` (the banner on every command, a `run end`
#: that could not close), `run check` (the SDK's capture warning), `sync` (an
#: offline run's "deliver it with `probe sync`"), `artifact download`
#: (`instrument-code`: a checkpoint back, bytes `probe ask` cannot hand over) --
#: and this machine's diagnostics: `daemon status` (is the daemon `probe ask`
#: waits on alive), `whoami` and `context list` (which team the runs land in),
#: `wandb discover` and `wandb key status` (local scans ahead of a `--directed`
#: W&B import).
#: And Probe's own upkeep: keeping this machine's Probe updated, running and
#: delivering (`update`, `status`, `service`, `outbox drain|retry|watch`,
#: `flush`, `token list`), local files (`draft edit`, `file preview`), and
#: team-note and managed-block upkeep. A daemon-profile agent could not run `probe update
#: --check` (2026-10-21) while nothing it ran touched the team's records.
#: A list, not "whatever the classifier calls neither read nor write": a word
#: the guard cannot read (`probe $G delete r1`) or a command added later stays
#: refused, and `test_daemon_profile.py` sorts every such command into this list
#: or the daemon's, so a new one fails a test instead of going stale here.
#: The daemon's, though the classifier says neither: what moves the key, account,
#: server or folder the daemon records with (`login` -- `PROBE_BASE_URL` in the
#: environment moves the server, out of the guard's sight -- `logout`, `context
#: use|delete`, `workspace use`, `project use`, `token revoke`, `session
#: initialize`), what drops, holds or releases queued writes (`outbox
#: discard|pause|resume`), the team's permissions and workspaces, printed
#: secrets (`mcp headers|env`, `token create`), the researcher's agent settings
#: (`statusline install|uninstall`), and the daemon's own ledger and install.
#: `session send` messages one of the researcher's own sessions (an orchestrator
#: steering its workers, G7): the server takes it only for a session of the same
#: person and labels it as from an agent session, never as the researcher.
#: `session owed` reads the session's own owed ledger (notes parity N3); the
#: plugin's end-of-turn hook runs it, and the agent may too. `session home show`
#: prints where this session's runs go, as `session status` does. `cli search`
#: searches this CLI's own commands, on this computer.
DAEMON_PROFILE_ALLOWED = frozenset(
    {"ask", "session status", "session parent", "session send", "ignore check", "run expect", "doctor", "paper find",
     "docs", "cli search", "feedback send", "approvals", "outbox status", "run check", "sync", "artifact download",
     "daemon status", "whoami", "context list", "wandb discover", "wandb key status",
     "update", "status", "flush", "service status", "service start", "service stop", "service check-now",
     "token list", "context show", "outbox drain", "outbox retry", "outbox watch", "statusline status",
     "statusline show", "mcp status", "workspace list", "workspace get", "workspace writers show",
     "access-group list", "notes sync", "agent-rules refresh", "wandb key set", "draft edit",
     "file preview", "feedback flush", "capy sync", "capy disconnect", "session owed", "session home show"}
)

#: Reads of ONE run, named by its id: the agent looks at the runs it launched
#: (is the loss falling, did the checkpoint land) without waiting on `probe ask`
#: (Richard 2026-10-21: the agent should see its own runs). Any run id passes --
#: the hook cannot tell this session's runs from a teammate's, and the ids an
#: agent holds are the ones `probe exec` printed or the daemon handed it.
#: Listings and searches across the team's work (`run list`, `series latest`,
#: `artifact list`, `provenance`, `commits`) stay the daemon's, through `probe ask`.
DAEMON_PROFILE_RUN_READS = frozenset(
    {"run get", "run series", "run metrics", "run inputs", "run upstream", "run reproduce", "get",
     "bundle", "events", "metrics wide", "metrics plot", "metrics export", "metrics grouped",
     "span list", "span get", "trial list", "trial get", "artifact tree", "artifact versions",
     "snapshot-show"}
)

#: ...but not where a flag writes what it read: `run reproduce --materialize`
#: restores the run's captured tree, as the kept `snapshot-restore` does, and
#: `--export` writes a file. A word the shell still expands may be either.
DAEMON_PROFILE_RUN_READ_WRITES = {"run reproduce": frozenset({"--materialize", "--export"})}

#: `probe wizard` (and its old name `setup`) also holds the researcher's own
#: settings -- who records, capture, the new-session default, imports,
#: uninstall, and signing in and out, which set the account, server and key the
#: daemon records with -- so the daemon profile runs it plainly only: for one of
#: these actions, with no flag but `DAEMON_PROFILE_PLAIN_FLAGS`, nothing
#: positional and no root option. `probe install` (the guided install) is kept
#: outright.
DAEMON_PROFILE_WIZARD_ACTIONS = frozenset({"update", "diagnose"})
DAEMON_PROFILE_PLAIN_FLAGS = {
    "wizard": frozenset({"--action", "--yes", "-y", "--json", "--no-browser"}),
    "setup": frozenset({"--action", "--yes", "-y", "--json", "--no-browser"}),
}

#: The researcher's switch and defaults, typed into a shell. In the daemon
#: profile the agent never moves them (`probe session state inline` included):
#: not under `off`, and not while Probe is inline. The researcher moves them
#: with `/probe`, which reaches the hooks, not a shell.
RESEARCHER_SWITCH = frozenset(
    {"session state", "session toggle", "session track", "session untrack", "session default"}
)

#: What the guard answers an agent that types one of `RESEARCHER_SWITCH`.
INLINE_SWITCH_DENY = (
    "`{matched}` moves the researcher's Probe switch, so it was refused before it ran: only "
    "the researcher moves it (`/probe on`, `/probe read`, `/probe off`, `/probe inline`)."
)

#: What the guard answers an agent the daemon records for that types one of
#: `RESEARCHER_SWITCH`. Kimi runs a typed `/probe on` through a hook whose output
#: never reaches the model, so the agent reads the skill, goes looking for the
#: command itself, and lands here: the answer is that the move already happened,
#: never `DAEMON_PROFILE_DENY`'s pointer to `/probe inline`.
RESEARCHER_SWITCH_DENY = (
    "`{matched}` moves the researcher's Probe switch, so it was refused before it ran: only "
    "the researcher moves it (`/probe on`, `/probe read`, `/probe off`, `/probe inline`), and "
    "a `/probe` they typed has already moved it. `probe session status` prints where it landed."
)

DAEMON_PROFILE_DENY = (
    'The Probe daemon records this session and reads the team\'s work for you, so `{matched}` was refused before it ran. You instrument your runs with the SDK and can read one by its id (`probe run get <id>`). To ask about the team\'s prior work: `probe ask "<question>"`. If you need to do it yourself, ask the researcher to type `/probe inline`.'
)

#: `DAEMON_PROFILE_DENY` for a WRITE: `--directed` admits one the researcher
#: asked for, and the daemon's writer takes any other (`probe ask --writer`). A
#: read keeps the plain text: no flag admits it, `probe ask` reads.
DAEMON_PROFILE_DENY_WRITE = DAEMON_PROFILE_DENY + "\n\n" + DIRECTED_RETRY + " " + WRITER_RETRY

#: What the papers hook answers a paper-type web search it holds (`papers_hook.py`):
#: at most once per `PAPER_FIND_WINDOW_S`, and never after `probe paper find` ran
#: inside it. Richard approved the wording 2026-10-12.
PAPER_SEARCH_HOLD = (
    "Probe searches research papers, so this web search was held. Run "
    '`probe paper find "<the question as a sentence>"` first. After that, web searches run '
    f"normally for {PAPER_FIND_WINDOW_S // 60} minutes."
)


#: `.probe.config`: paths at `read` or `off`, which Probe never records (`probe_config.py`).
EXCLUDED_DENY = (
    "`{path}` is excluded by `{source}`, so `{matched}` was refused before it ran. Probe "
    "records nothing about it; do not route around it."
)

#: A `.probe.config` above the launch folder: asked once per session, under `on`.
PARENT_ASK = (
    "`{files}`, above where this session started, blocks Probe from recording some paths here. "
    "Ask the researcher once: follow it, or set it aside for this session? Record their answer "
    "with `probe session parent follow --directed` or `probe session parent ignore --directed`. "
    "It is followed until then; never choose for them."
)

PARENT_ASK_DENY = "`{matched}` was held back so you ask this first; retry it after. " + PARENT_ASK

#: Session start, when any `.probe.config` reaches this session's folder: every
#: profile, the daemon's included (Richard 2026-10-09, his wording). `read` and
#: `off` paths alike: the agent records neither.
EXCLUDED_CONTEXT = "`.probe.config` blocks Probe from recording: {paths}."


def moves_switch(args: "list[str]") -> "str | None":
    """`probe <words>` when these args (after `probe`) move the researcher's
    switch (`RESEARCHER_SWITCH`), else None."""
    two = " ".join(command_words(args)[:2])
    return "probe " + two if two in RESEARCHER_SWITCH else None


def daemon_profile_allows(args: "list[str]") -> "tuple[bool, str]":
    """`(allowed, matched)` for the args after `probe` in the daemon profile.

    A write carrying `--directed` is allowed, as the CLI's gate allows it in the
    `daemon` state (`write_gate.refusal`). A read is not (reads go through
    `probe ask`) but one run's (`DAEMON_PROFILE_RUN_READS`), and neither is the
    researcher's switch (`RESEARCHER_SWITCH`). Probe's own upkeep runs
    (`DAEMON_PROFILE_ALLOWED`); the wizard runs only plainly
    (`DAEMON_PROFILE_PLAIN_FLAGS`). Anything else -- a word the guard cannot
    read included -- is refused.
    """
    words = command_words(args)
    if not words:
        return (True, "probe")
    head = words[0]
    two = " ".join(words[:2])
    if head in DAEMON_PROFILE_PLAIN_FLAGS:
        return (_runs_plainly(args, head), "probe " + head)
    for key in (" ".join(words[:3]), two, head):
        if key in DAEMON_PROFILE_ALLOWED:
            return (True, "probe " + key)
        if key in DAEMON_PROFILE_RUN_READS:
            return (not _flag_writes(args, DAEMON_PROFILE_RUN_READ_WRITES.get(key, frozenset())), "probe " + key)
    kind, matched = classify_probe_args(args)
    if kind == "write" and carries_directed(args) and two not in RESEARCHER_SWITCH:
        return (True, matched)
    return (daemon_allows_agent(matched), matched)


def _runs_plainly(args: "list[str]", head: str) -> bool:
    """Is this `head` (the wizard) run with nothing but
    `DAEMON_PROFILE_PLAIN_FLAGS`, and with every `--action` one of
    `DAEMON_PROFILE_WIZARD_ACTIONS`? Every `--action`, because click runs the
    LAST of a repeated one (`--action update --action recorder` runs
    `recorder`); a word the shell still expands matches nothing."""
    rest = list(args)
    rest.remove(head)
    flags = DAEMON_PROFILE_PLAIN_FLAGS[head]
    actions = 0
    i = 0
    while i < len(rest):
        name, eq, value = rest[i].partition("=")
        if name == "--action":
            if not eq:
                value = rest[i + 1] if i + 1 < len(rest) else ""
                i += 1
            if value not in DAEMON_PROFILE_WIZARD_ACTIONS:
                return False
            actions += 1
        elif eq or rest[i] not in flags:
            return False
        i += 1
    return actions > 0


def _flag_writes(args: "list[str]", flags: "frozenset[str]") -> bool:
    """Does one of these args name one of `flags` (`--flag=value` too), or may it
    once the shell expands it (`$F`, `--{add,x}`, `--a[d]d`)?"""
    return bool(flags) and any(
        name in flags
        or not _SHELL_EXPANSION_CHARS.isdisjoint(arg)
        or (name.startswith("-") and not _GLOB_CHARS.isdisjoint(name))
        for arg in args
        for name in [arg.split("=", 1)[0]]
    )


def daemon_profile_deny(args: "list[str]", matched: str) -> str:
    """The refusal for args `daemon_profile_allows` refused: a write is told
    that `--directed` runs it (`DAEMON_PROFILE_DENY_WRITE`)."""
    kind, _matched = classify_probe_args(args)
    deny = DAEMON_PROFILE_DENY_WRITE if kind == "write" else DAEMON_PROFILE_DENY
    return deny.format(matched=matched)


#: The refusals, shared by the guard hook and the CLI gate. Placeholders:
#: `{matched}` is the command the refusal names.
DENY_REASON = (
    "Probe is READ-ONLY for this conversation, so `{matched}` was refused before it ran. Reads "
    "are still fine. If the researcher wants this recorded they set `/probe on`; say so once, "
    "do not ask them to approve the call, and do not route around it."
)

DENY_REASON_OFF = (
    "Probe is OFF for this conversation, so `{matched}` was refused before it ran. Make no "
    "Probe calls at all, reads included: you cannot see prior work and cannot know what you "
    "missed, so say you could not look rather than reporting nothing was found; turning it "
    "back on does not backfill the gap. Only the researcher changes the state (`/probe read` "
    "restores searching); a repeat request is not permission: do not ask them to approve this "
    "call, and do not route around it."
)

DENY_REASON_DAEMON = (
    "The Probe daemon is recording this conversation (the `daemon` state), so `{matched}` was "
    "refused before it ran: that write is the daemon's (it files runs in an experiment and "
    "group, and renames or moves projects and runs). Yours are starting runs in a project "
    "(`probe project create <slug>` if none fits), the run's own data and `probe run end`; "
    "`probe session status` lists them.\n\n" + DIRECTED_RETRY
)

#: THE ONE STATEMENT OF WHO WRITES WHAT IN THE `daemon` STATE. Every surface that
#: tells the agent about the split carries this meaning; the hooks read this
#: constant (session start in `version_check`, the flip and the recovery in
#: `tracking_guard`), pi's `daemonNotice.ts` keeps a copy, and
#: `tests/test_daemon_split_texts.py` holds the rest (the skills, the refusal,
#: the after-the-fact notice) to the same nouns. The agent's list is
#: `DAEMON_AGENT_WRITES`. The daemon ending a run the agent left open is a
#: BACKSTOP, not the plan, so `run end` stays the agent's.
DAEMON_CONTEXT = (
    "The Probe daemon is recording this session: you launch and instrument runs, and the daemon "
    "records. Yours: start runs (a run on this machine naming no project goes to this session's "
    "project, which the daemon sets: `probe session home show` prints it; pass `project=` or "
    "`--project` for another, and before it is set pass one, or `probe project create <slug>` if "
    "none fits), "
    "the run's own data (metrics, spans, trials, files the run "
    "itself attaches) and `probe run end` when a run finishes. The daemon's: everything else, "
    "including the experiment and sweep group a run is filed in, renaming or moving projects "
    "and runs, and its notes, artifacts, papers, tags, names, descriptions and lineage, read "
    "from the transcript; it also ends any run you leave open. If the researcher asks for one "
    "of the daemon's writes, add `--directed`."
)


# ---------------------------------------------------------------------------
# THE DAEMON'S QUESTIONS ARE NOT THE AGENT'S TO ANSWER.
# ---------------------------------------------------------------------------

#: Where the Probe daemon keeps the questions it holds for the researcher and
#: their answers (`probe.daemon.approvals`): `<state>/probe/approvals`.
APPROVALS_DIRNAME = "approvals"

#: The guard hook's refusal of a coding-agent tool call aimed at that folder.
DENY_REASON_APPROVALS = (
    "`{tool}` would touch {path}, where the Probe daemon keeps the questions it holds for the "
    "researcher and their answers, so it was refused before it ran. Only the researcher answers "
    "them: through your question tool, word for word, or `probe approvals` in their own "
    "terminal. Do not write there, and do not route around this."
)

#: Tools that write a file named by one input field.
#: The argument naming the file, per write tool. Claude Code's Write/Edit take
#: `file_path`; Kimi Code's take `path` (relative to the session's folder). Both
#: are checked whichever harness sent the call: a forged answer is refused by
#: any name it uses.
_FILE_WRITE_TOOLS = {"Write": ("file_path", "path"), "Edit": ("file_path", "path"),
                     "MultiEdit": ("file_path",), "NotebookEdit": ("notebook_path",)}
#: The folder as a command's text names it (`~/.local/state/probe/approvals/answers/x.json`,
#: `$XDG_STATE_HOME/probe/approvals`, `cd probe && ... approvals/...`).
_APPROVALS_TEXT = re.compile(r"probe/+approvals\b|\bapprovals/+(answers|requests|keys|asked)\b")


def approvals_dir() -> Path:
    return state_dir() / APPROVALS_DIRNAME


def touches_approvals(tool_name: object, tool_input: object, cwd: "str | None" = None) -> "str | None":
    """The approvals path a coding agent's tool call aims at, or None.

    A TRIPWIRE, NOT A BOUNDARY: the agent runs as the same user as the daemon,
    so a script that builds the path at run time still reaches the folder. What
    this refuses is the plain way -- a Write/Edit whose file is in there, a Bash
    command that names it -- and that is what a model talked into "answering"
    a question for the researcher would try first. The daemon's own checks
    (`approvals.verify_held`, the lease) are what a yes must still pass.
    """
    if not isinstance(tool_input, dict):
        return None
    fields = _FILE_WRITE_TOOLS.get(tool_name) if isinstance(tool_name, str) else None
    if fields is not None:
        root = os.path.realpath(str(approvals_dir()))
        for field in fields:
            target = tool_input.get(field)
            if not isinstance(target, str) or not target:
                continue
            path = os.path.expanduser(target)
            if not os.path.isabs(path) and isinstance(cwd, str) and cwd:
                # A relative path is the SESSION's (Kimi resolves it against the
                # session folder; a hook runs from the plugin folder).
                path = os.path.join(cwd, path)
            real = os.path.realpath(path)
            if real == root or real.startswith(root.rstrip(os.sep) + os.sep):
                return target
        return None
    if tool_name == "Bash":
        command = tool_input.get("command")
        if isinstance(command, str) and (
            _APPROVALS_TEXT.search(command) or str(approvals_dir()) in command
        ):
            return str(approvals_dir())
    return None


#: The guard hook's refusal of a coding-agent tool call aimed at the per-session
#: state folder. Those files (`<sid>.state`, `<sid>.inline`, `<sid>.profile`, the
#: lease) are what the guard itself reads to decide a verdict, so writing one --
#: forging `on (inline)`, say -- would turn the guard off. Only the researcher's
#: `/probe` switch moves that state.
DENY_REASON_SESSIONS = (
    "`{tool}` would write {path}, where Probe records which conversation this is and whether the "
    "researcher has it recording -- the files this guard reads to decide. Changing them yourself "
    "would turn the guard off, so it was refused before it ran. Only the researcher's `/probe` "
    "switch moves that state; do not write there, and do not route around this."
)

#: The sessions folder as a command's text names it.
_SESSIONS_TEXT = re.compile(r"probe/+sessions\b")


def touches_sessions_dir(tool_name: object, tool_input: object, cwd: "str | None" = None) -> "str | None":
    """The per-session-state path a coding agent's tool call aims at, or None.

    The same tripwire as `touches_approvals`, for the folder whose files decide
    the guard's own verdict (state, inline marker, profile, lease). A TRIPWIRE,
    NOT A BOUNDARY: the agent runs as the same user, so a path built at run time
    still reaches the folder. What this refuses is the plain way -- the forge a
    model talked into bypassing the guard would write first.
    """
    if not isinstance(tool_input, dict):
        return None
    fields = _FILE_WRITE_TOOLS.get(tool_name) if isinstance(tool_name, str) else None
    if fields is not None:
        root = os.path.realpath(str(sessions_dir()))
        for field in fields:
            target = tool_input.get(field)
            if not isinstance(target, str) or not target:
                continue
            path = os.path.expanduser(target)
            if not os.path.isabs(path) and isinstance(cwd, str) and cwd:
                path = os.path.join(cwd, path)
            real = os.path.realpath(path)
            if real == root or real.startswith(root.rstrip(os.sep) + os.sep):
                return target
        return None
    if tool_name == "Bash":
        command = tool_input.get("command")
        if isinstance(command, str) and (
            _SESSIONS_TEXT.search(command) or str(sessions_dir()) in command
        ):
            return str(sessions_dir())
    return None


#: The guard hook's refusal of a coding-agent shell command that calls the
#: Probe service's mailbox (or has it run a hook event) itself (#3355;
#: `tracking_guard.calls_mailbox`). Placeholder: `{matched}`, the method.
DENY_REASON_MAILBOX = (
    "`Bash` would call the Probe service's `{matched}` itself, so it was refused before it ran. The service's "
    "mailbox is where the Probe daemon's questions for the researcher are answered and its messages to you are "
    "delivered, and only Probe's own hooks and daemon call it. Only the researcher answers the daemon's "
    "questions: through your question tool, word for word, or `probe approvals` in their own terminal. Do not "
    "call it, and do not route around this."
)

#: The guard hook's refusal of a coding-agent shell command that registers or
#: ends a session with the Probe service itself (#3360;
#: `tracking_guard.calls_mailbox`). Placeholder: `{matched}`, the method.
DENY_REASON_SESSION_CALL = (
    "`Bash` would call the Probe service's `{matched}` itself, so it was refused before it ran. The service's "
    "session registry is how Probe knows which conversations its daemon records, and only Probe's own recorder "
    "registers or ends a session. Do not call it, and do not route around this."
)

#: The guard hook's refusal of a coding-agent shell command that runs one of
#: Probe's own hook programs by hand (#3355; `tracking_guard.runs_probe_hook`).
#: Placeholder: `{matched}`, the program.
DENY_REASON_HOOK_BY_HAND = (
    "`Bash` would run Probe's hook program `{matched}` itself, so it was refused before it ran. Probe's hooks act "
    "on the events your harness sends them (the researcher's prompt, their answer to a question); run by hand they "
    "would act on an event you wrote. Only the harness runs them. Do not run them, and do not route around this."
)

#: The guard hook's refusal of a coding-agent tool call aimed at the folder of
#: Probe's warm hook hosts, `/tmp/probe-<uid>`: each host's socket and the key a
#: client must send it before it runs an event (#3355), and the service's own
#: fallback socket. Placeholders: `{tool}`, `{path}`.
DENY_REASON_HOOK_HOST = (
    "`{tool}` would touch {path}, where Probe's hook hosts keep their sockets and the keys that let a hook "
    "event in, so it was refused before it ran. Only your harness sends Probe's hooks their events. Do not "
    "touch it, and do not route around this."
)

def hook_host_dir() -> "str | None":
    """`/tmp/probe-<uid>` (`hooks/dispatch.py` `host_socket`), or None off POSIX."""
    getuid = getattr(os, "getuid", None)
    return os.path.join("/tmp", "probe-%d" % getuid()) if getuid is not None else None


def _hook_host_text() -> "re.Pattern | None":
    """That folder as a command's text names it: THIS user's number (another
    number, `/tmp/probe-42`, is a researcher's own folder), or the number as
    the shell spells it (`$(id -u)` and every `id` form with `-u`, the same in
    backticks, `$UID`, `$EUID`, `${UID}`, `${EUID}`); or one host's socket or
    key by its own name or a glob of it (`hooks-*.key`, never `hooks-tls.key`
    or `git-hooks-server.key`). A glob over `/tmp/probe-*` is
    `_globs_hook_hosts`'."""
    getuid = getattr(os, "getuid", None)
    if getuid is None:
        return None
    return re.compile(
        r"/tmp/+probe-(?:%d(?![0-9A-Za-z_.-])"
        r"|\$\(\s*id\b[^)]*-[A-Za-z]*u[^)]*\)"
        r"|`\s*id\b[^`]*-[A-Za-z]*u[^`]*`"
        r"|\$(?:E?UID\b|\{E?UID\}))" % getuid()
        + r"|(?<![\w.-])hooks-[0-9a-f*?\[\]]{1,16}\.(?:sock|key)\b"
    )


_HOOK_HOST_TEXT = _hook_host_text()
#: A glob in the folder's place: `/tmp/probe-*`, `/tmp/probe-[0-9]*/`.
_TMP_PROBE_GLOB = re.compile(r"/tmp/+(probe-[^/\s'\"`;|&()<>]*[*?\[][^/\s'\"`;|&()<>]*)")


def _globs_hook_hosts(command: str) -> bool:
    """Does a glob after `/tmp/` match this user's `probe-<uid>` (`du -sh
    /tmp/probe-*`)? A glob that cannot (`/tmp/probe-*.pt`) is a researcher's."""
    getuid = getattr(os, "getuid", None)
    if getuid is None:
        return False
    import fnmatch

    mine = "probe-%d" % getuid()
    return any(fnmatch.fnmatchcase(mine, found.group(1)) for found in _TMP_PROBE_GLOB.finditer(command))


def touches_hook_host(tool_name: object, tool_input: object, cwd: "str | None" = None) -> "str | None":
    """The hook hosts' folder a coding agent's tool call aims at, or None: a
    Write/Edit whose file is in it, a Bash command that names it (or one host's
    socket or key). The same TRIPWIRE as `touches_approvals`, NOT A BOUNDARY: a
    path built at run time still reaches it. A host runs an event only for a
    client that sends its key (`hooks/zygote.py`), and the key is in there."""
    folder = hook_host_dir()
    if folder is None or not isinstance(tool_input, dict):
        return None
    fields = _FILE_WRITE_TOOLS.get(tool_name) if isinstance(tool_name, str) else None
    if fields is not None:
        root = os.path.realpath(folder)
        for field in fields:
            target = tool_input.get(field)
            if not isinstance(target, str) or not target:
                continue
            path = os.path.expanduser(target)
            if not os.path.isabs(path) and isinstance(cwd, str) and cwd:
                path = os.path.join(cwd, path)
            real = os.path.realpath(path)
            if real == root or real.startswith(root.rstrip(os.sep) + os.sep):
                return target
        return None
    if tool_name == "Bash":
        command = tool_input.get("command")
        if isinstance(command, str) and (
            (_HOOK_HOST_TEXT is not None and _HOOK_HOST_TEXT.search(command)) or _globs_hook_hosts(command)
        ):
            return folder
    return None


