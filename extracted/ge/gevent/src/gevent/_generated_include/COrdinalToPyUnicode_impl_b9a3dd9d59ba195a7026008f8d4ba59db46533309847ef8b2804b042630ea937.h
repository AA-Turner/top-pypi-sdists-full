static CYTHON_INLINE int __Pyx_CheckUnicodeValue(int value) {
    return value <= 1114111;
}
static PyObject* __Pyx_PyUnicode_FromOrdinal_Padded(int value, Py_ssize_t ulength, char padding_char) {
    Py_ssize_t padding_length = ulength - 1;
    if (likely((padding_length <= 250) && (value < 0xD800 || value > 0xDFFF))) {
        char chars[256];
        if (value <= 255) {
            memset(chars, padding_char, (size_t) padding_length);
            chars[ulength-1] = (char) value;
            return PyUnicode_DecodeLatin1(chars, ulength, NULL);
        }
        char *cpos = chars + sizeof(chars);
        if (value < 0x800) {
            *--cpos = (char) (0x80 | (value & 0x3f));
            value >>= 6;
            *--cpos = (char) (0xc0 | (value & 0x1f));
        } else if (value < 0x10000) {
            *--cpos = (char) (0x80 | (value & 0x3f));
            value >>= 6;
            *--cpos = (char) (0x80 | (value & 0x3f));
            value >>= 6;
            *--cpos = (char) (0xe0 | (value & 0x0f));
        } else {
            *--cpos = (char) (0x80 | (value & 0x3f));
            value >>= 6;
            *--cpos = (char) (0x80 | (value & 0x3f));
            value >>= 6;
            *--cpos = (char) (0x80 | (value & 0x3f));
            value >>= 6;
            *--cpos = (char) (0xf0 | (value & 0x07));
        }
        cpos -= padding_length;
        memset(cpos, padding_char, (size_t) padding_length);
        return PyUnicode_DecodeUTF8(cpos, chars + sizeof(chars) - cpos, NULL);
    }
    if (value <= 127 && CYTHON_USE_UNICODE_INTERNALS) {
        const char chars[1] = {(char) value};
        return __Pyx_PyUnicode_BuildFromAscii(ulength, chars, 1, 0, padding_char);
    }
    {
        PyObject *uchar, *padding_uchar, *padding, *result;
        padding_uchar = PyUnicode_FromOrdinal(padding_char);
        if (unlikely(!padding_uchar)) return NULL;
        padding = PySequence_Repeat(padding_uchar, padding_length);
        Py_DECREF(padding_uchar);
        if (unlikely(!padding)) return NULL;
        uchar = PyUnicode_FromOrdinal(value);
        if (unlikely(!uchar)) {
            Py_DECREF(padding);
            return NULL;
        }
        result = PyUnicode_Concat(padding, uchar);
        Py_DECREF(padding);
        Py_DECREF(uchar);
        return result;
    }
}

