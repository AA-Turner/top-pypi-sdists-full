"""NgAppManager module."""

import contextlib
from logging import Logger
import time
from abc import ABCMeta
from typing import Optional
import pyautogui
import _ctypes
from retry import retry
from t_desktop import DesktopApp
from t_desktop.config import IS_WINDOWS_OS
from t_desktop.decorators import retry_if_pywin_error

if IS_WINDOWS_OS:
    from pywinauto.timings import TimeoutError
    from pywinauto.controls.uia_controls import ComboBoxWrapper
    from pywinauto.application import Application, WindowSpecification
    from pywinauto.findwindows import ElementNotFoundError
    from pywinauto.controls.hwndwrapper import InvalidWindowHandle
    from pywinauto.controls.uia_controls import ListItemWrapper


from t_nextgen.utils.logger import logger as lib_logger


class ScopedSingletonMeta(ABCMeta):
    """SingletonMeta class."""

    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        """Ensures that only one instance of the class is created per `app_path`.

        This method overrides the default `__call__` method to control the instantiation
        of the class. When called, it checks if an instance of the class already exists
        for the specified `app_path` in `cls._instances`. If an instance does not exist
        for the provided `app_path`, it creates one and stores it in the `cls._instances`
        dictionary. Otherwise, it returns the existing instance associated with the
        `app_path`.

        The `app_path` can be provided as a keyword argument (`app_path`) or as the first
        positional argument. If no `app_path` is specified, a TypeError is raised.

        Args:
            *args: Positional arguments for the class instantiation.
            **kwargs: Keyword arguments for the class instantiation. Includes `app_path`.

        Returns:
            object: The single instance of the class associated with the given `app_path`.
        """
        app_path = ""
        if "app_path" in kwargs:
            app_path = kwargs["app_path"]
        elif len(args) > 0:
            app_path = args[0]
        else:
            raise TypeError("app_path argument is required.")
        if app_path not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[app_path] = instance
        return cls._instances[app_path]


class NGAppManager(DesktopApp, metaclass=ScopedSingletonMeta):
    """NgAppManager class."""

    def __init__(self, app_path: str, logger: Optional[Logger] = None):
        """Initialize the NgAppManager class.

        Args:
            app_path (str): The path to the NextGen application.
            logger (Optional[Logger], optional): The logger object to use for logging. Defaults to None.
        """
        self.logger = logger if logger is not None else lib_logger
        super().__init__(app_path)

    def close_modal(
        self,
        modal_title: str = "NextGen",
        buttons_to_try: list[str] = ["OK"],
        timeout: int = 5,
        retry_interval: int = 0.001,
    ) -> tuple[bool, str]:
        """Close a modal in the app by clicking on the given button and returning the modal text.

        Args:
            modal_title (str): Title of the modal.
            buttons_to_try (list[str]): List of button texts to try clicking, in order.
              Defaults to ["OK"] if the list is empty.
            timeout (int): Maximum amount of time to check for modal.
            retry_interval (int): The control is checked for existence this number of seconds.

        """
        modal = self.dialog.child_window(title=modal_title, control_type="Window", top_level_only=True)
        if modal.exists(timeout, retry_interval):
            modal_text_control = modal.child_window(control_type="Text", top_level_only=True)
            modal_text = modal_text_control.window_text()

            # Find and click the button
            buttons_list = modal.wrapper_object().descendants(control_type="Button")
            for button_to_click in buttons_to_try:
                for button in buttons_list:
                    button_text = button.texts()[0].upper()
                    if button_text == button_to_click.upper():
                        with contextlib.suppress(_ctypes.COMError):
                            button.click()
                        return True, modal_text
            self.logger.debug(f"No matching button found in modal for options {buttons_to_try}.")
            return False, modal_text
        else:
            return False, ""

    @retry(tries=3, delay=4)
    def connect_to_logged_in_screen(self) -> None:
        """Connect to the Next Gen App after it has been logged into."""
        try:
            return self.connect_to_app(title="MainForm", timeout=20)
        except Exception as e:
            self.click_on_next_gen_window()
            raise e

    @retry(tries=3, delay=3)
    def close_login_window(self, app_path: str) -> None:
        """Close the login window.

        Args:
            app_path (str): The path to the NextGen application.
        """
        app = Application(backend="uia").connect(path=app_path, timeout=5)
        for window in app.windows():
            if window.element_info.control_type == "Window":
                self.logger.debug(f"Closing Login window: {window.window_text()}")
                window.close()

    @retry_if_pywin_error()
    def open_file_menu(self) -> None:
        """This function opens the file menu."""
        file_menu = self.dialog.child_window(title="File", control_type="MenuItem", top_level_only=True, found_index=0)
        file_menu.click_input()
        self.dialog.child_window(title="FileDropDown").wait("visible", 30)

    @retry((TimeoutError, OSError), 3, 1)
    def connect_to_main_form(self) -> None:
        """Connect to nextgen main form.

        Raises:
            TimeoutError: Failed to connect to NextGen main form.
        """
        with contextlib.suppress(TimeoutError):
            self.app = self.connect_to_app(title="MainForm", timeout=20)
            return
        with contextlib.suppress(TimeoutError):
            self.app = self.connect_to_app(path=self.app_path, timeout=20)
            return
        raise TimeoutError("Timeout, failed to connect to NextGen main form.")

    @retry_if_pywin_error()
    def clear_out_windows_function(self, practice: str = "") -> None:
        """This function clears out windows."""
        child_windows = self.dialog.descendants(control_type="Window")

        self.logger.info(f"Found {len(child_windows)} child windows to close.")

        closed_windows_count = 0
        for child_window in child_windows:
            try:
                child_window.close()
                self.deal_with_unhandled_exception_popup(f"NextGen - {practice}")
                self.click_no_button_in_next_gen_alert()
                closed_windows_count += 1
            except Exception as e:
                self.logger.error(f"Error closing window: {str(e)}")

        self.logger.debug(f"Closed {closed_windows_count} child windows.")

    def click_ok_if_only_option(
        self, call_count: int = 0, max_calls: int = 3, modal_exists_timeout: int = 3, sleep: float = 5
    ) -> bool:
        """Clicks the "OK" button on a modal if it is the only option and checks for additional modals.

        This function searches for a modal dialog with the title "NextGen". If found, it looks for "OK",
        "CLOSE", and "CANCEL" buttons. If "OK" is the only available button, it clicks it. The function
        will recursively check for additional modals up to a maximum of `max_calls`.

        Args:
            call_count (int, optional): _description_. Defaults to 0.
            max_calls (int, optional): _description_. Defaults to 3.
            modal_exists_timeout (int, optional): _description_. Defaults to 3.
            sleep (float, optional): _description_. Defaults to 5.
        """
        if call_count >= max_calls:
            return True
        try:
            modal = self.dialog.child_window(title="NextGen", control_type="Window")
            if modal.exists(timeout=modal_exists_timeout, retry_interval=0.001):
                wrapper_object = modal.wrapper_object()
                buttons_list = wrapper_object.descendants(control_type="Button")

                ok_button = None
                close_button = None
                more_buttons = False
                for button in buttons_list:
                    button_text = button.texts()[0].upper()
                    if button_text == "OK":
                        ok_button = button
                    elif button_text in ["CLOSE", "CANCEL"]:
                        close_button = button
                    else:
                        more_buttons = True
                if more_buttons:
                    return False
                if ok_button and close_button:
                    self.logger.debug("Ok button found. Clicking on it.")
                    texts = wrapper_object.descendants(control_type="Text")
                    if texts:
                        self.logger.debug(f"Text in the modal: {texts[0].texts()}")
                    with contextlib.suppress(_ctypes.COMError):
                        ok_button.click()
                    time.sleep(sleep)
                    self.click_ok_if_only_option(
                        call_count=call_count + 1, max_calls=max_calls
                    )  # Recursive call with incremented call_count
            else:
                return False
        except _ctypes.COMError:
            return True
        except (TimeoutError, ElementNotFoundError, IndexError):
            return False

    def click_ok_popup_getting_message(
        self, call_count: int = 0, max_calls: int = 3, modal_exists_timeout: int = 3, sleep: float = 5
    ) -> str:
        """Clicks the "OK" button on a modal if it is the only option and checks for additional modals.

        This function searches for a modal dialog with the title "NextGen". If found, it looks for "OK",
        "CLOSE", and "CANCEL" buttons. If "OK" is the only available button, it clicks it. The function
        will recursively check for additional modals up to a maximum of `max_calls`. And return the message
        in the modal.

        Args:
            call_count (int, optional): _description_. Defaults to 0.
            max_calls (int, optional): _description_. Defaults to 3.
            modal_exists_timeout (int, optional): _description_. Defaults to 3.
            sleep (float, optional): _description_. Defaults to 5.

        Returns:
            str: The text message from the modal dialog, or an empty string if modal was not found.
        """
        if call_count >= max_calls:
            return ""
        try:
            modal = self.dialog.child_window(title="NextGen", control_type="Window")
            if modal.exists(timeout=modal_exists_timeout, retry_interval=0.001):
                wrapper_object = modal.wrapper_object()
                buttons_list = wrapper_object.descendants(control_type="Button")

                ok_button = None
                close_button = None
                more_buttons = False
                for button in buttons_list:
                    button_text = button.texts()[0].upper()
                    if button_text == "OK":
                        ok_button = button
                    elif button_text in ["CLOSE", "CANCEL"]:
                        close_button = button
                    else:
                        more_buttons = True
                if more_buttons:
                    return ""
                if ok_button and close_button:
                    self.logger.debug("Ok button found. Clicking on it.")
                    texts = wrapper_object.descendants(control_type="Text")
                    modal_text = None
                    if texts:
                        modal_text = texts[0].texts()
                        self.logger.debug(f"Text in the modal: {modal_text}")
                    with contextlib.suppress(_ctypes.COMError):
                        ok_button.click()
                    time.sleep(sleep)
                    self.click_ok_popup_getting_message(
                        call_count=call_count + 1, max_calls=max_calls
                    )  # Recursive call with incremented call_count
                    return modal_text[0] if modal_text else ""
            else:
                return ""
        except _ctypes.COMError:
            return ""
        except (TimeoutError, ElementNotFoundError, IndexError):
            return ""

    def click_no_button_in_next_gen_alert(self) -> None:
        """Clicks the "No" button on the NextGen alert window if it exists."""
        no_button = self.dialog.child_window(title="NextGen", control_type="Window").child_window(
            auto_id="7", control_type="Button"
        )
        if no_button.exists(timeout=1, retry_interval=0.001):
            with contextlib.suppress(_ctypes.COMError):
                no_button.click()
            no_button.wait_not("visible", timeout=5)

    def select_value_from_combobox(
        self, combobox: ComboBoxWrapper, value: str, use_type_keys: bool = False, click_combobox: bool = True
    ) -> None:
        """Selects a value from a ComboBox by simulating a click and searching for the matching option.

        Args:
            combobox (ComboBoxWrapper): The ComboBox control in which to search for the value.
            value (str): The value to search for and select within the ComboBox.
            use_type_keys (bool, optional): If True, uses type_keys instead of set_text. Defaults to False.
            click_combobox (bool, optional): If True, clicks the combobox before selecting the value. Defaults to True.
        """
        if click_combobox:
            with contextlib.suppress(_ctypes.COMError):
                combobox.click_input()
        # Search for the matching option in the ComboBox
        option_to_select = self.get_option_to_select_from_combobox(combobox, value)
        # Select the option if found
        self.select_option_in_combobox(combobox, use_type_keys, option_to_select)

    def click_on_next_gen_window(self) -> None:
        """Click on the Next Gen window."""
        next_gen_app_coordinates = self.get_next_gen_app_coordinates()
        if next_gen_app_coordinates != (0, 0):
            self.mouse_click_element(self.app.top_window())

    def get_next_gen_app_coordinates(self) -> tuple:
        """Get the coordinates of the Next Gen App window.

        Returns:
            tuple: element coordinates
        """
        return self.get_element_coordinates(self.app.top_window())

    def double_click_row(self, row_elements: list[ListItemWrapper], row_index: int) -> None:
        """Double click a row.

        Args:
            row_elements (List[ListItemWrapper]): The list of row elements
            row_index (int): The row to be clicked. Follows zero based indexing.
        """
        with contextlib.suppress(_ctypes.COMError):
            row_elements[row_index].click_input(double=True)

    def click_down_n_times(self, n: int) -> None:
        """This method click down key 'n' times.

        Args:
            n (int): number of times to click
        """
        pyautogui.press("home")
        confidence_value = 3  # This is an extra number to ensure the row will be full visible, so let's scroll more
        self.logger.debug(f"Clicking down key {n + confidence_value} times.")
        for _ in range(n + confidence_value):
            pyautogui.press("down")

    def click_button_by_element_name(self, element_name: str) -> None:
        """This method clicks on a button by element name.

        Args:
            element_name (str): element name
        """
        with contextlib.suppress(_ctypes.COMError):
            button = self.dialog.child_window(title=element_name, control_type="Button")
            self.mouse_click_element(button)

    def click_file_menu_button(self) -> None:
        """Click on the File menu button."""
        with contextlib.suppress(_ctypes.COMError):
            self.dialog.child_window(title="File", control_type="MenuItem").wait("exists", timeout=10)
            self.dialog.child_window(title="File", control_type="MenuItem").invoke()

    def get_file_menu(self) -> WindowSpecification:
        """Get file menu window control.

        Returns:
            WindowSpecification: File Menu control
        """
        self.dialog.child_window(title="File", control_type="MenuItem").wait("exists", timeout=10)
        return self.dialog.child_window(title="File", control_type="MenuItem")

    def click_processes_button_in_file_menu(self, file_menu: WindowSpecification) -> None:
        """Click on the Processes option in the File menu.

        Args:
            file_menu (WindowSpecification): File Menu control
        """
        with contextlib.suppress(_ctypes.COMError):
            file_menu.child_window(title="Processes", control_type="MenuItem", found_index=0).wait("exists", timeout=10)
            file_menu.child_window(title="Processes", control_type="MenuItem", found_index=0).invoke()

    def get_processes_menu_from_file_menu(self, file_menu: WindowSpecification) -> WindowSpecification:
        """Get the Processes Menu Control.

        Args:
            file_menu (WindowSpecification): File Menu control

        Returns:
            WindowSpecification: Processes Menu Control
        """
        file_menu.child_window(title="Processes", control_type="MenuItem", found_index=0).wait("exists", timeout=10)
        return file_menu.child_window(title="Processes", control_type="MenuItem", found_index=0)

    def close_digital_image_function(self) -> None:
        """This function clears out Digital Image windows."""
        windows_menu = self.dialog.child_window(title="Window", control_type="MenuItem")
        windows_menu.set_focus()
        windows_menu.select()

        child_windows = self.dialog.descendants(control_type="Window")

        closed_windows_count = 0
        for active_child_window in child_windows:
            window_name = active_child_window.window_text()
            if window_name.startswith("Digital Image"):
                if self.close_window_if_exist(window_name):
                    closed_windows_count += 1
                    return

    def select_option_in_combobox(self, combobox: ComboBoxWrapper, use_type_keys: bool, option_to_select: str) -> None:
        """This method selects an option in a ComboBox.

        Args:
            combobox (ComboBoxWrapper): ComboBox control.
            use_type_keys (bool): Boolean to determine if type_keys should be used.
            option_to_select (str): Option to select in the ComboBox.
        """
        self.logger.debug(f"Selecting option '{option_to_select}' in ComboBox.")
        if use_type_keys:
            combobox.type_keys(option_to_select)
            time.sleep(1)
            combobox.type_keys("{ENTER}")
        else:
            with contextlib.suppress(_ctypes.COMError):
                combobox.child_window(control_type="Edit", found_index=0).set_text(option_to_select)

    def get_option_to_select_from_combobox(self, combobox: ComboBoxWrapper, value: str) -> str:
        """Gets the option to select from the ComboBox.

        Args:
            combobox (ComboBoxWrapper): The ComboBox control in which to search for the value.
            value (str): The value to search for and select within the ComboBox.

        Returns:
            str: The option to select from the ComboBox.
        """
        option_to_select: str = ""
        for option in combobox.descendants(control_type="ListItem"):
            option_text = option.window_text().lower().strip()
            value = value.lower().strip()
            if value in option_text:
                option_to_select = option.window_text()
                break
        return option_to_select

    def click_on_combobox(self, combobox: ComboBoxWrapper) -> None:
        """Clicks the combobox.

        Args:
            combobox (ComboBoxWrapper): The ComboBox control to click.
        """
        with contextlib.suppress(_ctypes.COMError):
            combobox.click_input()

    def deal_with_unhandled_exception_popup(self, windows_title: str = "Microsoft .NET Framework") -> bool:
        """This method deals with the unhandled exception popup.

        Args:
            windows_title (str): The title of the window to check for.

        Returns:
            bool: True if the popup was found and handled, False otherwise.
        """
        with contextlib.suppress(ElementNotFoundError, InvalidWindowHandle):
            popup_app = Application(backend="win32").connect(title=windows_title)
            top_window = popup_app.top_window()
            if top_window.exists(timeout=1, retry_interval=0.001):
                top_window.child_window(title="&Continue").click()
                return True
            return False

    def get_element_coordinates(self, element) -> tuple:
        """This method gets the element coordinates.

        Args:
            element (ListItemWrapper): element

        Returns:
            tuple: element coordinates
        """
        return element.rectangle().mid_point()

    def safe_wait(self, kwargs):
        """Waits for an element specified by `kwargs` to become visible in the `next_gen` dialog window.

        This function will attempt to wait for an element to become visible up to a maximum of 3 tries.
        If the element does not become visible within these tries, a `TimeoutError` will be raised.

        Parameters:
        kwargs : dict
            A dictionary of keyword arguments that specify the properties of the child window element
            to wait for. These arguments are passed to the `child_window` method.

        Returns:
        bool
            Returns True if the element becomes visible within the allowed tries.

        Raises:
        TimeoutError
            If the element does not become visible after 3 tries.

        Example:
        >>> kwargs = {"title": "Ok", "control_type": "Button"}
        >>> safe_wait(kwargs)
        True

        """
        max_tries = 3
        current_try = 0
        while not current_try > max_tries:
            try:
                self.dialog.child_window(**kwargs).wait("visible", 5)
                return True
            except (RuntimeError, TimeoutError):
                self.logger.debug("Element not yet loaded, waiting more 2 seconds")
                time.sleep(2)
                current_try += 1
        raise TimeoutError("Element was not loaded after 3 tries")

    def close_window_if_exist(self, window_title: str) -> bool:
        """Closes the specified window by its title.

        Args:
            window_title (str): The title of the window to close.
        """
        try:
            window = self.dialog.child_window(title=window_title, control_type="Window")
            window.close()
            self.click_no_button_in_next_gen_alert()
            self.logger.debug(f"Closed window: {window_title}")
            return True
        except ElementNotFoundError:
            self.logger.debug(f"Window '{window_title}' not found. It might already be closed.")
            return False

    def set_text(self, field: ListItemWrapper, text: str, max_retries: int = 4) -> None:
        """Set a text in a specific field and double check if the action was performed corretly, retry if not.

        Args:
            field (ListItemWrapper): Field where the text shoud be set.
            text (str): Text that will be set.
            max_retries (int, optional): Number of max retries attempt. Defaults to 4.
        """
        retries = 0
        while retries < max_retries:
            try:
                field.set_text(text)
                return
            except _ctypes.COMError:
                time.sleep(0.5)
                if field.get_value() == text:
                    return
            retries += 1
        self.logger.error(f"Failed to set text after {retries} retries")

    def toggle_checkbox(self, checkbox: ListItemWrapper, max_retries: int = 4) -> None:
        """Toggle a checkbox and double check if the action was performed corretly, retry if not.

        Args:
            checkbox (ListItemWrapper): Checkbox element that should be toggled.
            max_retries (int, optional): Number of max retries attempt. Defaults to 4.
        """
        retries = 0
        while retries < max_retries:
            try:
                if checkbox.get_toggle_state() == 1:
                    return
                checkbox.toggle()
                return
            except _ctypes.COMError:
                time.sleep(1)
                if checkbox.get_toggle_state() == 1:
                    return
            retries += 1
        self.logger.error(f"Failed to toggle checkbox after {retries} retries")

    def untoggle_checkbox(self, checkbox: ListItemWrapper, max_retries: int = 4) -> None:
        """Untoggle a checkbox and double check if the action was performed corretly, retry if not.

        Args:
            checkbox (ListItemWrapper): Checkbox element that should be untoggled.
            max_retries (int, optional): Number of max retries attempt. Defaults to 4.
        """
        retries = 0
        while retries < max_retries:
            try:
                if checkbox.get_toggle_state() == 0:
                    return
                checkbox.toggle()
                return
            except _ctypes.COMError:
                time.sleep(1)
                if checkbox.get_toggle_state() == 0:
                    return
            retries += 1
        self.logger.error(f"Failed to untoggle checkbox after {retries} retries")
