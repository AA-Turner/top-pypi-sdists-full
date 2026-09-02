"""Module containing the Data Tailor class and related errors"""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from eumdac.customisation import Customisation
from eumdac.errors import EumdacError, eumdac_raise_for_status
from eumdac.tailor_models import Chain, DataTailorCRUD, Filter, Quicklook, RegionOfInterest
from eumdac.request import get, post
import eumdac.common
from eumdac.token import AccessToken, AnonymousAccessToken

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from typing import Any, Optional

    from eumdac.product import Product
    from eumdac.token import BaseToken, URLs

    if sys.version_info < (3, 9):
        from typing import Iterable, Mapping, Sequence
    else:
        from collections.abc import Iterable, Mapping, Sequence


class DataTailor:
    """Interface with the EUMETSAT Data Tailor Webservice

    Instance it by providing a token and access the Data Tailor functions like
    posting new customisation jobs, listing the current jobs, cancelling running ones,
    download job outputs, and delete finished jobs.
    """

    token: BaseToken
    urls: URLs
    chains: DataTailorCRUD
    filters: DataTailorCRUD
    rois: DataTailorCRUD
    quicklooks: DataTailorCRUD
    _info: Optional[Mapping[str, Any]] = None
    _user_info: Optional[Mapping[str, Any]] = None

    def __init__(self, token: BaseToken) -> None:
        self.token = token
        self.urls = token.urls
        self.chains = DataTailorCRUD(self, Chain)
        self.filters = DataTailorCRUD(self, Filter)
        self.rois = DataTailorCRUD(self, RegionOfInterest)
        self.quicklooks = DataTailorCRUD(self, Quicklook)

    @property
    def customisations(self) -> Sequence[Customisation]:
        """Return the list of customisations"""
        url = self.urls.get("tailor", "customisations")
        response = get(
            url,
            auth=self.token.auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status("Could not get customisations", response, DataTailorError)
        customisations = response.json()["data"]
        return [Customisation.from_properties(properties, self) for properties in customisations]

    @property
    def info(self) -> Mapping[str, Any]:
        """Return information about Data Tailor Webservice in a Dict-like format."""
        if self._info is None:
            url = self.urls.get("tailor", "info")
            auth = self.token.auth
            response = get(
                url,
                auth=auth,
                headers=eumdac.common.headers,
            )
            eumdac_raise_for_status("Could not get info", response, DataTailorError)
            self._info = response.json()
        return self._info

    @property
    def user_info(self) -> Mapping[str, Any]:
        """Return information about the current Data Tailor Webservice user in a Dict-like format."""
        if self._user_info is None:
            url = self.urls.get("tailor", "user info")
            auth = self.token.auth
            response = get(
                url,
                auth=auth,
                headers=eumdac.common.headers,
            )
            eumdac_raise_for_status("Could not get user_info", response, DataTailorError)
            self._user_info = response.json()
        return self._user_info

    @property
    def quota(self) -> Mapping[str, Any]:
        """Return information about the user workspace quota on the Data Tailor Webservice in a Dict-like format."""
        url = self.urls.get("tailor", "report quota")
        auth = self.token.auth
        response = get(
            url,
            auth=auth,
            headers=eumdac.common.headers,
        )
        eumdac_raise_for_status("Could not get quota", response, DataTailorError)
        return response.json()

    @property
    def is_local(self) -> bool:
        """Return if the configured Data Tailor is the Data Tailor Webservice or a local instance."""
        # when no token for datatailor exists we assume this is a local tailor instance
        return isinstance(self.token, AnonymousAccessToken)

    def get_customisation(self, cutomisation_id: str) -> Customisation:
        """Return a customisation job given its id"""
        return Customisation(cutomisation_id, self)

    def new_customisation(self, product: Product, chain: Chain) -> Customisation:
        """Start a new customisation job for the given product.

        Started customisations will run asynchronously and need to be monitored.
        Once finished, their outputs can be downloaded, and then they need to be deleted.

        Arguments
        ---------
        - `product` : *Product*
            Data Store product to customise
        - `chain` : *Chain*
            Chain configuration to use for the customisation
        """
        (customisation,) = self.new_customisations([product], chain)
        return customisation

    def new_customisations(
        self, products: Iterable[Product], chain: Chain
    ) -> Sequence[Customisation]:
        """Starts multiple customisation jobs for the given products

        Started customisations will run asynchronously and need to be monitored.
        Once finished, their outputs can be downloaded, and then they need to be deleted.

        Arguments
        ---------
        - `products` : *Iterable[Product]*
            Data Store products to customise
        - `chain` : *Chain*
            Chain configuration to use for the customisation
        """
        product_paths = "|||".join(
            self.urls.get(
                "datastore",
                "download product",
                vars={
                    "product_id": product._id,
                    "collection_id": product.collection._id,
                },
            )
            for product in products
        )

        data = {"product_paths": product_paths}
        params = {}

        # instead of guessing the correct token, datatailor should use the token attached to each product
        if isinstance(self.token, AccessToken):
            # provide own token to the endpoint since we assume it is valid for datastore
            params["access_token"] = str(self.token)
        elif self.is_local and any(products):
            # for local tailor instances we use the token attached to the first product
            params["access_token"] = str(next(iter(products)).datastore.token)
        if isinstance(chain, str):
            data["chain_name"] = chain
        else:
            data["chain_config"] = json.dumps(chain.asdict())

        response = post(
            self.urls.get("tailor", "customisations"),
            auth=self.token.auth,
            params=params,
            files=data,
            headers=eumdac.common.headers,
        )

        eumdac_raise_for_status("Could not add customizations", response, DataTailorError)

        customisation_ids = response.json()["data"]
        return [self.get_customisation(customisation_id) for customisation_id in customisation_ids]


class DataTailorError(EumdacError):
    """Errors related to DataTailor operations"""
