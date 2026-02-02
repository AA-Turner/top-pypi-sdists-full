from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, Field, RootModel, constr, conint, confloat


PropertyType = Literal[
    "string", "number", "integer", "boolean", "date", "datetime", "object"
]

# ---------------------------
# Tipos básicos e utilitários
# ---------------------------

PrimitiveType = Literal[
    "string", "number", "integer", "boolean", "date", "datetime", "object"
]


# Em EDL, type também pode apontar para outra entidade "scope.object" ou "array"
# e propriedades podem ter metadados comuns.
class Property(BaseModel):
    # Tipo pode ser primitivo, "array", um caminho de entidade "escopo.entidade"
    # ou um formato especializado (ex.: "uuid", "currency", "cpf", "cnpj"...)
    type: str = Field(
        ..., description="Tipo EDL (primitivo, array, ou escopo.entidade)."
    )
    cardinality: Optional[Literal["1_1", "0_1", "1_N", "0_N", "N_N"]] = None

    # Metadados comuns
    label: Optional[str] = None
    description: Optional[str] = None
    length: Optional[int] = None
    pattern: Optional[str] = None
    default: Optional[Any] = None
    immutable: Optional[bool] = None
    minimum: Optional[confloat()] = None
    maximum: Optional[confloat()] = None
    enum: Optional[List[Union[str, int]]] = None

    # Chaves
    pk: Optional[bool] = None
    key_alternative: Optional[bool] = None  # alias semântico (chave natural)
    pk_substitute: Optional[bool] = None  # usado em alguns exemplos
    value: Optional[Any] = None  # valor fixo/derivado
    format: Optional[str] = None  # ex.: "uuid", "currency", "quantity"

    # Itens (para arrays embutidos)
    items: Optional[Union["RelationDef", Property, Dict[str, Any]]] = None


class ComposedMap(RootModel[Dict[str, Any]]):
    """
    Representa composed_properties: aceita mapeamentos arbitrários
    (strings de caminho e/ou mapas aninhados).
    """

    pass


# ---------------------------
# Relations (objetos inline)
# ---------------------------


class RelationDef(BaseModel):
    # Em EDL, relations podem ser "object" (estrutura inline) ou "array" de "object"
    type: Optional[str] = Field(None, description='Tipicamente "object" ou "array".')
    # Identificador opcional da relação/objeto
    id_: Optional[str] = Field(None, alias="$id")
    required: Optional[List[str]] = None
    properties: Optional[Dict[str, Property]] = None
    composed_properties: Optional[Dict[str, ComposedMap]] = None
    items: Optional[Union[Property, Dict[str, Any]]] = None


# ---------------------------
# Regras (motor de regras)
# ---------------------------

RuleType = Literal["required", "custom", "format"]


class Rule(BaseModel):
    field: str
    type: RuleType
    when: Optional[str] = None
    message: Optional[str] = None
    messageParams: Optional[List[str]] = None
    # Para tipo "format"
    pattern: Optional[str] = None
    # Para tipo "custom"
    fn: Optional[str] = None


# ---------------------------
# Repository (mapeamento físico)
# ---------------------------


class LinkToBase(BaseModel):
    base: str
    baseProperty: str
    column: str
    onDelete: Optional[Literal["cascade", "restrict", "set_null"]] = None
    nullable: Optional[bool] = None


class IndexDef(BaseModel):
    name: str
    fields: List[str]
    unique: Optional[bool] = None


class ColumnsMap(RootModel[Dict[str, Any]]):
    """
    Suporta tanto mapeamentos simples {"prop": {"column": "col"}}
    quanto caminhos aninhados ("totais.valorNf": {"column": "vnf"}).
    """

    pass


class RepositoryBlock(BaseModel):
    map: Optional[str] = None  # schema.tabela
    shared_table: Optional[bool] = None
    table_owner: Optional[bool] = None
    linkToBase: Optional[LinkToBase] = None  # obrigatório para parciais
    columns: Optional[ColumnsMap] = None
    indexes: Optional[List[IndexDef]] = None


# Em muitos exemplos, "repository" é um dicionário de blocos lógicos:
# { "Documento": {...}, "documento.linhas": {...} }
Repository = Dict[str, RepositoryBlock]


# ---------------------------
# API e Handlers
# ---------------------------

Verb = Literal["GET", "POST", "PUT", "PATCH", "DELETE"]
ComposePolicy = Literal["transparent", "readonly", "none"]


class HttpResultSpec(BaseModel):
    statusOnSuccess: Optional[int] = None
    location: Optional[str] = None


class HandlerResult(BaseModel):
    expect: Optional[Literal["entity_row", "rows", "void"]] = None
    entity: Optional[str] = None
    http: Optional[HttpResultSpec] = None


class ComposeMappingAttr(BaseModel):
    attr: str
    from_: Optional[str] = Field(None, alias="from")
    # Para arrays: indicar o tipo composto do banco
    as_: Optional[str] = Field(None, alias="as")
    # Mapeamento de itens (quando from aponta para array)
    mapping: Optional[List["ComposeMappingAttr"]] = None


class CallCompose(BaseModel):
    typeName: str
    mapping: List[ComposeMappingAttr]
    onMissing: Optional[Literal["error", "ignore", "null"]] = None


class ArgBinding(BaseModel):
    to: str
    source: Literal["body", "context"]
    from_: Optional[str] = Field(None, alias="from")
    dbType: Optional[str] = None
    compose: Optional[CallCompose] = None


class CallSpec(BaseModel):
    style: Optional[Literal["named"]] = None
    argBinding: Optional[List[ArgBinding]] = None


class HandlerError(BaseModel):
    sqlstate: Optional[str] = None
    httpStatus: Optional[int] = None
    message: Optional[str] = None


class HandlerConfig(BaseModel):
    impl: Optional[str] = None  # ex.: "pg_function"
    functionRef: Optional[str] = None
    signature: Optional[List[str]] = None
    call: Optional[CallSpec] = None
    result: Optional[HandlerResult] = None
    errors: Optional[List[HandlerError]] = None
    transaction: Optional[Literal["wrap", "none"]] = None
    validate: Optional[Literal["warn", "strict", "none"]] = None


class APIBlock(BaseModel):
    resource: Optional[str] = None
    expose: Optional[bool] = None
    verbs: Optional[List[Verb]] = None
    filters: Optional[List[str]] = None
    default_sort: Optional[List[str]] = None
    includeExtensionsByDefault: Optional[bool] = None
    subset: Optional[str] = None

    # Parciais / composição
    composeWithBase: Optional[bool] = None
    composePolicy: Optional[ComposePolicy] = None

    # Handlers por verbo
    handlers: Optional[Dict[Verb, HandlerConfig]] = None


# ---------------------------
# Bloco principal: model
# ---------------------------


class ModelBlock(BaseModel):
    mixins: Optional[List[str]] = None
    required: Optional[List[str]] = None
    main_properties: Optional[List[str]] = None

    properties: Dict[str, Property] = Field(default_factory=dict)
    composed_properties: Optional[Dict[str, ComposedMap]] = None
    relations: Optional[Dict[str, RelationDef]] = None
    rules: Optional[List[Rule]] = None

    # Repository pode conter múltiplos blocos lógicos
    repository: Optional[Repository] = None

    api: Optional[APIBlock] = None


# ---------------------------
# Arquivo EDL (raiz)
# ---------------------------


class EDLFile(BaseModel):
    edl_version: Literal["1.0"]
    escopo: str

    # Presentes conforme o tipo (entidade normal, trait, subclasse, parcial)
    id: Optional[str] = None
    trait_from: Optional[str] = None
    trait: Optional[str] = None
    extends: Optional[str] = None
    partial_of: Optional[str] = None
    partial: Optional[str] = None

    # Outros observados nos exemplos
    version: conint(ge=1)
    abstract: Optional[bool] = None
    native: Optional[bool] = None

    model: ModelBlock
