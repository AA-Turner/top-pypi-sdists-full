import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from faker import Faker

from wbcore.contrib.authentication.models.users import User
from wbcore.contrib.permission.internal.registry import UserBackendRegistry

fake = Faker()


def create_internal_user():
    user = User.objects.create(is_active=True, username=fake.user_name(), email=fake.email(), is_internal=True)
    permission = Permission.objects.get_or_create(
        content_type=ContentType.objects.get_for_model(User), codename="is_internal_user"
    )[0]
    user.user_permissions.add(permission)
    return user


@pytest.mark.django_db
class TestBackend:
    def test_get_internal_users(self):
        user = create_internal_user()
        assert set(UserBackendRegistry().get_internal_users()) == {user}
