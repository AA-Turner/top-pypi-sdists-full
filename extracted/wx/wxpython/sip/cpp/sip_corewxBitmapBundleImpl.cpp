/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/bmpbndl.h>
        #include <wx/gdicmn.h>
        #include <wx/bitmap.h>


class sipwxBitmapBundleImpl : public ::wxBitmapBundleImpl
{
public:
    sipwxBitmapBundleImpl();
    virtual ~sipwxBitmapBundleImpl();

    /*
     * There is a public method for every protected method visible from
     * this class.
     */
    ::wxSize sipProtect_DoGetPreferredSize(double) const;
    size_t sipProtect_GetIndexToUpscale(const ::wxSize&) const;
    double sipProtectVirt_GetNextAvailableScale(bool, size_t&) const;

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    double GetNextAvailableScale(size_t&) const SIP_OVERRIDE;
    ::wxBitmap GetBitmap(const ::wxSize&) SIP_OVERRIDE;
    ::wxSize GetPreferredBitmapSizeAtScale(double) const SIP_OVERRIDE;
    ::wxSize GetDefaultSize() const SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxBitmapBundleImpl(const sipwxBitmapBundleImpl &);
    sipwxBitmapBundleImpl &operator = (const sipwxBitmapBundleImpl &);

    char sipPyMethods[4];
};

sipwxBitmapBundleImpl::sipwxBitmapBundleImpl(): ::wxBitmapBundleImpl(), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxBitmapBundleImpl::~sipwxBitmapBundleImpl()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

double sipwxBitmapBundleImpl::GetNextAvailableScale(size_t& idx) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[0]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetNextAvailableScale);

    if (!sipMeth)
        return ::wxBitmapBundleImpl::GetNextAvailableScale(idx);

    extern double sipVH__core_28(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, size_t&);

    return sipVH__core_28(sipGILState, 0, sipPySelf, sipMeth, idx);
}

::wxBitmap sipwxBitmapBundleImpl::GetBitmap(const ::wxSize& size)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[1], &sipPySelf, sipName_BitmapBundleImpl, sipName_GetBitmap);

    if (!sipMeth)
        return ::wxBitmap();

    extern ::wxBitmap sipVH__core_27(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxSize&);

    return sipVH__core_27(sipGILState, 0, sipPySelf, sipMeth, size);
}

::wxSize sipwxBitmapBundleImpl::GetPreferredBitmapSizeAtScale(double scale) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[2]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_BitmapBundleImpl, sipName_GetPreferredBitmapSizeAtScale);

    if (!sipMeth)
        return ::wxSize();

    extern ::wxSize sipVH__core_26(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, double);

    return sipVH__core_26(sipGILState, 0, sipPySelf, sipMeth, scale);
}

::wxSize sipwxBitmapBundleImpl::GetDefaultSize() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[3]), const_cast<sipSimpleWrapper **>(&sipPySelf), sipName_BitmapBundleImpl, sipName_GetDefaultSize);

    if (!sipMeth)
        return ::wxSize();

    extern ::wxSize sipVH__core_25(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_25(sipGILState, 0, sipPySelf, sipMeth);
}

::wxSize sipwxBitmapBundleImpl::sipProtect_DoGetPreferredSize(double scale) const
{
    return ::wxBitmapBundleImpl::DoGetPreferredSize(scale);
}

size_t sipwxBitmapBundleImpl::sipProtect_GetIndexToUpscale(const ::wxSize& size) const
{
    return ::wxBitmapBundleImpl::GetIndexToUpscale(size);
}

double sipwxBitmapBundleImpl::sipProtectVirt_GetNextAvailableScale(bool sipSelfWasArg, size_t& idx) const
{
    return (sipSelfWasArg ? ::wxBitmapBundleImpl::GetNextAvailableScale(idx) : GetNextAvailableScale(idx));
}


PyDoc_STRVAR(doc_wxBitmapBundleImpl_GetDefaultSize, "GetDefaultSize() -> Size\n"
"\n"
"Return the size of the bitmaps represented by this bundle in the\n"
"default DPI.");

extern "C" {static PyObject *meth_wxBitmapBundleImpl_GetDefaultSize(PyObject *, PyObject *);}
static PyObject *meth_wxBitmapBundleImpl_GetDefaultSize(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxBitmapBundleImpl *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxBitmapBundleImpl, &sipCpp))
        {
            ::wxSize*sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_BitmapBundleImpl, sipName_GetDefaultSize);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxSize(sipCpp->GetDefaultSize());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxSize, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_BitmapBundleImpl, sipName_GetDefaultSize, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxBitmapBundleImpl_GetPreferredBitmapSizeAtScale, "GetPreferredBitmapSizeAtScale(scale) -> Size\n"
"\n"
"Return the preferred size that should be used at the given scale.");

extern "C" {static PyObject *meth_wxBitmapBundleImpl_GetPreferredBitmapSizeAtScale(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxBitmapBundleImpl_GetPreferredBitmapSizeAtScale(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        double scale;
        const ::wxBitmapBundleImpl *sipCpp;

        static const char *sipKwdList[] = {
            sipName_scale,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bd", &sipSelf, sipType_wxBitmapBundleImpl, &sipCpp, &scale))
        {
            ::wxSize*sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_BitmapBundleImpl, sipName_GetPreferredBitmapSizeAtScale);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxSize(sipCpp->GetPreferredBitmapSizeAtScale(scale));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxSize, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_BitmapBundleImpl, sipName_GetPreferredBitmapSizeAtScale, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxBitmapBundleImpl_GetBitmap, "GetBitmap(size) -> Bitmap\n"
"\n"
"Retrieve the bitmap of exactly the given size.");

extern "C" {static PyObject *meth_wxBitmapBundleImpl_GetBitmap(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxBitmapBundleImpl_GetBitmap(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    PyObject *sipOrigSelf = sipSelf;

    {
        const ::wxSize* size;
        int sizeState = 0;
        ::wxBitmapBundleImpl *sipCpp;

        static const char *sipKwdList[] = {
            sipName_size,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxBitmapBundleImpl, &sipCpp, sipType_wxSize, &size, &sizeState))
        {
            ::wxBitmap*sipRes;

            if (!sipOrigSelf)
            {
                sipAbstractMethod(sipName_BitmapBundleImpl, sipName_GetBitmap);
                return SIP_NULLPTR;
            }

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxBitmap(sipCpp->GetBitmap(*size));
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxSize *>(size), sipType_wxSize, sizeState);

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxBitmap, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_BitmapBundleImpl, sipName_GetBitmap, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxBitmapBundleImpl_DoGetPreferredSize, "DoGetPreferredSize(scale) -> Size\n"
"\n"
"Helper for implementing GetPreferredBitmapSizeAtScale() in the derived\n"
"classes.");

extern "C" {static PyObject *meth_wxBitmapBundleImpl_DoGetPreferredSize(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxBitmapBundleImpl_DoGetPreferredSize(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        double scale;
        const sipwxBitmapBundleImpl *sipCpp;

        static const char *sipKwdList[] = {
            sipName_scale,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bd", &sipSelf, sipType_wxBitmapBundleImpl, &sipCpp, &scale))
        {
            ::wxSize*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxSize(sipCpp->sipProtect_DoGetPreferredSize(scale));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxSize, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_BitmapBundleImpl, sipName_DoGetPreferredSize, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxBitmapBundleImpl_GetIndexToUpscale, "GetIndexToUpscale(size) -> int\n"
"\n"
"Return the index of the available scale most suitable to be upscaled\n"
"to the given size.");

extern "C" {static PyObject *meth_wxBitmapBundleImpl_GetIndexToUpscale(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxBitmapBundleImpl_GetIndexToUpscale(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxSize* size;
        int sizeState = 0;
        const sipwxBitmapBundleImpl *sipCpp;

        static const char *sipKwdList[] = {
            sipName_size,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxBitmapBundleImpl, &sipCpp, sipType_wxSize, &size, &sizeState))
        {
            size_t sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->sipProtect_GetIndexToUpscale(*size);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxSize *>(size), sipType_wxSize, sizeState);

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromUnsignedLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_BitmapBundleImpl, sipName_GetIndexToUpscale, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxBitmapBundleImpl_GetNextAvailableScale, "GetNextAvailableScale(idx) -> Tuple[float, int]\n"
"\n"
"Return information about the available bitmaps.");

extern "C" {static PyObject *meth_wxBitmapBundleImpl_GetNextAvailableScale(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxBitmapBundleImpl_GetNextAvailableScale(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        size_t idx;
        const sipwxBitmapBundleImpl *sipCpp;

        static const char *sipKwdList[] = {
            sipName_idx,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "B=", &sipSelf, sipType_wxBitmapBundleImpl, &sipCpp, &idx))
        {
            double sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->sipProtectVirt_GetNextAvailableScale(sipSelfWasArg, idx);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipBuildResult(0, "(d=)", sipRes, idx);
        }
    }

    sipNoMethod(sipParseErr, sipName_BitmapBundleImpl, sipName_GetNextAvailableScale, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxBitmapBundleImpl(void *, const sipTypeDef *);}
static void *cast_wxBitmapBundleImpl(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxBitmapBundleImpl *sipCpp = reinterpret_cast<::wxBitmapBundleImpl *>(sipCppV);

    if (targetType == sipType_wxBitmapBundleImpl)
        return sipCppV;

    if (targetType == sipType_wxRefCounter)
        return static_cast<::wxRefCounter *>(sipCpp);

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxBitmapBundleImpl(void *, int);}
static void release_wxBitmapBundleImpl(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxBitmapBundleImpl *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxBitmapBundleImpl(sipSimpleWrapper *);}
static void dealloc_wxBitmapBundleImpl(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxBitmapBundleImpl *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxBitmapBundleImpl(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxBitmapBundleImpl(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxBitmapBundleImpl(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxBitmapBundleImpl *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxBitmapBundleImpl();
            Py_END_ALLOW_THREADS

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}


/* Define this type's super-types. */
static sipEncodedTypeDef supers_wxBitmapBundleImpl[] = {{477, 255, 1}};


static PyMethodDef methods_wxBitmapBundleImpl[] = {
    {sipName_DoGetPreferredSize, SIP_MLMETH_CAST(meth_wxBitmapBundleImpl_DoGetPreferredSize), METH_VARARGS|METH_KEYWORDS, doc_wxBitmapBundleImpl_DoGetPreferredSize},
    {sipName_GetBitmap, SIP_MLMETH_CAST(meth_wxBitmapBundleImpl_GetBitmap), METH_VARARGS|METH_KEYWORDS, doc_wxBitmapBundleImpl_GetBitmap},
    {sipName_GetDefaultSize, meth_wxBitmapBundleImpl_GetDefaultSize, METH_VARARGS, doc_wxBitmapBundleImpl_GetDefaultSize},
    {sipName_GetIndexToUpscale, SIP_MLMETH_CAST(meth_wxBitmapBundleImpl_GetIndexToUpscale), METH_VARARGS|METH_KEYWORDS, doc_wxBitmapBundleImpl_GetIndexToUpscale},
    {sipName_GetNextAvailableScale, SIP_MLMETH_CAST(meth_wxBitmapBundleImpl_GetNextAvailableScale), METH_VARARGS|METH_KEYWORDS, doc_wxBitmapBundleImpl_GetNextAvailableScale},
    {sipName_GetPreferredBitmapSizeAtScale, SIP_MLMETH_CAST(meth_wxBitmapBundleImpl_GetPreferredBitmapSizeAtScale), METH_VARARGS|METH_KEYWORDS, doc_wxBitmapBundleImpl_GetPreferredBitmapSizeAtScale}
};

sipVariableDef variables_wxBitmapBundleImpl[] = {
    {PropertyVariable, sipName_DefaultSize, &methods_wxBitmapBundleImpl[2], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxBitmapBundleImpl, "Base class for custom implementations of wxBitmapBundle.");


sipClassTypeDef sipTypeDef__core_wxBitmapBundleImpl = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_ABSTRACT|SIP_TYPE_CLASS,
        sipNameNr_wxBitmapBundleImpl,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_BitmapBundleImpl,
        {0, 0, 1},
        6, methods_wxBitmapBundleImpl,
        0, SIP_NULLPTR,
        1, variables_wxBitmapBundleImpl,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxBitmapBundleImpl,
    -1,
    -1,
    supers_wxBitmapBundleImpl,
    SIP_NULLPTR,
    init_type_wxBitmapBundleImpl,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxBitmapBundleImpl,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxBitmapBundleImpl,
    cast_wxBitmapBundleImpl,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    sizeof (::wxBitmapBundleImpl),
};
