from django.utils.translation import gettext_lazy as _

from wbcore.menus import Menu, MenuItem

TEAM_MENUITEM = MenuItem(
    label=_("Team"),
    endpoint="example_app:team-list",
    add=MenuItem(
        label=_("Create Team"),
        endpoint="example_app:team-list",
    ),
)
LEAGUE_MENUITEM = MenuItem(
    label=_("League"),
    endpoint="example_app:league-list",
    add=MenuItem(
        label=_("Create League"),
        endpoint="example_app:league-list",
    ),
)
STADIUM_MENUITEM = MenuItem(
    label=_("Stadium"),
    endpoint="example_app:stadium-list",
    add=MenuItem(
        label=_("Create Stadium"),
        endpoint="example_app:stadium-list",
    ),
)
FIGURE_MENUITEM = MenuItem(
    label=_("Figure"),
    endpoint="example_app:figure-list",
    add=MenuItem(
        label=_("Create Figure"),
        endpoint="example_app:figure-list",
    ),
)
SPORT_MENUITEM = MenuItem(
    label=_("Sport"),
    endpoint="example_app:sport-list",
    add=MenuItem(
        label=_("Create Sport"),
        endpoint="example_app:sport-list",
    ),
)
PLAYER_MENUITEM = MenuItem(
    label=_("Player"),
    endpoint="example_app:player-list",
    add=MenuItem(
        label=_("Create player"),
        endpoint="example_app:player-list",
    ),
)

EXAMPLE_APP_MENU = Menu(
    label="Sports App",
    items=[
        FIGURE_MENUITEM,
        PLAYER_MENUITEM,
        TEAM_MENUITEM,
        STADIUM_MENUITEM,
        LEAGUE_MENUITEM,
        SPORT_MENUITEM,
    ],
)
