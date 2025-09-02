"""Transaction Ledger Module."""
from decimal import Decimal
from t_desktop.config import IS_WINDOWS_OS

from t_nextgen.utils.convert_to_decimal import convert_to_decimal

if IS_WINDOWS_OS:
    from pywinauto.controls.uia_controls import ListItemWrapper
    from pywinauto.application import WindowSpecification
import contextlib
from t_desktop.decorators import retry_if_pywin_error
import _ctypes
from t_nextgen.nextgen_window import NextGenWindow
from t_nextgen.exceptions import SearchEncounterNotFoundException, LockedBatchError, HeaderButtonNotFoundException


class TransactionLedgerWindow(NextGenWindow):
    """TransactionLedger class with methods to interact with transaction ledger window."""

    @property
    def window(self):
        """Return the BatchLedger window element."""
        return self.desktop_app.dialog.child_window(auto_id="BatchLedger", control_type="Window")

    def _get_amount(self, title: str, auto_id: str) -> str:
        """Fetch Billed/Allowed/Payment Amount from Window.

        Args:
            title (str): title of the element
            auto_id (str): auto_id of the element

        Returns:
            str: amount
        """
        amt = self.window.child_window(title=title, auto_id=auto_id, control_type="Edit").get_value()
        return amt.replace("$", "").replace(",", "").strip()

    def get_billed_amount(self) -> str:
        """Fetch Billed Amount.

        Returns:
            str: Billed Amount
        """
        return self._get_amount("Billed", "0")

    def get_allowed_amount(self) -> str:
        """Fetch Allowed Amount.

        Returns:
            str: allowed amount
        """
        return self._get_amount("Allowed", "1")

    def get_payment_amount(self) -> str:
        """Fetch Payment Amount.

        Returns:
            str: payment amount
        """
        return self._get_amount("Payment", "2")

    def get_adjustment_amount(self) -> str:
        """Fetch Adjustment Amount.

        Returns:
            str: adjustment amount
        """
        return self._get_amount("Adjustment", "3")

    @retry_if_pywin_error(retries=3, delay=2)  # type: ignore[misc]
    def click_header_from_menu_and_wait_for_batch_maintanance(self) -> None:
        """Clicks the Header button."""
        self.logger.debug("Clicking on the Header button.")
        header_button = self.window.child_window(title="cmdHeader", control_type="Button")
        if header_button.exists(timeout=2, retry_interval=0.001):
            with contextlib.suppress(_ctypes.COMError):
                self.desktop_app.mouse_click_element(header_button, "left")
        else:
            raise HeaderButtonNotFoundException("Header button not found")

        self.desktop_app.dialog.child_window(title="AMBatches", control_type="Window").wait("visible", 15)

    def filter_rows_by_source_value(self, rows: list[ListItemWrapper], value: str) -> list[dict]:
        """Filters rows based on the source value and ensures 'Billed' is not '0'."""
        filtered_rows = []
        for index, row in enumerate(rows):
            source_value = row.children(title="Source")[0].get_value()
            billed = row.children(title="Billed")[0].get_value()
            if self.is_row_valid(source_value, billed, value):
                filtered_rows.append({"element": row, "index": index})
        return filtered_rows

    def is_row_valid(self, source_value: str, billed: str, value: str) -> bool:
        """Validates whether a row matches the source value and is billed."""
        return source_value == value and billed != "0"

    def double_click_the_row_where_source_is(self, value: str) -> None:
        """This method double clicks on the row where the source is the value provided.

        Args:
            value (str): value to be searched for in the source column

        Returns:
            None
        """
        filtered_rows: list = []
        pane = self.window.child_window(title="lstLedger", control_type="Pane")
        rows = pane.wrapper_object().descendants(control_type="DataItem")
        filtered_rows = self.filter_rows_by_source_value(rows, value)
        if len(filtered_rows) > 0:
            self.logger.debug(f"Search encounter found for source: {value}")
            self.click_row(filtered_rows[0]["element"], filtered_rows[0]["index"], pane)
        else:
            self.logger.debug(f"Search encounter not found for source: {value}")
            raise SearchEncounterNotFoundException

    def click_row(self, row: ListItemWrapper, index: int, pane: WindowSpecification, offset: int = 3) -> None:
        """This method clicks on the transaction ledger row.

        Args:
            row (ListItemWrapper): row to be clicked
            index (int): index of the row
            pane (WindowSpecification): pane element where the row is located
            offset (int): offset to click on the row, default is 3

        Returns:
            None
        """
        self.logger.debug(f"Clicking on the row at index: {index}")
        pane.set_focus()
        self.desktop_app.mouse_click_element(pane, "left")
        self.desktop_app.click_down_n_times(index + offset)
        row.double_click_input()
        modal = self.window.child_window(
            title="Security has been specified for this batch.  This batch of "
            "transactions is only accessible by its specified owner."
        )
        if modal.exists(timeout=1, retry_interval=0.001):
            raise LockedBatchError("Batch locked: Security has been specified for this batch!")
        else:
            self.desktop_app.dialog.child_window(auto_id="PaymentEntry", control_type="Window").wait("visible", 5)

    def get_row_elements(self) -> list[ListItemWrapper]:
        """Get all row elements.

        Returns:
            List[ListItemWrapper]: Represent the row elements
        """
        pane = self.window.child_window(auto_id="lstLedger", control_type="Pane")
        tree_view = pane.child_window(control_type="Tree")
        return tree_view.children(control_type="DataItem")

    def open_the_encounter(
        self,
        source_value: str,
        billed_amt: Decimal,
        tran_code_value: str,
        clm_status: str,
    ) -> None:
        """Double clicks on the row matching source, payment, and tran code.

        Args:
            source_value (str): The source value to match.
            billed_amt (Decimal): The Billed Amt to match.
            tran_code_value (str): The tran code value to match.
            clm_status (str | None): The CLM status to consider for filtering rows.

        Raises:
            SearchEncounterNotFoundException: If no matching row is found.
        """
        self.logger.debug(
            f"Opening the encounter. Source: {source_value}, Billed Amt: {billed_amt}, " f"tran_code: {tran_code_value}"
        )
        pane = self.window.child_window(auto_id="lstLedger", control_type="Pane")
        rows = pane.wrapper_object().descendants(control_type="DataItem")
        for index, row in enumerate(rows):
            try:
                row_source = row.children(title="Source")[0].get_value()
                row_billed = convert_to_decimal(row.children(title="Billed")[0].get_value())
                row_tran_code = row.children(title="Tran Code")[0].get_value()
            except Exception as e:
                self.logger.warning(f"Skipping row due to error: {e}")
                continue
            source_match = row_source == source_value
            billed_match = row_billed == billed_amt
            tran_code_match = tran_code_value in row_tran_code
            billed_match_clm_status = (clm_status == "22" and row_billed < 0) or (clm_status != "22" and row_billed > 0)

            if (source_match and billed_match and tran_code_match) and billed_match_clm_status:
                self.logger.debug(
                    f"Found matching row for source: {source_value}, "
                    f"Billed Amt: {billed_amt}, tran code: {tran_code_value}"
                )
                self.click_row(row, index, pane)
                return

        self.logger.debug(
            f"No matching row found for source: {source_value}, Billed Amt: {billed_amt}, tran code: {tran_code_value},"
            f" Clm Status: {clm_status}"
        )
        raise SearchEncounterNotFoundException
