from enum import StrEnum
import os

class Environment(StrEnum):
    PRODUCTION = "PROD"
    DEVELOPMENT = "DEV"
    LOCAL = "LOCAL"


class Area(StrEnum):
    WAITING_AGENT = "WAITING AGENT"
    WITH_AGENT = "WITH AGENT"
    ARCHIVED = "ARCHIVED"
    BLOCKED = "BLOCKED"
    INBOX = "INBOX"
    FOLLOW_UP = "FOLLOW UP"

    @classmethod
    def list_all(cls) -> list[str]:
        return [area.value for area in cls]

frontend_areas_to_backend_areas = {
    "esperando agente": Area.WAITING_AGENT,
    "asignar a agente": Area.WITH_AGENT,
    "con agente": Area.WITH_AGENT,
    "archivados": Area.ARCHIVED,
    "seguimiento": Area.FOLLOW_UP
}
backend_areas_to_frontend_areas = {
    Area.WAITING_AGENT: "esperando agente",
    Area.WITH_AGENT: "con agente",
    Area.ARCHIVED: "archivados",
    Area.FOLLOW_UP: "seguimiento"
}