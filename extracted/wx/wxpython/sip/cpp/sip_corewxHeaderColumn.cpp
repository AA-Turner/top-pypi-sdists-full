/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/headercol.h>
        #include <wx/bmpbndl.h>
        #include <wx/bitmap.h>


class sipwxHeaderColumn : public ::wxHeaderColumn
{
public:
    sipwxHeaderColumn();
    sipwxHeaderColumn(const ::wxHeaderColumn&);
    virtual ~sipwxHeaderColumn();

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    bool IsSortOrderAscending() const SIP_OVERRIDE;
    bool IsSortKey() const SIP_OVERRIDE;
    bool IsHidden() const SIP_OVERRIDE;
    bool IsReorderable() const SIP_OVERRIDE;
    bool IsSortable() const SIP_OVERRIDE;
    bool IsResizeable() const SIP_OVERRIDE;
    int GetFlags() const SIP_OVERRIDE;
    ::wxAlignment GetAlignment() const SIP_OVERRIDE;
    int GetMinWidth() const SIP_OVERRIDE;
    int GetWidth() const SIP_OVERRIDE;
    ::wxBitmapBundle GetBitmapBundle() const SIP_OVERRIDE;
    ::wxBitmap GetBitmap() const SIP_OVERRIDE;
    ::wxString GetTitle() const SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxHeaderColumn(const sipwxHeaderColumn &);
    sipwxHeaderColumn &operator = (const sipwxHeaderColumn &);

    char sipPyMethods[13];
};

sipwxHeaderColumn::sipwxHeaderColumn(): ::wxHeaderColumn(), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxHeaderColumn::sipwxHeaderColumn(const ::wxHeaderColumn& a0): ::wxHeaderColumn(a0), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxHeaderColumn::~sipwxHeaderColumn()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

bool sipwxHeaderColumn::IsSortOrderAscending() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[0]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_IsSortOrderAscending);

    if (!sipMeth)
        return 0;

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxHeaderColumn::IsSortKey() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[1]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_IsSortKey);

    if (!sipMeth)
        return 0;

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxHeaderColumn::IsHidden() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[2]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_IsHidden);

    if (!sipMeth)
        return ::wxHeaderColumn::IsHidden();

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxHeaderColumn::IsReorderable() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[3]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_IsReorderable);

    if (!sipMeth)
        return ::wxHeaderColumn::IsReorderable();

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxHeaderColumn::IsSortable() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[4]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_IsSortable);

    if (!sipMeth)
        return ::wxHeaderColumn::IsSortable();

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxHeaderColumn::IsResizeable() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[5]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_IsResizeable);

    if (!sipMeth)
        return ::wxHeaderColumn::IsResizeable();

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

int sipwxHeaderColumn::GetFlags() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[6]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_GetFlags);

    if (!sipMeth)
        return 0;

    extern int sipVH__core_112(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_112(sipGILState, 0, sipPySelf, sipMeth);
}

::wxAlignment sipwxHeaderColumn::GetAlignment() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[7]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_GetAlignment);

    if (!sipMeth)
        return ::wxALIGN_INVALID;

    extern ::wxAlignment sipVH__core_166(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_166(sipGILState, 0, sipPySelf, sipMeth);
}

int sipwxHeaderColumn::GetMinWidth() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[8]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_GetMinWidth);

    if (!sipMeth)
        return 0;

    extern int sipVH__core_112(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_112(sipGILState, 0, sipPySelf, sipMeth);
}

int sipwxHeaderColumn::GetWidth() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[9]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_GetWidth);

    if (!sipMeth)
        return 0;

    extern int sipVH__core_112(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_112(sipGILState, 0, sipPySelf, sipMeth);
}

::wxBitmapBundle sipwxHeaderColumn::GetBitmapBundle() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[10]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetBitmapBundle);

    if (!sipMeth)
        return ::wxHeaderColumn::GetBitmapBundle();

    extern ::wxBitmapBundle sipVH__core_165(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_165(sipGILState, 0, sipPySelf, sipMeth);
}

::wxBitmap sipwxHeaderColumn::GetBitmap() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[11]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_GetBitmap);

    if (!sipMeth)
        return ::wxBitmap();

    extern ::wxBitmap sipVH__core_80(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_80(sipGILState, 0, sipPySelf, sipMeth);
}

::wxString sipwxHeaderColumn::GetTitle() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[12]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_HeaderColumn, sipName_GetTitle);

    if (!sipMeth)
        return ::wxString();

    extern ::wxString sipVH__core_11(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_11(sipGILState, 0, sipPySelf, sipMeth);
}


PyDoc_STRVAR(doc_wxHeaderColumn_GetTitle, "GetTitle() -> str\n"
"\n"
"Get the text shown in the column header.");

extern "C" {static PyObject *meth_wxHeaderColumn_GetTitle(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_GetTitle(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            ::wxString*sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_GetTitle);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxString(sipCpp->GetTitle());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxString, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_GetTitle, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_GetBitmap, "GetBitmap() -> Bitmap\n"
"\n"
"This function exists only for backwards compatibility, it's\n"
"recommended to override GetBitmapBundle() in the new code and override\n"
"this one to do nothing, as it will never be called if\n"
"GetBitmapBundle() is overridden.");

extern "C" {static PyObject *meth_wxHeaderColumn_GetBitmap(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_GetBitmap(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            ::wxBitmap*sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_GetBitmap);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxBitmap(sipCpp->GetBitmap());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxBitmap, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_GetBitmap, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_GetBitmapBundle, "GetBitmapBundle() -> BitmapBundle\n"
"\n"
"Returns the bitmap in the header of the column, if any.");

extern "C" {static PyObject *meth_wxHeaderColumn_GetBitmapBundle(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_GetBitmapBundle(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            ::wxBitmapBundle*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxBitmapBundle((sipSelfWasArg ? sipCpp->::wxHeaderColumn::GetBitmapBundle() : sipCpp->GetBitmapBundle()));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxBitmapBundle, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_GetBitmapBundle, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_GetWidth, "GetWidth() -> int\n"
"\n"
"Returns the current width of the column.");

extern "C" {static PyObject *meth_wxHeaderColumn_GetWidth(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_GetWidth(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            int sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_GetWidth);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetWidth();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_GetWidth, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_GetMinWidth, "GetMinWidth() -> int\n"
"\n"
"Return the minimal column width.");

extern "C" {static PyObject *meth_wxHeaderColumn_GetMinWidth(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_GetMinWidth(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            int sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_GetMinWidth);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetMinWidth();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_GetMinWidth, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_GetAlignment, "GetAlignment() -> Alignment\n"
"\n"
"Returns the current column alignment.");

extern "C" {static PyObject *meth_wxHeaderColumn_GetAlignment(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_GetAlignment(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            ::wxAlignment sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_GetAlignment);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetAlignment();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxAlignment);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_GetAlignment, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_GetFlags, "GetFlags() -> int\n"
"\n"
"Get the column flags.");

extern "C" {static PyObject *meth_wxHeaderColumn_GetFlags(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_GetFlags(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            int sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_GetFlags);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetFlags();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_GetFlags, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_HasFlag, "HasFlag(flag) -> bool\n"
"\n"
"Return true if the specified flag is currently set for this column.");

extern "C" {static PyObject *meth_wxHeaderColumn_HasFlag(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_HasFlag(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        int flag;
        const ::wxHeaderColumn *sipCpp;

        static const char *sipKwdList[] = {
            sipName_flag,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bi", &sipSelf, sipType_wxHeaderColumn, &sipCpp, &flag))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->HasFlag(flag);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_HasFlag, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_IsResizeable, "IsResizeable() -> bool\n"
"\n"
"Return true if the column can be resized by the user.");

extern "C" {static PyObject *meth_wxHeaderColumn_IsResizeable(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_IsResizeable(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxHeaderColumn::IsResizeable() : sipCpp->IsResizeable());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_IsResizeable, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_IsSortable, "IsSortable() -> bool\n"
"\n"
"Returns true if the column can be clicked by user to sort the control\n"
"contents by the field in this column.");

extern "C" {static PyObject *meth_wxHeaderColumn_IsSortable(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_IsSortable(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxHeaderColumn::IsSortable() : sipCpp->IsSortable());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_IsSortable, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_IsReorderable, "IsReorderable() -> bool\n"
"\n"
"Returns true if the column can be dragged by user to change its order.");

extern "C" {static PyObject *meth_wxHeaderColumn_IsReorderable(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_IsReorderable(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxHeaderColumn::IsReorderable() : sipCpp->IsReorderable());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_IsReorderable, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_IsHidden, "IsHidden() -> bool\n"
"\n"
"Returns true if the column is currently hidden.");

extern "C" {static PyObject *meth_wxHeaderColumn_IsHidden(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_IsHidden(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxHeaderColumn::IsHidden() : sipCpp->IsHidden());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_IsHidden, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_IsShown, "IsShown() -> bool\n"
"\n"
"Returns true if the column is currently shown.");

extern "C" {static PyObject *meth_wxHeaderColumn_IsShown(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_IsShown(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->IsShown();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_IsShown, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_IsSortKey, "IsSortKey() -> bool\n"
"\n"
"Returns true if the column is currently used for sorting.");

extern "C" {static PyObject *meth_wxHeaderColumn_IsSortKey(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_IsSortKey(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            bool sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_IsSortKey);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->IsSortKey();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_IsSortKey, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxHeaderColumn_IsSortOrderAscending, "IsSortOrderAscending() -> bool\n"
"\n"
"Returns true, if the sort order is ascending.");

extern "C" {static PyObject *meth_wxHeaderColumn_IsSortOrderAscending(PyObject *, PyObject *);}
static PyObject *meth_wxHeaderColumn_IsSortOrderAscending(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxHeaderColumn *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxHeaderColumn, &sipCpp))
        {
            bool sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_HeaderColumn, sipName_IsSortOrderAscending);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->IsSortOrderAscending();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_HeaderColumn, sipName_IsSortOrderAscending, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxHeaderColumn(void *, int);}
static void release_wxHeaderColumn(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxHeaderColumn *>(sipCppV);
    else
        delete reinterpret_cast<::wxHeaderColumn *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxHeaderColumn(sipSimpleWrapper *);}
static void dealloc_wxHeaderColumn(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxHeaderColumn *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxHeaderColumn(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxHeaderColumn(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxHeaderColumn(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxHeaderColumn *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxHeaderColumn();
            Py_END_ALLOW_THREADS

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    {
        const ::wxHeaderColumn* a0;

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, "J9", sipType_wxHeaderColumn, &a0))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxHeaderColumn(*a0);
            Py_END_ALLOW_THREADS

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}


static PyMethodDef methods_wxHeaderColumn[] = {
    {sipName_GetAlignment, meth_wxHeaderColumn_GetAlignment, METH_VARARGS, doc_wxHeaderColumn_GetAlignment},
    {sipName_GetBitmap, meth_wxHeaderColumn_GetBitmap, METH_VARARGS, doc_wxHeaderColumn_GetBitmap},
    {sipName_GetBitmapBundle, meth_wxHeaderColumn_GetBitmapBundle, METH_VARARGS, doc_wxHeaderColumn_GetBitmapBundle},
    {sipName_GetFlags, meth_wxHeaderColumn_GetFlags, METH_VARARGS, doc_wxHeaderColumn_GetFlags},
    {sipName_GetMinWidth, meth_wxHeaderColumn_GetMinWidth, METH_VARARGS, doc_wxHeaderColumn_GetMinWidth},
    {sipName_GetTitle, meth_wxHeaderColumn_GetTitle, METH_VARARGS, doc_wxHeaderColumn_GetTitle},
    {sipName_GetWidth, meth_wxHeaderColumn_GetWidth, METH_VARARGS, doc_wxHeaderColumn_GetWidth},
    {sipName_HasFlag, SIP_MLMETH_CAST(meth_wxHeaderColumn_HasFlag), METH_VARARGS|METH_KEYWORDS, doc_wxHeaderColumn_HasFlag},
    {sipName_IsHidden, meth_wxHeaderColumn_IsHidden, METH_VARARGS, doc_wxHeaderColumn_IsHidden},
    {sipName_IsReorderable, meth_wxHeaderColumn_IsReorderable, METH_VARARGS, doc_wxHeaderColumn_IsReorderable},
    {sipName_IsResizeable, meth_wxHeaderColumn_IsResizeable, METH_VARARGS, doc_wxHeaderColumn_IsResizeable},
    {sipName_IsShown, meth_wxHeaderColumn_IsShown, METH_VARARGS, doc_wxHeaderColumn_IsShown},
    {sipName_IsSortKey, meth_wxHeaderColumn_IsSortKey, METH_VARARGS, doc_wxHeaderColumn_IsSortKey},
    {sipName_IsSortOrderAscending, meth_wxHeaderColumn_IsSortOrderAscending, METH_VARARGS, doc_wxHeaderColumn_IsSortOrderAscending},
    {sipName_IsSortable, meth_wxHeaderColumn_IsSortable, METH_VARARGS, doc_wxHeaderColumn_IsSortable}
};

sipVariableDef variables_wxHeaderColumn[] = {
    {PropertyVariable, sipName_SortKey, &methods_wxHeaderColumn[12], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_SortOrderAscending, &methods_wxHeaderColumn[13], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Shown, &methods_wxHeaderColumn[11], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Hidden, &methods_wxHeaderColumn[8], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Reorderable, &methods_wxHeaderColumn[9], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Sortable, &methods_wxHeaderColumn[14], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Resizeable, &methods_wxHeaderColumn[10], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Width, &methods_wxHeaderColumn[6], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Title, &methods_wxHeaderColumn[5], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_MinWidth, &methods_wxHeaderColumn[4], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Flags, &methods_wxHeaderColumn[3], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_BitmapBundle, &methods_wxHeaderColumn[2], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Bitmap, &methods_wxHeaderColumn[1], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Alignment, &methods_wxHeaderColumn[0], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxHeaderColumn, "Represents a column header in controls displaying tabular data such as\n"
"wxDataViewCtrl or wxGrid.");


sipClassTypeDef sipTypeDef__core_wxHeaderColumn = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_ABSTRACT|SIP_TYPE_CLASS,
        sipNameNr_wxHeaderColumn,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_HeaderColumn,
        {0, 0, 1},
        15, methods_wxHeaderColumn,
        0, SIP_NULLPTR,
        14, variables_wxHeaderColumn,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxHeaderColumn,
    -1,
    -1,
    SIP_NULLPTR,
    SIP_NULLPTR,
    init_type_wxHeaderColumn,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxHeaderColumn,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxHeaderColumn,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    sizeof (::wxHeaderColumn),
};
