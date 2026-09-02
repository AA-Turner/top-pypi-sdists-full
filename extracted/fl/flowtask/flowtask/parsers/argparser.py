import sys
from argparse import ArgumentParser
import argparse
import orjson
from ..utils.parserqs import is_parseable, parse_arguments
from ..version import __version__


class ParseArgs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        kv = {}
        if not isinstance(values, (list,)):
            values = (values,)
        for value in values:
            n, v = value.split(":", 1)
            kv[n] = v
        setattr(namespace, self.dest, kv)


class ParseMask(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        kv = {}
        if not isinstance(values, (list,)):
            values = (values,)
        for value in values:
            n, v = value.split(":", 1)
            try:
                if newval := is_parseable(v):
                    val = newval(v)
                    if isinstance(val, list):
                        # recursive conversion of elements
                        new_val = []
                        for el in val:
                            if nval := is_parseable(el):
                                new_val.append(nval(el))
                            else:
                                new_val.append(el)
                        val = new_val
                else:
                    val = orjson.loads(v)
            except Exception as err:  # pylint: disable=W0718
                print(f"Error Parsing Mask: {err!s}")
                val = v
            kv[n] = val
        setattr(namespace, self.dest, kv)


class ParseParams(argparse._AppendAction):
    def __call__(self, parser, namespace, values, option_string=None):
        val = None
        for value in values:
            if newval := is_parseable(value):
                val = newval(value)
            else:
                try:
                    val = orjson.loads(value.encode("utf-8"))
                except ValueError:
                    val = value
        super(ParseParams, self).__call__(parser, namespace, val, option_string)


class ParseArguments(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        v = values.split(",")
        setattr(namespace, self.dest, v)


class ConfigParser(object):
    def __init__(self) -> None:
        self.options = None
        self.attributes: dict = {}
        self.stepattrs: dict = {}
        self.arguments: list = []
        self.parser = ArgumentParser(
            prog="FlowTask DataIntegration",
            usage="%(prog)s [options]",
            description="Run a Task, function (or Job) declared in flowtask.",
            epilog="Task Executor for Navigator: DataIntegrator",
            add_help=True,
            exit_on_error=True,
        )
        self.parser.add_argument(
            "-v", "--version", action="version", version=f"%(prog)s {__version__}"
        )
        self.parser.add_argument(
            "-d", "--debug", action="store_true", help="Enable Debug"
        )
        self.parser.add_argument(
            '--override-attributes',
            dest="override_attributes",
            action="store_true",
            help="Override the root-level attributes of all components"
        )
        self.parser.add_argument(
            "--no-worker",
            dest="no_worker",
            action="store_true",
            help="Avoid send Task to Worker",
        )
        self.parser.add_argument(
            "-q",
            "--queued",
            dest="queued",
            action="store_true",
            default=False,
            help="Put Task in Queue Worker",
        )
        self.parser.add_argument(
            "-r",
            "--run",
            dest="run",
            action="store_true",
            default=False,
            help=(
                "When dispatching to the QWorker, wait for the result "
                "(QClient.run) instead of the default fire-and-forget "
                "queue (QClient.queue)."
            ),
        )
        # ── Executor selection flags (FEAT-022) ───────────────────────────────
        self.parser.add_argument(
            "--executor",
            dest="executor",
            type=str,
            default=None,
            metavar="NAME",
            help=(
                "Executor backend to use for this task "
                "(local, qworker, publish, docker, k8s). "
                "Overrides task YAML executor and DEFAULT_EXECUTOR."
            ),
        )
        self.parser.add_argument(
            "--executor-image",
            dest="executor_image",
            type=str,
            default=None,
            metavar="IMAGE",
            help=(
                "Container image for docker/k8s executors. "
                "Overrides ExecutorConfig.image."
            ),
        )
        self.parser.add_argument(
            "--executor-namespace",
            dest="executor_namespace",
            type=str,
            default=None,
            metavar="NAMESPACE",
            help=(
                "Kubernetes namespace for k8s executor. "
                "Overrides ExecutorConfig.namespace."
            ),
        )
        # WIP: disable notifications
        self.parser.add_argument(
            "--no-notify",
            dest="no_notify",
            action="store_true",
            default=False,
            help="Disable Task Notification and Influx-events",
        )
        # disable custom events:
        self.parser.add_argument(
            "--no-events",
            dest="no_events",
            action="store_true",
            default=False,
            help="Avoid Trigger Custom Events on Tasks.",
        )
        self.parser.add_argument(
            "-p", "--program", help="Program (tenant) Name", type=str
        )
        self.parser.add_argument(
            "--storage",
            help="Task Storage",
            dest="storage",
            type=str,
            default="default",
        )
        self.parser.add_argument("-t", "--task", help="Task Name", type=str)
        self.parser.add_argument(
            "-f", "--function", help="Python Function Executable", type=str
        )
        self.parser.add_argument("-c", "--command", help="Path to Executable", type=str)
        self.parser.add_argument(
            "--ignore",
            action=ParseArguments,
            help="List of Components to be ignored in the execution",
            default=[],
        )
        self.parser.add_argument(
            "--run_only",
            action=ParseArguments,
            help="Only run this list of Components",
            default=[],
        )
        self.parser.add_argument(
            "--traceback",
            action="store_true",
            help="Return the Traceback on TaskError/Exception",
        )
        # parsing variables
        self.parser.add_argument(
            "--variables",
            action=ParseArgs,
            nargs="+",
            help="Passing Variables for dynamic replacement in a key:value format",
            default={},
            metavar="NAME1:VALUE NAME2:VALUE ...",
        )
        # masks replacement
        self.parser.add_argument(
            "--masks",
            action=ParseMask,
            nargs="+",
            help="Passing Mask values for dynamic replacement in a key:value format",
            default={},
            metavar="NAME1:VALUE NAME2:VALUE ...",
        )
        # attributes (component root attributes)
        self.parser.add_argument(
            "--attributes",
            action=ParseArgs,
            nargs="+",
            help="Override the root-level attributes of a component",
            default={},
            metavar="NAME1:VALUE NAME2:VALUE ...",
        )
        # passing arguments to component supporting
        self.parser.add_argument(
            "--args",
            action=ParseArgs,
            nargs="+",
            help="Passing Arguments in a key:value format",
            default={},
        )
        # conditions (component support)
        self.parser.add_argument(
            "--conditions",
            action=ParseArgs,
            nargs="+",
            help="Passing Conditions (for components support it) in a key:value format",
            default={},
            metavar="NAME1:VALUE NAME2:VALUE ...",
        )
        # parameters (usable to replace some values)
        self.parser.add_argument(
            "--parameters",
            action=ParseParams,
            nargs="+",
            help="Passing parseable parameters as lists, dicts or tuples.",
            default=[],
        )
        # arguments (are passed directly to a Task)
        self.parser.add_argument(
            "--arguments",
            action=ParseArguments,
            help="Command-line arguments for a Task (directly passed as kwargs)",
            default=[],
        )
        # ── Syntax check flags ───────────────────────────────────────────────
        # Added by FEAT-016.  These flags enable ``task --syntax`` mode which
        # short-circuits before TaskRunner and performs a static check.
        self.parser.add_argument(
            "-S", "--syntax",
            dest="syntax",
            action="store_true",
            default=False,
            help="Static syntax check (no execution). Reads file or stdin.",
        )
        self.parser.add_argument(
            "--strict",
            dest="syntax_strict",
            action="store_true",
            default=False,
            help="--syntax: treat undocumented components as errors.",
        )
        self.parser.add_argument(
            "--syntax-format",
            dest="syntax_format",
            choices=["text", "json"],
            default="text",
            help="--syntax: output format (default: text).",
        )
        # Path for ``task --syntax /path/to/file.yaml``.
        # Implemented as an optional flag (not a positional) to avoid
        # conflicts with the workers subparser positional argument.
        # Per spec §3 Module 7: "fall back to a --path/-P optional flag".
        self.parser.add_argument(
            "-P", "--syntax-path",
            dest="syntax_path",
            default=None,
            help="--syntax: path to task file, or '-' for stdin.",
        )
        # ── Worker Management subcommands ─────────────────────────────────────
        # Adds support for: flowtask workers queues
        # The subparser is declared on the top-level parser so that argparse
        # can recognise "workers" as the first positional argument.
        self._workers_subparsers = self.parser.add_subparsers(
            dest="workers_command",
            metavar="COMMAND",
            help="Worker management commands (use 'workers --help' for details)",
        )
        workers_parser = self._workers_subparsers.add_parser(
            "workers",
            help="Inspect and manage worker queues and tasks",
            description="Worker Management Commands — inspect QWorker processes and queues",
        )
        workers_action_subparsers = workers_parser.add_subparsers(
            dest="workers_action",
            metavar="ACTION",
            help="Worker action to perform",
        )
        _queues_parser = workers_action_subparsers.add_parser(
            "queues",
            help="Display a snapshot of queued tasks across all configured workers",
            description=(
                "Inspect all configured QWorker processes and print a table showing "
                "worker status, PID, and any queued tasks. "
                "Output is a point-in-time snapshot (approximate queue sizes)."
            ),
        )
        # Store reference so callers can extend or inspect it.
        self._queues_parser = _queues_parser

    def parse(self, arguments: list = None):
        args = []
        if arguments:
            args = arguments
        else:
            if len(sys.argv) > 1:
                args = sys.argv[1:]
        try:
            self.options, unknown = self.parser.parse_known_args(args)
            # TODO: accumulative sub-attributes for components
            # --Dummy_1 --Dummy_1 --Dummy_1
        except ValueError as err:
            raise ValueError(f"Invalid argument format: {err}") from err
        self.attributes, self.stepattrs = parse_arguments(unknown)
        try:
            self.attributes = {**self.attributes, **self.options.attributes}
        except (TypeError, ValueError):
            pass
        # list of unknown attributes
        self.arguments = unknown
