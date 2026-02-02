from pydantic import Field

from nsj_rest_lib2.compiler.edl_model.entity_model_base import EntityModelBase


class EntityModelRoot(EntityModelBase):
    escopo: str = Field(..., description="Escopo do EDL (define a aplicação).")
