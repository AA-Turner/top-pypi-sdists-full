#include "../common.h"

#include "linetable.h"

namespace devtools {
    namespace cdbg {
        namespace linetable {
#if PY_VERSION_HEX < 0x030A0000
            int GetLineOffset(int line, const ScopedPyObject *original_lnotab, PyCodeObject *code_object) {
                CodeObjectLinesEnumerator lines_enumerator(
                        code_object->co_firstlineno,
                        original_lnotab->get()
                        );
                while (lines_enumerator.line_number() != line) {
                    if (!lines_enumerator.Next()) {
                        return -1;
                    }
                }

                return lines_enumerator.offset();
            }

            void InsertAndUpdateLinetable(int offset, int size, std::vector<uint8> *lnotab, PyCodeObject *code_object) {
                DEBUG("InsertAndUpdateLnotab and update for offset: %d, size: %d\n", offset, size);
                int current_offset = 0;
                for (auto it = lnotab->begin(); it != lnotab->end(); it += 2) {
                    current_offset += it[0];

                    if (current_offset > offset) {
                        int remaining_size = it[0] + size;
                        int remaining_lines = it[1];
                        it = lnotab->erase(it, it + 2);
                        while (remaining_size > 0xFF) {
                            it = lnotab->insert(it, 0xFF) + 1;
                            it = lnotab->insert(it, 0) + 1;
                            remaining_size -= 0xFF;
                        }
                        it = lnotab->insert(it, remaining_size) + 1;
                        it = lnotab->insert(it, remaining_lines) + 1;
                        return;
                    }
                }
            }

            PyObject * GetLinetable(PyCodeObject *code_object) {
                return code_object->co_lnotab;
            }

            void UpdateLinetable(ScopedPyObject &line_table, PyCodeObject *code_object) {
                code_object->co_lnotab = line_table.release();
                Py_INCREF(code_object->co_lnotab);
            }
#endif
        }
    }
}