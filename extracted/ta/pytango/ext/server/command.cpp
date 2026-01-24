/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "function_call_macros.h"

#include "convertors/type_casters.h"
#include "convertors/commands/cpp_to_python.h"
#include "convertors/commands/python_to_cpp.h"

#include "base_types_structures/exception.h"
#include "server/command.h"

//+-------------------------------------------------------------------------
//
// method : 		PyCmd::is_allowed
//
// description : 	Decide if it is allowed to execute the command
//
// argin : - dev : The device on which the command has to be executed
//	   - any : The input data
//
// This method returns a boolean set to True if it is allowed to execute
// the command. Otherwise, returns false
//
//--------------------------------------------------------------------------
bool PyCmd::is_allowed(Tango::DeviceImpl *dev, [[maybe_unused]] const CORBA::Any &any) {
    if(py_allowed_defined) {
        GET_DEVICE
        try {
            return py_dev.attr(py_allowed_name.c_str())().cast<bool>();
        }
        CATCH_PY_EXCEPTION
    }
    return true;
}

void allocate_any(CORBA::Any *&any_ptr) {
    try {
        any_ptr = new CORBA::Any();
    } catch(std::bad_alloc &) {
        Tango::Except::throw_exception(
            "API_MemoryAllocation", "Can't allocate memory in server", "PyCmd::allocate_any()");
    }
}

CORBA::Any *PyCmd::execute(Tango::DeviceImpl *dev, const CORBA::Any &param_any) {
    GET_DEVICE
    try {
        CORBA::Any param_in = const_cast<CORBA::Any &>(param_any);
        // This call extracts the CORBA any into a python object.
        // So, the result is that param_py = param_in.
        // It is done with some template magic.

        py::object param_py;

        TANGO_DO_ON_DEVICE_DATA_TYPE_ID(in_type,
                                        (scalar_cpp_data_to_python<CORBA::Any, tangoTypeConst>(param_in, param_py));
                                        ,
                                        (array_cpp_data_to_python<tangoTypeConst>(param_in, param_py)););

        // Execute the python call for the command
        py::object ret_py_obj;

        if(in_type == Tango::DEV_VOID) {
            ret_py_obj = py_dev.attr(name.c_str())();
        } else {
            ret_py_obj = py_dev.attr(name.c_str())(param_py);
        }

        CORBA::Any *ret_any;
        allocate_any(ret_any);
        std::unique_ptr<CORBA::Any> ret_any_guard(ret_any);

        // It does: ret_any = ret_py_obj
        TANGO_DO_ON_DEVICE_DATA_TYPE_ID(out_type,
                                        (scalar_python_data_to_cpp<CORBA::Any, tangoTypeConst>(*ret_any, ret_py_obj));
                                        ,
                                        (array_python_data_to_cpp<CORBA::Any, tangoTypeConst>(*ret_any, ret_py_obj)););

        return ret_any_guard.release();
    } catch(py::error_already_set &eas) {
        TangoSys_OMemStream origin;
        origin << TANGO_EXCEPTION_ORIGIN << std::ends;
        handle_python_exception(eas, "PyDs_UnexpectedFailure", "Cannot execute command", origin.str());
    }
}
