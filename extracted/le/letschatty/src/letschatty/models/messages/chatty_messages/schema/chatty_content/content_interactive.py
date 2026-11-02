"""Contenido de un mensaje `interactive` de Meta (respuestas a Flows / botones / listas).

Hasta 2026-09 este modelo era un `pass`: MessageType.INTERACTIVE vivía en
uncontrolled_messages() y el webhook se descartaba con una notificación central
genérica — un lead que completaba el formulario de un Flow (nfm_reply) perdía
nombre, email y (si era primer contacto) hasta el chat y la atribución del anuncio.

Ahora el interactive es un mensaje de primera clase. Este modelo guarda las TRES
formas que Meta manda hoy bajo `interactive` — y degrada con elegancia cualquier
forma futura:

- ``nfm_reply``  (WhatsApp Flows / formularios): ``form_fields`` trae los pares
  campo/valor ya legibles (las claves ``screen_0_Name_0`` de Meta se limpian a
  ``Name``), más ``flow_token``/``flow_id``.
- ``button_reply`` / ``list_reply``: ``title`` es el texto visible que el cliente
  eligió; ``reply_id`` el id de developer; ``description`` sólo en listas.
- tipo desconocido: ``interactive_type`` conserva el tipo crudo y ``raw`` el dict
  original completo, con un ``body`` genérico. NUNCA se pierde el payload.

``body`` es SIEMPRE un resumen legible en español: es lo que ven las previews del
inbox, los checkers de fuente (literal/similarity), la IA al leer el thread y
cualquier export. ``raw`` conserva el dict `interactive` original para debugging
y para re-procesar formas futuras sin re-pedir el webhook.

`from_meta` NUNCA lanza: un ``response_json`` que no parsea, un Flow sin campos o
una forma nueva de Meta degradan a un contenido genérico con ``raw`` preservado.
Romper acá 500earía el webhook y envenenaría la cola SQS de backup-chatty
(incidente conocido — ver api-chatty docs/mensajes-sin-contenido-de-meta.md).
"""
from __future__ import annotations
import json
import logging
import re
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# Claves del response_json de un Flow que son metadata de Meta, no campos que el
# cliente completó. Se extraen a los campos dedicados y NUNCA van a form_fields.
_FLOW_METADATA_KEYS = {"flow_token", "flow_id", "flow_name"}

# screen_0_Name_1 → prefijo "screen_<n>_" + label del diseñador del Flow + sufijo "_<n>".
_FLOW_KEY_PREFIX = re.compile(r"^screen_\d+_")
_FLOW_KEY_SUFFIX = re.compile(r"_\d+$")


def clean_flow_field_key(key: str) -> str:
    """``screen_0_Email_Address_1`` → ``Email Address``.

    El prefijo ``screen_N_`` y el sufijo ``_M`` son ruido de serialización de Meta;
    el medio es el label que puso quien diseñó el Flow (con espacios convertidos a
    ``_``). Si después de limpiar no queda nada, se conserva la clave original —
    mejor una clave fea que un campo sin nombre."""
    cleaned = _FLOW_KEY_PREFIX.sub("", key)
    cleaned = _FLOW_KEY_SUFFIX.sub("", cleaned)
    cleaned = cleaned.replace("_", " ").strip()
    return cleaned or key


def _value_to_text(value: Any) -> str:
    """Representación legible de un valor de formulario (los multi-select llegan como lista)."""
    if isinstance(value, list):
        return ", ".join(_value_to_text(v) for v in value)
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


class InteractiveFormField(BaseModel):
    """Un campo completado de un formulario de WhatsApp Flow (nfm_reply).

    ``key`` conserva la clave cruda de Meta (``screen_0_Name_0``) para trazabilidad;
    ``label`` es la versión legible (``Name``) que se muestra y se usa como clave en
    ``client.lead_form_data``; ``value`` es el valor tal cual lo mandó el cliente
    (string casi siempre, pero puede ser lista/num — no se coerciona)."""
    key: str
    label: str
    value: Any = None

    def value_text(self) -> str:
        return _value_to_text(self.value)


class ChattyContentInteractive(BaseModel):

    # --- salida ---------------------------------------------------------------------------------
    # Un interactivo de ENTRADA es una respuesta (qué botón tocó el cliente); uno de SALIDA es un
    # pedido (elegí una opción, mandame tu ubicación). `prompt` lleva el pedido cuando el mensaje sale
    # de Chatty, y queda en None en todo lo que entra. Se guarda como dict para que el modelo del
    # paquete no dependa de los payloads de api-chatty, que son detalle del gateway.
    prompt: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Sólo en mensajes SALIENTES: el interactivo que se pidió (botones, lista, etc.)")
    interactive_type: str = Field(default="unknown", description="nfm_reply | button_reply | list_reply | el tipo crudo de una forma futura de Meta")
    body: str = Field(default="", description="Resumen legible en español — lo que ven previews, IA, checkers de fuente y exports")
    title: Optional[str] = Field(default=None, description="button_reply/list_reply: el texto visible que el cliente eligió")
    reply_id: Optional[str] = Field(default=None, description="button_reply/list_reply: el id de developer del botón/fila")
    description: Optional[str] = Field(default=None, description="list_reply: la descripción de la fila elegida")
    form_fields: List[InteractiveFormField] = Field(default_factory=list, description="nfm_reply: los pares campo/valor del formulario, con labels ya limpios")
    flow_token: Optional[str] = Field(default=None)
    flow_id: Optional[str] = Field(default=None)
    flow_name: Optional[str] = Field(default=None, description="nfm_reply.name — el nombre del Flow según Meta (suele ser 'flow')")
    raw: Optional[Dict[str, Any]] = Field(default=None, description="El dict `interactive` original del webhook, para debugging y formas futuras")

    def get_body_or_caption(self) -> str:
        return self.body or "El cliente envió un mensaje interactivo"

    def form_data(self) -> Dict[str, Any]:
        """``{label legible: valor}`` — la forma que se mergea en ``client.lead_form_data``.
        Ante labels repetidos gana el último (mismo criterio last-write-wins que el merge
        de lead_form_data en ChatService)."""
        return {field.label: field.value for field in self.form_fields}

    # ------------------------------------------------------------------
    # Construcción desde el webhook de Meta
    # ------------------------------------------------------------------

    @classmethod
    def from_meta(cls, meta_interactive: Any) -> "ChattyContentInteractive":
        """Construye el contenido desde el `interactive` del webhook (el modelo
        MetaInteractiveContent o el dict crudo). NUNCA lanza: cualquier forma
        inesperada degrada a un contenido genérico con ``raw`` preservado."""
        try:
            data = cls._as_dict(meta_interactive)
            interactive_type = str(data.get("type") or cls._infer_type(data) or "unknown")
            if interactive_type == "nfm_reply":
                return cls._from_nfm_reply(data)
            if interactive_type in ("button_reply", "list_reply"):
                return cls._from_reply(data, interactive_type)
            return cls(
                interactive_type=interactive_type,
                body="El cliente envió un mensaje interactivo",
                raw=data or None,
            )
        except Exception as e:  # noqa: BLE001 — la tolerancia es el contrato (webhook nunca 5xx)
            logger.warning("ChattyContentInteractive.from_meta degraded to generic content: %s", e)
            return cls(
                interactive_type="unknown",
                body="El cliente envió un mensaje interactivo",
                raw=cls._safe_raw(meta_interactive),
            )

    @staticmethod
    def _as_dict(meta_interactive: Any) -> Dict[str, Any]:
        if meta_interactive is None:
            return {}
        if isinstance(meta_interactive, dict):
            return meta_interactive
        if hasattr(meta_interactive, "model_dump"):
            # MetaInteractiveContent declara extra="allow": el dump trae también
            # nfm_reply/button_reply/list_reply aunque no estén declarados como campos.
            return meta_interactive.model_dump(exclude_none=True)
        return {}

    @staticmethod
    def _safe_raw(meta_interactive: Any) -> Optional[Dict[str, Any]]:
        try:
            raw = ChattyContentInteractive._as_dict(meta_interactive)
            # El raw viaja a Mongo: garantizamos que sea JSON-serializable.
            return json.loads(json.dumps(raw, ensure_ascii=False, default=str)) or None
        except Exception:
            return None

    @staticmethod
    def _infer_type(data: Dict[str, Any]) -> Optional[str]:
        for candidate in ("nfm_reply", "button_reply", "list_reply"):
            if isinstance(data.get(candidate), dict):
                return candidate
        return None

    @classmethod
    def _from_reply(cls, data: Dict[str, Any], interactive_type: str) -> "ChattyContentInteractive":
        reply = data.get(interactive_type)
        reply = reply if isinstance(reply, dict) else {}
        title = str(reply.get("title")) if reply.get("title") is not None else None
        description = str(reply.get("description")) if reply.get("description") is not None else None
        # El body ES el texto elegido: es literalmente lo que el cliente "dijo", y es
        # lo que los checkers literal/similarity pueden matchear contra smart messages.
        body = title or "El cliente respondió desde un menú interactivo"
        return cls(
            interactive_type=interactive_type,
            body=body,
            title=title,
            reply_id=str(reply.get("id")) if reply.get("id") is not None else None,
            description=description,
            raw=data or None,
        )

    @classmethod
    def _from_nfm_reply(cls, data: Dict[str, Any]) -> "ChattyContentInteractive":
        nfm = data.get("nfm_reply")
        nfm = nfm if isinstance(nfm, dict) else {}
        response = cls._parse_response_json(nfm.get("response_json"))
        flow_token = response.get("flow_token")
        flow_id = response.get("flow_id")
        form_fields = [
            InteractiveFormField(key=key, label=clean_flow_field_key(key), value=value)
            for key, value in response.items()
            if key not in _FLOW_METADATA_KEYS
        ]
        if form_fields:
            lines = [f"{f.label}: {f.value_text()}" for f in form_fields]
            body = "Completó el formulario:\n" + "\n".join(lines)
        else:
            # Flow sin campos o response_json roto: el nfm_reply.body de Meta ("Sent")
            # no le dice nada a un humano — dejamos constancia explícita.
            body = "Completó un formulario (contenido no disponible)"
        return cls(
            interactive_type="nfm_reply",
            body=body,
            form_fields=form_fields,
            flow_token=str(flow_token) if flow_token is not None else None,
            flow_id=str(flow_id) if flow_id is not None else None,
            flow_name=str(nfm.get("name")) if nfm.get("name") is not None else None,
            raw=data or None,
        )

    @staticmethod
    def _parse_response_json(response_json: Any) -> Dict[str, Any]:
        """El ``response_json`` de Meta es un STRING con JSON adentro. Tolerante:
        también acepta un dict ya parseado; cualquier otra cosa (None, JSON roto,
        un JSON que no es objeto) devuelve {} y el caller degrada el body."""
        if isinstance(response_json, dict):
            return response_json
        if not isinstance(response_json, str) or not response_json.strip():
            return {}
        try:
            parsed = json.loads(response_json)
        except (ValueError, TypeError):
            logger.warning("nfm_reply.response_json is not valid JSON — degrading to empty form")
            return {}
        return parsed if isinstance(parsed, dict) else {}
