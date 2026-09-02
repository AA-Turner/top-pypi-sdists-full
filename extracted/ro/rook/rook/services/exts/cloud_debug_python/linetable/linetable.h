//
// Created by Omer Koskas on 21/12/2022.
//

#ifndef CLOUD_DEBUG_PYTHON_LINETABLE_H
#define CLOUD_DEBUG_PYTHON_LINETABLE_H

#include "../common.h"
#include "../python_util.h"

namespace devtools
{
    namespace cdbg
    {
        namespace linetable
        {
            int GetLineOffset(int line, const ScopedPyObject *original_lnotab, PyCodeObject *code_object);
            void InsertAndUpdateLinetable(int offset, int size, std::vector<uint8> *lnotab, PyCodeObject *code_object);
            PyObject * GetLinetable(PyCodeObject *code_object);
            void UpdateLinetable(ScopedPyObject &line_table, PyCodeObject *code_object);
        }
    }
}

#endif //CLOUD_DEBUG_PYTHON_LINETABLE_H
