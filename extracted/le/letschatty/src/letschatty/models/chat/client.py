from pydantic import AliasChoices, BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any, List
from ..base_models.chatty_asset_model import CompanyAssetModel
# Re-exportado: `models/company/empresa.py` y otros importan QualityScore desde acá.
from .quality_scoring import QualityScore  # noqa: F401
from .chat_client_preview import ChatClientPreview
# Re-exportado: el modelo vive en su módulo para que la preview lo use sin import circular.
from .no_contactar import NoContactar  # noqa: F401
from .marcas_de_meta import MarcaDeMeta
from ..utils.types.serializer_type import SerializerType
from ..whatsapp.portfolio_bsuid import PortfolioBsuid


class Client(CompanyAssetModel):
    """La persona: un documento de la colección `clients`, compartido por todos sus chats.

    Una persona por teléfono (`waid`) o por BSUID (`user_id`) dentro de la empresa. Acá vive
    todo lo que es de la persona y no de una conversación: nombre, email, documento, id en el
    CRM y lo que contestó en formularios. Lo que es de la conversación (etiquetas, productos,
    ventas, touchpoints, highlights, calidad) vive en la raíz del chat.

    Los chats guardan sólo `ChatClientPreview` (lo que muestra la bandeja) más `client_id`.
    Quien necesita la persona completa (eventos, prompts de la IA, el detalle del chat) la
    pide al cargador.
    """
    # `waid` (teléfono) es OPCIONAL: un contacto que adoptó username y llegó fuera de la
    # ventana de 30 días trae sólo BSUID. Todo lo que depende del teléfono es condicional.
    waid: Optional[str] = None
    user_id: Optional[str] = Field(default=None, description="BSUID (e.g. 'AR.xxx') — identidad estable por portfolio; identity fallback when waid is absent")
    user_id_parent: Optional[str] = Field(default=None, description="BSUID padre (CC.ENT.x), multi-portfolio")
    username: Optional[str] = Field(default=None, description="Username de WhatsApp — display-only, mutable; NUNCA se usa como clave")
    bsuids: List[PortfolioBsuid] = Field(default_factory=list, description="One BSUID per business portfolio (multi-account). `user_id` keeps the default account's one for older readers")
    parent_bsuids: List[str] = Field(default_factory=list, description="Parent BSUIDs of enrolled portfolios")
    name: str
    country: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    #: Hoy hay chats con `document_id` y otros con `DNI` para el mismo dato: se lee
    #: cualquiera de los dos y se guarda siempre `document_id`.
    document_id: Optional[str] = Field(default=None, validation_alias=AliasChoices("document_id", "DNI"))
    lead_form_data: Dict[str, Any] = Field(default_factory=dict, description="Structured customer data collected during conversation")
    external_id: Optional[str] = Field(default=None)
    no_contactar: Optional[NoContactar] = Field(
        default=None,
        frozen=True,
        description="FROZEN A PROPOSITO: lo escribe SOLO el $set de api-chatty. None = se lo puede contactar. Ver NoContactar.",
    )
    marcas_de_meta: Dict[str, MarcaDeMeta] = Field(
        default_factory=dict,
        frozen=True,
        description="FROZEN A PROPOSITO: las escribe SOLO ClientCollection.set_marca_de_meta. Por tipo; vencidas no valen. Ver marcas_de_meta.py.",
    )

    model_config = ConfigDict(validate_by_name=True, validate_by_alias=True)

    @property
    def se_puede_contactar(self) -> bool:
        """¿Le podemos escribir por iniciativa nuestra? (contestarle cuando escribe, siempre)."""
        return self.no_contactar is None

    def preview(self) -> ChatClientPreview:
        """La copia que guardan sus chats."""
        return ChatClientPreview(**{field: getattr(self, field) for field in ChatClientPreview.FIELDS})

    def model_dump_json(self, *args, **kwargs) -> Dict[str, Any]:
        dump = super().model_dump_json(*args, **kwargs)
        if kwargs.get("serializer", SerializerType.API) == SerializerType.DATABASE:
            # «No contactar»: la fecha como fecha, y un None no se escribe (el documento de un
            # contacto contactable queda igual que antes).
            if self.no_contactar is None:
                dump.pop("no_contactar", None)
            else:
                dump["no_contactar"] = self.no_contactar.model_dump()
            if not self.marcas_de_meta:
                dump.pop("marcas_de_meta", None)
            else:
                dump["marcas_de_meta"] = {tipo: marca.model_dump() for tipo, marca in self.marcas_de_meta.items()}
            # Unique multikey indexes: two documents with an EMPTY list collide (Mongo indexes `[]`
            # as a value), so an empty identity list is never written.
            for name in ("bsuids", "parent_bsuids"):
                if not getattr(self, name):
                    dump.pop(name, None)
        return dump

    def get_waid(self) -> Optional[str]:
        return self.waid

    def get_identity(self) -> Optional[str]:
        """Con qué se le escribe: el teléfono si lo hay, si no el BSUID."""
        return self.waid or self.user_id

    def get_user_id(self) -> Optional[str]:
        return self.user_id

    def bsuid_for(self, portfolio_id: Optional[str]) -> Optional[str]:
        """The BSUID that numbers of `portfolio_id` can message. Falls back to the legacy scalar
        `user_id` while the person has no per-portfolio list yet (pre-migration documents)."""
        for entry in self.bsuids:
            if entry.portfolio_id == portfolio_id:
                return entry.bsuid
        return None if self.bsuids else self.user_id

    def get_name(self) -> str:
        return self.name

    def get_country(self) -> Optional[str]:
        return self.country

    def get_email(self) -> Optional[str]:
        return self.email

    @property
    def get_info(self) -> dict:
        return self.model_dump()


class ClientData(BaseModel):
    """Lo que manda la UI al editar a la persona. `DNI` es el nombre del contrato de la API."""
    name: Optional[str] = None
    country: Optional[str] = None
    email: Optional[str] = None
    DNI: Optional[str] = None
    photo: Optional[str] = None
    external_id: Optional[str] = None
    lead_form_data: Optional[Dict[str, Any]] = None
