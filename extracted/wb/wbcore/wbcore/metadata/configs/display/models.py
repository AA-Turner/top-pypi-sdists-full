from django.db import models

from wbcore.contrib.authentication.models.users import User


class Preset(models.Model):
    title = models.CharField(max_length=64)
    user = models.ForeignKey(to=User, related_name="presets", on_delete=models.CASCADE, null=True, blank=True)
    display_identifier = models.CharField(max_length=512)
    display = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.title} - {self.user} ({self.display_identifier})"


class AppliedPreset(models.Model):
    user = models.ForeignKey(to=User, related_name="applied_presets", on_delete=models.CASCADE)
    display_identifier_path = models.CharField(max_length=1024)
    preset = models.ForeignKey(
        to=Preset, related_name="applied_presets", on_delete=models.SET_NULL, null=True, blank=True
    )
    display = models.JSONField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.display_identifier_path} ({self.user})"
