#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    cli.py
    ~~~~~~~

    the main cli interface.

    :copyright: (c) 2015 by lord63.
    :license: MIT, see LICENSE for more details.
"""

from __future__ import absolute_import

import click

from getname import __version__
from getname.main import random_name


@click.group(context_settings={'help_option_names': ('-h', '--help')})
@click.version_option(__version__, '-v', '--version', message='%(version)s')
def cli():
    """Get popular cat/dog/superhero/supervillain names."""
    pass


@cli.command()
@click.option('--showall', is_flag=True,
              help='Top 100 cat names in alphabetical order.')
def cat(showall):
    """Get popular cat names."""
    click.echo(random_name('cat', showall=showall))


@cli.command()
@click.option('-f', '--female', is_flag=True,
              help='Show random female dog names.')
@click.option('-m', '--male', is_flag=True,
              help='Show random male dog names.')
@click.option('--showall', is_flag=True,
              help='All/all female/all male dog names sorted by popularity.')
def dog(female, male, showall):
    """Get popular dog names."""
    if female:
        click.echo(random_name('dog', 'female', showall=showall))
    elif male:
        click.echo(random_name('dog', 'male', showall=showall))
    else:
        click.echo(random_name('dog', showall=showall))


@cli.command()
@click.option('--showall', is_flag=True,
              help='All superhero names in alphabetical order.')
def superhero(showall):
    """Get superhero names."""
    click.echo(random_name('superhero', showall=showall))


@cli.command()
@click.option('--showall', is_flag=True,
              help='All supervillain names in alphabetical order.')
def supervillain(showall):
    """Get supervillain names."""
    click.echo(random_name('supervillain', showall=showall))
