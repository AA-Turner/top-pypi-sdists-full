"""This module provides a function to delete batches from the database."""
import contextlib
import time

from pywinauto.application import WindowSpecification
import _ctypes

from t_nextgen.ng_pm.core import NextGenPMCore
from t_nextgen.utils.logger import logger


class BatchDeleterCore:
    """Base class for deleting batches from the NextGen PM application."""

    def __init__(
        self,
        next_gen: NextGenPMCore,
    ):
        """Initialize the BatchDeleter object.

        Args:
            next_gen (NextGenPMCore): NextGen PM Core object.
            practice (str): Practice name.
        """
        self.next_gen = next_gen
        self.batches_marked_to_deletion: list[str] = []

    def get_batch_rows(self) -> WindowSpecification:
        """Get the batch rows from the batch posting window."""
        pane = self.next_gen.desktop_app.dialog.child_window(title="lstListing", control_type="Pane")
        return pane.descendants(control_type="DataItem")

    def mark_batch_for_deletion(self, data_item: WindowSpecification, description: str):
        """Mark the batch for deletion.

        Args:
            data_item (WindowSpecification): DataItem object of the batch.
            description (str): Description of the batch.
        """
        logger.info(f"Selecting batch for deletion: {description}")
        check_box = data_item.descendants(control_type="CheckBox")[0]
        self.next_gen.desktop_app.toggle_checkbox(check_box)

    def click_delete_option(self):
        """Click the delete option in the batch posting window."""
        self.next_gen.batch_posting_window.click_menu_icon("d")
        time.sleep(2)
        with contextlib.suppress(_ctypes.COMError):
            self.next_gen.desktop_app.dialog.child_window(title="OK", control_type="Button").click()

    def check_if_all_batches_were_selected_correctly(self):
        """Check if all batches were selected correctly."""
        batch_rows = self.get_batch_rows()
        batch_selected = 0
        for data_item in batch_rows:
            check_box = data_item.descendants(control_type="CheckBox")[0]
            if check_box.get_toggle_state() == 1:
                batch_selected += 1
        if batch_selected == len(self.batches_marked_to_deletion):
            logger.info("All batches were selected correctly for deletion.")
        else:
            logger.warning("Some batches were not selected correctly for deletion.")

    def wait_for_deletion_process_to_finish(self, timeout: int = 300, interval: int = 30) -> None:
        """Waits for the deletion process to finish.

        Args:
            timeout (int): Maximum time to wait for deletion in seconds. Defaults to 300 seconds.
            interval (int): Time interval between checks in seconds. Defaults to 10 seconds.
        """
        logger.info("Waiting for batches to be deleted")
        start_time = time.time()
        while time.time() - start_time < timeout:
            description_list = []
            try:
                found_batch = False
                for data_item in self.get_batch_rows():
                    description = data_item.descendants(title="Description", control_type="Edit")[0].get_value()
                    description_list.append(description)

                #  If one of the batches can't be found in the batch rows, it means the deletion process has ended
                for batch in self.batches_marked_to_deletion:
                    if not any(batch in description for description in description_list):
                        found_batch = False
                        logger.info("Deletion process has ended")
                        break
                if not found_batch:
                    return
                logger.info("Batches still found. Waiting...")
                time.sleep(interval)
            except RuntimeError:
                logger.warning("NextGen app seems to be in a freeze state. Waiting for it to recover.")
                time.sleep(10)
        logger.warning("Timeout reached. Some batches may not have been deleted.")
