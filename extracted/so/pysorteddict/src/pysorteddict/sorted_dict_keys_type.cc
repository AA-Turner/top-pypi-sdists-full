#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <algorithm>

#include "sorted_dict_keys_type.hh"
#include "sorted_dict_view_type.hh"

PyObject* SortedDictKeysIterType::next(void)
{
    return Py_XNewRef(this->SortedDictViewIterType::next().first);  // 🆕
}

PyObject* SortedDictKeysType::getitem(Py_ssize_t position)
{
    Py_ssize_t sz = this->sd->len();
    if (sz == -1)
    {
        return nullptr;
    }
    Py_ssize_t positive_position = position >= 0 ? position : position + sz;
    if (positive_position < 0 || sz <= positive_position)
    {
        PyErr_Format(PyExc_IndexError, "got invalid index %zd for view of length %zd", position, sz);
        return nullptr;
    }
    std::map<PyObject*, SortedDictValue>::iterator it;
    if (positive_position <= sz / 2)
    {
        it = this->sd->map->begin();
        std::advance(it, positive_position);
    }
    else
    {
        it = this->sd->map->end();
        std::advance(it, positive_position - sz);
    }
    return Py_NewRef(it->first);  // 🆕
}

PyObject* SortedDictKeysType::getitem(Py_ssize_t start, Py_ssize_t stop, Py_ssize_t step)
{
    Py_ssize_t sz = this->sd->len();
    if (sz == -1)
    {
        return nullptr;
    }
    Py_ssize_t slice_len = PySlice_AdjustIndices(sz, &start, &stop, step);
    PyObject* keys = PyList_New(slice_len);  // 🆕
    if (slice_len == 0)
    {
        return keys;
    }

    std::map<PyObject*, SortedDictValue>::iterator it;
    if ((step > 0 && start <= sz - stop) || (step < 0 && sz - 1 - start < stop + 1))
    {
        if (step > 0)
        {
            it = this->sd->map->begin();
            std::advance(it, start);
        }
        else
        {
            it = this->sd->map->end();
            std::advance(it, start - sz);
        }
        for (Py_ssize_t i = 0;; ++i)
        {
            PyList_SET_ITEM(keys, i, Py_NewRef(it->first));
            if (i == slice_len - 1)
            {
                break;
            }
            std::advance(it, step);
        }
    }
    else
    {
        start += (slice_len - 1) * step;
        if (step > 0)
        {
            it = this->sd->map->end();
            std::advance(it, start - sz);
        }
        else
        {
            it = this->sd->map->begin();
            std::advance(it, start);
        }
        for (Py_ssize_t i = slice_len - 1;; --i)
        {
            PyList_SET_ITEM(keys, i, Py_NewRef(it->first));
            if (i == 0)
            {
                break;
            }
            std::advance(it, -step);
        }
    }
    return keys;
}

int SortedDictKeysType::contains(PyObject* key)
{
    return this->sd->contains(key);
}

PyObject* SortedDictKeysType::getitem(PyObject* idx)
{
    if (PyIndex_Check(idx) != 0)
    {
        Py_ssize_t position = PyNumber_AsSsize_t(idx, PyExc_IndexError);
        if (position == -1 && PyErr_Occurred() != nullptr)
        {
            return nullptr;
        }
        return this->getitem(position);
    }

    if (PySlice_Check(idx))
    {
        Py_ssize_t start, stop, step;
        if (PySlice_Unpack(idx, &start, &stop, &step) != 0)
        {
            return nullptr;
        }
        return this->getitem(start, stop, step);
    }

    PyErr_Format(
        PyExc_TypeError, "got index %R of type %R, want index of type %R or %R", idx, Py_TYPE(idx), &PyLong_Type,
        &PySlice_Type
    );
    return nullptr;
}
