import re
from typing import List, Tuple


ANYSCALE_SDK_INTRO = """\
The AnyscaleSDK class must be constructed in order to make calls to the SDK. This class allows you to create an authenticated client in which to use the SDK.

| Param | Type | Description |
| :--- | :--- | :--- |
| `auth_token` | Optional String | Authentication token used to verify you have permissions to access Anyscale. If not provided, permissions default to the credentials set for your current user. Credentials can be set by following the instructions on this page: https://console.anyscale.com/credentials |

**Example**
```python
from anyscale import AnyscaleSDK

sdk = AnyscaleSDK()
```
"""


class LegacySDK:
    def __init__(self, name: str, docstring: str):
        self.name = name
        self.docstring = docstring

    @classmethod
    def from_md(cls, md: str) -> "LegacySDK":
        """
        Convert a blob of markdown into a LegacySDK object.
        """
        name = ""
        docstring = ""

        for line in md.split("\n"):
            if line.startswith("### "):
                name = line[4:]
            else:
                docstring += (
                    re.sub("\\(./models.md#([a-z]+)\\)", "(#\\1-legacy)", line) + "\n"
                )

        return cls(name=name, docstring=docstring.strip())


class LegacyModel:
    def __init__(self, name: str, docstring: str):
        self.name = name
        self.docstring = docstring

    @classmethod
    def from_md(cls, md: str) -> "LegacyModel":
        """
        Convert a blob of markdown into a LegacySDK object.
        """
        name = ""
        docstring = ""

        for line in md.split("\n"):
            if line.startswith("## "):
                name = line[3:]
            else:
                docstring += re.sub("\\(#([a-z]+)\\)", "(#\\1-legacy)", line) + "\n"

        return cls(name=name, docstring=docstring.strip())


def _chunk(md_file: str, start: str, ends: List[str]) -> List[str]:
    """
    Split a markdown file into chunks based on the header.
    """
    chunks = []
    with open(md_file) as f:
        line = f.readline()
        while line:
            if not line.startswith(start):
                line = f.readline()
                continue
            chunk = line
            line = f.readline()
            while line and not any(line.startswith(end) for end in ends):
                chunk += line
                line = f.readline()

            chunks.append(chunk)

    return chunks


def parse_legacy_sdks(
    api_md_file: str, model_md_file: str
) -> Tuple[List[LegacySDK], List[LegacyModel]]:
    """
    Parse the legacy SDK markdown files into a list of LegacySDK objects.
    """
    legacy_sdks = [
        LegacySDK.from_md(chunk)
        for chunk in _chunk(api_md_file, "### ", ["### ", "## ", "# "])
    ]
    legacy_models = [
        LegacyModel.from_md(chunk)
        for chunk in _chunk(model_md_file, "## ", ["## ", "# "])
    ]

    return legacy_sdks, legacy_models
