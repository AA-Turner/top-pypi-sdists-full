#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>
#include <utility>

#include "sorted_dict_type.hh"
#include "sorted_dict_utils.hh"
#include "sorted_dict_view_type.hh"

/**
 * Do all the necessary bookkeeping required to start tracking the given
 * iterator of the underlying sorted dictionary.
 *
 * The caller should ensure that this method is called immediately after the
 * iterator member is updated.
 *
 * @param it Current value of the iterator member.
 */
void SortedDictViewIterType::track(std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator it)
{
    if (it == this->sd->map->begin())
    {
        Py_INCREF(this->sd);
        ++this->sd->known_referrers;
        this->should_raise_stop_iteration = false;
    }
    if (it != this->sd->map->end())
    {
        ++it->second.known_referrers;
    }
    else
    {
        this->should_raise_stop_iteration = true;
        --this->sd->known_referrers;
        Py_DECREF(this->sd);
    }
}

/**
 * Do all the necessary bookkeeping required to stop tracking the given
 * iterator of the underlying sorted dictionary.
 *
 * The caller should ensure that this method is called immediately after the
 * iterator member is updated.
 *
 * @param it Previous value of the iterator member.
 */
void SortedDictViewIterType::untrack(std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator it)
{
    --it->second.known_referrers;
}

void SortedDictViewIterType::deinit(void)
{
    if (!this->should_raise_stop_iteration)
    {
        this->untrack(this->it);
        --this->sd->known_referrers;
        Py_DECREF(this->sd);
    }
}

std::pair<PyObject*, PyObject*> SortedDictViewIterType::next(void)
{
    static std::pair<PyObject* const, PyObject*> sentinel = { nullptr, nullptr };
    if (this->should_raise_stop_iteration)
    {
        return sentinel;
    }

    // The 'next' key-value pair is the current one the iterator points to.
    auto curr = this->it++;
    this->untrack(curr);
    this->track(this->it);
    return { curr->first, curr->second.value };
}

PyObject* SortedDictViewIterType::New(PyTypeObject* type, SortedDictType* sd)
{
    PyObject* self = type->tp_alloc(type, 0);  // 🆕
    if (self == nullptr)
    {
        return nullptr;
    }

    SortedDictViewIterType* sdvi = reinterpret_cast<SortedDictViewIterType*>(self);
    sdvi->sd = sd;
    sdvi->it = sdvi->sd->map->begin();
    sdvi->track(sdvi->it);
    return self;
}

void SortedDictViewType::deinit(void)
{
    Py_DECREF(this->sd);
}

PyObject* SortedDictViewType::repr(char const* name, PyObject* ob)
{
    PyObjectWrapper ob_list(PySequence_List(ob));  // 🆕
    if (ob_list == nullptr)
    {
        return nullptr;
    }
    return PyUnicode_FromFormat("%s(%R)", name, ob_list.get());
}

Py_ssize_t SortedDictViewType::len(void)
{
    return this->sd->map->size();
}

PyObject* SortedDictViewType::iter(PyTypeObject* type)
{
    return SortedDictViewIterType::New(type, this->sd);
}

PyObject* SortedDictViewType::New(PyTypeObject* type, SortedDictType* sd)
{
    PyObject* self = type->tp_alloc(type, 0);  // 🆕
    if (self == nullptr)
    {
        return nullptr;
    }

    SortedDictViewType* sdv = reinterpret_cast<SortedDictViewType*>(self);
    sdv->sd = sd;
    Py_INCREF(sdv->sd);
    return self;
}
