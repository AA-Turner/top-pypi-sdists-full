from typing import List, Optional
from pydantic import BaseModel, Field

from nsj_rest_lib2.compiler.edl_model.primitives import BasicTypes, PropertyType
from nsj_rest_lib2.compiler.edl_model.property_meta_model import DomainConfigModel


class TraitPropertyMetaModel(BaseModel):
    type: PropertyType = Field(..., description="Tipo da propriedade.")
    value: BasicTypes = Field(
        ..., description="Valor fixo da propriedade de condicionamento do trait."
    )
    domain_config: Optional[List[DomainConfigModel]] = Field(
        None,
        description="Lista de valores permitidos.",
    )


ExtendsPropertyMetaModel = TraitPropertyMetaModel
