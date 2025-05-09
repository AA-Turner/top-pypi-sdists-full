/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_adv.h"
        #include <wx/calctrl.h>
        #include <wx/window.h>
        #include <wx/datetime.h>
        #include <wx/event.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


class sipwxCalendarEvent : public ::wxCalendarEvent
{
public:
    sipwxCalendarEvent();
    sipwxCalendarEvent(::wxWindow*, const ::wxDateTime&, ::wxEventType);
    sipwxCalendarEvent(const ::wxCalendarEvent&);
    virtual ~sipwxCalendarEvent();

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    ::wxEvent* Clone() const SIP_OVERRIDE;
    ::wxEventCategory GetEventCategory() const SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxCalendarEvent(const sipwxCalendarEvent &);
    sipwxCalendarEvent &operator = (const sipwxCalendarEvent &);

    char sipPyMethods[2];
};

sipwxCalendarEvent::sipwxCalendarEvent(): ::wxCalendarEvent(), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxCalendarEvent::sipwxCalendarEvent(::wxWindow*win, const ::wxDateTime& dt, ::wxEventType type): ::wxCalendarEvent(win, dt, type), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxCalendarEvent::sipwxCalendarEvent(const ::wxCalendarEvent& a0): ::wxCalendarEvent(a0), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxCalendarEvent::~sipwxCalendarEvent()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

::wxEvent* sipwxCalendarEvent::Clone() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[0]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_Clone);

    if (!sipMeth)
        return ::wxCalendarEvent::Clone();

    extern ::wxEvent* sipVH__adv_27(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__adv_27(sipGILState, 0, sipPySelf, sipMeth);
}

::wxEventCategory sipwxCalendarEvent::GetEventCategory() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[1]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetEventCategory);

    if (!sipMeth)
        return ::wxCalendarEvent::GetEventCategory();

    extern ::wxEventCategory sipVH__adv_28(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__adv_28(sipGILState, 0, sipPySelf, sipMeth);
}


PyDoc_STRVAR(doc_wxCalendarEvent_GetWeekDay, "GetWeekDay() -> wx.DateTime.WeekDay\n"
"\n"
"Returns the week day on which the user clicked in\n"
"EVT_CALENDAR_WEEKDAY_CLICKED handler.");

extern "C" {static PyObject *meth_wxCalendarEvent_GetWeekDay(PyObject *, PyObject *);}
static PyObject *meth_wxCalendarEvent_GetWeekDay(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxCalendarEvent *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxCalendarEvent, &sipCpp))
        {
            ::wxDateTime::WeekDay sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetWeekDay();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxDateTime_WeekDay);
        }
    }

    sipNoMethod(sipParseErr, sipName_CalendarEvent, sipName_GetWeekDay, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxCalendarEvent_SetWeekDay, "SetWeekDay(day) -> None\n"
"\n"
"Sets the week day carried by the event, normally only used by the\n"
"library internally.");

extern "C" {static PyObject *meth_wxCalendarEvent_SetWeekDay(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxCalendarEvent_SetWeekDay(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxDateTime::WeekDay day;
        ::wxCalendarEvent *sipCpp;

        static const char *sipKwdList[] = {
            sipName_day,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxCalendarEvent, &sipCpp, sipType_wxDateTime_WeekDay, &day))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetWeekDay(day);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_CalendarEvent, sipName_SetWeekDay, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxCalendarEvent_Clone, "Clone(self) -> Optional[Event]");

extern "C" {static PyObject *meth_wxCalendarEvent_Clone(PyObject *, PyObject *);}
static PyObject *meth_wxCalendarEvent_Clone(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxCalendarEvent *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxCalendarEvent, &sipCpp))
        {
            ::wxEvent*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxCalendarEvent::Clone() : sipCpp->Clone());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxEvent, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_CalendarEvent, sipName_Clone, doc_wxCalendarEvent_Clone);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxCalendarEvent(void *, const sipTypeDef *);}
static void *cast_wxCalendarEvent(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxCalendarEvent *sipCpp = reinterpret_cast<::wxCalendarEvent *>(sipCppV);

    if (targetType == sipType_wxCalendarEvent)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxDateEvent)->ctd_cast(static_cast<::wxDateEvent *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxCalendarEvent(void *, int);}
static void release_wxCalendarEvent(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxCalendarEvent *>(sipCppV);
    else
        delete reinterpret_cast<::wxCalendarEvent *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxCalendarEvent(sipSimpleWrapper *);}
static void dealloc_wxCalendarEvent(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxCalendarEvent *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxCalendarEvent(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxCalendarEvent(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxCalendarEvent(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxCalendarEvent *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxCalendarEvent();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    {
        ::wxWindow* win;
        const ::wxDateTime* dt;
        int dtState = 0;
        ::wxEventType type;

        static const char *sipKwdList[] = {
            sipName_win,
            sipName_dt,
            sipName_type,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J8J1i", sipType_wxWindow, &win, sipType_wxDateTime, &dt, &dtState, &type))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxCalendarEvent(win, *dt, type);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxDateTime *>(dt), sipType_wxDateTime, dtState);

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    {
        const ::wxCalendarEvent* a0;

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, "J9", sipType_wxCalendarEvent, &a0))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxCalendarEvent(*a0);
            Py_END_ALLOW_THREADS

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}


/* Define this type's super-types. */
static sipEncodedTypeDef supers_wxCalendarEvent[] = {{18, 255, 1}};


static PyMethodDef methods_wxCalendarEvent[] = {
    {sipName_Clone, meth_wxCalendarEvent_Clone, METH_VARARGS, doc_wxCalendarEvent_Clone},
    {sipName_GetWeekDay, meth_wxCalendarEvent_GetWeekDay, METH_VARARGS, doc_wxCalendarEvent_GetWeekDay},
    {sipName_SetWeekDay, SIP_MLMETH_CAST(meth_wxCalendarEvent_SetWeekDay), METH_VARARGS|METH_KEYWORDS, doc_wxCalendarEvent_SetWeekDay}
};

sipVariableDef variables_wxCalendarEvent[] = {
    {PropertyVariable, sipName_WeekDay, &methods_wxCalendarEvent[1], &methods_wxCalendarEvent[2], SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxCalendarEvent, "CalendarEvent() -> None\n"
"CalendarEvent(win, dt, type) -> None\n"
"\n"
"The wxCalendarEvent class is used together with wxCalendarCtrl.");


sipClassTypeDef sipTypeDef__adv_wxCalendarEvent = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxCalendarEvent,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_CalendarEvent,
        {0, 0, 1},
        3, methods_wxCalendarEvent,
        0, SIP_NULLPTR,
        1, variables_wxCalendarEvent,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxCalendarEvent,
    -1,
    -1,
    supers_wxCalendarEvent,
    SIP_NULLPTR,
    init_type_wxCalendarEvent,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxCalendarEvent,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxCalendarEvent,
    cast_wxCalendarEvent,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    sizeof (::wxCalendarEvent),
};
