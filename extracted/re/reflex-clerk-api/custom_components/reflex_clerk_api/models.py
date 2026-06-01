from typing import Any, Literal

from reflex.components.props import PropsBase

LiteralBaseTheme = Literal["default", "dark", "neobrutalism", "shadesOfPurple"]


class Layout(PropsBase):
    animations: bool = True
    """Whether to enable animations inside the components. Defaults to true."""

    help_page_url: str = ""
    """The URL to your help page."""

    logo_image_url: str = ""
    """The URL to your logo image."""

    logo_link_url: str = ""
    """Controls where the browser will redirect to after the user clicks the application logo."""

    logo_placement: str = "inside"
    """The placement of your logo. Defaults to 'inside'."""

    privacy_page_url: str = ""
    """The URL to your privacy page."""

    shimmer: bool = True
    """Enables the shimmer animation for avatars. Defaults to true."""

    show_optional_fields: bool = True
    """Whether to show optional fields on the sign in and sign up forms. Defaults to true."""

    social_buttons_placement: str = "top"
    """The placement of your social buttons. Defaults to 'top'."""

    social_buttons_variant: str = "auto"
    """The variant of your social buttons."""

    terms_page_url: str = ""
    """The URL to your terms page."""

    unsafe_disable_development_mode_warnings: bool = False
    """Whether development warnings show up in development mode."""


class Variables(PropsBase):
    color_primary: str = ""
    color_danger: str = ""
    color_success: str = ""
    color_warning: str = ""
    color_neutral: str = ""
    color_text: str = ""
    color_text_on_primary_background: str = ""
    color_text_secondary: str = ""
    color_background: str = ""
    color_input_text: str = ""
    color_input_background: str = ""
    color_shimmer: str = ""
    font_family: str = "inherit"
    font_family_buttons: str = "inherit"
    font_size: str = "0.8125rem"
    font_weight: dict[str, int] = {
        "normal": 400,
        "medium": 500,
        "semibold": 600,
        "bold": 700,
    }
    border_radius: str = "0.375rem"
    spacing_unit: str = "1rem"


class Captcha(PropsBase):
    theme: str = "auto"
    """The CAPTCHA widget theme. Defaults to auto."""

    size: str = "normal"
    """The CAPTCHA widget size. Defaults to normal."""

    language: str = ""
    """The CAPTCHA widget language/locale."""


class Appearance(PropsBase):
    # TODO: This needs to reference the actual theme object, not a string -- don't know how to do that yet.
    # base_theme: LiteralBaseTheme = "default"
    # """A theme used as the base theme for the components."""

    layout: Layout | None = None
    """Configuration options that affect the layout of the components."""

    variables: Variables | None = None
    """General theme overrides."""

    elements: dict[str, Any] | None = None
    """Fine-grained theme overrides."""

    captcha: Captcha | None = None
    """Configuration options that affect the appearance of the CAPTCHA widget."""
