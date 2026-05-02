from typing import Union
from pathlib import PurePath, Path
# BeautifulSoup:
from bs4 import BeautifulSoup
from lxml import html, etree
# aiofiles:
import aiofiles

from .flow import FlowComponent


class ParseHTML(FlowComponent):
    """
    ParseHTML.
    Parse HTML Content using lxml etree and BeautifulSoup.


    Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ParseHTML:
          xml: true
        ```
    """
    _version = "1.0.0"

    async def open_html(self, filename: Union[str, PurePath]) -> str:
        """Open the HTML file."""
        if isinstance(filename, str):
            filename = Path(filename).resolve()
        if not filename.exists():
            raise FileNotFoundError(
                f"File not found: {filename}"
            )
        async with aiofiles.open(filename, '+rb') as fp:
            return await fp.read()

    async def start(self, **kwargs) -> bool:
        if self.previous:
            self._filelist = self.input
        else:
            # TODO: parsing from a directory provided instead.
            pass
        if not isinstance(self._filelist, list):
            raise TypeError(
                "Input must be a list of filenames"
            )
        return True

    def get_soup(self, content: str, parser: str = 'html.parser'):
        """Get a BeautifulSoup Object."""
        return BeautifulSoup(content, parser)

    def get_etree(self, content: str) -> tuple:
        try:
            x = etree.fromstring(content)
        except etree.XMLSyntaxError:
            x = None
        try:
            h = html.fromstring(content)
        except etree.XMLSyntaxError:
            h = None
        return x, h

    async def run(self):
        """
        Open all Filenames and convert them into BeautifulSoup and etree objects.
        """
        self._result = {}
        for filename in self._filelist:
            content = await self.open_html(filename)
            soup = self.get_soup(content)
            etree_obj, html_obj = self.get_etree(content)
            self._result[filename] = {
                'soup': soup,
                'html': html_obj,
                'content': content
            }
            if getattr(self, 'xml', False) is True:
                self._result[filename]['xml'] = etree_obj

        return self._result

    async def close(self):
        pass
