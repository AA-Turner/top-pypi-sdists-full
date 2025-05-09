/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"




extern "C" {static void assign_wxMessageDialogButtonLabel(void *, Py_ssize_t, void *);}
static void assign_wxMessageDialogButtonLabel(void *sipDst, Py_ssize_t sipDstIdx, void *sipSrc)
{
    reinterpret_cast<::wxMessageDialogButtonLabel *>(sipDst)[sipDstIdx] = *reinterpret_cast<::wxMessageDialogButtonLabel *>(sipSrc);
}


extern "C" {static void *array_wxMessageDialogButtonLabel(Py_ssize_t);}
static void *array_wxMessageDialogButtonLabel(Py_ssize_t sipNrElem)
{
    return new ::wxMessageDialogButtonLabel[sipNrElem];
}


extern "C" {static void *copy_wxMessageDialogButtonLabel(const void *, Py_ssize_t);}
static void *copy_wxMessageDialogButtonLabel(const void *sipSrc, Py_ssize_t sipSrcIdx)
{
    return new ::wxMessageDialogButtonLabel(reinterpret_cast<const ::wxMessageDialogButtonLabel *>(sipSrc)[sipSrcIdx]);
}


/* Call the mapped type's destructor. */
extern "C" {static void release_wxMessageDialogButtonLabel(void *, int);}
static void release_wxMessageDialogButtonLabel(void *sipCppV, int)
{
    ::wxMessageDialogButtonLabel *sipCpp = reinterpret_cast<::wxMessageDialogButtonLabel *>(sipCppV);
    Py_BEGIN_ALLOW_THREADS
    delete sipCpp;
    Py_END_ALLOW_THREADS
}



extern "C" {static int convertTo_wxMessageDialogButtonLabel(PyObject *, void **, int *, PyObject *);}
static int convertTo_wxMessageDialogButtonLabel(PyObject *sipPy, void **sipCppPtrV, int *sipIsErr, PyObject *sipTransferObj)
{
    ::wxMessageDialogButtonLabel **sipCppPtr = reinterpret_cast<::wxMessageDialogButtonLabel **>(sipCppPtrV);
        // Code to test a PyObject for compatibility
        if (!sipIsErr) {
            return (PyBytes_Check(sipPy) || PyUnicode_Check(sipPy) || wxPyInt_Check(sipPy));
        }

        // Code to create a new wxMessageDialogButtonLabel from the PyObject
        wxMessageDialogButtonLabel* label;
        if (PyBytes_Check(sipPy))
            label = new wxMessageDialogButtonLabel(PyBytes_AsString(sipPy));
        else if (PyUnicode_Check(sipPy))
            label = new wxMessageDialogButtonLabel(Py2wxString(sipPy));
        else
            label = new wxMessageDialogButtonLabel(wxPyInt_AsLong(sipPy));

        *sipCppPtr = label;
        return sipGetState(sipTransferObj);
}


extern "C" {static PyObject *convertFrom_wxMessageDialogButtonLabel(void *, PyObject *);}
static PyObject *convertFrom_wxMessageDialogButtonLabel(void *sipCppV, PyObject *)
{
    ::wxMessageDialogButtonLabel *sipCpp = reinterpret_cast<::wxMessageDialogButtonLabel *>(sipCppV);
        Py_INCREF(Py_None); return Py_None;
}


sipMappedTypeDef sipTypeDef__core_wxMessageDialogButtonLabel = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_MAPPED,
        sipNameNr_wxMessageDialogButtonLabel,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        -1,
        {0, 0, 1},
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR}
    },
    assign_wxMessageDialogButtonLabel,
    array_wxMessageDialogButtonLabel,
    copy_wxMessageDialogButtonLabel,
    release_wxMessageDialogButtonLabel,
    convertTo_wxMessageDialogButtonLabel,
    convertFrom_wxMessageDialogButtonLabel
};
