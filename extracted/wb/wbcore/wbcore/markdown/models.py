import mimetypes
import pathlib
import uuid

from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


def upload_to(instance, filename):
    return f"markdown/assets/{instance.filename}"


class Asset(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    file = models.FileField(max_length=256, upload_to=upload_to)
    content_type = models.CharField(max_length=32, null=True, blank=True)
    file_url_name = models.CharField(max_length=1024, null=True, blank=True)

    # public = models.BooleanField(default=True)
    class Meta:
        verbose_name = _("Asset")
        verbose_name_plural = _("Assets")
        db_table = "bridger_asset"

    def __str__(self) -> str:
        return str(self.id)

    @property
    def filename(self):
        if suffix := pathlib.Path(self.file.name).suffix:
            return f"{self.id}{suffix}"
        return self.id


@receiver(models.signals.pre_save, sender="wbcore.Asset")
def generate_content_type(sender, instance, **kwargs):
    content_type, encoding = mimetypes.guess_type(pathlib.Path(instance.file.name))
    instance.content_type = content_type
    instance.file_url_name = instance.filename
