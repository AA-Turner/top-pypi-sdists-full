# src/letschatty/models/chat/group_participant.py
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class GroupParticipant(BaseModel):
    """Un miembro (actual o pasado) de un grupo de WhatsApp (Groups API).

    Las filas NUNCA se borran: al salir del grupo se marca is_active=False y se
    estampa left_at. El historial del chat renderiza el nombre del autor de cada
    mensaje resolviendo Message.sent_by (waid del participante) contra este roster,
    así que borrar la fila rompería el render de los mensajes viejos (spec §3.2).

    Nota de persistencia: joined_at/left_at se guardan en Mongo como ISO strings (el
    dump del Client no re-inyecta datetimes en este array — decisión v1: nada los
    range-quería; pydantic los re-coerciona al leer).
    """
    waid: str
    name: Optional[str] = Field(default=None, description="profile.name del webhook; se refresca cuando el participante escribe")
    is_active: bool = True
    joined_at: Optional[datetime] = None
    left_at: Optional[datetime] = None
