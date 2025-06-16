# Copyright 2019 Cognite AS

from cognite.seismic._api_client import CogniteSeismicClient  # noqa: F401
from cognite.seismic._token import TokenGenerator, generate_oidc_token  # noqa: F401
from cognite.seismic.data_classes import errors  # noqa: F401
from cognite.seismic.data_classes.api_types import *  # noqa: F401, F403
from cognite.seismic.data_classes.extents import *  # noqa: F401, F403
from cognite.seismic.data_classes.geometry import *  # noqa: F401, F403
from cognite.seismic.data_classes.searchspec import *  # noqa: F401, F403
from cognite.seismic.data_classes.trace_data import *  # noqa: F401, F403

from ._version import get_version as _get_version

__version__ = _get_version()

del _get_version
