from cnvrgv2.config import routes
from cnvrgv2.errors import CnvrgHttpError
from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.utils.validators import attributes_validator

DISABLED_PROPERTY_INT = -1
DISABLED_PROPERTY_STRING = ""
STRING_PROPERTIES = ("slack_webhook_url", "custom_pypi_url")


class OrganizationSettings(DynamicAttributes):
    available_attributes = {
        "default_computes": list,
        "install_dependencies": bool,
        "slack_webhook_url": str,
        "debug_time_enabled": bool,
        "debug_time": int,
        "email_on_error": bool,
        "email_on_success": bool,
        "queued_compute_wait_time": int,
        "idle_enabled": bool,
        "idle_time": int,
        "max_duration_workspaces_enabled": bool,
        "max_duration_workspaces": int,
        "max_duration_experiments_enabled": bool,
        "max_duration_experiments": int,
        "max_duration_endpoints_enabled": bool,
        "max_duration_endpoints": int,
        "max_duration_webapps_enabled": bool,
        "max_duration_webapps": int,
        "automatically_clear_cached_commits": int,
        "custom_pypi_enabled": bool,
        "custom_pypi_url": str,
        "default_compute_ids": list,
    }

    def __init__(self, organization):
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._proxy = Proxy(context=self._context)
        self._route = routes.ORGANIZATION_SETTINGS.format(scope["organization"])

        self._attributes = {}

    def save(self):
        """
        Save the local settings in the current organization
        @return: None
        """
        self.update(**self._attributes)

    def update(self, **kwargs):
        """
        Updates current organization's settings with the given params
        @param kwargs: any param out of the available attributes can be sent
        @return: None
        """

        def set_attributes_value(attributes):
            def set_value(key, value):
                if value is not None:
                    return value

                if OrganizationSettings.available_attributes[key] is str:
                    return DISABLED_PROPERTY_STRING

                if OrganizationSettings.available_attributes[key] is bool:
                    return bool(value)

                return DISABLED_PROPERTY_INT if OrganizationSettings.available_attributes[key] is int else value

            return {k: set_value(k, v) for k, v in attributes.items()}

        attributes_validator(
            available_attributes=OrganizationSettings.available_attributes,
            attributes=kwargs,
        )

        try:
            response = self._proxy.call_api(
                route=self._route,
                http_method=HTTP.PUT,
                payload=JAF.serialize(type="settings", attributes={**self._attributes, **set_attributes_value(kwargs)})
            )
        except CnvrgHttpError as e:
            self.reload()
            raise e

        self._attributes = response.attributes

    def values(self):
        hash_representation = {}
        for key in self.__class__.available_attributes.keys():
            hash_representation[key] = getattr(self, key)

        return hash_representation
