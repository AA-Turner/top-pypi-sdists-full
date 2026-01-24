from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.fields.reverse_related import ManyToManyRel
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from slugify import slugify

from wbcore.contrib.color.fields import ColorField
from wbcore.models import WBModel
from wbcore.utils.models import ComplexToStringMixin


class ManagedMixin(models.Model):
    managed = models.BooleanField(default=False)

    class Meta:
        abstract = True


class Tag(ComplexToStringMixin, ManagedMixin):
    title = models.CharField(max_length=255)

    slug = models.CharField(max_length=255, null=True, blank=True)
    color = ColorField(default="#D3D3D3")

    groups = models.ManyToManyField(to="tags.TagGroup", blank=True)
    description = models.TextField(default="", blank=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, blank=True, null=True, related_name="associated_tags"
    )

    class Meta:
        constraints = (models.UniqueConstraint(name="unique_tag", fields=("slug", "content_type")),)
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self) -> str:
        return super().__str__()

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:tags:tag"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:tags:tagrepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{computed_str}}"

    def compute_str(self) -> str:
        # We need to check here if the instance already is in the database, otherwise groups cannot be linked yet
        if self.id and self.groups.exists():
            groups = ",".join(self.groups.all().values_list("title", flat=True))
            return f"{groups}::{self.title}"
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        self.computed_str = self.compute_str()
        super().save(*args, **kwargs)

    def get_tagged_queryset(self):
        qs = self.__class__.objects.none()
        for field in filter(lambda x: isinstance(x, ManyToManyRel), self.__class__._meta.get_fields()):
            _qs = getattr(self, field.related_name).all()
            qs = qs.union(_qs.values("tag_detail_endpoint", "tag_representation"))
        return qs


class TagGroup(ManagedMixin, WBModel):
    title = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:tags:taggroup"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:tags:taggrouprepresentation-list"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{title}}"

    def __str__(self) -> str:
        return f"{self.title}"

    class Meta:
        verbose_name = "Tag Group"
        verbose_name_plural = "Tag Groups"


@receiver(m2m_changed, sender=Tag.groups.through)
def tag_groups_m2m_changed(sender, instance, action, **kwargs):
    instance.save()
