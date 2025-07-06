import os

import pytest

from tests.e2e.data_owner_e2e.data_owner_files import DataOwnerFiles
from tests.e2e.test_queries import TestQueries


class TestDatasetFiles(DataOwnerFiles):

    def test_put_files_success(self, e2e_dataset, temp_file):
        self.data_owner_put_files(e2e_dataset, temp_file)

    def test_put_unchanged_files_success(self, e2e_dataset, temp_file):
        self.data_owner_put_unchanged_files(e2e_dataset, temp_file)

    def test_put_folder_success(self, e2e_dataset, tmpdir):
        self.data_owner_put_folder(e2e_dataset, tmpdir)

    def test_put_files_override_false_success(self, e2e_dataset, temp_file):
        self.data_owner_put_files_override_false(e2e_dataset, temp_file)

    def test_put_files_override_true_success(self, e2e_dataset, temp_file):
        self.data_owner_put_files_override_true(e2e_dataset, temp_file)

    def test_put_file_abs_path_dir_path_success(self, e2e_dataset, temp_file):
        self.data_owner_put_files_abs_path_dir_path(e2e_dataset, temp_file)

    def test_put_file_dir_path_relative_path_success(self, e2e_dataset, temp_file):
        self.data_owner_put_file_dir_path_relative_path(e2e_dataset, temp_file)

    def test_put_folder_abs_path_dir_path_success(self, e2e_dataset, tmpdir):
        self.data_owner_put_folder_abs_path_dir_path(e2e_dataset, tmpdir)

    def test_put_folder_dir_path_relative_path_success(self, e2e_dataset, tmpdir):
        self.data_owner_put_folder_dir_path_relative_path(e2e_dataset, tmpdir)

    def test_put_empty_folder_dir_path_relative_path_success(self, e2e_dataset, tmpdir):
        self.data_owner_put_folder_dir_path_relative_path(e2e_dataset, tmpdir)

    def test_put_files_force_success(self, e2e_dataset, temp_file, temp_file_second):
        self.data_owner_put_files_force(e2e_dataset, temp_file, temp_file_second)

    def test_list_files_success(self, e2e_dataset, tmpdir):
        self.data_owner_list_files(e2e_dataset, tmpdir)

    def test_list_files_with_names_success(self, e2e_dataset, tmpdir):
        for num_files in [5, 20, 30, 60]:
            self.data_owner_list_files_var(e2e_dataset, tmpdir, num_files)

    def test_list_files_and_folders_success(self, e2e_dataset, tmpdir):
        self.data_owner_list_files_and_folders(e2e_dataset, tmpdir)

    def test_delete_files_success(self, e2e_dataset, temp_file):
        self.data_owner_delete_files(e2e_dataset, temp_file)

    def test_clone_files_success(self, e2e_dataset, tmpdir):
        self.data_owner_clone_files(e2e_dataset, tmpdir)

    def test_clone_with_empty_folder_success(self, e2e_dataset, tmpdir):
        self.data_owner_clone_with_empty_folder(e2e_dataset, tmpdir)

    def test_clone_files_override_success(self, e2e_dataset, tmpdir, temp_file):
        self.data_owner_clone_override(e2e_dataset, tmpdir, temp_file)

    def test_upload_files_success(self, e2e_dataset, tmpdir):
        self.data_owner_upload_files(e2e_dataset, tmpdir)

    def test_upload_unchanged_files_success(self, e2e_dataset, tmpdir):
        self.data_owner_upload_unchanged_files(e2e_dataset, tmpdir)

    def test_upload_files_from_non_cnvrg_fails(self, e2e_dataset, tmpdir):
        self.data_owner_upload_files_from_non_cnvrg(e2e_dataset, tmpdir)

    def test_download_files_success(self, e2e_dataset):
        self.data_owner_download_files(e2e_dataset)

    def test_download_empty_folder_success(self, tmpdir, e2e_dataset):
        self.data_owner_download_empty_folder(e2e_dataset, tmpdir)

    def test_put_files_absolute_path_success(self, tmpdir, e2e_dataset):
        self.data_owner_put_files_absolute_path(tmpdir, e2e_dataset)

    def test_remove_files_absolute_path_success(self, tmpdir, e2e_dataset):
        self.data_owner_remove_files_absolute_path(tmpdir, e2e_dataset)

    def test_remove_folders_through_upload_success(self, e2e_dataset, tmpdir):
        self.data_owner_remove_folders_through_upload(tmpdir, e2e_dataset)

    def test_remove_file_through_upload(self, e2e_dataset, tmpdir):
        self.data_owner_remove_file_through_upload(tmpdir, e2e_dataset)

    def test_list_commits_success(self, e2e_dataset, temp_file):
        self.data_owner_list_commits(e2e_dataset, temp_file)

    def test_access_all_commit_fields_success(self, e2e_dataset, temp_file, second_temp_file):
        self.data_owner_access_all_commit_fields(e2e_dataset, temp_file, second_temp_file)

    def test_remove_folder_locally_through_download_success(self, e2e_dataset, tmpdir):
        self.data_owner_remove_folder_locally_through_download(tmpdir, e2e_dataset)

    def test_remove_file_locally_through_download_success(self, e2e_dataset, tmpdir):
        self.data_owner_remove_file_locally_through_download(tmpdir, e2e_dataset)

    def test_data_owner_nested(self, e2e_dataset, tmpdir):
        self.data_owner_nested(tmpdir, e2e_dataset)

    def test_data_owner_cache(self, e2e_dataset, tmpdir):
        self.data_owner_cache(tmpdir, e2e_dataset)

    def test_data_owner_verify_cnvrg_files_exists_success(self, e2e_dataset, tmpdir):
        self.data_owner_verify_cnvrg_files_exists(e2e_dataset, tmpdir)

    def test_sync_not_implemented(self, e2e_dataset):
        with pytest.raises(NotImplementedError):
            e2e_dataset.sync()

    def test_clone_txt_files_using_query_success(self, e2e_dataset, tmpdir):
        # Inflate dataset with files. Half of the files will have a .txt suffix and will be downloaded using query
        num_of_files = 100  # Must be even
        os.chdir(tmpdir.strpath)
        test_dir_name = "test_directory"
        os.mkdir(test_dir_name)
        for i in range(num_of_files):
            filename = "file_{}".format(i)
            if i % 2 == 0:
                filename = filename + ".txt"
            with open(os.path.join(test_dir_name, filename), "w") as f:
                f.write(str(i))

        files_to_upload = "{}/*".format(test_dir_name)
        e2e_dataset.put_files(paths=[files_to_upload])

        # Create query and clone
        query = TestQueries.create_query(e2e_dataset, "txt-query", "*txt")
        e2e_dataset.clone(query_slug=query.slug)

        # Assertions
        assert len(os.listdir(os.path.join(e2e_dataset.slug, test_dir_name))) == num_of_files / 2

    def test_clone_empty_folder_using_query_success(self, e2e_dataset, tmpdir):
        # Create some files and an empty directory
        num_of_files = 25
        test_dir_name = "test_directory"
        empty_folder_name = "im_empty"
        full_folder_name = "im_full"

        os.chdir(tmpdir.strpath)
        os.mkdir(test_dir_name)
        os.mkdir(os.path.join(test_dir_name, empty_folder_name))
        os.mkdir(os.path.join(test_dir_name, full_folder_name))

        for i in range(num_of_files):
            filename = "file_{}".format(i)
            with open(os.path.join(test_dir_name, filename), "w") as f:
                f.write(str(i))

        for i in range(num_of_files):
            filename = "file_{}".format(i)
            with open(os.path.join(test_dir_name, full_folder_name, filename), "w") as f:
                f.write(str(i))

        files_to_upload = "{}/*".format(test_dir_name)
        e2e_dataset.put_files(paths=[files_to_upload])

        # Create query and clone
        query = TestQueries.create_query(e2e_dataset, "empty-query", "*{}/".format(empty_folder_name))
        e2e_dataset.clone(query_slug=query.slug)

        # Assertions
        cloned_test_dir_path = os.path.join(e2e_dataset.slug, test_dir_name)
        files = os.listdir(cloned_test_dir_path)
        count_folders = 0
        count_files = 0

        for file in files:
            if os.path.isdir(os.path.join(cloned_test_dir_path, file)):
                count_folders += 1
            else:
                count_files += 1

        assert count_folders == 1
        assert count_files == 0
        assert os.path.isdir(os.path.join(cloned_test_dir_path, empty_folder_name))

    def test_clone_files_using_folder_query_success(self, e2e_dataset, tmpdir):
        # Create some files and an empty directory
        num_of_files = 150
        test_dir_name = "test_directory"
        empty_folder_name = "im_empty"
        full_folder_name = "im_full"

        os.chdir(tmpdir.strpath)
        os.mkdir(test_dir_name)
        os.mkdir(os.path.join(test_dir_name, empty_folder_name))
        os.mkdir(os.path.join(test_dir_name, full_folder_name))

        for i in range(num_of_files):
            filename = "file_{}".format(i)
            with open(os.path.join(test_dir_name, filename), "w") as f:
                f.write(str(i))

        for i in range(num_of_files):
            filename = "file_{}".format(i)
            with open(os.path.join(test_dir_name, full_folder_name, filename), "w") as f:
                f.write(str(i))

        files_to_upload = "{}/*".format(test_dir_name)
        e2e_dataset.put_files(paths=[files_to_upload])

        # Create query and clone
        query = TestQueries.create_query(e2e_dataset, "full-query", "*{}*".format(full_folder_name))
        e2e_dataset.clone(query_slug=query.slug)

        # Assertions
        cloned_test_dir_path = os.path.join(e2e_dataset.slug, test_dir_name)

        assert os.path.isdir(os.path.join(cloned_test_dir_path, full_folder_name))
        assert not os.path.exists(os.path.join(cloned_test_dir_path, empty_folder_name))
        assert len(list(os.listdir(os.path.join(cloned_test_dir_path, full_folder_name)))) == num_of_files
