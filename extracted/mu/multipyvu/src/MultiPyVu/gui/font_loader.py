"""
font_loader.py registers a bundled font file with the operating system so
that Tk can use it.

tkinter.font.Font(family=...) takes a font *family name*, not a path, and
Tk has no API for loading a font file.  A bundled font therefore has to be
handed to the platform's font system first, which is what this module does.
Registration has to happen before the Tk root window is created, because Tk
builds its list of available families as it starts up.

@author: djackson
"""


import ctypes
import logging
import os
import sys
from tkinter import font
from typing import List, Optional, Sequence

from ..project_vars import SERVER_NAME


# Used when the bundled font cannot be registered.  Naming these
# explicitly keeps the gui looking the same on Windows and macOS; falling
# through to Tk's own default would pick a different face on each.
FALLBACK_FAMILIES = ('Arial', 'Helvetica', 'DejaVu Sans')


def _logger() -> logging.Logger:
    return logging.getLogger(SERVER_NAME)


def _family_name_from_file(path: str) -> Optional[str]:
    """
    Read the family name out of the font file itself rather than assuming
    it matches the file name.

    Returns:
    --------
    The family name, or None if the file could not be parsed.
    """
    try:
        from PIL import ImageFont
        family, _style = ImageFont.truetype(path).getname()
    except Exception as e:
        _logger().debug(f'Could not read family name from {path}:  {e}')
        return None
    return family


def _register_windows(path: str) -> bool:
    """
    Add the font for this process only, using the GDI font API.
    """
    FR_PRIVATE = 0x10
    try:
        added = ctypes.windll.gdi32.AddFontResourceExW(
            ctypes.c_wchar_p(path), FR_PRIVATE, 0)
    except Exception as e:
        _logger().debug(f'AddFontResourceExW failed for {path}:  {e}')
        return False
    return added > 0


def _register_macos(path: str) -> bool:
    """
    Add the font for this process only, using CoreText.
    """
    frameworks = '/System/Library/Frameworks'
    try:
        cf = ctypes.cdll.LoadLibrary(
            f'{frameworks}/CoreFoundation.framework/CoreFoundation')
        ct = ctypes.cdll.LoadLibrary(
            f'{frameworks}/CoreText.framework/CoreText')
    except OSError as e:
        _logger().debug(f'Could not load CoreText:  {e}')
        return False

    kCFStringEncodingUTF8 = 0x08000100
    kCFURLPOSIXPathStyle = 0
    kCTFontManagerScopeProcess = 1

    cf.CFStringCreateWithCString.restype = ctypes.c_void_p
    cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p,
                                             ctypes.c_char_p,
                                             ctypes.c_uint32,
                                             ]
    cf.CFURLCreateWithFileSystemPath.restype = ctypes.c_void_p
    cf.CFURLCreateWithFileSystemPath.argtypes = [ctypes.c_void_p,
                                                 ctypes.c_void_p,
                                                 ctypes.c_int,
                                                 ctypes.c_bool,
                                                 ]
    cf.CFRelease.argtypes = [ctypes.c_void_p]
    ct.CTFontManagerRegisterFontsForURL.restype = ctypes.c_bool
    ct.CTFontManagerRegisterFontsForURL.argtypes = [ctypes.c_void_p,
                                                    ctypes.c_int,
                                                    ctypes.c_void_p,
                                                    ]

    cf_path = cf.CFStringCreateWithCString(None,
                                           path.encode('utf-8'),
                                           kCFStringEncodingUTF8,
                                           )
    if not cf_path:
        return False
    try:
        cf_url = cf.CFURLCreateWithFileSystemPath(None,
                                                  cf_path,
                                                  kCFURLPOSIXPathStyle,
                                                  False,
                                                  )
    finally:
        cf.CFRelease(cf_path)
    if not cf_url:
        return False
    try:
        return bool(ct.CTFontManagerRegisterFontsForURL(
            cf_url, kCTFontManagerScopeProcess, None))
    except Exception as e:
        _logger().debug(f'CTFontManagerRegisterFontsForURL failed:  {e}')
        return False
    finally:
        cf.CFRelease(cf_url)


def register_fonts(paths: Sequence[str]) -> Optional[str]:
    """
    Register font files with the OS so Tk can find them by family name.

    Must be called before the Tk root window is created.

    Parameters:
    -----------
    paths: Sequence[str]
        Absolute paths to the font files.  The family name is taken from
        the first one that registers successfully.

    Returns:
    --------
    The family name to ask Tk for, or None if nothing could be registered.
    """
    if sys.platform.startswith('win'):
        register = _register_windows
    elif sys.platform == 'darwin':
        register = _register_macos
    else:
        # On Linux a font has to be in the fontconfig search path, which
        # is not something this module should be changing.
        _logger().debug(f'No font registration support on {sys.platform}')
        return None

    family = None
    for path in paths:
        if not os.path.exists(path):
            _logger().debug(f'Font file not found:  {path}')
            continue
        if not register(path):
            continue
        if family is None:
            family = _family_name_from_file(path)
    return family


def resolve_family(preferred: Optional[str],
                   fallbacks: Sequence[str] = FALLBACK_FAMILIES,
                   ) -> str:
    """
    Pick the first font family Tk actually knows about.

    Requires the Tk root window to already exist, since Tk has to be
    running to report the available families.

    Parameters:
    -----------
    preferred: str or None
        The family to use if it is available, typically the return value
        of register_fonts().
    fallbacks: Sequence[str]
        Families to try, in order, if the preferred one is unavailable.

    Returns:
    --------
    A family name which Tk recognizes.  If none of the candidates are
    available, the first fallback is returned so that the caller still
    gets a consistent answer across platforms.
    """
    available = {name.lower(): name for name in font.families()}
    candidates: List[str] = []
    if preferred:
        candidates.append(preferred)
    candidates.extend(fallbacks)
    for candidate in candidates:
        match = available.get(candidate.lower())
        if match is not None:
            if preferred and match.lower() != preferred.lower():
                _logger().debug(f'Font "{preferred}" unavailable; '
                                f'falling back to "{match}"')
            return match
    _logger().debug(f'None of {candidates} are available; '
                    f'using "{fallbacks[0]}"')
    return fallbacks[0]
