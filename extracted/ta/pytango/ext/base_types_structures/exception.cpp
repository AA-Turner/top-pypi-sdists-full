/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "base_types_structures/exception.h"

py::object PyTango_DevFailed;

namespace Tango {
inline bool operator==(const Tango::NamedDevFailed &df1, const Tango::NamedDevFailed &df2) {
    /// @todo ? err_stack ?
    return (df1.name == df2.name) && (df1.idx_in_call == df2.idx_in_call);
}
} // namespace Tango

Tango::DevFailed convert_to_dev_failed(PyObject *type, PyObject *value, PyObject *traceback) {
    PyErr_NormalizeException(&type, &value, &traceback);

    Tango::DevErrorList dev_err;
    dev_err.length(1);

    if(value == nullptr) {
        //
        // Send a default exception in case Python does not send us information
        //
        dev_err[0].origin = CORBA::string_dup("Py_to_dev_failed");
        dev_err[0].desc = CORBA::string_dup("A badly formed exception has been received");
        dev_err[0].reason = CORBA::string_dup("PyDs_BadPythonException");
        dev_err[0].severity = Tango::ERR;
    } else {
        //
        // Populate a one level DevFailed exception
        //

        PyObject *tracebackModule = PyImport_ImportModule("traceback");
        if(tracebackModule != nullptr) {
            //
            // Format the traceback part of the Python exception
            // and store it in the origin part of the Tango exception
            //

            PyObject *tbList_ptr = PyObject_CallMethod(tracebackModule,
                                                       const_cast<char *>("format_exception"),
                                                       const_cast<char *>("OOO"),
                                                       type,
                                                       value,
                                                       traceback);

            try {
                py::object tbList = py::reinterpret_borrow<py::object>(tbList_ptr);
                py::str origin = py::str("").attr("join")(tbList);
                std::string origin_str = origin.cast<std::string>();
                dev_err[0].origin = CORBA::string_dup(origin_str.c_str());
            } catch(...) {
                dev_err[0].origin = CORBA::string_dup("UNKNOWN: cannot get Python's traceback. "
                                                      "Most probably, was a failure in c++ bindings");
            }

            //
            // Format the exec and value part of the Python exception
            // and store it in the desc part of the Tango exception
            //

            tbList_ptr = PyObject_CallMethod(tracebackModule,
                                             const_cast<char *>("format_exception_only"),
                                             const_cast<char *>("OO"),
                                             type,
                                             value == nullptr ? Py_None : value);

            py::object tbList = py::reinterpret_borrow<py::object>(tbList_ptr);
            py::str desc = py::str("").attr("join")(tbList);
            std::string desc_str = desc.cast<std::string>();
            dev_err[0].desc = CORBA::string_dup(desc_str.c_str());

            Py_DECREF(tracebackModule);

            dev_err[0].reason = CORBA::string_dup("PyDs_PythonError");
            dev_err[0].severity = Tango::ERR;
        } else {
            //
            // Send a default exception because we can't format the
            // different parts of the Python's one !
            //

            dev_err[0].origin = CORBA::string_dup("Py_to_dev_failed");
            dev_err[0].desc =
                CORBA::string_dup("Can't import Python traceback module. Can't extract info from Python exception");
            dev_err[0].reason = CORBA::string_dup("PyDs_PythonError");
            dev_err[0].severity = Tango::ERR;
        }
    }

    return Tango::DevFailed(dev_err);
}

// translates Python's exceptions to Tango::DevFailed
Tango::DevFailed to_dev_failed(PyObject *type, PyObject *value, PyObject *traceback) {
    bool from_fetch = false;
    if((type == nullptr) || (value == nullptr) || (traceback == nullptr) || (type == Py_None) || (value == Py_None) ||
       (traceback == Py_None)) {
        PyErr_Fetch(&type, &value, &traceback);
        PyErr_NormalizeException(&type, &value, &traceback);
        from_fetch = true;
    }

    Tango::DevFailed df = convert_to_dev_failed(type, value, traceback);

    if(from_fetch) {
        Py_XDECREF(type);
        Py_XDECREF(value);
        Py_XDECREF(traceback);
    }
    return df;
}

void handle_python_exception(py::error_already_set &eas,
                             const std::string &reason,
                             const std::string &desc,
                             const std::string &origin) {
    py::object exc_value = eas.value();

    Tango::DevFailed df;

    try {
        df = exc_value.cast<Tango::DevFailed>();
    } catch([[maybe_unused]] const py::cast_error &e) {
        py::object exc_type = eas.type();
        py::object exc_traceback = eas.trace();
        df = convert_to_dev_failed(exc_type.ptr(), exc_value.ptr(), exc_traceback.ptr());
    }

    if(origin != "" || desc != "" || reason != "") {
        _CORBA_ULong nb_err = df.errors.length();
        df.errors.length(nb_err + 1);
        df.errors[nb_err].reason = CORBA::string_dup(reason.c_str());
        df.errors[nb_err].desc = CORBA::string_dup(desc.c_str());
        df.errors[nb_err].origin = CORBA::string_dup(origin.c_str());
        df.errors[nb_err].severity = Tango::ERR;
    }

    throw df;
}

// from cpp exception to python
void translate_dev_failed(const Tango::DevFailed &dev_failed, py::object py_dev_failed) {
    py::object py_errors = py::cast(dev_failed.errors);
    PyErr_SetObject(py_dev_failed.ptr(), py_errors.ptr());
}

void export_exceptions(py::module_ &m) {
    py::class_<Tango::DevError>(m,
                                "DevError",
                                R"doc(
                                Structure describing any error resulting from a command execution,
                                or an attribute query, with following members:

                                    - reason : (str) reason
                                    - severity : (ErrSeverity) error severity (WARN, ERR, PANIC)
                                    - desc : (str) error description
                                    - origin : (str) Tango server method in which the error happened
                                )doc")
        .def(py::init<>())

        .def(py::pickle(
            [](const Tango::DevError &self) { // __getstate__
                return py::make_tuple(self.reason, self.desc, self.origin, self.severity);
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 4) {
                    throw std::runtime_error("Invalid state!");
                }

                Tango::DevError dev_error;

                dev_error.reason = py_tuple[0].cast<std::string>().c_str();
                dev_error.desc = py_tuple[1].cast<std::string>().c_str();
                dev_error.origin = py_tuple[2].cast<std::string>().c_str();
                dev_error.severity = py_tuple[3].cast<Tango::ErrSeverity>();

                return dev_error;
            }))

        .def_readwrite("reason", &Tango::DevError::reason)
        .def_readwrite("severity", &Tango::DevError::severity)
        .def_readwrite("desc", &Tango::DevError::desc)
        .def_readwrite("origin", &Tango::DevError::origin);

    // make a new custom exception and use it as a translation target
    static py::exception<Tango::DevFailed> DevFailed(m, "DevFailed");
    m.attr("DevFailed") = DevFailed;

    /*
        now we assign new python exception (ony base one) to the py::object, which will be later used in
        Tango::DevFailed caster. Casters are made before we create an exception class,
        so we first create caster with dummy py::object, which we then re-assign at run-time to new exception
    */
    PyTango_DevFailed = DevFailed;

    static py::exception<Tango::ConnectionFailed> ConnectionFailed(m, "ConnectionFailed", DevFailed.ptr());
    m.attr("ConnectionFailed") = ConnectionFailed;

    static py::exception<Tango::CommunicationFailed> CommunicationFailed(m, "CommunicationFailed", DevFailed.ptr());
    m.attr("CommunicationFailed") = CommunicationFailed;

    static py::exception<Tango::WrongNameSyntax> WrongNameSyntax(m, "WrongNameSyntax", DevFailed.ptr());
    m.attr("WrongNameSyntax") = WrongNameSyntax;

    static py::exception<Tango::NonDbDevice> NonDbDevice(m, "NonDbDevice", DevFailed.ptr());
    m.attr("NonDbDevice") = NonDbDevice;

    static py::exception<Tango::WrongData> WrongData(m, "WrongData", DevFailed.ptr());
    m.attr("WrongData") = WrongData;

    static py::exception<Tango::NonSupportedFeature> NonSupportedFeature(m, "NonSupportedFeature", DevFailed.ptr());
    m.attr("NonSupportedFeature") = NonSupportedFeature;

    static py::exception<Tango::AsynCall> AsynCall(m, "AsynCall", DevFailed.ptr());
    m.attr("AsynCall") = AsynCall;

    static py::exception<Tango::AsynReplyNotArrived> AsynReplyNotArrived(m, "AsynReplyNotArrived", DevFailed.ptr());
    m.attr("AsynReplyNotArrived") = AsynReplyNotArrived;

    static py::exception<Tango::EventSystemFailed> EventSystemFailed(m, "EventSystemFailed", DevFailed.ptr());
    m.attr("EventSystemFailed") = EventSystemFailed;

    static py::exception<Tango::DeviceUnlocked> DeviceUnlocked(m, "DeviceUnlocked", DevFailed.ptr());
    m.attr("DeviceUnlocked") = DeviceUnlocked;

    static py::exception<Tango::NotAllowed> NotAllowed(m, "NotAllowed", DevFailed.ptr());
    m.attr("NotAllowed") = NotAllowed;

    py::register_exception_translator(
        [](std::exception_ptr p) {
            try {
                if(p) {
                    std::rethrow_exception(p);
                }
            } catch(const Tango::ConnectionFailed &e) {
                translate_dev_failed(e, ConnectionFailed);
            } catch(const Tango::CommunicationFailed &e) {
                translate_dev_failed(e, CommunicationFailed);
            } catch(const Tango::WrongNameSyntax &e) {
                translate_dev_failed(e, WrongNameSyntax);
            } catch(const Tango::NonDbDevice &e) {
                translate_dev_failed(e, NonDbDevice);
            } catch(const Tango::WrongData &e) {
                translate_dev_failed(e, WrongData);
            } catch(const Tango::NonSupportedFeature &e) {
                translate_dev_failed(e, NonSupportedFeature);
            } catch(const Tango::AsynCall &e) {
                translate_dev_failed(e, AsynCall);
            } catch(const Tango::AsynReplyNotArrived &e) {
                translate_dev_failed(e, AsynReplyNotArrived);
            } catch(const Tango::EventSystemFailed &e) {
                translate_dev_failed(e, EventSystemFailed);
            } catch(const Tango::DeviceUnlocked &e) {
                translate_dev_failed(e, DeviceUnlocked);
            } catch(const Tango::NotAllowed &e) {
                translate_dev_failed(e, NotAllowed);
            } catch(const Tango::DevFailed &e) {
                translate_dev_failed(e, DevFailed);
            }
        });

    py::class_<Tango::Except>(m,
                              "Except",
                              R"doc(
                              A container for the static methods:

                                - throw_exception
                                - re_throw_exception
                                - print_exception
                                - compare_exception
                              )doc")
        .def_static(
            "throw_exception",
            [](const std::string &reason,
               const std::string &description,
               const std::string &origin,
               Tango::ErrSeverity severity) { Tango::Except::throw_exception(reason, description, origin, severity); },
            R"doc(
                    throw_exception(reason, desc, origin, sever=tango.ErrSeverity.ERR) -> None

                        Generate and throw a TANGO DevFailed exception.
                        The exception is created with a single :class:`~tango.DevError`
                        object. A default value *tango.ErrSeverity.ERR* is defined for
                        the :class:`~tango.DevError` severity field.

                    Parameters :
                        - reason   : (str) The exception :class:`~tango.DevError` object reason field
                        - desc     : (str) The exception :class:`~tango.DevError` object desc field
                        - origin   : (str) The exception :class:`~tango.DevError` object origin field
                        - severity : (tango.ErrSeverity) The exception DevError object severity field

                    Throws : DevFailed
               )doc",
            py::arg("reason"),
            py::arg("description"),
            py::arg("origin"),
            py::arg("severity") = Tango::ERR)

        .def_static(
            "re_throw_exception",
            [](Tango::DevFailed &exception,
               const std::string &reason,
               const std::string &description,
               const std::string &origin,
               Tango::ErrSeverity severity) { Tango::Except::re_throw_exception(exception, reason, description, origin, severity); },
            R"doc(
                re_throw_exception(ex, reason, desc, origin, sever=tango.ErrSeverity.ERR) -> None

                        Re-throw a TANGO :class:`~tango.DevFailed` exception with one more error.
                        The exception is re-thrown with one more :class:`~tango.DevError` object.
                        A default value *tango.ErrSeverity.ERR* is defined for the new
                        :class:`~tango.DevError` severity field.

                    Parameters :
                        - ex       : (tango.DevFailed) The :class:`~tango.DevFailed` exception
                        - reason   : (str) The exception :class:`~tango.DevError` object reason field
                        - desc     : (str) The exception :class:`~tango.DevError` object desc field
                        - origin   : (str) The exception :class:`~tango.DevError` object origin field
                        - severity : (tango.ErrSeverity) The exception DevError object severity field

                    Throws     : DevFailed
            )doc",
            py::arg("exception"),
            py::arg("reason"),
            py::arg("description"),
            py::arg("origin"),
            py::arg("severity") = Tango::ERR)

        .def_static("print_error_stack",
                    py::overload_cast<const Tango::DevErrorList &>(&Tango::Except::print_error_stack),
                    R"doc(
                        print_error_stack(ex) -> None

                        Print all the details of a TANGO error stack.

                        Parameters :
                        - ex     : (tango.DevErrorList) The error stack reference)
                    )doc")

        .def_static("compare_exception", &Tango::Except::compare_exception)

        .def_static(
            "to_dev_failed",
            [](py::object type,
               py::object value,
               py::object traceback) { return to_dev_failed(type.ptr(), value.ptr(), traceback.ptr()); },
            py::arg("type") = py::none(),
            py::arg("value") = py::none(),
            py::arg("traceback") = py::none())

        .def_static(
            "throw_python_exception",
            [](py::object type,
               py::object value,
               py::object traceback) { throw to_dev_failed(type.ptr(), value.ptr(), traceback.ptr()); },
            R"doc(
                throw_python_exception(type, value, traceback) -> None

                    Generate and throw a TANGO DevFailed exception.
                    The exception is created with a single :class:`~tango.DevError`
                    object. A default value *tango.ErrSeverity.ERR* is defined for
                    the :class:`~tango.DevError` severity field.

                    The parameters are the same as the ones generates by a call to
                    :func:`sys.exc_info`.

                Parameters :
                    - type : (class)  the exception type of the exception being handled
                    - value : (object) exception parameter (its associated value or the
                              second argument to raise, which is always a class instance
                              if the exception type is a class object)
                    - traceback : (traceback) traceback object

                Throws     : DevFailed

                New in PyTango 7.2.1
            )doc",
            py::arg("type") = py::none(),
            py::arg("value") = py::none(),
            py::arg("traceback") = py::none());

    /// NamedDevFailed & family:
    py::class_<Tango::NamedDevFailed>(m, "NamedDevFailed")
        .def_readonly("name", &Tango::NamedDevFailed::name)               // string
        .def_readonly("idx_in_call", &Tango::NamedDevFailed::idx_in_call) // long
        .def_readonly("err_stack", &Tango::NamedDevFailed::err_stack);    // DevErrorList

    // DevFailed is not really exported but just translated, so we can't
    // derivate.
    py::class_<Tango::NamedDevFailedList>(m, "NamedDevFailedList")
        .def("get_faulty_attr_nb", &Tango::NamedDevFailedList::get_faulty_attr_nb) // size_t
        .def("call_failed", &Tango::NamedDevFailedList::call_failed)               // bool
        .def_readonly("err_list", &Tango::NamedDevFailedList::err_list);           // std::vector<NamedDevFailed>
}
