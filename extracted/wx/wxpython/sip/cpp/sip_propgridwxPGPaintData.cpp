/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_propgrid.h"
        #include <wx/propgrid/property.h>
        #include <wx/propgrid/propgrid.h>


/* Call the instance's destructor. */
extern "C" {static void release_wxPGPaintData(void *, int);}
static void release_wxPGPaintData(void *sipCppV, int)
{
    Py_BEGIN_ALLOW_THREADS

    delete reinterpret_cast<::wxPGPaintData *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxPGPaintData(Py_ssize_t);}
static void *array_wxPGPaintData(Py_ssize_t sipNrElem)
{
    return new ::wxPGPaintData[sipNrElem];
}


extern "C" {static void array_delete_wxPGPaintData(void *);}
static void array_delete_wxPGPaintData(void *sipCpp)
{
    delete[] reinterpret_cast<::wxPGPaintData *>(sipCpp);
}


extern "C" {static void assign_wxPGPaintData(void *, Py_ssize_t, void *);}
static void assign_wxPGPaintData(void *sipDst, Py_ssize_t sipDstIdx, void *sipSrc)
{
    reinterpret_cast<::wxPGPaintData *>(sipDst)[sipDstIdx] = *reinterpret_cast<::wxPGPaintData *>(sipSrc);
}


extern "C" {static void *copy_wxPGPaintData(const void *, Py_ssize_t);}
static void *copy_wxPGPaintData(const void *sipSrc, Py_ssize_t sipSrcIdx)
{
    return new ::wxPGPaintData(reinterpret_cast<const ::wxPGPaintData *>(sipSrc)[sipSrcIdx]);
}


extern "C" {static void dealloc_wxPGPaintData(sipSimpleWrapper *);}
static void dealloc_wxPGPaintData(sipSimpleWrapper *sipSelf)
{
    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxPGPaintData(sipGetAddress(sipSelf), 0);
    }
}


extern "C" {static void *init_type_wxPGPaintData(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxPGPaintData(sipSimpleWrapper *, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    ::wxPGPaintData *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxPGPaintData();
            Py_END_ALLOW_THREADS

            return sipCpp;
        }
    }

    {
        const ::wxPGPaintData* a0;

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, "J9", sipType_wxPGPaintData, &a0))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxPGPaintData(*a0);
            Py_END_ALLOW_THREADS

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}


extern "C" {static PyObject *varget_wxPGPaintData_m_choiceItem(void *, PyObject *, PyObject *);}
static PyObject *varget_wxPGPaintData_m_choiceItem(void *sipSelf, PyObject *, PyObject *)
{
    int sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    sipVal = sipCpp->m_choiceItem;

    return PyLong_FromLong(sipVal);
}


extern "C" {static int varset_wxPGPaintData_m_choiceItem(void *, PyObject *, PyObject *);}
static int varset_wxPGPaintData_m_choiceItem(void *sipSelf, PyObject *sipPy, PyObject *)
{
    int sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    sipVal = sipLong_AsInt(sipPy);

    if (PyErr_Occurred() != SIP_NULLPTR)
        return -1;

    sipCpp->m_choiceItem = sipVal;

    return 0;
}


extern "C" {static PyObject *varget_wxPGPaintData_m_drawnHeight(void *, PyObject *, PyObject *);}
static PyObject *varget_wxPGPaintData_m_drawnHeight(void *sipSelf, PyObject *, PyObject *)
{
    int sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    sipVal = sipCpp->m_drawnHeight;

    return PyLong_FromLong(sipVal);
}


extern "C" {static int varset_wxPGPaintData_m_drawnHeight(void *, PyObject *, PyObject *);}
static int varset_wxPGPaintData_m_drawnHeight(void *sipSelf, PyObject *sipPy, PyObject *)
{
    int sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    sipVal = sipLong_AsInt(sipPy);

    if (PyErr_Occurred() != SIP_NULLPTR)
        return -1;

    sipCpp->m_drawnHeight = sipVal;

    return 0;
}


extern "C" {static PyObject *varget_wxPGPaintData_m_drawnWidth(void *, PyObject *, PyObject *);}
static PyObject *varget_wxPGPaintData_m_drawnWidth(void *sipSelf, PyObject *, PyObject *)
{
    int sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    sipVal = sipCpp->m_drawnWidth;

    return PyLong_FromLong(sipVal);
}


extern "C" {static int varset_wxPGPaintData_m_drawnWidth(void *, PyObject *, PyObject *);}
static int varset_wxPGPaintData_m_drawnWidth(void *sipSelf, PyObject *sipPy, PyObject *)
{
    int sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    sipVal = sipLong_AsInt(sipPy);

    if (PyErr_Occurred() != SIP_NULLPTR)
        return -1;

    sipCpp->m_drawnWidth = sipVal;

    return 0;
}


extern "C" {static PyObject *varget_wxPGPaintData_m_parent(void *, PyObject *, PyObject *);}
static PyObject *varget_wxPGPaintData_m_parent(void *sipSelf, PyObject *, PyObject *)
{
    const ::wxPropertyGrid*sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    sipVal = sipCpp->m_parent;

    return sipConvertFromType(const_cast<::wxPropertyGrid *>(sipVal), sipType_wxPropertyGrid, SIP_NULLPTR);
}


extern "C" {static int varset_wxPGPaintData_m_parent(void *, PyObject *, PyObject *);}
static int varset_wxPGPaintData_m_parent(void *sipSelf, PyObject *sipPy, PyObject *)
{
    const ::wxPropertyGrid*sipVal;
    ::wxPGPaintData *sipCpp = reinterpret_cast<::wxPGPaintData *>(sipSelf);

    int sipIsErr = 0;
    sipVal = reinterpret_cast<::wxPropertyGrid *>(sipForceConvertToType(sipPy, sipType_wxPropertyGrid, SIP_NULLPTR, 0, SIP_NULLPTR, &sipIsErr));

    if (sipIsErr)
        return -1;

    sipCpp->m_parent = sipVal;

    return 0;
}

sipVariableDef variables_wxPGPaintData[] = {
    {InstanceVariable, sipName_m_choiceItem, (PyMethodDef *)varget_wxPGPaintData_m_choiceItem, (PyMethodDef *)varset_wxPGPaintData_m_choiceItem, SIP_NULLPTR, SIP_NULLPTR},
    {InstanceVariable, sipName_m_drawnHeight, (PyMethodDef *)varget_wxPGPaintData_m_drawnHeight, (PyMethodDef *)varset_wxPGPaintData_m_drawnHeight, SIP_NULLPTR, SIP_NULLPTR},
    {InstanceVariable, sipName_m_drawnWidth, (PyMethodDef *)varget_wxPGPaintData_m_drawnWidth, (PyMethodDef *)varset_wxPGPaintData_m_drawnWidth, SIP_NULLPTR, SIP_NULLPTR},
    {InstanceVariable, sipName_m_parent, (PyMethodDef *)varget_wxPGPaintData_m_parent, (PyMethodDef *)varset_wxPGPaintData_m_parent, SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxPGPaintData, "Contains information related to property's OnCustomPaint.");


sipClassTypeDef sipTypeDef__propgrid_wxPGPaintData = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_CLASS,
        sipNameNr_wxPGPaintData,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_PGPaintData,
        {0, 0, 1},
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        4, variables_wxPGPaintData,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxPGPaintData,
    -1,
    -1,
    SIP_NULLPTR,
    SIP_NULLPTR,
    init_type_wxPGPaintData,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxPGPaintData,
    assign_wxPGPaintData,
    array_wxPGPaintData,
    copy_wxPGPaintData,
    release_wxPGPaintData,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxPGPaintData,
    sizeof (::wxPGPaintData),
};
