#ifndef SORTED_DICT_TYPE_HH_
#define SORTED_DICT_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>

/**
 * C++-style comparison implementation for Python objects.
 */
struct SortedDictKeyCompare
{
    bool operator()(PyObject* a, PyObject* b) const
    {
        // There must exist a total order on the set of possible keys. (Else,
        // this comparison may error out.) Hence, only instances of the type
        // of the first key inserted may be used as keys. (Instances of types
        // derived from that type are not allowed, because comparisons between
        // them can be customised to error out. Check the code to see how this
        // is enforced.) With these precautions, this comparison should always
        // work.
        return PyObject_RichCompareBool(a, b, Py_LT) == 1;
    }
};

struct SortedDictValue
{
public:
    PyObject* value;

    // Number of objects which require access to the key-value pair this value
    // is part of. They will all hold references to the containing sorted
    // dictionary.
    Py_ssize_t known_referrers;

public:
    SortedDictValue(PyObject* value) : value(value), known_referrers(0)
    {
    }
};

struct SortedDictType
{
public:
    PyObject_HEAD;

private:
    // Pointer to an object on the heap. Can't be the object itself, because
    // this container will be allocated a definite amount of space, which won't
    // allow the object to grow.
    std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>* map;

    // The type of each key.
    PyTypeObject* key_type;

    // Number of objects which require access to any key-value pair in this
    // sorted dictionary. They will all hold references to the latter.
    Py_ssize_t known_referrers;

private:
    bool is_key_good(PyObject*);
    bool are_key_type_and_key_value_pair_good(PyObject*, PyObject*);
    bool is_deletion_allowed(void);
    static bool is_deletion_allowed(Py_ssize_t);

public:
    void deinit(void);
    PyObject* repr(void);
    int contains(PyObject*);
    Py_ssize_t len(void);
    PyObject* getitem(PyObject*);
    int setitem(PyObject*, PyObject*);
    PyObject* clear(void);
    PyObject* copy(void);
    PyObject* items(void);
    PyObject* keys(PyTypeObject*);
    PyObject* values(void);
    PyObject* get_key_type(void);
    int init(PyObject*, PyObject*);
    static PyObject* New(PyTypeObject*, PyObject*, PyObject*);

    friend class SortedDictViewIterType;
    friend class SortedDictViewType;
};

#endif
