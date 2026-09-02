from typing import Any

from matrx_ai.db._registry import DBNotConfiguredError, get_base, get_model

AiModel = get_model("AiModel")

try:
    AiModelBase = get_base("AiModelBase")
except DBNotConfiguredError:
    # Standalone fallback (no host injection): a bare BaseManager over the injected
    # model with the SAME constructor signature as the host's generated base
    # (db/managers/ai/model_definition.py::ModelDefinitionBase). Only the generic
    # BaseManager vocabulary is available here — AiModelManager uses nothing else.
    from matrx_orm import BaseManager

    class AiModelBase(BaseManager[AiModel]):
        view_class = None

        def __init__(
            self,
            dto_class: type[Any] | None = None,
            view_class: type[Any] | None = None,
            fetch_on_init_limit: int = 0,
            fetch_on_init_with_warnings_off: str | None = None,
        ) -> None:
            if view_class is not None:
                self.view_class = view_class
            from .ai_model_dto import AiModelDTO

            super().__init__(
                AiModel,
                dto_class=dto_class or AiModelDTO,
                fetch_on_init_limit=fetch_on_init_limit,
                FETCH_ON_INIT_WITH_WARNINGS_OFF=fetch_on_init_with_warnings_off,
            )
