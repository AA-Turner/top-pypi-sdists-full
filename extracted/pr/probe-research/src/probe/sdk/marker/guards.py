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
        # The live example (agent-prompt install D18): `example start|conclude` record,
        # `status` reads, `keep` and `delete` end it. The agent runs them in every recorder mode.
        "example",
        # Panes (run compare + panes T11): `pane push` records; `data`, `get` and `list` read;
        # `rm` removes.
        "pane",
        # Chart layouts (team flag chart_layouts): `chart set` and `chart layout` record.
        "chart",
        # Pins (pinned views D11): `list` reads; `add` and `rm` run only with `--directed`
        # (DIRECTED_ONLY). Here, not in TOP_LEVEL_WRITES, which would make `list` a write too.
        "pin",
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
        "edits",
        "commands",
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
        # `probe checkpoint best` prints the best save by a named metric.
        "best",
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
        # `project pick`: the projects a run may be filed in (agent-prompt install D22).
        "pick",
        # `run logs`: what a run printed (run logs as a first-class feature).
        "logs",
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
#: set|status` and `wandb login` store or check a local credential: none of them talks to Probe.
#: `wandb key request|receive` (the W&B key drop, fixes-1107b T5) hand that local credential over from
#: the person's browser: they write no record of the work either.
#: `example keep` ends the live example's hold on this chat (its pins) and marks it
#: kept: cleanup, like its delete, so it stays possible in every state.
#: `import folders|review|status` read this computer's chats, folders and import jobs and save a
#: local review; nothing reaches the team's records until `import start|resume`, writes the
#: person asks for (`--directed` in a daemon chat; refused in a `read` or `off` one, D51).
#: `import cancel` stops a local import the person asked to stop (fixes-1107b T6b): what came in stays.
UNGATED_COMMANDS = frozenset(
    {"notes sync", "project use", "wandb discover", "wandb key set", "wandb key status", "wandb login",
     "wandb key request", "wandb key receive", "example keep", "import folders", "import review", "import status",
     "import cancel"}
)

#: `probe companion feedback` steers the daemon (its note reaches the model as
#: the researcher's correction), so from an agent session it is only admitted
#: with `--directed`, in every state. So are `pin add` and `pin rm`: a pin sits at the top of a
#: project's page for the whole team, so an agent pins or unpins only when the researcher asks
#: (pinned views D12).
DIRECTED_ONLY = frozenset({"companion feedback", "pin add", "pin rm"})

#: A write whose flag also makes another command's write, so it is classified as that one and every
#: rule for it applies: `pane push --pin` pins the pane it saves, so it is `pin add` (pinned views
#: D12). The flag is matched as typed: the CLI's own gate sees the expanded argv.
WRITES_ALSO = {"pane push": ("--pin", "pin add")}

#: Root `probe` options that take a VALUE (the root callback in `cli/main.py`).
#: Their value is not a command word: `probe --base-url URL notes push` runs
#: `notes push`, and reading the URL as the command waved that write through.
ROOT_VALUE_OPTIONS = frozenset({"--base-url", "--spool-dir"})

#: The only help flag the CLI has (`-h` is not registered: click refuses it).
HELP_FLAG = "--help"

#: What the guard hook lets through as asking for help: `--help`, and `-h`, which
#: click refuses as an unknown option before the command runs (D102). The CLI's
#: own write gate reads only `--help`, so it still gates a `-h` run.
HELP_FLAGS = frozenset({HELP_FLAG, "-h"})

#: Commands that hand an unknown option on (`ignore_unknown_options`): there `-h`
#: is an argument and the command runs (`probe daemon worker -h`), so it is no help.
#: `test_daemon_profile.py` holds this to the CLI's tree.
UNKNOWN_OPTIONS_PASSED = frozenset(
    {"exec", "docs", "cli search", "daemon worker", "daemon override", "daemon session", "daemon task", "run resume"}
)


def is_help_flag(word: str, args: "list[str]") -> bool:
    """Is `word`, one of these args (after `probe`), a help flag the command
    reads as one (`HELP_FLAGS`)? `-h` is not where the command passes it on."""
    if word == HELP_FLAG:
        return True
    if word not in HELP_FLAGS:
        return False
    words = command_words(args)
    return not {" ".join(words[:2]), " ".join(words[:1])} & UNKNOWN_OPTIONS_PASSED

#: Groups whose whole job is READING research content. Refused only under `off`.
#: `docs` reads Probe's own docs, not the team's record: a read so that `off`
#: refuses it as it refuses `paper find`.
READ_GROUPS = frozenset(
    {"metrics", "series", "get", "bundle", "events", "coordinates", "shared", "provenance", "docs", "samples", "watch"}
)

#: Commands inside a `READ_GROUPS` group that record rather than print:
#: `metrics backfill` stores a derived curve, `shared add` uploads into the
#: team's Shared folder, `shared share|unshare` move a file into or out of it,
#: `samples export` writes a file and can register it as a dataset, `samples cancel|retry`
#: ask a running sample's producer to stop or rerun it, `samples proxy` records a run's samples.
#: Read as reads, `read` let them through.
READ_GROUP_WRITES = frozenset(
    {"metrics backfill", "shared add", "shared share", "shared unshare", "samples export", "samples cancel",
     "samples retry", "samples proxy"}
)

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
#: `pane push` saves a pane, a visual the coding agent writes over its runs' data
#: (`write-pane`): the agent's own work, which the daemon never writes (R10 of
#: run-compare-and-panes; daemon-written panes are a later step). `pane rm` removes
#: the agent's own pane beside it (agent-friendly R11): the daemon never writes one,
#: so a removal sent its way (the profile's refusal) had nowhere to go.
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
        # Control of a live run the agent launched (agentic W&B C.1): checkpoint, a setting, stop.
        "run send",
        # ...and of its RL samples (rl-next W34): stop or rerun one; the rollout proxy sidecar (W35) a
        # launch starts beside its harness.
        "samples cancel",
        "samples retry",
        # Relaunching a run from its checkpoint (agentic W&B C.2): a launch, like `exec`.
        "run resume",
        "samples proxy",
        "span add",
        "trial add",
        "trial stage",
        "trial export",
        "trial drain",
        "trial watch",
        "trial reconcile",
        "trial expand",
        # The live example's own writes (agent-prompt install D18): the example works under
        # the daemon, which files nothing of it; `example status` and `delete` are below.
        "example start",
        "example conclude",
        "pane push",
        "pane rm",
        # Presentation only: how a chart draws, how a page lays out (team flag chart_layouts).
        "chart set",
        "chart layout",
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
    if command in WRITES_ALSO and _names_flag(args, WRITES_ALSO[command][0]):
        return ("write", "probe " + WRITES_ALSO[command][1])
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


def _names_flag(args: "list[str]", flag: str) -> bool:
    """Does one of these args name `flag` (`--flag=value` too)?"""
    return any(arg.split("=", 1)[0] == flag for arg in args)


def daemon_allows_agent(matched: str) -> bool:
    """Does the `daemon` state leave this write to the agent? (`matched` from
    `classify_probe_args`.)"""
    key = matched[len("probe "):] if matched.startswith("probe ") else matched
    return key in DAEMON_AGENT_WRITES


#: THE DAEMON PROFILE (daemon reads): the machine installed the lean
#: `probe-research-daemon` plugin, so the daemon records AND reads, and the main
#: agent's `probe` is `ask`, `exec`, its runs' own data and its panes
#: (`DAEMON_AGENT_WRITES`), reads of one run (`DAEMON_PROFILE_RUN_READS`) or of
#: one scope's panes (`DAEMON_PROFILE_PANE_READS`), `session status` and Probe's
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
#: waits on alive), `whoami` and `context list` (which team the runs land in).
#: And this machine's delivery (`service check-now`, `outbox drain|retry|watch`,
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
#: Probe's own upkeep the person asks for (install, update, uninstall, imports,
#: the example, W&B, the new-chat default, the service) is `PROBE_UPKEEP`, read
#: with its flags, not here by name (fixes-1107b T2).
#: `pin add|list|rm` pin a view the researcher asked for, read the pins and unpin
#: (pinned views D11, D12): the daemon's writer never pins, so they are the agent's;
#: the CLI's gate still asks `pin add` and `pin rm` for `--directed` (DIRECTED_ONLY).
DAEMON_PROFILE_ALLOWED = frozenset(
    {"ask", "session status", "session send", "run expect", "paper find",
     "docs", "cli search", "feedback send", "approvals", "outbox status", "run check", "sync", "artifact download",
     "daemon status", "context list", "flush", "service check-now",
     "token list", "context show", "outbox drain", "outbox retry", "outbox watch", "statusline status",
     "statusline show", "mcp status", "workspace list", "workspace get", "workspace writers show",
     "access-group list", "notes sync", "agent-rules refresh", "draft edit",
     "file preview", "feedback flush", "capy sync", "capy disconnect", "session owed", "session home show",
     "pin add", "pin list", "pin rm"}
)

#: Reads of ONE run, named by its id: the agent looks at the runs it launched
#: (is the loss falling, did the checkpoint land) without waiting on `probe ask`
#: (Richard 2026-10-21: the agent should see its own runs). Any run id passes --
#: the hook cannot tell this session's runs from a teammate's, and the ids an
#: agent holds are the ones `probe exec` printed or the daemon handed it.
#: Listings and searches across the team's work (`run list`, `series latest`,
#: `artifact list`, `provenance`, `commits`) stay the daemon's, through `probe ask`.
#: An RL run's samples and best checkpoint are its own (`instrument-code` checks the
#: capture of a run before its long launch); `samples export` writes, so it stays out.
DAEMON_PROFILE_RUN_READS = frozenset(
    {"run get", "run series", "run metrics", "run inputs", "run upstream", "run reproduce", "run edits",
     "run commands", "run logs", "get",
     "bundle", "events", "metrics wide", "metrics plot", "metrics export", "metrics grouped",
     "span list", "span get", "trial list", "trial get", "artifact tree", "artifact versions",
     "snapshot-show", "samples capture", "samples stats", "samples list", "samples show", "samples logs",
     "samples tokens", "samples tasks", "samples task", "samples weights", "samples compare", "checkpoint best",
     "samples live", "samples tail", "samples commands"}
)

#: Reads of the panes the agent writes (`write-pane`), in the one project or
#: experiment the agent names: what a recipe resolves to over that scope's runs,
#: checked before a push (`pane data`), and a pane read back (`pane get`, `pane
#: list`). A pane cannot be written without them (R10), so they are admitted
#: though `pane data` reads a scope's runs as the pane will; searches and
#: listings across the team's work stay the daemon's.
DAEMON_PROFILE_PANE_READS = frozenset({"pane data", "pane get", "pane list"})

#: ...but not where a flag writes what it read: `run reproduce --materialize`
#: restores the run's captured tree, as the kept `snapshot-restore` does, and
#: `--export` writes a file, as `run logs --output` does. A word the shell still
#: expands may be either. `pane get --out` is admitted (agent-friendly B3): it writes
#: the agent's own pane as the two files `pane push` takes, as `| jq -r .html > f` would.
DAEMON_PROFILE_READ_WRITES = {
    "run reproduce": frozenset({"--materialize", "--export"}),
    "run logs": frozenset({"--output"}),
}

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

#: The researcher's switch for this chat, typed into a shell. The agent moves it
#: only when the person asked, with `--directed`, and only by `session state
#: <target>` (fixes-1107b T3): `toggle`, `track` and `untrack` flip it, so a
#: retried one undoes itself, and an agent never runs them. The researcher's own
#: `/probe` reaches the hooks, not a shell. `session default` is not on it
#: (D102): it sets what NEW chats start as (`read|off` need `--directed`, UC2).
RESEARCHER_SWITCH = frozenset(
    {"session state", "session toggle", "session track", "session untrack"}
)

#: The one switch command an agent may run, with `--directed` (T3): it sets, never flips.
SWITCH_SET = "session state"

#: How an agent spells this chat's switch and the new-chat default (the npx
#: spelling: the launcher's floor picks a CLI that strips `--directed`).
SWITCH_COMMAND = "npx -y probe-research session state <on|read|off|inline> --directed"

#: Where the default for new chats is set, said in each switch refusal: `/probe` reaches only this chat.
SWITCH_DEFAULT_HINT = (
    "`/probe` moves only this chat; `npx -y probe-research session default on|read|off` sets what new chats "
    "start as (`read` and `off` with `--directed`, once the person said yes)."
)

#: What the guard and the CLI answer an agent that moves this chat's switch
#: without `--directed` (T3).
INLINE_SWITCH_DENY = (
    "`{matched}` moves the researcher's Probe switch, so it was refused before it ran. Move it only when the "
    "person asked for exactly this: then run `" + SWITCH_COMMAND + "`. Never move it on your own; the person "
    "can also type `/probe on`, `/probe read`, `/probe off` or `/probe inline`. "
    + SWITCH_DEFAULT_HINT
)

#: What the guard answers an agent the daemon records for that moves the switch
#: without `--directed`. Kimi runs a typed `/probe on` through a hook whose output
#: never reaches the model, so the agent reads the skill, goes looking for the
#: command itself, and lands here: the answer is that a typed move already
#: happened, never `DAEMON_PROFILE_DENY`'s pointer to `/probe inline`.
RESEARCHER_SWITCH_DENY = (
    "`{matched}` moves the researcher's Probe switch, so it was refused before it ran: a `/probe` they typed "
    "has already moved it, and `probe session status` prints where it landed. If they asked you to move it, "
    "run `" + SWITCH_COMMAND + "`; never move it on your own. "
    + SWITCH_DEFAULT_HINT
)

#: The agent's own Skill-tool call of the switch (Claude Code's `Skill`, the older `SlashCommand`) that
#: would lower this chat's recording or flip it (T3): the person's typed `/probe` is a prompt, never a
#: tool call, so this one is the model's. `{matched}` the call, `{target}` the state it asked for.
SKILL_SWITCH_DENY = (
    "`{matched}` is your own call of the Probe switch, and it would make this chat record less (or flip it), "
    "so it was refused before it ran: only the person moves it that way. Ask the person first; if they say "
    "yes, run `npx -y probe-research session state {target} --directed`. "
    + SWITCH_DEFAULT_HINT
)

#: The agent's own Skill-tool call of the switch in an auto chat (`is_auto_chat`): it moves the switch
#: through `session state`, which keeps the move the agent's, so auto goes on.
AUTO_SKILL_SWITCH = (
    "`{matched}` was not run: Probe is in auto mode, so set this chat's state with "
    "`probe session state <on|read|off|inline>`."
)

#: `toggle`, `track` and `untrack` from an agent, `--directed` or not (T3).
SWITCH_FLIP_DENY = (
    "`{matched}` flips this chat's Probe switch, so a retry would undo itself: it was refused before it ran. "
    "When the person asks, set it with `" + SWITCH_COMMAND + "`. "
    + SWITCH_DEFAULT_HINT
)

_DAEMON_PROFILE_DENY_HEAD = (
    'The Probe daemon records this session and reads the team\'s work for you, so `{matched}` was refused before it ran. You instrument your runs with the SDK and can read one by its id (`probe run get <id>`). To ask about the team\'s prior work: `probe ask "<question>"`. '
)
DAEMON_PROFILE_DENY = _DAEMON_PROFILE_DENY_HEAD + "If you need to do it yourself, ask the researcher to type `/probe inline`."
#: ...and in an auto chat (`is_auto_chat`), where the agent takes Probe inline itself (probe auto mode).
DAEMON_PROFILE_DENY_AUTO = _DAEMON_PROFILE_DENY_HEAD + "If you need to do it yourself, run `probe session state inline`."

#: `DAEMON_PROFILE_DENY` for a WRITE: `--directed` admits one the researcher
#: asked for, and the daemon's writer takes any other (`probe ask --writer`). A
#: read keeps the plain text: no flag admits it, `probe ask` reads.
DAEMON_PROFILE_DENY_WRITE = DAEMON_PROFILE_DENY + "\n\n" + DIRECTED_RETRY + " " + WRITER_RETRY
DAEMON_PROFILE_DENY_WRITE_AUTO = DAEMON_PROFILE_DENY_AUTO + "\n\n" + DIRECTED_RETRY + " " + WRITER_RETRY


def get_daemon_profile_deny(session_id: "str | None", is_write: bool = False) -> str:
    """The daemon profile's refusal (unformatted): the auto mode one in an auto chat."""
    if session_id and is_auto_chat(session_id):
        return DAEMON_PROFILE_DENY_WRITE_AUTO if is_write else DAEMON_PROFILE_DENY_AUTO
    return DAEMON_PROFILE_DENY_WRITE if is_write else DAEMON_PROFILE_DENY

#: What the papers hook answers a paper-type web search it holds (`papers_hook.py`):
#: at most once per `PAPER_FIND_WINDOW_S`, and never after `probe paper find` ran
#: inside it. Richard approved the wording 2026-10-12.
PAPER_SEARCH_HOLD = (
    "Probe searches research papers, so this web search was held. Run "
    '`probe paper find "<the question as a sentence>"` first. After that, web searches run '
    f"normally for {PAPER_FIND_WINDOW_S // 60} minutes."
)


def moves_switch(args: "list[str]") -> "str | None":
    """`probe <words>` when these args (after `probe`) move the researcher's
    switch (`RESEARCHER_SWITCH`), else None."""
    two = " ".join(command_words(args)[:2])
    return "probe " + two if two in RESEARCHER_SWITCH else None


def daemon_profile_allows(args: "list[str]", session_id: "str | None" = None) -> "tuple[bool, str]":
    """`(allowed, matched)` for the args after `probe` in the daemon profile.

    A write carrying `--directed` is allowed, as the CLI's gate allows it in the
    `daemon` state (`write_gate.refusal`). A read is not (reads go through
    `probe ask`) but one run's (`DAEMON_PROFILE_RUN_READS`) and one scope's
    panes (`DAEMON_PROFILE_PANE_READS`). The researcher's
    switch runs only as `session state <target> --directed` (`switch_refusal`).
    Probe's own upkeep runs with its own flags (`upkeep_command`), and what
    records less only with `--directed` (`records_less`); the agent's own
    commands are `DAEMON_PROFILE_ALLOWED`. Anything else -- a word the guard
    cannot read included -- is refused.
    """
    words = command_words(args)
    if not words:
        return (True, "probe")
    head = words[0]
    two = " ".join(words[:2])
    if two in RESEARCHER_SWITCH:
        return (switch_refusal(args, session_id=session_id) is None, "probe " + two)
    upkeep = upkeep_command(args)
    if upkeep is not None:
        return (needs_directed(args) is None, "probe " + upkeep)
    if head in DAEMON_PROFILE_PLAIN_FLAGS:
        return (_runs_plainly(args, head), "probe " + head)
    for key in (" ".join(words[:3]), two, head):
        if key in DAEMON_PROFILE_ALLOWED:
            return (True, "probe " + key)
        if key in DAEMON_PROFILE_RUN_READS or key in DAEMON_PROFILE_PANE_READS:
            return (not _flag_writes(args, DAEMON_PROFILE_READ_WRITES.get(key, frozenset())), "probe " + key)
    kind, matched = classify_probe_args(args)
    if kind == "write" and carries_directed(args):
        return (True, matched)
    if kind is None and two in DAEMON_AGENT_WRITES:
        return (True, "probe " + two)  # the removal of the agent's own (`pane rm`): cleanup, never classed a write
    if matched[len("probe "):] in DAEMON_PROFILE_ALLOWED:
        return (True, matched)  # `pane push --pin` is `pin add` (WRITES_ALSO): the CLI's gate asks
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


def daemon_profile_deny(args: "list[str]", matched: str, session_id: "str | None" = None) -> str:
    """The refusal for args `daemon_profile_allows` refused: the switch is told
    how the agent sets it (`switch_refusal`), upkeep that records less to ask
    first (`DIRECTED_REQUIRED_DENY`), upkeep with a flag it may not pass which
    one (`UPKEEP_FLAG_DENY`, never `/probe inline`), a write that `--directed`
    runs it (`DAEMON_PROFILE_DENY_WRITE`)."""
    switch = switch_refusal(args, RESEARCHER_SWITCH_DENY, session_id)
    if switch is not None:
        return switch
    key, offender = _check_upkeep(args)
    if key is not None and offender is None and needs_directed(args):
        return needs_directed(args)
    if key is not None and offender is not None:
        return UPKEEP_FLAG_DENY.format(matched="probe " + key, offender=offender)
    kind, _matched = classify_probe_args(args)
    return get_daemon_profile_deny(session_id, is_write=kind == "write").format(matched=matched)


# ---------------------------------------------------------------------------
# PROBE'S OWN UPKEEP, WHAT RECORDS LESS, AND THIS CHAT'S SWITCH (fixes-1107b
# T2, T3). Upkeep is Probe managing itself for the person who asked (install,
# settings, sign-in, update, uninstall, imports): it runs in every chat state,
# but only with the flags listed here. What records less runs from an agent
# only with `--directed`, after the person said yes (gate UC2).
# ---------------------------------------------------------------------------

#: Each upkeep command's flags: (the ones an agent may pass, the ones it may
#: not). Every option and argument `cli_spec.json` gives the command is in one
#: of the two (`test_daemon_profile.py` sorts them); `tools/vendor.py
#: sync-probe-upkeep` writes the allowed ones, with their value counts, into
#: `PROBE_UPKEEP` below and `npm/upkeep.json`. Refused for agents (the plan's
#: deny set): another server or a raw credential, capture or tracking off by
#: flag, another update channel or context, retired or unknown options.
#: `uninstall --discard-unsent|--force` stay: uninstall.md asks first, and an
#: uninstall needs `--directed` anyway.
UPKEEP_FLAG_RULES = {
    "install": ("--agent --tracking --capture --auto-update --agent-rules --yes -y --profile --json",
                "--no-tracking --no-capture --no-auto-update --no-agent-rules <auth_code>"),
    "wizard": ("--agent --tracking --capture --auto-update --agent-rules --action --yes -y --no-browser "
               "--who-records --reinstall --pending --recommended --session-default --session-control --attempt "
               "--profile --json",
               "--no-tracking --no-capture --no-auto-update --no-agent-rules --channel --uninstall --folder "
               "--experimental --token --base-url --context --ingest-token --hmac-secret --endpoint-only "
               "<auth_code>"),
    "login": ("--device", "--base-url --token --ingest-token --hmac-secret --endpoint-only --context"),
    "logout": ("", ""),
    "whoami": ("", ""),
    "doctor": ("--fix --send --bundle --out --json", ""),
    "repair": ("--json", ""),
    "update": ("--check --yes -y --plugin", "--no-plugin --channel"),
    "status": ("--json --refresh --timeout --repaste-choice --past-work-choice --demo-choice", ""),
    "uninstall": ("--yes -y --json --backup-unsent --discard-unsent --force", "--offline"),
    "import review": ("--sessions --folder --workspace --agent --wandb-project --wandb-folder --wandb-key "
                      "--skip-files-over --json --chats-agent --chats-since --chats-folder --chats-limit --chats-all",
                      ""),
    "import folders": ("--json", ""),
    "import status": ("--review --wait --json", ""),
    "import cancel": ("<job_id> --json", ""),
    "example status": ("--json", ""),
    "example keep": ("--json", ""),
    "example delete": ("--json", ""),
    "wandb login": ("", ""),
    "wandb discover": ("<root>", ""),
    "wandb key set": ("--key", ""),
    "wandb key status": ("", ""),
    "wandb key request": ("--json", ""),
    "wandb key receive": ("--request --wait --json", ""),
    "session default": ("<value>", "--folder"),
    "session control": ("<value>", ""),
    "service start": ("--min-version --json", ""),
    "service stop": ("--json", ""),
    "service status": ("--json", ""),
    "capture on": ("--agent --yes -y --json --no-browser", ""),
    "capture off": ("--agent --yes -y --json", ""),
}
#: Commands that are another's old name, with its flags: `setup` is the wizard's.
UPKEEP_ALIASES = {"setup": "wizard"}

#: The wizard actions that are upkeep (`--action`; the launcher maps `install`,
#: `update` and `sign-in --wait` onto configure, update and login --pending;
#: root `install`, `update`, `login`, `logout`, `uninstall` and `doctor` are the
#: same upkeep). `import-research` (a picker no agent can drive) is not.
UPKEEP_WIZARD_ACTIONS = ("configure", "diagnose", "login", "logout", "recorder", "uninstall", "update")

#: Where `PROBE_UPKEEP` keeps how many positional arguments a command takes.
UPKEEP_ARGUMENTS = "<arguments>"

#: The plan's deny set: never an allowed upkeep flag (a test holds it).
AGENT_DENIED_FLAGS = frozenset(
    {"--no-capture", "--no-tracking", "--channel", "--context", "--uninstall", "--token", "--ingest-token",
     "--hmac-secret", "--endpoint-only", "--base-url"}
)

# BEGIN PROBE_UPKEEP (generated by `make sync-probe-upkeep` from cli_spec.json; edit UPKEEP_FLAG_RULES)
PROBE_UPKEEP = {
    "capture off": {"--agent": 1, "--json": 0, "--yes": 0, "-y": 0},
    "capture on": {"--agent": 1, "--json": 0, "--no-browser": 0, "--yes": 0, "-y": 0},
    "doctor": {"--bundle": 0, "--fix": 0, "--json": 0, "--out": 1, "--send": 0},
    "example delete": {"--json": 0},
    "example keep": {"--json": 0},
    "example status": {"--json": 0},
    "import cancel": {"--json": 0, "<arguments>": 1},
    "import folders": {"--json": 0},
    "import review": {"--agent": 1, "--chats-agent": 1, "--chats-all": 0, "--chats-folder": 1, "--chats-limit": 1, "--chats-since": 1, "--folder": 1, "--json": 0, "--sessions": 1, "--skip-files-over": 1, "--wandb-folder": 1, "--wandb-key": 1, "--wandb-project": 1, "--workspace": 1},
    "import status": {"--json": 0, "--review": 1, "--wait": 0},
    "install": {"--agent": 1, "--agent-rules": 0, "--auto-update": 0, "--capture": 0, "--json": 0, "--profile": 1, "--tracking": 0, "--yes": 0, "-y": 0},
    "login": {"--device": 0},
    "logout": {},
    "repair": {"--json": 0},
    "service start": {"--json": 0, "--min-version": 1},
    "service status": {"--json": 0},
    "service stop": {"--json": 0},
    "session control": {"<arguments>": 1},
    "session default": {"<arguments>": 1},
    "setup": {"--action": 1, "--agent": 1, "--agent-rules": 0, "--attempt": 1, "--auto-update": 0, "--capture": 0, "--json": 0, "--no-browser": 0, "--pending": 0, "--profile": 1, "--recommended": 0, "--reinstall": 0, "--session-control": 1, "--session-default": 1, "--tracking": 0, "--who-records": 1, "--yes": 0, "-y": 0},
    "status": {"--demo-choice": 1, "--json": 0, "--past-work-choice": 1, "--refresh": 0, "--repaste-choice": 1, "--timeout": 1},
    "uninstall": {"--backup-unsent": 0, "--discard-unsent": 0, "--force": 0, "--json": 0, "--yes": 0, "-y": 0},
    "update": {"--check": 0, "--plugin": 0, "--yes": 0, "-y": 0},
    "wandb discover": {"<arguments>": 1},
    "wandb key receive": {"--json": 0, "--request": 1, "--wait": 0},
    "wandb key request": {"--json": 0},
    "wandb key set": {"--key": 1},
    "wandb key status": {},
    "wandb login": {},
    "whoami": {},
    "wizard": {"--action": 1, "--agent": 1, "--agent-rules": 0, "--attempt": 1, "--auto-update": 0, "--capture": 0, "--json": 0, "--no-browser": 0, "--pending": 0, "--profile": 1, "--recommended": 0, "--reinstall": 0, "--session-control": 1, "--session-default": 1, "--tracking": 0, "--who-records": 1, "--yes": 0, "-y": 0},
}
# END PROBE_UPKEEP

#: What records less, run from an agent (gate UC2): the commands, the wizard
#: actions, the flags whatever their value, and the flags with the values that
#: lower it. Raising (`session default on`, `--profile full`) is not on it.
RECORDS_LESS_COMMANDS = frozenset({"uninstall", "logout", "service stop", "capture off"})
RECORDS_LESS_WIZARD_ACTIONS = frozenset({"logout", "uninstall"})
RECORDS_LESS_FLAGS = frozenset({"--who-records", "--no-capture", "--no-tracking", "--uninstall"})
#: `--profile runs` (Runs only); `--session-default` and `session default` lower at `read` or `off`.
RECORDS_LESS_PROFILE = "runs"
#: The commands those flags are read on.
RECORDS_LESS_FLAG_HEADS = frozenset({"install", "wizard", "setup"})
#: The install's Recommended: it picks auto mode (`grants_auto`).
RECOMMENDED_FLAG = "--recommended"

#: Writes `--directed` admits in every chat state, `read` and `off` included
#: (D51 as amended by T2): bringing in past work the person consented to.
DIRECTED_IN_EVERY_STATE = frozenset({"import start", "import resume"})

#: Gate UC2's refusal (`directed_required`): the agent asks, and adds the flag only on a yes.
DIRECTED_REQUIRED_DENY = (
    "`{matched}` makes Probe record less, so it was refused before it ran: from an agent it runs only with "
    "`--directed`. Ask the person first, saying what stops; add `--directed` only if they say yes, never on "
    "your own."
)


#: Turning auto mode on from an agent without `--directed` (`grants_auto`).
AUTO_CONTROL_DENY = (
    "`{matched}` lets the agent set every chat's Probe switch, so it was refused before it ran: from an agent "
    "it runs only with `--directed`. Ask the person first; add `--directed` only if they asked for auto mode."
)


#: Upkeep with a word an agent may not pass (`upkeep_offender`), in every profile: never `/probe inline`.
UPKEEP_FLAG_DENY = (
    "`{matched}` is Probe's own upkeep, but `{offender}` keeps it from running from an agent, so it was "
    "refused before it ran. Run it with its usual flags only (`{matched} --help` lists them). Another server, "
    "a raw credential, or capture or tracking off by flag never comes from a chat: tell the person, and do "
    "not run it another way."
)


def _upkeep_key(words: "list[str]") -> "str | None":
    """The `PROBE_UPKEEP` key these command words (`command_words`) start with, longest first."""
    for size in (3, 2, 1):
        key = " ".join(words[:size])
        if len(words) >= size and key in PROBE_UPKEEP:
            return key
    return None


def get_wizard_actions(args: "list[str]") -> "list[str]":
    """Every `--action` value in these args (`--action x`, `--action=x`)."""
    actions = []
    for i, arg in enumerate(args):
        name, eq, value = arg.partition("=")
        if name == "--action":
            actions.append(value if eq else (args[i + 1] if i + 1 < len(args) else ""))
    return actions


def upkeep_command(args: "list[str]") -> "str | None":
    """The `PROBE_UPKEEP` command these args (after `probe`) run, or None.

    Only plainly: the command's words first (after any `--directed`), then
    nothing but its own flags (with their values) and arguments; the wizard
    only for an upkeep action, every `--action` one (click runs the last).
    A root option, a `--`, a word the shell still expands or any other flag
    makes it no upkeep, so it is judged as before (`upkeep_offender` names it).
    """
    key, offender = _check_upkeep(args)
    return key if offender is None else None


def upkeep_offender(args: "list[str]") -> "str | None":
    """For args naming an upkeep command that `upkeep_command` still refuses,
    the word that made it no upkeep (`--token`, `--action recorder`); else None."""
    return _check_upkeep(args)[1]


def _check_upkeep(args: "list[str]") -> "tuple[str | None, str | None]":
    """`(key, offender)`: the upkeep command these args name (None: none) and
    the first word that keeps it from running as upkeep (None: it runs)."""
    own = [arg for arg in args if arg != DIRECTED_FLAG]
    key = _upkeep_key(command_words(own)) if PROBE_UPKEEP else None
    if key is None:
        return (None, None)
    for arg in own:
        if arg == "--" or not _SHELL_EXPANSION_CHARS.isdisjoint(arg):
            return (key, arg)
    if own[: len(key.split())] != key.split():
        return (key, own[0])  # a root option before it (`--base-url`), or one between its words
    if key in ("wizard", "setup"):
        actions = get_wizard_actions(own)
        if not actions:
            return (key, "no --action")
        for action in actions:
            if action not in UPKEEP_WIZARD_ACTIONS:
                return (key, ("--action " + action).strip())
    flags = PROBE_UPKEEP[key]
    arguments = 0
    rest = own[len(key.split()):]
    i = 0
    while i < len(rest):
        name, eq, _value = rest[i].partition("=")
        if not name.startswith("-"):
            arguments += 1
            if arguments > flags.get(UPKEEP_ARGUMENTS, 0):
                return (key, rest[i])
        elif name not in flags or (eq and not flags[name]):
            return (key, name)
        elif not eq:
            if i + flags[name] >= len(rest):
                return (key, name)  # a value it takes is missing
            i += flags[name]
        i += 1
    return (key, None)


def _flag_values(args: "list[str]", flag: str) -> "list[str]":
    """Every value given to `flag` (`--flag v`, `--flag=v`)."""
    values = []
    for i, arg in enumerate(args):
        name, eq, value = arg.partition("=")
        if name == flag:
            values.append(value if eq else (args[i + 1] if i + 1 < len(args) else ""))
    return values


def records_less(args: "list[str]") -> "str | None":
    """What these args (after `probe`) run that makes Probe record less
    (`RECORDS_LESS_*`), spelled for a refusal (`probe wizard --action logout`,
    `probe install --profile runs`), else None. A word the shell still expands
    on one of those commands may be any of them, so it counts."""
    words = command_words(args)
    if not words:
        return None
    head, two = words[0], " ".join(words[:2])
    for key in (two, head):
        if key in RECORDS_LESS_COMMANDS:
            return "probe " + key
    if two == "session default" and len(words) > 2:
        return "probe session default " + words[2] if _lowers_default(words[2]) else None
    if head not in RECORDS_LESS_FLAG_HEADS:
        return None
    matched = "probe " + head
    for action in get_wizard_actions(args) if head != "install" else ():
        if action in RECORDS_LESS_WIZARD_ACTIONS:
            return matched + " --action " + action
    if any(not _SHELL_EXPANSION_CHARS.isdisjoint(arg) for arg in args):
        return matched
    for arg in args:
        if arg.split("=", 1)[0] in RECORDS_LESS_FLAGS:
            return matched + " " + arg.split("=", 1)[0]
    if any(value.strip().lower() == RECORDS_LESS_PROFILE for value in _flag_values(args, "--profile")):
        return matched + " --profile " + RECORDS_LESS_PROFILE
    for value in _flag_values(args, "--session-default"):
        if _lowers_default(value):
            return matched + " --session-default " + value
    return None


def grants_auto(args: "list[str]") -> "str | None":
    """What these args (after `probe`) run that turns auto mode on (`session control auto`, `--session-control
    auto`, or `--recommended` naming no `--session-control`: Recommended picks auto since 2026-11-09), spelled for
    a refusal, else None. It hands every chat's switch to the agent, so from an agent it runs only with
    `--directed`, after the person asked (`AUTO_CONTROL_DENY`). A word the shell still expands there may be
    `auto`, so it counts."""
    words = command_words(args)
    if " ".join(words[:2]) == "session control" and len(words) > 2:
        value = words[2]
        if value.strip().lower() == CONTROL_AUTO or not _SHELL_EXPANSION_CHARS.isdisjoint(value):
            return "probe session control " + value
        return None
    if not words or words[0] not in RECORDS_LESS_FLAG_HEADS:
        return None
    controls = _flag_values(args, "--session-control")
    for value in controls:
        if value.strip().lower() == CONTROL_AUTO or not _SHELL_EXPANSION_CHARS.isdisjoint(value):
            return "probe " + words[0] + " --session-control " + value
    if not controls and RECOMMENDED_FLAG in args:
        return "probe " + words[0] + " " + RECOMMENDED_FLAG
    return None


def needs_directed(args: "list[str]") -> "str | None":
    """The refusal for upkeep that runs from an agent only with `--directed` (what records less, or turns
    auto mode on) and was run without it, else None."""
    if carries_directed(args):
        return None
    lowering = records_less(args)
    if lowering:
        return DIRECTED_REQUIRED_DENY.format(matched=lowering)
    granting = grants_auto(args)
    return AUTO_CONTROL_DENY.format(matched=granting) if granting else None


def _lowers_default(value: str) -> bool:
    """Does this new-chat default (`read`, `off`, a spelling of either) record less than `on`?"""
    return normalize_state(value) in (STATE_READ_ONLY, STATE_OFF)


def directed_in_every_state(args: "list[str]") -> bool:
    """Is this a write `--directed` admits in every state (`DIRECTED_IN_EVERY_STATE`), carrying it?"""
    return " ".join(command_words(args)[:2]) in DIRECTED_IN_EVERY_STATE and carries_directed(args)


def get_switch_target(args: "list[str]") -> "str | None":
    """The target `session state <target>` names (None: it only prints the state).
    `--session <id>` and `--directed` are not targets."""
    rest = [arg for arg in args if arg != DIRECTED_FLAG]
    words = command_words(rest)
    if " ".join(words[:2]) != SWITCH_SET:
        return None
    after = rest[rest.index(words[1]) + 1:]
    i = 0
    while i < len(after):
        if after[i] == "--session":
            i += 2
            continue
        if not after[i].startswith("-"):
            return after[i]
        i += 1
    return None


def get_switch_session(args: "list[str]") -> "str | None":
    """The session `--session <id>` names in a switch command, else None."""
    values = _flag_values(args, "--session")
    return values[-1] if values else None


def switch_refusal(args: "list[str]", deny: str = INLINE_SWITCH_DENY,
                   session_id: "str | None" = None) -> "str | None":
    """What an agent's move of this chat's switch is refused with, or None (T3).

    `session state <target> --directed` runs (the person asked); without the
    flag it is refused with `deny`, unless `session_id` is in auto
    (`is_auto_chat`: the agent sets it by the work); `session state` alone only
    prints it. `toggle`, `track` and `untrack` flip it, so they never run from an agent.
    """
    matched = moves_switch(args)
    if matched is None:
        return None
    if matched != "probe " + SWITCH_SET:
        return SWITCH_FLIP_DENY.format(matched=matched)
    if get_switch_target(args) is None or carries_directed(args):
        return None
    if session_id and is_auto_chat(session_id):
        return None
    return deny.format(matched=matched)


#: Commands that save a server or a credential (`server_override`, T2): `install`,
#: `login`, `repair`, `context use`, the wizard's configure and login (and its
#: menu), and any `--context`. Every other command keeps its `--base-url`, so
#: local and staging stacks keep working.
SERVER_SAVING = frozenset({"install", "login", "repair", "context use"})
SERVER_SAVING_ACTIONS = frozenset({"configure", "login"})
#: Flags that hand Probe a raw credential.
CREDENTIAL_FLAGS = frozenset({"--token", "--ingest-token", "--hmac-secret", "--endpoint-only"})
#: The variable the CLI and the launcher read the server from first.
BASE_URL_ENV = "PROBE_BASE_URL"
#: Probe's own server, where a saved sign-in names none (`settings.DEFAULT_BASE_URL`).
DEFAULT_SERVER = "https://api.research.prbe.ai"
#: `PROBE_BASE_URL=<value>` written before a command on its line.
_BASE_URL_ASSIGNMENT = re.compile(r"(?:^|[\s;&|(])" + BASE_URL_ENV + r"=(\"[^\"]*\"|'[^']*'|[^\s;&|)]*)")

SERVER_OVERRIDE_DENY = (
    "`{matched}` would point Probe on this computer {what}, so it was refused before it ran: from a chat, "
    "Probe keeps the server and account it is signed in to ({saved}). Tell the person what was refused and "
    "why; do not run it another way."
)


def saves_server(args: "list[str]") -> "str | None":
    """`probe <command>` when these args (after `probe`) save a server or a credential (`SERVER_SAVING`), else None."""
    words = command_words(args)
    if not words:
        return None
    for key in (" ".join(words[:2]), words[0]):
        if key in SERVER_SAVING:
            return "probe " + key
    own = args[: args.index("--")] if "--" in args else args
    if words[0] in ("wizard", "setup"):
        actions = get_wizard_actions(own)
        if not actions or SERVER_SAVING_ACTIONS & set(actions):
            return "probe " + words[0]
    if any(arg.split("=", 1)[0] == "--context" for arg in own):
        return "probe " + words[0]
    return None


def normalize_server(url: "str | None") -> str:
    """A server URL as two compare (`settings.normalize_endpoint`, restated: the hooks
    cannot import it): no trailing slash, scheme and host lower case, https's `:443` dropped."""
    from urllib.parse import urlsplit, urlunsplit

    text = (url or "").strip().rstrip("/")
    try:
        parts = urlsplit(text)
    except ValueError:
        return text
    if not parts.scheme or not parts.netloc:
        return text
    userinfo, at, hostport = parts.netloc.rpartition("@")
    hostport = hostport.lower()
    if parts.scheme.lower() == "https" and hostport.endswith(":443"):
        hostport = hostport[: -len(":443")]
    return urlunsplit((parts.scheme.lower(), userinfo + at + hostport, parts.path.rstrip("/"), parts.query,
                       parts.fragment))


def saved_server(config: "dict | None" = None) -> "str | None":
    """The server this computer is signed in to (the current account's, holding a
    key), normalized; None when no sign-in is saved. The key itself is never read out."""
    data = _read_config() if config is None else config
    contexts = data.get("contexts")
    row = contexts.get(data.get("current_context") or "default") if isinstance(contexts, dict) else data
    if not isinstance(row, dict) or not row.get("token"):
        return None
    url = row.get("base_url")
    return normalize_server(url if isinstance(url, str) and url.strip() else DEFAULT_SERVER)


def spelled_server_override(command: str, args: "list[str]") -> "str | None":
    """The hook's `server_override` for a line it can read (T2): a command that saves
    a server, run with `PROBE_BASE_URL=<another server>` written before it, on a
    computer signed in. The CLI's write gate checks the real environment."""
    matched = saves_server(args)
    if matched is None:
        return None
    values = [value.strip("\"'").strip() for value in _BASE_URL_ASSIGNMENT.findall(command)]
    values = [value for value in values if value]  # an empty one is no server (the CLI reads it as unset)
    saved = saved_server() if values else None
    for value in values:
        if saved is not None and normalize_server(value) != saved:
            return SERVER_OVERRIDE_DENY.format(
                matched=matched, what="at %s (`%s`)" % (show_server(value), BASE_URL_ENV), saved=show_server(saved))
    return None


def show_server(url: str) -> str:
    """A server URL as a refusal names it: without a `user:password@` part (never a secret)."""
    from urllib.parse import urlsplit, urlunsplit

    try:
        parts = urlsplit(url.strip())
    except ValueError:
        return "(a URL that does not parse)"
    if "@" not in parts.netloc:
        return url.strip()
    return urlunsplit((parts.scheme, parts.netloc.rpartition("@")[2], parts.path, "", ""))


def agent_refusal(args: "list[str]", deny: str = INLINE_SWITCH_DENY,
                  session_id: "str | None" = None) -> "str | None":
    """What every chat state refuses an agent before anything else (T2, T3): its
    move of this chat's switch (`switch_refusal`; `session_id` for auto), and what
    records less without `--directed` (`DIRECTED_REQUIRED_DENY`). None when neither applies."""
    switch = switch_refusal(args, deny, session_id)
    if switch is not None:
        return switch
    return needs_directed(args)


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

#: The two above in an auto chat (`is_auto_chat`), where the agent sets the state itself (probe auto mode).
DENY_REASON_AUTO_OFF = (
    "Probe is off for this chat (auto mode), so `{matched}` was refused before it ran. If this is ML work, "
    "run `probe session state on` (or `read` to only look something up) and retry; if not, leave Probe alone."
)
DENY_REASON_AUTO_READ = (
    "Probe is read-only for this chat (auto mode), so `{matched}` was refused before it ran. If this work "
    "should be recorded, run `probe session state on` and retry."
)


def get_deny_reason(state: "str | None", session_id: "str | None") -> str:
    """The off or read-only refusal (unformatted) for `state`: the auto mode one in an auto chat."""
    is_auto = bool(session_id) and is_auto_chat(session_id)
    if state == STATE_OFF:
        return DENY_REASON_AUTO_OFF if is_auto else DENY_REASON_OFF
    return DENY_REASON_AUTO_READ if is_auto else DENY_REASON


# ---------------------------------------------------------------------------
# AUTO MODE'S LINE ON EACH RESEARCHER PROMPT (probe auto mode): the main agent
# sets an auto chat's state by the work, so every prompt says where it stands.
# The hook (`tracking_guard`) adds it; pi hears it through the same route.
# ---------------------------------------------------------------------------

#: Words that mark a prompt as ML work (track-work's "What counts as ML work"), whole
#: words, any case. A hit only adds `AUTO_PROMPT_MENTION` while off or read and never
#: moves the switch, which is why a fixed list is fine here (Richard 2026-11-07).
ML_PROMPT_TERMS = (
    "train", "training", "fine-tune", "fine-tuning", "finetune", "rl", "reward", "eval", "evals",
    "evaluation", "benchmark", "sweep", "ablation", "hyperparameter", "hyperparameters", "dataset",
    "datasets", "checkpoint", "epoch", "epochs", "loss", "baseline", "arxiv", "paper", "papers",
    "reproduce", "lora", "gpu", "wandb", "prompt engineering", "inference", "model", "accuracy",
)
_ML_PROMPT_TERM = re.compile(
    r"\b(" + "|".join(r"\s+".join(re.escape(part) for part in term.split())
                      for term in sorted(ML_PROMPT_TERMS, key=len, reverse=True)) + r")\b",
    re.IGNORECASE,
)

#: What the agent hears about a spent daemon allowance, in every message that names it (`inline_notice`, the
#: switch's answer, the auto line). Here, ahead of the inline piece, so module constants can use it.
ALLOWANCE_SPENT = "The team's free daemon allowance is exhausted."
#: What a `probe ask` the daemon can no longer answer hears when its chat goes inline on a spent allowance.
ALLOWANCE_SPENT_ASK = "the free daemon allowance is exhausted; Probe is inline"
#: Where a spent allowance puts a daemon move (`get_budget_inline_state`): the switch's answer and the auto line.
ALLOWANCE_SPENT_INLINE = ALLOWANCE_SPENT + " Probe's `on` is inline here: you record, with Probe's skills."

#: The chat's first researcher prompt, at its seeded default (`{state}`).
AUTO_FIRST_PROMPT_LINE = (
    "Probe is {state} here (the researcher's default, auto mode). Set it first: ML work, data included, "
    "is `on`."
)
AUTO_OFF_LINE = "Probe is off here (auto mode). If this request is ML work, data included, run `probe session state on` first."
AUTO_READ_LINE = (
    "Probe is read here (auto mode). To record this request's ML work, data included, run `probe session state on` first."
)
#: On (the daemon's or the agent's) or inline (`{state}`).
AUTO_ON_LINE = "Probe is {state} here (auto mode). If the work has clearly left ML, run `probe session state off`."
#: Added while off or read when the prompt names an ML word (`{word}`, as the prompt spells it).
AUTO_PROMPT_MENTION = ' It mentions "{word}".'


def make_auto_prompt_line(state: str, is_first: bool, prompt: str, *, is_allowance_spent: bool = False) -> str:
    """The one line an auto chat's researcher prompt gets: where Probe stands (`state`: off, read,
    on or inline), and, while off or read, the first ML word the prompt names; `is_allowance_spent`
    (`get_budget_inline_state`) adds that its `on` is inline. Pure: the hook and the eval both call it."""
    off, read = STATE_LABELS[STATE_OFF], STATE_LABELS[STATE_READ_ONLY]
    if is_first:
        line = AUTO_FIRST_PROMPT_LINE.format(state=state)
    elif state == off:
        line = AUTO_OFF_LINE
    elif state == read:
        line = AUTO_READ_LINE
    else:
        line = AUTO_ON_LINE.format(state=state)
    found = _ML_PROMPT_TERM.search(prompt or "") if state in (off, read) else None
    if found:
        line += AUTO_PROMPT_MENTION.format(word=" ".join(found.group(0).split()))
    return line + " " + ALLOWANCE_SPENT_INLINE if is_allowance_spent else line


def get_auto_state_word(session_id: str, state: "str | None") -> str:
    """Stored `state` as `make_auto_prompt_line` names it: off, read, on (the daemon's or the
    agent's own recording), or inline (the agent took Probe over from the daemon, `is_inline`)."""
    if state is None or state == STATE_OFF:
        return STATE_LABELS[STATE_OFF]
    if state == STATE_READ_ONLY:
        return STATE_LABELS[STATE_READ_ONLY]
    if state == STATE_FULL and is_inline(session_id, state):
        return INLINE_WORD
    return STATE_LABELS[STATE_FULL]


DENY_REASON_DAEMON = (
    "The Probe daemon is recording this conversation (the `daemon` state), so `{matched}` was "
    "refused before it ran: that write is the daemon's (it files runs in an experiment and "
    "group, and renames or moves projects and runs). Yours are starting runs in a project "
    "(`probe project create <slug>` if none fits), the run's own data, the panes you write and "
    "`probe run end`; `probe session status` lists them.\n\n" + DIRECTED_RETRY
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
    "itself attaches), the panes you write (`write-pane`) and `probe run end` when a run "
    "finishes. The daemon's: everything else, "
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
    "`{tool}` would touch {path}, where Probe records which conversation this is and whether the "
    "researcher has it recording -- the files this guard reads to decide. Changing them yourself "
    "would turn the guard off, so a command naming that folder is refused before it runs, reads "
    "included. To read this chat's state, run `probe session status`. Only the researcher's "
    "`/probe` switch moves that state; do not write there, and do not route around this."
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




# ---------------------------------------------------------------------------
# REFUSALS OF PROBE'S OWN UPKEEP, SPOOLED FOR THE SERVICE (fixes-1107b PR C)
# ---------------------------------------------------------------------------
#
#     ~/.local/state/probe/refusals/<session>.<reason>.json   {"reason", "step", "source", "chat_agent", "at"}
#
# The CLI's write gate and the hooks' guard add one when they refuse an agent's
# upkeep or install command (no network: a hook must answer at once); the Probe
# service sends each as `agent_install.refused` and renames it `.sent`, so a
# chat counts each reason once. Words only, never a value from the command.
# Never under `$XDG_STATE_HOME`: the service starts without it (`paths.py`), so
# that is the one folder writer and reader agree on. A chat with telemetry off
# (`PROBE_TELEMETRY`, `analytics.core.telemetry_disabled`) keeps none.

REFUSALS_DIRNAME = "refusals"
#: Files kept at most (sent ones included); a fuller folder takes no more.
MAX_REFUSALS = 200
#: A sent one is kept this long (the once-per-chat rule), then dropped.
REFUSAL_KEEP_S = 7 * 86400
REFUSAL_SOURCES = ("cli", "hook")
REFUSAL_WORD = re.compile(r"^[a-z][a-z0-9_]{0,39}$")
#: `PROBE_TELEMETRY` values that turn Probe's product events off (`analytics.core.telemetry_disabled`'s).
TELEMETRY_OFF_WORDS = frozenset({"off", "0", "false", "no", "disabled"})
#: A refused command's `step`, by its first word (the launcher's steps, and these).
REFUSAL_STEPS = {
    "install": "install", "setup": "install", "wizard": "install", "login": "sign_in", "sign-in": "sign_in",
    "logout": "sign_out", "repair": "repair", "update": "update", "uninstall": "uninstall", "status": "status",
    "import": "import", "example": "example", "wandb": "wandb", "session": "session", "service": "service",
    "capture": "capture",
}
#: The wizard's, by its `--action`.
REFUSAL_ACTION_STEPS = {
    "configure": "install", "recorder": "install", "login": "sign_in", "logout": "sign_out",
    "uninstall": "uninstall", "update": "update", "diagnose": "repair",
}


def get_refusals_dir() -> Path:
    """The default state folder's, never `$XDG_STATE_HOME`'s (the service reads it without one)."""
    return _home() / ".local" / "state" / STATE_DIRNAME / REFUSALS_DIRNAME


def get_refusal_step(args: "list[str]") -> str:
    """The `step` of the refused `probe` args (after `probe`): `REFUSAL_STEPS`, else `other`."""
    words = command_words([arg for arg in args if arg != DIRECTED_FLAG])
    if not words:
        return "other"
    if words[0] in ("wizard", "setup"):
        actions = get_wizard_actions(args)
        return REFUSAL_ACTION_STEPS.get(actions[-1], "other") if actions else "install"
    return REFUSAL_STEPS.get(words[0], "other")


def is_upkeep_refusal(args: "list[str]") -> bool:
    """Is this refused `probe` command Probe's own upkeep or install (what the spool counts)?"""
    own = [arg for arg in args if arg != DIRECTED_FLAG]
    return (_upkeep_key(command_words(own)) is not None or records_less(own) is not None
            or grants_auto(own) is not None
            or moves_switch(own) is not None or saves_server(own) is not None)


def save_refusal(session_id: str, reason: str, step: str, source: str,
                  chat_agent: "str | None" = None) -> bool:
    """Keep one refusal for the service to send (once per chat and reason). True when written. Never raises."""
    if not valid_session_id(session_id) or source not in REFUSAL_SOURCES:
        return False
    if (os.environ.get("PROBE_TELEMETRY") or "").strip().lower() in TELEMETRY_OFF_WORDS:
        return False  # this chat opted out: nothing about it is kept for later sending
    if not REFUSAL_WORD.match(reason or "") or not REFUSAL_WORD.match(step or ""):
        return False
    agent = chat_agent if isinstance(chat_agent, str) and REFUSAL_WORD.match(chat_agent) else None
    folder = get_refusals_dir()
    name = "%s.%s" % (session_id, reason)
    try:
        folder.mkdir(mode=0o700, parents=True, exist_ok=True)
        present = os.listdir(folder)
        if name + ".json" in present or name + ".sent" in present or len(present) >= MAX_REFUSALS:
            return False
        handle = os.open(str(folder / (name + ".json")), os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except OSError:
        return False
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as stream:
            json.dump({"reason": reason, "step": step, "source": source, "chat_agent": agent,
                       "at": int(time.time())}, stream)
    except OSError:
        return False
    return True


def load_spooled_refusals(now: "float | None" = None) -> "list[tuple[Path, dict]]":
    """The refusals not sent yet, oldest first; any past REFUSAL_KEEP_S (sent or never allowed out) is
    dropped. Never raises."""
    at = time.time() if now is None else now
    found = []
    try:
        entries = list(os.scandir(get_refusals_dir()))
    except OSError:
        return []
    for entry in entries:
        path = Path(entry.path)
        try:
            if not entry.is_file(follow_symlinks=False):
                continue
            if at - entry.stat(follow_symlinks=False).st_mtime > REFUSAL_KEEP_S:
                path.unlink()
                continue
            if not entry.name.endswith(".json"):
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if isinstance(data, dict):
            found.append((path, data))
    return sorted(found, key=lambda item: item[1].get("at") if isinstance(item[1].get("at"), int) else 0)


def mark_refusal_sent(path: Path) -> None:
    """Sent: kept as `.sent` (the once-per-chat rule) until REFUSAL_KEEP_S. Never raises."""
    try:
        os.replace(path, path.with_suffix(".sent"))
    except OSError:
        pass
