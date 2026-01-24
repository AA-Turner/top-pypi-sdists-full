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


class ViteIcon(Icon):
    """"""
    @property
    def name(self) -> "str":
        return "vite"

    @property
    def original_file_name(self) -> "str":
        return "vite.svg"

    @property
    def title(self) -> "str":
        return "Vite"

    @property
    def primary_color(self) -> "str":
        return "#9135FF"

    @property
    def raw_svg(self) -> "str":
        return ''' <svg xmlns="http://www.w3.org/2000/svg"
 role="img" viewBox="0 0 24 24">
    <title>Vite</title>
     <path d="M13.056 23.238a.57.57 0 0
 1-1.02-.355v-5.202c0-.63-.512-1.143-1.144-1.143H5.148a.57.57 0 0
 1-.464-.903l3.777-5.29c.54-.753 0-1.804-.93-1.804H.57a.574.574 0 0
 1-.543-.746.6.6 0 0 1 .08-.157L5.008.78a.57.57 0 0 1
 .467-.24h14.589a.57.57 0 0 1 .466.903l-3.778 5.29c-.54.755 0 1.806.93
 1.806h5.745c.238 0 .424.138.513.322a.56.56 0 0 1-.063.603z" />
</svg>'''

    @property
    def guidelines_url(self) -> "str | None":
        _value: "str" = ''''''
        if len(_value) > 0:
            return _value
        return None

    @property
    def source(self) -> "str":
        return '''https://github.com/voidzero-dev/community-des
ign-resources/blob/55902097229cf01cf2a4ceb376f992f5cf306756/brand-asse'''

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
