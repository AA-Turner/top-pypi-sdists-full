/* ====================================================================
 * Copyright (c) 2004-2025 Open Source Applications Foundation.
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
#include "structmember.h"

#include "bases.h"
#include "locale.h"
#include "format.h"
#include "dateformat.h"
#include "measureunit.h"
#include "numberformat.h"
#include "macros.h"

#include "arg.h"

#if U_ICU_VERSION_HEX >= 0x04080000
    DECLARE_CONSTANTS_TYPE(UTimeUnitFormatStyle)
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)
    DECLARE_CONSTANTS_TYPE(UMeasureFormatWidth)
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(63, 0, 0)
    DECLARE_CONSTANTS_TYPE(UListFormatterField)
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)
    DECLARE_CONSTANTS_TYPE(UFieldCategory)
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(67, 0, 0)
    DECLARE_CONSTANTS_TYPE(UListFormatterType)
    DECLARE_CONSTANTS_TYPE(UListFormatterWidth)
#endif

/* FieldPosition */

class t_fieldposition : public _wrapper {
public:
    FieldPosition *object;
};

static int t_fieldposition_init(t_fieldposition *self,
                                PyObject *args, PyObject *kwds);
static PyObject *t_fieldposition_getField(t_fieldposition *self);
static PyObject *t_fieldposition_setField(t_fieldposition *self, PyObject *arg);
static PyObject *t_fieldposition_getBeginIndex(t_fieldposition *self);
static PyObject *t_fieldposition_setBeginIndex(t_fieldposition *self,
                                               PyObject *arg);
static PyObject *t_fieldposition_getEndIndex(t_fieldposition *self);
static PyObject *t_fieldposition_setEndIndex(t_fieldposition *self,
                                             PyObject *arg);

static PyMethodDef t_fieldposition_methods[] = {
    DECLARE_METHOD(t_fieldposition, getField, METH_NOARGS),
    DECLARE_METHOD(t_fieldposition, setField, METH_O),
    DECLARE_METHOD(t_fieldposition, getBeginIndex, METH_NOARGS),
    DECLARE_METHOD(t_fieldposition, setBeginIndex, METH_O),
    DECLARE_METHOD(t_fieldposition, getEndIndex, METH_NOARGS),
    DECLARE_METHOD(t_fieldposition, setEndIndex, METH_O),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(FieldPosition, t_fieldposition, UObject,
                     FieldPosition, t_fieldposition_init)

/* ParsePosition */

class t_parseposition : public _wrapper {
public:
    ParsePosition *object;
};

static int t_parseposition_init(t_parseposition *self,
                                PyObject *args, PyObject *kwds);
static PyObject *t_parseposition_getIndex(t_parseposition *self);
static PyObject *t_parseposition_setIndex(t_parseposition *self, PyObject *arg);
static PyObject *t_parseposition_getErrorIndex(t_parseposition *self);
static PyObject *t_parseposition_setErrorIndex(t_parseposition *self,
                                               PyObject *arg);

static PyMethodDef t_parseposition_methods[] = {
    DECLARE_METHOD(t_parseposition, getIndex, METH_NOARGS),
    DECLARE_METHOD(t_parseposition, setIndex, METH_O),
    DECLARE_METHOD(t_parseposition, getErrorIndex, METH_NOARGS),
    DECLARE_METHOD(t_parseposition, setErrorIndex, METH_O),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(ParsePosition, t_parseposition, UObject,
                     ParsePosition, t_parseposition_init)

/* Format */

PyObject *t_format_format(t_format *self, PyObject *args);
static PyObject *t_format_parseObject(t_format *self, PyObject *args);
static PyObject *t_format_getLocale(t_format *self, PyObject *args);
static PyObject *t_format_getLocaleID(t_format *self, PyObject *args);

static PyMethodDef t_format_methods[] = {
    DECLARE_METHOD(t_format, format, METH_VARARGS),
    DECLARE_METHOD(t_format, parseObject, METH_VARARGS),
    DECLARE_METHOD(t_format, getLocale, METH_VARARGS),
    DECLARE_METHOD(t_format, getLocaleID, METH_VARARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(Format, t_format, UObject, Format, abstract_init)

/* MeasureFormat */

class t_measureformat : public _wrapper {
public:
    MeasureFormat *object;
    PyObject *locale;
};

#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)
static int t_measureformat_init(t_measureformat *self,
                                PyObject *args, PyObject *kwds);
#endif

static PyObject *t_measureformat_createCurrencyFormat(PyTypeObject *type,
                                                      PyObject *args);
#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)
static PyObject *t_measureformat_formatMeasure(t_measureformat *self,
                                               PyObject *args);
static PyObject *t_measureformat_formatMeasures(t_measureformat *self,
                                                PyObject *args);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(55, 0, 0)
static PyObject *t_measureformat_formatMeasurePerUnit(t_measureformat *self,
                                                      PyObject *args);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(58, 0, 0)
static PyObject *t_measureformat_getUnitDisplayName(t_measureformat *self,
                                                    PyObject *arg);
#endif

static PyMethodDef t_measureformat_methods[] = {
    DECLARE_METHOD(t_measureformat, createCurrencyFormat, METH_VARARGS | METH_CLASS),
#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)
    DECLARE_METHOD(t_measureformat, formatMeasure, METH_VARARGS),
    DECLARE_METHOD(t_measureformat, formatMeasures, METH_VARARGS),
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(55, 0, 0)
    DECLARE_METHOD(t_measureformat, formatMeasurePerUnit, METH_VARARGS),
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(58, 0, 0)
    DECLARE_METHOD(t_measureformat, getUnitDisplayName, METH_O),
#endif
    { NULL, NULL, 0, NULL }
};

static void t_measureformat_dealloc(t_measureformat *self)
{
    if (self->flags & T_OWNED)
        delete self->object;
    self->object = NULL;

    Py_CLEAR(self->locale);

    Py_TYPE(self)->tp_free((PyObject *) self);
}

#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)
DECLARE_TYPE(MeasureFormat, t_measureformat, Format, MeasureFormat,
             t_measureformat_init, t_measureformat_dealloc)
#else
DECLARE_TYPE(MeasureFormat, t_measureformat, Format, MeasureFormat,
             abstract_init, t_measureformat_dealloc)
#endif

#if U_ICU_VERSION_HEX >= 0x04020000

/* TimeUnitFormat */

class t_timeunitformat : public _wrapper {
public:
    TimeUnitFormat *object;
};

static int t_timeunitformat_init(t_timeunitformat *self,
                                 PyObject *args, PyObject *kwds);
static PyObject *t_timeunitformat_setLocale(t_timeunitformat *self,
                                            PyObject *arg);
static PyObject *t_timeunitformat_setNumberFormat(t_timeunitformat *self,
                                                  PyObject *arg);

static PyMethodDef t_timeunitformat_methods[] = {
    DECLARE_METHOD(t_timeunitformat, setLocale, METH_O),
    DECLARE_METHOD(t_timeunitformat, setNumberFormat, METH_O),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(TimeUnitFormat, t_timeunitformat, MeasureFormat,
                     TimeUnitFormat, t_timeunitformat_init)

#endif

/* MessageFormat */

class t_messageformat : public _wrapper {
public:
    MessageFormat *object;
};

static int t_messageformat_init(t_messageformat *self,
                                PyObject *args, PyObject *kwds);
static PyObject *t_messageformat_getLocale(t_messageformat *self);
static PyObject *t_messageformat_setLocale(t_messageformat *self,
                                           PyObject *arg);
static PyObject *t_messageformat_applyPattern(t_messageformat *self,
                                              PyObject *arg);
static PyObject *t_messageformat_toPattern(t_messageformat *self,
                                           PyObject *args);
static PyObject *t_messageformat_getFormats(t_messageformat *self);
static PyObject *t_messageformat_setFormats(t_messageformat *self,
                                            PyObject *arg);
static PyObject *t_messageformat_setFormat(t_messageformat *self,
                                           PyObject *args);
#if U_ICU_VERSION_HEX >= 0x04000000
static PyObject *t_messageformat_getFormatNames(t_messageformat *self);
#endif

static PyObject *t_messageformat_format(t_messageformat *self, PyObject *args);
static PyObject *t_messageformat_parse(t_messageformat *self, PyObject *args);
static PyObject *t_messageformat_formatMessage(PyTypeObject *type,
                                               PyObject *args);
static PyObject *t_messageformat_mod(t_messageformat *self, PyObject *args);

static PyNumberMethods t_messageformat_as_number = {
    0,                                 /* nb_add */
    0,                                 /* nb_subtract */
    0,                                 /* nb_multiply */
#if PY_MAJOR_VERSION >= 3
    (binaryfunc) t_messageformat_mod,  /* nb_remainder */
    0,                                 /* nb_divmod */
#else
    0,                                 /* nb_divide */
    (binaryfunc) t_messageformat_mod,  /* nb_remainder */
#endif
};

static PyMethodDef t_messageformat_methods[] = {
    DECLARE_METHOD(t_messageformat, getLocale, METH_NOARGS),
    DECLARE_METHOD(t_messageformat, setLocale, METH_O),
    DECLARE_METHOD(t_messageformat, applyPattern, METH_O),
    DECLARE_METHOD(t_messageformat, toPattern, METH_VARARGS),
    DECLARE_METHOD(t_messageformat, getFormats, METH_NOARGS),
    DECLARE_METHOD(t_messageformat, setFormats, METH_O),
    DECLARE_METHOD(t_messageformat, setFormat, METH_VARARGS),
#if U_ICU_VERSION_HEX >= 0x04000000
    DECLARE_METHOD(t_messageformat, getFormatNames, METH_NOARGS),
#endif
    DECLARE_METHOD(t_messageformat, format, METH_VARARGS),
    DECLARE_METHOD(t_messageformat, parse, METH_VARARGS),
    DECLARE_METHOD(t_messageformat, formatMessage, METH_VARARGS | METH_CLASS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(MessageFormat, t_messageformat, Format,
                     MessageFormat, t_messageformat_init)

#if U_ICU_VERSION_HEX >= 0x04000000

/* PluralRules */

class t_pluralrules : public _wrapper {
public:
    PluralRules *object;
};

static int t_pluralrules_init(t_pluralrules *self,
                              PyObject *args, PyObject *kwds);
static PyObject *t_pluralrules_select(t_pluralrules *self, PyObject *arg);
static PyObject *t_pluralrules_getKeywords(t_pluralrules *self);
static PyObject *t_pluralrules_getKeywordOther(t_pluralrules *self);
static PyObject *t_pluralrules_isKeyword(t_pluralrules *self, PyObject *arg);
static PyObject *t_pluralrules_createRules(PyTypeObject *type, PyObject *arg);
static PyObject *t_pluralrules_createDefaultRules(PyTypeObject *type);
static PyObject *t_pluralrules_forLocale(PyTypeObject *type, PyObject *arg);

static PyMethodDef t_pluralrules_methods[] = {
    DECLARE_METHOD(t_pluralrules, select, METH_O),
    DECLARE_METHOD(t_pluralrules, getKeywords, METH_NOARGS),
    DECLARE_METHOD(t_pluralrules, getKeywordOther, METH_NOARGS),
    DECLARE_METHOD(t_pluralrules, isKeyword, METH_O),
    DECLARE_METHOD(t_pluralrules, createRules, METH_O | METH_CLASS),
    DECLARE_METHOD(t_pluralrules, createDefaultRules, METH_NOARGS | METH_CLASS),
    DECLARE_METHOD(t_pluralrules, forLocale, METH_O | METH_CLASS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(PluralRules, t_pluralrules, UObject,
                     PluralRules, t_pluralrules_init)

/* PluralFormat */

class t_pluralformat : public _wrapper {
public:
    PluralFormat *object;
    PyObject *numberformat;
};

static int t_pluralformat_init(t_pluralformat *self,
                               PyObject *args, PyObject *kwds);
static PyObject *t_pluralformat_setLocale(t_pluralformat *self,
                                            PyObject *arg);
static PyObject *t_pluralformat_setNumberFormat(t_pluralformat *self,
                                                  PyObject *arg);
static PyObject *t_pluralformat_toPattern(t_pluralformat *self, PyObject *args);
static PyObject *t_pluralformat_applyPattern(t_pluralformat *self,
                                             PyObject *arg);
static PyObject *t_pluralformat_format(t_pluralformat *self, PyObject *args);

static PyMethodDef t_pluralformat_methods[] = {
    DECLARE_METHOD(t_pluralformat, setLocale, METH_O),
    DECLARE_METHOD(t_pluralformat, setNumberFormat, METH_O),
    DECLARE_METHOD(t_pluralformat, toPattern, METH_VARARGS),
    DECLARE_METHOD(t_pluralformat, applyPattern, METH_O),
    DECLARE_METHOD(t_pluralformat, format, METH_VARARGS),
    { NULL, NULL, 0, NULL }
};

static void t_pluralformat_dealloc(t_pluralformat *self)
{
    if (self->flags & T_OWNED)
        delete self->object;
    self->object = NULL;

    Py_CLEAR(self->numberformat);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

DECLARE_TYPE(PluralFormat, t_pluralformat, Format, PluralFormat,
             t_pluralformat_init, t_pluralformat_dealloc)

#endif

#if U_ICU_VERSION_HEX >= 0x04040000

/* SelectFormat */

class t_selectformat : public _wrapper {
public:
    SelectFormat *object;
};

static int t_selectformat_init(t_selectformat *self,
                               PyObject *args, PyObject *kwds);
static PyObject *t_selectformat_applyPattern(t_selectformat *self,
                                             PyObject *arg);
static PyObject *t_selectformat_toPattern(t_selectformat *self, PyObject *args);
static PyObject *t_selectformat_format(t_selectformat *self, PyObject *args);
static PyObject *t_selectformat_parseObject(t_selectformat *self,
                                            PyObject *args);

static PyMethodDef t_selectformat_methods[] = {
    DECLARE_METHOD(t_selectformat, applyPattern, METH_O),
    DECLARE_METHOD(t_selectformat, toPattern, METH_VARARGS),
    DECLARE_METHOD(t_selectformat, format, METH_VARARGS),
    DECLARE_METHOD(t_selectformat, parseObject, METH_VARARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(SelectFormat, t_selectformat, Format,
                     SelectFormat, t_selectformat_init)

#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)

class t_listformatter : public _wrapper {
public:
    ListFormatter *object;
};

static PyObject *t_listformatter_format(t_listformatter *self, PyObject *arg);
#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)
static PyObject *t_listformatter_formatStringsToValue(t_listformatter *self,
                                                      PyObject *arg);
#endif
static PyObject *t_listformatter_createInstance(PyTypeObject *type,
                                                PyObject *args);

static PyMethodDef t_listformatter_methods[] = {
    DECLARE_METHOD(t_listformatter, format, METH_O),
#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)
    DECLARE_METHOD(t_listformatter, formatStringsToValue, METH_O),
#endif
    DECLARE_METHOD(t_listformatter, createInstance, METH_VARARGS | METH_CLASS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(ListFormatter, t_listformatter, UObject,
                     ListFormatter, abstract_init)

#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(57, 0, 0)

class t_simpleformatter : public _wrapper {
public:
    SimpleFormatter *object;
    PyObject *pattern;
};

static int t_simpleformatter_init(t_simpleformatter *self,
                                  PyObject *args, PyObject *kwds);

static PyObject *t_simpleformatter_applyPattern(
    t_simpleformatter *self, PyObject *arg);
static PyObject *t_simpleformatter_applyPatternMinMaxArguments(
    t_simpleformatter *self, PyObject *args);
static PyObject *t_simpleformatter_getArgumentLimit(
    t_simpleformatter *self, PyObject *args);
static PyObject *t_simpleformatter_format(
    t_simpleformatter *self, PyObject *args);
static PyObject *t_simpleformatter_formatStrings(
    t_simpleformatter *self, PyObject *arg);

static PyNumberMethods t_simpleformatter_as_number = {
    0,                                             /* nb_add */
    0,                                             /* nb_subtract */
    0,                                             /* nb_multiply */
#if PY_MAJOR_VERSION >= 3
    (binaryfunc) t_simpleformatter_formatStrings,  /* nb_remainder */
    0,                                             /* nb_divmod */
#else
    0,                                             /* nb_divide */
    (binaryfunc) t_simpleformatter_formatStrings,  /* nb_remainder */
#endif
};

static PyMethodDef t_simpleformatter_methods[] = {
    DECLARE_METHOD(t_simpleformatter, applyPattern, METH_O),
    DECLARE_METHOD(t_simpleformatter, applyPatternMinMaxArguments, METH_VARARGS),
    DECLARE_METHOD(t_simpleformatter, getArgumentLimit, METH_NOARGS),
    DECLARE_METHOD(t_simpleformatter, format, METH_VARARGS),
    DECLARE_METHOD(t_simpleformatter, formatStrings, METH_O),
    { NULL, NULL, 0, NULL }
};

static void t_simpleformatter_dealloc(t_simpleformatter *self)
{
    if (self->flags & T_OWNED)
        delete self->object;
    self->object = NULL;

    Py_CLEAR(self->pattern);
    Py_TYPE(self)->tp_free((PyObject *) self);
}

DECLARE_TYPE(SimpleFormatter, t_simpleformatter, UMemory, SimpleFormatter,
             t_simpleformatter_init, t_simpleformatter_dealloc)

#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)

/* ConstrainedFieldPosition */

static int t_constrainedfieldposition_init(t_constrainedfieldposition *self,
                                           PyObject *args, PyObject *kwds);

static PyObject *t_constrainedfieldposition_constrainCategory(
    t_constrainedfieldposition *self, PyObject *arg);
static PyObject *t_constrainedfieldposition_constrainField(
    t_constrainedfieldposition *self, PyObject *args);
static PyObject *t_constrainedfieldposition_getCategory(
    t_constrainedfieldposition *self);
static PyObject *t_constrainedfieldposition_getField(
    t_constrainedfieldposition *self);
static PyObject *t_constrainedfieldposition_getStart(
    t_constrainedfieldposition *self);
static PyObject *t_constrainedfieldposition_getLimit(
    t_constrainedfieldposition *self);

static PyMethodDef t_constrainedfieldposition_methods[] = {
    DECLARE_METHOD(t_constrainedfieldposition, constrainCategory, METH_O),
    DECLARE_METHOD(t_constrainedfieldposition, constrainField, METH_VARARGS),
    DECLARE_METHOD(t_constrainedfieldposition, getCategory, METH_NOARGS),
    DECLARE_METHOD(t_constrainedfieldposition, getField, METH_NOARGS),
    DECLARE_METHOD(t_constrainedfieldposition, getStart, METH_NOARGS),
    DECLARE_METHOD(t_constrainedfieldposition, getLimit, METH_NOARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(
    ConstrainedFieldPosition, t_constrainedfieldposition, UMemory,
    ConstrainedFieldPosition, t_constrainedfieldposition_init)

/* FormattedValue */

class t_formattedvalue : public _wrapper {
public:
    FormattedValue *object;
    ConstrainedFieldPosition cfp;
};

static PyObject *t_formattedvalue_nextPosition(t_formattedvalue *self,
                                               PyObject *arg);

static PyMethodDef t_formattedvalue_methods[] = {
    DECLARE_METHOD(t_formattedvalue, nextPosition, METH_O),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(FormattedValue, t_formattedvalue, UMemory,
                     FormattedValue, abstract_init)

PyObject *wrap_FormattedValue(FormattedValue *value)
{
    using icu::number::FormattedNumber;
    using icu::number::FormattedNumberRange;

    RETURN_WRAPPED_IF_ISINSTANCE(value, FormattedDateInterval);
    RETURN_WRAPPED_IF_ISINSTANCE(value, FormattedNumber);
    RETURN_WRAPPED_IF_ISINSTANCE(value, FormattedList);
    RETURN_WRAPPED_IF_ISINSTANCE(value, FormattedRelativeDateTime);
    RETURN_WRAPPED_IF_ISINSTANCE(value, FormattedNumberRange);
    return wrap_FormattedValue(value, T_OWNED);
}

/* FormattedList */

class t_formattedlist : public _wrapper {
public:
    FormattedList *object;
    ConstrainedFieldPosition cfp;  // for iterator on t_formattedvalue
};

static PyMethodDef t_formattedlist_methods[] = {
    { NULL, NULL, 0, NULL }
};

DECLARE_BY_VALUE_TYPE(FormattedList, t_formattedlist, FormattedValue,
                      FormattedList, abstract_init)

#endif


/* FieldPosition */

static int t_fieldposition_init(t_fieldposition *self,
                                PyObject *args, PyObject *kwds)
{
    int i;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object = new FieldPosition();
        self->flags = T_OWNED;
        break;
      case 1:
        if (!parseArgs(args, arg::i(&i)))
        {
            self->object = new FieldPosition(i);
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      default:
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
    }

    if (self->object)
        return 0;

    return -1;
}

static PyObject *t_fieldposition_getField(t_fieldposition *self)
{
    return PyInt_FromLong(self->object->getField());
}

static PyObject *t_fieldposition_setField(t_fieldposition *self, PyObject *arg)
{
    int i;

    if (!parseArg(arg, arg::i(&i)))
    {
        self->object->setField(i);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setField", arg);
}

static PyObject *t_fieldposition_getBeginIndex(t_fieldposition *self)
{
    return PyInt_FromLong(self->object->getBeginIndex());
}

static PyObject *t_fieldposition_setBeginIndex(t_fieldposition *self,
                                               PyObject *arg)
{
    int i;

    if (!parseArg(arg, arg::i(&i)))
    {
        self->object->setBeginIndex(i);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setBeginIndex", arg);
}

static PyObject *t_fieldposition_getEndIndex(t_fieldposition *self)
{
    return PyInt_FromLong(self->object->getEndIndex());
}

static PyObject *t_fieldposition_setEndIndex(t_fieldposition *self,
                                             PyObject *arg)
{
    int i;

    if (!parseArg(arg, arg::i(&i)))
    {
        self->object->setEndIndex(i);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setEndIndex", arg);
}

DEFINE_RICHCMP__ARG__(FieldPosition, t_fieldposition)


/* ParsePosition */

static int t_parseposition_init(t_parseposition *self,
                                PyObject *args, PyObject *kwds)
{
    int i;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object = new ParsePosition();
        self->flags = T_OWNED;
        break;
      case 1:
        if (!parseArgs(args, arg::i(&i)))
        {
            self->object = new ParsePosition(i);
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      default:
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
    }

    if (self->object)
        return 0;

    return -1;
}

static PyObject *t_parseposition_getIndex(t_parseposition *self)
{
    return PyInt_FromLong(self->object->getIndex());
}

static PyObject *t_parseposition_setIndex(t_parseposition *self, PyObject *arg)
{
    int i;

    if (!parseArg(arg, arg::i(&i)))
    {
        self->object->setIndex(i);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setIndex", arg);
}

static PyObject *t_parseposition_getErrorIndex(t_parseposition *self)
{
    return PyInt_FromLong(self->object->getErrorIndex());
}

static PyObject *t_parseposition_setErrorIndex(t_parseposition *self,
                                               PyObject *arg)
{
    int i;

    if (!parseArg(arg, arg::i(&i)))
    {
        self->object->setErrorIndex(i);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setErrorIndex", arg);
}

DEFINE_RICHCMP__ARG__(ParsePosition, t_parseposition)


/* Format */

PyObject *t_format_format(t_format *self, PyObject *args)
{
    UnicodeString *u, _u;
    Formattable *obj;
    FieldPosition *fp;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj)))
        {
            STATUS_CALL(self->object->format(*obj, _u, status));
            return PyUnicode_FromUnicodeString(&_u);
        }
        break;
      case 2:
        if (!parseArgs(args,
                       arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj),
                       arg::U(&u)))
        {
            STATUS_CALL(self->object->format(*obj, *u, status));
            Py_RETURN_ARG(args, 1);
        }
        if (!parseArgs(args,
                       arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(*obj, _u, *fp, status));
            return PyUnicode_FromUnicodeString(&_u);
        }
        break;
      case 3:
        if (!parseArgs(args,
                       arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj),
                       arg::U(&u),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(*obj, *u, *fp, status));
            Py_RETURN_ARG(args, 1);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "format", args);
}

static PyObject *t_format_parseObject(t_format *self, PyObject *args)
{
    UnicodeString *u;
    UnicodeString _u;
    Formattable obj;
    ParsePosition *pp;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::S(&u, &_u)))
        {
            STATUS_CALL(self->object->parseObject(*u, obj, status));
            return wrap_Formattable(obj);
        }
        break;
      case 2:
        if (!parseArgs(args,
                       arg::S(&u, &_u),
                       arg::P<ParsePosition>(TYPE_CLASSID(ParsePosition), &pp)))
        {
            pp->setErrorIndex(-1);
            self->object->parseObject(*u, obj, *pp);
            if (pp->getErrorIndex() != -1)
                Py_RETURN_NONE;
            return wrap_Formattable(obj);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "parseObject", args);
}

static PyObject *t_format_getLocale(t_format *self, PyObject *args)
{
    ULocDataLocaleType type;
    Locale locale;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(locale = self->object->getLocale(ULOC_VALID_LOCALE,
                                                     status));
        return wrap_Locale(locale);
      case 1:
        if (!parseArgs(args, arg::Enum<ULocDataLocaleType>(&type)))
        {
            STATUS_CALL(locale = self->object->getLocale(type, status));
            return wrap_Locale(locale);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getLocale", args);
}

static PyObject *t_format_getLocaleID(t_format *self, PyObject *args)
{
    ULocDataLocaleType type;
    const char *id;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(id = self->object->getLocaleID(ULOC_VALID_LOCALE, status));
        return PyString_FromString(id);
      case 1:
        if (!parseArgs(args, arg::Enum<ULocDataLocaleType>(&type)))
        {
            STATUS_CALL(id = self->object->getLocaleID(type, status));
            return PyString_FromString(id);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getLocaleID", args);
}

DEFINE_RICHCMP__ARG__(Format, t_format)


/* MeasureFormat */

#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)

static int t_measureformat_init(t_measureformat *self,
                                PyObject *args, PyObject *kwds)
{
    UMeasureFormatWidth width;
    Locale *locale;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args,
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
                       arg::Enum<UMeasureFormatWidth>(&width)))
        {
            INT_STATUS_CALL(self->object = new MeasureFormat(*locale, width, status));
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      default:
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
    }

    if (self->object)
        return 0;

    return -1;
}

#endif

static PyObject *t_measureformat_createCurrencyFormat(PyTypeObject *type,
                                                      PyObject *args)
{
    MeasureFormat *format;
    Locale *locale;
    PyObject *localeObj = NULL;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(format = MeasureFormat::createCurrencyFormat(status));
        return wrap_MeasureFormat(format, T_OWNED);
      case 1:
        if (!parseArgs(args,
                       arg::p<Locale>(TYPE_CLASSID(Locale), &locale,
                                      &localeObj)))
        {
            UErrorCode status = U_ZERO_ERROR;
            MeasureFormat *format =
                MeasureFormat::createCurrencyFormat(*locale, status);

            if (U_FAILURE(status))
            {
                Py_XDECREF(localeObj);
                return ICUException(status).reportError();
            }

            PyObject *result = wrap_MeasureFormat(format, T_OWNED);
            t_measureformat *self = (t_measureformat *) result;

            self->locale = localeObj;

            return result;
        }
        break;
    }

    return PyErr_SetArgsError(type, "createCurrencyFormat", args);
}

#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)
static PyObject *t_measureformat_formatMeasure(t_measureformat *self,
                                               PyObject *args)
{
    Measure *measure;
    FieldPosition dont_care(FieldPosition::DONT_CARE);
    FieldPosition *fp;
    UnicodeString u;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::P<Measure>(TYPE_CLASSID(Measure), &measure)))
        {
            STATUS_CALL(self->object->formatMeasures(
                measure, 1, u, dont_care, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;

      case 2:
        if (!parseArgs(args,
                       arg::P<Measure>(TYPE_CLASSID(Measure), &measure),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->formatMeasures(
                measure, 1, u, *fp, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "formatMeasure", args);
}

// Limited to one measure since 'new Measure[len]' is forbidden because
// Measure() is protected.
static PyObject *t_measureformat_formatMeasures(t_measureformat *self,
                                                PyObject *args)
{
    std::unique_ptr<Measure *, decltype(free) *> measures(NULL, free);
    size_t len;
    FieldPosition dont_care(FieldPosition::DONT_CARE);
    FieldPosition *fp;
    UnicodeString u;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::Q<Measure>(TYPE_CLASSID(Measure), &measures, &len)))
        {
            if (len != 1)
                break;

            STATUS_CALL(self->object->formatMeasures(
                            measures.get()[0], 1, u, dont_care, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;

      case 2:
        if (!parseArgs(args,
                       arg::Q<Measure>(TYPE_CLASSID(Measure), &measures, &len),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            if (len != 1)
                break;

            STATUS_CALL(self->object->formatMeasures(
                            measures.get()[0], 1, u, *fp, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "formatMeasures", args);
}

#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(55, 0, 0)
static PyObject *t_measureformat_formatMeasurePerUnit(t_measureformat *self,
                                                      PyObject *args)
{
    Measure *measure;
    MeasureUnit *unit;
    FieldPosition *fp;
    UnicodeString u;
    FieldPosition dont_care(FieldPosition::DONT_CARE);

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args,
                       arg::P<Measure>(TYPE_CLASSID(Measure), &measure),
                       arg::P<MeasureUnit>(TYPE_CLASSID(MeasureUnit), &unit)))
        {
            STATUS_CALL(self->object->formatMeasurePerUnit(
                *measure, *unit, u, dont_care, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;
      case 3:
        if (!parseArgs(args,
                       arg::P<Measure>(TYPE_CLASSID(Measure), &measure),
                       arg::P<MeasureUnit>(TYPE_CLASSID(MeasureUnit), &unit),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->formatMeasurePerUnit(
                *measure, *unit, u, *fp, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "formatMeasurePerUnit", args);
}
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(58, 0, 0)
static PyObject *t_measureformat_getUnitDisplayName(t_measureformat *self,
                                                    PyObject *arg)
{
    MeasureUnit *unit;
    UnicodeString u;

    if (!parseArg(arg, arg::P<MeasureUnit>(TYPE_CLASSID(MeasureUnit), &unit)))
    {
        STATUS_CALL(u = self->object->getUnitDisplayName(*unit, status));
        return PyUnicode_FromUnicodeString(&u);
    }

    return PyErr_SetArgsError((PyObject *) self, "getUnitDisplayName", arg);
}
#endif // ICU >= 58


#if U_ICU_VERSION_HEX >= 0x04020000

/* TimeUnitFormat */

static int t_timeunitformat_init(t_timeunitformat *self,
                                 PyObject *args, PyObject *kwds)
{
#if U_ICU_VERSION_HEX >= 0x04080000
    UTimeUnitFormatStyle style;
#else
    TimeUnitFormat::EStyle style;
#endif
    Locale *locale;

    switch (PyTuple_Size(args)) {
      case 0:
        INT_STATUS_CALL(self->object = new TimeUnitFormat(status));
        self->flags = T_OWNED;
        break;
      case 1:
        if (!parseArgs(args, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
        {
            INT_STATUS_CALL(self->object = new TimeUnitFormat(*locale, status));
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      case 2:
        if (!parseArgs(args,
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
#if U_ICU_VERSION_HEX >= 0x04080000
                       arg::Enum<UTimeUnitFormatStyle>(&style)))
#else
                       arg::Enum<TimeUnitFormat::EStyle>(&style)))
#endif
        {
            INT_STATUS_CALL(self->object = new TimeUnitFormat(*locale, style, status));
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      default:
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
    }

    if (self->object)
        return 0;

    return -1;
}

static PyObject *t_timeunitformat_setLocale(t_timeunitformat *self,
                                            PyObject *arg)
{
    Locale *locale;

    if (!parseArg(arg, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
    {
        STATUS_CALL(self->object->setLocale(*locale, status)); /* copied */
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setLocale", arg);
}

static PyObject *t_timeunitformat_setNumberFormat(t_timeunitformat *self,
                                                  PyObject *arg)
{
    NumberFormat *format;

    if (!parseArg(arg, arg::P<NumberFormat>(TYPE_CLASSID(NumberFormat), &format))) /* copied */
    {
        STATUS_CALL(self->object->setNumberFormat(*format, status));
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setNumberFormat", arg);
}

#endif


/* MessageFormat */

static int t_messageformat_init(t_messageformat *self,
                                PyObject *args, PyObject *kwds)
{
    UnicodeString *u, _u;
    Locale *locale;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::S(&u, &_u)))
        {
            MessageFormat *format;

            INT_STATUS_CALL(format = new MessageFormat(*u, status));
            self->object = format;
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      case 2:
        if (!parseArgs(args,
                       arg::S(&u, &_u),
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
        {
            MessageFormat *format;

            INT_STATUS_PARSER_CALL(format = new MessageFormat(*u, *locale, parseError, status));
            self->object = format;
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      default:
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
    }

    if (self->object)
        return 0;

    return -1;
}

static PyObject *t_messageformat_getLocale(t_messageformat *self)
{
    return wrap_Locale(self->object->getLocale());
}

static PyObject *t_messageformat_setLocale(t_messageformat *self,
                                           PyObject *arg)
{
    Locale *locale;

    if (!parseArg(arg, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
    {
        self->object->setLocale(*locale); /* copied */
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setLocale", arg);
}

static PyObject *t_messageformat_applyPattern(t_messageformat *self,
                                              PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        STATUS_PARSER_CALL(self->object->applyPattern(*u, parseError, status));
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "applyPattern", arg);
}

static PyObject *t_messageformat_toPattern(t_messageformat *self,
                                           PyObject *args)
{
    UnicodeString *u, _u;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object->toPattern(_u);
        return PyUnicode_FromUnicodeString(&_u);
      case 1:
        if (!parseArgs(args, arg::U(&u)))
        {
            self->object->toPattern(*u);
            Py_RETURN_ARG(args, 0);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "toPattern", args);
}

PyObject *wrap_Format(Format *format)
{
    RETURN_WRAPPED_IF_ISINSTANCE(format, SimpleDateFormat);
    RETURN_WRAPPED_IF_ISINSTANCE(format, MessageFormat);
#if U_ICU_VERSION_HEX >= 0x04000000
    RETURN_WRAPPED_IF_ISINSTANCE(format, PluralFormat);
#endif
#if U_ICU_VERSION_HEX >= 0x04020000
    RETURN_WRAPPED_IF_ISINSTANCE(format, TimeUnitFormat);
#endif
#if U_ICU_VERSION_HEX >= 0x04040000
    RETURN_WRAPPED_IF_ISINSTANCE(format, SelectFormat);
#endif
    RETURN_WRAPPED_IF_ISINSTANCE(format, ChoiceFormat);
    RETURN_WRAPPED_IF_ISINSTANCE(format, DecimalFormat);
    RETURN_WRAPPED_IF_ISINSTANCE(format, RuleBasedNumberFormat);
    return wrap_Format(format, T_OWNED);
}

static PyObject *t_messageformat_getFormats(t_messageformat *self)
{
    int count;
    const Format **formats = self->object->getFormats(count);
    PyObject *list = PyList_New(count);

    for (int i = 0; i < count; i++) {
        if (formats[i] == NULL)
        {
            PyList_SET_ITEM(list, i, Py_None);
            Py_INCREF(Py_None);
        }
        else
        {
            PyObject *obj = wrap_Format(formats[i]->clone());
            PyList_SET_ITEM(list, i, obj);
        }
    }

    return list;
}

static PyObject *t_messageformat_setFormats(t_messageformat *self,
                                            PyObject *arg)
{
    std::unique_ptr<Format *, decltype(free) *> formats(NULL, free);
    size_t len;

    if (!parseArg(arg, arg::Q<Format>(TYPE_ID(Format), &formats, &len)))
    {
        self->object->setFormats(const_cast<const Format **>(formats.get()), len); /* copied */
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setFormats", arg);
}

static PyObject *t_messageformat_setFormat(t_messageformat *self,
                                           PyObject *args)
{
    Format *format;
    int i;

    if (!parseArgs(args, arg::i(&i), arg::P<Format>(TYPE_ID(Format), &format)))
    {
        self->object->setFormat(i, *format); /* copied */
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setFormat", args);
}

static PyObject *t_messageformat_format(t_messageformat *self, PyObject *args)
{
    std::unique_ptr<Formattable[]> f;
    UnicodeString *u, _u;
    FieldPosition *fp, _fp;
    std::unique_ptr<UnicodeString[]> strings;
    size_t len, strings_len;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args,
                       arg::R<Formattable>(TYPE_CLASSID(Formattable), &f, &len,
                                           toFormattableArray)))
        {
            STATUS_CALL(self->object->format(f.get(), len, _u, _fp, status));
            return PyUnicode_FromUnicodeString(&_u);
        }
        break;

      case 2:
        if (!parseArgs(args,
                       arg::R<Formattable>(TYPE_CLASSID(Formattable), &f, &len,
                                           toFormattableArray),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(f.get(), len, _u, *fp, status));
            return PyUnicode_FromUnicodeString(&_u);
        }
        if (!parseArgs(args,
                       arg::R<Formattable>(TYPE_CLASSID(Formattable), &f, &len,
                                           toFormattableArray),
                       arg::U(&u)))
        {
            STATUS_CALL(self->object->format(f.get(), len, *u, _fp, status));
            Py_RETURN_ARG(args, 1);
        }
#if U_ICU_VERSION_HEX >= VERSION_HEX(4, 0, 0)
        if (!parseArgs(args,
                       arg::T(&strings, &strings_len),
                       arg::R<Formattable>(TYPE_CLASSID(Formattable), &f, &len,
                                           toFormattableArray)))
        {
            STATUS_CALL(self->object->format(strings.get(), f.get(), len < strings_len ? len : strings_len, _u, status));
            return PyUnicode_FromUnicodeString(&_u);
        }
#endif
        break;

      case 3:
       if (!parseArgs(args,
                      arg::R<Formattable>(TYPE_CLASSID(Formattable), &f, &len,
                                          toFormattableArray),
                      arg::U(&u),
                      arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(f.get(), len, *u, *fp, status));
            Py_RETURN_ARG(args, 1);
        }
        break;
    }

    return t_format_format((t_format *) self, args);
}

#if U_ICU_VERSION_HEX >= 0x04000000

static PyObject *t_messageformat_getFormatNames(t_messageformat *self)
{
    StringEnumeration *se;
    STATUS_CALL(se = self->object->getFormatNames(status));

    return wrap_StringEnumeration(se, T_OWNED);
}

#endif

static PyObject *fromFormattableArray(Formattable *formattables, int len)
{
    PyObject *list = PyList_New(len);

    for (int i = 0; i < len; i++)
        PyList_SET_ITEM(list, i, wrap_Formattable(formattables[i]));

    return list;
}

static PyObject *t_messageformat_parse(t_messageformat *self, PyObject *args)
{
    std::unique_ptr<Formattable> f;
    int len;
    UnicodeString *u, _u;
    ParsePosition *pp;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::S(&u, &_u)))
        {
            STATUS_CALL(f.reset(self->object->parse(*u, len, status)));
            return fromFormattableArray(f.get(), len);
        }
        break;
      case 2:
        if (!parseArgs(args,
                       arg::S(&u, &_u),
                       arg::P<ParsePosition>(TYPE_CLASSID(ParsePosition), &pp)))
        {
            pp->setErrorIndex(-1);
            f.reset(self->object->parse(*u, *pp, len));
            if (pp->getErrorIndex() != -1)
                Py_RETURN_NONE;
            return fromFormattableArray(f.get(), len);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "parse", args);
}

static PyObject *t_messageformat_formatMessage(PyTypeObject *type,
                                               PyObject *args)
{
    std::unique_ptr<Formattable[]> f;
    size_t len;
    UnicodeString *u, *v;
    UnicodeString _u, _v;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args,
                       arg::S(&u, &_u),
                       arg::R<Formattable>(TYPE_CLASSID(Formattable), &f, &len,
                                           toFormattableArray)))
        {
            STATUS_CALL(MessageFormat::format(*u, f.get(), len, _v, status));
            return PyUnicode_FromUnicodeString(&_v);
        }
        break;
      case 3:
        if (!parseArgs(args,
                       arg::S(&u, &_u),
                       arg::R<Formattable>(TYPE_CLASSID(Formattable), &f, &len,
                                           toFormattableArray),
                       arg::U(&v)))
        {
            STATUS_CALL(MessageFormat::format(*u, f.get(), len, *v, status));
            Py_RETURN_ARG(args, 2);
        }
        break;
    }

    return PyErr_SetArgsError(type, "formatMessage", args);
}

static PyObject *t_messageformat_str(t_messageformat *self)
{
    UnicodeString u;

    self->object->toPattern(u);
    return PyUnicode_FromUnicodeString(&u);
}

static PyObject *t_messageformat_mod(t_messageformat *self, PyObject *args)
{
    size_t len;
    std::unique_ptr<Formattable[]> f(toFormattableArray(args, &len, TYPE_CLASSID(Formattable)));
    UnicodeString _u;
    FieldPosition _fp;

    if (!f.get())
    {
        PyErr_SetObject(PyExc_TypeError, args);
        return NULL;
    }

    STATUS_CALL(self->object->format(f.get(), len, _u, _fp, status));

    return PyUnicode_FromUnicodeString(&_u);
}


#if U_ICU_VERSION_HEX >= 0x04000000

/* PluralRules */

static int t_pluralrules_init(t_pluralrules *self,
                              PyObject *args, PyObject *kwds)
{
    if (PyTuple_Size(args) == 0)
    {
        INT_STATUS_CALL(self->object = new PluralRules(status));
        self->flags = T_OWNED;

        return 0;
    }

    PyErr_SetArgsError((PyObject *) self, "__init__", args);
    return -1;
}

static PyObject *t_pluralrules_select(t_pluralrules *self, PyObject *arg)
{
    UnicodeString u;
    int n;
    double d;
#if U_ICU_VERSION_HEX >= VERSION_HEX(68, 0, 0)
    PyObject *formatted;
#endif

    if (!parseArg(arg, arg::i(&n)))
        u = self->object->select(n);
    else if (!parseArg(arg, arg::d(&d)))
        u = self->object->select(d);
#if U_ICU_VERSION_HEX >= VERSION_HEX(68, 0, 0)
    else if (!parseArg(arg, arg::O(&FormattedNumberType_, &formatted)))
    {
        STATUS_CALL(u = self->object->select(
            *((t_formattednumber *) formatted)->object, status));
    }
    else if (!parseArg(arg, arg::O(&FormattedNumberRangeType_, &formatted)))
    {
        STATUS_CALL(u = self->object->select(
            *((t_formattednumberrange *) formatted)->object, status));
    }
#endif
    else
        return PyErr_SetArgsError((PyObject *) self, "select", arg);

    return PyUnicode_FromUnicodeString(&u);
}

static PyObject *t_pluralrules_getKeywords(t_pluralrules *self)
{
    StringEnumeration *se;
    STATUS_CALL(se = self->object->getKeywords(status));

    return wrap_StringEnumeration(se, T_OWNED);
}

static PyObject *t_pluralrules_getKeywordOther(t_pluralrules *self)
{
    UnicodeString u = self->object->getKeywordOther();
    return PyUnicode_FromUnicodeString(&u);
}

static PyObject *t_pluralrules_isKeyword(t_pluralrules *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        UBool b = self->object->isKeyword(*u);
        Py_RETURN_BOOL(b);
    }

    return PyErr_SetArgsError((PyObject *) self, "isKeyword", arg);
}


static PyObject *t_pluralrules_createRules(PyTypeObject *type, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        PluralRules *rules;
        STATUS_CALL(rules = PluralRules::createRules(*u, status));
        return wrap_PluralRules(rules, T_OWNED);
    }

    return PyErr_SetArgsError(type, "createRules", arg);
}

static PyObject *t_pluralrules_createDefaultRules(PyTypeObject *type)
{
    PluralRules *rules;
    STATUS_CALL(rules = PluralRules::createDefaultRules(status));

    return wrap_PluralRules(rules, T_OWNED);
}

static PyObject *t_pluralrules_forLocale(PyTypeObject *type, PyObject *arg)
{
    Locale *locale;

    if (!parseArg(arg, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
    {
        PluralRules *rules;
        STATUS_CALL(rules = PluralRules::forLocale(*locale, status));
        return wrap_PluralRules(rules, T_OWNED);
    }

    return PyErr_SetArgsError(type, "forLocale", arg);
}

DEFINE_RICHCMP__ARG__(PluralRules, t_pluralrules)


/* PluralFormat */

static int t_pluralformat_init(t_pluralformat *self,
                               PyObject *args, PyObject *kwds)
{
    Locale *locale;
    PluralRules *rules;
    UnicodeString *u, _u;

    switch (PyTuple_Size(args)) {
      case 0:
        INT_STATUS_CALL(self->object = new PluralFormat(status));
        self->flags = T_OWNED;
        break;
      case 1:
        if (!parseArgs(args, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
        {
            INT_STATUS_CALL(self->object = new PluralFormat(*locale, status));
            self->flags = T_OWNED;
            break;
        }
        if (!parseArgs(args, arg::P<PluralRules>(TYPE_CLASSID(PluralRules), &rules)))
        {
            INT_STATUS_CALL(self->object = new PluralFormat(*rules, status));
            self->flags = T_OWNED;
            break;
        }
        if (!parseArgs(args, arg::S(&u, &_u)))
        {
            INT_STATUS_CALL(self->object = new PluralFormat(*u, status));
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      case 2:
        if (!parseArgs(args,
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
                       arg::P<PluralRules>(TYPE_CLASSID(PluralRules), &rules)))
        {
            INT_STATUS_CALL(self->object = new PluralFormat(*locale, *rules,
                                                            status));
            self->flags = T_OWNED;
            break;
        }
        if (!parseArgs(args,
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
                       arg::S(&u, &_u)))
        {
            INT_STATUS_CALL(self->object = new PluralFormat(*locale, *u,
                                                            status));
            self->flags = T_OWNED;
            break;
        }
        if (!parseArgs(args,
                       arg::P<PluralRules>(TYPE_CLASSID(PluralRules), &rules),
                       arg::S(&u, &_u)))
        {
            INT_STATUS_CALL(self->object = new PluralFormat(*rules, *u,
                                                            status));
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      case 3:
        if (!parseArgs(args,
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
                       arg::P<PluralRules>(TYPE_CLASSID(PluralRules), &rules),
                       arg::S(&u, &_u)))
        {
            INT_STATUS_CALL(self->object = new PluralFormat(*locale, *rules, *u,
                                                            status));
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      default:
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
    }

    if (self->object)
        return 0;

    return -1;
}

static PyObject *t_pluralformat_setLocale(t_pluralformat *self, PyObject *arg)
{
    Locale *locale;

    if (!parseArg(arg, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
    {
        STATUS_CALL(self->object->setLocale(*locale, status)); /* copied */
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setLocale", arg);
}

static PyObject *t_pluralformat_setNumberFormat(t_pluralformat *self,
                                                PyObject *arg)
{
    NumberFormat *format;

    if (!parseArg(arg,
                  arg::p<NumberFormat>(TYPE_CLASSID(NumberFormat), &format,
                                       &self->numberformat))) /* ref'd */
    {
        STATUS_CALL(self->object->setNumberFormat(format, status));
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setNumberFormat", arg);
}

static PyObject *t_pluralformat_toPattern(t_pluralformat *self, PyObject *args)
{
    UnicodeString *u, _u;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object->toPattern(_u);
        return PyUnicode_FromUnicodeString(&_u);
      case 1:
        if (!parseArgs(args, arg::U(&u)))
        {
            self->object->toPattern(*u);
            Py_RETURN_ARG(args, 0);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "toPattern", args);
}

static PyObject *t_pluralformat_applyPattern(t_pluralformat *self,
                                             PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        STATUS_CALL(self->object->applyPattern(*u, status));
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "applyPattern", arg);
}

static PyObject *t_pluralformat_format(t_pluralformat *self, PyObject *args)
{
    UnicodeString *u, _u;
    FieldPosition *fp, _fp;
    double d;
    int n;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::i(&n)))
        {
            STATUS_CALL(_u = self->object->format(n, status));
            return PyUnicode_FromUnicodeString(&_u);
        }
        if (!parseArgs(args, arg::d(&d)))
        {
            STATUS_CALL(_u = self->object->format(d, status));
            return PyUnicode_FromUnicodeString(&_u);
        }
        break;
      case 2:
        if (!parseArgs(args, arg::i(&n), arg::S(&u, &_u)))
        {
            STATUS_CALL(self->object->format(n, *u, _fp, status));
            Py_RETURN_ARG(args, 1);
        }
        if (!parseArgs(args, arg::d(&d), arg::S(&u, &_u)))
        {
            STATUS_CALL(self->object->format(d, *u, _fp, status));
            Py_RETURN_ARG(args, 1);
        }
        break;
      case 3:
        if (!parseArgs(args,
                       arg::i(&n),
                       arg::S(&u, &_u),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(n, *u, *fp, status));
            Py_RETURN_ARG(args, 1);
        }
        if (!parseArgs(args,
                       arg::d(&d),
                       arg::S(&u, &_u),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(d, *u, *fp, status));
            Py_RETURN_ARG(args, 1);
        }
        break;
    }

    return t_format_format((t_format *) self, args);
}

static PyObject *t_pluralformat_str(t_pluralformat *self)
{
    UnicodeString u;

    self->object->toPattern(u);
    return PyUnicode_FromUnicodeString(&u);
}

#endif


#if U_ICU_VERSION_HEX >= 0x04040000

/* SelectFormat */

static int t_selectformat_init(t_selectformat *self,
                               PyObject *args, PyObject *kwds)
{
    UnicodeString *u, _u;

    if (!parseArgs(args, arg::S(&u, &_u)))
    {
        SelectFormat *format;

        INT_STATUS_CALL(format = new SelectFormat(*u, status));
        self->object = format;
        self->flags = T_OWNED;

        return 0;
    }

    PyErr_SetArgsError((PyObject *) self, "__init__", args);
    return -1;
}

static PyObject *t_selectformat_applyPattern(t_selectformat *self,
                                             PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        STATUS_CALL(self->object->applyPattern(*u, status));
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "applyPattern", arg);
}

static PyObject *t_selectformat_toPattern(t_selectformat *self, PyObject *args)
{
    UnicodeString *u, _u;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object->toPattern(_u);
        return PyUnicode_FromUnicodeString(&_u);
      case 1:
        if (!parseArgs(args, arg::U(&u)))
        {
            self->object->toPattern(*u);
            Py_RETURN_ARG(args, 0);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "toPattern", args);
}

PyObject *t_selectformat_format(t_selectformat *self, PyObject *args)
{
    UnicodeString *u0, _u0;
    UnicodeString *u1, _u1;
    Formattable *obj;
    FieldPosition *fp, _fp;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj)))
        {
            STATUS_CALL(self->object->format(*obj, _u1, _fp, status));
            return PyUnicode_FromUnicodeString(&_u1);
        }
        if (!parseArgs(args, arg::S(&u0, &_u0)))
        {
            STATUS_CALL(self->object->format(*u0, _u1, _fp, status));
            return PyUnicode_FromUnicodeString(&_u1);
        }
        break;
      case 2:
        if (!parseArgs(args,
                       arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj),
                       arg::U(&u1)))
        {
            STATUS_CALL(self->object->format(*obj, *u1, _fp, status));
            Py_RETURN_ARG(args, 1);
        }
        if (!parseArgs(args, arg::S(&u0, &_u0), arg::U(&u1)))
        {
            STATUS_CALL(self->object->format(*u0, *u1, _fp, status));
            Py_RETURN_ARG(args, 1);
        }
        if (!parseArgs(args,
                       arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(*obj, _u1, *fp, status));
            return PyUnicode_FromUnicodeString(&_u1);
        }
        if (!parseArgs(args,
                       arg::S(&u0, &_u0),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(*u0, _u1, *fp, status));
            return PyUnicode_FromUnicodeString(&_u1);
        }
        break;
      case 3:
        if (!parseArgs(args,
                       arg::P<Formattable>(TYPE_CLASSID(Formattable), &obj),
                       arg::U(&u1),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(*obj, *u1, *fp, status));
            Py_RETURN_ARG(args, 1);
        }
        if (!parseArgs(args,
                       arg::S(&u0, &_u0),
                       arg::U(&u1),
                       arg::P<FieldPosition>(TYPE_CLASSID(FieldPosition), &fp)))
        {
            STATUS_CALL(self->object->format(*u0, *u1, *fp, status));
            Py_RETURN_ARG(args, 1);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "format", args);
}

static PyObject *t_selectformat_parseObject(t_selectformat *self,
                                            PyObject *args)
{
    PyErr_SetString(PyExc_NotImplementedError, "SelectFormat.parseObject()");
    return NULL;
}

static PyObject *t_selectformat_str(t_selectformat *self)
{
    UnicodeString u;

    self->object->toPattern(u);
    return PyUnicode_FromUnicodeString(&u);
}

#endif


#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)

/* ListFormatter */

static PyObject *t_listformatter_format(t_listformatter *self, PyObject *arg)
{
    std::unique_ptr<UnicodeString[]> array;
    size_t count;

    if (!parseArg(arg, arg::T(&array, &count)))
    {
        UnicodeString u;

        STATUS_CALL(self->object->format(array.get(), (int32_t) count, u, status));
        return PyUnicode_FromUnicodeString(&u);
    }

    return PyErr_SetArgsError((PyObject *) self, "format", arg);
}

#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)
static PyObject *t_listformatter_formatStringsToValue(t_listformatter *self,
                                                      PyObject *arg)
{
    std::unique_ptr<UnicodeString[]> array;
    size_t count;

    if (!parseArg(arg, arg::T(&array, &count)))
    {
        FormattedList value;

        STATUS_CALL(value = self->object->formatStringsToValue(array.get(), (int32_t) count, status));

        return wrap_FormattedList(value);
    }

    return PyErr_SetArgsError((PyObject *) self, "formatStringsToValue", arg);
}
#endif

static PyObject *t_listformatter_createInstance(PyTypeObject *type,
                                                PyObject *args)
{
    ListFormatter *formatter;
    Locale *locale;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(formatter = ListFormatter::createInstance(status));
        return wrap_ListFormatter(formatter, T_OWNED);
      case 1:
        if (!parseArgs(args, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
        {
            STATUS_CALL(formatter = ListFormatter::createInstance(
                *locale, status));
            return wrap_ListFormatter(formatter, T_OWNED);
        }
        break;
#if U_ICU_VERSION_HEX >= VERSION_HEX(67, 0, 0)
      case 3: {
        UListFormatterType type;
        UListFormatterWidth width;
        if (!parseArgs(args,
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
                       arg::Enum<UListFormatterType>(&type),
                       arg::Enum<UListFormatterWidth>(&width)))
        {
            STATUS_CALL(formatter = ListFormatter::createInstance(
                *locale, type, width, status));
            return wrap_ListFormatter(formatter, T_OWNED);
        }
      }
#endif
    }

    return PyErr_SetArgsError(type, "createInstance", args);
}

#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(57, 0, 0)

static int t_simpleformatter_init(t_simpleformatter *self,
                                  PyObject *args, PyObject *kwds)
{
    UnicodeString *u, _u;
    int n0, n1;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object = new SimpleFormatter();
        self->pattern = Py_None;
        Py_INCREF(self->pattern);
        self->flags = T_OWNED;
        return 0;

      case 1:
        if (!parseArgs(args, arg::S(&u, &_u)))
        {
            SimpleFormatter *formatter;

            INT_STATUS_CALL(formatter = new SimpleFormatter(*u, status));
            self->object = formatter;
            self->pattern = PyUnicode_FromUnicodeString(u);
            self->flags = T_OWNED;

            return 0;
        }
        break;

      case 3:
        if (!parseArgs(args, arg::S(&u, &_u), arg::i(&n0), arg::i(&n1)))
        {
            SimpleFormatter *formatter;

            INT_STATUS_CALL(
                formatter = new SimpleFormatter(*u, n0, n1, status));
            self->object = formatter;
            self->pattern = PyUnicode_FromUnicodeString(u);
            self->flags = T_OWNED;

            return 0;
        }
        break;
    }

    PyErr_SetArgsError((PyObject *) self, "__init__", args);
    return -1;
}

static PyObject *t_simpleformatter_str(t_simpleformatter *self)
{
    Py_INCREF(self->pattern);
    return self->pattern;
}

static PyObject *t_simpleformatter_applyPattern(
    t_simpleformatter *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        UBool result;

        STATUS_CALL(result = self->object->applyPattern(*u, status));
        Py_DECREF(self->pattern);
        self->pattern = PyUnicode_FromUnicodeString(u);

        Py_RETURN_BOOL(result);
    }

    return PyErr_SetArgsError((PyObject *) self, "applyPattern", arg);
}

static PyObject *t_simpleformatter_applyPatternMinMaxArguments(
    t_simpleformatter *self, PyObject *args)
{
    UnicodeString *u, _u;
    int n0, n1;

    switch (PyTuple_Size(args)) {
      case 3:
        if (!parseArgs(args, arg::S(&u, &_u), arg::i(&n0), arg::i(&n1)))
        {
            UBool result;

            STATUS_CALL(result = self->object->applyPatternMinMaxArguments(
                *u, n0, n1, status));
            Py_DECREF(self->pattern);
            self->pattern = PyUnicode_FromUnicodeString(u);

            Py_RETURN_BOOL(result);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "applyPatternMinMaxArguments", args);
}

static PyObject *t_simpleformatter_getArgumentLimit(
    t_simpleformatter *self, PyObject *args)
{
    return PyInt_FromLong(self->object->getArgumentLimit());
}

static PyObject *t_simpleformatter_format(
    t_simpleformatter *self, PyObject *args)
{
    UnicodeString *u0, *u1, *u2, _u0, _u1, _u2;
    UnicodeString u;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::S(&u0, &_u0)))
        {
            STATUS_CALL(u = self->object->format(*u0, u, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;
      case 2:
        if (!parseArgs(args, arg::S(&u0, &_u0), arg::S(&u1, &_u1)))
        {
            STATUS_CALL(u = self->object->format(*u0, *u1, u, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;
      case 3:
        if (!parseArgs(args,
                       arg::S(&u0, &_u0),
                       arg::S(&u1, &_u1),
                       arg::S(&u2, &_u2)))
        {
            STATUS_CALL(u = self->object->format(*u0, *u1, *u2, u, status));
            return PyUnicode_FromUnicodeString(&u);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "format", args);
}

static PyObject *t_simpleformatter_formatStrings(
    t_simpleformatter *self, PyObject *arg)
{
    UnicodeString u;
    std::unique_ptr<UnicodeString[]> strings;
    size_t count;

    if (!parseArg(arg, arg::T(&strings, &count)))
    {
        std::unique_ptr<UnicodeString *[]> args(new UnicodeString *[count]);
        if (!args.get())
            return PyErr_NoMemory();

        for (size_t i = 0; i < count; ++i)
            args[i] = &strings[i];

        STATUS_CALL(self->object->formatAndAppend(args.get(), count, u, NULL, 0, status));
        return PyUnicode_FromUnicodeString(&u);
    }

    return PyErr_SetArgsError((PyObject *) self, "formatStrings", arg);
}

#endif  // ICU >= 57

#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)

/* ConstrainedFieldPosition */

static int t_constrainedfieldposition_init(t_constrainedfieldposition *self,
                                           PyObject *args, PyObject *kwds)
{
    switch (PyTuple_Size(args)) {
      case 0:
        self->object = new ConstrainedFieldPosition();
        self->flags = T_OWNED;
        return 0;
    }

    PyErr_SetArgsError((PyObject *) self, "__init__", args);
    return -1;
}

static PyObject *t_constrainedfieldposition_constrainCategory(
    t_constrainedfieldposition *self, PyObject *arg)
{
    int category;

    if (!parseArg(arg, arg::i(&category)))
        self->object->constrainCategory(category);

    Py_RETURN_NONE;
}

static PyObject *t_constrainedfieldposition_constrainField(
    t_constrainedfieldposition *self, PyObject *args)
{
    int category, field;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args, arg::i(&category), arg::i(&field)))
        {
            self->object->constrainField(category, field);
            Py_RETURN_NONE;
        }
    }

    return PyErr_SetArgsError((PyObject *) self, "constrainField", args);
}

static PyObject *t_constrainedfieldposition_getCategory(
    t_constrainedfieldposition *self)
{
    return PyInt_FromLong(self->object->getCategory());
}

static PyObject *t_constrainedfieldposition_getField(
    t_constrainedfieldposition *self)
{
    return PyInt_FromLong(self->object->getField());
}

static PyObject *t_constrainedfieldposition_getStart(
    t_constrainedfieldposition *self)
{
    return PyInt_FromLong(self->object->getStart());
}

static PyObject *t_constrainedfieldposition_getLimit(
    t_constrainedfieldposition *self)
{
    return PyInt_FromLong(self->object->getLimit());
}

/* FormattedValue */

static PyObject *t_formattedvalue_nextPosition(t_formattedvalue *self,
                                               PyObject *arg)
{
    PyObject *fp;

    if (!parseArg(arg, arg::O(&ConstrainedFieldPositionType_, &fp)))
    {
        bool b;

        STATUS_CALL(b = self->object->nextPosition(
            *((t_constrainedfieldposition *) fp)->object, status));

        Py_RETURN_BOOL(b);
    }

    return PyErr_SetArgsError((PyObject *) self, "nextPosition", arg);
}

static PyObject *t_formattedvalue_iter(t_formattedvalue *self)
{
    self->cfp.reset();
    Py_RETURN_SELF();
}

static PyObject *t_formattedvalue_iter_next(t_formattedvalue *self)
{
    bool b;

    STATUS_CALL(b = self->object->nextPosition(self->cfp, status));

    if (b)
    {
        return wrap_ConstrainedFieldPosition(
            new ConstrainedFieldPosition(self->cfp), T_OWNED);
    }

    PyErr_SetNone(PyExc_StopIteration);
    return NULL;
}

static PyObject *t_formattedvalue_str(t_formattedvalue *self)
{
    UnicodeString u;

    STATUS_CALL(u = self->object->toString(status));
    return PyUnicode_FromUnicodeString(&u);
}

#endif  // ICU >= 64


void _init_format(PyObject *m)
{
    FieldPositionType_.tp_richcompare = (richcmpfunc) t_fieldposition_richcmp;
    ParsePositionType_.tp_richcompare = (richcmpfunc) t_parseposition_richcmp;
    FormatType_.tp_richcompare = (richcmpfunc) t_format_richcmp;
    MessageFormatType_.tp_str = (reprfunc) t_messageformat_str;
    MessageFormatType_.tp_as_number = &t_messageformat_as_number;
    MessageFormatType_.tp_flags |= Py_TPFLAGS_CHECKTYPES;
#if U_ICU_VERSION_HEX >= 0x04000000
    PluralRulesType_.tp_richcompare = (richcmpfunc) t_pluralrules_richcmp;
    PluralFormatType_.tp_str = (reprfunc) t_pluralformat_str;
#endif
#if U_ICU_VERSION_HEX >= 0x04040000
    SelectFormatType_.tp_str = (reprfunc) t_selectformat_str;
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(57, 0, 0)
    SimpleFormatterType_.tp_str = (reprfunc) t_simpleformatter_str;
    SimpleFormatterType_.tp_as_number = &t_simpleformatter_as_number;
    SimpleFormatterType_.tp_flags |= Py_TPFLAGS_CHECKTYPES;
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)
    FormattedValueType_.tp_iter = (getiterfunc) t_formattedvalue_iter;
    FormattedValueType_.tp_iternext = (iternextfunc) t_formattedvalue_iter_next;
    FormattedValueType_.tp_str = (reprfunc) t_formattedvalue_str;
#endif

    REGISTER_TYPE(FieldPosition, m);
    REGISTER_TYPE(ParsePosition, m);
    INSTALL_TYPE(Format, m);
    INSTALL_TYPE(MeasureFormat, m);
    REGISTER_TYPE(MessageFormat, m);
#if U_ICU_VERSION_HEX >= 0x04000000
    REGISTER_TYPE(PluralRules, m);
    REGISTER_TYPE(PluralFormat, m);
#endif
#if U_ICU_VERSION_HEX >= 0x04020000
    REGISTER_TYPE(TimeUnitFormat, m);
#endif
#if U_ICU_VERSION_HEX >= 0x04040000
    REGISTER_TYPE(SelectFormat, m);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)
    INSTALL_TYPE(ListFormatter, m);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(57, 0, 0)
    INSTALL_STRUCT(SimpleFormatter, m);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)
    INSTALL_STRUCT(ConstrainedFieldPosition, m);
    INSTALL_STRUCT(FormattedValue, m);
    INSTALL_STRUCT(FormattedList, m);
#endif

    INSTALL_STATIC_INT(FieldPosition, DONT_CARE);

#if U_ICU_VERSION_HEX >= 0x04020000 && U_ICU_VERSION_HEX < 0x04080000
    INSTALL_STATIC_INT(TimeUnitFormat, kFull);
    INSTALL_STATIC_INT(TimeUnitFormat, kAbbreviate);
#endif
#if U_ICU_VERSION_HEX >= 0x04080000
    INSTALL_CONSTANTS_TYPE(UTimeUnitFormatStyle, m);
    INSTALL_ENUM(UTimeUnitFormatStyle, "FULL", UTMUTFMT_FULL_STYLE);
    INSTALL_ENUM(UTimeUnitFormatStyle, "ABBREVIATED", UTMUTFMT_ABBREVIATED_STYLE);
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(53, 0, 0)
    INSTALL_CONSTANTS_TYPE(UMeasureFormatWidth, m)
    INSTALL_ENUM(UMeasureFormatWidth, "WIDE", UMEASFMT_WIDTH_WIDE);
    INSTALL_ENUM(UMeasureFormatWidth, "SHORT", UMEASFMT_WIDTH_SHORT);
    INSTALL_ENUM(UMeasureFormatWidth, "NARROW", UMEASFMT_WIDTH_NARROW);
    INSTALL_ENUM(UMeasureFormatWidth, "NUMERIC", UMEASFMT_WIDTH_NUMERIC);
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(63, 0, 0)
    INSTALL_CONSTANTS_TYPE(UListFormatterField, m);
    INSTALL_ENUM(UListFormatterField, "LITERAL_FIELD", ULISTFMT_LITERAL_FIELD);
    INSTALL_ENUM(UListFormatterField, "ELEMENT_FIELD", ULISTFMT_ELEMENT_FIELD);
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(64, 0, 0)
    INSTALL_CONSTANTS_TYPE(UFieldCategory, m);
    INSTALL_ENUM(UFieldCategory, "UNDEFINED", UFIELD_CATEGORY_UNDEFINED);
    INSTALL_ENUM(UFieldCategory, "DATE", UFIELD_CATEGORY_DATE);
    INSTALL_ENUM(UFieldCategory, "NUMBER", UFIELD_CATEGORY_NUMBER);
    INSTALL_ENUM(UFieldCategory, "LIST", UFIELD_CATEGORY_LIST);
    INSTALL_ENUM(UFieldCategory, "RELATIVE_DATETIME", UFIELD_CATEGORY_RELATIVE_DATETIME);
    INSTALL_ENUM(UFieldCategory, "LIST_SPAN", UFIELD_CATEGORY_LIST_SPAN);
    INSTALL_ENUM(UFieldCategory, "DATE_INTERVAL_SPAN", UFIELD_CATEGORY_DATE_INTERVAL_SPAN);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(69, 0, 0)
    INSTALL_ENUM(UFieldCategory, "NUMBER_RANGE_SPAN", UFIELD_CATEGORY_NUMBER_RANGE_SPAN);
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(67, 0, 0)
    INSTALL_CONSTANTS_TYPE(UListFormatterType, m);
    INSTALL_ENUM(UListFormatterType, "AND", ULISTFMT_TYPE_AND);
    INSTALL_ENUM(UListFormatterType, "OR", ULISTFMT_TYPE_OR);
    INSTALL_ENUM(UListFormatterType, "UNITS", ULISTFMT_TYPE_UNITS);

    INSTALL_CONSTANTS_TYPE(UListFormatterWidth, m);
    INSTALL_ENUM(UListFormatterWidth, "WIDE", ULISTFMT_WIDTH_WIDE);
    INSTALL_ENUM(UListFormatterWidth, "SHORT", ULISTFMT_WIDTH_SHORT);
    INSTALL_ENUM(UListFormatterWidth, "NARROW", ULISTFMT_WIDTH_NARROW);
#endif
}
