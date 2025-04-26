#ifndef CLOUD_DEBUG_PYTHON_OPCODE_CACHES_H
#define CLOUD_DEBUG_PYTHON_OPCODE_CACHES_H

#include "common.h"

int GetCacheCount(int opcode) {
    switch (opcode) {
#if PY_VERSION_HEX >= 0x030C0000
#error "Unsupported Python version. Please make sure that opcode caches haven't changed"
#elif PY_VERSION_HEX >= 0x030B0000
        case LOAD_METHOD:
            return 10;
        case LOAD_GLOBAL:
            return 5;
        case BINARY_SUBSCR:
        case STORE_ATTR:
        case LOAD_ATTR:
        case CALL:
            return 4;
        case COMPARE_OP:
            return 2;
        case STORE_SUBSCR:
        case UNPACK_SEQUENCE:
        case BINARY_OP:
        case PRECALL:
            return 1;
#endif
        default:
            return 0;
    }
}
#endif //CLOUD_DEBUG_PYTHON_OPCODE_CACHES_H
