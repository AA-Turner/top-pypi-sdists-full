#include "types.h"
#include "methods.h"
#include "doc.h"


PyMethodDef atomic_dict_capi_methods[] = {
    {"get_pointer", (PyCFunction) get_pointer, METH_FASTCALL, get_pointer_doc},
    {NULL}  /* Sentinel */
};

struct PyModuleDef atomic_dict_capi_module = {
    PyModuleDef_HEAD_INIT,
    .m_name = "capi",
    .m_doc = atomic_dict_doc,
    .m_size = -1,
    .m_methods = atomic_dict_capi_methods,
};

PyMethodDef atomic_array_methods[] = {
    {"index",    (PyCFunction) atomic_array_index,    METH_FASTCALL, atomic_array_index_doc},
    {"iterator", (PyCFunction) atomic_array_iterator, METH_FASTCALL, atomic_array_iterator_doc},
    {NULL}  /* Sentinel */
};

PyTypeObject AtomicArrayType = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "atomic_dict.capi.AtomicArray",
    .tp_doc = atomic_array_doc,
    .tp_basicsize = sizeof(AtomicArray),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_init = (initproc) atomic_array_init,
    .tp_methods = atomic_array_methods,
};

PyMethodDef atomic_value_64_methods[] = {
    {"load",  (PyCFunction) atomic_value_64_load,  METH_FASTCALL, atomic_value_load_doc},
    {"store", (PyCFunction) atomic_value_64_store, METH_FASTCALL, atomic_value_store_doc},
    {"swap",  (PyCFunction) atomic_value_64_swap,  METH_FASTCALL, atomic_value_swap_doc},
    {"add",   (PyCFunction) atomic_value_64_add,   METH_FASTCALL, atomic_value_add_doc},
    {"sub",   (PyCFunction) atomic_value_64_sub,   METH_FASTCALL, atomic_value_sub_doc},
    {"band",  (PyCFunction) atomic_value_64_band,  METH_FASTCALL, atomic_value_band_doc},
    {"bor",   (PyCFunction) atomic_value_64_bor,   METH_FASTCALL, atomic_value_bor_doc},
    {"bxor",  (PyCFunction) atomic_value_64_bxor,  METH_FASTCALL, atomic_value_bxor_doc},
    {"cas",   (PyCFunction) atomic_value_64_cas,   METH_FASTCALL, atomic_value_cas_doc},
    {NULL}  /* Sentinel */
};

PyTypeObject AtomicValue64Type = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "atomic_dict.capi.AtomicValue64",
    .tp_basicsize = sizeof(AtomicValue64),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_methods = atomic_value_64_methods,
};

PyMethodDef atomic_value_32_methods[] = {
    {"load",  (PyCFunction) atomic_value_32_load,  METH_FASTCALL, atomic_value_load_doc},
    {"store", (PyCFunction) atomic_value_32_store, METH_FASTCALL, atomic_value_store_doc},
    {"swap",  (PyCFunction) atomic_value_32_swap,  METH_FASTCALL, atomic_value_swap_doc},
    {"add",   (PyCFunction) atomic_value_32_add,   METH_FASTCALL, atomic_value_add_doc},
    {"sub",   (PyCFunction) atomic_value_32_sub,   METH_FASTCALL, atomic_value_sub_doc},
    {"band",  (PyCFunction) atomic_value_32_band,  METH_FASTCALL, atomic_value_band_doc},
    {"bor",   (PyCFunction) atomic_value_32_bor,   METH_FASTCALL, atomic_value_bor_doc},
    {"bxor",  (PyCFunction) atomic_value_32_bxor,  METH_FASTCALL, atomic_value_bxor_doc},
    {"cas",   (PyCFunction) atomic_value_32_cas,   METH_FASTCALL, atomic_value_cas_doc},
    {NULL}  /* Sentinel */
};

PyTypeObject AtomicValue32Type = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "atomic_dict.capi.AtomicValue32",
    .tp_basicsize = sizeof(AtomicValue32),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_methods = atomic_value_32_methods,
};

PyMethodDef dict_iterator_methods[] = {
    {"key",   (PyCFunction) dict_iterator_key,   METH_FASTCALL, dict_iterator_key_doc},
    {"value", (PyCFunction) dict_iterator_value, METH_FASTCALL, dict_iterator_value_doc},
    {"next",  (PyCFunction) dict_iterator_next,  METH_FASTCALL, dict_iterator_next_doc},
    {NULL}  /* Sentinel */
};

PyTypeObject DictIteratorType = {
    .ob_base = PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "atomic_dict.capi.DictIterator",
    .tp_basicsize = sizeof(DictIterator),
    .tp_itemsize = 0,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,
    .tp_new = PyType_GenericNew,
    .tp_methods = dict_iterator_methods,
};

PyMODINIT_FUNC PyInit_capi(void) {
    PyObject *m;

    if (PyType_Ready(&AtomicArrayType) < 0 || PyType_Ready(&AtomicValue64Type) < 0 ||
        PyType_Ready(&AtomicValue32Type) < 0 || PyType_Ready(&DictIteratorType) < 0) {
        return NULL;
    }

    m = PyModule_Create(&atomic_dict_capi_module);
    if (m == NULL) {
        return NULL;
    }

    if (PyModule_AddObjectRef(m, "AtomicArray", (PyObject *) &AtomicArrayType) < 0) {
        Py_DECREF(m);
        return NULL;
    }

    if (PyModule_AddObjectRef(m, "AtomicValue64", (PyObject *) &AtomicValue64Type) < 0) {
        Py_DECREF(m);
        return NULL;
    }

    if (PyModule_AddObjectRef(m, "AtomicValue32", (PyObject *) &AtomicValue32Type) < 0) {
        Py_DECREF(m);
        return NULL;
    }

    if (PyModule_AddObjectRef(m, "DictIterator", (PyObject *) &DictIteratorType) < 0) {
        Py_DECREF(m);
        return NULL;
    }

    return m;
}
