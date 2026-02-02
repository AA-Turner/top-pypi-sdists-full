from pydantic import BaseModel, Field
from typing import List, Optional


class IndexModel(BaseModel):
    name: str = Field(..., description="Nome do índice no banco de dados.")
    columns: List[str] = Field(
        ..., description="Lista de colunas que compõem o índice."
    )
    unique: Optional[bool] = Field(
        default=False,
        description="Indica se é um índice de unicidade (padrão: False). Se não for de unicidade, será um índice usado para otimização de queries.",
    )
