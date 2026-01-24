from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.wait import WebDriverWait

from .e2e_helper_methods import find_element


def does_background_color_match(element: WebElement, expected_color: str) -> bool:
    """Check if the background color of an element matches the expected color.

    Args:
        element (WebElement): The element to check the background of.
        expected_color (str): The expected color.

    Returns:
        bool: True if the background color is as expected
    """
    element_rgb = element.value_of_css_property("background-color")
    element_rgb = Color.from_string(element_rgb).rgb
    return element_rgb == expected_color


def is_text_visible(driver: WebDriver, text: str) -> bool:
    """Check if the searched text is visible on the current page.

    Args:
        driver (WebDriver): The Selenium webdriver.
        text (str): Searched text.

    Returns:
        bool: True if the text is visible
    """
    return True if find_element(driver, f"//*[text()='{text}']") else False


def is_string_not_visible(driver: WebDriver, string: str) -> bool:
    """Check if the searched text is not visible on the current page.
    Sometimes selenium is faster, that the page can refresh. So this method can wait up to 10 seconds for a string to not be visible.

    Args:
        driver (WebDriver): The Selenium webdriver.
        text (str): Searched text.

    Returns:
        bool: True if the text is not visible
    """
    try:
        WebDriverWait(driver, 5).until(
            expected_conditions.invisibility_of_element_located((By.XPATH, f"//*[text()='{string}']"))
        )
        return True
    except TimeoutException:
        return False


def is_tag_visible(driver: WebDriver, tag_label: str) -> bool:
    """Check if a tag with a certain label is visible on the current page.

    Args:
        driver (WebDriver): The Selenium webdriver.
        text (str): The label text.


    Returns:
        bool: True if the label is visible
    """
    return True if find_element(driver, f"//*[@class='tag-label' and text()='{tag_label}']") else False


def is_tag_not_visible(driver: WebDriver, tag_label: str) -> bool:
    """Check if a tag with a certain label is not visible on the current page.
    Sometimes selenium is faster, that the page can refresh. So this method can wait up to 10 seconds for a tag to not be visible.

    Args:
        driver (WebDriver): The Selenium webdriver.
        text (str): The label text.

    Returns:
        bool: True if the tag is not visible
    """
    try:
        WebDriverWait(driver, 2.5).until(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, f"//*[@class='tag-label' and text()='{tag_label}']")
            )
        )
        return True
    except TimeoutException:
        return False


def is_error_visible(driver: WebDriver):
    """Check if an error element is visible on the current page.

    Args:
        driver (WebDriver): The Selenium webdriver.

    Returns:
        bool: True if an error element is visible
    """
    error_element = find_element(driver, "//div[contains(@type, 'error')]", 2.5)
    saving_failed_hint = find_element(driver, "//div[contains(@class, 'task-dropper-content')]", 2.5)

    if saving_failed_hint and saving_failed_hint.is_displayed():
        WebDriverWait(driver, 10).until_not(
            expected_conditions.invisibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'task-dropper-content')]")
            )
        )
    return error_element is not None


def is_counter_as_expected(driver: WebDriver, count: int):
    """Check if list counter displays the right number.

    Args:
        driver (WebDriver): The Selenium webdriver.

    Returns:
        bool: True if the counter is right.
    """
    find_element(driver, f"//span[@class='ag-status-name-value-value' and text()='{count}']")
    return find_element is not None
