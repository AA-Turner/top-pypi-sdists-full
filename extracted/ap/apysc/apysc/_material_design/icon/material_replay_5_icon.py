"""The class implementation for the `replay_5` material icon.
"""

from apysc._display.fixed_html_svg_icon_base import FixedHtmlSvgIconBase


class MaterialReplay5Icon(FixedHtmlSvgIconBase):
    """
    The class implementation for the `replay_5` material icon.
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
        return '<svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24" width="24"><g><rect fill="none" height="24" width="24"/></g><g><g><path d="M12,5V1L7,6l5,5V7c3.31,0,6,2.69,6,6s-2.69,6-6,6s-6-2.69-6-6H4c0,4.42,3.58,8,8,8s8-3.58,8-8S16.42,5,12,5z"/><g><path d="M10.69,13.9l0.25-2.17h2.39v0.71h-1.7l-0.11,0.92c0.03-0.02,0.07-0.03,0.11-0.05s0.09-0.04,0.15-0.05 s0.12-0.03,0.18-0.04s0.13-0.02,0.2-0.02c0.21,0,0.39,0.03,0.55,0.1s0.3,0.16,0.41,0.28s0.2,0.27,0.25,0.45s0.09,0.38,0.09,0.6 c0,0.19-0.03,0.37-0.09,0.54s-0.15,0.32-0.27,0.45s-0.27,0.24-0.45,0.31s-0.39,0.12-0.64,0.12c-0.18,0-0.36-0.03-0.53-0.08 s-0.32-0.14-0.46-0.24s-0.24-0.24-0.32-0.39s-0.13-0.33-0.13-0.53h0.84c0.02,0.18,0.08,0.32,0.19,0.41s0.25,0.15,0.42,0.15 c0.11,0,0.2-0.02,0.27-0.06s0.14-0.1,0.18-0.17s0.08-0.15,0.11-0.25s0.03-0.2,0.03-0.31s-0.01-0.21-0.04-0.31 s-0.07-0.17-0.13-0.24s-0.13-0.12-0.21-0.15s-0.19-0.05-0.3-0.05c-0.08,0-0.15,0.01-0.2,0.02s-0.11,0.03-0.15,0.05 s-0.08,0.05-0.12,0.07s-0.07,0.06-0.1,0.09L10.69,13.9z"/></g></g></g></svg>'  # noqa
