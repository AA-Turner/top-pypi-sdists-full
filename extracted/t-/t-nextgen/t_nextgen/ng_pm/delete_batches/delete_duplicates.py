"""This module provides a function to delete batches from the database."""
from collections import Counter
import re


from t_nextgen.ng_pm.core import NextGenPMCore
from t_nextgen.ng_pm.delete_batches.core import BatchDeleterCore
from t_nextgen.utils.logger import logger


class DuplicateBatchDeleter(BatchDeleterCore):
    """Class to delete batches from the NextGen PM application."""

    def __init__(
        self,
        next_gen: NextGenPMCore,
        practice: str,
    ):
        """Initialize the BatchDeleter object.

        Args:
            next_gen (NextGenPMCore): NextGen PM Core object.
            practice (str): Practice name.
        """
        self.next_gen = next_gen
        self.duplicated_batches: list[str] = []
        self.practice = practice
        self.batches_not_secured_to_thoughtful: list[str] = []
        self.number_of_remits = 0
        self.found_batch_to_delete = False
        self.batches_marked_to_deletion: list[str] = []
        self.total_number_of_batches_in_the_practice = 0
        self.batches_not_deleted: list[str] = []
        self.all_batches_secured_to_thoughtful_were_deleted: bool = False

    def check_if_all_batches_were_deleted(self):
        """Check if all batches were deleted."""
        data_items = self.get_batch_rows()
        if self.batches_marked_to_deletion and (
            self.total_number_of_batches_in_the_practice - len(self.batches_not_secured_to_thoughtful)
            == len(data_items)
        ):
            logger.info(f"All batches secured to thoughtful were deleted in {self.practice}")
            self.all_batches_secured_to_thoughtful_were_deleted = True
        else:
            batches_secured_to_thoughtful = [
                batch for batch in self.duplicated_batches if batch not in self.batches_not_secured_to_thoughtful
            ]

            for index, data_item in enumerate(data_items):
                next_gen_description = data_item.descendants(title="Description", control_type="Edit")[0].get_value()
                for description in batches_secured_to_thoughtful:
                    if description in next_gen_description:
                        self.batches_not_deleted.append(description)
                        break
            if self.batches_not_deleted:
                logger.warning(
                    f"Some batches were not deleted in {self.practice}. Batches not deleted: {self.batches_not_deleted}"
                )
                self.all_batches_secured_to_thoughtful_were_deleted = False

    def generate_report(self):
        """Generate a report of the batches that were not deleted."""
        return {
            "practice": self.practice,
            "batches_not_secured_to_thoughtful": self.batches_not_secured_to_thoughtful,
            "duplicated_batches": self.duplicated_batches,
            "number_of_duplicate_batches": len(self.duplicated_batches),
            "number_of_batches_not_secured_to_thoughtful": len(self.batches_not_secured_to_thoughtful),
            "all_batches_secured_to_thoughtful_deleted": self.all_batches_secured_to_thoughtful_were_deleted,
        }

    def delete(self) -> None:
        """Delete the batches."""
        data_items = self.get_batch_rows()
        self.total_number_of_batches_in_the_practice = len(data_items)
        for index, data_item in enumerate(data_items):
            next_gen_description = data_item.descendants(title="Description", control_type="Edit")[0].get_value()
            secured_to = data_item.descendants(title="Secured To", control_type="Edit")[0].get_value()
            for description in self.duplicated_batches:
                if description in next_gen_description:
                    if not data_item.is_visible():
                        self.next_gen.desktop_app.click_down_n_times(index)

                    if "thoughtful" in secured_to.lower() or secured_to.strip() == "":
                        members = data_item.descendants(title="Members", control_type="Edit")[0].get_value()
                        self.number_of_remits += int(members)
                        self.found_batch_to_delete = True
                        self.mark_batch_for_deletion(data_item, description)
                        self.batches_marked_to_deletion.append(description)
                    else:
                        self.batches_not_secured_to_thoughtful.append(description)
                        logger.warning(f"Batch {description} is secured to {secured_to}. Not marking it to delete")
                    break
        if self.found_batch_to_delete:
            self.check_if_all_batches_were_selected_correctly()
            self.click_delete_option()
            self.wait_for_deletion_process_to_finish(timeout=self.number_of_remits * 40, interval=40)
        else:
            logger.info(f"No duplicated batches found to delete in {self.practice}")
        self.check_if_all_batches_were_deleted()

    def delete_duplicate_batches(self) -> dict:
        """Check for duplicate batches in the batch posting window."""
        data_items = self.get_batch_rows()
        pattern = re.compile(r"\b(?=[A-Z0-9]{8,}\b)(?=.*\d)[A-Z0-9]+\b")
        payment_numbers = []
        for data_item in data_items:
            next_gen_description = data_item.descendants(title="Description", control_type="Edit")[0].get_value()
            matches = pattern.findall(next_gen_description)
            payment_numbers.extend(matches)

        # Count occurrences
        counter = Counter(payment_numbers)

        # Filter for duplicates
        duplicates = {num: count for num, count in counter.items() if count > 1}
        for num, count in duplicates.items():
            self.duplicated_batches.append(num)
            logger.info(f"Found duplicate batch: {num} with count: {count}")
        if self.duplicated_batches:
            logger.info(f"Found {len(self.duplicated_batches)} duplicate batches in {self.practice}")
            self.delete()
        else:
            logger.info(f"No duplicate batches found in {self.practice}")
        return self.generate_report()
