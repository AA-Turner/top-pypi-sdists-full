# ============================================================
# abstract_utilities/imports/imports.py
# Global imports hub — everything imported here will be
# automatically available to any module that does:
#     from ..imports import <names>
# ============================================================


from importlib import import_module as _import_module

imports = _import_module("...imports", __package__)

from ...imports import (
    re,
    shlex,
    os,
    json,
    tempfile,
    textwrap,
    glob,
    fnmatch,
    importlib,
    shutil,
    sys,
    posixpath,
    types,
    string,
    subprocess,
    pkgutil,
    inspect,
    Callable,
    Literal,
    Optional,
    Protocol,
    Tuple,
    Union,
    Iterable,
    Dict,
    List,
    Set,
    get_args,
    datetime,
    Path,
    ModuleType,
    dataclass,
    field,
    ezodf,
    gpd,
    PyPDF2,
    pdfplumber,
    pd,
    pytesseract,
    convert_from_path,
    load_dotenv,
    jsonify,
    secure_filename,
    FileStorage,
)

# ============================================================
# AUTO-EXPORT ALL NON-PRIVATE NAMES
# ============================================================
__all__ = [name for name in globals() if not name.startswith("_")]

