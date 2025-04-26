"""The specs module contains "Tecton object specs", i.e. Python data models for Tecton objects.

Specs provide a unified, frozen (i.e. immutable), and more useful abstraction over args and data protos for use within
the Python SDK.

See the RFC;
https://www.notion.so/tecton/RFC-Unified-SDK-for-Notebook-Driven-Development-a377af9d320f46488ea238e51e2ce656
"""

from tecton_core.specs.data_source_spec import *
from tecton_core.specs.entity_spec import *
from tecton_core.specs.feature_service_spec import *
from tecton_core.specs.feature_view_spec import *
from tecton_core.specs.resource_provider_spec import *
from tecton_core.specs.secret_spec import *
from tecton_core.specs.server_group_spec import *
from tecton_core.specs.tecton_object_spec import *
from tecton_core.specs.time_window_spec import *
from tecton_core.specs.time_window_spec import TimeWindowSeriesSpec
from tecton_core.specs.transformation_spec import *
