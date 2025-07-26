/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "precompiled_header.hpp"
#include "defs.h"
#include "pyutils.h"

bopy::object from_char_to_boost_str(const std::string &in,
                                    const char *encoding /*=NULL defaults to latin-1 */,
                                    const char *errors /*="strict" */)
{
    return from_char_to_boost_str(in.c_str(), in.size(), encoding, errors);
}

bopy::object from_char_to_boost_str(const char *in,
                                    Py_ssize_t size /* =-1 */,
                                    const char *encoding /*=NULL defaults to latin-1 */,
                                    const char *errors /*="strict" */)
{
    return bopy::object(bopy::handle<>(from_char_to_python_str(in, size, encoding, errors)));
}

PyObject *from_char_to_python_str(const std::string &in,
                                  const char *encoding /*=NULL defaults to latin-1 */,
                                  const char *errors /*="strict" */)
{
    return from_char_to_python_str(in.c_str(), in.size(), encoding, errors);
}

PyObject *from_char_to_python_str(const char *in,
                                  Py_ssize_t size /* =-1 */,
                                  const char *encoding /*=NULL defaults to latin-1 */,
                                  const char *errors /*="strict" */)
{
    if(size < 0)
    {
        size = strlen(in);
    }
    if(!encoding)
    {
        return PyUnicode_DecodeLatin1(in, size, errors);
    }
    else
    {
        return PyUnicode_Decode(in, size, encoding, errors);
    }
}

void throw_bad_type(const char *type, const char *source)
{
    TangoSys_OMemStream description;
    description << "Incompatible argument type, expected type is : Tango::" << type << std::ends;

    TangoSys_OMemStream origin;
    origin << source << std::ends;

    Tango::Except::throw_exception("API_IncompatibleCmdArgumentType", description.str(), origin.str());
}

char *__copy_bytes_to_char(PyObject *in, Py_ssize_t *size)
{
    Py_buffer view;

    if(PyObject_GetBuffer(in, &view, PyBUF_FULL_RO) < 0)
    {
        raise_(PyExc_TypeError, "Can't translate python object to C char* - PyObject_GetBuffer failed");
    }

    *size = view.len;
    char *out = new char[*size + 1];
    out[*size] = '\0';
    memcpy(out, (char *) view.buf, *size);

    PyBuffer_Release(&view);

    return out;
}

char *from_str_to_char(const bopy::object &in)
{
    Py_ssize_t size;
    return from_str_to_char(in.ptr(), &size);
}

char *from_str_to_char(PyObject *in)
{
    Py_ssize_t size;
    return from_str_to_char(in, &size);
}

char *from_str_to_char(const bopy::object &in, Py_ssize_t *size_out, const bool utf_encoding)
{
    return from_str_to_char(in.ptr(), size_out, utf_encoding);
}

// The result is a newly allocated buffer. It is the responsibility
// of the caller to manage the memory returned by this function
char *from_str_to_char(PyObject *in, Py_ssize_t *size_out, const bool utf_encoding)
{
    char *out = NULL;
    if(PyUnicode_Check(in))
    {
        PyObject *bytes_in;
        if(utf_encoding)
        {
            bytes_in = PyUnicode_AsUTF8String(in);
        }
        else
        {
            bytes_in = EncodeAsLatin1(in);
        }
        out = __copy_bytes_to_char(bytes_in, size_out);
        Py_DECREF(bytes_in);
    }
    else if(PyBytes_Check(in) || PyByteArray_Check(in))
    {
        out = __copy_bytes_to_char(in, size_out);
    }
    else
    {
        raise_(PyExc_TypeError, "can't translate python object to C char*");
    }
    return out;
}

// The out_array will be updated with a pointer to existing memory (e.g., Python's internal memory for
// a byte array). The caller gets a "view" of the memory and must not modify the memory.
void view_pybytes_as_char_array(const bopy::object &py_value, Tango::DevVarCharArray &out_array)
{
    CORBA::ULong nb;
    PyObject *data_ptr = py_value.ptr();

    if(PyUnicode_Check(data_ptr))
    {
        Py_ssize_t size;
        CORBA::Octet *encoded_data = (CORBA::Octet *) PyUnicode_AsUTF8AndSize(data_ptr, &size);
        nb = static_cast<CORBA::ULong>(size);
        out_array.replace(nb, nb, encoded_data, false);
    }

    else if(PyBytes_Check(data_ptr))
    {
        nb = static_cast<CORBA::ULong>(bopy::len(py_value));
        CORBA::Octet *encoded_data = (CORBA::Octet *) PyBytes_AsString(data_ptr);
        out_array.replace(nb, nb, encoded_data, false);
    }
    else if(PyByteArray_Check(data_ptr))
    {
        nb = static_cast<CORBA::ULong>(bopy::len(py_value));
        CORBA::Octet *encoded_data = (CORBA::Octet *) PyByteArray_AsString(data_ptr);
        out_array.replace(nb, nb, encoded_data, false);
    }
    else
    {
        throw_bad_type(Tango::CmdArgTypeName[Tango::DEV_ENCODED], TANGO_EXCEPTION_ORIGIN);
    }
}

bool is_method_defined(bopy::object &obj, const std::string &method_name)
{
    return is_method_defined(obj.ptr(), method_name);
}

bool is_method_defined(PyObject *obj, const std::string &method_name)
{
    bool exists, is_method;
    is_method_defined(obj, method_name, exists, is_method);
    return exists && is_method;
}

void is_method_defined(bopy::object &obj, const std::string &method_name, bool &exists, bool &is_method)
{
    is_method_defined(obj.ptr(), method_name, exists, is_method);
}

void is_method_defined(PyObject *obj, const std::string &method_name, bool &exists, bool &is_method)
{
    exists = is_method = false;

    PyObject *meth = PyObject_GetAttrString_(obj, method_name.c_str());

    exists = NULL != meth;

    if(!exists)
    {
        PyErr_Clear();
        return;
    }

    is_method = (1 == PyCallable_Check(meth));
    Py_DECREF(meth);
}

#ifdef PYCAPSULE_OLD

int PyCapsule_SetName(PyObject *capsule, const char *unused)
{
    unused = unused;
    PyErr_SetString(PyExc_NotImplementedError, "can't use PyCapsule_SetName with CObjects");
    return 1;
}

void *PyCapsule_Import(const char *name, int no_block)
{
    PyObject *object = NULL;
    void *return_value = NULL;
    char *trace;
    size_t name_length = (strlen(name) + 1) * sizeof(char);
    char *name_dup = (char *) PyMem_MALLOC(name_length);

    if(!name_dup)
    {
        return NULL;
    }

    memcpy(name_dup, name, name_length);

    trace = name_dup;
    while(trace)
    {
        char *dot = strchr(trace, '.');
        if(dot)
        {
            *dot++ = '\0';
        }

        if(object == NULL)
        {
            if(no_block)
            {
                object = PyImport_ImportModuleNoBlock(trace);
            }
            else
            {
                object = PyImport_ImportModule(trace);
                if(!object)
                {
                    PyErr_Format(PyExc_ImportError,
                                 "PyCapsule_Import could not "
                                 "import module \"%s\"",
                                 trace);
                }
            }
        }
        else
        {
            PyObject *object2 = PyObject_GetAttrString(object, trace);
            Py_DECREF(object);
            object = object2;
        }
        if(!object)
        {
            goto EXIT;
        }

        trace = dot;
    }

    if(PyCObject_Check(object))
    {
        PyCObject *cobject = (PyCObject *) object;
        return_value = cobject->cobject;
    }
    else
    {
        PyErr_Format(PyExc_AttributeError, "PyCapsule_Import \"%s\" is not valid", name);
    }

EXIT:
    Py_XDECREF(object);
    if(name_dup)
    {
        PyMem_FREE(name_dup);
    }
    return return_value;
}

#endif

bool hasattr(bopy::object &obj, const std::string &name)
{
    return PyObject_HasAttrString(obj.ptr(), name.c_str());
}

void export_ensure_omni_thread()
{
    bopy::class_<EnsureOmniThread, boost::noncopyable>("EnsureOmniThread", bopy::init<>())
        .def("_acquire", &EnsureOmniThread::acquire)
        .def("_release", &EnsureOmniThread::release);
    bopy::def("is_omni_thread", is_omni_thread);
}

#if defined(TANGO_USE_TELEMETRY)
// I.e., cppTango is compiled with telemetry support.

  #include <opentelemetry/sdk/common/global_log_handler.h>

namespace otel_log = opentelemetry::sdk::common::internal_log;

void set_log_level(std::string level_str)
{
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
    if(it != level_map.end())
    {
        otel_log::GlobalLogHandler::SetLogLevel(it->second);
    }
    // else ignore request, leaving default log level
}

Tango::telemetry::InterfacePtr telemetry_interface{nullptr};
bool shutdown{false};

void ensure_default_telemetry_interface_initialized()
{
    if(shutdown)
    {
        return;
    }

    if(!telemetry_interface)
    {
        std::string client_name;
        if(Tango::ApiUtil::get_env_var("PYTANGO_TELEMETRY_CLIENT_SERVICE_NAME", client_name) != 0)
        {
            client_name = "pytango.client";
        }
        std::string name_space{"tango"};
        auto details = Tango::telemetry::Configuration::Client{client_name};
        Tango::telemetry::Configuration cfg{client_name, name_space, details};
        telemetry_interface = Tango::telemetry::InterfaceFactory::create(cfg);
    }
    // else: we already made our custom interface singleton.

    auto span = Tango::telemetry::Interface::get_current();
    if(span->is_default())
    {
        // Make our client interface active (applies to current thread only, as cppTango uses a thread_local variable)
        Tango::telemetry::Interface::set_current(telemetry_interface);
    }
    // else: a non-default interface is either from a device, or we already set our client interface for this thread.
}

void cleanup_default_telemetry_interface()
{
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
bopy::dict get_trace_context()
{
    ensure_default_telemetry_interface_initialized();

    std::string trace_parent;
    std::string trace_state;
    Tango::telemetry::Interface::get_trace_context(trace_parent, trace_state);

    bopy::dict carrier;
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
class TraceContextScope
{
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
        trace_state{trace_state_}
    {
    }

    void acquire()
    {
        if(scope == nullptr && !shutdown)
        {
            ensure_default_telemetry_interface_initialized();
            scope = Tango::telemetry::Interface::set_trace_context(
                new_span_name, trace_parent, trace_state, Tango::telemetry::Span::Kind::kClient);
        }
    }

    void release()
    {
        scope = nullptr;
    }

    ~TraceContextScope()
    {
        release();
    }
};

#else
// cppTango is *not* compiled with telemetry support.
// We use no-op handlers, so the Python code can run without errors but does nothing.

void no_op_cleanup() { }

void no_op_set_log_level(std::string level_str) { }

bopy::dict no_op_get_trace_context()
{
    bopy::dict carrier;
    carrier["traceparent"] = "";
    carrier["tracestate"] = "";
    return carrier;
}

class NoOpTraceContextScope
{
  public:
    NoOpTraceContextScope(const std::string &new_span_name_,
                          const std::string &trace_parent_,
                          const std::string &trace_state_)
    {
    }

    void acquire() { }

    void release() { }

    ~NoOpTraceContextScope() { }
};

#endif

void export_telemetry_helpers()
{
    bopy::object telemetry_module(bopy::handle<>(bopy::borrowed(PyImport_AddModule("tango._telemetry"))));
    bopy::scope().attr("_telemetry") = telemetry_module;
    bopy::scope telemetry_scope = telemetry_module;

#if defined(TANGO_USE_TELEMETRY)
    telemetry_scope.attr("TELEMETRY_ENABLED") = true;
    bopy::def("get_trace_context", get_trace_context);
    bopy::def("cleanup_default_telemetry_interface", &cleanup_default_telemetry_interface);
    bopy::def("set_log_level", &set_log_level);
    bopy::class_<TraceContextScope, boost::noncopyable>(
        "TraceContextScope", bopy::init<const std::string &, const std::string &, const std::string &>())
        .def("_acquire", &TraceContextScope::acquire)
        .def("_release", &TraceContextScope::release);
#else
    bopy::def("get_trace_context", no_op_get_trace_context);
    bopy::def("cleanup_default_telemetry_interface", &no_op_cleanup);
    bopy::def("set_log_level", &no_op_set_log_level);
    bopy::class_<NoOpTraceContextScope, boost::noncopyable>(
        "TraceContextScope", bopy::init<const std::string &, const std::string &, const std::string &>())
        .def("_acquire", &NoOpTraceContextScope::acquire)
        .def("_release", &NoOpTraceContextScope::release);
#endif
}
