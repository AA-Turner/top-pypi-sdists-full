#include "../common.h"

#include "codeobject.h"

namespace devtools {
    namespace cdbg {
        namespace codeobject {
#if PY_VERSION_HEX < 0x030B0000
            PyObject * GetCoCode(PyCodeObject *code_object) {
                DEBUG("code_object->co_code = %p\n", code_object->co_code);
                return code_object->co_code;
            }

            void SetCoCode(PyCodeObject *code_object, ScopedPyObject &co_code) {
                code_object->co_code = co_code.get();
                Py_INCREF(code_object->co_code);
                DEBUG("code_object->co_code = %p\n", code_object->co_code);
            }
#endif
        }
    }
}