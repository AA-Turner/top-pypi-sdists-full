"""ImportFile module."""

from retry import retry
from t_nextgen.nextgen_window import NextGenWindow

import contextlib
import _ctypes
from t_nextgen.exceptions import (
    NextGenEdiNotFoundException,
    NextGenControlLostException,
    NextGenDuplicateImportException,
    NextGenImportTimeoutException,
    NextGenPatientPayException,
    PostingSheetTimeOutException,
)
from t_desktop.config import IS_WINDOWS_OS

from t_nextgen.utils.wait_if_high_usage import wait_if_high_usage

if IS_WINDOWS_OS:
    from pywinauto.application import WindowSpecification
    from pywinauto.findwindows import ElementNotFoundError
    from pywinauto.keyboard import send_keys
    from t_desktop.decorators import capture_screenshot_if_exception
import time
from datetime import datetime, timedelta

from pathlib import Path
from t_nextgen.utils import utility


class ImportFileWindow(NextGenWindow):
    """ImportFile class with methods to interact with import file window."""

    @property
    def window(self) -> WindowSpecification:
        """Get control of Import Window."""
        self.desktop_app.dialog.child_window(title="frmERA", control_type="Window").wait("exists", timeout=10)
        return self.desktop_app.dialog.child_window(title="frmERA", control_type="Window")

    @property
    def enhanced_report_mode_window(self) -> WindowSpecification:
        """Get control of Enhanced Report Mode Window."""
        return self.desktop_app.dialog.child_window(
            title="ERA Import Posting - Enhanced Report Mode", control_type="Window"
        )

    @property
    def report_viewer_window(self) -> WindowSpecification:
        """Return the report_viewer_window window element."""
        return self.desktop_app.dialog.child_window(auto_id="ReportViewer", control_type="Window")

    def click_era_posting_from_processes_menu(self) -> None:
        """Click on the ERA Posting option in the Processes menu."""
        self.logger.debug("Clicking on ERA Posting from Processes Menu.")
        self.desktop_app.click_file_menu_button()
        file_menu = self.desktop_app.get_file_menu()
        self.desktop_app.click_processes_button_in_file_menu(file_menu)
        processes_menu = self.desktop_app.get_processes_menu_from_file_menu(file_menu)
        with contextlib.suppress(_ctypes.COMError):
            processes_menu.child_window(title="ERA Posting...", control_type="MenuItem", found_index=0).click_input()

    def click_cancel_import_window(self) -> None:
        """Click on cancel button in Import Window."""
        self.logger.debug("Clicking on Cancel button in Import Window.")
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(title="cmdCancel", auto_id="cmdCancel", control_type="Button").click()

    @retry(tries=3, delay=1)
    def select_directory_import(self) -> None:
        """Select the directory import option."""
        self.logger.debug("Selecting Directory Import option.")
        try:
            with contextlib.suppress(_ctypes.COMError):
                self.window.child_window(
                    title="optFolderSearch", auto_id="optFolderSearch", control_type="RadioButton"
                ).click()
        except TimeoutError as e:
            self.logger.warning("Directory Import option not found within timeout.")
            self.click_cancel_import_window()
            self.click_era_posting_from_processes_menu()
            raise e

    def set_835_directory_path(self, folder_835_path: str) -> None:
        """Set the path for the 835 directory.

        Args:
            folder_835_path (str): the folder path where 835 files are stored
        """
        self.logger.debug(f"Setting 835 Directory Path: {folder_835_path}")
        self.desktop_app.set_text(
            self.window.child_window(title="txtFolderName", auto_id="txtFolderName", control_type="Edit"),
            folder_835_path,
        )

    def click_find_button(self) -> None:
        """Click on find button."""
        self.logger.debug("Clicking on Find button.")
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(title="cmdFind", auto_id="cmdFind", control_type="Button").click()

    def get_edi_pane(self) -> WindowSpecification:
        """Get EDI Pane control.

        Returns:
            WindowSpecification: EDI Pane Control
        """
        pane = self.window.child_window(auto_id="frmFolderResults", control_type="Group").child_window(
            auto_id="lstListing", control_type="Pane"
        )
        pane.wait("exists", timeout=15)
        return pane

    @capture_screenshot_if_exception()
    def get_edi_checkbox_count(self, edi_pane: WindowSpecification) -> int:
        """Get the EDI CheckBox count aka total number of EDIs to be imported.

        Args:
            edi_pane (WindowSpecification): EDI Pane control

        Returns:
            int: number of EDIs found
        """
        check_box_count = len(edi_pane.descendants(control_type="CheckBox"))
        if check_box_count == 0:
            with contextlib.suppress(_ctypes.COMError):
                self.desktop_app.dialog.child_window(title="cmdCancel", control_type="Button").click()
            self.logger.debug("No EDI files found in the 835 folder.")
            raise NextGenEdiNotFoundException("No EDI files found in the 835 folder")
        return check_box_count

    def select_edi_row_checkboxes(self) -> None:
        """Select all the EDIs as visible in ERA processing window in NextGen App."""
        edi_pane = self.get_edi_pane()
        check_box_count = self.get_edi_checkbox_count(edi_pane)
        self.logger.debug(f"Selecting EDI Row Checkboxes. {check_box_count} EDIs found.")
        for i in range(check_box_count):
            send_keys("{DOWN}")
            time.sleep(1)
            with contextlib.suppress(_ctypes.COMError):
                checkbox_index = 6 if i > 6 else i
                edi_pane.child_window(control_type="CheckBox", found_index=checkbox_index).click()

    def import_edi_files(self) -> None:
        """Click on import button in the ERA processing window in NextGen App."""
        self.logger.debug("Clicking on Import button.")
        data = self.window.child_window(title="cmdImport", auto_id="cmdImport", control_type="Button")
        with contextlib.suppress(_ctypes.COMError):
            data.click()
        self.wait_for_edi_import_to_finish()

    def wait_for_edi_import_to_finish(self) -> None:
        """Waits for the EDIs to be imported into the NextGen App."""
        self.logger.debug("Waiting for EDI import to finish.")
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=3600)
        time.sleep(1)
        max_tries = 7
        current_try = 0
        try:
            if self.patient_has_duplicated_import():
                self.logger.debug("Patient has duplicated import.")
                raise NextGenDuplicateImportException("Current 835 folder has EDI that is already imported")
            elif self.patient_pay_file_modal_exist():
                self.logger.debug(
                    "There are more than 835 files in the folder. Please ensure only 835 files remain in the folder."
                )
                raise NextGenPatientPayException("Remove Patient Pay from the current 835 Folder")
        except RuntimeError:
            raise NextGenControlLostException("Lost control of NextGen Application")

        while self.import_edi_modal_exist() and datetime.now() < end_time:
            wait_if_high_usage()
            if current_try > max_tries:
                raise Exception(
                    "Could not import current payment folder or lost NextGen reference and could not recover"
                )
            try:
                self._process_import_modal()
            except (ElementNotFoundError, TimeoutError):
                time.sleep(10)
            except _ctypes.COMError:
                wait_if_high_usage()
                self.logger.warning(
                    "Lost control of NextGen Application while processing import modal.Waiting 10 seconds."
                )
                self.desktop_app.app = self.desktop_app.connect_to_logged_in_screen()
                current_try += 1
                time.sleep(10)

        if datetime.now() >= end_time:
            raise NextGenImportTimeoutException("Could not import current payment folder within 3600 seconds")

    @capture_screenshot_if_exception()
    @retry(exceptions=_ctypes.COMError, tries=3, delay=20, backoff=2)
    def _process_import_modal(self) -> None:
        """Handle Import Processing Dialog."""
        modal = self.desktop_app.dialog.child_window(title="NextGen", control_type="Window", found_index=0)
        if self._modal_exists(modal):
            buttons_list = modal.wrapper_object().descendants(control_type="Button")
            if len(buttons_list) == 2 and buttons_list[0].texts()[0] == "OK" and buttons_list[1].texts()[0] == "Close":
                with contextlib.suppress(_ctypes.COMError):
                    modal.child_window(title="OK", auto_id="2", control_type="Button").click()

    def _modal_exists(self, modal: WindowSpecification) -> bool:
        """Check if modal exists.

        Args:
            modal (WindowSpecification): Modal window to check
        Returns:
            bool: True if modal exists, False otherwise
        """
        try:
            return modal.exists()
        except (_ctypes.COMError, RuntimeError):
            wait_if_high_usage()
            self.logger.warning(
                "Lost control of NextGen Application while checking modal existence. Waiting 10 seconds."
            )
            time.sleep(10)
            self.desktop_app.app = self.desktop_app.connect_to_logged_in_screen()
            return modal.exists()

    def convert_edi_files_to_excel(self, excel_file_path: str) -> None:
        """Converts EDI files to Excel format by interacting with the application's excel export functionality.

        Args:
            excel_file_path (str): The file path where the exported excel should be saved.
        """
        self.logger.debug("Converting EDI files to Excel.")
        self.click_export_to_excel_icon()
        self.set_excel_export_path(excel_file_path)
        self.export_edi_files()
        pathlib_path = Path(rf"{excel_file_path}")
        try:
            utility.wait_until_file_downloads(pathlib_path.parent, pathlib_path.name, wait_time=500)
        except TimeoutError:
            if self.is_export_modal_open():
                self.desktop_app.dialog.child_window(auto_id="Cancel", control_type="Button")
                raise PostingSheetTimeOutException("PostingSheet not created within 500 seconds")

    def convert_edi_files_to_csv(self, csv_file_path: str) -> None:
        """Converts EDI files to CSV format by interacting with the application's csv export functionality.

        Args:
            csv_file_path (str): The file path where the exported csv should be saved.
        """
        self.logger.debug("Converting EDI files to CSV.")
        self.click_export_to_csv_icon()
        self.set_csv_export_path(csv_file_path)
        self.export_edi_files()
        pathlib_path = Path(rf"{csv_file_path}")
        try:
            utility.wait_until_file_downloads(pathlib_path.parent, pathlib_path.name, wait_time=500)
        except TimeoutError:
            if self.is_export_modal_open():
                self.desktop_app.dialog.child_window(auto_id="Cancel", control_type="Button")
                raise PostingSheetTimeOutException("PostingSheet not created within 500 seconds")

    def is_export_modal_open(self) -> bool:
        """Checks if the export modal dialog is currently open in the NextGen."""
        try:
            with contextlib.suppress(_ctypes.COMError):
                return self.desktop_app.dialog.child_window(auto_id="FileDialog", control_type="Custom").exists(
                    timeout=3, retry_interval=0.001
                )
        except ElementNotFoundError:
            return False

    def export_edi_files(self) -> None:
        """Click the export button in the window after clicking the excel icon in the NextGen App."""
        self.logger.debug("Exporting EDI files to Excel.")
        with contextlib.suppress(_ctypes.COMError):
            self.report_viewer_window.child_window(title="Export", control_type="Button").click_input()

    def set_excel_export_path(self, export_path: str) -> None:
        """Set csv export path for converted EDIs in the window that pops up after clicking the excel icon.

        Args:
            export_path (str): The path where the generated csv would be stored
        """
        self.logger.debug(f"Setting Excel Export Path: {export_path}")
        closest_window = self.desktop_app.dialog.child_window(
            auto_id="ReportViewer", control_type="Window"
        ).child_window(auto_id="FileDialog", control_type="Custom")
        self.desktop_app.set_text(closest_window.child_window(control_type="Edit"), export_path)

    def click_export_to_excel_icon(self) -> None:
        """Convert imported EDIs to Excel. Clicks on the Export to Excel icon in the NextGen App."""
        self.logger.debug("Clicking on Export to Excel icon.")
        excel_button = (
            self.desktop_app.dialog.child_window(auto_id="ReportViewer", control_type="Window")
            .child_window(control_type="ToolBar", class_name="ToolBar")
            .child_window(control_type="Button", found_index=7)
        )
        if excel_button.exists(timeout=5):
            with contextlib.suppress(_ctypes.COMError):
                excel_button.click_input()
                self.logger.info("Excel button clicked successfully.")

            closest_window = self.desktop_app.dialog.child_window(
                auto_id="ReportViewer", control_type="Window"
            ).child_window(auto_id="FileDialog", control_type="Custom")
            closest_window.wait("ready", timeout=3)
            self.logger.info("FileDialog window is ready.")
        else:
            self.logger.warning("Excel button not found within timeout.")

    def click_export_to_csv_icon(self) -> None:
        """Convert imported EDIs to Excel. Clicks on the Export to Excel icon in the NextGen App."""
        self.logger.debug("Clicking on Export to Excel icon.")
        csv_button = (
            self.desktop_app.dialog.child_window(auto_id="ReportViewer", control_type="Window")
            .child_window(control_type="ToolBar", class_name="ToolBar")
            .child_window(control_type="Button", found_index=8)
        )
        if csv_button.exists(timeout=5):
            with contextlib.suppress(_ctypes.COMError):
                csv_button.click_input()
                self.logger.info("Excel button clicked successfully.")

            closest_window = self.desktop_app.dialog.child_window(
                auto_id="ReportViewer", control_type="Window"
            ).child_window(auto_id="FileDialog", control_type="Custom")
            closest_window.wait("ready", timeout=3)
            self.logger.info("FileDialog window is ready.")
        else:
            self.logger.warning("Excel button not found within timeout.")

    def set_csv_export_path(self, export_path: str) -> None:
        """Set csv export path for converted EDIs in the window that pops up after clicking the excel icon.

        Args:
            export_path (str): The path where the generated csv would be stored
        """
        self.logger.debug(f"Setting Excel Export Path: {export_path}")
        closest_window = self.desktop_app.dialog.child_window(
            auto_id="ReportViewer", control_type="Window"
        ).child_window(auto_id="FileDialog", control_type="Custom")
        self.desktop_app.set_text(closest_window.child_window(control_type="Edit"), export_path)

    @retry(exceptions=(_ctypes.COMError, RuntimeError), tries=5, delay=10, backoff=2)
    def import_edi_modal_exist(self) -> bool:
        """Look at a reference to a modal on the next screen to see if the import is finished.

        The reference of this template comes from the screen after importation.
        If it finds the screen, it returns False due to negation; if it doesn't find the screen,
        a _ctypes.COMError error is raised, which falls into the exception and returns True to
        maintain waiting for the download.
        """
        try:
            report_viewer = self.desktop_app.dialog.child_window(
                title="ERA Import Posting - Enhanced Report Mode", auto_id="ReportViewer", control_type="Window"
            )
            return not report_viewer.exists(timeout=5, retry_interval=1)
        except (ElementNotFoundError, TimeoutError):
            return False
        except (_ctypes.COMError, RuntimeError):
            wait_if_high_usage()
            time.sleep(20)
            self.desktop_app.app = self.desktop_app.connect_to_logged_in_screen()
            report_viewer = self.desktop_app.dialog.child_window(
                title="ERA Import Posting - Enhanced Report Mode", auto_id="ReportViewer", control_type="Window"
            )
            return not report_viewer.exists(timeout=5, retry_interval=0.001)

    def patient_has_duplicated_import(self) -> bool:
        """This method checks if the patient has duplicated import.

        Args:
            dialog2 (WindowSpecification): dialog2 window
        Returns:
            bool: True if the patient has duplicated import, False otherwise
        """
        with contextlib.suppress(_ctypes.COMError):
            return self.desktop_app.dialog.child_window(
                auto_id="65535",
                control_type="Text",
                title="Some files/checks were identified as duplicate imports.  Continue?",
                found_index=0,
            ).exists(timeout=3, retry_interval=0.001)
        return False

    def _handle_duplicate_import(self) -> None:
        """Handle Duplicate Import Dialog.

        Raises:
            NextGenDuplicateImportException: For duplicate import
        """
        nextgen_dialog = self.desktop_app.dialog.child_window(title="NextGen", control_type="Window")
        with contextlib.suppress(_ctypes.COMError):
            nextgen_dialog.child_window(title="No", auto_id="7", control_type="Button").click_input()
            self.window.child_window(title="cmdCancel", control_type="Button").click_input()

    def _handle_patient_pay_exception(self) -> None:
        """Handles Patient Pay Dialog."""
        with contextlib.suppress(_ctypes.COMError):
            self.desktop_app.dialog.child_window(title="Close", control_type="Button", found_index=0).click()
            self.desktop_app.dialog.child_window(title="cmdCancel", control_type="Button").click()

    def patient_pay_file_modal_exist(self) -> bool:
        """This method checks if the Patient Pay file modal exists.

        Returns:
            bool: True if the Patient Pay file modal exists, False otherwise
        """
        with contextlib.suppress(_ctypes.COMError):
            return self.desktop_app.dialog.child_window(
                auto_id="65535",
                control_type="Text",
                title="Please select either ERA files or Patient Pay files but not both.",
                found_index=0,
            ).exists(timeout=3, retry_interval=0.001)
        return False

    @retry(tries=4, delay=2)
    def click_columns_button(self) -> None:
        """Click on the Columns button in the Import Window."""
        self.logger.debug("Clicking on Columns button in Import Window.")
        self.enhanced_report_mode_window.child_window(title="Columns", control_type="Button").click_input()
        self.enhanced_report_mode_window.child_window(auto_id="FilterText", control_type="Edit").wait(
            "ready", timeout=2, retry_interval=0.001
        )

    @retry(tries=4, delay=2)
    def click_totals_button(self) -> None:
        """Click on the Totals button in the Import Window."""
        self.logger.debug("Clicking on Totals button in Import Window.")
        self.enhanced_report_mode_window.child_window(title="Totals", control_type="Button").click_input()
        self.enhanced_report_mode_window.child_window(auto_id="Totals", control_type="Custom").wait(
            "ready", timeout=2, retry_interval=0.001
        )

    @retry(tries=4, delay=2)
    def click_options_button(self) -> None:
        """Click on the Options button in the Import Window."""
        self.logger.debug("Clicking on Options button in Import Window.")
        self.enhanced_report_mode_window.child_window(title="Options", control_type="Button").click_input()
        self.enhanced_report_mode_window.child_window(title="Column Text Wrapping", control_type="CheckBox").wait(
            "ready", timeout=2, retry_interval=0.001
        )

    @retry(tries=4, delay=2)
    def click_header_footer_button(self) -> None:
        """Click on the Header/Footer button in the Import Window."""
        self.logger.debug("Clicking on Header/Footer button in Import Window.")
        header_button = self.enhanced_report_mode_window.child_window(title="Header/Footer", control_type="Button")
        header_button.wait("ready", timeout=10, retry_interval=0.001)
        header_button.click_input()
        self.enhanced_report_mode_window.child_window(title="Header Options", control_type="Group").wait(
            "ready", timeout=10, retry_interval=0.001
        )

    @retry(tries=4, delay=2)
    def click_sorting_button(self) -> None:
        """Click on the Sorting button in the Import Window."""
        self.logger.debug("Clicking on Sorting button in Import Window.")
        self.enhanced_report_mode_window.child_window(title="Sorting", control_type="Button").click_input()
        self.enhanced_report_mode_window.child_window(auto_id="Sorting", control_type="Custom").wait(
            "exists", timeout=2
        )

    def uncheck_all_group_by_checkboxes(self, max_iterations: int = 10) -> None:
        """Uncheck all checkboxes in the Group By Window.

        Args:
            max_iterations (int): Maximum number of iterations to uncheck all checkboxes
        """
        self.logger.debug("Unchecking all group by checkboxes in the Sorting Window.")
        iteration = 0
        while iteration < max_iterations:
            sorting = self.enhanced_report_mode_window.child_window(auto_id="Sorting", control_type="Custom")
            data_grid = sorting.child_window(control_type="DataGrid", found_index=0)
            data_items = data_grid.descendants(control_type="DataItem")
            self.logger.debug(len(data_items))
            for data_item in data_items:
                if data_item.is_visible():
                    text = data_item.descendants(control_type="Text")[0].window_text()
                    if text == "CSC Claim Payment":
                        self.unselect_check_box(data_item)
                        return
                    self.unselect_check_box(data_item)
                    with contextlib.suppress(_ctypes.COMError):
                        data_item.descendants(control_type="Custom")[0].click_input()
            send_keys("{PGDN}")

    def click_column_name_check_box(self) -> None:
        """Click on the Column Name checkbox in the Columns Window."""
        self.logger.debug("Clicking on the Column Name checkbox in the Columns Window.")
        s_text = self.enhanced_report_mode_window.child_window(auto_id="FilterText", control_type="Edit")
        with contextlib.suppress(_ctypes.COMError):
            s_text.click_input()
        send_keys("{TAB}")
        send_keys("{TAB}")
        send_keys("{SPACE}")

    def unselect_check_box(self, data_item: WindowSpecification, index: int = 2) -> None:
        """Click on the checkbox in the ImportFile template options Window.

        Args:
            data_item (WindowSpecification): DataItem control
            index (int): Index of the checkbox in the DataItem control
        """
        check_box = data_item.descendants(control_type="CheckBox")[index]
        self.desktop_app.untoggle_checkbox(check_box)

    def unselect_count_check_boxes(self, max_iterations: int = 10):
        """Unselect the Count checkboxes in the Columns Window.

        Args:
            max_iterations (int): Maximum number of iterations to unselect the Count checkboxes
        """
        iteration = 0
        while iteration < max_iterations:
            totals = self.enhanced_report_mode_window.child_window(auto_id="Totals", control_type="Custom")
            data_grid = totals.child_window(control_type="DataGrid", found_index=0)
            data_items = data_grid.descendants(control_type="DataItem")
            self.logger.debug(f"Number of data items: {len(data_items)}")
            for data_item in data_items:
                if data_item.is_visible():
                    text = data_item.descendants(control_type="Text")[0].window_text()
                    if text == "CSC Claim Payment":
                        self.unselect_check_box(data_item)
                        return
                    self.unselect_check_box(data_item)
                    with contextlib.suppress(_ctypes.COMError):
                        data_item.descendants(control_type="Custom")[0].click_input()
            send_keys("{PGDN}")

    def unselect_count_records_check_box(self) -> None:
        """Unselect the Count Records checkbox in the Columns Window."""
        self.logger.debug("Unselecting the Count Records checkbox in the Columns Window.")
        count_record_check_box = self.enhanced_report_mode_window.child_window(
            title="Count Records", control_type="CheckBox"
        )
        self.desktop_app.untoggle_checkbox(count_record_check_box)

    def click_refresh_report_button(self):
        """Click on the Refresh Report button."""
        self.logger.debug("Clicking on the Refresh Report button.")
        custom = self.enhanced_report_mode_window.child_window(auto_id="Me", control_type="Custom")
        buttons = custom.descendants(control_type="Button")
        for button in buttons:
            if button.descendants(control_type="Text")[0].window_text() == "_Refresh Report":
                with contextlib.suppress(_ctypes.COMError):
                    button.click_input()
                break

    def unselect_column_text_wrapping_check_box(self) -> None:
        """Unselect the Column Text Wrapping checkbox in the Columns Window."""
        self.logger.debug("Unselecting the Column Text Wrapping checkbox in the Columns Window.")
        check_box = self.enhanced_report_mode_window.child_window(title="Column Text Wrapping", control_type="CheckBox")
        self.desktop_app.untoggle_checkbox(check_box)

    def unselect_all_check_box_from_header(self) -> None:
        """Unselect all checkboxes from the Header Window."""
        self.logger.debug("Unselecting all checkboxes from the Header Window.")

        header = self.enhanced_report_mode_window.child_window(auto_id="HeaderFooter", control_type="Custom")
        check_boxes = header.descendants(control_type="CheckBox")
        for check_box in check_boxes:
            self.desktop_app.untoggle_checkbox(check_box)

    def click_close_button_in_import_posting_report_window(self):
        """Click on the Close button in the Import Posting Report Window."""
        self.logger.debug("Clicking on the Close button in the Import Posting Report Window.")
        with contextlib.suppress(_ctypes.COMError):
            self.report_viewer_window.child_window(control_type="ToolBar", class_name="ToolBar").child_window(
                control_type="Button", found_index=18
            ).click_input()
