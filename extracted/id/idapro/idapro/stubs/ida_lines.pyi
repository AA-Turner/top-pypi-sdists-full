from typing import Any, Optional, List, Dict, Tuple, Callable, Union, Iterator, overload

r"""High level functions that deal with the generation of the disassembled text lines.

This file also contains definitions for the syntax highlighting.
Finally there are functions that deal with anterior/posterior user-defined lines.

"""

class export_listing_t:
    @property
    def current_place(self) -> place_t: ...
    @property
    def palette(self) -> listing_palette_t: ...
    @palette.setter
    def palette(self, value: listing_palette_t) -> None: ...
    @property
    def ranges(self) -> lines_gen_range_vec_t: ...
    @ranges.setter
    def ranges(self, value: lines_gen_range_vec_t) -> None: ...
    @property
    def style_block(self) -> str: ...
    @style_block.setter
    def style_block(self, value: str) -> None: ...
    @property
    def template_path(self) -> str: ...
    @template_path.setter
    def template_path(self, value: str) -> None: ...
    @property
    def title(self) -> str: ...
    @title.setter
    def title(self, value: str) -> None: ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def add_all_types(self) -> None:
        ...
    def add_decompilation(self, cfunc: Any) -> Any:
        r"""Append a decompilation: a snapshot of `cfunc`'s pseudocode, taken
        now (add_pseudocode copies the lines into the config) -- the export
        depends neither on the cfunc staying alive nor on its text staying
        unchanged (the decompiler cache may drop or regenerate it at any
        time). Returns False if the decompiler is not available.
        """
        ...
    def add_disasm_range(self, *args: Any) -> None:
        ...
    def add_function(self, ea: ida_idaapi.ea_t, expand: bool = False) -> bool:
        ...
    def add_item(self, ea: ida_idaapi.ea_t, expand: bool = False) -> bool:
        ...
    def add_pseudocode(self, lines: strvec_t, ea: ida_idaapi.ea_t) -> bool:
        ...
    def add_type(self, ordinal: int) -> bool:
        ...
    def add_whole_disassembly(self, expand: bool = False) -> None:
        ...
    def clear_ranges(self) -> None:
        ...
    def create_lines(self, flags: int, range_index: int) -> listing_lines_t:
        r"""The streaming engine: a generator over the range `range_index`, rendering per `flags` (listing_format_t | LLF_LINKS) - the consumer loops over the ranges itself, so it always knows which region it is rendering. The document is the config: in-document links may target any of its ranges, and the generators of one generation pass share the document's navigation state (a name anchors once per document), so create them in range order - a non-monotonic index starts a new pass. The caller owns the result and must delete it; the config is borrowed and must outlive it. 
                
        :returns: nullptr for an out-of-range index.
        """
        ...
    def ensure_scope(self, current: bool, expand: bool = False) -> bool:
        ...

class link_anchor_t:
    @property
    def flags(self) -> int: ...
    @flags.setter
    def flags(self, value: int) -> None: ...
    @property
    def identifier(self) -> str: ...
    @identifier.setter
    def identifier(self, value: str) -> None: ...
    def __eq__(self, r: link_anchor_t) -> bool:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __ne__(self, r: link_anchor_t) -> bool:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...

class link_anchors_t:
    def __eq__(self, r: link_anchors_t) -> bool:
        ...
    def __getitem__(self, i: int) -> link_anchor_t:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __iter__(self) -> Iterator[link_anchor_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, r: link_anchors_t) -> bool:
        ...
    def __repr__(self) -> Any:
        ...
    def __setitem__(self, i: int, v: link_anchor_t) -> None:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def add_unique(self, x: link_anchor_t) -> bool:
        ...
    def append(self, x: link_anchor_t) -> None:
        ...
    def at(self, _idx: int) -> link_anchor_t:
        ...
    def back(self) -> Any:
        ...
    def begin(self, *args: Any) -> qvector:
        ...
    def capacity(self) -> int:
        ...
    def clear(self) -> None:
        ...
    def empty(self) -> bool:
        ...
    def end(self, *args: Any) -> qvector:
        ...
    def erase(self, *args: Any) -> qvector:
        ...
    def extend(self, x: link_anchors_t) -> None:
        ...
    def extract(self) -> link_anchor_t:
        ...
    def find(self, *args: Any) -> qvector:
        ...
    def front(self) -> Any:
        ...
    def grow(self, *args: Any) -> None:
        ...
    def has(self, x: link_anchor_t) -> bool:
        ...
    def inject(self, s: link_anchor_t, len: int) -> None:
        ...
    def insert(self, it: link_anchor_t, x: link_anchor_t) -> qvector:
        ...
    def pop_back(self) -> None:
        ...
    def push_back(self, *args: Any) -> link_anchor_t:
        ...
    def qclear(self) -> None:
        ...
    def reserve(self, cnt: int) -> None:
        ...
    def resize(self, *args: Any) -> None:
        ...
    def size(self) -> int:
        ...
    def swap(self, r: link_anchors_t) -> None:
        ...
    def truncate(self) -> None:
        ...

class listing_line_t:
    @property
    def anchors(self) -> link_anchors_t: ...
    @anchors.setter
    def anchors(self, value: link_anchors_t) -> None: ...
    @property
    def bg_color(self) -> int: ...
    @bg_color.setter
    def bg_color(self, value: int) -> None: ...
    @property
    def place(self) -> place_t: ...
    @place.setter
    def place(self, value: place_t) -> None: ...
    @property
    def prefix_color(self) -> color_t: ...
    @prefix_color.setter
    def prefix_color(self, value: color_t) -> None: ...
    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...

class listing_lines_t:
    @property
    def cancelled(self) -> bool: ...
    @property
    def flags(self) -> int: ...
    @property
    def title(self) -> str: ...
    def __init__(self, *args: Any, **kwargs: Any) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def emit_links(self) -> bool:
        r"""HTML: emit in-document anchors/links (LLF_LINKS).
        
        """
        ...
    def format(self) -> listing_format_t:
        r"""The listing text encoding (the low 8 bits of flags).
        
        """
        ...
    def get_style_block(self) -> Union[str, None]:
        r"""The CSS style block for LLFMT_HTML_CLASSES (empty otherwise). 
                
        :returns: false if there is nothing to emit.
        """
        ...
    def next(self) -> listing_line_t:
        r"""The next line, or `nullptr` at end. WARNING: the returned instance is a BORROW owned by the stream and valid ONLY until the next next() call (which overwrites it) or until the stream is destroyed. Do not store the pointer or any part of it (text, place, ...); copy what you need before calling next() again. 
                
        """
        ...
    def place_to_identifier(self, place: place_t) -> Union[str, None]:
        r"""The anchor identifier of the definition rendered at `place` (populated lazily as lines are produced); false if none. For a function sidebar etc. 
                
        """
        ...
    def was_cancelled(self) -> bool:
        r"""Whether the stream stopped early because the user cancelled: next() then returns `nullptr` as at end. The stream polls the wait box's Cancel as it produces lines, so a consumer (e.g. an HTML-export template) need not poll. 
                
        """
        ...

class listing_palette_entries_array:
    @property
    def bytes(self) -> Any: ...
    @bytes.setter
    def bytes(self, value: Any) -> None: ...
    @property
    def data(self) -> Any: ...
    def __getitem__(self, i: int) -> listing_palette_entry_t:
        ...
    def __init__(self, data: Any) -> Any:
        ...
    def __iter__(self) -> Iterator[listing_palette_entry_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __len__(self) -> int:
        ...
    def __repr__(self) -> Any:
        ...
    def __setitem__(self, i: int, v: listing_palette_entry_t) -> None:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...

class listing_palette_entry_t:
    @property
    def css(self) -> str: ...
    @css.setter
    def css(self, value: str) -> None: ...
    @property
    def rgb(self) -> int: ...
    @rgb.setter
    def rgb(self, value: int) -> None: ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...

class listing_palette_t:
    @property
    def fg(self) -> Any: ...
    @property
    def inited(self) -> bool: ...
    @inited.setter
    def inited(self, value: bool) -> None: ...
    @property
    def pfx(self) -> Any: ...
    def __get_fg__(self) -> wrapped_array_t:
        ...
    def __get_pfx__(self) -> wrapped_array_t:
        ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def resolve_tag_color(self, tag: color_t) -> int:
        r""":returns: the tag's text color, or DEFCOLOR to inherit."""
        ...
    def resolve_tag_color_class(self, tag: color_t) -> Union[str, None]:
        r""":returns: true and set `out` to the tag's text CSS class, else false (inline)."""
        ...
    def resolve_tag_prefix(self, tag: color_t) -> int:
        r""":returns: the tag's line-prefix (gutter) color, or DEFCOLOR to inherit."""
        ...
    def resolve_tag_prefix_class(self, tag: color_t) -> Union[str, None]:
        r""":returns: true and set `out` to the tag's line-prefix CSS class, else false."""
        ...

class sourcefile_info_t:
    @property
    def filename(self) -> str: ...
    @filename.setter
    def filename(self, value: str) -> None: ...
    @property
    def range(self) -> range_t: ...
    @range.setter
    def range(self, value: range_t) -> None: ...
    def __init__(self) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...

class sourcefile_t:
    @property
    def end_ea(self) -> ida_idaapi.ea_t: ...
    @end_ea.setter
    def end_ea(self, value: ida_idaapi.ea_t) -> None: ...
    @property
    def filename(self) -> str: ...
    @filename.setter
    def filename(self, value: str) -> None: ...
    @property
    def start_ea(self) -> ida_idaapi.ea_t: ...
    @start_ea.setter
    def start_ea(self, value: ida_idaapi.ea_t) -> None: ...
    def __eq__(self, r: range_t) -> bool:
        ...
    def __ge__(self, r: range_t) -> bool:
        ...
    def __gt__(self, r: range_t) -> bool:
        ...
    def __init__(self) -> Any:
        ...
    def __le__(self, r: range_t) -> bool:
        ...
    def __lt__(self, r: range_t) -> bool:
        ...
    def __ne__(self, r: range_t) -> bool:
        ...
    def __repr__(self) -> Any:
        ...
    def __str__(self) -> str:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def clear(self) -> None:
        r"""Set start_ea, end_ea to 0.
        
        """
        ...
    def compare(self, r: range_t) -> int:
        ...
    @overload
    def contains(self, ea: ida_idaapi.ea_t) -> bool:
        r"""Compare two range_t instances, based on the start_ea.
        
        Is 'ea' in the address range?
        """
        ...
    @overload
    def contains(self, r: range_t) -> bool:
        r"""Is every ea in 'r' also in this range_t?"""
        ...
    def empty(self) -> bool:
        r"""Is the size of the range_t <= 0?
        
        """
        ...
    def extend(self, ea: ida_idaapi.ea_t) -> None:
        r"""Ensure that the range_t includes 'ea'.
        
        """
        ...
    def intersect(self, r: range_t) -> None:
        r"""Assign the range_t to the intersection between the range_t and 'r'.
        
        """
        ...
    def overlaps(self, r: range_t) -> bool:
        r"""Is there an ea in 'r' that is also in this range_t?
        
        """
        ...
    def size(self) -> int:
        r"""Get end_ea - start_ea.
        
        """
        ...

class sourcefilevec_t:
    def __eq__(self, r: sourcefilevec_t) -> bool:
        ...
    def __getitem__(self, i: int) -> sourcefile_t:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __iter__(self) -> Iterator[sourcefile_t]:
        r"""Helper function, to be set as __iter__ method for qvector-, or array-based classes."""
        ...
    def __len__(self) -> int:
        ...
    def __ne__(self, r: sourcefilevec_t) -> bool:
        ...
    def __repr__(self) -> Any:
        ...
    def __setitem__(self, i: int, v: sourcefile_t) -> None:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def add_unique(self, x: sourcefile_t) -> bool:
        ...
    def append(self, x: sourcefile_t) -> None:
        ...
    def at(self, _idx: int) -> sourcefile_t:
        ...
    def back(self) -> Any:
        ...
    def begin(self, *args: Any) -> qvector:
        ...
    def capacity(self) -> int:
        ...
    def clear(self) -> None:
        ...
    def empty(self) -> bool:
        ...
    def end(self, *args: Any) -> qvector:
        ...
    def erase(self, *args: Any) -> qvector:
        ...
    def extend(self, x: sourcefilevec_t) -> None:
        ...
    def extract(self) -> sourcefile_t:
        ...
    def find(self, *args: Any) -> qvector:
        ...
    def front(self) -> Any:
        ...
    def grow(self, *args: Any) -> None:
        ...
    def has(self, x: sourcefile_t) -> bool:
        ...
    def inject(self, s: sourcefile_t, len: int) -> None:
        ...
    def insert(self, it: sourcefile_t, x: sourcefile_t) -> qvector:
        ...
    def pop_back(self) -> None:
        ...
    def push_back(self, *args: Any) -> sourcefile_t:
        ...
    def qclear(self) -> None:
        ...
    def reserve(self, cnt: int) -> None:
        ...
    def resize(self, *args: Any) -> None:
        ...
    def size(self) -> int:
        ...
    def swap(self, r: sourcefilevec_t) -> None:
        ...
    def truncate(self) -> None:
        ...

class user_defined_prefix_t:
    def __disown__(self) -> Any:
        ...
    def __init__(self, *args: Any) -> Any:
        ...
    def __repr__(self) -> Any:
        ...
    def __swig_destroy__(self, object: Any) -> Any:
        ...
    def get_user_defined_prefix(self, ea: ida_idaapi.ea_t, insn: insn_t, lnnum: int, indent: int, line: str) -> str:
        r"""This callback must be overridden by the derived class. 
                
        :param ea: the current address
        :param insn: the current instruction. if the current item is not an instruction, then insn.itype is zero.
        :param lnnum: number of the current line (each address may have several listing lines for it). 0 means the very first line for the current address.
        :param indent: see explanations for gen_printf()
        :param line: the line to be generated. the line usually contains color tags. this argument can be examined to decide whether to generate the prefix.
        """
        ...

def COLSTR(str: Any, tag: Any) -> Any:
    r"""
    Utility function to create a colored line
    :param str: The string
    :param tag: Color tag constant. One of SCOLOR_XXXX
    
    """
    ...

def add_extra_cmt(*args: Any) -> bool:
    ...

def add_extra_line(*args: Any) -> bool:
    ...

def add_pgm_cmt(*args: Any) -> bool:
    ...

def add_sourcefile(ea1: ida_idaapi.ea_t, ea2: ida_idaapi.ea_t, filename: str) -> bool:
    ...

def add_sourcefiles(items: sourcefilevec_t) -> bool:
    ...

def calc_bg_color(ea: ida_idaapi.ea_t) -> int:
    r"""Get background color for line at 'ea' 
            
    :returns: RGB color
    """
    ...

def calc_prefix_color(ea: ida_idaapi.ea_t) -> color_t:
    r"""Get prefix color for line at 'ea' 
            
    :returns: Line prefix colors
    """
    ...

def create_encoding_helper(*args: Any) -> encoder_t:
    ...

def del_extra_cmt(ea: ida_idaapi.ea_t, what: int) -> bool:
    ...

def del_sourcefile(ea: ida_idaapi.ea_t) -> bool:
    ...

def delete_extra_cmts(ea: ida_idaapi.ea_t, what: int) -> None:
    ...

def export_listing_t__from_ptrval__(ptrval: int) -> export_listing_t:
    ...

def export_listing_to_file(*args: Any) -> Any:
    r"""Whole-output producer: write a complete HTML document to `path`. When export_listing_t::template_path is set, that .py template's `run(path, cfg)` takes over (receiving `cfg`, borrowed) and builds its own generator(s); otherwise the built-in css-class document is emitted. 
            
    :returns: false with `errbuf` set on failure; `out_lines` (optional) receives the built-in document's line count.
    """
    ...

def export_listing_to_string(cfg: export_listing_t, flags: int) -> Union[str, None]:
    r"""Whole-output producer: every range's lines joined into one string (no trailing newline), rendered per `flags`. 
            
    """
    ...

def generate_disasm_line(ea: ida_idaapi.ea_t, flags: int = 0) -> str:
    ...

def generate_disassembly(ea: Any, max_lines: Any, as_stack: Any, notag: Any, include_hidden: Boolean = False) -> Any:
    r"""Generate disassembly lines (many lines) and put them into a buffer
    
    :param ea: address to generate disassembly for
    :param max_lines: how many lines max to generate
    :param as_stack: Display undefined items as 2/4/8 bytes
    :param notag: remove color tags
    :param include_hidden: automatically unhide hidden objects
    :returns: tuple(most_important_line_number, list(lines)) : Returns a tuple containing
              the most important line number and a list of generated lines
    :returns: None on failure
    """
    ...

def get_extra_cmt(ea: ida_idaapi.ea_t, what: int) -> int:
    ...

def get_first_free_extra_cmtidx(ea: ida_idaapi.ea_t, start: int) -> int:
    ...

def get_sourcefile(ea: ida_idaapi.ea_t, bounds: range_t = None) -> str:
    ...

def get_sourcefile_by_ea(ea: ida_idaapi.ea_t, bounds: range_t = None) -> str:
    ...

def get_sourcefiles_qty() -> int:
    ...

def getn_sourcefile(out: sourcefile_info_t, n: int) -> bool:
    ...

def install_user_defined_prefix(*args: Any) -> bool:
    ...

def listing_lines_t__from_ptrval__(ptrval: int) -> listing_lines_t:
    ...

def requires_color_esc(c: Any) -> Any:
    r"""Is the given char a color escape character?
    
    """
    ...

def tag_addr(ea: ida_idaapi.ea_t) -> str:
    r"""Insert an address mark into a string. 
            
    :param ea: address to include
    """
    ...

def tag_advance(line: str, cnt: int) -> int:
    r"""Move pointer to a 'line' to 'cnt' positions right. Take into account escape sequences. 
            
    :param line: pointer to string
    :param cnt: number of positions to move right
    :returns: moved pointer
    """
    ...

def tag_get_addr(line: str) -> ida_idaapi.ea_t:
    r"""Decode an address from an address mark. 
            
    :param line: points to sequence: COLOR_ON COLOR_ADDR ADDRESS
    :returns: the decoded address, or BADADDR on malformed input
    """
    ...

def tag_get_semspan_kind(at: str, payload: idc_value_t = None) -> color_t:
    r"""Decode the semantic kind of a COLOR_SEMSPAN span, and what it bundles. 
            
    :param at: points to the span header: COLOR_ON COLOR_SEMSPAN <kind> [<payload>]
    :param payload: if non-nullptr, receives the payload, decoded according to the returned kind. Cleared first, and left cleared for a kind that bundles nothing - which is every kind so far. Only ever VT_LONG, VT_INT64 or VT_STR. Pass nullptr if only the kind is wanted.
    :returns: the kind (a Color string constants code), or 0 on malformed input
    """
    ...

def tag_remove(nonnul_instr: str) -> str:
    r"""Remove color escape sequences from a string. 
            
    :returns: length of resulting string, -1 if error
    """
    ...

def tag_semspan(kind: color_t = 1) -> str:
    r"""Open a COLOR_SEMSPAN span with the given semantic kind. Appends the span header: COLOR_ON COLOR_SEMSPAN <kind>. Close the span with tag_semspan_off(). 
            
    :param kind: a Color string constants color code describing the span (e.g. COLOR_CNAME for a symbol name); COLOR_DEFAULT = no specific kind. Must not be 0.
    """
    ...

def tag_semspan_off() -> str:
    r"""Close a COLOR_SEMSPAN span opened with tag_semspan(). Appends COLOR_OFF COLOR_SEMSPAN (the closing side carries no header). 
            
    """
    ...

def tag_skipcode(line: str) -> int:
    r"""Skip one color code, including any payload it carries: this is the right way to step over an entire COLOR_ADDR or COLOR_SEMSPAN header - whose size is not something a caller may assume - starting from its COLOR_ON byte. This function should be used if you are interested in color codes and want to analyze all of them. Otherwise tag_skipcodes() function is better since it will skip all colors at once. This function will skip the current color code if there is one. If the current symbol is not a color code, it will return the input. 
            
    :returns: moved pointer
    """
    ...

def tag_skipcodes(line: str) -> int:
    r"""Move the pointer past all color codes. 
            
    :param line: can't be nullptr
    :returns: moved pointer, can't be nullptr
    """
    ...

def tag_strlen(line: str) -> int:
    r"""Calculate length of a colored string This function computes the length in unicode codepoints of a line 
            
    :returns: the number of codepoints in the line, or -1 on error
    """
    ...

def update_extra_cmt(ea: ida_idaapi.ea_t, what: int, str: str) -> bool:
    ...

COLOR_ADDR: int  # 40
COLOR_ADDR_EXPR: int  # 53
COLOR_ADDR_SIZE: int  # 16
COLOR_ALTOP: int  # 22
COLOR_ARGLOC: int  # 16
COLOR_ARGNAME: int  # 33
COLOR_ASMDIR: int  # 27
COLOR_ATTR: int  # 23
COLOR_AUTOCMT: int  # 4
COLOR_BG_MAX: int  # 13
COLOR_BINPREF: int  # 20
COLOR_CHAR: int  # 10
COLOR_CMT: int  # 12
COLOR_CNAME: int  # 37
COLOR_CODE: int  # 5
COLOR_CODNAME: int  # 26
COLOR_COLLAPSED: int  # 39
COLOR_CREF: int  # 14
COLOR_CREFTAIL: int  # 16
COLOR_CURITEM: int  # 9
COLOR_CURLINE: int  # 10
COLOR_DATA: int  # 6
COLOR_DATNAME: int  # 6
COLOR_DCHAR: int  # 30
COLOR_DEFAULT: int  # 1
COLOR_DEMNAME: int  # 8
COLOR_DNAME: int  # 7
COLOR_DNUM: int  # 31
COLOR_DREF: int  # 15
COLOR_DREFTAIL: int  # 17
COLOR_DSTR: int  # 29
COLOR_ERROR: int  # 18
COLOR_ESC: str  # 
COLOR_EXTERN: int  # 8
COLOR_EXTRA: int  # 21
COLOR_FG_MAX: int  # 40
COLOR_GROUP: int  # 54
COLOR_HIDLINE: int  # 11
COLOR_HIDNAME: int  # 23
COLOR_IMPNAME: int  # 34
COLOR_INSN: int  # 5
COLOR_INV: str  # 
COLOR_KEYWORD: int  # 32
COLOR_LIBFUNC: int  # 3
COLOR_LIBNAME: int  # 24
COLOR_LOCNAME: int  # 25
COLOR_LUMFUNC: int  # 12
COLOR_LUMINA: int  # 52
COLOR_MACRO: int  # 28
COLOR_NAME: int  # 37
COLOR_NUMBER: int  # 12
COLOR_OFF: str  # 
COLOR_ON: str  # 
COLOR_OPND1: int  # 41
COLOR_OPND2: int  # 42
COLOR_OPND3: int  # 43
COLOR_OPND4: int  # 44
COLOR_OPND5: int  # 45
COLOR_OPND6: int  # 46
COLOR_OPND7: int  # 47
COLOR_OPND8: int  # 48
COLOR_PRAGMA: int  # 28
COLOR_PREFIX: int  # 19
COLOR_REG: int  # 33
COLOR_REGCMT: int  # 2
COLOR_REGFUNC: int  # 4
COLOR_RESERVED1: int  # 51
COLOR_RPTCMT: int  # 3
COLOR_SEGNAME: int  # 35
COLOR_SELECTED: int  # 2
COLOR_SEMSPAN: int  # 54
COLOR_STRING: int  # 11
COLOR_SYMBOL: int  # 9
COLOR_TNUM: int  # 24
COLOR_TYPE: int  # 23
COLOR_UNAME: int  # 38
COLOR_UNKNAME: int  # 36
COLOR_UNKNOWN: int  # 7
COLOR_VOIDOP: int  # 13
E_NEXT: int  # 2000
E_PREV: int  # 1000
GDISMF_ADDR_TAG: int  # 2
GDISMF_AS_STACK: int  # 1
GDISMF_REMOVE_TAGS: int  # 4
GDISMF_UNHIDE: int  # 8
GENDSM_FORCE_CODE: int  # 1
GENDSM_MULTI_LINE: int  # 2
GENDSM_REMOVE_TAGS: int  # 4
GENDSM_UNHIDE: int  # 8
LAF_INCOMING: int  # 1
LAF_OUTGOING: int  # 2
LAF_XREF: int  # 4
LLFMT_HTML_CLASSES: int  # 3
LLFMT_HTML_INLINE: int  # 2
LLFMT_PLAIN: int  # 1
LLFMT_TAGGED: int  # 0
LLF_FORMAT_MASK: int  # 255
LLF_LINKS: int  # 256
PALETTE_SIZE: int  # 53
SCOLOR_ADDR: str  # (
SCOLOR_ADDR_EXPR: str  # 5
SCOLOR_ALTOP: str  # 
SCOLOR_ARGLOC: str  # 
SCOLOR_ARGNAME: str  # !
SCOLOR_ASMDIR: str  # 
SCOLOR_ATTR: str  # 
SCOLOR_AUTOCMT: str  # 
SCOLOR_BINPREF: str  # 
SCOLOR_CHAR: str  # 

SCOLOR_CMT: str  # 
SCOLOR_CNAME: str  # %
SCOLOR_CODNAME: str  # 
SCOLOR_COLLAPSED: str  # '
SCOLOR_CREF: str  # 
SCOLOR_CREFTAIL: str  # 
SCOLOR_DATNAME: str  # 
SCOLOR_DCHAR: str  # 
SCOLOR_DEFAULT: str  # 
SCOLOR_DEMNAME: str  # 
SCOLOR_DNAME: str  # 
SCOLOR_DNUM: str  # 
SCOLOR_DREF: str  # 
SCOLOR_DREFTAIL: str  # 
SCOLOR_DSTR: str  # 
SCOLOR_ERROR: str  # 
SCOLOR_ESC: str  # 
SCOLOR_EXTRA: str  # 
SCOLOR_FG_MAX: str  # (
SCOLOR_HIDNAME: str  # 
SCOLOR_IMPNAME: str  # "
SCOLOR_INSN: str  # 
SCOLOR_INV: str  # 
SCOLOR_KEYWORD: str  #  
SCOLOR_LIBNAME: str  # 
SCOLOR_LOCNAME: str  # 
SCOLOR_LUMINA: str  # 4
SCOLOR_MACRO: str  # 
SCOLOR_NAME: str  # %
SCOLOR_NUMBER: str  # 
SCOLOR_OFF: str  # 
SCOLOR_ON: str  # 
SCOLOR_OPND1: str  # )
SCOLOR_OPND2: str  # *
SCOLOR_OPND3: str  # +
SCOLOR_OPND4: str  # ,
SCOLOR_OPND5: str  # -
SCOLOR_OPND6: str  # .
SCOLOR_OPND7: str  # /
SCOLOR_OPND8: str  # 0
SCOLOR_PRAGMA: str  # 
SCOLOR_PREFIX: str  # 
SCOLOR_REG: str  # !
SCOLOR_REGCMT: str  # 
SCOLOR_RESERVED1: str  # 3
SCOLOR_RPTCMT: str  # 
SCOLOR_SEGNAME: str  # #
SCOLOR_SEMSPAN: str  # 6
SCOLOR_STRING: str  # 
SCOLOR_SYMBOL: str  # 	
SCOLOR_TNUM: str  # 
SCOLOR_TYPE: str  # 
SCOLOR_UNAME: str  # &
SCOLOR_UNKNAME: str  # $
SCOLOR_UTF8: str  # 2
SCOLOR_VOIDOP: str  # 
SWIG_PYTHON_LEGACY_BOOL: int  # 1
VEL_CMT: int  # 2
VEL_POST: int  # 1
annotations: _Feature  # _Feature((3, 7, 0, 'beta', 1), None, 16777216)
cvar: swigvarlink
ida_idaapi: module
ida_range: module
weakref: module