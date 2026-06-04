/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "convertors/generic_to_py.h"
#include "convertors/generic_from_py.h"

extern py::object PyTango_DevFailed;

PYBIND11_MAKE_OPAQUE(StdStringVector)
PYBIND11_MAKE_OPAQUE(StdLongVector)
PYBIND11_MAKE_OPAQUE(StdDoubleVector)

PYBIND11_MAKE_OPAQUE(Tango::CommandInfoList)
PYBIND11_MAKE_OPAQUE(Tango::AttributeInfoList)
PYBIND11_MAKE_OPAQUE(Tango::AttributeInfoListEx)

PYBIND11_MAKE_OPAQUE(Tango::EventDataList)
PYBIND11_MAKE_OPAQUE(Tango::DbData)
PYBIND11_MAKE_OPAQUE(Tango::DbDevInfos)
PYBIND11_MAKE_OPAQUE(Tango::DbDevExportInfos)
PYBIND11_MAKE_OPAQUE(Tango::DbDevImportInfos)

PYBIND11_MAKE_OPAQUE(std::vector<Tango::DbHistory>)
PYBIND11_MAKE_OPAQUE(std::vector<Tango::DeviceData>)
PYBIND11_MAKE_OPAQUE(Tango::DeviceDataHistoryList)
PYBIND11_MAKE_OPAQUE(StdNamedDevFailedVector)

template <typename T>
class LeakingSmartPtr {
  public:
    LeakingSmartPtr(T *ptr) :
        m_ptr(ptr) {
        TANGO_LOG_DEBUG << "LeakingSmartPtr constructor" << std::endl;
    }

    ~LeakingSmartPtr() {
        TANGO_LOG_DEBUG << "LeakingSmartPtr destructor" << std::endl;
    }

    T *get() const {
        return m_ptr;
    }

  private:
    T *m_ptr;
};

// cppcheck-suppress unknownMacro
PYBIND11_DECLARE_HOLDER_TYPE(T, LeakingSmartPtr<T>, false)

template <typename CorbaContainerType>
bool generic_sequence_caster_load(py::handle &src, CorbaContainerType &result) {
    if(py::isinstance<py::str>(src) || !py::isinstance<py::sequence>(src)) {
        return false;
    }

    py::list py_list;
    try {
        py_list = py::reinterpret_borrow<py::list>(src);
    } catch(const py::cast_error &) {
        return false; // Cannot cast to list
    }

    python_seq_to_tango(py_list, result);
    return true;
}

namespace pybind11::detail {

template <>
struct type_caster<Tango::DevVarCharArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarCharArray, _("list[str]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarCharArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarShortArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarShortArray, _("list[int]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarShortArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarLongArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarLongArray, _("list[int]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarLongArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarFloatArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarFloatArray, _("list[float]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarFloatArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarDoubleArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarDoubleArray, _("list[float]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarDoubleArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarUShortArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarUShortArray, _("list[int]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarUShortArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarULongArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarULongArray, _("list[int]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarULongArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarStringArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarStringArray, _("list[str]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarStringArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarLongStringArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarLongStringArray, _("tuple[list[int], list[str]]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarLongStringArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarDoubleStringArray> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarDoubleStringArray, _("tuple[list[float], list[str]]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarDoubleStringArray &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarLong64Array> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarLong64Array, _("list[int]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarLong64Array &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevVarULong64Array> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevVarULong64Array, _("list[int]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::DevVarULong64Array &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::DevEncoded> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevEncoded, _("DevEncoded"));

    bool load(handle src, bool) {
        python_scalar_to_cpp<Tango::DEV_ENCODED>::convert(py::reinterpret_borrow<py::object>(src), value);
        return true;
    }

    static handle cast(const Tango::DevEncoded &src, return_value_policy, handle) {
        return cpp_to_python_scalar<Tango::DEV_ENCODED>::convert(src).release();
    }
};

template <>
struct type_caster<CORBA::String_member> {
  public:
    PYBIND11_TYPE_CASTER(CORBA::String_member, _("str"));

    bool load(handle src, bool) {
        char *new_value = nullptr;
        python_scalar_to_cpp<Tango::DEV_STRING>::convert(py::reinterpret_borrow<py::object>(src), new_value);
        value = CORBA::string_dup(new_value);
        delete[] new_value;
        return true;
    }

    // Conversion from C++ to Python
    static handle cast(const CORBA::String_member &src, return_value_policy /* policy */, handle /* parent */) {
        return from_cpp_char_to_pybind11_str(src.in()).release();
    }
};

template <>
struct type_caster<_CORBA_String_element> {
  public:
    PYBIND11_TYPE_CASTER(_CORBA_String_element, _("str"));

    bool load(handle src, bool) {
        char *new_value = nullptr;
        python_scalar_to_cpp<Tango::DEV_STRING>::convert(py::reinterpret_borrow<py::object>(src), new_value);
        value = CORBA::string_dup(new_value);
        delete[] new_value;
        return true;
    }

    static handle cast(const _CORBA_String_element &src, return_value_policy /* policy */, handle /* parent */) {
        return from_cpp_char_to_pybind11_str(src.in()).release();
    }
};

template <>
struct type_caster<Tango::DevErrorList> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevErrorList, _("list[DevError]"));

    bool load(handle src, bool) {
        bool ret = generic_sequence_caster_load(src, value);
        if(!ret) {
            Tango::Except::throw_exception(static_cast<const char *>("PyDs_BadDevFailedException"),
                                           static_cast<const char *>("A badly formed exception has been received"),
                                           static_cast<const char *>("Tango::DevErrorList caster"));
        }
        return ret;
    }

    static handle cast(const Tango::DevErrorList &src, return_value_policy, handle) {
        return to_py_tuple(&src).release();
    }
};

template <>
struct type_caster<Tango::DevFailed> {
  public:
    PYBIND11_TYPE_CASTER(Tango::DevFailed, _("DevFailed"));

    bool load(handle src, bool) {
        py::object exception = py::reinterpret_borrow<py::object>(src);
        if(py::isinstance(exception, PyTango_DevFailed)) {
            value.errors = exception.attr("args").cast<Tango::DevErrorList>();
            return true;
        }
        return false;
    }

    static handle cast(const Tango::DevFailed &src, return_value_policy, handle) {
        py::tuple py_errors = py::cast(src.errors);
        py::object exception_instance = PyTango_DevFailed(*py_errors);
        return exception_instance.release();
    }
};

template <>
struct type_caster<Tango::AttributeConfigList> {
  public:
    PYBIND11_TYPE_CASTER(Tango::AttributeConfigList, _("list[AttributeConfig]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::AttributeConfigList &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::AttributeConfigList_2> {
  public:
    PYBIND11_TYPE_CASTER(Tango::AttributeConfigList_2, _("list[AttributeConfig_2]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::AttributeConfigList_2 &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::AttributeConfigList_3> {
  public:
    PYBIND11_TYPE_CASTER(Tango::AttributeConfigList_3, _("list[AttributeConfig_3]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::AttributeConfigList_3 &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<Tango::AttributeConfigList_5> {
  public:
    PYBIND11_TYPE_CASTER(Tango::AttributeConfigList_5, _("list[AttributeConfig_5]"));

    bool load(handle src, bool) {
        return generic_sequence_caster_load(src, value);
    }

    static handle cast(const Tango::AttributeConfigList_5 &src, return_value_policy, handle) {
        return to_py_list(&src).release();
    }
};

template <>
struct type_caster<std::vector<Tango::Attr *>> {
  public:
    PYBIND11_TYPE_CASTER(std::vector<Tango::Attr *>, _("tuple[Attr]"));

    bool load([[maybe_unused]] handle src, [[maybe_unused]] bool) {
        return false;
    }

    static handle cast(const std::vector<Tango::Attr *> &src, return_value_policy policy, handle parent) {
        py::tuple t(src.size());
        for(size_t i = 0; i < src.size(); ++i) {
            t[i] = py::cast(src[i], policy, parent);
        }
        return t.release();
    }
};

template <>
struct type_caster<std::vector<Tango::Attribute *>> {
  public:
    PYBIND11_TYPE_CASTER(std::vector<Tango::Attribute *>, _("tuple[Attribute]"));

    bool load([[maybe_unused]] handle src, [[maybe_unused]] bool) {
        return false;
    }

    static handle cast(const std::vector<Tango::Attribute *> &src, return_value_policy policy, handle parent) {
        py::tuple t(src.size());
        for(size_t i = 0; i < src.size(); ++i) {
            t[i] = py::cast(src[i], policy, parent);
        }
        return t.release();
    }
};

#if defined(PYTANGO_USE_TELEMETRY)

template <>
struct type_caster<Tango::telemetry::Configuration::Collector> {
  public:
    // Collector is not default-constructible, so we cannot use PYBIND11_TYPE_CASTER
    // here because it declares an in-place `value` member of the target type.

    using Collector = Tango::telemetry::Configuration::Collector;
    using Exporter = Tango::telemetry::Configuration::Exporter;

    static constexpr auto name = _("TelemetryEndpoint");

    std::unique_ptr<Collector> value;

    static Exporter exporter_from_python(handle src) {
        auto exporter_name = py::reinterpret_borrow<py::object>(src).attr("name").cast<std::string>();
        if(exporter_name == "GRPC") {
            return Exporter::grpc;
        }
        if(exporter_name == "HTTP") {
            return Exporter::http;
        }
        if(exporter_name == "CONSOLE") {
            return Exporter::console;
        }
        throw py::cast_error("unsupported telemetry exporter: " + exporter_name);
    }

    static const char *exporter_name(Exporter exporter) {
        switch(exporter) {
        case Exporter::grpc:
            return "GRPC";
        case Exporter::http:
            return "HTTP";
        case Exporter::console:
            return "CONSOLE";
        }
        throw py::cast_error("unsupported telemetry exporter");
    }

    bool load(handle src, bool) {
        if(!py::hasattr(src, "exporter") || !py::hasattr(src, "endpoint")) {
            return false;
        }
        value =
            std::make_unique<Collector>(exporter_from_python(py::reinterpret_borrow<py::object>(src).attr("exporter")),
                                        py::reinterpret_borrow<py::object>(src).attr("endpoint").cast<std::string>());
        return true;
    }

    template <
        typename T_,
        ::pybind11::detail::enable_if_t<std::is_same<Collector, ::pybind11::detail::remove_cv_t<T_>>::value, int> = 0>
    static handle cast(T_ *src, return_value_policy policy, handle parent) {
        if(!src) {
            return py::none().release();
        }
        if(policy == return_value_policy::take_ownership) {
            auto h = cast(std::move(*src), policy, parent);
            delete src;
            return h;
        }
        return cast(*src, policy, parent);
    }

    operator Collector *() {
        return value.get();
    }

    operator Collector &() {
        return *value;
    }

    operator Collector &&() && {
        return std::move(*value);
    }

    template <typename T_>
    using cast_op_type = ::pybind11::detail::movable_cast_op_type<T_>;

    static handle cast(const Collector &src, return_value_policy, handle) {
        py::object telemetry_module = py::module_::import("tango.telemetry");
        py::object telemetry_exporter = telemetry_module.attr("TelemetryExporter");
        py::object telemetry_endpoint = telemetry_module.attr("TelemetryEndpoint");
        return telemetry_endpoint(telemetry_exporter[exporter_name(src.exporter_type)], py::cast(src.endpoint))
            .release();
    }
};

#endif

} // namespace pybind11::detail
