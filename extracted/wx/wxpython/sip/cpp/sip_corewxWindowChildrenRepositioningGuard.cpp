/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/window.h>
            #include <wx/window.h>
        #include <wx/window.h>


/* Call the instance's destructor. */
extern "C" {static void release_wxWindow_ChildrenRepositioningGuard(void *, int);}
static void release_wxWindow_ChildrenRepositioningGuard(void *sipCppV, int)
{
    Py_BEGIN_ALLOW_THREADS

    delete reinterpret_cast<::wxWindow::ChildrenRepositioningGuard *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxWindow_ChildrenRepositioningGuard(sipSimpleWrapper *);}
static void dealloc_wxWindow_ChildrenRepositioningGuard(sipSimpleWrapper *sipSelf)
{
    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxWindow_ChildrenRepositioningGuard(sipGetAddress(sipSelf), 0);
    }
}


extern "C" {static void *init_type_wxWindow_ChildrenRepositioningGuard(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxWindow_ChildrenRepositioningGuard(sipSimpleWrapper *, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    ::wxWindow::ChildrenRepositioningGuard *sipCpp = SIP_NULLPTR;

    {
        ::wxWindow* win;

        static const char *sipKwdList[] = {
            sipName_win,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J8", sipType_wxWindow, &win))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxWindow::ChildrenRepositioningGuard(win);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}

PyDoc_STRVAR(doc_wxWindow_ChildrenRepositioningGuard, "ChildrenRepositioningGuard(win) -> None\n"
"\n"
"Helper for ensuring EndRepositioningChildren() is called correctly.");


sipClassTypeDef sipTypeDef__core_wxWindow_ChildrenRepositioningGuard = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_CLASS,
        sipNameNr_wxWindow__ChildrenRepositioningGuard,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_ChildrenRepositioningGuard,
        {631, 255, 0},
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxWindow_ChildrenRepositioningGuard,
    -1,
    -1,
    SIP_NULLPTR,
    SIP_NULLPTR,
    init_type_wxWindow_ChildrenRepositioningGuard,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxWindow_ChildrenRepositioningGuard,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxWindow_ChildrenRepositioningGuard,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    sizeof (::wxWindow::ChildrenRepositioningGuard),
};
