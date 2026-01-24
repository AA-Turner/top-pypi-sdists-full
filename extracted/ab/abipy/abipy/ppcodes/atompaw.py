# coding: utf-8
"""Pseudopotential Generators."""
from __future__ import annotations

#import abc
#import os
#import tempfile
#import collections
#import shutil
#import time

#from shutil import which
#from monty.termcolor import cprint
#from abipy.flowtk.pseudos import Pseudo
from abipy.ppcodes.base_parser import BaseParser

import logging
logger = logging.getLogger(__name__)


class AtompawParser(BaseParser):

    def scan(self, verbose: int = 0) -> AtompawParser:
        """
        Scan the output directory, set `run_completed` attribute.

        Raises: self.Error if invalid file.
        """
        try:
            self._scan(verbose=verbose)
        except Exception as exc:
            raise self.Error(f"Exception while parsing: {self.filepath}") from exc

    #def _select_by_prefix(self, prefix: str) -> list:
    #    return [p for p in self.all_filepaths if p.startswith(prefix)]

    def _scan(self, verbose: int=0) -> AtompawParser:
        if not os.path.exists(self.filepath):
            raise self.Error(f"File {self.filepath} does not exist")

        self.all_filepaths = os.listdir(self.workdir)

        # parse AE and PS wavefunctions.

        # aepsi.1


