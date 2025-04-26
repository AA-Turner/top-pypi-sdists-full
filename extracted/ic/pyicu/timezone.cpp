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
#include "timezone.h"
#include "macros.h"

#include "arg.h"

/* apparently a macro defined by some versions of the MSVC compiler */
#ifdef daylight
#undef daylight
#endif

DECLARE_CONSTANTS_TYPE(DateRuleType)
DECLARE_CONSTANTS_TYPE(TimeRuleType)

#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)
DECLARE_CONSTANTS_TYPE(UTimeZoneNameType)
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(69, 0, 0)
DECLARE_CONSTANTS_TYPE(UTimeZoneLocalOption)
#endif


/* TimeZoneRule */

class t_timezonerule : public _wrapper {
public:
    TimeZoneRule *object;
};

static PyObject *t_timezonerule_getName(t_timezonerule *self);
static PyObject *t_timezonerule_getRawOffset(t_timezonerule *self);
static PyObject *t_timezonerule_getDSTSavings(t_timezonerule *self);
static PyObject *t_timezonerule_isEquivalentTo(t_timezonerule *self, PyObject *arg);
static PyObject *t_timezonerule_getFirstStart(t_timezonerule *self, PyObject *args);
static PyObject *t_timezonerule_getFinalStart(t_timezonerule *self, PyObject *args);
static PyObject *t_timezonerule_getNextStart(t_timezonerule *self, PyObject *args);
static PyObject *t_timezonerule_getPreviousStart(t_timezonerule *self, PyObject *args);

static PyMethodDef t_timezonerule_methods[] = {
    DECLARE_METHOD(t_timezonerule, getName, METH_NOARGS),
    DECLARE_METHOD(t_timezonerule, getRawOffset, METH_NOARGS),
    DECLARE_METHOD(t_timezonerule, getDSTSavings, METH_NOARGS),
    DECLARE_METHOD(t_timezonerule, isEquivalentTo, METH_O),
    DECLARE_METHOD(t_timezonerule, getFirstStart, METH_VARARGS),
    DECLARE_METHOD(t_timezonerule, getFinalStart, METH_VARARGS),
    DECLARE_METHOD(t_timezonerule, getNextStart, METH_VARARGS),
    DECLARE_METHOD(t_timezonerule, getPreviousStart, METH_VARARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(TimeZoneRule, t_timezonerule, UObject,
                     TimeZoneRule, abstract_init)


/* AnnualTimeZoneRule */

class t_annualtimezonerule : public _wrapper {
public:
    AnnualTimeZoneRule *object;
};

static PyObject *t_annualtimezonerule_getStartYear(t_annualtimezonerule *self);
static PyObject *t_annualtimezonerule_getEndYear(t_annualtimezonerule *self);
static PyObject *t_annualtimezonerule_getStartInYear(t_annualtimezonerule *self, PyObject *args);
static PyObject *t_annualtimezonerule_getRule(t_annualtimezonerule *self);

static PyMethodDef t_annualtimezonerule_methods[] = {
    DECLARE_METHOD(t_annualtimezonerule, getStartYear, METH_NOARGS),
    DECLARE_METHOD(t_annualtimezonerule, getEndYear, METH_NOARGS),
    DECLARE_METHOD(t_annualtimezonerule, getStartInYear, METH_VARARGS),
    DECLARE_METHOD(t_annualtimezonerule, getRule, METH_NOARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(AnnualTimeZoneRule, t_annualtimezonerule, TimeZoneRule,
                     AnnualTimeZoneRule, abstract_init)


/* InitialTimeZoneRule */

class t_initialtimezonerule : public _wrapper {
public:
    InitialTimeZoneRule *object;
};

static PyMethodDef t_initialtimezonerule_methods[] = {
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(InitialTimeZoneRule, t_initialtimezonerule, TimeZoneRule,
                     InitialTimeZoneRule, abstract_init)


/* TimeArrayTimeZoneRule */

class t_timearraytimezonerule : public _wrapper {
public:
    TimeArrayTimeZoneRule *object;
};

static PyObject *t_timearraytimezonerule_getTimeType(t_timearraytimezonerule *self);
static PyObject *t_timearraytimezonerule_countStartTimes(t_timearraytimezonerule *self);
static PyObject *t_timearraytimezonerule_getStartTimeAt(t_timearraytimezonerule *self, PyObject *arg);

static PyMethodDef t_timearraytimezonerule_methods[] = {
    DECLARE_METHOD(t_timearraytimezonerule, getTimeType, METH_NOARGS),
    DECLARE_METHOD(t_timearraytimezonerule, countStartTimes, METH_NOARGS),
    DECLARE_METHOD(t_timearraytimezonerule, getStartTimeAt, METH_O),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(
    TimeArrayTimeZoneRule, t_timearraytimezonerule, TimeZoneRule,
    TimeArrayTimeZoneRule, abstract_init)


/* DateTimeRule */

class t_datetimerule : public _wrapper {
public:
    DateTimeRule *object;
};

static PyObject *t_datetimerule_getDateRuleType(t_datetimerule *self);
static PyObject *t_datetimerule_getTimeRuleType(t_datetimerule *self);
static PyObject *t_datetimerule_getRuleMonth(t_datetimerule *self);
static PyObject *t_datetimerule_getRuleDayOfMonth(t_datetimerule *self);
static PyObject *t_datetimerule_getRuleDayOfWeek(t_datetimerule *self);
static PyObject *t_datetimerule_getRuleWeekInMonth(t_datetimerule *self);
static PyObject *t_datetimerule_getRuleMillisInDay(t_datetimerule *self);

static PyMethodDef t_datetimerule_methods[] = {
    DECLARE_METHOD(t_datetimerule, getDateRuleType, METH_NOARGS),
    DECLARE_METHOD(t_datetimerule, getTimeRuleType, METH_NOARGS),
    DECLARE_METHOD(t_datetimerule, getRuleMonth, METH_NOARGS),
    DECLARE_METHOD(t_datetimerule, getRuleDayOfMonth, METH_NOARGS),
    DECLARE_METHOD(t_datetimerule, getRuleDayOfWeek, METH_NOARGS),
    DECLARE_METHOD(t_datetimerule, getRuleWeekInMonth, METH_NOARGS),
    DECLARE_METHOD(t_datetimerule, getRuleMillisInDay, METH_NOARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(DateTimeRule, t_datetimerule, UObject,
                     DateTimeRule, abstract_init)


/* TimeZoneTransition */

class t_timezonetransition : public _wrapper {
public:
    TimeZoneTransition *object;
};

static PyObject *t_timezonetransition_getTime(t_timezonetransition *self);
static PyObject *t_timezonetransition_getFrom(t_timezonetransition *self);
static PyObject *t_timezonetransition_getTo(t_timezonetransition *self);

static PyMethodDef t_timezonetransition_methods[] = {
    DECLARE_METHOD(t_timezonetransition, getTime, METH_NOARGS),
    DECLARE_METHOD(t_timezonetransition, getFrom, METH_NOARGS),
    DECLARE_METHOD(t_timezonetransition, getTo, METH_NOARGS),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(TimeZoneTransition, t_timezonetransition, UObject,
                     TimeZoneTransition, abstract_init)


/* TimeZone */

static PyObject *t_timezone_getOffset(t_timezone *self, PyObject *args);
static PyObject *t_timezone_getRawOffset(t_timezone *self);
static PyObject *t_timezone_setRawOffset(t_timezone *self, PyObject *arg);
static PyObject *t_timezone_getID(t_timezone *self, PyObject *args);
static PyObject *t_timezone_setID(t_timezone *self, PyObject *arg);
static PyObject *t_timezone_getDisplayName(t_timezone *self, PyObject *args);
static PyObject *t_timezone_useDaylightTime(t_timezone *self);
static PyObject *t_timezone_inDaylightTime(t_timezone *self, PyObject *arg);
static PyObject *t_timezone_hasSameRules(t_timezone *self, PyObject *arg);
static PyObject *t_timezone_getDSTSavings(t_timezone *self);
static PyObject *t_timezone_getGMT(PyTypeObject *type);
static PyObject *t_timezone_createEnumeration(PyTypeObject *type,
                                              PyObject *args);
static PyObject *t_timezone_countEquivalentIDs(PyTypeObject *type,
                                               PyObject *arg);
static PyObject *t_timezone_getEquivalentID(PyTypeObject *type, PyObject *args);
#if U_ICU_VERSION_HEX >= 0x04080000
static PyObject *t_timezone_getRegion(PyTypeObject *type, PyObject *arg);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(52, 0, 0)
static PyObject *t_timezone_getIDForWindowsID(PyTypeObject *type,
                                              PyObject *args);
static PyObject *t_timezone_getWindowsID(PyTypeObject *type, PyObject *arg);
#endif
static PyObject *t_timezone_createDefault(PyTypeObject *type);
static PyObject *t_timezone_setDefault(PyTypeObject *type, PyObject *arg);
#if U_ICU_VERSION_HEX >= VERSION_HEX(74, 0, 0)
static PyObject *t_timezone_getIanaID(PyTypeObject *type, PyObject *args);
#endif

static PyMethodDef t_timezone_methods[] = {
    DECLARE_METHOD(t_timezone, getOffset, METH_VARARGS),
    DECLARE_METHOD(t_timezone, getRawOffset, METH_NOARGS),
    DECLARE_METHOD(t_timezone, setRawOffset, METH_O),
    DECLARE_METHOD(t_timezone, getID, METH_VARARGS),
    DECLARE_METHOD(t_timezone, setID, METH_O),
    DECLARE_METHOD(t_timezone, getDisplayName, METH_VARARGS),
    DECLARE_METHOD(t_timezone, useDaylightTime, METH_NOARGS),
    DECLARE_METHOD(t_timezone, inDaylightTime, METH_O),
    DECLARE_METHOD(t_timezone, hasSameRules, METH_O),
    DECLARE_METHOD(t_timezone, getDSTSavings, METH_NOARGS),
    DECLARE_METHOD(t_timezone, getGMT, METH_NOARGS | METH_CLASS),
    DECLARE_METHOD(t_timezone, createTimeZone, METH_O | METH_CLASS),
    DECLARE_METHOD(t_timezone, createEnumeration, METH_VARARGS | METH_CLASS),
    DECLARE_METHOD(t_timezone, countEquivalentIDs, METH_O | METH_CLASS),
    DECLARE_METHOD(t_timezone, getEquivalentID, METH_VARARGS | METH_CLASS),
#if U_ICU_VERSION_HEX >= 0x04080000
    DECLARE_METHOD(t_timezone, getRegion, METH_O | METH_CLASS),
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(52, 0, 0)
    DECLARE_METHOD(t_timezone, getIDForWindowsID, METH_VARARGS | METH_CLASS),
    DECLARE_METHOD(t_timezone, getWindowsID, METH_O | METH_CLASS),
#endif
    DECLARE_METHOD(t_timezone, createDefault, METH_NOARGS | METH_CLASS),
    DECLARE_METHOD(t_timezone, setDefault, METH_O | METH_CLASS),
#if U_ICU_VERSION_HEX >= VERSION_HEX(74, 0, 0)
    DECLARE_METHOD(t_timezone, getIanaID, METH_O | METH_CLASS),
#endif
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(TimeZone, t_timezone, UObject, TimeZone, abstract_init)


/* BasicTimeZone */

class t_basictimezone : public _wrapper {
public:
    BasicTimeZone *object;
};

static PyObject *t_basictimezone_getNextTransition(t_basictimezone *self, PyObject *args);
static PyObject *t_basictimezone_getPreviousTransition(t_basictimezone *self, PyObject *args);
static PyObject *t_basictimezone_hasEquivalentTransitions(t_basictimezone *self, PyObject *args);
static PyObject *t_basictimezone_countTransitionRules(t_basictimezone *self);
static PyObject *t_basictimezone_getTimeZoneRules(t_basictimezone *self);
static PyObject *t_basictimezone_getSimpleRulesNear(t_basictimezone *self, PyObject *arg);

#if U_ICU_VERSION_HEX >= VERSION_HEX(69, 0, 0)
static PyObject *t_basictimezone_getOffsetFromLocal(t_basictimezone *self,
                                                    PyObject *args);
#endif

static PyMethodDef t_basictimezone_methods[] = {
    DECLARE_METHOD(t_basictimezone, getNextTransition, METH_VARARGS),
    DECLARE_METHOD(t_basictimezone, getPreviousTransition, METH_VARARGS),
    DECLARE_METHOD(t_basictimezone, hasEquivalentTransitions, METH_VARARGS),
    DECLARE_METHOD(t_basictimezone, countTransitionRules, METH_NOARGS),
    DECLARE_METHOD(t_basictimezone, getTimeZoneRules, METH_NOARGS),
    DECLARE_METHOD(t_basictimezone, getSimpleRulesNear, METH_O),
#if U_ICU_VERSION_HEX >= VERSION_HEX(69, 0, 0)
    DECLARE_METHOD(t_basictimezone, getOffsetFromLocal, METH_VARARGS),
#endif
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(BasicTimeZone, t_basictimezone, TimeZone,
                     BasicTimeZone, abstract_init)


/* RuleBasedTimeZone */

class t_rulebasedtimezone : public _wrapper {
public:
    RuleBasedTimeZone *object;
};

static PyMethodDef t_rulebasedtimezone_methods[] = {
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(RuleBasedTimeZone, t_rulebasedtimezone, BasicTimeZone,
                     RuleBasedTimeZone, abstract_init)


/* SimpleTimeZone */

class t_simpletimezone : public _wrapper {
public:
    SimpleTimeZone *object;
};

static int t_simpletimezone_init(t_simpletimezone *self,
                                 PyObject *args, PyObject *kwds);
static PyObject *t_simpletimezone_setStartYear(t_simpletimezone *self,
                                               PyObject *arg);
static PyObject *t_simpletimezone_setStartRule(t_simpletimezone *self,
                                               PyObject *args);
static PyObject *t_simpletimezone_setEndRule(t_simpletimezone *self,
                                             PyObject *args);
static PyObject *t_simpletimezone_getOffset(t_simpletimezone *self,
                                            PyObject *args);
static PyObject *t_simpletimezone_setDSTSavings(t_simpletimezone *self,
                                                PyObject *arg);

static PyMethodDef t_simpletimezone_methods[] = {
    DECLARE_METHOD(t_simpletimezone, setStartYear, METH_O),
    DECLARE_METHOD(t_simpletimezone, setStartRule, METH_VARARGS),
    DECLARE_METHOD(t_simpletimezone, setEndRule, METH_VARARGS),
    DECLARE_METHOD(t_simpletimezone, getOffset, METH_VARARGS),
    DECLARE_METHOD(t_simpletimezone, setDSTSavings, METH_O),
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(SimpleTimeZone, t_simpletimezone, BasicTimeZone,
                     SimpleTimeZone, t_simpletimezone_init)


/* VTimeZone */

class t_vtimezone : public _wrapper {
public:
    VTimeZone *object;
};

static PyObject *t_vtimezone_getTZURL(t_vtimezone *self);
static PyObject *t_vtimezone_getLastModified(t_vtimezone *self);
static PyObject *t_vtimezone_write(t_vtimezone *self, PyObject *args);
static PyObject *t_vtimezone_writeSimple(t_vtimezone *self, PyObject *arg);
static PyObject *t_vtimezone_createVTimeZone(PyTypeObject *type, PyObject *arg);
static PyObject *t_vtimezone_createVTimeZoneByID(PyTypeObject *type, PyObject *arg);
#if U_ICU_VERSION_HEX >= 0x04060000
static PyObject *t_vtimezone_createVTimeZoneFromBasicTimeZone(PyTypeObject *type, PyObject *arg);
#endif

static PyMethodDef t_vtimezone_methods[] = {
    DECLARE_METHOD(t_vtimezone, getTZURL, METH_NOARGS),
    DECLARE_METHOD(t_vtimezone, getLastModified, METH_NOARGS),
    DECLARE_METHOD(t_vtimezone, write, METH_VARARGS),
    DECLARE_METHOD(t_vtimezone, writeSimple, METH_O),
    DECLARE_METHOD(t_vtimezone, createVTimeZone, METH_O | METH_CLASS),
    DECLARE_METHOD(t_vtimezone, createVTimeZoneByID, METH_O | METH_CLASS),
#if U_ICU_VERSION_HEX >= 0x04060000
    DECLARE_METHOD(t_vtimezone, createVTimeZoneFromBasicTimeZone, METH_O | METH_CLASS),
#endif
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(VTimeZone, t_vtimezone, BasicTimeZone,
                     VTimeZone, abstract_init)


#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)

/* TimeZoneNames */

class t_timezonenames : public _wrapper {
public:
    TimeZoneNames *object;
};

static PyObject *t_timezonenames_getAvailableMetaZoneIDs(t_timezonenames *self, PyObject *args);
static PyObject *t_timezonenames_getMetaZoneID(t_timezonenames *self, PyObject *args);
static PyObject *t_timezonenames_getReferenceZoneID(t_timezonenames *self, PyObject *args);
static PyObject *t_timezonenames_getMetaZoneDisplayName(t_timezonenames *self, PyObject *args);
static PyObject *t_timezonenames_getTimeZoneDisplayName(t_timezonenames *self, PyObject *args);
static PyObject *t_timezonenames_getExemplarLocationName(t_timezonenames *self, PyObject *arg);
static PyObject *t_timezonenames_getDisplayName(t_timezonenames *self, PyObject *args);

static PyObject *t_timezonenames_createInstance(PyTypeObject *type, PyObject *arg);
#if U_ICU_VERSION_HEX >= VERSION_HEX(54, 0, 0)
static PyObject *t_timezonenames_createTZDBInstance(PyTypeObject *type, PyObject *arg);
#endif

static PyMethodDef t_timezonenames_methods[] = {
    DECLARE_METHOD(t_timezonenames, getAvailableMetaZoneIDs, METH_VARARGS),
    DECLARE_METHOD(t_timezonenames, getMetaZoneID, METH_VARARGS),
    DECLARE_METHOD(t_timezonenames, getReferenceZoneID, METH_VARARGS),
    DECLARE_METHOD(t_timezonenames, getMetaZoneDisplayName, METH_VARARGS),
    DECLARE_METHOD(t_timezonenames, getTimeZoneDisplayName, METH_VARARGS),
    DECLARE_METHOD(t_timezonenames, getExemplarLocationName, METH_O),
    DECLARE_METHOD(t_timezonenames, getDisplayName, METH_VARARGS),
    DECLARE_METHOD(t_timezonenames, createInstance, METH_O | METH_CLASS),
#if U_ICU_VERSION_HEX >= VERSION_HEX(54, 0, 0)
    DECLARE_METHOD(t_timezonenames, createTZDBInstance, METH_O | METH_CLASS),
#endif
    { NULL, NULL, 0, NULL }
};

DECLARE_DEALLOC_TYPE(TimeZoneNames, t_timezonenames, UObject,
                     TimeZoneNames, abstract_init)

#endif  // ICU >= 50


/* TimeZoneRule */

PyObject *wrap_TimeZoneRule(TimeZoneRule *tzr)
{
    RETURN_WRAPPED_IF_ISINSTANCE(tzr, AnnualTimeZoneRule);
    RETURN_WRAPPED_IF_ISINSTANCE(tzr, InitialTimeZoneRule);
    RETURN_WRAPPED_IF_ISINSTANCE(tzr, TimeArrayTimeZoneRule);
    return wrap_TimeZoneRule(tzr, T_OWNED);
}

PyObject *wrap_TimeZoneRule(const TimeZoneRule &tz)
{
    return wrap_TimeZoneRule(tz.clone());
}

static PyObject *t_timezonerule_getName(t_timezonerule *self)
{
    UnicodeString u;

    self->object->getName(u);
    return PyUnicode_FromUnicodeString(&u);
}

static PyObject *t_timezonerule_getRawOffset(t_timezonerule *self)
{
    return PyInt_FromLong(self->object->getRawOffset());
}

static PyObject *t_timezonerule_getDSTSavings(t_timezonerule *self)
{
    return PyInt_FromLong(self->object->getDSTSavings());
}

static PyObject *t_timezonerule_isEquivalentTo(t_timezonerule *self,
                                               PyObject *arg)
{
    TimeZoneRule *tzr;

    if (!parseArg(arg, arg::P<TimeZoneRule>(TYPE_CLASSID(TimeZoneRule), &tzr)))
    {
        UBool result = self->object->isEquivalentTo(*tzr);
        Py_RETURN_BOOL(result);
    }

    return PyErr_SetArgsError((PyObject *) self, "isEquivalentTo", arg);
}

static PyObject *t_timezonerule_getFirstStart(t_timezonerule *self,
                                              PyObject *args)
{
    int prevRawOffset, prevDSTSavings;
    UDate date;
    UBool result;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(result = self->object->getFirstStart(0, 0, date));

        if (result)
            return PyFloat_FromDouble(date / 1000.0);

        Py_RETURN_NONE;
        break;

      case 2:
        if (!parseArgs(args, arg::i(&prevRawOffset), arg::i(&prevDSTSavings)))
        {
            STATUS_CALL(result = self->object->getFirstStart(
                prevRawOffset, prevDSTSavings, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getFirstStart", args);
}

static PyObject *t_timezonerule_getFinalStart(t_timezonerule *self,
                                              PyObject *args)
{
    int prevRawOffset, prevDSTSavings;
    UDate date;
    UBool result;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(result = self->object->getFinalStart(0, 0, date));

        if (result)
            return PyFloat_FromDouble(date / 1000.0);

        Py_RETURN_NONE;
        break;

      case 2:
        if (!parseArgs(args, arg::i(&prevRawOffset), arg::i(&prevDSTSavings)))
        {
            STATUS_CALL(result = self->object->getFinalStart(
                prevRawOffset, prevDSTSavings, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getFinalStart", args);
}

static PyObject *t_timezonerule_getNextStart(t_timezonerule *self,
                                             PyObject *args)
{
    UDate base, date;
    int prevRawOffset, prevDSTSavings;
    UBool result, inclusive;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::D(&base)))
        {
            STATUS_CALL(result = self->object->getNextStart(
                base, 0, 0, false, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;

      case 2:
        if (!parseArgs(args, arg::D(&base), arg::b(&inclusive)))
        {
            STATUS_CALL(result = self->object->getNextStart(
                base, 0, 0, inclusive, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;

      case 3:
        if (!parseArgs(args, arg::D(&base), arg::i(&prevRawOffset), arg::i(&prevDSTSavings)))
        {
            STATUS_CALL(result = self->object->getNextStart(
                base, prevRawOffset, prevDSTSavings, false, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;

      case 4:
        if (!parseArgs(args, arg::D(&base), arg::i(&prevRawOffset), arg::i(&prevDSTSavings), arg::b(&inclusive)))
        {
            STATUS_CALL(result = self->object->getNextStart(
                base, prevRawOffset, prevDSTSavings, inclusive, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getNextStart", args);
}

static PyObject *t_timezonerule_getPreviousStart(t_timezonerule *self,
                                                 PyObject *args)
{
    UDate base, date;
    int prevRawOffset, prevDSTSavings;
    UBool result, inclusive;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::D(&base)))
        {
            STATUS_CALL(result = self->object->getPreviousStart(
                base, 0, 0, false, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;

      case 2:
        if (!parseArgs(args, arg::D(&base), arg::b(&inclusive)))
        {
            STATUS_CALL(result = self->object->getPreviousStart(
                base, 0, 0, inclusive, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;

      case 3:
        if (!parseArgs(args, arg::D(&base), arg::i(&prevRawOffset), arg::i(&prevDSTSavings)))
        {
            STATUS_CALL(result = self->object->getPreviousStart(
                base, prevRawOffset, prevDSTSavings, false, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;

      case 4:
        if (!parseArgs(args, arg::D(&base), arg::i(&prevRawOffset), arg::i(&prevDSTSavings), arg::b(&inclusive)))
        {
            STATUS_CALL(result = self->object->getPreviousStart(
                base, prevRawOffset, prevDSTSavings, inclusive, date));

            if (result)
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getPreviousStart", args);
}

static PyObject *t_timezonerule_str(t_timezonerule *self)
{
    UnicodeString u;

    self->object->getName(u);
    return PyUnicode_FromUnicodeString(&u);
}

DEFINE_RICHCMP__ARG__(TimeZoneRule, t_timezonerule)


/* AnnualTimeZoneRule */

static PyObject *t_annualtimezonerule_getStartYear(t_annualtimezonerule *self)
{
    return PyInt_FromLong(self->object->getStartYear());
}

static PyObject *t_annualtimezonerule_getEndYear(t_annualtimezonerule *self)
{
    return PyInt_FromLong(self->object->getEndYear());
}

static PyObject *t_annualtimezonerule_getStartInYear(t_annualtimezonerule *self,
                                                     PyObject *args)
{
    int year, prevRawOffset, prevDSTSavings;
    UDate date;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::i(&year)))
        {
            if (self->object->getStartInYear(year, 0, 0, date))
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;

      case 3:
        if (!parseArgs(args, arg::i(&year), arg::i(&prevRawOffset), arg::i(&prevDSTSavings)))
        {
            if (self->object->getStartInYear(
                    year, prevRawOffset, prevDSTSavings, date))
                return PyFloat_FromDouble(date / 1000.0);

            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getStartInYear", args);
}

static PyObject *t_annualtimezonerule_getRule(t_annualtimezonerule *self)
{
    const DateTimeRule *dtr = self->object->getRule();

    if (dtr)
        return wrap_DateTimeRule((DateTimeRule *) (dtr->clone()), T_OWNED);

    Py_RETURN_NONE;
}


/* TimeArrayTimeZoneRule */

static PyObject *t_timearraytimezonerule_getTimeType(
    t_timearraytimezonerule *self) {
    return PyInt_FromLong(self->object->getTimeType());
}

static PyObject *t_timearraytimezonerule_countStartTimes(
    t_timearraytimezonerule *self) {
    return PyInt_FromLong(self->object->countStartTimes());
}

static PyObject *t_timearraytimezonerule_getStartTimeAt(
    t_timearraytimezonerule *self, PyObject *arg)
{
    int index;

    if (!parseArg(arg, arg::i(&index)))
    {
        UDate date;

        if (self->object->getStartTimeAt(index, date))
            return PyFloat_FromDouble(date / 1000.0);

        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "getStartTimeAt", arg);
}


/* DateTimeRule */

static PyObject *t_datetimerule_getDateRuleType(t_datetimerule *self)
{
    return PyInt_FromLong(self->object->getDateRuleType());
}

static PyObject *t_datetimerule_getTimeRuleType(t_datetimerule *self)
{
    return PyInt_FromLong(self->object->getTimeRuleType());
}

static PyObject *t_datetimerule_getRuleMonth(t_datetimerule *self)
{
    return PyInt_FromLong(self->object->getRuleMonth());
}

static PyObject *t_datetimerule_getRuleDayOfMonth(t_datetimerule *self)
{
    return PyInt_FromLong(self->object->getRuleDayOfMonth());
}

static PyObject *t_datetimerule_getRuleDayOfWeek(t_datetimerule *self)
{
    return PyInt_FromLong(self->object->getRuleDayOfWeek());
}

static PyObject *t_datetimerule_getRuleWeekInMonth(t_datetimerule *self)
{
    return PyInt_FromLong(self->object->getRuleWeekInMonth());
}

static PyObject *t_datetimerule_getRuleMillisInDay(t_datetimerule *self)
{
    return PyInt_FromLong(self->object->getRuleMillisInDay());
}


/* TimeZoneTransition */

static PyObject *t_timezonetransition_getTime(t_timezonetransition *self)
{
    return PyFloat_FromDouble(self->object->getTime() / 1000.0);
}

static PyObject *t_timezonetransition_getFrom(t_timezonetransition *self)
{
    const TimeZoneRule *tzr = self->object->getFrom();

    if (tzr != NULL)
        return wrap_TimeZoneRule(*tzr);

    Py_RETURN_NONE;
}

static PyObject *t_timezonetransition_getTo(t_timezonetransition *self)
{
    const TimeZoneRule *tzr = self->object->getTo();

    if (tzr != NULL)
        return wrap_TimeZoneRule(*tzr);

    Py_RETURN_NONE;
}


/* TimeZone */

PyObject *wrap_TimeZone(TimeZone *tz)
{
    RETURN_WRAPPED_IF_ISINSTANCE(tz, RuleBasedTimeZone);
    RETURN_WRAPPED_IF_ISINSTANCE(tz, SimpleTimeZone);
    RETURN_WRAPPED_IF_ISINSTANCE(tz, VTimeZone);
    RETURN_WRAPPED_IF_ISINSTANCE(tz, BasicTimeZone);
    return wrap_TimeZone(tz, T_OWNED);
}

PyObject *wrap_TimeZone(const TimeZone &tz)
{
    return wrap_TimeZone(tz.clone());
}

static PyObject *t_timezone_getOffset(t_timezone *self, PyObject *args)
{
    UDate date;
    UBool local;
    int rawOffset, dstOffset, offset;
    int era, year, month, day, dayOfWeek, millis, monthLength;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args, arg::D(&date), arg::b(&local)))
        {
            STATUS_CALL(self->object->getOffset(date, (UBool) local,
                                                rawOffset, dstOffset, status));
            return Py_BuildValue("(ii)", rawOffset, dstOffset);
        }
        break;
      case 6:
        if (!parseArgs(args, arg::i(&era), arg::i(&year), arg::i(&month), arg::i(&day), arg::i(&dayOfWeek), arg::i(&millis)))
        {
            STATUS_CALL(offset = self->object->getOffset((uint8_t) era, year, month, day, dayOfWeek, millis, status));
            return PyInt_FromLong(offset);
        }
        break;
      case 7:
        if (!parseArgs(args, arg::i(&era), arg::i(&year), arg::i(&month), arg::i(&day), arg::i(&dayOfWeek), arg::i(&millis), arg::i(&monthLength)))
        {
            STATUS_CALL(offset = self->object->getOffset((uint8_t) era, year, month, day, dayOfWeek, millis, monthLength, status));
            return PyInt_FromLong(offset);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getOffset", args);
}

static PyObject *t_timezone_getRawOffset(t_timezone *self)
{
    return PyInt_FromLong(self->object->getRawOffset());
}

static PyObject *t_timezone_setRawOffset(t_timezone *self, PyObject *arg)
{
    int offset;

    if (!parseArg(arg, arg::i(&offset)))
    {
        self->object->setRawOffset(offset);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setRawOffset", arg);
}

static PyObject *t_timezone_getID(t_timezone *self, PyObject *args)
{
    UnicodeString *u, _u;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object->getID(_u);
        return PyUnicode_FromUnicodeString(&_u);
      case 1:
        if (!parseArgs(args, arg::U(&u)))
        {
            self->object->getID(*u);
            Py_RETURN_ARG(args, 0);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getID", args);
}

static PyObject *t_timezone_setID(t_timezone *self, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        self->object->setID(*u); /* copied */
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setID", arg);
}

static PyObject *t_timezone_getDisplayName(t_timezone *self, PyObject *args)
{
    UnicodeString *u, _u;
    UBool daylight;
    Locale *locale;
    TimeZone::EDisplayType type;

    switch (PyTuple_Size(args)) {
      case 0:
        self->object->getDisplayName(_u);
        return PyUnicode_FromUnicodeString(&_u);
      case 1:
        if (!parseArgs(args, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
        {
            self->object->getDisplayName(*locale, _u);
            return PyUnicode_FromUnicodeString(&_u);
        }
        if (!parseArgs(args, arg::U(&u)))
        {
            self->object->getDisplayName(*u);
            Py_RETURN_ARG(args, 0);
        }
        break;
      case 2:
        if (!parseArgs(args,
                       arg::b(&daylight),
                       arg::Enum<TimeZone::EDisplayType>(&type)))
        {
            self->object->getDisplayName(daylight, type, _u);
            return PyUnicode_FromUnicodeString(&_u);
        }
        if (!parseArgs(args,
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
                       arg::U(&u)))
        {
            self->object->getDisplayName(*locale, *u);
            Py_RETURN_ARG(args, 1);
        }
        break;
      case 3:
        if (!parseArgs(args,
                       arg::b(&daylight),
                       arg::Enum<TimeZone::EDisplayType>(&type),
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
        {
            self->object->getDisplayName(daylight, type, *locale, _u);
            return PyUnicode_FromUnicodeString(&_u);
        }
        if (!parseArgs(args,
                       arg::b(&daylight),
                       arg::Enum<TimeZone::EDisplayType>(&type),
                       arg::U(&u)))
        {
            self->object->getDisplayName(daylight, type, *u);
            Py_RETURN_ARG(args, 2);
        }
        break;
      case 4:
        if (!parseArgs(args,
                       arg::b(&daylight),
                       arg::Enum<TimeZone::EDisplayType>(&type),
                       arg::P<Locale>(TYPE_CLASSID(Locale), &locale),
                       arg::U(&u)))
        {
            self->object->getDisplayName(daylight, type, *locale, *u);
            Py_RETURN_ARG(args, 3);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getDisplayName", args);
}

static PyObject *t_timezone_useDaylightTime(t_timezone *self)
{
    UBool b = self->object->useDaylightTime();
    Py_RETURN_BOOL(b);
}

static PyObject *t_timezone_inDaylightTime(t_timezone *self, PyObject *arg)
{
    UDate date;
    UBool b;

    if (!parseArg(arg, arg::D(&date)))
    {
        STATUS_CALL(b = self->object->inDaylightTime(date, status));
        Py_RETURN_BOOL(b);
    }

    return PyErr_SetArgsError((PyObject *) self, "inDaylightTime", arg);
}

static PyObject *t_timezone_hasSameRules(t_timezone *self, PyObject *arg)
{
    TimeZone *tz;
    UBool b;

    if (!parseArg(arg, arg::P<TimeZone>(TYPE_CLASSID(TimeZone), &tz)))
    {
        b = self->object->hasSameRules(*tz);
        Py_RETURN_BOOL(b);
    }

    return PyErr_SetArgsError((PyObject *) self, "hasSameRules", arg);
}

static PyObject *t_timezone_getDSTSavings(t_timezone *self)
{
    return PyInt_FromLong(self->object->getDSTSavings());
}

static PyObject *t_timezone_getGMT(PyTypeObject *type)
{
    return wrap_TimeZone((TimeZone *) TimeZone::getGMT(), 0);
}

PyObject *t_timezone_createTimeZone(PyTypeObject *type, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        std::unique_ptr<TimeZone> tz(TimeZone::createTimeZone(*u));
        const TimeZone *gmt = TimeZone::getGMT();
        UnicodeString tzid, GMT;

        /* PyICU bug 8180 and ICU bug 5612:
         *    https://bugzilla.osafoundation.org/show_bug.cgi?id=8180
         *    http://bugs.icu-project.org/trac/ticket/5612
         * Only an Olson ID can be used with createTimeZone().
         * If GMT is returned, it means the requested id was incorrect.
         * Matching it with the default timezone increases the likelihood of
         * returning a sensible timezone with the intended raw offset as the
         * non-Olson requested id is likely to have come from the OS's default
         * timezone id in the first place.
         */

        tz->getID(tzid);
        gmt->getID(GMT);

        if (tzid == GMT && *u != GMT)
        {
            std::unique_ptr<TimeZone> deflt(TimeZone::createDefault());

            deflt->getID(tzid);
            if (tzid == *u)
                tz.swap(deflt);
        }

        return wrap_TimeZone(tz.release());
    }

    return PyErr_SetArgsError(type, "createTimeZone", arg);
}

#if U_ICU_VERSION_HEX >= VERSION_HEX(70, 0, 0)
static PyObject *t_timezone_createEnumeration(PyTypeObject *type,
                                              PyObject *args)
{
    int offset;
    charsArg region;
    StringEnumeration *tze;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(tze = TimeZone::createEnumeration(status));
        return wrap_StringEnumeration(tze, T_OWNED);

      case 1:
        if (!parseArgs(args, arg::i(&offset)))
        {
            STATUS_CALL(tze = TimeZone::createEnumerationForRawOffset(
                offset, status));
            return wrap_StringEnumeration(tze, T_OWNED);
        }
        if (!parseArgs(args, arg::n(&region)))
        {
            STATUS_CALL(tze = TimeZone::createEnumerationForRegion(
                region, status));
            return wrap_StringEnumeration(tze, T_OWNED);
        }
        break;
    }

    return PyErr_SetArgsError(type, "createEnumeration", args);
}
#else
static PyObject *t_timezone_createEnumeration(PyTypeObject *type,
                                              PyObject *args)
{
    int offset;
    charsArg country;

    switch (PyTuple_Size(args)) {
      case 0:
        return wrap_StringEnumeration(TimeZone::createEnumeration(), T_OWNED);
      case 1:
        if (!parseArgs(args, arg::i(&offset)))
            return wrap_StringEnumeration(TimeZone::createEnumeration(offset), T_OWNED);
        if (!parseArgs(args, arg::n(&country)))
            return wrap_StringEnumeration(TimeZone::createEnumeration(country), T_OWNED);
        break;
    }

    return PyErr_SetArgsError(type, "createEnumeration", args);
}
#endif

static PyObject *t_timezone_countEquivalentIDs(PyTypeObject *type,
                                               PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
        return PyInt_FromLong(TimeZone::countEquivalentIDs(*u));

    return PyErr_SetArgsError(type, "countEquivalentIDs", arg);
}

static PyObject *t_timezone_getEquivalentID(PyTypeObject *type, PyObject *args)
{
    UnicodeString *u, _u;
    int index;

    if (!parseArgs(args, arg::S(&u, &_u), arg::i(&index)))
    {
        UnicodeString v = TimeZone::getEquivalentID(*u, index);
        return PyUnicode_FromUnicodeString(&v);
    }

    return PyErr_SetArgsError(type, "getEquivalentID", args);
}

#if U_ICU_VERSION_HEX >= 0x04080000

static PyObject *t_timezone_getRegion(PyTypeObject *type, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        char region[16];
        int size;
        STATUS_CALL(size = TimeZone::getRegion(*u, region, sizeof(region), status));
        return PyString_FromStringAndSize(region, size);
    }
    
    return PyErr_SetArgsError(type, "getRegion", arg);
}

#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(52, 0, 0)
static PyObject *t_timezone_getIDForWindowsID(PyTypeObject *type,
                                              PyObject *args)
{
    UnicodeString *winId, _winId;
    charsArg region;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::S(&winId, &_winId)))
        {
            UnicodeString id;

            STATUS_CALL(TimeZone::getIDForWindowsID(*winId, NULL, id, status));
            return PyUnicode_FromUnicodeString(&id);
        }
        break;
      case 2:
        if (!parseArgs(args, arg::S(&winId, &_winId), arg::n(&region)))
        {
            UnicodeString id;

            STATUS_CALL(TimeZone::getIDForWindowsID(*winId, region, id,
                                                    status));
            return PyUnicode_FromUnicodeString(&id);
        }
        break;
    }

    return PyErr_SetArgsError(type, "getIDForWindowsID", args);
}

static PyObject *t_timezone_getWindowsID(PyTypeObject *type, PyObject *arg)
{
    UnicodeString *id, _id;

    if (!parseArg(arg, arg::S(&id, &_id)))
    {
        UnicodeString winId;

        STATUS_CALL(TimeZone::getWindowsID(*id, winId, status));
        return PyUnicode_FromUnicodeString(&winId);
    }

    return PyErr_SetArgsError(type, "getWindowsID", arg);
}
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(74, 0, 0)

static PyObject *t_timezone_getIanaID(PyTypeObject *type, PyObject *arg)
{
    UnicodeString *id, _id;

    if (!parseArg(arg, arg::S(&id, &_id)))
    {
        UnicodeString ianaId;

        STATUS_CALL(TimeZone::getIanaID(*id, ianaId, status));
        return PyUnicode_FromUnicodeString(&ianaId);
    }

    return PyErr_SetArgsError(type, "getIanaID", arg);
}

#endif

static PyObject *t_timezone_createDefault(PyTypeObject *type)
{
    return wrap_TimeZone(TimeZone::createDefault());
}

static PyObject *t_timezone_setDefault(PyTypeObject *type, PyObject *arg)
{
    TimeZone *tz;

    if (!parseArg(arg, arg::P<TimeZone>(TYPE_CLASSID(TimeZone), &tz)))
    {
        TimeZone::setDefault(*tz); /* copied */

        PyObject *m = PyImport_ImportModule("icu");
        PyObject *cls = PyObject_GetAttrString(m, "ICUtzinfo");
        PyObject *result = PyObject_CallMethod(
            cls, (char *) "_resetDefault", (char *) "", NULL);

        Py_DECREF(m);
        Py_DECREF(cls);

        return result;
    }

    return PyErr_SetArgsError(type, "setDefault", arg);
}

static PyObject *t_timezone_str(t_timezone *self)
{
    UnicodeString u;

    self->object->getID(u);
    return PyUnicode_FromUnicodeString(&u);
}

DEFINE_RICHCMP__ARG__(TimeZone, t_timezone)


/* BasicTimeZone */

static PyObject *t_basictimezone_getNextTransition(t_basictimezone *self,
                                                   PyObject *args)
{
    UDate base;
    UBool inclusive;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::D(&base)))
        {
            TimeZoneTransition tzt;
            UBool found = self->object->getNextTransition(base, false, tzt);

            if (found)
              return wrap_TimeZoneTransition(
                  (TimeZoneTransition *) (tzt.clone()), T_OWNED);

            Py_RETURN_NONE;
        }
        break;

      case 2:
        if (!parseArgs(args, arg::D(&base), arg::b(&inclusive)))
        {
            TimeZoneTransition tzt;
            UBool found = self->object->getNextTransition(base, inclusive, tzt);

            if (found)
              return wrap_TimeZoneTransition(
                  (TimeZoneTransition *) (tzt.clone()), T_OWNED);

            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getNextTransition", args);
}

static PyObject *t_basictimezone_getPreviousTransition(t_basictimezone *self,
                                                       PyObject *args)
{
    UDate base;
    UBool inclusive;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::D(&base)))
        {
            TimeZoneTransition tzt;
            UBool found = self->object->getPreviousTransition(base, false, tzt);

            if (found)
              return wrap_TimeZoneTransition(
                  (TimeZoneTransition *) (tzt.clone()), T_OWNED);

            Py_RETURN_NONE;
        }
        break;

      case 2:
        if (!parseArgs(args, arg::D(&base), arg::b(&inclusive)))
        {
            TimeZoneTransition tzt;
            UBool found = self->object->getPreviousTransition(
                base, inclusive, tzt);

            if (found)
              return wrap_TimeZoneTransition(
                  (TimeZoneTransition *) (tzt.clone()), T_OWNED);

            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getPreviousTransition", args);
}

static PyObject *t_basictimezone_hasEquivalentTransitions(t_basictimezone *self,
                                                          PyObject *args)
{
    BasicTimeZone *tz;
    UDate start, end;
    UBool ignoreDstAmount, result;

    switch (PyTuple_Size(args)) {
      case 3:
        if (!parseArgs(args,
                       arg::P<BasicTimeZone>(TYPE_CLASSID(BasicTimeZone), &tz),
                       arg::D(&start), arg::D(&end)))
        {
            STATUS_CALL(result = self->object->hasEquivalentTransitions(
                *tz, start, end, false, status));

            Py_RETURN_BOOL(result);
        }
        break;

      case 4:
        if (!parseArgs(args,
                       arg::P<BasicTimeZone>(TYPE_CLASSID(BasicTimeZone), &tz),
                       arg::D(&start), arg::D(&end),
                       arg::b(&ignoreDstAmount)))
        {
            STATUS_CALL(result = self->object->hasEquivalentTransitions(
                *tz, start, end, ignoreDstAmount, status));

            Py_RETURN_BOOL(result);
        }
        break;
    }

    return PyErr_SetArgsError(
        (PyObject *) self, "hasEquivalentTransitions", args);
}

static PyObject *t_basictimezone_countTransitionRules(t_basictimezone *self)
{
    int32_t count;
    STATUS_CALL(count = self->object->countTransitionRules(status));

    return PyInt_FromLong(count);
}

static PyObject *t_basictimezone_getTimeZoneRules(t_basictimezone *self)
{
    int32_t count = 0;
    STATUS_CALL(count = self->object->countTransitionRules(status));

    const InitialTimeZoneRule *initial;
    const TimeZoneRule **rules =
        (const TimeZoneRule **) calloc(count, sizeof(const TimeZoneRule *));
    if (rules == NULL)
        return PyErr_NoMemory();

    UErrorCode status = U_ZERO_ERROR;

    self->object->getTimeZoneRules(initial, rules, count, status);
    if (U_FAILURE(status))
    {
        free(rules);
        return ICUException(status).reportError();
    }

    PyObject *result = PyTuple_New(count + 1);

    if (result == NULL)
    {
        free(rules);
        return NULL;
    }

    PyTuple_SET_ITEM(result, 0, wrap_TimeZoneRule(*initial));
    for (int i = 0; i < count; ++i)
      PyTuple_SET_ITEM(result, i + 1, wrap_TimeZoneRule(*rules[i]));

    free(rules);
    return result;
}

static PyObject *t_basictimezone_getSimpleRulesNear(t_basictimezone *self,
                                                    PyObject *arg) {
    UDate date;

    if (!parseArg(arg, arg::D(&date)))
    {
        InitialTimeZoneRule *initial;
        AnnualTimeZoneRule *std = NULL, *dst = NULL;

        STATUS_CALL(self->object->getSimpleRulesNear(
            date, initial, std, dst, status));

        PyObject *result = PyTuple_New(3);

        if (result == NULL)
            return NULL;

        PyTuple_SET_ITEM(result, 0, wrap_TimeZoneRule(initial));

        if (std != NULL)
            PyTuple_SET_ITEM(result, 1, wrap_TimeZoneRule(std));
        else
        {
            PyTuple_SET_ITEM(result, 1, Py_None);
            Py_INCREF(Py_None);
        }

        if (dst != NULL)
            PyTuple_SET_ITEM(result, 2, wrap_TimeZoneRule(dst));
        else
        {
            PyTuple_SET_ITEM(result, 2, Py_None);
            Py_INCREF(Py_None);
        }

        return result;
    }

    return PyErr_SetArgsError((PyObject *) self, "getSimpleRulesNear", arg);
}


#if U_ICU_VERSION_HEX >= VERSION_HEX(69, 0, 0)

static PyObject *t_basictimezone_getOffsetFromLocal(t_basictimezone *self,
                                                    PyObject *args)
{
    UDate date;
    UTimeZoneLocalOption nonExistingOpt, duplicateOpt;

    switch (PyTuple_Size(args)) {
      case 3:
        if (!parseArgs(args,
                       arg::D(&date),
                       arg::Enum<UTimeZoneLocalOption>(&nonExistingOpt),
                       arg::Enum<UTimeZoneLocalOption>(&duplicateOpt)))
        {
            int32_t rawOffset, dstOffset;

            STATUS_CALL(self->object->getOffsetFromLocal(
                date, nonExistingOpt, duplicateOpt,
                rawOffset, dstOffset, status));

            return Py_BuildValue("(ii)", (int) rawOffset, (int) dstOffset);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getOffsetFromLocal", args);
}

#endif  // ICU >= 69


/* SimpleTimeZone */

static int t_simpletimezone_init(t_simpletimezone *self,
                                 PyObject *args, PyObject *kwds)
{
    SimpleTimeZone *tz;
    UnicodeString *u, _u;
    int rawOffsetGMT, savingsStartMonth, savingsStartDayOfWeekInMonth;
    int savingsStartDayOfWeek, savingsStartTime, savingsEndMonth, savingsDST;
    int savingsEndDayOfWeekInMonth, savingsEndDayOfWeek, savingsEndTime;
    SimpleTimeZone::TimeMode startMode, endMode;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args, arg::i(&rawOffsetGMT), arg::S(&u, &_u)))
        {
            tz = new SimpleTimeZone(rawOffsetGMT, *u);
            self->object = tz;
            self->flags = T_OWNED;
            break;
        }
      case 10:
        if (!parseArgs(args,
                       arg::i(&rawOffsetGMT), arg::S(&u, &_u),
                       arg::i(&savingsStartMonth), arg::i(&savingsStartDayOfWeekInMonth), arg::i(&savingsStartDayOfWeek), arg::i(&savingsStartTime), arg::i(&savingsEndMonth), arg::i(&savingsEndDayOfWeekInMonth), arg::i(&savingsEndDayOfWeek), arg::i(&savingsEndTime)))
        {
            INT_STATUS_CALL(tz = new SimpleTimeZone(rawOffsetGMT, *u, savingsStartMonth, savingsStartDayOfWeekInMonth, savingsStartDayOfWeek, savingsStartTime, savingsEndMonth, savingsEndDayOfWeekInMonth, savingsEndDayOfWeek, savingsEndTime, status));
            self->object = tz;
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      case 11:
        if (!parseArgs(args,
                       arg::i(&rawOffsetGMT), arg::S(&u, &_u),
                       arg::i(&savingsStartMonth), arg::i(&savingsStartDayOfWeekInMonth), arg::i(&savingsStartDayOfWeek), arg::i(&savingsStartTime), arg::i(&savingsEndMonth), arg::i(&savingsEndDayOfWeekInMonth), arg::i(&savingsEndDayOfWeek), arg::i(&savingsEndTime), arg::i(&savingsDST)))
        {
            INT_STATUS_CALL(tz = new SimpleTimeZone(rawOffsetGMT, *u, savingsStartMonth, savingsStartDayOfWeekInMonth, savingsStartDayOfWeek, savingsStartTime, savingsEndMonth, savingsEndDayOfWeekInMonth, savingsEndDayOfWeek, savingsEndTime, savingsDST, status));
            self->object = tz;
            self->flags = T_OWNED;
            break;
        }
        PyErr_SetArgsError((PyObject *) self, "__init__", args);
        return -1;
      case 13:
        if (!parseArgs(args,
                       arg::i(&rawOffsetGMT), arg::S(&u, &_u),
                       arg::i(&savingsStartMonth), arg::i(&savingsStartDayOfWeekInMonth), arg::i(&savingsStartDayOfWeek), arg::i(&savingsStartTime),
                       arg::Enum<SimpleTimeZone::TimeMode>(&startMode),
                       arg::i(&savingsEndMonth), arg::i(&savingsEndDayOfWeekInMonth), arg::i(&savingsEndDayOfWeek), arg::i(&savingsEndTime),
                       arg::Enum<SimpleTimeZone::TimeMode>(&endMode),
                       arg::i(&savingsDST)))
        {
            INT_STATUS_CALL(tz = new SimpleTimeZone(rawOffsetGMT, *u, savingsStartMonth, savingsStartDayOfWeekInMonth, savingsStartDayOfWeek, savingsStartTime, startMode, savingsEndMonth, savingsEndDayOfWeekInMonth, savingsEndDayOfWeek, savingsEndTime, endMode, savingsDST, status));
            self->object = tz;
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

static PyObject *t_simpletimezone_setStartYear(t_simpletimezone *self,
                                               PyObject *arg)
{
    int year;

    if (!parseArg(arg, arg::i(&year)))
    {
        self->object->setStartYear(year);
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setStartYear", arg);
}

static PyObject *t_simpletimezone_setStartRule(t_simpletimezone *self,
                                               PyObject *args)
{
    SimpleTimeZone::TimeMode mode;
    int month, dayOfMonth, dayOfWeek, dayOfWeekInMonth, time;
    UBool after;

    switch (PyTuple_Size(args)) {
      case 3:
        if (!parseArgs(args, arg::i(&month), arg::i(&dayOfMonth), arg::i(&time)))
        {
            STATUS_CALL(self->object->setStartRule(month, dayOfMonth, time,
                                                   status));
            Py_RETURN_NONE;
        }
        break;
      case 4:
        if (!parseArgs(args, arg::i(&month), arg::i(&dayOfWeekInMonth), arg::i(&dayOfWeek), arg::i(&time)))
        {
            STATUS_CALL(self->object->setStartRule(month, dayOfWeekInMonth,
                                                   dayOfWeek, time, status));
            Py_RETURN_NONE;
        }
        break;
      case 5:
        if (!parseArgs(args,
                       arg::i(&month), arg::i(&dayOfMonth), arg::i(&dayOfWeek), arg::i(&time),
                       arg::B(&after)))
        {
            STATUS_CALL(self->object->setStartRule(month, dayOfMonth, dayOfWeek,
                                                   time, (UBool) after,
                                                   status));
            Py_RETURN_NONE;
        }
        if (!parseArgs(args,
                       arg::i(&month), arg::i(&dayOfMonth), arg::i(&dayOfWeek), arg::i(&time),
                       arg::Enum<SimpleTimeZone::TimeMode>(&mode)))
        {
            STATUS_CALL(self->object->setStartRule(month, dayOfMonth, dayOfWeek,
                                                   time, mode, status));
            Py_RETURN_NONE;
        }
        break;
      case 6:
        if (!parseArgs(args,
                       arg::i(&month), arg::i(&dayOfMonth), arg::i(&dayOfWeek), arg::i(&time),
                       arg::Enum<SimpleTimeZone::TimeMode>(&mode),
                       arg::b(&after)))
        {
            STATUS_CALL(self->object->setStartRule(month, dayOfMonth, dayOfWeek,
                                                   time, mode, after, status));
            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "setStartRule", args);
}

static PyObject *t_simpletimezone_setEndRule(t_simpletimezone *self,
                                             PyObject *args)
{
    SimpleTimeZone::TimeMode mode;
    int month, dayOfMonth, dayOfWeek, dayOfWeekInMonth, time;
    UBool after;

    switch (PyTuple_Size(args)) {
      case 3:
        if (!parseArgs(args, arg::i(&month), arg::i(&dayOfMonth), arg::i(&time)))
        {
            STATUS_CALL(self->object->setEndRule(month, dayOfMonth,
                                                 time, status));
            Py_RETURN_NONE;
        }
        break;
      case 4:
        if (!parseArgs(args, arg::i(&month), arg::i(&dayOfWeekInMonth), arg::i(&dayOfWeek), arg::i(&time)))
        {
            STATUS_CALL(self->object->setEndRule(month, dayOfWeekInMonth,
                                                 dayOfWeek, time, status));
            Py_RETURN_NONE;
        }
        break;
      case 5:
        if (!parseArgs(args,
                       arg::i(&month), arg::i(&dayOfMonth), arg::i(&dayOfWeek), arg::i(&time),
                       arg::B(&after)))
        {
            STATUS_CALL(self->object->setEndRule(month, dayOfMonth, dayOfWeek,
                                                 time, (UBool) after, status));
            Py_RETURN_NONE;
        }
        if (!parseArgs(args, arg::i(&month), arg::i(&dayOfMonth), arg::i(&dayOfWeek), arg::i(&time),
                       arg::Enum<SimpleTimeZone::TimeMode>(&mode)))
        {
            STATUS_CALL(self->object->setEndRule(month, dayOfMonth, dayOfWeek,
                                                 time, mode, status));
            Py_RETURN_NONE;
        }
        break;
      case 6:
        if (!parseArgs(args,
                       arg::i(&month), arg::i(&dayOfMonth), arg::i(&dayOfWeek), arg::i(&time),
                       arg::Enum<SimpleTimeZone::TimeMode>(&mode),
                       arg::b(&after)))
        {
            STATUS_CALL(self->object->setEndRule(month, dayOfMonth, dayOfWeek,
                                                 time, mode, after, status));
            Py_RETURN_NONE;
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "setEndRule", args);
}

static PyObject *t_simpletimezone_getOffset(t_simpletimezone *self,
                                            PyObject *args)
{
    int era, year, month, day, dayOfWeek, millis;
    int monthLength, prevMonthLength;
    int offset;

    if (!parseArgs(args, arg::i(&era), arg::i(&year), arg::i(&month), arg::i(&day), arg::i(&dayOfWeek), arg::i(&millis), arg::i(&monthLength), arg::i(&prevMonthLength)))
    {
        STATUS_CALL(offset = self->object->getOffset(era, year, month, day, dayOfWeek, millis, monthLength, prevMonthLength, status));
        return PyInt_FromLong(offset);
    }

    return t_timezone_getOffset((t_timezone *) self, args);
}

static PyObject *t_simpletimezone_setDSTSavings(t_simpletimezone *self,
                                                PyObject *arg)
{
    int savings;

    if (!parseArg(arg, arg::i(&savings)))
    {
        STATUS_CALL(self->object->setDSTSavings(savings, status));
        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError((PyObject *) self, "setDSTSavings", arg);
}


/* VTimeZone */

static PyObject *t_vtimezone_getTZURL(t_vtimezone *self)
{
    UnicodeString url;

    if (self->object->getTZURL(url))
        return PyUnicode_FromUnicodeString(&url);

    Py_RETURN_NONE;
}

static PyObject *t_vtimezone_getLastModified(t_vtimezone *self)
{
    UDate date;

    if (self->object->getLastModified(date))
        return PyFloat_FromDouble(date / 1000.0);

    Py_RETURN_NONE;
}

static PyObject *t_vtimezone_write(t_vtimezone *self, PyObject *args)
{
    UDate start;
    UnicodeString data;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(self->object->write(data, status));
        return PyUnicode_FromUnicodeString(&data);

      case 1:
        if (!parseArgs(args, arg::D(&start)))
        {
            STATUS_CALL(self->object->write(start, data, status));
            return PyUnicode_FromUnicodeString(&data);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "write", args);
}

static PyObject *t_vtimezone_writeSimple(t_vtimezone *self, PyObject *arg)
{
    UDate date;

    if (!parseArg(arg, arg::D(&date)))
    {
        UnicodeString data;
        STATUS_CALL(self->object->writeSimple(date, data, status));

        return PyUnicode_FromUnicodeString(&data);
    }

    return PyErr_SetArgsError((PyObject *) self, "writeSimple", arg);
}

static PyObject *t_vtimezone_createVTimeZone(PyTypeObject *type, PyObject *arg)
{
    UnicodeString *u, _u;

    if (!parseArg(arg, arg::S(&u, &_u)))
    {
        VTimeZone *vtz;
        STATUS_CALL(vtz = VTimeZone::createVTimeZone(*u, status));

        return wrap_VTimeZone(vtz, T_OWNED);
    }

    return PyErr_SetArgsError(type, "createVTimeZone", arg);
}

static PyObject *t_vtimezone_createVTimeZoneByID(
    PyTypeObject *type, PyObject *arg)
{
    UnicodeString *id, _id;

    if (!parseArg(arg, arg::S(&id, &_id)))
    {
        VTimeZone *vtz = VTimeZone::createVTimeZoneByID(*id);

        if (vtz != NULL)
            return wrap_VTimeZone(vtz, T_OWNED);

        Py_RETURN_NONE;
    }

    return PyErr_SetArgsError(type, "createVTimeZoneByID", arg);
}

#if U_ICU_VERSION_HEX >= 0x04060000
static PyObject *t_vtimezone_createVTimeZoneFromBasicTimeZone(
    PyTypeObject *type, PyObject *arg)
{
    BasicTimeZone *tz;

    if (!parseArg(arg, arg::P<BasicTimeZone>(TYPE_CLASSID(BasicTimeZone), &tz)))
    {
        VTimeZone *vtz;
        STATUS_CALL(vtz = VTimeZone::createVTimeZoneFromBasicTimeZone(
            *tz, status));

        return wrap_VTimeZone(vtz, T_OWNED);
    }

    return PyErr_SetArgsError(type, "createVTimeZoneFromBasicTimeZone", arg);
}
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)

/* TimeZoneNames */

static PyObject *t_timezonenames_getAvailableMetaZoneIDs(t_timezonenames *self, PyObject *args)
{
    UnicodeString *id, _id;
    StringEnumeration *se;

    switch (PyTuple_Size(args)) {
      case 0:
        STATUS_CALL(se = self->object->getAvailableMetaZoneIDs(status));
        return wrap_StringEnumeration(se, T_OWNED);

      case 1:
        if (!parseArgs(args, arg::S(&id, &_id)))
        {
            STATUS_CALL(se = self->object->getAvailableMetaZoneIDs(*id, status));
            return wrap_StringEnumeration(se, T_OWNED);
        }
        break;
    }

    return PyErr_SetArgsError((PyObject *) self, "getAvailableMetaZoneIDs", args);
}

static PyObject *t_timezonenames_getMetaZoneID(t_timezonenames *self, PyObject *args)
{
    UnicodeString *tzID, _tzID;
    UDate date;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args, arg::S(&tzID, &_tzID), arg::D(&date)))
        {
            UnicodeString mzID;
            self->object->getMetaZoneID(*tzID, date, mzID);
            return PyUnicode_FromUnicodeString(&mzID);
        }
    }
    
    return PyErr_SetArgsError((PyObject *) self, "getMetaZoneID", args);
}

static PyObject *t_timezonenames_getReferenceZoneID(t_timezonenames *self, PyObject *args)
{
    UnicodeString *mzID, _mzID;
    charsArg region;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args, arg::S(&mzID, &_mzID), arg::n(&region)))
        {
            UnicodeString tzID;
            self->object->getReferenceZoneID(*mzID, region, tzID);
            return PyUnicode_FromUnicodeString(&tzID);
        }
    }

    return PyErr_SetArgsError((PyObject *) self, "getReferenceZoneID", args);
}

static PyObject *t_timezonenames_getMetaZoneDisplayName(t_timezonenames *self, PyObject *args)
{
    UnicodeString *mzID, _mzID;
    UTimeZoneNameType type;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::S(&mzID, &_mzID)))
        {
            UnicodeString name;
            self->object->getMetaZoneDisplayName(*mzID, UTZNM_UNKNOWN, name);
            return PyUnicode_FromUnicodeString(&name);
        }
      case 2:
        if (!parseArgs(args,
                       arg::S(&mzID, &_mzID),
                       arg::Enum<UTimeZoneNameType>(&type)))
        {
            UnicodeString name;
            self->object->getMetaZoneDisplayName(*mzID, type, name);
            return PyUnicode_FromUnicodeString(&name);
        }
    }

    return PyErr_SetArgsError((PyObject *) self, "getMetaZoneDisplayName", args);
}

static PyObject *t_timezonenames_getTimeZoneDisplayName(t_timezonenames *self, PyObject *args)
{
    UnicodeString *tzID, _tzID;
    UTimeZoneNameType type;

    switch (PyTuple_Size(args)) {
      case 1:
        if (!parseArgs(args, arg::S(&tzID, &_tzID)))
        {
            UnicodeString name;
            self->object->getTimeZoneDisplayName(*tzID, UTZNM_UNKNOWN, name);
            return PyUnicode_FromUnicodeString(&name);
        }
      case 2:
        if (!parseArgs(args,
                       arg::S(&tzID, &_tzID),
                       arg::Enum<UTimeZoneNameType>(&type)))
        {
            UnicodeString name;
            self->object->getTimeZoneDisplayName(*tzID, type, name);
            return PyUnicode_FromUnicodeString(&name);
        }
    }

    return PyErr_SetArgsError((PyObject *) self, "getTimeZoneDisplayName", args);
}

static PyObject *t_timezonenames_getExemplarLocationName(t_timezonenames *self, PyObject *arg)
{
    UnicodeString *tzID, _tzID;

    if (!parseArg(arg, arg::S(&tzID, &_tzID)))
    {
        UnicodeString name;
        self->object->getExemplarLocationName(*tzID, name);
        return PyUnicode_FromUnicodeString(&name);
    }

    return PyErr_SetArgsError((PyObject *) self, "getExemplarLocationName", arg);
}

static PyObject *t_timezonenames_getDisplayName(t_timezonenames *self, PyObject *args)
{
    UnicodeString *tzID, _tzID;
    UTimeZoneNameType type;
    UDate date;

    switch (PyTuple_Size(args)) {
      case 2:
        if (!parseArgs(args, arg::S(&tzID, &_tzID), arg::D(&date)))
        {
            UnicodeString name;
            self->object->getDisplayName(*tzID, UTZNM_UNKNOWN, date, name);
            return PyUnicode_FromUnicodeString(&name);
        }
      case 3:
        if (!parseArgs(args,
                       arg::S(&tzID, &_tzID),
                       arg::Enum<UTimeZoneNameType>(&type),
                       arg::D(&date)))
        {
            UnicodeString name;
            self->object->getDisplayName(*tzID, type, date, name);
            return PyUnicode_FromUnicodeString(&name);
        }
    }

    return PyErr_SetArgsError((PyObject *) self, "getDisplayName", args);
}

static PyObject *t_timezonenames_createInstance(PyTypeObject *type, PyObject *arg)
{
    TimeZoneNames *tzn;
    Locale *locale;

    if (!parseArg(arg, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
    {
        STATUS_CALL(tzn = TimeZoneNames::createInstance(*locale, status));
        return wrap_TimeZoneNames(tzn, T_OWNED);
    }

    return PyErr_SetArgsError(type, "createInstance", arg);
}

#endif // ICU >= 50

#if U_ICU_VERSION_HEX >= VERSION_HEX(54, 0, 0)

static PyObject *t_timezonenames_createTZDBInstance(PyTypeObject *type, PyObject *arg)
{
    TimeZoneNames *tzn;
    Locale *locale;

    if (!parseArg(arg, arg::P<Locale>(TYPE_CLASSID(Locale), &locale)))
    {
        STATUS_CALL(tzn = TimeZoneNames::createTZDBInstance(*locale, status));
        return wrap_TimeZoneNames(tzn, T_OWNED);
    }

    return PyErr_SetArgsError(type, "createInstance", arg);
}

#endif // ICU >= 54

void _init_timezone(PyObject *m)
{
    TimeZoneRuleType_.tp_str = (reprfunc) t_timezonerule_str;
    TimeZoneRuleType_.tp_richcompare = (richcmpfunc) t_timezonerule_richcmp;
    TimeZoneType_.tp_str = (reprfunc) t_timezone_str;
    TimeZoneType_.tp_richcompare = (richcmpfunc) t_timezone_richcmp;

    INSTALL_CONSTANTS_TYPE(DateRuleType, m);
    INSTALL_CONSTANTS_TYPE(TimeRuleType, m);
#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)
    INSTALL_CONSTANTS_TYPE(UTimeZoneNameType, m);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(69, 0, 0)
    INSTALL_CONSTANTS_TYPE(UTimeZoneLocalOption, m);
#endif
    REGISTER_TYPE(TimeZoneRule, m);
    REGISTER_TYPE(AnnualTimeZoneRule, m);
    REGISTER_TYPE(InitialTimeZoneRule, m);
    REGISTER_TYPE(TimeArrayTimeZoneRule, m);
    REGISTER_TYPE(DateTimeRule, m);
    REGISTER_TYPE(TimeZoneTransition, m);
    REGISTER_TYPE(TimeZone, m);
    REGISTER_TYPE(BasicTimeZone, m);
    REGISTER_TYPE(RuleBasedTimeZone, m);
    REGISTER_TYPE(SimpleTimeZone, m);
    REGISTER_TYPE(VTimeZone, m);
#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)
    REGISTER_TYPE(TimeZoneNames, m);
#endif
    
#if U_ICU_VERSION_HEX >= VERSION_HEX(50, 0, 0)
    INSTALL_ENUM(UTimeZoneNameType, "UNKNOWN", UTZNM_UNKNOWN);
    INSTALL_ENUM(UTimeZoneNameType, "LONG_GENERIC", UTZNM_LONG_GENERIC);
    INSTALL_ENUM(UTimeZoneNameType, "LONG_STANDARD", UTZNM_LONG_STANDARD);
    INSTALL_ENUM(UTimeZoneNameType, "LONG_DAYLIGHT", UTZNM_LONG_DAYLIGHT);
    INSTALL_ENUM(UTimeZoneNameType, "SHORT_GENERIC", UTZNM_SHORT_GENERIC);
    INSTALL_ENUM(UTimeZoneNameType, "SHORT_STANDARD", UTZNM_SHORT_STANDARD);
    INSTALL_ENUM(UTimeZoneNameType, "SHORT_DAYLIGHT", UTZNM_SHORT_DAYLIGHT);
#endif
#if U_ICU_VERSION_HEX >= VERSION_HEX(51, 0, 0)
    INSTALL_ENUM(UTimeZoneNameType, "EXEMPLAR_LOCATION", UTZNM_EXEMPLAR_LOCATION);
#endif

#if U_ICU_VERSION_HEX >= VERSION_HEX(69, 0, 0)
    INSTALL_ENUM(UTimeZoneLocalOption, "FORMER", UCAL_TZ_LOCAL_FORMER);
    INSTALL_ENUM(UTimeZoneLocalOption, "LATTER", UCAL_TZ_LOCAL_LATTER);
    INSTALL_ENUM(UTimeZoneLocalOption, "STANDARD_FORMER", UCAL_TZ_LOCAL_STANDARD_FORMER);
    INSTALL_ENUM(UTimeZoneLocalOption, "STANDARD_LATTER", UCAL_TZ_LOCAL_STANDARD_LATTER);
    INSTALL_ENUM(UTimeZoneLocalOption, "DAYLIGHT_FORMER", UCAL_TZ_LOCAL_DAYLIGHT_FORMER);
    INSTALL_ENUM(UTimeZoneLocalOption, "DAYLIGHT_LATTER", UCAL_TZ_LOCAL_DAYLIGHT_LATTER);
#endif

    INSTALL_ENUM(DateRuleType, "DOM", DateTimeRule::DOM);
    INSTALL_ENUM(DateRuleType, "DOW", DateTimeRule::DOW);
    INSTALL_ENUM(DateRuleType, "DOW_GEQ_DOM", DateTimeRule::DOW_GEQ_DOM);
    INSTALL_ENUM(DateRuleType, "DOW_LEQ_DOM", DateTimeRule::DOW_LEQ_DOM);

    INSTALL_ENUM(TimeRuleType, "WALL_TIME", DateTimeRule::WALL_TIME);
    INSTALL_ENUM(TimeRuleType, "STANDARD_TIME", DateTimeRule::STANDARD_TIME);
    INSTALL_ENUM(TimeRuleType, "UTC_TIME", DateTimeRule::UTC_TIME);

    INSTALL_STATIC_INT(TimeZone, SHORT);
    INSTALL_STATIC_INT(TimeZone, LONG);
#if U_ICU_VERSION_HEX >= 0x04040000
    INSTALL_STATIC_INT(TimeZone, SHORT_GENERIC);
    INSTALL_STATIC_INT(TimeZone, LONG_GENERIC);
    INSTALL_STATIC_INT(TimeZone, SHORT_GMT);
    INSTALL_STATIC_INT(TimeZone, LONG_GMT);
    INSTALL_STATIC_INT(TimeZone, SHORT_COMMONLY_USED);
    INSTALL_STATIC_INT(TimeZone, GENERIC_LOCATION);
#endif

    INSTALL_STATIC_INT(SimpleTimeZone, WALL_TIME);
    INSTALL_STATIC_INT(SimpleTimeZone, STANDARD_TIME);
    INSTALL_STATIC_INT(SimpleTimeZone, UTC_TIME);

    INSTALL_STATIC_INT(AnnualTimeZoneRule, MAX_YEAR);
}
