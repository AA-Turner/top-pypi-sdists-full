/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        
        
        class wxPointList_iterator {
        public:
            wxPointList_iterator(wxPointList::compatibility_iterator start)
                : m_node(start) {}

            wxPoint* __next__() {
                wxPoint* obj = NULL;
                if (m_node) {
                    obj = (wxPoint*) m_node->GetData();
                    m_node = m_node->GetNext();
                }
                else {
                    PyErr_SetString(PyExc_StopIteration, "");
                }
                return (wxPoint*)obj;
            }
        private:
            wxPointList::compatibility_iterator m_node;
        };
        #include <wx/gdicmn.h>


extern "C" {static PyObject *slot_wxPointList_iterator___iter__(PyObject *);}
static PyObject *slot_wxPointList_iterator___iter__(PyObject *sipSelf)
{
    ::wxPointList_iterator *sipCpp = reinterpret_cast<::wxPointList_iterator *>(sipGetCppPtr((sipSimpleWrapper *)sipSelf, sipType_wxPointList_iterator));

    if (!sipCpp)
        return SIP_NULLPTR;


    {
        {
            PyObject * sipRes = SIP_NULLPTR;
        return PyObject_SelfIter(sipSelf);

            return sipRes;
        }
    }

    return 0;
}


extern "C" {static PyObject *slot_wxPointList_iterator___next__(PyObject *);}
static PyObject *slot_wxPointList_iterator___next__(PyObject *sipSelf)
{
    ::wxPointList_iterator *sipCpp = reinterpret_cast<::wxPointList_iterator *>(sipGetCppPtr((sipSimpleWrapper *)sipSelf, sipType_wxPointList_iterator));

    if (!sipCpp)
        return SIP_NULLPTR;


    {
        {
            ::wxPoint*sipRes = 0;
        sipRes = sipCpp->__next__();
        if (PyErr_Occurred())
            return NULL;

            return sipConvertFromType(sipRes, sipType_wxPoint, SIP_NULLPTR);
        }
    }

    return 0;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxPointList_iterator(void *, int);}
static void release_wxPointList_iterator(void *sipCppV, int)
{
    Py_BEGIN_ALLOW_THREADS

    delete reinterpret_cast<::wxPointList_iterator *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxPointList_iterator(sipSimpleWrapper *);}
static void dealloc_wxPointList_iterator(sipSimpleWrapper *sipSelf)
{
    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxPointList_iterator(sipGetAddress(sipSelf), 0);
    }
}


/* Define this type's Python slots. */
static sipPySlotDef slots_wxPointList_iterator[] = {
    {(void *)slot_wxPointList_iterator___iter__, iter_slot},
    {(void *)slot_wxPointList_iterator___next__, next_slot},
    {0, (sipPySlotType)0}
};


sipClassTypeDef sipTypeDef__core_wxPointList_iterator = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_ABSTRACT|SIP_TYPE_CLASS,
        sipNameNr_wxPointList_iterator,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_PointList_iterator,
        {0, 0, 1},
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    SIP_NULLPTR,
    -1,
    -1,
    SIP_NULLPTR,
    slots_wxPointList_iterator,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxPointList_iterator,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxPointList_iterator,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    0,
};
