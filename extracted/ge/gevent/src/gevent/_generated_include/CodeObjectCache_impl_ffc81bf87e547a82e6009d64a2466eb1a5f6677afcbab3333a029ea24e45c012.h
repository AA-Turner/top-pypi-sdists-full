static int __pyx_bisect_code_objects(__Pyx_CodeObjectCacheEntry* entries, int count, int code_line) {
    int start = 0, mid = 0, end = count - 1;
    if (end >= 0 && code_line > entries[end].code_line) {
        return count;
    }
    while (start < end) {
        mid = start + (end - start) / 2;
        if (code_line < entries[mid].code_line) {
            end = mid;
        } else if (code_line > entries[mid].code_line) {
             start = mid + 1;
        } else {
            return mid;
        }
    }
    if (code_line <= entries[mid].code_line) {
        return mid;
    } else {
        return mid + 1;
    }
}
static __Pyx_CachedCodeObjectType *__pyx__find_code_object(struct __Pyx_CodeObjectCache *code_cache, int code_line) {
    __Pyx_CachedCodeObjectType* code_object;
    int pos;
    if (unlikely(!code_line) || unlikely(!code_cache->entries)) {
        return NULL;
    }
    pos = __pyx_bisect_code_objects(code_cache->entries, code_cache->count, code_line);
    if (unlikely(pos >= code_cache->count) || unlikely(code_cache->entries[pos].code_line != code_line)) {
        return NULL;
    }
    code_object = code_cache->entries[pos].code_object;
    Py_INCREF(code_object);
    return code_object;
}
static __Pyx_CachedCodeObjectType *__pyx_find_code_object(int code_line) {
#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING && !CYTHON_ATOMICS
    (void)__pyx__find_code_object;
    return NULL; // Most implementation should have atomics. But otherwise, don't make it thread-safe, just miss.
#else
    struct __Pyx_CodeObjectCache *code_cache = &__pyx_mstate_global->__pyx_code_cache;
#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
    __pyx_nonatomic_int_type old_count = __pyx_atomic_incr_acq_rel(&code_cache->accessor_count);
    if (old_count < 0) {
        __pyx_atomic_decr_acq_rel(&code_cache->accessor_count);
        return NULL;
    }
#endif
    __Pyx_CachedCodeObjectType *result = __pyx__find_code_object(code_cache, code_line);
#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
    __pyx_atomic_decr_acq_rel(&code_cache->accessor_count);
#endif
    return result;
#endif
}
static void __pyx__insert_code_object(struct __Pyx_CodeObjectCache *code_cache, int code_line, __Pyx_CachedCodeObjectType* code_object)
{
    int pos, i;
    __Pyx_CodeObjectCacheEntry* entries = code_cache->entries;
    if (unlikely(!code_line)) {
        return;
    }
    if (unlikely(!entries)) {
        entries = (__Pyx_CodeObjectCacheEntry*)PyMem_Malloc(64*sizeof(__Pyx_CodeObjectCacheEntry));
        if (likely(entries)) {
            code_cache->entries = entries;
            code_cache->max_count = 64;
            code_cache->count = 1;
            entries[0].code_line = code_line;
            entries[0].code_object = code_object;
            Py_INCREF(code_object);
        }
        return;
    }
    pos = __pyx_bisect_code_objects(code_cache->entries, code_cache->count, code_line);
    if ((pos < code_cache->count) && unlikely(code_cache->entries[pos].code_line == code_line)) {
        __Pyx_CachedCodeObjectType* tmp = entries[pos].code_object;
        entries[pos].code_object = code_object;
        Py_INCREF(code_object);
        Py_DECREF(tmp);
        return;
    }
    if (code_cache->count == code_cache->max_count) {
        int new_max = code_cache->max_count + 64;
        entries = (__Pyx_CodeObjectCacheEntry*)PyMem_Realloc(
            code_cache->entries, ((size_t)new_max) * sizeof(__Pyx_CodeObjectCacheEntry));
        if (unlikely(!entries)) {
            return;
        }
        code_cache->entries = entries;
        code_cache->max_count = new_max;
    }
    for (i=code_cache->count; i>pos; i--) {
        entries[i] = entries[i-1];
    }
    entries[pos].code_line = code_line;
    entries[pos].code_object = code_object;
    code_cache->count++;
    Py_INCREF(code_object);
}
static void __pyx_insert_code_object(int code_line, __Pyx_CachedCodeObjectType* code_object) {
#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING && !CYTHON_ATOMICS
    (void)__pyx__insert_code_object;
    return; // Most implementation should have atomics. But otherwise, don't make it thread-safe, just fail.
#else
    struct __Pyx_CodeObjectCache *code_cache = &__pyx_mstate_global->__pyx_code_cache;
#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
    __pyx_nonatomic_int_type expected = 0;
    if (!__pyx_atomic_int_cmp_exchange(&code_cache->accessor_count, &expected, INT_MIN)) {
        return;
    }
#endif
    __pyx__insert_code_object(code_cache, code_line, code_object);
#if CYTHON_COMPILING_IN_CPYTHON_FREETHREADING
    __pyx_atomic_sub(&code_cache->accessor_count, INT_MIN);
#endif
#endif
}

