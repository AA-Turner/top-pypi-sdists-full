import os
import shutil
import pytest

from os import path
from tests.e2e.conftest import call_database

from cnvrgv2.errors import CnvrgHttpError
from cnvrgv2.modules.dataset import Dataset


class TestDatasets:

    @staticmethod
    def cleanup(context_prefix):
        delete_user_command = "DELETE FROM datasets WHERE slug LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    def test_create(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        model = e2e_client.datasets.create(name=name)
        assert type(model) == Dataset
        assert model.slug == name

    def test_get(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        e2e_client.datasets.create(name=name)

        model = e2e_client.datasets.get(slug=name)
        assert type(model) == Dataset
        assert model.slug == name
        assert model.title == name

    def test_get_non_existent(self, class_context, e2e_client):
        name = class_context.generate_name(5)

        model = e2e_client.datasets.get(slug=name)
        assert type(model) == Dataset

        with pytest.raises(CnvrgHttpError) as exception_info:
            model.title

        assert "found" in str(exception_info.value)

    def test_delete(self, class_context, e2e_client):
        name = class_context.generate_name(5)
        e2e_client.datasets.create(name=name)

        model = e2e_client.datasets.get(slug=name)
        assert model.title == name

        model.delete()

        model = e2e_client.datasets.get(slug=name)
        with pytest.raises(CnvrgHttpError) as exception_info:
            model.title

        assert "found" in str(exception_info.value)

    def test_delete_non_existent(self, class_context, e2e_client):
        name = class_context.generate_name(5)

        model = e2e_client.datasets.get(slug=name)
        with pytest.raises(CnvrgHttpError) as exception_info:
            model.delete()

        assert "found" in str(exception_info.value)

    def test_list(self, class_context, e2e_client):
        # Clean the db before testing list
        TestDatasets.cleanup(class_context.prefix)

        name_base = class_context.generate_name(5)
        for i in range(40):
            name = "{}{}".format(name_base, i)
            e2e_client.datasets.create(name=name)

        # Check descending order works
        idx = 39
        models = e2e_client.datasets.list()
        for model in models:
            assert model.slug == "{}{}".format(name_base, idx)
            idx -= 1

        # Check ascending order works
        idx = 0
        models = e2e_client.datasets.list(sort="id")
        for model in models:
            assert model.slug == "{}{}".format(name_base, idx)
            idx += 1

    def test_search(self, class_context, e2e_client):
        # Clean the db before testing list
        TestDatasets.cleanup(class_context.prefix)

        name_base = class_context.generate_name(5)
        search_slugs = []

        for i in range(5):
            name = "{}{}".format(name_base, i)
            e2e_client.datasets.create(name=name)

        models = e2e_client.datasets.list()
        for model in models:
            search_slugs.append(model.slug)

        for slug in search_slugs:
            datasets = e2e_client.datasets.search(slug)
            for dataset in datasets:
                assert dataset.slug == slug

    def test_clone_success(self, random_name, e2e_dataset):
        try:
            # Arrange
            filename = random_name(5)
            expected_output_dir = path.join(e2e_dataset.title)
            expected_output_file = path.join(expected_output_dir, filename)
            open(filename, 'w')
            e2e_dataset.put_files([filename], message="test dataset files")

            e2e_dataset.clone()
            assert path.exists(expected_output_file)
        finally:
            # cleanup
            if path.exists(filename):
                os.remove(filename)
            if path.exists(expected_output_dir):
                shutil.rmtree(expected_output_dir)
