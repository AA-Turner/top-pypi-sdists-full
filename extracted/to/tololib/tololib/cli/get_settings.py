from argparse import ArgumentParser, Namespace

from tololib.const import DEFAULT_PORT, DEFAULT_RETRY_COUNT, DEFAULT_RETRY_TIMEOUT

from ..client import ToloClient, ToloCommunicationError
from .common import Command


class GetSettingsCommand(Command):
    def __init__(self, argument_parser: ArgumentParser) -> None:
        super().__init__(argument_parser)
        argument_parser.add_argument("address", type=str)
        argument_parser.add_argument("-p", "--port", default=DEFAULT_PORT, type=int)
        argument_parser.add_argument("--retry-count", default=DEFAULT_RETRY_COUNT, type=int)
        argument_parser.add_argument("--retry-timeout", default=DEFAULT_RETRY_TIMEOUT, type=float)

    def __call__(self, args: Namespace) -> int:
        client = ToloClient(
            address=args.address, port=args.port, retry_count=args.retry_count, retry_timeout=args.retry_timeout
        )
        try:
            settings = client.get_settings()
            print(settings)

            for label, value in [
                ("Power Timer", settings.power_timer),
                ("Target Temperature", settings.target_temperature),
                ("Target Humidity", settings.target_humidity),
                ("Lamp Mode", settings.lamp_mode.name.capitalize()),
                ("Fan Timer", settings.fan_timer),
                ("Salt Bath Timer", settings.salt_bath_timer),
                ("Aroma Therapy Slot", settings.aroma_therapy_slot.name.capitalize()),
                ("Sweep Timer", settings.sweep_timer),
            ]:
                print(f"{label}:".ljust(21, " ") + str(value))
        except ToloCommunicationError:
            print(f"error fetching status from {args.address}:{args.port}")
            return 1

        return 0
