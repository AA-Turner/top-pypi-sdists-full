from pydantic import BaseModel, Field
from typing import List, Optional

from nsj_rest_lib2.compiler.edl_model.column_meta_model import ColumnMetaModel
from nsj_rest_lib2.compiler.edl_model.index_model import IndexModel


class RepositoryLinkToBaseModel(BaseModel):
    base_property: str = Field(
        ...,
        description="Nome da propriedade na entidade base utilizada para o relacionamento 1x1.",
    )
    column: str = Field(
        ...,
        description="Nome da coluna (ou propriedade) na entidade parcial responsável por referenciar a entidade base.",
    )
    on_delete: Optional[str] = Field(
        None,
        description="Política de exclusão configurada no relacionamento com a entidade base.",
    )
    nullable: Optional[bool] = Field(
        False,
        description="Indica se o relacionamento com a entidade base pode ser nulo.",
    )


class RepositoryModel(BaseModel):
    map: str = Field(
        ..., description="Nome da tabela, no BD, para a qual a entidade é mapeada."
    )
    shared_table: Optional[bool] = Field(
        default=False,
        description="Indica se a tabela é compartilhada entre múltiplas entidades (padrão: False).",
    )
    table_owner: Optional[bool] = Field(
        None, description="Indica que essa entidade é dona da tabela (schema)."
    )  # TODO Validar explicação
    properties: Optional[dict[str, ColumnMetaModel]] = Field(
        None, description="Dicionário de colunas da entidade."
    )
    indexes: Optional[List[IndexModel]] = Field(
        None, description="Lista de índices de banco de dados, associados à entidade."
    )
    link_to_base: Optional[RepositoryLinkToBaseModel] = Field(
        None,
        description="Configuração de relacionamento 1x1 com a entidade base (extensões parciais).",
    )
