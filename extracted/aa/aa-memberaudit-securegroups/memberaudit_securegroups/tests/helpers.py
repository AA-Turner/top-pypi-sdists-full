from django.contrib.auth.models import User
from django.db.models import QuerySet


def make_user_queryset(*users) -> QuerySet[User]:
    params = {"pk__in": [obj.pk for obj in users]}
    return User.objects.filter(**params)
