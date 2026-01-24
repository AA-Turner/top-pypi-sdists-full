from django.contrib.auth.models import Permission


def perm_to_permission(perm: str) -> Permission:
    """
    Convert a identifier string permission format in 'app_label.codename'
    (teremd as *perm*) to a django permission instance.

    Args:
        perm: The string permission identifier in the form 'app_label.codename'

    Returns:
        The Permission object corresponding to the given string identifier

    Raises:
        AttributeError: When the given string identifier does not match the expected format 'app_label.codename'
    """
    try:
        app_label, codename = perm.split(".", 1)
    except IndexError as e:
        raise AttributeError(
            "The format of identifier string permission (perm) is wrong. " "It should be in 'app_label.codename'."
        ) from e
    else:
        permission = Permission.objects.get(content_type__app_label=app_label, codename=codename)
        return permission
