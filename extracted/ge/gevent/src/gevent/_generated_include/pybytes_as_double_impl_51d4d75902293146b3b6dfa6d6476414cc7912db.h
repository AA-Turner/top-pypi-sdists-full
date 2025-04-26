static double __Pyx_SlowPyString_AsDouble(PyObject *obj) {
    PyObject *float_value;
#if PY_MAJOR_VERSION >= 3
    float_value = PyFloat_FromString(obj);
#else
    float_value = PyFloat_FromString(obj, 0);
#endif
    if (likely(float_value)) {
#if CYTHON_ASSUME_SAFE_MACROS
        double value = PyFloat_AS_DOUBLE(float_value);
#else
        double value = PyFloat_AsDouble(float_value);
#endif
        Py_DECREF(float_value);
        return value;
    }
    return (double)-1;
}
static const char* __Pyx__PyBytes_AsDouble_Copy(const char* start, char* buffer, Py_ssize_t length) {
    int last_was_punctuation = 1;
    Py_ssize_t i;
    for (i=0; i < length; i++) {
        char chr = start[i];
        int is_punctuation = (chr == '_') | (chr == '.') | (chr == 'e') | (chr == 'E');
        *buffer = chr;
        buffer += (chr != '_');
        if (unlikely(last_was_punctuation & is_punctuation)) goto parse_failure;
        last_was_punctuation = is_punctuation;
    }
    if (unlikely(last_was_punctuation)) goto parse_failure;
    *buffer = '\0';
    return buffer;
parse_failure:
    return NULL;
}
static double __Pyx__PyBytes_AsDouble_inf_nan(const char* start, Py_ssize_t length) {
    int matches = 1;
    char sign = start[0];
    int is_signed = (sign == '+') | (sign == '-');
    start += is_signed;
    length -= is_signed;
    switch (start[0]) {
        #ifdef Py_NAN
        case 'n':
        case 'N':
            if (unlikely(length != 3)) goto parse_failure;
            matches &= (start[1] == 'a' || start[1] == 'A');
            matches &= (start[2] == 'n' || start[2] == 'N');
            if (unlikely(!matches)) goto parse_failure;
            return (sign == '-') ? -Py_NAN : Py_NAN;
        #endif
        case 'i':
        case 'I':
            if (unlikely(length < 3)) goto parse_failure;
            matches &= (start[1] == 'n' || start[1] == 'N');
            matches &= (start[2] == 'f' || start[2] == 'F');
            if (likely(length == 3 && matches))
                return (sign == '-') ? -Py_HUGE_VAL : Py_HUGE_VAL;
            if (unlikely(length != 8)) goto parse_failure;
            matches &= (start[3] == 'i' || start[3] == 'I');
            matches &= (start[4] == 'n' || start[4] == 'N');
            matches &= (start[5] == 'i' || start[5] == 'I');
            matches &= (start[6] == 't' || start[6] == 'T');
            matches &= (start[7] == 'y' || start[7] == 'Y');
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
static CYTHON_INLINE int __Pyx__PyBytes_AsDouble_IsSpace(char ch) {
    return (ch == 0x20) | !((ch < 0x9) | (ch > 0xd));
}
CYTHON_UNUSED static double __Pyx__PyBytes_AsDouble(PyObject *obj, const char* start, Py_ssize_t length) {
    double value;
    Py_ssize_t i, digits;
    const char *last = start + length;
    char *end;
    while (__Pyx__PyBytes_AsDouble_IsSpace(*start))
        start++;
    while (start < last - 1 && __Pyx__PyBytes_AsDouble_IsSpace(last[-1]))
        last--;
    length = last - start;
    if (unlikely(length <= 0)) goto fallback;
    value = __Pyx__PyBytes_AsDouble_inf_nan(start, length);
    if (unlikely(value == -1.0)) goto fallback;
    if (value != 0.0) return value;
    digits = 0;
    for (i=0; i < length; digits += start[i++] != '_');
    if (likely(digits == length)) {
        value = PyOS_string_to_double(start, &end, NULL);
    } else if (digits < 40) {
        char number[40];
        last = __Pyx__PyBytes_AsDouble_Copy(start, number, length);
        if (unlikely(!last)) goto fallback;
        value = PyOS_string_to_double(number, &end, NULL);
    } else {
        char *number = (char*) PyMem_Malloc((digits + 1) * sizeof(char));
        if (unlikely(!number)) goto fallback;
        last = __Pyx__PyBytes_AsDouble_Copy(start, number, length);
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

