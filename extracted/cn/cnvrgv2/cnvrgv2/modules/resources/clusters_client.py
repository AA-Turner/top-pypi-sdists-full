import os

import yaml

from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.resources.cluster import Cluster
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.url_utils import urljoin


class ClustersClient:
    def __init__(self, organization):
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._proxy = Proxy(context=self._context)
        self._route = routes.CLUSTERS_BASE.format(scope["organization"])

    def list(self, sort="-id"):
        """
        List all clusters in a specific resource
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields cluster objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=Cluster,
            sort=sort,
        )

    def get(self, slug):
        """
        Retrieves a cluster by the given slug
        @param slug: The slug of the requested cluster
        @return: Cluster object
        """
        if not slug or not isinstance(slug, str):
            raise CnvrgArgumentsError(error_messages.CLUSTER_GET_FAULTY_SLUG)

        return Cluster(context=self._context, slug=slug)

    def create(self,
               build_yaml_path=None,
               kube_config_yaml_path=None,
               resource_name=None,
               provider_name=None,
               domain=None,
               **kwargs):
        """
        Create a new Cluster
        @param build_yaml_path: ccp yaml path
        @param kube_config_yaml_path: kube config yaml path
        @param resource_name: the name of the resource
        @param provider_name: the provider name [aws,gke,eks,dell...]
        @param domain: domain url of existing kubernetes_cluster
        @param kwargs: Dictionary. Rest of optional attributes for creation
            for managed ccp(Cnvrg Cluster Provisioner):
                network: istio as default
            for existing kubernetes_cluster/on premise:
                scheduler: cnvrg_scheduler as default
                namespace: cnvrg as default
                https_scheme: false
                persistent_volumes: false
                gaudi_enabled: false
        @return: Cluster Object
        """

        if build_yaml_path and kube_config_yaml_path:
            raise CnvrgArgumentsError(
                error_messages.CLUSTER_ONE_TYPE.format("build_yaml_path", "kube_config_yaml_path"))

        route = urljoin(self._route, routes.CLUSTER_RESOURCE_REQUEST)
        attributes = {}

        if kube_config_yaml_path:
            if not os.path.exists(kube_config_yaml_path):
                raise CnvrgArgumentsError(error_messages.NO_FILE)

            route = self._route
            kube_config_yaml_content = yaml.safe_load(open(kube_config_yaml_path, "r"))
            attributes = {"domain": domain,
                          "kube_config": str(kube_config_yaml_content),
                          "name": resource_name}
        elif build_yaml_path:
            if not os.path.exists(build_yaml_path):
                raise CnvrgArgumentsError(error_messages.NO_FILE)

            build_yaml_content = yaml.safe_load(open(build_yaml_path, "r"))
            attributes = {"yaml": yaml.dump(build_yaml_content),
                          "provider_name": provider_name}
        elif provider_name:  # No kube_config and no build_yaml_path
            attributes = {"provider_name": provider_name,
                          "resource_name": resource_name}

        attributes.update(**kwargs)

        response = self._proxy.call_api(
            route=route,
            http_method=HTTP.POST,
            payload=attributes
        )

        slug = response.attributes['slug']
        return Cluster(context=self._context, slug=slug)

    def delete(self, slug):
        """
        Delete a cluster by the given slug
        @param slug: The slug of the requested cluster
        @return: None
        """
        if not slug or not isinstance(slug, str):
            raise CnvrgArgumentsError(error_messages.CLUSTER_GET_FAULTY_SLUG)

        Cluster(context=self._context, slug=slug).delete()
