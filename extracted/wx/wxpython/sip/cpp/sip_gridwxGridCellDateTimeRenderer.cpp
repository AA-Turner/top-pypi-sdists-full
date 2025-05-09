/*
 * Interface wrapper code.
 *
 * Generated by SIP 6.10.0
 *
 *     Copyright: (c) 2020 by Total Control Software
 *     License:   wxWindows License
 */

#include "sipAPI_grid.h"
        #include <wx/grid.h>
        #include <wx/gdicmn.h>
        #include <wx/grid.h>
        #include <wx/grid.h>
        #include <wx/dc.h>
        #include <wx/gdicmn.h>
        #include <wx/grid.h>


class sipwxGridCellDateTimeRenderer : public ::wxGridCellDateTimeRenderer
{
public:
    sipwxGridCellDateTimeRenderer(const ::wxString&, const ::wxString&);
    virtual ~sipwxGridCellDateTimeRenderer();

    /*
     * There is a protected method for every virtual method visible from
     * this class.
     */
protected:
    ::wxGridCellRenderer* Clone() const SIP_OVERRIDE;
    void Draw(::wxGrid&, ::wxGridCellAttr&, ::wxDC&, const ::wxRect&, int, int, bool) SIP_OVERRIDE;
    ::wxSize GetBestSize(::wxGrid&, ::wxGridCellAttr&, ::wxDC&, int, int) SIP_OVERRIDE;
    int GetBestHeight(::wxGrid&, ::wxGridCellAttr&, ::wxDC&, int, int, int) SIP_OVERRIDE;
    int GetBestWidth(::wxGrid&, ::wxGridCellAttr&, ::wxDC&, int, int, int) SIP_OVERRIDE;
    ::wxSize GetMaxBestSize(::wxGrid&, ::wxGridCellAttr&, ::wxDC&) SIP_OVERRIDE;
    void SetParameters(const ::wxString&) SIP_OVERRIDE;

public:
    sipSimpleWrapper *sipPySelf;

private:
    sipwxGridCellDateTimeRenderer(const sipwxGridCellDateTimeRenderer &);
    sipwxGridCellDateTimeRenderer &operator = (const sipwxGridCellDateTimeRenderer &);

    char sipPyMethods[7];
};

sipwxGridCellDateTimeRenderer::sipwxGridCellDateTimeRenderer(const ::wxString& outformat, const ::wxString& informat): ::wxGridCellDateTimeRenderer(outformat, informat), sipPySelf(SIP_NULLPTR)
{
    memset(sipPyMethods, 0, sizeof (sipPyMethods));
}

sipwxGridCellDateTimeRenderer::~sipwxGridCellDateTimeRenderer()
{
    sipInstanceDestroyedEx(&sipPySelf);
}

::wxGridCellRenderer* sipwxGridCellDateTimeRenderer::Clone() const
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, const_cast<char *>(&sipPyMethods[0]), const_cast<sipSimpleWrapper **>(&sipPySelf), SIP_NULLPTR, sipName_Clone);

    if (!sipMeth)
        return ::wxGridCellDateTimeRenderer::Clone();

    extern ::wxGridCellRenderer* sipVH__grid_0(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *);

    return sipVH__grid_0(sipGILState, 0, sipPySelf, sipMeth);
}

void sipwxGridCellDateTimeRenderer::Draw(::wxGrid& grid, ::wxGridCellAttr& attr, ::wxDC& dc, const ::wxRect& rect, int row, int col, bool isSelected)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[1], &sipPySelf, SIP_NULLPTR, sipName_Draw);

    if (!sipMeth)
    {
        ::wxGridCellDateTimeRenderer::Draw(grid, attr, dc, rect, row, col, isSelected);
        return;
    }

    extern void sipVH__grid_1(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxGrid&, ::wxGridCellAttr&, ::wxDC&, const ::wxRect&, int, int, bool);

    sipVH__grid_1(sipGILState, 0, sipPySelf, sipMeth, grid, attr, dc, rect, row, col, isSelected);
}

::wxSize sipwxGridCellDateTimeRenderer::GetBestSize(::wxGrid& grid, ::wxGridCellAttr& attr, ::wxDC& dc, int row, int col)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[2], &sipPySelf, SIP_NULLPTR, sipName_GetBestSize);

    if (!sipMeth)
        return ::wxGridCellDateTimeRenderer::GetBestSize(grid, attr, dc, row, col);

    extern ::wxSize sipVH__grid_2(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxGrid&, ::wxGridCellAttr&, ::wxDC&, int, int);

    return sipVH__grid_2(sipGILState, 0, sipPySelf, sipMeth, grid, attr, dc, row, col);
}

int sipwxGridCellDateTimeRenderer::GetBestHeight(::wxGrid& grid, ::wxGridCellAttr& attr, ::wxDC& dc, int row, int col, int width)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[3], &sipPySelf, SIP_NULLPTR, sipName_GetBestHeight);

    if (!sipMeth)
        return ::wxGridCellDateTimeRenderer::GetBestHeight(grid, attr, dc, row, col, width);

    extern int sipVH__grid_3(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxGrid&, ::wxGridCellAttr&, ::wxDC&, int, int, int);

    return sipVH__grid_3(sipGILState, 0, sipPySelf, sipMeth, grid, attr, dc, row, col, width);
}

int sipwxGridCellDateTimeRenderer::GetBestWidth(::wxGrid& grid, ::wxGridCellAttr& attr, ::wxDC& dc, int row, int col, int height)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[4], &sipPySelf, SIP_NULLPTR, sipName_GetBestWidth);

    if (!sipMeth)
        return ::wxGridCellDateTimeRenderer::GetBestWidth(grid, attr, dc, row, col, height);

    extern int sipVH__grid_3(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxGrid&, ::wxGridCellAttr&, ::wxDC&, int, int, int);

    return sipVH__grid_3(sipGILState, 0, sipPySelf, sipMeth, grid, attr, dc, row, col, height);
}

::wxSize sipwxGridCellDateTimeRenderer::GetMaxBestSize(::wxGrid& grid, ::wxGridCellAttr& attr, ::wxDC& dc)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[5], &sipPySelf, SIP_NULLPTR, sipName_GetMaxBestSize);

    if (!sipMeth)
        return ::wxGridCellDateTimeRenderer::GetMaxBestSize(grid, attr, dc);

    extern ::wxSize sipVH__grid_4(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, ::wxGrid&, ::wxGridCellAttr&, ::wxDC&);

    return sipVH__grid_4(sipGILState, 0, sipPySelf, sipMeth, grid, attr, dc);
}

void sipwxGridCellDateTimeRenderer::SetParameters(const ::wxString& params)
{
    sip_gilstate_t sipGILState;
    PyObject *sipMeth;

    sipMeth = sipIsPyMethod(&sipGILState, &sipPyMethods[6], &sipPySelf, SIP_NULLPTR, sipName_SetParameters);

    if (!sipMeth)
    {
        ::wxGridCellDateTimeRenderer::SetParameters(params);
        return;
    }

    extern void sipVH__grid_5(sip_gilstate_t, sipVirtErrorHandlerFunc, sipSimpleWrapper *, PyObject *, const ::wxString&);

    sipVH__grid_5(sipGILState, 0, sipPySelf, sipMeth, params);
}


PyDoc_STRVAR(doc_wxGridCellDateTimeRenderer_Clone, "Clone(self) -> Optional[GridCellRenderer]");

extern "C" {static PyObject *meth_wxGridCellDateTimeRenderer_Clone(PyObject *, PyObject *);}
static PyObject *meth_wxGridCellDateTimeRenderer_Clone(PyObject *sipSelf, PyObject *sipArgs)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        const ::wxGridCellDateTimeRenderer *sipCpp;

        if (sipParseArgs(&sipParseErr, sipArgs, "B", &sipSelf, sipType_wxGridCellDateTimeRenderer, &sipCpp))
        {
            ::wxGridCellRenderer*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = (sipSelfWasArg ? sipCpp->::wxGridCellDateTimeRenderer::Clone() : sipCpp->Clone());
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxGridCellRenderer, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_GridCellDateTimeRenderer, sipName_Clone, doc_wxGridCellDateTimeRenderer_Clone);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxGridCellDateTimeRenderer_Draw, "Draw(self, grid: Grid, attr: GridCellAttr, dc: DC, rect: Rect, row: int, col: int, isSelected: bool)");

extern "C" {static PyObject *meth_wxGridCellDateTimeRenderer_Draw(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxGridCellDateTimeRenderer_Draw(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxGrid* grid;
        ::wxGridCellAttr* attr;
        ::wxDC* dc;
        const ::wxRect* rect;
        int rectState = 0;
        int row;
        int col;
        bool isSelected;
        ::wxGridCellDateTimeRenderer *sipCpp;

        static const char *sipKwdList[] = {
            sipName_grid,
            sipName_attr,
            sipName_dc,
            sipName_rect,
            sipName_row,
            sipName_col,
            sipName_isSelected,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9J9J9J1iib", &sipSelf, sipType_wxGridCellDateTimeRenderer, &sipCpp, sipType_wxGrid, &grid, sipType_wxGridCellAttr, &attr, sipType_wxDC, &dc, sipType_wxRect, &rect, &rectState, &row, &col, &isSelected))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            (sipSelfWasArg ? sipCpp->::wxGridCellDateTimeRenderer::Draw(*grid, *attr, *dc, *rect, row, col, isSelected) : sipCpp->Draw(*grid, *attr, *dc, *rect, row, col, isSelected));
            Py_END_ALLOW_THREADS
            sipReleaseType(const_cast<::wxRect *>(rect), sipType_wxRect, rectState);

            if (PyErr_Occurred())
                return 0;

            Py_INCREF(Py_None);
            return Py_None;
        }
    }

    sipNoMethod(sipParseErr, sipName_GridCellDateTimeRenderer, sipName_Draw, doc_wxGridCellDateTimeRenderer_Draw);

    return SIP_NULLPTR;
}


PyDoc_STRVAR(doc_wxGridCellDateTimeRenderer_GetBestSize, "GetBestSize(self, grid: Grid, attr: GridCellAttr, dc: DC, row: int, col: int) -> Size");

extern "C" {static PyObject *meth_wxGridCellDateTimeRenderer_GetBestSize(PyObject *, PyObject *, PyObject *);}
static PyObject *meth_wxGridCellDateTimeRenderer_GetBestSize(PyObject *sipSelf, PyObject *sipArgs, PyObject *sipKwds)
{
    PyObject *sipParseErr = SIP_NULLPTR;
    bool sipSelfWasArg = (!sipSelf || sipIsDerivedClass((sipSimpleWrapper *)sipSelf));

    {
        ::wxGrid* grid;
        ::wxGridCellAttr* attr;
        ::wxDC* dc;
        int row;
        int col;
        ::wxGridCellDateTimeRenderer *sipCpp;

        static const char *sipKwdList[] = {
            sipName_grid,
            sipName_attr,
            sipName_dc,
            sipName_row,
            sipName_col,
        };

        if (sipParseKwdArgs(&sipParseErr, sipArgs, sipKwds, sipKwdList, SIP_NULLPTR, "BJ9J9J9ii", &sipSelf, sipType_wxGridCellDateTimeRenderer, &sipCpp, sipType_wxGrid, &grid, sipType_wxGridCellAttr, &attr, sipType_wxDC, &dc, &row, &col))
        {
            ::wxSize*sipRes;

            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipRes = new ::wxSize((sipSelfWasArg ? sipCpp->::wxGridCellDateTimeRenderer::GetBestSize(*grid, *attr, *dc, row, col) : sipCpp->GetBestSize(*grid, *attr, *dc, row, col)));
            Py_END_ALLOW_THREADS

            if (PyErr_Occurred())
                return 0;

            return sipConvertFromNewType(sipRes, sipType_wxSize, SIP_NULLPTR);
        }
    }

    sipNoMethod(sipParseErr, sipName_GridCellDateTimeRenderer, sipName_GetBestSize, doc_wxGridCellDateTimeRenderer_GetBestSize);

    return SIP_NULLPTR;
}


/* Cast a pointer to a type somewhere in its inheritance hierarchy. */
extern "C" {static void *cast_wxGridCellDateTimeRenderer(void *, const sipTypeDef *);}
static void *cast_wxGridCellDateTimeRenderer(void *sipCppV, const sipTypeDef *targetType)
{
    ::wxGridCellDateTimeRenderer *sipCpp = reinterpret_cast<::wxGridCellDateTimeRenderer *>(sipCppV);

    if (targetType == sipType_wxGridCellDateTimeRenderer)
        return sipCppV;

    sipCppV = ((const sipClassTypeDef *)sipType_wxGridCellDateRenderer)->ctd_cast(static_cast<::wxGridCellDateRenderer *>(sipCpp), targetType);
    if (sipCppV)
        return sipCppV;

    return SIP_NULLPTR;
}


/* Call the instance's destructor. */
extern "C" {static void release_wxGridCellDateTimeRenderer(void *, int);}
static void release_wxGridCellDateTimeRenderer(void *sipCppV, int sipState)
{
    Py_BEGIN_ALLOW_THREADS

    if (sipState & SIP_DERIVED_CLASS)
        delete reinterpret_cast<sipwxGridCellDateTimeRenderer *>(sipCppV);
    else
        delete reinterpret_cast<::wxGridCellDateTimeRenderer *>(sipCppV);

    Py_END_ALLOW_THREADS
}


extern "C" {static void *array_wxGridCellDateTimeRenderer(Py_ssize_t);}
static void *array_wxGridCellDateTimeRenderer(Py_ssize_t sipNrElem)
{
    return new ::wxGridCellDateTimeRenderer[sipNrElem];
}


extern "C" {static void array_delete_wxGridCellDateTimeRenderer(void *);}
static void array_delete_wxGridCellDateTimeRenderer(void *sipCpp)
{
    delete[] reinterpret_cast<::wxGridCellDateTimeRenderer *>(sipCpp);
}


extern "C" {static void dealloc_wxGridCellDateTimeRenderer(sipSimpleWrapper *);}
static void dealloc_wxGridCellDateTimeRenderer(sipSimpleWrapper *sipSelf)
{
    if (sipIsDerivedClass(sipSelf))
        reinterpret_cast<sipwxGridCellDateTimeRenderer *>(sipGetAddress(sipSelf))->sipPySelf = SIP_NULLPTR;

    if (sipIsOwnedByPython(sipSelf))
    {
        release_wxGridCellDateTimeRenderer(sipGetAddress(sipSelf), sipIsDerivedClass(sipSelf));
    }
}


extern "C" {static void *init_type_wxGridCellDateTimeRenderer(sipSimpleWrapper *, PyObject *, PyObject *, PyObject **, PyObject **, PyObject **);}
static void *init_type_wxGridCellDateTimeRenderer(sipSimpleWrapper *sipSelf, PyObject *sipArgs, PyObject *sipKwds, PyObject **sipUnused, PyObject **sipOwner, PyObject **sipParseErr)
{
    sipwxGridCellDateTimeRenderer *sipCpp = SIP_NULLPTR;

    {
        const ::wxString& outformatdef = wxDefaultDateTimeFormat;
        const ::wxString* outformat = &outformatdef;
        int outformatState = 0;
        const ::wxString& informatdef = wxDefaultDateTimeFormat;
        const ::wxString* informat = &informatdef;
        int informatState = 0;

        static const char *sipKwdList[] = {
            sipName_outformat,
            sipName_informat,
        };

        if (sipParseKwdArgs(sipParseErr, sipArgs, sipKwds, sipKwdList, sipUnused, "|J1J1", sipType_wxString, &outformat, &outformatState, sipType_wxString, &informat, &informatState))
        {
            PyErr_Clear();

            Py_BEGIN_ALLOW_THREADS
            sipCpp = new sipwxGridCellDateTimeRenderer(*outformat, *informat);
            Py_END_ALLOW_THREADS

            *sipOwner = Py_None;
            sipReleaseType(const_cast<::wxString *>(outformat), sipType_wxString, outformatState);
            sipReleaseType(const_cast<::wxString *>(informat), sipType_wxString, informatState);

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
static sipEncodedTypeDef supers_wxGridCellDateTimeRenderer[] = {{24, 255, 1}};


static PyMethodDef methods_wxGridCellDateTimeRenderer[] = {
    {sipName_Clone, meth_wxGridCellDateTimeRenderer_Clone, METH_VARARGS, doc_wxGridCellDateTimeRenderer_Clone},
    {sipName_Draw, SIP_MLMETH_CAST(meth_wxGridCellDateTimeRenderer_Draw), METH_VARARGS|METH_KEYWORDS, doc_wxGridCellDateTimeRenderer_Draw},
    {sipName_GetBestSize, SIP_MLMETH_CAST(meth_wxGridCellDateTimeRenderer_GetBestSize), METH_VARARGS|METH_KEYWORDS, doc_wxGridCellDateTimeRenderer_GetBestSize}
};

PyDoc_STRVAR(doc_wxGridCellDateTimeRenderer, "GridCellDateTimeRenderer(outformat=wx.DefaultDateTimeFormat, informat=wx.DefaultDateTimeFormat) -> None\n"
"\n"
"This class may be used to format a date/time data in a cell.");


sipClassTypeDef sipTypeDef__grid_wxGridCellDateTimeRenderer = {
    {
        -1,
        SIP_NULLPTR,
        SIP_NULLPTR,
        SIP_TYPE_CLASS,
        sipNameNr_wxGridCellDateTimeRenderer,
        SIP_NULLPTR,
        SIP_NULLPTR,
    },
    {
        sipNameNr_GridCellDateTimeRenderer,
        {0, 0, 1},
        3, methods_wxGridCellDateTimeRenderer,
        0, SIP_NULLPTR,
        0, SIP_NULLPTR,
        {SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR, SIP_NULLPTR},
    },
    doc_wxGridCellDateTimeRenderer,
    -1,
    -1,
    supers_wxGridCellDateTimeRenderer,
    SIP_NULLPTR,
    init_type_wxGridCellDateTimeRenderer,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    dealloc_wxGridCellDateTimeRenderer,
    SIP_NULLPTR,
    array_wxGridCellDateTimeRenderer,
    SIP_NULLPTR,
    release_wxGridCellDateTimeRenderer,
    cast_wxGridCellDateTimeRenderer,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    SIP_NULLPTR,
    array_delete_wxGridCellDateTimeRenderer,
    sizeof (::wxGridCellDateTimeRenderer),
};
