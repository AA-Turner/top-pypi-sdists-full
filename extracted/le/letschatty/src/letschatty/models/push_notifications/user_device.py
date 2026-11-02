from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field

from ..base_models.chatty_asset_model import CompanyAssetModel
from .enums import DeviceStatus, Platform, TokenStatus


class UserDevice(CompanyAssetModel):
    user_id: str = Field(
        description="Usuario dueño de esta instalación. Se usa para buscar todos los devices de un usuario."
    )

    installation_id: str = Field(
        description="Identificador estable de la instalación generado por el cliente. Se usa para hacer upsert aunque cambie el FCM token."
    )

    platform: Platform = Field(
        description="Plataforma del cliente: web, ios o android. Se usa para debugging, segmentación y futuras reglas."
    )

    fcm_token: Optional[str] = Field(
        default=None,
        description="Token actual de Firebase Cloud Messaging para enviar push a esta instalación."
    )

    token_status: TokenStatus = Field(
        default=TokenStatus.UNKNOWN,
        description="Estado del FCM token. Se usa para saber si el token puede seguir usándose o si FCM ya lo invalidó."
    )

    app_version: Optional[str] = Field(
        default=None,
        description="Versión de la app/web que reporta el cliente. Se usa para debugging y compatibilidad."
    )

    online: bool = Field(
        default=False,
        description="Flag materializado de presencia. Se usa para saber si esta instalación está considerada online."
    )

    last_seen_at: Optional[datetime] = Field(
        default=None,
        description="Último heartbeat recibido de esta instalación. Se usa para presencia y expiración de online."
    )

    status: DeviceStatus = Field(
        default=DeviceStatus.ACTIVE,
        description="Estado funcional del device. Se usa para excluir instalaciones logout o deshabilitadas."
    )

    is_active: bool = Field(
        default=True,
        description="Flag rápido para saber si la instalación sigue vigente para notificaciones."
    )

    last_push_sent_at: Optional[datetime] = Field(
        default=None,
        description="Última vez que intentamos enviar una push a esta instalación. Se usa para auditoría y debugging."
    )

    last_push_error_at: Optional[datetime] = Field(
        default=None,
        description="Última vez que FCM devolvió error para este device. Se usa para troubleshooting."
    )

    last_push_error_code: Optional[str] = Field(
        default=None,
        description="Último código de error devuelto por FCM para este token. Se usa para invalidar o investigar fallos."
    )

    invalidated_at: Optional[datetime] = Field(
        default=None,
        description="Fecha en la que marcamos este token como inválido. Se usa para no seguir intentando enviar."
    )
