/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/dcclient.h>
        #include <wx/window.h>
    #include <wx/setup.h>
    #include <wxPython/wxpy_api.h>
        #include <wx/gdicmn.h>
        #include <wx/graphics.h>
        #include <wx/bitmap.h>
        #include <wx/gdicmn.h>
        #include <wx/palette.h>
        #include <wx/gdicmn.h>
        #include <wx/colour.h>
        #include <wx/dc.h>
        #include <wx/affinematrix2d.h>
        #include <wx/pen.h>
        #include "arrayholder.h"
        #include <wx/brush.h>
        #include <wx/font.h>
        #include <wx/dc.h>
        #include <wx/region.h>
        #include <wx/icon.h>
        #include <wx/object.h>
        #include <wx/object.h>
        #include <wx/object.h>


class sipwxWindowDC : public ::wxWindowDC
{
public:
    sipwxWindowDC(::wxWindow*);
    ~sipwxWindowDC();

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxWindowDC(const sipwxWindowDC &);
    sipwxWindowDC &operator = (const sipwxWindowDC &);
};

sipwxWindowDC::sipwxWindowDC(::wxWindow*window): ::wxWindowDC(window), sipPySelf(SIP_NULLPTR)
{
}

sipwxWindowDC::~sipwxWindowDC()
{
    sipInstanceDestroyedEx(&sipPySelf);
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxWindowDC(void *, const sipTypeDef *);}
static void *cast_wxWindowDC(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxWindowDC *sipCpp = reinterpret_cast<::wxWindowDC *>(sipCppV);

    if (targetType == sipType_wxWindowDC)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxDC)->ctd_cast(static_cast<::wxDC *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxWindowDC(void *, int);}
static void release_wxWindowDC(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxWindowDC *>(sipCppV);
    else
        delete reinterpret_cast<::wxWindowDC *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxWindowDC(sipSimpleWrapper *);}
static void dealloc_wxWindowDC(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxWindowDC *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxWindowDC(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxWindowDC(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxWindowDC(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxWindowDC *sipCpp = SIP_NULLPTR;

    {
        ::wxWindow* window;

        static const char *sipKwdList[] = {
            sipName_window,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "J8", sipType_wxWindow, &window))
        {
        if (!wxPyCheckForApp()) return NULL;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxWindowDC(window);
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
static sipEncodedTypeDef supers_wxWindowDC[] = {{101, 255, 1}};

PyDoc_STRVAR(doc_wxWindowDC, "WindowDC(window) -> None\n"
"\n"
"A wxWindowDC must be constructed if an application wishes to paint on\n"
"the whole area of a window (client and decorations).");


sipClassTypeDef sipTypeDef__core_wxWindowDC = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxWindowDC,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_WindowDC,
        {0, 0, 1},
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxWindowDC,
    -1,
    -1,
    supers_wxWindowDC,
    SIP_NULLPTR,
    init_type_wxWindowDC,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxWindowDC,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxWindowDC,
    cast_wxWindowDC,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    sizeof (::wxWindowDC),
};
