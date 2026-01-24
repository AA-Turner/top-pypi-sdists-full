from rest_framework.reverse import reverse

from wbcore.metadata.configs.endpoints import EndpointViewConfig


class EntryModelEndpointConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return reverse("wbcore:directory:entry-list", args=[self.view.kwargs["entry_id"]], request=self.request)


class CompanyModelEndpointConfig(EndpointViewConfig):
    def get_create_endpoint(self, **kwargs):
        return reverse("wbcore:directory:company-list", args=[], request=self.request)


class PersonModelEndpointConfig(EndpointViewConfig):
    def get_create_endpoint(self, **kwargs):
        return reverse("wbcore:directory:person-list", args=[], request=self.request)


class UserIsManagerEndpointConfig(EndpointViewConfig):
    def get_instance_endpoint(self, **kwargs):
        return "{{_additional_resources.detail}}"

    def _get_instance_endpoint(self):
        return self.get_instance_endpoint()

    def get_create_endpoint(self, **kwargs):
        base_url = "wbcore:directory:clientmanagerrelationship-list"
        filter_url = f"?relationship_manager={self.request.user.profile.id}"
        return f"{reverse(base_url, args=[], request=self.request)}{filter_url}"


class PersonRepresentationEndpointConfig(EndpointViewConfig):
    def get_create_endpoint(self, **kwargs):
        return PersonModelEndpointConfig(self.view, self.request, self.instance).get_create_endpoint(**kwargs)


class CompanyRepresentationEndpointConfig(EndpointViewConfig):
    def get_create_endpoint(self, **kwargs):
        return CompanyModelEndpointConfig(self.view, self.request, self.instance).get_create_endpoint(**kwargs)
