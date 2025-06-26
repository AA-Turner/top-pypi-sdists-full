from django.utils.translation import gettext_lazy as _

from wbcore.menus import Menu, MenuItem

TEAM_MENUITEM = MenuItem(
    label=_("Teams"),
    endpoint="example_app:team-list",
    add=MenuItem(
        label=_("Create Team"),
        endpoint="example_app:team-list",
    ),
)
LEAGUE_MENUITEM = MenuItem(
    label=_("Leagues"),
    endpoint="example_app:league-list",
    add=MenuItem(
        label=_("Create League"),
        endpoint="example_app:league-list",
    ),
)
STADIUM_MENUITEM = MenuItem(
    label=_("Stadiums"),
    endpoint="example_app:stadium-list",
    add=MenuItem(
        label=_("Create Stadium"),
        endpoint="example_app:stadium-list",
    ),
)
PERSONS_MENUITEM = MenuItem(
    label=_("Persons"),
    endpoint="example_app:person-list",
    add=MenuItem(
        label=_("Create Person"),
        endpoint="example_app:person-list",
    ),
)
SPORT_MENUITEM = MenuItem(
    label=_("Sports"),
    endpoint="example_app:sport-list",
    add=MenuItem(
        label=_("Create Sport"),
        endpoint="example_app:sport-list",
    ),
)
SEASON_MENUITEM = MenuItem(
    label=_("Season"),
    endpoint="example_app:season-list",
    add=MenuItem(label=_("Create Season"), endpoint="example_app:season-list"),
)
PLAYER_MENUITEM = MenuItem(
    label=_("Players"),
    endpoint="example_app:player-list",
    add=MenuItem(
        label=_("Create Player"),
        endpoint="example_app:player-list",
    ),
)
ROLE_MENUITEM = MenuItem(
    label=_("Roles"),
    endpoint="example_app:role-list",
    add=MenuItem(
        label=_("Create Role"),
        endpoint="example_app:role-list",
    ),
)
MATCH_MENUITEM = MenuItem(
    label=_("Matches"),
    endpoint="example_app:match-list",
    add=MenuItem(
        label=_("Create Match"),
        endpoint="example_app:match-list",
    ),
)
EVENT_MENUITEM = MenuItem(
    label=_("Events"),
    endpoint="example_app:event-list",
    add=MenuItem(
        label=_("Create Event"),
        endpoint="example_app:event-list",
    ),
)
EVENTTYPE_MENUITEM = MenuItem(
    label=_("Event Types"),
    endpoint="example_app:eventtype-list",
    add=MenuItem(
        label=_("Create Event Type"),
        endpoint="example_app:eventtype-list",
    ),
)

EXAMPLE_APP_MENU = Menu(
    label="Sports App",
    items=[
        Menu(label=_("Persons"), items=[PERSONS_MENUITEM, PLAYER_MENUITEM]),
        ROLE_MENUITEM,
        TEAM_MENUITEM,
        STADIUM_MENUITEM,
        Menu(label=_("Leagues"), items=[LEAGUE_MENUITEM, SEASON_MENUITEM]),
        SPORT_MENUITEM,
        MATCH_MENUITEM,
        Menu(label=_("Events"), items=[EVENT_MENUITEM, EVENTTYPE_MENUITEM]),
    ],
)
