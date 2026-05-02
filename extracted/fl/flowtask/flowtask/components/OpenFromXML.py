import io
from pathlib import Path
from lxml import etree
from ..exceptions import ComponentError, FileError
from .OpenWithBase import FlowComponent


class OpenFromXML(FlowComponent):
    """
    OpenFromXML


        Overview

            This component opens an XML file and returns it as an XML etree Object.

        :widths: auto


        | directory    |   No     | The directory where the XML file is located.                      |
        | filename     |   Yes    | The name of the XML file to be opened.                            |
        | use_strings  |   No     | If True, the component will treat the input as a string containing|
        |              |          | XML data.                                                         |
        | as_nodes     |   No     | If set, specifies the node to be extracted from the XML tree.     |

    Returns:
        - An `lxml.etree.ElementTree` object if the entire XML tree is parsed.
        - A list of nodes (`lxml.etree.Element`) if `as_nodes` is set.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          OpenFromXML:
          # attributes here
        ```
    """
    _version = "1.0.0"
    async def start(self, **kwargs):
        """
        start.

            Get if directory exists
        """
        if self.previous:
            print("PREVIOUS FILE >", self.previous, type(self.input))
            if isinstance(self.input, dict):
                try:
                    filenames = list(self.input.keys())
                    if filenames:
                        self.filename = filenames[0]
                except (TypeError, IndexError) as exc:
                    raise FileError("File is empty or doesn't exists") from exc
            else:
                self.data = self.input
        if hasattr(self, "directory"):
            self.path = Path(self.directory).resolve()
            if not self.path.exists() or not self.path.is_dir():
                raise ComponentError(
                    f"Directory not found: {self.directory}", status=404
                )
            # TODO: all logic for opening from File, pattern, etc
            if not self.filename:
                raise ComponentError("Filename empty", status=404)

    async def close(self):
        """
        close.
            close method
        """
        pass

    async def run(self):
        """
        run.

            Open the XML file and return the object
        """
        root = None
        if hasattr(self, "use_strings") and self.use_strings is True:
            fp = open(self.filename, "r")
            self.data = fp.read()
            self.filename = None
        if self.filename:
            print(f"Opening XML filename {self.filename}")
            # Create a parser object
            parser = etree.XMLParser(encoding="utf-8")
            # open XML from File
            tree = etree.parse(str(self.filename), parser)
            try:
                root = tree.getroot()
                if etree.iselement(root):
                    self._result = tree
                    numrows = int(tree.xpath("count(/*)"))
                    self.add_metric("NUMROWS", numrows)
                    self.add_metric("OPENED_FILE", self.filename)
                    if hasattr(self, "as_nodes"):
                        objs = root.findall(self.node)
                        if objs:
                            self._result = objs
                    return self._result
            except Exception as err:
                print(err)
                return False
        elif self.data:
            if isinstance(self.data, str):
                # open XML from string
                xml = io.BytesIO(self.data.encode("utf-8"))
                parser = etree.XMLParser(recover=True, encoding="utf-8")
                root = etree.parse(xml, parser)
                try:
                    if etree.iselement(root.getroot()):
                        self._result = root
                except Exception as err:
                    print("Error on parsing XML Tree: ", err)
                    return False
            else:
                #  TODO: check if data is already an XML element
                try:
                    print(etree.iselement(self.data.getroot()))
                except Exception as err:
                    raise ComponentError(f"Invalid Object lxml, Error: {err}") from err
                root = self.data
            self._result = root
            return self._result
        else:
            return False
