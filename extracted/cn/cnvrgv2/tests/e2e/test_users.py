import os

import pytest
from cnvrgv2.config import error_messages
from cnvrgv2 import Cnvrg
from cnvrgv2.errors import CnvrgError, CnvrgHttpError, CnvrgLoginError
from cnvrgv2.modules.organization.organizations_client import OrganizationsClient
from cnvrgv2.modules.users import ROLES
from cnvrgv2.modules.users.users_client import UsersClient
from tests.e2e.conftest import call_database


class TestUsers:
    @staticmethod
    def cleanup(context_prefix):
        delete_user_command = "DELETE FROM users WHERE username LIKE'{}%'".format(context_prefix)
        call_database(delete_user_command)

    @pytest.fixture()
    def env_vars_cleaner(self):
        yield
        os.environ.pop("CNVRG_URL", None)
        os.environ.pop("CNVRG_USER", None)
        os.environ.pop("CNVRG_EMAIL", None)
        os.environ.pop("CNVRG_TOKEN", None)
        os.environ.pop("CNVRG_ORGANIZATION", None)

    def test_create_user(self, class_context, domain, e2e_env):
        username = class_context.generate_name(5)
        email = username + "@cnvrg.io"
        password = "qwe123"

        uc = UsersClient(domain=domain)
        user = uc.register(username=username, email=email, password=password)
        assert user

    def test_user_update_success(self, domain, e2e_user):
        uc = UsersClient(domain=domain)
        uc.login(user=e2e_user["email"], password=e2e_user["password"])

        user = uc.me()
        new_name = "new_name"
        new_git_access_token = "larger_than_eight_characters"
        new_company = "new_company"
        new_bio = "new_bio"
        new_timezone = "Asia/Jerusalem"

        # Test single update
        user.name = new_name
        user.save()

        # Test multi update
        user.update(
            **{
                "git_access_token": new_git_access_token,
                "company": new_company,
                "bio": new_bio,
                "time_zone": new_timezone
            }
        )

        assert user.name == new_name
        assert user.git_access_token == new_git_access_token[-8:]
        assert user.company == new_company
        assert user.bio == new_bio
        assert user.time_zone == new_timezone

    def test_create_duplicate_user(self, class_context, domain, e2e_env):
        username = class_context.generate_name(5)
        email = username + "@cnvrg.io"
        password = "qwe123"

        uc = UsersClient(domain=domain)
        user = uc.register(username=username, email=email, password=password)
        assert user

        with pytest.raises(CnvrgHttpError) as exception_info:
            uc.register(username=username, email=email, password=password)
        assert "exists" in str(exception_info.value)

    def test_create_user_bad_arguments(self, domain, e2e_env):
        username = "bad"
        email = username
        password = "qwe123"

        uc = UsersClient(domain=domain)
        with pytest.raises(CnvrgError) as exception_info:
            uc.register(username=username, email=email, password=password)
        assert "Faulty" in str(exception_info.value)

    def test_user_login(self, class_context, domain, e2e_env):
        rand_name = class_context.generate_name(5)
        user_info = {
            "username": rand_name,
            "email": rand_name + "@cnvrg.io",
            "password": "qwe123"
        }

        uc = UsersClient(domain=domain)
        uc.register(**user_info)
        token, org, _, _ = uc.login(user=user_info["email"], password=user_info["password"])
        assert type(token) == str
        assert org is None

    def test_user_login_bad_user(self, domain, e2e_env):
        uc = UsersClient(domain=domain)
        with pytest.raises(CnvrgLoginError) as exception_info:
            uc.login(user="fake@fake.com", password="fake")
        assert "login" in str(exception_info.value)

    def test_user_login_using_env_vars(self, env_vars_cleaner, class_context, domain, e2e_env):
        uc = UsersClient(domain=domain)
        rand_name = class_context.generate_name(5)
        user_info = {
            "username": rand_name,
            "email": rand_name + "@cnvrg.io",
            "password": "qwe123"
        }
        uc.register(**user_info)
        token, org, _, _ = uc.login(user=user_info["email"], password=user_info["password"])
        get_internal_token = "SELECT token FROM users WHERE username LIKE '{}'".format(rand_name)
        res = call_database(get_internal_token)
        internal_token = res.split("\n")[2].strip()
        org_name = rand_name + "org"
        oc = OrganizationsClient(domain=domain, token=token)
        oc.create(name=org_name)

        os.environ["CNVRG_EMAIL"] = user_info["email"]
        os.environ["CNVRG_TOKEN"] = internal_token
        os.environ["CNVRG_ORGANIZATION"] = org_name
        os.environ["CNVRG_URL"] = domain
        c = Cnvrg()
        assert c is not None

    def test_user_login_using_bad_env_vars(self, env_vars_cleaner, class_context, domain, e2e_env):
        # This could fail when running locally if there is a cnvrg.config file
        uc = UsersClient(domain=domain)
        rand_name = class_context.generate_name(5)
        user_info = {
            "username": rand_name,
            "email": rand_name + "@cnvrg.io",
            "password": "qwe123"
        }
        uc.register(**user_info)
        token, org, _, _ = uc.login(user=user_info["email"], password=user_info["password"])
        get_internal_token = "SELECT token FROM users WHERE username LIKE '{}'".format(rand_name)
        res = call_database(get_internal_token)
        internal_token = res.split("\n")[2].strip()
        org_name = rand_name + "org"
        oc = OrganizationsClient(domain=domain, token=token)
        oc.create(name=org_name)

        # CNVRG_USER is deprecated, hence login using this env var should fail. It should use CNVRG_EMAIL
        os.environ["CNVRG_USER"] = user_info["email"]
        os.environ["CNVRG_TOKEN"] = internal_token
        os.environ["CNVRG_ORGANIZATION"] = org_name
        os.environ["CNVRG_URL"] = domain

        with pytest.raises(CnvrgLoginError) as exception_info:
            Cnvrg()
        assert error_messages.CONTEXT_BAD_ENV_VARIABLES in str(exception_info.value)

    def test_user_me(self, class_context, domain, e2e_env):
        username = class_context.generate_name(5)
        email = username + "@cnvrg.io"
        password = "qwe123"

        uc = UsersClient(domain=domain)
        uc.register(username=username, email=email, password=password)
        uc.login(user=email, password=password)

        user = uc.me()
        assert user.email == email
        assert user.username == username

    def test_user_leave_org(self, class_context, domain, e2e_env):
        username = class_context.generate_name(5)
        email1 = username + "1@cnvrg.io"
        email2 = username + "2@cnvrg.io"
        password = "qwe123"

        uc = UsersClient(domain=domain)
        user1 = uc.register(username=username + "1", email=email1, password=password)
        user2 = uc.register(username=username + "2", email=email2, password=password)

        assert len(user1.organizations) == 0
        assert len(user2.organizations) == 0

        org_name = username + "org"
        oc = OrganizationsClient(domain=domain, token=user1._token)
        oc.create(name=org_name)

        user1.reload()
        user2.reload()
        assert len(user1.organizations) == 1
        assert len(user2.organizations) == 0

        with pytest.raises(CnvrgHttpError) as exception_info:
            user1.leave_org(org_name)
        assert "you created" in str(exception_info.value)

        cnvrg = Cnvrg(domain=domain, email=email1, password=password)
        cnvrg.members.add(email=email2, role=ROLES.MANAGER)
        user2.reload()
        assert len(user1.organizations) == 1

        # Make sure we remove the organization membership both locally and in server (tested after reload)
        user2.leave_org(org_name)
        assert len(user2.organizations) == 0
        user2.reload()
        assert len(user2.organizations) == 0
