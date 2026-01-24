/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#if defined(TANGO_USE_TELEMETRY)
// I.e., cppTango is compiled with telemetry support.

  #include <opentelemetry/sdk/common/global_log_handler.h>

namespace otel_log = opentelemetry::sdk::common::internal_log;

void set_log_level(std::string level_str) {
    std::transform(level_str.begin(), level_str.end(), level_str.begin(), ::toupper);

    static const std::unordered_map<std::string, otel_log::LogLevel> level_map = {
        {"NONE", otel_log::LogLevel::None},
        {"CRITICAL", otel_log::LogLevel::None},
        {"FATAL", otel_log::LogLevel::None},
        {"ERROR", otel_log::LogLevel::Error},
        {"WARNING", otel_log::LogLevel::Warning},
        {"INFO", otel_log::LogLevel::Info},
        {"DEBUG", otel_log::LogLevel::Debug}};

    auto it = level_map.find(level_str);
    if(it != level_map.end()) {
        otel_log::GlobalLogHandler::SetLogLevel(it->second);
    }
    // else ignore request, leaving default log level
}

Tango::telemetry::InterfacePtr telemetry_interface{nullptr};
bool shutdown{false};

void ensure_default_telemetry_interface_initialized() {
    if(shutdown) {
        return;
    }

    if(!telemetry_interface) {
        std::string client_name;
        if(Tango::ApiUtil::get_env_var("PYTANGO_TELEMETRY_CLIENT_SERVICE_NAME", client_name) != 0) {
            client_name = "pytango.client";
        }
        std::string name_space{"tango"};
        auto details = Tango::telemetry::Configuration::Client{client_name};
        Tango::telemetry::Configuration cfg{client_name, name_space, details};
        telemetry_interface = Tango::telemetry::InterfaceFactory::create(cfg);
    }
    // else: we already made our custom interface singleton.

    auto span = Tango::telemetry::Interface::get_current();
    if(span->is_default()) {
        // Make our client interface active (applies to current thread only, as cppTango uses a thread_local variable)
        Tango::telemetry::Interface::set_current(telemetry_interface);
    }
    // else: a non-default interface is either from a device, or we already set our client interface for this thread.
}

void cleanup_default_telemetry_interface() {
    // Ensure we release the telemetry interface object at shutdown time.  Hopefully, this happens before
    // OpenSSL's atexit handler starts cleaning up.  This is important if we are sending traces to an
    // https endpoint.  We need to flush any outstanding traces before shutting down
    shutdown = true;
    telemetry_interface = nullptr;
}

/*
 * Get the current trace context (from cppTango, to be used in PyTango).
 *
 * This function is used to propagate the trace context, fetching it from the cppTango kernel context,
 * The trace context is obtained in its W3C format as a dict of strings, with keys: "traceparent" and "tracestate".
 *
 * For details of the W3C format see: https://www.w3.org/TR/trace-context/
 */
py::dict get_trace_context() {
    ensure_default_telemetry_interface_initialized();

    std::string trace_parent;
    std::string trace_state;
    Tango::telemetry::Interface::get_trace_context(trace_parent, trace_state);

    py::dict carrier;
    carrier["traceparent"] = trace_parent;
    carrier["tracestate"] = trace_state;
    return carrier;
}

/*
 * Set the trace context (from PyTango to cppTango)
 *
 * This class is used to propagate trace context, writing the Python context into cppTango's telemetry context using
 * the two strings passed as constructor arguments (trace_parent & trace_state) in W3C format. A new span, with
 * the name specified by the "new_span_name" argument will be created when then acquire() method is called.
 * We have an acquire() method and a release() method so that this class can be used with a Python context handler.
 * Entering the context handler must call acquire(), which activates the scope in cppTango.  Exiting the context
 * handler must call release(), thus ending the scope (and associated span), and returning cppTango's context to
 * whatever it was before.  The restoration of the scope happens automatically when the scope pointer is released,
 * and the underlying cppTango object destroyed.
 *
 * For details of the W3C format see: https://www.w3.org/TR/trace-context/
 */
class TraceContextScope {
    Tango::telemetry::ScopePtr scope;
    const std::string new_span_name;
    std::string trace_parent;
    std::string trace_state;

  public:
    TraceContextScope(const std::string &new_span_name_,
                      const std::string &trace_parent_,
                      const std::string &trace_state_) :
        new_span_name{new_span_name_},
        trace_parent{trace_parent_},
        trace_state{trace_state_} {
    }

    void acquire() {
        if(scope == nullptr && !shutdown) {
            ensure_default_telemetry_interface_initialized();
            scope = Tango::telemetry::Interface::set_trace_context(
                new_span_name, trace_parent, trace_state, Tango::telemetry::Span::Kind::kClient);
        }
    }

    void release() {
        scope = nullptr;
    }

    ~TraceContextScope() {
        release();
    }
};

#else
// cppTango is *not* compiled with telemetry support.
// We use no-op handlers, so the Python code can run without errors but does nothing.

void no_op_cleanup() {
}

void no_op_set_log_level([[maybe_unused]] std::string level_str) { }

py::dict no_op_get_trace_context() {
    py::dict carrier;
    carrier["traceparent"] = "";
    carrier["tracestate"] = "";
    return carrier;
}

class NoOpTraceContextScope {
  public:
    NoOpTraceContextScope([[maybe_unused]] const std::string &new_span_name_,
                          [[maybe_unused]] const std::string &trace_parent_,
                          [[maybe_unused]] const std::string &trace_state_) {
    }

    void acquire() { }

    void release() { }

    ~NoOpTraceContextScope() { }
};

#endif

void export_telemetry_helpers(py::module_ &m) {
    py::module telemetry_module = m.def_submodule("_telemetry");

#if defined(TANGO_USE_TELEMETRY)
    telemetry_module.attr("TELEMETRY_ENABLED") = true;
    telemetry_module.def("get_trace_context", &get_trace_context);
    telemetry_module.def("cleanup_default_telemetry_interface", &cleanup_default_telemetry_interface);
    telemetry_module.def("set_log_level", &set_log_level);

    py::class_<TraceContextScope>(telemetry_module,
                                  "TraceContextScope",
                                  R"doc(
            Internal - for telemetry tracing purposes.

            Used to propagate the Python OpenTelemetry context to the cppTango telemetry context.
            When the context handler is entered, a new span is created.  During this process, the
            the current cppTango context is stored before the new span is set as the active scope.
            When the context handler exists, the span ends and the old context is restored at the
            C++ level.

            trace_parent and trace_state strings encoded as per the W3C standard: https://www.w3.org/TR/trace-context/

            with tango._telemetry.TraceContextScope(new_span_name, trace_parent, trace_state):
                x = proxy.read_attribute("foo")

            This is a no-op if telemetry support isn't compiled into cppTango (check tango.constants.TANGO_USE_TELEMETRY)

            .. versionadded:: 10.0.0)doc")
        .def(py::init<const std::string &, const std::string &, const std::string &>())
        .def("_acquire", &TraceContextScope::acquire)
        .def("_release", &TraceContextScope::release);
#else
    telemetry_module.attr("TELEMETRY_ENABLED") = false;
    telemetry_module.def("get_trace_context", &no_op_get_trace_context);
    telemetry_module.def("cleanup_default_telemetry_interface", &no_op_cleanup);
    telemetry_module.def("set_log_level", &no_op_set_log_level);

    py::class_<NoOpTraceContextScope>(telemetry_module, "TraceContextScope")
        .def(py::init<const std::string &, const std::string &, const std::string &>())
        .def("_acquire", &NoOpTraceContextScope::acquire)
        .def("_release", &NoOpTraceContextScope::release);
#endif
}
