from pydantic import BaseModel, Field, model_validator
from typing import List, Optional

from nsj_rest_lib2.compiler.edl_model.primitives import BasicTypes, DefaultTypes
from nsj_rest_lib2.compiler.edl_model.primitives import CardinalityTypes, PropertyType


class DomainConfigModel(BaseModel):
    value: str = Field(..., description="Valor do enum.")
    mapped_value: Optional[BasicTypes] = Field(
        None, description="Valor mapeado do enum (gravado no BD)."
    )


class PropertyMetaModel(BaseModel):
    type: PropertyType = Field(..., description="Tipo da propriedade.")
    label: Optional[str] = Field(None, description="Rótulo da propriedade.")
    description: Optional[str] = Field(None, description="Descrição da propriedade.")
    default: Optional[DefaultTypes] = Field(
        None,
        description="Valor padrão da propriedade (caso não fornecido numa chamada de persistência). Pode indicar um valor, ou uma expressão (ex.: 'now()' para data/hora atual).",
    )
    pk: Optional[bool] = Field(
        default=False, description="Indica se a propriedade é parte da chave primária."
    )
    key_alternative: Optional[bool] = Field(
        default=False,
        description="Indica se a propriedade é parte de uma chave alternativa (chave natural).",
    )
    cardinality: Optional[CardinalityTypes] = Field(
        None,
        description="Cardinalidade do relacionamento (válido para propriedades do tipo 'array' ou 'object').",
    )
    # Validação
    max_length: Optional[int] = Field(
        None, description="Comprimento máximo (para strings)."
    )

    min_length: Optional[int] = Field(
        None, description="Comprimento mínimo (para strings)."
    )
    pattern: Optional[str] = Field(
        None,
        description="Expressão regular que o valor da propriedade deve obedecer (para strings).",
    )
    minimum: Optional[float] = Field(
        None, description="Valor mínimo permitido (para números)."
    )
    maximum: Optional[float] = Field(
        None, description="Valor máximo permitido (para números)."
    )
    validator: Optional[str] = Field(
        None,
        description="Caminho completo para uma função de validação e alteração personalizada (ex.: 'module.validator'). Sendo que as funções dinâmicas sempre estarão no modulo XPTO.",
    )  # TODO Definir padrão de carregamento do módulo de funções customizadas
    domain_config: Optional[List[DomainConfigModel]] = Field(
        None,
        description="Lista de valores permitidos.",
    )
    immutable: Optional[bool] = Field(
        default=False,
        description="Indica se a propriedade é imutável (não pode ser alterada após a criação).",
    )
    trim: Optional[bool] = Field(
        default=False,
        description="Indica se espaços em branco devem ser removidos do início e fim (para strings).",
    )
    lowercase: Optional[bool] = Field(
        default=False,
        description="Indica se o valor deve ser convertido para minúsculas (para strings).",
    )
    uppercase: Optional[bool] = Field(
        default=False,
        description="Indica se o valor deve ser convertido para maiúsculas (para strings).",
    )

    on_save: Optional[str] = Field(
        None,
        description="Função de conversão para o tipo da entidade (ex.: converter string para uuid).",
    )
    on_retrieve: Optional[str] = Field(
        None,
        description="Função de conversão do tipo da entidade para o tipo da API (ex.: converter uuid para string).",
    )

    @model_validator(mode="after")
    def check_cardinality_required(self):
        if isinstance(self.type, str) and self.cardinality is None:
            raise ValueError(
                "The property 'cardinality' is required when type point to other entity."
            )
        return self
