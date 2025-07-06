from tests.e2e.conftest import call_database
from tests.e2e.data_owner_e2e.data_owner_labels import DataOwnerLabels


class TestDatasetLabels(DataOwnerLabels):
    @staticmethod
    def cleanup(context_prefix):
        delete_command = "DELETE FROM labels WHERE name LIKE'{}%'".format(context_prefix)
        call_database(delete_command)

    def test_list_labels_of_dataset(self, e2e_dataset, e2e_label_dataset):
        self.data_owner_list_labels(e2e_dataset, e2e_label_dataset)

    def test_add_labels_to_dataset(self, e2e_dataset, e2e_label_dataset):
        self.data_owner_add_labels(e2e_dataset, e2e_label_dataset)

    def test_remove_labels_from_dataset(self, e2e_dataset, e2e_label_dataset):
        self.data_owner_remove_labels(e2e_dataset, e2e_label_dataset)
