from typing import Any, ClassVar, Dict, List, Optional
from pydantic import Field, model_validator, field_validator, ConfigDict
from abc import abstractmethod

from ...utils.types.source_types import SourceType, SourceCheckerType
from ...utils.custom_exceptions import InvalidSourceChecker
from ...utils.types.identifier import StrObjectId
from .helpers import SourceHelpers
from .mapeo_motivo import MapeoDeMotivo
from ...base_models import CompanyAssetModel
from ....models.company.assets.ai_agents_v2.chatty_ai_agent_config_for_automation import ChattyAIConfigForAutomation


import logging
logger = logging.getLogger("source_base")

class SourceBase(CompanyAssetModel):
    agent_id: Optional[str] = Field(alias="agent_email", default=None)
    description: Optional[str] = Field(default="")
    tags: List[StrObjectId] = Field(default_factory=list)
    products: List[StrObjectId] = Field(default_factory=list)
    flow: List[StrObjectId] = Field(default_factory=list)
    # Removal automations — asset IDs to REMOVE from the chat when this source matches
    # (mirror of tags/products/flow, which add).
    tags_to_remove: List[StrObjectId] = Field(default_factory=list)
    products_to_remove: List[StrObjectId] = Field(default_factory=list)
    flows_to_remove: List[StrObjectId] = Field(default_factory=list)
    chatty_ai_agent_config: Optional[ChattyAIConfigForAutomation] = Field(default=None)
    trackeable: bool = Field(default=True)
    category: str = Field(default="")
    source_checker: SourceCheckerType
    name: str = Field()
    target_funnel_id: Optional[StrObjectId] = Field(
        default=None,
        description="Target funnel to move the chat to (for cross-funnel transitions)"
    )
    target_stage_id: Optional[StrObjectId] = Field(
        default=None,
        description="Target stage within the target funnel"
    )
    campaign_id: Optional[str] = Field(default=None)
    campaign_name: Optional[str] = Field(default=None)
    motivo_id: Optional[StrObjectId] = Field(
        default=None,
        description=(
            "El motivo de consulta que esta fuente declara. Determinístico: el lead entra con "
            "el tag espejo, la automatización y el workflow del motivo, sin ninguna llamada de "
            "IA. None = la fuente no declara motivo."
        ),
    )
    motivo_ids: List[StrObjectId] = Field(
        default_factory=list,
        description=(
            "Los motivos que declara la fuente (0.5.10). [] = la IA elige entre todos (o, sin IA, "
            "Consulta general); [m] = declara el motivo, sin clasificar; [m1, m2, …] (hasta 5) = la "
            "IA elige SÓLO entre esos y repregunta si duda. `motivo_id` queda por compatibilidad y "
            "se mantiene en sincronía: un motivo => motivo_id = motivo_ids[0]; 0 o varios => None."
        ),
    )
    mapeo_motivo: Optional[MapeoDeMotivo] = Field(
        default=None,
        description="Quién mapeó la fuente a sus motivos (persona o IA) y en qué estado quedó.",
    )
    entrada_id: Optional[StrObjectId] = Field(
        default=None,
        description="Entrada del Flujo de atención a la que pertenece",
    )
    account_id: Optional[StrObjectId] = Field(
        default=None,
        description=(
            "The WhatsApp account (`whatsapp_accounts`) the source belongs to (multi-account). "
            "Sources created before multi-account have none: the company's default account owns "
            "them. A null is never written (see UpdateableMixin.scope_fields)."
        ),
    )

    model_config = ConfigDict(extra='ignore', exclude_none=True) #type: ignore

    @property
    @abstractmethod
    def default_category(self) -> str:
        pass

    @property
    def topic_id_set(self) -> StrObjectId:
        if not hasattr(self, "topic_id"):
            raise ValueError(f"Source {self.name} of type {self.type} has no attribute topic_id")
        if not self.topic_id:
            raise ValueError(f"Topic id not set for source {self.name} of type {self.type} id {self.id}")
        return self.topic_id


    def model_dump(self, *args, **kwargs) -> Dict:
        kwargs["by_alias"] = True
        data = super().model_dump(*args, **kwargs)
        data["type"] = self.type
        return data

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        kwargs["by_alias"] = True
        data = super().model_dump_json(*args, **kwargs)
        data["type"] = self.type.value
        return data

    @field_validator('source_checker', mode="before")
    @classmethod
    def lowercase_source_checker(cls, v: str) -> str:
        return v.lower()

    @model_validator(mode='after')
    def validate_source(self):
        if not SourceHelpers.is_valid_source_checker(source_type=self.type,source_checker=self.source_checker):
            raise InvalidSourceChecker(f"Source checker {self.source_checker} not valid for source type {self.type} | Allowed ones are {SourceHelpers.get_source_checkers(self.type)}")
        if not self.category:
            self.category = self.default_category
        return self

    #: Tope de motivos por fuente: con más, «la IA elige entre estos» deja de ser una ayuda.
    MAX_MOTIVOS: ClassVar[int] = 5

    @model_validator(mode='after')
    def sincronizar_motivos(self):
        """`motivo_ids` manda; `motivo_id` es su espejo para los lectores viejos.

        Un documento viejo trae sólo `motivo_id`: se lee como `[motivo_id]`.
        """
        if self.motivo_id and not self.motivo_ids:
            self.motivo_ids = [self.motivo_id]
        self.motivo_ids = list(dict.fromkeys(self.motivo_ids))
        if len(self.motivo_ids) > self.MAX_MOTIVOS:
            raise ValueError(
                f"Una fuente puede declarar hasta {self.MAX_MOTIVOS} motivos "
                f"(llegaron {len(self.motivo_ids)})."
            )
        self.motivo_id = self.motivo_ids[0] if len(self.motivo_ids) == 1 else None
        return self


    @model_validator(mode='before')
    def validate_lists(cls, data: Dict) -> Dict:
        if "products" in data and data["products"] is None:
            data["products"] = []
        if "flow" in data and data["flow"] is None:
            data["flow"] = []
        if "tags" in data and data["tags"] is None:
            data["tags"] = []
        if "motivo_ids" in data and data["motivo_ids"] is None:
            data["motivo_ids"] = []
        if "category" in data and data["category"] is None:
            data["category"] = ""
        return data

    @property
    @abstractmethod
    def type(self) -> SourceType:
        pass