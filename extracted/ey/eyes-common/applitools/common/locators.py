from __future__ import absolute_import, division, print_function

from copy import copy
from typing import Dict, List, Text, Union

import attr

from .geometry import Region
from .utils import argument_guard
from .validators import is_list_or_tuple

__all__ = ("VisualLocator", "VisualLocatorSettings")

LOCATORS_TYPE = Dict[Text, List[Region]]  # typedef


def _clean_names(names):
    argument_guard.not_list_or_tuple(names)
    if len(names) == 1 and is_list_or_tuple(names[0]):
        names = names[0]
    argument_guard.are_(names, klass=str)
    return names


@attr.s
class VisualLocatorSettingsValues(object):
    names = attr.ib()  # type: List[Text]
    first_only = attr.ib(default=True)  # type: bool
    image = attr.ib(default=None)  # type: Text | None

    @property
    def is_first_only(self):
        # type: () -> bool
        return self.first_only


class VisualLocatorSettings(object):
    def __init__(self, *names):
        # type: (*Text) -> None
        self.values = VisualLocatorSettingsValues(names=list(names))

    def first(self):
        # type: () -> VisualLocatorSettings
        clone = self.clone()
        clone.values.first_only = True
        return clone

    def all(self):
        # type: () -> VisualLocatorSettings
        clone = self.clone()
        clone.values.first_only = False
        return clone

    def clone(self):
        # type: () -> VisualLocatorSettings
        return copy(self)

    def name(self, name):
        # type: (Text) -> VisualLocatorSettings
        argument_guard.is_a(name, str)
        cloned = self.clone()
        cloned.values.names.append(name)
        return cloned

    def names(self, *names):
        # type: (*Union[Text, List[Text]]) -> VisualLocatorSettings
        cleaned_names = _clean_names(names)
        cloned = self.clone()
        cloned.values.names = cleaned_names
        return cloned

    def image(self, image):
        # type: (Text) -> VisualLocatorSettings
        argument_guard.is_a(image, str)
        cloned = self.clone()
        cloned.values.image = image
        return cloned


class VisualLocator(object):
    @staticmethod
    def name(name):
        # type: (Text) -> VisualLocatorSettings
        argument_guard.is_a(name, str)
        return VisualLocatorSettings(name)

    @staticmethod
    def names(*names):
        # type: (*Union[Text, List[Text]]) -> VisualLocatorSettings
        return VisualLocatorSettings(*_clean_names(names))


@attr.s
class VisualLocatorsData(object):
    app_name = attr.ib()
    image_url = attr.ib()
    first_only = attr.ib()
    locator_names = attr.ib()
