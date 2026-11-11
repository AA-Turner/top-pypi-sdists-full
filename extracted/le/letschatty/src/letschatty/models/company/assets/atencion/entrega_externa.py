"""Entregas de las acciones externas: qué se manda, el log de cada envío y la respuesta (0.6.57.1).

Diseño: api-chatty `docs/precalificacion-con-accion-externa.md` §4.2–§4.4 y §4.8 (doc de este repo:
`docs/acciones-externas.md`).

- `PayloadDeEntrega`: el cuerpo JSON del POST (§4.2). Lo firma api-chatty con Standard Webhooks
  (`webhook-id` = `id`, `webhook-timestamp`, `webhook-signature`).
- `EntregaExterna`: un documento por envío en `entregas_externas` (TTL 90 días). `_id` es el `id` del
  payload, determinístico por hecho (`id_de_entrega`): una rama re-aplicada no duplica (unique por
  `_id`) y un reintento manda el mismo `id`, que el receptor usa como clave de idempotencia.
- `RespuestaExterna`: lo que puede contestar el sistema externo, síncrono (cuerpo del 2xx) o asíncrono
  (`POST …/entregas/{id}/respuesta`). `leer_respuesta` aplica los topes: lo que no cumple se DESCARTA con
  motivo (va al log) y el resto se aplica.

Las reglas de reintento (`proximo_intento_en`, `es_reintentable`) viven acá para que api-chatty y
cualquier otro lector cuenten igual.
"""
import hashlib
import json
import re
from datetime import datetime, timedelta
from enum import StrEnum
from typing import Any, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator

from letschatty.models.utils.types.identifier import StrObjectId

from ..destino_externo import validar_url_de_destino
from .accion_externa import CuandoAccionExterna
from .turno import Turno

# --------------------------------------------------------------------------- qué se manda (§4.2)

#: El `tipo` del payload. «prueba» es el botón «Probar» del destino. Mover y cancelar un turno
#: (`atencion.turno.movido` / `.cancelado`) son v2.
TIPO_CALIFICA = "atencion.precalificacion.califica"
TIPO_NO_CALIFICA = "atencion.precalificacion.no_califica"
TIPO_TURNO_AGENDADO = "atencion.turno.agendado"
TIPO_PRUEBA = "prueba"
TipoDeEntrega = Literal[
    "atencion.precalificacion.califica",
    "atencion.precalificacion.no_califica",
    "atencion.turno.agendado",
    "prueba",
]
RamaDePrecalificacion = Literal["califica", "no_califica"]

PREFIJO_ID_DE_ENTREGA = "ent_"


def tipo_de_entrega(rama: RamaDePrecalificacion, cuando: CuandoAccionExterna) -> str:
    """El `tipo` del payload para una rama y un `cuando`."""
    if cuando == "al_agendar":
        return TIPO_TURNO_AGENDADO
    return TIPO_CALIFICA if rama == "califica" else TIPO_NO_CALIFICA


def id_de_entrega(
    *, company_id: str, motivo_id: str, chat_id: str, turno_id: str, rama: str, tipo: str
) -> str:
    """El `id` determinístico de una entrega (= `webhook-id` = `_id` del documento).

    El mismo hecho da el mismo id (un reintento, una rama re-aplicada); una precalificación nueva del
    mismo chat (otro `turno_id`) es otro id a propósito: el receptor decide si da lo mismo. `tipo` entra
    en el hash para que el aviso `al_agendar` y el de la rama nunca choquen."""
    partes = [company_id, motivo_id, chat_id, turno_id, rama, tipo]
    if any(not str(p).strip() for p in partes):
        raise ValueError("El id de la entrega necesita empresa, motivo, chat, turno, rama y tipo")
    crudo = "\x1f".join(str(p).strip() for p in partes)
    return PREFIJO_ID_DE_ENTREGA + hashlib.sha256(crudo.encode("utf-8")).hexdigest()[:32]


class _Abierto(BaseModel):
    """Lo que leemos de afuera o mandamos afuera: ignorar campos de más (un receptor nuevo no rompe)."""

    model_config = ConfigDict(extra="ignore")


class EmpresaDelPayload(_Abierto):
    id: StrObjectId
    nombre: str


class CuentaDelPayload(_Abierto):
    id: Optional[StrObjectId] = None
    telefono: Optional[str] = None


class MotivoDelPayload(_Abierto):
    id: StrObjectId
    nombre: str


class ContactoDelPayload(_Abierto):
    nombre: Optional[str] = None
    telefono: Optional[str] = None
    bsuid: Optional[str] = None


class ChatDelPayload(_Abierto):
    id: StrObjectId
    contacto: ContactoDelPayload = Field(default_factory=ContactoDelPayload)
    url: Optional[str] = None


class PrecalificacionDelPayload(_Abierto):
    razon: str = ""
    aprobado_por: str = Field(description="«ia» si decidió la IA sola, o el user_id de quien aprobó")


class ResponderA(_Abierto):
    """Para la respuesta ASÍNCRONA (§4.4 b; v1 o v2 está abierto, §7): a dónde y con qué token. El token
    sirve para ESA entrega (un chat, una vez, 72 h) y no es una API key. api-chatty guarda sólo su hash;
    el token en claro viaja únicamente en el cuerpo del POST."""

    url: str
    token: str
    vence: datetime


class PayloadDeEntrega(_Abierto):
    tipo: TipoDeEntrega
    id: str = Field(description="= webhook-id; clave de idempotencia")
    fecha: datetime
    empresa: EmpresaDelPayload
    cuenta: Optional[CuentaDelPayload] = None
    motivo: Optional[MotivoDelPayload] = None
    rama: Optional[RamaDePrecalificacion] = None
    chat: Optional[ChatDelPayload] = None
    datos: dict[str, Any] = Field(default_factory=dict, description="Sólo los datos que declara la rama")
    precalificacion: Optional[PrecalificacionDelPayload] = None
    turno: Optional[Turno] = Field(default=None, description="Sólo en atencion.turno.agendado")
    responder_a: Optional[ResponderA] = None

    @model_validator(mode="after")
    def _validar(self) -> "PayloadDeEntrega":
        if not self.id.startswith(PREFIJO_ID_DE_ENTREGA):
            raise ValueError(f"El id de una entrega empieza con «{PREFIJO_ID_DE_ENTREGA}»")
        if self.tipo == TIPO_PRUEBA:
            return self
        if self.motivo is None or self.rama is None or self.chat is None:
            raise ValueError("Una entrega de atención lleva motivo, rama y chat")
        if (self.tipo == TIPO_TURNO_AGENDADO) != (self.turno is not None):
            raise ValueError("El turno va en atencion.turno.agendado, y sólo ahí")
        if self.tipo == TIPO_CALIFICA and self.rama != "califica":
            raise ValueError("atencion.precalificacion.califica es de la rama califica")
        if self.tipo == TIPO_NO_CALIFICA and self.rama != "no_califica":
            raise ValueError("atencion.precalificacion.no_califica es de la rama no_califica")
        return self


# --------------------------------------------------------------------------- la respuesta (§4.4)

#: Topes de la respuesta. Lo que no cumple se descarta con motivo en el log; el resto se aplica.
MAX_MENSAJES_DE_RESPUESTA = 5
MAX_LARGO_TEXTO_DE_RESPUESTA = 4096
MAX_ETIQUETAS_DE_RESPUESTA = 10
MAX_DATOS_DE_RESPUESTA = 20
MAX_LARGO_DATO_DE_RESPUESTA = 500
MAX_BYTES_CUERPO_DE_RESPUESTA = 64 * 1024
MAX_LARGO_NOMBRE_ETIQUETA = 100
_CLAVE_DE_DATO = re.compile(r"^[a-z0-9_]{1,64}$")

ResultadoDeRespuesta = Literal["ok", "rechazado"]


class MensajeTexto(BaseModel):
    tipo: Literal["texto"] = "texto"
    texto: str = Field(min_length=1, max_length=MAX_LARGO_TEXTO_DE_RESPUESTA)

    @field_validator("texto")
    @classmethod
    def _texto(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El mensaje de texto está vacío")
        return v


class MensajeImagen(BaseModel):
    tipo: Literal["imagen"] = "imagen"
    url: str = Field(description="https; api-chatty la baja y la valida por el camino de media de siempre")
    texto: Optional[str] = Field(default=None, max_length=MAX_LARGO_TEXTO_DE_RESPUESTA, description="El epígrafe")

    @field_validator("url")
    @classmethod
    def _url(cls, v: str) -> str:
        return validar_url_de_destino(v)


MensajeDeRespuesta = Union[MensajeTexto, MensajeImagen]


class RespuestaExterna(BaseModel):
    """La respuesta YA ACOTADA. Construirla directo valida los topes y LANZA; para leer lo que mandó un
    sistema externo usá `leer_respuesta`, que descarta lo que no cumple y aplica el resto."""

    model_config = ConfigDict(extra="ignore")

    resultado: ResultadoDeRespuesta = "ok"
    mensajes: list[MensajeDeRespuesta] = Field(default_factory=list, max_length=MAX_MENSAJES_DE_RESPUESTA)
    etiquetas: list[str] = Field(
        default_factory=list, max_length=MAX_ETIQUETAS_DE_RESPUESTA,
        description="Nombres de etiquetas que YA existen en la empresa (no se crean desde afuera)",
    )
    datos: dict[str, str] = Field(
        default_factory=dict, description="Van a lead_form_data; sólo field_keys que ya existen en la empresa"
    )

    @field_validator("etiquetas")
    @classmethod
    def _etiquetas(cls, v: list[str]) -> list[str]:
        limpias = [" ".join(e.split()) for e in v]
        if any(not e or len(e) > MAX_LARGO_NOMBRE_ETIQUETA for e in limpias):
            raise ValueError("Una etiqueta de la respuesta está vacía o es muy larga")
        if len({e.casefold() for e in limpias}) != len(limpias):
            raise ValueError("Hay una etiqueta repetida en la respuesta")
        return limpias

    @field_validator("datos")
    @classmethod
    def _datos(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) > MAX_DATOS_DE_RESPUESTA:
            raise ValueError(f"Hasta {MAX_DATOS_DE_RESPUESTA} datos en la respuesta")
        for clave, valor in v.items():
            if not _CLAVE_DE_DATO.match(clave):
                raise ValueError(f"«{clave}» no es un campo del contacto válido")
            if len(valor) > MAX_LARGO_DATO_DE_RESPUESTA:
                raise ValueError(f"El dato «{clave}» tiene hasta {MAX_LARGO_DATO_DE_RESPUESTA} caracteres")
        return v

    @property
    def vacia(self) -> bool:
        return not (self.mensajes or self.etiquetas or self.datos)


class Descarte(BaseModel):
    """Una parte de la respuesta que no se aplicó, y por qué (va al log de la entrega)."""

    donde: str = Field(description="«mensajes[2]», «etiquetas[0]», «datos.numero», «cuerpo»…")
    motivo: str


class RespuestaLeida(BaseModel):
    respuesta: RespuestaExterna
    descartes: list[Descarte] = Field(default_factory=list)


def _como_texto_de_dato(valor: Any) -> Optional[str]:
    if isinstance(valor, bool):
        return "true" if valor else "false"
    if isinstance(valor, (str, int, float)):
        return str(valor)
    return None


def leer_respuesta(cuerpo: Union[bytes, str, dict, None]) -> RespuestaLeida:
    """Lee lo que contestó el sistema externo y aplica los topes de §4.4: hasta 5 mensajes, 4.096
    caracteres por texto, 10 etiquetas, 20 datos y un cuerpo de hasta 64 KB. Lo que no cumple se
    descarta con su motivo y lo demás se aplica. Un cuerpo vacío, que no es JSON o que no es un objeto
    es una respuesta vacía (la entrega igual fue un éxito: el 2xx es lo que cuenta).

    Que las etiquetas y los campos EXISTAN en la empresa lo chequea api-chatty (necesita la base)."""
    descartes: list[Descarte] = []
    if cuerpo is None or cuerpo == b"" or cuerpo == "":
        return RespuestaLeida(respuesta=RespuestaExterna())
    if isinstance(cuerpo, (bytes, str)):
        crudo = cuerpo.encode("utf-8") if isinstance(cuerpo, str) else cuerpo
        if len(crudo) > MAX_BYTES_CUERPO_DE_RESPUESTA:
            return RespuestaLeida(
                respuesta=RespuestaExterna(),
                descartes=[Descarte(donde="cuerpo", motivo=f"más de {MAX_BYTES_CUERPO_DE_RESPUESTA} bytes")],
            )
        try:
            cuerpo = json.loads(crudo)
        except (UnicodeDecodeError, json.JSONDecodeError):
            return RespuestaLeida(respuesta=RespuestaExterna(), descartes=[Descarte(donde="cuerpo", motivo="no es JSON")])
    if not isinstance(cuerpo, dict):
        return RespuestaLeida(respuesta=RespuestaExterna(), descartes=[Descarte(donde="cuerpo", motivo="no es un objeto JSON")])

    resultado = cuerpo.get("resultado", "ok")
    if resultado not in ("ok", "rechazado"):
        descartes.append(Descarte(donde="resultado", motivo=f"«{resultado}» no es ok ni rechazado: se toma ok"))
        resultado = "ok"

    mensajes: list[MensajeDeRespuesta] = []
    crudos = cuerpo.get("mensajes") or []
    if not isinstance(crudos, list):
        descartes.append(Descarte(donde="mensajes", motivo="no es una lista"))
        crudos = []
    for i, m in enumerate(crudos):
        donde = f"mensajes[{i}]"
        if len(mensajes) >= MAX_MENSAJES_DE_RESPUESTA:
            descartes.append(Descarte(donde=donde, motivo=f"más de {MAX_MENSAJES_DE_RESPUESTA} mensajes"))
            continue
        tipo = m.get("tipo") if isinstance(m, dict) else None
        modelo = {"texto": MensajeTexto, "imagen": MensajeImagen}.get(tipo) if isinstance(tipo, str) else None
        if modelo is None:
            descartes.append(Descarte(donde=donde, motivo=f"tipo de mensaje desconocido: {tipo!r}"))
            continue
        try:
            mensajes.append(modelo.model_validate(m))
        except ValidationError as e:
            descartes.append(Descarte(donde=donde, motivo=_primer_error(e)))

    etiquetas: list[str] = []
    vistas: set[str] = set()
    crudas = cuerpo.get("etiquetas") or []
    if not isinstance(crudas, list):
        descartes.append(Descarte(donde="etiquetas", motivo="no es una lista"))
        crudas = []
    for i, e in enumerate(crudas):
        donde = f"etiquetas[{i}]"
        nombre = " ".join(e.split()) if isinstance(e, str) else ""
        if not nombre or len(nombre) > MAX_LARGO_NOMBRE_ETIQUETA:
            descartes.append(Descarte(donde=donde, motivo="no es un nombre de etiqueta válido"))
        elif nombre.casefold() in vistas:
            descartes.append(Descarte(donde=donde, motivo="repetida"))
        elif len(etiquetas) >= MAX_ETIQUETAS_DE_RESPUESTA:
            descartes.append(Descarte(donde=donde, motivo=f"más de {MAX_ETIQUETAS_DE_RESPUESTA} etiquetas"))
        else:
            etiquetas.append(nombre)
            vistas.add(nombre.casefold())

    datos: dict[str, str] = {}
    crudos_d = cuerpo.get("datos") or {}
    if not isinstance(crudos_d, dict):
        descartes.append(Descarte(donde="datos", motivo="no es un objeto"))
        crudos_d = {}
    for clave, valor in crudos_d.items():
        donde = f"datos.{clave}"
        texto = _como_texto_de_dato(valor)
        if not isinstance(clave, str) or not _CLAVE_DE_DATO.match(clave):
            descartes.append(Descarte(donde=donde, motivo="no es un campo del contacto válido"))
        elif texto is None:
            descartes.append(Descarte(donde=donde, motivo="el valor no es texto ni número"))
        elif len(texto) > MAX_LARGO_DATO_DE_RESPUESTA:
            descartes.append(Descarte(donde=donde, motivo=f"más de {MAX_LARGO_DATO_DE_RESPUESTA} caracteres"))
        elif len(datos) >= MAX_DATOS_DE_RESPUESTA:
            descartes.append(Descarte(donde=donde, motivo=f"más de {MAX_DATOS_DE_RESPUESTA} datos"))
        else:
            datos[clave] = texto

    respuesta = RespuestaExterna(resultado=resultado, mensajes=mensajes, etiquetas=etiquetas, datos=datos)
    return RespuestaLeida(respuesta=respuesta, descartes=descartes)


def _primer_error(e: ValidationError) -> str:
    err = e.errors()[0]
    return str(err.get("msg", "no cumple")).removeprefix("Value error, ")


# --------------------------------------------------------------------------- la entrega (§4.3)


class EstadoEntrega(StrEnum):
    PENDIENTE = "pendiente"
    ENVIANDO = "enviando"
    ENTREGADA = "entregada"
    RESPONDIDA_APLICADA = "respondida_aplicada"
    FALLIDA = "fallida"
    DESCARTADA = "descartada"


#: Estados de los que ya no se sale solo («Reintentar» de una fallida la vuelve a pendiente a mano).
ESTADOS_FINALES = frozenset({EstadoEntrega.RESPONDIDA_APLICADA, EstadoEntrega.FALLIDA, EstadoEntrega.DESCARTADA})

#: Backoff entre intentos: 30 s, 2 min, 10 min, 1 h, 6 h → fallida. Son 6 intentos en total.
BACKOFF_SEGUNDOS = (30, 120, 600, 3600, 21600)
MAX_INTENTOS = len(BACKOFF_SEGUNDOS) + 1
#: Cuánto se guarda del cuerpo que contestó el receptor en cada intento.
MAX_BYTES_CUERPO_EN_LOG = 2048
#: Cuántos días vive una entrega (índice TTL sobre `created_at`).
DIAS_DE_VIDA_DE_LA_ENTREGA = 90
#: Lo que espera el «enviar» de la rama a la respuesta con `esperar_respuesta` (§7: propuesto).
SEGUNDOS_DE_ESPERA_DE_LA_RESPUESTA = 30


def es_reintentable(status: Optional[int]) -> bool:
    """¿Se reintenta? Sí en errores de red (sin status), 5xx, 408 y 429. Un 2xx es éxito y cualquier otro
    4xx es `fallida` de una (el receptor dijo que no)."""
    if status is None:
        return True
    return status >= 500 or status in (408, 429)


def proximo_intento_en(
    intentos_hechos: int, ahora: datetime, retry_after_s: Optional[int] = None
) -> Optional[datetime]:
    """Cuándo va el próximo intento después de `intentos_hechos` intentos fallidos, o None si ya no hay
    más (pasa a `fallida`). Con `Retry-After` (429) se respeta, pero nunca menos que el backoff."""
    if intentos_hechos < 1 or intentos_hechos > len(BACKOFF_SEGUNDOS):
        return None
    espera = BACKOFF_SEGUNDOS[intentos_hechos - 1]
    if retry_after_s is not None and retry_after_s > espera:
        espera = min(retry_after_s, BACKOFF_SEGUNDOS[-1])
    return ahora + timedelta(seconds=espera)


class IntentoDeEntrega(BaseModel):
    at: datetime
    status: Optional[int] = Field(default=None, description="El status HTTP; None = error de red o timeout")
    ms: int = Field(ge=0, description="Cuánto tardó")
    error: Optional[str] = Field(default=None, max_length=500)
    cuerpo_truncado: Optional[str] = Field(
        default=None, description=f"Lo que contestó el receptor, hasta {MAX_BYTES_CUERPO_EN_LOG} bytes. Nunca los headers de firma"
    )

    @field_validator("cuerpo_truncado")
    @classmethod
    def _truncar(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        crudo = v.encode("utf-8")
        if len(crudo) <= MAX_BYTES_CUERPO_EN_LOG:
            return v
        return crudo[:MAX_BYTES_CUERPO_EN_LOG].decode("utf-8", errors="ignore")


class RespuestaAplicada(BaseModel):
    """Lo que se aplicó de la respuesta (una sola vez por entrega, venga por el camino que venga)."""

    at: datetime
    camino: Literal["sincrona", "asincrona"]
    resultado: ResultadoDeRespuesta = "ok"
    mensajes: int = Field(default=0, ge=0, description="Cuántos mensajes salieron")
    etiquetas: list[str] = Field(default_factory=list)
    datos: list[str] = Field(default_factory=list, description="Qué campos se escribieron")
    descartes: list[Descarte] = Field(default_factory=list)
    ventana_cerrada: bool = Field(default=False, description="Los textos no salieron: la ventana de 24 h estaba cerrada")


class EntregaExterna(BaseModel):
    """Un envío a un destino externo (`entregas_externas`). La escribe sólo api-chatty: `aplicar_rama`
    INSERTA (pendiente) y un despachador la reclama con lease, la manda y anota cada intento."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id", description="= payload.id (determinístico, `id_de_entrega`)")
    company_id: StrObjectId
    destino_id: StrObjectId
    chat_id: Optional[StrObjectId] = Field(default=None, description="None sólo en una entrega «prueba»")
    motivo_id: Optional[StrObjectId] = None
    rama: Optional[RamaDePrecalificacion] = None
    cuando: Optional[CuandoAccionExterna] = None
    payload: PayloadDeEntrega
    estado: EstadoEntrega = EstadoEntrega.PENDIENTE
    motivo_descarte: Optional[str] = Field(default=None, description="Por qué quedó descartada (p. ej. falta un dato obligatorio)")
    intentos: list[IntentoDeEntrega] = Field(default_factory=list)
    proximo_intento_at: Optional[datetime] = None
    lease_hasta: Optional[datetime] = None
    respuesta_aplicada: Optional[RespuestaAplicada] = None
    responder_token_hash: Optional[str] = Field(default=None, description="Hash del token de la respuesta asíncrona")
    created_at: datetime
    updated_at: datetime

    @model_validator(mode="after")
    def _validar(self) -> "EntregaExterna":
        if self.id != self.payload.id:
            raise ValueError("El _id de la entrega es el id del payload")
        if self.payload.tipo != TIPO_PRUEBA and self.chat_id is None:
            raise ValueError("Una entrega de atención es de un chat")
        if self.estado == EstadoEntrega.DESCARTADA and not self.motivo_descarte:
            raise ValueError("Una entrega descartada dice por qué")
        if self.estado == EstadoEntrega.RESPONDIDA_APLICADA and self.respuesta_aplicada is None:
            raise ValueError("Una entrega respondida_aplicada trae lo que se aplicó")
        return self

    @property
    def final(self) -> bool:
        return self.estado in ESTADOS_FINALES
