from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class DarklyThemeHook(ThemeHook):
    """
    Bootswatch Darkly Theme
    https://bootswatch.com/darkly/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "Darkly",
            "Flatly in night mode!",
            html_tags={"data-theme": "darkly"},
            css=[],
            js=[],
            css_template="theme/darkly/css.html",
            js_template="bundles/bootstrap-js-bs5.html",
            header_padding="4.5em"
        )


@hooks.register('theme_hook')
def register_darkly_hook() -> DarklyThemeHook:
    return DarklyThemeHook()
