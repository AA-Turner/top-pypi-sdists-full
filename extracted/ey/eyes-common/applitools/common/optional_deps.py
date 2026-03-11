from __future__ import absolute_import, division, print_function

try:
    from os import PathLike, fspath
except ImportError:

    class PathLibNotAvailable(object):
        def __init__(self, *_, **__):
            raise RuntimeError("Please upgrade to python>=3.6 to use path-like objs")

    PathLike = PathLibNotAvailable
    fspath = PathLibNotAvailable


try:
    from PIL.Image import Image
except ImportError:

    class Image(object):
        def __init__(self, *_, **__):
            raise RuntimeError("pillow package is required for this functionality")

        save = __init__


try:
    from appium.webdriver import WebElement as AppiumWebElement
except (ImportError, TypeError):
    # TypeError is related to Appium-Python-Client above 5+ where they use tuple[...] syntax
    class AppiumWebElement(object):
        def __init__(self, *_, **__):
            raise RuntimeError(
                "appium-python-client package is required for this functionality"
            )


try:
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.webdriver.common.by import By
    from selenium.webdriver.remote.webdriver import WebDriver
    from selenium.webdriver.remote.webelement import WebElement
    from selenium.webdriver.support.event_firing_webdriver import EventFiringWebElement
except ImportError:

    class SeleniumNotInstalled(object):
        def __init__(self, *_, **__):
            raise RuntimeError("selenium package is required for this functionality")

    By = SeleniumNotInstalled
    EventFiringWebElement = SeleniumNotInstalled
    StaleElementReferenceException = SeleniumNotInstalled
    WebDriver = SeleniumNotInstalled
    WebElement = SeleniumNotInstalled

try:
    from playwright.sync_api import ElementHandle
    from playwright.sync_api import Locator as PlaywrightLocator
    from playwright.sync_api import Page
except ImportError:

    class PlaywrightNotInstalled(object):
        def __init__(self, *_, **__):
            raise RuntimeError("playwright package is required for this functionality")

    Page = PlaywrightNotInstalled
    PlaywrightLocator = PlaywrightNotInstalled
    ElementHandle = PlaywrightNotInstalled
