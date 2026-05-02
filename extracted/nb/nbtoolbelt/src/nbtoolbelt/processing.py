"""
Common processing definitions

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from pathlib import Path
from collections.abc import Sequence

from nbformat import NotebookNode

# type alias for processing result
ProcessingResultType = Sequence[tuple[NotebookNode, Path]]
