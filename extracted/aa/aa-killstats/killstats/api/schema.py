# Standard Library
from datetime import datetime

# Third Party
from ninja import Schema


class Killboard(Schema):
    kills: int | None = None
    date: datetime | None = None
    character_id: int | None = None
    character_name: str | None = None
    ship_id: int | None = None
    ship_name: str | None = None
    hash: str | None = None
    totalValue: int | None = None
    attackers: list | None = None


class KillboardHall(Schema):
    shame: list | None = None
    fame: list | None = None


class KillboardStats(Schema):
    stats: list | None = None


class CorporationAdmin(Schema):
    corporation: dict | None = None


class AllianceAdmin(Schema):
    alliance: dict | None = None
