"""Estilo de los mensajes: la regla dura «sin ¿ ¡» y «sin rayas largas».

Muchos clientes no quieren signos de apertura (¿ ¡) ni rayas (— –) en lo que la empresa
manda por WhatsApp: delatan texto escrito por una IA. Pedírselo al modelo no alcanza (MA
Distribución, 19-nov-2026: «Sin signos de apertura, como pediste» sobre un «¿me contás…?»),
así que, si la empresa lo marca en `MessagingSettings`, el texto se limpia SIEMPRE antes de
guardarlo o de enviarlo.

Función pura y sin dependencias: este archivo se copia tal cual en cintia-lambdas
(`shared/shared/cintia_lambdas/services/estilo_de_mensajes.py`) con los mismos tests. Si
cambia acá, cambia allá.

Qué hace:
- «¿» y «¡» se borran; la letra que sigue queda como está.
- Raya «—» / «–» (y «―»):
  - entre espacios («hola — chau») → «, » (si antes ya hay puntuación, sólo un espacio);
  - de inciso («Él —dijo— vino») → «Él, dijo, vino»;
  - pegada entre palabras o números («9–18», «a—b») → «-»;
  - entre números con espacios («9 – 18») → «9 - 18» (es un rango, no una pausa);
  - al principio de línea (diálogo o lista) → «- »; sola en la línea → se saca;
  - al final de una línea → se saca.

Qué NO toca: el guion común «-», URLs, mails, variables `{{1}}` / `{cuando_atienden}` y
código entre comillas invertidas (``` o `).
"""

from __future__ import annotations

import re
from dataclasses import dataclass

SIGNOS_DE_APERTURA = "¿¡"
RAYAS = "—–―"

_PROTEGIDO = re.compile(
    r"```.*?```"                      # bloque de código / monoespaciado de WhatsApp
    r"|`[^`\n]+`"                     # código en línea
    r"|\{\{.*?\}\}"                   # variables de plantilla {{1}}
    r"|\{[A-Za-z_][A-Za-z0-9_]*\}"    # tokens {cuando_atienden}
    r"|\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+"  # mails
    r"|(?:https?://|www\.)\S+",       # URLs
    re.DOTALL,
)
_SIGNO = re.compile(f"[{SIGNOS_DE_APERTURA}]")
_RAYA = re.compile(f"(?P<pre>[ \\t]*)(?P<raya>[{RAYAS}]+)(?P<post>[ \\t]*)")
_PUNTUACION_ANTES = ",;:.!?(«\"'"
_PUNTUACION_DESPUES = ",;:.!?)»\"'"


@dataclass(frozen=True)
class ResultadoDeEstilo:
    texto: str
    signos_quitados: int = 0
    rayas_quitadas: int = 0

    @property
    def cambio(self) -> bool:
        return bool(self.signos_quitados or self.rayas_quitadas)


def _tramos_protegidos(texto: str) -> list[tuple[int, int]]:
    return [m.span() for m in _PROTEGIDO.finditer(texto)]


def _protegido(tramos: list[tuple[int, int]], inicio: int, fin: int) -> bool:
    return any(a < fin and inicio < b for a, b in tramos)


def _reemplazo_de_raya(texto: str, m: re.Match[str]) -> str:
    pre, post = m.group("pre"), m.group("post")
    antes, despues = texto[: m.start()], texto[m.end():]
    inicio_de_linea = antes == "" or antes.endswith("\n")
    fin_de_linea = despues == "" or despues.startswith(("\n", "\r"))

    if inicio_de_linea:
        return pre if fin_de_linea else pre + "- "
    if fin_de_linea:
        return ""
    anterior, siguiente = antes[-1], despues[0]
    if anterior.isdigit() and siguiente.isdigit():
        return pre + "-" + post
    if not pre and not post and siguiente not in _PUNTUACION_DESPUES:
        return "-"
    if anterior in _PUNTUACION_ANTES:
        return " "
    if siguiente in _PUNTUACION_DESPUES:
        return ""
    return ", "


def limpiar_estilo(
    texto: str | None,
    *,
    sin_signos_de_apertura: bool = False,
    sin_rayas: bool = False,
) -> ResultadoDeEstilo:
    """Limpia el texto según el estilo de la empresa y cuenta lo que sacó."""
    if not texto or not (sin_signos_de_apertura or sin_rayas):
        return ResultadoDeEstilo(texto=texto or "")

    signos = rayas = 0

    if sin_rayas:
        tramos = _tramos_protegidos(texto)

        def _raya(m: re.Match[str]) -> str:
            nonlocal rayas
            if _protegido(tramos, m.start("raya"), m.end("raya")):
                return m.group(0)
            rayas += len(m.group("raya"))
            return _reemplazo_de_raya(texto, m)

        texto = _RAYA.sub(_raya, texto)

    if sin_signos_de_apertura:
        tramos = _tramos_protegidos(texto)

        def _signo(m: re.Match[str]) -> str:
            nonlocal signos
            if _protegido(tramos, m.start(), m.end()):
                return m.group(0)
            signos += 1
            return ""

        texto = _SIGNO.sub(_signo, texto)

    return ResultadoDeEstilo(texto=texto, signos_quitados=signos, rayas_quitadas=rayas)


def aplicar_estilo(
    texto: str | None,
    *,
    sin_signos_de_apertura: bool = False,
    sin_rayas: bool = False,
) -> str:
    """Igual que `limpiar_estilo`, pero devuelve sólo el texto."""
    return limpiar_estilo(
        texto, sin_signos_de_apertura=sin_signos_de_apertura, sin_rayas=sin_rayas
    ).texto


def describir_cambios(signos: int, rayas: int) -> str | None:
    """Una frase para avisarle a quien escribió el texto (app, MCP, Lucía)."""
    partes = []
    if signos:
        partes.append(f"{signos} signo{'s' if signos != 1 else ''} de apertura (¿ ¡)")
    if rayas:
        partes.append(f"{rayas} raya{'s' if rayas != 1 else ''} (— –)")
    if not partes:
        return None
    return "Se sacaron " + " y ".join(partes) + ": la empresa los tiene desactivados."
