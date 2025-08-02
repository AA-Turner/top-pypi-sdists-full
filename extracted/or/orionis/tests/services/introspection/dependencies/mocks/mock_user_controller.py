from tests.services.introspection.dependencies.mocks.mock_user import FakeUser
from tests.services.introspection.dependencies.mocks.mock_users_permissions import FakeUserWithPermissions


class UserController:
    """
    UserController manages user-related operations, utilizing a user repository for data access.
    Methods:
        __init__(user_repository: FakeUser)
            Initializes the controller with a user repository.
        createUserWithPermissions(user_permissions: FakeUserWithPermissions, permissions: list[str]) -> FakeUserWithPermissions
            Adds a list of permissions to the given user_permissions object and returns it.
    """

    def __init__(self, user_repository: FakeUser):
        """
        Initializes the class with a user repository.

        Args:
            user_repository (FakeUser): An instance of FakeUser to be used as the user repository.
        """
        self.user_repository = user_repository

    def createUserWithPermissions(self, user_permissions: FakeUserWithPermissions, permissions: list[str]):
        for permission in permissions:
            user_permissions.addPermission(permission)
        return user_permissions