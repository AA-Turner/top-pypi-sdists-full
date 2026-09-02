"""Module containing the Data Store class and related errors"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import unquote

from eumdac.collection import Collection, SearchResults
from eumdac.errors import EumdacError, eumdac_raise_for_status
from eumdac.product import Product
from eumdac.request import get
from eumdac.token import BaseToken, URLs
from eumdac.logging import logger
import eumdac.common

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from typing import Optional

    if sys.version_info < (3, 9):
        from typing import Iterable, Mapping
    else:
        from collections.abc import Iterable, Mapping


class DataStore:
    """Interface with EUMETSAT Data Store.

    Instance it providing a token and access Data Store functions like
    listing available collections, fetching specific products or performing
    OpenSearch queries.
    """

    token: BaseToken
    urls: URLs
    _collections: Mapping[str, Collection]

    def __init__(self, token: BaseToken) -> None:
        self.token = token
        self.urls = token.urls
        self._collections = {}

    def _load_collections(self) -> None:
        if self._collections:
            return
        url = self.urls.get("datastore", "browse collections")
        response = get(
            url,
            params={"format": "json"},
            auth=self.token.auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status("Load collections failed", response, DataStoreError)
        collection_ids_titles = [
            (item["title"], item["datasetTitle"]) for item in response.json()["links"]
        ]
        self._collections = {
            collection_id: Collection(collection_id, self, title)
            for collection_id, title in collection_ids_titles
        }

    @property
    def collections(self) -> Iterable[Collection]:
        """Collections available"""
        self._load_collections()
        return list(self._collections.values())

    def get_collection(self, collection_id: str) -> Collection:
        """
        Return the collection with the given collection id.

        Parameters
        ----------
        - `collection_id` : *str*
            Collection id, e.g. 'EO:EUM:DAT:MSG:HRSEVIRI'
        """
        return Collection(collection_id, self)

    def check_collection_id(self, collection_id: str) -> None:
        """Validate a collection id, raising CollectionNotFoundError if it's not valid."""
        url = self.urls.get("datastore", "browse collection", vars={"collection_id": collection_id})
        response = None
        try:
            response = get(url, auth=self.token.auth, headers=eumdac.common.headers)
        except Exception as err:
            logger.warning(f"Could not verify collection id due to {err}")

        if response is not None and (
            response.status_code == 401
            or response.status_code == 403
            or response.status_code == 404
        ):
            eumdac_raise_for_status(
                "The collection you are searching for does not exist or you do not have authorisation to access it",
                response,
                CollectionNotFoundError,
            )

    def get_product(self, collection_id: str, product_id: str) -> Product:
        """Return the product with the given id, from the provided collection"""
        return Product(collection_id, product_id, self)

    def get_product_from_search_feature(
        self, collection_id: str, feature: dict[str, Any]
    ) -> Product:
        """Return a product built from the provided Data Store search results feature object"""
        product = Product(collection_id, feature["id"], self)
        # Full searches yield a longer property page
        if len(feature["properties"]) > 4:
            product._parse_browse_properties(feature["properties"], feature["geometry"])
        # Brief searches yield a basic property page (sensing and publication time)
        elif len(feature["properties"]) == 4:
            product._parse_date_properties(feature["properties"])

        return product

    def get_product_from_url(self, product_url: str) -> Product:
        """Return the product matching the given URL, if any"""
        try:
            if product_url.find("api.eumetsat.int/data/download") < 0:
                raise ValueError(f"{product_url} is not a valid Data Store URL")
            url_members: list[str] = product_url.split("/")
            products_index = url_members.index("products")
            # Fetch collection and product, unquoting the URL encoding
            collection_str = unquote(url_members[products_index - 1])
            product_str = unquote(url_members[products_index + 1])
            return self.get_product(collection_str, product_str)
        except Exception as e:
            raise DataStoreError(f"Could not parse product url {product_url}: {e}") from e

    def opensearch(self, query: str) -> SearchResults:
        """Perform an OpenSearch query, returning a SearchResults object with the results.

        Raises DataStoreError if no collection id is provided through the pi parameter.

        Parameters
        ----------
        - `query` : *str*
            OpenSearch query, e.g. 'pi=EO:EUM:DAT:MSG:HRSEVIRI'
        """

        q = self._parse_opensearchquery(query)
        if not "pi" in q:
            raise DataStoreError(
                "Please provide a Collection ID via the pi query parameter (i.e. pi=EO:EUM:DAT:MSG:HRSEVIRI)"
            )
        c = Collection(q.pop("pi"), self)
        return c.search(**q)

    def _parse_opensearchquery(self, query: str) -> dict[str, str]:
        query_dict = {}
        for member in query.split("&"):
            items = member.split("=")
            if len(items) != 2:
                raise DataStoreError(f"Invalid query member: {member}")
            if items[0] not in ["format", "si", "c", "id", "pw"] and items[0] is not None:
                query_dict[items[0]] = items[1]
        return query_dict


class DataStoreError(EumdacError):
    "Errors related to the DataStore"


class CollectionNotFoundError(EumdacError):
    """Collection not found error"""
