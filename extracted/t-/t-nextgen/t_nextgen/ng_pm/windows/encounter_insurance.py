"""EncounterInsurance module."""
import contextlib
from t_desktop.config import IS_WINDOWS_OS

if IS_WINDOWS_OS:
    from pywinauto.application import WindowSpecification
    from pywinauto.controls.uia_controls import ListItemWrapper
    from pywinauto.timings import TimeoutError

from typing import Any
import _ctypes
from retry import retry

from t_nextgen.nextgen_window import NextGenWindow
from t_nextgen.ng_pm.windows.models.insurance_listing import InsuranceListing


class EncounterInsuranceWindow(NextGenWindow):
    """EncounterInsurance class with methods to interact with encounter insurance window."""

    @property
    def window(self):
        """Get Encounter Insurance Window."""
        return self.desktop_app.dialog.child_window(title="frmEncounterPayer", control_type="Window")

    def _get_tree_view_from_insurance_listing(self) -> WindowSpecification:
        """Get tree view of insurance listing from Encounter Insurance Selection Window.

        Returns:
            WindowSpecification: It contains the nested elements that have insurance listing data
        """
        pane = self.window.child_window(title="lstRelations", control_type="Pane")
        return pane.child_window(control_type="Tree")

    def get_insurance_listings_from_encounter_insurance_selection_window(self) -> list[InsuranceListing]:
        """Build Insurance Listing object from insurance listings present in encounter insurance selection window.

        Returns:
            List[InsuranceListing]: A list of InsuranceListing objects
        """
        tree_view = self._get_tree_view_from_insurance_listing()
        data_items = tree_view.children(control_type="DataItem")
        insurance_listings = []
        for item in data_items:
            data_grids = item.children(control_type="DataGrid")
            for grid in data_grids:
                payers = grid.children(control_type="DataItem")
                for curr_payer in payers:
                    curr_insurance_listing = InsuranceListing()
                    curr_cols = curr_payer.children(control_type="Edit")
                    for col in curr_cols:
                        if col.window_text() == "Column1":
                            payer = col.get_value()
                            curr_insurance_listing.payer_row = col
                            curr_insurance_listing.payer = payer
                        elif col.window_text() == "Column3":
                            policy_number = col.get_value()
                            curr_insurance_listing.policy_number = policy_number
                    insurance_listings.append(curr_insurance_listing)
        self.logger.debug(f"Insurance List: {insurance_listings}")
        return insurance_listings

    def select_payer_row_in_insurance_listing(self, payer_row: ListItemWrapper) -> None:
        """Click the payer row from insurance listing in encounter insurance selection window.

        Args:
            payer_row (ListItemWrapper): The payer row to be clicked
        """
        self.logger.debug("Selecting payer row in insurance listing")
        payer_row.type_keys("{DOWN}")
        with contextlib.suppress(_ctypes.COMError):
            payer_row.click_input()

    def _get_tree_view_from_selected_insurance(self) -> WindowSpecification:
        """Get tree view of selected insurance from Encounter Insurance Selection Window.

        Returns:
            WindowSpecification: It contains the nested elements that have selected insurance data
        """
        pane = self.window.child_window(title="lstPayers", control_type="Pane")
        return pane.child_window(control_type="Tree")

    def get_payers_from_selected_insurance(self) -> list[str]:
        """Get Payers from selected insurance in encounter insurance selection window.

        Returns:
            List[str]: List of Payer Names
        """
        tree_view = self._get_tree_view_from_selected_insurance()
        data_items = tree_view.children(control_type="DataItem")
        payers = []
        for item in data_items:
            payers.append(item.window_text())
        self.logger.debug(f"Payers from selected insurance: {payers}")
        return payers

    def click_right_arrow_in_encounter_insurance_selection_window(self) -> None:
        """Click right arrow in Encounter Insurance Selection Window."""
        with contextlib.suppress(_ctypes.COMError):
            self.desktop_app.dialog.child_window(title="cmdAdd", control_type="Button").click_input()

    def click_ok_in_encounter_insurance_selection_window(self) -> None:
        """Click ok in Encounter Insurance Selection Window."""
        self.logger.debug("Clicking ok in Encounter Insurance Selection Window")
        with contextlib.suppress(_ctypes.COMError):
            self.desktop_app.dialog.child_window(title="cmdOk", control_type="Button").click_input()

    def click_ok_encounter_insurance_selection_window_pop_up(self) -> None:
        """Click ok in Encounter Insurance Selection Window pop-up."""
        self.logger.debug("Clicking ok in Encounter Insurance Selection Window pop-up")
        if self.desktop_app.dialog.child_window(title="OK", control_type="Button").exists(timeout=2):
            with contextlib.suppress(_ctypes.COMError):
                self.desktop_app.dialog.child_window(title="OK", control_type="Button").click_input()

    def get_insurance_maintenance_window(self) -> WindowSpecification:
        """Get Insurance Maintenance Window.

        Returns:
            WindowSpecification: The Insurance Maintenance Window
        """
        insurance_window = self.desktop_app.dialog.child_window(title="frmAMIns", control_type="Window")
        if insurance_window.exists(timeout=2):
            return insurance_window

    def enter_co_pay(self, insurance_window: WindowSpecification, co_pay_amount: int) -> None:
        """Enter co-pay information in Insurance Maintenance Window.

        Args:
            insurance_window (WindowSpecification): The Insurance Maintenance Window
            co_pay_amount (int): The co-pay amount to be set
        """
        self.logger.debug(f"Entering co-pay amount: {co_pay_amount}")
        self.desktop_app.set_text(
            insurance_window.child_window(title="txtEncounterCopayAmt", control_type="Edit"), co_pay_amount
        )

    def click_ok(self, insurance_window: WindowSpecification) -> None:
        """Click ok in Insurance Maintenance Window.

        Args:
            insurance_window (WindowSpecification): The insurance maintenance window
        """
        self.logger.debug("Clicking OK in Insurance Maintenance Window")
        with contextlib.suppress(_ctypes.COMError):
            insurance_window.child_window(title="cmdOK", control_type="Button").click_input()

    @retry(tries=3, delay=3)
    def click_close_nextgen_alerts(self, title: str = "Edits") -> None:
        """Click close button on NextGen Alerts.

        Args:
            title (str): The title of the NextGen Alerts window. Defaults to "Edits".
        """
        self.logger.debug("Clicking close on NextGen Alerts")
        alert = self.desktop_app.dialog.child_window(title=title, control_type="Window")
        if alert.exists(timeout=2, retry_interval=0.001):
            with contextlib.suppress(_ctypes.COMError):
                alert.child_window(title="Close", control_type="Button").click()
                alert.wait_not("visible", timeout=5)

    def attach_unattached_payer(self, listing: InsuranceListing) -> None:
        """Handles the process of attaching an unattached payer to the insurance listing.

        Args:
            listing (InsuranceListing): The insurance listing containing the payer information.
        """
        self.logger.debug("Attaching unattached payer")
        self.select_payer_row_in_insurance_listing(listing.payer_row)
        self.click_right_arrow_in_encounter_insurance_selection_window()
        self.click_ok_in_encounter_insurance_selection_window()
        self.click_ok_encounter_insurance_selection_window_pop_up()

        insurance_window = self.get_insurance_maintenance_window()
        if insurance_window:
            self.logger.info("Insurance maintenance window opened")
            insurance_window.set_focus()
            self.enter_co_pay(insurance_window, 0)
            self.click_ok(insurance_window)
            self.click_close_nextgen_alerts()

        self.click_close_nextgen_alerts_encounter_insurance_selection_window()

    def click_close_nextgen_alerts_encounter_insurance_selection_window(self) -> None:
        """Click close button on NextGen Alerts."""
        self.logger.debug("Clicking close on NextGen Encounter Insurance Selection Alerts")
        alert = self.desktop_app.dialog.child_window(
            title="NextGen Encounter Insurance Selection Alerts", control_type="Window"
        )
        if alert.exists(timeout=2, retry_interval=0.001):
            alert.set_focus()
            with contextlib.suppress(_ctypes.COMError):
                alert.child_window(title="Close", control_type="Button").click()

    def get_payer_list(self) -> list[Any]:
        """Retrieves the payer list from the Encounter Insurance window."""
        payers = self.window.child_window(auto_id="lstRelations", control_type="Pane").child_window(
            title="Patient", control_type="DataItem"
        )

        options = payers.descendants(control_type="DataItem")
        self.logger.debug(f"Payers options list: {options}")
        return options

    @retry(exceptions=TimeoutError, tries=3, delay=1)
    def click_cancel_insurance_window(self) -> None:
        """Clicks the Cancel button in the Encounter Insurance window."""
        self.logger.debug("Clicking Cancel in Encounter Insurance window")
        with contextlib.suppress(_ctypes.COMError):
            self.window.child_window(auto_id="cmdCancel", control_type="Button").click_input()
            self.window.wait_not("visible", timeout=5, retry_interval=0.001)
