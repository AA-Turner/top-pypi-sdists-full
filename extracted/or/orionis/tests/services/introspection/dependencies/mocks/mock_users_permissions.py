class FakeUserWithPermissions:
    """
    A fake user class for testing permission-based logic.
    This class simulates a user object with a set of permissions, providing methods to add and check permissions.
        permissions (set): A set containing the permissions assigned to the user.
    Methods:
        addPermission(permission: str):
            Adds a permission to the user's set of permissions.
        hasPermission(permission: str) -> bool:
            Checks if the user has a specific permission.
    """

    def __init__(self):
        """
        Initializes the object with an empty set of permissions.

        Attributes:
            permissions (set): A set to store permission values.
        """
        self.permissions = set()

    def addPermission(self, permission: str):
        """
        Adds a permission to the set of permissions.

        Args:
            permission (str): The permission to add.
        """
        self.permissions.add(permission)

    def hasPermission(self, permission: str) -> bool:
        """
        Check if the specified permission exists in the user's permissions.

        Args:
            permission (str): The permission to check for.

        Returns:
            bool: True if the permission exists, False otherwise.
        """
        return permission in self.permissions