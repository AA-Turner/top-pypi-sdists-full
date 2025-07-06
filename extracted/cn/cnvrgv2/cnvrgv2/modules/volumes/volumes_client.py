from cnvrgv2.modules.volumes.volume import Volume
from cnvrgv2.proxy import Proxy, HTTP
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.config import error_messages, routes
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.json_api_format import JAF
from cnvrgv2.utils.url_utils import urljoin


class VolumesClient:
    def __init__(self, organization):
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._proxy = Proxy(context=self._context)
        self._route = routes.VOLUMES_BASE.format(scope["organization"])

    def list(self, sort="-id", page_size=20, filter=None):
        """
        List all volumes in a specific organization
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields volume objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=Volume,
            sort=sort,
            page_size=page_size,
            filter=filter
        )

    def get(self, slug=None, name=None):
        """
        Retrieves an volume by the given slug, or name
        @param slug: The slug of the requested volume
        @param name: The name of the requested volume
        @return: volume object
        """

        if slug and isinstance(slug, str):
            return Volume(context=self._context, slug=slug)
        elif not slug and name:
            get_volume_by_name_url = urljoin(self._route, routes.GET_BY_NAME_SUFFIX)

            attributes = {
                "volume_name": name,
            }

            res_attributes = self._proxy.call_api(
                route=get_volume_by_name_url,
                http_method=HTTP.GET,
                payload=attributes
            ).attributes

            return Volume(context=self._context, slug=res_attributes['slug'], attributes=res_attributes)

        else:
            raise CnvrgArgumentsError(error_messages.VOLUME_GET_FAULTY_PARAMS)

    def create(self, title, size, cluster, storage_class, read_write_many=False):
        """
        Creates a new volume
        @param title: Title of the volume
        @param size: Size of the volume
        @param cluster: Cluster slug to create the volume on
        @param storage_class: storage class slug to create the volume on
        @param read_write_many: to select the acsses mode of the volume rwm/rwo True/False
        @return:
        """
        attributes = {
            "external_disk_title": title,
            "external_disk_size": size,
            "cluster_slug": cluster,
            "storage_class_slug": storage_class,
            "is_read_only": not read_write_many
        }

        res_attributes = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="Volume", attributes=attributes)
        ).attributes

        return Volume(context=self._context, slug=res_attributes["slug"], attributes=res_attributes)

    def connect(self, title, pvc_name, storage_class):
        """
        connect a volume from cluster
        @param title: Title of the volume
        @param pvc_name: volume claim name in kubernetes
        @param storage_class: storage class that contains the volume
        @return:
        """
        attributes = {
            "existing_volume": pvc_name,
            "storage_class_slug": storage_class,
            "volume_title": title
        }
        res_attributes = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="Volume", attributes=attributes)
        ).attributes
        return Volume(context=self._context, slug=res_attributes["slug"], attributes=res_attributes)
