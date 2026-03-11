from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING

from .context_vars import set_object_registry
from .schema import (
    CheckSettings,
    CloseBatchSettings,
    CloseSettings,
    DeleteTestSettings,
    ECClientSettings,
    ExtractTextSettings,
    EyesConfig,
    ImageTarget,
    LocateSettings,
    OCRSearchSettings,
    OpenSettings,
    Size,
)

if TYPE_CHECKING:
    from typing import List, Tuple

    from .. import common
    from . import config as cfg
    from . import ec_client_settings, extract_text, locators
    from . import target as t
    from .batch_close import _EnabledBatchClose  # noqa
    from .fluent import selenium_check_settings as cs
    from .object_registry import ObjectRegistry
    from .optional_deps import WebDriver
    from .utils.custom_types import ViewPort


class Marshaller(object):
    def __init__(self, object_registry):
        # type: (ObjectRegistry) -> None
        self._object_registry = object_registry

    def marshal_viewport_size(self, viewport_size):
        # type: (ViewPort) -> dict
        with set_object_registry(self._object_registry):
            return Size().dump(viewport_size)

    def marshal_webdriver_ref(self, driver):
        # type: (WebDriver) -> dict
        return self._object_registry.marshal_driver(driver)

    def marshal_ec_client_settings(self, client_settings):
        # type: (ec_client_settings.ECClientSettings) -> dict
        return ECClientSettings().dump(client_settings)

    def marshal_enabled_batch_close(self, close_batches):
        # type: (_EnabledBatchClose) -> dict
        with set_object_registry(self._object_registry):
            return CloseBatchSettings().dump(close_batches)

    def marshal_delete_test_settings(self, test_results):
        # type: (common.TestResults) -> dict
        with set_object_registry(self._object_registry):
            return DeleteTestSettings().dump(test_results)

    def marshal_configuration(self, configuration):
        # type: (cfg.Configuration) -> dict
        with set_object_registry(self._object_registry):
            open = OpenSettings().dump(configuration)
            config = EyesConfig().dump(configuration)
            close = CloseSettings().dump(configuration)
            return {"open": open, "screenshot": config, "check": config, "close": close}

    def marshal_check_settings(self, check_settings):
        # type: (cs.SeleniumCheckSettings) -> dict
        with set_object_registry(self._object_registry):
            return CheckSettings().dump(check_settings.values)

    def marshal_image_target(self, image_target):
        # type: (t.ImageTarget) -> dict
        with set_object_registry(self._object_registry):
            return ImageTarget().dump(image_target)

    def marshal_locate_settings(self, locate_settings):
        # type: (locators.VisualLocatorSettings) -> dict
        with set_object_registry(self._object_registry):
            return LocateSettings().dump(locate_settings.values)

    def marshal_ocr_extract_settings(self, extract_settings):
        # type: (Tuple[extract_text.OCRRegion, ...]) -> List[dict]
        with set_object_registry(self._object_registry):
            return [ExtractTextSettings().dump(s) for s in extract_settings]

    def marshal_ocr_search_settings(self, search_settings):
        # type: (extract_text.TextRegionSettings) -> dict
        with set_object_registry(self._object_registry):
            return OCRSearchSettings().dump(search_settings)
