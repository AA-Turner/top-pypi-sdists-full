from agilicus import context
from . import json


def output_if_console(ctx, output: str):
    if context.output_console(ctx):
        print(output)


def output_formatted(ctx, output):
    if context.output_json(ctx):
        json.output_json(ctx, output)
        return

    if context.output_console(ctx):
        print(output)
        return

    raise ValueError("unknown output format method")
