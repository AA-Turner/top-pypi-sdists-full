#
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2026 Carsten Igel.
#
# This file is part of simplepycons
# (see https://github.com/carstencodes/simplepycons).
#
# This file is published using the MIT license.
# Refer to LICENSE for more information
#
""""""
# pylint: disable=C0302
# Justification: Code is generated

from typing import TYPE_CHECKING

from .base_icon import Icon

if TYPE_CHECKING:
    from collections.abc import Iterable


class SanityIcon(Icon):
    """"""
    @property
    def name(self) -> "str":
        return "sanity"

    @property
    def original_file_name(self) -> "str":
        return "sanity.svg"

    @property
    def title(self) -> "str":
        return "Sanity"

    @property
    def primary_color(self) -> "str":
        return "#0D0E12"

    @property
    def raw_svg(self) -> "str":
        return ''' <svg xmlns="http://www.w3.org/2000/svg"
 role="img" viewBox="0 0 24 24">
    <title>Sanity</title>
     <path d="m23.327 15.205-.893-1.555-4.321 2.632
 4.799-6.11.726-.426-.179-.27.33-.421-1.515-1.261-.693.883-13.992
 8.186 5.173-6.221 9.636-5.282-.915-1.769-5.248 2.876
 2.584-3.106-1.481-1.305-5.816 6.994-5.777 3.168 4.423-5.847
 2.771-1.442-.88-1.789-8.075 4.203L6.186 4.43 4.648 3.198 0
 9.349l.072.058.868 1.768 5.153-2.683-4.696 6.207.77.617.458.885
 5.425-2.974-5.974 7.185 1.481 1.304.297-.358 14.411-8.459-4.785
 6.094.078.065-.007.005.992 1.726 6.364-3.877-2.451 3.954 1.642
 1.077L24 15.648z" />
</svg>'''

    @property
    def guidelines_url(self) -> "str | None":
        _value: "str" = ''''''
        if len(_value) > 0:
            return _value
        return None

    @property
    def source(self) -> "str":
        return '''https://github.com/sanity-io/logos/blob/e298a'''

    @property
    def license(self) -> "tuple[str | None, str | None]":
        _type: "str | None" = ''''''
        _url: "str | None" = ''''''

        if _type is not None and len(_type) == 0:
            _type = None

        if _url is not None and len(_url) == 0:
            _url = None

        return _type, _url

    @property
    def aliases(self) -> "Iterable[str]":
        yield from []
