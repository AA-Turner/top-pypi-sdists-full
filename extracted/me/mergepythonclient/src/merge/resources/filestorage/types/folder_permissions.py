# This file was auto-generated by Fern from our API Definition.

import typing
from .permission import Permission
from .folder_permissions_item import FolderPermissionsItem

FolderPermissions = typing.Union[str, Permission, typing.List[FolderPermissionsItem]]
