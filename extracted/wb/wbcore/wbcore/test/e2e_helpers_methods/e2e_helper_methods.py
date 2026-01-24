from pytest_django.live_server_helper import LiveServer
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from wbcore import serializers as wb_serializers

WAIT_TIME_SEC = 30


def login(driver: WebDriver, user_mail: str | None, user_password: str | None):
    """Automatically logs in a user into the workbench.

    Args:
        driver (WebDriver): Selenium webdriver.
        user_mail (str | None): The users email.
        user_password (str | None): The users password
    """
    write_text(driver, "//input[@placeholder='E-Mail']", user_mail)
    write_text(driver, "//input[@placeholder='Password']", user_password)
    click_element_by_path(driver, "//button[@label='Login']")


def set_up(driver: WebDriver, server: LiveServer, user_mail: str, user_password: str):
    """Used for setting up the test environment and needs to be called before executing the test logic.

    Args:
        driver (WebDriver): Selenium webdriver.
        server (LiveServer): Live server.
        user_mail (str): The email of the user used for authentication.
        user_password (str): The password of the user used for authentication.
    """
    driver.get(server.url)
    driver.set_window_size(1920, 1080)
    login(driver, user_mail, user_password)


def open_menu_item(driver: WebDriver, *menu_items, perform_mouse_move=False):
    """Automatically opens a menu item of the CRM.

    Args:
        driver (WebDriver): The Selenium webdriver.
        *menu_items: The path to the menu item you want to open (e.g. for Person you would have to insert "CRM", "Persons" to get to the person list.)
        perform_mouse_move (bool, optional): Should the mouse move after opening the correct menu item. This can be helpful, when the navigation bar block certain things. When moving the mouse away from the navigation bar, the bar will collapse. Defaults to False.
    """
    actions = ActionChains(driver, 1000)
    ele = find_element(driver, "//div[@title='Navigation']")
    actions.move_to_element(ele).perform()

    for menu_item in menu_items:
        click_element_by_path(driver, f"//div[@title='{menu_item}']")

    if perform_mouse_move:
        window_width = (driver.get_window_size().get("width")) / 1.75
        actions.move_by_offset(window_width, 0).perform()
        actions.click()


def open_create_instance(driver: WebDriver, *menu_items: str, create_instance_title: str):
    """Opens a create instance widget

    Args:
        driver (WebDriver): The Selenium webdriver.
        *menu_items: The path to the menu item you want to open (e.g. for Person you would have to insert "CRM", "Persons" to get to the person list.)
        create_instance_title (str): The title of the create instance button (e.g. Create Activity)
    """
    actions = ActionChains(driver, 1000)
    open_menu_item(driver, *menu_items)
    click_element_by_path(driver, f"//span[@title='{create_instance_title}']")
    window_width = (driver.get_window_size().get("width")) / 2
    actions.move_by_offset(window_width, 0).perform()


def write_text(driver: WebDriver, xpath: str, text: str) -> WebElement:
    """Writes a given text into an element. Requires the element to be writable.

    Args:
        driver (WebDriver): Selenium webdriver.
        xpath (str): The xpath leading to the element.
        text (str): The desired text.

    Returns:
        WebElement: The element in which it was written.
    """
    element = find_element(driver, xpath)
    element.send_keys(text)

    return element


def approve_form(driver: WebDriver, element: WebElement):
    click_button_by_label(driver, "Approve")


# ====================================================================================================================================== #
# ========================================================== FINDING ELEMENTS ========================================================== #
# ====================================================================================================================================== #


def find_element(driver: WebDriver, xpath: str, wait_sec=WAIT_TIME_SEC) -> WebElement | None:
    """Find a single web element on the current page.

    Args:
        driver (WebDriver): Selenium webdriver.
        xpath (str): The xpath used to look up the element.
        wait_sec (int): the seconds the driver waits for the element to be visible.

    Returns:
        WebElement: The found element.
    """
    try:
        return WebDriverWait(driver, wait_sec).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        return None


def find_element_by_text(driver: WebDriver, text: str, wait_sec=WAIT_TIME_SEC) -> WebElement | None:
    """Find a web element based on a string.

    Args:
        driver (WebDriver): Selenium webdriver.
        text (str): The text that appears in the element we are searching

    Returns:
        WebElement: The found element.
    """
    try:
        xpath: str = f"//*[contains(text(), '{text}')]//parent::div"
        return WebDriverWait(driver, wait_sec).until(lambda x: x.find_element(By.XPATH, xpath))
    except TimeoutException:
        return None


# ====================================================================================================================================== #
# ========================================================= CLICKING ELEMENTS ========================================================== #
# ====================================================================================================================================== #


def click_element(driver: WebDriver, element: WebElement) -> None:
    """Click a given web element.

    Args:
        driver (WebDriver): Selenium webdriver.
        xpath (str): The element that needs clicking.
    """
    element.click()


def click_element_by_path(driver: WebDriver, xpath: str, wait_sec=WAIT_TIME_SEC) -> None:
    """Click on the item corresponding to the xpath.

    Args:
        driver (WebDriver): Selenium webdriver.
        xpath (str): The xpath leading to the element.
    """
    try:
        WebDriverWait(driver, wait_sec).until(
            expected_conditions.presence_of_element_located((By.XPATH, xpath))
        ).click()
    except TimeoutException:
        return []


def click_button_by_label(driver: WebDriver, label: str):
    """Clicks a button according to its label.

    Args:
        driver (WebDriver): Selenium webdriver.
        label (str): The button label.
    """
    click_element_by_path(driver, f"//button[@label='{label}']")


def click_new_button(driver: WebDriver):
    """Clicks the new button on the current page.

    Args:
        driver (WebDriver): Selenium webdriver.
    """
    click_element_by_path(driver, "//button[contains(@class, 'new-button')]")


def click_cancel_on_button(driver: WebDriver, button_label: str):
    """Clicks the cancel symbol on the button with the specified label.

    Args:
        driver (WebDriver): Selenium webdriver.
        label (str): The button label.
    """
    click_element_by_path(driver, f"//td[@title='{button_label}']//parent::tr//div//span[.='cancel']")


def click_close_all_widgets(driver: WebDriver):
    """Clicks the close all widgets button.

    Args:
        driver (WebDriver): Selenium webdriver.
    """
    click_element_by_path(driver, "//button[@title='Close all widgets']")


# ====================================================================================================================================== #
# ========================================================= HANDLE FORM FIELDS ========================================================= #
# ====================================================================================================================================== #


def edit_form_fields(driver: WebDriver, serializer: wb_serializers, changes: dict[str]):
    """A method to edit the fields in a form.

    Args:
        driver (WebDriver): The Selenium webdriver.
        serializer (wb_serializers): The serializer that matches the model of the form.
        changes (dict[str]): A dict containing the changes. The dict keys should have the names of the corresponding fields (e.g. {"last_name": "Hotzenplotz"}).
    """
    field_list = list(changes.keys())
    for field in field_list:
        if not changes.get(field):
            continue
        if type(serializer.fields[field]) is wb_serializers.CharField:
            find_element(
                driver, f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//input"
            ).clear()
            write_text(
                driver,
                f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//input",
                changes[field],
            )
        elif type(serializer.fields[field]) is wb_serializers.ChoiceField:
            click_element_by_path(
                driver,
                f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//span[text()='expand_more']",
            )
            click_element_by_path(driver, f"//div[contains(text(),'{changes[field]}')]")
        elif type(serializer.fields[field]) is wb_serializers.PrimaryKeyRelatedField:
            click_element_by_path(
                driver,
                f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//span[text()='expand_more']",
            )
            click_element_by_path(driver, f"//li[contains(text(),'{changes[field]}')]")


def fill_out_form_fields(driver: WebDriver, serializer: wb_serializers, field_list: list[str], entity):
    """A method to fill out the fields in a form.

    Args:
        driver (WebDriver): The Selenium webdriver.
        serializer (wb_serializers): The serializer that matches the model of the form.
        field_list (list[str]): A list of the field names to be changed.
        entity (_type_): An entity on which the changes to the form are based. The entity should be created via the corresponding factory. (The entity should be created by using the Factory build method: e.g. PersonFactory.build())
    """
    for field in field_list:
        if type(serializer.fields[field]) in [wb_serializers.CharField, wb_serializers.IntegerField]:
            write_text(
                driver,
                f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//input",
                getattr(entity, field),
            )
        elif type(serializer.fields[field]) is wb_serializers.ChoiceField:
            click_element_by_path(
                driver,
                f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//span[text()='expand_more']",
            )
            click_element_by_path(driver, f"//div[contains(text(), '{getattr(entity, field)}')]")
        elif type(serializer.fields[field]) is wb_serializers.PrimaryKeyRelatedField:
            click_element_by_path(
                driver,
                f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//span[text()='expand_more']",
            )
            click_element_by_path(driver, f"//li[contains(text(), '{getattr(entity, field)}')]")
        elif type(serializer.fields[field]) is wb_serializers.BooleanField:
            click_element_by_path(
                driver,
                f"//label[contains(text(), '{serializer.fields[field].label}')]//parent::div//div//span[text()='{'Yes' if {getattr(entity, field)} else 'No'}']",
            )


# ====================================================================================================================================== #
# ======================================================== HANDLE LIST INSTANCES ======================================================= #
# ====================================================================================================================================== #


def edit_list_instance(
    driver: WebDriver,
    actions,
    list_name: str,
    serializer: wb_serializers.ModelSerializer,
    new_inputs: dict,
):
    """Edits a list instance.

    Args:
        driver (WebDriver): The Selenium webdriver.
        actions (_type_): The selenium action chains.
        list_name (str): The name of the list (e.g.: Persons)
        serializer (wb_serializers.ModelSerializer): The model serializer that matches the lists model.
        new_inputs (dict): A dict containing changes. The dict keys should have the names of the corresponding fields (e.g. {"last_name": "Hotzenplotz"}).
    """
    list_element = find_element(driver, f"//div[text()='{list_name}']")
    actions.double_click(list_element).perform()
    if unlock_button := find_element(driver, "//button[@label='Unlock']"):
        click_element(driver, unlock_button)
    edit_form_fields(driver, serializer, new_inputs)
    click_element_by_path(driver, "//button[@label='Save and close']")


def delete_list_entry(driver: WebDriver, actions: ActionChains, title: str):
    """Deletes a list entry. Requires that you are already in the correct list view.

    Args:
        driver (WebDriver): The Selenium webdriver.
        actions (ActionChains): The selenium action chains.
        title (str): The title of the list element that shall be deleted.
    """
    list_element = find_element(driver, f"//div[text()='{title}']")
    actions.context_click(list_element).perform()
    click_element_by_path(driver, "//span[text()='Delete instance']")
    click_element_by_path(driver, "//button[@label='Confirm']")


# ====================================================================================================================================== #
# =========================================================== HANDLE FILTERS =========================================================== #
# ====================================================================================================================================== #


def navigate_to_filter(driver: WebDriver, *menu_items):
    """Navigates to a specified list instance and opens the filter menu there.

    Args:
        driver (WebDriver): Selenium webdriver
        menu_item (str): The menu in which the filters should be open. You need to specify the whole path to the menu. E.g. ["CRM", "Persons"] to get to the CRMs persons menu.
    """
    actions = ActionChains(driver, 1000)
    open_menu_item(driver, *menu_items)
    # we need to move the mouse away from the side bar, so that the side bar closes.
    window_width = (driver.get_window_size().get("width")) / 2
    window_height = (driver.get_window_size().get("height")) / 2
    actions.move_by_offset(window_width, window_height).perform()

    filter_menu_btn = find_element(driver, "//button[@data-testid='control-bar-toggle-button']")
    click_element(driver, filter_menu_btn)


def select_filter(driver: WebDriver, label: str, option: str):
    """Select a filter from the filter menu a filter by the corresponding label.

    Args:
        driver (WebDriver): Selenium webdriver
        label (str): The filter label. (e.g. "Status" for the status - filter )
        option (str): The filter choice. (e.g. the "Planned" choice for the status filter)
    """
    no_activity_choices = find_element(
        driver, f"//label[text()='{label}']/parent::div//parent::div/button[contains(span, 'expand_more')]"
    )
    click_element(driver, no_activity_choices)
    click_element_by_path(driver, f"//li//div[text()='{option}']")
    click_element_by_path(driver, "//button[@label='Apply']")


def select_async_filter(driver: WebDriver, label: str, option: str):
    """Select a async filter from the filter menu a filter by the corresponding label.

    Args:
        driver (WebDriver): Selenium webdriver
        label (str): The filter label. (e.g. "Status" for the status - filter )
        option (str): The filter choice. (e.g. the "Planned" choice for the status filter)
    """
    no_activity_choices = find_element(
        driver, f"//label[text()='{label}']/parent::div//parent::span[contains(text(), 'expand_more')]"
    )
    click_element(driver, no_activity_choices)
    click_element_by_path(driver, f"//li[@title='{option}']")
    click_element_by_path(driver, "//button[@label='Apply']")


def select_column_filter(driver: WebDriver, label: str, option: str):
    """Select a filter from a list column by the corresponding label.

    Args:
        driver (WebDriver): Selenium webdriver
        label (str): The filter label. (e.g. "Status" for the status - filter )
        option (str): The filter choice. (e.g. the "Planned" choice for the status filter)
    """
    click_element_by_path(
        driver,
        f"//div[contains(@class, 'ag-cell-label-container') and ./div/span/text()='{label}']//span[contains(@class, 'ag-header-cell-menu-button')]",
    )
    click_element_by_path(
        driver, "//div[@class='ag-tabs-header ag-menu-header']//span[contains(@class, 'ag-icon-filter')]"
    )
    click_element_by_path(
        driver,
        f"//div[contains(@class, 'ag-virtual-list-container')]//div[contains(@class, 'ag-virtual-list-item') and ./div/div/div/text()='{option}']//input",
    )
    click_element_by_path(driver, "//button[@type='submit']")
