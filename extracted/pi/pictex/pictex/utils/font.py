import skia

def is_variable_font(typeface: skia.Typeface) -> bool:
    try:
        return bool(typeface.getVariationDesignParameters())
    except:
        return False

def is_grapheme_supported_for_typeface(grapheme: str, typeface: skia.Typeface) -> bool:
    return all(typeface.unicharToGlyph(ord(cp)) != 0 for cp in grapheme)
