/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/iconbndl.h>
        #include <wx/stream.h>
        #include <wx/icon.h>
        #include <wx/gdicmn.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


class sipwxIconBundle : public ::wxIconBundle
{
public:
    sipwxIconBundle();
    sipwxIconBundle(const ::wxString&, ::wxBitmapType);
    sipwxIconBundle(::wxInputStream&, ::wxBitmapType);
    sipwxIconBundle(const ::wxIcon&);
    sipwxIconBundle(const ::wxIconBundle&);
    ~sipwxIconBundle();

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxIconBundle(const sipwxIconBundle &);
    sipwxIconBundle &operator = (const sipwxIconBundle &);
};

sipwxIconBundle::sipwxIconBundle(): ::wxIconBundle(), sipPySelf(SIP_NULLPTR)
{
}

sipwxIconBundle::sipwxIconBundle(const ::wxString& file, ::wxBitmapType type): ::wxIconBundle(file, type), sipPySelf(SIP_NULLPTR)
{
}

sipwxIconBundle::sipwxIconBundle(::wxInputStream& stream, ::wxBitmapType type): ::wxIconBundle(stream, type), sipPySelf(SIP_NULLPTR)
{
}

sipwxIconBundle::sipwxIconBundle(const ::wxIcon& icon): ::wxIconBundle(icon), sipPySelf(SIP_NULLPTR)
{
}

sipwxIconBundle::sipwxIconBundle(const ::wxIconBundle& ic): ::wxIconBundle(ic), sipPySelf(SIP_NULLPTR)
{
}

sipwxIconBundle::~sipwxIconBundle()
{
    sipInstanceDestroyedEx(&sipPySelf);
}


PyDoc_STRVAR(doc_wxIconBundle_AddIcon, "AddIcon(file, type=BITMAP_TYPE_ANY) -> None\n"
"AddIcon(stream, type=BITMAP_TYPE_ANY) -> None\n"
"AddIcon(icon) -> None\n"
"\n"
"Adds all the icons contained in the file to the bundle; if the\n"
"collection already contains icons with the same width and height, they\n"
"are replaced by the new ones.\n"
"\n"
"");

extern "C" {static PyObject *meth_wxIconBundle_AddIcon(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxIconBundle_AddIcon(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxString* file;
        int fileState = 0;
        ::wxBitmapType type = wxBITMAP_TYPE_ANY;
        ::wxIconBundle *sipCpp;

        static const char *sipKwdList[] = {
            sipName_file,
            sipName_type,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1|E", &sipSelf, sipType_wxIconBundle, &sipCpp, sipType_wxString, &file, &fileState, sipType_wxBitmapType, &type))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->AddIcon(*file, type);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxString *>(file), sipType_wxString, fileState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    {
        ::wxInputStream* stream;
        int streamState = 0;
        ::wxBitmapType type = wxBITMAP_TYPE_ANY;
        ::wxIconBundle *sipCpp;

        static const char *sipKwdList[] = {
            sipName_stream,
            sipName_type,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1|E", &sipSelf, sipType_wxIconBundle, &sipCpp, sipType_wxInputStream, &stream, &streamState, sipType_wxBitmapType, &type))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->AddIcon(*stream, type);
            Py_END_ALLOW_THREADS
            sipReleaseType(stream, sipType_wxInputStream, streamState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    {
        const ::wxIcon* icon;
        ::wxIconBundle *sipCpp;

        static const char *sipKwdList[] = {
            sipName_icon,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9", &sipSelf, sipType_wxIconBundle, &sipCpp, sipType_wxIcon, &icon))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->AddIcon(*icon);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_IconBundle, sipName_AddIcon, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxIconBundle_GetIcon, "GetIcon(size, flags=FALLBACK_SYSTEM) -> Icon\n"
"GetIcon(size=DefaultCoord, flags=FALLBACK_SYSTEM) -> Icon\n"
"\n"
"Returns the icon with the given size.\n"
"");

extern "C" {static PyObject *meth_wxIconBundle_GetIcon(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxIconBundle_GetIcon(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxSize* size;
        int sizeState = 0;
        int flags = ::wxIconBundle::FALLBACK_SYSTEM;
        const ::wxIconBundle *sipCpp;

        static const char *sipKwdList[] = {
            sipName_size,
            sipName_flags,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1|i", &sipSelf, sipType_wxIconBundle, &sipCpp, sipType_wxSize, &size, &sizeState, &flags))
        {
            ::wxIcon*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxIcon(sipCpp->GetIcon(*size, flags));
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxSize *>(size), sipType_wxSize, sizeState);

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxIcon, SIP_NULLPTR);
        }
    }

    {
        ::wxCoord size = wxDefaultCoord;
        int flags = ::wxIconBundle::FALLBACK_SYSTEM;
        const ::wxIconBundle *sipCpp;

        static const char *sipKwdList[] = {
            sipName_size,
            sipName_flags,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "B|ii", &sipSelf, sipType_wxIconBundle, &sipCpp, &size, &flags))
        {
            ::wxIcon*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxIcon(sipCpp->GetIcon(size, flags));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxIcon, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_IconBundle, sipName_GetIcon, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxIconBundle_GetIconOfExactSize, "GetIconOfExactSize(size) -> Icon\n"
"\n"
"Returns the icon with exactly the given size or wxNullIcon if this\n"
"size is not available.");

extern "C" {static PyObject *meth_wxIconBundle_GetIconOfExactSize(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxIconBundle_GetIconOfExactSize(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxSize* size;
        int sizeState = 0;
        const ::wxIconBundle *sipCpp;

        static const char *sipKwdList[] = {
            sipName_size,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxIconBundle, &sipCpp, sipType_wxSize, &size, &sizeState))
        {
            ::wxIcon*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxIcon(sipCpp->GetIconOfExactSize(*size));
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxSize *>(size), sipType_wxSize, sizeState);

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxIcon, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_IconBundle, sipName_GetIconOfExactSize, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxIconBundle_GetIconCount, "GetIconCount() -> int\n"
"\n"
"return the number of available icons");

extern "C" {static PyObject *meth_wxIconBundle_GetIconCount(PyObject *, PyObject *);}
static PyObject *meth_wxIconBundle_GetIconCount(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxIconBundle *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxIconBundle, &sipCpp))
        {
            size_t sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetIconCount();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromUnsignedLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_IconBundle, sipName_GetIconCount, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxIconBundle_GetIconByIndex, "GetIconByIndex(n) -> Icon\n"
"\n"
"return the icon at index (must be < GetIconCount())");

extern "C" {static PyObject *meth_wxIconBundle_GetIconByIndex(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxIconBundle_GetIconByIndex(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        size_t n;
        const ::wxIconBundle *sipCpp;

        static const char *sipKwdList[] = {
            sipName_n,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "B=", &sipSelf, sipType_wxIconBundle, &sipCpp, &n))
        {
            ::wxIcon*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxIcon(sipCpp->GetIconByIndex(n));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxIcon, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_IconBundle, sipName_GetIconByIndex, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxIconBundle_IsEmpty, "IsEmpty() -> bool\n"
"\n"
"Returns true if the bundle doesn't contain any icons, false otherwise\n"
"(in which case a call to GetIcon() with default parameter should\n"
"return a valid icon).");

extern "C" {static PyObject *meth_wxIconBundle_IsEmpty(PyObject *, PyObject *);}
static PyObject *meth_wxIconBundle_IsEmpty(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxIconBundle *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxIconBundle, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->IsEmpty();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_IconBundle, sipName_IsEmpty, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxIconBundle(void *, const sipTypeDef *);}
static void *cast_wxIconBundle(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxIconBundle *sipCpp = reinterpret_cast<::wxIconBundle *>(sipCppV);

    if (targetType == sipType_wxIconBundle)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxGDIObject)->ctd_cast(static_cast<::wxGDIObject *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxIconBundle(void *, int);}
static void release_wxIconBundle(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxIconBundle *>(sipCppV);
    else
        delete reinterpret_cast<::wxIconBundle *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxIconBundle(Py_ssize_t);}
static void *array_wxIconBundle(Py_ssize_t sipNrElem)
{
    return new ::wxIconBundle[sipNrElem];
}


extern "C" {static void array_delete_wxIconBundle(void *);}
static void array_delete_wxIconBundle(void *sipCpp)
{
    delete[] reinterpret_cast<::wxIconBundle *>(sipCpp);
}


extern "C" {static void assign_wxIconBundle(void *, Py_ssize_t, void *);}
static void assign_wxIconBundle(void *sipDst, Py_ssize_t sipDstIdx, void *sipSrc)
{
    reinterpret_cast<::wxIconBundle *>(sipDst)[sipDstIdx] = *reinterpret_cast<::wxIconBundle *>(sipSrc);
}


extern "C" {static void *copy_wxIconBundle(const void *, Py_ssize_t);}
static void *copy_wxIconBundle(const void *sipSrc, Py_ssize_t sipSrcIdx)
{
    return new ::wxIconBundle(reinterpret_cast<const ::wxIconBundle *>(sipSrc)[sipSrcIdx]);
}


extern "C" {static void dealloc_wxIconBundle(sipSimpleWrapper *);}
static void dealloc_wxIconBundle(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxIconBundle *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxIconBundle(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxIconBundle(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxIconBundle(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxIconBundle *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxIconBundle();
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
        const ::wxString* file;
        int fileState = 0;
        ::wxBitmapType type = wxBITMAP_TYPE_ANY;

        static const char *sipKwdList[] = {
            sipName_file,
            sipName_type,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J1|E", sipType_wxString, &file, &fileState, sipType_wxBitmapType, &type))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxIconBundle(*file, type);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxString *>(file), sipType_wxString, fileState);

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
        ::wxInputStream* stream;
        int streamState = 0;
        ::wxBitmapType type = wxBITMAP_TYPE_ANY;

        static const char *sipKwdList[] = {
            sipName_stream,
            sipName_type,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J1|E", sipType_wxInputStream, &stream, &streamState, sipType_wxBitmapType, &type))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxIconBundle(*stream, type);
            Py_END_ALLOW_THREADS
            sipReleaseType(stream, sipType_wxInputStream, streamState);

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
        const ::wxIcon* icon;

        static const char *sipKwdList[] = {
            sipName_icon,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J9", sipType_wxIcon, &icon))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxIconBundle(*icon);
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
        const ::wxIconBundle* ic;

        static const char *sipKwdList[] = {
            sipName_ic,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J9", sipType_wxIconBundle, &ic))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxIconBundle(*ic);
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
static sipEncodedTypeDef supers_wxIconBundle[] = {{226, 255, 1}};


static PyMethodDef methods_wxIconBundle[] = {
    {sipName_AddIcon, SIP_MLMETH_CAST(meth_wxIconBundle_AddIcon), METH_VARARGS|METH_KEYWORDS, doc_wxIconBundle_AddIcon},
    {sipName_GetIcon, SIP_MLMETH_CAST(meth_wxIconBundle_GetIcon), METH_VARARGS|METH_KEYWORDS, doc_wxIconBundle_GetIcon},
    {sipName_GetIconByIndex, SIP_MLMETH_CAST(meth_wxIconBundle_GetIconByIndex), METH_VARARGS|METH_KEYWORDS, doc_wxIconBundle_GetIconByIndex},
    {sipName_GetIconCount, meth_wxIconBundle_GetIconCount, METH_VARARGS, doc_wxIconBundle_GetIconCount},
    {sipName_GetIconOfExactSize, SIP_MLMETH_CAST(meth_wxIconBundle_GetIconOfExactSize), METH_VARARGS|METH_KEYWORDS, doc_wxIconBundle_GetIconOfExactSize},
    {sipName_IsEmpty, meth_wxIconBundle_IsEmpty, METH_VARARGS, doc_wxIconBundle_IsEmpty}
};

static sipEnumMemberDef enummembers_wxIconBundle[] = {
    {sipName_FALLBACK_NEAREST_LARGER, static_cast<int>(::wxIconBundle::FALLBACK_NEAREST_LARGER), -1},
    {sipName_FALLBACK_NONE, static_cast<int>(::wxIconBundle::FALLBACK_NONE), -1},
    {sipName_FALLBACK_SYSTEM, static_cast<int>(::wxIconBundle::FALLBACK_SYSTEM), -1},
};

sipVariableDef variables_wxIconBundle[] = {
    {PropertyVariable, sipName_IconCount, &methods_wxIconBundle[3], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Icon, &methods_wxIconBundle[1], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxIconBundle, "IconBundle() -> None\n"
"IconBundle(file, type=BITMAP_TYPE_ANY) -> None\n"
"IconBundle(stream, type=BITMAP_TYPE_ANY) -> None\n"
"IconBundle(icon) -> None\n"
"IconBundle(ic) -> None\n"
"\n"
"This class contains multiple copies of an icon in different sizes.");


sipClassTypeDef sipTypeDef__core_wxIconBundle = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxIconBundle,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_IconBundle,
        {0, 0, 1},
        6, methods_wxIconBundle,
        3, enummembers_wxIconBundle,
        2, variables_wxIconBundle,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxIconBundle,
    -1,
    -1,
    supers_wxIconBundle,
    SIP_NULLPTR,
    init_type_wxIconBundle,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxIconBundle,
    assign_wxIconBundle,
    array_wxIconBundle,
    copy_wxIconBundle,
    release_wxIconBundle,
    cast_wxIconBundle,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxIconBundle,
    sizeof (::wxIconBundle),
};
