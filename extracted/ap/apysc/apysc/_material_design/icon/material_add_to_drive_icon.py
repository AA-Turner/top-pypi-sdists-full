"""The class implementation for the `add_to_drive` material icon.
"""

from apysc._display.fixed_html_svg_icon_base import FixedHtmlSvgIconBase


class MaterialAddToDriveIcon(FixedHtmlSvgIconBase):
    """
    The class implementation for the `add_to_drive` material icon.
    """

    def _get_fixed_svg_icon_html(self) -> str:
        """
        Get a fixed SVG icon HTML string.

        Returns
        -------
        fixed_svg_icon_html : str
            Fixed SVG icon HTML string.

        References
        ----------
        - Material icon document
            - https://simon-ritchie.github.io/apysc/en/material_icon.html
        - Material Symbols & Icons, APACHE LICENSE, VERSION 2.0
            - https://fonts.google.com/icons?icon.size=24&icon.color=%23e8eaed
            - https://www.apache.org/licenses/LICENSE-2.0.html
        """
        return '<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M7.71 3.52L1.15 15l3.42 5.99 6.56-11.47-3.42-6zM13.35 15H9.73L6.3 21h8.24c-.96-1.06-1.54-2.46-1.54-4 0-.7.13-1.37.35-2zM20 16v-3h-2v3h-3v2h3v3h2v-3h3v-2h-3zm.71-4.75L15.42 2H8.58v.01l6.15 10.77C15.82 11.68 17.33 11 19 11c.59 0 1.17.09 1.71.25z"/></svg>'  # noqa
