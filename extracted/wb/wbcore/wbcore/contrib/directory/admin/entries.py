import re

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from reversion.admin import VersionAdmin

from wbcore.admin import ExportCsvMixin, ImportCsvMixin

from ..models import (
    AddressContact,
    BankingContact,
    Company,
    CompanyType,
    CustomerStatus,
    EmailContact,
    Entry,
    Person,
    SocialMediaContact,
    Specialization,
    TelephoneContact,
    WebsiteContact,
)


@admin.register(CustomerStatus)
class CustomerStatusAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("id", "title")


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("id", "title")


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    search_fields = ("title",)
    list_display = ("id", "title")


class AddressContactInline(admin.StackedInline):
    model = AddressContact
    raw_id_fields = ["entry", "geography_city"]
    extra = 0


class BankingContactInline(admin.StackedInline):
    model = BankingContact
    extra = 0
    raw_id_fields = ["entry", "currency"]
    autocomplete_fields = ["currency"]


class EmailContactInline(admin.StackedInline):
    model = EmailContact
    extra = 0
    raw_id_fields = ["entry"]


class TelephoneContactInline(admin.StackedInline):
    model = TelephoneContact
    extra = 0
    raw_id_fields = ["entry"]


class WebsiteContactInline(admin.StackedInline):
    model = WebsiteContact
    extra = 0
    raw_id_fields = ["entry"]


class SocialMediaContactInline(admin.StackedInline):
    model = SocialMediaContact
    extra = 0
    raw_id_fields = ["entry"]


class EmployeesInline(admin.StackedInline):
    model = Person
    extra = 0
    raw_id_fields = ["entry", "employers", "specializations"]


@admin.register(Entry)
class EntryAdmin(ExportCsvMixin, ImportCsvMixin, VersionAdmin):
    list_display = ("computed_str", "entry_type", "is_active")
    fieldsets = ((_("Main information"), {"fields": ("computed_str", "is_active")}),)
    search_fields = ("computed_str",)
    raw_id_fields = ("relationship_managers",)
    inlines = [
        EmployeesInline,
        AddressContactInline,
        BankingContactInline,
        EmailContactInline,
        TelephoneContactInline,
        WebsiteContactInline,
        SocialMediaContactInline,
    ]

    def reversion_register(self, model, **options):
        options = {}
        if issubclass(model, Entry):
            options = {
                "follow": (
                    "relationship_managers",
                    "relationships",
                )
            }

        super().reversion_register(model, **options)

    def get_queryset(self, request):
        return self.model.all_objects.all()


@admin.register(Company)
class CompanyAdmin(EntryAdmin):
    fieldsets = (
        (_("Main information"), {"fields": ("name", "computed_str", "slugify_computed_str", "is_active")}),
        (
            _("Additional Fields"),
            {"fields": ("headcount", "tier", "activity_heat", "salutation")},
        ),
        (_("System-Files"), {"fields": ("profile_image",)}),
    )

    def reversion_register(self, model, **options):
        super().reversion_register(model, **options)

    def process_model(self, model):
        managers = []
        if model.get("relationship_managers", None):
            managers = [Person.objects.get(id=person) for person in model.get("relationship_managers").split(",")]
            del model["relationship_managers"]

        obj = self.model.objects.create(**model)
        if managers:
            obj.relationship_managers.add(*managers)


@admin.register(Person)
class PersonAdmin(EntryAdmin):
    search_fields = ("first_name", "last_name")
    list_display = ("first_name", "last_name", "is_active")
    fieldsets = (
        (
            _("Main information"),
            {"fields": ("first_name", "last_name", "computed_str", "slugify_computed_str", "is_active")},
        ),
        (_("Work Fields"), {"fields": ("active_employee",)}),
        (
            _("Additional Fields"),
            {"fields": ("additional_fields",)},
        ),
        (_("Misc."), {"fields": ("birthday",)}),
        (
            _("System-Files"),
            {
                "fields": (
                    "profile_image",
                    "signature",
                )
            },
        ),
        (_("Activity Heat"), {"fields": ("activity_heat",)}),
    )

    def _get_base_fields(self):
        return [f.name for f in self.model._meta.get_fields()]

    def get_import_fields(self):
        emails_fields = [f"email__{e.name}" for e in EmailContact._meta.get_fields()]
        telephone_fields = [f"telephone__{t.name}" for t in TelephoneContact._meta.get_fields()]

        return emails_fields + telephone_fields + self._get_base_fields()

    def reversion_register(self, model, **options):
        options = {}
        if issubclass(self.model, Entry):
            options = {
                "follow": (
                    "employers",
                    "objects",
                    "employees",
                )
            }
        super().reversion_register(model, **options)

    def process_model(self, model):
        employer = relationship_managers = None

        # Extract reverse relation ship (i.e. person's contacts)
        email = {}
        delete_keys = set()
        for k in model.keys():
            m = re.search("email__(.+)", k)
            if m:
                email[m.group(1)] = model[k]
                delete_keys.add(k)

        telephone = {}
        for k in model.keys():
            m = re.search("telephone__(.+)", k)
            if m:
                telephone[m.group(1)] = model[k]
                delete_keys.add(k)
        for key in delete_keys:
            del model[key]
        # Sanitize Foreign keys
        if model.get("employers", None):
            employer, created = Company.objects.get_or_create(name=model["employers"])
            del model["employers"]
        if model.get("relationship_managers", None):
            relationship_managers = Person.objects.get(id=model["relationship_managers"])
            del model["relationship_managers"]

        # Filter non-model fields
        model = dict(filter(lambda elem: elem[0] in self._get_base_fields(), model.items()))
        qs = self.model.objects.filter(first_name=model["first_name"], last_name=model["last_name"])
        if qs.exists():
            obj = qs.first()
        else:
            obj = self.model.objects.create(**model)

        # Create reverse relationship
        if employer:
            obj.employers.add(employer)
        if relationship_managers:
            obj.relationship_managers.add(relationship_managers)
        if telephone and telephone.get("number", None):
            TelephoneContact.objects.get_or_create(entry=obj, number=telephone["number"], defaults=telephone)
        if email and email.get("address", None):
            EmailContact.objects.get_or_create(address=email["address"], defaults={"entry": obj})
