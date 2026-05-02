import json
import logging
from argparse import ArgumentParser, Namespace

from spotml.commands.abstract_config_command import AbstractConfigCommand
from spotml.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotml.constants.constants import INTERNAL_TAG
from spotml.constants.run_status import STOPPED_DUE_TO_IDLE_TIME, WAITING_FOR_SPOT, RUNNING, \
    STOPPED_UNKNOWN_REASON
from spotml.deployment.abstract_ssh_instance_manager import AbstractSshInstanceManager
from spotml.services.run_service import update_run_status, get_run


class HandleActiveRunCommand(AbstractConfigCommand):
    name = 'handle-active-run'
    description = 'Run a custom script from the configuration file inside the container'

    def configure(self, parser: ArgumentParser):
        super().configure(parser)
        parser.add_argument('script_name', metavar='SCRIPT_NAME', type=str, help='Script name')
        parser.add_argument('-u', '--user', type=str, default=None,
                            help='Container username or UID (format: <name|uid>[:<group|gid>])')
        parser.add_argument('-s', '--session-name', type=str, default=None, help='tmux session name')
        parser.add_argument('-i', '--max-idle-minutes', type=int,
                            help='Maximum Idle minutes to wait before turning off '
                                 'instance.')
        parser.add_argument('-l', '--logging', action='store_true', help='Log the script outputs to a file')
        parser.add_argument('-p', '--parameter', metavar='PARAMETER=VALUE', action='append', type=str, default=[],
                            help='Set a value for the script parameter (format: PARAMETER=VALUE). This '
                                 'argument can be used multiple times to set several parameters. Parameters can be '
                                 'used in the script as Mustache variables (for example: {{PARAMETER}}).')
        parser.add_argument('--no-sync', action='store_true', help='Don\'t sync the project before running the script')

        # add the "double-dash" argument to the usage message
        parser.prog = 'spotml run'
        parser.usage = parser.format_usage()[7:-1] + ' [-- args...]\n'
        parser.epilog = 'The double dash (--) separates custom arguments that you can pass to the script ' \
                        'from the spotml arguments.'

    def _run(self, instance_manager: AbstractSshInstanceManager, args: Namespace, output: AbstractOutputWriter):
        run = get_run(args.run_id)
        # check that the instance is started
        if not instance_manager.is_running():
            logging.info("Instance is already not running.")
            if run['status'] == RUNNING and run['command'] == "run":
                logging.info("It was probably killed by spot instance recall")
                update_run_status(args.run_id, WAITING_FOR_SPOT)
            if run['status'] == RUNNING and run['command'] == "start":
                logging.info("It was probably killed by spot instance recall")
                update_run_status(args.run_id, STOPPED_UNKNOWN_REASON)
            return

        result = instance_manager.exec_capture_output(
            'python3 /tmp/spotml/instance/scripts/startup/07_check_host_status.py')

        host_status = json.loads(result.stdout)
        print(f'{INTERNAL_TAG} {json.dumps(host_status)}')
        print(f"{INTERNAL_TAG} Idle Time Seconds: {host_status['idle_time_seconds']}")
        print(f"Detected Instance Idle Time: {host_status['idle_time']}")
        print(f"Detected Running Command: {host_status['running_command']}")
        print(f"Configured Max Idle minutes: {args.max_idle_minutes}")
        if not host_status['running_command'] and float(host_status['idle_time_seconds']) > args.max_idle_minutes * 60:
            print(f"Stopping instance due to idle time being longer than {args.max_idle_minutes} mins")
            instance_manager.stop(only_shutdown=False, output=output)
            update_run_status(args.run_id, STOPPED_DUE_TO_IDLE_TIME)
