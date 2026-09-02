"""This module contains classes modeling Data Tailor resources."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import asdict, dataclass
import requests
from typing import TYPE_CHECKING

from eumdac.request import _request
import eumdac.common

if TYPE_CHECKING:  # pragma: no cover
    import sys
    from typing import Any, Optional, Type, Union

    if sys.version_info < (3, 9):
        from typing import MutableMapping, Sequence
    else:
        from collections.abc import MutableMapping, Sequence
    from eumdac.datatailor import DataTailor

from eumdac.errors import EumdacError, eumdac_raise_for_status


def _none_filter(*args: Any, **kwargs: Any) -> MutableMapping[str, Any]:
    """Build a mapping of '*args' and '**kwargs' removing None values."""
    return {k: v for k, v in dict(*args, **kwargs).items() if v is not None}


class AsDictMixin:
    """Base class adding an 'asdict' method that removes None values."""

    def asdict(self) -> MutableMapping[str, Any]:
        """Return the fields of the instance as a new dictionary mapping field names to field values, removing None values."""
        return asdict(self, dict_factory=_none_filter)  # type: ignore


@dataclass
class Filter(AsDictMixin):
    """Layer filter, a list of `bands` or layers for a given `product`.

    Attributes
    ----------
    - `id`: *str*
    - `name`: *str*
        Human readable name.
    - `product`: *str*
        Product that the filter applies to.
    - `bands`: *list[dict]*
        List of bands part of the filter, as dicts of {id, number, name}.
    """

    __endpoint = "filters"
    id: Optional[str] = None
    bands: Optional[list] = None  # type: ignore[type-arg]
    name: Optional[str] = None
    product: Optional[str] = None


@dataclass
class RegionOfInterest(AsDictMixin):
    """Region of interest, a geographical area defined by its `NSWE` coordinates.

    Attributes
    ----------
    - `id`: *str*
    - `name`: *str*
        Human readable name.
    - `description`: *str*
        Human readable description.
    - `NSWE`:
        North, south, west, east coordinates, in decimal degrees.
    """

    __endpoint = "rois"
    id: Optional[str] = None
    name: Optional[str] = None
    NSWE: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Quicklook(AsDictMixin):
    """Configuration for generating quicklooks."""

    __endpoint = "quicklooks"
    id: Optional[str] = None
    name: Optional[str] = None
    resample_method: Optional[str] = None
    stretch_method: Optional[str] = None
    product: Optional[str] = None
    format: Optional[str] = None
    nodatacolor: Optional[str] = None
    filter: Union[None, dict, Filter] = None  # type: ignore[type-arg]
    x_size: Optional[int] = None
    y_size: Optional[int] = None

    def __post_init__(self) -> None:
        """Prepare `filter` as a Filter instance if given as dict."""
        if self.filter is not None and isinstance(self.filter, dict):
            self.filter = Filter(**self.filter)


@dataclass
class Chain(AsDictMixin):
    """Chain configuration for Data Tailor customisation jobs."""

    __endpoint = "chains"
    __submodels = {"filter": Filter, "roi": RegionOfInterest, "quicklook": Quicklook}
    id: Optional[str] = None
    product: Optional[str] = None
    format: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    aggregation: Optional[str] = None
    projection: Optional[str] = None
    roi: Union[None, dict, RegionOfInterest] = None  # type: ignore[type-arg]
    filter: Union[None, dict, Filter] = None  # type: ignore[type-arg]
    quicklook: Union[None, dict, Quicklook] = None  # type: ignore[type-arg]
    resample_method: Optional[str] = None
    resample_resolution: Optional[list] = None  # type: ignore[type-arg]
    compression: Optional[dict] = None  # type: ignore[type-arg]
    xrit_segments: Optional[list] = None  # type: ignore[type-arg]

    def __post_init__(self) -> None:
        """Prepare attributes as an instance of their class if given as dict."""
        for name, Model in self.__submodels.items():
            attr = getattr(self, name)
            if attr is not None and isinstance(attr, Mapping):
                setattr(self, name, Model(**attr))


if TYPE_CHECKING:  # pragma: no cover
    CrudModelClass = Union[Type[Filter], Type[RegionOfInterest], Type[Quicklook], Type[Chain]]
    CrudModel = Union[Filter, RegionOfInterest, Quicklook, Chain]


class DataTailorCRUD:
    """Generic CRUD for Data Tailor models (Chain, ROI, Filter, Quicklook)."""

    datatailor: DataTailor
    Model: CrudModelClass
    endpoint: str
    url: str

    def __init__(self, datatailor: DataTailor, Model: CrudModelClass) -> None:
        """Init the CRUD for `datatailor` and `Model`."""
        self.datatailor = datatailor
        self.Model = Model
        endpoint = getattr(Model, f"_{Model.__name__}__endpoint")
        self.url = datatailor.urls.get("tailor", endpoint)

    def search(
        self, product: Optional[str] = None, format: Optional[str] = None
    ) -> Sequence[CrudModel]:
        """Search resources by 'format' and 'product'."""
        params = _none_filter(product=product, format=format)
        auth = self.datatailor.token.auth
        response = self._request("get", self.url, auth=auth, params=params)
        return [self.Model(**data) for data in response.json()["data"]]

    def create(self, model: CrudModel) -> None:
        """Create a new resource from 'model' on Data Tailor."""
        auth = self.datatailor.token.auth
        payload = model.asdict()
        self._request("post", self.url, auth=auth, json=payload)

    def read(self, model_id: str) -> CrudModel:
        """Retrieve the resource data with id 'model_id' from Data Tailor."""
        url = f"{self.url}/{model_id}"
        auth = self.datatailor.token.auth
        response = self._request("get", url, auth=auth)
        return self.Model(**response.json())

    def update(self, model: CrudModel) -> None:
        """Update the resource based on 'model' in Data Tailor."""
        data = model.asdict()
        url = f"{self.url}/{data['id']}"
        auth = self.datatailor.token.auth
        self._request("put", url, auth=auth, json=data)

    def delete(self, model: Union[str, CrudModel]) -> None:
        """Remove the resource 'model' from Data Tailor."""
        if isinstance(model, str):
            model_id = model
        else:
            model_id = model.id  # type: ignore[assignment]
        url = f"{self.url}/{model_id}"
        auth = self.datatailor.token.auth
        self._request("delete", url, auth=auth)

    def _request(self, method: str, url: str, **options: Any) -> requests.Response:
        """Perform a 'method' request to 'url' with 'options'."""
        response = _request(method, url, headers=eumdac.common.headers, **options)
        eumdac_raise_for_status(f"Request for {self.Model} failed.", response, EumdacError)
        return response
