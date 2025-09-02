from argparse import ArgumentParser, Namespace

from tololib.const import DEFAULT_PORT, DEFAULT_RETRY_COUNT, DEFAULT_RETRY_TIMEOUT

from ..client import ToloClient, ToloCommunicationError
from .common import Command


class GetStatusCommand(Command):
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
            status = client.get_status()
            for label, value in [
                ("Model", status.model.name.capitalize()),
                ("Power On", status.power_on),
                ("Power Timer", status.power_timer),
                ("Water Level (%)", status.water_level_percent),
                ("Flow In", status.flow_in),
                ("Flow Out", status.flow_out),
                ("Current Temperature", status.current_temperature),
                ("Tank Temperature", status.tank_temperature),
                ("Current Humidity", status.current_humidity),
                ("Lamp On", status.lamp_on),
                ("Fan On", status.fan_on),
                ("Fan Timer", status.fan_timer),
                ("Salt Bath On", status.salt_bath_on),
                ("Salt Bath Timer", status.salt_bath_timer),
                ("Aroma Therapy On", status.aroma_therapy_on),
                ("Sweep On", status.sweep_on),
                ("Sweep Timer", status.sweep_timer),
                ("Calefaction", status.calefaction.name.capitalize()),
            ]:
                print(f"{label}:".ljust(21, " ") + str(value))
        except ToloCommunicationError:
            print(f"error fetching status from {args.address}:{args.port}")
            return 1

        return 0
