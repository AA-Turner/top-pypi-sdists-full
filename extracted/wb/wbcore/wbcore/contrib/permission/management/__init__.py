from wbcore.contrib.permission.internal.registry import UserBackendRegistry

def refresh_internal_users(*args, **kwargs):
    UserBackendRegistry().refresh_users()
