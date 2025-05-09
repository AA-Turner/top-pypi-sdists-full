/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/cmndata.h>
        #include <wx/gdicmn.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>
    void _wxPrintData_SetPaperSize(wxPrintData* self, const wxSize* sz)
    {
        self->SetPaperSize(*sz);
    }
    wxSize* _wxPrintData_GetPaperSize(wxPrintData* self)
    {
        return new wxSize(self->GetPaperSize());
    }
    int _wxPrintData___nonzero__(wxPrintData* self)
    {
        return self->IsOk();
    }
    int _wxPrintData___bool__(wxPrintData* self)
    {
        return self->IsOk();
    }
    PyObject* _wxPrintData_GetPrivData(wxPrintData* self)
    {
        PyObject* data;
        wxPyThreadBlocker blocker;
        data = PyBytes_FromStringAndSize(self->GetPrivData(),
                                         self->GetPrivDataLen());
        return data;
    }
    void _wxPrintData_SetPrivData(wxPrintData* self, PyObject* data)
    {
        wxPyThreadBlocker blocker;
        if (! PyBytes_Check(data)) {
            wxPyErr_SetString(PyExc_TypeError, "Expected string object");
            return;
        }
        
        self->SetPrivData(PyBytes_AS_STRING(data), PyBytes_GET_SIZE(data));
    }


PyDoc_STRVAR(doc_wxPrintData_GetBin, "GetBin() -> PrintBin\n"
"\n"
"Returns the current bin (papersource).");

extern "C" {static PyObject *meth_wxPrintData_GetBin(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetBin(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxPrintBin sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetBin();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPrintBin);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetBin, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetCollate, "GetCollate() -> bool\n"
"\n"
"Returns true if collation is on.");

extern "C" {static PyObject *meth_wxPrintData_GetCollate(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetCollate(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetCollate();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetCollate, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetColour, "GetColour() -> bool\n"
"\n"
"Returns true if colour printing is on.");

extern "C" {static PyObject *meth_wxPrintData_GetColour(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetColour(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetColour();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetColour, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetDuplex, "GetDuplex() -> DuplexMode\n"
"\n"
"Returns the duplex mode.");

extern "C" {static PyObject *meth_wxPrintData_GetDuplex(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetDuplex(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxDuplexMode sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetDuplex();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxDuplexMode);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetDuplex, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetNoCopies, "GetNoCopies() -> int\n"
"\n"
"Returns the number of copies requested by the user.");

extern "C" {static PyObject *meth_wxPrintData_GetNoCopies(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetNoCopies(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            int sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetNoCopies();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetNoCopies, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetOrientation, "GetOrientation() -> PrintOrientation\n"
"\n"
"Gets the orientation.");

extern "C" {static PyObject *meth_wxPrintData_GetOrientation(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetOrientation(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxPrintOrientation sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetOrientation();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPrintOrientation);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetOrientation, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetPaperId, "GetPaperId() -> PaperSize\n"
"\n"
"Returns the paper size id.");

extern "C" {static PyObject *meth_wxPrintData_GetPaperId(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetPaperId(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxPaperSize sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetPaperId();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPaperSize);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetPaperId, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetPrinterName, "GetPrinterName() -> str\n"
"\n"
"Returns the printer name.");

extern "C" {static PyObject *meth_wxPrintData_GetPrinterName(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetPrinterName(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxString*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxString(sipCpp->GetPrinterName());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxString, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetPrinterName, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetQuality, "GetQuality() -> PrintQuality\n"
"\n"
"Returns the current print quality.");

extern "C" {static PyObject *meth_wxPrintData_GetQuality(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetQuality(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxPrintQuality sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetQuality();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetQuality, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_IsOk, "IsOk() -> bool\n"
"\n"
"Returns true if the print data is valid for using in print dialogs.");

extern "C" {static PyObject *meth_wxPrintData_IsOk(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_IsOk(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->IsOk();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_IsOk, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetBin, "SetBin(flag) -> None\n"
"\n"
"Sets the current bin.");

extern "C" {static PyObject *meth_wxPrintData_SetBin(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetBin(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPrintBin flag;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_flag,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxPrintBin, &flag))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetBin(flag);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetBin, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetCollate, "SetCollate(flag) -> None\n"
"\n"
"Sets collation to on or off.");

extern "C" {static PyObject *meth_wxPrintData_SetCollate(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetCollate(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        bool flag;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_flag,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bb", &sipSelf, sipType_wxPrintData, &sipCpp, &flag))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetCollate(flag);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetCollate, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetColour, "SetColour(flag) -> None\n"
"\n"
"Sets colour printing on or off.");

extern "C" {static PyObject *meth_wxPrintData_SetColour(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetColour(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        bool flag;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_flag,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bb", &sipSelf, sipType_wxPrintData, &sipCpp, &flag))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetColour(flag);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetColour, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetDuplex, "SetDuplex(mode) -> None\n"
"\n"
"Returns the duplex mode.");

extern "C" {static PyObject *meth_wxPrintData_SetDuplex(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetDuplex(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxDuplexMode mode;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_mode,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxDuplexMode, &mode))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetDuplex(mode);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetDuplex, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetNoCopies, "SetNoCopies(n) -> None\n"
"\n"
"Sets the default number of copies to be printed out.");

extern "C" {static PyObject *meth_wxPrintData_SetNoCopies(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetNoCopies(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        int n;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_n,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bi", &sipSelf, sipType_wxPrintData, &sipCpp, &n))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetNoCopies(n);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetNoCopies, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetOrientation, "SetOrientation(orientation) -> None\n"
"\n"
"Sets the orientation.");

extern "C" {static PyObject *meth_wxPrintData_SetOrientation(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetOrientation(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPrintOrientation orientation;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_orientation,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxPrintOrientation, &orientation))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetOrientation(orientation);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetOrientation, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetPaperId, "SetPaperId(paperId) -> None\n"
"\n"
"Sets the paper id.");

extern "C" {static PyObject *meth_wxPrintData_SetPaperId(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetPaperId(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPaperSize paperId;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_paperId,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxPaperSize, &paperId))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetPaperId(paperId);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetPaperId, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetPaperSize, "SetPaperSize(size) -> None\n"
"SetPaperSize(sz) -> None\n"
"\n"
"Sets custom paper size.\n"
"");

extern "C" {static PyObject *meth_wxPrintData_SetPaperSize(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetPaperSize(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxSize* size;
        int sizeState = 0;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_size,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxSize, &size, &sizeState))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetPaperSize(*size);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxSize *>(size), sipType_wxSize, sizeState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    {
        const ::wxSize* sz;
        int szState = 0;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_sz,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ0", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxSize, &sz, &szState))
        {
            int sipIsErr = 0;
        PyErr_Clear();
        Py_BEGIN_ALLOW_THREADS
        _wxPrintData_SetPaperSize(sipCpp, sz);
        Py_END_ALLOW_THREADS
        if (PyErr_Occurred()) sipIsErr = 1;
            sipReleaseType(const_cast<::wxSize *>(sz), sipType_wxSize, szState);

            if (sipIsErr)
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetPaperSize, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetPrinterName, "SetPrinterName(printerName) -> None\n"
"\n"
"Sets the printer name.");

extern "C" {static PyObject *meth_wxPrintData_SetPrinterName(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetPrinterName(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxString* printerName;
        int printerNameState = 0;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_printerName,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxString, &printerName, &printerNameState))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetPrinterName(*printerName);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxString *>(printerName), sipType_wxString, printerNameState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetPrinterName, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetQuality, "SetQuality(quality) -> None\n"
"\n"
"Sets the desired print quality.");

extern "C" {static PyObject *meth_wxPrintData_SetQuality(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetQuality(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPrintQuality quality;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_quality,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bi", &sipSelf, sipType_wxPrintData, &sipCpp, &quality))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetQuality(quality);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetQuality, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetFilename, "GetFilename() -> str");

extern "C" {static PyObject *meth_wxPrintData_GetFilename(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetFilename(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxString*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxString(sipCpp->GetFilename());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxString, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetFilename, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetFilename, "SetFilename(filename) -> None");

extern "C" {static PyObject *meth_wxPrintData_SetFilename(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetFilename(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxString* filename;
        int filenameState = 0;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_filename,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxString, &filename, &filenameState))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetFilename(*filename);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxString *>(filename), sipType_wxString, filenameState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetFilename, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetPrintMode, "GetPrintMode() -> PrintMode");

extern "C" {static PyObject *meth_wxPrintData_GetPrintMode(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetPrintMode(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxPrintMode sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetPrintMode();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromEnum(static_cast<int>(sipRes), sipType_wxPrintMode);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetPrintMode, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetPrintMode, "SetPrintMode(printMode) -> None");

extern "C" {static PyObject *meth_wxPrintData_SetPrintMode(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetPrintMode(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPrintMode printMode;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_printMode,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxPrintData, &sipCpp, sipType_wxPrintMode, &printMode))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp->SetPrintMode(printMode);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetPrintMode, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetPaperSize, "GetPaperSize() -> Size");

extern "C" {static PyObject *meth_wxPrintData_GetPaperSize(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetPaperSize(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            ::wxSize*sipRes = 0;
            int sipIsErr = 0;
        PyErr_Clear();
        Py_BEGIN_ALLOW_THREADS
        sipRes = _wxPrintData_GetPaperSize(sipCpp);
        Py_END_ALLOW_THREADS
        if (PyErr_Occurred()) sipIsErr = 1;

            if (sipIsErr)
                return 0;

            return sipConvertFromType(sipRes, sipType_wxSize, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetPaperSize, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData___nonzero__, "__nonzero__() -> bool");

extern "C" {static PyObject *meth_wxPrintData___nonzero__(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData___nonzero__(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            int sipRes = 0;
            int sipIsErr = 0;
        PyErr_Clear();
        Py_BEGIN_ALLOW_THREADS
        sipRes = _wxPrintData___nonzero__(sipCpp);
        Py_END_ALLOW_THREADS
        if (PyErr_Occurred()) sipIsErr = 1;

            if (sipIsErr)
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName___nonzero__, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_GetPrivData, "GetPrivData() -> Any");

extern "C" {static PyObject *meth_wxPrintData_GetPrivData(PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_GetPrivData(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxPrintData *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxPrintData, &sipCpp))
        {
            PyObject * sipRes = SIP_NULLPTR;
            int sipIsErr = 0;
        PyErr_Clear();
        Py_BEGIN_ALLOW_THREADS
        sipRes = _wxPrintData_GetPrivData(sipCpp);
        Py_END_ALLOW_THREADS
        if (PyErr_Occurred()) sipIsErr = 1;

            if (sipIsErr)
                return 0;

            return sipRes;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_GetPrivData, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPrintData_SetPrivData, "SetPrivData(data) -> None");

extern "C" {static PyObject *meth_wxPrintData_SetPrivData(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPrintData_SetPrivData(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        PyObject * data;
        ::wxPrintData *sipCpp;

        static const char *sipKwdList[] = {
            sipName_data,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BP0", &sipSelf, sipType_wxPrintData, &sipCpp, &data))
        {
            int sipIsErr = 0;
        PyErr_Clear();
        Py_BEGIN_ALLOW_THREADS
        _wxPrintData_SetPrivData(sipCpp, data);
        Py_END_ALLOW_THREADS
        if (PyErr_Occurred()) sipIsErr = 1;

            if (sipIsErr)
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_PrintData, sipName_SetPrivData, SIP_NULLPTR);

    return SIP_NULLPTR;
}


extern "C" {static int slot_wxPrintData___bool__(PyObject *);}
static int slot_wxPrintData___bool__(PyObject *sipSelf)
{
    ::wxPrintData *sipCpp = reinterpret_cast<::wxPrintData *>(sipGetCppPtr((sipSimpleWrapper *)sipSelf, sipType_wxPrintData));

    if (!sipCpp)
        return -1;


    {
        {
            int sipRes = 0;
            int sipIsErr = 0;
        PyErr_Clear();
        Py_BEGIN_ALLOW_THREADS
        sipRes = _wxPrintData___bool__(sipCpp);
        Py_END_ALLOW_THREADS
        if (PyErr_Occurred()) sipIsErr = 1;

            if (sipIsErr)
                return -1;

            return sipRes;
        }
    }

    return 0;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxPrintData(void *, const sipTypeDef *);}
static void *cast_wxPrintData(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxPrintData *sipCpp = reinterpret_cast<::wxPrintData *>(sipCppV);

    if (targetType == sipType_wxPrintData)
        return sipCppV;

    if (targetType == sipType_wxObject)
        return static_cast<::wxObject *>(sipCpp);

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxPrintData(void *, int);}
static void release_wxPrintData(void *sipCppV, int)
{
    Py_BEGIN_ALLOW_THREADS

    delete reinterpret_cast<::wxPrintData *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxPrintData(Py_ssize_t);}
static void *array_wxPrintData(Py_ssize_t sipNrElem)
{
    return new ::wxPrintData[sipNrElem];
}


extern "C" {static void array_delete_wxPrintData(void *);}
static void array_delete_wxPrintData(void *sipCpp)
{
    delete[] reinterpret_cast<::wxPrintData *>(sipCpp);
}


extern "C" {static void assign_wxPrintData(void *, Py_ssize_t, void *);}
static void assign_wxPrintData(void *sipDst, Py_ssize_t sipDstIdx, void *sipSrc)
{
    reinterpret_cast<::wxPrintData *>(sipDst)[sipDstIdx] = *reinterpret_cast<::wxPrintData *>(sipSrc);
}


extern "C" {static void *copy_wxPrintData(const void *, Py_ssize_t);}
static void *copy_wxPrintData(const void *sipSrc, Py_ssize_t sipSrcIdx)
{
    return new ::wxPrintData(reinterpret_cast<const ::wxPrintData *>(sipSrc)[sipSrcIdx]);
}


extern "C" {static void dealloc_wxPrintData(sipSimpleWrapper *);}
static void dealloc_wxPrintData(sipSimpleWrapper *sipSelf)
{
    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxPrintData(sipGetAddress(sipSelf), 0);
    }
}


extern "C" {static void *init_type_wxPrintData(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxPrintData(sipSimpleWrapper *, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    ::wxPrintData *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxPrintData();
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
        const ::wxPrintData* data;

        static const char *sipKwdList[] = {
            sipName_data,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J9", sipType_wxPrintData, &data))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new ::wxPrintData(*data);
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
static sipEncodedTypeDef supers_wxPrintData[] = {{392, 255, 1}};


/* Define this type's Python slots. */
static sipPySlotDef slots_wxPrintData[] = {
    {(void *)slot_wxPrintData___bool__, bool_slot},
    {0, (sipPySlotType)0}
};


static PyMethodDef methods_wxPrintData[] = {
    {sipName_GetBin, meth_wxPrintData_GetBin, METH_VARARGS, doc_wxPrintData_GetBin},
    {sipName_GetCollate, meth_wxPrintData_GetCollate, METH_VARARGS, doc_wxPrintData_GetCollate},
    {sipName_GetColour, meth_wxPrintData_GetColour, METH_VARARGS, doc_wxPrintData_GetColour},
    {sipName_GetDuplex, meth_wxPrintData_GetDuplex, METH_VARARGS, doc_wxPrintData_GetDuplex},
    {sipName_GetFilename, meth_wxPrintData_GetFilename, METH_VARARGS, doc_wxPrintData_GetFilename},
    {sipName_GetNoCopies, meth_wxPrintData_GetNoCopies, METH_VARARGS, doc_wxPrintData_GetNoCopies},
    {sipName_GetOrientation, meth_wxPrintData_GetOrientation, METH_VARARGS, doc_wxPrintData_GetOrientation},
    {sipName_GetPaperId, meth_wxPrintData_GetPaperId, METH_VARARGS, doc_wxPrintData_GetPaperId},
    {sipName_GetPaperSize, meth_wxPrintData_GetPaperSize, METH_VARARGS, doc_wxPrintData_GetPaperSize},
    {sipName_GetPrintMode, meth_wxPrintData_GetPrintMode, METH_VARARGS, doc_wxPrintData_GetPrintMode},
    {sipName_GetPrinterName, meth_wxPrintData_GetPrinterName, METH_VARARGS, doc_wxPrintData_GetPrinterName},
    {sipName_GetPrivData, meth_wxPrintData_GetPrivData, METH_VARARGS, doc_wxPrintData_GetPrivData},
    {sipName_GetQuality, meth_wxPrintData_GetQuality, METH_VARARGS, doc_wxPrintData_GetQuality},
    {sipName_IsOk, meth_wxPrintData_IsOk, METH_VARARGS, doc_wxPrintData_IsOk},
    {sipName_SetBin, SIP_MLMETH_CAST(meth_wxPrintData_SetBin), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetBin},
    {sipName_SetCollate, SIP_MLMETH_CAST(meth_wxPrintData_SetCollate), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetCollate},
    {sipName_SetColour, SIP_MLMETH_CAST(meth_wxPrintData_SetColour), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetColour},
    {sipName_SetDuplex, SIP_MLMETH_CAST(meth_wxPrintData_SetDuplex), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetDuplex},
    {sipName_SetFilename, SIP_MLMETH_CAST(meth_wxPrintData_SetFilename), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetFilename},
    {sipName_SetNoCopies, SIP_MLMETH_CAST(meth_wxPrintData_SetNoCopies), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetNoCopies},
    {sipName_SetOrientation, SIP_MLMETH_CAST(meth_wxPrintData_SetOrientation), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetOrientation},
    {sipName_SetPaperId, SIP_MLMETH_CAST(meth_wxPrintData_SetPaperId), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetPaperId},
    {sipName_SetPaperSize, SIP_MLMETH_CAST(meth_wxPrintData_SetPaperSize), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetPaperSize},
    {sipName_SetPrintMode, SIP_MLMETH_CAST(meth_wxPrintData_SetPrintMode), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetPrintMode},
    {sipName_SetPrinterName, SIP_MLMETH_CAST(meth_wxPrintData_SetPrinterName), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetPrinterName},
    {sipName_SetPrivData, SIP_MLMETH_CAST(meth_wxPrintData_SetPrivData), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetPrivData},
    {sipName_SetQuality, SIP_MLMETH_CAST(meth_wxPrintData_SetQuality), METH_VARARGS|METH_KEYWORDS, doc_wxPrintData_SetQuality},
    {sipName___nonzero__, meth_wxPrintData___nonzero__, METH_VARARGS, doc_wxPrintData___nonzero__}
};

sipVariableDef variables_wxPrintData[] = {
    {PropertyVariable, sipName_Quality, &methods_wxPrintData[12], &methods_wxPrintData[26], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_PrivData, &methods_wxPrintData[11], &methods_wxPrintData[25], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_PrinterName, &methods_wxPrintData[10], &methods_wxPrintData[24], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_PrintMode, &methods_wxPrintData[9], &methods_wxPrintData[23], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_PaperSize, &methods_wxPrintData[8], &methods_wxPrintData[22], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_PaperId, &methods_wxPrintData[7], &methods_wxPrintData[21], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Orientation, &methods_wxPrintData[6], &methods_wxPrintData[20], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_NoCopies, &methods_wxPrintData[5], &methods_wxPrintData[19], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Filename, &methods_wxPrintData[4], &methods_wxPrintData[18], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Duplex, &methods_wxPrintData[3], &methods_wxPrintData[17], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Colour, &methods_wxPrintData[2], &methods_wxPrintData[16], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Collate, &methods_wxPrintData[1], &methods_wxPrintData[15], SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_Bin, &methods_wxPrintData[0], &methods_wxPrintData[14], SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxPrintData, "PrintData() -> None\n"
"PrintData(data) -> None\n"
"\n"
"This class holds a variety of information related to printers and\n"
"printer device contexts.");


sipClassTypeDef sipTypeDef__core_wxPrintData = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxPrintData,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_PrintData,
        {0, 0, 1},
        28, methods_wxPrintData,
        0, SIP_NULLPTR,
        13, variables_wxPrintData,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxPrintData,
    -1,
    -1,
    supers_wxPrintData,
    slots_wxPrintData,
    init_type_wxPrintData,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxPrintData,
    assign_wxPrintData,
    array_wxPrintData,
    copy_wxPrintData,
    release_wxPrintData,
    cast_wxPrintData,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxPrintData,
    sizeof (::wxPrintData),
};
