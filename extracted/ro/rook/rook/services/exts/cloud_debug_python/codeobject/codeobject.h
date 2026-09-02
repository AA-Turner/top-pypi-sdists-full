#ifndef CLOUD_DEBUG_PYTHON_CODEOBJECT_H
#define CLOUD_DEBUG_PYTHON_CODEOBJECT_H

#include "../common.h"
#include "../python_util.h"

namespace devtools {
    namespace cdbg {
        namespace codeobject {
            PyObject * GetCoCode(PyCodeObject *code_object);
            void SetCoCode(PyCodeObject *code_object, ScopedPyObject &co_code);
        }
    }
}

#endif //CLOUD_DEBUG_PYTHON_CODEOBJECT_H
