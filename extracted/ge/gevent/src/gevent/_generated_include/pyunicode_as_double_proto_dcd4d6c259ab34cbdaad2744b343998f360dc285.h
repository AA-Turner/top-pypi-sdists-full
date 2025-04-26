#if PY_MAJOR_VERSION >= 3 && !CYTHON_COMPILING_IN_PYPY && CYTHON_ASSUME_SAFE_MACROS
static const char* __Pyx__PyUnicode_AsDouble_Copy(const void* data, const int kind, char* buffer, Py_ssize_t start, Py_ssize_t end) {
    int last_was_punctuation;
    Py_ssize_t i;
    last_was_punctuation = 1;
    for (i=start; i <= end; i++) {
        Py_UCS4 chr = PyUnicode_READ(kind, data, i);
        int is_punctuation = (chr == '_') | (chr == '.');
        *buffer = (char)chr;
        buffer += (chr != '_');
        if (unlikely(chr > 127)) goto parse_failure;
        if (unlikely(last_was_punctuation & is_punctuation)) goto parse_failure;
        last_was_punctuation = is_punctuation;
    }
    if (unlikely(last_was_punctuation)) goto parse_failure;
    *buffer = '\0';
    return buffer;
parse_failure:
    return NULL;
}
static double __Pyx__PyUnicode_AsDouble_inf_nan(const void* data, int kind, Py_ssize_t start, Py_ssize_t length) {
    int matches = 1;
    Py_UCS4 chr;
    Py_UCS4 sign = PyUnicode_READ(kind, data, start);
    int is_signed = (sign == '-') | (sign == '+');
    start += is_signed;
    length -= is_signed;
    switch (PyUnicode_READ(kind, data, start)) {
        #ifdef Py_NAN
        case 'n':
        case 'N':
            if (unlikely(length != 3)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+1);
            matches &= (chr == 'a') | (chr == 'A');
            chr = PyUnicode_READ(kind, data, start+2);
            matches &= (chr == 'n') | (chr == 'N');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_NAN : Py_NAN;
        #endif
        case 'i':
        case 'I':
            if (unlikely(length < 3)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+1);
            matches &= (chr == 'n') | (chr == 'N');
            chr = PyUnicode_READ(kind, data, start+2);
            matches &= (chr == 'f') | (chr == 'F');
            if (likely(length == 3 && matches))
                return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
            if (unlikely(length != 8)) goto parse_failure;
            chr = PyUnicode_READ(kind, data, start+3);
            matches &= (chr == 'i') | (chr == 'I');
            chr = PyUnicode_READ(kind, data, start+4);
            matches &= (chr == 'n') | (chr == 'N');
            chr = PyUnicode_READ(kind, data, start+5);
            matches &= (chr == 'i') | (chr == 'I');
            chr = PyUnicode_READ(kind, data, start+6);
            matches &= (chr == 't') | (chr == 'T');
            chr = PyUnicode_READ(kind, data, start+7);
            matches &= (chr == 'y') | (chr == 'Y');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
        case '.': case '0': case '1': case '2': case '3': case '4': case '5': case '6': case '7': case '8': case '9':
            break;
        default:
            goto parse_failure;
    }
    return 0.0;
parse_failure:
    return -1.0;
}
static double __Pyx_PyUnicode_AsDouble_WithSpaces(PyObject *obj) {
    double value;
    const char *last;
    char *end;
    Py_ssize_t start, length = PyUnicode_GET_LENGTH(obj);
    const int kind = PyUnicode_KIND(obj);
    const void* data = PyUnicode_DATA(obj);
    start = 0;
    while (Py_UNICODE_ISSPACE(PyUnicode_READ(kind, data, start)))
        start++;
    while (start < length - 1 && Py_UNICODE_ISSPACE(PyUnicode_READ(kind, data, length - 1)))
        length--;
    length -= start;
    if (unlikely(length <= 0)) goto fallback;
    value = __Pyx__PyUnicode_AsDouble_inf_nan(data, kind, start, length);
    if (unlikely(value == -1.0)) goto fallback;
    if (value != 0.0) return value;
    if (length < 40) {
        char number[40];
        last = __Pyx__PyUnicode_AsDouble_Copy(data, kind, number, start, start + length);
        if (unlikely(!last)) goto fallback;
        value = PyOS_string_to_double(number, &end, NULL);
    } else {
        char *number = (char*) PyMem_Malloc((length + 1) * sizeof(char));
        if (unlikely(!number)) goto fallback;
        last = __Pyx__PyUnicode_AsDouble_Copy(data, kind, number, start, start + length);
        if (unlikely(!last)) {
            PyMem_Free(number);
            goto fallback;
        }
        value = PyOS_string_to_double(number, &end, NULL);
        PyMem_Free(number);
    }
    if (likely(end == last) || (value == (double)-1 && PyErr_Occurred())) {
        return value;
    }
fallback:
    return __Pyx_SlowPyString_AsDouble(obj);
}
#endif
static CYTHON_INLINE double __Pyx_PyUnicode_AsDouble(PyObject *obj) {
#if PY_MAJOR_VERSION >= 3 && !CYTHON_COMPILING_IN_PYPY && CYTHON_ASSUME_SAFE_MACROS
    if (unlikely(__Pyx_PyUnicode_READY(obj) == -1))
        return (double)-1;
    if (likely(PyUnicode_IS_ASCII(obj))) {
        const char *s;
        Py_ssize_t length;
        s = PyUnicode_AsUTF8AndSize(obj, &length);
        return __Pyx__PyBytes_AsDouble(obj, s, length);
    }
    return __Pyx_PyUnicode_AsDouble_WithSpaces(obj);
#else
    return __Pyx_SlowPyString_AsDouble(obj);
#endif
}

