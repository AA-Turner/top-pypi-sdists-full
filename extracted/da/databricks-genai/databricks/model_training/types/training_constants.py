"""
Databricks training constants
"""

from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Dict, List, Tuple

from mcli.api.schema.generic_model import DeserializableModel
from mcli.utils.utils_string_functions import camel_case_to_snake_case

from databricks.model_training.api.engine.engine import MAPIException


@dataclass()
class TrainingModelConstants(DeserializableModel):
    """Databricks model constants

    Args:
        name: The name of the model
        display_name: A more `displayable` name for the model
        max_context_length: Maximum context length of the model (tokens)
    """

    name: str
    display_name: str
    max_context_length: int

    _required_properties: Tuple[str, ...] = tuple([
        'name',
        'displayName',
        'maxContextLength',
    ])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> 'TrainingModelConstants':
        """Load the model info from MAPI response.
        """
        missing = set(cls._required_properties) - set(response)

        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message='Missing required key(s) in response to deserialize TrainingModelConstants'
                f'object: {", ".join(missing)} ',
            )

        args = {camel_case_to_snake_case(prop): response.get(prop) for prop in cls._required_properties}
        return cls(**args)

    def _repr_html_(self) -> str:
        """Display the model card as HTML.
        """
        keys = ['name', 'display_name', 'max_context_length']

        attr_to_label = {key: ' '.join([word.title() for word in key.split('_')]) for key in keys}

        # pylint: disable-next=import-outside-toplevel,cyclic-import
        from databricks.model_training.types.common import generate_vertical_html_table
        return generate_vertical_html_table([self], attr_to_label)


@dataclass
class TrainingConstants(DeserializableModel):
    """Contains a list of Databricks model constants for training

    Args:
        models: A list of model cards
    """
    models: List[TrainingModelConstants]

    _required_properties: Tuple[str, ...] = tuple([
        'models',
    ])

    @classmethod
    def from_mapi_response(cls, response: Dict[str, Any]) -> 'TrainingConstants':
        """Load the model info list from MAPI response.
        """

        missing = set(cls._required_properties) - set(response)

        if missing:
            raise MAPIException(
                status=HTTPStatus.BAD_REQUEST,
                message='Missing required key(s) in response to deserialize TrainingConstants'
                f'object: {", ".join(missing)} ',
            )

        return cls(**{
            'models': [TrainingModelConstants.from_mapi_response(model_info) for model_info in response.get('models')]
        })
