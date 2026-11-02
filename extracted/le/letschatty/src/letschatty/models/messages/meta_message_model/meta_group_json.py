# src/letschatty/models/messages/meta_message_model/meta_group_json.py
from __future__ import annotations
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class MetaGroupNotificationJson(BaseModel):
    """Envelope LENIENTE para los webhook fields group_* de la Groups API.

    Deliberadamente NO extiende BaseMetaNotificationJson: el Value estricto no
    modela estos payloads y el shape real está pendiente de validación en sandbox
    (spec 2026-08-29 §9.3). extra="allow" + accessors defensivos: un shape
    inesperado degrada a listas vacías/None, nunca a un ValidationError que
    convierta el webhook en veneno SQS.

    El ruteo NO usa get_notification_type(): MetaNotificationFactory lo resuelve
    por el raw Change-level `field` ANTES de cualquier parse (patrón HISTORY).
    """
    object: Optional[str] = None
    entry: List[Any] = Field(default_factory=list)
    model_config = ConfigDict(extra="allow")

    def _change(self) -> Dict[str, Any]:
        try:
            change = self.entry[0]["changes"][0]
            return change if isinstance(change, dict) else {}
        except (IndexError, KeyError, TypeError):
            return {}

    def get_field(self) -> Optional[str]:
        return self._change().get("field")

    def get_value(self) -> Dict[str, Any]:
        value = self._change().get("value")
        return value if isinstance(value, dict) else {}

    def get_phone_number_id(self) -> Optional[str]:
        metadata = self.get_value().get("metadata")
        if isinstance(metadata, dict):
            return metadata.get("phone_number_id")
        return None

    def get_group_entries(self) -> List[Dict[str, Any]]:
        """Las entradas de grupo del payload. Shape candidato A: value.groups = [ {...} ].
        Shape candidato B (fallback): el objeto plano en value. Devuelve [] solo si no
        hay nada reconocible con pinta de grupo."""
        value = self.get_value()
        groups = value.get("groups")
        if isinstance(groups, list):
            return [g for g in groups if isinstance(g, dict)]
        if self.extract_group_id(value) is not None:
            return [value]
        return []

    @staticmethod
    def extract_group_id(entry: Dict[str, Any]) -> Optional[str]:
        """Candidatos de clave para el group id, en orden de probabilidad. `id` va último
        porque en un shape plano podría colisionar con otros ids del value."""
        for key in ("group_id", "wa_group_id", "id"):
            candidate = entry.get(key)
            if isinstance(candidate, str) and candidate:
                return candidate
        return None


class MetaGroupLifecycleJson(MetaGroupNotificationJson):
    """group_lifecycle_update: creación (trae invite_link), suspensión, borrado."""
    pass


class MetaGroupParticipantsJson(MetaGroupNotificationJson):
    """group_participants_update: altas y bajas de miembros."""

    @staticmethod
    def extract_participant_updates(entry: Dict[str, Any]) -> List[Dict[str, Any]]:
        participants = entry.get("participants")
        if isinstance(participants, list):
            return [p for p in participants if isinstance(p, dict)]
        return []

    @staticmethod
    def extract_participant_waid(participant: Dict[str, Any]) -> Optional[str]:
        for key in ("user", "wa_id", "phone_number"):
            candidate = participant.get(key)
            if isinstance(candidate, str) and candidate:
                return candidate
        return None

    @staticmethod
    def extract_action(participant: Dict[str, Any]) -> Optional[str]:
        for key in ("action", "type", "event"):
            candidate = participant.get(key)
            if isinstance(candidate, str) and candidate:
                return candidate.lower()
        return None
