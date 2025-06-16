from rest_framework.reverse import reverse
from wbcore.metadata.configs.endpoints import EndpointViewConfig


class PivotUserObjectPermissionEndpointViewConfig(EndpointViewConfig):
    def get_instance_endpoint(self, **kwargs):
        return reverse(
            "wbcore:guardian:pivoteduserobjectpermission-list",
            args=[self.view.kwargs.get("content_type_id", None), self.view.kwargs.get("object_pk", None)],
            request=self.request,
        )

    def get_update_endpoint(self, **kwargs):
        return reverse(
            "wbcore:guardian:pivoteduserobjectpermission-list",
            args=[self.view.kwargs.get("content_type_id", None), self.view.kwargs.get("object_pk", None)],
            request=self.request,
        )

    def get_create_endpoint(self, **kwargs):
        return reverse(
            "wbcore:guardian:pivoteduserobjectpermission-list",
            args=[self.view.kwargs.get("content_type_id", None), self.view.kwargs.get("object_pk", None)],
            request=self.request,
        )
