from argparse import ArgumentParser, Namespace

from spotml.commands.abstract_config_command import AbstractConfigCommand
from spotml.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotml.constants.constants import INTERNAL_TAG
from spotml.constants.run_status import RUNNING, LAUNCHING_INSTANCE, STOPPED_BY_USER, SCHEDULED, WAITING_FOR_SPOT
from spotml.deployment.abstract_instance_manager import AbstractInstanceManager
from spotml.deployment.utils.commands import get_tmux_session_command, \
    get_bash_command, get_send_keys_command, get_script_command
from spotml.deployment.utils.user_scripts import parse_script_parameters, render_script
from spotml.errors.nothing_to_do import NothingToDoError
from spotml.services.run_service import update_run_status, get_run


class HandleScheduledRunCommand(AbstractConfigCommand):
    name = 'handle-scheduled-run'
    description = 'Run a custom script from the configuration file inside the container'

    def configure(self, parser: ArgumentParser):
        super().configure(parser)
        parser.add_argument('script_name', metavar='SCRIPT_NAME', type=str, help='Script name')
        parser.add_argument('-u', '--user', type=str, default=None,
                            help='Container username or UID (format: <name|uid>[:<group|gid>])')
        parser.add_argument('-s', '--session-name', type=str, default=None, help='tmux session name')
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

    def _run(self, instance_manager: AbstractInstanceManager, args: Namespace, output: AbstractOutputWriter):
        run_status = get_run(args.run_id)['status']
        # Either it's a new scheduled run OR it's waiting for spot OR user reran a new run on a running instance.
        if run_status != SCHEDULED and run_status != WAITING_FOR_SPOT and run_status != RUNNING:
            print(f'{INTERNAL_TAG}Run status: {run_status} is neither "Scheduled", "Waiting for spot" nor "Running". '
                  f'Exiting now')
            return
        script_name = args.script_name
        scripts = instance_manager.project_config.scripts
        if script_name not in scripts:
            raise ValueError('Script "%s" is not defined in the configuration file.' % script_name)

        # replace script parameters
        params = parse_script_parameters(args.parameter)
        script_content = render_script(scripts[script_name], params)

        # check that the instance is started
        if not instance_manager.is_running():
            update_run_status(args.run_id, LAUNCHING_INSTANCE)
            instance_manager.start(output)

            instance_name = ''
            if len(instance_manager.project_config.instances) > 1:
                instance_name = ' ' + instance_manager.instance_config.name

            output.write('\n%s\n'
                         '\nUse the "spotml sh%s" command to connect to the container.\n'
                         % (instance_manager.get_status_text(), instance_name))

        # sync the project with the instance
        if not args.no_sync:
            try:
                instance_manager.sync_to_instance(output)
            except NothingToDoError:
                pass

        session_name = 'run'
        # get a command to run the script with "docker exec"
        # send_keys_command = get_send_keys_command(script_content, session_name)
        script_command = get_script_command(script_name, script_content, script_args=args.custom_args,
                                            logging=args.logging)
        command = instance_manager.container_commands.exec(script_command, interactive=True, tty=True,
                                                           user=args.user)

        # wrap the command with the tmux session
        if instance_manager.use_tmux:
            default_command = instance_manager.container_commands.exec(get_bash_command(), interactive=True, tty=True,
                                                                       user=args.user)
            command = get_tmux_session_command(command, session_name, script_name, default_command=default_command,
                                               keep_pane=True, detached=True)

        # execute command on the host OS
        print("\n Running below script on instance. \n")
        print(script_content)
        instance_manager.exec(command)
        update_run_status(args.run_id, RUNNING)
