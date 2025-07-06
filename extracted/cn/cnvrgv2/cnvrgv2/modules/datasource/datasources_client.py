import json
from typing import Optional
from cnvrgv2 import cnvrg
from cnvrgv2.config import error_messages, routes
from cnvrgv2.context import Context, SCOPE
from cnvrgv2.errors import CnvrgArgumentsError
from cnvrgv2.modules.datasource.datasource import Datasource, StorageTypes
from cnvrgv2.proxy import HTTP, Proxy
from cnvrgv2.utils.api_list_generator import api_list_generator
from cnvrgv2.utils.json_api_format import JAF


class DatasourcesClient:
    def __init__(self, organization):
        if type(organization) is not cnvrg.Cnvrg:
            raise CnvrgArgumentsError(error_messages.ARGUMENT_BAD_TYPE.format(cnvrg.Cnvrg, type(organization)))
        self._context = Context(context=organization._context)
        scope = self._context.get_scope(SCOPE.ORGANIZATION)

        self._proxy = Proxy(context=self._context)
        self._route = routes.DATASOURCES_BASE.format(scope["organization"])

    def list(self, filter=None, sort="-id"):
        """
        List all datasources in a specific organization, assigned to the current user
        @param filter: Filter json
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Generator that yields data source objects
        """
        return api_list_generator(
            context=self._context,
            route=self._route,
            object=Datasource,
            sort=sort,
            filter=filter
        )

    def list_count(self, filter=None, sort="-id"):
        """
        Count of datasources in a specific organization, assigned to the current user
        @param filter: Filter json
        @param sort: key to sort the list by (-key -> DESC | key -> ASC)
        @raise: HttpError
        @return: Total count of data sources
        """
        proxy = Proxy(self._context)
        data = {}
        page_size = 20
        filters = json.dumps(filter) if filter else None
        payload = {"sort": sort, "page[size]": page_size, "filter": filters, **data}
        response = proxy.call_api(
            route=self._route,
            http_method=HTTP.GET,
            payload=payload
        )
        return response.meta['total']

    def get(self, slug):
        """
        Retrieves a data source by the given slug
        @param slug: The slug of the requested data source
        @return: Datasource object
        """
        if not slug or not isinstance(slug, str):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_GET_FAULTY_SLUG)

        return Datasource(context=self._context, slug=slug)

    def create(self,
               name: str,
               storage_type: str,
               bucket_name: str,
               credentials: dict,
               region: str,
               description: str = None,
               public: bool = None,
               path: str = None,
               endpoint: str = None,
               collaborators: Optional[list] = None,
               access_point: str = None):
        """
        Creates a new datasource with the given name
        @param storage_type: Enum storage type of the new data source (S3, minio etc), StorageTypes
        @param name: name of the new data source
        @param bucket_name: bucket_name of the new data source
        @param path: path of the new data source
        @param endpoint: endpoint of the new data source
        @param region: region of the new data source
        @param description: description of the new data source
        @param public: permission level of the new data source
        @param credentials: credentials of the new data source
        @param collaborators: users of the new data source (collaborators), array of emails
        @param access_point: AWS Access-point
        @return: the newly created Datasource object
        """
        # mandatory fields
        if not name or not isinstance(name, str):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("name", "string"))
        if not bucket_name or not isinstance(bucket_name, str):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("bucket_name", "string"))
        if not credentials or not isinstance(credentials, dict):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("credentials", "dict"))
        if not region or not isinstance(region, str):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("region", "string"))
        # optional fields
        if path and not isinstance(path, str):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("path", "string"))
        if endpoint and not isinstance(endpoint, str):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("endpoint", "string"))
        if description and not isinstance(description, str):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("description", "string"))
        if public and not isinstance(public, bool):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("public", "boolean"))
        if collaborators and not isinstance(collaborators, list):
            raise CnvrgArgumentsError(error_messages.DATASOURCE_NOT_VALID_PARAM.format("users", "array"))
        if not storage_type or not isinstance(storage_type, StorageTypes):
            arr = list(StorageTypes.__members__.keys())
            valid_types = ', '.join(arr)
            raise CnvrgArgumentsError(error_messages.DATASOURCE_FAULTY_STORAGE_TYPE.format(valid_types))

        attributes = {
            "bucket_name": bucket_name,
            "name": name,
            "storage_type": storage_type.value if storage_type else None,
            "path": path,
            "endpoint": endpoint,
            "region": region,
            "description": description,
            "credentials": credentials,
            "users_emails": collaborators,
            "access_point": access_point
        }

        if public is not None:
            attributes['public'] = public

        response = self._proxy.call_api(
            route=self._route,
            http_method=HTTP.POST,
            payload=JAF.serialize(type="datasource", attributes=attributes)
        )

        slug = response.attributes['slug']
        return Datasource(context=self._context, slug=slug)
