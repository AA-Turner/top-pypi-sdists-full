#ifndef SORTED_DICT_UTILS_HH_
#define SORTED_DICT_UTILS_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <memory>

#define LEFT_PARENTHESIS "\u0028"
#define RIGHT_PARENTHESIS "\u0029"
#define LEFT_CURLY_BRACKET "\u007B"
#define RIGHT_CURLY_BRACKET "\u007D"

/**
 * C++-style clean-up implementation for Python objects.
 */
struct PyObject_Delete
{
    void operator()(PyObject* ob)
    {
        Py_XDECREF(ob);
    }
};

using PyObjectWrapper = std::unique_ptr<PyObject, PyObject_Delete>;

#endif
