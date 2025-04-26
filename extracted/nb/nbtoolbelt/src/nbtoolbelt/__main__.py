"""
Main entry point

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

# Command line argument handling inspired by nbdime.
# Config file mechanism: see config.py

import sys

from ._version import __version__, package_name

COMMANDS = ("config", "validate", "head", "dump", "stats", "view", "cat", "clean", "run", "split", "punch",)

HELP_MESSAGE_VERBOSE = ("Usage: nbtb [OPTIONS]\n\n"
                        "OPTIONS: -h, --version, COMMAND{%s}\n\n"
                        "Examples: nbtb --version\n"
                        "          nbtb config run\n"
                        "          nbtb stats -h\n"
                        "          nbtb clean -o \n\n"
                        "Documentation: https://nbtoolbelt.readthedocs.io"
                        % ", ".join(COMMANDS)
                        )


def main_dispatch(args=None) -> int:
    """Main entry point.

    :param args: command-line arguments (list of strings)
    :return: exit code
    """
    if args is None:
        args = sys.argv[1:]
    if len(args) < 1:
        sys.exit("Option missing.\n\n{}".format(HELP_MESSAGE_VERBOSE))

    cmd = args[0]
    args = args[1:]

    if cmd == 'config':
        from .config import load_config
        if len(args) == 0:
            tool = package_name
        elif len(args) == 1:
            tool = 'nb' + args[0]
        else:
            sys.exit("Too many arguments.\n\n{}".format(HELP_MESSAGE_VERBOSE))
        _ = load_config(tool, verbose=True)
        sys.exit(0)

    # TODO there should be a better way than the following way of dispatching
    elif cmd == "base":  # for testing of the Tool base class
        from .toolbaseapp import main
    elif cmd == "head":
        from .nbheadapp import main
    elif cmd == "dump":
        from .nbdumpapp import main
    elif cmd == "validate":
        from .nbvalidateapp import main
    elif cmd == "view":
        from nbtoolbelt.nbviewapp import main
    elif cmd == "stats":
        from nbtoolbelt.nbstatsapp import main
    elif cmd == "cat":
        from nbtoolbelt.nbcatapp import main
    elif cmd == "clean":
        from nbtoolbelt.nbcleanapp import main
    elif cmd == "run":
        from nbtoolbelt.nbrunapp import main
    elif cmd == "split":
        from nbtoolbelt.nbsplitapp import main
    elif cmd == "punch":
        from nbtoolbelt.nbpunchapp import main
    else:
        if cmd == '--version':
            sys.exit(__version__)
        if cmd == '-h' or cmd == '--help':
            sys.exit(HELP_MESSAGE_VERBOSE)
        else:
            sys.exit("Unrecognized command '%s'\n\n%s" %
                     (cmd, HELP_MESSAGE_VERBOSE))

    # use the imported main for selected command
    exit_code = main(args)
    if exit_code:
        print("Tool '{}' aborted.".format(cmd), file=sys.stderr)

    return exit_code


if __name__ == "__main__":
    # This is triggered by "python -m nbtoolbelt <args>"
    sys.exit(main_dispatch())
