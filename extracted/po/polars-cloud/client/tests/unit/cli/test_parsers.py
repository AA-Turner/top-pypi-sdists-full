import argparse

from polars_cloud.cli.parsers import create_parser


def test_create_parser() -> None:
    parser = create_parser()
    assert isinstance(parser, argparse.ArgumentParser)
