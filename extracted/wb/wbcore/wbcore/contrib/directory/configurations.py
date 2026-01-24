from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy
from rest_framework.reverse import reverse


class ConfigurationRegistry:
    DEFAULT_COMPANY_MODEL_VIEWSET = "wbcore.contrib.directory.viewsets.entries.CompanyModelViewSet"
    DEFAULT_COMPANY_REPRESENTATION_VIEWSET = "wbcore.contrib.directory.viewsets.entries.CompanyRepresentationViewSet"
    DEFAULT_COMPANY_MODEL_SERIALIZER = "wbcore.contrib.directory.serializers.companies.CompanyModelSerializer"
    DEFAULT_COMPANY_REPRESENTATION_SERIALIZER = (
        "wbcore.contrib.directory.serializers.entries.CompanyRepresentationSerializer"
    )
    DEFAULT_PERSON_MODEL_VIEWSET = "wbcore.contrib.directory.viewsets.entries.PersonModelViewSet"
    DEFAULT_PERSON_REPRESENTATION_VIEWSET = "wbcore.contrib.directory.viewsets.entries.PersonRepresentationViewSet"
    DEFAULT_PERSON_MODEL_SERIALIZER = "wbcore.contrib.directory.serializers.persons.PersonModelSerializer"
    DEFAULT_PERSON_REPRESENTATION_SERIALIZER = (
        "wbcore.contrib.directory.serializers.entries.PersonRepresentationSerializer"
    )

    @property
    def company_model_viewset(self):
        return import_string(self.DEFAULT_COMPANY_MODEL_VIEWSET)

    @property
    def company_representation_viewset(self):
        return import_string(self.DEFAULT_COMPANY_REPRESENTATION_VIEWSET)

    @property
    def company_model_serializer(self):
        return import_string(self.DEFAULT_COMPANY_MODEL_SERIALIZER)

    @property
    def company_representation_serializer(self):
        return import_string(self.DEFAULT_COMPANY_REPRESENTATION_SERIALIZER)

    @property
    def person_model_viewset(self):
        return import_string(self.DEFAULT_PERSON_MODEL_VIEWSET)

    @property
    def person_representation_viewset(self):
        return import_string(self.DEFAULT_PERSON_REPRESENTATION_VIEWSET)

    @property
    def person_model_serializer(self):
        return import_string(self.DEFAULT_PERSON_MODEL_SERIALIZER)

    @property
    def person_representation_serializer(self):
        return import_string(self.DEFAULT_PERSON_REPRESENTATION_SERIALIZER)


class DirectoryConfigurationMixin:
    WBCORE_PROFILE = "wbcore.contrib.directory.configurations.resolve_profile"

    DEFAULT_TIERING_HELP_TEXT = gettext_lazy(
        "The tier of the company with 1 being the top tier and 5 being the lowest tier."
    )


def resolve_profile(request):
    user = request.user
    return {
        "image": user.profile.profile_image.url if user.profile.profile_image else None,
        "endpoint": reverse("wbcore:authentication:userprofile-detail", args=[user.id], request=request),
    }


configuration_registry = ConfigurationRegistry()
