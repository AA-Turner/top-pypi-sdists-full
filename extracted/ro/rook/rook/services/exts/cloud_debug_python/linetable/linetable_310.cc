#include "../common.h"

#include "linetable.h"

namespace devtools
{
    namespace cdbg
    {
        namespace linetable
        {
#if PY_VERSION_HEX >= 0x030A0000 && PY_VERSION_HEX < 0x030B0000
            static void PyLineTable_InitAddressRange(const char *linetable, Py_ssize_t length, int firstlineno, PyCodeAddressRange *range)
            {
                range->opaque.lo_next = linetable;
                range->opaque.limit = range->opaque.lo_next + length;
                range->ar_start = -1;
                range->ar_end = 0;
                range->opaque.computed_line = firstlineno;
                range->ar_line = -1;
            }

            static void
            advance(PyCodeAddressRange *bounds)
            {
                bounds->ar_start = bounds->ar_end;
                int delta = ((unsigned char *)bounds->opaque.lo_next)[0];
                bounds->ar_end += delta;
                int ldelta = ((signed char *)bounds->opaque.lo_next)[1];
                bounds->opaque.lo_next += 2;
                if (ldelta == -128) {
                    bounds->ar_line = -1;
                }
                else {
                    bounds->opaque.computed_line += ldelta;
                    bounds->ar_line = bounds->opaque.computed_line;
                }
            }

            static inline int at_end(PyCodeAddressRange *bounds)
            {
                return bounds->opaque.lo_next >= bounds->opaque.limit;
            }

            static int PyLineTable_NextAddressRange(PyCodeAddressRange *range)
            {
                if (at_end(range)) {
                    return 0;
                }
                advance(range);
                while (range->ar_start == range->ar_end) {
                    assert(!at_end(range));
                    advance(range);
                }
                return 1;
            }

            int GetLineOffset(int line, const ScopedPyObject *original_lnotab, PyCodeObject *code_object)
            {
                PyCodeAddressRange range;
                const char * linetable = PyBytes_AS_STRING(code_object->co_linetable);
                Py_ssize_t length = PyBytes_GET_SIZE(code_object->co_linetable);
                linetable::PyLineTable_InitAddressRange(linetable, length, code_object->co_firstlineno, &range);
                while (range.ar_line != line)
                {
                    DDEBUG("range.ar_line: %d, range.ar_start: %d, range.ar_end: %d\n", range.ar_line, range.ar_start, range.ar_end);
                    if (!linetable::PyLineTable_NextAddressRange(&range))
                    {
                        DEBUG("Line %d not found in %s\n", line, CodeObjectDebugString(code_object).c_str());
                        return -1;
                    }
                }
                return range.ar_start;
            }

            // Updates the line number table for an insertion in the bytecode.
            // This is different from what the Python 2 version of InsertMethodCall() does.
            // It should be more accurate, but is confined to Python 3 only for safety.
            // This handles the case of adding insertion for EXTENDED_ARG better.
            // Example for inserting 2 bytes at offset 2:
            // lnotab: [{2, 1}, {4, 1}] // {offset_delta, line_delta}
            // Old algorithm: [{2, 0}, {2, 1}, {4, 1}]
            // New algorithm: [{2, 1}, {6, 1}]
            // In the old version, trying to get the offset to insert a breakpoint right
            // before line 1 would result in an offset of 2, which is inaccurate as the
            // instruction before is an EXTENDED_ARG which will now be applied to the first
            // instruction inserted instead of its original target.
            void InsertAndUpdateLinetable(int offset, int size, std::vector<uint8> *lnotab, PyCodeObject *code_object)
            {
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
                return code_object->co_linetable;
            }

            void UpdateLinetable(ScopedPyObject &line_table, PyCodeObject *code_object) {
                code_object->co_linetable = line_table.release();
                Py_INCREF(code_object->co_linetable);
            }
#endif
        }
    }
}