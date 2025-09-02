import abc
from typing import Type, List
from pydantic import BaseModel

from pymultirole_plugins.v1 import ABCSingleton
from pymultirole_plugins.v1.schema import Document


class SegmenterParameters(BaseModel):
    pass


class SegmenterBase(metaclass=ABCSingleton):
    """Base class for example plugin used in the tutorial."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def segment(
        self, documents: List[Document], options: SegmenterParameters
    ) -> List[Document]:
        """Segment the input documents and return the modified documents.

        :param documents: A list of annotated documents.
        :param options: options of the parser.
        :returns: List[Document].
        """

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return SegmenterParameters
