import pytest

from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.labels.utils import LabelColor, LabelKind
from tests.e2e.conftest import call_database


class TestLabels:
    @staticmethod
    def cleanup(context_prefix):
        delete_command = "DELETE FROM labels WHERE name LIKE'{}%'".format(context_prefix)
        call_database(delete_command)

    def test_create_label__of_kind_project(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        color_name = LabelColor.GREEN
        kind = LabelKind.PROJECT

        label = e2e_client.labels.create(name=name, kind=kind, color_name=color_name)

        assert label.name == name
        assert label.color_name == color_name
        assert label.kind == kind

    def test_create_label__of_kind_dataset(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        color_name = LabelColor.YELLOW
        kind = LabelKind.DATASET

        label = e2e_client.labels.create(name=name, kind=kind, color_name=color_name)

        assert label.name == name
        assert label.color_name == color_name
        assert label.kind == kind

    def test_get_label(self, e2e_client, e2e_label_project):
        label = e2e_client.labels.get(name=e2e_label_project.name, kind=e2e_label_project.kind)
        assert label.name == e2e_label_project.name
        assert label.color_name == e2e_label_project.color_name

    def test_update_label(self, e2e_client, e2e_label_project):
        label = e2e_client.labels.get(name=e2e_label_project.name, kind=e2e_label_project.kind)
        assert label.name == e2e_label_project.name

        label.update(color_name=LabelColor.YELLOW)

        assert label.color_name == LabelColor.YELLOW

    def test_delete_label(self, e2e_client, e2e_label_project):
        label = e2e_client.labels.get(name=e2e_label_project.name, kind=e2e_label_project.kind)
        assert label.name == e2e_label_project.name

        label.delete()
        with pytest.raises(CnvrgArgumentsError):
            e2e_client.labels.get(name=e2e_label_project.name, kind=e2e_label_project.kind).color_name
