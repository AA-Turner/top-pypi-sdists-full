from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class VisibilityItem(str, Enum):
    DISPLAY_NONE = "display:none"
    VISIBILITY_HIDDEN = "visibility:hidden"
    ARIA_HIDDEN_TRUE = "aria-hidden:true"
    HTML_HIDDEN = "hidden"


NOISE_ROLE: list[str] = [
    "navigation",
    "banner",
    "complementary",
    "menu",
    "dialog",
    "menuitem",
    "figure",
    "icon",
    "picture",
    "toolbar",
    "menubar",
]

NOISE_NAME: list[str] = [
    "header",
    "footer",
    "sidebar",
    "bridged-flipcard-div",
    "script",
    "style",
    "svg",
    "head",
    "select",
    "button",
    "figure",
    "fieldset",
    "form",
    "section",
    "mbox-text-span",
    "sidebar-section",
]

NOISE_CLASS: list[str] = [
    "ui-consent-roadblock",
    "w3-sidebar",
    "interlanguage-link-target",
    "breadcrumb",
    "hidden-xs",
    "subnav-container",
    "visually-hidden",
    "show-comments",
    "notification-prompt",
    "newsletter-component",
    "news-letter-title",
    "header",
    "footer",
    "sidebar",
    "ad",
    "menu",
    "popup",
    "modal",
    "google-dfp-ad-wrapper",
    "TaboolaRecommendationModule",
    "sr-only",
    "ad-feedback-link",
    "share",
    "social",
    "advert",
    "promo",
    "overlay",
    "icon",
    "mbox-text-span",
    "sidebar-section",
]

NOISE_TAG: list[str] = [
    "label",
    "iframe",
    "header",
    "script",
    "style",
    "svg",
    "head",
    "nav",
    "footer",
    "select",
    "button",
    "fieldset",
    "mbox-text-span",
    "sidebar-section",
    "aside",
    "ps-header",
    "ps-section-nav",
    "ps-actionbar",
    "ps-gift-article-modal",
    "ps-newsletter-module",
    "bsp-page-actions",
    "bsp-header",
    "noscript",
    "link",
]

NOISE_ID: list[str] = [
    "success-hint",
    "success-hint-header",
    "read-next",
    "popover-content",
    "accessibility-banner",
]

NOISE_DATA_CONTENT: list[str] = []

NOISE_VISIBILITY: list[str] = [
    VisibilityItem.DISPLAY_NONE.value,
    VisibilityItem.VISIBILITY_HIDDEN.value,
    VisibilityItem.ARIA_HIDDEN_TRUE.value,
    VisibilityItem.HTML_HIDDEN.value,
]


@dataclass
class BaseRemoverConfig:
    override: bool = False
    add_items: list[str] = field(default_factory=list)
    remove_items: list[str] = field(default_factory=list)

    def get_standard_items(self) -> list[str]:
        raise NotImplementedError


@dataclass
class RoleConfig(BaseRemoverConfig):
    def get_standard_items(self) -> list[str]:
        return NOISE_ROLE


@dataclass
class NameConfig(BaseRemoverConfig):
    def get_standard_items(self) -> list[str]:
        return NOISE_NAME


@dataclass
class ClassConfig(BaseRemoverConfig):
    def get_standard_items(self) -> list[str]:
        return NOISE_CLASS


@dataclass
class TagConfig(BaseRemoverConfig):
    def get_standard_items(self) -> list[str]:
        return NOISE_TAG


@dataclass
class IdConfig(BaseRemoverConfig):
    def get_standard_items(self) -> list[str]:
        return NOISE_ID


@dataclass
class DataContentConfig(BaseRemoverConfig):
    def get_standard_items(self) -> list[str]:
        return NOISE_DATA_CONTENT


@dataclass
class VisibilityConfig(BaseRemoverConfig):
    add_items: list[VisibilityItem] = field(default_factory=list)
    remove_items: list[VisibilityItem] = field(default_factory=list)

    def get_standard_items(self) -> list[str]:
        return NOISE_VISIBILITY

    def _determine_list(self) -> list[str]:
        standard = list(self.get_standard_items())
        if not self.override:
            return standard
        result = set(standard)
        if self.add_items:
            result.update(item.value for item in self.add_items)
        if self.remove_items:
            result.difference_update(item.value for item in self.remove_items)
        return list(result)


@dataclass
class NoiseRemoverConfig:
    role: RoleConfig = field(default_factory=RoleConfig)
    name: NameConfig = field(default_factory=NameConfig)
    class_: ClassConfig = field(default_factory=ClassConfig)
    tag: TagConfig = field(default_factory=TagConfig)
    id_: IdConfig = field(default_factory=IdConfig)
    data_content: DataContentConfig = field(default_factory=DataContentConfig)
    visibility: VisibilityConfig = field(default_factory=VisibilityConfig)
