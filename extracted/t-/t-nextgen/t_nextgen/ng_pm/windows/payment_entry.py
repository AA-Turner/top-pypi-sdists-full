"""PaymentEntry module."""
import contextlib
import ctypes
import _ctypes
from datetime import datetime
from logging import Logger
import os
from pathlib import Path
import re
from typing import Optional
from typing import Any, List
from retry import retry
from t_ocr.ocr import OCR

from decimal import Decimal
from t_desktop.config import IS_WINDOWS_OS
from t_desktop.utils.capture_screenshot import capture_screenshot

if IS_WINDOWS_OS:
    from pywinauto.application import WindowSpecification
    from pywinauto.controls.uia_controls import ListItemWrapper, EditWrapper
    from pywinauto.findwindows import ElementNotFoundError
    from pywinauto.base_wrapper import ElementNotEnabled
    from pywinauto.keyboard import send_keys
    from pywinauto.timings import wait_until, TimeoutError

from t_desktop.decorators import retry_if_pywin_error
from t_desktop.decorators import capture_screenshot_if_pywin_error
from t_ocr import Textract
from PIL import Image, ImageFilter

from t_nextgen.nextgen_window import NextGenWindow
from t_nextgen.utils.convert_to_decimal import convert_to_decimal
from t_nextgen.utils.opencv import OpenCV
from t_nextgen.exceptions import (
    AdjFieldNotFoundException,
    BalanceFieldNotFoundException,
    Ins1FieldNotFoundException,
    Ins2FieldNotFoundException,
    Ins3FieldNotFoundException,
    LnItemRsnsNotUpdatedException,
    PayFieldNotFoundException,
    ServiceLineMissingRequiredFieldError,
    TransactionNumberNotFoundError,
    DeductFieldNotFoundException,
    FieldNotFoundException,
    StatusNotUpdatedException,
    ButtonIsStillEnabledException,
    PayerNotUpdatedException,
)


class PaymentEntryWindow(NextGenWindow):
    """PaymentEntry class with methods to interact with payment entry window."""

    def __init__(self, app_path: str, logger: Logger, textract: Optional[Textract]):
        """Initialize the PaymentEntryWindow class.

        Args:
            app_path (str): The application path.
            textract (Optional[Textract]): The Textract object.
            logger (Logger): The logger object.

        """
        self.textract = textract
        super().__init__(app_path, logger)

    @property
    def window(self) -> WindowSpecification:
        """Return the PaymentEntry window element."""
        return self.desktop_app.dialog.child_window(title="PaymentEntry", control_type="Window")

    def set_all_service_lines_to_appeal(self) -> None:
        """This method sets all the service lines to appeal."""
        # Look at set_encounter_to_appeal_function
        self.logger.info("Setting Encounter to Appeal...")
        self.click_open_button()
        rows = self.get_service_rows()
        for row in rows:
            if self.get_pay_field(row):
                self.select_status_in_dropdown(status="Appeal", row=row, status_key="A")

    def get_pay_field(self, row: ListItemWrapper) -> str:
        """This method gets the pay field text in a specific row.

        Args:
            row (ListItemWrapper): list item wrapper with the row
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "pay" in window_text.lower():
                return item.get_value()
        raise PayFieldNotFoundException("Pay field not found in the row")

    def get_cpt4_field(self, row: ListItemWrapper) -> str:
        """This method gets the cpt 4 field text in a specific row."""
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "cpt4" in window_text.lower():
                element = row.descendants(title=window_text, control_type="Edit")[0]
                return element.get_value()
        raise FieldNotFoundException("cpt 4 field not found in the row")

    def get_qty_charge_field(self, row: ListItemWrapper) -> str:
        """This method gets the qty/charge text in a specific row."""
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "qty/charge" in window_text.lower():
                return item.get_value()
        raise FieldNotFoundException("qty/charge not found in the row")

    def get_date_field(self, row: ListItemWrapper) -> str:
        """This method gets the Date field text in a specific row."""
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "date" in window_text.lower():
                return item.get_value()
        raise FieldNotFoundException("Date field not found in the row")

    def is_line_voided(
        self, row: ListItemWrapper, column_name: str = "Rendering", image_path: Path = Path("C:\\Temp\\")
    ) -> bool:
        """Check if the line is voided.

        Args:
            row: The row to be checked
            column_name: The column name to be checked (optional - default: "Rendering")

        Returns:
            bool: True if the line is voided, False otherwise
        """
        image_path.mkdir(parents=True, exist_ok=True)
        element = row.descendants(title=column_name)[0]
        is_line_voided = self.is_text_strikethrough(element, image_path)
        if is_line_voided:
            self.logger.debug("The line is voided")
        return is_line_voided

    @staticmethod
    def is_text_strikethrough(element: Any, image_path: Path) -> bool:
        """Check if the text in the element is strikethrough.

        Args:
            element: The element to be checked
        Returns:
            bool: True if the text is strikethrough, False otherwise
            image_path: Path to save the image
        """
        # element name with the hour min and sec
        element_name_with_date = f"{element.window_text()}_{datetime.now().strftime('%H_%M_%S_%f')}.png"
        element_image_path = os.path.join(image_path, element_name_with_date)
        image_element = element.capture_as_image()
        # Convert the image to grayscale
        grayscale_image = image_element.convert("L")
        # Sharpen the grayscale image to enhance the edges of the text
        sharpened_image = grayscale_image.filter(ImageFilter.SHARPEN)
        # Convert the sharpened image back to RGB
        sharpened_rgb_image = sharpened_image.convert("RGB")
        sharpened_rgb_image.save(element_image_path)
        is_strikethrough_present = OpenCV.check_strikethrough_in_text_image(element_image_path)
        os.remove(element_image_path)
        return is_strikethrough_present

    @retry(ButtonIsStillEnabledException, tries=3, delay=1)
    def click_open_button(self) -> None:
        """This method clicks on the open button."""
        self.logger.debug("Clicking on the open button.")
        try:
            open_button = self.window.child_window(title="_cmdAction_1", control_type="Button")
            if open_button.is_enabled():
                with contextlib.suppress(_ctypes.COMError):
                    open_button.click_input()
                    open_button.wait_not("enabled", timeout=3, retry_interval=0.001)
        except TimeoutError:
            self.logger.error("Timeout error waiting for open button to be disabled.")
            raise ButtonIsStillEnabledException()

    def get_service_rows(self) -> list[ListItemWrapper]:
        """This method gets the service rows from the current payment entry window.

        Returns:
            rows (list): list of service rows
        """
        pane = self.window.child_window(title="lstPayLedger", control_type="Pane")
        rows = pane.wrapper_object().descendants(control_type="DataItem")
        self.logger.debug(f"Number of rows in Payment Entry: {len(rows)}")
        return rows

    @retry(LnItemRsnsNotUpdatedException, tries=3, delay=1)
    def insert_text_in_ln_item_rsns(self, text: str, row: ListItemWrapper) -> None:
        """This method inserts text in the Ln Item Rsns field.

        Args:
            text (str): text to be inserted. This text will have codes separated by commas (Ex:"PR2,CO45")
            row (ListItemWrapper): row to select. Will use the first row if not provided
        """
        self.logger.debug(f"Inserting text in Ln Item Rsns: {text}")
        if self.is_payer_a_patient():
            self.logger.info("The payer is Patient. Ln Item Rsns field is disabled")
            return

        self.remove_selected_items_from_ln_combobox(row)
        self.set_text_in_specific_row(row, "Ln Item Rsns", text, is_combobox=True)
        row = self._get_row_by_auto_id(row.automation_id())  # need to get the row with updated Ln Item Rsns
        next_gen_codes = row.descendants(title="Ln Item Rsns", control_type="Edit")[0].get_value()
        # next_gen_codes example :  'CO45  (Charges exceed fee arrangement); PR2  (Coinsurance amount)'
        codes_inserted = text.split(",")
        for code in codes_inserted:
            if code.strip() not in next_gen_codes:
                self.skipping_payer_aarp_pop_up_exist()
                raise LnItemRsnsNotUpdatedException(f"Error trying to insert {text} in Ln Item Rsns field.")
        return row

    @retry(LnItemRsnsNotUpdatedException, tries=3, delay=1)
    def add_codes_in_ln_item_rsns(self, text: str, row: ListItemWrapper) -> None:
        """Add one or more codes to Ln Item Rsns without removing existing ones.

        Args:
            text (str): Comma-separated codes to add (e.g., "PR2,CO45").
            row (ListItemWrapper): Row to update.
        """
        self.logger.debug(f"Adding codes to Ln Item Rsns: {text}")
        if self.is_payer_a_patient():
            self.logger.info("The payer is Patient. Ln Item Rsns field is disabled")
            return

        existing_codes = self._get_existing_ln_item_rsns_codes(row)
        new_codes = [c.strip().upper() for c in text.split(",") if c.strip()]
        combined_codes = existing_codes + [c for c in new_codes if c not in existing_codes]

        if combined_codes == existing_codes:
            self.logger.debug("Ln Item Rsns already contains requested codes; nothing to do.")
            return row

        combined_text = ",".join(combined_codes)

        self.remove_selected_items_from_ln_combobox(row)
        self.set_text_in_specific_row(row, "Ln Item Rsns", combined_text, is_combobox=True)

        row = self._get_row_by_auto_id(row.automation_id())
        next_gen_codes = (row.descendants(title="Ln Item Rsns", control_type="Edit")[0].get_value() or "").upper()

        for code in combined_codes:
            if code.strip().upper() not in next_gen_codes:
                self.skipping_payer_aarp_pop_up_exist()
                raise LnItemRsnsNotUpdatedException(f"Error trying to add {text} in Ln Item Rsns field.")

        return row

    def _get_existing_ln_item_rsns_codes(self, row: ListItemWrapper) -> list[str]:
        """Return the list of currently selected Ln Item Rsns codes for the given row.

        The NextGen control renders values like:
        'CO45  (Charges exceed fee arrangement); PR2  (Coinsurance amount)'.
        We parse and return only the raw codes: ['CO45', 'PR2'].
        """
        row = self.revalidate_service_row(row)
        value = row.descendants(title="Ln Item Rsns", control_type="Edit")[0].get_value()
        if value.strip() == "":
            return []

        parts = re.split(r"[;,]\s*", value)
        parts = [p.strip() for p in parts if p.strip()]

        codes: list[str] = []
        for part in parts:
            code_text = part.split("(")[0].strip()
            code_token = code_text.split()[0] if code_text else ""
            if code_token:
                codes.append(code_token.upper())

        return codes

    def remove_selected_items_from_status_combobox(self, row: ListItemWrapper) -> None:
        """Removes the selected items from the Status combobox.

        Args:
            row (ListItemWrapper): row to select
        """
        self.logger.debug("Removing selected items from Status combobox")
        row = self.revalidate_service_row(row)
        _input = row.descendants(title="Status", control_type="Edit")[0]

        if _input.get_value() == "":
            return
        with contextlib.suppress(_ctypes.COMError):
            _input.click_input(double=True)
        pane = self.window.child_window(title="_cboInput_0", control_type="Pane")
        combo_box = pane.child_window(control_type="ComboBox")
        combo_box.wait("ready", 2)
        self.desktop_app.dialog.child_window(
            auto_id="ColScrollRegion: 0, RowScrollRegion: 0", found_index=0
        ).right_click_input()
        send_keys("D")
        send_keys("{ESC}{TAB}")

    def is_payer_a_patient(self) -> bool:
        """This method checks if the payer is Patient.

        Returns:
            bool: True if payer is Patient, False otherwise
        """
        vse_container = self.window.child_window(auto_id="vseContainer", control_type="Text")
        cbo_input = vse_container.child_window(auto_id="_cboInput_104", control_type="Pane")
        mcbo = cbo_input.child_window(auto_id="mcbo", control_type="ComboBox")
        payer = mcbo.child_window(control_type="Edit", found_index=0)
        return payer.get_value().lower() == "patient"

    @retry(StatusNotUpdatedException, tries=3, delay=1)
    def select_status_in_dropdown(
        self, status: str = "Appeal", row: ListItemWrapper | None = None, status_key: str = ""
    ) -> bool:
        """This method selects the specified status in the dropdown.

        Args:
            status (str): status to be selected (default is "Appeal")
            row (ListItemWrapper): row to select. Will use the first row if not provided
            status_key (str): Shortcut key for setting status (default sets to "Appeal" using "A"). Use
            only if first character of status is unique

        Returns:
            bool: True if the status was selected, False if it was already set
        """
        self.logger.debug(f"Selecting status in dropdown: {status}")
        self.click_open_button()
        row = self.revalidate_service_row(row)
        status_field = self.get_status_field(row)
        if status_field.get_value().lower() == status.lower():
            self.logger.debug(f"Status was already set. Value: {status}")
            return
        pane = self.open_status_dropdown_in_service_row(status_field, row)
        if len(status.split()) > 2:
            beginning, end = status.split()[0], status.split()[-1]
            status = self.get_status_in_dropdown_that_begin_with_and_end_with(beginning, end, pane)
        self.select_status_in_service_row(pane, status, status_key)
        row = self.revalidate_service_row(row)
        status_field = self.get_status_field(row)
        selected_status = status_field.get_value()
        if selected_status == "" or selected_status.lower() != status.lower():
            capture_screenshot(f"Failed_to_set_status_{status}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise StatusNotUpdatedException(f"Failed to select status {status} in dropdown")

    def get_statuses(self, pane: ListItemWrapper) -> list[str]:
        """This method gets all the statuses in the status dropdown.

        Args:
            pane (ListItemWrapper): Pane element containing the status dropdown.

        Returns:
            list[str]: A list of all the statuses in the dropdown.
        """
        combo_box = pane.child_window(control_type="ComboBox")
        combo_box_element = combo_box.wrapper_object()
        status_list = []
        for item in combo_box_element.descendants(control_type="ListItem"):
            status_list.append(item.window_text())
        return status_list

    def get_status_in_dropdown_that_begin_with_and_end_with(
        self, start_with: str, ends_with: str, pane: EditWrapper
    ) -> str:
        """This method gets the status in the drop down that begins with the value provided.

        Args:
            start_with (str): value to be searched for in the status column
            ends_with (str): value to be searched for in the status column
            pane (EditWrapper): Represents the pane element of the status field

        Returns:
            str: The selected status
        """
        self.logger.debug(f"Selecting status in dropdown that begins with: {start_with} and ends with {ends_with}")

        combo_box = pane.child_window(control_type="ComboBox")
        combo_box_element = combo_box.wrapper_object()
        for item in combo_box_element.descendants(control_type="ListItem"):
            status = item.window_text()
            if status.lower().startswith(start_with.lower()) and status.lower().endswith(ends_with.lower()):
                return status
        return ValueError(f"Could not find status that begins with: {start_with} and ends with {ends_with}")

    def select_status_in_service_row(self, pane: WindowSpecification, status: str, status_key: str = "") -> None:
        """Set status in the status column of current service row.

        Args:
            pane (WindowSpecification): Represents the pane element of the status field
            status (str): Status we want to set
            status_key (str, optional): Shortcut Key for setting status using first character of status. Use
            only if first character of status is unique
        """
        if status_key:
            send_keys(status_key)
            send_keys("{ENTER}")
        else:
            combo_box = pane.child_window(control_type="ComboBox")
            self.desktop_app.set_text(
                combo_box.child_window(auto_id="mcbo_EmbeddableTextBox", control_type="Edit"), status
            )
            with contextlib.suppress(_ctypes.COMError):
                pane.click_input()
                send_keys("+{TAB}")

    @retry(ElementNotFoundError, tries=3, delay=1)
    def open_status_dropdown_in_service_row(self, status_field: EditWrapper, row: ListItemWrapper) -> EditWrapper:
        """Open the status dropdown for the provided status field.

        Args:
            status_field (EditWrapper): the status field whose dropdown is to be opened
            row (ListItemWrapper): row to revalidate

        Returns:
            WindowSpecification: Represents the pane element of the status field
        """
        self.logger.debug("Opening status dropdown in service row")
        for i in range(3):
            row = self.revalidate_service_row(row)
            status_field = self.get_status_field(row)
            status_field.click_input()
        pane = self.desktop_app.dialog.child_window(title="_cboInput_0", control_type="Pane")
        return pane

    def get_status_field(self, row: ListItemWrapper) -> EditWrapper:
        """Get status field from service row.

        Args:
            row (ListItemWrapper): The service row from which to fetch status field

        Returns:
            EditWrapper: the status field
        """
        status_field = row.descendants(title="Status", control_type="Edit")[0]
        return status_field

    def select_item_in_line_dropdown(self, row: ListItemWrapper, column_name: str, item: str) -> None:
        """This method selects the specified item in the dropdown.

        Args:
            row (ListItemWrapper): row to use
            column_name (str): column name
            item (str): item to be selected
        """
        self.logger.debug(f"Selecting item in dropdown: {item}")
        row = self._get_row_by_auto_id(row.automation_id())
        input = row.descendants(title=column_name, control_type="Edit")[0]
        if input.get_value() == str(item):
            return
        self.desktop_app.mouse_click_element(input, "left")
        self.desktop_app.mouse_click_element(input, "left")
        pane = self.desktop_app.dialog.child_window(title="_cboInput_0", control_type="Pane")
        combo_box = pane.child_window(control_type="ComboBox")
        combo_box.wait("ready", 2)
        edit_text = combo_box.child_window(control_type="Edit", found_index=0)
        self.desktop_app.set_text(edit_text, item)
        edit_text.type_keys("{ENTER}")
        combo_box.wait("ready", 2)
        input.set_focus()  # focus again in input to remove the dropdown from screen

    def _get_row_by_auto_id(self, auto_id: str) -> ListItemWrapper:
        """This method gets the row by auto_id from the current payment entry window.

        Args:
            auto_id (str): auto_id of the row
        Returns:
            row (ListItemWrapper): row object
        """
        pane = self.desktop_app.dialog.child_window(title="lstPayLedger", control_type="Pane")
        row = pane.child_window(control_type="DataItem", auto_id=auto_id)
        return row.wrapper_object()

    def set_transaction_notes_text(self, notes: str) -> None:
        """This method sets the transaction notes text.

        Args:
            notes (str): transaction notes text
        """
        self.logger.debug(f"Setting transaction notes text: {notes}")
        transaction_note_input = self.window.child_window(auto_id="txtTransactionNotes", control_type="Edit")
        with contextlib.suppress(_ctypes.COMError):
            transaction_note_input.set_edit_text(notes)

    def click_recalc_button(self, click_recalc_button: bool = True) -> None:
        """Clicks the recalc button."""
        if click_recalc_button:
            self.logger.debug("Clicking recalc button in Payment Entry Window.")
            with contextlib.suppress(_ctypes.COMError):
                self.window.child_window(title="_cmdAction_6", control_type="Button").click()
        else:
            self.logger.warning("Skipping recalc button click to prevent changes.")

    def click_save_button(self, click_save_button: bool = True) -> None:
        """Clicks the save button."""
        if click_save_button:
            self.logger.debug("Clicking save button on Payment Entry Window.")
            with contextlib.suppress(_ctypes.COMError):
                self.window.child_window(title="_cmdAction_2", control_type="Button").click()
            self.verify_and_handle_modal("Please specify a status for each line item payments and adjustment.")
        else:
            self.logger.warning("Clicking cancel in payment entry to prevent changes.")
            self.click_cancel()

    def click_cancel(self) -> None:
        """Clicks the cancel button on the payment entry window."""
        self.logger.debug("Clicking cancel button on Payment Entry Window.")
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(title="_cmdAction_3", control_type="Button").click()

    def verify_and_handle_modal(self, expected_text: str) -> None:
        """Verifies a modal's text and raises an exception if it matches the expected text.

        Args:
            expected_text (str): The expected text to verify in the modal.
        """
        success, modal_text = self.desktop_app.close_modal(timeout=2)
        if not success:
            return
        self.logger.debug(f"Modal appeared. Text: {modal_text}")
        if modal_text.upper() == expected_text.upper():
            message = f"'{expected_text}' found in the modal. Raising exception."
            self.click_cancel()
            raise ServiceLineMissingRequiredFieldError(message)

    def set_text_in_specific_row_to_adj_field(self, row: ListItemWrapper, text: str | float) -> None:
        """This method sets the text in a specific row to the adj field.

        The adj column can have different names on it. All of them have pay in the text.

        Args:
            row (ListItemWrapper): list item wrapper with the row
            text (str): text to be inserted
        """
        self.logger.debug(f"Setting text in Adj field: {text}")
        items = row.children(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "adj" in window_text.lower():
                self.set_text_in_specific_row(row, window_text, text)
                self.skipping_payer_aarp_pop_up_exist()
                return
        raise AdjFieldNotFoundException("Adj field not found in the row")

    def set_text_in_specific_row(
        self, row: ListItemWrapper, element_name: str, text: str | float, is_combobox: bool = False
    ) -> None:
        """This method sets the text in a specific row.

        Args:
            row (ListItemWrapper): list item wrapper with the row
            element_name (str): element name
            text (str): text to be inserted
            is_combobox (bool): True if the element is a combobox, False otherwise
        """
        row = self.revalidate_service_row(row)
        element = row.descendants(title=element_name, control_type="Edit")[0]
        if element.get_value() == str(text):
            return
        self.desktop_app.mouse_double_click_element(element)
        with contextlib.suppress(_ctypes.COMError):
            wait_until(timeout=7, retry_interval=0.7, func=element.is_visible)
        self.desktop_app.mouse_double_click_element(element)
        with contextlib.suppress(_ctypes.COMError):
            wait_until(timeout=10, retry_interval=1, func=element.is_editable)
        self.desktop_app.set_text(element, text)
        self.desktop_app.mouse_double_click_element(element)

    def revalidate_service_row(self, row: ListItemWrapper, retries: int = 2) -> ListItemWrapper:
        """This method revalidates the service row in case the state of the row is not as expected.

        (i.e. the row is not visible or the coordinates are (0, 0))

        Args:
            row (ListItemWrapper): row to revalidate
            retries (int): number of retries
        Returns:
            row (ListItemWrapper): revalidated row
        """
        row_coords = self.desktop_app.get_element_coordinates(row)
        if row_coords == (0, 0) and retries > 0:
            refreshed_row = self._get_row_by_auto_id(row.automation_id())
            return self.revalidate_service_row(refreshed_row, retries=retries - 1)
        return row

    def get_claim_date(self) -> str:
        """This method get Claim Date Input value.

        Returns:
             str: claim input date value
        """
        claim_date_input = self.desktop_app.dialog.child_window(auto_id="mtxtDate", control_type="Edit")
        claim_date_value = claim_date_input.get_value()
        return claim_date_value

    def get_transaction_notes_text(self) -> str:
        """This method gets the transaction notes text.

        Returns:
            str: transaction notes text
        """
        transaction_note_input = self.window.child_window(auto_id="txtTransactionNotes", control_type="Edit")
        notes_value = transaction_note_input.get_value()
        return notes_value

    def get_pay_value_from_specific_row(self, row: ListItemWrapper) -> str:
        """This method gets a value from a specific row.

        Args:
            row (ListItemWrapper): list item wrapper with the row
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "pay" in window_text.lower():
                element = row.descendants(title=window_text, control_type="Edit")[0]
                return element.get_value()
        raise PayFieldNotFoundException("Pay Field not found")

    def get_adj_value_from_specific_row(self, row: ListItemWrapper) -> str:
        """Get the value from the "Adj" field in the row.

        Args
            matching_row (ListItemWrapper): if this argument is given, the method will
            search for the adj in this line.

        Returns:
            str: The value in the "Adj" field.
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "adj" in window_text.lower():
                adj = row.children(title=window_text, control_type="Edit")[0]
                return adj.get_value()
        raise AdjFieldNotFoundException("Adj Field not found")

    def get_ins1_value_from_specific_row(self, row: ListItemWrapper) -> str:
        """Get the value from the "Ins 1" field in the row.

        Args:
            row (ListItemWrapper): Will search for the Ins 1 in this line.

        Returns:
            str: The value in the "Ins 1" field.
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "ins 1" in window_text.lower():
                ins1 = row.children(title=window_text, control_type="Edit")[0]
                return ins1.get_value()
        raise Ins1FieldNotFoundException("Ins 1 field not found")

    def get_ins2_value_from_specific_row(self, row: ListItemWrapper) -> str:
        """Get the value from the "Ins 2" field in the row.

        Args:
            row (ListItemWrapper): Will search for the Ins 2 in this line.

        Returns:
            str: The value in the "Ins 2" field.
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "ins 2" in window_text.lower():
                ins2 = row.children(title=window_text, control_type="Edit")[0]
                return ins2.get_value()
        raise Ins2FieldNotFoundException("Ins 2 field not found")

    def get_ins3_value_from_specific_row(self, row: ListItemWrapper) -> str:
        """Get the value from the "Ins 3" field in the row.

        Args:
            row (ListItemWrapper): Will search for the Ins 3 in this line.

        Returns:
            str: The value in the "Ins 3" field.
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "ins 3" in window_text.lower():
                ins3 = row.children(title=window_text, control_type="Edit")[0]
                return ins3.get_value()
        raise Ins3FieldNotFoundException("Ins 3 field not found")

    def get_balance_value_from_specific_row(self, row: ListItemWrapper) -> str:
        """Get the value from the "Balance" field in the row.

        Args:
            row (ListItemWrapper): Will search for the Balance in this line.

        Returns:
            str: The value in the "Balance" field.
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "balance" in window_text.lower():
                balance = row.children(title=window_text, control_type="Edit")[0]
                return balance.get_value()
        raise BalanceFieldNotFoundException("Balance field not found")

    @retry(ElementNotFoundError, tries=3, delay=0.5)
    def remove_selected_items_from_ln_combobox(self, row: ListItemWrapper) -> None:
        """Removes the selected items from the Ln Item Rsns combobox.

        Args:
            row (ListItemWrapper): row to select
        """
        row = self.revalidate_service_row(row)
        _input = row.descendants(title="Ln Item Rsns", control_type="Edit")[0]
        if _input.get_value() == "":
            return
        with contextlib.suppress(_ctypes.COMError):
            _input.double_click_input()
            _input.click_input()
            _input.click_input()
        with contextlib.suppress(_ctypes.COMError):
            self.desktop_app.app.window(title="MainForm").child_window(
                title="", control_type="Window"
            ).right_click_input()
        send_keys("D")
        send_keys("{ESC}{TAB}")

    def maximize_window(self) -> None:
        """Maximize the Payment Entry Window."""
        self.logger.debug("Maximizing Payment Entry Window.")
        self.window.maximize()

    @retry_if_pywin_error(retries=2, delay=5)
    @capture_screenshot_if_pywin_error()
    def click_new_button(self) -> None:
        """Click New Button."""
        self.logger.debug("Clicking New Button.")
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(title="_cmdAction_0", control_type="Button").click()
            self.desktop_app.wait_until_element_visible(
                title="_txtActiveSearch_103", control_type="Edit", timeout=30, retries=3
            )

    def enter_text_in_enc_clm_field(self, text: str) -> None:
        """This method inserts text in the Enc/Clm #.

        Args:
            text (str): text to be inserted
        """
        self.logger.debug(f"Inserting text in Enc/Clm #: {text}")
        with contextlib.suppress(_ctypes.COMError):
            container = self.window.child_window(auto_id="vseContainer", control_type="Text")
            self.desktop_app.set_text(container.child_window(title="_txtActiveSearch_103", control_type="Edit"), text)
            send_keys("{ENTER}")

    def enter_text_in_tracking_field(self, text: str) -> None:
        """This method inserts text in the Enc/Clm #.

        Args:
            text (str): text to be inserted
        """
        self.logger.debug(f"Inserting text in Tracking #: {text}")
        with contextlib.suppress(_ctypes.COMError):
            container = self.window.child_window(auto_id="vseContainer", control_type="Text")
            self.desktop_app.set_text(container.child_window(title="_txtDataEntry_105", control_type="Edit"), text)
            send_keys("{ENTER}")

    def click_close_nextgen_alerts(self, timeout: int = 5, retry_interval: float = 0.001) -> None:
        """Click close button on NextGen Alerts.

        Args:
            timeout (int, optional): Time to wait for alert to appear. Defaults to 5.
            retry_interval (float, optional): Time between retries when checking for alert. Defaults to 1.
        """
        alert = self.desktop_app.dialog.child_window(title="NextGen Alerts", control_type="Window")
        if alert.exists(timeout=timeout, retry_interval=retry_interval):
            self.logger.debug("Clicking close on NextGen Alerts")
            with contextlib.suppress(_ctypes.COMError):
                alert.child_window(title="Close", control_type="Button").click()

    def click_yes_encounter_in_history_status_pop_up(self, timeout: int = 1, window_title: str = "NextGen") -> None:
        """Click yes button in the encounter in history status pop-up.

        Args:
            timeout (int, optional): Time to wait for the pop-up to appear. Defaults to 1.
            window_title (str, optional): Title of the pop-up window. Defaults to "NextGen".
        """
        alert_window = self.desktop_app.dialog.child_window(title=window_title, control_type="Window")

        if alert_window.child_window(
            title="The encounter is in a history status.  Posting a transaction(s) against this encounter "
            "will reinstate the encounter to a billed status.  Do you want to continue?",
            control_type="Text",
        ).exists(timeout=timeout, retry_interval=0.001):
            self.logger.debug("Clicking Yes in Encounter in History Status pop-up")
            with contextlib.suppress(_ctypes.COMError):
                alert_window.child_window(title="Yes", control_type="Button").click()

    def _capture_pages_data_as_image_in_window(self) -> Image:
        """Capture Pages Data as Image.

        Returns:
            Image: the captured image
        """
        container = self.desktop_app.dialog.child_window(auto_id="vseContainer", control_type="Text")
        custom_control = container.child_window(auto_id="_lblDisplayField_0", control_type="Text")
        return custom_control.capture_as_image()

    def get_pay_column_header_text(self) -> str:
        """Get the text of the Pay column header.

        Returns:
            str: The Pay column header text.
        """
        pay_column_header = self.window.child_window(auto_id="[Column Header] Column18", control_type="HeaderItem")
        pay_column_header_text = pay_column_header.window_text()
        self.logger.debug(f"Pay column header text: {pay_column_header_text}")
        return pay_column_header_text

    def get_adj_column_header_text(self) -> str:
        """Get the text of the Adj column header.

        Returns:
            str: The Adj column header text.
        """
        adj_column_header = self.window.child_window(auto_id="[Column Header] Column19", control_type="HeaderItem")
        adj_column_header_text = adj_column_header.window_text()
        self.logger.debug(f"Adj column header text: {adj_column_header_text}")
        return adj_column_header_text

    def get_pages_data(self, screenshot_destination: Path, text_extraction_service: OCR) -> str:
        """Extract Pages Dataw.

        Returns:
            str: the pages data as text
            text_extraction_service (OCR): Object of OCR class
        """
        image = self._capture_pages_data_as_image_in_window()
        return self.get_data_from_image(image, screenshot_destination, text_extraction_service)

    def get_data_from_image(
        self, image: Image.Image, screenshot_destination: Path, text_extraction_service: OCR
    ) -> str:
        """Extract text from image after preprocessing it.

        Args:
            image (Image.Image): The image from which to extract text.
            parsing_settings (PSM): The parsing settings.
            text_extraction_service (OCR): Object of OCR class

        Returns:
            str: The extracted text.
        """
        screenshot_name = f'temp_screenshot_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
        screenshot_location = screenshot_destination / screenshot_name
        image.save(screenshot_location)

        # Perform OCR
        ocrd_image = text_extraction_service.read_image_page(screenshot_location, cache_data=False)

        # Clean up the temporary image file
        screenshot_location.unlink()

        return ocrd_image.full_text

    def get_transaction_number(
        self, screenshot_destination: Path, text_extraction_services: List[OCR]
    ) -> Optional[str]:
        """Extracts and returns the transaction number using fallback approach.

        First tries to get the transaction number using handle method,
        then falls back to OCR if the handle method fails.

        Returns:
            Optional[str]: The transaction number if found, otherwise raises TransactionNumberNotFoundError.
        """
        # First approach: Try to get transaction number using handle method
        txn_handle = self.get_handle_of_transaction_number_field()
        txn_value = self.get_text_from_hwnd(txn_handle)
        match = re.search(r"(\d+)\s*of\s*\d+", txn_value)
        if match:
            txn_value = "00" + match.group(1)
            self.logger.debug(f"Transaction Number (handle method): {txn_value}")
            return txn_value

        # Second approach: Fallback to OCR method
        self.logger.debug("Handle method failed, trying OCR approach")
        self.maximize_window()
        self.desktop_app.wait_until_element_visible(auto_id="vseContainer", control_type="Text")
        for service in text_extraction_services:
            page_data = self.get_pages_data(screenshot_destination, service)
            match = re.search(r"(\d+)\s*of\s*\d+", page_data)
            if match:
                txn_value = "00" + match.group(1)
                self.logger.debug(f"Transaction Number (OCR method): {txn_value}")
                return txn_value

        raise TransactionNumberNotFoundError("Transaction number not found in the page data.")

    def get_handle_of_transaction_number_field(self) -> int:
        """This method gets the handle of transaction number field."""
        element = self.window.child_window(auto_id="_lblDisplayField_0", control_type="Text")
        return element.handle

    def get_text_from_hwnd(self, hwnd: int) -> str:
        """Get text from a window/control handle using SendMessage."""
        # Text size in control
        length = ctypes.windll.user32.SendMessageW(hwnd, 0x000E, 0, 0)
        if length == 0:
            return ""
        # Create buffer to receive the text
        buffer = ctypes.create_unicode_buffer(length + 1)
        # Fill the buffer with text
        ctypes.windll.user32.SendMessageW(hwnd, 0x000D, length + 1, buffer)
        return buffer.value

    def click_shield_icon(self) -> None:
        """Click shield icon in payment entry window."""
        self.logger.debug("Clicking shield icon in Payment Entry Window.")
        pnl_small_tool = self.window.child_window(title="pnlSmallTool", control_type="Text")
        with contextlib.suppress(_ctypes.COMError):
            pnl_small_tool.child_window(auto_id="_cmdSmallTool_03", control_type="Button").click_input()

    def click_balance_control_icon(self) -> None:
        """Click balance control icon in payment entry window."""
        self.logger.debug("Clicking balance control icon in Payment Entry Window.")
        pnl_small_tool = self.window.child_window(title="pnlSmallTool", control_type="Text")
        with contextlib.suppress(_ctypes.COMError):
            pnl_small_tool.child_window(auto_id="_cmdSmallTool_04", control_type="Button").click_input()

    @retry(PayerNotUpdatedException, tries=3, delay=1)
    def select_payer_in_drop_down(self, payer: str) -> None:
        """This method selects the payer in the drop down.

        Args:
            payer (str): payer to be selected
        """
        self.logger.debug(f"Selecting payer in dropdown: {payer}")
        container = self.window.child_window(auto_id="vseContainer", control_type="Text", top_level_only=True)
        pane = container.child_window(title="_cboInput_104", control_type="Pane", top_level_only=True)
        combo_box = pane.child_window(auto_id="mcbo", control_type="ComboBox", top_level_only=True)
        pane_object = pane.wrapper_object()
        options = pane_object.descendants(control_type="ListItem")
        for option in options:
            value = option.window_text()
            if payer.lower() in value.lower():
                self.desktop_app.set_text(
                    combo_box.child_window(control_type="Edit", top_level_only=True, found_index=0), value
                )
                break
        nextgen_payer = combo_box.child_window(auto_id="[Editor] Edit Area", control_type="Edit").get_value()
        if payer.lower() not in nextgen_payer.lower():
            self.logger.debug(f"Failed to select payer {payer} in dropdown. Retrying...")
            capture_screenshot(f"Failed_to_set_payer_{payer}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise PayerNotUpdatedException(f"Failed to select payer {payer} in dropdown")

    def get_payers_from_dropdown(self) -> list:
        """Get all the Payer element from the dropdown.

        Returns:
            list: List of payers as ListItem
        """
        container = self.window.child_window(auto_id="vseContainer", control_type="Text")
        pane = container.child_window(title="_cboInput_104", control_type="Pane")
        pane_object = pane.wrapper_object()
        return pane_object.descendants(control_type="ListItem")

    def set_text_in_allowed(self, row: ListItemWrapper, allowed_amt: Decimal) -> None:
        """Update the Allowed field for a specific service line."""
        self.logger.debug(f"Setting Allowed value in specific row: {allowed_amt}")
        items = row.children(control_type="Edit")
        allowed_element_name = None
        for item in items:
            window_text = item.window_text()
            if "allowed" in window_text.lower():
                allowed_element_name = window_text
                self.set_text_in_specific_row(row, allowed_element_name, str(allowed_amt))
                self.skipping_payer_aarp_pop_up_exist()
                return

    def set_text_in_specific_row_to_pay_field(self, row: ListItemWrapper, text: str | float) -> None:
        """This method sets the text in a specific row to the pay field.

        Args:
            row (ListItemWrapper): list item wrapper with the row
            text (str): text to be inserted
        """
        self.logger.debug(f"Setting text in Pay field: {text}")
        with contextlib.suppress(_ctypes.COMError):
            str_text = str(convert_to_decimal(text))
            items = row.children(control_type="Edit")
            payment_element_name = None
            for item in items:
                window_text = item.window_text()
                if "pay" in window_text.lower():
                    payment_element_name = window_text
                    self.set_text_in_specific_row(row, payment_element_name, str_text)
                    self.skipping_payer_aarp_pop_up_exist()
                    return
            raise PayFieldNotFoundException("Pay field not found in the row")

    def skipping_payer_aarp_pop_up_exist(self, timeout: int = 1) -> bool:
        """This method checks if the skipping payer AARP pop up exists. If it does, it clicks on the ok button.

        Returns:
            bool: True if the pop up exists, False otherwise
        """
        alert_window = self.desktop_app.dialog.child_window(auto_id="65535", control_type="Text")
        if alert_window.exists(timeout=timeout, retry_interval=0.001):
            with contextlib.suppress(_ctypes.COMError):
                self.desktop_app.dialog.child_window(title="OK", control_type="Button").click()
            self.logger.debug("Clicked on OK button in Payer AARP pop up.")
            return True
        return False

    def get_next_gen_payer(self) -> str:
        """Get NextGen Payer on Payment Entry Window."""
        vse_container = self.window.child_window(auto_id="vseContainer", control_type="Text")
        cbo_input = vse_container.child_window(auto_id="_cboInput_104", control_type="Pane")
        mcbo = cbo_input.child_window(auto_id="mcbo", control_type="ComboBox", found_index=0)
        nextgen_payer = mcbo.child_window(auto_id="[Editor] Edit Area", control_type="Edit").get_value()
        match = re.search(r"^(.*?)\/", nextgen_payer)
        if match:
            return match.group(1)
        self.logger.debug(f"Payer: {nextgen_payer}")
        return nextgen_payer

    def get_deduct_value_from_specific_row(self, row: ListItemWrapper) -> str:
        """Get the value from the "Deduct" field in the row.

        Args:
            row (ListItemWrapper): Will search for the Balance in this line.

        Returns:
            str: The value in the "Deduct" field.
        """
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "deduct" in window_text.lower():
                deduct = row.children(title=window_text, control_type="Edit")[0]
                self.logger.debug(f"Deduct value: {deduct.get_value()}")
                return deduct.get_value()
        raise DeductFieldNotFoundException("Deduct field not found")

    def set_text_in_deduct_field(self, row: ListItemWrapper, deduct_amt: Decimal) -> None:
        """Update the Deduct field for a specific service line."""
        self.logger.debug(f"Setting Deduct value in specific row: {deduct_amt}")
        items = row.descendants(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "deduct" in window_text.lower():
                allowed_element_name = window_text
                self.set_text_in_specific_row(row, allowed_element_name, str(deduct_amt))
                self.skipping_payer_aarp_pop_up_exist()
                return

    def refresh_and_enter_encounter_num_and_trn(self, encounter_num: str, payment_trn: str) -> None:
        """This function closes and reopens the payment.

        Args:
            encounter_num (str): Encounter number
            payment_trn (str): Payment TRN
        """
        self.logger.debug("Refreshing the PaymentEntry window.")
        with contextlib.suppress(_ctypes.COMError):
            self.logger.debug("Clean the PaymentEntry window with ALT+L.")
            self.window.type_keys("%l")
            self.logger.debug(f"Entering encounter number: {encounter_num} in PaymentEntry window.")
            self.enter_text_in_enc_clm_field(encounter_num)
            self.click_close_nextgen_alerts()
            self.click_yes_encounter_in_history_status_pop_up()
            self.enter_text_in_tracking_field(payment_trn)
            self.logger.debug("Payment window cleaned and tracking number entered successfully.")

    def select_pay_code_in_drop_down(self, option_to_select: str) -> None:
        """This method selects the pay code in the drop down.

        Args:
            option_to_select (str): pay code to be selected
        """
        self.logger.debug(f"Selecting payer in dropdown: {option_to_select}")
        container = self.window.child_window(auto_id="vseContainer", control_type="Text")
        pane = container.child_window(title="_cboInput_112", control_type="Pane")
        combo_box = pane.child_window(auto_id="mcbo", control_type="ComboBox")
        pane_object = pane.wrapper_object()
        options = pane_object.descendants(control_type="ListItem")
        for option in options:
            value = option.window_text()
            if option_to_select.lower() in value.lower():
                self.desktop_app.set_text(combo_box.child_window(control_type="Edit", found_index=0), value)
                return

    def select_adj_code_in_drop_down(self, option_to_select: str) -> None:
        """Select the adjustment code from the dropdown.

        Args:
            option_to_select (str): the adjustment code to be selected
        """
        container = self.window.child_window(auto_id="vseContainer", control_type="Text")
        pane = container.child_window(title="_cboInput_113", control_type="Pane")
        combo_box = pane.child_window(auto_id="mcbo", control_type="ComboBox")
        pane_object = pane.wrapper_object()
        options = pane_object.descendants(control_type="ListItem")
        for option in options:
            value = option.window_text()
            if option_to_select.lower() in value.lower():
                self.desktop_app.set_text(combo_box.child_window(control_type="Edit", found_index=0), value)
                return

    def close_payment_entry_window(self) -> None:
        """Click close payment entry window."""
        title_bar = self.window.child_window(control_type="TitleBar")
        title_bar.child_window(title="Close", control_type="Button").click_input()

    def insert_control_number_in_resub(self, control_number: str) -> None:
        """This method inserts the control number in the resubmission field.

        Args:
            control_number (str): _description_
        """
        self.desktop_app.set_text(
            self.window.child_window(title="_txtDataEntry_116", control_type="Edit", top_level_only=True),
            control_number,
        )

    def click_show_all_lines_check_box(self) -> None:
        """This method clicks on the show all lines check box."""
        check_box = self.window.child_window(title="chkShowAll", control_type="CheckBox")
        self.desktop_app.toggle_checkbox(check_box)

    def check_bad_debt(self, timeout: int = 2, window_title: str = "NextGen") -> bool:
        """This method checks if the encounter is pre-listed for bad debt.

        Returns:
            bool: True if the pop up exists, False otherwise
        """
        alert_window = self.desktop_app.dialog.child_window(title=window_title, control_type="Window")

        bad_debt_text = alert_window.child_window(
            title="This encounter is pre-listed for bad debt or in bad debt.  You may not edit any information.",
            control_type="Text",
        )
        if bad_debt_text.exists(timeout=timeout, retry_interval=0.001):
            alert_window.child_window(title="OK", control_type="Button").click_input()
            return True
        return False

    def check_invalid_encounter_pop_up_exist(self, timeout: int = 2, window_title: str = "NextGen") -> bool:
        """This method checks if the invalid encounter pop up exists.

        Args:
            timeout (int, optional): Time to wait for the pop-up to appear. Defaults to 2.

        Returns:
            bool: True if the pop up exists, False otherwise
        """
        alert_window = self.desktop_app.dialog.child_window(title=window_title, control_type="Window")

        invalid_encounter_text_1 = alert_window.child_window(
            title="The Encounter number entered is invalid.", control_type="Text", top_level_only=True
        )
        if invalid_encounter_text_1.exists(timeout=timeout, retry_interval=0.001) or alert_window.child_window(
            title="Invalid encounter number!", control_type="Text"
        ).exists(timeout=1, retry_interval=0.001):
            alert_window.child_window(title="OK", control_type="Button").click()
            return True
        return False

    def get_tracking_date(self) -> str:
        """Get the value of the Date input under the Tracking input.

        Returns:
            str: The Date field value.
        """
        self.logger.debug("Getting Date field value under Tracking input.")
        container = self.desktop_app.dialog.child_window(auto_id="vseContainer", control_type="Text")
        date_input = container.child_window(auto_id="mtxtDate", control_type="Edit")
        date_value = date_input.get_value()
        self.logger.debug(f"Date field value found: {date_value}")
        return date_value

    def get_enc_clm_edit_value(self) -> str:
        """This method gets the value by element name in edit control type.

        Args:
            element_name (str): element name

        Returns:
            str: value
        """
        pane = self.desktop_app.dialog.child_window(auto_id="_cboInput_103", control_type="Pane", top_level_only=True)
        combo_box = pane.child_window(auto_id="mcbo", control_type="ComboBox")
        edit_control = combo_box.child_window(control_type="Edit", found_index=0)
        enc_clm = edit_control.get_value()
        return enc_clm

    def get_resub_value(self) -> str:
        """This method quickly gets the value from the resub field.

        Returns:
            str | None: resub value if found, otherwise None
        """
        edit = self.desktop_app.dialog.child_window(title="PaymentEntry", control_type="Window").child_window(
            auto_id="_txtDataEntry_116", control_type="Edit"
        )
        return str(edit.get_value())

    def payment_entry_window_opened_in_encounter(self, num: str, resub: str) -> bool:
        """Check if Payment Entry is opened for a given encounter number and resub value.

        Args:
            num (str): Encounter number to verify.
            resub (str): Expected resub value.

        Returns:
            bool: True if Payment Entry matches both encounter and resub, else False.
        """
        self.logger.debug(f"Checking if payment entry window is opened for encounter: {num}")
        try:
            enc_clm = self.get_enc_clm_edit_value()
        except (ElementNotFoundError, ElementNotEnabled, TimeoutError):
            self.logger.info("Payment Entry window not opened or encounter field not readable.")
            return False

        if not enc_clm or num not in enc_clm:
            return False

        resub_value = self.get_resub_value()
        if str(resub) != str(resub_value):
            self.logger.debug(f"Resub mismatch or not readable: expected={resub!r}, got={resub_value!r}")
            return False

        self.logger.debug("Payment Entry is opened for the expected encounter and resub.")
        return True

    def delete_allowed_field(self, row: WindowSpecification) -> None:
        """Delete (set to empty) the Allowed field of the given service line."""
        self.logger.debug("Deleting Allowed field (set to empty).")
        row = self.revalidate_service_row(row)
        items = row.children(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "allowed" in window_text.lower():
                element = row.descendants(title=window_text, control_type="Edit")[0]
                element.click_input()
                send_keys("^a{DELETE}")
                if element.get_value() != "":
                    element.click_input()
                    send_keys("^a{DELETE}")
                return
        raise FieldNotFoundException("Allowed field not found in the row")

    def delete_adj_field(self, row: WindowSpecification) -> None:
        """Delete (set to empty) the Adj field of the given service line."""
        self.logger.debug("Deleting Adj field (set to empty).")
        row = self.revalidate_service_row(row)
        items = row.children(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "adj" in window_text.lower():
                element = row.descendants(title=window_text, control_type="Edit")[0]
                element.click_input()
                send_keys("^a{DELETE}")
                if element.get_value() != "":
                    element.click_input()
                    send_keys("^a{DELETE}")
                return
        raise AdjFieldNotFoundException("Adj field not found in the row")

    def delete_pay_field(self, row: WindowSpecification) -> None:
        """Delete (set to empty) the Pay field of the given service line."""
        self.logger.debug("Deleting Pay field (set to empty).")
        row = self.revalidate_service_row(row)
        items = row.children(control_type="Edit")
        for item in items:
            window_text = item.window_text()
            if "pay" in window_text.lower():
                element = row.descendants(title=window_text, control_type="Edit")[0]
                element.click_input()
                send_keys("^a{DELETE}")
                if element.get_value() != "":
                    element.click_input()
                    send_keys("^a{DELETE}")
                return
        raise PayFieldNotFoundException("Pay field not found in the row")
