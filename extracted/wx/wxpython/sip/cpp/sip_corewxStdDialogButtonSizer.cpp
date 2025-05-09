/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/sizer.h>
        #include <wx/gdicmn.h>
        #include <wx/button.h>
        #include <wx/sizer.h>
        #include <wx/window.h>
        #include <wx/sizer.h>
        #include <wx/gdicmn.h>
        #include <wx/sizer.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


class sipwxStdDialogButtonSizer : public ::wxStdDialogButtonSizer
{
public:
    sipwxStdDialogButtonSizer();
    virtual ~sipwxStdDialogButtonSizer();

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    void RecalcSizes() SIP_OVERRIDE;
    void RepositionChildren(const ::wxSize&) SIP_OVERRIDE;
    bool InformFirstDirection(int, int, int) SIP_OVERRIDE;
    ::wxSize CalcMin() SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxStdDialogButtonSizer(const sipwxStdDialogButtonSizer &);
    sipwxStdDialogButtonSizer &operator = (const sipwxStdDialogButtonSizer &);

    char sipPyMethods[4];
};

sipwxStdDialogButtonSizer::sipwxStdDialogButtonSizer(): ::wxStdDialogButtonSizer(), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxStdDialogButtonSizer::~sipwxStdDialogButtonSizer()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

void sipwxStdDialogButtonSizer::RecalcSizes()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[0], &sipPySelf, SIP_NULLPTR, sipName_RecalcSizes);

    if (!sipMeth)
    {
        ::wxStdDialogButtonSizer::RecalcSizes();
        return;
    }

    extern void sipVH__core_57(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    sipVH__core_57(sipGILState, 0, sipPySelf, sipMeth);
}

void sipwxStdDialogButtonSizer::RepositionChildren(const ::wxSize& minSize)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[1], &sipPySelf, SIP_NULLPTR, sipName_RepositionChildren);

    if (!sipMeth)
    {
        ::wxStdDialogButtonSizer::RepositionChildren(minSize);
        return;
    }

    extern void sipVH__core_106(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxSize&);

    sipVH__core_106(sipGILState, 0, sipPySelf, sipMeth, minSize);
}

bool sipwxStdDialogButtonSizer::InformFirstDirection(int direction, int size, int availableOtherDir)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[2], &sipPySelf, SIP_NULLPTR, sipName_InformFirstDirection);

    if (!sipMeth)
        return ::wxStdDialogButtonSizer::InformFirstDirection(direction, size, availableOtherDir);

    extern bool sipVH__core_105(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, int, int, int);

    return sipVH__core_105(sipGILState, 0, sipPySelf, sipMeth, direction, size, availableOtherDir);
}

::wxSize sipwxStdDialogButtonSizer::CalcMin()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[3], &sipPySelf, SIP_NULLPTR, sipName_CalcMin);

    if (!sipMeth)
        return ::wxStdDialogButtonSizer::CalcMin();

    extern ::wxSize sipVH__core_25(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_25(sipGILState, 0, sipPySelf, sipMeth);
}


PyDoc_STRVAR(doc_wxStdDialogButtonSizer_AddButton, "AddButton(button) -> None\n"
"\n"
"Adds a button to the wxStdDialogButtonSizer.");

extern "C" {static PyObject *meth_wxStdDialogButtonSizer_AddButton(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxStdDialogButtonSizer_AddButton(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxButton* button;
        ::wxStdDialogButtonSizer *sipCpp;

        static const char *sipKwdList[] = {
            sipName_button,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ8", &sipSelf, sipType_wxStdDialogButtonSizer, &sipCpp, sipType_wxButton, &button))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->AddButton(button);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_StdDialogButtonSizer, sipName_AddButton, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxStdDialogButtonSizer_Realize, "Realize() -> None\n"
"\n"
"Rearranges the buttons and applies proper spacing between buttons to\n"
"make them match the platform or toolkit's interface guidelines.");

extern "C" {static PyObject *meth_wxStdDialogButtonSizer_Realize(PyObject *, PyObject *);}
static PyObject *meth_wxStdDialogButtonSizer_Realize(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxStdDialogButtonSizer *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxStdDialogButtonSizer, &sipCpp))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->Realize();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_StdDialogButtonSizer, sipName_Realize, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxStdDialogButtonSizer_SetAffirmativeButton, "SetAffirmativeButton(button) -> None\n"
"\n"
"Sets the affirmative button for the sizer.");

extern "C" {static PyObject *meth_wxStdDialogButtonSizer_SetAffirmativeButton(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxStdDialogButtonSizer_SetAffirmativeButton(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxButton* button;
        ::wxStdDialogButtonSizer *sipCpp;

        static const char *sipKwdList[] = {
            sipName_button,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ8", &sipSelf, sipType_wxStdDialogButtonSizer, &sipCpp, sipType_wxButton, &button))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetAffirmativeButton(button);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_StdDialogButtonSizer, sipName_SetAffirmativeButton, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxStdDialogButtonSizer_SetCancelButton, "SetCancelButton(button) -> None\n"
"\n"
"Sets the cancel button for the sizer.");

extern "C" {static PyObject *meth_wxStdDialogButtonSizer_SetCancelButton(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxStdDialogButtonSizer_SetCancelButton(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxButton* button;
        ::wxStdDialogButtonSizer *sipCpp;

        static const char *sipKwdList[] = {
            sipName_button,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ8", &sipSelf, sipType_wxStdDialogButtonSizer, &sipCpp, sipType_wxButton, &button))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetCancelButton(button);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_StdDialogButtonSizer, sipName_SetCancelButton, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxStdDialogButtonSizer_SetNegativeButton, "SetNegativeButton(button) -> None\n"
"\n"
"Sets the negative button for the sizer.");

extern "C" {static PyObject *meth_wxStdDialogButtonSizer_SetNegativeButton(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxStdDialogButtonSizer_SetNegativeButton(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxButton* button;
        ::wxStdDialogButtonSizer *sipCpp;

        static const char *sipKwdList[] = {
            sipName_button,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ8", &sipSelf, sipType_wxStdDialogButtonSizer, &sipCpp, sipType_wxButton, &button))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetNegativeButton(button);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_StdDialogButtonSizer, sipName_SetNegativeButton, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxStdDialogButtonSizer_RepositionChildren, "RepositionChildren(minSize) -> None\n"
"\n"
"Method which must be overridden in the derived sizer classes.");

extern "C" {static PyObject *meth_wxStdDialogButtonSizer_RepositionChildren(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxStdDialogButtonSizer_RepositionChildren(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxSize* minSize;
        int minSizeState = 0;
        ::wxStdDialogButtonSizer *sipCpp;

        static const char *sipKwdList[] = {
            sipName_minSize,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxStdDialogButtonSizer, &sipCpp, sipType_wxSize, &minSize, &minSizeState))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            (sipSelfWasArg ? sipCpp->::wxStdDialogButtonSizer::RepositionChildren(*minSize) : sipCpp->RepositionChildren(*minSize));
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxSize *>(minSize), sipType_wxSize, minSizeState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_StdDialogButtonSizer, sipName_RepositionChildren, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxStdDialogButtonSizer_CalcMin, "CalcMin() -> Size\n"
"\n"
"Implements the calculation of a box sizer's minimal.");

extern "C" {static PyObject *meth_wxStdDialogButtonSizer_CalcMin(PyObject *, PyObject *);}
static PyObject *meth_wxStdDialogButtonSizer_CalcMin(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxStdDialogButtonSizer *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxStdDialogButtonSizer, &sipCpp))
        {
            ::wxSize*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxSize((sipSelfWasArg ? sipCpp->::wxStdDialogButtonSizer::CalcMin() : sipCpp->CalcMin()));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxSize, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_StdDialogButtonSizer, sipName_CalcMin, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxStdDialogButtonSizer(void *, const sipTypeDef *);}
static void *cast_wxStdDialogButtonSizer(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxStdDialogButtonSizer *sipCpp = reinterpret_cast<::wxStdDialogButtonSizer *>(sipCppV);

    if (targetType == sipType_wxStdDialogButtonSizer)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxBoxSizer)->ctd_cast(static_cast<::wxBoxSizer *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxStdDialogButtonSizer(void *, int);}
static void release_wxStdDialogButtonSizer(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxStdDialogButtonSizer *>(sipCppV);
    else
        delete reinterpret_cast<::wxStdDialogButtonSizer *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxStdDialogButtonSizer(sipSimpleWrapper *);}
static void dealloc_wxStdDialogButtonSizer(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxStdDialogButtonSizer *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxStdDialogButtonSizer(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxStdDialogButtonSizer(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxStdDialogButtonSizer(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxStdDialogButtonSizer *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxStdDialogButtonSizer();
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

    return SIP_NULLPTR;
}


/* Define this type's super-types. */
static sipEncodedTypeDef supers_wxStdDialogButtonSizer[] = {{44, 255, 1}};


static PyMethodDef methods_wxStdDialogButtonSizer[] = {
    {sipName_AddButton, SIP_MLMETH_CAST(meth_wxStdDialogButtonSizer_AddButton), METH_VARARGS|METH_KEYWORDS, doc_wxStdDialogButtonSizer_AddButton},
    {sipName_CalcMin, meth_wxStdDialogButtonSizer_CalcMin, METH_VARARGS, doc_wxStdDialogButtonSizer_CalcMin},
    {sipName_Realize, meth_wxStdDialogButtonSizer_Realize, METH_VARARGS, doc_wxStdDialogButtonSizer_Realize},
    {sipName_RepositionChildren, SIP_MLMETH_CAST(meth_wxStdDialogButtonSizer_RepositionChildren), METH_VARARGS|METH_KEYWORDS, doc_wxStdDialogButtonSizer_RepositionChildren},
    {sipName_SetAffirmativeButton, SIP_MLMETH_CAST(meth_wxStdDialogButtonSizer_SetAffirmativeButton), METH_VARARGS|METH_KEYWORDS, doc_wxStdDialogButtonSizer_SetAffirmativeButton},
    {sipName_SetCancelButton, SIP_MLMETH_CAST(meth_wxStdDialogButtonSizer_SetCancelButton), METH_VARARGS|METH_KEYWORDS, doc_wxStdDialogButtonSizer_SetCancelButton},
    {sipName_SetNegativeButton, SIP_MLMETH_CAST(meth_wxStdDialogButtonSizer_SetNegativeButton), METH_VARARGS|METH_KEYWORDS, doc_wxStdDialogButtonSizer_SetNegativeButton}
};

PyDoc_STRVAR(doc_wxStdDialogButtonSizer, "StdDialogButtonSizer() -> None\n"
"\n"
"This class creates button layouts which conform to the standard button\n"
"spacing and ordering defined by the platform or toolkit's user\n"
"interface guidelines (if such things exist).");


sipClassTypeDef sipTypeDef__core_wxStdDialogButtonSizer = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxStdDialogButtonSizer,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_StdDialogButtonSizer,
        {0, 0, 1},
        7, methods_wxStdDialogButtonSizer,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxStdDialogButtonSizer,
    -1,
    -1,
    supers_wxStdDialogButtonSizer,
    SIP_NULLPTR,
    init_type_wxStdDialogButtonSizer,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxStdDialogButtonSizer,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxStdDialogButtonSizer,
    cast_wxStdDialogButtonSizer,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    sizeof (::wxStdDialogButtonSizer),
};
