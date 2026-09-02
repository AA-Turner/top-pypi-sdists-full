from __future__ import annotations

import os
import sys
from pathlib import Path

THISDIR = Path(__file__).resolve().parent
sys.path.insert(0, os.path.dirname(THISDIR))

from gimpformats.native_convert import convert_xcf_to_flat_image

FILES = THISDIR.parent / "test_files"


convert_xcf_to_flat_image(
	xcf_path=(FILES / "64x64.xcf").as_posix(), output_path="exclude_64x64.png"
)
convert_xcf_to_flat_image(
	xcf_path=(FILES / "base24.xcf").as_posix(), output_path="exclude_base24.png"
)
