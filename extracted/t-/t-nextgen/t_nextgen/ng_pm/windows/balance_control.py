import contextlib

import _ctypes

from t_nextgen.nextgen_window import NextGenWindow


class BalanceControlWindow(NextGenWindow):
    """Balance Control Class with methods to interact with balance control window."""

    @property
    def window(self):
        """Get Balance Control Window."""
        return self.desktop_app.dialog.child_window(title="BalanceControl", control_type="Window")

    def get_insurance_listing_rows(self) -> list[dict]:
        """Get Insurance Listing Rows.

        Returns:
            list[dict]: Insurance Listing Rows. Dict with keys Insurance, Insured, Policy Nbr, CoPay, Deductible
        """
        insurance_listing_rows = []
        pane = self.window.child_window(title="lstInsPatBal", control_type="Pane")
        tree_view = pane.child_window(control_type="Tree")
        data_items = tree_view.children(control_type="DataItem")
        for item in data_items:
            row_data = {}
            cells = item.children(control_type="Edit")
            for cell in cells:
                row_data[cell.window_text()] = cell.get_value()
            insurance_listing_rows.append(row_data)
        return insurance_listing_rows

    def click_cancel_balance_control_window(self) -> None:
        """Clicks the Cancel button in the Balance Control window."""
        self.logger.debug("Clicking Cancel in BalanceControl window")
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(auto_id="cmdCancel", control_type="Button").click_input()
