# Python internals
import argparse
from typing import Any, Callable, Optional

# Other libraries
from dlt.common.configuration.plugins import SupportsCliCommand, TCliCommandCompose


def _apply_timestamps(args: argparse.Namespace) -> None:
    # Current package
    from dlt_runtime._runtime_command_views import set_show_exact_timestamps

    set_show_exact_timestamps(bool(getattr(args, "timestamps", False)))


def _dispatch(action: Callable[[], Any]) -> None:
    # Other libraries
    from dlt._workspace.cli import echo as fmt
    from dlt._workspace.cli.exceptions import CliCommandInnerException

    # Current package
    from dlt_runtime.exceptions import RuntimeNotAuthenticated

    try:
        action()
    except RuntimeNotAuthenticated as e:
        # Mid-command 401: token wiped by httpx auth_flow → next invocation
        # will re-trigger device flow via @requires_login(auto_login=True).
        raise CliCommandInnerException(
            cmd="dlthub",
            msg=str(e) or "Authentication required. Run 'dlthub login'.",
            inner_exc=e,
        ) from e
    except CliCommandInnerException:
        raise
    except Exception as e:
        raise CliCommandInnerException(cmd="dlthub", msg=str(e), inner_exc=e) from e
    finally:
        fmt.echo("")


def _add_timestamps_flag(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--timestamps",
        action="store_true",
        help=(
            "Show exact ISO timestamps and precise durations (e.g. 1.291 s)"
            " instead of humanized relative times."
        ),
    )


def _add_launch_flags(
    parser: argparse.ArgumentParser,
    *,
    follow_help: str,
    add_refresh: bool,
) -> None:
    """Shared flags for any command that ends in `_do_launch`: run, serve, pipeline run."""
    _add_timestamps_flag(parser)
    parser.add_argument(
        "-f",
        "--follow",
        action="store_true",
        help=follow_help,
    )
    if add_refresh:
        parser.add_argument(
            "--refresh",
            action="store_true",
            help=(
                "Re-run from scratch (full reload). Cascades to freshness-graph"
                " downstream jobs."
            ),
        )
    parser.add_argument(
        "--job-ref",
        type=str,
        default=None,
        metavar="REF",
        help=(
            "Pick this job from the matched candidate set when the selector"
            " matches multiple jobs. Errors if REF is not in the matched set."
        ),
    )


def _add_run_serve_args(
    parser: argparse.ArgumentParser,
    *,
    selector_help: str,
    follow_help: str,
    add_refresh: bool,
) -> None:
    """Args for `dlthub run` / `dlthub serve`: positional + --deployment + shared launch flags."""
    parser.add_argument(
        "selector_or_job_ref",
        nargs="?",
        default=None,
        help=selector_help,
    )
    parser.add_argument(
        "--deployment",
        type=str,
        default=None,
        help="Python file to use as manifest source (instead of __deployment__)",
    )
    _add_launch_flags(parser, follow_help=follow_help, add_refresh=add_refresh)


# ---------------------------------------------------------------------------
# Top-level commands
# ---------------------------------------------------------------------------


class LoginCommand(SupportsCliCommand):
    command = "login"
    help_string = "Log in to dltHub (identity only)"
    description = (
        "Log in to dltHub. Authenticates the current user; does not"
        " connect a workspace. Run `dlthub workspace connect` to bind this"
        " project to a remote workspace. Opens your browser to authenticate"
        " by default; use `--device` to force the device-code flow (e.g. on"
        " a remote session)."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        parser.add_argument(
            "--resume",
            type=str,
            default=None,
            metavar="DEVICE_CODE",
            help=(
                "Resume a previously started device flow login. The DEVICE_CODE"
                " is printed by `dlthub login` when no TTY is attached."
            ),
        )
        parser.add_argument(
            "--device",
            action="store_true",
            default=False,
            help=(
                "Force the device authorization flow instead of the default"
                " browser loopback login."
            ),
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _dispatch(
            lambda: cmd.login(
                minimal_logging=False, resume=args.resume, force_device=args.device
            )
        )


class LogoutCommand(SupportsCliCommand):
    command = "logout"
    help_string = "Log out from dltHub"
    description = "Log out from dltHub"
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _dispatch(cmd.logout)


class RunCommand(SupportsCliCommand):
    command = "run"
    help_string = "Deploy code/config and run a script (alias for `dlthub job run`)"
    description = (
        "Deploy current workspace and run a batch script remotely. Use -f/--follow"
        " to tail logs until completion. A plain `.py` script may also be passed:"
        " if it exposes no jobs it is deployed and executed remotely as a regular"
        " Python script. Alias for `dlthub job run`."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        _add_run_serve_args(
            parser,
            selector_help=(
                "Selector or job ref to pick a job from the manifest, or a .py file"
                " path to deploy and run as a regular script"
            ),
            follow_help="Follow status changes and stream logs until the run completes",
            add_refresh=True,
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _apply_timestamps(args)
        _dispatch(
            lambda: cmd.launch(
                selector_or_job_ref=args.selector_or_job_ref,
                deployment=getattr(args, "deployment", None),
                follow=bool(args.follow),
                refresh=bool(getattr(args, "refresh", False)),
                job_ref=getattr(args, "job_ref", None),
            )
        )


class ServeCommand(SupportsCliCommand):
    command = "serve"
    help_string = (
        "Deploy and serve an interactive notebook/app (alias for `dlthub job serve`)"
    )
    description = (
        "Deploy current workspace and run a notebook as a read-only web app."
        " A plain `.py` script (marimo notebook, Streamlit app, FastMCP server, etc.)"
        " may also be passed and will be deployed and served remotely as a regular"
        " script. Alias for `dlthub job serve`."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        _add_run_serve_args(
            parser,
            selector_help=(
                "Selector or job ref to pick an interactive app from the manifest,"
                " or a .py file path to deploy and serve as a regular script"
            ),
            follow_help="Stream logs until the app stops",
            add_refresh=False,
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _apply_timestamps(args)
        _dispatch(
            lambda: cmd.serve(
                selector_or_job_ref=args.selector_or_job_ref,
                deployment=getattr(args, "deployment", None),
                follow=bool(getattr(args, "follow", False)),
                job_ref=getattr(args, "job_ref", None),
            )
        )


class JobRunCommand(RunCommand):
    """`dlthub job run` — canonical form; `dlthub run` is the alias."""

    parent: Optional[str] = "job"
    help_string = "Deploy code/config and run a batch job"
    description = (
        "Deploy current workspace and run a batch script remotely."
        " Use -f/--follow to tail logs until completion."
        " A plain `.py` script may also be passed: if it exposes no jobs it is"
        " deployed and executed remotely as a regular Python script."
    )


class JobServeCommand(ServeCommand):
    """`dlthub job serve` — canonical form; `dlthub serve` is the alias."""

    parent: Optional[str] = "job"
    help_string = "Deploy and serve an interactive notebook/app"
    description = (
        "Deploy current workspace and run a notebook as a read-only web app."
        " A plain `.py` script (marimo notebook, Streamlit app, FastMCP server, etc.)"
        " may also be passed and will be deployed and served remotely as a regular"
        " script."
    )


class DeployCommand(SupportsCliCommand):
    command = "deploy"
    help_string = "Sync code/config and deploy jobs"
    description = (
        "Sync workspace files, generate job manifest from __deployment__.py, and"
        " reconcile jobs with the runtime. Use --dry-run to preview changes."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        _add_timestamps_flag(parser)
        self._add_args(parser)

    @staticmethod
    def _add_args(parser: argparse.ArgumentParser) -> None:
        # Args-only helper so this command can be mounted inline under
        # `WorkspaceCommand` (which already declares --timestamps) without
        # creating a duplicate flag.
        parser.add_argument(
            "--deployment",
            type=str,
            default=None,
            help="Python file to use as manifest source (instead of __deployment__)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without applying them",
        )
        parser.add_argument(
            "--show-manifest",
            action="store_true",
            help="Dump the expanded deployment manifest as YAML and exit",
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _apply_timestamps(args)
        _dispatch(
            lambda: cmd.deploy_manifest(
                deployment=getattr(args, "deployment", None),
                dry_run=bool(getattr(args, "dry_run", False)),
                show_manifest=bool(getattr(args, "show_manifest", False)),
            )
        )


class ShowCommand(SupportsCliCommand):
    command = "show"
    help_string = "Open the current workspace in the dltHub web app (alias for `dlthub workspace show`)"
    description = (
        "Open the workspace overview for the current remote workspace in the browser."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _dispatch(cmd.open_workspace)


class DashboardCommand(SupportsCliCommand):
    command = "dashboard"
    help_string = "Open the workspace dashboard in the dltHub web app (deploys a default one if missing)"
    description = "Open the dltHub dashboard for the current remote workspace, deploying a default dashboard if none exists."
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _dispatch(cmd.open_dashboard)


# ---------------------------------------------------------------------------
# Workspace command — single class with internal subparsers
# ---------------------------------------------------------------------------


class WorkspaceCommand(SupportsCliCommand):
    command = "workspace"
    compose: TCliCommandCompose = "additive"
    help_string = "Workspace operations: connect, list, info, show, deploy, deployment, configuration"
    description = (
        "Bind this project to a remote dltHub workspace and manage its"
        " deployments and configurations."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        _add_timestamps_flag(parser)
        sub = parser.add_subparsers(
            title="Available subcommands", dest="op1", required=False
        )

        sub.add_parser(
            "list",
            help="List all workspaces you have access to",
            description="List all workspaces you have access to",
        )

        connect_p = sub.add_parser(
            "connect",
            help="Connects local to a remote workspace by name or ID",
            description=(
                "Connects local and remote workspaces. Jobs, pipelines and code available "
                "locally can then be deployed, scheduled and run in remote workspace."
            ),
        )
        connect_p.add_argument(
            "workspace",
            type=str,
            nargs="?",
            default=None,
            help=(
                "Workspace name or ID to connect to. When omitted interactive "
                "picker will allow to select existing or create a new one. "
                "Required when using an API key."
            ),
        )
        connect_p.add_argument(
            "--create",
            dest="create",
            action="store_true",
            default=False,
            help=(""),
        )
        connect_p.add_argument(
            "--org-id",
            dest="org_id",
            type=str,
            default=None,
            help=(
                "Organization UUID to scope the connection to. Required in"
                " non-interactive mode when you belong to multiple"
                " organizations and local workspace has no organization pinned."
            ),
        )

        sub.add_parser(
            "info",
            help=(
                "Show overview of current dltHub workspace (workspace, job count,"
                " latest run, latest deployment, latest configuration)"
            ),
            description=(
                "Show workspace ID and summary of deployments, configurations and jobs."
            ),
        )

        # `show`, `dashboard` and `deploy` are mounted inline via shared
        # command instances so they behave identically to the top-level
        # aliases. The op1-walker in `execute` dispatches to them.
        self._show_cmd = ShowCommand()
        sub.add_parser(
            "show",
            help=ShowCommand.help_string,
            description=ShowCommand.description,
        )

        self._dashboard_cmd = DashboardCommand()
        sub.add_parser(
            "dashboard",
            help=DashboardCommand.help_string,
            description=DashboardCommand.description,
        )

        deploy_p = sub.add_parser(
            "deploy",
            help=DeployCommand.help_string,
            description=DeployCommand.description,
        )
        # Skip --timestamps here; the workspace parent declares it already.
        DeployCommand._add_args(deploy_p)
        self._deploy_cmd = DeployCommand()

        deployment_p = sub.add_parser(
            "deployment",
            help="Manipulate deployments in the workspace",
            description="Manipulate deployments in the workspace",
        )
        self._deployment_parser = deployment_p
        deployment_p.add_argument(
            "deployment_version_no",
            nargs="?",
            type=int,
            help="Deployment version number. Only used in the `info` subcommand",
        )
        dep_sub = deployment_p.add_subparsers(
            title="Available subcommands", dest="op2", required=False
        )
        dep_sub.add_parser(
            "list",
            help="List all deployments in workspace",
            description="List all deployments in workspace",
        )
        dep_sub.add_parser(
            "info",
            help="Get detailed information about a deployment",
            description="Get detailed information about a deployment",
        )
        dep_sync = dep_sub.add_parser(
            "sync",
            help="Create new deployment if local workspace content changed",
            description="Create new deployment if local workspace content changed",
        )
        dep_sync.add_argument(
            "--dry-run",
            action="store_true",
            help="Compare local files to latest deployment without uploading",
        )
        dep_sync.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Print per-file added/updated/deleted tree alongside the summary",
        )

        configuration_p = sub.add_parser(
            "configuration",
            help="Manipulate configurations in the workspace",
            description="Manipulate configurations in the workspace",
        )
        self._configuration_parser = configuration_p
        configuration_p.add_argument(
            "configuration_version_no",
            nargs="?",
            type=int,
            help="Configuration version number. Only used in the `info` subcommand",
        )
        cfg_sub = configuration_p.add_subparsers(
            title="Available subcommands", dest="op2", required=False
        )
        cfg_sub.add_parser(
            "list",
            help="List all configuration versions",
            description="List all configuration versions",
        )
        cfg_sub.add_parser(
            "info",
            help="Get detailed information about a configuration",
            description="Get detailed information about a configuration",
        )
        cfg_sync = cfg_sub.add_parser(
            "sync",
            help="Create new configuration if local config content changed",
            description="Create new configuration if local config content changed",
        )
        cfg_sync.add_argument(
            "--dry-run",
            action="store_true",
            help="Compare local config to latest configuration without uploading",
        )
        cfg_sync.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Print per-file added/updated/deleted tree alongside the summary",
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Other libraries
        from dlt._workspace.cli import echo as fmt

        # Current package
        import dlt_runtime._runtime_command as cmd

        _apply_timestamps(args)
        op1 = getattr(args, "op1", None)
        op2 = getattr(args, "op2", None)

        def action() -> None:
            if op1 is None:
                self.parser.print_help()
                return
            if op1 == "list":
                cmd.workspace_list()
            elif op1 == "connect":
                cmd.workspace_connect(
                    args.workspace, org_id=args.org_id, create=args.create
                )
            elif op1 == "info":
                cmd.runtime_info()
            elif op1 == "show":
                self._show_cmd.execute(args)
            elif op1 == "dashboard":
                self._dashboard_cmd.execute(args)
            elif op1 == "deploy":
                self._deploy_cmd.execute(args)
            elif op1 == "deployment":
                if op2 is None:
                    self._deployment_parser.print_help()
                    return
                if op2 == "list":
                    cmd.get_deployments()
                elif op2 == "info":
                    cmd.get_deployment_info(
                        deployment_version_no=(
                            int(args.deployment_version_no)
                            if args.deployment_version_no
                            else None
                        ),
                    )
                elif op2 == "sync":
                    cmd.sync_deployment(
                        level="full",
                        dry_run=bool(getattr(args, "dry_run", False)),
                        verbose=bool(getattr(args, "verbose", False)),
                    )
                else:
                    fmt.echo(f"Unknown deployment subcommand: {op2}")
                    self._deployment_parser.print_usage()
            elif op1 == "configuration":
                if op2 is None:
                    self._configuration_parser.print_help()
                    return
                if op2 == "list":
                    cmd.get_configurations()
                elif op2 == "info":
                    cmd.get_configuration_info(
                        configuration_version_no=(
                            int(args.configuration_version_no)
                            if args.configuration_version_no
                            else None
                        ),
                    )
                elif op2 == "sync":
                    cmd.sync_configuration(
                        level="full",
                        dry_run=bool(getattr(args, "dry_run", False)),
                        verbose=bool(getattr(args, "verbose", False)),
                    )
                else:
                    fmt.echo(f"Unknown configuration subcommand: {op2}")
                    self._configuration_parser.print_usage()
            else:
                fmt.echo(f"Unknown workspace subcommand: {op1}")
                self.parser.print_usage()

        _dispatch(action)


class VariableCommand(SupportsCliCommand):
    command = "variable"
    compose: TCliCommandCompose = "additive"
    help_string = "Workspace variable operations: list, set, delete"
    description = (
        "Manage workspace variables — plain or secret values injected into every"
        " run's environment. Scope them workspace-wide or to a single profile."
    )
    docs_url: Optional[str] = None

    @staticmethod
    def _add_scope_args(
        parser: argparse.ArgumentParser, *, required: bool = False
    ) -> None:
        # A write targets exactly one scope, so absence must not silently mean one.
        scope = parser.add_mutually_exclusive_group(required=required)
        scope.add_argument(
            "--profile",
            type=str,
            default=None,
            help="Target the scope of this profile",
        )
        scope.add_argument(
            "--workspace",
            dest="workspace_only",
            action="store_true",
            help="Target the workspace-wide scope",
        )

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        _add_timestamps_flag(parser)
        sub = parser.add_subparsers(
            title="Available subcommands", dest="op1", required=False
        )

        list_p = sub.add_parser(
            "list",
            help="List variables in every scope, or in one scope",
            description=(
                "List workspace variables. Without a scope selector every scope is"
                " listed, with the profile shown per row. Secret values are masked."
            ),
        )
        self._add_scope_args(list_p)

        set_p = sub.add_parser(
            "set",
            help="Create or update one variable",
            description=(
                "Create or update a variable. The value is read from stdin unless"
                " --value is given, so secrets need not appear in argv or shell"
                " history."
            ),
        )
        set_p.add_argument("name", type=str, help="Variable name")
        set_p.add_argument(
            "--value",
            type=str,
            default=None,
            help="Value to store. Omit to read it from stdin",
        )
        # Never defaulted: an omitted flag is invisible, so either mistake would be silent.
        kind = set_p.add_mutually_exclusive_group(required=True)
        kind.add_argument(
            "--plain",
            dest="secret",
            action="store_false",
            help="Store a readable value",
        )
        kind.add_argument(
            "--secret",
            dest="secret",
            action="store_true",
            help="Store a write-only value, never shown again",
        )
        self._add_scope_args(set_p, required=True)

        delete_p = sub.add_parser(
            "delete",
            help="Remove one variable",
            description="Remove a variable from the workspace or a profile scope.",
        )
        delete_p.add_argument("name", type=str, help="Variable name")
        delete_p.add_argument(
            "--allow-missing",
            action="store_true",
            help="Treat an absent variable as success instead of an error",
        )
        self._add_scope_args(delete_p, required=True)

    def execute(self, args: argparse.Namespace) -> None:
        # Other libraries
        from dlt._workspace.cli import echo as fmt

        # Current package
        import dlt_runtime._runtime_command as cmd

        _apply_timestamps(args)

        def action() -> None:
            op1 = getattr(args, "op1", None)
            if op1 is None:
                self.parser.print_help()
                return
            if op1 == "list":
                cmd.variable_list(
                    getattr(args, "profile", None),
                    bool(getattr(args, "workspace_only", False)),
                )
            elif op1 == "set":
                cmd.variable_set(
                    args.name,
                    bool(args.secret),
                    getattr(args, "value", None),
                    getattr(args, "profile", None),
                )
            elif op1 == "delete":
                cmd.variable_delete(
                    args.name,
                    getattr(args, "profile", None),
                    bool(getattr(args, "allow_missing", False)),
                )
            else:
                fmt.echo(f"Unknown variable subcommand: {op1}")
                self.parser.print_usage()

        _dispatch(action)


class JobCommand(SupportsCliCommand):
    command = "job"
    compose: TCliCommandCompose = "additive"
    help_string = (
        "Job operations: list, info, run, serve, trigger, publish, unpublish,"
        " pause, resume, logs, cancel, runs"
    )
    description = (
        "List and operate on jobs registered in the connected workspace, plus"
        " their runs."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        _add_timestamps_flag(parser)
        sub = parser.add_subparsers(
            title="Available subcommands", dest="op1", required=False
        )

        list_p = sub.add_parser(
            "list",
            help=("List jobs (filter with selectors: batch, schedule:*, tag:ops, ...)"),
            description=(
                "List jobs registered in the workspace. Pass selectors to filter:"
                " batch, interactive, schedule:*, tag:<name>, manual:*, etc."
            ),
        )
        list_p.add_argument(
            "selector_or_job_name",
            nargs="*",
            help="Selector(s) or job name(s) used to filter the listing",
        )
        list_p.add_argument(
            "--archived",
            action="store_true",
            help="Include archived jobs in the listing (hidden by default)",
        )

        info_p = sub.add_parser(
            "info",
            help="Show job info",
            description="Display detailed information about the job",
        )
        info_p.add_argument(
            "selector_or_job_name",
            nargs="?",
            help="Job name, script path, or selector identifying the job",
        )

        show_p = sub.add_parser(
            "show",
            help="Open the job page in the web GUI",
            description=(
                "Print the URL of the job page in the dltHub dashboard and"
                " open it in a browser when interactive."
            ),
        )
        show_p.add_argument(
            "selector_or_job_name",
            nargs="?",
            help="Job name, script path, or selector identifying the job",
        )

        trigger_p = sub.add_parser(
            "trigger",
            help="Trigger jobs matching selectors (does not sync or deploy)",
            description=(
                "Trigger runs for jobs matching the given selectors. Can select only jobs already deployed. Does not"
                " sync code or deploy jobs. Examples: 'tag:backfill',"
                " 'manual:jobs.etl.*', 'schedule:*'"
            ),
        )
        trigger_p.add_argument(
            "selectors",
            nargs="+",
            help=(
                "Trigger selectors (fnmatch patterns), e.g. 'tag:backfill',"
                " 'manual:jobs.etl.*'"
            ),
        )
        trigger_p.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview matched jobs without creating runs",
        )
        trigger_p.add_argument(
            "--profile",
            type=str,
            default=None,
            help="Profile override for all triggered runs",
        )
        trigger_p.add_argument(
            "--refresh",
            action="store_true",
            help=(
                "Force a refresh on every triggered job (jobs skipped by"
                " freshness are not refreshed)."
            ),
        )

        publish_p = sub.add_parser(
            "publish",
            help="Generate or revoke a public link for an interactive notebook/app",
            description=(
                "Generate a public link for a notebook/app, or revoke it with --cancel."
            ),
        )
        publish_p.add_argument("script_path", help="Local path to the notebook/app")
        publish_p.add_argument(
            "--cancel",
            action="store_true",
            help="Revoke the public link for the notebook/app",
        )

        unpublish_p = sub.add_parser(
            "unpublish",
            help="Revoke the public link for an interactive notebook/app",
            description="Revoke the public link for an interactive notebook/app.",
        )
        unpublish_p.add_argument("script_path", help="Local path to the notebook/app")

        pause_p = sub.add_parser(
            "pause",
            help="Pause the schedule of one or more jobs",
            description=(
                "Pause the schedule of every job matching the given names, refs or"
                " selectors (batch, schedule:*, tag:ops, ...). Only jobs with a schedule can be paused."
            ),
        )
        pause_p.add_argument(
            "selector_or_job_name",
            nargs="+",
            help="Job names, script paths, job refs, or selectors.",
        )

        resume_p = sub.add_parser(
            "resume",
            help="Resume the schedule of one or more jobs",
            description=(
                "Resume the schedule of every job matching the given names, refs or"
                " selectors (batch, schedule:*, tag:ops, ...). The first run covers"
                " the whole period the job was paused for."
            ),
        )
        resume_p.add_argument(
            "selector_or_job_name",
            nargs="+",
            help="Job names, script paths, job refs, or selectors.",
        )

        logs_p = sub.add_parser(
            "logs",
            help="Show logs for latest or selected job run",
            description=(
                "Show logs for the latest run of a job or a specific run number."
                " Use -f/--follow to stream logs in real-time."
            ),
        )
        logs_p.add_argument(
            "selector_or_job_name",
            help="Job name, script path, or selector (e.g. batch, schedule:*).",
        )
        logs_p.add_argument(
            "run_number", nargs="?", type=int, help="Run number (optional)"
        )
        logs_p.add_argument(
            "-f",
            "--follow",
            action="store_true",
            help="Follow logs in real-time until the run completes",
        )

        cancel_p = sub.add_parser(
            "cancel",
            help="Cancel active runs for matching jobs",
            description=(
                "Cancel active (non-terminal) runs for jobs matching selectors or"
                " names. Multiple values cancel active runs for all matching"
                " jobs. Use --dry-run to preview."
            ),
        )
        cancel_p.add_argument(
            "selector_or_job_name",
            nargs="+",
            help="Job name, script path, or selector (e.g. batch, schedule:*).",
        )
        cancel_p.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be cancelled without actually cancelling",
        )

        runs_p = sub.add_parser(
            "runs",
            help="Manage job runs: list, info, logs, cancel",
            description=(
                "Operate on runs of a job: list runs, show info, stream logs, cancel."
            ),
        )
        self._runs_parser = runs_p
        self._configure_runs(runs_p)

    @staticmethod
    def _configure_runs(runs_parser: argparse.ArgumentParser) -> None:
        runs_sub = runs_parser.add_subparsers(
            title="Available subcommands", dest="op2", required=False
        )

        runs_list_p = runs_sub.add_parser(
            "list",
            help="List job runs (filter with a selector: batch, schedule:*, ...)",
            description=(
                "List job runs registered in the workspace. Pass a selector to"
                " filter by matching jobs."
            ),
        )
        runs_list_p.add_argument(
            "selector_or_job_name",
            nargs="?",
            help="Selector or job name to filter runs by",
        )
        runs_list_p.add_argument(
            "--running",
            action="store_true",
            help="Show only runs that are not in a terminal state",
        )

        runs_info_p = runs_sub.add_parser(
            "info",
            help="Show job run info",
            description="Display detailed information about the job run",
        )
        runs_info_p.add_argument(
            "selector_or_job_name", help="Job name, script path, or selector"
        )
        runs_info_p.add_argument(
            "run_number",
            nargs="?",
            type=int,
            help="Run number (defaults to latest run of the given job)",
        )

        runs_logs_p = runs_sub.add_parser(
            "logs",
            help="Show logs for the latest or selected job run",
            description=(
                "Show logs for the latest or selected job run. Use -f/--follow"
                " to stream logs in real-time until completion."
            ),
        )
        runs_logs_p.add_argument(
            "selector_or_job_name", help="Job name, script path, or selector"
        )
        runs_logs_p.add_argument(
            "run_number",
            nargs="?",
            type=int,
            help="Run number (defaults to latest run)",
        )
        runs_logs_p.add_argument(
            "-f",
            "--follow",
            action="store_true",
            help="Follow logs in real-time until the run completes",
        )

        runs_show_p = runs_sub.add_parser(
            "show",
            help="Open the job run page in the web GUI",
            description=(
                "Print the URL of the job run page in the dltHub dashboard"
                " and open it in a browser when interactive."
            ),
        )
        runs_show_p.add_argument(
            "selector_or_job_name", help="Job name, script path, or selector"
        )
        runs_show_p.add_argument(
            "run_number",
            nargs="?",
            type=int,
            help="Run number (defaults to latest run of the given job)",
        )

        runs_cancel_p = runs_sub.add_parser(
            "cancel",
            help="Cancel the latest or selected job run",
            description="Cancel the latest or selected job run",
        )
        runs_cancel_p.add_argument(
            "selector_or_job_name", help="Job name, script path, or selector"
        )
        runs_cancel_p.add_argument(
            "run_number",
            nargs="?",
            type=int,
            help="Run number (defaults to latest run)",
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Other libraries
        from dlt._workspace.cli import echo as fmt

        # Current package
        import dlt_runtime._runtime_command as cmd

        _apply_timestamps(args)
        op1 = getattr(args, "op1", None)
        op2 = getattr(args, "op2", None)

        def action() -> None:
            if op1 is None:
                self.parser.print_help()
                return
            if op1 == "list":
                names = getattr(args, "selector_or_job_name", None) or []
                cmd.jobs_list(
                    selectors=names or None,
                    archived=bool(getattr(args, "archived", False)),
                )
            elif op1 == "info":
                cmd.job_info(getattr(args, "selector_or_job_name", None))
            elif op1 == "show":
                cmd.show_job(getattr(args, "selector_or_job_name", None))
            elif op1 == "trigger":
                cmd.trigger(
                    selectors=args.selectors,
                    dry_run=bool(getattr(args, "dry_run", False)),
                    profile=getattr(args, "profile", None),
                    refresh=bool(getattr(args, "refresh", False)),
                )
            elif op1 == "publish":
                if bool(getattr(args, "cancel", False)):
                    fmt.warning(
                        "'dlthub job publish --cancel' is deprecated. Use"
                        " 'dlthub job unpublish <script>' instead."
                    )
                cmd.publish(
                    args.script_path,
                    cancel=bool(getattr(args, "cancel", False)),
                )
            elif op1 == "unpublish":
                cmd.unpublish(args.script_path)
            elif op1 == "pause":
                cmd.pause_job(args.selector_or_job_name)
            elif op1 == "resume":
                cmd.resume_job(args.selector_or_job_name)
            elif op1 == "logs":
                cmd.logs(
                    args.selector_or_job_name,
                    args.run_number,
                    follow=bool(args.follow),
                )
            elif op1 == "cancel":
                cmd.cancel(
                    args.selector_or_job_name,
                    dry_run=bool(getattr(args, "dry_run", False)),
                )
            elif op1 == "runs":
                if op2 is None:
                    self._runs_parser.print_help()
                    return
                if op2 == "list":
                    cmd.get_runs(
                        getattr(args, "selector_or_job_name", None),
                        running=bool(getattr(args, "running", False)),
                    )
                elif op2 == "info":
                    cmd.get_job_run_info(args.selector_or_job_name, args.run_number)
                elif op2 == "logs":
                    cmd.job_run_logs(
                        args.selector_or_job_name,
                        args.run_number,
                        follow=bool(args.follow),
                    )
                elif op2 == "cancel":
                    cmd.cancel_job_run(args.selector_or_job_name, args.run_number)
                elif op2 == "show":
                    cmd.show_job_run(args.selector_or_job_name, args.run_number)
                else:
                    fmt.echo(f"Unknown runs subcommand: {op2}")
                    self.parser.print_usage()
            else:
                fmt.echo(f"Unknown job subcommand: {op1}")
                self.parser.print_usage()

        _dispatch(action)


# ---------------------------------------------------------------------------
# Pipeline extension — registers `dlthub pipeline run` as a sub-subcommand of dlt's pipeline shell.
# ---------------------------------------------------------------------------


class PipelineRunCommand(SupportsCliCommand):
    command = "run"
    parent: Optional[str] = "pipeline"
    compose: TCliCommandCompose = "replace"
    help_string = "Run a job by pipeline name"
    description = (
        "Run a job decorated with @run.pipeline, using pipeline_name: selector"
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        parser.add_argument(
            "pipeline_name",
            help="Name of the pipeline to run",
        )
        _add_launch_flags(
            parser,
            follow_help="Follow status changes and stream logs until the run completes",
            add_refresh=True,
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _apply_timestamps(args)
        _dispatch(
            lambda: cmd.run_pipeline(
                pipeline_name=args.pipeline_name,
                job_ref=getattr(args, "job_ref", None),
                follow=bool(getattr(args, "follow", False)),
                refresh=bool(getattr(args, "refresh", False)),
            )
        )


class PipelineShowCommand(SupportsCliCommand):
    command = "show"
    parent: Optional[str] = "pipeline"
    compose: TCliCommandCompose = "replace"
    help_string = "Open the pipeline observability view in the dltHub dashboard"
    description = (
        "Show the URL of the pipeline observability view in the dltHub"
        " dashboard and open it in a browser when interactive. Replaces the"
        " core dlt local-marimo `pipeline show`."
    )
    docs_url: Optional[str] = None

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        parser.add_argument("pipeline_name", help="Name of the pipeline to show")

    def execute(self, args: argparse.Namespace) -> None:
        # Current package
        import dlt_runtime._runtime_command as cmd

        _dispatch(lambda: cmd.show_pipeline(pipeline_name=args.pipeline_name))
