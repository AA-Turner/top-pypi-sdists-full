######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37                                                                                #
# Generated on 2026-08-11T17:17:32.748081                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow._vendor.click.core

from .._vendor import click as click

class LazyPluginCommandCollection(metaflow._vendor.click.core.CommandCollection, metaclass=type):
    def __init__(self, *args, lazy_sources = None, **kwargs):
        ...
    def invoke(self, ctx):
        ...
    def list_commands(self, ctx):
        ...
    def get_command(self, ctx, cmd_name):
        ...
    ...

class LazyGroup(metaflow._vendor.click.core.Group, metaclass=type):
    def __init__(self, *args, lazy_subcommands = None, **kwargs):
        ...
    def list_commands(self, ctx):
        ...
    def get_command(self, ctx, cmd_name):
        ...
    ...

