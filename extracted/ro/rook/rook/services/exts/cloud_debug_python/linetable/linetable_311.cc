#include "../common.h"

#include "linetable.h"

namespace devtools
{
    namespace cdbg
    {
        namespace linetable
        {
#if PY_VERSION_HEX >= 0x030B0000
#define ASSERT_VALID_BOUNDS(bounds) \
    assert(bounds->opaque.lo_next <=  bounds->opaque.limit && \
        (bounds->ar_line == -1 || bounds->ar_line == bounds->opaque.computed_line) && \
        (bounds->opaque.lo_next == bounds->opaque.limit || \
        (*bounds->opaque.lo_next) & 128))

            void PyLineTable_InitAddressRange(const char *linetable, Py_ssize_t length, int firstlineno,
                                              PyCodeAddressRange *range) {
                range->opaque.lo_next = (const uint8_t *) linetable;
                range->opaque.limit = range->opaque.lo_next + length;
                range->ar_start = -1;
                range->ar_end = 0;
                range->opaque.computed_line = firstlineno;
                range->ar_line = -1;
            }

            static unsigned int scan_varint(const uint8_t *ptr) {
                unsigned int read = *ptr++;
                unsigned int val = read & 63;
                unsigned int shift = 0;
                while (read & 64) {
                    read = *ptr++;
                    shift += 6;
                    val |= (read & 63) << shift;
                }
                return val;
            }

            static int scan_signed_varint(const uint8_t *ptr) {
                unsigned int uval = scan_varint(ptr);
                if (uval & 1) {
                    return -(int) (uval >> 1);
                } else {
                    return uval >> 1;
                }
            }

            static inline int at_end(PyCodeAddressRange *bounds) {
                return bounds->opaque.lo_next >= bounds->opaque.limit;
            }

            static int
            get_line_delta(const uint8_t *ptr) {
                int code = ((*ptr) >> 3) & 15;
                DDDEBUG("ptr: 0x%x, code: 0x%x\n", *ptr, code);

                switch (code) {
                    case PY_CODE_LOCATION_INFO_NONE:
                        return 0;
                    case PY_CODE_LOCATION_INFO_NO_COLUMNS:
                    case PY_CODE_LOCATION_INFO_LONG:
                        DDDEBUG("scan signed varint for: 0x%x\n", *ptr);
                        return scan_signed_varint(ptr + 1);
                    case PY_CODE_LOCATION_INFO_ONE_LINE0:
                        return 0;
                    case PY_CODE_LOCATION_INFO_ONE_LINE1:
                        return 1;
                    case PY_CODE_LOCATION_INFO_ONE_LINE2:
                        return 2;
                    default:
                        /* Same line */
                        return 0;
                }
            }

            static inline int is_no_line_marker(uint8_t b) {
                return (b >> 3) == 0x1f;
            }

            static int
            next_code_delta(PyCodeAddressRange *bounds) {
                assert((*bounds->opaque.lo_next) & 128);
                return (((*bounds->opaque.lo_next) & 7) + 1) * sizeof(_Py_CODEUNIT);
                // lo_next & 7 - gets the lowest 3 bits (which is the length-1)
                // then we multiply it be 2 because it's code units length and not count
            }

            static int advance(PyCodeAddressRange *bounds) {
                int bytes_advanced = 0;
                ASSERT_VALID_BOUNDS(bounds);
                bounds->opaque.computed_line += get_line_delta(bounds->opaque.lo_next);
                if (is_no_line_marker(*bounds->opaque.lo_next)) {
                    bounds->ar_line = -1;
                } else {
                    bounds->ar_line = bounds->opaque.computed_line;
                }
                bounds->ar_start = bounds->ar_end;
                bounds->ar_end += next_code_delta(bounds);

                do {
                    bounds->opaque.lo_next++;
                    bytes_advanced++;
                    DDDEBUG("curIndex: %d\n", bytes_advanced);
                } while (bounds->opaque.lo_next < bounds->opaque.limit && ((*bounds->opaque.lo_next) & 128) == 0);
                ASSERT_VALID_BOUNDS(bounds);
                return bytes_advanced;
            }

            static int PyLineTable_NextAddressRange(PyCodeAddressRange *range) {
                if (at_end(range)) {
                    return 0;
                }

                int bytes_advanced = advance(range);
                assert(range->ar_end > range->ar_start);
                return bytes_advanced;
            }

            int GetLineOffset(int line, const ScopedPyObject *original_lnotab, PyCodeObject *code_object) {
                PyCodeAddressRange range;
                const char *linetable = PyBytes_AS_STRING(original_lnotab->get());
                Py_ssize_t length = PyTuple_GET_SIZE(original_lnotab->get());
                PyLineTable_InitAddressRange(linetable, length, code_object->co_firstlineno, &range);
                while (range.ar_line != line) {
                    DDEBUG("range.ar_line: %d, range.ar_start: %d, range.ar_end: %d\n", range.ar_line, range.ar_start,
                           range.ar_end);
                    if (!PyLineTable_NextAddressRange(&range)) {
                        DEBUG("Line %d not found in %s\n", line, CodeObjectDebugString(code_object).c_str());
                        return -1;
                    }
                }

                return range.ar_start;
            }


            void InsertAndUpdateLinetable(int offset, int size, std::vector<uint8> *lnotab, PyCodeObject *code_object) {
                DEBUG("insert and update linetable for offset: %d, size: %d\n", offset, size);
                char *linetable = reinterpret_cast<char *>(lnotab->data());
                PyCodeAddressRange range;
                PyLineTable_InitAddressRange(linetable, lnotab->size(), code_object->co_firstlineno, &range);
                int total_bytes_advanced = 0;
                int bytes_advanced = 0;

                while (range.ar_start < offset) {
                    DDEBUG("find where to insert at offset: %d, range.ar_start: %d, range.ar_end: %d\n", offset,
                           range.ar_start,
                           range.ar_end);
                    bytes_advanced = PyLineTable_NextAddressRange(&range);
                    if (!bytes_advanced) {
                        break;
                    }
                    total_bytes_advanced += bytes_advanced;
                }
                auto it = lnotab->begin();

                it += total_bytes_advanced;
                DDEBUG("insert before it[0]: 0x%x, it[1]: 0x%x, insert: range.ar_start: %d, range.ar_end: %d\n", it[0],
                       it[1], range.ar_start, range.ar_end);

                int codeUnitSize = size / 2;
                while (codeUnitSize > 0) {
                    uint8_t newEntry = 0;
                    if (codeUnitSize > 7) {
                        newEntry = 0xF8 | (7 - 1);
                    } else {
                        newEntry = 0xF8 | (codeUnitSize - 1);
                    }

                    DDEBUG("insert size: %d, new entry: %d\n", codeUnitSize, newEntry);
                    it = lnotab->insert(it, newEntry);
                    codeUnitSize -= 7;
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