import os
import shutil

import pytest
import yaml

from cnvrgv2 import Project
from cnvrgv2.config import Config, CONFIG_FOLDER_NAME, error_messages
from cnvrgv2.config import CONFIG_FILE_NAME
from cnvrgv2.data.file_downloader import cache_file
from cnvrgv2.errors import CnvrgFileError
from tests.conftest import random_string
from tests.e2e.helpers.storage_helper import clean_cnvrg_metadata_files_and_folders


class DataOwnerFiles:

    def data_owner_verify_cnvrg_files_exists(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)
        data_owner.clone()
        assert os.path.exists(os.path.join(data_owner.slug, ".cnvrgignore"))
        assert os.path.exists(os.path.join(data_owner.slug, ".cnvrg/cnvrg.config"))

    def data_owner_put_files(self, data_owner, temp_file):
        data_owner.put_files([temp_file.strpath])
        files = data_owner.list_files()
        assert (len(list(files))) == 1

    def data_owner_put_unchanged_files(self, data_owner, temp_file):
        initial_last_commit = data_owner.last_commit
        local_commit = data_owner.local_commit
        assert (local_commit is None)
        data_owner.put_files([temp_file.strpath])
        data_owner.reload()
        # Local commit should be null
        local_commit_after_first_put = data_owner.local_commit
        assert (local_commit_after_first_put is None)
        # Last commit should be updated to the new commit
        last_commit_after_first_put = data_owner.last_commit
        assert (initial_last_commit != last_commit_after_first_put)
        # Upload the same file once again without any changes
        # It should not create a commit (no changes have been made)
        data_owner.put_files([temp_file.strpath])
        data_owner.reload()
        # Last commit should be the same as the previous commit : no new commit should have been created
        last_commit_after_second_put = data_owner.last_commit
        assert (last_commit_after_second_put == last_commit_after_first_put)
        # Local commit should be null
        local_commit_after_second_put = data_owner.local_commit
        assert (local_commit_after_second_put is None)

    def data_owner_put_folder(self, data_owner, tmpdir):
        # Add one file to tmpdir
        tmpdir.join("temp.txt")
        data_owner.put_files([tmpdir.strpath])

        files = data_owner.list_files()
        for file in files:
            if tmpdir.strpath.lstrip("/") in file.fullpath:  # Server saves files without leading /
                return
        assert False

    def data_owner_put_files_override_false(self, data_owner, temp_file):
        data_owner.put_files([temp_file.strpath])
        files_after_first_upload = data_owner.list_files()
        first_file = next(files_after_first_upload)

        # Try to upload the same file again, override set to False (by default)
        data_owner.put_files([temp_file.strpath])
        files_after_second_upload = data_owner.list_files()
        second_file = next(files_after_second_upload)

        assert len(list(files_after_second_upload)) == len(list(files_after_first_upload))
        assert first_file.created_at == second_file.created_at

    def data_owner_put_files_override_true(self, data_owner, temp_file):
        data_owner.put_files([temp_file.strpath])
        files_after_first_upload = data_owner.list_files()
        first_file = next(files_after_first_upload)

        # Try to upload the same file again, override set to True
        data_owner.put_files([temp_file.strpath], override=True)
        files_after_second_upload = data_owner.list_files()
        second_file = next(files_after_second_upload)

        assert len(list(files_after_second_upload)) == len(list(files_after_first_upload))
        assert first_file.created_at != second_file.created_at

    def data_owner_put_files_abs_path_dir_path(self, data_owner, temp_file):
        # Add one file to tmpdir upload from absolute path that is not pwd
        dir_path = "destination1/destination2"
        data_owner.put_files(temp_file.strpath, dir_path=dir_path)
        files = list(data_owner.list_files())
        assert len(files) == 1
        assert files[0].fullpath.startswith(dir_path), \
            "File {0} does not start with the expected dir_path".format(temp_file.strpath)

    def data_owner_put_file_dir_path_relative_path(self, data_owner, temp_file):
        dir_path = "destination"
        os.chdir(os.path.dirname(temp_file))
        data_owner.put_files(paths=os.path.basename(temp_file), dir_path=dir_path)
        files = list(data_owner.list_files())
        assert len(files) == 1
        assert files[0].fullpath in os.path.join(dir_path, os.path.basename(temp_file)), \
            "File {0} not uploaded".format(files[0].fullpath)

    def data_owner_put_folder_abs_path_dir_path(self, data_owner, tmpdir):
        dir_path = "destination"
        data_owner.put_files([tmpdir.strpath], dir_path=dir_path)
        folders = list(data_owner.list_folders())
        assert len(folders) > 0
        for folder in folders:
            # Exclude root folder when checking the list of dataset folders.
            if folder.name != "root":
                assert folder.fullpath.startswith(dir_path), f"Folder {tmpdir.strpath} not uploaded"

    def data_owner_put_folder_dir_path_relative_path(self, data_owner, tmpdir):
        folder = "relative_folder_testing"
        dir_path = "destination"
        os.chdir(tmpdir)
        if not os.path.exists(folder):
            os.makedirs(folder)
        with open(os.path.join(folder, "file_from_folder2.txt"), 'w') as file:
            file.write("content: this file not empty")
        data_owner.put_files(paths=folder, dir_path=dir_path)
        folders = list(data_owner.list_folders())
        assert len(folders) > 0
        for folder in folders:
            # Exclude root folder when checking the list of dataset folders.
            if folder.name != "root":
                assert folder.fullpath.startswith(dir_path), \
                    "Folder {0} does not start with dir_path".format(tmpdir)
        files = list(data_owner.list_files())
        assert len(files) == 1

    def data_owner_put_empty_folder_dir_path_relative_path(self, data_owner, tmpdir):
        folder = "empty"
        dir_path = "destination"
        os.chdir(tmpdir)
        if not os.path.exists(folder):
            os.makedirs(folder)
        data_owner.put_files(paths=folder, dir_path=dir_path)
        folders = list(data_owner.list_folders())
        assert len(folders) > 0
        for folder in folders:
            # Exclude root folder when checking the list of dataset folders.
            if folder.name != "root":
                assert folder.fullpath.startswith(dir_path), \
                    "Folder {0} does not start with dir_path".format(tmpdir)
        files = list(data_owner.list_files())
        assert len(files) == 0

    def data_owner_put_files_force(self, data_owner, temp_file, temp_file_second):
        commit1 = data_owner.put_files([temp_file.strpath, temp_file_second.strpath])
        filenames = [file.file_name for file in data_owner.list_files()]
        assert temp_file.basename in filenames
        assert temp_file_second.basename in filenames
        assert len(filenames) == 2

        commit2 = data_owner.put_files([temp_file.strpath], force=True)
        filenames = [file.file_name for file in data_owner.list_files()]
        assert temp_file.basename in filenames
        assert temp_file_second.basename not in filenames
        assert len(filenames) == 1
        assert commit1 != commit2

    def data_owner_list_files(self, data_owner, tmpdir):
        num_files_to_upload = 5

        # create files and upload them
        files_to_upload = []
        for i in range(num_files_to_upload):
            file = tmpdir.join("temp{}.txt".format(i))
            file.write("content")
            files_to_upload.append(file.strpath)
        data_owner.put_files(files_to_upload)

        files = data_owner.list_files()
        assert (len(list(files))) == num_files_to_upload

    def data_owner_list_files_var(self, data_owner, tmpdir, num_of_files):
        files_to_upload = []
        filenames_to_upload = []
        for i in range(num_of_files):
            file = tmpdir.join("temp{}.txt".format(i))
            with open(file, "w") as f:
                f.write("file data{}".format(i))

            files_to_upload.append(file.strpath)
            filenames_to_upload.append(os.path.basename(file.strpath))

        data_owner.put_files(files_to_upload, force=True)
        files_retrieved = [file.file_name for file in data_owner.list_files()]

        assert len(filenames_to_upload) == num_of_files
        assert sorted(files_retrieved) == sorted(filenames_to_upload)

    def data_owner_list_files_and_folders(self, data_owner, tmpdir):
        num_files_and_folders = 5
        folders_to_upload = []

        os.chdir(tmpdir.strpath)

        for i in range(num_files_and_folders):
            test_folder_path = tmpdir.mkdir("test_folder_{}".format(i))
            test_file = test_folder_path.join("temp{}.txt".format(i))
            test_file.write("content")
            folders_to_upload.append(test_folder_path.basename)

        data_owner.put_files(folders_to_upload)
        files_and_folders = clean_cnvrg_metadata_files_and_folders(data_owner.list())

        assert (len(list(files_and_folders))) == num_files_and_folders * 2

    def data_owner_delete_files(self, data_owner, temp_file):
        data_owner.put_files([temp_file.strpath])

        data_owner.remove_files([temp_file.strpath])
        files = data_owner.list_files()
        assert (len(list(files))) == 0

    def data_owner_clone_files(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)
        data_owner.clone()
        assert not data_owner._validate_config_ownership()
        os.chdir(data_owner.slug)
        data_owner.reload()
        assert data_owner._validate_config_ownership()
        assert os.path.exists(CONFIG_FOLDER_NAME)

    def data_owner_clone_with_empty_folder(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)

        empty_folder_name = "empty"
        os.mkdir(empty_folder_name)
        data_owner.put_files(paths=[empty_folder_name])

        data_owner.clone()

        os.chdir(data_owner.slug)
        assert os.path.isdir(empty_folder_name)

    def data_owner_clone_override(self, data_owner, tmpdir, temp_file):
        # preparing 2 folders, with the same file name and diffrent content.
        os.chdir(tmpdir.strpath)
        os.mkdir("folder1")
        file = tmpdir.join("folder1/t1.txt")
        file.write("t1data")

        os.mkdir("folder2")
        file = tmpdir.join("folder2/t1.txt")
        file.write("t2data")

        # upload first file, and clone
        os.chdir("folder1")
        data_owner.put_files(paths=["t1.txt"])
        data_owner.clone()

        # on different folder, upload, and clone
        os.chdir("../folder2")
        data_owner.put_files(paths=["t1.txt"])
        os.chdir("../folder1/")
        data_owner.clone(override=True)

        os.chdir(data_owner.slug)
        assert open('t1.txt').read() == "t2data"

    def data_owner_upload_files(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)

        new_file = 'new.txt'
        deleted_file = 'deleted.txt'

        # Init one file in the data owner and make sure it exists
        open(deleted_file, "a").close()
        data_owner.put_files([deleted_file])
        data_owner_files = list(data_owner.list_files())
        assert data_owner_files[0].fullpath == deleted_file

        # Clone the data_owner and enter the new folder
        data_owner.clone()
        os.chdir(data_owner.slug)

        # check number of files locally (including .cnvrg + .cnvrgignore) and remove the tmp file
        assert len(os.listdir()) == 3
        os.remove(deleted_file)
        assert len(os.listdir()) == 2

        # Add new file and upload it
        open(new_file, "a").close()
        data_owner.upload()

        # Now we should have only the new file in the data owner without the deleted file
        files_after_upload = list(clean_cnvrg_metadata_files_and_folders(data_owner.list_files()))
        assert len(files_after_upload) == 1
        assert files_after_upload[0].fullpath == new_file

    def data_owner_upload_unchanged_files(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)

        new_file = 'new.txt'
        deleted_file = 'deleted.txt'

        # Init one file in the data owner and make sure it exists
        open(deleted_file, "a").close()
        data_owner.put_files([deleted_file])
        data_owner_files = list(data_owner.list_files())
        # Initial local commit should be null
        initial_local_commit = data_owner.local_commit
        assert (initial_local_commit is None)
        assert data_owner_files[0].fullpath == deleted_file

        # Clone the data_owner and enter the new folder
        data_owner.clone()
        os.chdir(data_owner.slug)

        # check number of files locally (including .cnvrg + .cnvrgignore) and remove the tmp file
        assert len(os.listdir()) == 3
        os.remove(deleted_file)
        assert len(os.listdir()) == 2

        # Add new file and upload it
        open(new_file, "a").close()
        data_owner.upload()

        # Now we should have only the new file in the data owner without the deleted file
        files_after_upload = list(data_owner.list_files())
        assert len(list(files_after_upload)) == 2  # With .cnvrgingore
        assert len([f for f in files_after_upload if f.fullpath == new_file]) == 1
        # Local commit should be updated to the new commit
        local_commit_after_first_upload = data_owner.local_commit
        assert (initial_local_commit != local_commit_after_first_upload)
        # Upload the same file once again without any changes
        # It should not create a commit (no changes have been made)
        data_owner.upload()
        local_commit_after_second_upload = data_owner.local_commit
        # Local commit should be the same as the previous commit : no new commit should have been created
        assert (local_commit_after_second_upload == local_commit_after_first_upload)

    def data_owner_upload_files_from_non_cnvrg(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)
        tmpdir.join("temp.txt")

        with pytest.raises(CnvrgFileError) as exception_info:
            data_owner._config = Config()
            data_owner.upload()

        assert error_messages.CONFIG_YAML_NOT_FOUND == str(exception_info.value)

    def data_owner_download_files(self, data_owner):
        tmp_file = 'temp.txt'
        try:
            data_owner.clone()
            os.chdir(data_owner.slug)

            # Upload new file to project, then download
            open(tmp_file, "a").close()
            data_owner.put_files([tmp_file])
            os.remove(tmp_file)
            data_owner.download()
            files_after_download = [f.name for f in os.scandir(os.getcwd()) if f.name != CONFIG_FOLDER_NAME]

            assert len(files_after_download) == 2

        finally:
            # Cleanups
            if data_owner.slug in os.getcwd():
                os.chdir('..')
            if os.path.exists(data_owner.slug):
                shutil.rmtree(data_owner.slug)

    def data_owner_download_empty_folder(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)
        empty_dir_name = "empty"
        os.mkdir(empty_dir_name)
        data_owner.clone()
        data_owner.put_files(paths=[empty_dir_name])

        os.chdir(data_owner.slug)
        data_owner.download()

        assert os.path.isdir(empty_dir_name)

    def data_owner_sync_local(self, data_owner):
        tmp_file1 = 'temp1.txt'
        tmp_file2 = 'temp2.txt'
        try:
            data_owner.clone()

            # Upload one file to project
            open(tmp_file1, 'a').close()
            data_owner.put_files([tmp_file1])

            # Add one file to local project dir
            os.chdir(data_owner.slug)
            open(os.getcwd() + "/" + tmp_file2, "a").close()

            commit_sha1 = data_owner.sync()
            remote_files_after_sync = [f.file_name for f in data_owner.list_files()]
            local_files_after_sync = [f.name for f in os.scandir(os.getcwd()) if f.name != CONFIG_FOLDER_NAME]

            assert all(f in remote_files_after_sync for f in local_files_after_sync)
            assert commit_sha1 == data_owner.local_commit
            assert commit_sha1 is not None

        finally:
            # Cleanups
            if data_owner.slug in os.getcwd():
                os.chdir('..')
            if os.path.exists(tmp_file1):
                os.remove(tmp_file1)
            if os.path.exists(data_owner.slug):
                shutil.rmtree(data_owner.slug)

    def data_owner_sync_local_with_output_dir(self, data_owner):
        tmp_file1 = 'temp1.txt'
        tmp_file2 = 'temp2.txt'
        tmp_file3 = 'temp3.txt'

        try:
            data_owner.clone()

            # Upload one file to project
            open(tmp_file1, 'a').close()
            data_owner.put_files([tmp_file1])

            # Add one file to local project dir
            os.chdir(data_owner.slug)
            open(os.getcwd() + "/" + tmp_file2, "a").close()

            # Add one file to local project's output dir
            os.mkdir('output')
            open(os.getcwd() + "/output/" + tmp_file3, "a").close()

            data_owner.sync(output_dir='output')
            remote_files_after_sync = [f.file_name for f in data_owner.list_files()]
            expected_files = [tmp_file1, tmp_file3]

            assert all(f in remote_files_after_sync for f in expected_files)
            assert not any(set(remote_files_after_sync) - set(expected_files))

        finally:
            # Cleanups
            if data_owner.slug in os.getcwd():
                os.chdir('..')
            if os.path.exists(tmp_file1):
                os.remove(tmp_file1)
            if os.path.exists(data_owner.slug):
                shutil.rmtree(data_owner.slug)

    def data_owner_put_files_absolute_path(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)
        filename = random_string(5)
        try:
            open(filename, 'w').close()
            absolute_path = os.path.abspath(filename)
            data_owner.put_files([absolute_path], message="test project files fullpath")

            files = data_owner.list_files()
            for file in files:
                if file.fullpath == absolute_path.lstrip("/"):  # Server saves files without leading /
                    return

            assert False
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def data_owner_remove_files_absolute_path(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)
        filename = random_string(5)
        try:
            open(filename, 'w').close()
            absolute_path = os.path.abspath(filename)
            data_owner.put_files([absolute_path], message="test dataset files fullpath")

            data_owner.remove_files([absolute_path])

            files = data_owner.list_files()
            assert len(list(files)) == 0
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def data_owner_remove_folders_through_upload(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)
        folder_name = random_string(5)
        filename = random_string(5)

        os.mkdir(folder_name)
        open(folder_name + "/" + filename, 'w').close()
        data_owner.put_files([folder_name])

        # check file and folder were created on remote
        check_folder_exist = False
        for i in list(data_owner.list_folders()):
            if folder_name in i._attributes["fullpath"]:
                check_folder_exist = True

        check_file_exist = False
        for i in list(data_owner.list_files()):
            if filename in i._attributes["fullpath"]:
                check_file_exist = True

        assert check_folder_exist
        assert check_file_exist

        data_owner.clone()
        os.chdir(data_owner.slug)
        shutil.rmtree(folder_name)

        data_owner.upload()

        folders = clean_cnvrg_metadata_files_and_folders(data_owner.list_folders())
        files = clean_cnvrg_metadata_files_and_folders(data_owner.list_files())
        assert len(list(files)) == 0
        assert len(list(folders)) == 0

    def data_owner_remove_file_through_upload(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)
        filename = random_string(5)

        open(filename, 'w').close()
        data_owner.put_files([filename])

        check_file_exist = False
        for i in list(data_owner.list_files()):
            if i._attributes["fullpath"] == filename:
                check_file_exist = True
        assert check_file_exist

        data_owner.clone()
        os.chdir(data_owner.slug)
        os.remove(filename)

        data_owner.upload()
        folders = clean_cnvrg_metadata_files_and_folders(data_owner.list_folders())
        assert len(list(folders)) == 0

    def data_owner_remove_folder_locally_through_download(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)
        folder_name = random_string(5)
        filename = random_string(5)

        os.mkdir(folder_name)
        open(folder_name + "/" + filename, 'w').close()
        data_owner.put_files([folder_name])
        data_owner.clone()
        data_owner.remove_files([folder_name + "/"])

        os.chdir(data_owner.slug)
        data_owner.download()
        assert not os.path.isdir(folder_name)

    def data_owner_remove_file_locally_through_download(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)
        filename = random_string(5)

        open(filename, 'w').close()
        data_owner.put_files([filename])
        data_owner.clone()
        data_owner.remove_files([filename])

        os.chdir(data_owner.slug)
        data_owner.download()
        assert not os.path.isfile(filename)

    def data_owner_sync_complex(self, tmpdir, data_owner):

        def create_full(paths):
            for path in paths:
                if "/" in path:
                    os.makedirs(os.path.dirname(path))

                if not path.endswith("/"):
                    open(path, "a").close()

        init_paths = ["a/del_server/c/f1", "del_folder_local/f2", "remove_on_server", "remove_local",
                      "mod_local_del_server", "modified_both"]
        os.chdir(tmpdir.strpath)
        create_full(init_paths)

        data_owner.put_files(["."])
        data_owner.clone()

        modified_both = open("modified_both", "a")
        modified_both.write("file changed remotely")
        modified_both.close()
        data_owner.put_files(["modified_both"])

        create_full(["new_folder_server/file.txt"])
        data_owner.put_files(["new_folder_server/"])

        os.chdir(data_owner.slug)

        os.remove("remove_local")
        shutil.rmtree("del_folder_local")

        mod_local_del_server = open("mod_local_del_server", "a")
        mod_local_del_server.write("file changed locally")
        mod_local_del_server.close()

        modified_both = open("modified_both", "a")
        modified_both.write("file changed locally")
        modified_both.close()

        data_owner.remove_files(["remove_on_server"])
        data_owner.remove_files(["mod_local_del_server"])
        data_owner.remove_files(["a/b"])

        create_full(["new_folder_local/file.txt"])

        commit_sha1 = data_owner.sync()

        # testing
        assert commit_sha1 == data_owner.local_commit
        assert commit_sha1 is not None

        server_folders = []
        for folder in list(data_owner.list_folders()):
            server_folders.append(folder._attributes["fullpath"])

        server_files = []
        for file in list(data_owner.list_files()):
            server_files.append(file._attributes["fullpath"])

        assert os.path.exists("modified_both.conflict")
        assert os.path.exists("new_folder_server")
        assert "new_folder_local/" in server_folders
        assert "remove_local" not in server_files
        assert "del_folder_local/f2" not in server_files
        assert "remove_on_server" not in server_folders

        with open('modified_both', 'r') as f:
            assert f.read() == "file changed locally"

        assert not os.path.exists("remove_on_server")
        assert not os.path.exists("mod_local_del_server")

    def data_owner_nested(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)

        conf = yaml.dump({
            "commit_sha1": "test-commit",
            "git": True,
            "dataset_slug": "fake-slug",
        })

        os.makedirs('.cnvrg/')
        config_file = open('.cnvrg/' + CONFIG_FILE_NAME, 'a')

        config_file.write(conf)
        config_file.close()

        data_owner.clone()

        # check that local config is not corrupted
        config_file = Config()

        assert config_file.project_slug is None
        assert config_file.dataset_slug == "fake-slug"

        # check that local config is not corrupted
        os.chdir(data_owner.slug)
        config_file = Config()

        if isinstance(data_owner, Project):
            assert config_file.project_slug is not None
            assert config_file.dataset_slug is None
            assert config_file.project_slug == data_owner.slug
        else:
            assert config_file.dataset_slug is not None
            assert config_file.project_slug is None
            assert config_file.dataset_slug == data_owner.slug

        assert not data_owner._validate_config_ownership()

    def data_owner_cache(self, tmpdir, data_owner):
        os.chdir(tmpdir.strpath)

        def create_files(paths):
            for path in paths:
                if "/" in path:
                    os.makedirs(os.path.dirname(path), exist_ok=True)

                if not path.endswith("/"):
                    open(path, "a").close()

        init_paths = ["a/dataset_name/a.txt", "a/dataset_name/b.txt", "b/dataset_name/"]

        create_files(init_paths)

        os.chdir("b/dataset_name/")

        cached = cache_file("dataset_name", "a.txt", "a.txt", "a", back_path="../../") and os.path.exists("a.txt")

        not_cached = not cache_file("dataset_name", "c.txt", "c.txt", "a", back_path="../../") and not os.path.exists(
            "c.txt")

        assert cached and not_cached

    def data_owner_sync_removed_file(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)
        filename = random_string(5)
        open(filename, "a")
        data_owner.put_files([filename])
        data_owner.clone()
        data_owner.remove_files([filename])

        os.chdir(data_owner.slug)
        commit_sha1 = data_owner.sync()

        assert commit_sha1 == data_owner.local_commit
        assert commit_sha1 is not None
        assert os.path.exists(filename) is False

    def data_owner_sync_removed_folder(self, data_owner, tmpdir):
        os.chdir(tmpdir.strpath)
        folder_name = random_string(5)
        os.mkdir(folder_name)
        filename = random_string(5)
        open("{}/{}".format(folder_name, filename), "a")
        data_owner.put_files([folder_name])
        data_owner.clone()
        data_owner.remove_files([folder_name + "/"])

        os.chdir(data_owner.slug)
        commit_sha1 = data_owner.sync()

        assert commit_sha1 == data_owner.local_commit
        assert commit_sha1 is not None
        assert os.path.exists(folder_name) is False

    def data_owner_zero_size_file(self, data_owner):
        old_working_dir = os.getcwd()
        try:
            # Clone Git Project
            data_owner.clone()
            os.chdir(data_owner.slug)

            # Create zero size file
            folder_name = random_string(5)
            os.mkdir(folder_name)
            filename = random_string(5)
            open("{}/{}".format(folder_name, filename), "a")

            # Upload zero size file
            data_owner.sync(progress_bar_enabled=True, output_dir=folder_name)

            # Check if file successfully uploaded
            files = data_owner.list_files()
            files_list = list(files)
            assert filename == files_list[0].file_name

        except Exception as e:
            assert False, "Error: {}".format(e)

        finally:
            os.chdir(old_working_dir)
            if os.path.isdir(data_owner.slug):
                shutil.rmtree(data_owner.slug)

    def data_owner_list_commits(self, data_owner, temp_file):
        inserted_commits = [data_owner.put_files(paths=[temp_file.strpath], message='commit message 1')]
        commits_generator = data_owner.list_commits()
        commits = []
        for commit in commits_generator:
            commits.append(commit.sha1)
        assert set(inserted_commits).issubset(commits)

    def data_owner_access_all_commit_fields(self, data_owner, temp_file, second_temp_file):
        """
        This test was added after a bug where exception was thrown when message was empty (the init commit)
        """
        data_owner.put_files(paths=[temp_file.strpath])  # empty commit message
        data_owner.put_files(paths=[second_temp_file.strpath], message="committing another file")

        for commit in data_owner.list_commits():
            attributes = list(commit.available_attributes.keys())
            for attribute in attributes:
                commit.__getattr__(attribute)
