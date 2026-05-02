"""
spotilyzer init subcommand
"""

# system imports
import os
import shutil

# project imports
from .base import SubCommand
from .utils.paths import get_package_datadir, get_user_datadir, SEEDS_FILE

# constants
_DESCRIPTION = "initialize spotilyzer"


class Init(SubCommand):
    """
    init subcommand
    """

    name = 'init'

    @classmethod
    def add_parser(cls, subparsers):
        """
        Add init subcommand parser.
        :param subparsers: object to attach parser
        :return: None
        """
        subparsers.add_parser(cls.name, description=_DESCRIPTION,
                              help=_DESCRIPTION)

    @staticmethod
    def run():
        """
        Copy package seeds file so user can edit it.
        :return: None
        """
        spotilyzer_dir = get_user_datadir()
        os.makedirs(spotilyzer_dir, exist_ok=True)
        if not os.path.exists(os.path.join(spotilyzer_dir, SEEDS_FILE)):
            seeds_file = os.path.join(get_package_datadir(), SEEDS_FILE)
            shutil.copy(seeds_file, spotilyzer_dir)
