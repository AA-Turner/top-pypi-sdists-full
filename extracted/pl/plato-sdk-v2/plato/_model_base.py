"""Shared pydantic base class for the code-generated model modules.

``plato._generated.models`` and ``plato.chronos.models`` define ~800 pydantic
models between them. Building every model's validator + serializer at import
time cost ~0.7s of process startup, and a given process usually touches only a
handful of those models. ``defer_build=True`` moves that work to first use
(first validate / serialize / json-schema call), which pydantic handles through
its mock-validator machinery -- no ``model_rebuild()`` call is required.

Pydantic merges ``model_config`` from base classes into subclasses, so the
generated classes keep their own ``ConfigDict(extra="allow")`` and additionally
inherit ``defer_build``.

Regeneration note: the generator (``openapi/generator/python.py``) must pass
``base_class="plato._model_base.BaseModel"`` to
``datamodel_code_generator.generate()`` for regenerated models to keep this.
``tests/unit/test_generated_models_defer_build.py`` fails if that is lost.
"""

from __future__ import annotations

from pydantic import BaseModel as _PydanticBaseModel
from pydantic import ConfigDict

__all__ = ["BaseModel"]


class BaseModel(_PydanticBaseModel):
    """Pydantic base model whose validator/serializer is built on first use."""

    model_config = ConfigDict(defer_build=True)
