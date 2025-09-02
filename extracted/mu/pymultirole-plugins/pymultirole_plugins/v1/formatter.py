import abc
from typing import Type

from pydantic import BaseModel
from starlette.responses import Response

from pymultirole_plugins.v1 import ABCSingleton
from pymultirole_plugins.v1.schema import Document


class FormatterParameters(BaseModel):
    pass


class FormatterBase(metaclass=ABCSingleton):
    """Base class for example plugin used in the tutorial."""

    def __init__(self):
        pass

    @abc.abstractmethod
    def format(self, document: Document, options: FormatterParameters) -> Response:
        """Parse the input document and return a formatted response.

        :param document: An annotated document.
        :param options: options of the parser.
        :returns: Response.
        """

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return FormatterParameters
