from argparse import ArgumentParser, Namespace
from spotml.commands.abstract_config_command import AbstractConfigCommand
from spotml.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotml.deployment.utils.commands import get_bash_command, get_tmux_session_command
from spotml.errors.instance_not_running import InstanceNotRunningError
from spotml.deployment.abstract_instance_manager import AbstractInstanceManager


def get_session_name(args):
    session_name = 'spotml-sh-container'
    if args.session_name:
        session_name = args.session_name
    elif args.run:
        session_name = args.run
    return session_name


class ShCommand(AbstractConfigCommand):
    name = 'sh'
    description = 'Get a shell to the container or to the instance itself'

    def configure(self, parser: ArgumentParser):
        parser.add_argument('run', metavar='run', nargs='?', type=str, help='Ssh into run tmux session')
        super().configure(parser)
        parser.add_argument('-u', '--user', type=str, default=None,
                            help='Container username or UID (format: <name|uid>[:<group|gid>])')
        parser.add_argument('-H', '--host-os', action='store_true', help='Connect to the host OS instead of the Docker '
                                                                         'container')
        parser.add_argument('-s', '--session-name', type=str, default=None, help='tmux session name')
        parser.add_argument('-l', '--list-sessions', action='store_true', help='List all tmux sessions managed by the '
                                                                               'instance')

    def _run(self, instance_manager: AbstractInstanceManager, args: Namespace, output: AbstractOutputWriter):

        # check that the instance is started
        if not instance_manager.is_running():
            raise InstanceNotRunningError(instance_manager.instance_config.name)

        if args.list_sessions:
            if not instance_manager.use_tmux:
                raise ValueError('The "%s" provider doesn\'t support tmux.'
                                 % instance_manager.instance_config.provider_name)

            # a command to list existing tmux session on the host OS
            command = 'tmux ls; echo ""'
        else:
            if args.host_os:
                # get a command to open a login shell on the host OS
                session_name = args.session_name if args.session_name else 'spotml-sh-host'
                shell_command = '$SHELL'
                command = get_tmux_session_command(shell_command, session_name, keep_pane=False) \
                    if instance_manager.use_tmux else shell_command
            else:
                # get a command to run bash inside the docker container
                command = instance_manager.container_commands.exec(get_bash_command(), interactive=True, tty=True,
                                                                   user=args.user)

                # wrap the command with the tmux session
                if instance_manager.use_tmux:
                    session_name = get_session_name(args)

                    command = get_tmux_session_command(command, session_name, default_command=command, keep_pane=False)

        # execute command on the host OS
        instance_manager.exec(command)
