"""Recetas de motivo y plantillas de industria.

Son documentos globales (colecciones `recetas_de_motivo` y `plantillas_de_industria`): una
receta o una plantilla nueva es un documento, no un deploy. El motivo de una receta se guarda
como diccionario porque lleva referencias a ids que todavía no existen y huecos (`{{clave}}`) que
completa cada empresa.

Dos clases de referencia, las dos como el string ENTERO de un valor (un `@ref:` o un `@empresa:` en
el medio de un texto es texto, no se resuelve):
- `"@ref:<ref>"` — una respuesta rápida que la receta trae en `respuestas_rapidas` y que se crea al
  aplicarla.
- `"@empresa:<clave>"` — algo que es de cada empresa y la receta no puede crear: la estrategia de
  seguimiento de «seguimientos de IA», la capacidad de una acción personalizada, un agente. Toda
  clave usada va declarada en `de_la_empresa` y toda declarada se usa: así quien aplica sabe
  exactamente qué pedirle a la empresa.

Quien aplica: (1) completa huecos, (2) crea las respuestas rápidas, (3) le pide a la empresa sus
ids de `de_la_empresa`, (4) resuelve las dos clases de referencia (`resolver_referencias`),
(5) valida el resultado como `Motivo`.

Lo que se puede revisar sin la empresa se revisa AL CARGAR el documento, no al aplicarlo:
- Referencias: las `@ref:` apuntan a una respuesta rápida de la receta; las `@empresa:` están
  declaradas en `de_la_empresa` y viceversa.
- Huecos: todo `{{…}}` que llega a un cliente o a un motivo (textos y nombres de las respuestas
  rápidas, el motivo, los textos, motivos y overrides de la plantilla) tiene que estar bien
  escrito (`{{clave}}`, minúsculas; se toleran espacios adentro) y declarado en `huecos`. Si no,
  `reemplazar_huecos` no lo tocaría y le llegaría a un cliente tal cual.
- El motivo de la receta y los overrides de la plantilla: sólo las claves de `CLAVES_DEL_MOTIVO`,
  y cada bloque se valida en seco (las dos clases de referencia y los huecos por valores de
  relleno) con el mismo modelo que usa `Motivo`. Un bloque en None es «hereda» y no se valida.
  Consecuencia: un hueco sólo puede ir donde va texto (no en un número ni en un id).
"""
import re
from enum import StrEnum
from typing import Annotated, Any, Optional

from pydantic import BaseModel, Field, StringConstraints, TypeAdapter, ValidationError, model_validator

from letschatty.models.utils.types.identifier import StrObjectId

from .accion import Accion
from .al_responder import AlResponder
from .seguimientos import Seguimientos

REF = "@ref:"
REF_EMPRESA = "@empresa:"
_CLAVE = r"[a-z][a-z0-9_]*"
_HUECO = re.compile(r"\{\{\s*(" + _CLAVE + r")\s*\}\}")
# Amplio a propósito: encuentra TODO lo que parece un hueco, bien o mal escrito, para revisarlo.
_CUALQUIER_HUECO = re.compile(r"\{\{(.*?)\}\}")
_CLAVE_OK = re.compile(r"^" + _CLAVE + r"$")

CLAVES_DEL_MOTIVO = frozenset({"respuesta", "seguimientos", "al_responder", "bienvenida_fast_answer_id"})

# Valores de relleno para validar en seco: nunca se guardan.
_ID_DE_RELLENO = "000000000000000000000000"
_TEXTO_DE_RELLENO = "hueco"
_VALIDADORES_DEL_MOTIVO: dict[str, TypeAdapter] = {
    "respuesta": TypeAdapter(Accion),
    "seguimientos": TypeAdapter(Seguimientos),
    "al_responder": TypeAdapter(AlResponder),
    "bienvenida_fast_answer_id": TypeAdapter(Optional[StrObjectId]),
}


class TipoHueco(StrEnum):
    TEXTO = "texto"
    LINK = "link"
    ARCHIVO = "archivo"
    PRECIO = "precio"


class Hueco(BaseModel):
    clave: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    etiqueta: str
    tipo: TipoHueco = TipoHueco.TEXTO
    obligatorio: bool = False


_ClaveDeEmpresa = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]*$")]


class RespuestaRapidaDeReceta(BaseModel):
    ref: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    nombre: str
    texto: str


def _strings(obj: Any) -> list[str]:
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, dict):
        return [s for v in obj.values() for s in _strings(v)]
    if isinstance(obj, list):
        return [s for v in obj for s in _strings(v)]
    return []


def _referencias(obj: Any, marca: str = REF) -> set[str]:
    return {s[len(marca):] for s in _strings(obj) if s.startswith(marca)}


def _revisar_huecos(textos: list[str], huecos: list[Hueco]) -> None:
    """Todo `{{…}}` bien escrito y declarado. El error nombra el hueco tal como está escrito."""
    declaradas = {h.clave for h in huecos}
    for texto in textos:
        for m in _CUALQUIER_HUECO.finditer(texto):
            clave = m.group(1).strip()
            if not _CLAVE_OK.match(clave):
                raise ValueError(f"Hueco mal escrito: {m.group(0)} (va en minúsculas, p. ej. {{{{precio}}}})")
            if clave not in declaradas:
                raise ValueError(f"Hueco no declarado: {m.group(0)} (agregalo a `huecos`)")


def _sin_repetidos(valores: list[str], que: str) -> None:
    repetidos = sorted({v for v in valores if valores.count(v) > 1})
    if repetidos:
        raise ValueError(f"{que} repetido: {repetidos}")


def _validar_motivo_en_seco(motivo: dict[str, Any], donde: str = "el motivo de la receta") -> None:
    """Las claves permitidas y cada bloque con el modelo de `Motivo`, con las dos clases de
    referencia y los huecos por valores de relleno. Un bloque en None es «hereda»: no se valida."""
    desconocidas = set(motivo) - CLAVES_DEL_MOTIVO
    if desconocidas:
        raise ValueError(
            f"{donde[0].upper()}{donde[1:]} tiene claves desconocidas: {sorted(desconocidas)} "
            f"(valen {sorted(CLAVES_DEL_MOTIVO)})"
        )
    relleno = _rellenar(resolver_referencias(motivo, _TodasAlRelleno(), _TodasAlRelleno()))
    for bloque, valor in relleno.items():
        if valor is None:
            continue
        try:
            _VALIDADORES_DEL_MOTIVO[bloque].validate_python(valor)
        except ValidationError as e:
            raise ValueError(f"El bloque «{bloque}» de {donde} no es válido: {e}") from None


def _rellenar(obj: Any) -> Any:
    if isinstance(obj, str):
        return _HUECO.sub(lambda _: _TEXTO_DE_RELLENO, obj)
    if isinstance(obj, dict):
        return {k: _rellenar(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_rellenar(v) for v in obj]
    return obj


class _TodasAlRelleno(dict):
    """Para `resolver_referencias` en seco: toda referencia resuelve al id de relleno."""

    def __missing__(self, key: str) -> str:
        return _ID_DE_RELLENO


class RecetaDeMotivo(BaseModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    nombre: str
    descripcion: str = ""
    huecos: list[Hueco] = Field(default_factory=list)
    respuestas_rapidas: list[RespuestaRapidaDeReceta] = Field(default_factory=list)
    de_la_empresa: list[_ClaveDeEmpresa] = Field(
        default_factory=list,
        description=(
            "Las referencias `@empresa:<clave>` que usa el motivo: ids que son de cada empresa y la "
            "receta no puede crear (estrategia de seguimiento, capacidad, agente). Quien aplica se "
            "los pide a la empresa."
        ),
    )
    motivo: dict[str, Any] = Field(
        description=(
            "respuesta / seguimientos / al_responder / bienvenida_fast_answer_id, "
            "con @ref: y @empresa: (el string entero) y {{huecos}}"
        )
    )

    @model_validator(mode="after")
    def validar(self) -> "RecetaDeMotivo":
        _sin_repetidos([h.clave for h in self.huecos], "Hueco")
        _sin_repetidos([r.ref for r in self.respuestas_rapidas], "Respuesta rápida")
        _sin_repetidos(list(self.de_la_empresa), "Referencia de la empresa")
        definidas = {r.ref for r in self.respuestas_rapidas}
        sueltas = _referencias(self.motivo) - definidas
        if sueltas:
            raise ValueError(f"La receta referencia respuestas rápidas que no define: {sorted(sueltas)}")
        usadas = _referencias(self.motivo, REF_EMPRESA)
        declaradas = set(self.de_la_empresa)
        if usadas - declaradas:
            raise ValueError(
                f"La receta usa referencias de la empresa que no declara en `de_la_empresa`: "
                f"{sorted(usadas - declaradas)}"
            )
        if declaradas - usadas:
            raise ValueError(
                f"La receta declara en `de_la_empresa` referencias que no usa: {sorted(declaradas - usadas)}"
            )
        textos = [t for r in self.respuestas_rapidas for t in (r.nombre, r.texto)]
        _revisar_huecos(textos + _strings(self.motivo), self.huecos)
        _validar_motivo_en_seco(self.motivo)
        return self


class MotivoDePlantilla(BaseModel):
    nombre: str
    frase: str = Field(description="La frase principal (description del motivo)")
    variantes: list[str] = Field(default_factory=list, description="Se cargan como triggers manuales")
    receta_id: str
    overrides: dict[str, Any] = Field(default_factory=dict, description="Pisa bloques de la receta")


class ConsultaGeneralDePlantilla(BaseModel):
    receta_id: str
    overrides: dict[str, Any] = Field(default_factory=dict)


class PlantillaDeIndustria(BaseModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]*$")
    industria: str
    nombre: str
    descripcion: str = ""
    bienvenida_texto: Optional[str] = None
    aviso_de_cerrado_texto: Optional[str] = None
    consulta_general: ConsultaGeneralDePlantilla
    motivos: list[MotivoDePlantilla] = Field(default_factory=list)
    huecos: list[Hueco] = Field(default_factory=list)

    @model_validator(mode="after")
    def validar(self) -> "PlantillaDeIndustria":
        _sin_repetidos([h.clave for h in self.huecos], "Hueco")
        textos = [t for t in (self.bienvenida_texto, self.aviso_de_cerrado_texto) if t is not None]
        textos += _strings(self.consulta_general.overrides)
        for m in self.motivos:
            textos += [m.nombre, m.frase, *m.variantes, *_strings(m.overrides)]
        _revisar_huecos(textos, self.huecos)
        # Los overrides pisan bloques del motivo: se validan como el motivo de una receta. Pueden
        # llevar @ref:/@empresa: de la receta; la plantilla no las conoce, el relleno las cubre.
        _validar_motivo_en_seco(self.consulta_general.overrides, "los overrides de «Consulta general»")
        for m in self.motivos:
            _validar_motivo_en_seco(m.overrides, f"los overrides del motivo «{m.nombre}»")
        return self


def reemplazar_huecos(obj: Any, valores: dict[str, Any]) -> Any:
    """Reemplaza `{{clave}}` en todo string, a cualquier profundidad. Cada valor se pasa a texto
    (`1500` → `"1500"`); un hueco que la empresa dejó vacío (`""`) sale vacío.

    `[clave]` es la marca de ÚLTIMO recurso, para una clave que no tiene ninguna entrada en
    `valores` (nadie la completó, o vale None): queda visible para que nadie le mande un
    `{{precio}}` a un cliente. Los obligatorios se chequean antes con `faltantes`.

    Un booleano no es un valor de hueco: le llegaría al cliente un «True». TypeError."""
    booleanos = sorted(k for k, v in valores.items() if isinstance(v, bool))
    if booleanos:
        raise TypeError(f"Un hueco no puede valer un booleano (se mandaría «True»/«False»): {booleanos}")
    return _reemplazar(obj, valores)


def _reemplazar(obj: Any, valores: dict[str, Any]) -> Any:
    if isinstance(obj, str):
        def _valor(m: re.Match) -> str:
            v = valores.get(m.group(1))
            return f"[{m.group(1)}]" if v is None else str(v)

        return _HUECO.sub(_valor, obj)
    if isinstance(obj, dict):
        return {k: _reemplazar(v, valores) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_reemplazar(v, valores) for v in obj]
    return obj


def faltantes(huecos: list[Hueco], valores: dict[str, Any]) -> list[str]:
    """Los huecos OBLIGATORIOS sin valor (o con sólo espacios). Los opcionales nunca faltan."""
    def _vacio(v: Any) -> bool:
        return v is None or not str(v).strip()

    return [h.clave for h in huecos if h.obligatorio and _vacio(valores.get(h.clave))]


def resolver_referencias(
    obj: Any, ids: dict[str, str], ids_de_empresa: Optional[dict[str, str]] = None
) -> Any:
    """Cambia cada `"@ref:<ref>"` por el id de la respuesta rápida creada (`ids`) y cada
    `"@empresa:<clave>"` por el id que dio la empresa (`ids_de_empresa`). Una referencia es el
    string ENTERO: un `@ref:` o un `@empresa:` en el medio de un texto queda como está. Una
    referencia sin id es un error del que aplica (no creó esa respuesta rápida, no le pidió ese id
    a la empresa): KeyError con la referencia entera, no un motivo a medias."""
    de_empresa = {} if ids_de_empresa is None else ids_de_empresa
    if isinstance(obj, str):
        for marca, tabla in ((REF, ids), (REF_EMPRESA, de_empresa)):
            if obj.startswith(marca):
                try:
                    return tabla[obj[len(marca):]]
                except KeyError:
                    raise KeyError(obj) from None
        return obj
    if isinstance(obj, dict):
        return {k: resolver_referencias(v, ids, de_empresa) for k, v in obj.items()}
    if isinstance(obj, list):
        return [resolver_referencias(v, ids, de_empresa) for v in obj]
    return obj
