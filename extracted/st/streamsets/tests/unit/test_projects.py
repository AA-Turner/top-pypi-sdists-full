#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2024

import json

import pytest
from requests import Response

from streamsets.sdk.sch_api import Command
from streamsets.sdk.sch_models import Group, Project, User
from streamsets.sdk.utils import get_random_string

from .resources.projects import SAMPLE_PROJECT_JSON


def generate_random_user_data():
    # create a user dict with random data
    return {
        'id': get_random_string(),
        'organization': get_random_string(),
        'name': get_random_string(),
        'email': get_random_string(),
        'roles': ['some-internal-name'],
        'groups': [f'all@{get_random_string()}'],
    }


def generate_random_group_data():
    # create a group dict with random data
    return {
        'id': get_random_string(),
        'organization': get_random_string(),
        'name': get_random_string(),
        'roles': ['user'],
        'users': [get_random_string()],
        'lastModifiedOn': 'just now',
    }


def wrap_in_response(json_data):
    res = Response()
    res._content = json.dumps(json_data).encode()
    return res


class MockSchAPI:
    def get_all_users_in_project(self, project_id):
        return Command(self, wrap_in_response({'data': [generate_random_user_data(), generate_random_user_data()]}))

    def get_all_groups_in_project(self, project_id):
        return Command(self, wrap_in_response({'data': [generate_random_group_data(), generate_random_group_data()]}))

    def get_group(self, org_id, group_id):
        return Command(self, wrap_in_response(generate_random_group_data()))

    def update_users_in_project(self, project_id, body):
        pass

    def update_groups_in_project(self, project_id, body):
        pass


class MockSch:
    def __init__(self):
        self.api_client = MockSchAPI()
        self._roles = {'some-internal-name': 'Nice Display Name'}
        self.organization = 'random organization id'


@pytest.fixture(scope='module')
def mock_sch():
    yield MockSch()


@pytest.fixture(scope='function')
def sample_project(mock_sch):
    yield Project(project=SAMPLE_PROJECT_JSON, control_hub=mock_sch)


@pytest.fixture(scope='function')
def new_user(mock_sch):
    yield User(user=generate_random_user_data(), roles=mock_sch._roles, control_hub=mock_sch)


@pytest.fixture(scope='function')
def new_group(mock_sch):
    yield Group(group=generate_random_group_data(), roles=mock_sch._roles, control_hub=mock_sch)


def test_add_user_raises_type_error(sample_project):
    with pytest.raises(TypeError):
        sample_project.add_user('not of type User')


def test_remove_user_raises_type_error(sample_project):
    with pytest.raises(TypeError):
        sample_project.remove_user('not of type User')


def test_add_group_raises_type_error(sample_project):
    with pytest.raises(TypeError):
        sample_project.add_group('not of type Group')


def test_remove_group_raises_type_error(sample_project):
    with pytest.raises(TypeError):
        sample_project.remove_group('not of type Group')


def test_add_user_raises_value_error(sample_project, new_user):
    new_user.id = None
    with pytest.raises(ValueError):
        sample_project.add_user(new_user)


def test_remove_user_raises_value_error(sample_project, new_user):
    new_user.id = None
    with pytest.raises(ValueError):
        sample_project.remove_user(new_user)


def test_add_group_raises_value_error(sample_project, new_group):
    new_group.id = None
    with pytest.raises(ValueError):
        sample_project.add_group(new_group)


def test_remove_group_raises_value_error(sample_project, new_group):
    new_group.id = None
    with pytest.raises(ValueError):
        sample_project.remove_group(new_group)


def test_add_user(sample_project, new_user):
    assert new_user not in sample_project.users
    sample_project.add_user(new_user)
    assert new_user in sample_project.users


def test_add_group(sample_project, new_group):
    assert new_group not in sample_project.groups
    sample_project.add_group(new_group)
    assert new_group in sample_project.groups


def test_add_user_does_not_add_already_existing_user(sample_project, new_user):
    already_existing_user = sample_project.users[0]
    previous_length = len(sample_project.users)
    sample_project.add_user(already_existing_user, new_user)

    assert len(sample_project.users) == previous_length + 1
    assert new_user in sample_project.users
    assert len(sample_project.users.get_all(id=already_existing_user.id)) == 1


def test_add_group_does_not_add_already_existing_group(sample_project, new_group):
    already_existing_group = sample_project.groups[0]
    previous_length = len(sample_project.groups)
    sample_project.add_group(already_existing_group, new_group)

    assert len(sample_project.groups) == previous_length + 1
    assert new_group in sample_project.groups
    assert len(sample_project.groups.get_all(id=already_existing_group.id)) == 1


def test_remove_user(sample_project):
    user = sample_project.users[0]
    sample_project.remove_user(user)

    assert user not in sample_project.users


def test_remove_group(sample_project):
    group = sample_project.groups[0]
    sample_project.remove_group(group)

    assert group not in sample_project.groups


def test_remove_user_only_when_all_users_are_present(sample_project, new_user):
    user = sample_project.users[0]

    with pytest.raises(ValueError):
        sample_project.remove_user(user, new_user)

    assert user in sample_project.users


def test_remove_group_only_when_all_groups_are_present(sample_project, new_group):
    group = sample_project.groups[0]

    with pytest.raises(ValueError):
        sample_project.remove_group(group, new_group)

    assert group in sample_project.groups
