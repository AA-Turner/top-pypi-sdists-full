from allianceauth import hooks
from allianceauth.theme.hooks import ThemeHook


class FlatlyThemeHook(ThemeHook):
    """
    Bootswatch Flatly Theme
    https://bootswatch.com/flatly/
    """

    def __init__(self) -> None:
        ThemeHook.__init__(
            self,
            "Flatly",
            "Flat and modern!",
            html_tags={"data-theme": "flatly"},
            css=[],
            js=[],
            css_template="theme/flatly/css.html",
            js_template="bundles/bootstrap-js-bs5.html",
            header_padding="4.5em"
        )


@hooks.register('theme_hook')
def register_flatly_hook() -> FlatlyThemeHook:
    return FlatlyThemeHook()
