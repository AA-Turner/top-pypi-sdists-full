"""Emoji Data for UTS #51.

`UTS #51: Unicode Emoji (16.0)
<https://www.unicode.org/reports/tr51/tr51-27.html>`_
"""

from uniseg.db import get_handle, get_value
from uniseg.unicodeproperty import character_property

__all__ = [
    'emoji',
    'emoji_presentation',
    'emoji_modifier_base',
    'emoji_component',
    'extended_pictographic',
]


_H_EMOJI = get_handle('Emoji')
_H_EMOJI_PRESENTATION = get_handle('Emoji_Presentation')
_H_EMOJI_MODIFIER_BASE = get_handle('Emoji_Modifier_Base')
_H_EMOJI_COMPONENT = get_handle('Emoji_Component')
_H_EXTENDED_PICTOGRAPHIC = get_handle('Extended_Pictographic')


@character_property
def emoji(c: str, /) -> bool:
    """Return Emoji boolean Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> emoji('A')
    False
    >>> emoji('🐸')
    True
    """
    return bool(get_value(_H_EMOJI, ord(c)))


@character_property
def emoji_presentation(c: str, /) -> bool:
    """Return Emoji_Presentation boolean Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> emoji_presentation('A')
    False
    >>> emoji_presentation('🌞')
    True
    """
    return bool(get_value(_H_EMOJI_PRESENTATION, ord(c)))


@character_property
def emoji_modifier_base(c: str, /) -> bool:
    """Return Emoji_Modifier_Base boolean Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> emoji_modifier_base('A')
    False
    >>> emoji_modifier_base('👼')
    True
    """
    return bool(get_value(_H_EMOJI_MODIFIER_BASE, ord(c)))


@character_property
def emoji_component(c: str, /) -> bool:
    """Return Emoji_Component boolean Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> emoji_component('A')
    False
    >>> emoji_component('#')
    True
    """
    return bool(get_value(_H_EMOJI_COMPONENT, ord(c)))


@character_property
def extended_pictographic(c: str, /) -> bool:
    """Return Extended_Pictographic boolean Unicode property value for `c`.

    `c` must be a single Unicode character (code point).

    >>> extended_pictographic('A')
    False
    >>> extended_pictographic('🐤')
    True
    """
    return bool(get_value(_H_EXTENDED_PICTOGRAPHIC, ord(c)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
