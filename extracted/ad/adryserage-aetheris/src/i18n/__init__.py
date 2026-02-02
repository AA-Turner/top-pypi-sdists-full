"""
Internationalization (i18n) module for Aetheris CLI.

Provides translation support with automatic locale detection and fallback to English.

Usage:
    from src.i18n import t, set_language, get_language, get_available_languages

    # Basic translation
    print(t("cli.analysis.start"))

    # With interpolation
    print(t("error.file_not_found", path="/some/file.py"))

    # Language control
    set_language("fr")
    print(get_available_languages())
"""

from src.i18n.locale_detector import LocaleDetector, detect_language
from src.i18n.translator import (
    LanguageInfo,
    Translator,
    get_available_languages,
    get_language,
    get_translator,
    set_language,
    t,
)

__all__ = [
    "Translator",
    "LanguageInfo",
    "LocaleDetector",
    "get_translator",
    "t",
    "set_language",
    "get_language",
    "get_available_languages",
    "detect_language",
]
