from tests.e2e.data_owner_e2e.data_owner_files import DataOwnerFiles


class TestProjectFiles(DataOwnerFiles):

    def test_put_files_success(self, e2e_project, temp_file):
        self.data_owner_put_files(e2e_project, temp_file)

    def test_put_unchanged_files_success(self, e2e_project, temp_file):
        self.data_owner_put_unchanged_files(e2e_project, temp_file)

    def test_put_folder_success(self, e2e_project, tmpdir):
        self.data_owner_put_folder(e2e_project, tmpdir)

    def test_put_files_override_false_success(self, e2e_project, temp_file):
        self.data_owner_put_files_override_false(e2e_project, temp_file)

    def test_put_files_override_true_success(self, e2e_project, temp_file):
        self.data_owner_put_files_override_true(e2e_project, temp_file)

    def test_put_file_abs_path_dir_path_success(self, e2e_project, temp_file):
        self.data_owner_put_files_abs_path_dir_path(e2e_project, temp_file)

    def test_put_file_dir_path_relative_path_success(self, e2e_project, temp_file):
        self.data_owner_put_file_dir_path_relative_path(e2e_project, temp_file)

    def test_put_folder_abs_path_dir_path_success(self, e2e_project, tmpdir):
        self.data_owner_put_folder_abs_path_dir_path(e2e_project, tmpdir)

    def test_put_folder_dir_path_relative_path_success(self, e2e_project, tmpdir):
        self.data_owner_put_folder_dir_path_relative_path(e2e_project, tmpdir)

    def test_put_empty_folder_dir_path_relative_path_success(self, e2e_project, tmpdir):
        self.data_owner_put_empty_folder_dir_path_relative_path(e2e_project, tmpdir)

    def test_put_files_force_success(self, e2e_project, temp_file, temp_file_second):
        self.data_owner_put_files_force(e2e_project, temp_file, temp_file_second)

    def test_list_files_success(self, e2e_project, tmpdir):
        self.data_owner_list_files(e2e_project, tmpdir)

    def test_list_files_with_names_success(self, e2e_project, tmpdir):
        for num_files in [5, 20, 30, 60]:
            self.data_owner_list_files_var(e2e_project, tmpdir, num_files)

    def test_list_files_and_folders_success(self, e2e_project, tmpdir):
        self.data_owner_list_files_and_folders(e2e_project, tmpdir)

    def test_clone_files_override_success(self, e2e_project, tmpdir, temp_file):
        self.data_owner_clone_override(e2e_project, tmpdir, temp_file)

    def test_delete_files_success(self, e2e_project, temp_file):
        self.data_owner_delete_files(e2e_project, temp_file)

    def test_clone_files_success(self, e2e_project, tmpdir):
        self.data_owner_clone_files(e2e_project, tmpdir)

    def test_clone_with_empty_folder_success(self, e2e_project, tmpdir):
        self.data_owner_clone_with_empty_folder(e2e_project, tmpdir)

    def test_upload_files_success(self, e2e_project, tmpdir):
        self.data_owner_upload_files(e2e_project, tmpdir)

    def test_upload_unchanged_files_success(self, e2e_project, tmpdir):
        self.data_owner_upload_unchanged_files(e2e_project, tmpdir)

    def test_upload_files_from_non_cnvrg_fails(self, e2e_project, tmpdir):
        self.data_owner_upload_files_from_non_cnvrg(e2e_project, tmpdir)

    def test_download_files_success(self, e2e_project):
        self.data_owner_download_files(e2e_project)

    def test_data_owner_download_empty_folder_success(self, e2e_project, tmpdir):
        self.data_owner_download_empty_folder(e2e_project, tmpdir)

    def test_sync_local_success(self, e2e_project):
        self.data_owner_sync_local(e2e_project)

    def test_sync_local_with_output_success(self, e2e_project):
        self.data_owner_sync_local_with_output_dir(e2e_project)

    def test_put_files_absolute_path_success(self, tmpdir, e2e_project):
        self.data_owner_put_files_absolute_path(tmpdir, e2e_project)

    def test_remove_files_absolute_path_success(self, tmpdir, e2e_project):
        self.data_owner_remove_files_absolute_path(tmpdir, e2e_project)

    def test_remove_folders_through_upload_success(self, e2e_project, tmpdir):
        self.data_owner_remove_folders_through_upload(tmpdir, e2e_project)

    def test_remove_file_through_upload(self, e2e_project, tmpdir):
        self.data_owner_remove_file_through_upload(tmpdir, e2e_project)

    def test_list_commits_success(self, e2e_project, temp_file):
        self.data_owner_list_commits(e2e_project, temp_file)

    def test_filtered_list_commits_success(self, e2e_project, temp_file, second_temp_file):
        first_commit_sha_1 = e2e_project.put_files(paths=[temp_file.strpath], message='commit message 1')
        e2e_project.put_files(paths=[second_temp_file.strpath], message='commit message 2')
        commits_generator = e2e_project.list_commits(filter={'message': 'commit message 1'})

        commits = []

        for commit in commits_generator:
            commits.append(commit.sha1)

        assert [first_commit_sha_1] == commits

    def test_empty_filtered_list_commits(self, e2e_project, temp_file):
        e2e_project.put_files(paths=[temp_file.strpath], message='commit message 1')
        commits_generator = e2e_project.list_commits(filter={'message': 'this commit doesnt exist'})

        assert next(commits_generator, None) is None

    def test_access_all_commit_fields_success(self, e2e_project, temp_file, second_temp_file):
        self.data_owner_access_all_commit_fields(e2e_project, temp_file, second_temp_file)

    def test_remove_folder_locally_through_download_success(self, e2e_project, tmpdir):
        self.data_owner_remove_folder_locally_through_download(tmpdir, e2e_project)

    def test_remove_file_locally_through_download_success(self, e2e_project, tmpdir):
        self.data_owner_remove_file_locally_through_download(tmpdir, e2e_project)

    def test_data_owner_sync_complex(self, e2e_project, tmpdir):
        self.data_owner_sync_complex(tmpdir, e2e_project)

    def test_data_owner_sync_removed_file_success(self, e2e_project, tmpdir):
        self.data_owner_sync_removed_file(e2e_project, tmpdir)

    def test_data_owner_sync_removed_folder_success(self, e2e_project, tmpdir):
        self.data_owner_sync_removed_folder(e2e_project, tmpdir)

    def test_data_owner_verify_cnvrg_files_exists_success(self, e2e_project, tmpdir):
        self.data_owner_verify_cnvrg_files_exists(e2e_project, tmpdir)

    def test_sync_zero_size_files_success(self, e2e_git_project):
        self.data_owner_zero_size_file(e2e_git_project)
