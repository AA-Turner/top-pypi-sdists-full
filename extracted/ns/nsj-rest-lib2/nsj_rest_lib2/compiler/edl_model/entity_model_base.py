from __future__ import annotations

import uuid

from pydantic import BaseModel, Field
from typing import Dict, List, Optional

from nsj_rest_lib2.compiler.edl_model.property_meta_model import PropertyMetaModel
from nsj_rest_lib2.compiler.edl_model.repository_model import RepositoryModel
from nsj_rest_lib2.compiler.edl_model.trait_property_meta_model import (
    ExtendsPropertyMetaModel,
    TraitPropertyMetaModel,
)


class EntityModelBase(BaseModel):
    description: str = Field(..., description="Descrição da entidade.")
    id: str = Field(
        ...,
        description="Identificador único da entidade, dentro de um determinado escopo (podendo ser sobreescrito para um tenant ou grupo _empresarial).",
    )
    mixin: Optional[bool] = Field(
        False,
        description="Indica se o modelo é um mixin (bloco reutilizável, que não gera contém tabela própria no banco).",
    )
    extends: Optional[str] = Field(
        None, description="Identificador da entidade estendida por esta."
    )
    trait_from: Optional[str] = Field(
        None, description="Identificador da entidade que a trait estende."
    )
    partial_of: Optional[str] = Field(
        None,
        description="Identificador da entidade base estendida por esta extensão parcial (relacionamento 1x1 transparente).",
    )
    mixins: Optional[List[str]] = Field(
        None,
        description="Lista de mixins (blocos reutilizáveis) aplicados ao modelo.",
    )
    required: Optional[List[str]] = Field(
        None, description="Lista de campos obrigatórios no modelo."
    )
    partition_data: Optional[List[str]] = Field(
        None,
        description="Lista de propriedades da entidade, que serã usadas para particionamento dos dados no banco (sendo obrigatórias em todas as chamadas, inclusive como um tipo de filtro obrigatório).",
    )
    main_properties: Optional[List[str]] = Field(
        None,
        description="Lista de propriedades resumo do modelo (retornadas em qualquer chamada GET, mesmo que não pedidas por meio do parâmetro 'fields').",
    )
    search_properties: Optional[List[str]] = Field(
        None,
        description="Lista de propriedades do modelo que serão utilizadas nas chamadas de query do usuário (suportando também campos das entidades relacionadas). Sugere-se que a biblioteca crie automaticamente os índices para fulltext search.",
    )
    metric_label: Optional[List[str]] = Field(
        None,
        description="Lista de campos incluídos no agrupamento das métricas enviadas ao OpenTelemetry.",
    )
    trait_properties: Optional[Dict[str, TraitPropertyMetaModel]] = Field(
        None,
        description="Dicionário de propriedades condicionais da trait (isso é, especifica propriedades, e seus valores fixos, que serão usados como um tipo de filtro fixo usado como condição para que a propridade principal assum o papel daquele tipo de trait).",
    )
    extends_properties: Optional[Dict[str, ExtendsPropertyMetaModel]] = Field(
        None,
        description="Dicionário de propriedades condicionais associadas ao uso de extends (especifica propriedades e seus valores fixos, usados como filtros quando a entidade é uma especialização via extends).",
    )
    properties: Dict[str, PropertyMetaModel] = Field(
        ..., description="Dicionário de propriedades do modelo."
    )
    composed_properties: Optional[Dict[str, List[str]]] = Field(
        None,
        description="Dicionário que define grupos de propriedades compostas, permitindo agrupar propriedades existentes em DTOs agregados.",
    )
    components: Optional[Dict[str, "EntityModelBase"]] = Field(
        None,
        description="Entidades filhas, relacionadas por composição e definidas inline (evitando a criação de novos arquivos EDL para a definição de entidades componentes da entidade atual).",
    )
    repository: RepositoryModel = Field(
        ..., description="Configurações de mapeamento para o banco de dados."
    )

    # Propriedades de controle da compilação (não fazem parte do JSON de representação das entidades)
    tenant: int = Field(default=0, exclude=True)
    grupo_empresarial: uuid.UUID = Field(
        default=uuid.UUID("00000000-0000-0000-0000-000000000000"), exclude=True
    )


EntityModelBase.model_rebuild()
