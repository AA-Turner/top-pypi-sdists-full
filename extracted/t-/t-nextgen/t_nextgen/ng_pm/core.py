"""NextGenCore Module."""

import time
from typing import Optional
from retry import retry
from t_desktop.config import IS_WINDOWS_OS
from logging import Logger
import _ctypes
import contextlib

from t_nextgen.ng_pm.windows.balance_control import BalanceControlWindow

if IS_WINDOWS_OS:
    from pywinauto import keyboard
    from pywinauto.findwindows import ElementNotFoundError

from t_desktop.utils.capture_screenshot import capture_screenshot
from t_desktop.decorators import retry_if_pywin_error
from t_desktop.decorators import capture_screenshot_if_pywin_error
from t_desktop.exceptions import AppCrashException
from t_ocr import Textract
from t_nextgen.exceptions import WrongDatabaseSelectedError, MultipleSessionsError
from t_nextgen.config import Config
from t_nextgen.ng_app_manager import NGAppManager
from t_nextgen.ng_pm.windows.batch_maitenance import BatchMaintenanceWindow
from t_nextgen.ng_pm.windows.batch_posting import BatchPostingWindow
from t_nextgen.ng_pm.windows.cob import COBWindow
from t_nextgen.ng_pm.windows.encounter_insurance import EncounterInsuranceWindow
from t_nextgen.ng_pm.windows.import_file import ImportFileWindow
from t_nextgen.ng_pm.windows.payment_entry import PaymentEntryWindow
from t_nextgen.ng_pm.windows.transaction_ledger import TransactionLedgerWindow
from t_nextgen.utils.logger import logger as lib_logger


class NextGenPMCore:
    """NextGenPMCore Class.

    This class is used to access all the windows of NextGen PM.
    """

    def __init__(
        self,
        username: Optional[str] = "",
        password: Optional[str] = "",
        textract: Optional[Textract] = None,
        app_path: str = Config.DIRECTORIES.ENTERPRISE_PM,
        logger: Optional[Logger] = None,
        database: Optional[str] = Config.DATABASES.TEST,
        practice: Optional[str] = None,
    ):
        """This method is used to initialize the NextGenPMCore class.

        Args:
            username (Optional[str]): username of the user.
            password (Optional[str]): password of the user.
            textract (Optional[Textract], optional): Textract object. Defaults to None.
            app_path (str, optional): path of nextgen PM application. Defaults to Config.DIRECTORIES.ENTERPRISE_PM.
            logger (Optional[Logger], optional): logger object. Defaults to None.
            database (Optional[str], optional): database to be used. Defaults to Config.DATABASES.TEST.
            practice (Optional[str], optional): practice to be used. Defaults to None.

        """
        self.username = username
        self.password = password
        self.app_path = app_path
        self.textract = textract
        self.database = database
        self.practice = practice
        self._batch_posting_window = None
        self._batch_maintenance_window = None
        self._balance_control_window = None
        self._cob_window = None
        self._encounter_insurance_window = None
        self._import_file_window = None
        self._payment_entry_window = None
        self._transaction_legder_window = None
        self.logger = logger if logger is not None else lib_logger
        self.desktop_app = NGAppManager(app_path, self.logger)

    @property
    def batch_posting_window(self):
        """This property is used to access BatchPostingWindow class."""
        if self._batch_posting_window is None:
            self._batch_posting_window = BatchPostingWindow(self.app_path, self.logger)
        return self._batch_posting_window

    @property
    def batch_maintenance_window(self):
        """This property is used to access BatchMaintenanceWindow class."""
        if self._batch_maintenance_window is None:
            self._batch_maintenance_window = BatchMaintenanceWindow(self.app_path, self.logger)
        return self._batch_maintenance_window

    @property
    def balance_control_window(self):
        """This property is used to access BatchMaintenanceWindow class."""
        if self._balance_control_window is None:
            self._balance_control_window = BalanceControlWindow(self.app_path, self.logger)
        return self._balance_control_window

    @property
    def cob_window(self):
        """This property is used to access COBWindow class."""
        if self._cob_window is None:
            self._cob_window = COBWindow(self.app_path, self.logger)
        return self._cob_window

    @property
    def encounter_insurance_window(self):
        """This property is used to access EncounterInsuranteWindow class."""
        if self._encounter_insurance_window is None:
            self._encounter_insurance_window = EncounterInsuranceWindow(self.app_path, self.logger)
        return self._encounter_insurance_window

    @property
    def import_file_window(self):
        """This property is used to access ImportFileWindow class."""
        if self._import_file_window is None:
            self._import_file_window = ImportFileWindow(self.app_path, self.logger)
        return self._import_file_window

    @property
    def payment_entry_window(self):
        """This property is used to access PaymentEntryWindow class."""
        if self._payment_entry_window is None:
            self._payment_entry_window = PaymentEntryWindow(self.app_path, self.logger, self.textract)
        return self._payment_entry_window

    @property
    def transaction_ledger_window(self):
        """This property is used to access TransactionLedgerWiundow class."""
        if self._transaction_legder_window is None:
            self._transaction_legder_window = TransactionLedgerWindow(self.app_path, self.logger)
        return self._transaction_legder_window

    @retry_if_pywin_error(retries=2, delay=5)
    @capture_screenshot_if_pywin_error()
    def login(
        self,
        practice: Optional[str] = None,
        database: Optional[str | list[str]] = None,
        app_folder: str = Config.DIRECTORIES.BASE_DIR,
    ) -> None:
        """Login to the app."""
        if not database:
            databases = [self.database]
        elif isinstance(database, str):
            databases = [database]
        else:
            databases = database
        practice = practice if practice else self.practice
        if process := self.desktop_app.get_app_session_if_running(self.app_path):
            self.logger.debug(f"Process {process} is already running.")
            capture_screenshot("app_session_is_running.png")
            self.close_session(process, ignore_errors=True)  # Close a NextGen Session if it exists
        try:
            self.desktop_app.start_app(app_path=self.app_path, app_folder=app_folder)
            self.desktop_app.wait_until_element_visible(auto_id="txtUserName", control_type="Edit")
            self._check_database_names(db_names=databases)
            if not self.desktop_app.dialog.child_window(title="Windows Integrated", control_type="ComboBox").exists():
                self.desktop_app.set_input_text(auto_id="txtUserName", text=self.username)
                self.desktop_app.set_input_text(auto_id="txtPassword", text=self.password)
            if practice:
                self.desktop_app.select_dropdown_item("cboPractice", practice)
            self.desktop_app.invoke_button(auto_id="btnLogon")
            self.desktop_app.app = self.desktop_app.connect_to_app(title="MainForm", timeout=20)
            self.logger.info("Logged into NextGen")
        except Exception as e:
            try:
                if app := self.desktop_app.connect_to_app(title="MainForm", timeout=20):
                    self.logger.info("Logged into NextGen")
                    self.desktop_app.app = app
                    return
            except Exception as inner_e:
                self.handle_multiple_sessions_popup()
                self.desktop_app.close_login_window(self.app_path)
                raise inner_e
            self.logger.error(f"Login failed: {e}")
            raise e

    @retry_if_pywin_error(retries=3, delay=5, exceptions=(ElementNotFoundError))  # type: ignore[misc]
    def _check_database_name(self, db_name_flag: str = Config.DATABASES.PROD) -> None:
        """Validates if the name received is part of the database selected.

        Args:
            db_name_flag (str): The database name to be validated.

        Returns:
            Raises WrongDatabaseSelected: if the database doesn't match.
        """
        database_name = self.desktop_app.dialog.child_window(auto_id="lblDatabase").window_text()
        self.logger.info(f"App is connected to '{database_name}' database")
        if db_name_flag.lower() not in database_name.lower():
            raise WrongDatabaseSelectedError(f"'{database_name}' selected, wrong database selected.")

    def _check_database_names(self, db_names: list[str]) -> None:
        """Validates if the name received is part of the database selected.

        Args:
            db_names (list[str]): The database names to be validated.

        Returns:
            Raises WrongDatabaseSelected: if the database doesn't match.
        """
        for db_name in db_names:
            try:
                self._check_database_name(db_name)
                return
            except WrongDatabaseSelectedError:
                continue
        raise WrongDatabaseSelectedError(f"None of the databases '{db_names}' selected.")

    def handle_multiple_sessions_popup(self) -> None:
        """Close multiple sessions pop-up that comes immediately after login.

        Raises:
            MultipleSessionsError: if the modal exists
        """
        if self.desktop_app.dialog.child_window(title="Multiple station logon error", control_type="Window").exists(
            timeout=2, retry_interval=0.001
        ):
            self.logger.warning("Multiple sessions detected. Closing the popup.")
            if next_gen_process := self.desktop_app.get_app_session_if_running(self.app_path):
                self.close_session(next_gen_process)
            raise MultipleSessionsError("Process failed with multiple sessions issue")

    @capture_screenshot_if_pywin_error()
    def select_practice_from_app(self, practice: str):
        """Select practice from the Health Practice menu.

        Args:
            practice (str): The practice to select.
        """
        self.click_practice_from_bar()
        self.input_check_practice(practice)

    def check_if_practice_was_set_correctly(self, practice: str):
        """Check if the practice was set correctly.

        Args:
            practice (str): The practice to check.
        """
        pane = self.desktop_app.dialog.child_window(title="cboPractice", control_type="Pane").wait("visible", 5)
        practice_selected = str(pane.descendants(control_type="Edit")[0].get_value())
        if practice_selected.strip() != practice.strip():
            raise Exception(
                f"Practice was not set correctly. Expected: {practice.strip()}, Actual: {practice_selected.strip()}"
            )

    @retry(tries=3, delay=3)
    def click_practice_from_bar(self):
        """Clicks the Health Practice button from the menu bar."""
        practice_icon = self.desktop_app.dialog.child_window(title="cmdToolPractice", control_type="Button")
        with contextlib.suppress(_ctypes.COMError):
            practice_icon.set_focus()
        with contextlib.suppress(_ctypes.COMError):
            practice_icon.click_input(button="left")
        self.desktop_app.dialog.child_window(auto_id="cboPractice", control_type="Pane").wait("visible", 5)

    @retry(tries=3, delay=3)
    def input_check_practice(self, practice: str):
        """Input check practice information and click OK.

        Args:
            practice (str): the name of the practice to be selected
        """
        pane = self.desktop_app.dialog.child_window(auto_id="cboPractice")
        combo_box = pane.child_window(auto_id="mcbo", control_type="ComboBox")
        self.desktop_app.set_text(combo_box.child_window(control_type="Edit", found_index=0), practice)
        self.check_if_practice_was_set_correctly(practice)
        with contextlib.suppress(_ctypes.COMError):
            self.desktop_app.dialog.child_window(auto_id="cmdOK").click()

    @capture_screenshot_if_pywin_error()
    def close_session(self, process: str, practice: str = None, ignore_errors: bool = False) -> None:
        """Close the session using keyboard shortcuts.

        Args:
            process (str): The name of the process to kill if necessary.
            practice (str, optional): The practice to select. Defaults to None
            ignore_errors (bool, optional): Whether to ignore errors. Defaults to False.

        Returns:
            None
        """
        self.logger.info("Running close_session method.")
        try:
            self.desktop_app.connect_to_main_form()
            self.desktop_app.close_modal(buttons_to_try=["NO", "OK"], timeout=1)
            self.desktop_app.clear_out_windows_function(practice=practice)
            self.desktop_app.open_file_menu()
            logout_key = "l"
            keyboard.send_keys(logout_key)
        except (ElementNotFoundError, TimeoutError, RuntimeError) as e:
            if not ignore_errors:
                raise e
            self.logger.warning(f"Error closing session, ignoring the error: {e}")

        # This kind of .exe needs to kill the app after logout
        try:
            self.desktop_app.close_modal(buttons_to_try=["YES"], timeout=2)
            time.sleep(10)
            self.desktop_app.wait_to_disappear(auto_id="cmdToolApptlist", control_type="Button", max_attempts=12)
            self.logger.info("Session closed successfully.")
        except (AssertionError, RuntimeError):
            if not ignore_errors:
                raise AppCrashException("Session not closed successfully")
            self.logger.warning("Session not closed successfully, ignoring the error.")
        self.logger.info("Killing the process for EnterprisePM.exe")
        time.sleep(3)
        self.desktop_app.kill_app(process=process, app_path=self.app_path)
