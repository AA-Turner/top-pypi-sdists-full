import abc
from typing import Type, List
from pydantic import BaseModel

from pymultirole_plugins.v1 import ABCSingleton
from pymultirole_plugins.v1.schema import Document


class ProcessorParameters(BaseModel):
    pass


class ProcessorBase(metaclass=ABCSingleton):
    """Base class for example plugin used in the tutorial."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def process(
        self, documents: List[Document], options: ProcessorParameters
    ) -> List[Document]:
        """Process the input documents and return the modified documents.

        :param documents: A list of annotated documents.
        :param options: options of the parser.
        :returns: List[Document].
        """

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return ProcessorParameters
