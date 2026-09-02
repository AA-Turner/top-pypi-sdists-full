from __future__ import annotations

import copy

import bs4

from .noise_config import (
    NoiseRemoverConfig,
    BaseRemoverConfig,
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
            VisibilityNoiseRemover(cfg.visibility),
        ]

    def remove_noise(self, soup: bs4.BeautifulSoup, remove: bool = False) -> bs4.BeautifulSoup:
        original = copy.deepcopy(soup)
        processed = copy.deepcopy(soup)

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
