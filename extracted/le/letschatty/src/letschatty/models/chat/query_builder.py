"""
Compila `FilterParameters` al `$match` de Mongo.

Vive EN EL PAQUETE y no en api-chatty desde 2026-09-10, y el motivo no es
prolijidad: la tabla campo → path de Mongo estaba escrita dos veces, en dos
repos (acá y en `shared/audience/filter.py::MONGO_PATH` de lambdas). Agregar un
filtro obligaba a tocar los dos, y olvidarse de uno no falla — devuelve de más.
Acá lo pueden importar los dos consumidores.

⚠️ Lo que NO va acá, y no es un olvido: `AreaFilter` y el piso de visibilidad
(`visibility_policy`) se quedan en api-chatty. Dependen del usuario que pregunta
y de su `ExecutionContext` — son guardias de un request, no lenguaje. Esa línea
es la que deja que campañas resuelva DELIBERADAMENTE sin scope mientras las
vistas resuelven con scope: mismo lenguaje, distinta guardia, y la diferencia
queda visible en vez de ser un import que alguien se olvidó.

Este módulo es PURO: stdlib + `FilterParameters`. Sin I/O, sin Mongo, sin
`ExecutionContext`. Si algo de eso aparece, dejó de poder vivir en el paquete.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

from .filter_parameters import FilterParameters

#: date_field de la query string → campo persistido en el documento del chat.
#: Los tres están denormalizados; ninguno se calcula al vuelo.
DATE_FIELD_TO_MONGO: dict[str, str] = {
    "created_at": "created_at",
    "last_message": "last_message_timestamp",
    "last_incoming": "last_incoming_message_timestamp",
}


def merge_bounds(query: dict, field: str, gte=None, lte=None, lt=None, gt=None) -> None:
    """Suma cotas a `field` SIN pisar lo que otro filtro ya haya puesto ahí.

    `query[field] = {...}` sería un bug: hay CUATRO filtros distintos que escriben
    `last_message_timestamp` (`time_since_last_message_hours`, `last_message_date_range`,
    el filtro de fecha del board y la guarda de chats vacíos de la bandeja), y una
    reasignación descarta la condición anterior en silencio — sin error, solo
    resultados mal.

    TODOS los escritores de una clave de rango deben pasar por acá, incluso el que hoy
    corre primero: el orden dentro de `to_query` no es un contrato, y basta con que
    alguien agregue un filtro más arriba para que el que reasigna se coma al otro.

    ⚠️ Es PÚBLICA (sin guión bajo) desde 2026-09-10 justamente por eso: el cuarto
    escritor no vive en este módulo — es la guarda `$gt: _MIN_TS` de
    `get_chat_previews` —, estaba escrito como una reasignación en un dict literal, y
    se comía la ventana de fecha de «Actividad» de la bandeja en silencio. La regla no
    sirve si sólo la pueden cumplir los de adentro del archivo.
    """
    bounds = {}
    if gte is not None:
        bounds["$gte"] = gte
    if lte is not None:
        bounds["$lte"] = lte
    if lt is not None:
        bounds["$lt"] = lt
    if gt is not None:
        bounds["$gt"] = gt
    if bounds:
        query.setdefault(field, {}).update(bounds)


#: Alias interno histórico. Los call sites de este módulo lo siguen usando.
_merge_bounds = merge_bounds


def _collect_date_ranges(
    date_field: Optional[str],
    date_from: Optional[datetime],
    date_to: Optional[datetime],
    date_ranges: Optional[dict[str, tuple[Optional[datetime], Optional[datetime]]]],
) -> dict[str, tuple[Optional[datetime], Optional[datetime]]]:
    """Las dos formas de pedir una ventana de fecha, en una sola estructura.

    `date_field`/`date_from`/`date_to` es la forma de UNA ventana (la que manda el
    board desde que existe el filtro); `date_ranges` es la de VARIAS, una por campo.
    Se unifican acá para que `to_query` tenga un solo camino que aplique fechas: con
    dos ramas separadas, el día que alguien agregue una tercera condición sobre
    `last_message_timestamp` va a tener que acordarse de las dos.

    Ante el mismo campo en las dos formas gana `date_ranges` — misma regla, y por el
    mismo motivo, que documenta `parse_date_ranges` en `routes/common/dates.py`.
    """
    collected = dict(date_ranges or {})
    if date_field and date_field not in collected:
        collected[date_field] = (date_from, date_to)
    return collected


class QueryBuilder:
    @staticmethod
    def to_query(
        filters: FilterParameters,
        has_sales: bool = False,
        date_field: Optional[str] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        without_funnel: bool = False,
        date_ranges: Optional[dict[str, tuple[Optional[datetime], Optional[datetime]]]] = None,
    ) -> dict:
        query: dict = {}

        if filters.unread == 1:
            query["is_read_status"] = False

        if filters.starred == 1:
            query["starred"] = True

        if filters.time_left_order == 1:
            now = datetime.now(tz=ZoneInfo("UTC"))
            query["$or"] = [
                {"free_conversation_expire_date": {"$gte": now}},
                {"free_template_window_expire_date": {"$gte": now}},
            ]

        if filters.products:
            query["products.asset_id"] = {"$in": filters.products}

        if filters.tags:
            query["tags.asset_id"] = {"$in": filters.tags}

        if filters.accounts:
            # Multi-account: the chats of these WhatsApp accounts.
            query["account_id"] = {"$in": filters.accounts}

        if has_sales:
            query["sales.0"] = {"$exists": True}

        # Producto y fecha de venta se piden DENTRO DE LA MISMA venta ($elemMatch). Con dos
        # condiciones sueltas sobre el array, un chat con una venta del producto en enero y
        # otra de otro producto en marzo entraba en «vendió el producto en marzo».
        sale_conditions: dict = {}
        if filters.sales_products:
            # Una venta nueva lista todos sus productos en `product_ids`; las referencias
            # guardadas antes de las líneas sólo tienen `product_id`.
            sale_conditions["$or"] = [
                {"product_id": {"$in": filters.sales_products}},
                {"product_ids": {"$in": filters.sales_products}},
            ]
        if filters.sales_date_range:
            sale_conditions["assigned_at"] = {
                "$gte": filters.sales_date_range[0],
                "$lte": filters.sales_date_range[1],
            }
        if sale_conditions:
            query["sales"] = {"$elemMatch": sale_conditions}

        funnel_id = getattr(filters, "funnel_id", None)
        if without_funnel:
            # Chats que NO están en ningún funnel. IGUALDAD contra null, no `$not`.
            #
            # ⚠️ NO volver a `{"$not": {"$type": "string"}}`. Era la negación exacta del
            # positivo de count_service.py, pero una negación NO TIENE COTA: el planner
            # no puede usarla como bound, así que el índice deja de poder PROVEER EL
            # ORDEN de last_message_timestamp y Mongo mete un SORT bloqueante — trae
            # TODOS los chats de la empresa (~29KB c/u) para ordenarlos en memoria y
            # devolver 10. Medido en prod el 2026-08-25: 151.658 docs examinados para
            # devolver 1, 28,52 min de ejecución. Eso solo no sería más que una pantalla
            # lenta, pero son ~4,4GB pasando por los 8GB de caché del M30: desaloja el
            # working set, TODA otra query del cluster pasa a leer de disco, y
            # /meta/send_json se va por arriba de los 10s de timeout de backup-chatty,
            # que entra en modo SQS y frena el pipeline entero 90s. Ver
            # docs/previews-sin-funnel-index-seek.md.
            #
            # `{: null}` sí es igualdad: matchea tanto null como campo ausente (que es
            # el caso real — `active_funnel` es Optional y cuando no hay funnel el
            # subdocumento entero no está), y el índice guarda esas entradas bajo la
            # clave null. Equivale al `$not` de antes porque funnel_id, cuando existe,
            # es SIEMPRE string (StrObjectId — ver count_service.py:108).
            #
            # Las dos claves juntas cubren el prefijo de
            # `company_id_1_deleted_at_1_active_funnel.funnel_id_1
            #  _active_funnel.current_stage_id_1_last_message_timestamp_-1`
            # (REGULAR + COMPOUND, verificado en Atlas: ni sparse ni partial, si no
            # `{: null}` no podría usarlo). Con las 4 primeras claves fijadas por
            # igualdad el índice entrega last_message_timestamp ya ordenado, el $sort
            # desaparece y el $limit corta al décimo documento.
            #
            # Gana sobre funnel_id / funnels / funnel_stages a propósito: "sin funnel"
            # y "en estos funnels" son contradictorios, y un AND de los dos devolvería
            # cero en silencio. El front nunca los manda juntos; esto está para que la
            # combinación no pueda existir.
            query["active_funnel.funnel_id"] = None
        elif funnel_id:
            query["active_funnel.funnel_id"] = str(funnel_id)
        elif filters.funnels:
            query["active_funnel.funnel_id"] = {"$in": [str(f) for f in filters.funnels]}

        stage_id = getattr(filters, "stage_id", None)
        if without_funnel:
            # Sin funnel no hay etapa, así que esto es semánticamente gratis — pero NO
            # es opcional: es la 4ta clave del índice de arriba. Sin fijarla queda un
            # hueco en esa posición y el planner ya no puede probar que
            # last_message_timestamp viene ordenado (nosotros sabemos que dentro del
            # bucket null la etapa también es null; el planner no lo sabe, sólo ve los
            # bounds), así que vuelve el SORT bloqueante y todo lo de arriba.
            query["active_funnel.current_stage_id"] = None
        elif stage_id:
            query["active_funnel.current_stage_id"] = str(stage_id)
        elif filters.funnel_stages:
            query["active_funnel.current_stage_id"] = {"$in": [str(s) for s in filters.funnel_stages]}

        if filters.time_since_last_message_hours > 0:
            hours_ago = datetime.now() - timedelta(hours=filters.time_since_last_message_hours)
            _merge_bounds(query, "last_message_timestamp", lt=hours_ago)

        # Fuente y fecha del touchpoint, dentro del MISMO touchpoint (mismo motivo que ventas).
        touchpoint_conditions: dict = {}
        if filters.sources:
            touchpoint_conditions["source_id"] = {"$in": filters.sources}
        if filters.sources_date_range:
            touchpoint_conditions["assigned_at"] = {
                "$gte": filters.sources_date_range[0],
                "$lte": filters.sources_date_range[1],
            }
        if touchpoint_conditions:
            query["contact_points"] = {"$elemMatch": touchpoint_conditions}

        if filters.quality_score:
            query["lead_quality"] = {"$in": filters.quality_score}

        if filters.con_seguimiento_sin_respuesta == 1:
            query["seguimientos_consecutivos"] = {"$gte": 1}

        if filters.sin_seguimiento_hace_dias > 0:
            # `$not $gte` y no `$lt`: los chats que NUNCA tuvieron seguimiento no tienen
            # el campo (o lo tienen en null) y «sin seguimiento hace N días» los incluye.
            # Fecha NAIVE: misma convención que time_since_last_message_hours arriba —
            # Mongo/PyMongo decodifica las fechas guardadas como naive-UTC, y comparar
            # con una fecha aware acá sería un bug silencioso (corre la ventana por el
            # offset local en vez de comparar UTC contra UTC).
            limite = datetime.now() - timedelta(days=filters.sin_seguimiento_hace_dias)
            query["ultimo_seguimiento_at"] = {"$not": {"$gte": limite}}

        if filters.seguimientos_min > 0:
            query["seguimientos_total"] = {"$gte": filters.seguimientos_min}

        if filters.workflows:
            # `flow_ids` es el espejo de `chat_flow_states` en el chat. Antes se consultaba
            # `flow_states.flow_id` y el estado guardaba `asset_id`: devolvía siempre cero.
            query["flow_ids"] = {"$in": filters.workflows}

        if filters.last_message_date_range:
            _merge_bounds(
                query, "last_message_timestamp",
                gte=filters.last_message_date_range[0],
                lte=filters.last_message_date_range[1],
            )

        # Filtros de fecha del board de CRM y de la Vista Listado. Cada entrada elige
        # sobre qué campo se aplica; cualquiera de las dos cotas puede venir vacía
        # (rango abierto), y un campo que no esté en DATE_FIELD_TO_MONGO se ignora.
        #
        # Son VARIAS a propósito: "creados en agosto Y con actividad esta semana" son
        # dos preguntas sobre campos DISTINTOS, y hasta este cambio elegir una
        # descartaba la otra. Como cada una escribe su propia clave del match, el AND
        # lo hace Mongo sin que haya que coordinar nada acá.
        #
        # ⚠️ Dos ventanas sobre el MISMO campo no pueden llegar hasta acá — las formas
        # se resuelven antes, en `_collect_date_ranges`. Si alguna vez llegaran, el
        # `_merge_bounds` las intersectaría en silencio, que es justo lo que esa
        # función existe para evitar.
        for field, (desde, hasta) in _collect_date_ranges(
            date_field, date_from, date_to, date_ranges
        ).items():
            mongo_field = DATE_FIELD_TO_MONGO.get(field)
            if mongo_field:
                _merge_bounds(query, mongo_field, gte=desde, lte=hasta)

        return query
