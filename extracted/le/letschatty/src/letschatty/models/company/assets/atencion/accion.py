"""La unión completa de acciones: todo lo que puede ser «¿Qué les enviamos?» de un motivo."""
from typing import Annotated, Union

from pydantic import Tag
from pydantic.json_schema import SkipJsonSchema

from .acciones_basicas import (
    DESCONOCIDA,
    TIPOS_DE_ACCION,
    AccionAgendar,
    AccionCrearPendiente,
    AccionDesconocida,
    AccionIaResponde,
    AccionNada,
    AccionPersonalizada,
    AccionRespuestaRapida,
    discriminador_con_respaldo,
)
from .precalificacion import AccionPrecalificar

# TIPOS_DE_ACCION se define en acciones_basicas (la única lista); se reexporta desde acá.

Accion = Annotated[
    Union[
        Annotated[AccionRespuestaRapida, Tag("respuesta_rapida")],
        Annotated[AccionIaResponde, Tag("ia_responde")],
        Annotated[AccionPrecalificar, Tag("precalificar")],
        Annotated[AccionAgendar, Tag("agendar")],
        Annotated[AccionCrearPendiente, Tag("crear_pendiente")],
        Annotated[AccionPersonalizada, Tag("accion_personalizada")],
        Annotated[AccionNada, Tag("nada")],
        Annotated[SkipJsonSchema[AccionDesconocida], Tag(DESCONOCIDA)],
    ],
    discriminador_con_respaldo(TIPOS_DE_ACCION),
]
