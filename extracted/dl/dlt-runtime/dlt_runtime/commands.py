# Python internals
import argparse

# Other libraries
from dlt.common.configuration.plugins import SupportsCliCommand
from dlt_runtime.runtime_clients.api.models import InteractiveScriptType


class RuntimeCommand(SupportsCliCommand):
    command = "runtime"
    help_string = "Connect to dltHub Runtime and run your code remotely"
    description = """
    Allows you to connect to the dltHub Runtime, deploy and run local workspaces there. Requires dltHub license.
    """

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        self.parser = parser

        subparsers = parser.add_subparsers(
            title="Available subcommands", dest="runtime_command", required=False
        )

        subparsers.add_parser(
            "login",
            help=(
                "Log in to dltHub Runtime and connect the current workspace to"
                " the remote one"
            ),
            description="Log in to dltHub Runtime",
        )

        subparsers.add_parser(
            "logout",
            help="Log out from dltHub Runtime",
            description="Log out from dltHub Runtime",
        )

        # convenience commands
        launch_cmd = subparsers.add_parser(
            "launch",
            help="Deploy code/config and run a script (follow status and logs by default)",
            description="Deploy current workspace and run a batch script remotely.",
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

        schedule_cmd = subparsers.add_parser(
            "schedule",
            help=(
                "Deploy and schedule a script with a cron timetable, or cancel the scheduled script"
                " from future runs"
            ),
            description=(
                "Schedule a batch script to run on a cron timetable, or cancel the scheduled script"
                " from future runs."
            ),
        )
        self._configure_schedule_parser(schedule_cmd)

        logs_cmd = subparsers.add_parser(
            "logs",
            help="Show logs for latest or selected job run",
            description="Show logs for the latest run of a job or a specific run number.",
        )
        self._configure_logs_parser(logs_cmd)

        cancel_cmd = subparsers.add_parser(
            "cancel",
            help="Cancel latest or selected job run",
            description="Cancel the latest run of a job or a specific run number.",
        )
        self._configure_cancel_parser(cancel_cmd)

        subparsers.add_parser(
            "dashboard",
            help="Open the Runtime dashboard for this workspace",
            description="Open link to the Runtime dashboard for current remote workspace.",
        )

        subparsers.add_parser(
            "deploy",
            help="Sync code and configuration to Runtime without running anything",
            description="Upload deployment and configuration if changed.",
        )

        subparsers.add_parser(
            "info",
            help="Show overview of current Runtime workspace",
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
        # plural alias
        jobs_cmd = subparsers.add_parser(
            "jobs",
            help="List, create and inspect jobs",
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
        # plural alias
        job_runs_cmd = subparsers.add_parser(
            "job-runs",
            help="List, create and inspect job runs",
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

    def _configure_launch_parser(self, launch_cmd: argparse.ArgumentParser) -> None:
        launch_cmd.add_argument("script_path", help="Local path to the script")
        launch_cmd.add_argument(
            "-d",
            "--detach",
            action="store_true",
            help="Do not follow status changes and logs after starting",
        )

    def _configure_serve_parser(self, serve_cmd: argparse.ArgumentParser) -> None:
        serve_cmd.add_argument("script_path", help="Local path to the notebook/app")
        serve_cmd.add_argument(
            "--app-type",
            choices=[v.value for v in InteractiveScriptType],
            default=InteractiveScriptType.MARIMO.value,
            help="Specify if the interactive job is a marimo notebook, Streamlit app, or MCP server",
        )

    def _configure_publish_parser(self, publish_cmd: argparse.ArgumentParser) -> None:
        publish_cmd.add_argument("script_path", help="Local path to the notebook/app")
        publish_cmd.add_argument(
            "--cancel",
            action="store_true",
            help="Revoke the public link for the notebook/app",
        )

    def _configure_schedule_parser(self, schedule_cmd: argparse.ArgumentParser) -> None:
        schedule_cmd.add_argument("script_path", help="Local path to the script")
        schedule_cmd.add_argument(
            "cron_expr_or_cancel",
            help=(
                "Either a cron schedule string if you want to schedule the script, or the literal"
                " 'cancel' command if you want to cancel it"
            ),
        )
        schedule_cmd.add_argument(
            "--current",
            action="store_true",
            help="When cancelling the schedule, also cancel the currently running instance if any",
        )

    def _configure_logs_parser(self, logs_cmd: argparse.ArgumentParser) -> None:
        logs_cmd.add_argument("script_path_or_job_name", help="Local path or job name")
        logs_cmd.add_argument(
            "run_number", nargs="?", type=int, help="Run number (optional)"
        )

    def _configure_cancel_parser(self, cancel_cmd: argparse.ArgumentParser) -> None:
        cancel_cmd.add_argument(
            "script_path_or_job_name", help="Local path or job name"
        )
        cancel_cmd.add_argument(
            "run_number", nargs="?", type=int, help="Run number (optional)"
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
        deployment_subparsers.add_parser(
            "sync",
            help="Create new deployment if local workspace content changed",
            description="Create new deployment if local workspace content changed",
        )

    def _configure_jobs_parser(self, job_cmd: argparse.ArgumentParser) -> None:
        job_cmd.add_argument(
            "script_path_or_job_name",
            nargs="?",
            help="Local script path or job name. Required for all commands except `list`",
        )
        job_subparsers = job_cmd.add_subparsers(
            title="Available subcommands", dest="operation", required=False
        )
        job_subparsers.add_parser(
            "list",
            help="List the jobs registered in the workspace",
            description="List the jobs registered in the workspace",
        )
        job_subparsers.add_parser(
            "info",
            help="Show job info",
            description="Display detailed information about the job",
        )
        create_cmd = job_subparsers.add_parser(
            "create",
            help="Create a job without running it",
            description="Manually create the job",
        )
        create_cmd.add_argument("--name", nargs="?", help="Job name to create")
        create_cmd.add_argument(
            "--schedule",
            nargs="?",
            help="Cron schedule for the job if it's a scheduled one",
        )
        create_cmd.add_argument(
            "--interactive",
            action="store_true",
            help="Run the job interactively, e.g. for a notebook",
        )
        create_cmd.add_argument(
            "--app-type",
            choices=[v.value for v in InteractiveScriptType],
            help="Specify if the interactive app is a marimo notebook, Streamlit app, or MCP server.",
        )
        create_cmd.add_argument("--description", nargs="?", help="Job description")

    def _configure_job_runs_parser(self, job_run_cmd: argparse.ArgumentParser) -> None:
        job_run_cmd.add_argument(
            "script_path_or_job_name",
            nargs="?",
            help="Local script path or job name. Required for all commands except `list`",
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
            help="List the job runs registered in the workspace",
            description="List the job runs registered in the workspace",
        )
        job_run_subparsers.add_parser(
            "info",
            help="Show job run info",
            description="Display detailed information about the job run",
        )
        job_run_subparsers.add_parser(
            "create",
            help="Create a job run without running it",
            description="Manually create the job run",
        )
        job_run_subparsers.add_parser(
            "logs",
            help="Show logs for the latest or selected job run",
            description=(
                "Show logs for the latest or selected job run. Will follow logs if the run is not in a terminal state."
            ),
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
        configuration_subparsers.add_parser(
            "sync",
            help="Create new configuration if local config content changed",
            description="Create new configuration if local config content changed",
        )

    def execute(self, args: argparse.Namespace) -> None:
        # Other libraries
        from dlt._workspace.cli import echo as fmt

        import dlt_runtime._runtime_command as cmd
        from dlt_runtime.runtime import get_api_client

        fmt.echo("")  # leading newline for all runtime commands
        try:
            if args.runtime_command == "login":
                cmd.login(minimal_logging=False)
                return
            elif args.runtime_command == "logout":
                cmd.logout()
                return

            auth_service = cmd.login()
            api_client = get_api_client(auth_service)
            if args.runtime_command == "launch":
                cmd.launch(
                    args.script_path,
                    bool(args.detach),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "serve":
                cmd.serve(
                    args.script_path,
                    args.app_type,
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "publish":
                cmd.publish(
                    args.script_path,
                    cancel=bool(getattr(args, "cancel", False)),
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "schedule":
                if args.cron_expr_or_cancel == "cancel":
                    cmd.schedule_cancel(
                        args.script_path,
                        cancel_current=bool(args.current),
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                else:
                    cmd.schedule(
                        args.script_path,
                        args.cron_expr_or_cancel,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            elif args.runtime_command == "logs":
                cmd.logs(
                    args.script_path_or_job_name,
                    args.run_number,
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "cancel":
                cmd.cancel(
                    args.script_path_or_job_name,
                    args.run_number,
                    auth_service=auth_service,
                    api_client=api_client,
                )
            elif args.runtime_command == "dashboard":
                cmd.open_dashboard(auth_service=auth_service, api_client=api_client)
            elif args.runtime_command == "deploy":
                cmd.deploy(auth_service=auth_service, api_client=api_client)
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
                        minimal_logging=False,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            elif args.runtime_command in ("job", "jobs"):
                if args.operation == "list" or not args.operation:
                    cmd.jobs_list(auth_service=auth_service, api_client=api_client)
                elif args.operation == "info":
                    cmd.job_info(
                        args.script_path_or_job_name,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "create":
                    cmd.job_create(
                        args.script_path_or_job_name,
                        args,
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
                        minimal_logging=False,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            elif args.runtime_command in ("job-run", "job-runs"):
                # list runs across workspace or for a job
                if args.operation == "list" or not args.operation:
                    cmd.get_runs(
                        args.script_path_or_job_name,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "create":
                    cmd.create_job_run(
                        args.script_path_or_job_name,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "info":
                    cmd.get_job_run_info(
                        args.script_path_or_job_name,
                        args.run_number,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "logs":
                    cmd.job_run_logs(
                        args.script_path_or_job_name,
                        args.run_number,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
                elif args.operation == "cancel":
                    cmd.cancel_job_run(
                        args.script_path_or_job_name,
                        args.run_number,
                        auth_service=auth_service,
                        api_client=api_client,
                    )
            else:
                self.parser.print_usage()
        finally:
            fmt.echo("")  # trailing newline for all runtime commands
