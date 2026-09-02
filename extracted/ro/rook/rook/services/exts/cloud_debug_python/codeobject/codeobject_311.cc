#include "../common.h"

#include "codeobject.h"

namespace devtools {
    namespace cdbg {
        namespace codeobject {
#if PY_VERSION_HEX >= 0x030B0000
            PyObject * GetCoCode(PyCodeObject *code_object) {
                return PyCode_GetCode(code_object);
            }

            void SetCoCode(PyCodeObject *code_object, ScopedPyObject &co_code) {
                // This is a NO-OP in the case of python 3.11+, since we are not actually updating co_code,
                // but creating a new code object and passing it the updated co_code instead
            }
#endif
        }
    }
}