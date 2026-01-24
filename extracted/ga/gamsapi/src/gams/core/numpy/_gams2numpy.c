/*
 * GAMS - General Algebraic Modeling System Python API
 *
 * Copyright (c) 2017-2026 GAMS Development Corp. <support@gams.com>
 * Copyright (c) 2017-2026 GAMS Software GmbH <support@gams.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

#define NPY_NO_DEPRECATED_API NPY_1_21_API_VERSION

#include <Python.h>
#include <numpy/arrayobject.h>
#include "gclgms.h"
#include "gdxcc.h"
#include "gmdcc.h"

#define MODE_RAW         0
#define MODE_STRING      1
#define MODE_MAP         2
#define MODE_CATEGORICAL 3

#define C_LAYOUT 0
#define F_LAYOUT 1

#define PY_CHECK_ERROR if( PyErr_Occurred() != NULL ) return (PyObject *) NULL;

#define DECREF_PYOBJECT_P(obj)  \
{                               \
   Py_DECREF(obj);              \
   obj = NULL;                  \
}

#define ERROR(msg) ERROR_GDX(msg, NULL)

#define ERROR_GDX(msg, gdx)                   \
{                                             \
   PyErr_SetString(PyExc_RuntimeError, msg);  \
   if( gdx )                                  \
   {                                          \
      gdxDataWriteDone(gdx);                  \
   }                                          \
   return (PyObject *) NULL;                  \
}                                             \

#define LAST_ERROR_GDX(gdx) \
{ \
   char errorMsg[GMS_SSSIZE+11]; \
   char msg[GMS_SSSIZE]; \
   gdxErrorStr(gdx, gdxGetLastError(gdx), msg); \
   sprintf(errorMsg, msg); \
   ERROR_GDX(errorMsg, gdx); \
}

#define LAST_ERROR_GMD(gmd) \
{ \
   char errorMsg[GMS_SSSIZE+11]; \
   char msg[GMS_SSSIZE]; \
   gmdGetLastError(gmd, msg); \
   sprintf(errorMsg, msg); \
   ERROR(errorMsg); \
}

#define NP_GET_ITEM(arr, i, j) PyArray_GETITEM(arr, PyArray_GETPTR2(arr, i, j))

#define NP_GET_STRING(arr, i, j, target) NP_GET_STRING_GDX(arr, i, j, target, NULL)

#define NP_GET_STRING_GDX(arr, i, j, target, gdx)                                      \
{                                                                                      \
   PyObject* item = NP_GET_ITEM(arr, i, j);                                            \
   if( PyUnicode_Check(item) )                                                         \
   {                                                                                   \
      target = (char *) PyUnicode_AsUTF8(item);                                        \
      DECREF_PYOBJECT_P(item);                                                         \
   }                                                                                   \
   else                                                                                \
   {                                                                                   \
      char errorMsg[GMS_SSSIZE];                                                       \
      sprintf(errorMsg, "Expected type str but got %s", item->ob_type->tp_name);       \
      DECREF_PYOBJECT_P(item);                                                         \
      ERROR_GDX(errorMsg, gdx);                                                        \
   }                                                                                   \
}

#define VALIDATE_ARRAYS(arrKeys, arrValues, dim, symType, nrRecs, nrValCols, keysLayout, valuesLayout, keysType, valuesType) \
{ \
   if( PyArray_NDIM(arrKeys) != 2 ) \
   { \
      ERROR("Numpy array for keys needs to have exactly two dimensions"); \
   } \
   if( PyArray_NDIM(arrValues) != 2 ) \
   { \
      ERROR("Numpy array for values needs to have exactly two dimensions"); \
   } \
   if( PyArray_DIMS(arrKeys)[0] != PyArray_DIMS(arrValues)[0] ) \
   { \
      ERROR("Numpy arrays for keys and values need to have the same number of records."); \
   } \
   if( PyArray_DIMS(arrKeys)[1] != dim ) \
   { \
      ERROR("Unexpected number of columns in key array"); \
   } \
   int expectedValCols = 1; \
   if( symType == GMS_DT_VAR || symType == GMS_DT_EQU ) \
   { \
      expectedValCols = GMS_VAL_MAX; \
   } \
   if( PyArray_DIMS(arrValues)[1] != expectedValCols ) \
   { \
      if( !( ( symType == GMS_DT_SET || symType == GMS_DT_ALIAS) && PyArray_DIMS(arrValues)[1] == 0 ) ) \
      { \
         ERROR("Unexpected number of columns in value array"); \
      } \
   } \
   nrRecs = PyArray_DIMS(arrKeys)[0]; \
   nrValCols = PyArray_DIMS(arrValues)[1]; \
   keysLayout = PyArray_ISCARRAY(arrKeys) ? C_LAYOUT : F_LAYOUT; \
   valuesLayout = PyArray_ISCARRAY(arrValues) ? C_LAYOUT : F_LAYOUT; \
   keysType = PyArray_TYPE(arrKeys); \
   valuesType = PyArray_TYPE(arrValues); \
}

#define CHECK_CREATE_UELLIST(mode, uelList, createUelList, uelCount, encoding, gmd, gdx) \
{ \
   createUelList = 0; \
   if( mode == MODE_STRING || mode == MODE_CATEGORICAL ) \
   { \
      if( uelList == Py_None || uelList == NULL ) \
      { \
         createUelList = 1; \
      } \
      else if( !PyList_Check(uelList) ) \
      { \
         ERROR("Parameter uelList needs to be of type list"); \
      } \
      if( !createUelList && uelCount + 1 != PyList_Size(uelList) ) \
      { \
         char msg[GMS_SSSIZE]; \
         sprintf(msg, "List of UELs has %ld elements, but did expect %d", PyList_Size(uelList), uelCount + 1); \
         ERROR(msg); \
      } \
      if( createUelList ) \
      { \
         if( gdx != NULL) \
         { \
            uelList = i_gdxCreateUelList(gdx, encoding); \
         } \
         else if( gmd != NULL) \
         { \
            uelList = i_gmdCreateUelList(gmd, encoding); \
         } \
         else \
         { \
            ERROR("Neither gmd nor gdx has been specified."); \
         } \
         if( uelList == Py_None ) \
         { \
            return (PyObject *) NULL; \
         } \
      } \
   } \
} \

#define CHECK_CREATE_UELLIST_GDX(mode, uelList, createUelList, uelCount, gdx, encoding) \
{ \
   CHECK_CREATE_UELLIST(mode, uelList, createUelList, uelCount, encoding, NULL, gdx); \
} \

#define CHECK_CREATE_UELLIST_GMD(mode, uelList, createUelList, uelCount, gmd, encoding) \
{ \
   CHECK_CREATE_UELLIST(mode, uelList, createUelList, uelCount, encoding, gmd, NULL); \
} \

#define GET_VAL_COL_COUNT(symType, nValCols) \
{ \
   if( symType == GMS_DT_SET || symType == GMS_DT_ALIAS || symType == GMS_DT_PAR ) \
   { \
      nValCols = 1; \
   } \
   else if( symType == GMS_DT_VAR || symType == GMS_DT_EQU ) \
   { \
      nValCols = GMS_VAL_MAX; \
   } \
   else \
   { \
      PyErr_SetString(PyExc_Exception, "Encountered unknown symbol type while creating numpy array"); \
      return (PyObject *) NULL; \
   } \
}

#define GET_ARR_TYPES(mode, symType, uelCount, keysType, valuesType) \
{ \
   if( mode == MODE_STRING) \
   { \
      keysType = NPY_OBJECT; \
   } \
   else if( mode == MODE_CATEGORICAL ) \
   { \
      if(uelCount < NPY_MAX_UINT8 - 1) \
      { \
         keysType = NPY_UINT8; \
      } \
      else if(uelCount < NPY_MAX_UINT16 - 1) \
      { \
         keysType = NPY_UINT16; \
      } \
      else \
      { \
         keysType = NPY_UINT32; \
      } \
   } \
   else \
   { \
      /* Use INT32 always since the uelCount does not tell us anything about the size of negative UEL indexes which are supported in raw mode */ \
      keysType = NPY_INT32; \
   } \
   if( symType == GMS_DT_SET || symType == GMS_DT_ALIAS  ) \
   { \
      valuesType = NPY_OBJECT; \
   } \
   else if( symType == GMS_DT_PAR || symType == GMS_DT_VAR || symType == GMS_DT_EQU ) \
   { \
      valuesType = NPY_FLOAT64; \
   } \
}

#define PREP_DS_CAT(mode, count, mapUel, uelsInCol, uelCount, dim) \
{ \
   for( int i = 0; i < GMS_MAX_INDEX_DIM; i++) \
   { \
      count[i] = 0; \
   } \
   mapUel = malloc(uelCount * dim * sizeof(npy_uint32)); \
   memset(mapUel, 0, uelCount * dim * sizeof(npy_uint32)); \
   uelsInCol = malloc(uelCount *dim * sizeof(npy_uint32)); \
   memset(uelsInCol, 0, uelCount * dim * sizeof(npy_uint32)); \
}

#define REMAP_CAT(mode, dim, nrRecs, mapUel, uelsInCol, uelCount, uelList, count, keysType, rawKeys, majList) \
{ \
   for( int col=0; col<dim; col++ ) \
   { \
      qsort( &uelsInCol[uelCount*col], count[col], sizeof(npy_uint32), compare_npy_uint32 ); \
   } \
   for( int col=0; col<dim; col++ ) \
   { \
      for( int uelidx=0; uelidx<count[col]; uelidx++ ) \
      { \
         mapUel[col*uelCount+uelsInCol[uelCount*col + uelidx]-1] = uelidx; \
      } \
   } \
   for( int rec=0; rec<nrRecs; rec++ ) \
   { \
      for( int col=0; col<dim; col++ ) \
      { \
         switch( keysType ) \
         { \
            case NPY_UINT8: \
               ((npy_uint8 *)rawKeys)[rec*dim+col] = mapUel[col*uelCount + ((npy_uint8 *)rawKeys)[rec*dim + col]]; break; \
            case NPY_UINT16: \
               ((npy_uint16 *)rawKeys)[rec*dim+col] = mapUel[col*uelCount + ((npy_uint16 *)rawKeys)[rec*dim + col]]; break; \
            case NPY_UINT32: \
               ((npy_uint32 *)rawKeys)[rec*dim+col] = mapUel[col*uelCount + ((npy_uint32 *)rawKeys)[rec*dim + col]]; break; \
            default: \
               ERROR("Unsupported data type."); \
         } \
      } \
   } \
   majList = PyList_New(dim); \
   for( int col=0; col<dim; col++ ) \
   { \
      PyObject *l = PyList_New(0); \
      for( int i=0; i<count[col]; i++ ) \
      { \
         PyList_Append(l, PyList_GET_ITEM(uelList, uelsInCol[uelCount*col + i])); \
      } \
      PyList_SET_ITEM(majList, col, l); \
   } \
   FREE_CAT_DS(mapUel, uelsInCol); \
}

#define FREE_UEL_MAP(uelMap, dim) \
{ \
   for( int i=0; i<dim; i++) \
   { \
      free(uelMap[i]); \
      uelMap[i] = NULL; \
   } \
   free(uelMap); \
   uelMap = NULL; \
}

#define CREATE_UEL_MAP_CAT(majorList, dim, uelMap, gmd, gdx) \
{ \
   if( !PyList_Check(majorList) ) \
   { \
      ERROR("Parameter majorList needs to be of type list"); \
   } \
   for( int col=0; col<dim; col++ ) \
   { \
      if( !PyList_Check(PyList_GET_ITEM(majorList, col)) ) \
      { \
         ERROR("Items in majorList need to be of type list"); \
      } \
   } \
   if( PyList_Size(majorList) != dim) \
   { \
      ERROR("Length of majorList needs to match the dimensionality of the symbol"); \
   } \
   uelMap = malloc(dim * sizeof(npy_uint32*)); \
   for( int col=0; col<dim; col++ ) \
   { \
      uelMap[col] = malloc(PyList_Size(PyList_GET_ITEM(majorList, col)) * sizeof(npy_uint32)); \
   } \
   for( int col=0; col<dim; col++ ) \
   { \
      PyObject *l = PyList_GET_ITEM(majorList, col); \
      int uel; \
      PyObject *item = NULL; \
      char *label = NULL; \
      int rc = 0; \
      for( int i=0; i<PyList_Size(l); i++) \
      { \
         item = PyList_GET_ITEM(l, i); \
         if( PyUnicode_Check(item) ) \
         { \
            label = (char *) PyUnicode_AsUTF8(item); \
         } \
         else \
         { \
            FREE_UEL_MAP(uelMap, dim); \
            char errorMsg[GMS_SSSIZE]; \
            sprintf(errorMsg, "Expected type str but got %s", item->ob_type->tp_name); \
            ERROR(errorMsg); \
         } \
         if( gmd != NULL ) \
         { \
            rc = gmdFindUel(gmd, label, &uel); \
         } \
         else if ( gdx != NULL ) \
         { \
            int dummy; \
            rc = gdxUMFindUEL(gdx, label, &uel, &dummy); \
         } \
         else \
         { \
            FREE_UEL_MAP(uelMap, dim); \
            ERROR("Neither GMD nor GDX handle has been specified"); \
         } \
         if( rc == 0 ) \
         { \
            FREE_UEL_MAP(uelMap, dim); \
            if( gmd != NULL ) \
            { \
               LAST_ERROR_GMD(gmd); \
            } \
            else if ( gdx != NULL ) \
            { \
               LAST_ERROR_GDX(gdx); \
            } \
         } \
         uelMap[col][i] = uel; \
      } \
   } \
}

#define CREATE_UEL_MAP_CAT_GDX(majorList, dim, uelMap, gdx) \
{ \
   CREATE_UEL_MAP_CAT(majorList, dim, uelMap, NULL, gdx); \
}

#define CREATE_UEL_MAP_CAT_GMD(majorList, dim, uelMap, gmd) \
{ \
   CREATE_UEL_MAP_CAT(majorList, dim, uelMap, gmd, NULL); \
}

#define SET_DOMAINS_GDX(gdx, domains) \
{ \
   if( domains != Py_None ) \
   { \
      if( !PyList_Check(domains) ) \
      { \
         ERROR("Expected a list for parameter domains"); \
      } \
      int size = PyList_Size(domains); \
      if( size != dim ) \
      { \
         ERROR("Length of domain list and dimension does not match"); \
      } \
      char **doms = (char **) malloc((size+1)*sizeof(char *)); \
      for( int i = 0; i < size; i++ ) \
      { \
         PyObject* o = PyList_GetItem(domains,i); \
         if( PyUnicode_Check(o) ) \
         { \
            doms[i] = (char *) PyUnicode_AsUTF8(o); \
         } \
         else \
         { \
            free((char **) doms); \
            ERROR("Parameter domains has to contain strings only"); \
         } \
         doms[size]=0; \
      } \
      int error_code = gdxSymbolSetDomain(gdx, (const char **) doms); \
      free((char **) doms); \
      if( !error_code ) \
      { \
         LAST_ERROR_GDX(gdx); \
      } \
   } \
}

#define FREE_CAT_DS(mapUel, uelsInCol) \
{ \
   free(mapUel); \
   mapUel = NULL; \
   free(uelsInCol); \
   uelsInCol = NULL; \
}

#define EPS_TO_ZERO_PAR(values) \
{ \
   if( 0 == values[GMS_VAL_LEVEL] ) \
   { \
      values[GMS_VAL_LEVEL] = 0; \
   } \
}

#define EPS_TO_ZERO_VAR_EQU(values) \
{ \
   for( int v = 0; v < GMS_VAL_MAX; v++ ) \
   { \
      if( 0 == values[v] ) \
      { \
         values[v] = 0; \
      } \
   } \
}

// prototype declarations
int compare_npy_uint32( const void* a, const void* b);
void npSetString (PyArrayObject* arr, int i, int j, char* str, const char* encoding);
PyMODINIT_FUNC PyInit__gams2numpy (void);
int gdxReadFastExCB(const int k[], const double v[], int dimFrst, void *usermem);

struct ReadRawFastExData
{
   void* rawKeys;
   void* rawValues;
   int* count;
   int dim;
   int keysType;
   int rec;
   int symType;
   npy_uint32 *mapUel;
   npy_uint32 *uelsInCol;
   int uelCount;
   PyObject *uelList;
   PyObject *strPool;
   int strCount;
   char *encoding;
   PyArrayObject *arrKeys;
   PyArrayObject *arrValues;
   int mode;
   char *errorMsg;
};

//We assume that the stucture of SwigPyObject to be like this
typedef struct
{
   PyObject_HEAD
   void *ptr; // this is the pointer we are interested in
   void *ty;  // originally swig_type_info
   int own;
   PyObject *next;
}
SwigPyObject;

int compare_npy_uint32( const void* a, const void* b)
{
     return ( *(npy_uint32*)a - *(npy_uint32*)b );
}

void npSetString(
   PyArrayObject* arr,
   int i,
   int j,
   char* str,
   const char* encoding
)
{
   void* p = PyArray_GETPTR2(arr, i, j);
   PyObject* setStr;
   if( NULL == encoding )
   {
      setStr = PyUnicode_FromString(str);
      if( PyErr_Occurred() != NULL )
      {
         PyErr_Clear();
         setStr = PyUnicode_DecodeUTF8(str, strlen(str), "backslashreplace");
      }
   }
   else
   {
      setStr = PyUnicode_Decode(str, strlen(str), encoding, "backslashreplace");
   }
   PyArray_SETITEM(arr, p, setStr);
   Py_DECREF(setStr);
}


static PyObject* gdxGetSymbolExplTxt(
   PyObject * self,
   PyObject * args
)
{
   char *encoding = NULL;
   gdxHandle_t gdx;
   int symNr;
   SwigPyObject* gdxHandle = NULL;

   if( !PyArg_ParseTuple(args, "Oi|z", &gdxHandle, &symNr, &encoding) )
   {
      ERROR("Error while parsing arguments");
   }

   gdx = (gdxHandle_t)gdxHandle->ptr;
   int nrRecs;
   char explText[GMS_SSSIZE];
   int userInfo;

   if( !gdxSymbolInfoX(gdx, symNr, &nrRecs, &userInfo, explText) ) {
      char errorMsg[GMS_SSSIZE];
      sprintf(errorMsg, "Problems getting symbol information for symbol number %d", symNr);
      ERROR(errorMsg);
   }

   PyObject* setStr;
   if( NULL == encoding )
   {
      setStr = PyUnicode_FromString(explText);
      if( PyErr_Occurred() != NULL )
      {
         PyErr_Clear();
         setStr = PyUnicode_DecodeUTF8(explText, strlen(explText), "backslashreplace");
      }
   }
   else
   {
      setStr = PyUnicode_Decode(explText, strlen(explText), encoding, "backslashreplace");
   }
   return setStr;
}

static PyObject* gmdGetSymbolExplTxt(
   PyObject* self,
   PyObject* args
)
{
   SwigPyObject* gmdHandle = NULL;
   SwigPyObject* symbol = NULL;
   char *encoding = NULL;

   if( !PyArg_ParseTuple(args, "OO|z", &gmdHandle, &symbol, &encoding) )
   {
      ERROR("Error while parsing arguments");
   }

   gmdHandle_t gmd = (gmdHandle_t)gmdHandle->ptr;
   void* symPtr = (void*)symbol->ptr;
   int rc;
   char explText[GMS_SSSIZE];
   gmdSymbolInfo(gmd, symPtr, GMD_EXPLTEXT, NULL , NULL, explText);

   PyObject* setStr;
   if( NULL == encoding )
   {
      setStr = PyUnicode_FromString(explText);
      if( PyErr_Occurred() != NULL )
      {
         PyErr_Clear();
         setStr = PyUnicode_DecodeUTF8(explText, strlen(explText), "backslashreplace");
      }
   }
   else
   {
      setStr = PyUnicode_Decode(explText, strlen(explText), encoding, "backslashreplace");
   }
   return setStr;
}

static PyObject* gdxRegisterUels(
   PyObject* self,
   PyObject* args
)
{
   SwigPyObject* gdxHandle = NULL;
   PyObject* uelList = NULL;
   if( !PyArg_ParseTuple(args, "OO", &gdxHandle, &uelList) )
   {
      ERROR("Error while parsing arguments");
   }
   gdxHandle_t gdx = (gdxHandle_t)gdxHandle->ptr;

   if( !PyList_Check(uelList) )
   {
       ERROR("Argument 'uelList' must be of type list");
   }

   int uelCount = PyList_Size(uelList);
   char *label = NULL;
   int uelnr;

   gdxUELRegisterStrStart(gdx);
   for( int i = 0; i < uelCount; i++ )
   {
      PyObject *item = PyList_GET_ITEM(uelList, i);
      if( PyUnicode_Check(item) )
      {
         label = (char *) PyUnicode_AsUTF8(item);
         if( !gdxUELRegisterStr(gdx, label, &uelnr) )
         {
               char errorMsg[GMS_SSSIZE];
               sprintf(errorMsg, "Could not register UEL: %s", label);
               gdxUELRegisterDone(gdx);
               ERROR(errorMsg);
         }
      }
      else
      {
         gdxUELRegisterDone(gdx);
         ERROR("Argument 'uelList' has to contain strings only");
      }
   }
   gdxUELRegisterDone(gdx);
   return Py_None;
}


static PyObject* gmdRegisterUels(
   PyObject* self,
   PyObject* args
)
{
   SwigPyObject* gmdHandle = NULL;
   PyObject* uelList = NULL;
   if( !PyArg_ParseTuple(args, "OO", &gmdHandle, &uelList) )
   {
      ERROR("Error while parsing arguments");
   }
   gmdHandle_t gmd = (gmdHandle_t)gmdHandle->ptr;

   if( !PyList_Check(uelList) )
   {
       ERROR("Argument 'uelList' must be of type list");
   }

   int uelCount = PyList_Size(uelList);
   char *label = NULL;
   int uelnr;

   for( int i = 0; i < uelCount; i++ )
   {
      PyObject *item = PyList_GET_ITEM(uelList, i);
      if( PyUnicode_Check(item) )
      {
         label = (char *) PyUnicode_AsUTF8(item);
         if( !gmdMergeUel(gmd, label, &uelnr) )
         {
               char errorMsg[GMS_SSSIZE];
               sprintf(errorMsg, "Could not register UEL: %s", label);
               ERROR(errorMsg);
         }
      }
      else
      {
         ERROR("Argument 'uelList' has to contain strings only");
      }
   }
   return Py_None;
}

static PyObject* i_gdxCreateUelList(
   gdxHandle_t gdx,
   const char *encoding
)
{
   int symCount;
   int uelCount;
   int n;
   if( !gdxSystemInfo(gdx, &symCount, &uelCount) )
   {
      ERROR("Problems getting system information");
   }
   char label[GMS_SSSIZE];
   PyObject* uelList = PyList_New(uelCount+1);
   for( int i = 0; i <= uelCount; i++ )
   {
      gdxUMUelGet(gdx, i, label, &n);
      PyObject* setStr;
      if( NULL == encoding )
      {
         setStr = PyUnicode_FromString(label);
         if( PyErr_Occurred() != NULL )
         {
            PyErr_Clear();
            setStr = PyUnicode_DecodeUTF8(label, strlen(label), "backslashreplace");
         }
      }
      else
      {
         setStr = PyUnicode_Decode(label, strlen(label), encoding, "backslashreplace");
      }
      PyList_SET_ITEM(uelList, i, setStr);
   }
   return uelList;
}

static PyObject* gdxGetUelList(
   PyObject* self,
   PyObject* args
)
{
   SwigPyObject* gdxHandle = NULL;
   char *encoding = NULL;
   if( !PyArg_ParseTuple(args, "O|z", &gdxHandle, &encoding) )
   {
      ERROR("Error while parsing arguments");
   }
   gdxHandle_t gdx = (gdxHandle_t)gdxHandle->ptr;

   PyObject* uelList = i_gdxCreateUelList(gdx, encoding);
   if( uelList == Py_None )
   {
      return (PyObject *) NULL;
   }
   return uelList;
}

static PyObject* i_gmdCreateUelList(
   gmdHandle_t gmd,
   const char *encoding
)
{
   int rc;
   int uelCount = 0;
   rc = gmdInfo(gmd, GMD_NRUELS, &uelCount, NULL, NULL);
   if( !rc )
   {
      ERROR("Problems getting system information");
   }
   char label[GMS_SSSIZE];
   PyObject* uelList = PyList_New(uelCount+1);
   PyList_SET_ITEM(uelList, 0, PyUnicode_FromString("INVALID"));
   for( int i = 1; i <= uelCount; i++ )
   {
      rc = gmdGetUelByIndex(gmd, i, label);
      PyObject* setStr;
      if( NULL == encoding )
      {
         setStr = PyUnicode_FromString(label);
         if( PyErr_Occurred() != NULL )
         {
            PyErr_Clear();
            setStr = PyUnicode_DecodeUTF8(label, strlen(label), "backslashreplace");
         }
      }
      else
      {
         setStr = PyUnicode_Decode(label, strlen(label), encoding, "backslashreplace");
      }
      PyList_SET_ITEM(uelList, i, setStr);
   }
   return uelList;
}

static PyObject* gmdGetUelList(
   PyObject* self,
   PyObject* args
)
{
   SwigPyObject* gmdHandle = NULL;
   char *encoding = NULL;
   if( !PyArg_ParseTuple(args, "O|z", &gmdHandle, &encoding) )
   {
      ERROR("Error while parsing arguments");
   }
   gmdHandle_t gmd = (gmdHandle_t)gmdHandle->ptr;

   PyObject* uelList = i_gmdCreateUelList(gmd, encoding);
   if( uelList == Py_None )
   {
      return (PyObject *) NULL;
   }
   return uelList;
}

#define NP_SET_KEYS_INT(rawKeys, keysIn, idxOut, idxIn, keysType, inOffset) \
{ \
   switch (keysType) \
   { \
      case NPY_INT32: \
         ((npy_int32 *) rawKeys)[idxOut] = keysIn[idxIn]+inOffset; break; \
      case NPY_UINT8: \
         ((npy_uint8 *) rawKeys)[idxOut] = keysIn[idxIn]+inOffset; break; \
      case NPY_UINT16: \
         ((npy_uint16 *) rawKeys)[idxOut] = keysIn[idxIn]+inOffset; break; \
      case NPY_UINT32: \
         ((npy_uint32 *) rawKeys)[idxOut] = keysIn[idxIn]+inOffset; break; \
   } \
}

#define NP_SET_KEYS_STR(arrKeys, keys, rec, i, uelCount, uelList, encoding) \
{ \
   if( ( keys[i] < 0 ) || ( keys[i] > uelCount ) ) \
   { \
      char label[GMS_UEL_IDENT_SIZE]; \
      sprintf(label, "L__%d", keys[i]); \
      npSetString(arrKeys, rec, i, label, encoding); \
   } \
   else \
   { \
      void* npItemPtr = PyArray_GETPTR2(arrKeys, rec, i); \
      PyArray_SETITEM(arrKeys, npItemPtr, PyList_GET_ITEM(uelList, keys[i])); \
   } \
}

#define NP_GET_KEYS_INT(rawKeys, keys, keysLayout, keysType, i, j, dim, nrRecs) \
{ \
   int idx = -1; \
   switch( keysLayout ) \
   { \
      case C_LAYOUT: idx = i*dim+j; break; \
      case F_LAYOUT: idx = i+j*nrRecs; break; \
   } \
   switch( keysType ) \
   { \
      case NPY_INT8: \
         keys[j] = ((npy_int8 *)rawKeys)[idx]; break; \
      case NPY_INT16: \
         keys[j] = ((npy_int16 *)rawKeys)[idx]; break; \
      case NPY_INT32: \
         keys[j] = ((npy_int32 *)rawKeys)[idx]; break; \
      case NPY_INT64: \
         keys[j] = ((npy_int64 *)rawKeys)[idx]; break; \
      case NPY_UINT8: \
         keys[j] = ((npy_uint8 *)rawKeys)[idx]; break; \
      case NPY_UINT16: \
         keys[j] = ((npy_uint16 *)rawKeys)[idx]; break; \
      case NPY_UINT32: \
         keys[j] = ((npy_uint32 *)rawKeys)[idx]; break; \
      default: \
         ERROR("Unsupported data type."); \
   } \
}

#define NP_GET_KEYS_CAT(rawKeys, keys, keysLayout, keysType, i, j, dim, nrRecs, uelMap) \
{ \
   int idx = -1; \
   switch( keysLayout ) \
   { \
      case C_LAYOUT: idx = i*dim+j; break; \
      case F_LAYOUT: idx = i+j*nrRecs; break; \
   } \
   switch( keysType ) \
   { \
      case NPY_INT8: \
         keys[j] = uelMap[j][((npy_int8 *)rawKeys)[idx]]; break; \
      case NPY_INT16: \
         keys[j] = uelMap[j][((npy_int16 *)rawKeys)[idx]]; break; \
      case NPY_INT32: \
         keys[j] = uelMap[j][((npy_int32 *)rawKeys)[idx]]; break; \
      case NPY_INT64: \
         keys[j] = uelMap[j][((npy_int64 *)rawKeys)[idx]]; break; \
      case NPY_UINT8: \
         keys[j] = uelMap[j][((npy_uint8 *)rawKeys)[idx]]; break; \
      case NPY_UINT16: \
         keys[j] = uelMap[j][((npy_uint16 *)rawKeys)[idx]]; break; \
      case NPY_UINT32: \
         keys[j] = uelMap[j][((npy_uint32 *)rawKeys)[idx]]; break; \
      default: \
         ERROR("Unsupported data type."); \
   } \
}

#define NP_GET_VALUES_PAR_VAR_EQU(rawValues, values, symType) \
{ \
   if( symType == GMS_DT_PAR ) \
   { \
      values[0] = ((npy_double *)rawValues)[i]; \
   } \
   else if( symType == GMS_DT_VAR || symType == GMS_DT_EQU ) \
   { \
      int idx = -1; \
      for( int j = 0; j < GMS_VAL_MAX; j++ ) \
      { \
         switch( valuesLayout ) \
         { \
            case C_LAYOUT: idx = i*GMS_VAL_MAX+j; break; \
            case F_LAYOUT: idx = i+j*nrRecs; break; \
         } \
         values[j] = ((npy_double *)rawValues)[idx]; \
      } \
   } \
}

#define NP_GET_VALUES_GDX(rawValues, values, symType, setText, gdx, nrValCols) \
{ \
   NP_GET_VALUES_PAR_VAR_EQU(rawValues, values, symType) \
   if( (symType == GMS_DT_SET || symType == GMS_DT_ALIAS) && nrValCols != 0 ) \
   { \
      NP_GET_STRING_GDX(arrValues, i, 0, setText, gdx); \
      gdxAddSetText(gdx, setText, &txtNr); \
      values[GMS_VAL_LEVEL] = txtNr; \
   } \
} \

#define NP_GET_VALUES_GMD(rawValues, values, symType, setText, gmd, nrValCols) \
{ \
   NP_GET_VALUES_PAR_VAR_EQU(rawValues, values, symType) \
   if( (symType == GMS_DT_SET || symType == GMS_DT_ALIAS) && nrValCols == 1 ) \
   { \
      NP_GET_STRING(arrValues, i, 0, setText); \
   } \
} \

static PyObject* gdxReadSymbol(
   PyObject * self,
   PyObject * args
)
{
   char* symName;
   int mode;
   int createUelList = 0;
   char *encoding = NULL;

   gdxHandle_t gdx;
   SwigPyObject* gdxHandle = NULL;
   PyObject* uelList = NULL;

   if( !PyArg_ParseTuple(args, "Osi|Oz", &gdxHandle, &symName, &mode, &uelList, &encoding) )
   {
      ERROR("Error while parsing arguments");
   }

   if( mode != MODE_RAW && mode != MODE_STRING && mode != MODE_CATEGORICAL)
   {
      ERROR("Unsupported mode.");
   }

   gdx = (gdxHandle_t)gdxHandle->ptr;
   char name[GMS_SSSIZE];
   int symNr;
   int dim;
   int symType;
   int nrRecs;
   int symCount;
   int uelCount;
   int strCount = 0;
   int nvalcols;
   char explText[GMS_SSSIZE];
   int userInfo;

   if( !gdxFindSymbol(gdx, symName, &symNr) )
   {
      char errorMsg[GMS_SSSIZE];
      sprintf(errorMsg, "Could not find symbol %s", symName);
      ERROR(errorMsg);
   }

   if( !gdxSymbolInfo(gdx, symNr, name, &dim, &symType) )
   {
      char errorMsg[GMS_SSSIZE];
      sprintf(errorMsg, "Problems getting symbol information for symbol %s", symName);
      ERROR(errorMsg);
   }
   if( !gdxSymbolInfoX(gdx, symNr, &nrRecs, &userInfo, explText) ) {
      char errorMsg[GMS_SSSIZE];
      sprintf(errorMsg, "Problems getting symbol information for symbol number %d", symNr);
      ERROR(errorMsg);
   }
   if( !gdxSystemInfo(gdx, &symCount, &uelCount) )
   {
      ERROR("Problems getting system information");
   }

   GET_VAL_COL_COUNT(symType, nvalcols);
   CHECK_CREATE_UELLIST_GDX(mode, uelList, createUelList, uelCount, gdx, encoding);

   PyObject* strPool = NULL;

   if( symType == GMS_DT_SET || symType == GMS_DT_ALIAS )
   {
      strPool = PyList_New(0);
      PyObject* label = PyUnicode_FromString("");
      PyList_Append(strPool, label);
      Py_DECREF(label);

      strCount = 1;
      char text[GMS_SSSIZE];
      int node = 0;
      while( gdxGetElemText(gdx, strCount, text, &node) )
      {
         PyObject* setStr;
         if( NULL == encoding )
         {
            setStr = PyUnicode_FromString(text);
            if( PyErr_Occurred() != NULL )
            {
               PyErr_Clear();
               setStr = PyUnicode_DecodeUTF8(text, strlen(text), "backslashreplace");
            }
         }
         else
         {
            setStr = PyUnicode_Decode(text, strlen(text), encoding, "backslashreplace");
         }

         PyList_Append(strPool, setStr);
         Py_DECREF(setStr);
         strCount++;
      }
   }

   // Create Numpy Arrays
   int keysType = -1;
   int valuesType = -1;

   // sizes
   npy_intp keysShape[2] = { nrRecs, dim };
   npy_intp valuesShape[2] = { nrRecs, nvalcols };
   GET_ARR_TYPES(mode, symType, uelCount, keysType, valuesType);

   int count[GMS_MAX_INDEX_DIM];
   npy_uint32 *mapUel = NULL;
   npy_uint32 *uelsInCol = NULL;
   if( mode == MODE_CATEGORICAL )
   {
      PREP_DS_CAT(mode, count, mapUel, uelsInCol, uelCount, dim);
   }

   // create arrays
   PyArrayObject *arrKeys = (PyArrayObject *) PyArray_SimpleNew(2, keysShape, keysType);
   PyArrayObject *arrValues = (PyArrayObject *) PyArray_SimpleNew(2, valuesShape, valuesType);
   if( NULL == arrKeys || NULL == arrValues )
   {
      if( mode == MODE_CATEGORICAL)
      {
         FREE_CAT_DS(mapUel, uelsInCol);
      }
      ERROR("Error creating arrays");
   }
   void *rawKeys = PyArray_DATA(arrKeys);
   void *rawValues = PyArray_DATA(arrValues);

   struct ReadRawFastExData usermem =
   {
      .rawKeys = rawKeys,
      .rawValues = rawValues,
      .arrKeys = arrKeys,
      .arrValues = arrValues,
      .dim = dim,
      .rec = 0,
      .symType = symType,
      .mapUel = mapUel,
      .uelsInCol = uelsInCol,
      .uelCount = uelCount,
      .uelList = uelList,
      .count = count,
      .keysType = keysType,
      .strPool = strPool,
      .encoding = encoding,
      .strCount = strCount,
      .mode = mode,
      .errorMsg = NULL,
   };
   int recCount = 0;

   int rc = gdxDataReadRawFastEx( gdx, symNr, gdxReadFastExCB, &recCount, &usermem );
   // free
   if( strPool != NULL )
   {
      Py_DECREF(strPool);
      strPool = NULL;
   }

   if( !rc || usermem.errorMsg != NULL )
   {
      Py_DECREF(arrKeys);
      arrKeys = NULL;
      Py_DECREF(arrValues);
      arrValues = NULL;
      if( createUelList )
      {
         Py_DECREF(uelList);
         uelList = NULL;
      }
      if( mode == MODE_CATEGORICAL )
      {
         FREE_CAT_DS(mapUel, uelsInCol);
      }
      if( usermem.errorMsg != NULL )
      {
         ERROR(usermem.errorMsg);
      }
      else // !rc
      {
         LAST_ERROR_GDX(gdx);
      }
   }

   PyObject *majList = NULL;
   if( mode == MODE_CATEGORICAL)
   {
      REMAP_CAT(mode, dim, nrRecs, mapUel, uelsInCol, uelCount, uelList, count, keysType, rawKeys, majList);
   }

   if( createUelList )
   {
      Py_DECREF(uelList);
      uelList = NULL;
   }

   PyObject *ret = PyTuple_New(mode == MODE_RAW || mode == MODE_STRING ? 2 : 3);
   PyTuple_SetItem(ret, 0, (PyObject *)arrKeys);
   PyTuple_SetItem(ret, 1, (PyObject *)arrValues);
   if ( mode == MODE_CATEGORICAL )
   {
      PyTuple_SetItem(ret, 2, majList);
   }
   return ret;
}

int gdxReadFastExCB(const int k[], const double v[], int dimFrst, void *usermem)
{
   struct ReadRawFastExData *um = (struct ReadRawFastExData *)usermem;
   void *rawKeys = um->rawKeys;
   double *rawValues = um->rawValues;
   int keysType = um->keysType;
   int rec = um->rec;
   int dim = um->dim;
   int symType = um->symType;
   int uelCount = um->uelCount;
   PyObject *uelList = um->uelList;
   npy_uint32 *mapUel = um->mapUel;
   npy_uint32 *uelsInCol = um->uelsInCol;
   int *count = um->count;
   if( dim !=0 ) {
      if( um->mode != MODE_STRING ) {  // no memcpy for string mode
         if( dimFrst > 1 ) {
            int copyToIdx = rec*dim;
            int copyFromIdx = (rec-1)*dim;
            int copySize = dimFrst-1;
            switch( keysType ) {
               case NPY_INT32:
                  memcpy( &((npy_int32 *) rawKeys)[copyToIdx],  &((npy_int32 *) rawKeys)[copyFromIdx], copySize * sizeof(npy_int32) ); break;
               case NPY_UINT8:
                  memcpy( &((npy_uint8 *) rawKeys)[copyToIdx], &((npy_uint8 *) rawKeys)[copyFromIdx], copySize * sizeof(npy_int8) ); break;
               case NPY_UINT16:
                  memcpy( &((npy_uint16 *) rawKeys)[copyToIdx],  &((npy_uint16 *) rawKeys)[copyFromIdx], copySize * sizeof(npy_int16) ); break;
               case NPY_UINT32:
                  memcpy( &((npy_uint32 *) rawKeys)[copyToIdx],  &((npy_uint32 *) rawKeys)[copyFromIdx], copySize * sizeof(npy_int32) ); break;
            }
         }
      }

      if( um->mode == MODE_RAW )
      {
         for( int i = dimFrst-1; i < dim; i++ )
         {
            NP_SET_KEYS_INT(rawKeys, k, rec*dim+i, i, keysType, 0);
         }
      }
      else if( um->mode == MODE_STRING )
      {
         PyArrayObject *arrKeys = um->arrKeys;
         for( int i = 0; i < dim; i++ )
         {
            NP_SET_KEYS_STR(arrKeys, k, rec, i, uelCount, uelList, um->encoding);
         }
      }
      else if( um->mode == MODE_CATEGORICAL )
      {
         for( int i = dimFrst-1; i < dim; i++ )
         {
            int uel = k[i];
            if( uel < 0 || uel > uelCount )
            {
               um->errorMsg = "Found invalid UEL not supported when reading categorical";
               return 0;
            }
            int idx = i*(uelCount) + uel -1;
            if( !mapUel[idx] )
            {
               mapUel[idx] = 1;
               uelsInCol[uelCount*i + count[i]] = uel;
               count[i]++;
            }
            NP_SET_KEYS_INT(rawKeys, k, rec*dim+i, i, keysType, -1);
         }
      }
   }

   if( symType == GMS_DT_SET || symType == GMS_DT_ALIAS )
   {
      PyArrayObject *arrValues = um->arrValues;
      int strIdx = (int) v[GMS_VAL_LEVEL];
      void *npItemPtr = PyArray_GETPTR2(arrValues, rec, 0);
      if( ( strIdx < 0 ) || ( strIdx >= um->strCount ) )
      {
         char text[GMS_SSSIZE];
         sprintf(text, "?Str__%d", strIdx);
         npSetString(arrValues, rec, 0, text, um->encoding);
      }
      else
      {
         PyArray_SETITEM(arrValues, npItemPtr, PyList_GET_ITEM(um->strPool, strIdx));
      }
   }
   else if( symType == GMS_DT_PAR )
   {
      rawValues[rec] = v[GMS_VAL_LEVEL];
   }
   else {
      for( int i = 0; i < GMS_VAL_MAX; i++ )
      {
         rawValues[rec*GMS_VAL_MAX+i] = v[i];
      }
   }
   um->rec++;
   return 1;
}


static PyObject* gdxWriteSymbol(
   PyObject* self,
   PyObject* args
)
{
   SwigPyObject* gdxHandle = NULL;
   char* symName;
   char* explText;
   int dim;
   int type;
   int subType;
   PyArrayObject* arrKeys = NULL;
   PyArrayObject* arrValues = NULL;
   PyObject* majorList = NULL;
   int mode;
   PyObject* domains = NULL;

   if( !PyArg_ParseTuple(args, "OssiiiOOOiO", &gdxHandle, &symName, &explText, &dim, &type, &subType, &arrKeys, &arrValues, &majorList, &mode, &domains) )
   {
      ERROR("Error while parsing arguments");
   }

   if( mode != MODE_RAW && mode != MODE_STRING && mode != MODE_MAP && mode != MODE_CATEGORICAL )
   {
      ERROR("Unsupported mode.");
   }

   gdxHandle_t gdx = (gdxHandle_t)gdxHandle->ptr;

   int nrRecs;
   int nrValCols;
   int keysLayout;
   int valuesLayout;
   int keysType;
   int valuesType;
   npy_uint32 **uelMap = NULL;
   VALIDATE_ARRAYS(arrKeys, arrValues, dim, type, nrRecs, nrValCols, keysLayout, valuesLayout, keysType, valuesType);

   if( type == GMS_DT_PAR || type == GMS_DT_VAR || type == GMS_DT_EQU )
   {
      if( valuesType != NPY_DOUBLE )
      {
         ERROR_GDX("Unsupported data type.", gdx);
      }
   }

   if( mode == MODE_CATEGORICAL )
   {
      CREATE_UEL_MAP_CAT_GDX(majorList, dim, uelMap, gdx);
   }

   void *rawKeys = PyArray_DATA(arrKeys);
   void *rawValues = PyArray_DATA(arrValues);
   double values[GMS_VAL_MAX];
   char* setText = "";
   int txtNr;
   int rc = 0;

   if( mode == MODE_RAW || mode == MODE_MAP || mode == MODE_CATEGORICAL )
   {
      if( mode == MODE_RAW )
      {
         rc = gdxDataWriteRawStart(gdx, symName, explText, dim, type, subType);
      }
      else  // map, categorical
      {
         rc = gdxDataWriteMapStart(gdx, symName, explText, dim, type, subType);
      }

      if( !rc )
      {
         if( mode == MODE_CATEGORICAL)
         {
            FREE_UEL_MAP(uelMap, dim);
         }
         LAST_ERROR_GDX(gdx);
      }
      SET_DOMAINS_GDX(gdx, domains);

      int keys[GMS_MAX_INDEX_DIM];
      for( int i = 0; i < nrRecs; i++ )
      {
         for( int j = 0; j < dim; j++ )
         {
            if( mode == MODE_CATEGORICAL)
            {
               NP_GET_KEYS_CAT(rawKeys, keys, keysLayout, keysType, i, j, dim, nrRecs, uelMap);
            }
            else
            {
               NP_GET_KEYS_INT(rawKeys, keys, keysLayout, keysType, i, j, dim, nrRecs);
            }
         }
         NP_GET_VALUES_GDX(rawValues, values, type, setText, gdx, nrValCols);

         if( mode == MODE_RAW )
         {
            rc = gdxDataWriteRaw(gdx, keys, values);
         }
         else  // map, categorical
         {
            rc = gdxDataWriteMap(gdx, keys, values);
         }
         if( !rc )
         {
            if( mode == MODE_CATEGORICAL)
            {
               FREE_UEL_MAP(uelMap, dim);
            }
            LAST_ERROR_GDX(gdx);
         }
      }
      if( mode == MODE_CATEGORICAL)
      {
         FREE_UEL_MAP(uelMap, dim);
      }

      rc = gdxDataWriteDone(gdx);
      if( !rc )
      {
         LAST_ERROR_GDX(gdx);
      }
   }
   else // write string
   {
      gdxStrIndexPtrs_t Indx;
      gdxStrIndex_t     IndxXXX;
      GDXSTRINDEXPTRS_INIT(IndxXXX, Indx);
      if( !gdxDataWriteStrStart(gdx, symName, explText, dim, type, subType) )
      {
         LAST_ERROR_GDX(gdx);
      }

      SET_DOMAINS_GDX(gdx, domains);

      for( int i = 0; i < nrRecs; i++ )
      {
         for( int j = 0; j < dim; j++ )
         {
            NP_GET_STRING_GDX(arrKeys, i, j, Indx[j], gdx);
         }
         NP_GET_VALUES_GDX(rawValues, values, type, setText, gdx, nrValCols);

         if( !gdxDataWriteStr(gdx, (const char **) Indx, values) )
         {
            LAST_ERROR_GDX(gdx);
         }
      }
      rc = gdxDataWriteDone(gdx);
      if( !rc )
      {
         LAST_ERROR_GDX(gdx);
      }
   }
   Py_RETURN_NONE;
}


static PyObject* gmdReadSymbol(
   PyObject* self,
   PyObject* args
)
{
   int rc;
   char* symName;
   gmdHandle_t gmd;
   SwigPyObject* gmdHandle = NULL;
   PyObject* uelList = NULL;
   int mode = 0;
   int createUelList = 0;
   char *encoding = NULL;
   int keysType = -1;
   int valuesType = -1;
   int nvalcols;

   if( !PyArg_ParseTuple(args, "Osi|Oz", &gmdHandle, &symName, &mode, &uelList, &encoding) )
   {
      ERROR("Error while parsing arguments");
   }

   if( mode != MODE_RAW && mode != MODE_STRING && mode != MODE_CATEGORICAL )
   {
      ERROR("Unsupported mode.");
   }

   gmd = (gmdHandle_t)gmdHandle->ptr;
   void* symPtr = NULL;
   rc = gmdFindSymbol(gmd, symName, &symPtr);
   if( 0 == rc )
   {
      ERROR("Symbol not found");
   }

   int uelCount;
   int symType;
   int dim;
   int nrRecs;
   rc = gmdInfo(gmd, GMD_NRUELS, &uelCount, NULL, NULL);
   rc = gmdSymbolInfo(gmd, symPtr, GMD_TYPE, &symType, NULL, NULL);
   rc = gmdSymbolInfo(gmd, symPtr, GMD_DIM, &dim, NULL, NULL);
   rc = gmdSymbolInfo(gmd, symPtr, GMD_NRRECORDS, &nrRecs, NULL, NULL);

   GET_VAL_COL_COUNT(symType, nvalcols);
   CHECK_CREATE_UELLIST_GMD(mode, uelList, createUelList, uelCount, gmd, encoding);

   npy_intp keysShape[2] = { nrRecs, dim };
   npy_intp valuesShape[2] = { nrRecs, nvalcols };
   GET_ARR_TYPES(mode, symType, uelCount, keysType, valuesType);

   int count[GMS_MAX_INDEX_DIM];
   npy_uint32 *mapUel = NULL;
   npy_uint32 *uelsInCol = NULL;
   void* symIterPtr;

   int keys[GMS_MAX_INDEX_DIM];
   double values[GMS_VAL_MAX];

   if( mode == MODE_CATEGORICAL )
   {
      PREP_DS_CAT(mode, count, mapUel, uelsInCol, uelCount, dim);
   }

   // create arrays
   PyArrayObject *arrKeys = (PyArrayObject *) PyArray_SimpleNew(2, keysShape, keysType);
   PyArrayObject *arrValues = (PyArrayObject *) PyArray_SimpleNew(2, valuesShape, valuesType);
   if( NULL == arrKeys || NULL == arrValues )
   {
      if( mode == MODE_CATEGORICAL)
      {
         FREE_CAT_DS(mapUel, uelsInCol);
      }
      ERROR("Error creating arrays");
   }
   void *rawKeys = PyArray_DATA(arrKeys);
   void *rawValues = PyArray_DATA(arrValues);

   gmdFindFirstRecord(gmd, symPtr, &symIterPtr);
   for( int rec = 0; rec < nrRecs; rec++ )
   {
      gmdGetRecordRaw(gmd, symIterPtr, dim, keys, values);
      if( mode == MODE_RAW )
      {
         for( int i = 0; i < dim; i++ )
         {
            NP_SET_KEYS_INT(rawKeys, keys, rec*dim+i, i, keysType, 0);
         }
      }
      else if( mode == MODE_STRING )
      {
         for( int i = 0; i < dim; i++ )
         {
            NP_SET_KEYS_STR(arrKeys, keys, rec, i, uelCount, uelList, encoding);
         }
      }
      else if( mode == MODE_CATEGORICAL )
      {
         for( int i = 0; i < dim; i++ )
         {
            int idx = i*uelCount + keys[i] - 1;
            if( keys[i] < 0 || keys[i] > uelCount )
            {
               if( createUelList )
               {
                  Py_DECREF(uelList);
                  uelList = NULL;
               }
               Py_DECREF(arrKeys);
               arrKeys = NULL;
               Py_DECREF(arrValues);
               arrValues = NULL;
               FREE_CAT_DS(mapUel, uelsInCol);
               ERROR("Found invalid UEL not supported when reading categorical");
            }

            if( !mapUel[idx] )
            {
               mapUel[idx] = 1;
               uelsInCol[uelCount*i + count[i]] = keys[i];
               count[i]++;
            }
            NP_SET_KEYS_INT(rawKeys, keys, rec*dim+i, i, keysType, -1);
         }
      }

      char label[GMS_SSSIZE];
      if( symType == GMS_DT_SET || symType == GMS_DT_ALIAS )
      {
         gmdGetElemText(gmd, symIterPtr, label);
         npSetString(arrValues, rec, 0, label, encoding);
      }
      else if( symType == GMS_DT_PAR )
      {
         ((double *)rawValues)[rec] = values[GMS_VAL_LEVEL];
      }
      else if( symType == GMS_DT_VAR || symType == GMS_DT_EQU )
      {
         for( int i = 0; i < GMS_VAL_MAX; i++ )
         {
            ((double *)rawValues)[rec*GMS_VAL_MAX+i] = values[i];
         }
      }
      rc = gmdRecordMoveNext(gmd, symIterPtr);
   }
   gmdFreeSymbolIterator(gmd, symIterPtr);

   PyObject *majList = NULL;
   if( mode == MODE_CATEGORICAL)
   {
      REMAP_CAT(mode, dim, nrRecs, mapUel, uelsInCol, uelCount, uelList, count, keysType, rawKeys, majList);
   }

   if( createUelList )
   {
      Py_DECREF(uelList);
      uelList = NULL;
   }

   PyObject *ret = ( mode == MODE_RAW || mode == MODE_STRING ) ? PyTuple_New(2) : PyTuple_New(3);
   PyTuple_SetItem(ret, 0, (PyObject *)arrKeys);
   PyTuple_SetItem(ret, 1, (PyObject *)arrValues);
   if ( mode == MODE_CATEGORICAL )
   {
      PyTuple_SetItem(ret, 2, majList);
   }
   return ret;
}


static PyObject* gmdFillSymbol(
   PyObject* self,
   PyObject* args
)
{
   SwigPyObject* gmdHandle = NULL;
   SwigPyObject* symbol = NULL;
   PyArrayObject* arrKeys = NULL;
   PyArrayObject* arrValues = NULL;
   PyObject* majorList = NULL;
   int mode = 0;
   int merge = 0;
   int checkUel = 1;
   int epsToZero = 1;

   if( !PyArg_ParseTuple(args, "OOOOOi|ppp", &gmdHandle, &symbol, &arrKeys, &arrValues, &majorList, &mode, &merge, &checkUel, &epsToZero) )
   {
      ERROR("Error while parsing arguments");
   }

   if( mode != MODE_RAW && mode != MODE_STRING && mode != MODE_CATEGORICAL)
   {
      ERROR("Unsupported mode.");
   }

   gmdHandle_t gmd = (gmdHandle_t)gmdHandle->ptr;
   void * symPtr = (void*)symbol->ptr;

   int symType;
   int dim;
   int nrRecsGMD;
   // TODO: check return code
   gmdSymbolInfo(gmd, symPtr, GMD_TYPE, &symType, NULL, NULL);
   gmdSymbolInfo(gmd, symPtr, GMD_DIM, &dim, NULL, NULL);
   gmdSymbolInfo(gmd, symPtr, GMD_NRRECORDS, &nrRecsGMD, NULL, NULL);

   // merge=False -> we expect a symbol that is empty
   if( !merge && nrRecsGMD != 0 )
   {
      ERROR("Symbol already contains records, but needs to be empty");
   }

   int nrRecs;
   int nrValCols;
   int keysLayout;
   int valuesLayout;
   int keysType;
   int valuesType;
   npy_uint32 **uelMap = NULL;
   VALIDATE_ARRAYS(arrKeys, arrValues, dim, symType, nrRecs, nrValCols, keysLayout, valuesLayout, keysType, valuesType);

   if( symType == GMS_DT_PAR || symType == GMS_DT_VAR || symType == GMS_DT_EQU )
   {
      if( valuesType != NPY_DOUBLE )
      {
         ERROR("Unsupported data type.");
      }
   }
   if( mode == MODE_CATEGORICAL )
   {
      CREATE_UEL_MAP_CAT_GMD(majorList, dim, uelMap, gmd);
   }

   void *rawKeys = PyArray_DATA(arrKeys);
   void *rawValues = PyArray_DATA(arrValues);
   char* setText = "";
   void* symIterPtr = NULL;
   double values[GMS_VAL_MAX];
   int rc = 0;

   if( mode == MODE_RAW || mode == MODE_CATEGORICAL )
   {
      int keys[GMS_MAX_INDEX_DIM];

      for( int i = 0; i < nrRecs; i++ )
      {
         for( int j = 0; j < dim; j++ )
         {
            if( mode == MODE_CATEGORICAL )
            {
               NP_GET_KEYS_CAT(rawKeys, keys, keysLayout, keysType, i, j, dim, nrRecs, uelMap);
            }
            else
            {
               NP_GET_KEYS_INT(rawKeys, keys, keysLayout, keysType, i, j, dim, nrRecs);
            }
         }
         NP_GET_VALUES_GMD(rawValues, values, symType, setText, gmd, nrValCols);

         if( symType == GMS_DT_SET || symType == GMS_DT_ALIAS )
         {
            rc = gmdMergeSetRecordInt(gmd, symPtr, keys, checkUel, 0, &symIterPtr, setText);
         }
         else
         {

            if( epsToZero )
            {
               if( symType == GMS_DT_PAR )
               {
                  EPS_TO_ZERO_PAR(values);
               }
               else  // var, equ
               {
                  EPS_TO_ZERO_VAR_EQU(values);
               }
            }

            rc = gmdMergeRecordInt(gmd, symPtr, keys, checkUel, 0, &symIterPtr, 1, values);
         }
         if( !rc )
         {
            if( mode == MODE_CATEGORICAL )
            {
               FREE_UEL_MAP(uelMap, dim);
            }
            LAST_ERROR_GMD(gmd);
         }
      }
      if( mode == MODE_CATEGORICAL )
      {
         FREE_UEL_MAP(uelMap, dim);
      }
   }
   else //write string
   {
      gdxStrIndexPtrs_t Indx;
      gdxStrIndex_t     IndxXXX;
      GDXSTRINDEXPTRS_INIT(IndxXXX, Indx);
      char* label;
      for( int i = 0; i < nrRecs; i++ )
      {
         for( int j = 0; j < dim; j++ )
         {
            NP_GET_STRING(arrKeys, i, j, label);
            Indx[j] = label;
         }
         NP_GET_VALUES_GMD(rawValues, values, symType, setText, gmd, nrValCols);

         if( merge )
         {
            rc = gmdMergeRecord(gmd, symPtr, (const char **) Indx, &symIterPtr);
         }
         else
         {
            rc = gmdAddRecord(gmd, symPtr, (const char **) Indx, &symIterPtr);
         }
         if( !rc )
         {
            LAST_ERROR_GMD(gmd);
         }
         if( symType == GMS_DT_PAR )
         {
            if( epsToZero )
            {
               EPS_TO_ZERO_PAR(values);
            }
            gmdSetLevel(gmd, symIterPtr, values[GMS_VAL_LEVEL]);
         }
         else if( symType == GMS_DT_VAR || symType == GMS_DT_EQU )
         {
            if( epsToZero )
            {
               EPS_TO_ZERO_VAR_EQU(values);
            }
            gmdSetLevel(gmd, symIterPtr, values[GMS_VAL_LEVEL]);
            gmdSetMarginal(gmd, symIterPtr, values[GMS_VAL_MARGINAL]);
            gmdSetLower(gmd, symIterPtr, values[GMS_VAL_LOWER]);
            gmdSetUpper(gmd, symIterPtr, values[GMS_VAL_UPPER]);
            gmdSetScale(gmd, symIterPtr, values[GMS_VAL_SCALE]);
         }
         else if( (symType == GMS_DT_SET || symType == GMS_DT_ALIAS) && nrValCols == 1 ) // only set explanatory text if we have an extra column in the array
         {
            NP_GET_STRING(arrValues, i, 0, setText);
            gmdSetElemText(gmd, symIterPtr, setText);
         }
         gmdFreeSymbolIterator(gmd, symIterPtr);
      }
   }
   Py_RETURN_NONE;
}

static PyObject* getReady(
   PyObject* self,
   PyObject* args
)
{
   char msg[GMS_SSSIZE];
   char* sysDir;

   if( !PyArg_ParseTuple(args, "s", &sysDir) )
   {
      ERROR("Error while parsing arguments");
   }
   if( !gmdGetReadyD(sysDir, msg, sizeof(msg)) )
   {
      ERROR(msg);
   }
   if( !gdxGetReadyD(sysDir, msg, sizeof(msg)) )
   {
      ERROR(msg)
   }
   Py_RETURN_NONE;
}

static PyMethodDef methods[] = {
   { "gdxGetUelList",  gdxGetUelList,  METH_VARARGS, "Retrieve the UEL list" },
   { "gdxReadSymbol",  gdxReadSymbol,  METH_VARARGS, "Read a symbol from a GDX file." },
   { "gdxWriteSymbol", gdxWriteSymbol, METH_VARARGS, "Write a GDX symbol." },
   { "gdxRegisterUels", gdxRegisterUels, METH_VARARGS, "Register a list of UELs with a gdxHandle." },
   { "gdxGetSymbolExplTxt", gdxGetSymbolExplTxt, METH_VARARGS, "Get the decoded explanatory text from a symbol." },
   { "gmdGetUelList",  gmdGetUelList,  METH_VARARGS, "Retrieve the UEL list" },
   { "gmdReadSymbol",  gmdReadSymbol,  METH_VARARGS, "Read a symbol from GMD." },
   { "gmdFillSymbol",  gmdFillSymbol,  METH_VARARGS, "Fill an empty GMD symbol with a numpy array." },
   { "gmdRegisterUels", gmdRegisterUels,  METH_VARARGS, "Register a list of UELs with a gmdHandle." },
   { "gmdGetSymbolExplTxt", gmdGetSymbolExplTxt, METH_VARARGS, "Get the decoded explanatory text from a symbol." },
   { "getReady",  getReady,  METH_VARARGS, "Handles loading of GDX and GMD libraries. Always needs to be called first." },
   { NULL, NULL, 0, NULL }
};

// Our Module Definition struct
static struct PyModuleDef myModule = {
   PyModuleDef_HEAD_INIT,
   "_gams2numpy",
   "GAMS numpy API",
   -1,
   methods
};

// Initializes omodule
PyMODINIT_FUNC PyInit__gams2numpy(void)
{
   import_array();
   return PyModule_Create(&myModule);
}
