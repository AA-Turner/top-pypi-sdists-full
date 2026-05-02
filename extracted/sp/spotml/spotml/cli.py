#!/usr/bin/env python

import sys
import logging
import spotml
from spotml.parser import get_parser
from spotml.commands.writers.output_writrer import OutputWriter


def run_command(output: OutputWriter):
    parser = get_parser()
    args = sys.argv[1:]
    # display the version
    if '-V' in args:
        output.write(spotml.__version__)
        sys.exit(0)
    # separate Spotml arguments from custom arguments
    custom_args = []
    if '--' in args:
        dd_idx = args.index('--')
        custom_args = args[(dd_idx + 1):]
        args = args[:dd_idx]
    # parse arguments
    args = parser.parse_args(args)
    args.custom_args = custom_args
    # logging
    logging_level = logging.DEBUG if 'debug' in args and args.debug else logging.WARNING
    logging.basicConfig(level=logging_level, format='[%(levelname)s] %(message)s')
    if 'command' not in args:
        parser.print_help()
        sys.exit(1)
    args.command.run(args, output)


def main():
    try:
        output = OutputWriter()
        run_command(output)
    except Exception as e:
        output.write('Error:\n------\n%s' % str(e))
        sys.exit(1)


if __name__ == '__main__':
    main()
