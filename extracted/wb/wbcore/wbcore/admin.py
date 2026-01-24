import csv
from functools import partial
from io import StringIO

import pandas as pd
from django import forms
from django.contrib import admin
from django.contrib.admin.checks import InlineModelAdminChecks
from django.contrib.admin.options import flatten_fieldsets
from django.forms import ALL_FIELDS
from django.forms.models import modelform_defines_fields
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import path
from django.utils.translation import gettext_lazy as _

from .forms import NonrelatedInlineFormSet, nonrelated_inlineformset_factory
from .markdown.admin import AssetModelAdmin  # noqa: F401
from .models import AppliedPreset, FrontendUserConfiguration, Preset
from .release_notes.admin import ReleaseNoteModelAdmin  # noqa: F401

admin.site.register(AppliedPreset)
admin.site.register(Preset)


class FrontendUserConfigurationInline(admin.TabularInline):
    model = FrontendUserConfiguration
    extra = 0
    fields = ["id", "user", "config"]
    readonly_fields = ["id", "user", "config"]


@admin.register(FrontendUserConfiguration)
class FrontendUserConfigurationModelAdmin(admin.ModelAdmin):
    list_display = ["id", "user"]
    search_fields = ["user__email", "user__username", "id"]
    fieldsets = ((_("Main Information"), {"fields": ("user", "parent_configuration", "config")}),)
    inlines = [FrontendUserConfigurationInline]
    list_filter = ["user"]


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()


class ExportCsvMixin:
    def export_as_csv(self, admin, request, queryset, *args, **kwargs):
        meta = queryset.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}.csv".format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions["export_as_csv"] = (self.export_as_csv, "export_as_csv", "Export Selected")
        return actions


class ImportCsvMixin:
    change_list_template = "wbcore/admin/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [path("import-csv/", self._import_csv)]
        return my_urls + urls

    def manipulate_df(self, df):
        return df

    def process_model(self, model):
        self.model.create(**model)

    def get_import_fields(self):
        return [f.name for f in self.model._meta.get_fields()]

    def _import_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]

            str_text = ""
            for line in csv_file:
                str_text = str_text + line.decode()
            # Import csv as df
            df = pd.read_csv(StringIO(str_text))
            # Sanitize dataframe
            df = df.where(pd.notnull(df), None)
            df = df.drop(df.columns.difference(self.get_import_fields()), axis=1)

            # Overide this function if there is foreign key ids in the dataframe
            df = self.manipulate_df(df)
            errors = 0
            for model in df.to_dict("records"):
                # by default, process the modela as a create request. Can be override to change the behavior
                try:
                    self.process_model(model)
                except Exception:
                    errors += 1
            self.message_user(
                request,
                _("Your CSV file has been imported ( {imports}  imported, {errors} errors)").format(
                    imports=df.shape[0] - errors, errors=errors
                ),
            )
            return redirect("..")
        form = CsvImportForm()
        payload = {"form": form}
        return render(request, "wbcore/admin/csv_form.html", payload)


class NonrelatedInlineModelAdminChecks(InlineModelAdminChecks):
    """
    Check used by the admin system to determine whether or not an inline model
    has a relationship to the parent object.
    In this case we always want this check to pass.
    """

    def _check_exclude_of_parent_model(self, obj, parent_model):
        return []

    def _check_relation(self, obj, parent_model):
        return []


class NonrelatedInlineMixin:
    """
    Mixin for models not explicitly related to the inline model.
    """

    checks_class = NonrelatedInlineModelAdminChecks
    formset = NonrelatedInlineFormSet

    def get_form_queryset(self, obj):
        raise NotImplementedError()

    def save_new_instance(self, parent, instance):
        raise NotImplementedError()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            self.update_instance(formset.instance, instance)
            instance.save()
        formset.save_m2m()

    def get_formset(self, request, obj=None, **kwargs):
        if "fields" in kwargs:
            fields = kwargs.pop("fields")
        else:
            fields = flatten_fieldsets(self.get_fieldsets(request, obj))

        exclude = [*(self.exclude or []), *self.get_readonly_fields(request, obj)]
        if self.exclude is None and hasattr(self.form, "_meta") and self.form._meta.exclude:
            exclude.extend(self.form._meta.exclude)
        exclude = exclude or None

        can_delete = self.can_delete and self.has_delete_permission(request, obj)

        queryset = self.model.objects.none()
        if obj:
            queryset = self.get_form_queryset(obj)

        defaults = {
            "form": self.form,
            "formfield_callback": partial(self.formfield_for_dbfield, request=request),
            "formset": self.formset,
            "extra": self.get_extra(request, obj),
            "can_delete": can_delete,
            "can_order": False,
            "fields": fields,
            "min_num": self.get_min_num(request, obj),
            "max_num": self.get_max_num(request, obj),
            "exclude": exclude,
            "queryset": queryset,
            **kwargs,
        }

        if defaults["fields"] is None and not modelform_defines_fields(defaults["form"]):
            defaults["fields"] = ALL_FIELDS

        return nonrelated_inlineformset_factory(self.model, save_new_instance=self.save_new_instance, **defaults)


class NonrelatedStackedInline(NonrelatedInlineMixin, admin.StackedInline):
    pass


class NonrelatedTabularInline(NonrelatedInlineMixin, admin.TabularInline):
    pass
