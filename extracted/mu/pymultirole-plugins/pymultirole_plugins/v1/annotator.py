import abc

from pydantic import BaseModel

from pymultirole_plugins.v1 import ABCSingleton
from pymultirole_plugins.v1.schema import Document


class AnnotatorParameters(BaseModel):
    pass


class AnnotatorBase(metaclass=ABCSingleton):
    """Base class for example plugin used in the tutorial."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def annotate(self, documents: list[Document], options: AnnotatorParameters) -> list[Document]:
        """Annotate the input documents and return the modified documents.

        :param document: An annotated document.
        :param options: options of the parser.
        :returns: Document.
        """

    @classmethod
    def get_model(cls) -> type[BaseModel]:
        return AnnotatorParameters
