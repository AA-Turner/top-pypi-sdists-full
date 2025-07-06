import os
import shutil
from os import path

import pytest
from tests.conftest import random_string
from cnvrgv2 import Cnvrg
from cnvrgv2.errors import CnvrgHttpError
from cnvrgv2.modules.project import Project
from tests.e2e.conftest import call_database


class TestProjects:

    @staticmethod
    def cleanup(context_prefix):
        delete_user_command = "DELETE FROM projects WHERE slug LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    @staticmethod
    def create_project(class_context, e2e_client):
        name = class_context.generate_name(5)
        return e2e_client.projects.create(name=name)

    def test_create(self, class_context, e2e_client):
        model = TestProjects.create_project(class_context, e2e_client)
        assert type(model) == Project

    def test_get(self, class_context, e2e_client):
        project = TestProjects.create_project(class_context, e2e_client)

        model = e2e_client.projects.get(slug=project.slug)
        assert type(model) == Project
        assert model.slug == project.slug
        assert model.title == project.slug

    def test_get_non_existent(self, random_name, e2e_client):
        name = random_name(5)

        model = e2e_client.projects.get(slug=name)
        assert type(model) == Project

        with pytest.raises(CnvrgHttpError) as exception_info:
            model.title

        assert "found" in str(exception_info.value)

    def test_delete(self, class_context, e2e_client):
        model = TestProjects.create_project(class_context, e2e_client)
        name = model.slug
        model.delete()

        model = e2e_client.projects.get(slug=name)
        with pytest.raises(CnvrgHttpError) as exception_info:
            model.title

        assert "found" in str(exception_info.value)

    def test_delete_non_existent(self, random_name, e2e_client):
        name = random_name(5)

        model = e2e_client.projects.get(slug=name)
        with pytest.raises(CnvrgHttpError) as exception_info:
            model.delete()

        assert "found" in str(exception_info.value)

    def test_delete_not_authorized(self, domain, e2e_data_scientist_user, e2e_project):
        cnvrg = Cnvrg(
            domain=domain,
            email=e2e_data_scientist_user["email"],
            password=e2e_data_scientist_user["password"],
        )

        with pytest.raises(CnvrgHttpError) as exception_info:
            cnvrg.projects.delete([e2e_project.slug])

        assert "unauthorized" in str(exception_info.value).lower()

    def test_empty_bulk_delete_fail(self, e2e_client):

        with pytest.raises(CnvrgHttpError) as exception_info:
            e2e_client.projects.delete([])

        assert "no project slug was sent." in str(exception_info.value).lower()

    def test_bulk_delete_projects_success(self, class_context, e2e_client):
        num_of_projects = 5
        project_slugs = []

        # Create some projects
        for i in range(num_of_projects):
            project = TestProjects.create_project(class_context, e2e_client)
            project_slugs.append(project.slug)

        e2e_client.projects.delete(project_slugs)

        for slug in project_slugs:
            with pytest.raises(CnvrgHttpError) as exception_info:
                e2e_client.projects.get(slug).title
            assert exception_info.value.status_code == 404

    def test_clone_success(self, random_name, e2e_project):
        filename = expected_output_dir = ""
        try:
            filename = random_name(5)
            expected_output_dir = path.join(e2e_project.title)
            expected_output_file = path.join(expected_output_dir, filename)
            open(filename, 'w')
            e2e_project.put_files([filename], message="test project files")

            e2e_project.clone()

            assert path.exists(expected_output_file)

        finally:
            # cleanup
            if path.exists(filename):
                os.remove(filename)
            if path.exists(expected_output_dir):
                shutil.rmtree(expected_output_dir)

    def test_list(self, class_context, e2e_client):
        # Clean the db before testing list
        TestProjects.cleanup(class_context.prefix)
        name_base = class_context.generate_name(5)
        for i in range(40):
            name = "{}{}".format(name_base, i)
            e2e_client.projects.create(name=name)
        # Check descending order works
        idx = 39
        projects = e2e_client.projects.list()
        for project in projects:
            assert project.slug == "{}{}".format(name_base, idx)
            idx -= 1
        # Check ascending order works
        idx = 0
        projects = e2e_client.projects.list(sort="id")
        for project in projects:
            assert project.slug == "{}{}".format(name_base, idx)
            idx += 1

    def test_sync_should_download(self, e2e_project, e2e_git_project):
        """
        this test simulates the following scenario:
        1. on running experiment when we do sync, download should not happen
        2. on running workspace with git project when we do sync, download should not happen
        """
        folders_to_delete = []
        old_working_dir = os.getcwd()
        try:
            # Create scenarios of envs
            jobs = ["NotebookSession", "Experiment"]
            for job in jobs:
                # Setup project and project files
                project = None
                if job == "NotebookSession":
                    # should be git project for should_download to be false
                    project = e2e_git_project
                elif job == "Experiment":
                    project = e2e_project
                assert project is not None

                # create experiment temp folder
                exp_folder_name = random_string(5)
                folders_to_delete.append(exp_folder_name)
                if not os.path.isdir(exp_folder_name):
                    os.mkdir(exp_folder_name)
                os.chdir(exp_folder_name)
                project.clone()

                os.chdir(old_working_dir)

                # Create new project latest commit
                folder_name = random_string(5)
                folders_to_delete.append(folder_name)
                if not os.path.isdir(folder_name):
                    os.mkdir(folder_name)
                os.chdir(folder_name)
                project.clone()
                os.chdir(project.slug)

                # upload new file as master commit
                master_filename = random_string(5)
                open(master_filename, "a")
                project.put_files(paths=[path.join(master_filename)])

                # Simulate sync inside the experiment
                os.chdir(path.join(old_working_dir, exp_folder_name, project.slug))
                # Set env for test
                os.environ["CNVRG_JOB_TYPE"] = job

                # Test sync, should not download master file, only upload.
                project.sync()
                assert os.path.exists(master_filename) is False

                del os.environ["CNVRG_JOB_TYPE"]
                os.chdir(old_working_dir)
        finally:
            # Clean up
            if os.environ.get("CNVRG_JOB_TYPE"):
                del os.environ["CNVRG_JOB_TYPE"]

            os.chdir(old_working_dir)
            for folder in folders_to_delete:
                if os.path.isdir(folder):
                    shutil.rmtree(folder)
