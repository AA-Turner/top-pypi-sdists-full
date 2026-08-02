import sys
from typing import Optional

# Use the compatibility library for Python < 3.10
if sys.version_info >= (3, 10):
    from importlib import resources
else:
    import importlib_resources as resources

from ..models import TypefaceLoadingInfo, TypefaceSource
from .. import utils
import skia

class TypefaceLoader:
    _typefaces_loading_info: list[TypefaceLoadingInfo] = []
    _font_manager: skia.FontMgr = None

    @staticmethod
    def load_default() -> skia.Typeface:
        font_path = resources.files("pictex.fonts").joinpath("InterVariable.ttf")
        tf = TypefaceLoader.load_from_file(str(font_path))
        if tf is None:
            raise RuntimeError("Failed to load default font (bundled Inter font)")
        return tf

    @staticmethod
    def load_from_file(filepath: str) -> Optional[skia.Typeface]:
        try:
            tf = skia.Typeface.MakeFromFile(filepath)
            return TypefaceLoader._save(tf, TypefaceSource.FILE, filepath)
        except:
            return None

    @staticmethod
    def load_system_font(family: str, style: skia.FontStyle = None) -> Optional[skia.Typeface]:
        """
            Creates a new reference to the typeface that most closely
            matches the requested familyName and fontStyle.
            It shouldn't return null if it's handled correctly.
            However, it can return null if an unhandled exception is thrown in Skia.
        """
        try:
            tf = skia.Typeface(family, style)
            return TypefaceLoader._save(tf, TypefaceSource.SYSTEM)
        except:
            return None

    @staticmethod
    def load_for_grapheme(grapheme: str, style: skia.FontStyle) -> Optional[skia.Typeface]:
        for cp in grapheme:
            system_typeface = TypefaceLoader.find_system_font_for_grapheme(style, ord(cp))
            if system_typeface and utils.is_grapheme_supported_for_typeface(grapheme, system_typeface):
                return TypefaceLoader._save(system_typeface, TypefaceSource.SYSTEM)
        
        return None

    @staticmethod
    def find_system_font_for_grapheme(style: skia.FontStyle, character: int) -> Optional[skia.Typeface]:
        try:
            return TypefaceLoader._get_font_manager().matchFamilyStyleCharacter(
                "",
                style,
                [],
                character
            )
        except:
            return None

    @staticmethod
    def clone_with_arguments(typeface: skia.Typeface, arguments: skia.FontArguments) -> skia.Typeface:
        typeface_loading_info = TypefaceLoader.get_typeface_loading_info(typeface)
        if not typeface_loading_info:
            raise RuntimeError("Impossible to clone typeface: it was not loaded")

        new_typeface = typeface.makeClone(arguments)
        typeface_loading_info.typeface = new_typeface
        return new_typeface
    
    @staticmethod
    def get_typeface_loading_info(typeface: skia.Typeface) -> Optional[TypefaceLoadingInfo]:
        for loading_info in TypefaceLoader._typefaces_loading_info:
            if loading_info.typeface == typeface:
                return loading_info
        return None

    @staticmethod
    def _save(typeface: Optional[skia.Typeface], source: TypefaceSource, filepath: Optional[str] = None) -> Optional[skia.Typeface]:
        if not typeface:
            return None
        
        TypefaceLoader._typefaces_loading_info.append(TypefaceLoadingInfo(typeface, source, filepath))
        return typeface

    @staticmethod
    def _get_font_manager() -> skia.FontMgr:
        if TypefaceLoader._font_manager is None:
            TypefaceLoader._font_manager = skia.FontMgr()
        return TypefaceLoader._font_manager
