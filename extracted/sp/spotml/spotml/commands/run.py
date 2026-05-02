from argparse import ArgumentParser, Namespace

from spotml.commands.abstract_config_command import AbstractConfigCommand
from spotml.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotml.deployment.abstract_instance_manager import AbstractInstanceManager
from spotml.errors.nothing_to_do import NothingToDoError
from spotml.services.run_service import track_instance_start, track_instance_stop


class ManageCommand(AbstractConfigCommand):
    name = 'run'
    description = 'Run a custom script remotely managed by SpotML'

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
        # check that the script exists
        script_name = args.script_name
        if script_name == "stop":
            if instance_manager.is_running():
                track_instance_start(instance_manager.ssh_key_path)
                print(
                    'Note that you need to manually ssh and kill any running commands. Use the "spotml sh run" '
                    'command to connect to the running session.\n')
            else:
                track_instance_stop()
            return

        scripts = instance_manager.project_config.scripts
        if script_name not in scripts:
            raise ValueError('Script "%s" is not defined in the configuration file.' % script_name)

        instance_manager.check_dockerfile_exists()
        instance_manager.create_or_get_bucket(output, False)
        instance_manager.maybe_create_key()

        # sync the project with the instance
        if not args.no_sync:
            try:
                instance_manager.sync_to_bucket(output, False)
            except NothingToDoError:
                pass

        instance_manager.sendConfigCredentialFiles(args.script_name)
        output.write("Scheduled run on the cloud. Use 'spotml status' to check the status of the run. \n")
