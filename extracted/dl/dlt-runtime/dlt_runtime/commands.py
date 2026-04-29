# Python internals
import argparse
from collections.abc import Iterator

# Other libraries
from dlt.common.configuration.plugins import SupportsCliCommand


def _has_visible_subparsers(parser: argparse.ArgumentParser) -> bool:
    """Check whether a parser has any non-suppressed subparsers.

    Note: uses argparse private attributes (_subparsers, _actions,
    _SubParsersAction, _choices_actions) because argparse has no public
    introspection API.
    """
    if parser._subparsers is None:
        return False
    for action in parser._subparsers._actions:
        if not isinstance(action, argparse._SubParsersAction):
            continue
        for choice_action in action._choices_actions:
            if choice_action.help != argparse.SUPPRESS:
                return True
    return False


def _build_command_tree_lines(
    parser: argparse.ArgumentParser, prefix: str = "", base_indent: int = 0
) -> Iterator[str]:
    """Recursively yield formatted lines of the command tree.

    ``base_indent`` is a fixed left-margin (in two-space units) applied to
    every line.  It is not incremented during recursion -- nested depth is
    conveyed by growing the ``prefix`` (e.g. "deployment list").

    Note: uses argparse private attributes (_subparsers, _actions,
    _SubParsersAction, _choices_actions) because argparse has no public
    introspection API.
    """
    if parser._subparsers is None:
        return
    for action in parser._subparsers._actions:
        if not isinstance(action, argparse._SubParsersAction):
            continue
        seen: set[str] = set()
        for choice_action in action._choices_actions:
            name = choice_action.dest
            if name in seen:
                continue
            seen.add(name)
            help_msg = choice_action.help
            if help_msg == argparse.SUPPRESS:
                continue
            subparser = action.choices[name]
            full_name = f"{prefix} {name}" if prefix else name
            if _has_visible_subparsers(subparser):
                yield from _build_command_tree_lines(subparser, full_name, base_indent)
            else:
                padding = " " * max(1, 30 - len(full_name) - base_indent * 2)
                yield f"{'  ' * base_indent}{full_name}{padding}{help_msg}"


class RuntimeCommand(SupportsCliCommand):
    command = "runtime"
    help_string = "Connect to dltHub Runtime and run your code remotely"
    description = """
    Allows you to connect to the dltHub Runtime, deploy and run local workspaces there. Requires dltHub license.
    """

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser
        parser.add_argument(
            "--help-all",
            action="store_true",
            help="Show all commands including subcommands",
        )
        parser.add_argument(
            "--timestamps",
            action="store_true",
            help=(
                "Show exact ISO timestamps and precise durations (e.g. 1.291 s)"
                " instead of humanized relative times."
            ),
        )

        subparsers = parser.add_subparsers(
            title="Available subcommands", dest="runtime_command", required=False
        )

        login_parser = subparsers.add_parser(
            "login",
            help=(
                "Log in to dltHub Runtime and connect the current workspace to"
                " the remote one"
            ),
            description="Log in to dltHub Runtime",
        )
        login_parser.add_argument(
            "--workspace",
            "-w",
            type=str,
            default=None,
            help="Select workspace by name or ID (skip interactive prompt)",
        )
        login_parser.add_argument(
            "--resume",
            type=str,
            default=None,
            metavar="DEVICE_CODE",
            help=(
                "Resume a previously started device flow login. The DEVICE_CODE"
                " is printed by `dlt runtime login` when no TTY is attached."
            ),
        )

        subparsers.add_parser(
            "logout",
            help="Log out from dltHub Runtime",
            description="Log out from dltHub Runtime",
        )

        # convenience commands
        launch_cmd = subparsers.add_parser(
            "launch",
            help="Deploy code/config and run a script",
            description="Deploy current workspace and run a batch script remotely. Use -f/--follow to tail logs until completion.",
        )
        self._configure_launch_parser(launch_cmd)

        serve_cmd = subparsers.add_parser(
            "serve",
            help="Deploy and serve an interactive notebook/app (read-only) and follow until ready",
            description="Deploy current workspace and run a notebook as a read-only web app.",
        )
        self._configure_serve_parser(serve_cmd)

        publish_cmd = subparsers.add_parser(
            "publish",
            help="Generate or revoke a public link for an interactive notebook/app",
            description="Generate a public link for a notebook/app, or revoke it with --cancel.",
        )
        self._configure_publish_parser(publish_cmd)

        unpublish_cmd = subparsers.add_parser(
            "unpublish",
            help="Revoke the public link for an interactive notebook/app",
            description="Revoke the public link for an interactive notebook/app.",
        )
        self._configure_unpublish_parser(unpublish_cmd)

        trigger_cmd = subparsers.add_parser(
            "trigger",
            help="Trigger jobs matching selectors (does not sync or deploy)",
            description=(
                "Trigger runs for jobs matching the given selectors. "
                "Does not sync code or deploy jobs. "
                "Examples: 'tag:backfill', 'manual:jobs.etl.*', 'schedule:*'"
            ),
        )
        self._configure_trigger_parser(trigger_cmd)

        run_pipeline_cmd = subparsers.add_parser(
            "run-pipeline",
            help="Run a job by pipeline name",
            description="Run a job that uses the given pipeline. Uses 'pipeline_name:' trigger selector.",
        )
        self._configure_run_pipeline_parser(run_pipeline_cmd)

        logs_cmd = subparsers.add_parser(
            "logs",
            help="Show logs for latest or selected job run (shortcut for 'job-run logs')",
            description="Show logs for the latest run of a job or a specific run number. Use -f/--follow to stream logs in real-time.",
        )
        self._configure_logs_parser(logs_cmd)

        cancel_cmd = subparsers.add_parser(
            "cancel",
            help="Cancel active runs for matching jobs",
            description=(
                "Cancel active (non-terminal) runs for jobs matching selectors or names."
                " Accepts one or more selectors (batch, schedule:*, tag:ops, etc.)"
                " or job names. Use --dry-run to preview."
            ),
        )
        self._configure_cancel_parser(cancel_cmd)

        subparsers.add_parser(
            "dashboard",
            help="Open the Runtime dashboard for this workspace",
            description="Open link to the Runtime dashboard for current remote workspace.",
        )

        deploy_cmd = subparsers.add_parser(
            "deploy",
            help="Sync code/config and deploy jobs from __deployment__ manifest",
            description="Sync workspace files, generate job manifest from __deployment__.py, and reconcile jobs with the runtime. Use --dry-run to preview changes.",
        )
        deploy_cmd.add_argument(
            "--file",
            type=str,
            default=None,
            help="Python file to use as manifest source (instead of __deployment__)",
        )
        deploy_cmd.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview changes without applying them",
        )
        deploy_cmd.add_argument(
            "--show-manifest",
            action="store_true",
            help="Dump the expanded deployment manifest as YAML and exit",
        )

        subparsers.add_parser(
            "info",
            help="Show overview of current Runtime workspace (shows workspace, job count, latest run, latest deployment, and latest configuration)",
            description="Show workspace ID and summary of deployments, configurations and jobs.",
        )

        # deployments
        deployment_cmd = subparsers.add_parser(
            "deployment",
            help="Manipulate deployments in the workspace",
            description="Manipulate deployments in the workspace",
        )
        self._configure_deployments_parser(deployment_cmd)

        # jobs (ex-scripts)
        job_cmd = subparsers.add_parser(
            "job",
            help="List, create and inspect jobs",
            description="List and manipulate jobs registered in the workspace.",
        )
        self._configure_jobs_parser(job_cmd)
        # plural alias (hidden from help output)
        jobs_cmd = subparsers.add_parser(
            "jobs",
            description="List and manipulate jobs registered in the workspace.",
        )
        self._configure_jobs_parser(jobs_cmd)

        # job-runs (ex-script-runs)
        job_run_cmd = subparsers.add_parser(
            "job-run",
            help="List, create and inspect job runs",
            description="List and manipulate job runs registered in the workspace.",
        )
        self._configure_job_runs_parser(job_run_cmd)
        # plural alias (hidden from help output)
        job_runs_cmd = subparsers.add_parser(
            "job-runs",
            description="List and manipulate job runs registered in the workspace.",
        )
        self._configure_job_runs_parser(job_runs_cmd)

        # configurations
        configuration_cmd = subparsers.add_parser(
            "configuration",
            help="Manipulate configurations in the workspace",
            description="Manipulate configurations in the workspace",
        )
        self._configure_configurations_parser(configuration_cmd)

        # workspaces
        workspace_cmd = subparsers.add_parser(
            "workspace",
            help="List and manage workspaces",
            description="List and manage workspaces in your organization.",
        )
        self._configure_workspace_parser(workspace_cmd)

    def _configure_workspace_parser(
        self, workspace_cmd: argparse.ArgumentParser
    ) -> None:
        workspace_subparsers = workspace_cmd.add_subparsers(
            title="Available subcommands", dest="operation", required=False
        )
        workspace_subparsers.add_parser(
            "list",
            help="List all workspaces you have access to",
            description="List all workspaces you have access to",
        )
        switch_parser = workspace_subparsers.add_parser(
            "switch",
            help="Switch to a different workspace by name or ID",
            description="Switch the locally connected workspace without re-running login",
        )
        switch_parser.add_argument(
            "workspace",
            type=str,
            nargs="?",
            default=None,
            help=(
                "Workspace name or ID to switch to. If omitted, an interactive "
                "picker is shown with an option to create a new workspace."
            ),
        )

    def _configure_launch_parser(self, launch_cmd: argparse.ArgumentParser) -> None:
        launch_cmd.add_argument(
            "selector_or_job_ref",
            nargs="?",
            default=None,
            help="Selector or job ref to pick a job from the manifest",
        )
        launch_cmd.add_argument(
            "--file",
            type=str,
            default=None,
            help="Python file to use as manifest source (instead of __deployment__)",
        )
        launch_cmd.add_argument(
            "-f",
            "--follow",
            action="store_true",
            help="Follow status changes and stream logs until the run completes",
        )
        launch_cmd.add_argument(
            "--refresh",
            action="store_true",
            help="Re-run from scratch (full reload). Cascades to freshness-graph downstream jobs.",
        )

    def _configure_serve_parser(self, serve_cmd: argparse.ArgumentParser) -> None:
        serve_cmd.add_argument(
            "selector_or_job_ref",
            nargs="?",
            default=None,
            help="Selector or job ref to pick an interactive app from the manifest",
        )
        serve_cmd.add_argument(
            "--file",
            type=str,
            default=None,
            help="Python file to use as manifest source (instead of __deployment__)",
        )
        serve_cmd.add_argument(
            "-f",
            "--follow",
            action="store_true",
            help="Stream logs until the app stops",
        )

    def _configure_publish_parser(self, publish_cmd: argparse.ArgumentParser) -> None:
        publish_cmd.add_argument("script_path", help="Local path to the notebook/app")
        publish_cmd.add_argument(
            "--cancel",
            action="store_true",
            help="Revoke the public link for the notebook/app",
        )

    def _configure_trigger_parser(self, trigger_cmd: argparse.ArgumentParser) -> None:
        trigger_cmd.add_argument(
            "selectors",
            nargs="+",
            help="Trigger selectors (fnmatch patterns), e.g. 'tag:backfill', 'manual:jobs.etl.*'",
        )
        trigger_cmd.add_argument(
            "--dry-run",
            action="store_true",
            help="Preview matched jobs without creating runs",
        )
        trigger_cmd.add_argument(
            "--profile",
            type=str,
            default=None,
            help="Profile override for all triggered runs",
        )
        trigger_cmd.add_argument(
            "--refresh",
            action="store_true",
            help="Force a refresh on every triggered job (jobs skipped by freshness are not refreshed).",
        )

    def _configure_run_pipeline_parser(
        self, run_pipeline_cmd: argparse.ArgumentParser
    ) -> None:
        run_pipeline_cmd.add_argument(
            "pipeline_name",
            help="Name of the pipeline to run",
        )
        run_pipeline_cmd.add_argument(
            "--job-ref",
            type=str,
            default=None,
            help="Specific job ref if multiple jobs use the same pipeline",
        )
        run_pipeline_cmd.add_argument(
            "-f",
            "--follow",
            action="store_true",
            help="Follow status changes and stream logs until the run completes",
        )
        run_pipeline_cmd.add_argument(
            "--refresh",
            action="store_true",
            help="Re-run from scratch (full reload). Cascades to freshness-graph downstream jobs.",
        )

    def _configure_unpublish_parser(
        self, unpublish_cmd: argparse.ArgumentParser
    ) -> None:
        unpublish_cmd.add_argument("script_path", help="Local path to the notebook/app")

    def _configure_logs_parser(self, logs_cmd: argparse.ArgumentParser) -> None:
        logs_cmd.add_argument(
            "selector_or_job_name",
            help=("Job name, script path, or selector (e.g. batch, schedule:*)."),
        )
        logs_cmd.add_argument(
            "run_number", nargs="?", type=int, help="Run number (optional)"
        )
        logs_cmd.add_argument(
            "-f",
            "--follow",
            action="store_true",
            help="Follow logs in real-time until the run completes",
        )

    def _configure_cancel_parser(self, cancel_cmd: argparse.ArgumentParser) -> None:
        cancel_cmd.add_argument(
            "selector_or_job_name",
            nargs="+",
            help=(
                "Job name, script path, or selector (e.g. batch, schedule:*)."
                " Multiple values cancel active runs for all matching jobs."
            ),
        )
        cancel_cmd.add_argument(
            "--dry-run",
            action="store_true",
            help="Show what would be cancelled without actually cancelling",
        )

    def _configure_deployments_parser(
        self, deployment_cmd: argparse.ArgumentParser
    ) -> None:
        # list/info/sync on deployments
        deployment_cmd.add_argument(
            "deployment_version_no",
            nargs="?",
            type=int,
            help="Deployment version number. Only used in the `info` subcommand",
        )
        deployment_subparsers = deployment_cmd.add_subparsers(
            title="Available subcommands", dest="operation", required=False
        )
        deployment_subparsers.add_parser(
            "list",
            help="List all deployments in workspace",
            description="List all deployments in workspace",
        )
        deployment_subparsers.add_parser(
            "info",
            help="Get detailed information about a deployment",
            description="Get detailed information about a deployment",
        )
        deployment_sync_parser = deployment_subparsers.add_parser(
            "sync",
            help="Create new deployment if local workspace content changed",
            description="Create new deployment if local workspace content changed",
        )
        deployment_sync_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Compare local files to latest deployment without uploading",
        )
        deployment_sync_parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Print per-file added/updated/deleted tree alongside the summary",
        )

    def _configure_jobs_parser(self, job_cmd: argparse.ArgumentParser) -> None:
        job_cmd.add_argument(
            "selector_or_job_name",
            nargs="*",
            help=(
                "Job name, script path, or selector (e.g. batch, schedule:*)."
                " Multiple selectors narrow the listing. Required for `info`."
            ),
        )
        job_subparsers = job_cmd.add_subparsers(
            title="Available subcommands", dest="operation", required=False
        )
        job_subparsers.add_parser(
            "list",
            help="List jobs (filter with selectors: batch, schedule:*, tag:ops, ...)",
            description=(
                "List jobs registered in the workspace."
                " Pass selectors before `list` to filter:"
                " batch, interactive, schedule:*, tag:<name>, manual:*, etc."
            ),
        )
        job_subparsers.add_parser(
            "info",
            help="Show job info",
            description="Display detailed information about the job",
        )

    def _configure_job_runs_parser(self, job_run_cmd: argparse.ArgumentParser) -> None:
        job_run_cmd.add_argument(
            "selector_or_job_name",
            nargs="?",
            help=(
                "Job name, script path, or selector (e.g. batch, schedule:*)."
                " For `list`: filters runs by matching jobs."
                " Required for `info`, `logs`, `cancel`."
            ),
        )
        job_run_cmd.add_argument(
            "run_number",
            nargs="?",
            type=int,
            help=(
                "Run number. Used in all commands except `list` and `create` as optional argument."
                " If not specified, the latest run of the given script will be used."
            ),
        )
        job_run_subparsers = job_run_cmd.add_subparsers(
            title="Available subcommands", dest="operation", required=False
        )
        job_run_subparsers.add_parser(
            "list",
            help="List job runs (filter with a selector: batch, schedule:*, ...)",
            description=(
                "List job runs registered in the workspace."
                " Pass a selector before `list` to filter by matching jobs."
            ),
        )
        job_run_subparsers.add_parser(
            "info",
            help="Show job run info",
            description="Display detailed information about the job run",
        )
        logs_sub = job_run_subparsers.add_parser(
            "logs",
            help="Show logs for the latest or selected job run",
            description=(
                "Show logs for the latest or selected job run. Use -f/--follow to stream logs in real-time until completion."
            ),
        )
        logs_sub.add_argument(
            "-f",
            "--follow",
            action="store_true",
            help="Follow logs in real-time until the run completes",
        )
        job_run_subparsers.add_parser(
            "cancel",
            help="Cancel the latest or selected job run",
            description="Cancel the latest or selected job run",
        )

    def _configure_configurations_parser(
        self, configuration_cmd: argparse.ArgumentParser
    ) -> None:
        # list/info/sync on configurations
        configuration_cmd.add_argument(
            "configuration_version_no",
            nargs="?",
            type=int,
            help="Configuration version number. Only used in the `info` subcommand",
        )
        configuration_subparsers = configuration_cmd.add_subparsers(
            title="Available subcommands", dest="operation", required=False
        )
        configuration_subparsers.add_parser(
            "list",
            help="List all configuration versions",
            description="List all configuration versions",
        )
        configuration_subparsers.add_parser(
            "info",
            help="Get detailed information about a configuration",
            description="Get detailed information about a configuration",
        )
        configuration_sync_parser = configuration_subparsers.add_parser(
            "sync",
            help="Create new configuration if local config content changed",
            description="Create new configuration if local config content changed",
        )
        configuration_sync_parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Compare local config to latest configuration without uploading",
        )
        configuration_sync_parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Print per-file added/updated/deleted tree alongside the summary",
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Other libraries
        from dlt._workspace.cli import echo as fmt
        from dlt._workspace.cli.exceptions import CliCommandInnerException

        import dlt_runtime._runtime_command as cmd
        from dlt_runtime._runtime_command_views import set_show_exact_timestamps
        from dlt_runtime.exceptions import RuntimeNotAuthenticated
        from dlt_runtime.runtime import get_api_client
        from dlt_runtime.version import __version__

        # Apply --timestamps flag to all view formatting before any subcommand runs.
        set_show_exact_timestamps(bool(getattr(args, "timestamps", False)))

        # Command tree: shown for --help-all OR when no subcommand is given
        if args.help_all or not args.runtime_command:
            fmt.echo("")
            fmt.echo(f"dlt-runtime v{__version__}")
            fmt.echo("")
            fmt.echo("dlt runtime")
            for line in _build_command_tree_lines(self.parser, base_indent=1):
                fmt.echo(line)
            fmt.echo("")
            fmt.echo(
                'Use "dlt runtime <command> --help" for detailed usage of a'
                " specific command."
            )
            fmt.echo("")
            return

        # Banner + hint for specific commands
        fmt.echo("")
        fmt.echo(f"dlt-runtime v{__version__}")
        fmt.echo('Use "dlt runtime --help-all" for full command reference.')
        fmt.echo("")
        try:
            if args.runtime_command == "login":
                cmd.login(
                    minimal_logging=False,
                    workspace=args.workspace,
                    resume=args.resume,
                    # select workspace as additional step in non interactive mode
                    restart_if_no_workspace=True,
                )
                return
            elif args.runtime_command == "logout":
                cmd.logout()
                return
            # workspace commands only need auth (token), not a connected workspace,
            # so they are dispatched before login() which would force workspace selection.
            elif args.runtime_command == "workspace":
                if args.operation == "list" or not args.operation:
                    cmd.workspace_list()
                    return
                elif args.operation == "switch":
                    cmd.workspace_switch(args.workspace)
                    return

            auth_service = cmd.login(not_logged_in_hint=True)
            # In non-interactive mode without an existing token, login() prints
            # device-flow info and returns None. Abort here — the user must
            # complete Phase 1 → 2 before running other commands.
            if auth_service is None:
                return
            api_client = get_api_client(auth_service)
            if args.runtime_command == "launch":
                cmd.launch(
                    selector_or_job_ref=args.selector_or_job_ref,
                    file=getattr(args, "file", None),
                    follow=bool(args.follow),
                    refresh=bool(getattr(args, "refresh", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "serve":
                cmd.serve(
                    selector_or_job_ref=args.selector_or_job_ref,
                    file=getattr(args, "file", None),
                    follow=bool(getattr(args, "follow", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "trigger":
                cmd.trigger(
                    selectors=args.selectors,
                    dry_run=bool(getattr(args, "dry_run", False)),
                    profile=getattr(args, "profile", None),
                    refresh=bool(getattr(args, "refresh", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "run-pipeline":
                cmd.run_pipeline(
                    pipeline_name=args.pipeline_name,
                    job_ref=getattr(args, "job_ref", None),
                    follow=bool(getattr(args, "follow", False)),
                    refresh=bool(getattr(args, "refresh", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "unpublish":
                cmd.unpublish(
                    args.script_path,
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "publish":
                if bool(getattr(args, "cancel", False)):
                    fmt.warning(
                        "'dlt runtime publish --cancel' is deprecated."
                        " Use 'dlt runtime unpublish <script>' instead."
                    )
                cmd.publish(
                    args.script_path,
                    cancel=bool(getattr(args, "cancel", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "logs":
                cmd.logs(
                    args.selector_or_job_name,
                    args.run_number,
                    follow=bool(args.follow),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "cancel":
                cmd.cancel(
                    args.selector_or_job_name,
                    dry_run=bool(getattr(args, "dry_run", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "dashboard":
                cmd.open_dashboard(auth_service=auth_service, api_client=api_client)
            elif args.runtime_command == "deploy":
                cmd.deploy_manifest(
                    file=getattr(args, "file", None),
                    dry_run=bool(getattr(args, "dry_run", False)),
                    show_manifest=bool(getattr(args, "show_manifest", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "info":
                cmd.runtime_info(auth_service=auth_service, api_client=api_client)
            elif args.runtime_command == "deployment":
                if args.operation == "list":
                    cmd.get_deployments(
                        auth_service=auth_service, api_client=api_client
                    )
                elif args.operation == "info" or not args.operation:
                    cmd.get_deployment_info(
                        deployment_version_no=(
                            int(args.deployment_version_no)
                            if args.deployment_version_no
                            else None
                        ),
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "sync":
                    cmd.sync_deployment(
                        level="full",
                        dry_run=bool(getattr(args, "dry_run", False)),
                        verbose=bool(getattr(args, "verbose", False)),
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            elif args.runtime_command in ("job", "jobs"):
                _names = args.selector_or_job_name or []
                if args.operation == "list" or not args.operation:
                    cmd.jobs_list(
                        selectors=_names or None,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "info":
                    cmd.job_info(
                        _names[0] if _names else None,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            elif args.runtime_command == "configuration":
                if args.operation == "list":
                    cmd.get_configurations(
                        auth_service=auth_service, api_client=api_client
                    )
                elif args.operation == "info" or not args.operation:
                    cmd.get_configuration_info(
                        configuration_version_no=(
                            int(args.configuration_version_no)
                            if args.configuration_version_no
                            else None
                        ),
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "sync":
                    cmd.sync_configuration(
                        level="full",
                        dry_run=bool(getattr(args, "dry_run", False)),
                        verbose=bool(getattr(args, "verbose", False)),
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            elif args.runtime_command in ("job-run", "job-runs"):
                # list runs across workspace or for a job
                if args.operation == "list" or not args.operation:
                    cmd.get_runs(
                        args.selector_or_job_name,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "info":
                    cmd.get_job_run_info(
                        args.selector_or_job_name,
                        args.run_number,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "logs":
                    cmd.job_run_logs(
                        args.selector_or_job_name,
                        args.run_number,
                        follow=bool(args.follow),
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "cancel":
                    cmd.cancel_job_run(
                        args.selector_or_job_name,
                        args.run_number,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            else:
                fmt.echo(f"Unknown command: {args.runtime_command}")
                self.parser.print_usage()
        except RuntimeNotAuthenticated as e:
            # `workspace list/switch` are pre-login commands — pointing the user
            # at `dlt runtime login` is more useful than auto-starting a device
            # flow they didn't ask for.
            if args.runtime_command == "workspace":
                raise CliCommandInnerException(
                    cmd="runtime",
                    msg="Not logged in. Run `dlt runtime login` to authenticate.",
                    inner_exc=e,
                ) from e
            # Issue #645: 401 from API or no/expired token. Surface the original
            # error and drop into Phase 1 device flow so an LLM agent gets
            # actionable `--resume <code>` instructions.
            from dlt_runtime._runtime_command import (
                _print_device_flow_start,
                _start_device_flow,
            )

            flow = _start_device_flow()
            _print_device_flow_start(
                flow["verification_uri"],
                flow["user_code"],
                flow["device_code"],
                not_logged_in_hint=True,
            )
            raise CliCommandInnerException(
                cmd="runtime",
                msg=str(e) or "Authentication required. Run 'dlt runtime login'.",
                inner_exc=e,
            ) from e
        except CliCommandInnerException:
            # Already user-facing with cmd/msg/inner_exc set. Pass through.
            raise
        except Exception as e:
            # Single uniform translation: every other exception becomes a
            # CliCommandInnerException so dlt display layer formats it
            # consistently. KeyboardInterrupt is BaseException (not caught).
            raise CliCommandInnerException(
                cmd="runtime", msg=str(e), inner_exc=e
            ) from e
        finally:
            fmt.echo("")  # trailing newline for all runtime commands
