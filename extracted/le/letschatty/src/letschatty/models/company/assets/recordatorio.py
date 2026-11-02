"""Un recordatorio: algo que hay que hacer, con fecha. Puede colgar de un chat o no.

No es un highlight —que es una nota y se queda quieta— ni un mensaje programado —que le
habla al cliente—. Este le habla al agente: vence y se resuelve.

DE QUIÉN ES
-----------
Dos ejes independientes, `chat_id` y `assignee_id`, dan cuatro casos:

    chat + sin responsable  → de quien tenga el chat (y si no tiene agente, de la empresa)
    chat + responsable      → del responsable
    sin chat + sin resp.    → del creador: es un pendiente propio
    sin chat + responsable  → se lo dejaron a esa persona

En las empresas con APB el agente del chat rota con cada apertura, y eso juega a favor:
"este chat es tuyo ahora" ES el mecanismo de asignación de APB, así que un recordatorio sin
responsable siguiendo al chat es la semántica correcta, no una desincronización.

⚠️ POR QUÉ `assignee_id` VOLVIÓ, Y QUÉ HAY QUE VALIDAR
------------------------------------------------------
Este campo existió, se sacó en `8991c2f` y volvió. El motivo por el que se sacó sigue
siendo cierto y NO lo arregla el modelo: asignarle un recordatorio a alguien que no puede
ver ese chat le deja un link muerto en la agenda —y el título filtrándole el nombre de un
cliente al que no tiene acceso—.

Lo que lo cierra es una validación que vive en quien escribe, no acá:

    con chat  → sólo se puede asignar a alguien que pueda VER ese chat
    sin chat  → a quien sea; no hay cliente, no hay título que filtre nada

Un `assignee_id` que no pasó por esa validación es una fuga, no un dato.

VISIBILIDAD
-----------
No vive acá: se calcula al leer. Quien puede ver el chat ve sus recordatorios, más el
creador y el responsable, que siempre ven lo suyo. Sin chat, sólo el creador y el
responsable. Guardar acá una copia del agente del chat se desincronizaría en cuanto el chat
se reasigna.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, ClassVar, List, Optional

from pydantic import Field, field_validator

from ...base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel
from ...utils.types import StrObjectId


class RecordatorioPreview(ChattyAssetPreview):
    titulo: str
    remind_at: datetime
    #: Nulo en los pendientes sueltos, que no cuelgan de ninguna conversación.
    chat_id: Optional[StrObjectId] = Field(default=None)
    resolved_at: Optional[datetime] = Field(default=None)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {
            "titulo": 1, "remind_at": 1, "chat_id": 1, "resolved_at": 1,
        }

    @classmethod
    def from_asset(cls, asset: "Recordatorio") -> "RecordatorioPreview":
        return cls(
            _id=asset.id,
            name=asset.titulo,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            titulo=asset.titulo,
            remind_at=asset.remind_at,
            chat_id=asset.chat_id,
            resolved_at=asset.resolved_at,
            deleted_at=asset.deleted_at,
        )


class Recordatorio(CompanyAssetModel):
    titulo: str = Field(description="Qué hay que hacer. 'Llamar a Pepe'")
    detalle: Optional[str] = Field(default=None, description="Por qué, o qué decirle. Se lee cuando el recordatorio salta, días después")
    remind_at: datetime = Field(description="Cuándo vence, en UTC")
    #: NO es `frozen`: se le puede colgar un chat después, o sacárselo. Cambiarlo cambia
    #: quién lo ve, así que quien escriba tiene que validar el chat destino igual que en el alta.
    chat_id: Optional[StrObjectId] = Field(default=None, description="El chat del que cuelga. Nulo = pendiente suelto: no es sobre ninguna conversación")
    assignee_id: Optional[StrObjectId] = Field(default=None, description="Responsable. Nulo: lo atiende quien tenga el chat, o el creador si no hay chat. ⚠️ Con chat, sólo puede ser alguien que pueda ver ese chat")
    created_by: StrObjectId = Field(frozen=True, description="Quién lo pidió. Lo sigue viendo aunque el chat pase a otra persona")
    resolved_at: Optional[datetime] = Field(default=None)
    resolved_by: Optional[StrObjectId] = Field(default=None)
    categoria_ids: List[StrObjectId] = Field(
        default_factory=list,
        description="Categorías del recordatorio. Vacía = sin categoría; nunca se infiere.",
    )

    preview_class: ClassVar[type[RecordatorioPreview]] = RecordatorioPreview
    #: Sin esto se guardan como string y la agenda —que filtra por rango de fechas—
    #: devuelve vacío aunque los recordatorios existan.
    database_datetime_fields: ClassVar[set[str]] = {"remind_at", "resolved_at"}

    @field_validator("remind_at", "resolved_at", mode="before")
    @classmethod
    def _a_utc(cls, v: object) -> object:
        # Mongo devuelve datetimes naive. Sin esto, comparar con `now(UTC)` para saber si
        # venció explota con "can't compare offset-naive and offset-aware".
        if isinstance(v, datetime):
            return v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v.astimezone(timezone.utc)
        return v

    @field_validator("categoria_ids", mode="before")
    @classmethod
    def _deduplicar_preservando_orden(cls, v: object) -> object:
        # El orden lo elige quien carga el recordatorio; un id repetido no agrega ninguna
        # información y sólo haría que un chip se dibuje dos veces.
        if not isinstance(v, list):
            return v
        vistos: set[Any] = set()
        sin_duplicados = []
        for categoria_id in v:
            if categoria_id not in vistos:
                vistos.add(categoria_id)
                sin_duplicados.append(categoria_id)
        return sin_duplicados

    @property
    def resuelto(self) -> bool:
        return self.resolved_at is not None

    @property
    def vencido(self) -> bool:
        """Se calcula, no se guarda.

        Un estado guardado necesitaría a alguien que lo escriba al vencer —el schedule que
        el diseño descarta— y se desincronizaría en cuanto alguien reprograma.
        """
        return not self.resuelto and self.remind_at <= datetime.now(timezone.utc)
