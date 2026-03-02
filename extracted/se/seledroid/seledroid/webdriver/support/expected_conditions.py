from seledroid.webdriver.remote.web_element import WebElement


def find_element(driver, locator, command):
    locator = driver.find_element(*locator, command)
    return locator if isinstance(locator, WebElement) else False


def presence_of_element_located(locator):
    def _predicate(driver, _locator, command):
        _locator = find_element(driver, _locator, command)
        return True if _locator and _locator.element.result else _locator

    return lambda driver, command: _predicate(driver, locator, command)


def visibility_of_element_located(locator):
    def _predicate(driver, _locator, command):
        _locator = find_element(driver, _locator, command)
        return _locator if _locator and _locator.element.result and _locator.is_displayed else False

    return lambda driver, command: _predicate(driver, locator, command)


def invisibility_of_element_located(locator):
    def _predicate(driver, _locator, command):
        _locator = find_element(driver, _locator, command)
        return _locator if _locator and _locator.element.result and not _locator.is_displayed else False

    return lambda driver, command: _predicate(driver, locator, command)


def element_to_be_clickable(locator):
    def _predicate(driver, _locator, command):
        _locator = find_element(driver, _locator, command)
        return _locator if _locator and _locator.element.result and _locator.is_displayed and not _locator.disabled else False

    return lambda driver, command: _predicate(driver, locator, command)
