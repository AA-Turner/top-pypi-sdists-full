from typing import Annotated

from msgspec import Meta

FilePath = Annotated[str, Meta(extra={"file_reference": True})]
