/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_propgrid.h"
        #include <wx/propgrid/property.h>
        #include <wx/window.h>
        #include <wx/font.h>
        #include <wx/propgrid/property.h>
        #include <wx/bmpbndl.h>
        #include <wx/validate.h>
        #include <wx/colour.h>
        #include <wx/propgrid/property.h>
        #include <wx/propgrid/property.h>
        #include <wx/propgrid/editors.h>
        #include <wx/bitmap.h>
        #include <wx/propgrid/propgrid.h>
        #include <wx/propgrid/editors.h>
        #include <wx/propgrid/property.h>
        #include <wx/dc.h>
        #include <wx/gdicmn.h>
        #include <wx/propgrid/property.h>
        #include <wx/event.h>
        #include <wx/gdicmn.h>
        #include <wx/propgrid/propgrid.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


class sipwxPropertyCategory : public ::wxPropertyCategory
{
public:
    sipwxPropertyCategory();
    sipwxPropertyCategory(const ::wxString&, const ::wxString&);
    sipwxPropertyCategory(const ::wxPropertyCategory&);
    virtual ~sipwxPropertyCategory();

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    void OnSetValue() SIP_OVERRIDE;
    ::wxPGVariant DoGetValue() const SIP_OVERRIDE;
    bool ValidateValue(::wxPGVariant&, ::wxPGValidationInfo&) const SIP_OVERRIDE;
    bool StringToValue(::wxPGVariant&, const ::wxString&, int) const SIP_OVERRIDE;
    bool IntToValue(::wxPGVariant&, int, int) const SIP_OVERRIDE;
    ::wxString ValueToString(::wxPGVariant&, int) const SIP_OVERRIDE;
    ::wxSize OnMeasureImage(int) const SIP_OVERRIDE;
    bool OnEvent(::wxPropertyGrid*, ::wxWindow*, ::wxEvent&) SIP_OVERRIDE;
    ::wxPGVariant ChildChanged(::wxPGVariant&, int, ::wxPGVariant&) const SIP_OVERRIDE;
    const ::wxPGEditor* DoGetEditorClass() const SIP_OVERRIDE;
    ::wxValidator* DoGetValidator() const SIP_OVERRIDE;
    void OnCustomPaint(::wxDC&, const ::wxRect&, ::wxPGPaintData&) SIP_OVERRIDE;
    ::wxPGCellRenderer* GetCellRenderer(int) const SIP_OVERRIDE;
    int GetChoiceSelection() const SIP_OVERRIDE;
    void RefreshChildren() SIP_OVERRIDE;
    bool DoSetAttribute(const ::wxString&, ::wxPGVariant&) SIP_OVERRIDE;
    ::wxPGVariant DoGetAttribute(const ::wxString&) const SIP_OVERRIDE;
    ::wxPGEditorDialogAdapter* GetEditorDialog() const SIP_OVERRIDE;
    void OnValidationFailure(::wxPGVariant&) SIP_OVERRIDE;
    ::wxString GetValueAsString(int) const SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxPropertyCategory(const sipwxPropertyCategory &);
    sipwxPropertyCategory &operator = (const sipwxPropertyCategory &);

    char sipPyMethods[20];
};

sipwxPropertyCategory::sipwxPropertyCategory(): ::wxPropertyCategory(), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxPropertyCategory::sipwxPropertyCategory(const ::wxString& label, const ::wxString& name): ::wxPropertyCategory(label, name), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxPropertyCategory::sipwxPropertyCategory(const ::wxPropertyCategory& a0): ::wxPropertyCategory(a0), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxPropertyCategory::~sipwxPropertyCategory()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

void sipwxPropertyCategory::OnSetValue()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[0], &sipPySelf, SIP_NULLPTR, sipName_OnSetValue);

    if (!sipMeth)
    {
        ::wxPropertyCategory::OnSetValue();
        return;
    }

    extern void sipVH__propgrid_3(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    sipVH__propgrid_3(sipGILState, 0, sipPySelf, sipMeth);
}

::wxPGVariant sipwxPropertyCategory::DoGetValue() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[1]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_DoGetValue);

    if (!sipMeth)
        return ::wxPropertyCategory::DoGetValue();

    extern ::wxPGVariant sipVH__propgrid_4(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__propgrid_4(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxPropertyCategory::ValidateValue(::wxPGVariant& value, ::wxPGValidationInfo& validationInfo) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[2]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_ValidateValue);

    if (!sipMeth)
        return ::wxPropertyCategory::ValidateValue(value, validationInfo);

    extern bool sipVH__propgrid_5(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxPGVariant&, ::wxPGValidationInfo&);

    return sipVH__propgrid_5(sipGILState, 0, sipPySelf, sipMeth, value, validationInfo);
}

bool sipwxPropertyCategory::StringToValue(::wxPGVariant& variant, const ::wxString& text, int argFlags) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[3]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_StringToValue);

    if (!sipMeth)
        return ::wxPropertyCategory::StringToValue(variant, text, argFlags);

    extern bool sipVH__propgrid_6(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxPGVariant&, const ::wxString&, int);

    return sipVH__propgrid_6(sipGILState, 0, sipPySelf, sipMeth, variant, text, argFlags);
}

bool sipwxPropertyCategory::IntToValue(::wxPGVariant& variant, int number, int argFlags) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[4]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_IntToValue);

    if (!sipMeth)
        return ::wxPropertyCategory::IntToValue(variant, number, argFlags);

    extern bool sipVH__propgrid_7(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxPGVariant&, int, int);

    return sipVH__propgrid_7(sipGILState, 0, sipPySelf, sipMeth, variant, number, argFlags);
}

::wxString sipwxPropertyCategory::ValueToString(::wxPGVariant& value, int argFlags) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[5]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_ValueToString);

    if (!sipMeth)
        return ::wxPropertyCategory::ValueToString(value, argFlags);

    extern ::wxString sipVH__propgrid_8(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxPGVariant&, int);

    return sipVH__propgrid_8(sipGILState, 0, sipPySelf, sipMeth, value, argFlags);
}

::wxSize sipwxPropertyCategory::OnMeasureImage(int item) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[6]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_OnMeasureImage);

    if (!sipMeth)
        return ::wxPropertyCategory::OnMeasureImage(item);

    extern ::wxSize sipVH__propgrid_9(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, int);

    return sipVH__propgrid_9(sipGILState, 0, sipPySelf, sipMeth, item);
}

bool sipwxPropertyCategory::OnEvent(::wxPropertyGrid*propgrid, ::wxWindow*wnd_primary, ::wxEvent& event)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[7], &sipPySelf, SIP_NULLPTR, sipName_OnEvent);

    if (!sipMeth)
        return ::wxPropertyCategory::OnEvent(propgrid, wnd_primary, event);

    extern bool sipVH__propgrid_10(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxPropertyGrid*, ::wxWindow*, ::wxEvent&);

    return sipVH__propgrid_10(sipGILState, 0, sipPySelf, sipMeth, propgrid, wnd_primary, event);
}

::wxPGVariant sipwxPropertyCategory::ChildChanged(::wxPGVariant& thisValue, int childIndex, ::wxPGVariant& childValue) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[8]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_ChildChanged);

    if (!sipMeth)
        return ::wxPropertyCategory::ChildChanged(thisValue, childIndex, childValue);

    extern ::wxPGVariant sipVH__propgrid_11(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxPGVariant&, int, ::wxPGVariant&);

    return sipVH__propgrid_11(sipGILState, 0, sipPySelf, sipMeth, thisValue, childIndex, childValue);
}

const ::wxPGEditor* sipwxPropertyCategory::DoGetEditorClass() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[9]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_DoGetEditorClass);

    if (!sipMeth)
        return ::wxPropertyCategory::DoGetEditorClass();

    extern const ::wxPGEditor* sipVH__propgrid_12(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__propgrid_12(sipGILState, 0, sipPySelf, sipMeth);
}

::wxValidator* sipwxPropertyCategory::DoGetValidator() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[10]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_DoGetValidator);

    if (!sipMeth)
        return ::wxPropertyCategory::DoGetValidator();

    extern ::wxValidator* sipVH__propgrid_13(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__propgrid_13(sipGILState, 0, sipPySelf, sipMeth);
}

void sipwxPropertyCategory::OnCustomPaint(::wxDC& dc, const ::wxRect& rect, ::wxPGPaintData& paintdata)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[11], &sipPySelf, SIP_NULLPTR, sipName_OnCustomPaint);

    if (!sipMeth)
    {
        ::wxPropertyCategory::OnCustomPaint(dc, rect, paintdata);
        return;
    }

    extern void sipVH__propgrid_14(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxDC&, const ::wxRect&, ::wxPGPaintData&);

    sipVH__propgrid_14(sipGILState, 0, sipPySelf, sipMeth, dc, rect, paintdata);
}

::wxPGCellRenderer* sipwxPropertyCategory::GetCellRenderer(int column) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[12]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetCellRenderer);

    if (!sipMeth)
        return ::wxPropertyCategory::GetCellRenderer(column);

    extern ::wxPGCellRenderer* sipVH__propgrid_15(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, int);

    return sipVH__propgrid_15(sipGILState, 0, sipPySelf, sipMeth, column);
}

int sipwxPropertyCategory::GetChoiceSelection() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[13]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetChoiceSelection);

    if (!sipMeth)
        return ::wxPropertyCategory::GetChoiceSelection();

    extern int sipVH__propgrid_16(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__propgrid_16(sipGILState, 0, sipPySelf, sipMeth);
}

void sipwxPropertyCategory::RefreshChildren()
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[14], &sipPySelf, SIP_NULLPTR, sipName_RefreshChildren);

    if (!sipMeth)
    {
        ::wxPropertyCategory::RefreshChildren();
        return;
    }

    extern void sipVH__propgrid_3(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    sipVH__propgrid_3(sipGILState, 0, sipPySelf, sipMeth);
}

bool sipwxPropertyCategory::DoSetAttribute(const ::wxString& name, ::wxPGVariant& value)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[15], &sipPySelf, SIP_NULLPTR, sipName_DoSetAttribute);

    if (!sipMeth)
        return ::wxPropertyCategory::DoSetAttribute(name, value);

    extern bool sipVH__propgrid_17(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxString&, ::wxPGVariant&);

    return sipVH__propgrid_17(sipGILState, 0, sipPySelf, sipMeth, name, value);
}

::wxPGVariant sipwxPropertyCategory::DoGetAttribute(const ::wxString& name) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[16]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_DoGetAttribute);

    if (!sipMeth)
        return ::wxPropertyCategory::DoGetAttribute(name);

    extern ::wxPGVariant sipVH__propgrid_18(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxString&);

    return sipVH__propgrid_18(sipGILState, 0, sipPySelf, sipMeth, name);
}

::wxPGEditorDialogAdapter* sipwxPropertyCategory::GetEditorDialog() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[17]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetEditorDialog);

    if (!sipMeth)
        return ::wxPropertyCategory::GetEditorDialog();

    extern ::wxPGEditorDialogAdapter* sipVH__propgrid_19(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__propgrid_19(sipGILState, 0, sipPySelf, sipMeth);
}

void sipwxPropertyCategory::OnValidationFailure(::wxPGVariant& pendingValue)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[18], &sipPySelf, SIP_NULLPTR, sipName_OnValidationFailure);

    if (!sipMeth)
    {
        ::wxPropertyCategory::OnValidationFailure(pendingValue);
        return;
    }

    extern void sipVH__propgrid_20(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxPGVariant&);

    sipVH__propgrid_20(sipGILState, 0, sipPySelf, sipMeth, pendingValue);
}

::wxString sipwxPropertyCategory::GetValueAsString(int argFlags) const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[19]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_GetValueAsString);

    if (!sipMeth)
        return ::wxPropertyCategory::GetValueAsString(argFlags);

    extern ::wxString sipVH__propgrid_21(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, int);

    return sipVH__propgrid_21(sipGILState, 0, sipPySelf, sipMeth, argFlags);
}


PyDoc_STRVAR(doc_wxPropertyCategory_GetTextExtent, "GetTextExtent(wnd, font) -> int");

extern "C" {static PyObject *meth_wxPropertyCategory_GetTextExtent(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPropertyCategory_GetTextExtent(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;

    {
        const ::wxWindow* wnd;
        const ::wxFont* font;
        const ::wxPropertyCategory *sipCpp;

        static const char *sipKwdList[] = {
            sipName_wnd,
            sipName_font,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ8J9", &sipSelf, sipType_wxPropertyCategory, &sipCpp, sipType_wxWindow, &wnd, sipType_wxFont, &font))
        {
            int sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = sipCpp->GetTextExtent(wnd, *font);
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return PyLong_FromLong(sipRes);
        }
    }

    sipNoMethod(sipParseErr, sipName_PropertyCategory, sipName_GetTextExtent, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPropertyCategory_ValueToString, "ValueToString(value, argFlags) -> str\n"
"\n"
"Converts property value into a text representation.");

extern "C" {static PyObject *meth_wxPropertyCategory_ValueToString(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPropertyCategory_ValueToString(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxPGVariant* value;
        int valueState = 0;
        int argFlags;
        const ::wxPropertyCategory *sipCpp;

        static const char *sipKwdList[] = {
            sipName_value,
            sipName_argFlags,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ1i", &sipSelf, sipType_wxPropertyCategory, &sipCpp, sipType_wxPGVariant, &value, &valueState, &argFlags))
        {
            ::wxString*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxString((sipSelfWasArg ? sipCpp->::wxPropertyCategory::ValueToString(*value, argFlags) : sipCpp->ValueToString(*value, argFlags)));
            Py_END_ALLOW_THREADS
            sipReleaseType(value, sipType_wxPGVariant, valueState);

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxString, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PropertyCategory, sipName_ValueToString, SIP_NULLPTR);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxPropertyCategory_GetValueAsString, "GetValueAsString(argFlags=0) -> str\n"
"\n"
"Returns text representation of property's value.");

extern "C" {static PyObject *meth_wxPropertyCategory_GetValueAsString(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxPropertyCategory_GetValueAsString(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        int argFlags = 0;
        const ::wxPropertyCategory *sipCpp;

        static const char *sipKwdList[] = {
            sipName_argFlags,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "B|i", &sipSelf, sipType_wxPropertyCategory, &sipCpp, &argFlags))
        {
            ::wxString*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxString((sipSelfWasArg ? sipCpp->::wxPropertyCategory::GetValueAsString(argFlags) : sipCpp->GetValueAsString(argFlags)));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxString, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_PropertyCategory, sipName_GetValueAsString, SIP_NULLPTR);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxPropertyCategory(void *, const sipTypeDef *);}
static void *cast_wxPropertyCategory(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxPropertyCategory *sipCpp = reinterpret_cast<::wxPropertyCategory *>(sipCppV);

    if (targetType == sipType_wxPropertyCategory)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxPGProperty)->ctd_cast(static_cast<::wxPGProperty *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxPropertyCategory(void *, int);}
static void release_wxPropertyCategory(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxPropertyCategory *>(sipCppV);
    else
        delete reinterpret_cast<::wxPropertyCategory *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxPropertyCategory(Py_ssize_t);}
static void *array_wxPropertyCategory(Py_ssize_t sipNrElem)
{
    return new ::wxPropertyCategory[sipNrElem];
}


extern "C" {static void array_delete_wxPropertyCategory(void *);}
static void array_delete_wxPropertyCategory(void *sipCpp)
{
    delete[] reinterpret_cast<::wxPropertyCategory *>(sipCpp);
}


extern "C" {static void assign_wxPropertyCategory(void *, Py_ssize_t, void *);}
static void assign_wxPropertyCategory(void *sipDst, Py_ssize_t sipDstIdx, void *sipSrc)
{
    reinterpret_cast<::wxPropertyCategory *>(sipDst)[sipDstIdx] = *reinterpret_cast<::wxPropertyCategory *>(sipSrc);
}


extern "C" {static void *copy_wxPropertyCategory(const void *, Py_ssize_t);}
static void *copy_wxPropertyCategory(const void *sipSrc, Py_ssize_t sipSrcIdx)
{
    return new ::wxPropertyCategory(reinterpret_cast<const ::wxPropertyCategory *>(sipSrc)[sipSrcIdx]);
}


extern "C" {static void dealloc_wxPropertyCategory(sipSimpleWrapper *);}
static void dealloc_wxPropertyCategory(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxPropertyCategory *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxPropertyCategory(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxPropertyCategory(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxPropertyCategory(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxPropertyCategory *sipCpp = SIP_NULLPTR;

    {
        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, ""))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxPropertyCategory();
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
        const ::wxString* label;
        int labelState = 0;
        const ::wxString& namedef = wxPG_LABEL;
        const ::wxString* name = &namedef;
        int nameState = 0;

        static const char *sipKwdList[] = {
            sipName_label,
            sipName_name,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J1|J1", sipType_wxString, &label, &labelState, sipType_wxString, &name, &nameState))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxPropertyCategory(*label, *name);
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxString *>(label), sipType_wxString, labelState);
            sipReleaseType(const_cast<::wxString *>(name), sipType_wxString, nameState);

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
        const ::wxPropertyCategory* a0;

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, SIP_NULLPTR, sipUnused, "J9", sipType_wxPropertyCategory, &a0))
        {
            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxPropertyCategory(*a0);
            Py_END_ALLOW_THREADS

            sipCpp->sipPySelf = sipSelf;

            return sipCpp;
        }
    }

    return SIP_NULLPTR;
}


/* Define this type's super-types. */
static sipEncodedTypeDef supers_wxPropertyCategory[] = {{44, 255, 1}};


static PyMethodDef methods_wxPropertyCategory[] = {
    {sipName_GetTextExtent, SIP_MLMETH_CAST(meth_wxPropertyCategory_GetTextExtent), METH_VARARGS|METH_KEYWORDS, doc_wxPropertyCategory_GetTextExtent},
    {sipName_GetValueAsString, SIP_MLMETH_CAST(meth_wxPropertyCategory_GetValueAsString), METH_VARARGS|METH_KEYWORDS, doc_wxPropertyCategory_GetValueAsString},
    {sipName_ValueToString, SIP_MLMETH_CAST(meth_wxPropertyCategory_ValueToString), METH_VARARGS|METH_KEYWORDS, doc_wxPropertyCategory_ValueToString}
};

sipVariableDef variables_wxPropertyCategory[] = {
    {PropertyVariable, sipName_ValueAsString, &methods_wxPropertyCategory[1], SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
};

PyDoc_STRVAR(doc_wxPropertyCategory, "PropertyCategory() -> None\n"
"PropertyCategory(label, name=PG_LABEL) -> None\n"
"\n"
"Category (caption) property.");


sipClassTypeDef sipTypeDef__propgrid_wxPropertyCategory = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxPropertyCategory,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_PropertyCategory,
        {0, 0, 1},
        3, methods_wxPropertyCategory,
        0, SIP_NULLPTR,
        1, variables_wxPropertyCategory,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxPropertyCategory,
    -1,
    -1,
    supers_wxPropertyCategory,
    SIP_NULLPTR,
    init_type_wxPropertyCategory,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxPropertyCategory,
    assign_wxPropertyCategory,
    array_wxPropertyCategory,
    copy_wxPropertyCategory,
    release_wxPropertyCategory,
    cast_wxPropertyCategory,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxPropertyCategory,
    sizeof (::wxPropertyCategory),
};
