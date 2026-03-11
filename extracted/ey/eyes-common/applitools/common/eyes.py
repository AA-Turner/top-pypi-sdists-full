from __future__ import absolute_import, division, print_function, unicode_literals

from typing import TYPE_CHECKING, List, Optional, Text, Tuple, Union, overload

from .. import common
from ..common.command_executor import CommandExecutor
from ..common.schema import demarshal_locate_result, demarshal_test_results
from . import EyesError, RectangleSize, deprecated
from .config import Configuration
from .extract_text import ImageOCRRegion
from .fluent.check_settings import CheckSettings
from .fluent.images_check_settings import ImagesCheckSettings
from .fluent.target import Target
from .fluent.web_target import WebTarget
from .runner import EyesRunner, log_session_results_and_raise_exception
from .schema import demarshal_locate_text_result
from .target import ImageTarget

if TYPE_CHECKING:
    from typing import ByteString, TypeVar

    from . import Region, TestResults
    from .extract_text import PATTERN_TEXT_REGIONS, Image, OCRRegion, TextRegionSettings
    from .locators import LOCATORS_TYPE, VisualLocatorSettings
    from .optional_deps import (
        ElementHandle,
        Page,
        PlaywrightLocator,
        WebDriver,
        WebElement,
    )
    from .utils.custom_types import FrameReference, ViewPort

    Self = TypeVar("Self", bound="EyesBase")  # typedef


class EyesBase(object):
    _Configuration = Configuration
    _DefaultRunner = EyesRunner

    def __init__(self, runner):
        # type: (Optional[Self._DefaultRunner]) -> None
        self._eyes_ref = None
        # get_results should be possible to call after close so we can't use
        # only _eyes_ref to determine openness anymore.
        self._is_open = False
        self._object_registry = None
        self.configuration = self._Configuration()
        self._runner = runner or self._DefaultRunner()
        self._commands = self._runner._commands  # noqa

    @property
    def configure(self):
        # type: () -> Self._Configuration
        return self.configuration

    @configure.setter
    def configure(self, value):
        self.configuration = value

    def get_configuration(self):
        # type:() -> Self._Configuration
        return self.configuration.clone()

    def set_configuration(self, configuration):
        # type:(Self._Configuration) -> None
        self.configuration = configuration.clone()

    @property
    def is_open(self):
        # type: () -> bool
        return self._is_open

    @property
    def base_agent_id(self):
        # type: () -> Text
        """
        Must return version of SDK. (e.g. selenium, visualgrid) in next format:
            "eyes.{package}.python/{lib_version}"
        """
        return "{}/{}".format(self._runner.BASE_AGENT_ID, common.__version__)

    @property
    def full_agent_id(self):
        # type: () -> Text
        """
        Gets the agent id, which identifies the current library using the SDK.

        """
        if self.configuration.agent_id is None:
            return self.base_agent_id
        else:
            return "{} [{}]".format(self.configuration.agent_id, self.base_agent_id)

    @overload
    def check(self, name, check_settings):
        # type: (Text, ImagesCheckSettings) -> bool
        pass

    @overload
    def check(self, check_settings):
        # type: (ImagesCheckSettings) -> bool
        pass

    def check(self, check_settings, name=None):
        # type: (ImagesCheckSettings, Optional[Text]) -> None
        if isinstance(name, ImagesCheckSettings) or isinstance(check_settings, str):
            check_settings, name = name, check_settings
        if name:
            check_settings = check_settings.with_name(name)

        self._commands.eyes_check(
            self._object_registry,
            self._eyes_ref,
            ImageTarget(check_settings.values.image, check_settings.values.dom),
            check_settings,
            self.configuration,
        )

    def check_image(self, image, tag=None):
        # type: (Union[ByteString, Text, Image], Optional[Text]) -> bool
        return self.check(tag, Target.image(image))

    def locate_text(self, config):
        # type: (TextRegionSettings) -> PATTERN_TEXT_REGIONS
        return self.extract_text_regions(config)

    def extract_text_regions(self, config):
        # type: (TextRegionSettings) -> PATTERN_TEXT_REGIONS
        image = config._image  # noqa
        assert image, "TextRegionSettings has to specify the image to extract text from"
        result = self._commands.core_locate_text(
            ImageTarget(config._image),  # noqa
            config,
            self.configuration,
        )
        return demarshal_locate_text_result(result)

    def extract_text(self, *regions):
        # type: (*ImageOCRRegion) -> List[Text]
        image = regions[0].image
        assert all(r.image == image for r in regions), "All images same"
        return self._commands.core_extract_text(
            ImageTarget(image),
            regions,
            self.configuration,
        )

    def locate(self, visual_locator_settings):
        # type: (VisualLocatorSettings) -> LOCATORS_TYPE
        results = self._commands.core_locate(
            ImageTarget(visual_locator_settings.values.image),
            visual_locator_settings,
            self.configuration,
        )
        return demarshal_locate_result(results)

    def get_results(self, raise_ex=True):
        # type: (bool) -> List[TestResults]
        """
        Wait and return results of checks made after eyes were opened.

        :param raise_ex: raise an exception if at least one check has failed.
        """
        if not self._eyes_ref:
            raise EyesError("Eyes was never open")
        results = self._commands.eyes_get_results(self._eyes_ref, raise_ex)
        if results is not None:
            results = demarshal_test_results(results, self.configuration)
            if results:  # eyes are already aborted by closed runner
                for r in results:
                    log_session_results_and_raise_exception(raise_ex, r)
                return results
        return []

    def close(self, raise_ex=True):
        # type: (bool) -> Optional[TestResults]
        """
        Ends the test.

        :param raise_ex: If true, an exception will be raised for failed/new tests.
        :return: The test results.
        """
        return self._close(raise_ex, True)

    def abort(self):
        # type: () -> Optional[TestResults]
        return self._abort(True)

    def _open(
        self,
        app_name,  # type: Optional[Text]
        test_name,  # type: Optional[Text]
        viewport_size,  # type: Optional[ViewPort]
        target,  # type: Union[None, WebDriver, Page]
    ):
        # type: (...) -> None
        if not self.configuration.is_disabled:
            if app_name is not None:
                self.configuration.app_name = app_name
            if test_name is not None:
                self.configuration.test_name = test_name
            if viewport_size is not None:
                self.configuration.viewport_size = viewport_size
            if self.configuration.app_name is None:
                raise ValueError(
                    "app_name should be set via configuration or an argument"
                )
            if self.configuration.test_name is None:
                raise ValueError(
                    "test_name should be set via configuration or an argument"
                )

            self._runner._set_connection_config(self.configuration)  # noqa, friend
            self._object_registry = self._runner.Protocol.object_registry()
            self._eyes_ref = self._commands.manager_open_eyes(
                self._object_registry,
                self._runner._ref,  # noqa
                target,
                self.configuration,
            )
            self._is_open = True

    def _close(self, raise_ex, wait_result):
        # type: (bool, bool) -> Optional[TestResults]
        if self.configuration.is_disabled:
            return None
        if not self.is_open:
            raise EyesError("Eyes not open")
        self._commands.eyes_close(
            self._object_registry, self._eyes_ref, raise_ex, self.configuration
        )
        results = self.get_results(raise_ex) if wait_result else []
        self._object_registry = None
        self._is_open = False
        # Original interface returns just the first result
        return results[0] if results else None

    def _abort(self, wait_result):
        # type: (bool) -> Optional[TestResults]
        if self.configuration.is_disabled:
            return None
        elif self.is_open:
            self._commands.eyes_abort(self._object_registry, self._eyes_ref)
            results = self.get_results(False) if wait_result else None
            self._object_registry = None
            self._is_open = False
            # Original interface returns just the first result
            return results[0] if results else None

    def __getattr__(self, item):
        return getattr(self.configuration, item)

    def __setattr__(self, key, value):
        if "configuration" in vars(self) and (
            key in vars(self.configuration)
            or key in ("match_level", "ignore_displacements")
        ):
            return setattr(self.configuration, key, value)
        else:
            return super(EyesBase, self).__setattr__(key, value)


class WebEyes(EyesBase):
    Target = WebTarget

    def __init__(self, runner=None):
        # type: (Union[None, EyesRunner, Text]) -> None
        if isinstance(runner, str):
            server_url = runner
            runner = None
        else:
            server_url = None
        super(WebEyes, self).__init__(runner)
        self.driver = None
        if server_url:
            self.configuration.set_server_url(server_url)

    def open(
        self,
        driver,  # type: Union[WebDriver, Page]
        app_name=None,  # type: Optional[Text]
        test_name=None,  # type: Optional[Text]
        viewport_size=None,  # type: Optional[ViewPort]
    ):
        # type: (...) -> Union[WebDriver, Page]
        self._open(app_name, test_name, viewport_size, driver)
        self.driver = driver
        return driver

    @overload
    def check(self, name, check_settings):
        # type: (Text, CheckSettings) -> None
        """
        Takes a snapshot and matches it with the expected output.

        :param name: The name of the tag.
        :param check_settings: target which area of the window to check.
        """
        pass

    @overload
    def check(self, check_settings):
        # type: (CheckSettings) -> None
        """
        Takes a snapshot and matches it with the expected output.

        :param check_settings: target which area of the window to check.
        """
        pass

    def check(self, check_settings, name=None):
        # type: (CheckSettings, Optional[Text]) -> None
        if isinstance(name, CheckSettings) or isinstance(check_settings, str):
            check_settings, name = name, check_settings
        if type(check_settings) is ImagesCheckSettings:
            return super(WebEyes, self).check(check_settings, name)
        if check_settings is None:
            check_settings = self.Target.window()
        if name:
            check_settings = check_settings.with_name(name)

        if self.configuration.is_disabled:
            return
        if not self.is_open:
            self.abort()
            raise EyesError("you must call open() before checking")

        self._commands.eyes_check(
            self._object_registry,
            self._eyes_ref,
            None,
            check_settings,
            self.configuration,
        )

    def locate(self, visual_locator_settings):
        # type: (VisualLocatorSettings) -> LOCATORS_TYPE
        if visual_locator_settings.values.image:  # noqa
            return super(WebEyes, self).locate(visual_locator_settings)
        else:
            results = self._commands.core_locate(
                self.driver,
                visual_locator_settings,
                self.configuration,
            )
            return demarshal_locate_result(results)

    def extract_text(self, *regions):
        # type: (*OCRRegion) -> List[Text]
        first_region = regions[0]
        assert all(
            type(r) is type(first_region) for r in regions
        ), "Regions should be same type"
        if isinstance(first_region, ImageOCRRegion):
            return super(WebEyes, self).extract_text(*regions)
        else:
            return self._commands.core_extract_text(
                self.driver,
                regions,
                self.configuration,
            )

    def extract_text_regions(self, config):
        # type: (TextRegionSettings) -> PATTERN_TEXT_REGIONS
        if config._image:  # noqa
            return super(WebEyes, self).extract_text_regions(config)
        else:
            return self._commands.core_locate_text(
                self.driver, config, self.configuration
            )

    def close(self, raise_ex=True):
        # type: (bool) -> Optional[TestResults]
        """
        Ends the test.

        :param raise_ex: If true, an exception will be raised for failed/new tests.
        :return: The test results.
        """
        self.driver = None
        return super(WebEyes, self).close(raise_ex)

    def close_async(self):
        # type: () -> Optional[TestResults]
        self.driver = None
        return self._close(False, False)

    def abort(self):
        # type: () -> Optional[TestResults]
        """
        If a test is running, aborts it. Otherwise, does nothing.
        """
        self.driver = None
        return super(WebEyes, self).abort()

    def abort_async(self):
        self.driver = None
        return self._abort(False)

    @deprecated.attribute("use `abort()` instead")
    def abort_if_not_closed(self):
        return self.abort()

    @classmethod
    def get_viewport_size(cls, driver):
        # type: (Union[WebDriver, Page]) -> RectangleSize
        cmd = CommandExecutor.get_instance(cls._DefaultRunner.Protocol)
        result = cmd.core_get_viewport_size(driver)
        return RectangleSize.from_(result)

    @classmethod
    def set_viewport_size(cls, driver, viewport_size):
        # type: (Union[WebDriver, Page], ViewPort) -> None
        cmd = CommandExecutor.get_instance(cls._DefaultRunner.Protocol)
        cmd.core_set_viewport_size(driver, viewport_size)

    def check_window(self, tag=None, match_timeout=-1, fully=None):
        # type: (Optional[Text], int, Optional[bool]) -> None
        """
        Takes a snapshot of the application under test and matches it with the expected
         output.

        :param tag: An optional tag to be associated with the snapshot.
        :param match_timeout:  The amount of time to retry matching (milliseconds)
        :param fully: Defines that the screenshot will contain the entire window.
        """
        return self.check(tag, self.Target.window().timeout(match_timeout).fully(fully))

    def check_frame(self, frame_reference, tag=None, match_timeout=-1):
        # type: (FrameReference, Optional[Text], int) -> None
        """
        Check frame.

        :param frame_reference: The name or id of the frame to check. (The same
                name/id as would be used in a call to driver.switch_to.frame()).
        :param tag: An optional tag to be associated with the match.
        :param match_timeout: The amount of time to retry matching. (Milliseconds)
        """
        return self.check(
            tag, self.Target.frame(frame_reference).fully().timeout(match_timeout)
        )

    def check_region(
        self,
        region,  # type: Union[Region, Text, List, Tuple, WebElement]
        tag=None,  # type: Optional[Text]
        match_timeout=-1,  # type: int
        stitch_content=False,  # type: bool
    ):
        # type: (...) -> None
        """
        Takes a snapshot of the given region from the browser using the web driver
        and matches it with the expected output. If the current context is a frame,
        the region is offsetted relative to the frame.

        :param region: The region which will be visually validated. The coordinates are
                       relative to the viewport of the current frame.
        :param tag: Description of the visual validation checkpoint.
        :param match_timeout: Timeout for the visual validation checkpoint
                              (milliseconds).
        :param stitch_content: If `True`, stitch the internal content of the region
        """
        return self.check(
            tag,
            self.Target.region(region).timeout(match_timeout).fully(stitch_content),
        )

    def check_element(
        self,
        element,
        # type: Union[Text,List,Tuple,WebElement,PlaywrightLocator,ElementHandle]
        tag=None,  # type: Optional[Text]
        match_timeout=-1,  # type: int
    ):
        # type: (...) -> None
        """
        Takes a snapshot of the given region from the browser using the web driver
        and matches it with the expected output. If the current context is a frame,
        the region is offsetted relative to the frame.

        :param element: The element to check.
        :param tag: Description of the visual validation checkpoint.
        :param match_timeout: Timeout for the visual validation checkpoint
                              (milliseconds).
        """
        return self.check(
            tag,
            self.Target.region(element).timeout(match_timeout).fully(),
        )

    def check_region_in_frame(
        self,
        frame_reference,  # type: FrameReference
        region,
        # type: Union[Region,Text,List,Tuple,WebElement,PlaywrightLocator,ElementHandle]
        tag=None,  # type: Optional[Text]
        match_timeout=-1,  # type: int
        stitch_content=False,  # type: bool
    ):
        # type: (...) -> None
        """
        Checks a region within a frame, and returns to the current frame.

        :param frame_reference: A reference to the frame in which the region
                                should be checked.
        :param region: Specifying the region to check inside the frame.
        :param tag: Description of the visual validation checkpoint.
        :param match_timeout: Timeout for the visual validation checkpoint
                              (milliseconds).
        :param stitch_content: If `True`, stitch the internal content of the region
        """
        return self.check(
            tag,
            self.Target.region(region)
            .frame(frame_reference)
            .stitch_content(stitch_content)
            .timeout(match_timeout),
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver = None
        if exc_type:
            self._abort(self._runner.AUTO_CLOSE_MODE_SYNC)
        else:
            self._close(True, self._runner.AUTO_CLOSE_MODE_SYNC)
