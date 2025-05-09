/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/dragimag.h>
        #include <wx/bitmap.h>
        #include <wx/cursor.h>
        #include <wx/icon.h>
        #include <wx/treectrl.h>
        #include <wx/treebase.h>
        #include <wx/listctrl.h>
        #include <wx/gdicmn.h>
        #include <wx/window.h>
        #include <wx/gdicmn.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


PyDoc_STRVAR(doc_wxDragImage_BeginDrag, "BeginDrag(hotspot, window, fullScreen=False, rect=None) -> bool\n"
"BeginDrag(hotspot, window, boundingWindow) -> bool\n"
"\n"
"Start dragging the image, in a window or full screen.\n"
"");

extern "C" {static PyObject *meth_wxDragImage_BeginDrag(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxDragImage_BeginDrag(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPoint* hotspot;
        int hotspotState = 0;
        ::wxWindow* window;
        bool fullScreen = 0;
        ::wxRect* rect = 0;
        int rectState = 0;
        ::wxDragImage *sipCpp;

        static const char *sipKwdList[] = {
            sipName_hotspot,
            sipName_window,
            sipName_fullScreen,
            sipName_rect,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1J8|bJ0", &sipSelf, sipType_wxDragImage, &sipCpp, sipType_wxPoint, &hotspot, &hotspotState, sipType_wxWindow, &window, &fullScreen, sipType_wxRect, &rect, &rectState))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->BeginDrag(*hotspot, window, fullScreen, rect);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxPoint *>(hotspot), sipType_wxPoint, hotspotState);
            sipReleaseType(rect, sipType_wxRect, rectState);

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    {
        const ::wxPoint* hotspot;
        int hotspotState = 0;
        ::wxWindow* window;
        ::wxWindow* boundingWindow;
        ::wxDragImage *sipCpp;

        static const char *sipKwdList[] = {
            sipName_hotspot,
            sipName_window,
            sipName_boundingWindow,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1J8J8", &sipSelf, sipType_wxDragImage, &sipCpp, sipType_wxPoint, &hotspot, &hotspotState, sipType_wxWindow, &window, sipType_wxWindow, &boundingWindow))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->BeginDrag(*hotspot, window, boundingWindow);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxPoint *>(hotspot), sipType_wxPoint, hotspotState);

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_DragImage, sipName_BeginDrag, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxDragImage_EndDrag, "EndDrag() -> bool\n"
"\n"
"Call this when the drag has finished.");

extern "C" {static PyObject *meth_wxDragImage_EndDrag(PyObject *, PyObject *);}
static PyObject *meth_wxDragImage_EndDrag(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxDragImage *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxDragImage, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->EndDrag();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_DragImage, sipName_EndDrag, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxDragImage_Hide, "Hide() -> bool\n"
"\n"
"Hides the image.");

extern "C" {static PyObject *meth_wxDragImage_Hide(PyObject *, PyObject *);}
static PyObject *meth_wxDragImage_Hide(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxDragImage *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxDragImage, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->Hide();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_DragImage, sipName_Hide, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxDragImage_Move, "Move(pt) -> bool\n"
"\n"
"Call this to move the image to a new position.");

extern "C" {static PyObject *meth_wxDragImage_Move(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxDragImage_Move(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPoint* pt;
        int ptState = 0;
        ::wxDragImage *sipCpp;

        static const char *sipKwdList[] = {
            sipName_pt,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxDragImage, &sipCpp, sipType_wxPoint, &pt, &ptState))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->Move(*pt);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxPoint *>(pt), sipType_wxPoint, ptState);

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_DragImage, sipName_Move, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxDragImage_Show, "Show() -> bool\n"
"\n"
"Shows the image.");

extern "C" {static PyObject *meth_wxDragImage_Show(PyObject *, PyObject *);}
static PyObject *meth_wxDragImage_Show(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxDragImage *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxDragImage, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->Show();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_DragImage, sipName_Show, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxDragImage(void *, const sipTypeDef *);}
static void *cast_wxDragImage(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxDragImage *sipCpp = reinterpret_cast<::wxDragImage *>(sipCppV);

    if (targetType == sipType_wxDragImage)
        return sipCppV;

    if (targetType == sipType_wxObject)
        return static_cast<::wxObject *>(sipCpp);

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxDragImage(void *, int);}
static void release_wxDragImage(void *sipCppV, int)
{
    Py_BEGIN_ALLOW_THREADS

    delete reinterpret_cast<::wxDragImage *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxDragImage(Py_ssize_t);}
static void *array_wxDragImage(Py_ssize_t sipNrElem)
{
    return new ::wxDragImage[sipNrElem];
}


extern "C" {static void array_delete_wxDragImage(void *);}
static void array_delete_wxDragImage(void *sipCpp)
{
    delete[] reinterpret_cast<::wxDragImage *>(sipCpp);
}


extern "C" {static void dealloc_wxDragImage(sipSimpleWrapper *);}
static void dealloc_wxDragImage(sipSimpleWrapper *sipSelf)
{
    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxDragImage(sipGetAddress(sipSelf), 0);
    }
}


extern "C" {static void *init_type_wxDragImage(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxDragImage(sipSimpleWrapper *, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    ::wxDragImage *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxDragImage();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            return sipCpp;
        }
    }

    {
        const ::wxBitmap* image;
        const ::wxCursor& cursordef = wxNullCursor;
        const ::wxCursor* cursor = &cursordef;

        static const char *sipKwdList[] = {
            sipName_image,
            sipName_cursor,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J9|J9", sipType_wxBitmap, &image, sipType_wxCursor, &cursor))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxDragImage(*image, *cursor);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            return sipCpp;
        }
    }

    {
        const ::wxIcon* image;
        const ::wxCursor& cursordef = wxNullCursor;
        const ::wxCursor* cursor = &cursordef;

        static const char *sipKwdList[] = {
            sipName_image,
            sipName_cursor,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J9|J9", sipType_wxIcon, &image, sipType_wxCursor, &cursor))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxDragImage(*image, *cursor);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            return sipCpp;
        }
    }

    {
        const ::wxString* text;
        int textState = 0;
        const ::wxCursor& cursordef = wxNullCursor;
        const ::wxCursor* cursor = &cursordef;

        static const char *sipKwdList[] = {
            sipName_text,
            sipName_cursor,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J1|J9", sipType_wxString, &text, &textState, sipType_wxCursor, &cursor))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxDragImage(*text, *cursor);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxString *>(text), sipType_wxString, textState);

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            return sipCpp;
        }
    }

    {
        const ::wxTreeCtrl* treeCtrl;
        ::wxTreeItemId* id;

        static const char *sipKwdList[] = {
            sipName_treeCtrl,
            sipName_id,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J9J9", sipType_wxTreeCtrl, &treeCtrl, sipType_wxTreeItemId, &id))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxDragImage(*treeCtrl, *id);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            return sipCpp;
        }
    }

    {
        const ::wxListCtrl* listCtrl;
        long id;

        static const char *sipKwdList[] = {
            sipName_listCtrl,
            sipName_id,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J9l", sipType_wxListCtrl, &listCtrl, &id))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxDragImage(*listCtrl, id);
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


/* Define this type's super-types. */
static sipEncodedTypeDef supers_wxDragImage[] = {{392, 255, 1}};


static PyMethodDef methods_wxDragImage[] = {
    {sipName_BeginDrag, SIP_MLMETH_CAST(meth_wxDragImage_BeginDrag), METH_VARARGS|METH_KEYWORDS, doc_wxDragImage_BeginDrag},
    {sipName_EndDrag, meth_wxDragImage_EndDrag, METH_VARARGS, doc_wxDragImage_EndDrag},
    {sipName_Hide, meth_wxDragImage_Hide, METH_VARARGS, doc_wxDragImage_Hide},
    {sipName_Move, SIP_MLMETH_CAST(meth_wxDragImage_Move), METH_VARARGS|METH_KEYWORDS, doc_wxDragImage_Move},
    {sipName_Show, meth_wxDragImage_Show, METH_VARARGS, doc_wxDragImage_Show}
};

PyDoc_STRVAR(doc_wxDragImage, "DragImage() -> None\n"
"DragImage(image, cursor=NullCursor) -> None\n"
"DragImage(image, cursor=NullCursor) -> None\n"
"DragImage(text, cursor=NullCursor) -> None\n"
"DragImage(treeCtrl, id) -> None\n"
"DragImage(listCtrl, id) -> None\n"
"\n"
"This class is used when you wish to drag an object on the screen, and\n"
"a simple cursor is not enough.");


sipClassTypeDef sipTypeDef__core_wxDragImage = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxDragImage,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_DragImage,
        {0, 0, 1},
        5, methods_wxDragImage,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxDragImage,
    -1,
    -1,
    supers_wxDragImage,
    SIP_NULLPTR,
    init_type_wxDragImage,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxDragImage,
    SIP_NULLPTR,
    array_wxDragImage,
    SIP_NULLPTR,
    release_wxDragImage,
    cast_wxDragImage,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxDragImage,
    sizeof (::wxDragImage),
};
