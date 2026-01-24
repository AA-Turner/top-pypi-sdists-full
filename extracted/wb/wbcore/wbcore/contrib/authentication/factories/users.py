import factory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from dynamic_preferences.registries import global_preferences_registry

from wbcore.contrib.directory.factories import CompanyFactory, PersonFactory
from wbcore.contrib.directory.models import Company
from wbcore.permissions.registry import user_registry

from ..models import Group, User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ["email"]
        skip_postgeneration_save = True

    email = factory.Sequence(lambda n: "email%d@admin.com" % n)
    # username = factory.Faker('user_name')
    username = factory.Sequence(lambda n: "user%d" % n)

    profile = factory.SubFactory("wbcore.contrib.directory.factories.entries.PersonFactory")
    is_active = True
    is_register = True
    is_superuser = False

    plaintext_password = factory.PostGenerationMethodCall("set_password", "defaultpassword")

    @factory.post_generation
    def user_permissions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for permission_key in extracted:
            app_label, codename = permission_key.split(".")
            permission = Permission.objects.get(codename=codename, content_type__app_label=app_label)
            self.user_permissions.add(permission)

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for group in extracted:
            self.groups.add(group)


class InternalUserFactory(UserFactory):
    @factory.post_generation
    def add_internal_profile(self, create, extracted, **kwargs):
        main_company_id = global_preferences_registry.manager()["directory__main_company"]
        if main_company_id and Company.objects.filter(id=main_company_id).exists():
            self.profile.employers.add(Company.objects.get(id=main_company_id))
        else:
            # Create company
            company = CompanyFactory()
            # Set global config main_company=company.id
            global_preferences_registry.manager()["directory__main_company"] = company.id
            self.profile.employers.add(company)
        self.user_permissions.add(
            Permission.objects.get(content_type__app_label="authentication", codename="is_internal_user")
        )
        user_registry.reset_cache()


class SuperUserFactory(UserFactory):
    is_superuser = True
    profile = None

    class Meta:
        pass

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        super()._after_postgeneration(instance, create, results)
        if create:
            instance.save()


class AuthenticatedPersonFactory(PersonFactory):
    user_account = factory.RelatedFactory(UserFactory, "profile")


class GroupFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("text", max_nb_chars=150)

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        for permission in extracted:
            self.permissions.add(permission)

    class Meta:
        model = Group


class ContentTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ContentType

    app_label = "app"
    model = "model"


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
        django_get_or_create = ("content_type", "codename")

    name = factory.Sequence(lambda n: f"Permission {n}")
    codename = factory.Sequence(lambda n: f"codename_{n}")
    content_type = factory.SubFactory(ContentTypeFactory)
