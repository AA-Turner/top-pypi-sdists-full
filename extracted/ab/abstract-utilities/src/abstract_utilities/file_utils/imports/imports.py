# ============================================================
# abstract_utilities/imports/imports.py
# Global imports hub — everything imported here will be
# automatically available to any module that does:
#     from ..imports import *
# ============================================================


from ...imports import *
from pathlib import Path
from typing import *

from typing import *
from types import MethodType

from datetime import datetime

from typing import *
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from pdf2image import convert_from_path   # only used for OCR fallback
# ---- Core standard library modules -------------------------

from datetime import datetime
from types import ModuleType

# ---- Dataclasses and typing --------------------------------
from dataclasses import dataclass, field
from typing import (
    Any, Optional, List, Dict, Set, Tuple,
    Iterable, Callable, Literal, Union, TypeVar
)

# ---- Common 3rd-party dependencies --------------------------
from pdf2image import convert_from_path
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

# ---- Helpers ------------------------------------------------
from pprint import pprint

# ============================================================
# AUTO-EXPORT ALL NON-PRIVATE NAMES
# ============================================================
__all__ = [name for name in globals() if not name.startswith("_")]

