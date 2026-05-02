from argparse import ArgumentParser, Namespace
from spotml.commands.abstract_config_command import AbstractConfigCommand
from spotml.commands.writers.abstract_output_writrer import AbstractOutputWriter
from spotml.deployment.abstract_instance_manager import AbstractInstanceManager
from spotml.services.run_service import print_run_status


class StatusCommand(AbstractConfigCommand):
    name = 'status'
    description = 'Print information about the instance'

    def configure(self, parser: ArgumentParser):
        super().configure(parser)
        parser.add_argument('-l', '--logs', action='store_true', help='Print the latest run logs')

    def _run(self, instance_manager: AbstractInstanceManager, args: Namespace, output: AbstractOutputWriter):
        output.write("INSTANCE STATUS:")
        output.write(instance_manager.get_status_text())
        output.write("\nLAST RUN STATUS:")
        print_run_status(args.logs)
