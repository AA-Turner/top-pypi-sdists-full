from pydantic import BaseModel, Field, model_validator
from typing import Optional


class ColumnMetaModel(BaseModel):
    column: Optional[str] = Field(None, description="Nome da coluna no banco de dados.")
    relation_column: Optional[str] = Field(
        None,
        description="Nome da coluna usada para relacionamento com outra entidade (para um relacionamento 1_N, indica a coluna da entidade relacionada, que aponta para a PK da entidade corrente).",
    )

    @model_validator(mode="after")
    def check_columns(self):
        if self.column is None and self.relation_column is None:
            raise ValueError("column or relation_column must be provided")
        return self
