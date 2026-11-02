from abstract_essentials import (
    combineList,
    compare_lists,
    ensure_nested_list,
    filter_json_list_values,
    find_original_case,
    get_actual_number,
    get_highest_value_obj,
    get_single_from_list,
    get_sort,
    get_symetric_difference,
    list_set,
    make_list,
    make_list_add,
    make_list_it,
    recursive_json_list,
    remove_from_list,
    safe_list_return,
)

from .functions import _LazyCallable, _lazy_module, _lazy_type

# Optional dependencies are resolved only when their features are used.
pexpect = _lazy_module("pexpect")
ezodf = _lazy_module("ezodf")
tiktoken = _lazy_module("tiktoken")
gpd = _lazy_module("geopandas")
PyPDF2 = _lazy_module("PyPDF2")
pdfplumber = _lazy_module("pdfplumber")
pd = _lazy_module("pandas")
pytesseract = _lazy_module("pytesseract")
convert_from_path = _LazyCallable("pdf2image", "convert_from_path")
FileStorage = _lazy_type("werkzeug.datastructures", "FileStorage")
