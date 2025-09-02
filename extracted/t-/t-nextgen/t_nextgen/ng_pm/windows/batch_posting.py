"""Module for Batch Posting Window."""
import re
import time
import contextlib
from decimal import Decimal

import _ctypes
from typing import Optional
from retry import retry
from t_desktop.config import IS_WINDOWS_OS
from t_desktop.utils.capture_screenshot import capture_screenshot

if IS_WINDOWS_OS:
    from pywinauto.keyboard import send_keys
    from pywinauto.controls.uia_controls import ListItemWrapper
    from pywinauto.application import WindowSpecification
    from pywinauto.findwindows import ElementNotFoundError
    from pywinauto.timings import TimeoutError
from t_desktop.decorators import retry_if_pywin_error
from t_nextgen.nextgen_window import NextGenWindow
from t_nextgen.constants import CONST
from t_nextgen.exceptions import (
    NoMatchingBatchDescriptionException,
    NextGenDuplicateImportException,
    BatchFromBarNotFound,
)

from t_nextgen.ng_pm.windows.models.batch_posting_row import BatchPostingRow


class BatchPostingWindow(NextGenWindow):
    """Batch Posting Class with methods to interact with batch posting window."""

    @property
    def window(self):
        """Return the AMBatches window element."""
        self.desktop_app.dialog.child_window(auto_id="NGEPMBatchLookup", control_type="Window").wait("visible", 5)
        return self.desktop_app.dialog.child_window(auto_id="NGEPMBatchLookup", control_type="Window")

    @property
    def batch_posting_window(self):
        """Return the BatchPosting window element."""
        return self.desktop_app.dialog.child_window(title="BatchPosting", control_type="Window")

    @retry(tries=3, delay=2)
    def click_batch_icon_from_bar(self, practice_name: str) -> None:
        """Clicks the Batch Posting button from the menu bar."""
        try:
            self.logger.debug("Clicking on the batch icon from the bar.")
            batch_icon = self.desktop_app.dialog.child_window(auto_id="cmdToolPosting")
            batch_icon.click()
            self.desktop_app.safe_wait({"auto_id": "Data Area", "control_type": "Custom", "found_index": 0})
        except _ctypes.COMError:
            pass
        except (ElementNotFoundError, TimeoutError, RuntimeError):
            if self.desktop_app.deal_with_unhandled_exception_popup(f"NextGen - {practice_name}"):
                raise RuntimeError("Unhandled Exception popup appeared")
            raise BatchFromBarNotFound("Element with auto_id: cmdToolPosting, not found")

    def post_batch(self, row: ListItemWrapper, post_the_batch: bool = True) -> bool:
        """Function for Posts the batch.

        Post a batch by right-clicking the given row and selecting the 'Post' option
        from the context menu, if the button is enabled.

        Args:
            row (ListItemWrapper): The UI element representing the batch row to be posted.
            post_the_batch (bool): If True, the batch will be posted. Defaults to True.
        """
        self.logger.debug("Posting the batch in NextGen.")
        if not post_the_batch:
            self.logger.warning("Post the batch is set to False, not clicking the button. Returning fake True.")
            return True
        self.maximize_batch_window()
        row.click_input(button="right")
        button = self.desktop_app.dialog.child_window(title_re="Post", control_type="MenuItem")
        if button.is_enabled():
            button.click_input()
            self.desktop_app.close_modal(buttons_to_try=["OK"])
            return True
        else:
            self.logger.warning("Button disabled unable to post the batch.")
            return False

    def click_batch_from_window_menu_if_exist(self) -> bool:
        """This method clicks on the batch from the window menu.

        Returns:
            bool: True if the window menu is found, False otherwise
        """
        windows_menu = self.desktop_app.dialog.child_window(title="Window", control_type="MenuItem")
        windows_menu.select()
        try:
            windows_menu.child_window(title="1 Batch Posting", control_type="MenuItem").select()
            self.logger.debug("Clicked on the batch from the window menu")
            return True
        except _ctypes.COMError:
            return True
        except ElementNotFoundError:
            return False

    def _deal_with_no_batch_found_popup(self) -> None | NoMatchingBatchDescriptionException:
        modal = self.desktop_app.dialog.child_window(title="NextGen", control_type="Window")
        if modal.exists(timeout=2, retry_interval=0.001):
            self.logger.debug("No batch found. Closing popup")
            send_keys("{ENTER}")
            send_keys("%C")
            raise NoMatchingBatchDescriptionException(CONST.BATCH_DESCRIPTION_NOT_FOUND)
        return None

    def _set_amount_field_in_batch_lookup(self, search_criteria_window: WindowSpecification, amount: Decimal) -> None:
        self.logger.debug(f"Setting amount field in batch lookup to {amount}")
        amount_field = search_criteria_window.child_window(auto_id="txtAmount", control_type="Edit")
        self.desktop_app.set_text(amount_field, amount)

    def find_batch(
        self, description: str, amount: Optional[Decimal] = None, fill_amount: bool = False
    ) -> ListItemWrapper:
        """Find a batch in the Batch Posting window.

        Args:
            description (str): The description of the batch to find.
            amount (Optional[Decimal]): The amount of the batch to find.
            fill_amount (Optional[bool]): Whether to fill the amount field before searching.
        """
        batch_row = self.run_batch_lookup(description, amount, fill_amount)
        return batch_row.row_element

    @retry(TimeoutError, tries=3, delay=1)
    def run_batch_lookup(self, trn: str, amount: Optional[Decimal], fill_amount: bool = False) -> BatchPostingRow:
        """Performs a batch lookup based on the provided criteria.

        Args:
            trn (str): The batch description to search for.
            amount (Decimal): The amount associated with the batch, used to filter the results.
            fill_amount (bool): If True, fills in the amount field in the search interface before performing the search.
                                Default is False.

        Returns:
            BatchPositngRow: Returns BatchPostingRow object or raises an exception if row not found

        Raises:
            NoMatchingBatchDescriptionException: If no matching batch is found.
            NextGenDuplicateImportException: If more than one matching batch is found.
        """
        self.logger.info(f"Running batch lookup: trn={trn}, amount={amount}")
        self.click_menu_icon("a")
        search_criteria_window = self.window.child_window(auto_id="grpSearchCriteria", control_type="Group")
        if fill_amount:
            self._set_amount_field_in_batch_lookup(search_criteria_window, amount)
        description_field = search_criteria_window.child_window(auto_id="txtDesc", control_type="Edit")
        self.desktop_app.set_text(description_field, trn)
        send_keys("%F")

        self._deal_with_no_batch_found_popup()

        tree_view = self.window.child_window(auto_id="ColScrollRegion: 0, RowScrollRegion: 0", control_type="Tree")

        filtered_rows = self.get_batch_posting_rows(tree_view)
        if filtered_rows is None:
            send_keys("%C")
            self.logger.debug("No matching batch description found")
            raise NoMatchingBatchDescriptionException(CONST.BATCH_DESCRIPTION_NOT_FOUND)

        rows = self._filter_batch_posting_rows(filtered_rows, trn, amount)
        rows_count = len(rows)
        if rows_count == 1:
            row: BatchPostingRow = rows[0]
            if not row.visible:
                self.desktop_app.click_down_n_times(row.index)
                row.visible = True
            with contextlib.suppress(_ctypes.COMError):
                row.edit_wrapper.click_input()
            self.logger.info("Batch row found")
            return row
        elif rows_count == 0:
            send_keys("%C")
            raise NoMatchingBatchDescriptionException(CONST.BATCH_DESCRIPTION_NOT_FOUND)
        else:
            send_keys("%C")
            self.logger.debug("More than one batch with the same description was found")
            capture_screenshot(file_name=f"{trn}_duplicated_batch.png")
            raise NextGenDuplicateImportException("More than one batch with the same description was found")

    def click_menu_icon(self, key: str) -> None:
        """Clicks the menu icon button in the 'Batch Posting' window.

        Args:
            batch_window (WindowSpecification): The 'Batch Posting' window object.
            key (str): The key to send after clicking the button.
        """
        self.logger.debug("Clicking the menu icon button in the 'Batch Posting' window")
        self.batch_window = self._get_batch_window()
        cmd_drill_button = self.batch_window.child_window(title="cmdDrill", control_type="Button")
        cmd_drill_button.click_input()
        time.sleep(1)

        send_keys(key)

    @retry(tries=3, delay=1)
    def _get_batch_window(self) -> WindowSpecification:
        """Retrieves the 'Batch Posting' window.

        Returns:
            WindowSpecification: The 'Batch Posting' window object.
        """
        self.logger.debug("Getting the 'Batch Posting' window")
        self.desktop_app.wait_until_element_visible(control_type="Pane", title="lstListing", timeout=1)
        batch_window = self.desktop_app.dialog.child_window(title="BatchPosting", control_type="Window")
        return batch_window

    def get_batch_posting_rows(self, rows_list: ListItemWrapper) -> list[BatchPostingRow]:
        """The function retrieves about the Batch Posting rows.

        :param rows_list: The `rows_list` parameter is the object representing the tree view control in
        the user interface. It is used to access the elements and descendants of the tree view
        :return: a list of filtered rows consisting of the BatchPostingRow object
        """
        filtered_rows = []
        all_descendants = rows_list.descendants()

        index = 0
        for element in all_descendants:
            if "DataItem" in element.element_info.control_type:
                index += 1
                data_item_descendants = element.descendants(control_type="Edit")
                batch_posting_row = BatchPostingRow(
                    text=element.element_info.name,
                    visible=element.is_visible(),
                    index=index,
                    row_element=element,
                )
                for descendant in data_item_descendants:
                    if "Description" in descendant.element_info.name:
                        batch_posting_row.description = descendant.get_value()
                        batch_posting_row.edit_wrapper = descendant
                    if "Members" in descendant.element_info.name:
                        batch_posting_row.member_count = descendant.get_value()
                    if batch_posting_row.member_count and batch_posting_row.description:
                        break
                filtered_rows.append(batch_posting_row)
        return filtered_rows

    def _filter_batch_posting_rows(
        self, batch_posting_rows: list[BatchPostingRow], description: str, amt: Decimal
    ) -> list[BatchPostingRow]:
        """Filter Batch Posting rows based on description and amount text in BatchPostingRow.description.

        Args:
            dicts (list[dict]): A list of dictionaries to search through.
            description (str): The description to match within each dictionary.
            amt (Decimal): Amount from the payment object

        Returns:
            list[BatchPostingRow]: A list of BatchPostingRow where the description matches the given description.
        """
        result = []
        for row in batch_posting_rows:
            if description not in row.description:
                continue
            amt_extracted = self._extract_amt_from_description(row.description)
            if amt_extracted is None:
                self.logger.info("Unable to determine amount value from batch description")
            elif amt == Decimal(amt_extracted):
                result.append(row)
        return result

    def _extract_amt_from_description(self, description: str) -> None | str:
        """Extract amount from batch description in nextgen.

        Args:
            description (str): The description from which we want the amount.

        Returns
            (str): The amount extracted.
        """
        # Find the amount with optional commas and dollar sign
        match = re.search(r"-?\$\s?(-?[\d,]+\.?\d*)", description)
        if match:
            # Extract the numeric part and replace commas
            amount_str = match.group(1).replace(",", "")
            self.logger.debug(f"Extracted amount from description: {amount_str}")
            return amount_str
        return None

    def check_boxes_in_batch_posting(self, current_phase: str) -> None:
        """Toggle the state of three checkboxes in a batch posting dialog.

        Toggles the state of checkboxes with auto_ids "_chkSecure_0", "_chkSecure_1", and "_chkSecure_2"
        in the current dialog.

        Args:
            current_phase: the current phase of the work item
        """
        checkbox_ids = ["_chkSecure_0", "_chkSecure_1", "_chkSecure_2"]
        checkboxes = []
        checkboxes.append(
            self.desktop_app.dialog.child_window(auto_id=checkbox_ids[0], control_type="CheckBox").wait("visible", 10)
        )
        for checkbox_id in checkbox_ids:
            checkboxes.append(self.desktop_app.dialog.child_window(auto_id=checkbox_id, control_type="CheckBox"))

        for checkbox in checkboxes:
            untoggle = False
            if checkbox == "_chkSecure_0" and current_phase == CONST.WORK_ITEM_PHASE.RETRY.value:
                untoggle = True
            if untoggle:
                self.desktop_app.untoggle_checkbox(checkbox)
            else:
                self.desktop_app.toggle_checkbox(checkbox)

    def unselect_checkboxes(self) -> None:
        """Untoggle three checkboxes in a batch posting dialog.

        UnToggles checkboxes with auto_ids "_chkSecure_0", "_chkSecure_1", and "_chkSecure_2"
        in the current dialog.

        """
        checkbox_ids = ["_chkSecure_0", "_chkSecure_1", "_chkSecure_2"]
        checkboxes = []
        self.desktop_app.dialog.child_window(auto_id=checkbox_ids[0], control_type="CheckBox").wait("visible", 5)

        for checkbox_id in checkbox_ids:
            checkboxes.append(self.desktop_app.dialog.child_window(auto_id=checkbox_id, control_type="CheckBox"))

        for checkbox in checkboxes:
            self.desktop_app.untoggle_checkbox(checkbox)

    @retry(tries=3, delay=3)
    def set_focus_in_batch_window(self):
        """This method sets the focus in the batch window."""
        self.logger.debug("Setting focus in the batch window")
        window = self.desktop_app.dialog.child_window(title="BatchPosting", control_type="Window")
        pane = window.child_window(auto_id="lstListing")
        div = pane.child_window(auto_id="Data Area", control_type="Custom", found_index=0)
        tree_view = div.child_window(auto_id="ColScrollRegion: 0, RowScrollRegion: 0")
        self.desktop_app.mouse_click_element(tree_view)

    @retry(tries=3, delay=3)
    def click_ok_quick_batch(self) -> None:
        """The function clicks on the "OK" button in the Quick Batch dialog window."""
        self.logger.debug("Clicking on the OK button in the Quick Batch dialog window")
        ok_button = self.desktop_app.dialog.child_window(title="cmdOK", control_type="Button")
        with contextlib.suppress(_ctypes.COMError):
            ok_button.click()

    @staticmethod
    def click_quick_batch_from_batch_menu(quick_batch_position: int = 2) -> None:
        """The function clicks on the "Quick Batch" option in the batch menu."""
        for _ in range(quick_batch_position):
            send_keys("{DOWN}")
        send_keys("{ENTER}")

    @staticmethod
    def click_new_from_batch_menu(new_batch_item_position: int = 1) -> None:
        """The function clicks on the "New..." option in the batch menu.

        Args:
            new_batch_item_position (int): the position of the "New..." option in the batch menu
        """
        for _ in range(new_batch_item_position):
            send_keys("{DOWN}")
        send_keys("{RIGHT}")

    def maximize_batch_window(self) -> None:
        """This method maximizes the batch window."""
        try:
            if not self.batch_posting_window.was_maximized():
                self.logger.debug("Maximizing the batch window")
                self.batch_posting_window.maximize()
                time.sleep(1)
        except Exception as e:
            self.logger.warning(f"Could not maximize the batch window: {str(e)}")

    def get_batch_row(self, trn: str, amount: str) -> None | BatchPostingRow:
        """This method retrieves the batch row in the batch posting dialog that matches the given description.

        Args:
            description (str): The description to match against the batch posting dialog.
            amount (str): The amount to match against the batch posting dialog.

        Returns:
            None | BatchPostingRow: The batch row that matches the given description.

        Raises:
            NoMatchingBatchDescription: If no matching description is found.
            NextGenDuplicateImportException: If multiple matching descriptions are found.
        """
        div = self.desktop_app.dialog.child_window(auto_id="Data Area", control_type="Custom", found_index=0)
        tree_view = div.child_window(auto_id="ColScrollRegion: 0, RowScrollRegion: 0")
        batch_posting_rows = self.get_batch_posting_rows(tree_view)

        if batch_posting_rows is None:
            send_keys("%C")
            self.logger.debug("No matching batch description found")
            raise NoMatchingBatchDescriptionException(CONST.BATCH_DESCRIPTION_NOT_FOUND)

        rows = self._filter_batch_posting_rows(batch_posting_rows, trn, amount)
        rows_count = len(rows)
        if rows_count == 1:
            row: BatchPostingRow = rows[0]
            if not row.visible:
                self.desktop_app.click_down_n_times(row.index)
                row.visible = True
            with contextlib.suppress(_ctypes.COMError):
                row.edit_wrapper.click_input()
            self.logger.info("Batch row found")
            return row
        elif rows_count == 0:
            send_keys("%C")
            raise NoMatchingBatchDescriptionException(CONST.BATCH_DESCRIPTION_NOT_FOUND)
        else:
            send_keys("%C")
            self.logger.debug("More than one batch with the same description was found")
            raise NextGenDuplicateImportException("More than one batch with the same description was found")

    def close_batch_look_up_window(self) -> None:
        """Click close button in Batch Lookup Window."""
        self.logger.debug("Closing the Batch Lookup window")
        batch_lookup_window = self.desktop_app.dialog.child_window(title="Batch Lookup", control_type="Window")
        batch_lookup_window.set_focus()
        with contextlib.suppress(_ctypes.COMError):
            batch_lookup_window.child_window(title="Close", control_type="Button", found_index=0).click_input()

    @retry_if_pywin_error()  # type: ignore[misc]
    def get_batch_date(self) -> str:
        """This function gets the batch date.

        Returns:
            str: Batch date
        """
        batch_date = (
            self.window.child_window(auto_id="ColScrollRegion: 0, RowScrollRegion: 0")
            .child_window(control_type="DataItem")
            .child_window(title="Date", control_type="Edit")
            .get_value()
        )
        self.logger.debug(f"Batch date: {batch_date}")
        return batch_date

    def get_batch_id(self) -> str:
        """This function gets the batch ID in the batch lookup flow.

        Returns:
            str: Batch ID
        """
        batch_id = (
            self.window.child_window(auto_id="ColScrollRegion: 0, RowScrollRegion: 0")
            .child_window(control_type="DataItem")
            .child_window(title="ID", control_type="Edit")
            .get_value()
        )
        self.logger.debug(f"Batch ID: {batch_id}")
        return batch_id

    def enter_quick_batch_name(self, name: str) -> None:
        """The function enters a Bach name into a text field in the Quick Batch dialog window.

        Args:
            name (str): the name of the batch
        """
        self.logger.debug(f"Entering quick batch name: {name}")
        quick_batch_window = self.desktop_app.dialog.child_window(auto_id="NGEPMQuickBatch", control_type="Window")
        batch_name_field = quick_batch_window.child_window(auto_id="txtDesc", control_type="Edit")
        batch_name_field.wait("visible", 5)
        with contextlib.suppress(_ctypes.COMError):
            batch_name_field.set_edit_text(name)

    @retry_if_pywin_error(3, 3)  # type: ignore[misc]
    def press_l_to_open_ledger_in_dropdown(self) -> None:
        """Press "l" to open the ledger in the opened dropdown."""
        self.logger.debug("Pressing 'l' to open the ledger in the dropdown")
        send_keys("l")
        self.desktop_app.dialog.child_window(title="BatchLedger", control_type="Window").wait("visible", 10)

    def _open_dropdown_for_batch_row(self) -> None:
        """Click on the ledger left button to open the options dropdown for the selected row."""
        self.logger.debug("Opening the options dropdown for the selected row")
        button = self.desktop_app.dialog.child_window(title="cmdDrill", control_type="Button")
        with contextlib.suppress(_ctypes.COMError):
            button.click()
        time.sleep(2)
