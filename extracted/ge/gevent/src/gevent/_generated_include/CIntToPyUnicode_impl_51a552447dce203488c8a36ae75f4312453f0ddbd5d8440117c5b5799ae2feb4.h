static CYTHON_INLINE PyObject* __Pyx_uchar___Pyx_PyUnicode_From_unsigned_long(unsigned long value, Py_ssize_t width, char padding_char) {
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const unsigned long neg_one = (unsigned long) -1, const_zero = (unsigned long) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
    if (unlikely(!(is_unsigned || value == 0 || value > 0) ||
                    !(sizeof(value) <= 2 || value & ~ (unsigned long) 0x01fffff || __Pyx_CheckUnicodeValue((int) value)))) {
        PyErr_SetString(PyExc_OverflowError, "%c arg not in range(0x110000)");
        return NULL;
    }
    if (width <= 1) {
        return PyUnicode_FromOrdinal((int) value);
    }
    return __Pyx_PyUnicode_FromOrdinal_Padded((int) value, width, padding_char);
}
static CYTHON_INLINE PyObject* __Pyx____Pyx_PyUnicode_From_unsigned_long(unsigned long value, Py_ssize_t width, char padding_char, char format_char) {
    char digits[sizeof(unsigned long)*3+2];
    char *dpos, *end = digits + sizeof(unsigned long)*3+2;
    const char *hex_digits = DIGITS_HEX;
    Py_ssize_t length, ulength;
    int prepend_sign, last_one_off;
    unsigned long remaining;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wconversion"
#endif
    const unsigned long neg_one = (unsigned long) -1, const_zero = (unsigned long) 0;
#ifdef __Pyx_HAS_GCC_DIAGNOSTIC
#pragma GCC diagnostic pop
#endif
    const int is_unsigned = neg_one > const_zero;
    if (format_char == 'X') {
        hex_digits += 16;
        format_char = 'x';
    }
    remaining = value;
    last_one_off = 0;
    dpos = end;
    do {
        int digit_pos;
        switch (format_char) {
        case 'o':
            digit_pos = abs((int)(remaining % (8*8)));
            remaining = (unsigned long) (remaining / (8*8));
            dpos -= 2;
            memcpy(dpos, DIGIT_PAIRS_8 + digit_pos * 2, 2);
            last_one_off = (digit_pos < 8);
            break;
        case 'd':
            digit_pos = abs((int)(remaining % (10*10)));
            remaining = (unsigned long) (remaining / (10*10));
            dpos -= 2;
            memcpy(dpos, DIGIT_PAIRS_10 + digit_pos * 2, 2);
            last_one_off = (digit_pos < 10);
            break;
        case 'x':
            *(--dpos) = hex_digits[abs((int)(remaining % 16))];
            remaining = (unsigned long) (remaining / 16);
            break;
        default:
            assert(0);
            break;
        }
    } while (unlikely(remaining != 0));
    assert(!last_one_off || *dpos == '0');
    dpos += last_one_off;
    length = end - dpos;
    ulength = length;
    prepend_sign = 0;
    if (!is_unsigned && value <= neg_one) {
        if (padding_char == ' ' || width <= length + 1) {
            *(--dpos) = '-';
            ++length;
        } else {
            prepend_sign = 1;
        }
        ++ulength;
    }
    if (width > ulength) {
        ulength = width;
    }
    if (ulength == 1) {
        return PyUnicode_FromOrdinal(*dpos);
    }
    return __Pyx_PyUnicode_BuildFromAscii(ulength, dpos, (int) length, prepend_sign, padding_char);
}

