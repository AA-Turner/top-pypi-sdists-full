from collections.abc import Callable
from typing import Any, get_args, get_origin

from pydantic import ValidationError

from ._default_model_extractor import DefaultExtractor
from ._types import ParsedResponse, ResponseModelType
from .payload_extractor_protocol import PayloadExtractor


class ModelParserMixin:
    """
    A mixin that applies a Pydantic model to various input formats,
    with optional support for custom model handlers.
    """

    _extractor: PayloadExtractor | None

    def __init__(self, *, extractor: PayloadExtractor | None = None):
        self._extractor = extractor

    def apply_model(
        self,
        source: Any,
        *,
        model: ResponseModelType | None = None,
        model_handler: Callable | None = None,
        exception: type[Exception] | None = None,
        extractor: PayloadExtractor | None = None,
    ) -> ParsedResponse:
        """
        Convert source data into a parsed model or passthrough object.

        Args:
            source: Input data (dict, list, or raw object) to parse.
            model: Optional model class or List[Model] to parse against.
            model_handler: Optional custom callable to handle parsing.
            exception: Optional exception type to raise on failure.
            extractor: Optional extraction handler callable to handle parsing.

        Returns:
            ParsedResponse: The parsed object(s) or raw source.
        """
        try:
            if model_handler:
                return model_handler(source, model)

            extractor = extractor or self._extractor
            data = self._resolve_payload(source, extractor)

            if model is None:
                return data

            if get_origin(model) is list:
                item_type = get_args(model)[0]
                if not isinstance(data, list):
                    raise TypeError("Expected list in input payload")
                return [item_type(**item) for item in data]

            if not isinstance(data, dict):
                raise TypeError("Expected dict in input payload")

            return model(**data)

        except (ValidationError, TypeError, ValueError, KeyError) as e:
            if exception:
                raise exception(e) from e
            raise

    @staticmethod
    def _resolve_payload(source: Any, extractor: PayloadExtractor | None = None) -> Any:
        """
        Uses a pluggable extractor to transform source into raw payload.
        """
        extractor = extractor or DefaultExtractor()
        return extractor.extract(source)
