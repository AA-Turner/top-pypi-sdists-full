from django.conf import settings
from django.contrib import admin
from django_better_admin_arrayfield.models.fields import ArrayField

from wbcore.contrib.color.forms import DynamicArrayColorWidget
from wbcore.contrib.color.models import ColorGradient


@admin.register(ColorGradient)
class ColorGradientModelAdmin(admin.ModelAdmin):
    class Media:
        if settings.DEBUG:
            js = [
                "colorfield/jscolor/jscolor.js",
                "colorfield/colorfield.js",
                "js/django_better_admin_arrayfield.min.js",
            ]
        else:
            js = [
                "colorfield/jscolor/jscolor.min.js",
                "colorfield/colorfield.js",
                "js/django_better_admin_arrayfield.min.js",
            ]
        css = {"all": ("css/django_better_admin_arrayfield.min.css",)}

    formfield_overrides = {
        ArrayField: {"widget": DynamicArrayColorWidget},
    }
    list_display = ["title"]
