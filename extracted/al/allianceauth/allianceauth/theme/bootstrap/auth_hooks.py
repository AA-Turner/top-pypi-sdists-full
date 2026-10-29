from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class BootstrapThemeHook(ThemeHook):
    """
    Bootstrap in all its glory!
    https://getbootstrap.com/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "Bootstrap",
            "Powerful, extensible, and feature-packed frontend toolkit.",
            html_tags={"data-theme": "bootstrap"},
            css=[],
            js=[],
            css_template="theme/bootstrap/css.html",
            js_template="bundles/bootstrap-js-bs5.html",
            header_padding="3.5em",
        )


class BootstrapDarkThemeHook(ThemeHook):
    """
    Bootstrap in all its glory!, but _dark_
    https://getbootstrap.com/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "Bootstrap Dark",
            "Powerful, extensible, and feature-packed frontend toolkit.",
            html_tags={"data-theme": "bootstrap-dark", "data-bs-theme":"dark"},
            css=[],
            js=[],
            css_template="theme/bootstrap/css.html",
            js_template="bundles/bootstrap-js-bs5.html",
            header_padding="3.5em"
        )


@hooks.register('theme_hook')
def register_bootstrap_dark_hook() -> BootstrapDarkThemeHook:
    return BootstrapDarkThemeHook()


@hooks.register('theme_hook')
def register_bootstrap_hook() -> BootstrapThemeHook:
    return BootstrapThemeHook()
