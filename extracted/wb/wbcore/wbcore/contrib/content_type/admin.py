from django.contrib import admin
from django.contrib.contenttypes.models import ContentType


@admin.register(ContentType)
class ContentTypeModelAdmin(admin.ModelAdmin):
    list_display = ["app_label", "model"]
    search_fields = ["app_label", "model"]
