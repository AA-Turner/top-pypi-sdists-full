"""
Common processing definitions

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

from pathlib import Path
from typing import Sequence, Tuple

from nbformat import NotebookNode

# type alias for processing result
ProcessingResultType = Sequence[Tuple[NotebookNode, Path]]
