from spotml.commands.abstract_provider_command import AbstractProviderCommand
from spotml.providers.aws.commands.clean_logs import CleanLogsCommand
from spotml.providers.aws.commands.spot_prices import SpotPricesCommand


class AwsCommand(AbstractProviderCommand):

    name = 'aws'
    description = 'AWS commands'
    commands = [
        SpotPricesCommand,
        CleanLogsCommand,
    ]
