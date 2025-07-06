from tests.e2e.conftest import call_database


class DataOwnerLabels:
    @staticmethod
    def cleanup(context_prefix):
        delete_command = "DELETE FROM labels WHERE name LIKE'{}%'".format(context_prefix)
        call_database(delete_command)

    def data_owner_list_labels(self, e2e_data_owner, e2e_label):
        e2e_data_owner.labels.add(e2e_label)

        label = next(e2e_data_owner.labels.list())
        assert label.name == e2e_label.name
        assert label.color_name == e2e_label.color_name

    def data_owner_add_labels(self, e2e_data_owner, e2e_label):
        e2e_data_owner.labels.add(e2e_label)
        label = next(e2e_data_owner.labels.list())
        assert label.name == e2e_label.name
        assert label.color_name == e2e_label.color_name

    def data_owner_remove_labels(self, e2e_data_owner, e2e_label):
        e2e_data_owner.labels.add(e2e_label)
        label = next(e2e_data_owner.labels.list())
        assert label.name == e2e_label.name

        e2e_data_owner.labels.remove()

        labels = list(e2e_data_owner.labels.list())
        assert len(labels) == 0
