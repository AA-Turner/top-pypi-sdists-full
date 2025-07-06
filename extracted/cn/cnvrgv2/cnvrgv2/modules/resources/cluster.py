import os

import yaml

from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError, CnvrgError
from cnvrgv2.modules.base.dynamic_attributes import DynamicAttributes
from cnvrgv2.modules.resources.templates.kube_templates_client import KubeTemplatesClient
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.url_utils import urljoin


class Cluster(DynamicAttributes):
    available_attributes = {
        "slug": str,
        "title": str,
        "status": str,
        "is_default": bool,
        "cluster_type": str,
        "domain": str,
        "last_health_check": str,
        "scheduler": str,
        "https_scheme": bool,
        "namespace": str,
        "persistent_volumes": bool,
    }

    def __init__(self, context=None, slug=None, attributes=None):
        self._context = Context(context=context)

        # Set current context scope to current machine
        if slug:
            self._context.set_scope(SCOPE.RESOURCE, slug)

        scope = self._context.get_scope(SCOPE.RESOURCE)

        self._proxy = Proxy(context=self._context)
        self._route = routes.CLUSTER_BASE.format(scope["organization"], scope["resource"])
        self._attributes = attributes or {}
        self.slug = scope["resource"]
        self._init_clients()

    def save(self):
        pass

    def delete(self):
        """
        Deletes the current cluster
        @return: None
        """
        # TODO: Change routes without resource_request
        scope = self._context.get_scope(SCOPE.RESOURCE)
        base_route = routes.CLUSTERS_BASE.format(scope["organization"])
        route = urljoin(base_route, routes.CLUSTER_RESOURCE_REQUEST, self.slug)
        self._proxy.call_api(route=route, http_method=HTTP.DELETE)

    def _init_clients(self):
        """
        Sets up the clients that are exposed to user user via machine
        @return: Void
        """
        try:
            self.templates = KubeTemplatesClient(context=self._context)
        except CnvrgError:
            # TODO: Surpress exceptions here
            pass

    def update(self,
               kube_config_yaml_path=None,
               resource_name=None,
               **kwargs
               ):
        """
        @param kube_config_yaml_path: path to the kube_config yaml file
        @param resource_name: the name of the resource
        @param kwargs: kwargs: Dictionary. attributes for updating
            for existing kubernetes_cluster:
                scheduler: cnvrg_scheduler
                namespace: cnvrg
                domain: domain url of existing kubernetes_cluster
                https_scheme: false
                persistent_volumes: false
                gaudi_enabled: false
        @return: None
        """
        if kube_config_yaml_path and not os.path.exists(kube_config_yaml_path):
            raise CnvrgArgumentsError(error_messages.NO_FILE)

        attributes = {**kwargs}
        if kube_config_yaml_path:
            kube_config_yaml_content = yaml.safe_load(open(kube_config_yaml_path, "r"))
            attributes["kube_config"] = str(kube_config_yaml_content)

        if resource_name:
            attributes["name"] = resource_name

        self._proxy.call_api(
            route=self._route,
            http_method=HTTP.PUT,
            payload=attributes
        )
