"""Wrap text based on Unicode line breaking algorithm."""

from collections.abc import Iterator, Sequence
from typing import Callable, Optional, Protocol

from uniseg.breaking import Breakables, boundaries
from uniseg.graphemecluster import grapheme_clusters
from uniseg.linebreak import line_break_breakables
from uniseg.unicodedatawrapper import EA, east_asian_width

__all__ = [
    'Formatter',
    'Wrapper',
    'wrap',
    'TTFormatter',
    'tt_width',
    'tt_text_extents',
    'tt_wrap',
]


class Formatter(Protocol):
    """Protocol methods and properties for formatters invoked by the
    :class:`Wrapper` instance.

    Your formatter should have the same methods and properties this class has.
    They are invoked by the :class:`Wrapper` instance to determin logical
    widths of texts and to give you the ways to handle them, such as to render
    them.
    """

    @property
    def wrap_width(self) -> Optional[int]:
        """Logical width of text wrapping.

        Note that returning ``None`` (which is the default) means "do not
        wrap" while returning ``0`` means "wrap as narrowly as possible."
        """
        ...

    @property
    def tab_width(self) -> int:
        """Logical width of tab forwarding.

        This property value is used by the :class:`Wrapper` instance to
        determin the actual forwarding extents of tabs in each of the
        positions.
        """
        ...

    def text_extents(self, s: str, /) -> list[int]:
        """Return a list of logical lengths from start of the string to each of
        code point in `s`.
        """
        ...

    def handle_text(self, text: str, extents: list[int], /) -> None:
        """Handler method which is invoked when the `text` should be put on the
        current position and `extents`.
        """
        ...

    def handle_new_line(self) -> None:
        """Handler method which is invoked when a new line begins."""
        ...


class Wrapper:
    """Text wrapping engine.

    Usually, you don't need to create an instance of the class directly.  Use
    :func:`wrap` instead.
    """

    def wrap(
        self,
        formatter: Formatter,
        s: str,
        /,
        cur: int = 0,
        offset: int = 0,
        *,
        iter_breakables: Callable[[str], Breakables] = line_break_breakables,
    ) -> int:
        """Wrap string `s` with `formatter` and invoke its handlers.

        The optional arguments, `cur` is the starting position of the string
        in logical length, and `offset` means left-side offset of the wrapping
        area in logical length --- this parameter is only used for calculating
        tab-stopping positions for now.

        If `char_wrap` is set to ``True``, the text will be warpped with its
        grapheme cluster boundaries instead of its line break boundaries.
        This may be helpful when you don't want the word wrapping feature in
        your application.

        The method returns the total count of wrapped lines.
        """
        _expand_tabs = self.__class__._expand_tabs
        _wrap_width = formatter.wrap_width
        _tab_width = formatter.tab_width
        _get_text_extents = formatter.text_extents
        iline = 0
        start = offset + cur
        for para in s.splitlines(True):
            while True:
                formatter.handle_new_line()
                iline += 1
                extents = _get_text_extents(para)
                extents = _expand_tabs(para, extents, _tab_width, start)
                for end in boundaries(iter_breakables(para)):
                    extent = extents[end-1]
                    if _wrap_width is not None and _wrap_width < extent and 0 < start:
                        # do wrap
                        line = para[:start]
                        para = para[start:]
                        formatter.handle_text(line, extents[:start])
                        start = offset
                        break
                    start = end
                else:
                    formatter.handle_text(para, extents)
                    start = offset
                    break
        return iline

    @staticmethod
    def _expand_tabs(
        s: str, extents: list[int], /, tab_width: int, offset: int = 0
    ) -> list[int]:
        # expand tabs
        expanded_extens = []
        gap = 0
        for c, extent in zip(s, extents):
            extent += gap
            if c == '\t':
                tab_extent = ((offset + extent + tab_width) // tab_width) * tab_width
                new_extent = tab_extent - offset
                gap += new_extent - extent
                extent = new_extent
            expanded_extens.append(extent)
        return expanded_extens


# static objects
_wrapper = Wrapper()


def wrap(
    formatter: Formatter,
    s: str,
    /,
    cur: int = 0,
    offset: int = 0,
    *,
    iter_breakables: Callable[[str], Breakables] = line_break_breakables,
) -> int:
    """Wrap string `s` with `formatter` using the module's static
    :class:`Wrapper` instance

    See :meth:`Wrapper.wrap` for further details of the parameters.
    """
    return _wrapper.wrap(formatter, s, cur, offset, iter_breakables=iter_breakables)


# TT

class TTFormatter:
    """Fixed-width text wrapping formatter."""

    def __init__(
        self,
        width: int,
        *,
        tab_width: int = 8,
        tab_char: str = ' ',
        ambiguous_as_wide: bool = False,
    ) -> None:
        self._lines: list[str] = []
        self.wrap_width = width
        self.tab_width = tab_width
        self.ambiguous_as_wide = ambiguous_as_wide
        self.tab_char = tab_char

    @property
    def wrap_width(self) -> int:
        """Wrapping width."""
        return self._wrap_width

    @wrap_width.setter
    def wrap_width(self, value: int) -> None:
        self._wrap_width = value

    @property
    def tab_width(self) -> int:
        """Forwarding size of tabs."""
        return self._tab_width

    @tab_width.setter
    def tab_width(self, value: int) -> None:
        self._tab_width = value

    @property
    def tab_char(self) -> str:
        """Character to fill tab spaces with."""
        return self._tab_char

    @tab_char.setter
    def tab_char(self, value: str):
        if (east_asian_width(value) not in (EA.N, EA.NA, EA.H)):
            raise ValueError('only narrow code point is available for tab_char')
        self._tab_char = value

    @property
    def ambiguous_as_wide(self) -> bool:
        """Treat code points with its East_Easian_Width property is 'A' as
        those with 'W'; having double width as alpha-numerics.
        """
        return self._ambiguous_as_wide

    @ambiguous_as_wide.setter
    def ambiguous_as_wide(self, value: bool) -> None:
        self._ambiguous_as_wide = value

    def text_extents(self, s: str, /) -> list[int]:
        """Return a list of logical lengths from the start of the string to the
        end of each code point for `s`.
        """
        return tt_text_extents(s, ambiguous_as_wide=self.ambiguous_as_wide)

    def handle_text(self, text: str, extents: Sequence[int], /) -> None:
        """Handler which is invoked when a text should be put on the current
        position.
        """
        chars: list[str] = []
        prev_extent = 0
        for c, extent in zip(text, extents):
            if c == '\t':
                chars.append(self.tab_char * (extent - prev_extent))
            else:
                chars.append(c)
            prev_extent = extent
        self._lines[-1] += ''.join(chars)

    def handle_new_line(self) -> None:
        self._lines.append('')

    def lines(self) -> Iterator[str]:
        """Iterate every wrapped line strings."""
        return iter(self._lines)


def tt_width(s: str, /, index: int = 0, *, ambiguous_as_wide: bool = False) -> int:
    R"""Return logical width of the grapheme cluster at `s[index]` on
    fixed-width typography

    Return value will be ``1`` (halfwidth) or ``2`` (fullwidth).

    Generally, the width of a grapheme cluster is determined by its leading
    code point.

    >>> tt_width('A')
    1
    >>> tt_width('\u8240')  # U+8240: CJK UNIFIED IDEOGRAPH-8240
    2
    >>> tt_width('g\u0308')     # U+0308: COMBINING DIAERESIS
    1
    >>> tt_width('\U00029e3d')  # U+29E3D: CJK UNIFIED IDEOGRAPH-29E3D
    2

    If `ambiguous_as_wide` is specified to ``True``, some characters such as
    greek alphabets are treated as they have fullwidth as well as ideographics
    does.

    >>> tt_width('α')   # U+03B1: GREEK SMALL LETTER ALPHA
    1
    >>> tt_width('α', ambiguous_as_wide=True)
    2
    """
    cp = s[index]
    eaw = east_asian_width(cp)
    if eaw in (EA.W, EA.F) or (eaw == EA.A and ambiguous_as_wide):
        return 2
    return 1


def tt_text_extents(s: str, /, *, ambiguous_as_wide: bool = False) -> list[int]:
    R"""Return a list of logical lengths from the start of the string to the
    end of each code point for `s`.

    >>> tt_text_extents('abc')
    [1, 2, 3]
    >>> tt_text_extents('あいう')
    [2, 4, 6]
    >>> tt_text_extents('𩸽')    # test a code point out of BMP
    [2]

    Calling with an empty string will return an empty list:

    >>> tt_text_extents('')
    []

    The meaning of `ambiguous_as_wide` is the same as that of :func:`tt_width`:

    >>> tt_text_extents('αβ')
    [1, 2]
    >>> tt_text_extents('αβ', ambiguous_as_wide=True)
    [2, 4]
    """
    widths: list[int] = []
    total_width = 0
    for g in grapheme_clusters(s):
        total_width += tt_width(g, ambiguous_as_wide=ambiguous_as_wide)
        widths.extend(total_width for __ in g)
    return widths


def tt_wrap(
    s: str,
    /,
    wrap_width: int,
    *,
    tab_width: int = 8,
    tab_char: str = ' ',
    ambiguous_as_wide: bool = False,
    cur: int = 0,
    offset: int = 0,
    iter_breakables: Callable[[str], Breakables] = line_break_breakables,
) -> Iterator[str]:
    R"""Wrap string `s` based on fixed-width typography algorithm and return
    a list of wrapped lines.

    >>> s1 = 'A quick brown fox jumped over the lazy dog.'
    >>> list(tt_wrap(s1, 24))
    ['A quick brown fox ', 'jumped over the lazy ', 'dog.']
    >>> s2 = '和歌は、人の心を種として、万の言の葉とぞなれりける。'
    >>> list(tt_wrap(s2, 24))
    ['和歌は、人の心を種とし', 'て、万の言の葉とぞなれり', 'ける。']

    If `wrap_width` is less than the length of the word of the line, at least
    one word will be remain as the part of the line:

    >>> list(tt_wrap('supercalifragilisticexpialidocious', 24))
    ['supercalifragilisticexpialidocious']
    >>> list(tt_wrap('wrap supercalifragilisticexpialidocious long words', 24))
    ['wrap ', 'supercalifragilisticexpialidocious ', 'long words']

    Tab options:

    >>> s3 = 'A\tquick\tbrown fox jumped\tover\tthe lazy dog.'
    >>> print('\n'.join(s.rstrip() for s in tt_wrap(s3, 32)))
    A       quick   brown fox
    jumped  over    the lazy dog.
    >>> print('\n'.join(s.rstrip() for s in tt_wrap(s3, 32, tab_width=10)))
    A         quick     brown fox
    jumped    over      the lazy
    dog.
    >>> print('\n'.join(s.rstrip() for s in tt_wrap(s3, 32, tab_char='+')))
    A+++++++quick+++brown fox
    jumped++over++++the lazy dog.

    (We use `s.rstrip()` for every line because trailing spaces will be
    removed in the docstring here while every wrapped line returned may
    keep them.)

    An option for treating code points of which East_Asian_Width propertiy is
    'A' (ambiguous):

    >>> s4 = 'μῆνιν ἄειδε θεὰ Πηληϊάδεω Ἀχιλῆος'
    >>> list(tt_wrap(s4, 24, ambiguous_as_wide=True))
    ['μῆνιν ἄειδε ', 'θεὰ Πηληϊάδεω ', 'Ἀχιλῆος']
    >>> list(tt_wrap(s4, 24, ambiguous_as_wide=False))
    ['μῆνιν ἄειδε θεὰ ', 'Πηληϊάδεω Ἀχιλῆος']

    The `cur` option controls the indentation of the first line of the result:

    >>> print('*** ' + '\n'.join(s.rstrip() for s in tt_wrap(s3, 32, cur=4)))
    *** A   quick   brown fox
    jumped  over    the lazy dog.

    The `offset` affects indent level for every line:

    >>> print('\n'.join(('||' + s.rstrip()) for s in tt_wrap(s3, 32, offset=2)))
    ||A     quick   brown fox
    ||jumped        over    the lazy
    ||dog.
    """
    formatter = TTFormatter(
        width=wrap_width,
        tab_width=tab_width,
        tab_char=tab_char,
        ambiguous_as_wide=ambiguous_as_wide,
    )
    _wrapper.wrap(formatter, s, cur, offset, iter_breakables=iter_breakables)
    return formatter.lines()


# Main

if __name__ == '__main__':
    import doctest
    doctest.testmod()
