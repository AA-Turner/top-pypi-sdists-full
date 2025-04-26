/**
 * Copyright 2015 Google Inc. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

// Ensure that Python.h is included before any other header.
#include "common.h"

#include "bytecode_breakpoint.h"
#include "python_callback_evaluator.h"
#include "native_module.h"
#include "python_util.h"

namespace devtools {
namespace cdbg {

// Class to set zero overhead breakpoints.
static BytecodeBreakpoint g_bytecode_breakpoint;

// Initializes C++ flags and logging.
//
// This function should be called exactly once during debugger bootstrap. It
// should be called before any other method in this module is used.
//
// If omitted, the module will stay with default C++ flag values and logging
// will go to stderr.
//
// Args:
//   flags: dictionary of all the flags (flags that don't match names of C++
//          flags will be ignored).
static PyObject* InitializeModule(PyObject* self, PyObject* py_args) {
  PyObject* flags = nullptr;
  if (!PyArg_ParseTuple(py_args, "O", &flags)) {
    return nullptr;
  }

  Py_RETURN_NONE;
}

// Sets a new breakpoint in Python code. The breakpoint may have an optional
// condition to evaluate. When the breakpoint hits (and the condition matches)
// a callable object will be invoked from that thread.
//
// The breakpoint doesn't expire automatically after hit. It is the
// responsibility of the caller to call "ClearConditionalBreakpoint"
// appropriately.
//
// Args:
//   code_object: Python code object to set the breakpoint.
//   line: line number to set the breakpoint.
//   condition: optional callable object representing the condition to evaluate
//       or None for an unconditional breakpoint.
//   callback: callable object to invoke on breakpoint event. The callable is
//       invoked with two arguments: (event, frame). See "BreakpointFn" for more
//       details.
//
// Returns:
//   Integer cookie identifying this breakpoint. It needs to be specified when
//   clearing the breakpoint.
static PyObject* SetConditionalBreakpoint(PyObject* self, PyObject* py_args) {
  PyCodeObject* code_object = nullptr;
  int line = -1;
  PyCodeObject* condition = nullptr;
  PyObject* callback = nullptr;
  PyObject* error_callback = nullptr;
  if (!PyArg_ParseTuple(py_args, "OiOOO",
                        &code_object, &line, &condition, &callback, &error_callback)) {
    return nullptr;
  }

  if ((code_object == nullptr) || !PyCode_Check(code_object)) {
    PyErr_SetString(PyExc_TypeError, "invalid code_object argument");
    return nullptr;
  }

  if ((callback == nullptr) || !PyCallable_Check(callback)) {
    PyErr_SetString(PyExc_TypeError, "callback must be a callable object");
    return nullptr;
  }

  if ((error_callback == nullptr) || !PyCallable_Check(error_callback)) {
    PyErr_SetString(PyExc_TypeError, "error callback must be a callable object");
    return nullptr;
  }

  if (reinterpret_cast<PyObject*>(condition) == Py_None) {
    condition = nullptr;
  }

  if ((condition != nullptr) && !PyCode_Check(condition)) {
    PyErr_SetString(
        PyExc_TypeError,
        "condition must be None or a code object");
    return nullptr;
  }

  auto conditional_breakpoint = std::make_shared<PythonCallbackEvaluator>(
          ScopedPyObject::NewReference(callback));

  auto shared_error_callback_evaluator = std::make_shared<PythonCallbackEvaluator>(
      ScopedPyObject::NewReference(error_callback));

  int cookie = -1;
  PyObject* new_co_code = nullptr;

  DDEBUG("set breakpoint\n");
  cookie = g_bytecode_breakpoint.SetBreakpoint(
      code_object,
      line,
      callback,
      std::bind(
          &PythonCallbackEvaluator::EvaluateCallback,
          shared_error_callback_evaluator),
      &new_co_code);
  if (cookie == -1) {
    conditional_breakpoint->EvaluateCallback();
  }
  DDEBUG("after breakpoint set\n");
  DDEBUG("Null checks: %p\n", new_co_code);

#if PY_VERSION_HEX >= 0x030B0000
  return PyTuple_Pack(2, PyInt_FromLong(cookie), new_co_code);
#else
  return PyInt_FromLong(cookie);
#endif
}


// Clears the breakpoint previously set by "SetConditionalBreakpoint". Must be
// called exactly once per each call to "SetConditionalBreakpoint".
//
// Args:
//   cookie: breakpoint identifier returned by "SetConditionalBreakpoint".
static PyObject* ClearConditionalBreakpoint(PyObject* self, PyObject* py_args) {
  int cookie = -1;
  if (!PyArg_ParseTuple(py_args, "i", &cookie)) {
    return nullptr;
  }

    PyObject* new_co_code = nullptr;

    g_bytecode_breakpoint.ClearBreakpoint(cookie, &new_co_code);

#if PY_VERSION_HEX >= 0x030B0000
    return new_co_code;
#else
    Py_RETURN_NONE;
#endif
}

static PyObject* UpdateCoConsts(PyObject* self, PyObject* py_args) {
    PyObject* co = nullptr;
    PyObject* tuple = nullptr;

    if (!PyArg_ParseTuple(py_args, "OO", &co, &tuple)) {
        return nullptr;
    }

    if ((co == nullptr) || !PyCode_Check(co)) {
        PyErr_SetString(PyExc_TypeError, "invalid code_object argument");
        return nullptr;
    }

    ((PyCodeObject*)co)->co_consts = tuple;
    Py_INCREF(((PyCodeObject*)co)->co_consts);

    Py_RETURN_NONE;
}

static PyMethodDef g_module_functions[] = {
  {
    "InitializeModule",
    InitializeModule,
    METH_VARARGS,
    "Initialize C++ flags and logging."
  },
  {
    "SetConditionalBreakpoint",
    SetConditionalBreakpoint,
    METH_VARARGS,
    "Sets a new breakpoint in Python code."
  },
  {
    "ClearConditionalBreakpoint",
    ClearConditionalBreakpoint,
    METH_VARARGS,
    "Clears previously set breakpoint in Python code."
  },
  {
      "UpdateCoConsts",
      UpdateCoConsts,
      METH_VARARGS,
      "Updates co_consts of a code object"
  },
  { nullptr, nullptr, 0, nullptr }  // sentinel
};


#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef moduledef = {
  PyModuleDef_HEAD_INIT, /** m_base */
  CDBG_MODULE_NAME, /** m_name */
  "Native module for Python Cloud Debugger", /** m_doc */
  -1, /** m_size */
  g_module_functions, /** m_methods */
  NULL, /** m_slots */
  NULL, /** m_traverse */
  NULL, /** m_clear */
  NULL /** m_free */
};

PyObject* InitDebuggerNativeModuleInternal() {
  PyObject* module = PyModule_Create(&moduledef);
#else
PyObject* InitDebuggerNativeModuleInternal() {
  PyObject* module = Py_InitModule3(
      CDBG_MODULE_NAME,
      g_module_functions,
      "Native module for Python Cloud Debugger");
#endif

  SetDebugletModule(module);

  return module;
}

void InitDebuggerNativeModule() {
  InitDebuggerNativeModuleInternal();
}

}  // namespace cdbg
}  // namespace devtools


// This function is called to initialize the module.
#if PY_MAJOR_VERSION >= 3
PyMODINIT_FUNC PyInit_cdbg_native() {
  return devtools::cdbg::InitDebuggerNativeModuleInternal();
}
#else
PyMODINIT_FUNC initcdbg_native() {
  devtools::cdbg::InitDebuggerNativeModule();
}
#endif
