# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Module to create an a2l file from a conversion table file."""

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional


PARSER_HELP = "Create a2l file from conversion_table.json file."


def get_vtab_text(vtab):
    """Convert vtab dict to a2l text."""

    vtab_text = (
        '    /begin COMPU_VTAB\n'
        f'        CONV_TAB_{vtab["name"]}             /* Name */\n'
        '        "Conversion table"          /* LongIdentifier */\n'
        '        TAB_VERB            /* ConversionType */\n'
        f'        {len(vtab["disp_values"])}          /* NumberValuePairs */\n'
    )

    vtab_text += ''.join(
        f'        {vtab["start_value"]+i}          /* InVal */\n'
        f'        "{value}"          /* OutVal */\n'
        for i, value in enumerate(vtab['disp_values'])
    )

    vtab_text += '    /end COMPU_VTAB\n\n'

    return vtab_text


def create_conversion_table(input_json: Path, output_a2l: Path):
    """Create a2l conversion table for custom units."""
    with open(input_json.resolve(), encoding="utf-8") as f_h:
        conversion_table = json.load(f_h)

    with open(output_a2l.resolve(), 'w', encoding="utf-8") as f_h:
        for vtab in conversion_table:
            f_h.write(get_vtab_text(vtab))


def create_conversion_table_cli(args: argparse.Namespace):
    """CLI wrapper function for passing in Namespace object.

    This allows maintaining a standardized CLI function signature while not breaking backwards
    compatibility with create_converstion_table.
    """
    create_conversion_table(args.input_file, args.output_file)


def configure_parser(parser: argparse.ArgumentParser):
    """Set up parser for CLI."""
    parser.add_argument('input_file', type=Path)
    parser.add_argument('output_file', type=Path)
    parser.set_defaults(func=create_conversion_table_cli)


def main(argv: Optional[List[str]] = None):
    """Main function for CLI."""
    parser = argparse.ArgumentParser(description=PARSER_HELP)
    configure_parser(parser)
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == '__main__':
    main(sys.argv[1:])
