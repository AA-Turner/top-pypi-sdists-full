"""The class implementation for the `lock_clock` material icon.
"""

from apysc._display.fixed_html_svg_icon_base import FixedHtmlSvgIconBase


class MaterialLockClockIcon(FixedHtmlSvgIconBase):
    """
    The class implementation for the `lock_clock` material icon.
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
        return '<svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M14.5 14.2l2.9 1.7-.8 1.3L13 15v-5h1.5v4.2zM22 14c0 4.41-3.59 8-8 8-2.02 0-3.86-.76-5.27-2H4c-1.15 0-2-.85-2-2V9c0-1.12.89-1.96 2-2v-.5C4 4.01 6.01 2 8.5 2c2.34 0 4.24 1.79 4.46 4.08.34-.05.69-.08 1.04-.08 4.41 0 8 3.59 8 8zM6 7h5v-.74C10.88 4.99 9.8 4 8.5 4 7.12 4 6 5.12 6 6.5V7zm14 7c0-3.31-2.69-6-6-6s-6 2.69-6 6 2.69 6 6 6 6-2.69 6-6z"/></svg>'  # noqa
