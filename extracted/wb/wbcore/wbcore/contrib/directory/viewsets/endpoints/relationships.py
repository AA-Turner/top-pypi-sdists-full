from rest_framework.reverse import reverse

from wbcore.contrib.directory.models import ClientManagerRelationship
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class RelationshipEntryModelEndpoint(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return reverse(
            "wbcore:directory:entry-relationship-list",
            args=[
                self.view.kwargs["entry_id"],
            ],
            request=self.request,
        )


class ClientManagerEndpoint(EndpointViewConfig):
    def get_create_endpoint(self, **kwargs):
        base_url = "wbcore:directory:clientmanagerrelationship-list"
        filter_url = ""
        if "client" in self.request.GET:
            entry_id = self.request.GET["client"]
            filter_url = f"?client={entry_id}"
        if "relationship_manager" in self.request.GET:
            person_id = self.request.GET["relationship_manager"]
            filter_url = f"?relationship_manager={person_id}"
        return f"{reverse(base_url, args=[], request=self.request)}{filter_url}"

    def get_delete_endpoint(self, **kwargs):
        if "pk" in self.view.kwargs:
            cmr_obj = ClientManagerRelationship.objects.get(id=self.view.kwargs["pk"])
            if cmr_obj.status not in [
                ClientManagerRelationship.Status.DRAFT,
                ClientManagerRelationship.Status.REMOVED,
            ]:
                return None
        return super().get_delete_endpoint(**kwargs)


class EmployeeEmployerEndpointConfig(EndpointViewConfig):
    PK_FIELD = "employee"

    def get_endpoint(self, **kwargs):
        return reverse(
            "wbcore:directory:employer-employee-list", args=[self.view.kwargs["employer_id"]], request=self.request
        )

    def get_instance_endpoint(self, **kwargs):
        return reverse("wbcore:directory:person-list", args=[], request=self.request)

    def get_update_endpoint(self, **kwargs):
        return super().get_endpoint()


class EmployerEmployeeEndpointConfig(EndpointViewConfig):
    PK_FIELD = "employer"

    def get_endpoint(self, **kwargs):
        return reverse(
            "wbcore:directory:employee-employer-list", args=[self.view.kwargs["employee_id"]], request=self.request
        )

    def get_instance_endpoint(self, **kwargs):
        return reverse("wbcore:directory:company-list", args=[], request=self.request)

    def get_update_endpoint(self, **kwargs):
        return super().get_endpoint()


class UserIsClientEndpointConfig(EndpointViewConfig):
    PK_FIELD = "relationship_manager"

    def get_endpoint(self, **kwargs):
        return None

    def get_instance_endpoint(self, **kwargs):
        if self.request.user.is_internal:
            return reverse("wbcore:directory:person-list", request=self.request)
        return None
