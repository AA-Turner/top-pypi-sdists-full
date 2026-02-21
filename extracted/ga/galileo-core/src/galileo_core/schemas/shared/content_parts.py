from enum import Enum
from typing import List, Literal, Union

from pydantic import BaseModel, Field
from pydantic.types import UUID4
from typing_extensions import Annotated


class ContentPartType(str, Enum):
    text = "text"
    file = "file"


class TextContentPart(BaseModel):
    """A text segment within a message."""

    type: Literal[ContentPartType.text] = ContentPartType.text
    text: str


class FileContentPart(BaseModel):
    """Reference to a file associated with this message.

    The file_id can be resolved via the ``files`` dict returned on
    trace/span detail responses, which contains metadata such as
    modality, MIME type, and a presigned download URL.
    """

    type: Literal[ContentPartType.file] = ContentPartType.file
    file_id: UUID4


ContentPart = Annotated[
    Union[TextContentPart, FileContentPart],
    Field(discriminator="type"),
]

MessageContent = Union[str, List[ContentPart]]
