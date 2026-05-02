from argparse import Namespace

from spotml.commands.abstract_config_command import AbstractConfigCommand
from spotml.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotml.deployment.abstract_instance_manager import AbstractInstanceManager
from spotml.services.run_service import track_instance_stop


class StopCommand(AbstractConfigCommand):
    name = 'stop'
    description = 'Terminate running instance and apply deletion policies for the volumes'

    # TODO: the "spotml start" command should restart the instance and the container if the instance was shutdown
    # def configure(self, parser: ArgumentParser):
    #     super().configure(parser)
    #     parser.add_argument('-s', '--shutdown', action='store_true',
    #                         help='Shutdown the instance without terminating it. Deletion policies for the volumes '
    #                              'won\'t be applied.')

    def _run(self, instance_manager: AbstractInstanceManager, args: Namespace, output: AbstractOutputWriter):
        instance_manager.stop(only_shutdown=False, output=output)
        track_instance_stop()
