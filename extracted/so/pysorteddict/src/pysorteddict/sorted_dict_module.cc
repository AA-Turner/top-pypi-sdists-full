#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sorted_dict_items_type.hh"
#include "sorted_dict_keys_type.hh"
#include "sorted_dict_type.hh"
#include "sorted_dict_values_type.hh"

/**
 * Deinitialise and deallocate.
 */
static void sorted_dict_items_iter_type_dealloc(PyObject* self)
{
    SortedDictItemsIterType::Delete(self);
}

/**
 * Retrieve the next element.
 */
static PyObject* sorted_dict_items_iter_type_next(PyObject* self)
{
    SortedDictItemsIterType* sdii = reinterpret_cast<SortedDictItemsIterType*>(self);
    return sdii->next();
}

static PyTypeObject sorted_dict_items_iter_type = {
    // clang-format off
    .ob_base = PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "pysorteddict.SortedDictItemsIter",
    // clang-format on
    .tp_basicsize = sizeof(SortedDictItemsIterType),
    .tp_dealloc = sorted_dict_items_iter_type_dealloc,
    .tp_getattro = PyObject_GenericGetAttr,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Iterator over the items in a sorted dictionary.",
    .tp_iter = PyObject_SelfIter,
    .tp_iternext = sorted_dict_items_iter_type_next,
    .tp_alloc = PyType_GenericAlloc,
    .tp_free = PyObject_Free,
};

/**
 * Deinitialise and deallocate.
 */
static void sorted_dict_items_type_dealloc(PyObject* self)
{
    SortedDictItemsType::Delete(self);
}

/**
 * Stringify.
 */
static PyObject* sorted_dict_items_type_repr(PyObject* self)
{
    return SortedDictItemsType::repr(self);
}

/**
 * Obtain the number of items.
 */
static Py_ssize_t sorted_dict_items_type_len(PyObject* self)
{
    SortedDictItemsType* sdi = reinterpret_cast<SortedDictItemsType*>(self);
    return sdi->len();
}

/**
 * Check whether a item is present.
 */
static int sorted_dict_items_type_contains(PyObject* self, PyObject* item)
{
    SortedDictItemsType* sdi = reinterpret_cast<SortedDictItemsType*>(self);
    return sdi->contains(item);
}

static PySequenceMethods sorted_dict_items_type_sequence = {
    .sq_length = sorted_dict_items_type_len,
    .sq_contains = sorted_dict_items_type_contains,
};

/**
 * Retrieve the item at a position or items in a slice.
 */
static PyObject* sorted_dict_items_type_getitem(PyObject* self, PyObject* idx)
{
    SortedDictItemsType* sdi = reinterpret_cast<SortedDictItemsType*>(self);
    return sdi->getitem(idx);
}

static PyMappingMethods sorted_dict_items_type_mapping = {
    .mp_subscript = sorted_dict_items_type_getitem,
};

/**
 * Create an iterator.
 */
static PyObject* sorted_dict_items_type_iter(PyObject* self)
{
    SortedDictItemsType* sdi = reinterpret_cast<SortedDictItemsType*>(self);
    return sdi->iter(&sorted_dict_items_iter_type);
}

static PyTypeObject sorted_dict_items_type = {
    // clang-format off
    .ob_base = PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "pysorteddict.SortedDictItems",
    // clang-format on
    .tp_basicsize = sizeof(SortedDictItemsType),
    .tp_dealloc = sorted_dict_items_type_dealloc,
    .tp_repr = sorted_dict_items_type_repr,
    .tp_as_sequence = &sorted_dict_items_type_sequence,
    .tp_as_mapping = &sorted_dict_items_type_mapping,
    .tp_hash = PyObject_HashNotImplemented,
    .tp_getattro = PyObject_GenericGetAttr,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Dynamic view on the items in a sorted dictionary.",
    .tp_iter = sorted_dict_items_type_iter,
    .tp_alloc = PyType_GenericAlloc,
    .tp_free = PyObject_Free,
};

/**
 * Deinitialise and deallocate.
 */
static void sorted_dict_keys_iter_type_dealloc(PyObject* self)
{
    SortedDictKeysIterType::Delete(self);
}

/**
 * Retrieve the next element.
 */
static PyObject* sorted_dict_keys_iter_type_next(PyObject* self)
{
    SortedDictKeysIterType* sdki = reinterpret_cast<SortedDictKeysIterType*>(self);
    return sdki->next();
}

static PyTypeObject sorted_dict_keys_iter_type = {
    // clang-format off
    .ob_base = PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "pysorteddict.SortedDictKeysIter",
    // clang-format on
    .tp_basicsize = sizeof(SortedDictKeysIterType),
    .tp_dealloc = sorted_dict_keys_iter_type_dealloc,
    .tp_getattro = PyObject_GenericGetAttr,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Iterator over the keys in a sorted dictionary.",
    .tp_iter = PyObject_SelfIter,
    .tp_iternext = sorted_dict_keys_iter_type_next,
    .tp_alloc = PyType_GenericAlloc,
    .tp_free = PyObject_Free,
};

/**
 * Deinitialise and deallocate.
 */
static void sorted_dict_keys_type_dealloc(PyObject* self)
{
    SortedDictKeysType::Delete(self);
}

/**
 * Stringify.
 */
static PyObject* sorted_dict_keys_type_repr(PyObject* self)
{
    return SortedDictKeysType::repr(self);
}

/**
 * Obtain the number of keys.
 */
static Py_ssize_t sorted_dict_keys_type_len(PyObject* self)
{
    SortedDictKeysType* sdk = reinterpret_cast<SortedDictKeysType*>(self);
    return sdk->len();
}

/**
 * Check whether a key is present.
 */
static int sorted_dict_keys_type_contains(PyObject* self, PyObject* key)
{
    SortedDictKeysType* sdk = reinterpret_cast<SortedDictKeysType*>(self);
    return sdk->contains(key);
}

static PySequenceMethods sorted_dict_keys_type_sequence = {
    .sq_length = sorted_dict_keys_type_len,
    .sq_contains = sorted_dict_keys_type_contains,
};

/**
 * Retrieve the key at a position or keys in a slice.
 */
static PyObject* sorted_dict_keys_type_getitem(PyObject* self, PyObject* idx)
{
    SortedDictKeysType* sdk = reinterpret_cast<SortedDictKeysType*>(self);
    return sdk->getitem(idx);
}

static PyMappingMethods sorted_dict_keys_type_mapping = {
    .mp_subscript = sorted_dict_keys_type_getitem,
};

/**
 * Create an iterator.
 */
static PyObject* sorted_dict_keys_type_iter(PyObject* self)
{
    SortedDictKeysType* sdk = reinterpret_cast<SortedDictKeysType*>(self);
    return sdk->iter(&sorted_dict_keys_iter_type);
}

static PyTypeObject sorted_dict_keys_type = {
    // clang-format off
    .ob_base = PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "pysorteddict.SortedDictKeys",
    // clang-format on
    .tp_basicsize = sizeof(SortedDictKeysType),
    .tp_dealloc = sorted_dict_keys_type_dealloc,
    .tp_repr = sorted_dict_keys_type_repr,
    .tp_as_sequence = &sorted_dict_keys_type_sequence,
    .tp_as_mapping = &sorted_dict_keys_type_mapping,
    .tp_hash = PyObject_HashNotImplemented,
    .tp_getattro = PyObject_GenericGetAttr,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Dynamic view on the keys in a sorted dictionary.",
    .tp_iter = sorted_dict_keys_type_iter,
    .tp_alloc = PyType_GenericAlloc,
    .tp_free = PyObject_Free,
};

/**
 * Deinitialise and deallocate.
 */
static void sorted_dict_values_iter_type_dealloc(PyObject* self)
{
    SortedDictValuesIterType::Delete(self);
}

/**
 * Retrieve the next element.
 */
static PyObject* sorted_dict_values_iter_type_next(PyObject* self)
{
    SortedDictValuesIterType* sdvi = reinterpret_cast<SortedDictValuesIterType*>(self);
    return sdvi->next();
}

static PyTypeObject sorted_dict_values_iter_type = {
    // clang-format off
    .ob_base = PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "pysorteddict.SortedDictValuesIter",
    // clang-format on
    .tp_basicsize = sizeof(SortedDictValuesIterType),
    .tp_dealloc = sorted_dict_values_iter_type_dealloc,
    .tp_getattro = PyObject_GenericGetAttr,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Iterator over the values in a sorted dictionary.",
    .tp_iter = PyObject_SelfIter,
    .tp_iternext = sorted_dict_values_iter_type_next,
    .tp_alloc = PyType_GenericAlloc,
    .tp_free = PyObject_Free,
};

/**
 * Deinitialise and deallocate.
 */
static void sorted_dict_values_type_dealloc(PyObject* self)
{
    SortedDictValuesType::Delete(self);
}

/**
 * Stringify.
 */
static PyObject* sorted_dict_values_type_repr(PyObject* self)
{
    return SortedDictValuesType::repr(self);
}

/**
 * Obtain the number of values.
 */
static Py_ssize_t sorted_dict_values_type_len(PyObject* self)
{
    SortedDictValuesType* sdv = reinterpret_cast<SortedDictValuesType*>(self);
    return sdv->len();
}

static PySequenceMethods sorted_dict_values_type_sequence = {
    .sq_length = sorted_dict_values_type_len,
};

/**
 * Retrieve the value at a position or values in a slice.
 */
static PyObject* sorted_dict_values_type_getitem(PyObject* self, PyObject* idx)
{
    SortedDictValuesType* sdv = reinterpret_cast<SortedDictValuesType*>(self);
    return sdv->getitem(idx);
}

static PyMappingMethods sorted_dict_values_type_mapping = {
    .mp_subscript = sorted_dict_values_type_getitem,
};

/**
 * Create an iterator.
 */
static PyObject* sorted_dict_values_type_iter(PyObject* self)
{
    SortedDictValuesType* sdv = reinterpret_cast<SortedDictValuesType*>(self);
    return sdv->iter(&sorted_dict_values_iter_type);
}

static PyTypeObject sorted_dict_values_type = {
    // clang-format off
    .ob_base = PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "pysorteddict.SortedDictValues",
    // clang-format on
    .tp_basicsize = sizeof(SortedDictValuesType),
    .tp_dealloc = sorted_dict_values_type_dealloc,
    .tp_repr = sorted_dict_values_type_repr,
    .tp_as_sequence = &sorted_dict_values_type_sequence,
    .tp_as_mapping = &sorted_dict_values_type_mapping,
    .tp_getattro = PyObject_GenericGetAttr,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Dynamic view on the values in a sorted dictionary.",
    .tp_iter = sorted_dict_values_type_iter,
    .tp_alloc = PyType_GenericAlloc,
    .tp_free = PyObject_Free,
};

/**
 * Deinitialise and deallocate.
 */
static void sorted_dict_type_dealloc(PyObject* self)
{
    // I could have separated deinitialisation and deallocation the way I
    // separated allocation and initialisation using the Python type methods,
    // but it looks like the deinitialisation (finalisation) function is not
    // automatically called prior to deallocation. Further, the documentation
    // recommends doing both here.
    SortedDictType::Delete(self);
}

/**
 * Stringify.
 */
static PyObject* sorted_dict_type_repr(PyObject* self)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->repr();
}

/**
 * Check whether a key is present.
 */
static int sorted_dict_type_contains(PyObject* self, PyObject* key)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->contains(key);
}

static PySequenceMethods sorted_dict_type_sequence = {
    .sq_contains = sorted_dict_type_contains,
};

/**
 * Obtain the number of key-value pairs.
 */
static Py_ssize_t sorted_dict_type_len(PyObject* self)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->len();
}

/**
 * Find the value mapped to a key.
 */
static PyObject* sorted_dict_type_getitem(PyObject* self, PyObject* key)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->getitem(key);
}

/**
 * Map a value to a key or remove a key-value pair.
 */
static int sorted_dict_type_setitem(PyObject* self, PyObject* key, PyObject* value)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->setitem(key, value);
}

static PyMappingMethods sorted_dict_type_mapping = {
    .mp_length = sorted_dict_type_len,
    .mp_subscript = sorted_dict_type_getitem,
    .mp_ass_subscript = sorted_dict_type_setitem,
};

static PyObject* sorted_dict_type_iter(PyObject* self)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->iter(&sorted_dict_keys_iter_type);
}

PyDoc_STRVAR(
    sorted_dict_type_clear_doc,
    "d.clear()\n"
    "Remove all key-value pairs in the sorted dictionary ``d``."
);

static PyObject* sorted_dict_type_clear(PyObject* self, PyObject* args)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->clear();
}

PyDoc_STRVAR(
    sorted_dict_type_copy_doc,
    "d.copy() -> SortedDict\n"
    "Return a shallow copy of the sorted dictionary ``d``."
);

static PyObject* sorted_dict_type_copy(PyObject* self, PyObject* args)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->copy();
}

PyDoc_STRVAR(
    sorted_dict_type_get_doc,
    "d.get(key: Any, default: Any = None, /) -> Any\n"
    "Return the value mapped to ``key`` in the sorted dictionary ``d``, or ``default`` if ``key`` isn't in ``d``."
);

static PyObject* sorted_dict_type_get(PyObject* self, PyObject* args)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->get(args);
}

PyDoc_STRVAR(
    sorted_dict_type_items_doc,
    "d.items() -> SortedDictItems\n"
    "Return a dynamic view on the items in the sorted dictionary ``d``."
);

static PyObject* sorted_dict_type_items(PyObject* self, PyObject* args)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->items(&sorted_dict_items_type);
}

PyDoc_STRVAR(
    sorted_dict_type_keys_doc,
    "d.keys() -> SortedDictKeys\n"
    "Return a dynamic view on the keys in the sorted dictionary ``d``."
);

static PyObject* sorted_dict_type_keys(PyObject* self, PyObject* args)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->keys(&sorted_dict_keys_type);
}

PyDoc_STRVAR(
    sorted_dict_type_setdefault_doc,
    "d.setdefault(key: Any, default: Any = None, /) -> Any\n"
    "Return ``d.get(key, default)``, and map ``default`` to ``key`` if ``key`` isn't in the sorted dictionary ``d``."
);

static PyObject* sorted_dict_type_setdefault(PyObject* self, PyObject* args)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->setdefault(args);
}

PyDoc_STRVAR(
    sorted_dict_type_values_doc,
    "d.values() -> SortedDictValues\n"
    "Return a dynamic view on the values in the sorted dictionary ``d``."
);

static PyObject* sorted_dict_type_values(PyObject* self, PyObject* args)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->values(&sorted_dict_values_type);
}

static PyMethodDef sorted_dict_type_methods[] = {
    {
        .ml_name = "clear",
        .ml_meth = sorted_dict_type_clear,
        .ml_flags = METH_NOARGS,
        .ml_doc = sorted_dict_type_clear_doc,
    },
    {
        .ml_name = "copy",
        .ml_meth = sorted_dict_type_copy,
        .ml_flags = METH_NOARGS,
        .ml_doc = sorted_dict_type_copy_doc,
    },
    {
        .ml_name = "get",
        .ml_meth = sorted_dict_type_get,
        .ml_flags = METH_VARARGS,
        .ml_doc = sorted_dict_type_get_doc,
    },
    {
        .ml_name = "items",
        .ml_meth = sorted_dict_type_items,
        .ml_flags = METH_NOARGS,
        .ml_doc = sorted_dict_type_items_doc,
    },
    {
        .ml_name = "keys",
        .ml_meth = sorted_dict_type_keys,
        .ml_flags = METH_NOARGS,
        .ml_doc = sorted_dict_type_keys_doc,
    },
    {
        .ml_name = "setdefault",
        .ml_meth = sorted_dict_type_setdefault,
        .ml_flags = METH_VARARGS,
        .ml_doc = sorted_dict_type_setdefault_doc,
    },
    {
        .ml_name = "values",
        .ml_meth = sorted_dict_type_values,
        .ml_flags = METH_NOARGS,
        .ml_doc = sorted_dict_type_values_doc,
    },
    { nullptr },
};

PyDoc_STRVAR(
    sorted_dict_type_get_key_type_doc,
    "d.key_type: type | None\n"
    "The key type of the sorted dictionary ``d``, or ``None`` if no key-value pairs have been inserted in it."
);

static PyObject* sorted_dict_type_get_key_type(PyObject* self, void* closure)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->get_key_type();
}

static PyGetSetDef sorted_dict_type_getset[] = {
    {
        .name = "key_type",
        .get = sorted_dict_type_get_key_type,
        .doc = sorted_dict_type_get_key_type_doc,
    },
    { nullptr },
};

/**
 * Initialise.
 */
static int sorted_dict_type_init(PyObject* self, PyObject* args, PyObject* kwargs)
{
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    return sd->init(args, kwargs);
}

/**
 * Allocate.
 */
static PyObject* sorted_dict_type_new(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    // In C++, the operator with the same name is used to allocate memory. I
    // could override it to call Python's memory allocator, but the latter
    // requires the Python type object, while the former receives only the
    // requested amount of memory. Hence, I am forced to use a custom method.
    return SortedDictType::New(type, args, kwargs);
}

static PyTypeObject sorted_dict_type = {
    // clang-format off
    .ob_base = PyVarObject_HEAD_INIT(&PyType_Type, 0)
    .tp_name = "pysorteddict.SortedDict",
    // clang-format on
    .tp_basicsize = sizeof(SortedDictType),
    .tp_dealloc = sorted_dict_type_dealloc,
    .tp_repr = sorted_dict_type_repr,
    .tp_as_sequence = &sorted_dict_type_sequence,
    .tp_as_mapping = &sorted_dict_type_mapping,
    .tp_hash = PyObject_HashNotImplemented,
    .tp_getattro = PyObject_GenericGetAttr,
    .tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_DICT_SUBCLASS,
    .tp_doc = "Sorted dictionary: a dictionary in which the keys are always in ascending order.\n\n"
              "SortedDict(*args, **kwargs) -> SortedDict\n"
              "Create an empty sorted dictionary. ``args`` and ``kwargs`` are ignored.",
    .tp_iter = sorted_dict_type_iter,
    .tp_methods = sorted_dict_type_methods,
    .tp_getset = sorted_dict_type_getset,
    .tp_init = sorted_dict_type_init,
    .tp_alloc = PyType_GenericAlloc,
    .tp_new = sorted_dict_type_new,
    .tp_free = PyObject_Free,
};

static PyModuleDef sorted_dict_module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "pysorteddict",
    .m_doc = "enriches Python with a sorted dictionary\n\n"
             "See https://tfpf.github.io/pysorteddict/.",
    .m_size = -1,
};

PyMODINIT_FUNC PyInit_pysorteddict(void)
{
    if (PyType_Ready(&sorted_dict_items_iter_type) < 0 || PyType_Ready(&sorted_dict_items_type) < 0
        || PyType_Ready(&sorted_dict_keys_iter_type) < 0 || PyType_Ready(&sorted_dict_keys_type) < 0
        || PyType_Ready(&sorted_dict_values_iter_type) < 0 || PyType_Ready(&sorted_dict_values_type) < 0
        || PyType_Ready(&sorted_dict_type) < 0)
    {
        return nullptr;
    }
    PyObject* mod = PyModule_Create(&sorted_dict_module);  // 🆕
    if (mod == nullptr)
    {
        return nullptr;
    }
    if (PyModule_AddObjectRef(mod, "SortedDict", reinterpret_cast<PyObject*>(&sorted_dict_type)) < 0)  // 🆕
    {
        Py_DECREF(mod);
        return nullptr;
    }
    return mod;
}
