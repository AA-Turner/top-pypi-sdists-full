/* ====================================================================
 * Copyright (c) 2021-2021 Open Source Applications Foundation.
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

#if U_ICU_VERSION_HEX >= VERSION_HEX(4, 8, 0)

#include "bases.h"
#include "messagepattern.h"
#include "macros.h"

DECLARE_CONSTANTS_TYPE(UMessagePatternApostropheMode)
DECLARE_CONSTANTS_TYPE(UMessagePatternPartType)
DECLARE_CONSTANTS_TYPE(UMessagePatternArgType)

/* MessagePattern::Part */

class t_messagepattern_part : public _wrapper {
public:
    MessagePattern::Part *object;
};

static PyObject *t_messagepattern_part_getType(t_messagepattern_part *self);
static PyObject *t_messagepattern_part_getIndex(t_messagepattern_part *self);
static PyObject *t_messagepattern_part_getLength(t_messagepattern_part *self);
static PyObject *t_messagepattern_part_getLimit(t_messagepattern_part *self);
static PyObject *t_messagepattern_part_getValue(t_messagepattern_part *self);
static PyObject *t_messagepattern_part_getArgType(t_messagepattern_part *self);

static PyMethodDef t_messagepattern_part_methods[] = {
    DECLARE_METHOD(t_messagepattern_part, getType, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern_part, getIndex, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern_part, getLength, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern_part, getLimit, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern_part, getValue, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern_part, getArgType, METH_NOARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_TYPE(MessagePattern_Part, t_messagepattern_part, UMemory,
             MessagePattern::Part, abstract_init, NULL);

PyObject *wrap_MessagePattern_Part(const MessagePattern::Part &part)
{
    return wrap_MessagePattern_Part(new MessagePattern::Part(part), T_OWNED);
}

static PyObject *t_messagepattern_part_getType(t_messagepattern_part *self)
{
    return PyInt_FromLong(self->object->getType());
}
static PyObject *t_messagepattern_part_getIndex(t_messagepattern_part *self)
{
    return PyInt_FromLong(self->object->getIndex());
}

static PyObject *t_messagepattern_part_getLength(t_messagepattern_part *self)
{
    return PyInt_FromLong(self->object->getLength());
}

static PyObject *t_messagepattern_part_getLimit(t_messagepattern_part *self)
{
    return PyInt_FromLong(self->object->getLimit());
}

static PyObject *t_messagepattern_part_getValue(t_messagepattern_part *self)
{
    return PyInt_FromLong(self->object->getValue());
}

static PyObject *t_messagepattern_part_getArgType(t_messagepattern_part *self)
{
    return PyInt_FromLong(self->object->getArgType());
}

static PyObject *t_messagepattern_part_str(t_messagepattern_part *self)
{
    return PyString_FromFormat(
        "([%d:%d] type=%d, arg=%d, val=%d)",
        (int) self->object->getIndex(), (int) self->object->getLimit(),
        (int) self->object->getType(), (int) self->object->getArgType(),
        (int) self->object->getValue());
}

/* MessagePattern */

class t_messagepattern : public _wrapper {
public:
    MessagePattern *object;
};

static int t_messagepattern_init(t_messagepattern *self,
                                 PyObject *args, PyObject *kwds);
static PyObject *t_messagepattern_parse(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_parseChoiceStyle(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_parsePluralStyle(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_parseSelectStyle(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_clearPatternAndSetApostropheMode(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_getApostropheMode(t_messagepattern *self);
static PyObject *t_messagepattern_getPatternString(t_messagepattern *self);
static PyObject *t_messagepattern_hasNamedArguments(t_messagepattern *self);
static PyObject *t_messagepattern_hasNumberedArguments(t_messagepattern *self);
static PyObject *t_messagepattern_validateArgumentName(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_autoQuoteApostropheDeep(t_messagepattern *self);
static PyObject *t_messagepattern_countParts(t_messagepattern *self);
static PyObject *t_messagepattern_getPart(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_getPartType(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_getPatternIndex(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_getSubstring(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_partSubstringMatches(t_messagepattern *self, PyObject *args);
static PyObject *t_messagepattern_getNumericValue(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_getPluralOffset(t_messagepattern *self, PyObject *arg);
static PyObject *t_messagepattern_getLimitPartIndex(t_messagepattern *self, PyObject *arg);

static PyMethodDef t_messagepattern_methods[] = {
    DECLARE_METHOD(t_messagepattern, parse, METH_O),
    DECLARE_METHOD(t_messagepattern, parseChoiceStyle, METH_O),
    DECLARE_METHOD(t_messagepattern, parsePluralStyle, METH_O),
    DECLARE_METHOD(t_messagepattern, parseSelectStyle, METH_O),
    DECLARE_METHOD(t_messagepattern, clearPatternAndSetApostropheMode, METH_O),
    DECLARE_METHOD(t_messagepattern, getApostropheMode, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern, getPatternString, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern, hasNamedArguments, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern, hasNumberedArguments, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern, validateArgumentName, METH_O),
    DECLARE_METHOD(t_messagepattern, autoQuoteApostropheDeep, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern, countParts, METH_NOARGS),
    DECLARE_METHOD(t_messagepattern, getPart, METH_O),
    DECLARE_METHOD(t_messagepattern, getPartType, METH_O),
    DECLARE_METHOD(t_messagepattern, getPatternIndex, METH_O),
    DECLARE_METHOD(t_messagepattern, getSubstring, METH_O),
    DECLARE_METHOD(t_messagepattern, partSubstringMatches, METH_VARARGS),
    DECLARE_METHOD(t_messagepattern, getNumericValue, METH_O),
    DECLARE_METHOD(t_messagepattern, getPluralOffset, METH_O),
    DECLARE_METHOD(t_messagepattern, getLimitPartIndex, METH_O),
    { NULL, NULL, 0, NULL }
};

DECLARE_TYPE(MessagePattern, t_messagepattern, UObject, MessagePattern,
             t_messagepattern_init, NULL)

static int t_messagepattern_init(t_messagepattern *self,
                                 PyObject *args, PyObject *kwds)
{
    UnicodeString *u, _u;
    UMessagePatternApostropheMode mode;

    switch (PyTuple_Size(args)) {
      case 0:
        MessagePattern *pattern;

        INT_STATUS_CALL(pattern = new MessagePattern(status));
        self->object = pattern;
        self->flags = T_OWNED;
        break;
      case 1:
        if (!parseArgs(args, "S", &u, &_u))
        {
            MessagePattern *pattern;

            INT_STATUS_PARSER_CALL(pattern = new MessagePattern(*u, &parseError, status));
            self->object = pattern;
            self->flags = T_OWNED;
            break;
        }
        if (!parseArgs(args, "i", &mode))
        {
            MessagePattern *pattern;

            INT_STATUS_CALL(pattern = new MessagePattern(mode, status));
            self->object = pattern;
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

static PyObject *t_messagepattern_parse(t_messagepattern *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, "S", &u, &_u))
    {
        STATUS_PARSER_CALL(self->object->parse(*u, &parseError, status));
        Py_RETURN_SELF();
    }
    return PyErr_SetArgsError((PyObject *) self, "parse", arg);
}

static PyObject *t_messagepattern_parseChoiceStyle(t_messagepattern *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, "S", &u, &_u))
    {
        STATUS_PARSER_CALL(self->object->parseChoiceStyle(*u, &parseError, status));
        Py_RETURN_SELF();
    }
    return PyErr_SetArgsError((PyObject *) self, "parseChoiceStyle", arg);
}

static PyObject *t_messagepattern_parsePluralStyle(t_messagepattern *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, "S", &u, &_u))
    {
        STATUS_PARSER_CALL(self->object->parsePluralStyle(*u, &parseError, status));
        Py_RETURN_SELF();
    }
    return PyErr_SetArgsError((PyObject *) self, "parsePluralStyle", arg);
}

static PyObject *t_messagepattern_parseSelectStyle(t_messagepattern *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, "S", &u, &_u))
    {
        STATUS_PARSER_CALL(self->object->parseSelectStyle(*u, &parseError, status));
        Py_RETURN_SELF();
    }
    return PyErr_SetArgsError((PyObject *) self, "parseSelectStyle", arg);
}

static PyObject *t_messagepattern_clearPatternAndSetApostropheMode(
    t_messagepattern *self, PyObject *arg)
{
    UMessagePatternApostropheMode mode;

    if (!parseArg(arg, "i", &mode))
    {
        self->object->clearPatternAndSetApostropheMode(mode);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError(
        (PyObject *) self, "clearPatternAndSetApostropheMode", arg);
}

static PyObject *t_messagepattern_getApostropheMode(t_messagepattern *self)
{
    return PyInt_FromLong(self->object->getApostropheMode());
}

static PyObject *t_messagepattern_getPatternString(t_messagepattern *self)
{
    return PyUnicode_FromUnicodeString(&self->object->getPatternString());
}

static PyObject *t_messagepattern_hasNamedArguments(t_messagepattern *self)
{
    Py_RETURN_BOOL(self->object->hasNamedArguments())
}

static PyObject *t_messagepattern_hasNumberedArguments(t_messagepattern *self)
{
    Py_RETURN_BOOL(self->object->hasNumberedArguments())
}

static PyObject *t_messagepattern_validateArgumentName(t_messagepattern *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, "S", &u, &_u))
    {
        return PyInt_FromLong(self->object->validateArgumentName(*u));
    }
    return PyErr_SetArgsError((PyObject *) self, "validateArgumentName", arg);
}

static PyObject *t_messagepattern_autoQuoteApostropheDeep(t_messagepattern *self)
{
    UnicodeString result = self->object->autoQuoteApostropheDeep();
    return PyUnicode_FromUnicodeString(&result);
}


static PyObject *t_messagepattern_countParts(t_messagepattern *self) {
  return PyInt_FromLong(self->object->countParts());
}

static PyObject *t_messagepattern_getPart(t_messagepattern *self, PyObject *arg)
{
    int i;
    if (!parseArg(arg, "i", &i))
    {
        return wrap_MessagePattern_Part(self->object->getPart(i));
    }
    return PyErr_SetArgsError((PyObject *) self, "getPart", arg);
}

static PyObject *t_messagepattern_getPartType(t_messagepattern *self, PyObject *arg)
{
    int i;
    if (!parseArg(arg, "i", &i))
    {
        return PyInt_FromLong(self->object->getPartType(i));
    }
    return PyErr_SetArgsError((PyObject *) self, "getPartType", arg);
}


static PyObject *t_messagepattern_getPatternIndex(t_messagepattern *self, PyObject *arg)
{
    int i;
    if (!parseArg(arg, "i", &i))
    {
        return PyInt_FromLong(self->object->getPatternIndex(i));
    }
    return PyErr_SetArgsError((PyObject *) self, "getPatternIndex", arg);
}


static PyObject *t_messagepattern_getSubstring(t_messagepattern *self, PyObject *arg)
{
    PyObject *part;

    if (!parseArg(arg, "O", &MessagePattern_PartType_, &part))
    {
        const UnicodeString result = self->object->getSubstring(
            *((t_messagepattern_part *)part)->object);
        return PyUnicode_FromUnicodeString(&result);
    }
    return PyErr_SetArgsError((PyObject *) self, "getSubstring", arg);
}

static PyObject *t_messagepattern_partSubstringMatches(t_messagepattern *self, PyObject *args)
{
    PyObject *part;
    UnicodeString *u, _u;
    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args, "OS", &MessagePattern_PartType_, &part, &u, &_u))
        {
            UBool result = self->object->partSubstringMatches(
                *((t_messagepattern_part *)part)->object, *u);
            Py_RETURN_BOOL(result);
        }
    }
    return PyErr_SetArgsError((PyObject *) self, "partSubstringMatches", args);
}

static PyObject *t_messagepattern_getNumericValue(t_messagepattern *self, PyObject *arg)
{
    PyObject *part;

    if (!parseArg(arg, "O", &MessagePattern_PartType_, &part))
    {
        return PyInt_FromLong(self->object->getNumericValue(
            *((t_messagepattern_part *)part)->object));
    }
    return PyErr_SetArgsError((PyObject *) self, "getNumericValue", arg);
}

static PyObject *t_messagepattern_getPluralOffset(t_messagepattern *self, PyObject *arg)
{
    int i;
    if (!parseArg(arg, "i", &i))
    {
        return PyInt_FromLong(self->object->getPluralOffset(i));
    }
    return PyErr_SetArgsError((PyObject *) self, "getPluralOffset", arg);
}


static PyObject *t_messagepattern_getLimitPartIndex(t_messagepattern *self, PyObject *arg)
{
    int i;
    if (!parseArg(arg, "i", &i))
    {
        return PyInt_FromLong(self->object->getLimitPartIndex(i));
    }
    return PyErr_SetArgsError((PyObject *) self, "getLimitPartIndex", arg);
}

#endif // ICU >= 4.8

void _init_messagepattern(PyObject *m)
{
#if U_ICU_VERSION_HEX >= VERSION_HEX(4, 8, 0)
    MessagePattern_PartType_.tp_str = (reprfunc) t_messagepattern_part_str;
    MessagePatternType_.tp_str = (reprfunc) t_messagepattern_getPatternString;
    REGISTER_TYPE(MessagePattern, m);
    INSTALL_ENUM(MessagePattern, "ARG_NAME_NOT_NUMBER", UMSGPAT_ARG_NAME_NOT_NUMBER);
    INSTALL_ENUM(MessagePattern, "ARG_NAME_NOT_VALID", UMSGPAT_ARG_NAME_NOT_VALID);
    INSTALL_ENUM(MessagePattern, "NO_NUMERIC_VALUE", UMSGPAT_NO_NUMERIC_VALUE);
    INSTALL_STRUCT(MessagePattern_Part, m);

    INSTALL_CONSTANTS_TYPE(UMessagePatternApostropheMode, m);
    INSTALL_ENUM(UMessagePatternApostropheMode, "DOUBLE_OPTIONAL", UMSGPAT_APOS_DOUBLE_OPTIONAL);
    INSTALL_ENUM(UMessagePatternApostropheMode, "DOUBLE_REQUIRED", UMSGPAT_APOS_DOUBLE_REQUIRED);
    INSTALL_CONSTANTS_TYPE(UMessagePatternPartType, m);
    INSTALL_ENUM(UMessagePatternPartType, "MSG_START", UMSGPAT_PART_TYPE_MSG_START);
    INSTALL_ENUM(UMessagePatternPartType, "MSG_LIMIT", UMSGPAT_PART_TYPE_MSG_LIMIT);
    INSTALL_ENUM(UMessagePatternPartType, "SKIP_SYNTAX", UMSGPAT_PART_TYPE_SKIP_SYNTAX);
    INSTALL_ENUM(UMessagePatternPartType, "INSERT_CHAR", UMSGPAT_PART_TYPE_INSERT_CHAR);
    INSTALL_ENUM(UMessagePatternPartType, "REPLACE_NUMBER", UMSGPAT_PART_TYPE_REPLACE_NUMBER);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_START", UMSGPAT_PART_TYPE_ARG_START);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_LIMIT", UMSGPAT_PART_TYPE_ARG_LIMIT);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_NUMBER", UMSGPAT_PART_TYPE_ARG_NUMBER);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_NAME", UMSGPAT_PART_TYPE_ARG_NAME);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_TYPE", UMSGPAT_PART_TYPE_ARG_TYPE);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_STYLE", UMSGPAT_PART_TYPE_ARG_STYLE);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_SELECTOR", UMSGPAT_PART_TYPE_ARG_SELECTOR);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_INT", UMSGPAT_PART_TYPE_ARG_INT);
    INSTALL_ENUM(UMessagePatternPartType, "ARG_DOUBLE", UMSGPAT_PART_TYPE_ARG_DOUBLE);
    INSTALL_CONSTANTS_TYPE(UMessagePatternArgType, m);
    INSTALL_ENUM(UMessagePatternArgType, "NONE", UMSGPAT_ARG_TYPE_NONE);
    INSTALL_ENUM(UMessagePatternArgType, "SIMPLE", UMSGPAT_ARG_TYPE_SIMPLE);
    INSTALL_ENUM(UMessagePatternArgType, "CHOICE", UMSGPAT_ARG_TYPE_CHOICE);
    INSTALL_ENUM(UMessagePatternArgType, "PLURAL", UMSGPAT_ARG_TYPE_PLURAL);
    INSTALL_ENUM(UMessagePatternArgType, "SELECT", UMSGPAT_ARG_TYPE_SELECT);
    INSTALL_ENUM(UMessagePatternArgType, "SELECTORDINAL", UMSGPAT_ARG_TYPE_SELECTORDINAL);
#endif // ICU >= 4.8
}

