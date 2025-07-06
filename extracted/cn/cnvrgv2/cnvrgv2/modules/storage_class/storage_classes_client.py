import time

from cnvrgv2 import cnvrg
from cnvrgv2.modules.resources.clusters_client import ClustersClient
from cnvrgv2.modules.storage_class.storage_class import StorageClass
from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.config import error_messages, routes
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.utils.url_utils import urljoin


class StorageClassesClient:
    def __init__(self, organization):
        if type(organization) is not cnvrg.Cnvrg:
            raise CnvrgArgumentsError(error_messages.ARGUMENT_BAD_TYPE.format(cnvrg.Cnvrg, type(organization)))
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)
        self._proxy = Proxy(context=self._context)
        self._route = routes.STORAGE_CLASSES_BASE.format(scope["organization"])

    def list(self, sort="-id", page_size=20, filter=None):
        """
        List all StorageClass in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @param page_size: size of list per page
        @param filter: using filter to show specific results
        @raise: HttpError
        @return: Generator that yields StorageClass objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=StorageClass,
            sort=sort,
            filter=filter,
            page_size=page_size
        )

    def get(self, slug=None, name=None):
        """
        Retrieves an StorageClass by the given slug, or name
        @param slug: The slug of the requested StorageClass
        @param name: The name of the requested StroageClass
        @return: StorageClass object
        """

        if slug and isinstance(slug, str):
            return StorageClass(context=self._context, slug=slug)
        elif not slug and name:
            get_storage_class_by_name_url = urljoin(self._route, routes.GET_BY_NAME_SUFFIX)

            attributes = {
                "storage_class_name": name,
            }

            res_attributes = self._proxy.call_api(
                route=get_storage_class_by_name_url,
                http_method=HTTP.GET,
                payload=attributes
            ).attributes

            return StorageClass(context=self._context, slug=res_attributes['slug'], attributes=res_attributes)

        else:
            raise CnvrgArgumentsError(error_messages.STORAGE_CLASS_GET_FAULTY_PARAMS)

    def create(self, title, host_ip, host_path, cluster=None, wait=False):
        """
        Creates a new Storage class
        @param cluster: cluster slug to create storage class on
        @param title: Title of the StorageClass
        @param host_ip: Host IP of NFS
        @param host_path: Host path of NFS
        @param cluster_slug: Cluster slug where the Storage Class will be created.
        @param wait: Wait to Storage Class to be created
        @return:
        """

        cluster = cluster or self.get_default_cluster_slug()
        attributes = {
            "storage_class_title": title,
            "host_ip": host_ip,
            "host_path": host_path,
            "cluster_slug": cluster
        }

        res_attributes = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="StorageClass", attributes=attributes)
        ).attributes
        if wait:
            return self.polling_status(polling_interval=10, slug=res_attributes["slug"])

        return StorageClass(context=self._context, slug=res_attributes["slug"], attributes=res_attributes)

    def connect(self, title, connect_all_volumes=False, cluster=None, wait=False):
        """
        Connect existing Storage Class
        @param title: Title of the storage class in kubernetes
        @param connect_all_volumes: connect all storage class volumes
        @param cluster_slug: Cluster slug where the Storage Class will be created.
        @param wait: Wait to Storage Class to be created
        @return:
        """
        attributes = {
            "storage_class_title_k8s": title,
            "connect_all_volumes_exists": connect_all_volumes,
            "cluster_slug": cluster
        }

        res_attributes = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="StorageClass", attributes=attributes)
        ).attributes
        if wait:
            return self.polling_status(polling_interval=10, slug=res_attributes["slug"])
        return StorageClass(context=self._context, slug=res_attributes["slug"], attributes=res_attributes)

    def polling_status(self, polling_interval=10, slug=None):
        res_attributes = self.get(slug)
        while res_attributes.status == "pending":
            res_attributes = self.get(slug)
            time.sleep(polling_interval)
        return res_attributes

    def get_default_cluster_slug(self):
        cluster = next((item for item in ClustersClient(self).list() if item.is_default), None)
        return cluster.slug
