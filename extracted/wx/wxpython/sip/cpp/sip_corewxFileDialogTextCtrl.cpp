/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/filedlgcustomize.h>
        #include <wx/event.h>
        #include <wx/eventfilter.h>
        #include <wx/event.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


PyDoc_STRVAR(doc_wxFileDialogTextCtrl_GetValue, "GetValue() -> str\n"
"\n"
"Get the current value entered into the control.");

extern "C" {static PyObject *meth_wxFileDialogTextCtrl_GetValue(PyObject *, PyObject *);}
static PyObject *meth_wxFileDialogTextCtrl_GetValue(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxFileDialogTextCtrl *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxFileDialogTextCtrl, &sipCpp))
        {
            ::wxString*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxString(sipCpp->GetValue());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxString, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_FileDialogTextCtrl, sipName_GetValue, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxFileDialogTextCtrl_SetValue, "SetValue(text) -> None\n"
"\n"
"Set the current control value.");

extern "C" {static PyObject *meth_wxFileDialogTextCtrl_SetValue(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxFileDialogTextCtrl_SetValue(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxString* text;
        int textState = 0;
        ::wxFileDialogTextCtrl *sipCpp;

        static const char *sipKwdList[] = {
            sipName_text,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxFileDialogTextCtrl, &sipCpp, sipType_wxString, &text, &textState))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetValue(*text);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxString *>(text), sipType_wxString, textState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_FileDialogTextCtrl, sipName_SetValue, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxFileDialogTextCtrl(void *, const sipTypeDef *);}
static void *cast_wxFileDialogTextCtrl(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxFileDialogTextCtrl *sipCpp = reinterpret_cast<::wxFileDialogTextCtrl *>(sipCppV);

    if (targetType == sipType_wxFileDialogTextCtrl)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxFileDialogCustomControl)->ctd_cast(static_cast<::wxFileDialogCustomControl *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxFileDialogTextCtrl(void *, int);}
static void release_wxFileDialogTextCtrl(void *sipCppV, int)
{
    Py_BEGIN_ALLOW_THREADS

    delete reinterpret_cast<::wxFileDialogTextCtrl *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxFileDialogTextCtrl(sipSimpleWrapper *);}
static void dealloc_wxFileDialogTextCtrl(sipSimpleWrapper *sipSelf)
{
    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxFileDialogTextCtrl(sipGetAddress(sipSelf), 0);
    }
}


/* Define this type's super-types. */
static sipEncodedTypeDef supers_wxFileDialogTextCtrl[] = {{171, 255, 1}};


static PyMethodDef methods_wxFileDialogTextCtrl[] = {
    {sipName_GetValue, meth_wxFileDialogTextCtrl_GetValue, METH_VARARGS, doc_wxFileDialogTextCtrl_GetValue},
    {sipName_SetValue, SIP_MLMETH_CAST(meth_wxFileDialogTextCtrl_SetValue), METH_VARARGS|METH_KEYWORDS, doc_wxFileDialogTextCtrl_SetValue}
};

sipVariableDef variables_wxFileDialogTextCtrl[] = {
    {PropertyVariable, sipName_Value, &methods_wxFileDialogTextCtrl[0], &methods_wxFileDialogTextCtrl[1], SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxFileDialogTextCtrl, "Represents a custom text control inside wxFileDialog.");


sipClassTypeDef sipTypeDef__core_wxFileDialogTextCtrl = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxFileDialogTextCtrl,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_FileDialogTextCtrl,
        {0, 0, 1},
        2, methods_wxFileDialogTextCtrl,
        0, SIP_NULLPTR,
        1, variables_wxFileDialogTextCtrl,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxFileDialogTextCtrl,
    -1,
    -1,
    supers_wxFileDialogTextCtrl,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxFileDialogTextCtrl,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxFileDialogTextCtrl,
    cast_wxFileDialogTextCtrl,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    0,
};
