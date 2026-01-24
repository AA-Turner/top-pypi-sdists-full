import re

from django.urls import NoReverseMatch, resolve
from rest_framework.reverse import reverse

from wbcore.enums import WidgetType
from wbcore.utils.urls import get_parse_endpoint, get_urlencode_endpoint

from ...utils.deprecations import deprecate_warning
from .base import WBCoreViewConfig


class EndpointViewConfig(WBCoreViewConfig):
    metadata_key = "endpoints"
    config_class_attribute = "endpoint_config_class"

    PK_FIELD = "id"
    DELETE_PK_FIELD = "id"
    UPDATE_PK_FIELD = "id"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "get_list_endpoint"):
            deprecate_warning("get_list_endpoint might be deprecated in a future version of wbcore.")

    def get_endpoint(self, **kwargs):
        model = self.view.get_model()
        basename_method_name = (
            "get_representation_endpoint"
            if self.view.WIDGET_TYPE == WidgetType.SELECT.value
            else "get_endpoint_basename"
        )

        if model and (basename_method := getattr(model, basename_method_name, None)):
            basename = basename_method().replace(
                "-list", ""
            )  # we replace "-list" in case it's a representation endpoint which historically comes with the sufix "-list"
            is_list = kwargs.get("is_list", False)
            if self.instance and not is_list:
                return reverse(f"{basename}-detail", args=[self.view.kwargs.get("pk")], request=self.request)
            else:
                return reverse(f"{basename}-list", request=self.request)
        return None

    def get_instance_endpoint(self, **kwargs):
        return self.get_endpoint()

    def _get_instance_endpoint(self):
        if endpoint := self.get_instance_endpoint():
            from wbcore.viewsets import ViewSet

            content_type = self.view.get_content_type()
            if content_type:
                change_permission = f"{content_type.app_label}.view_{content_type.model}"
                permission = self.request.user.has_perm(change_permission)
            elif isinstance(self.view, ViewSet):
                permission = True
            if permission:
                if self.instance:
                    if not re.search(r"\/\d+\/$", endpoint) and (pk := self.view.kwargs.get("pk", None)):
                        endpoint += str(pk) + "/"
                else:
                    endpoint += "{{" + self.PK_FIELD + "}}/"
                return endpoint
        return None

    def _get_list_endpoint(self):
        try:
            return reverse(resolve(self.request.path).view_name, kwargs=self.view.kwargs, request=self.request)
        except NoReverseMatch:
            return None

    def get_delete_endpoint(self, **kwargs):
        if not hasattr(self.view, "ONLY_READ_ONLY_ENDPOINT"):
            return self.get_endpoint()

    def _get_delete_endpoint(self, **kwargs):
        read_only = getattr(self.view, "ONLY_READ_ONLY_ENDPOINT", False)
        content_type = self.view.get_content_type()

        if content_type is None:
            return None

        delete_permission = f"{content_type.app_label}.delete_{content_type.model}"

        if read_only or not self.request.user.has_perm(delete_permission):
            return None
        if endpoint := self.get_delete_endpoint():
            if self.instance:
                if not re.search(r"\/\d+\/$", endpoint) and (pk := self.view.kwargs.get("pk", None)):
                    return f"{endpoint}{pk}/"
                return endpoint
            else:
                return endpoint + "{{" + self.DELETE_PK_FIELD + "}}/"
        return None

    def get_create_endpoint(self, **kwargs):
        return self.get_endpoint(is_list=True)

    def _get_create_endpoint(self):
        from wbcore.viewsets import ViewSet

        read_only = getattr(self.view, "ONLY_READ_ONLY_ENDPOINT", False)
        if read_only:
            return None

        if endpoint := self.get_create_endpoint():
            content_type = self.view.get_content_type()
            if content_type:
                create_permission = f"{content_type.app_label}.add_{content_type.model}"
                permission = self.request.user.has_perm(create_permission)
            elif isinstance(self.view, ViewSet):
                permission = True
            if permission:
                endpoint, query_params = get_parse_endpoint(endpoint)
                query_params["new_mode"] = "true"
                return get_urlencode_endpoint(endpoint, query_params)

        return None

    def get_update_endpoint(self, **kwargs):
        if not hasattr(self.view, "ONLY_READ_ONLY_ENDPOINT"):
            return self.get_instance_endpoint()

    def _get_update_endpoint(self):
        if (endpoint := self.get_update_endpoint()) and not getattr(self.view, "ONLY_READ_ONLY_ENDPOINT", False):
            from wbcore.viewsets import ViewSet

            content_type = self.view.get_content_type()
            if content_type:
                change_permission = f"{content_type.app_label}.change_{content_type.model}"
                permission = self.request.user.has_perm(change_permission)
            elif isinstance(self.view, ViewSet):
                permission = True
            if permission:
                if self.instance:
                    if not re.search(r"\/\d+\/$", endpoint) and (pk := self.view.kwargs.get("pk", None)):
                        endpoint += str(pk) + "/"
                else:
                    endpoint += "{{" + self.UPDATE_PK_FIELD + "}}/"
                return endpoint
        return None

    def get_reorder_endpoint(self, **kwargs):
        return self._get_update_endpoint()

    def _get_reorder_endpoint(self):
        if (endpoint := self.get_reorder_endpoint()) and hasattr(self.view, "reorder"):
            return endpoint + "reorder/"

    def get_pre_change_endpoint(self, pk):
        return None

    def _get_pre_change_endpoint(self):
        if (pk := self.view.kwargs.get("pk", None)) and (endpoint := self.get_pre_change_endpoint(pk)):
            return endpoint
        return None

    def get_pre_create_endpoint(self, pk):
        return None

    def _get_pre_create_endpoint(self):
        if (pk := self.view.kwargs.get("pk", None)) and (endpoint := self.get_pre_create_endpoint(pk)):
            return endpoint
        return None

    def get_pre_delete_endpoint(self, pk):
        return None

    def _get_pre_delete_endpoint(self):
        if (pk := self.view.kwargs.get("pk", None)) and (endpoint := self.get_pre_delete_endpoint(pk)):
            return endpoint
        return None

    def get_metadata(self) -> dict:
        return {
            "instance": self._get_instance_endpoint(),
            "list": self._get_list_endpoint(),
            "delete": self._get_delete_endpoint(),
            "create": self._get_create_endpoint(),
            "update": self._get_update_endpoint(),
            "reorder": self._get_reorder_endpoint(),
            "pre_change": self._get_pre_change_endpoint(),
            "pre_create": self._get_pre_create_endpoint(),
            "pre_delete": self._get_pre_delete_endpoint(),
        }


class NoEndpointViewConfig(EndpointViewConfig):
    def get_endpoint(self, **kwargs):
        return None
