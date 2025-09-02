"""COB Module."""

from t_desktop.config import IS_WINDOWS_OS

if IS_WINDOWS_OS:
    from pywinauto.application import WindowSpecification
    from pywinauto.controls.uia_controls import ListItemWrapper
    from pywinauto.keyboard import send_keys
    from pywinauto.uia_element_info import UIAElementInfo
from t_nextgen.nextgen_window import NextGenWindow
from datetime import datetime
import contextlib
import _ctypes
from t_nextgen.ng_pm.windows.models.cob_details import COBDetails
from decimal import Decimal


class COBWindow(NextGenWindow):
    """COB class with methods to interact with COB window."""

    @property
    def window(self) -> WindowSpecification:
        """This function gets the COB window.

        Returns:
            WindowSpecification: The COB Window Control
        """
        return self.desktop_app.dialog.child_window(auto_id="frmCOBInfoEntry", control_type="Window")

    def click_on_the_cob_button(self) -> None:
        """This function clicks on the COB button."""
        self.logger.debug("Clicking on the COB button.")
        self.desktop_app.dialog.child_window(auto_id="PaymentEntry", control_type="Window").type_keys("%b")

    def get_filtered_code(self, rsn_code_element: WindowSpecification) -> str:
        """This function retrieves and filters the code from the rsn_code_element directly.

        Args:
            rsn_code_element (WindowSpecification): RSN Code Window Control

        Returns:
            str: The RSN Code value in lowercase
        """
        rsn_code = rsn_code_element.get_value()
        if rsn_code:
            return rsn_code.strip().lower()
        else:
            raise ValueError("RSN code not found in the element.")

    def type_date(self, cob_window: WindowSpecification, codes: WindowSpecification, date: datetime) -> None:
        """This function types the date in the service row.

        Args:
            cob_window (WindowSpecification): COB Window Control
            codes (WindowSpecification): Codes window control
            date (datetime): The date to be entered

        Returns:
            str: The RSN Code value in lowercase
        """
        self.logger.debug(f"Typing date: {date.strftime('%m%d%Y')}")
        send_keys("{TAB}{TAB}{TAB}")
        (
            cob_window.child_window(auto_id="mtxtDate", control_type="Edit", found_index=0).type_keys(
                date.strftime("%m%d%Y")
            )
        )
        codes.child_window(title="Column4", found_index=0).type_keys("{ENTER}")

    def get_details(self, data_item: ListItemWrapper) -> list:
        """This method gets the data item info.

        Args:
            data_item (ListItemWrapper): DataItem containing a DataGrid

        Returns:
            list: A list of COB Details item
        """
        self.logger.debug("Getting COB details.")
        cob_details_list = []
        children = data_item.children()
        data_grid = next((child for child in children if child.element_info.control_type == "DataGrid"), None)
        if data_grid:
            data_items = data_grid.children(control_type="DataItem")
            self.logger.debug(f"Number of rows in COB Window: {len(data_items)}")
            for data_item in data_items:
                rsn_code_element = next(
                    (child for child in data_item.children() if child.element_info.name == "Column13"),
                    None,
                )
                rsn_code = None
                if rsn_code_element:
                    rsn_code_edit_element = rsn_code_element.descendants(control_type="Edit")[0]
                    rsn_code = rsn_code_edit_element.get_value()
                rsn_element = next(
                    (child for child in data_item.children() if child.element_info.name == "Column16"),
                    None,
                )
                rsn_amt_edit_element = None
                rsn_amt = None
                if rsn_element:
                    rsn_amt_edit_element = rsn_element.descendants(control_type="Edit")[0]
                    rsn_amt_value = rsn_amt_edit_element.get_value()
                    rsn_amt = Decimal(rsn_amt_value)
                cob_details_list.append(
                    COBDetails(
                        rsn_code=rsn_code,
                        rsn_amt=rsn_amt,
                        rsn_amt_element=rsn_amt_edit_element,
                    )
                )
        return cob_details_list

    def type_amount(self, rsn_amt_element: WindowSpecification, amount: Decimal) -> None:
        """Type a new amount in the specified element.

        Args:
            rsn_amt_element (WindowSpecification): The RSN Amount WindowSpecification
            amount (Decimal): The amount to be entered
        """
        self.logger.debug(f"Typing amount: {amount}")
        with contextlib.suppress(_ctypes.COMError):
            rsn_amt_element.click_input()
        amount_value = rsn_amt_element.get_value()

        if amount_value == "0.00":
            self.logger.info(f"Setting amount: {amount}")
            self.desktop_app.set_text(rsn_amt_element, str(amount))
        else:
            self.logger.debug(f"Amount already set: {amount_value}.")

    def set_text_in_adj_date(self, adj_date_element: UIAElementInfo, text: str) -> None:
        """This method sets the text in the adj date field.

        Args:
            adj_date_element (UIAElementInfo): the element
            text (str): text to be inserted
        """
        self.logger.debug(f"Setting text in adj date: {text}")
        self.desktop_app.mouse_click_element(adj_date_element)
        self.desktop_app.mouse_double_click_element(adj_date_element)
        send_keys(text)
        send_keys("{TAB}")

    def get_data_item_info(self, data_item: ListItemWrapper) -> tuple:
        """This method gets the data item info.

        Args:
            data_item (ListItemWrapper): DataItem containing a DataGrid

        Returns:
            tuple: A tuple consisting of data_item_info, adj_date_edit_element, rsn_amt_edit_element
        """
        data_item_info = {}
        children = data_item.children()
        adj_date_edit_element = None
        rsn_amt_edit_element = None
        data_grid = next((child for child in children if child.element_info.control_type == "DataGrid"), None)
        if data_grid:
            first_data_item = data_grid.children(control_type="DataItem")[0]
            data_item_info["name"] = first_data_item.window_text()

            for edit in first_data_item.children(control_type="Edit"):
                data_item_info[edit.window_text()] = edit.get_value()

            adj_date_element = next(
                (child for child in first_data_item.children() if child.element_info.name == "Column4"),
                None,
            )
            rsn_amt_element = next(
                (child for child in first_data_item.children() if child.element_info.name == "Column16"),
                None,
            )

            if adj_date_element:
                adj_date_edit_element = adj_date_element.descendants(control_type="Edit")[0]

            if rsn_amt_element:
                rsn_amt_edit_element = rsn_amt_element.descendants(control_type="Edit")[0]

        cpt4_edit = next((child for child in children if child.element_info.name == "CPT4"), None)
        if cpt4_edit:
            data_item_info["CPT4_value"] = cpt4_edit.get_value()

        return data_item_info, adj_date_edit_element, rsn_amt_edit_element

    def get_cob_service_rows(self) -> WindowSpecification:
        """This method gets all the service rows from the COB window.

        Returns:
            list: List of service rows
        """
        self.logger.debug("Getting COB service rows.")
        pane = self.window.child_window(auto_id="lstPayLedger", control_type="Pane")
        tree_view = pane.child_window(control_type="Tree")
        return tree_view.children(control_type="DataItem")

    def click_ok(self) -> None:
        """This method clicks the OK button."""
        self.logger.debug("Clicking OK button.")
        with contextlib.suppress(_ctypes.COMError):
            self.window.type_keys("%o")
