from __future__ import annotations

from pydantic import Field
from typing import Optional

from nsj_rest_lib2.compiler.edl_model.api_model import APIModel
from nsj_rest_lib2.compiler.edl_model.entity_model_root import EntityModelRoot


class EntityModel(EntityModelRoot):
    edl_version: Optional[str] = Field(default="1.0", description="Versão do EDL")
    version: Optional[str] = Field(
        default="1.0", description="Versão da entidade (padrão: 1.0)."
    )
    abstract: Optional[bool] = Field(
        default=False,
        description="Indica se a entidade é abstrata (padrão: False). Caso positivo, não gera código, mas pode ser usada na geração de código de outras entidades.",
    )
    api: APIModel = Field(
        ...,
        description="Definição da API REST associada ao modelo, com todos os seus endpoints.",
    )
