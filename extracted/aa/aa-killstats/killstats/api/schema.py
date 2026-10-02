# Standard Library
from datetime import datetime
from typing import Literal

# Third Party
from dateutil.relativedelta import relativedelta
from ninja import Field, FilterSchema, Schema

# Django
from django.db.models import Q


class UserData(Schema):
    """
    Schema for user data, including character ID and character name.
    """

    user_id: int
    character_id: int
    character_name: str
    corporation_id: int
    corporation_name: str
    alliance_id: int | None = None
    alliance_name: str | None = None
    portrait: str | None = None
    is_admin: bool = False


class CorporationAdmin(Schema):
    corporation: dict | None = None


class AllianceAdmin(Schema):
    alliance: dict | None = None


class TopPilotSchema(Schema):
    character_id: int
    character_name: str
    main_name: str | None = None
    count: int  # kills or deaths
    total_value: int | float


class CombatStatsResponse(Schema):
    total_kills: int
    active_pvpers: int
    destroyed_isk: int | float
    lost_isk: int | float
    top_attackers: list[TopPilotSchema]
    top_victims: list[TopPilotSchema]


class CombatSummaryResponse(Schema):
    """Lightweight summary: counters + ISK totals only. Fast to compute."""

    total_kills: int
    active_pvpers: int
    destroyed_isk: int | float
    lost_isk: int | float


class TopPilotsResponse(Schema):
    """Top-N pilot list (attackers OR victims). Returned by dedicated endpoints."""

    pilots: list[TopPilotSchema]


class HallEntrySchema(Schema):
    killmail_id: int
    char_id: int
    char_name: str
    ship_id: int = 0
    ship_name: str = "Unknown"
    victim_ship_id: int = 0
    victim_ship_name: str = "Unknown"
    total_value: int | float
    damage_done: int = 0
    zkb_link: str


class HallResponseSchema(Schema):
    hall_of_fame: list[HallEntrySchema]
    hall_of_shame: list[HallEntrySchema]


class KillmailItemSchema(Schema):
    killmail_id: int
    killmail_date: str
    victim_id: int
    victim_name: str
    victim_ship_id: int
    victim_ship_name: str
    total_value: int | float
    solar_system_id: int = 0
    solar_system_name: str = "Unknown"
    security_status: float = 0.0
    pilot_count: int
    final_blow_id: int = 0
    final_blow_name: str = "Unknown"
    is_loss: bool = False
    zkb_link: str


class KillmailListResponse(Schema):
    killmails: list[KillmailItemSchema]
    total: int
    page: int = 1
    page_size: int = 50


class ModalSchema(Schema):
    """Schema for modal dialog data."""

    title: str
    text: str
    icon: str
    modal_id: str
    url: str
    color: str | None = None
    buttonText: str | None = None


class MenuLink(Schema):
    """
    Represents a link in the menu.
    """

    name: str
    link: str | None = None
    is_external: bool = False


class MenuCategory(MenuLink):
    """
    Represents a category in the menu, which can contain multiple links.
    """

    links: list[MenuLink] = []


class MenuModalSchema(Schema):
    """Schema for menu modals."""

    modal: ModalSchema | None = None


class MenuSchema(Schema):
    """
    Schema for the overall menu, including links and modals.
    """

    left_links: list[MenuLink] = []
    right_links: list[MenuLink] = []
    modals: MenuModalSchema | None = None


class DateRangeFilter(FilterSchema):
    year: int | None = Field(
        None, ge=2000, le=2100, description="Filter by year (e.g. 2026)"
    )
    month: int | None = Field(None, ge=1, le=12, description="Filter by month (1-12)")

    def get_date_range(self) -> tuple[datetime | None, datetime | None]:
        """Return (start_datetime, end_datetime) for index-backed range queries."""
        if self.year and self.year > 0 and self.month and self.month > 0:
            start = datetime(self.year, self.month, 1)
            end = start + relativedelta(months=1)
            return start, end
        if self.year and self.year > 0:
            start = datetime(self.year, 1, 1)
            end = datetime(self.year + 1, 1, 1)
            return start, end
        return None, None

    @property
    def km_date_q(self) -> Q:
        """Q expression for filtering Killmail rows by date range."""
        start, end = self.get_date_range()
        return (
            Q(killmail_date__gte=start, killmail_date__lt=end) if start and end else Q()
        )

    @property
    def att_date_q(self) -> Q:
        """Q expression for filtering Attacker rows by related killmail date range."""
        start, end = self.get_date_range()
        return (
            Q(killmail__killmail_date__gte=start, killmail__killmail_date__lt=end)
            if start and end
            else Q()
        )


class TopPilotsFilter(DateRangeFilter):
    limit: int = Field(10, ge=1, le=100, description="Number of top pilots to return")


class HallFilter(DateRangeFilter):
    limit: int = Field(5, ge=1, le=50, description="Number of hall entries to return")


class KillmailFilter(DateRangeFilter):
    mode: Literal["all", "kills", "losses"] = Field("all", description="Mode filter")
    page: int = Field(1, ge=1, description="Page number")
    page_size: int = Field(50, ge=1, le=250, description="Items per page")
