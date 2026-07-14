"""Core functions."""

import datetime as dt

from memberaudit.models import Character

from django.contrib.auth.models import User
from django.db.models import Case, F, Q, QuerySet, Value, When


def check_user_active(user: User, threshold_date: dt.date) -> bool:
    """Report whether a user is active."""

    threshold_datetime = dt.datetime.combine(
        date=threshold_date, time=dt.datetime.min.time(), tzinfo=dt.timezone.utc
    )
    characters: QuerySet[Character] = Character.objects.owned_by_user(user)
    annotated = characters.annotate(
        is_active=Case(
            When(
                Q(online_status__last_login__gt=threshold_datetime)
                | Q(online_status__last_logout__gt=threshold_datetime),
                then=Value(True),
            ),
            When(
                Q(online_status__last_login__isnull=False)
                & Q(online_status__last_logout__lt=F("online_status__last_login")),
                then=Value(True),
            ),
            When(
                Q(online_status__last_login__isnull=False)
                & Q(online_status__last_logout__isnull=True),
                then=Value(True),
            ),
            default=Value(False),
        )
    )
    return annotated.filter(is_active=True).exists()
