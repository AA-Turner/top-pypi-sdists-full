from django.db import models

from allianceauth.authentication.models import User


class DiscourseUser(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE, related_name="discourse")
    enabled = models.BooleanField()

    class Meta:
        default_permissions = ()
        permissions = (("access_discourse", "Can access the Discourse service"),)

    def __str__(self) -> str:
        return self.user.username
