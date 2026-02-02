from __future__ import annotations

from typing import Dict, List, Literal, Optional

from pydantic import AliasChoices, BaseModel, Field, model_validator

APIVerbs = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]


class HandlerMapping(BaseModel):
    attr: str = Field(..., description="Nome do atributo no tipo composto de destino.")
    from_: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("from", "from_"),
        serialization_alias="from",
        description="Path de origem no payload (ex.: body.estabelecimento).",
    )
    as_: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("as", "as_"),
        serialization_alias="as",
        description="Tipo composto do elemento quando houver arrays (ex.: ns.t_item[]).",
    )
    mapping: Optional[List["HandlerMapping"]] = Field(
        default=None,
        description="Sub-mapeamento utilizado quando 'from' aponta para coleções.",
    )


class HandlerArgBinding(BaseModel):
    type_name: str = Field(
        ...,
        description="Nome qualificado do tipo composto esperado pela função no banco.",
    )
    mapping: List[HandlerMapping] = Field(
        ...,
        description="Mapeamento dos campos do payload para os atributos do tipo composto.",
    )


class HandlerCall(BaseModel):
    arg_binding: HandlerArgBinding = Field(
        ...,
        description="Configuração de binding do payload para o tipo composto.",
    )


class HandlerResult(BaseModel):
    expected: Literal["empty", "entity_row", "custom_json", "partial_row"] = Field(
        default="empty",
        description="Define o formato esperado do retorno da função.",
    )
    properties: Optional[List[str]] = Field(
        default=None,
        description="Lista de propriedades a serem retornadas quando o resultado esperado for 'partial_row'.",
    )

    @model_validator(mode="after")
    def validate_partial_row(self):
        if self.expected == "partial_row" and not self.properties:
            raise ValueError(
                "result.properties é obrigatório quando result.expected for 'partial_row'."
            )
        return self


class HandlerError(BaseModel):
    sqlstate: Optional[str] = Field(
        default=None,
        description="Código SQLSTATE tratado explicitamente.",
    )
    http_status: Optional[int] = Field(
        default=None,
        description="Código HTTP retornado quando o SQLSTATE for encontrado.",
    )
    message: Optional[str] = Field(
        default=None,
        description="Mensagem alternativa retornada quando o erro for capturado.",
    )


class HandlerConfig(BaseModel):
    impl: Optional[Literal["pg_function"]] = Field(
        default=None,
        description="Somente funções PostgreSQL (pg_function) são suportadas neste estágio.",
    )
    function_ref: Optional[str] = Field(
        default=None,
        description="Referência qualificada para a função no banco (ex.: schema.fn_nome).",
    )
    call: Optional[HandlerCall] = Field(
        default=None,
        description="Configuração de chamada (binding de argumentos).",
    )
    result: HandlerResult = Field(
        default_factory=HandlerResult,
        description="Especificação do que se espera da função.",
    )
    errors: Optional[List[HandlerError]] = Field(
        default=None,
        description="Tratamento específico para SQLSTATE conhecidos.",
    )


class APIModel(BaseModel):
    resource: str = Field(
        ...,
        description="Nome do recurso REST (rota base dos endpoints; exemplo: 'clientes').",
    )
    expose: Optional[bool] = Field(
        default=True,
        description="Indica se a API deve ser exposta (padrão: True).",
    )
    verbs: Optional[List[APIVerbs]] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH"],
        description="Lista de verbos HTTP suportados pela API (padrão: todos).",
    )
    default_sort: Optional[List[str]] = Field(
        None,
        description="Lista de campos usados na ordenação padrão (padrão: se nada for fornecido, será usada, ao menos, a PK).",
    )
    handlers: Optional[Dict[str, HandlerConfig]] = Field(
        default=None,
        description="Mapeamento opcional de verbos para handlers implementados via funções pg_function.",
    )


APIModel.model_rebuild()
