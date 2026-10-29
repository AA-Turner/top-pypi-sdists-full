def can_impersonate(*, hijacker, hijacked) -> bool:
    """Active superusers may impersonate active users that are not superusers.

    Superusers can't impersonate each other, so every action stays attributable,
    and impersonation can't be nested.
    """
    return bool(
        hijacker
        and hijacked
        and hijacker.is_authenticated
        and hijacker.is_active
        and hijacker.is_superuser
        and hijacked.is_active
        and not hijacked.is_superuser
        and hijacker.pk != hijacked.pk
    )
