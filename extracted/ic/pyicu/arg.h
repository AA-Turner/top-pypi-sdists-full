/* ====================================================================
 * Copyright (c) 2024-2025 Open Source Applications Foundation.
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included
 * in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
 * OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
 * DEALINGS IN THE SOFTWARE.
 * ====================================================================
 */

#ifndef _arg_h
#define _arg_h

#include <type_traits>

#include "common.h"

namespace arg {

class BooleanStrict {
private:
    UBool *const b;

public:
    BooleanStrict() = delete;

    explicit BooleanStrict(UBool *param) noexcept : b(param) {}

    int parse(PyObject *arg) const
    {
        if (arg == Py_True) {
            *b = 1;
            return 0;
        }
        if (arg == Py_False) {
            *b = 0;
            return 0;
        }

        return -1;
    }
};

class Boolean {
private:
    UBool *const b;

public:
    Boolean() = delete;

    explicit Boolean(UBool *param) noexcept : b(param) {}

    int parse(PyObject *arg) const
    {
        int res = PyObject_IsTrue(arg);

        if (res == 0 || res == 1) {
            *b = (UBool) res;
            return 0;
        }

        return -1;
    }
};

class BooleanArray {
private:
    std::unique_ptr<UBool[]> *const array;
    size_t *const len;

public:
    BooleanArray() = delete;

    explicit BooleanArray(std::unique_ptr<UBool[]> *param1, size_t *param2) noexcept
        : array(param1), len(param2) {}

    int parse(PyObject *arg) const
    {
        if (!PySequence_Check(arg))
            return -1;

        array->reset(toUBoolArray(arg, len));
        if (!array->get())
            return -1;

        return 0;
    }
};    

class Double {
private:
    double *const d;

public:
    Double() = delete;

    explicit Double(double *param) noexcept : d(param) {}

    int parse(PyObject *arg) const
    {
        if (PyFloat_Check(arg)) {
            *d = PyFloat_AsDouble(arg);
            return 0;
        }

#if PY_MAJOR_VERSION < 3
        if (PyInt_Check(arg)) {
            *d = (double) PyInt_AsLong(arg);
            return 0;
        }
#endif

        if (PyInt_Check(arg) || PyLong_Check(arg)) {
            *d = PyLong_AsDouble(arg);
            return 0;
        }

        return -1;
    }
};

class DoubleArray {
private:
    std::unique_ptr<double[]> *const array;
    size_t *const len;

public:
    DoubleArray() = delete;

    explicit DoubleArray(std::unique_ptr<double[]> *param1, size_t *param2) noexcept
        : array(param1), len(param2) {}

    int parse(PyObject *arg) const
    {
        if (!PySequence_Check(arg))
            return -1;

        if (PySequence_Length(arg) > 0)
        {
            PyObject *obj = PySequence_GetItem(arg, 0);
            int ok = (PyFloat_Check(obj) ||
                      PyInt_Check(obj) ||
                      PyLong_Check(obj));
            Py_DECREF(obj);

            if (!ok)
                return -1;
        }

        array->reset(toDoubleArray(arg, len));
        if (!array->get())
            return -1;

        return 0;
    }
};    

class Int {
private:
    int *const n;

public:
    Int() = delete;

    explicit Int(int *param) noexcept : n(param) {}

    int parse(PyObject *arg) const
    {
        if (!PyInt_Check(arg))
            return -1;

#if PY_MAJOR_VERSION >= 3
        if ((*n = PyLong_AsLong(arg)) == -1 && PyErr_Occurred())
            return -1;
#else
        *n = (int) PyInt_AsLong(arg);
#endif

        return 0;
    }
};

template <typename T>
class Enum {
private:
    T *const e;

public:
    Enum() = delete;

    explicit Enum(T *param) noexcept
        : e(param) {}

    int parse(PyObject *arg) const
    {
        static_assert(sizeof(T) == sizeof(int), "wrong size of enum");

        int n;
        int rc = Int(&n).parse(arg);
        if (rc == 0)
            *e = T(n);

        return rc;
    }
};    

class IntArray {
private:
    std::unique_ptr<int[]> *const array;
    size_t *const len;

public:
    IntArray() = delete;

    explicit IntArray(std::unique_ptr<int[]> *param1, size_t *param2) noexcept
        : array(param1), len(param2) {}

    int parse(PyObject *arg) const
    {
        if (!PySequence_Check(arg))
            return -1;

        if (PySequence_Length(arg) > 0)
        {
            PyObject *obj = PySequence_GetItem(arg, 0);
            int ok = (PyInt_Check(obj) || PyLong_Check(obj));
            Py_DECREF(obj);

            if (!ok)
                return -1;
        }

        array->reset(toIntArray(arg, len));
        if (!array->get())
            return -1;

        return 0;
    }
};    

template <typename T> IntArray Enums(std::unique_ptr<T[]> *param, size_t *len) {
    static_assert(sizeof(T) == sizeof(int), "wrong size of enum");
    return IntArray((std::unique_ptr<int[]> *) param, len);
}

class Long {
private:
    PY_LONG_LONG *const l;

public:
    Long() = delete;

    explicit Long(PY_LONG_LONG *param) noexcept : l(param) {}

    int parse(PyObject *arg) const
    {
        if (!(PyLong_Check(arg) || PyInt_Check(arg)))
            return -1;

        *l = PyLong_AsLongLong(arg);
        return 0;
    }
};

class Date {
private:
    UDate *const d;

public:
    Date() = delete;

    explicit Date(UDate *param) noexcept : d(param) {}

    int parse(PyObject *arg) const
    {
        if (!isDate(arg))
            return -1;

        *d = PyObject_AsUDate(arg);
        return 0;
    }
};

class DateExact {
private:
    UDate *const d;

public:
    DateExact() = delete;

    explicit DateExact(UDate *param) noexcept : d(param) {}

    int parse(PyObject *arg) const
    {
        if (!isDateExact(arg))
            return -1;

        *d = PyObject_AsUDate(arg);
        return 0;
    }
};

class BytesToCStringAndSize {
private:
    const char **const data;
    size_t *const len;

public:
    BytesToCStringAndSize() = delete;

    explicit BytesToCStringAndSize(const char **param1, size_t *param2) noexcept
        : data(param1), len(param2) {}

    int parse(PyObject *arg) const
    {
        if (!PyBytes_Check(arg))
            return -1;

        *data = PyBytes_AS_STRING(arg);
        *len = PyBytes_GET_SIZE(arg);
        return 0;
    }
};

template <typename T> class ICUObject {
private:
    const classid id;
    PyTypeObject *const type;
    T **const obj;

public:
    ICUObject() = delete;

    explicit ICUObject(classid param1, PyTypeObject *param2, T **param3) noexcept
        : id(param1), type(param2), obj(param3) {}

    int parse(PyObject *arg) const
    {
        if (!isInstance(arg, id, type))
            return -1;

        *obj = reinterpret_cast<T *>(((t_uobject *) arg)->object);
        return 0;
    }
};

template <typename T> class SavedICUObject {
private:
    const classid id;
    PyTypeObject *const type;
    T **const obj;
    PyObject **const pyobj;

public:
    SavedICUObject() = delete;

    explicit SavedICUObject(classid param1, PyTypeObject *param2, T **param3, PyObject **param4) noexcept
        : id(param1), type(param2), obj(param3), pyobj(param4) {}

    int parse(PyObject *arg) const
    {
        if (!isInstance(arg, id, type))
            return -1;

        *obj = reinterpret_cast<T *>(((t_uobject *) arg)->object);
        Py_INCREF(arg); Py_XDECREF(*pyobj); *pyobj = arg;
        return 0;
    }
};

template <typename T> class ICUObjectArray {
private:
    const classid id;
    PyTypeObject *const type;
    std::unique_ptr<T *, decltype(free) *> *const array;
    size_t *const len;

public:
    ICUObjectArray() = delete;

    explicit ICUObjectArray(classid param1, PyTypeObject *param2, std::unique_ptr<T *, decltype(free) *> *param3, size_t *param4) noexcept
        : id(param1), type(param2), array(param3), len(param4) {}

    int parse(PyObject *arg) const
    {
        if (!PySequence_Check(arg))
            return -1;

        if (PySequence_Length(arg) > 0)
        {
            PyObject *obj = PySequence_GetItem(arg, 0);
            int ok = isInstance(obj, id, type);
            Py_DECREF(obj);

            if (!ok)
                return -1;
        }

        array->reset(reinterpret_cast<T **>(pl2cpa(arg, len, id, type)));
        if (!array->get())
            return -1;

        return 0;
    }
};

template <typename T> class ICUObjectValueArray {
private:
    typedef T *(*convFn)(PyObject *, size_t *, classid, PyTypeObject *);
    const classid id;
    PyTypeObject *const type;
    std::unique_ptr<T[]> *const array;
    size_t *const len;
    const convFn fn;

public:
    ICUObjectValueArray() = delete;

    explicit ICUObjectValueArray(classid param1, PyTypeObject *param2, std::unique_ptr<T[]> *param3, size_t *param4, convFn param5) noexcept
        : id(param1), type(param2), array(param3), len(param4), fn(param5) {}

    int parse(PyObject *arg) const
    {
        if (!PySequence_Check(arg))
            return -1;

        if (PySequence_Length(arg) > 0)
        {
            PyObject *obj = PySequence_GetItem(arg, 0);
            int ok = isInstance(obj, id, type);
            Py_DECREF(obj);

            if (!ok)
                return -1;
        }

        array->reset(fn(arg, len, id, type));
        if (!array->get())
            return -1;

        return 0;
    }
};

class None {
public:
    int parse(PyObject *arg) const
    {
        if (arg != Py_None)
            return -1;

        return 0;
    }
};

class StringOrUnicodeToFSCharsArg {
private:
    charsArg *const p;

public:
    StringOrUnicodeToFSCharsArg() = delete;

    explicit StringOrUnicodeToFSCharsArg(charsArg *param) noexcept
        : p(param) {}

    int parse(PyObject *arg) const
    {
        if (PyUnicode_Check(arg))
        {
#if PY_MAJOR_VERSION >= 3
            PyObject *bytes = PyUnicode_EncodeFSDefault(arg);
#else
            // TODO: Figure out fs encoding in a reasonable way
            PyObject *bytes = PyUnicode_AsUTF8String(arg);
#endif
            if (bytes == NULL)
                return -1;

            p->own(bytes);
            return 0;
        }

        if (PyBytes_Check(arg))
        {
            p->borrow(arg);
            return 0;
        }

        return -1;
    }
};

class StringOrUnicodeToUtf8CharsArg {
private:
    charsArg *const p;

public:
    StringOrUnicodeToUtf8CharsArg() = delete;

    explicit StringOrUnicodeToUtf8CharsArg(charsArg *param) noexcept
        : p(param) {}

    int parse(PyObject *arg) const
    {
        if (PyUnicode_Check(arg))
        {
            PyObject *bytes = PyUnicode_AsUTF8String(arg);
            if (bytes == NULL)
                return -1;

            p->own(bytes);
            return 0;
        }

        if (PyBytes_Check(arg))
        {
            p->borrow(arg);
            return 0;
        }

        return -1;
    }
};

class StringOrUnicodeToUtf8CharsArgArray {
private:
    std::unique_ptr<charsArg[]> *const array;
    size_t *const len;

public:
    StringOrUnicodeToUtf8CharsArgArray() = delete;

    explicit StringOrUnicodeToUtf8CharsArgArray(std::unique_ptr<charsArg[]> *param1, size_t *param2) noexcept
        : array(param1), len(param2) {}

    int parse(PyObject *arg) const
    {
        if (!PySequence_Check(arg))
            return -1;

        if (PySequence_Length(arg) > 0)
        {
            PyObject *obj = PySequence_GetItem(arg, 0);
            int ok = PyBytes_Check(obj) || PyUnicode_Check(obj);
            Py_DECREF(obj);

            if (!ok)
                return -1;
        }

        array->reset(toCharsArgArray(arg, len));
        if (!array->get())
            return -1;

        return 0;
    }
};

class String {
private:
    UnicodeString **const u;
    UnicodeString *const _u;

public:
    String() = delete;

    explicit String(UnicodeString **param1, UnicodeString *param2) noexcept
        : u(param1), _u(param2) {}

    int parse(PyObject *arg) const
    {
        if (isUnicodeString(arg)) {
            *u = (UnicodeString *) ((t_uobject *) arg)->object;
            return 0;
        }

        if (PyBytes_Check(arg) || PyUnicode_Check(arg)) {
            try {
                PyObject_AsUnicodeString(arg, *_u);
                *u = _u;
            } catch (ICUException e) {
                e.reportError();
                return -1;
            }
            return 0;
        }

        return -1;
    }
};

class SavedString {
private:
    UnicodeString **const u;
    PyObject **const obj;

public:
    SavedString() = delete;

    explicit SavedString(UnicodeString **param1, PyObject **param2) noexcept
        : u(param1), obj(param2) {}

    int parse(PyObject *arg) const
    {
        if (isUnicodeString(arg)) {
            *u = (UnicodeString *) ((t_uobject *) arg)->object;
            Py_INCREF(arg); Py_XDECREF(*obj); *obj = arg;
            return 0;
        }

        if (PyBytes_Check(arg) || PyUnicode_Check(arg)) {
            try {
                *u = PyObject_AsUnicodeString(arg);
                Py_XDECREF(*obj); *obj = wrap_UnicodeString(*u, T_OWNED);
            } catch (ICUException e) {
                e.reportError();
                return -1;
            }
            return 0;
        }

        return -1;
    }
};

class PythonBytes {
private:
    PyObject **const obj;

public:
    PythonBytes() = delete;

    explicit PythonBytes(PyObject **param) noexcept
        : obj(param) {}

    int parse(PyObject *arg) const
    {
        if (!PyBytes_Check(arg))
            return -1;

        *obj = arg;
        return 0;
    }
};

class CString {
private:
    char **const c;

public:
    CString() = delete;

    explicit CString(char **param) noexcept
        : c(param) {}

    int parse(PyObject *arg) const
    {
        if (!PyBytes_Check(arg))
            return -1;

        *c = PyBytes_AS_STRING(arg);
        return 0;
    }
};

class UnicodeStringArg {
private:
    UnicodeString **const u;

public:
    UnicodeStringArg() = delete;

    explicit UnicodeStringArg(UnicodeString **param) noexcept : u(param) {}

    int parse(PyObject *arg) const
    {
        if (!isUnicodeString(arg))
            return -1;

        *u = (UnicodeString *) ((t_uobject *) arg)->object;
        return 0;
    }
};

class UnicodeStringNew {
private:
    UnicodeString **const u;

public:
    UnicodeStringNew() = delete;

    explicit UnicodeStringNew(UnicodeString **param) noexcept : u(param) {}

    int parse(PyObject *arg) const
    {
        if (!(PyBytes_Check(arg) || PyUnicode_Check(arg)))
            return -1;

        try {
            *u = PyObject_AsUnicodeString(arg);  // a new UnicodeString
        } catch (ICUException e) {
            e.reportError();
            return -1;
        }
        return 0;
    }
};

class UnicodeStringRef {
private:
    UnicodeString *const u;

public:
    UnicodeStringRef() = delete;

    explicit UnicodeStringRef(UnicodeString *param) noexcept : u(param) {}

    int parse(PyObject *arg) const
    {
        if (!(PyBytes_Check(arg) || PyUnicode_Check(arg)))
            return -1;

        try {
            PyObject_AsUnicodeString(arg, *u);
        } catch (ICUException e) {
            e.reportError();
            return -1;
        }

        return 0;
    }
};

class UnicodeStringArray {
private:
    std::unique_ptr<UnicodeString[]> *const array;
    size_t *const len;

public:
    UnicodeStringArray() = delete;

    explicit UnicodeStringArray(std::unique_ptr<UnicodeString[]> *param1, size_t *param2) noexcept
        : array(param1), len(param2) {}

    int parse(PyObject *arg) const
    {
        if (!PySequence_Check(arg))
            return -1;

        if (PySequence_Length(arg) > 0)
        {
            PyObject *obj = PySequence_GetItem(arg, 0);
            int ok = (PyBytes_Check(obj) || PyUnicode_Check(obj) ||
                      isUnicodeString(obj));
            Py_DECREF(obj);

            if (!ok)
                return -1;
        }

        array->reset(toUnicodeStringArray(arg, len));
        return 0;
    }
};

class UnicodeStringAndPythonObject {
private:
    UnicodeString **const u;
    PyObject **const obj;

public:
    UnicodeStringAndPythonObject() = delete;

    explicit UnicodeStringAndPythonObject(UnicodeString **param1, PyObject **param2) noexcept : u(param1), obj(param2) {}

    int parse(PyObject *arg) const
    {
        if (!isUnicodeString(arg))
            return -1;
        
        *u = (UnicodeString *) ((t_uobject *) arg)->object;
        *obj = arg;
        return 0;
    }
};

class AnyPythonObject {
private:
    PyObject **const obj;

public:
    AnyPythonObject() = delete;

    explicit AnyPythonObject(PyObject **param) noexcept : obj(param) {}

    int parse(PyObject *arg) const
    {
        *obj = arg;
        return 0;
    }
};

class PythonObject {
private:
    PyTypeObject *const type;
    PyObject **const obj;

public:
    PythonObject() = delete;

    explicit PythonObject(PyTypeObject *param1, PyObject **param2) noexcept : type(param1), obj(param2) {}

    int parse(PyObject *arg) const
    {
        if (!PyObject_TypeCheck(arg, type))
            return -1;
        
        *obj = arg;
        return 0;
    }
};

class PythonCallable {
private:
    PyObject **const obj;

public:
    PythonCallable() = delete;

    explicit PythonCallable(PyObject **param) noexcept : obj(param) {}

    int parse(PyObject *arg) const
    {
        if (!PyCallable_Check(arg))
            return -1;
        
        *obj = arg;
        return 0;
    }
};

#define _IS_POD(T)                                      \
  static_assert(std::is_trivial<T>::value);             \
  static_assert(std::is_standard_layout<T>::value)

_IS_POD(AnyPythonObject);
_IS_POD(Boolean);
_IS_POD(BooleanArray);
_IS_POD(BooleanStrict);
_IS_POD(BytesToCStringAndSize);
_IS_POD(CString);
_IS_POD(Date);
_IS_POD(DateExact);
_IS_POD(Double);
_IS_POD(DoubleArray);
_IS_POD(ICUObject<UObject>);
_IS_POD(ICUObjectArray<UObject>);
_IS_POD(ICUObjectValueArray<UObject>);
_IS_POD(Int);
_IS_POD(IntArray);
_IS_POD(Long);
_IS_POD(None);
_IS_POD(PythonBytes);
_IS_POD(PythonCallable);
_IS_POD(PythonObject);
_IS_POD(SavedICUObject<UObject>);
_IS_POD(SavedString);
_IS_POD(String);
_IS_POD(StringOrUnicodeToFSCharsArg);
_IS_POD(StringOrUnicodeToUtf8CharsArg);
_IS_POD(StringOrUnicodeToUtf8CharsArgArray);
_IS_POD(UnicodeStringAndPythonObject);
_IS_POD(UnicodeStringArg);
_IS_POD(UnicodeStringArray);
_IS_POD(UnicodeStringNew);
_IS_POD(UnicodeStringRef);

#undef _IS_POD

// Convenience abbreviations that match the previous format char constants.

using B = BooleanStrict;
using b = Boolean;
using C = PythonBytes;
using c = CString;
using D = Date;
using E = DateExact;
using d = Double;
using F = DoubleArray;
using f = StringOrUnicodeToFSCharsArg;
using G = BooleanArray;
using H = IntArray;
using i = Int;
using K = AnyPythonObject;
using L = Long;
using k = BytesToCStringAndSize;
using M = PythonCallable;
using m = StringOrUnicodeToUtf8CharsArgArray;
using N = None;
using n = StringOrUnicodeToUtf8CharsArg;
using O = PythonObject;
template <typename T> using P = ICUObject<T>;
template <typename T> using p = SavedICUObject<T>;
template <typename T> using Q = ICUObjectArray<T>;
template <typename T> using R = ICUObjectValueArray<T>;
using S = String;
using s = UnicodeStringRef;
using T = UnicodeStringArray;
using U = UnicodeStringArg;
using u = UnicodeStringNew;
using V = UnicodeStringAndPythonObject;
using W = SavedString;

// Argument parsing

inline int _parse(PyObject *args, int index) {
  return 0;
}

template <typename T, typename... Ts>
int _parse(PyObject *args, int index, T param, Ts... params) {
  PyObject *arg = PyTuple_GET_ITEM(args, index);
  int result = param.parse(arg);
  if (result != 0)
    return result;
  return _parse(args, index + 1, params...);
}

// Parse a Python argument tuple into C++ types with type checking.
//
// Usage example:
//
//   int flag;
//   char *data;
//   int size;
//   if (!arg::parse(args, arg::B(&flag), arg::k(&data, &size))) {
//     // do stuff
//   }
//
template <typename... Ts>
int parseArgs(PyObject *args, Ts... params) {
  if (PyTuple_Size(args) != sizeof...(params)) {
    PyErr_SetString(PyExc_ValueError, "number of args doesn't match number of params");
    return -1;
  }
  return _parse(args, 0, params...);
}

// Parse a single Python object into a C++ parameter type.
template <typename T>
int parseArg(PyObject *arg, T param) {
  return param.parse(arg);
}

}  // namespace arg

using arg::parseArgs;
using arg::parseArg;

#endif /* _arg_h */
