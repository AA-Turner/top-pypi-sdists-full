"""The class implementation for the outlined `contactless` material icon.
"""

from apysc._display.fixed_html_svg_icon_base import FixedHtmlSvgIconBase


class MaterialContactlessOutlinedIcon(FixedHtmlSvgIconBase):
    """
    The class implementation for the outlined `contactless` material icon.
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
        return '<svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24" width="24"><g><rect fill="none" height="24" width="24"/></g><g><g><path d="M12,2C6.48,2,2,6.48,2,12c0,5.52,4.48,10,10,10s10-4.48,10-10C22,6.48,17.52,2,12,2z M12,20c-4.42,0-8-3.58-8-8 s3.58-8,8-8s8,3.58,8,8S16.42,20,12,20z"/><path d="M7.1,10.18c0.26,0.56,0.39,1.16,0.4,1.8c0.01,0.63-0.13,1.25-0.4,1.86l1.37,0.62c0.37-0.81,0.55-1.65,0.54-2.5 c-0.01-0.84-0.19-1.65-0.54-2.4L7.1,10.18z"/><path d="M13.33,7.33c0.78,1.57,1.18,3.14,1.18,4.64c0,1.51-0.4,3.09-1.18,4.69l1.35,0.66c0.88-1.81,1.33-3.61,1.33-5.35 c0-1.74-0.45-3.53-1.33-5.31L13.33,7.33z"/><path d="M10.2,8.72c0.53,1.07,0.8,2.21,0.8,3.4c0,1.17-0.26,2.23-0.78,3.15l1.3,0.74c0.65-1.15,0.98-2.45,0.98-3.89 c0-1.42-0.32-2.79-0.96-4.07L10.2,8.72z"/></g></g></svg>'  # noqa
