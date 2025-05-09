/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/pen.h>
        #include <wx/colour.h>
        #include <wx/bitmap.h>


PyDoc_STRVAR(doc_wxPenInfo_Colour, "Colour(col) -> PenInfo");

extern "C" {static PyObject *meth_wxPenInfo_Colour(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_Colour(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxColour* col;
        int colState = 0;
        ::wxPenInfo *sipCpp;

        static const char *sipKwdList[] = {
            sipName_col,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxPenInfo, &sipCpp, sipType_wxColour, &col, &colState))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->Colour(*col);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxColour *>(col), sipType_wxColour, colState);

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_Colour, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_Width, "Width(width) -> PenInfo");

extern "C" {static PyObject *meth_wxPenInfo_Width(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_Width(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        int width;
        ::wxPenInfo *sipCpp;

        static const char *sipKwdList[] = {
            sipName_width,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bi", &sipSelf, sipType_wxPenInfo, &sipCpp, &width))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->Width(width);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_Width, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_Style, "Style(style) -> PenInfo");

extern "C" {static PyObject *meth_wxPenInfo_Style(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_Style(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPenStyle style;
        ::wxPenInfo *sipCpp;

        static const char *sipKwdList[] = {
            sipName_style,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPenInfo, &sipCpp, sipType_wxPenStyle, &style))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->Style(style);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_Style, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_Stipple, "Stipple(stipple) -> PenInfo");

extern "C" {static PyObject *meth_wxPenInfo_Stipple(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_Stipple(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxBitmap* stipple;
        ::wxPenInfo *sipCpp;

        static const char *sipKwdList[] = {
            sipName_stipple,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9", &sipSelf, sipType_wxPenInfo, &sipCpp, sipType_wxBitmap, &stipple))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->Stipple(*stipple);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_Stipple, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_Join, "Join(join) -> PenInfo");

extern "C" {static PyObject *meth_wxPenInfo_Join(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_Join(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPenJoin join;
        ::wxPenInfo *sipCpp;

        static const char *sipKwdList[] = {
            sipName_join,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPenInfo, &sipCpp, sipType_wxPenJoin, &join))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->Join(join);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_Join, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_Cap, "Cap(cap) -> PenInfo");

extern "C" {static PyObject *meth_wxPenInfo_Cap(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_Cap(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPenCap cap;
        ::wxPenInfo *sipCpp;

        static const char *sipKwdList[] = {
            sipName_cap,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPenInfo, &sipCpp, sipType_wxPenCap, &cap))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->Cap(cap);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_Cap, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_Quality, "Quality(quality) -> PenInfo\n"
"\n"
"Set the pen quality.");

extern "C" {static PyObject *meth_wxPenInfo_Quality(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_Quality(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPenQuality quality;
        ::wxPenInfo *sipCpp;

        static const char *sipKwdList[] = {
            sipName_quality,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPenInfo, &sipCpp, sipType_wxPenQuality, &quality))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->Quality(quality);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_Quality, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_LowQuality, "LowQuality() -> PenInfo\n"
"\n"
"Set low pen quality.");

extern "C" {static PyObject *meth_wxPenInfo_LowQuality(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_LowQuality(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->LowQuality();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_LowQuality, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_HighQuality, "HighQuality() -> PenInfo\n"
"\n"
"Set high pen quality.");

extern "C" {static PyObject *meth_wxPenInfo_HighQuality(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_HighQuality(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxPenInfo*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = &sipCpp->HighQuality();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxPenInfo, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_HighQuality, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_GetColour, "GetColour() -> Colour");

extern "C" {static PyObject *meth_wxPenInfo_GetColour(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_GetColour(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxColour*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxColour(sipCpp->GetColour());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxColour, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_GetColour, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_GetStipple, "GetStipple() -> Bitmap");

extern "C" {static PyObject *meth_wxPenInfo_GetStipple(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_GetStipple(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxBitmap*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxBitmap(sipCpp->GetStipple());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxBitmap, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_GetStipple, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_GetStyle, "GetStyle() -> PenStyle");

extern "C" {static PyObject *meth_wxPenInfo_GetStyle(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_GetStyle(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxPenStyle sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetStyle();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPenStyle);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_GetStyle, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_GetJoin, "GetJoin() -> PenJoin");

extern "C" {static PyObject *meth_wxPenInfo_GetJoin(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_GetJoin(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxPenJoin sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetJoin();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPenJoin);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_GetJoin, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_GetCap, "GetCap() -> PenCap");

extern "C" {static PyObject *meth_wxPenInfo_GetCap(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_GetCap(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxPenCap sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetCap();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPenCap);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_GetCap, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_GetQuality, "GetQuality() -> PenQuality");

extern "C" {static PyObject *meth_wxPenInfo_GetQuality(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_GetQuality(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            ::wxPenQuality sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetQuality();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPenQuality);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_GetQuality, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_IsTransparent, "IsTransparent() -> bool");

extern "C" {static PyObject *meth_wxPenInfo_IsTransparent(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_IsTransparent(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->IsTransparent();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_IsTransparent, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPenInfo_GetWidth, "GetWidth() -> int");

extern "C" {static PyObject *meth_wxPenInfo_GetWidth(PyObject *, PyObject *);}
static PyObject *meth_wxPenInfo_GetWidth(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPenInfo *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPenInfo, &sipCpp))
        {
            int sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetWidth();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PenInfo, sipName_GetWidth, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxPenInfo(void *, int);}
static void release_wxPenInfo(void *sipCppV, int)
{
    Py_BEGIN_ALLOW_THREADS

    delete reinterpret_cast<::wxPenInfo *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxPenInfo(Py_ssize_t);}
static void *array_wxPenInfo(Py_ssize_t sipNrElem)
{
    return new ::wxPenInfo[sipNrElem];
}


extern "C" {static void array_delete_wxPenInfo(void *);}
static void array_delete_wxPenInfo(void *sipCpp)
{
    delete[] reinterpret_cast<::wxPenInfo *>(sipCpp);
}


extern "C" {static void assign_wxPenInfo(void *, Py_ssize_t, void *);}
static void assign_wxPenInfo(void *sipDst, Py_ssize_t sipDstIdx, void *sipSrc)
{
    reinterpret_cast<::wxPenInfo *>(sipDst)[sipDstIdx] = *reinterpret_cast<::wxPenInfo *>(sipSrc);
}


extern "C" {static void *copy_wxPenInfo(const void *, Py_ssize_t);}
static void *copy_wxPenInfo(const void *sipSrc, Py_ssize_t sipSrcIdx)
{
    return new ::wxPenInfo(reinterpret_cast<const ::wxPenInfo *>(sipSrc)[sipSrcIdx]);
}


extern "C" {static void dealloc_wxPenInfo(sipSimpleWrapper *);}
static void dealloc_wxPenInfo(sipSimpleWrapper *sipSelf)
{
    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxPenInfo(sipGetAddress(sipSelf), 0);
    }
}


extern "C" {static void *init_type_wxPenInfo(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxPenInfo(sipSimpleWrapper *, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    ::wxPenInfo *sipCpp = SIP_NULLPTR;

    {
        const ::wxColour& colourdef = wxColour();
        const ::wxColour* colour = &colourdef;
        int colourState = 0;
        int width = 1;
        ::wxPenStyle style = wxPENSTYLE_SOLID;

        static const char *sipKwdList[] = {
            sipName_colour,
            sipName_width,
            sipName_style,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "|J1iE", sipType_wxColour, &colour, &colourState, &width, sipType_wxPenStyle, &style))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxPenInfo(*colour, width, style);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxColour *>(colour), sipType_wxColour, colourState);

            if (PyErr_Occurred())
            {
                delete sipCpp;
                return SIP_NULLPTR;
            }

            return sipCpp;
        }
    }

    {
        const ::wxPenInfo* a0;

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, "J9", sipType_wxPenInfo, &a0))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxPenInfo(*a0);
            Py_END_ALLOW_THREADS

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}


static PyMethodDef methods_wxPenInfo[] = {
    {sipName_Cap, SIP_MLMETH_CAST(meth_wxPenInfo_Cap), METH_VARARGS|METH_KEYWORDS, doc_wxPenInfo_Cap},
    {sipName_Colour, SIP_MLMETH_CAST(meth_wxPenInfo_Colour), METH_VARARGS|METH_KEYWORDS, doc_wxPenInfo_Colour},
    {sipName_GetCap, meth_wxPenInfo_GetCap, METH_VARARGS, doc_wxPenInfo_GetCap},
    {sipName_GetColour, meth_wxPenInfo_GetColour, METH_VARARGS, doc_wxPenInfo_GetColour},
    {sipName_GetJoin, meth_wxPenInfo_GetJoin, METH_VARARGS, doc_wxPenInfo_GetJoin},
    {sipName_GetQuality, meth_wxPenInfo_GetQuality, METH_VARARGS, doc_wxPenInfo_GetQuality},
    {sipName_GetStipple, meth_wxPenInfo_GetStipple, METH_VARARGS, doc_wxPenInfo_GetStipple},
    {sipName_GetStyle, meth_wxPenInfo_GetStyle, METH_VARARGS, doc_wxPenInfo_GetStyle},
    {sipName_GetWidth, meth_wxPenInfo_GetWidth, METH_VARARGS, doc_wxPenInfo_GetWidth},
    {sipName_HighQuality, meth_wxPenInfo_HighQuality, METH_VARARGS, doc_wxPenInfo_HighQuality},
    {sipName_IsTransparent, meth_wxPenInfo_IsTransparent, METH_VARARGS, doc_wxPenInfo_IsTransparent},
    {sipName_Join, SIP_MLMETH_CAST(meth_wxPenInfo_Join), METH_VARARGS|METH_KEYWORDS, doc_wxPenInfo_Join},
    {sipName_LowQuality, meth_wxPenInfo_LowQuality, METH_VARARGS, doc_wxPenInfo_LowQuality},
    {sipName_Quality, SIP_MLMETH_CAST(meth_wxPenInfo_Quality), METH_VARARGS|METH_KEYWORDS, doc_wxPenInfo_Quality},
    {sipName_Stipple, SIP_MLMETH_CAST(meth_wxPenInfo_Stipple), METH_VARARGS|METH_KEYWORDS, doc_wxPenInfo_Stipple},
    {sipName_Style, SIP_MLMETH_CAST(meth_wxPenInfo_Style), METH_VARARGS|METH_KEYWORDS, doc_wxPenInfo_Style},
    {sipName_Width, SIP_MLMETH_CAST(meth_wxPenInfo_Width), METH_VARARGS|METH_KEYWORDS, doc_wxPenInfo_Width}
};

PyDoc_STRVAR(doc_wxPenInfo, "PenInfo(colour=Colour(), width=1, style=PENSTYLE_SOLID) -> None\n"
"\n"
"This class is a helper used for wxPen creation using named parameter\n"
"idiom: it allows specifying various wxPen attributes using the chained\n"
"calls to its clearly named methods instead of passing them in the\n"
"fixed order to wxPen constructors.");


sipClassTypeDef sipTypeDef__core_wxPenInfo = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_CLASS,
        sipNameNr_wxPenInfo,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_PenInfo,
        {0, 0, 1},
        17, methods_wxPenInfo,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxPenInfo,
    -1,
    -1,
    SIP_NULLPTR,
    SIP_NULLPTR,
    init_type_wxPenInfo,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxPenInfo,
    assign_wxPenInfo,
    array_wxPenInfo,
    copy_wxPenInfo,
    release_wxPenInfo,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxPenInfo,
    sizeof (::wxPenInfo),
};
