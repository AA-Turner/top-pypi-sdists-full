from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium import webdriver
import time
import re


def query_cleaner(query: str) -> str:
    """
    Cleans up a query by removing extra spaces.

    Parameters:
    - query (str): The input query to be cleaned.

    Returns:
    - str: The cleaned query.
    """

    return " ".join(filter(lambda x: x != "", query.split(" ")))


def cleanup(dimension: str) -> int:
    """
    Cleans up a dimension value by converting it to an integer.

    Parameters:
    - dimension (str): The dimension value to be cleaned.

    Returns:
    - int: The cleaned integer value.
    """

    try:
        # Use regular expression to find the first occurrence of a number in the string
        match = re.search(r"\d+", dimension)

        if match:
            # Extract the matched number and convert it to an integer
            return int(match.group())
        else:
            # Return 0 if no number is found in the string
            return 0
    except Exception as e:
        return 0


def disable_safesearch(
    driver: webdriver.Chrome, action: ActionChains, wait: WebDriverWait
) -> bool:
    """
    Disables SafeSearch in a Google search page using Selenium.

    Parameters:
    - driver (webdriver.Chrome): The Chrome WebDriver instance.
    - action (ActionChains): The ActionChains instance for performing actions.
    - wait (WebDriverWait): The WebDriverWait instance for waiting for elements.

    Returns:
    - bool: True if SafeSearch is successfully disabled, False otherwise.
    """

    try:
        safesearch_dropdown = driver.find_elements(By.CLASS_NAME, "CgGjZc")[-1]
        action.click(safesearch_dropdown).perform()

        off_button = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "#lb > div > g-menu > g-menu-item:nth-child(3)")
            )
        )

        action.click(off_button).perform()

    except Exception as e:
        # print(e)
        return False

    return True


def scroll_range(action: ActionChains, count: int):
    for _ in range(count):
        action.send_keys(Keys.END).perform()
        time.sleep(0.5)
