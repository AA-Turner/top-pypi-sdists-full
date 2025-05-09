/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_core.h"
        #include <wx/dcbuffer.h>
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


class sipwxAutoBufferedPaintDC : public ::wxAutoBufferedPaintDC
{
public:
    sipwxAutoBufferedPaintDC(::wxWindow*);
    ~sipwxAutoBufferedPaintDC();

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxAutoBufferedPaintDC(const sipwxAutoBufferedPaintDC &);
    sipwxAutoBufferedPaintDC &operator = (const sipwxAutoBufferedPaintDC &);
};

sipwxAutoBufferedPaintDC::sipwxAutoBufferedPaintDC(::wxWindow*window): ::wxAutoBufferedPaintDC(window), sipPySelf(SIP_NULLPTR)
{
}

sipwxAutoBufferedPaintDC::~sipwxAutoBufferedPaintDC()
{
    sipInstanceDestroyedEx(&sipPySelf);
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxAutoBufferedPaintDC(void *, const sipTypeDef *);}
static void *cast_wxAutoBufferedPaintDC(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxAutoBufferedPaintDC *sipCpp = reinterpret_cast<::wxAutoBufferedPaintDC *>(sipCppV);

    if (targetType == sipType_wxAutoBufferedPaintDC)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxDC)->ctd_cast(static_cast<::wxDC *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxAutoBufferedPaintDC(void *, int);}
static void release_wxAutoBufferedPaintDC(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxAutoBufferedPaintDC *>(sipCppV);
    else
        delete reinterpret_cast<::wxAutoBufferedPaintDC *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void dealloc_wxAutoBufferedPaintDC(sipSimpleWrapper *);}
static void dealloc_wxAutoBufferedPaintDC(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxAutoBufferedPaintDC *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxAutoBufferedPaintDC(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxAutoBufferedPaintDC(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxAutoBufferedPaintDC(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **, PyObject **sipParseErr)
{
    sipwxAutoBufferedPaintDC *sipCpp = SIP_NULLPTR;

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
            sipCpp = new sipwxAutoBufferedPaintDC(window);
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
static sipEncodedTypeDef supers_wxAutoBufferedPaintDC[] = {{101, 255, 1}};

PyDoc_STRVAR(doc_wxAutoBufferedPaintDC, "AutoBufferedPaintDC(window) -> None\n"
"\n"
"This wxDC derivative can be used inside of an EVT_PAINT() event\n"
"handler to achieve double-buffered drawing.");


sipClassTypeDef sipTypeDef__core_wxAutoBufferedPaintDC = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_SCC|SIP_TYPE_CLASS,
        sipNameNr_wxAutoBufferedPaintDC,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_AutoBufferedPaintDC,
        {0, 0, 1},
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxAutoBufferedPaintDC,
    -1,
    -1,
    supers_wxAutoBufferedPaintDC,
    SIP_NULLPTR,
    init_type_wxAutoBufferedPaintDC,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxAutoBufferedPaintDC,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    release_wxAutoBufferedPaintDC,
    cast_wxAutoBufferedPaintDC,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    sizeof (::wxAutoBufferedPaintDC),
};
