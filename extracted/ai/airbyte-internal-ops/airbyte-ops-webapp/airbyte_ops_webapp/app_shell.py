"""Shared application shell for Ops Webapp pages."""

from prefab_ui.app import PrefabApp

from airbyte_ops_webapp.auth.oauth import OAUTH_JS_ACTIONS, hydrate_oauth_action
from airbyte_ops_webapp.theme import _airbyte_theme, _app_root_class


def build_ops_app(
    *,
    title: str,
    state: dict[str, object],
    oauth_issuer: str,
) -> PrefabApp:
    return PrefabApp(
        title=title,
        css_class=_app_root_class(),
        state=state,
        theme=_airbyte_theme(),
        connect_domains=[oauth_issuer],
        js_actions=OAUTH_JS_ACTIONS,
        on_mount=hydrate_oauth_action(),
    )
