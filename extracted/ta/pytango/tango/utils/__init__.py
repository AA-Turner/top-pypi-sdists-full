# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""
This is an internal PyTango module.

The implementation is split across the private submodules of this package;
they are grouped by concern and imported here so that ``tango.utils`` keeps
exposing the names it always has.
"""

# This module is a re-export facade: every import below exists to keep a name
# reachable as tango.utils.<name>, so none of them is used here.
# ruff: noqa: F401

from ._bindings import (
    __auto_die_callbacks_holder,
    _check_only_allowed_kwargs,
    _exception_converter,
    _get_command_inout_param,
    _get_new_CallbackAutoDie,
    _InterfaceDefinedByIDL,
    _is_coroutine_function,
    _release_CallbackAutoDie,
    _RemovedClass,
)
from ._concurrency import (
    PyTangoThread,
    PyTangoThreadPoolExecutor,
    _thread_pool_executor_ctx_worker,
    _thread_pool_executor_worker,
)
from ._containers import (
    CaselessDict,
    CaselessList,
)
from ._convert import (
    __NO_STR_VALUE,
    StdDoubleVector_2_seq,
    StdStringVector_2_seq,
    __seq_2_vector,
    __vector_2_seq,
    _seqStr_2_obj_from_type,
    _seqStr_2_obj_from_type_format,
    ensure_binary,
    obj_2_str,
    seq_2_StdDoubleVector,
    seq_2_StdStringVector,
    seqStr_2_obj,
    str_2_obj,
    strtobool,
)
from ._db import (
    DbData_2_dict,
    _append_dict_to_db_data,
    get_property_from_db,
    parameter_2_dbdata,
    seq_2_DbData,
    seq_2_DbDevExportInfos,
    seq_2_DbDevInfos,
)
from ._deprecated import (
    get_telemetry_tracer_provider_factory,
    set_telemetry_tracer_provider_factory,
)
from ._events import (
    AsyncEventCallback,
    EventCallback,
)
from ._introspect import (
    __get_meth_func,
    dir2,
    document_method,
    document_static_method,
    get_attrs,
)
from ._platform import (
    PyTangoHelpFormatter,
    __import,
    __requires,
    from_version_str_to_hex_str,
    from_version_str_to_int,
    get_home,
    get_latest_device_class,
    get_tango_device_classes,
    info,
    requires_pytango,
    requires_tango,
)
from ._trl import (
    InvalidTangoHostTrlError,
    _clear_test_context_tango_host_fqtrl,
    _get_device_fqtrl,
    _get_device_fqtrl_if_necessary,
    _get_test_context_tango_host_fqtrl,
    _is_tango_uri_resolved,
    _is_valid_tango_trl,
    _resolve_tango_trl,
    _set_test_context_tango_host_fqtrl,
    _try_resolve_tango_trl,
)
from ._typeinfo import (
    EnumTypeError,
    __check_types_uniformity,
    __get_tango_type,
    __has_ellipsis_in_types,
    eval_in_fallback_frames,
    get_attribute_type_format,
    get_enum_labels,
    get_tango_type,
    get_tango_type_format,
    parse_type_hint,
    set_complex_value,
)
from ._types import (
    FROM_TANGO_TO_NUMPY_TYPE,
    TO_TANGO_TYPE,
    __add_derived_scalar_types,
    __build_to_tango_type,
    __int_klasses,
    __is_type,
    __number_klasses,
    __seq_klasses,
    __str_klasses,
    _array_binary_types,
    _array_bool_types,
    _array_float_types,
    _array_int_types,
    _array_numerical_types,
    _array_str_types,
    _array_types,
    _scalar_binary_types,
    _scalar_bool_types,
    _scalar_float_types,
    _scalar_int_types,
    _scalar_numerical_types,
    _scalar_str_types,
    _scalar_to_array_type,
    _scalar_types,
    is_array,
    is_array_type,
    is_binary,
    is_binary_type,
    is_bool,
    is_bool_type,
    is_devstate,
    is_devstate_seq,
    is_enum,
    is_enum_seq,
    is_float,
    is_float_type,
    is_int,
    is_int_type,
    is_integer,
    is_non_str_seq,
    is_number,
    is_numerical,
    is_numerical_type,
    is_pure_str,
    is_scalar,
    is_scalar_type,
    is_seq,
    is_str,
    is_str_type,
    scalar_to_array_type,
)

__all__ = (
    "TO_TANGO_TYPE",
    "AsyncEventCallback",
    "CaselessDict",
    "CaselessList",
    "EventCallback",
    "InvalidTangoHostTrlError",
    "PyTangoThread",
    "PyTangoThreadPoolExecutor",
    "StdStringVector_2_seq",
    "_clear_test_context_tango_host_fqtrl",
    "_get_command_inout_param",
    "_get_device_fqtrl_if_necessary",
    "_get_test_context_tango_host_fqtrl",
    "_set_test_context_tango_host_fqtrl",
    "dir2",
    "document_method",
    "document_static_method",
    "ensure_binary",
    "from_version_str_to_hex_str",
    "from_version_str_to_int",
    "get_home",
    "get_telemetry_tracer_provider_factory",
    "is_array_type",
    "is_binary_type",
    "is_bool_type",
    "is_float_type",
    "is_int_type",
    "is_integer",
    "is_non_str_seq",
    "is_number",
    "is_numerical_type",
    "is_pure_str",
    "is_scalar_type",
    "is_seq",
    "is_str_type",
    "obj_2_str",
    "parameter_2_dbdata",
    "parse_type_hint",
    "requires_pytango",
    "requires_tango",
    "scalar_to_array_type",
    "seqStr_2_obj",
    "seq_2_StdStringVector",
    "set_telemetry_tracer_provider_factory",
)

__docformat__ = "restructuredtext"
