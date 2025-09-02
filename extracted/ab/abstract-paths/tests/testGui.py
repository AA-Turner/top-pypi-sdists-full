#!/usr/bin/env python3
import os

from abstract_utilities.dynimport import call_for_all_tabs# = get_abstract_import(module='abstract_gui', symbol='get_for_all_tabs')
call_for_all_tabs()
from src.abstract_paths.finderConsole import (
    collectFilesTab, diffParserTab,directoryMapTab,
    extractImportsTab, finderTab,ConsoleBase,
    ContentFinderConsole)
from abstract_gui.QT6.startConsole import startConsole
startConsole(ContentFinderConsole)

