"""La recepción: lo que pasa SIEMPRE cuando alguien escribe.

Es la capa de más abajo de la cadena `recepción → topic default → fuente → motivo`,
y existe porque hoy el default de una empresa está colgado de la **fuente por
defecto** — así que una fuente nueva no hereda nada y el default falla justo en
el caso para el que existe: lo nuevo. No falta un lugar donde ponerlo; estaba
colgado del objeto equivocado.

Hay **exactamente un documento por empresa**. No es un ABM: se lee y se edita, no se crean
varios ni se borra.

Por cuenta (número de WhatsApp): cada cuenta tiene su bienvenida, su ausencia (mensaje, horario y
zona, pausa) y su estado borrador/activo, TODO dentro de este mismo documento. Los campos de arriba
son los de la cuenta POR DEFECTO (así un lector viejo sigue viendo lo de siempre) y las demás
cuentas viven en `account_receptions` (ver `Recepcion.for_account`).
"""
import logging
from datetime import datetime, time, timedelta, timezone
from enum import StrEnum
from typing import Any, ClassVar, Literal, Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator, model_validator

from ...base_models.chatty_asset_model import ChattyAssetPreview, CompanyAssetModel
from ...utils.types import StrObjectId
from ...utils.types.serializer_type import SerializerType
from .automation import Automation

logger = logging.getLogger(__name__)


class AlcanceAusencia(StrEnum):
    """A qué chats les llega el mensaje de ausencia."""

    TODOS = "todos"
    SOLO_NUEVOS = "solo_nuevos"
    SOLO_EXISTENTES = "solo_existentes"


class AusenciaConAutomatizacion(StrEnum):
    """Qué hacer cuando el chat además dispara un envío de información.

    Callar la info y mandar sólo la ausencia es una decisión de producto, no un
    detalle: hay empresas que prefieren que el lead se lleve el material igual.
    """

    INFO_Y_AUSENCIA = "info_y_ausencia"
    SOLO_AUSENCIA = "solo_ausencia"


class AusenciaConIaAutonoma(StrEnum):
    """Qué hacer fuera de horario cuando hay un agente de IA respondiendo solo (lo elige el negocio,
    2026-10-05). En todas, como mucho UN aviso por chat por cierre, y `AlcanceAusencia` vale igual.

    - `AVISO_E_IA` (el default): sale el aviso Y la IA contesta.
    - `IA_Y_AVISO_AL_FINAL`: la IA contesta y, apenas manda su primera respuesta del cierre, sale el aviso.
    - `IA_AVISO_SI_ESCALA`: la IA contesta; el aviso sale sólo si la IA pasa el chat a una persona
      mientras está cerrado.
    - `AUSENCIA`: sale el aviso y la IA espera a que abra (cintia-creator no la corre). Se sigue
      aceptando; la pantalla no la ofrece por defecto.
    - `CONTINUA`: DEPRECADA. Era «la IA contesta, sin aviso»; se lee como `IA_AVISO_SI_ESCALA`, que la
      contiene (el validador de `Ausencia.con_ia_autonoma` la convierte), así que nunca vuelve a salir
      de un modelo. Queda en el enum para que el código que la nombra no rompa.

    No hay opción equivalente para la IA apagada: ahí el mensaje de ausencia sale
    siempre. Es la regla, no una preferencia — si no responde nadie y tampoco
    avisa nadie, el chat queda mudo.

    ⚠️ Un lector con un letschatty anterior a 0.5.3 no conoce los tres valores nuevos y falla al
    validar la recepción (cintia-creator falla abierto: la IA corre, sin saber que está cerrado).
    """

    AVISO_E_IA = "aviso_e_ia"
    IA_Y_AVISO_AL_FINAL = "ia_y_aviso_al_final"
    IA_AVISO_SI_ESCALA = "ia_aviso_si_escala"
    AUSENCIA = "ausencia"
    CONTINUA = "continua"

    @property
    def aviso_en_la_entrada(self) -> bool:
        """¿El aviso sale cuando el cliente escribe (y no después, con la respuesta o la escalada)?"""
        return self in (AusenciaConIaAutonoma.AVISO_E_IA, AusenciaConIaAutonoma.AUSENCIA)

    @property
    def ia_se_calla(self) -> bool:
        """¿La IA espera a que abra? Sólo `AUSENCIA`."""
        return self == AusenciaConIaAutonoma.AUSENCIA


class DiaSemana(StrEnum):
    LUNES = "lunes"
    MARTES = "martes"
    MIERCOLES = "miercoles"
    JUEVES = "jueves"
    VIERNES = "viernes"
    SABADO = "sabado"
    DOMINGO = "domingo"

    @classmethod
    def desde_weekday(cls, weekday: int) -> "DiaSemana":
        """`datetime.weekday()`: lunes = 0 … domingo = 6. Es el único puente entre el calendario
        de Python y la grilla; que exista una sola vez."""
        if not 0 <= weekday <= 6:
            raise ValueError(f"weekday fuera de rango: {weekday}")
        return _DIAS_EN_ORDEN[weekday]


_DIAS_EN_ORDEN = [
    DiaSemana.LUNES, DiaSemana.MARTES, DiaSemana.MIERCOLES, DiaSemana.JUEVES,
    DiaSemana.VIERNES, DiaSemana.SABADO, DiaSemana.DOMINGO,
]


class FranjaHoraria(BaseModel):
    """Un tramo de un día. `18:00 → 09:00` no existe: son dos franjas.

    Los minutos desde medianoche y no un `time` porque lo que se compara es
    "¿estoy adentro?", y con enteros esa cuenta no depende de la fecha.
    """

    desde_minuto: int = Field(ge=0, le=1440)
    hasta_minuto: int = Field(ge=0, le=1440)

    @model_validator(mode="after")
    def validate_franja(self) -> "FranjaHoraria":
        if self.hasta_minuto <= self.desde_minuto:
            raise ValueError("La franja tiene que terminar después de empezar")
        return self


class HorarioDeAtencion(BaseModel):
    """Cuándo hay alguien. Vacío = sin horario definido.

    ⚠️ `timezone` no es opcional en la práctica: "de 9 a 18" no significa nada
    para un servidor en UTC. Se guarda el nombre IANA y no un offset, porque el
    offset cambia con el horario de verano y un número congelado empieza a mentir
    en marzo.
    """

    activo: bool = Field(
        default=False, description="Si está apagado, el horario no se evalúa y manda el interruptor"
    )
    timezone: str = Field(default="America/Argentina/Buenos_Aires")
    franjas: dict[DiaSemana, list[FranjaHoraria]] = Field(default_factory=dict)

    def dias_configurados(self) -> int:
        return len([d for d, fs in self.franjas.items() if fs])

    def proxima_apertura(self, ahora_local: datetime) -> Optional[datetime]:
        """El próximo inicio de franja estrictamente después de `ahora_local`, en el mismo
        tzinfo. Si `ahora_local` cae ADENTRO de una franja devuelve el inicio de la siguiente:
        quien pregunta ya sabe que está cerrado (interruptor manual) y sólo mira adelante.
        `None` si no hay ninguna franja en la semana.

        Vive acá y no en cada consumidor porque la usan api-chatty (diferir workflows, una vez
        por cierre) y cintia-creator («hasta X»): dos implementaciones del mismo calendario
        divergen el primer feriado.

        No mira `activo`: es calendario puro; el gate (¿estamos cerrados?) es de quien
        pregunta, vía `deberia_avisar`.
        """
        if not any(self.franjas.values()):
            return None
        for offset in range(0, 8):  # hoy + 7 días cubre la semana entera
            dia = ahora_local.date() + timedelta(days=offset)
            nombre = DiaSemana.desde_weekday(dia.weekday())
            for franja in sorted(self.franjas.get(nombre) or [], key=lambda f: f.desde_minuto):
                inicio = datetime.combine(dia, time(0), tzinfo=ahora_local.tzinfo) + timedelta(
                    minutes=franja.desde_minuto
                )
                if inicio > ahora_local:
                    return inicio
        return None

    def esta_adentro(self, momento_local: datetime) -> bool:
        """¿`momento_local` cae dentro de alguna franja de su día? La misma cuenta que
        `Ausencia.deberia_avisar` (por minuto, `desde <= m < hasta`). Calendario puro: no mira `activo`."""
        franjas = self.franjas.get(DiaSemana.desde_weekday(momento_local.weekday())) or []
        minuto = momento_local.hour * 60 + momento_local.minute
        return any(f.desde_minuto <= minuto < f.hasta_minuto for f in franjas)

    def _tramos(self, centro_local: datetime) -> list[tuple[datetime, datetime]]:
        """Las franjas de la semana anterior y la siguiente a `centro_local`, como instantes en su tzinfo,
        ordenadas y con las pegadas unidas (`lunes 20–24` + `martes 0–2` es UNA atención que cruza la
        medianoche: el modelo la guarda partida, pero quien pregunta «hasta cuándo» no la ve partida)."""
        tramos: list[tuple[datetime, datetime]] = []
        for offset in range(-8, 9):
            dia = centro_local.date() + timedelta(days=offset)
            cero = datetime.combine(dia, time(0), tzinfo=centro_local.tzinfo)
            for f in self.franjas.get(DiaSemana.desde_weekday(dia.weekday())) or []:
                tramos.append((cero + timedelta(minutes=f.desde_minuto), cero + timedelta(minutes=f.hasta_minuto)))
        tramos.sort()
        unidos: list[tuple[datetime, datetime]] = []
        for inicio, fin in tramos:
            if unidos and inicio <= unidos[-1][1]:
                unidos[-1] = (unidos[-1][0], max(unidos[-1][1], fin))
            else:
                unidos.append((inicio, fin))
        return unidos

    def franja_actual(self, ahora_local: datetime) -> Optional[tuple[datetime, datetime]]:
        """(desde, hasta) de la atención en curso —con las franjas pegadas unidas—, o None si
        `ahora_local` está fuera de toda franja. Calendario puro: no mira `activo`."""
        if not self.esta_adentro(ahora_local):
            return None
        for inicio, fin in self._tramos(ahora_local):
            if inicio <= ahora_local < fin:
                return inicio, fin
        return None

    def ultimo_cierre(self, ahora_local: datetime) -> Optional[datetime]:
        """El fin de la última atención terminada antes de `ahora_local` (hasta una semana atrás), o None."""
        anteriores = [fin for _, fin in self._tramos(ahora_local) if fin <= ahora_local]
        return anteriores[-1] if anteriores else None


EstadoDeAtencion = Literal["atendiendo", "fuera_de_horario", "pausa"]


class EstadoAhora(BaseModel):
    """¿Se está atendiendo ahora? Lo que muestra «Tu atención» del home (api-chatty
    `GET …/atencion/ahora`). Las horas, en la zona del horario.

    - `atendiendo`: `desde`/`hasta` son la franja en curso (None sin horario activo).
    - `fuera_de_horario`: `desde` es el último cierre, `hasta` = `proxima_apertura`.
    - `pausa`: `hasta` es `activa_hasta` (None = sin vencimiento) y `proxima_apertura` cuándo vuelve a
      haber alguien de verdad (el fin de la pausa, o la próxima franja si la pausa termina con el local
      cerrado). `desde` no se guarda: None.

    `Literal` y no un `StrEnum` a propósito: no se persiste, y un enum nuevo entra al snapshot de
    valores guardados (`tests/enum_values_snapshot.json`) sin necesidad."""

    estado: EstadoDeAtencion
    desde: Optional[datetime] = None
    hasta: Optional[datetime] = None
    proxima_apertura: Optional[datetime] = None


def _a_utc(valor: datetime) -> datetime:
    """Naive = UTC (lo que devuelve Mongo); con zona, se pasa a UTC."""
    if valor.tzinfo is None:
        return valor.replace(tzinfo=timezone.utc)
    return valor.astimezone(timezone.utc)


class Ausencia(BaseModel):
    """Qué se contesta cuando no hay nadie.

    Dos cosas la prenden, y no son lo mismo:

    - `activa`: el interruptor **manual**. Gana siempre. Es para el feriado, el
      corte de luz y el día que cerraron antes — casos que no se modelan con una
      grilla semanal y que igual pasan.
    - `HorarioDeAtencion`: la evaluación automática, para que no dependa de que
      alguien se acuerde de prenderla y apagarla todos los días.

    La pausa manual puede tener vencimiento (`activa_hasta`, 0.5.8): está en vigor sólo si
    `activa and (activa_hasta is None or ahora < activa_hasta)` (`pausa_vigente`). Vencida se
    comporta como apagada SIN que nadie escriba nada: todo lector que decide «cerrado» pasa por
    `deberia_avisar` / `proxima_apertura` / `estado_ahora`, nunca por `activa` suelto.
    ⚠️ Un lector con un letschatty anterior a 0.5.8 ignora `activa_hasta` y ve la pausa vencida
    como prendida hasta que alguien la apague.
    """

    activa: bool = Field(default=False)
    activa_hasta: Optional[datetime] = Field(
        default=None,
        description=(
            "Hasta cuándo dura la pausa manual (UTC). None = hasta que alguien la apague. Sin "
            "`activa` no significa nada y se guarda None."
        ),
    )
    fast_answer_id: Optional[StrObjectId] = Field(
        default=None, description="El mensaje que se manda. Es una fast answer, no texto suelto."
    )
    alcance: AlcanceAusencia = Field(default=AlcanceAusencia.TODOS)
    con_automatizacion: AusenciaConAutomatizacion = Field(
        default=AusenciaConAutomatizacion.INFO_Y_AUSENCIA
    )
    con_ia_autonoma: AusenciaConIaAutonoma = Field(default=AusenciaConIaAutonoma.AVISO_E_IA)
    ia_avisa_horario_al_escalar: bool = Field(
        default=True,
        description=(
            "Con la IA respondiendo fuera de horario (todas las opciones menos AUSENCIA): si al escalar a una persona "
            "dice desde cuándo la van a atender. Booleano y no un valor más del enum a "
            "propósito: un miembro nuevo de enum rompe a los lectores con pin viejo."
        ),
    )

    horario: HorarioDeAtencion = Field(default_factory=HorarioDeAtencion)

    TOPE_REENVIO: ClassVar[timedelta] = timedelta(hours=24)

    @field_validator("con_ia_autonoma", mode="before")
    @classmethod
    def migrar_continua(cls, valor: Any) -> Any:
        """`continua` → `ia_aviso_si_escala` (ver `AusenciaConIaAutonoma`): al leer lo guardado y al
        recibirlo de un cliente viejo."""
        if valor == AusenciaConIaAutonoma.CONTINUA.value:
            return AusenciaConIaAutonoma.IA_AVISO_SI_ESCALA
        return valor

    @field_validator("activa_hasta", mode="after")
    @classmethod
    def activa_hasta_en_utc(cls, valor: Optional[datetime]) -> Optional[datetime]:
        return _a_utc(valor) if valor is not None else None

    @model_validator(mode="after")
    def validate_ausencia(self) -> "Ausencia":
        # Prenderla sin mensaje no falla en runtime: no manda nada, y el chat
        # queda igual de mudo que sin la feature. Que falle acá, donde se ve.
        if (self.activa or self.horario.activo) and not self.fast_answer_id:
            raise ValueError("Para activar la ausencia hace falta elegir el mensaje que se manda")
        if not self.activa and self.activa_hasta is not None:
            # Un vencimiento sin pausa no significa nada; que no quede uno viejo esperando a la próxima.
            self.activa_hasta = None
        return self

    def pausa_vigente(self, ahora: Optional[datetime] = None) -> bool:
        """¿La pausa manual está en vigor? `activa` y (sin vencimiento o `ahora < activa_hasta`).
        `ahora` con zona (naive = UTC); None = el reloj. En el borde exacto ya terminó."""
        if not self.activa:
            return False
        if self.activa_hasta is None:
            return True
        momento = _a_utc(ahora) if ahora is not None else datetime.now(timezone.utc)
        return momento < self.activa_hasta

    def deberia_avisar(self, minuto_local: int, dia: DiaSemana, ahora: Optional[datetime] = None) -> bool:
        """¿Corresponde mandar el aviso?

        El interruptor manual gana sobre el horario: prenderlo un feriado no
        debería obligar a editar la grilla semanal, y apagar el horario no
        debería desarmar lo que ya se configuró. Con vencimiento (`activa_hasta`)
        gana sólo mientras está vigente: `ahora` es el instante de `minuto_local`
        (None = el reloj).

        Sin horario activo, la única fuente es el interruptor. Con horario
        activo, avisa cuando el momento cae FUERA de toda franja del día.
        """
        if self.pausa_vigente(ahora):
            return True
        if not self.horario.activo:
            return False
        franjas = self.horario.franjas.get(dia) or []
        dentro = any(f.desde_minuto <= minuto_local < f.hasta_minuto for f in franjas)
        return not dentro

    def _paso_el_tope(self, ultimo_aviso_local: datetime, ahora_local: datetime) -> bool:
        # En UTC y no en hora de pared: con un mismo tzinfo, `datetime - datetime` resta
        # las partes naive y se corre una hora al cruzar un cambio de horario de verano.
        return (ahora_local.astimezone(timezone.utc) - ultimo_aviso_local.astimezone(timezone.utc)) > self.TOPE_REENVIO

    def proxima_apertura(self, ahora_local: datetime) -> Optional[datetime]:
        """Cuándo vuelve a haber alguien, en el tzinfo de `ahora_local`, para quien ya sabe que está
        cerrado. Con la pausa vigente: su fin, o —si termina con el local cerrado por el horario— la
        próxima franja después del fin; sin vencimiento, None (un feriado no tiene apertura
        derivable). Sin pausa: la del horario si está activo, si no None.

        La usan api-chatty (diferir, enganchar «al abrir», el pendiente de la ausencia con IA) y
        cintia-creator («hasta X», el Smart Follow Up): una sola cuenta."""
        if self.pausa_vigente(ahora_local):
            if self.activa_hasta is None:
                return None
            fin = self.activa_hasta.astimezone(ahora_local.tzinfo)
            if self.horario.activo and not self.horario.esta_adentro(fin):
                return self.horario.proxima_apertura(fin)
            return fin
        if self.horario.activo:
            return self.horario.proxima_apertura(ahora_local)
        return None

    def estado_ahora(self, ahora: datetime) -> EstadoAhora:
        """El estado de la atención en `ahora` (con zona), con las horas en la zona del horario (ver
        `EstadoAhora`). Levanta si la zona guardada no existe: quien llama decide cómo degradar."""
        local = ahora.astimezone(ZoneInfo(self.horario.timezone))
        if self.pausa_vigente(local):
            hasta = self.activa_hasta.astimezone(local.tzinfo) if self.activa_hasta is not None else None
            return EstadoAhora(estado="pausa", hasta=hasta, proxima_apertura=self.proxima_apertura(local))
        if self.horario.activo:
            franja = self.horario.franja_actual(local)
            if franja is None:
                abre = self.horario.proxima_apertura(local)
                return EstadoAhora(
                    estado="fuera_de_horario", desde=self.horario.ultimo_cierre(local), hasta=abre,
                    proxima_apertura=abre,
                )
            return EstadoAhora(estado="atendiendo", desde=franja[0], hasta=franja[1])
        return EstadoAhora(estado="atendiendo")

    def deberia_reenviar(self, ultimo_aviso_local: datetime, ahora_local: datetime) -> bool:
        """Una vez por chat por cierre: se reenvía sólo si entre el último aviso y ahora hubo
        horario de atención. Con el interruptor manual prendido, tope de 24 h AUNQUE haya
        grilla — la grilla no describe un feriado, y derivar el cierre de ella avisaría cada
        dos horas. Sin próxima apertura derivable, el mismo tope.

        Una pausa con vencimiento que terminó entre el aviso y ahora: el cierre terminó cuando
        volvió a haber alguien (`proxima_apertura` desde el aviso: el fin de la pausa, o la
        franja siguiente si terminó con el local cerrado)."""
        if self.pausa_vigente(ahora_local):
            return self._paso_el_tope(ultimo_aviso_local, ahora_local)
        if self.pausa_vigente(ultimo_aviso_local):
            apertura = self.proxima_apertura(ultimo_aviso_local)
            if apertura is None:
                return self._paso_el_tope(ultimo_aviso_local, ahora_local)
            return apertura < ahora_local
        if not self.horario.activo:
            return self._paso_el_tope(ultimo_aviso_local, ahora_local)
        proxima = self.horario.proxima_apertura(ultimo_aviso_local)
        if proxima is None:
            return self._paso_el_tope(ultimo_aviso_local, ahora_local)
        return proxima < ahora_local


class RecepcionPreview(ChattyAssetPreview):
    ausencia_activa: bool = Field(default=False)
    tiene_bienvenida: bool = Field(default=False)

    @classmethod
    def get_projection(cls) -> dict[str, Any]:
        return super().get_projection() | {"ausencia": 1, "bienvenida_fast_answer_id": 1}

    @classmethod
    def from_asset(cls, asset: "Recepcion") -> "RecepcionPreview":
        return cls(
            _id=asset.id,
            name=asset.name,
            company_id=asset.company_id,
            created_at=asset.created_at,
            updated_at=asset.updated_at,
            deleted_at=asset.deleted_at,
            # La pausa EN VIGOR (con su vencimiento), no el interruptor guardado.
            ausencia_activa=asset.ausencia.pausa_vigente(),
            tiene_bienvenida=asset.bienvenida_fast_answer_id is not None,
        )


class ReglaSeguimientoHumano(BaseModel):
    """La heurística para los humanos. Los caminos automáticos declaran; esto es lo único que
    adivina, y se corrige con un clic."""
    silencio_minimo_horas: int = Field(default=24, ge=1, description="Un saliente de una persona se marca seguimiento si pasaron al menos estas horas desde el último mensaje del cliente.")
    rafaga_minutos: int = Field(default=15, ge=1, description="Tres mensajes seguidos de la misma persona son UN seguimiento: no se abre otro si el anterior es de hace menos de estos minutos y no hubo entrante entre medio.")


class Recepcion(CompanyAssetModel):
    # `name` viene de CompanyAssetModel y no se usa para nada más que trazas:
    # hay una sola por empresa, así que nadie la elige por nombre.
    name: str = Field(default="Recepción")

    bienvenida_fast_answer_id: Optional[StrObjectId] = Field(
        default=None,
        description=(
            "El mensaje de bienvenida. Es una fast answer y no texto suelto a propósito: así se "
            "edita, versiona y reutiliza en el mismo lugar que el resto de los mensajes de la "
            "empresa, en vez de quedar escondido en una pantalla de configuración."
        ),
    )

    # ⚠️ DEPRECADO por el flujo de atención configurable (spec 2026-09-29): pasa a «Consulta
    # general» (el motivo is_fallback). Se borra cuando api-chatty migre (plan 2).
    # La automatización que corre en TODO chat nuevo — etiquetas, funnel, calidad.
    #
    # `target_funnel_id` en None NO es "sin funnel": es **"depende del motivo"**.
    # Cada motivo decide, y el que no diga nada no entra a ninguno. Por eso la
    # pantalla ofrece dos opciones y no un selector que se pueda vaciar.
    automation: Optional[Automation] = Field(default=None)

    # ⚠️ DEPRECADO por el flujo de atención configurable (spec 2026-09-29): pasa a «Consulta
    # general» (el motivo is_fallback). Se borra cuando api-chatty migre (plan 2).
    asignar_ia_a_chats_nuevos: bool = Field(
        default=True,
        description=(
            "Si la empresa tiene un agente activo, lo recibe todo chat nuevo. Opt-OUT y no "
            "opt-in a propósito: con opt-in, la empresa que contrata IA y no toca nada la "
            "tiene apagada y no entiende por qué. No lleva `agent_id` — el agente se deriva "
            "del que la empresa tenga activo, no se elige acá."
        ),
    )

    ausencia: Ausencia = Field(default_factory=Ausencia)

    seguimientos: ReglaSeguimientoHumano = Field(default_factory=ReglaSeguimientoHumano)

    motivos_con_ia: bool = Field(
        default=True,
        description=(
            "Si la IA reconoce el motivo de cada chat nuevo y puede repreguntar cuando duda. "
            "Prendido por defecto porque es lo que pasa hoy. Apagado: no se clasifica ni se "
            "repregunta; el chat va al motivo que declara su fuente (si declara uno) o a "
            "Consulta general, y una fuente no puede declarar varios motivos."
        ),
    )

    dias_para_reclasificar: int = Field(
        default=7,
        ge=1,
        description=(
            "Un chat que vuelve después de estos días sin actividad se reclasifica (motivo nuevo, "
            "sin bienvenida). Una conversación activa no se reclasifica, salvo que el mensaje entre por "
            "una fuente (contact point: anuncio, smart message, texto literal): eso es una conversación "
            "nueva aunque no hayan pasado estos días."
        ),
    )

    bienvenida_demora_s: int = Field(
        default=0,
        ge=0,
        le=30,
        description=(
            "Cuántos segundos espera la entrada de un chat NUEVO antes de arrancar: la bienvenida y "
            "todo lo que la sigue (el aviso de cerrado, la respuesta del motivo, las automatizaciones, "
            "la IA) salen juntos y en el mismo orden, sólo que más tarde. 0 = apenas escribe, como "
            "siempre. Tope 30: es para que no parezca un robot, no para hacer esperar."
        ),
    )

    # --- Por cuenta (0.6.17) ---------------------------------------------------------------
    account_receptions: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Lo propio de cada cuenta de WhatsApp que NO es la por defecto, por id de cuenta: "
            "`{<account_id>: {bienvenida_fast_answer_id, ausencia, atencion_estado}}`. La cuenta por "
            "defecto es la base (los campos de arriba); no tiene entrada acá. Una cuenta sin entrada "
            "usa la base. Dict crudo a propósito: un bloque ilegible no puede tirar el parseo del "
            "documento entero (se valida al escribir y dentro de `for_account`, que no levanta). "
            "No sale al frontend (cada cuenta tiene su ruta) y NUNCA se escribe con el `$set` del "
            "documento: api-chatty lo toca sólo con paths punteados."
        ),
    )

    exclude_fields: ClassVar[dict[SerializerType, set[str]]] = {
        SerializerType.FRONTEND: {"account_receptions"},
    }

    @field_validator("account_receptions", mode="before")
    @classmethod
    def _tolerant_account_receptions(cls, value: Any) -> dict[str, Any]:
        """Never raises: a corrupt map (not an object) reads as «no accounts» and a corrupt block is ignored by
        `for_account`. One bad value must not take the reception of every account down."""
        if value is None:
            return {}
        if not isinstance(value, dict):
            logger.error("recepcion_cuentas_ilegible: account_receptions no es un objeto, se ignora")
            return {}
        return {str(k): v for k, v in value.items()}

    preview_class: ClassVar[type[RecepcionPreview]] = RecepcionPreview

    #: Lo que una cuenta propia pisa de la base. El resto (`automation`, `seguimientos`,
    #: `motivos_con_ia`, `dias_para_reclasificar`, `bienvenida_demora_s`, …) es de la empresa.
    ACCOUNT_FIELDS: ClassVar[tuple[str, ...]] = ("bienvenida_fast_answer_id", "ausencia")

    def model_dump_json(self, *args, serializer: SerializerType = SerializerType.API, **kwargs):
        """What gets written to Mongo (`serializer=DATABASE`) leaves out an EMPTY `account_receptions`:
        a company with one number keeps a document byte-identical to today's, and a plain `update()`
        (a `$set` of the whole document) can never overwrite blocks it did not read."""
        data = super().model_dump_json(*args, serializer=serializer, **kwargs)
        if serializer == SerializerType.DATABASE and not self.account_receptions:
            data.pop("account_receptions", None)
        return data

    def for_account(self, account_id: Optional[str]) -> "Recepcion":
        """La recepción efectiva de un chat de esa cuenta. Pura, sin I/O y NUNCA levanta.

        - Sin cuenta, o sin bloque propio (la cuenta por defecto, o una cuenta que todavía no
          tiene el suyo): `self`, la MISMA instancia. Una empresa de un número no cambia en nada.
        - Con bloque: una copia con la bienvenida y la ausencia de esa cuenta; lo demás, de la base.
        - Bloque ilegible: ERROR y la base (peor es tirar la recepción de todas las cuentas).

        La cuenta del chat es `chat.account_id` tal cual; el que no la tiene es de la por defecto, o
        sea la base: no hace falta resolver cuál es la cuenta por defecto."""
        if not account_id or not self.account_receptions:
            return self
        block = self.account_receptions.get(str(account_id))
        if not isinstance(block, dict):
            return self
        try:
            update: dict[str, Any] = {}
            if "bienvenida_fast_answer_id" in block:
                update["bienvenida_fast_answer_id"] = block["bienvenida_fast_answer_id"] or None
            if block.get("ausencia") is not None:
                update["ausencia"] = Ausencia.model_validate(block["ausencia"])
            if not update:
                return self
            return self.model_copy(update=update)
        except Exception:  # noqa: BLE001 — a broken block never takes the reception down
            logger.error(
                "recepcion_cuenta_ilegible company_id=%s account_id=%s: se usa la base",
                self.company_id, account_id, exc_info=True,
            )
            return self
