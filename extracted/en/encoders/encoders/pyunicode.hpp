#include <cstring>
#define PY_SSIZE_T_CLEAN
#include "Python.h"
#include "smartptr.h"

class PyUnicodeSmartPtr : public PyObjectSmartPtr {

public:
  PyUnicodeSmartPtr() : PyObjectSmartPtr() {}
  PyUnicodeSmartPtr(PyObject *ptr) : PyObjectSmartPtr(ptr) {}

  bool operator==(const PyUnicodeSmartPtr &other) const noexcept {
    return PyUnicode_KIND(get()) == PyUnicode_KIND(other.get()) &&
           PyUnicode_GET_LENGTH(get()) == PyUnicode_GET_LENGTH(other.get()) &&
           std::memcmp(PyUnicode_DATA(get()), PyUnicode_DATA(other.get()),
                       PyUnicode_GET_LENGTH(get())) == 0;
  }
};

template <> struct std::hash<PyUnicodeSmartPtr> {
  std::size_t operator()(const PyUnicodeSmartPtr &s) const noexcept {
    return static_cast<std::size_t>(PyObject_Hash(s.get())); // reinterpret_cast
  }
};
