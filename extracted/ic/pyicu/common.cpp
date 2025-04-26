/* ====================================================================
 * Copyright (c) 2005-2025 Open Source Applications Foundation.
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

#include "common.h"
#include <stdarg.h>
#include <stdlib.h>
#include <string.h>
#include <datetime.h>

#include <unicode/ustring.h>
#include <unicode/utf16.h>

#include "bases.h"
#include "macros.h"

#include "arg.h"

// From Python's Objects/unicodeobject.c
// Maximum code point of Unicode 6.0: 0x10ffff (1,114,111).
#define MAX_UNICODE 0x10ffff

static PyObject *utcoffset_NAME;
static PyObject *toordinal_NAME;
static PyObject *getDefault_NAME;


typedef struct {
    UConverterCallbackReason reason;
    const char *src;
    int32_t src_length;
    char chars[8];
    int32_t length;
    int32_t error_position;
} _STOPReason;

U_STABLE void U_EXPORT2 _stopDecode(const void *context,
                                    UConverterToUnicodeArgs *args,
                                    const char *chars, int32_t length,
                                    UConverterCallbackReason reason,
                                    UErrorCode *err)
{
    _STOPReason *stop = (_STOPReason *) context;

    stop->reason = reason;
    stop->length = length;

    if (chars && length)
    {
        const int size = stop->src_length - length + 1;
        const size_t len = (size_t) length < sizeof(stop->chars) - 1
            ? (size_t) length
            : sizeof(stop->chars) - 1;

        strncpy(stop->chars, chars, len); stop->chars[len] = '\0';
        stop->error_position = -1;

        for (int i = 0; i < size; ++i)
        {
            if (!memcmp(stop->src + i, chars, length))
            {
                stop->error_position = i;
                break;
            }
        }
    }
}


PyObject *PyExc_ICUError;
PyObject *PyExc_InvalidArgsError;


EXPORT ICUException::ICUException()
{
    code = NULL;
    msg = NULL;
}

EXPORT ICUException::ICUException(const ICUException &e)
    : code(e.code), msg(e.msg)
{
    Py_XINCREF(code);
    Py_XINCREF(msg);
}

EXPORT ICUException::ICUException(UErrorCode status)
{
    PyObject *messages = PyObject_GetAttrString(PyExc_ICUError, "messages");

    code = PyInt_FromLong((long) status);
    msg = PyObject_GetItem(messages, code);
    Py_DECREF(messages);
}

EXPORT ICUException::ICUException(UErrorCode status, char *format, ...)
{
    ICUException::code = PyInt_FromLong((long) status);

    va_list ap;
    va_start(ap, format);
    ICUException::msg = PyString_FromFormatV(format, ap);
    va_end(ap);
}

EXPORT ICUException::ICUException(UParseError &pe, UErrorCode status)
{
    PyObject *messages = PyObject_GetAttrString(PyExc_ICUError, "messages");
    UnicodeString pre((const UChar *) pe.preContext, U_PARSE_CONTEXT_LEN);
    UnicodeString post((const UChar *) pe.postContext, U_PARSE_CONTEXT_LEN);
    PyObject *tuple = PyTuple_New(5);

    ICUException::code = PyInt_FromLong((long) status);

    PyTuple_SET_ITEM(tuple, 0, PyObject_GetItem(messages, code));
    PyTuple_SET_ITEM(tuple, 1, PyInt_FromLong(pe.line));
    PyTuple_SET_ITEM(tuple, 2, PyInt_FromLong(pe.offset));
    PyTuple_SET_ITEM(tuple, 3, PyUnicode_FromUnicodeString(&pre));
    PyTuple_SET_ITEM(tuple, 4, PyUnicode_FromUnicodeString(&post));
    ICUException::msg = tuple;

    Py_DECREF(messages);
}

EXPORT ICUException::~ICUException()
{
    Py_XDECREF(ICUException::code);
    Py_XDECREF(ICUException::msg);
}

EXPORT PyObject *ICUException::reportError()
{
    if (ICUException::code)
    {
        PyObject *tuple = Py_BuildValue("(OO)", ICUException::code, ICUException::msg ? ICUException::msg : Py_None);

        PyErr_SetObject(PyExc_ICUError, tuple);
        Py_DECREF(tuple);
    }

    return NULL;
}


EXPORT PyObject *PyUnicode_FromUnicodeString(const UnicodeString *string)
{
    if (!string)
    {
        Py_INCREF(Py_None);
        return Py_None;
    }

    return PyUnicode_FromUnicodeString(string->getBuffer(), string->length());
}

EXPORT PyObject *PyUnicode_FromUnicodeString(const UnicodeString &string)
{
    return PyUnicode_FromUnicodeString(string.getBuffer(), string.length());
}

EXPORT PyObject *PyUnicode_FromUnicodeString(const UChar *utf16, int len16)
{
    if (!utf16)
    {
        Py_INCREF(Py_None);
        return Py_None;
    }
#if PY_VERSION_HEX < 0x03030000 || defined(PYPY_VERSION)
    else if (sizeof(Py_UNICODE) == sizeof(UChar))
        return PyUnicode_FromUnicode((const Py_UNICODE *) utf16, len16);
    else
    {
        int32_t len32 = u_countChar32(utf16, len16);
        PyObject *u = PyUnicode_FromUnicode(NULL, len32);

        if (u)
        {
            Py_UNICODE *pchars = PyUnicode_AS_UNICODE(u);
            UErrorCode status = U_ZERO_ERROR;

            u_strToUTF32((UChar32 *) pchars, len32, NULL,
                         utf16, len16, &status);
            if (U_FAILURE(status))
            {
                Py_DECREF(u);
                return ICUException(status).reportError();
            }
        }

        return u;
    }
#else
    {
        int32_t len32 = 0;
        UChar32 max_char = 0;

        for (int32_t i = 0; i < len16;) {
            UChar32 cp;

            U16_NEXT(utf16, i, len16, cp);
            max_char |= cp;  // we only care about the leftmost bit
            len32 += 1;
        }
        if (max_char > MAX_UNICODE)
            max_char = MAX_UNICODE;

        PyObject *result = PyUnicode_New(len32, max_char);

        if (result == NULL)
            return NULL;

        switch (PyUnicode_KIND(result)) {
          case PyUnicode_1BYTE_KIND:
            // note: len16 == len32
            for (int32_t i = 0; i < len32; ++i)
                PyUnicode_1BYTE_DATA(result)[i] = (Py_UCS1) (utf16[i]);
            break;

          case PyUnicode_2BYTE_KIND:
            // note: len16 == len32
            u_memcpy((UChar *) PyUnicode_2BYTE_DATA(result), utf16, len16);
            break;

          case PyUnicode_4BYTE_KIND: {
            UErrorCode status = U_ZERO_ERROR;

            // note: len16 > len32 (len32 is at least half of len16)
            u_strToUTF32((UChar32 *) PyUnicode_4BYTE_DATA(result), len32, NULL,
                         utf16, len16, &status);
            if (U_FAILURE(status))
            {
                Py_DECREF(result);
                return ICUException(status).reportError();
            }
            break;
          }

          default:
            Py_DECREF(result);
            return NULL;
        }

        return result;
    }
#endif
}

EXPORT UnicodeString &PyBytes_AsUnicodeString(PyObject *object,
                                              const char *encoding,
                                              const char *mode,
                                              UnicodeString &string)
{
    UErrorCode status = U_ZERO_ERROR;
    UConverter *conv = ucnv_open(encoding, &status);

    if (U_FAILURE(status))
        throw ICUException(status);

    _STOPReason stop;
    char *src;
    Py_ssize_t len;

    memset(&stop, 0, sizeof(stop));

    if (!strcmp(mode, "strict"))
    {
        ucnv_setToUCallBack(conv, _stopDecode, &stop, NULL, NULL, &status);
        if (U_FAILURE(status))
        {
            ucnv_close(conv);
            throw ICUException(status);
        }
    }

    PyBytes_AsStringAndSize(object, &src, &len);
    stop.src = src;
    stop.src_length = (int) len;

    std::unique_ptr<UChar[]> buffer(new UChar[len]);
    if (!buffer.get())
    {
        ucnv_close(conv);

        PyErr_NoMemory();
        throw ICUException();
    }
    UChar *target = buffer.get();

    ucnv_toUnicode(conv, &target, target + (int) len,
                   (const char **) &src, src + len, NULL, true, &status);

    if (U_FAILURE(status))
    {
        const char *reasonName;

        switch (stop.reason) {
          case UCNV_UNASSIGNED:
            reasonName = "the code point is unassigned";
            break;
          case UCNV_ILLEGAL:
            reasonName = "the code point is illegal";
            break;
          case UCNV_IRREGULAR:
            reasonName = "the code point is not a regular sequence in the encoding";
            break;
          default:
            reasonName = "unexpected reason code";
            break;
        }
        status = U_ZERO_ERROR;

        PyErr_Format(PyExc_ValueError, "'%s' codec can't decode byte 0x%x in position %d: reason code %d (%s)", ucnv_getName(conv, &status), (int) (unsigned char) stop.chars[0], stop.error_position, stop.reason, reasonName);

        ucnv_close(conv);

        throw ICUException();
    }

    string.setTo(buffer.get(), (int32_t) (target - buffer.get()));
    ucnv_close(conv);

    return string;
}

EXPORT UnicodeString &PyObject_AsUnicodeString(PyObject *object,
                                               const char *encoding,
                                               const char *mode,
                                               UnicodeString &string)
{
    if (PyUnicode_Check(object))
    {
#if PY_VERSION_HEX < 0x03030000
        if (sizeof(Py_UNICODE) == sizeof(UChar))
            string.setTo((const UChar *) PyUnicode_AS_UNICODE(object),
                         (int32_t) PyUnicode_GET_SIZE(object));
        else if (sizeof(Py_UNICODE) == sizeof(UChar32))
        {
            int32_t len = (int32_t) PyUnicode_GET_SIZE(object);
            Py_UNICODE *pchars = PyUnicode_AS_UNICODE(object);

            string = UnicodeString::fromUTF32((const UChar32 *) pchars, len);
        }
        else
            abort();  // we should not get here
#else
        PyUnicode_READY(object);

        switch (PyUnicode_KIND(object)) {
#if PY_VERSION_HEX < 0x030c0000
          case PyUnicode_WCHAR_KIND: {  // this code path should be deprecated
              if (SIZEOF_WCHAR_T == sizeof(UChar))
              {
                  Py_ssize_t len;
                  wchar_t *wchars = PyUnicode_AsWideCharString(object, &len);

                  if (wchars != NULL)
                  {
                      string.setTo((const UChar *) wchars, len);
                      PyMem_Free(wchars);
                  }
              }
              else if (SIZEOF_WCHAR_T == sizeof(UChar32))
              {
                  Py_ssize_t len;
                  wchar_t *wchars = PyUnicode_AsWideCharString(object, &len);

                  if (wchars != NULL)
                  {
                      string = UnicodeString::fromUTF32(
                          (const UChar32 *) wchars, len);
                      PyMem_Free(wchars);
                  }
              }
              break;
          }
#endif
          case PyUnicode_1BYTE_KIND: {
              Py_ssize_t len = PyUnicode_GET_LENGTH(object);
              Py_UCS1 *pchars = PyUnicode_1BYTE_DATA(object);
              UChar *chars = string.getBuffer(len);

              if (chars != NULL)
              {
                  for (int i = 0; i < len; ++i)
                      chars[i] = (UChar) pchars[i];
                  string.releaseBuffer(len);
              }
              break;
          }

          case PyUnicode_2BYTE_KIND: {
              Py_ssize_t len = PyUnicode_GET_LENGTH(object);
              Py_UCS2 *pchars = PyUnicode_2BYTE_DATA(object);

              string.setTo((const UChar *) pchars, len);
              break;
          }

          case PyUnicode_4BYTE_KIND: {
              Py_ssize_t len = PyUnicode_GET_LENGTH(object);
              Py_UCS4 *pchars = PyUnicode_4BYTE_DATA(object);

              string = UnicodeString::fromUTF32((const UChar32 *) pchars, len);
              break;
          }
        }
#endif
    }
    else if (PyBytes_Check(object))
        PyBytes_AsUnicodeString(object, encoding, mode, string);
    else
    {
        PyErr_SetObject(PyExc_TypeError, object);
        throw ICUException();
    }

    return string;
}

EXPORT UnicodeString &PyObject_AsUnicodeString(PyObject *object,
                                               UnicodeString &string)
{
    return PyObject_AsUnicodeString(object, "utf-8", "strict", string);
}

EXPORT UnicodeString *PyObject_AsUnicodeString(PyObject *object)
{
    if (object == Py_None)
        return NULL;
    else
    {
        UnicodeString string;

        try {
            PyObject_AsUnicodeString(object, string);
        } catch (ICUException e) {
            throw e;
        }

        return new UnicodeString(string);
    }
}


#if PY_VERSION_HEX < 0x02040000
    /* Replace some _CheckExact macros for Python < 2.4 since the actual
     * datetime types are private until then.  This is ugly, but allows
     * support for datetime objects in Python 2.3.
     */
    #include <string.h>

    #undef PyDateTime_CheckExact
    #define PyDateTime_CheckExact(op) \
       (!strcmp(Py_TYPE(op)->tp_name, "datetime.datetime"))

    #undef PyDelta_CheckExact
    #define PyDelta_CheckExact(op) \
       (!strcmp(Py_TYPE(op)->tp_name, "datetime.timedelta"))
#endif


int isDate(PyObject *object)
{
    if (PyFloat_CheckExact(object))
        return 1;

    return PyDateTime_CheckExact(object);
}

int isDateExact(PyObject *object)
{
    return PyDateTime_CheckExact(object);
}

EXPORT UDate PyObject_AsUDate(PyObject *object)
{
    if (PyFloat_CheckExact(object))
        return (UDate) (PyFloat_AsDouble(object) * 1000.0);
    else
    {
        if (PyDateTime_CheckExact(object))
        {
            PyObject *tzinfo = PyObject_GetAttrString(object, "tzinfo");
            PyObject *utcoffset, *ordinal;

            if (tzinfo == Py_None)
            {
                PyObject *m = PyImport_ImportModule("icu");
                PyObject *cls = PyObject_GetAttrString(m, "ICUtzinfo");

                tzinfo = PyObject_CallMethodObjArgs(cls, getDefault_NAME, NULL);
                Py_DECREF(cls);
                Py_DECREF(m);

                utcoffset = PyObject_CallMethodObjArgs(tzinfo, utcoffset_NAME,
                                                       object, NULL);
                Py_DECREF(tzinfo);
            }
            else
            {
                utcoffset = PyObject_CallMethodObjArgs(object, utcoffset_NAME,
                                                       NULL);
                Py_DECREF(tzinfo);
            }

            ordinal = PyObject_CallMethodObjArgs(object, toordinal_NAME, NULL);

            if (utcoffset != NULL && PyDelta_CheckExact(utcoffset) &&
                ordinal != NULL && PyInt_CheckExact(ordinal))
            {
#if PY_MAJOR_VERSION >= 3
                double ordinalValue = PyLong_AsDouble(ordinal);
#else
                long ordinalValue = PyInt_AsLong(ordinal);
#endif

                double timestamp =
                    (ordinalValue - 719163) * 86400.0 +
                    PyDateTime_DATE_GET_HOUR(object) * 3600.0 +
                    PyDateTime_DATE_GET_MINUTE(object) * 60.0 +
                    (double) PyDateTime_DATE_GET_SECOND(object) +
                    PyDateTime_DATE_GET_MICROSECOND(object) / 1e6 -
#ifndef PYPY_VERSION
                    (((PyDateTime_Delta *) utcoffset)->days * 86400.0 +
                     (double) ((PyDateTime_Delta *) utcoffset)->seconds);
#else
                    (PyDateTime_DELTA_GET_DAYS(
                        (PyDateTime_Delta *) utcoffset) * 86400.0 +
                     (double) PyDateTime_DELTA_GET_SECONDS(
                         (PyDateTime_Delta *) utcoffset));
#endif

                Py_DECREF(utcoffset);
                Py_DECREF(ordinal);

                return (UDate) (timestamp * 1000.0);
            }

            Py_XDECREF(utcoffset);
            Py_XDECREF(ordinal);
        }
    }

    PyErr_SetObject(PyExc_TypeError, object);
    throw ICUException();
}

int abstract_init(PyObject *self, PyObject *args, PyObject *kwds)
{
    PyObject *err = Py_BuildValue("(sO)", "instantiating class", self->ob_type);

    PyErr_SetObject(PyExc_NotImplementedError, err);
    Py_DECREF(err);

    return -1;
}

PyObject *abstract_method(PyObject *self, PyObject *args)
{
    PyObject *err = Py_BuildValue("(sO)", "calling abstract method on",
                                  self->ob_type);

    PyErr_SetObject(PyExc_NotImplementedError, err);
    Py_DECREF(err);

    return NULL;
}

static PyObject *types;

void registerType(PyTypeObject *type, classid id)
{
#if U_ICU_VERSION_HEX < 0x04060000
    PyObject *n = PyInt_FromLong((Py_intptr_t) id);
#else
    PyObject *n = PyString_FromString(id);
#endif
    PyObject *list = PyList_New(0);
    PyObject *bn;

    PyDict_SetItem(types, n, list); Py_DECREF(list);
    PyDict_SetItem(types, (PyObject *) type, n);

    while (type != &UObjectType_) {
        type = type->tp_base;
        bn = PyDict_GetItem(types, (PyObject *) type);
        list = PyDict_GetItem(types, bn);
        PyList_Append(list, n);
    }

    Py_DECREF(n);
}

int isInstance(PyObject *arg, classid id, PyTypeObject *type)
{
    if (PyObject_TypeCheck(arg, &UObjectType_))
    {
#if U_ICU_VERSION_HEX < 0x04060000
        classid oid = ((t_uobject *) arg)->object->getDynamicClassID();

        if (id == oid)
            return 1;

        PyObject *bn = PyInt_FromLong((Py_intptr_t) id);
        PyObject *n = PyInt_FromLong((Py_intptr_t) oid);

#else
        classid oid = typeid(*(((t_uobject *) arg)->object)).name();

        if (!strcmp(id, oid))
            return 1;

        PyObject *bn = PyString_FromString(id);
        PyObject *n = PyString_FromString(oid);
#endif

        PyObject *list = PyDict_GetItem(types, bn);
        int b = PySequence_Contains(list, n);

        Py_DECREF(bn);
        Py_DECREF(n);

        return b ? b : PyObject_TypeCheck(arg, type);
    }

    return 0;
}

UObject **pl2cpa(PyObject *arg, size_t *len, classid id, PyTypeObject *type)
{
    if (PySequence_Check(arg))
    {
        *len = (int) PySequence_Size(arg);
        UObject **array = (UObject **) calloc(*len, sizeof(UObject *));

        for (size_t i = 0; i < *len; i++) {
            PyObject *obj = PySequence_GetItem(arg, i);

            if (isInstance(obj, id, type))
            {
                array[i] = ((t_uobject *) obj)->object;
                Py_DECREF(obj);
            }
            else
            {
                Py_DECREF(obj);
                free(array);
                return NULL;
            }
        }

        return array;
    }

    return NULL;
}

PyObject *cpa2pl(UObject **array, size_t len, PyObject *(*wrap)(UObject *, int))
{
    PyObject *list = PyList_New(len);

    for (size_t i = 0; i < len; i++)
        PyList_SET_ITEM(list, i, wrap(array[i], T_OWNED));

    return list;
}

Formattable *toFormattable(PyObject *arg)
{
    UDate date;
    double d;
    int i;
    PY_LONG_LONG l;
    UnicodeString *u, _u;
    char *s;

    if (!parseArg(arg, arg::d(&d)))
        return new Formattable(d);

    if (!parseArg(arg, arg::i(&i)))
        return new Formattable(i);

    if (!parseArg(arg, arg::L(&l)))
      return new Formattable((int64_t) l);

    if (!parseArg(arg, arg::c(&s)))
        return new Formattable(s);

    if (!parseArg(arg, arg::S(&u, &_u)))
        return new Formattable(*u);

    if (!parseArg(arg, arg::E(&date)))
        return new Formattable(date, Formattable::kIsDate);

    return NULL;
}

Formattable *toFormattableArray(PyObject *arg, size_t *len,
                                classid id, PyTypeObject *type)
{
    if (PySequence_Check(arg))
    {
        *len = PySequence_Size(arg);
        std::unique_ptr<Formattable[]> array(new Formattable[*len + 1]);

        if (!array.get())
            return (Formattable *) PyErr_NoMemory();

        for (size_t i = 0; i < *len; i++) {
            PyObject *obj = PySequence_GetItem(arg, i);

            if (isInstance(obj, id, type))
            {
                array[i] = *(Formattable *) ((t_uobject *) obj)->object;
                Py_DECREF(obj);
            }
            else
            {
                std::unique_ptr<Formattable> f(toFormattable(obj));

                if (f)
                {
                    array[i] = *f;
                    Py_DECREF(obj);
                }
                else
                {
                    Py_DECREF(obj);
                    return NULL;
                }
            }
        }

        return array.release();
    }

    return NULL;
}

UnicodeString *toUnicodeStringArray(PyObject *arg, size_t *len)
{
    if (PySequence_Check(arg))
    {
        *len = PySequence_Size(arg);
        std::unique_ptr<UnicodeString[]> array(new UnicodeString[*len + 1]);

        if (!array.get())
            return (UnicodeString *) PyErr_NoMemory();

        for (size_t i = 0; i < *len; i++) {
            PyObject *obj = PySequence_GetItem(arg, i);

            if (PyObject_TypeCheck(obj, &UObjectType_))
            {
                array[i] = *(UnicodeString *) ((t_uobject *) obj)->object;
                Py_DECREF(obj);
            }
            else
            {
                try {
                    PyObject_AsUnicodeString(obj, array[i]);
                } catch (ICUException e) {
                    Py_DECREF(obj);
                    e.reportError();

                    return NULL;
                }
            }
        }

        return array.release();
    }

    return NULL;
}

charsArg *toCharsArgArray(PyObject *arg, size_t *len)
{
    if (PySequence_Check(arg))
    {
        *len = PySequence_Size(arg);
        std::unique_ptr<charsArg[]> array(new charsArg[*len + 1]);

        if (!array.get())
            return (charsArg *) PyErr_NoMemory();

        for (size_t i = 0; i < *len; i++) {
            PyObject *obj = PySequence_GetItem(arg, i);

            if (PyUnicode_Check(obj))
            {
                PyObject *bytes = PyUnicode_AsUTF8String(obj);

                if (bytes == NULL)
                {
                    Py_DECREF(obj);
                    return NULL;
                }

                array[i].own(bytes);
            }
            else
            {
                array[i].borrow(obj);
            }

            Py_DECREF(obj);
        }

        return array.release();
    }

    return NULL;
}

int *toIntArray(PyObject *arg, size_t *len)
{
    if (PySequence_Check(arg))
    {
        *len = (int) PySequence_Size(arg);
        std::unique_ptr<int[]> array(new int[*len + 1]);

        if (!array.get())
            return (int *) PyErr_NoMemory();

        for (size_t i = 0; i < *len; i++) {
            PyObject *obj = PySequence_GetItem(arg, i);

#if PY_MAJOR_VERSION < 3
            if (PyInt_Check(obj))
            {
                array[i] = PyInt_AsLong(obj);
                Py_DECREF(obj);

                if (!PyErr_Occurred())
                    continue;
            }
            else if (PyLong_Check(obj))
            {
                array[i] = PyLong_AsLong(obj);
                Py_DECREF(obj);

                if (!PyErr_Occurred())
                    continue;
            }
#else
            if (PyLong_Check(obj))
            {
                array[i] = PyLong_AsLong(obj);
                Py_DECREF(obj);

                if (!PyErr_Occurred())
                    continue;
            }
#endif

            Py_DECREF(obj);
            return NULL;
        }

        return array.release();
    }

    return NULL;
}

double *toDoubleArray(PyObject *arg, size_t *len)
{
    if (PySequence_Check(arg))
    {
        *len = PySequence_Size(arg);
        std::unique_ptr<double[]> array(new double[*len + 1]);

        if (!array.get())
            return (double *) PyErr_NoMemory();

        for (size_t i = 0; i < *len; i++) {
            PyObject *obj = PySequence_GetItem(arg, i);

            if (PyFloat_Check(obj))
            {
                array[i] = PyFloat_AsDouble(obj);
                Py_DECREF(obj);
            }
#if PY_MAJOR_VERSION < 3
            else if (PyInt_Check(obj))
            {
                array[i] = (double) PyInt_AsLong(obj);
                Py_DECREF(obj);
            }
#endif
            else if (PyLong_Check(obj))
            {
                array[i] = PyLong_AsDouble(obj);
                Py_DECREF(obj);
            }
            else
            {
                Py_DECREF(obj);
                return NULL;
            }
        }

        return array.release();
    }

    return NULL;
}

UBool *toUBoolArray(PyObject *arg, size_t *len)
{
    if (PySequence_Check(arg))
    {
        *len = PySequence_Size(arg);
        UBool *array = new UBool[*len + 1];

        if (!array)
          return (UBool *) PyErr_NoMemory();

        for (size_t i = 0; i < *len; i++) {
            PyObject *obj = PySequence_GetItem(arg, i);

            array[i] = (UBool) PyObject_IsTrue(obj);
            Py_DECREF(obj);
        }

        return array;
    }

    return NULL;
}

PyObject *PyErr_SetArgsError(PyObject *self, const char *name, PyObject *args)
{
    if (!PyErr_Occurred())
    {
        PyObject *type = (PyObject *) self->ob_type;
        PyObject *err = Py_BuildValue("(OsO)", type, name, args);

        PyErr_SetObject(PyExc_InvalidArgsError, err);
        Py_DECREF(err);
    }

    return NULL;
}

PyObject *PyErr_SetArgsError(PyTypeObject *type, const char *name, PyObject *args)
{
    if (!PyErr_Occurred())
    {
        PyObject *err = Py_BuildValue("(OsO)", type, name, args);

        PyErr_SetObject(PyExc_InvalidArgsError, err);
        Py_DECREF(err);
    }

    return NULL;
}

int isUnicodeString(PyObject *arg)
{
    return (PyObject_TypeCheck(arg, &UObjectType_) &&
            ISINSTANCE(((t_uobject *) arg)->object, UnicodeString));
}

int32_t toUChar32(UnicodeString &u, UChar32 *c, UErrorCode &status)
{
#if U_ICU_VERSION_HEX >= 0x04020000
    return u.toUTF32(c, 1, status);
#else
    int32_t len = u.length();
    if (len >= 1)
        *c = u.char32At(0);
    return len;
#endif
}

UnicodeString fromUChar32(UChar32 c)
{
#if U_ICU_VERSION_HEX >= 0x04020000
    return UnicodeString::fromUTF32(&c, 1);
#else
    return UnicodeString(c);
#endif
}


void _init_common(PyObject *m)
{
    types = PyDict_New();
    PyModule_AddObject(m, "__types__", types);

#if PY_VERSION_HEX > 0x02040000
    PyDateTime_IMPORT;
#endif

    utcoffset_NAME = PyString_FromString("utcoffset");
    toordinal_NAME = PyString_FromString("toordinal");
    getDefault_NAME = PyString_FromString("getDefault");
}
