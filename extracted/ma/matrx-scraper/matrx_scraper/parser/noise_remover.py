from __future__ import annotations

import copy
import re

import bs4

from .noise_config import (
    NoiseRemoverConfig,
    BaseRemoverConfig,
    NavMarkerConfig,
    VisibilityConfig,
    VisibilityItem,
)


class BaseNoiseRemover:
    def __init__(self, config: BaseRemoverConfig):
        self.config = config
        self.standard_items = self.config.get_standard_items()
        self.items = self._determine_list()

    def _determine_list(self) -> list[str]:
        if not self.config.override:
            return self.standard_items
        result = set(self.standard_items)
        if self.config.add_items:
            result.update(self.config.add_items)
        if self.config.remove_items:
            result.difference_update(self.config.remove_items)
        return list(result)

    def prepare(self, soup: bs4.BeautifulSoup) -> None:
        """Called once per `remove_noise` pass before any element is checked."""

    def check_element(self, element: bs4.Tag, soup=None) -> tuple[bool, str | None]:
        raise NotImplementedError


class RoleNoiseRemover(BaseNoiseRemover):
    def check_element(self, element, soup=None):
        if element and element.attrs and element.has_attr("role"):
            if element["role"] in self.items:
                return True, element["role"]
        return False, None


class NameNoiseRemover(BaseNoiseRemover):
    def check_element(self, element, soup=None):
        if element and element.attrs and element.has_attr("name"):
            if element["name"] in self.items:
                return True, element["name"]
        return False, None


class ClassNoiseRemover(BaseNoiseRemover):
    def check_element(self, element, soup=None):
        if element and element.attrs and element.has_attr("class"):
            cls_str = " ".join(element["class"])
            cls_set = set(element["class"])
            if cls_str in self.items:
                return True, cls_str
            for cls in self.items:
                if cls in cls_set:
                    return True, cls
        return False, None


class JunkTagNoiseRemover(BaseNoiseRemover):
    def check_element(self, element, soup=None):
        if element and element.name in self.items:
            return True, element.name
        return False, None


class IdNoiseRemover(BaseNoiseRemover):
    def check_element(self, element, soup=None):
        if element and element.attrs and element.has_attr("id"):
            if element["id"] in self.items:
                return True, element["id"]
        return False, None


class DataContentNoiseRemover(BaseNoiseRemover):
    def check_element(self, element, soup=None):
        if element and element.attrs and element.has_attr("data-content"):
            if element["data-content"] in self.items:
                return True, element["data-content"]
        return False, None


_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
_SEGMENT_SPLIT = re.compile(r"[-_\s]+")
_MAIN_CONTENT_TAGS = ("main", "article")


def _segments(token: str) -> list[str]:
    """`site-nav` → [site, nav]; `mainNav` → [main, nav]; `skip_links` → [skip, links]."""
    return [s for s in _SEGMENT_SPLIT.split(_CAMEL_BOUNDARY.sub("-", token).lower()) if s]


class NavMarkerNoiseRemover(BaseNoiseRemover):
    """Segment-rule matcher for navigation chrome on `class` / `id`.

    Rule and rationale: `NOISE_NAV_MARKER` in noise_config.py. Guarded so the
    page's main content is never removed by the heuristic.
    """

    def __init__(self, config: NavMarkerConfig):
        super().__init__(config)
        self._words = {item for item in self.items if "-" not in item}
        self._phrases = [tuple(_segments(item)) for item in self.items if "-" in item]
        self._body_text_len = 0

    def prepare(self, soup: bs4.BeautifulSoup) -> None:
        body = soup.body if soup is not None else None
        self._body_text_len = len((body or soup).get_text(" ", strip=True)) if soup is not None else 0

    def _marker_for(self, token: str) -> str | None:
        segs = _segments(token)
        for seg in segs:
            if seg in self._words:
                return seg
        for phrase in self._phrases:
            n = len(phrase)
            for i in range(len(segs) - n + 1):
                if tuple(segs[i : i + n]) == phrase:
                    return "-".join(phrase)
        return None

    def _is_main_content(self, element: bs4.Tag) -> bool:
        if element.name in _MAIN_CONTENT_TAGS:
            return True
        if element.find_parent(_MAIN_CONTENT_TAGS) is not None:
            return True
        if element.find(_MAIN_CONTENT_TAGS) is not None:
            return True
        if self._body_text_len:
            own = len(element.get_text(" ", strip=True))
            if own * 2 > self._body_text_len:
                return True
        return False

    def check_element(self, element, soup=None):
        if not element or not element.attrs:
            return False, None
        candidates: list[str] = []
        if element.has_attr("id"):
            candidates.append(str(element["id"]))
        if element.has_attr("class"):
            candidates.extend(element["class"])
        for token in candidates:
            marker = self._marker_for(token)
            if marker is not None:
                if self._is_main_content(element):
                    return False, None
                return True, f"{marker} (in {token!r})"
        return False, None


class VisibilityNoiseRemover(BaseNoiseRemover):
    def __init__(self, config: VisibilityConfig):
        self.config = config
        self.items = config._determine_list()

    def check_element(self, element, soup=None):
        if not element or not element.attrs:
            return False, None

        for item in self.items:
            if item == VisibilityItem.ARIA_HIDDEN_TRUE.value:
                if element.get("aria-hidden") == "true":
                    return True, item
            elif item == VisibilityItem.HTML_HIDDEN.value:
                if element.has_attr("hidden"):
                    return True, item
            elif item in (
                VisibilityItem.DISPLAY_NONE.value,
                VisibilityItem.VISIBILITY_HIDDEN.value,
            ):
                style = element.get("style", "").lower().strip()
                if style:
                    styles = dict(s.split(":", 1) for s in style.split(";") if ":" in s)
                    if (
                        item == VisibilityItem.DISPLAY_NONE.value
                        and styles.get("display", "").strip() == "none"
                    ) or (
                        item == VisibilityItem.VISIBILITY_HIDDEN.value
                        and styles.get("visibility", "").strip() == "hidden"
                    ):
                        return True, item

        return False, None


class NoiseRemover:
    def __init__(self, config: NoiseRemoverConfig | None = None):
        cfg = config or NoiseRemoverConfig()
        self.removers = [
            RoleNoiseRemover(cfg.role),
            NameNoiseRemover(cfg.name),
            ClassNoiseRemover(cfg.class_),
            JunkTagNoiseRemover(cfg.tag),
            IdNoiseRemover(cfg.id_),
            DataContentNoiseRemover(cfg.data_content),
            NavMarkerNoiseRemover(cfg.nav_marker),
            VisibilityNoiseRemover(cfg.visibility),
        ]

    def remove_noise(self, soup: bs4.BeautifulSoup, remove: bool = False) -> bs4.BeautifulSoup:
        original = copy.deepcopy(soup)
        processed = copy.deepcopy(soup)
        for remover in self.removers:
            remover.prepare(original)

        elements_to_remove = []
        for element in processed.find_all():
            if element.name == "NoiseRemover":
                continue
            for remover in self.removers:
                is_noise, trigger_item = remover.check_element(element, soup=original)
                if is_noise:
                    if remove:
                        elements_to_remove.append(element)
                    else:
                        noise_tag = processed.new_tag(
                            "NoiseRemover",
                            type=remover.__class__.__name__,
                            trigger_item=trigger_item,
                        )
                        element.wrap(noise_tag)
                    break

        if remove:
            for element in elements_to_remove:
                element.decompose()

        return processed
