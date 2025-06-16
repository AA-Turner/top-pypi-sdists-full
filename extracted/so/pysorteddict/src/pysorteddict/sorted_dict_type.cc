#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <cmath>
#include <map>
#include <string>

#include "sorted_dict_keys_type.hh"
#include "sorted_dict_type.hh"
#include "sorted_dict_utils.hh"

/**
 * Import a Python type.
 *
 * The caller should ensure that the module and type names actually name a
 * Python type.
 *
 * @param module_name Name of the module to import the type from.
 * @param type_name Name of the type to import.
 *
 * @return Python type object if successful, else `nullptr`.
 */
static PyTypeObject* import_python_type(char const* module_name, char const* type_name)
{
    PyObjectWrapper module_ob(PyImport_ImportModule(module_name));  // 🆕
    if (module_ob == nullptr)
    {
        return nullptr;
    }
    PyObject* type_ob = PyObject_GetAttrString(module_ob.get(), type_name);  // 🆕
    if (type_ob == nullptr)
    {
        return nullptr;
    }
    if (Py_IS_TYPE(type_ob, &PyType_Type) == 0)
    {
        return nullptr;
    }
    return reinterpret_cast<PyTypeObject*>(type_ob);
}

// Key types which have to be imported explicitly using the above function.
static PyTypeObject* PyDecimal_Type;

/**
 * Import all supported key types from Python which are not built-in. Make them
 * available globally so that their reference counts need not be managed.
 *
 * @return `true` if successful, else `false`.
 */
static bool import_supported_key_types(void)
{
    // Import each type only once.
    static bool import_decimal = []
    {
        return (PyDecimal_Type = import_python_type("decimal", "Decimal")) != nullptr;
    }();
    if (!import_decimal)
    {
        PyErr_Clear();
        PyErr_SetString(PyExc_ImportError, "failed to import the `decimal.Decimal` type");
        return false;
    }
    return true;
}

/**
 * Check whether the given key can be inserted into this sorted dictionary. For
 * instance, NaN cannot be compared with other floating-point numbers, so it
 * cannot be inserted.
 *
 * The caller should ensure that the key type is set and that it matches the
 * type of the given key prior to calling this method.
 *
 * @param key Key.
 *
 * @return `true` if the check succeeds, else `false`.
 */
bool SortedDictType::is_key_good(PyObject* key)
{
    if (this->key_type == &PyFloat_Type)
    {
        return !std::isnan(PyFloat_AS_DOUBLE(key));
    }
    if (this->key_type == PyDecimal_Type)
    {
        PyObjectWrapper key_is_nan_callable(PyObject_GetAttrString(key, "is_nan"));  // 🆕
        if (key_is_nan_callable == nullptr)
        {
            return false;
        }
        PyObjectWrapper key_is_nan_result(PyObject_CallNoArgs(key_is_nan_callable.get()));  // 🆕
        if (key_is_nan_result == nullptr)
        {
            return false;
        }
        return PyObject_Not(key_is_nan_result.get()) == 1;
    }
    return true;
}

/**
 * Check whether the key type of this sorted dictionary is set and whether the
 * given key-value pair can be inserted into this sorted dictionary. If the
 * value is not supplied, check whether it is valid to get or delete the key.
 * On failure, set a Python exception.
 *
 * @param key Key.
 * @param value Value.
 *
 * @return `true` if the check succeeds, else `false`.
 */
bool SortedDictType::are_key_type_and_key_value_pair_good(PyObject* key, PyObject* value = nullptr)
{
    bool key_type_set_here = false;
    if (this->key_type == nullptr)
    {
        if (value == nullptr)
        {
            // No key-value pairs have been inserted, so can't get or delete
            // anything.
            PyErr_SetString(PyExc_RuntimeError, "key type not set: insert at least one item first");
            return false;
        }

        // The first key-value pair is being inserted.
        static PyTypeObject* allowed_key_types[] = {
            &PyBytes_Type,
            &PyFloat_Type,
            &PyLong_Type,
            &PyUnicode_Type,
            // The following types are not built-in.
            PyDecimal_Type,
        };
        for (PyTypeObject* allowed_key_type : allowed_key_types)
        {
            if (Py_IS_TYPE(key, allowed_key_type) != 0)
            {
                this->key_type = allowed_key_type;
                key_type_set_here = true;
                break;
            }
        }
        if (this->key_type == nullptr)
        {
            PyErr_Format(PyExc_TypeError, "got key %R of unsupported type %R", key, Py_TYPE(key));
            return false;
        }
    }

    // At this point, the key type is guaranteed to be non-null.
    if (!key_type_set_here && Py_IS_TYPE(key, this->key_type) == 0)
    {
        PyErr_Format(PyExc_TypeError, "got key %R of type %R, want key of type %R", key, Py_TYPE(key), this->key_type);
        return false;
    }

    // At this point, the key is guaranteed to be of the correct type. Hence,
    // it is safe to call this method.
    if (!this->is_key_good(key))
    {
        PyErr_Clear();
        PyErr_Format(PyExc_ValueError, "got bad key %R of type %R", key, Py_TYPE(key));
        if (key_type_set_here)
        {
            // Insertion of the key-value pair was unsuccessful, so clear the
            // key type.
            this->key_type = nullptr;
        }
        return false;
    }
    return true;
}

/**
 * Check whether every key-value pair in this sorted dictionary can be deleted.
 *
 * @return `true` if the check succeeds, else `false`.
 */
bool SortedDictType::is_deletion_allowed(void)
{
    if (this->known_referrers != 0)
    {
        PyErr_Format(
            PyExc_RuntimeError, "operation not permitted: sorted dictionary locked by %zd iterator(s)",
            this->known_referrers
        );
        return false;
    }
    return true;
}

/**
 * Check whether a key-value pair in this sorted dictionary can be deleted.
 *
 * @param kv_known_referrers Known referrers of the key-value pair.
 *
 * @return `true` if the check succeeds, else `false`.
 */
bool SortedDictType::is_deletion_allowed(Py_ssize_t kv_known_referrers)
{
    if (kv_known_referrers != 0)
    {
        PyErr_Format(
            PyExc_RuntimeError, "operation not permitted: key-value pair locked by %zd iterator(s)", kv_known_referrers
        );
        return false;
    }
    return true;
}

void SortedDictType::deinit(void)
{
    for (auto& item : *this->map)
    {
        Py_DECREF(item.first);
        Py_DECREF(item.second.value);
    }
    delete this->map;
}

PyObject* SortedDictType::repr(void)
{
    char const* delimiter = "";
    char const* actual_delimiter = ", ";
    std::string this_repr_utf8 = "SortedDict" LEFT_PARENTHESIS LEFT_CURLY_BRACKET;
    for (auto& item : *this->map)
    {
        PyObjectWrapper key_repr(PyObject_Repr(item.first));  // 🆕
        if (key_repr == nullptr)
        {
            return nullptr;
        }
        PyObjectWrapper value_repr(PyObject_Repr(item.second.value));  // 🆕
        if (value_repr == nullptr)
        {
            return nullptr;
        }
        Py_ssize_t key_repr_size, value_repr_size;
        char const* key_repr_utf8 = PyUnicode_AsUTF8AndSize(key_repr.get(), &key_repr_size);
        char const* value_repr_utf8 = PyUnicode_AsUTF8AndSize(value_repr.get(), &value_repr_size);
        this_repr_utf8.append(delimiter)
            .append(key_repr_utf8, key_repr_size)
            .append(": ")
            .append(value_repr_utf8, value_repr_size);
        delimiter = actual_delimiter;
    }
    this_repr_utf8.append(RIGHT_CURLY_BRACKET RIGHT_PARENTHESIS);
    return PyUnicode_FromStringAndSize(this_repr_utf8.data(), this_repr_utf8.size());  // 🆕
}

/**
 * Check whether a key is present.
 *
 * @param ob Python object.
 *
 * @return -1 on error. 1 if it is present, else 0.
 */
int SortedDictType::contains(PyObject* key)
{
    if (!this->are_key_type_and_key_value_pair_good(key))
    {
        return -1;
    }
    return this->map->find(key) == this->map->end() ? 0 : 1;
}

Py_ssize_t SortedDictType::len(void)
{
    return this->map->size();
}

/**
 * Find the value mapped to a key. On failure, set a Python exception.
 *
 * @param key Key.
 *
 * @return Value if present, else `nullptr`.
 */
PyObject* SortedDictType::getitem(PyObject* key)
{
    if (!this->are_key_type_and_key_value_pair_good(key))
    {
        return nullptr;
    }
    auto it = this->map->find(key);
    if (it == this->map->end())
    {
        PyErr_SetObject(PyExc_KeyError, key);
        return nullptr;
    }
    return Py_NewRef(it->second.value);  // 🆕
}

/**
 * Map a value to a key or remove a key-value pair. On failure, set a Python
 * exception.
 *
 * @param key Key.
 * @param value Value.
 *
 * @return 0 if a key-value pair was inserted or removed, else -1.
 */
int SortedDictType::setitem(PyObject* key, PyObject* value)
{
    if (!this->are_key_type_and_key_value_pair_good(key, value))
    {
        return -1;
    }

    // Insertion will be faster if the approximate location is known. Hence,
    // look for the nearest match.
    auto it = this->map->lower_bound(key);
    bool found = it != this->map->end() && !this->map->key_comp()(key, it->first);

    if (value == nullptr)
    {
        // Remove the key-value pair.
        if (!found)
        {
            PyErr_SetObject(PyExc_KeyError, key);
            return -1;
        }
        if (!this->is_deletion_allowed(it->second.known_referrers))
        {
            return -1;
        }
        Py_DECREF(it->first);
        Py_DECREF(it->second.value);
        this->map->erase(it);
        return 0;
    }

    // Map the value to the key. This merely stores additional references to
    // the key (if applicable) and the value. If I ever plan to allow mutable
    // types as keys, I should store references to their copies instead. Like
    // the C++ standard library containers do.
    if (!found)
    {
        // Insert a new key-value pair. The hint is correct; the key will get
        // inserted just before it.
        it = this->map->emplace_hint(it, key, value);
        Py_INCREF(it->first);  // 🆕
    }
    else
    {
        // Replace the previously-mapped value.
        Py_DECREF(it->second.value);
        it->second.value = value;
    }
    Py_INCREF(it->second.value);  // 🆕
    return 0;
}

PyObject* SortedDictType::clear(void)
{
    if (!this->is_deletion_allowed())
    {
        return nullptr;
    }
    for (auto& item : *this->map)
    {
        Py_DECREF(item.first);
        Py_DECREF(item.second.value);
    }
    this->map->clear();
    Py_RETURN_NONE;
}

PyObject* SortedDictType::copy(void)
{
    PyTypeObject* type = Py_TYPE(this);
    PyObject* sd_copy = type->tp_alloc(type, 0);  // 🆕
    if (sd_copy == nullptr)
    {
        return nullptr;
    }
    SortedDictType* this_copy = reinterpret_cast<SortedDictType*>(sd_copy);
    this_copy->map = new std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>(*this->map);
    for (auto& item : *this_copy->map)
    {
        Py_INCREF(item.first);  // 🆕
        Py_INCREF(item.second.value);  // 🆕
        item.second.known_referrers = 0;
    }
    this_copy->key_type = this->key_type;
    this_copy->known_referrers = 0;
    return sd_copy;
}

PyObject* SortedDictType::items(void)
{
    PyObject* sd_items = PyList_New(this->map->size());  // 🆕
    if (sd_items == nullptr)
    {
        return nullptr;
    }
    Py_ssize_t idx = 0;
    for (auto& item : *this->map)
    {
        PyObject* sd_item = PyTuple_New(2);  // 🆕
        if (sd_item == nullptr)
        {
            Py_DECREF(sd_items);
            return nullptr;
        }
        PyTuple_SET_ITEM(sd_item, 0, Py_NewRef(item.first));  // 🆕
        PyTuple_SET_ITEM(sd_item, 1, Py_NewRef(item.second.value));  // 🆕
        PyList_SET_ITEM(sd_items, idx++, sd_item);
    }
    return sd_items;
}

PyObject* SortedDictType::keys(PyTypeObject* type)
{
    return SortedDictKeysType::New(type, this);
}

PyObject* SortedDictType::values(void)
{
    PyObject* sd_values = PyList_New(this->map->size());  // 🆕
    if (sd_values == nullptr)
    {
        return nullptr;
    }
    Py_ssize_t idx = 0;
    for (auto& item : *this->map)
    {
        PyList_SET_ITEM(sd_values, idx++, Py_NewRef(item.second.value));  // 🆕
    }
    return sd_values;
}

PyObject* SortedDictType::get_key_type(void)
{
    if (this->key_type == nullptr)
    {
        Py_RETURN_NONE;
    }
    return Py_NewRef(this->key_type);  // 🆕
}

int SortedDictType::init(PyObject* args, PyObject* kwargs)
{
    // All initialisation is done immediately after allocation in order to
    // avoid leaving essential members uninitialised. This method is kept to
    // allow adding functionality in the future.
    return 0;
}

PyObject* SortedDictType::New(PyTypeObject* type, PyObject* args, PyObject* kwargs)
{
    if (!import_supported_key_types())
    {
        return nullptr;
    }

    PyObject* self = type->tp_alloc(type, 0);  // 🆕
    if (self == nullptr)
    {
        return nullptr;
    }

    // Python's default allocator claims to initialise the contents of the
    // allocated memory to null, but actually writes zeros to it. Hence,
    // explicitly initialise them.
    SortedDictType* sd = reinterpret_cast<SortedDictType*>(self);
    sd->map = new std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>;
    sd->key_type = nullptr;
    sd->known_referrers = 0;
    return self;
}
