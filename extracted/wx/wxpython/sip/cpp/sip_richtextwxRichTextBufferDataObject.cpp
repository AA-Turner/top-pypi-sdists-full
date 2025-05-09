/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_richtext.h"
        #include <wx/richtext/richtextbuffer.h>
        #include <wx/richtext/richtextbuffer.h>
        #include <wx/dataobj.h>
        #include <wx/dataobj.h>


class sipwxRichTextBufferDataObject : public ::wxRichTextBufferDataObject
{
public:
    sipwxRichTextBufferDataObject(::wxRichTextBuffer*);
    virtual ~sipwxRichTextBufferDataObject();

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    bool SetData(const ::wxDataFormat&, size_t, const void*) SIP_OVERRIDE;
    ::wxDataFormat GetPreferredFormat(::wxDataObject::Direction) const SIP_OVERRIDE;
    size_t GetFormatCount(::wxDataObject::Direction) const SIP_OVERRIDE;
    size_t GetDataSize(const ::wxDataFormat&) const SIP_OVERRIDE;
    bool GetDataHere(const ::wxDataFormat&, void*) const SIP_OVERRIDE;
    void GetAllFormats(::wxDataFormat*, ::wxDataObject::Direction) const SIP_OVERRIDE;
    bool GetDataHere(void*) const SIP_OVERRIDE;
    size_t GetDataSize() const SIP_OVERRIDE;
    bool SetData(size_t, const void*) SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxRichTextBufferDataObject(const sipwxRichTextBufferDataObject &);
    sipwxRichTextBufferDataObject &operator = (const sipwxRichTextBufferDataObject &);

    char sipPyMethods[9];
};

sipwxRichTextBufferDataObject::sipwxRichTextBufferDataObject(::wxRichTextBuffer*richTextBuffer): ::wxRichTextBufferDataObject(richTextBuffer), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxRichTextBufferDataObject::~sipwxRichTextBufferDataObject()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

bool sipwxRichTextBufferDataObject::SetData(const ::wxDataFormat& format, size_t len, const void*buf)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[0], &sipPySelf, SIP_NULLPTR, sipName_SetData);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::SetData(format, len, buf);

    extern bool sipVH__richtext_124(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxDataFormat&, size_t, const void*);

    return sipVH__richtext_124(sipGILState, 0, sipPySelf, sipMeth, format, len, buf);
}

::wxDataFormat sipwxRichTextBufferDataObject::GetPreferredFormat(::wxDataObject::Direction dir) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[1]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetPreferredFormat);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::GetPreferredFormat(dir);

    extern ::wxDataFormat sipVH__richtext_123(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxDataObject::Direction);

    return sipVH__richtext_123(sipGILState, 0, sipPySelf, sipMeth, dir);
}

size_t sipwxRichTextBufferDataObject::GetFormatCount(::wxDataObject::Direction dir) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[2]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetFormatCount);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::GetFormatCount(dir);

    extern size_t sipVH__richtext_122(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxDataObject::Direction);

    return sipVH__richtext_122(sipGILState, 0, sipPySelf, sipMeth, dir);
}

size_t sipwxRichTextBufferDataObject::GetDataSize(const ::wxDataFormat& format) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[3]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetDataSize);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::GetDataSize(format);

    extern size_t sipVH__richtext_121(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxDataFormat&);

    return sipVH__richtext_121(sipGILState, 0, sipPySelf, sipMeth, format);
}

bool sipwxRichTextBufferDataObject::GetDataHere(const ::wxDataFormat& format, void*buf) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[4]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetDataHere);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::GetDataHere(format, buf);

    extern bool sipVH__richtext_120(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxDataFormat&, void*);

    return sipVH__richtext_120(sipGILState, 0, sipPySelf, sipMeth, format, buf);
}

void sipwxRichTextBufferDataObject::GetAllFormats(::wxDataFormat*formats, ::wxDataObject::Direction dir) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[5]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetAllFormats);

    if (!sipMeth)
    {
        ::wxRichTextBufferDataObject::GetAllFormats(formats, dir);
        return;
    }

    extern void sipVH__richtext_119(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxDataFormat*, ::wxDataObject::Direction);

    sipVH__richtext_119(sipGILState, 0, sipPySelf, sipMeth, formats, dir);
}

bool sipwxRichTextBufferDataObject::GetDataHere(void*buf) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[6]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetDataHere);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::GetDataHere(buf);

    extern bool sipVH__richtext_118(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, void*);

    return sipVH__richtext_118(sipGILState, 0, sipPySelf, sipMeth, buf);
}

size_t sipwxRichTextBufferDataObject::GetDataSize() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[7]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetDataSize);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::GetDataSize();

    extern size_t sipVH__richtext_100(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__richtext_100(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxRichTextBufferDataObject::SetData(size_t len, const void*buf)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[8], &sipPySelf, SIP_NULLPTR, sipName_SetData);

    if (!sipMeth)
        return ::wxRichTextBufferDataObject::SetData(len, buf);

    extern bool sipVH__richtext_117(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, size_t, const void*);

    return sipVH__richtext_117(sipGILState, 0, sipPySelf, sipMeth, len, buf);
}


PyDoc_STRVAR(doc_wxRichTextBufferDataObject_GetRichTextBuffer, "GetRichTextBuffer() -> RichTextBuffer\n"
"\n"
"After a call to this function, the buffer is owned by the caller and\n"
"it is responsible for deleting it.");

extern "C" {static PyObject *meth_wxRichTextBufferDataObject_GetRichTextBuffer(PyObject *, PyObject *);}
static PyObject *meth_wxRichTextBufferDataObject_GetRichTextBuffer(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        ::wxRichTextBufferDataObject *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp))
        {
            ::wxRichTextBuffer*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetRichTextBuffer();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromType(sipRes, sipType_wxRichTextBuffer, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_RichTextBufferDataObject, sipName_GetRichTextBuffer, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxRichTextBufferDataObject_GetPreferredFormat, "GetPreferredFormat(dir) -> wx.DataFormat\n"
"\n"
"Returns the preferred format for either rendering the data (if dir is\n"
"Get, its default value) or for setting it.");

extern "C" {static PyObject *meth_wxRichTextBufferDataObject_GetPreferredFormat(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxRichTextBufferDataObject_GetPreferredFormat(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxDataObject::Direction dir;
        const ::wxRichTextBufferDataObject *sipCpp;

        static const char *sipKwdList[] = {
            sipName_dir,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BE", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp, sipType_wxDataObject_Direction, &dir))
        {
            ::wxDataFormat*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxDataFormat((sipSelfWasArg ? sipCpp->::wxRichTextBufferDataObject::GetPreferredFormat(dir) : sipCpp->GetPreferredFormat(dir)));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxDataFormat, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_RichTextBufferDataObject, sipName_GetPreferredFormat, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxRichTextBufferDataObject_GetDataSize, "GetDataSize() -> int\n"
"GetDataSize(format) -> int\n"
"\n"
"Gets the size of our data.\n"
"");

extern "C" {static PyObject *meth_wxRichTextBufferDataObject_GetDataSize(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxRichTextBufferDataObject_GetDataSize(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxRichTextBufferDataObject *sipCpp;

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, SIP_NULLPTR, "B", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp))
        {
            size_t sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxRichTextBufferDataObject::GetDataSize() : sipCpp->GetDataSize());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromUnsignedLong(sipRes);
        }
    }

    {
        const ::wxDataFormat* format;
        const ::wxRichTextBufferDataObject *sipCpp;

        static const char *sipKwdList[] = {
            sipName_format,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp, sipType_wxDataFormat, &format))
        {
            size_t sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxRichTextBufferDataObject::GetDataSize(*format) : sipCpp->GetDataSize(*format));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromUnsignedLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_RichTextBufferDataObject, sipName_GetDataSize, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxRichTextBufferDataObject_GetDataHere, "GetDataHere(buf) -> bool\n"
"GetDataHere(format, buf) -> bool\n"
"\n"
"Copy the data to the buffer, return true on success.\n"
"");

extern "C" {static PyObject *meth_wxRichTextBufferDataObject_GetDataHere(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxRichTextBufferDataObject_GetDataHere(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        void* buf;
        const ::wxRichTextBufferDataObject *sipCpp;

        static const char *sipKwdList[] = {
            sipName_buf,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "Bv", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp, &buf))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxRichTextBufferDataObject::GetDataHere(buf) : sipCpp->GetDataHere(buf));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    {
        const ::wxDataFormat* format;
        void* buf;
        const ::wxRichTextBufferDataObject *sipCpp;

        static const char *sipKwdList[] = {
            sipName_format,
            sipName_buf,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9v", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp, sipType_wxDataFormat, &format, &buf))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxRichTextBufferDataObject::GetDataHere(*format, buf) : sipCpp->GetDataHere(*format, buf));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_RichTextBufferDataObject, sipName_GetDataHere, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxRichTextBufferDataObject_SetData, "SetData(len, buf) -> bool\n"
"SetData(format, len, buf) -> bool\n"
"\n"
"Copy the data from the buffer, return true on success.\n"
"");

extern "C" {static PyObject *meth_wxRichTextBufferDataObject_SetData(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxRichTextBufferDataObject_SetData(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        size_t len;
        const void* buf;
        ::wxRichTextBufferDataObject *sipCpp;

        static const char *sipKwdList[] = {
            sipName_len,
            sipName_buf,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "B=v", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp, &len, &buf))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxRichTextBufferDataObject::SetData(len, buf) : sipCpp->SetData(len, buf));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    {
        const ::wxDataFormat* format;
        size_t len;
        const void* buf;
        ::wxRichTextBufferDataObject *sipCpp;

        static const char *sipKwdList[] = {
            sipName_format,
            sipName_len,
            sipName_buf,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9=v", &sipSelf, sipType_wxRichTextBufferDataObject, &sipCpp, sipType_wxDataFormat, &format, &len, &buf))
        {
            bool sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxRichTextBufferDataObject::SetData(*format, len, buf) : sipCpp->SetData(*format, len, buf));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyBool_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_RichTextBufferDataObject, sipName_SetData, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxRichTextBufferDataObject_GetRichTextBufferFormatId, "GetRichTextBufferFormatId() -> str\n"
"\n"
"Returns the id for the new data format.");

extern "C" {static PyObject *meth_wxRichTextBufferDataObject_GetRichTextBufferFormatId(PyObject *, PyObject *);}
static PyObject *meth_wxRichTextBufferDataObject_GetRichTextBufferFormatId(PyObject *, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        if (sipParseArgs(&sipParseErr, sipArgs, ""))
        {
            const ::wxChar*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = ::wxRichTextBufferDataObject::GetRichTextBufferFormatId();
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            if (sipRes == SIP_NULLPTR)
            {
                Py_INCREF(Py_None);
                return Py_None;
            }

            return PyUnicode_FromWideChar(sipRes, (Py_ssize_t)wcslen(sipRes));
        }
    }

    sipNoMethod(sipParseErr, sipName_RichTextBufferDataObject, sipName_GetRichTextBufferFormatId, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxRichTextBufferDataObject(void *, const sipTypeDef *);}
static void *cast_wxRichTextBufferDataObject(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxRichTextBufferDataObject *sipCpp = reinterpret_cast<::wxRichTextBufferDataObject *>(sipCppV);

    if (targetType == sipType_wxRichTextBufferDataObject)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxDataObjectSimple)->ctd_cast(static_cast<::wxDataObjectSimple *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxRichTextBufferDataObject(void *, int);}
static void release_wxRichTextBufferDataObject(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxRichTextBufferDataObject *>(sipCppV);
    else
        delete reinterpret_cast<::wxRichTextBufferDataObject *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxRichTextBufferDataObject(Py_ssize_t);}
static void *array_wxRichTextBufferDataObject(Py_ssize_t sipNrElem)
{
    return new ::wxRichTextBufferDataObject[sipNrElem];
}


extern "C" {static void array_delete_wxRichTextBufferDataObject(void *);}
static void array_delete_wxRichTextBufferDataObject(void *sipCpp)
{
    delete[] reinterpret_cast<::wxRichTextBufferDataObject *>(sipCpp);
}


extern "C" {static void dealloc_wxRichTextBufferDataObject(sipSimpleWrapper *);}
static void dealloc_wxRichTextBufferDataObject(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxRichTextBufferDataObject *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxRichTextBufferDataObject(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxRichTextBufferDataObject(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxRichTextBufferDataObject(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxRichTextBufferDataObject *sipCpp = SIP_NULLPTR;

    {
        ::wxRichTextBuffer* richTextBuffer = 0;

        static const char *sipKwdList[] = {
            sipName_richTextBuffer,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "|J8", sipType_wxRichTextBuffer, &richTextBuffer))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxRichTextBufferDataObject(richTextBuffer);
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
static sipEncodedTypeDef supers_wxRichTextBufferDataObject[] = {{21, 0, 1}};


static PyMethodDef methods_wxRichTextBufferDataObject[] = {
    {sipName_GetDataHere, SIP_MLMETH_CAST(meth_wxRichTextBufferDataObject_GetDataHere), METH_VARARGS|METH_KEYWORDS, doc_wxRichTextBufferDataObject_GetDataHere},
    {sipName_GetDataSize, SIP_MLMETH_CAST(meth_wxRichTextBufferDataObject_GetDataSize), METH_VARARGS|METH_KEYWORDS, doc_wxRichTextBufferDataObject_GetDataSize},
    {sipName_GetPreferredFormat, SIP_MLMETH_CAST(meth_wxRichTextBufferDataObject_GetPreferredFormat), METH_VARARGS|METH_KEYWORDS, doc_wxRichTextBufferDataObject_GetPreferredFormat},
    {sipName_GetRichTextBuffer, meth_wxRichTextBufferDataObject_GetRichTextBuffer, METH_VARARGS, doc_wxRichTextBufferDataObject_GetRichTextBuffer},
    {sipName_GetRichTextBufferFormatId, meth_wxRichTextBufferDataObject_GetRichTextBufferFormatId, METH_VARARGS, doc_wxRichTextBufferDataObject_GetRichTextBufferFormatId},
    {sipName_SetData, SIP_MLMETH_CAST(meth_wxRichTextBufferDataObject_SetData), METH_VARARGS|METH_KEYWORDS, doc_wxRichTextBufferDataObject_SetData}
};

sipVariableDef variables_wxRichTextBufferDataObject[] = {
    {PropertyVariable, sipName_RichTextBuffer, &methods_wxRichTextBufferDataObject[3], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    {PropertyVariable, sipName_DataSize, &methods_wxRichTextBufferDataObject[1], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxRichTextBufferDataObject, "RichTextBufferDataObject(richTextBuffer=None) -> None\n"
"\n"
"Implements a rich text data object for clipboard transfer.");


sipClassTypeDef sipTypeDef__richtext_wxRichTextBufferDataObject = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_CLASS,
        sipNameNr_wxRichTextBufferDataObject,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_RichTextBufferDataObject,
        {0, 0, 1},
        6, methods_wxRichTextBufferDataObject,
        0, SIP_NULLPTR,
        2, variables_wxRichTextBufferDataObject,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxRichTextBufferDataObject,
    -1,
    -1,
    supers_wxRichTextBufferDataObject,
    SIP_NULLPTR,
    init_type_wxRichTextBufferDataObject,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxRichTextBufferDataObject,
    SIP_NULLPTR,
    array_wxRichTextBufferDataObject,
    SIP_NULLPTR,
    release_wxRichTextBufferDataObject,
    cast_wxRichTextBufferDataObject,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxRichTextBufferDataObject,
    sizeof (::wxRichTextBufferDataObject),
};
