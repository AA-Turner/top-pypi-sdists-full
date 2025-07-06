import os
import platform
import shutil
import time
from subprocess import PIPE, Popen
from urllib.parse import urlparse

import pytest
import requests
from requests.exceptions import ConnectionError

from cnvrgv2.cnvrg import Cnvrg
from cnvrgv2.config import CONFIG_FOLDER_NAME
from cnvrgv2.config import routes
from cnvrgv2.modules.organization.organizations_client import OrganizationsClient
from cnvrgv2.modules.users import ROLES
from cnvrgv2.modules.users.users_client import UsersClient
from cnvrgv2.modules.workflows import EndpointEnvSetup, EndpointKind, NotebookType, WebappType
from cnvrgv2.utils.url_utils import urljoin
from cnvrgv2.modules.labels.utils import LabelColor, LabelKind
from tests.conftest import get_domain, random_string

datasource_test_bukcet_name = 'cnvrg-datasources-bucket'
datasource_test_region = 'us-east-2'


class TestContext(object):
    def __init__(self, prefix):
        self.prefix = prefix

    def generate_name(self, length):
        return self.prefix + random_string(length)


def call_database(command):
    username = os.environ.get("PSQL_USER")
    password = os.environ.get("PSQL_PASS")
    database_name = os.environ.get("PSQL_DATABASE", "cnvrg_development")  # Default name for localhost

    command = [get_psql_path(), "-h", get_postgres_hostname(), "-d", database_name, "-c", command]
    env_cp = os.environ.copy()

    if all([username, password]):
        command += ["-U", username]
        env_cp["PGPASSWORD"] = password

    pipe = Popen(command, stdout=PIPE, env=env_cp)
    result = pipe.communicate()
    return result[0].decode("utf-8")


def get_postgres_hostname():
    return urlparse(get_domain()).hostname.replace("app", "postgres")


def get_psql_path():
    if platform.system().lower() == "linux":  # This is when running automated tests on a linux machine
        psql_path = "/usr/bin/psql"
    else:  # And this is for running on developer's env
        psql_path = "/usr/local/bin/psql"  # This is intel chip
        if not os.path.isfile(psql_path):
            psql_path = "/opt/homebrew/bin/psql"  # And this is to support M1
    return psql_path


@pytest.fixture(autouse=True, scope="class")
def class_context(request):
    context_prefix = request.cls.__name__.lower() + random_string(3)

    yield TestContext(context_prefix)

    # Remove config file
    path_to_remove = CONFIG_FOLDER_NAME
    if os.path.exists(path_to_remove):
        shutil.rmtree(CONFIG_FOLDER_NAME)

    # Clean using class cleanup function
    cleanup = request.cls.__dict__.get("cleanup")
    if cleanup:
        cleanup_func = getattr(cleanup, '__func__')
        cleanup_func(context_prefix)


@pytest.fixture(scope="package")
def e2e_env(domain):
    # Wait till the server is up and running
    while True:
        try:
            resp = requests.get(urljoin(domain, "api", routes.VERSION))
            if resp.status_code == 200:
                break
            else:
                time.sleep(1)
        except ConnectionError:
            time.sleep(1)


@pytest.fixture(scope="class")
def e2e_user(e2e_env, domain, request):
    username = random_string(5)
    email = username + "@cnvrg.io"
    password = "qwe123"

    uc = UsersClient(domain=domain)
    uc.register(username=username, email=email, password=password)
    token, _, _, _ = uc.login(user=email, password=password)

    def cleanup():
        delete_user_command = "DELETE FROM users WHERE username = '{}'".format(username)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return {
        "token": token,
        "username": username,
        "email": email,
        "password": password,
    }


@pytest.fixture(scope="class")
def e2e_client(e2e_user, domain, request):
    org = random_string(5)

    oc = OrganizationsClient(domain=domain, token=e2e_user["token"])
    oc.create(name=org)

    cnvrg = Cnvrg(
        domain=domain,
        email=e2e_user["email"],
        password=e2e_user["password"],
        organization=org
    )

    # Update cluster's status to be online, so that templates could be used
    update_cluster_status = "UPDATE clusters SET status=2 WHERE id IN(SELECT max(id) FROM clusters)"
    call_database(update_cluster_status)

    # Update organization plan to premium to be able to add new clusters
    id_command = "SELECT id FROM organizations WHERE slug = '{}'".format(org)
    command_output = call_database(id_command)
    org_id = int(command_output.split('\n')[2].strip())

    # rails saves hashes as yaml
    metadata = "--- \n :unlimited: true \n :enterprise: true"
    update_plan = f"UPDATE plans SET metadata = '{metadata}' WHERE organization_id = {org_id}"
    call_database(update_plan)

    def cleanup():
        id_command = "SELECT id FROM organizations WHERE slug = '{}'".format(org)
        command_output = call_database(id_command)
        organization_id = int(command_output.split('\n')[2].strip())

        delete_clusters_command = "DELETE FROM clusters WHERE organization_id={}".format(organization_id)
        call_database(delete_clusters_command)

        delete_memebers_command = "DELETE FROM memberships WHERE organization_id={}".format(organization_id)
        call_database(delete_memebers_command)

        delete_images_command = "DELETE FROM images WHERE organization_id={}".format(organization_id)
        call_database(delete_images_command)

        delete_registries_command = "DELETE FROM registries WHERE organization_id={}".format(organization_id)
        call_database(delete_registries_command)

        delete_plans_command = "DELETE FROM plans WHERE organization_id={}".format(organization_id)
        call_database(delete_plans_command)

        delete_organization_command = "DELETE FROM organizations WHERE id={}".format(organization_id)
        call_database(delete_organization_command)

    request.addfinalizer(cleanup)

    return cnvrg


@pytest.fixture(scope="class")
def e2e_data_scientist_user(request, domain, e2e_client):
    username = random_string(5)
    email = username + "@cnvrg.io"
    password = "qwe123"

    uc = UsersClient(domain=domain)
    uc.register(username=username, email=email, password=password)
    e2e_client.members.add(email=email, role=ROLES.MEMBER)
    token, _, _, _ = uc.login(user=email, password=password)

    def cleanup():
        delete_user_command = "DELETE FROM users WHERE username = '{}'".format(username)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return {
        "token": token,
        "username": username,
        "email": email,
        "password": password,
    }


@pytest.fixture(scope="function")
def e2e_project(request, e2e_client, domain):
    project_name = random_string(5)
    project = e2e_client.projects.create(project_name)

    def cleanup():
        delete_project_command = "DELETE FROM projects WHERE title = '{}'".format(project_name)
        call_database(delete_project_command)

    request.addfinalizer(cleanup)

    return project


@pytest.fixture(scope="function")
def e2e_local_experiment(request, e2e_client, e2e_project, domain):
    experiment_name = random_string(5)
    experiment = e2e_project.experiments.init(experiment_name=experiment_name)
    slug = experiment.slug

    def cleanup():
        get_workflow_command = "SELECT id FROM workflows WHERE slug = '{}'".format(slug)
        command_output = call_database(get_workflow_command)
        organization_id = int(command_output.split('\n')[2].strip())
        delete_session_command = "DELETE FROM session_updates WHERE organization_id={}".format(organization_id)
        call_database(delete_session_command)
        delete_workflow_command = "DELETE FROM workflows WHERE slug = '{}'".format(slug)
        call_database(delete_workflow_command)

    request.addfinalizer(cleanup)

    return experiment


@pytest.fixture(scope="function")
def e2e_git_project(e2e_client, domain):
    project_name = random_string(5)
    project = e2e_client.projects.create(project_name)
    project.settings.update(**{
        "git_repo": "https://github.com/githubtraining/hellogitworld",
        "git_branch": "master",
        "is_git": True
    })
    return project


@pytest.fixture(scope="function", autouse=True)
def temp_file(tmpdir):
    file_path = "temp.txt"
    file = tmpdir.join(file_path)
    file.write("temp")
    return file


@pytest.fixture(scope="function", autouse=True)
def second_temp_file(tmpdir):
    file_path = "temp2.txt"
    file = tmpdir.join(file_path)
    file.write("temp 2")
    return file


@pytest.fixture(scope="function")
def e2e_flow(request, e2e_project):
    flow = e2e_project.flows.create()
    request.addfinalizer(lambda: flow.delete())
    return flow


@pytest.fixture(scope="class")
def e2e_flow_yaml():
    # TODO: Make it generate a yaml with a custom flow name or at least edit the file with a given flow name
    return {
        "title": "e2e Flow",
        "path": os.path.dirname(__file__) + "/assets/flow.yaml",
        "string": '''---
                    flow: e2e Flow
                    recurring:
                    next_run_utc:
                    tasks: []
                    relations: []'''
    }


@pytest.fixture(scope="function")
def e2e_flow_version(e2e_flow, domain):
    flow_version = next(e2e_flow.flow_versions.list())
    return flow_version


@pytest.fixture(scope="function")
def e2e_workspace(request, e2e_project, domain):
    title = random_string(5)
    templates = ["dev.small"]

    workspace = e2e_project.workspaces.create(
        title=title,
        templates=templates,
        notebook_type=NotebookType.JUPYTER_LAB
    )

    def cleanup():
        delete_user_command = "DELETE FROM workflows WHERE title = '{}'".format(title)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return workspace


@pytest.fixture(scope="function")
def e2e_webapp(request, e2e_project, domain):
    title = random_string(5)
    templates = ["dev.small"]
    non_existing_file = "filename.py"

    webapp = e2e_project.webapps.create(
        title=title,
        templates=templates,
        file_name=non_existing_file,
        webapp_type=WebappType.SHINY
    )

    def cleanup():
        delete_user_command = "DELETE FROM workflows WHERE title = '{}'".format(title)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return webapp


@pytest.fixture(scope="function")
def e2e_endpoint(request, e2e_project, domain):
    title = "ep-" + random_string(5)
    templates = ["dev.small"]
    non_existing_file = "filename.py"
    function_name = "predict"

    endpoint = e2e_project.endpoints.create(
        title=title,
        templates=templates,
        kind=EndpointKind.WEB_SERVICE,
        file_name=non_existing_file,
        function_name=function_name,
        env_setup=EndpointEnvSetup.PYTHON3
    )

    def cleanup():
        delete_user_command = "DELETE FROM workflows WHERE title = '{}'".format(title)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return endpoint


@pytest.fixture(scope="function")
def e2e_experiment(request, e2e_project):
    title = random_string(5)
    templates = ["dev.small"]
    command = "python3 -c 1+1"

    experiment = e2e_project.experiments.create(
        title=title,
        templates=templates,
        command=command,
        sync_before=False,
        sync_after=False,
    )

    def cleanup():
        delete_user_command = "DELETE FROM workflows WHERE title = '{}'".format(title)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return experiment


@pytest.fixture(scope="function")
def e2e_empty_experiment(request, e2e_project):
    title = random_string(5)

    def cleanup():
        delete_user_command = "DELETE FROM workflows WHERE title = '{}'".format(title)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return e2e_project.experiments.init(title)


@pytest.fixture(scope="function")
def e2e_dataset(request, e2e_client):
    dataset_name = random_string(5)
    dataset = e2e_client.datasets.create(dataset_name)

    request.addfinalizer(lambda: dataset.delete())

    return dataset


@pytest.fixture(scope="function")
def e2e_cluster(request, e2e_client):
    cluster_name = "cnvrg-test"
    attributes = {
        "domain": "test-domain.cicd.cnvrg.me",
        "scheduler": "cnvrg_scheduler",
        "namespace": "test-namespace"
    }
    cluster = e2e_client.clusters.create(
        kube_config_yaml_path="assets/kube_config.yaml",
        resource_name=cluster_name,
        domain=attributes["domain"],
        scheduler=attributes["scheduler"],
        namespace=attributes["namespace"],
        https_scheme=True,
        persistent_volumes=True,
        gaudi_enabled=True
    )

    def cleanup():
        delete_cluster_command = "DELETE FROM clusters WHERE title = '{}'".format(cluster_name)
        call_database(delete_cluster_command)

    request.addfinalizer(cleanup)

    return cluster


@pytest.fixture(scope="function")
def e2e_label_project(request, e2e_client):
    label_name = random_string(5)
    color_name = LabelColor.GREEN
    kind = LabelKind.PROJECT
    label = e2e_client.labels.create(name=label_name, kind=kind, color_name=color_name)

    def cleanup():
        delete_command = "DELETE FROM labels WHERE name = '{}'".format(label_name)
        call_database(delete_command)

    request.addfinalizer(cleanup)

    return label


@pytest.fixture(scope="function")
def e2e_label_dataset(request, e2e_client):
    label_name = random_string(5)
    color_name = LabelColor.RED
    kind = LabelKind.DATASET
    label = e2e_client.labels.create(name=label_name, kind=kind, color_name=color_name)

    def cleanup():
        delete_command = "DELETE FROM labels WHERE name = '{}'".format(label_name)
        call_database(delete_command)

    request.addfinalizer(cleanup)

    return label


@pytest.fixture(scope="function", autouse=True)
def temp_file_second(tmpdir):
    file_path = "temp2.txt"
    file = tmpdir.join(file_path)
    file.write("temp2")
    return file


@pytest.fixture(scope="function")
def e2e_temp_user(e2e_client, e2e_env, domain, request):
    username = random_string(5)
    email = username + "@cnvrg.io"
    password = "qwe123"

    uc = UsersClient(domain=domain)
    uc.register(username=username, email=email, password=password)
    e2e_client.members.add(email=email, role=ROLES.MEMBER)

    def cleanup():
        delete_user_command = "DELETE FROM users WHERE username = '{}'".format(username)
        call_database(delete_user_command)

    request.addfinalizer(cleanup)

    return {
        "username": username,
        "email": email,
        "password": password
    }
