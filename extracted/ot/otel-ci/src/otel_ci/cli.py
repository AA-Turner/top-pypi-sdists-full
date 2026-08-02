import argparse
import pathlib

from otel_ci import settings
from otel_ci.exec import exec_command
from otel_ci.logging import configure_logging
from otel_ci.replay import replay
from otel_ci.trace import configure_tracer

parser = argparse.ArgumentParser(description="A CLI tool")
parser.add_argument(
    "--service",
    "-s",
    type=str,
    dest="service_name",
    help="The name of the service [default:otel-cli]",
)
parser.add_argument(
    "--name",
    "-n",
    type=str,
    dest="span_name",
    help="The name of the span [default: command]",
)
parser.add_argument(
    "--resource-attributes",
    "-r",
    type=str,
    help="Resource attributes in key=value format, separated by commas",
)
parser.add_argument(
    "--protocol", type=str, help="Desired OTLP protocol: grpc,http/protobuf"
)
parser.add_argument(
    "--traces-exporter",
    "-e",
    type=str,
    help="The traces exporter to use: otlp, console, file",
)
parser.add_argument(
    "--output-directory",
    "-o",
    type=str,
    help="Export traces to directory (only for file exporter)",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="count",
    default=0,
    dest="verbosity_level",
    help="Increase output verbosity (can be used multiple times)",
)

subparsers = parser.add_subparsers(dest="subcommand")
# Replay command
subparsers.add_parser("replay", help="Replay exported traces to an OTLP endpoint")

# Exec command
exec_parser = subparsers.add_parser("exec", help="Runs a command within a span")
exec_parser.add_argument("command", help="The command to run")


def main():
    args, other = parser.parse_known_args()

    configure_logging(args.verbosity_level)

    if args.service_name:
        settings.OTEL_SERVICE_NAME = args.service_name
    if args.resource_attributes:
        settings.OTEL_RESOURCE_ATTRIBUTES = settings.parse_key_val(
            args.resource_attributes
        )
    if args.protocol:
        settings.OTEL_EXPORTER_OTLP_PROTOCOL = args.protocol
    if args.traces_exporter:
        settings.OTEL_TRACES_EXPORTER = args.traces_exporter
    if args.output_directory:
        settings.OTEL_EXPORTER_FILE_DIRECTORY = args.output_directory
    if args.subcommand:
        configure_tracer()
        match args.subcommand:
            case "exec":
                if not args.command:
                    raise argparse.ArgumentError(None, "exec: No command provided")
                command = [args.command] + other
                exec_command(command, span_name=args.span_name)
            case "replay":
                replay(pathlib.Path(settings.OTEL_EXPORTER_FILE_DIRECTORY))
            case _:
                raise ValueError(f"Unknown subcommand: {args.subcommand}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
