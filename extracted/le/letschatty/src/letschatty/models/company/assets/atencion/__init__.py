"""El flujo de atención configurable: acciones, seguimientos, qué pasa cuando responden,
precalificación, capacidades a medida, recetas y plantillas.

Spec: frontend/docs/superpowers/specs/2026-09-29-flujos-de-atencion-configurables-design.md

`herencia` NO se reexporta acá: depende de `Motivo`, que a su vez importa este paquete.
"""

from .accion import Accion
from .acciones_fijas import AccionesFijas
from .acciones_basicas import (
    TIPOS_DE_ACCION,
    AccionAgendar,
    AccionCrearPendiente,
    AccionDeRama,
    AccionDesconocida,
    AccionIaResponde,
    AccionNada,
    AccionPersonalizada,
    AccionRespuestaRapida,
    CambiarMotivo,
    cambiar_motivo_activo,
)
from .al_responder import AlResponder, Asignacion, IaAlResponder, ModoAsignacion
from .capacidad import Capacidad, CapacidadPreview, EjecutorDeCapacidad
from .entradas import Entrada, EntradaPreview, ReglaDeEntrada
from .precalificacion import AccionPrecalificar, DatoAPedir, ObjetivoPrecalificacion, Precalificacion, Rama
from .recetas import (
    CLAVES_DEL_MOTIVO,
    REF,
    REF_EMPRESA,
    ConsultaGeneralDePlantilla,
    Hueco,
    MotivoDePlantilla,
    PlantillaDeIndustria,
    RecetaDeMotivo,
    RespuestaRapidaDeReceta,
    TipoHueco,
    faltantes,
    reemplazar_huecos,
    resolver_referencias,
)
from .seguimientos import (
    TIPOS_DE_PASO,
    AccionDePaso,
    AccionesDeEtiquetas,
    AlTerminar,
    CierreSinRespuesta,
    EtapaDestino,
    ModoSeguimientos,
    PasoDeSeguimiento,
    PasoDeSeguimientoIa,
    Seguimientos,
    SeguimientosDeIa,
    SiVuelve,
    SiVuelveA,
)
