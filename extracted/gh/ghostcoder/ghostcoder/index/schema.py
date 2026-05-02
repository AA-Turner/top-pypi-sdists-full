
from llama_index.schema import TextNode, Document
from pydantic import Field

from ghostcoder.codeblocks import CodeBlock


class CodeNode(TextNode):
    """Node with a code block."""

    codeblock: CodeBlock = Field(default=None, description="Code block.")

    #@classmethod
    #def get_type(cls) -> str:
    #    return ObjectType.CODE

    @classmethod
    def class_name(cls) -> str:
        return "CodeNode"


class CodeDocument(Document, CodeNode):
    """Data document containing a code block."""

    @classmethod
    def class_name(cls) -> str:
        return "CodeDocument"
