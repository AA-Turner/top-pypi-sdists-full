static PyObject *__Pyx_DecompressString(const char *s, Py_ssize_t length, int algo) {
    PyObject *module = NULL, *decompress, *compressed_bytes, *decompressed;
    const char* module_name = algo == 3 ? "compression.zstd" : algo == 2 ? "bz2" : "zlib";
    PyObject *methodname = PyUnicode_FromString("decompress");
    if (unlikely(!methodname)) return NULL;
    #if __PYX_LIMITED_VERSION_HEX >= 0x030e0000
    if (algo == 3) {
        PyObject *fromlist = Py_BuildValue("[O]", methodname);
        if (unlikely(!fromlist)) goto bad;
        module = PyImport_ImportModuleLevel("compression.zstd", NULL, NULL, fromlist, 0);
        Py_DECREF(fromlist);
    } else
    #endif
        module = PyImport_ImportModule(module_name);
    if (unlikely(!module)) goto import_failed;
    decompress = PyObject_GetAttr(module, methodname);
    if (unlikely(!decompress)) goto import_failed;
    {
        #ifdef __cplusplus
            char *memview_bytes = const_cast<char*>(s);
        #else
            #if defined(__clang__)
              #pragma clang diagnostic push
              #pragma clang diagnostic ignored "-Wcast-qual"
            #elif !defined(__INTEL_COMPILER) && defined(__GNUC__)
              #pragma GCC diagnostic push
              #pragma GCC diagnostic ignored "-Wcast-qual"
            #endif
            char *memview_bytes = (char*) s;
            #if defined(__clang__)
              #pragma clang diagnostic pop
            #elif !defined(__INTEL_COMPILER) && defined(__GNUC__)
              #pragma GCC diagnostic pop
            #endif
        #endif
        #if CYTHON_COMPILING_IN_LIMITED_API && !defined(PyBUF_READ)
        int memview_flags = 0x100;
        #else
        int memview_flags = PyBUF_READ;
        #endif
        compressed_bytes = PyMemoryView_FromMemory(memview_bytes, length, memview_flags);
    }
    if (unlikely(!compressed_bytes)) {
        Py_DECREF(decompress);
        goto bad;
    }
    decompressed = PyObject_CallFunctionObjArgs(decompress, compressed_bytes, NULL);
    Py_DECREF(compressed_bytes);
    Py_DECREF(decompress);
    Py_DECREF(module);
    Py_DECREF(methodname);
    return decompressed;
import_failed:
    PyErr_Format(PyExc_ImportError,
        "Failed to import '%.20s.decompress' - cannot initialise module strings. "
        "String compression was configured with the C macro 'CYTHON_COMPRESS_STRINGS=%d'.",
        module_name, algo);
bad:
    Py_XDECREF(module);
    Py_DECREF(methodname);
    return NULL;
}

