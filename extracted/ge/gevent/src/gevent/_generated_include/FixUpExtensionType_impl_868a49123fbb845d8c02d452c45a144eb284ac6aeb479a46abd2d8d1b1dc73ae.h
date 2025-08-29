static int __Pyx_fix_up_extension_type_from_spec(PyType_Spec *spec, PyTypeObject *type) {
#if __PYX_LIMITED_VERSION_HEX > 0x030900B1
    CYTHON_UNUSED_VAR(spec);
    CYTHON_UNUSED_VAR(type);
    CYTHON_UNUSED_VAR(__Pyx__SetItemOnTypeDict);
#else
    const PyType_Slot *slot = spec->slots;
    int changed = 0;
#if !CYTHON_COMPILING_IN_LIMITED_API
    while (slot && slot->slot && slot->slot != Py_tp_members)
        slot++;
    if (slot && slot->slot == Py_tp_members) {
#if !CYTHON_COMPILING_IN_CPYTHON
        const
#endif  // !CYTHON_COMPILING_IN_CPYTHON)
            PyMemberDef *memb = (PyMemberDef*) slot->pfunc;
        while (memb && memb->name) {
            if (memb->name[0] == '_' && memb->name[1] == '_') {
                if (strcmp(memb->name, "__weaklistoffset__") == 0) {
                    assert(memb->type == T_PYSSIZET);
                    assert(memb->flags == READONLY);
                    type->tp_weaklistoffset = memb->offset;
                    changed = 1;
                }
                else if (strcmp(memb->name, "__dictoffset__") == 0) {
                    assert(memb->type == T_PYSSIZET);
                    assert(memb->flags == READONLY);
                    type->tp_dictoffset = memb->offset;
                    changed = 1;
                }
#if CYTHON_METH_FASTCALL
                else if (strcmp(memb->name, "__vectorcalloffset__") == 0) {
                    assert(memb->type == T_PYSSIZET);
                    assert(memb->flags == READONLY);
#if PY_VERSION_HEX >= 0x030800b4
                    type->tp_vectorcall_offset = memb->offset;
#else
                    type->tp_print = (printfunc) memb->offset;
#endif
                    changed = 1;
                }
#endif  // CYTHON_METH_FASTCALL
                else if (strcmp(memb->name, "__module__") == 0) {
                    PyObject *descr;
                    assert(memb->type == T_OBJECT);
                    assert(memb->flags == 0 || memb->flags == READONLY);
                    descr = PyDescr_NewMember(type, memb);
                    if (unlikely(!descr))
                        return -1;
                    int set_item_result = PyDict_SetItem(type->tp_dict, PyDescr_NAME(descr), descr);
                    Py_DECREF(descr);
                    if (unlikely(set_item_result < 0)) {
                        return -1;
                    }
                    changed = 1;
                }
            }
            memb++;
        }
    }
#endif  // !CYTHON_COMPILING_IN_LIMITED_API
    slot = spec->slots;
    while (slot && slot->slot && slot->slot != Py_tp_getset)
        slot++;
    if (slot && slot->slot == Py_tp_getset) {
        PyGetSetDef *getset = (PyGetSetDef*) slot->pfunc;
        while (getset && getset->name) {
            if (getset->name[0] == '_' && getset->name[1] == '_' && strcmp(getset->name, "__module__") == 0) {
                PyObject *descr = PyDescr_NewGetSet(type, getset);
                if (unlikely(!descr))
                    return -1;
                #if CYTHON_COMPILING_IN_LIMITED_API
                PyObject *pyname = PyUnicode_FromString(getset->name);
                if (unlikely(!pyname)) {
                    Py_DECREF(descr);
                    return -1;
                }
                int set_item_result = __Pyx_SetItemOnTypeDict(type, pyname, descr);
                Py_DECREF(pyname);
                #else
                CYTHON_UNUSED_VAR(__Pyx__SetItemOnTypeDict);
                int set_item_result = PyDict_SetItem(type->tp_dict, PyDescr_NAME(descr), descr);
                #endif
                Py_DECREF(descr);
                if (unlikely(set_item_result < 0)) {
                    return -1;
                }
                changed = 1;
            }
            ++getset;
        }
    }
    if (changed)
        PyType_Modified(type);
#endif  // PY_VERSION_HEX > 0x030900B1
    return 0;
}

