# File Location: /matrix/ai_models/ai_model_dto.py

from dataclasses import dataclass

from matrx_orm import BaseDTO
from matrx_utils import vcprint

from matrx_ai.db._registry import get_model

AiModel = get_model("AiModel")

info = True
debug = False
verbose = False

""" vcprint guidelines
verbose=verbose for things we do not want to see most of the time
verbose=debug for things we want to see during debugging
verbose=info for things that should almost ALWAYS print
verbose=True for errors and things that should never be silenced
Errors are always set to verbose=True, color="red"
"""

DEFAULT_MAX_TOKENS = 4096


@dataclass
class AiModelDTO(BaseDTO):
    id: str
    default_max_tokens: int | None = None

    async def _initialize_dto(self, model: AiModel) -> None:
        """Override to populate DTO fields from the model."""
        vcprint(f"[Ai Model DTO] {model.name} initializing...", verbose=verbose, color="green")
        self.id = str(model.id)
        await self._process_core_data(model)
        await self._process_metadata(model)
        await self._initial_validation(model)
        self.initialized = True
        vcprint(f"[Ai Model DTO] {self.name} initialized---", verbose=verbose, color="green")

    async def _process_core_data(self, ai_model_item: AiModel) -> None:
        """Process core data and compute runtime properties.

        NOTE: this DTO no longer reads ``model_definition.endpoints`` (a DROP column of the
        AI-catalog reshape). Routing is resolved from ``ai.offering``→``ai.api.translator_key``
        via ``matrx_ai.catalog``; this DTO is a thin metadata shell and ``default_endpoint`` is
        retired (it had zero consumers). Skip-of-unroutable-models now lives in the catalog.
        """
        # Compute default_max_tokens
        max_tokens = ai_model_item.max_tokens
        if max_tokens is None or not isinstance(max_tokens, int) or max_tokens <= 0:
            self.default_max_tokens = DEFAULT_MAX_TOKENS
            vcprint(
                f"Model {self.name} has invalid or missing max_tokens ({max_tokens}); using default: {DEFAULT_MAX_TOKENS}",
                verbose=debug,
                color="yellow",
                log_level="info",
            )
        else:
            self.default_max_tokens = max_tokens

    async def _process_metadata(self, ai_model_item):
        """Placeholder for future metadata processing."""
        pass

    async def _initial_validation(self, ai_model_item):
        """Validate that required fields are present."""
        if not ai_model_item.name:
            raise ValueError(f"Model {self.id} has no name")

    async def _final_validation(self):
        """Final validation of the DTO."""
        if self.default_max_tokens is None:
            vcprint(
                f"Model {self.name} has no default_max_tokens after initialization",
                verbose=info,
                color="red",
            )
            return False
        return True

    async def get_validated_dict(self):
        """Get the validated dictionary."""
        validated = await self._final_validation()
        dict_data = self.to_dict()
        if not validated:
            vcprint(
                dict_data,
                "[AiModelDTO] Validation Failed",
                verbose=info,
                pretty=True,
                color="red",
            )
        return dict_data
