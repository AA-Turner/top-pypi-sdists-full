/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/clipbrd.h>
        #include <wx/dataobj.h>
        #include <wx/dataobj.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


class sipwxClipboard : public ::wxClipboard
{
public:
    sipwxClipboard();
    sipwxClipboard(const ::wxClipboard&);
    virtual ~sipwxClipboard();

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    void UsePrimarySelection(bool) SIP_OVERRIDE;
    bool SetData(::wxDataObject*) SIP_OVERRIDE;
    bool Open() SIP_OVERRIDE;
    bool IsSupported(const ::wxDataFormat&) SIP_OVERRIDE;
    bool IsOpened() const SIP_OVERRIDE;
    bool GetData(::wxDataObject&) SIP_OVERRIDE;
    bool Flush() SIP_OVERRIDE;
    void Close() SIP_OVERRIDE;
    void Clear() SIP_OVERRIDE;
    bool AddData(::wxDataObject*) SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxClipboard(const sipwxClipboard &);
    sipwxClipboard &operator = (const sipwxClipboard &);

    char sipPyMethods[10];
};

sipwxClipboard::sipwxClipboard(): ::wxClipboard(), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxClipboard::sipwxClipboard(const ::wxClipboard& a0): ::wxClipboard(a0), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxClipboard::~sipwxClipboard()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

void sipwxClipboard::UsePrimarySelection(bool primary)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[0], &sipPySelf, SIP_NULLPTR, sipName_UsePrimarySelection);

    if (!sipMeth)
    {
        ::wxClipboard::UsePrimarySelection(primary);
        return;
    }

    extern void sipVH__core_96(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, bool);

    sipVH__core_96(sipGILState, 0, sipPySelf, sipMeth, primary);
}

bool sipwxClipboard::SetData(::wxDataObject*data)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[1], &sipPySelf, SIP_NULLPTR, sipName_SetData);

    if (!sipMeth)
        return ::wxClipboard::SetData(data);

    extern bool sipVH__core_93(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxDataObject*);

    return sipVH__core_93(sipGILState, 0, sipPySelf, sipMeth, data);
}

bool sipwxClipboard::Open()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[2], &sipPySelf, SIP_NULLPTR, sipName_Open);

    if (!sipMeth)
        return ::wxClipboard::Open();

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxClipboard::IsSupported(const ::wxDataFormat& format)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[3], &sipPySelf, SIP_NULLPTR, sipName_IsSupported);

    if (!sipMeth)
        return ::wxClipboard::IsSupported(format);

    extern bool sipVH__core_95(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxDataFormat&);

    return sipVH__core_95(sipGILState, 0, sipPySelf, sipMeth, format);
}

bool sipwxClipboard::IsOpened() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[4]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_IsOpened);

    if (!sipMeth)
        return ::wxClipboard::IsOpened();

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxClipboard::GetData(::wxDataObject& data)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[5], &sipPySelf, SIP_NULLPTR, sipName_GetData);

    if (!sipMeth)
        return ::wxClipboard::GetData(data);

    extern bool sipVH__core_94(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxDataObject&);

    return sipVH__core_94(sipGILState, 0, sipPySelf, sipMeth, data);
}

bool sipwxClipboard::Flush()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[6], &sipPySelf, SIP_NULLPTR, sipName_Flush);

    if (!sipMeth)
        return ::wxClipboard::Flush();

    extern bool sipVH__core_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__core_6(sipGILState, 0, sipPySelf, sipMeth);
}

void sipwxClipboard::Close()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[7], &sipPySelf, SIP_NULLPTR, sipName_Close);

    if (!sipMeth)
    {
        ::wxClipboard::Close();
        return;
    }

    extern void sipVH__core_57(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    sipVH__core_57(sipGILState, 0, sipPySelf, sipMeth);
}

void sipwxClipboard::Clear()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[8], &sipPySelf, SIP_NULLPTR, sipName_Clear);

    if (!sipMeth)
    {
        ::wxClipboard::Clear();
        return;
    }

    extern void sipVH__core_57(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    sipVH__core_57(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxClipboard::AddData(::wxDataObject*data)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[9], &sipPySelf, SIP_NULLPTR, sipName_AddData);

    if (!sipMeth)
        return ::wxClipboard::AddData(data);

    extern bool sipVH__core_93(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxDataObject*);

    return sipVH__core_93(sipGILState, 0, sipPySelf, sipMeth, data);
}


PyDoc_STRVAR(doc_wxClipboard_AddData, "AddData(data) -> bool\n"
"\n"
"Call this function to add the data object to the clipboard.");

extern "C" {static PyObject *meth_wxClipboard_AddData(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_AddData(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxDataObject* data;
        ::wxClipboard *sipCpp;

        static const char *sipKwdList[] = {
            sipName_data,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ:", &sipSelf, sipType_wxClipboard, &sipCpp, sipType_wxDataObject, &data))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxClipboard::AddData(data) : sipCpp->AddData(data));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_AddData, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_Clear, "Clear() -> None\n"
"\n"
"Clears the global clipboard object and the system's clipboard if possible.");

extern "C" {static PyObject *meth_wxClipboard_Clear(PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_Clear(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxClipboard *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxClipboard, &sipCpp))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            (sipSelfWasArg ? sipCpp->::wxClipboard::Clear() : sipCpp->Clear());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_Clear, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_Close, "Close() -> None\n"
"\n"
"Call this function to close the clipboard, having opened it with\n"
"Open().");

extern "C" {static PyObject *meth_wxClipboard_Close(PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_Close(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxClipboard *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxClipboard, &sipCpp))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            (sipSelfWasArg ? sipCpp->::wxClipboard::Close() : sipCpp->Close());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_Close, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_Flush, "Flush() -> bool\n"
"\n"
"Flushes the clipboard: this means that the data which is currently on clipboard will stay available even after the application exits (possibly eating memory), otherwise the clipboard will be emptied on exit.");

extern "C" {static PyObject *meth_wxClipboard_Flush(PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_Flush(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxClipboard *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxClipboard, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxClipboard::Flush() : sipCpp->Flush());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_Flush, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_GetData, "GetData(data) -> bool\n"
"\n"
"Call this function to fill data with data on the clipboard, if\n"
"available in the required format.");

extern "C" {static PyObject *meth_wxClipboard_GetData(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_GetData(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxDataObject* data;
        ::wxClipboard *sipCpp;

        static const char *sipKwdList[] = {
            sipName_data,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9", &sipSelf, sipType_wxClipboard, &sipCpp, sipType_wxDataObject, &data))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxClipboard::GetData(*data) : sipCpp->GetData(*data));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_GetData, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_IsOpened, "IsOpened() -> bool\n"
"\n"
"Returns true if the clipboard has been opened.");

extern "C" {static PyObject *meth_wxClipboard_IsOpened(PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_IsOpened(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxClipboard *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxClipboard, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxClipboard::IsOpened() : sipCpp->IsOpened());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_IsOpened, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_IsSupported, "IsSupported(format) -> bool\n"
"\n"
"Returns true if there is data which matches the data format of the\n"
"given data object currently available on the clipboard.");

extern "C" {static PyObject *meth_wxClipboard_IsSupported(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_IsSupported(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxDataFormat* format;
        ::wxClipboard *sipCpp;

        static const char *sipKwdList[] = {
            sipName_format,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9", &sipSelf, sipType_wxClipboard, &sipCpp, sipType_wxDataFormat, &format))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxClipboard::IsSupported(*format) : sipCpp->IsSupported(*format));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_IsSupported, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_IsUsingPrimarySelection, "IsUsingPrimarySelection() -> bool\n"
"\n"
"Returns true if we are using the primary selection, false if clipboard\n"
"one.");

extern "C" {static PyObject *meth_wxClipboard_IsUsingPrimarySelection(PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_IsUsingPrimarySelection(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxClipboard *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxClipboard, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->IsUsingPrimarySelection();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_IsUsingPrimarySelection, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_Open, "Open() -> bool\n"
"\n"
"Call this function to open the clipboard before calling SetData() and\n"
"GetData().");

extern "C" {static PyObject *meth_wxClipboard_Open(PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_Open(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxClipboard *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxClipboard, &sipCpp))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxClipboard::Open() : sipCpp->Open());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_Open, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_SetData, "SetData(data) -> bool\n"
"\n"
"Call this function to set the data object to the clipboard.");

extern "C" {static PyObject *meth_wxClipboard_SetData(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_SetData(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxDataObject* data;
        ::wxClipboard *sipCpp;

        static const char *sipKwdList[] = {
            sipName_data,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ:", &sipSelf, sipType_wxClipboard, &sipCpp, sipType_wxDataObject, &data))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxClipboard::SetData(data) : sipCpp->SetData(data));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_SetData, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_UsePrimarySelection, "UsePrimarySelection(primary=False) -> None\n"
"\n"
"On platforms supporting it (all X11-based ports), wxClipboard uses the\n"
"CLIPBOARD X11 selection by default.");

extern "C" {static PyObject *meth_wxClipboard_UsePrimarySelection(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_UsePrimarySelection(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        bool primary = 0;
        ::wxClipboard *sipCpp;

        static const char *sipKwdList[] = {
            sipName_primary,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "B|b", &sipSelf, sipType_wxClipboard, &sipCpp, &primary))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            (sipSelfWasArg ? sipCpp->::wxClipboard::UsePrimarySelection(primary) : sipCpp->UsePrimarySelection(primary));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_UsePrimarySelection, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxClipboard_Get, "Get() -> Clipboard\n"
"\n"
"Returns the global instance (wxTheClipboard) of the clipboard object.");

extern "C" {static PyObject *meth_wxClipboard_Get(PyObject *, PyObject *);}
static PyObject *meth_wxClipboard_Get(PyObject *, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        if (sipParseArgs(&sipParseErr, sipArgs, ""))
        {
            ::wxClipboard*sipRes;
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = ::wxClipboard::Get();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxClipboard, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_Clipboard, sipName_Get, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxClipboard(void *, const sipTypeDef *);}
static void *cast_wxClipboard(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxClipboard *sipCpp = reinterpret_cast<::wxClipboard *>(sipCppV);

    if (targetType == sipType_wxClipboard)
        return sipCppV;

    if (targetType == sipType_wxObject)
        return static_cast<::wxObject *>(sipCpp);

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxClipboard(void *, int);}
static void release_wxClipboard(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxClipboard *>(sipCppV);
    else
        delete reinterpret_cast<::wxClipboard *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxClipboard(Py_ssize_t);}
static void *array_wxClipboard(Py_ssize_t sipNrElem)
{
    return new ::wxClipboard[sipNrElem];
}


extern "C" {static void array_delete_wxClipboard(void *);}
static void array_delete_wxClipboard(void *sipCpp)
{
    delete[] reinterpret_cast<::wxClipboard *>(sipCpp);
}


extern "C" {static void assign_wxClipboard(void *, Py_ssize_t, void *);}
static void assign_wxClipboard(void *sipDst, Py_ssize_t sipDstIdx, void *sipSrc)
{
    reinterpret_cast<::wxClipboard *>(sipDst)[sipDstIdx] = *reinterpret_cast<::wxClipboard *>(sipSrc);
}


extern "C" {static void *copy_wxClipboard(const void *, Py_ssize_t);}
static void *copy_wxClipboard(const void *sipSrc, Py_ssize_t sipSrcIdx)
{
    return new ::wxClipboard(reinterpret_cast<const ::wxClipboard *>(sipSrc)[sipSrcIdx]);
}


extern "C" {static void dealloc_wxClipboard(sipSimpleWrapper *);}
static void dealloc_wxClipboard(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxClipboard *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxClipboard(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxClipboard(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxClipboard(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxClipboard *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxClipboard();
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
        const ::wxClipboard* a0;

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, "J9", sipType_wxClipboard, &a0))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxClipboard(*a0);
            Py_END_ALLOW_THREADS

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}


/* Define this type's super-types. */
static sipEncodedTypeDef supers_wxClipboard[] = {{392, 255, 1}};


static PyMethodDef methods_wxClipboard[] = {
    {sipName_AddData, SIP_MLMETH_CAST(meth_wxClipboard_AddData), METH_VARARGS|METH_KEYWORDS, doc_wxClipboard_AddData},
    {sipName_Clear, meth_wxClipboard_Clear, METH_VARARGS, doc_wxClipboard_Clear},
    {sipName_Close, meth_wxClipboard_Close, METH_VARARGS, doc_wxClipboard_Close},
    {sipName_Flush, meth_wxClipboard_Flush, METH_VARARGS, doc_wxClipboard_Flush},
    {sipName_Get, meth_wxClipboard_Get, METH_VARARGS, doc_wxClipboard_Get},
    {sipName_GetData, SIP_MLMETH_CAST(meth_wxClipboard_GetData), METH_VARARGS|METH_KEYWORDS, doc_wxClipboard_GetData},
    {sipName_IsOpened, meth_wxClipboard_IsOpened, METH_VARARGS, doc_wxClipboard_IsOpened},
    {sipName_IsSupported, SIP_MLMETH_CAST(meth_wxClipboard_IsSupported), METH_VARARGS|METH_KEYWORDS, doc_wxClipboard_IsSupported},
    {sipName_IsUsingPrimarySelection, meth_wxClipboard_IsUsingPrimarySelection, METH_VARARGS, doc_wxClipboard_IsUsingPrimarySelection},
    {sipName_Open, meth_wxClipboard_Open, METH_VARARGS, doc_wxClipboard_Open},
    {sipName_SetData, SIP_MLMETH_CAST(meth_wxClipboard_SetData), METH_VARARGS|METH_KEYWORDS, doc_wxClipboard_SetData},
    {sipName_UsePrimarySelection, SIP_MLMETH_CAST(meth_wxClipboard_UsePrimarySelection), METH_VARARGS|METH_KEYWORDS, doc_wxClipboard_UsePrimarySelection}
};

PyDoc_STRVAR(doc_wxClipboard, "Clipboard() -> None\n"
"\n"
"A class for manipulating the clipboard.");


sipClassTypeDef sipTypeDef__core_wxClipboard = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxClipboard,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_Clipboard,
        {0, 0, 1},
        12, methods_wxClipboard,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxClipboard,
    -1,
    -1,
    supers_wxClipboard,
    SIP_NULLPTR,
    init_type_wxClipboard,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxClipboard,
    assign_wxClipboard,
    array_wxClipboard,
    copy_wxClipboard,
    release_wxClipboard,
    cast_wxClipboard,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxClipboard,
    sizeof (::wxClipboard),
};
