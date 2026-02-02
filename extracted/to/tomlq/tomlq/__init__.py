# -*- coding: utf-8 -*-

"""Top-level package for tomlq."""

__author__ = """Max Dymond"""
__email__ = 'cmeister2@gmail.com'
__version__ = '0.1.0'


import yq


def main():
    """Call through to the tq_cli() command that exists in yq."""
    yq.tq_cli()
