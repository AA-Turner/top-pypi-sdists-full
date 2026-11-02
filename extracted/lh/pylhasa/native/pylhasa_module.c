#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>
#include <stdlib.h>
#include <string.h>

#include "lhasa.h"
#include "lha_file_header.h"
#include "lha_reader.h"

typedef enum {
    BACKEND_PATH = 1,
    BACKEND_BYTES = 2
} BackendType;

typedef struct {
    const unsigned char *data;
    size_t size;
    size_t pos;
} MemoryStream;

typedef struct {
    PyObject_HEAD
    BackendType backend;
    char *path;
    PyObject *bytes_owner;
    PyObject *entries_cache;
    size_t entry_count;
    int closed;
} PyLhasaArchive;

typedef struct {
    PyObject_HEAD
    LHAReader *reader;
    LHAInputStream *stream;
    PyObject *bytes_owner;
    int closed;
} PyLhasaEntryReader;

static PyObject *PylhasaError;
static PyObject *BadArchiveError;

static PyTypeObject PyLhasaArchive_Type;
static PyTypeObject PyLhasaEntryReader_Type;

static PyObject *decode_utf8_replace(const char *value) {
    if (!value) {
        Py_RETURN_NONE;
    }
    return PyUnicode_DecodeUTF8(value, (Py_ssize_t)strlen(value), "replace");
}

static int mem_read(void *handle, void *buf, size_t buf_len) {
    MemoryStream *stream = (MemoryStream *)handle;
    if (stream->pos >= stream->size) {
        return 0;
    }
    size_t remaining = stream->size - stream->pos;
    size_t to_read = buf_len < remaining ? buf_len : remaining;
    memcpy(buf, stream->data + stream->pos, to_read);
    stream->pos += to_read;
    return (int)to_read;
}

static int mem_skip(void *handle, size_t bytes) {
    MemoryStream *stream = (MemoryStream *)handle;
    size_t remaining = stream->size - stream->pos;
    if (bytes > remaining) {
        stream->pos = stream->size;
        return 0;
    }
    stream->pos += bytes;
    return 1;
}

static void mem_close(void *handle) {
    free(handle);
}

static const LHAInputStreamType memory_stream_type = {
    mem_read,
    mem_skip,
    mem_close,
};

static LHAInputStream *create_input_stream(PyLhasaArchive *archive, PyObject **bytes_owner_out) {
    if (archive->backend == BACKEND_PATH) {
        return lha_input_stream_from(archive->path);
    }
    if (archive->backend == BACKEND_BYTES) {
        MemoryStream *ms = (MemoryStream *)calloc(1, sizeof(MemoryStream));
        if (!ms) {
            return NULL;
        }
        Py_ssize_t len = PyBytes_GET_SIZE(archive->bytes_owner);
        ms->data = (const unsigned char *)PyBytes_AS_STRING(archive->bytes_owner);
        ms->size = (size_t)len;
        ms->pos = 0;
        if (bytes_owner_out) {
            *bytes_owner_out = archive->bytes_owner;
            Py_INCREF(archive->bytes_owner);
        }
        return lha_input_stream_new(&memory_stream_type, ms);
    }
    return NULL;
}

static void free_reader(LHAReader *reader, LHAInputStream *stream) {
    if (reader) {
        lha_reader_free(reader);
    }
    if (stream) {
        lha_input_stream_free(stream);
    }
}

static PyObject *build_entries(PyLhasaArchive *self) {
    PyObject *list = PyList_New(0);
    if (!list) {
        return NULL;
    }

    PyObject *bytes_owner = NULL;
    LHAInputStream *stream = create_input_stream(self, &bytes_owner);
    if (!stream) {
        Py_XDECREF(bytes_owner);
        Py_DECREF(list);
        PyErr_SetString(BadArchiveError, "failed to open archive stream");
        return NULL;
    }

    LHAReader *reader = lha_reader_new(stream);
    if (!reader) {
        Py_XDECREF(bytes_owner);
        lha_input_stream_free(stream);
        Py_DECREF(list);
        PyErr_SetString(BadArchiveError, "failed to initialize reader");
        return NULL;
    }
    lha_reader_set_dir_policy(reader, LHA_READER_DIR_PLAIN);

    LHAFileHeader *header;
    while ((header = lha_reader_next_file(reader)) != NULL) {
        if (lha_reader_current_is_fake(reader)) {
            continue;
        }
        char *full_path = lha_file_header_full_path(header);
        if (!full_path) {
            free_reader(reader, stream);
            Py_XDECREF(bytes_owner);
            Py_DECREF(list);
            PyErr_SetString(BadArchiveError, "failed to read header path");
            return NULL;
        }

        PyObject *dict = PyDict_New();
        if (!dict) {
            free(full_path);
            free_reader(reader, stream);
            Py_XDECREF(bytes_owner);
            Py_DECREF(list);
            return NULL;
        }

        PyObject *raw_bytes = PyBytes_FromStringAndSize(full_path, (Py_ssize_t)strlen(full_path));
        PyObject *method = PyUnicode_FromString(header->compress_method);
        PyObject *size_obj = PyLong_FromUnsignedLongLong(header->length);
        PyObject *csize_obj = PyLong_FromUnsignedLongLong(header->compressed_length);
        PyObject *ts_obj = PyLong_FromUnsignedLong(header->timestamp);
        int is_symlink = header->symlink_target != NULL;
        int is_dir = strcmp(header->compress_method, LHA_COMPRESS_TYPE_DIR) == 0 && !is_symlink;
        PyObject *is_dir_obj = PyBool_FromLong(is_dir ? 1 : 0);
        PyObject *is_symlink_obj = PyBool_FromLong(is_symlink ? 1 : 0);
        PyObject *crc_obj = PyLong_FromUnsignedLong(header->crc);
        PyObject *header_level_obj = PyLong_FromUnsignedLong(header->header_level);
        PyObject *os_type_obj = PyLong_FromUnsignedLong(header->os_type);
        PyObject *extra_flags_obj = PyLong_FromUnsignedLong(header->extra_flags);
        PyObject *path_obj = decode_utf8_replace(header->path);
        PyObject *filename_obj = decode_utf8_replace(header->filename);
        PyObject *symlink_obj = decode_utf8_replace(header->symlink_target);
        PyObject *unix_username_obj = decode_utf8_replace(header->unix_username);
        PyObject *unix_group_obj = decode_utf8_replace(header->unix_group);
        PyObject *raw_header_obj = Py_None;
        PyObject *raw_header_len_obj = PyLong_FromUnsignedLongLong(header->raw_data_len);
        if (header->raw_data != NULL && header->raw_data_len > 0) {
            raw_header_obj = PyBytes_FromStringAndSize((const char *)header->raw_data,
                                                       (Py_ssize_t)header->raw_data_len);
        } else {
            Py_INCREF(Py_None);
        }

        if (!raw_bytes || !method || !size_obj || !csize_obj || !ts_obj || !is_dir_obj || !is_symlink_obj || !crc_obj
            || !header_level_obj || !os_type_obj || !extra_flags_obj || !path_obj || !filename_obj || !symlink_obj
            || !unix_username_obj || !unix_group_obj || !raw_header_obj || !raw_header_len_obj) {
            Py_XDECREF(raw_bytes);
            Py_XDECREF(method);
            Py_XDECREF(size_obj);
            Py_XDECREF(csize_obj);
            Py_XDECREF(ts_obj);
            Py_XDECREF(is_dir_obj);
            Py_XDECREF(is_symlink_obj);
            Py_XDECREF(crc_obj);
            Py_XDECREF(header_level_obj);
            Py_XDECREF(os_type_obj);
            Py_XDECREF(extra_flags_obj);
            Py_XDECREF(path_obj);
            Py_XDECREF(filename_obj);
            Py_XDECREF(symlink_obj);
            Py_XDECREF(unix_username_obj);
            Py_XDECREF(unix_group_obj);
            Py_XDECREF(raw_header_obj);
            Py_XDECREF(raw_header_len_obj);
            Py_DECREF(dict);
            free(full_path);
            free_reader(reader, stream);
            Py_XDECREF(bytes_owner);
            Py_DECREF(list);
            return NULL;
        }

        PyDict_SetItemString(dict, "raw_path_bytes", raw_bytes);
        PyDict_SetItemString(dict, "method", method);
        PyDict_SetItemString(dict, "size", size_obj);
        PyDict_SetItemString(dict, "compressed_size", csize_obj);
        PyDict_SetItemString(dict, "timestamp", ts_obj);
        PyDict_SetItemString(dict, "crc", crc_obj);
        PyDict_SetItemString(dict, "is_dir", is_dir_obj);
        PyDict_SetItemString(dict, "is_symlink", is_symlink_obj);
        PyDict_SetItemString(dict, "header_level", header_level_obj);
        PyDict_SetItemString(dict, "os_type", os_type_obj);
        PyDict_SetItemString(dict, "extra_flags", extra_flags_obj);
        PyDict_SetItemString(dict, "path", path_obj);
        PyDict_SetItemString(dict, "filename", filename_obj);
        PyDict_SetItemString(dict, "symlink_target", symlink_obj);
        PyDict_SetItemString(dict, "unix_username", unix_username_obj);
        PyDict_SetItemString(dict, "unix_group", unix_group_obj);
        PyDict_SetItemString(dict, "raw_header_bytes", raw_header_obj);
        PyDict_SetItemString(dict, "raw_header_len", raw_header_len_obj);

        if (LHA_FILE_HAVE_EXTRA(header, LHA_FILE_UNIX_PERMS)) {
            PyObject *obj = PyLong_FromUnsignedLong(header->unix_perms);
            PyDict_SetItemString(dict, "unix_perms", obj ? obj : Py_None);
            Py_XDECREF(obj);
        } else {
            PyDict_SetItemString(dict, "unix_perms", Py_None);
        }

        if (LHA_FILE_HAVE_EXTRA(header, LHA_FILE_UNIX_UID_GID)) {
            PyObject *uid_obj = PyLong_FromUnsignedLong(header->unix_uid);
            PyObject *gid_obj = PyLong_FromUnsignedLong(header->unix_gid);
            PyDict_SetItemString(dict, "unix_uid", uid_obj ? uid_obj : Py_None);
            PyDict_SetItemString(dict, "unix_gid", gid_obj ? gid_obj : Py_None);
            Py_XDECREF(uid_obj);
            Py_XDECREF(gid_obj);
        } else {
            PyDict_SetItemString(dict, "unix_uid", Py_None);
            PyDict_SetItemString(dict, "unix_gid", Py_None);
        }

        if (LHA_FILE_HAVE_EXTRA(header, LHA_FILE_OS9_PERMS)) {
            PyObject *obj = PyLong_FromUnsignedLong(header->os9_perms);
            PyDict_SetItemString(dict, "os9_perms", obj ? obj : Py_None);
            Py_XDECREF(obj);
        } else {
            PyDict_SetItemString(dict, "os9_perms", Py_None);
        }

        if (LHA_FILE_HAVE_EXTRA(header, LHA_FILE_COMMON_CRC)) {
            PyObject *obj = PyLong_FromUnsignedLong(header->common_crc);
            PyDict_SetItemString(dict, "common_crc", obj ? obj : Py_None);
            Py_XDECREF(obj);
        } else {
            PyDict_SetItemString(dict, "common_crc", Py_None);
        }

        if (LHA_FILE_HAVE_EXTRA(header, LHA_FILE_WINDOWS_TIMESTAMPS)) {
            PyObject *c_obj = PyLong_FromUnsignedLongLong(header->win_creation_time);
            PyObject *m_obj = PyLong_FromUnsignedLongLong(header->win_modification_time);
            PyObject *a_obj = PyLong_FromUnsignedLongLong(header->win_access_time);
            PyDict_SetItemString(dict, "win_creation_time", c_obj ? c_obj : Py_None);
            PyDict_SetItemString(dict, "win_modification_time", m_obj ? m_obj : Py_None);
            PyDict_SetItemString(dict, "win_access_time", a_obj ? a_obj : Py_None);
            Py_XDECREF(c_obj);
            Py_XDECREF(m_obj);
            Py_XDECREF(a_obj);
        } else {
            PyDict_SetItemString(dict, "win_creation_time", Py_None);
            PyDict_SetItemString(dict, "win_modification_time", Py_None);
            PyDict_SetItemString(dict, "win_access_time", Py_None);
        }

        Py_DECREF(raw_bytes);
        Py_DECREF(method);
        Py_DECREF(size_obj);
        Py_DECREF(csize_obj);
        Py_DECREF(ts_obj);
        Py_DECREF(is_dir_obj);
        Py_DECREF(is_symlink_obj);
        Py_DECREF(crc_obj);
        Py_DECREF(header_level_obj);
        Py_DECREF(os_type_obj);
        Py_DECREF(extra_flags_obj);
        Py_DECREF(path_obj);
        Py_DECREF(filename_obj);
        Py_DECREF(symlink_obj);
        Py_DECREF(unix_username_obj);
        Py_DECREF(unix_group_obj);
        Py_DECREF(raw_header_obj);
        Py_DECREF(raw_header_len_obj);

        PyList_Append(list, dict);
        Py_DECREF(dict);
        free(full_path);
    }

    free_reader(reader, stream);
    Py_XDECREF(bytes_owner);
    return list;
}

static void PyLhasaArchive_dealloc(PyLhasaArchive *self) {
    Py_XDECREF(self->entries_cache);
    Py_XDECREF(self->bytes_owner);
    free(self->path);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *PyLhasaArchive_close(PyLhasaArchive *self, PyObject *args) {
    self->closed = 1;
    Py_RETURN_NONE;
}

static PyObject *PyLhasaArchive_entries(PyLhasaArchive *self, PyObject *args) {
    if (self->closed) {
        PyErr_SetString(PylhasaError, "archive is closed");
        return NULL;
    }
    if (self->entries_cache) {
        Py_INCREF(self->entries_cache);
        return self->entries_cache;
    }
    PyObject *list = build_entries(self);
    if (!list) {
        return NULL;
    }
    self->entries_cache = list;
    self->entry_count = (size_t)PyList_GET_SIZE(list);
    Py_INCREF(self->entries_cache);
    return list;
}

static PyObject *PyLhasaArchive_open_entry(PyLhasaArchive *self, PyObject *args) {
    Py_ssize_t index = 0;
    if (!PyArg_ParseTuple(args, "n", &index)) {
        return NULL;
    }
    if (self->closed) {
        PyErr_SetString(PylhasaError, "archive is closed");
        return NULL;
    }
    if (index < 0) {
        PyErr_SetString(BadArchiveError, "entry index out of range");
        return NULL;
    }
    if (!self->entries_cache) {
        PyObject *list = build_entries(self);
        if (!list) {
            return NULL;
        }
        self->entries_cache = list;
        self->entry_count = (size_t)PyList_GET_SIZE(list);
    }
    if ((size_t)index >= self->entry_count) {
        PyErr_SetString(BadArchiveError, "entry index out of range");
        return NULL;
    }

    PyObject *bytes_owner = NULL;
    LHAInputStream *stream = create_input_stream(self, &bytes_owner);
    if (!stream) {
        Py_XDECREF(bytes_owner);
        PyErr_SetString(BadArchiveError, "failed to open archive stream");
        return NULL;
    }
    LHAReader *reader = lha_reader_new(stream);
    if (!reader) {
        Py_XDECREF(bytes_owner);
        lha_input_stream_free(stream);
        PyErr_SetString(BadArchiveError, "failed to initialize reader");
        return NULL;
    }
    lha_reader_set_dir_policy(reader, LHA_READER_DIR_PLAIN);

    size_t current = 0;
    LHAFileHeader *header = NULL;
    while ((header = lha_reader_next_file(reader)) != NULL) {
        if (lha_reader_current_is_fake(reader)) {
            continue;
        }
        if (current == (size_t)index) {
            break;
        }
        current++;
    }

    if (!header || current != (size_t)index) {
        free_reader(reader, stream);
        Py_XDECREF(bytes_owner);
        PyErr_SetString(BadArchiveError, "entry not found");
        return NULL;
    }

    PyLhasaEntryReader *entry_reader = PyObject_New(PyLhasaEntryReader, &PyLhasaEntryReader_Type);
    if (!entry_reader) {
        free_reader(reader, stream);
        Py_XDECREF(bytes_owner);
        return NULL;
    }
    entry_reader->reader = reader;
    entry_reader->stream = stream;
    entry_reader->bytes_owner = bytes_owner;
    entry_reader->closed = 0;
    return (PyObject *)entry_reader;
}

static PyMethodDef PyLhasaArchive_methods[] = {
    {"close", (PyCFunction)PyLhasaArchive_close, METH_NOARGS, "Close the archive"},
    {"entries", (PyCFunction)PyLhasaArchive_entries, METH_NOARGS, "List entry metadata"},
    {"open_entry", (PyCFunction)PyLhasaArchive_open_entry, METH_VARARGS, "Open entry by index"},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject PyLhasaArchive_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_pylhasa.Archive",
    .tp_basicsize = sizeof(PyLhasaArchive),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor)PyLhasaArchive_dealloc,
    .tp_methods = PyLhasaArchive_methods,
};

static void PyLhasaEntryReader_dealloc(PyLhasaEntryReader *self) {
    if (self->reader || self->stream) {
        free_reader(self->reader, self->stream);
    }
    Py_XDECREF(self->bytes_owner);
    Py_TYPE(self)->tp_free((PyObject *)self);
}

static PyObject *PyLhasaEntryReader_read(PyLhasaEntryReader *self, PyObject *args) {
    Py_ssize_t size = -1;
    if (!PyArg_ParseTuple(args, "|n", &size)) {
        return NULL;
    }
    if (self->closed) {
        PyErr_SetString(PylhasaError, "entry reader is closed");
        return NULL;
    }
    if (size < 0) {
        PyObject *ba = PyByteArray_FromStringAndSize(NULL, 0);
        if (!ba) {
            return NULL;
        }
        char buf[65536];
        while (1) {
            size_t got = lha_reader_read(self->reader, buf, sizeof(buf));
            if (got == 0) {
                break;
            }
            Py_ssize_t old_size = PyByteArray_Size(ba);
            if (PyByteArray_Resize(ba, old_size + (Py_ssize_t)got) != 0) {
                Py_DECREF(ba);
                return NULL;
            }
            memcpy(PyByteArray_AsString(ba) + old_size, buf, got);
        }
        PyObject *result = PyBytes_FromStringAndSize(PyByteArray_AsString(ba), PyByteArray_Size(ba));
        Py_DECREF(ba);
        return result;
    }

    if (size == 0) {
        return PyBytes_FromStringAndSize("", 0);
    }

    PyObject *result = PyBytes_FromStringAndSize(NULL, size);
    if (!result) {
        return NULL;
    }
    char *buf = PyBytes_AS_STRING(result);
    size_t got = lha_reader_read(self->reader, buf, (size_t)size);
    if (got == 0) {
        _PyBytes_Resize(&result, 0);
        return result;
    }
    if (got < (size_t)size) {
        _PyBytes_Resize(&result, (Py_ssize_t)got);
    }
    return result;
}

static PyObject *PyLhasaEntryReader_readinto(PyLhasaEntryReader *self, PyObject *args) {
    PyObject *buffer_obj;
    if (!PyArg_ParseTuple(args, "O", &buffer_obj)) {
        return NULL;
    }
    if (self->closed) {
        PyErr_SetString(PylhasaError, "entry reader is closed");
        return NULL;
    }
    Py_buffer view;
    if (PyObject_GetBuffer(buffer_obj, &view, PyBUF_WRITABLE) != 0) {
        return NULL;
    }
    size_t got = lha_reader_read(self->reader, view.buf, view.len);
    PyBuffer_Release(&view);
    return PyLong_FromLong((long)got);
}

static PyObject *PyLhasaEntryReader_close(PyLhasaEntryReader *self, PyObject *args) {
    if (!self->closed) {
        self->closed = 1;
        free_reader(self->reader, self->stream);
        self->reader = NULL;
        self->stream = NULL;
        Py_XDECREF(self->bytes_owner);
        self->bytes_owner = NULL;
    }
    Py_RETURN_NONE;
}

static PyObject *PyLhasaEntryReader_readable(PyLhasaEntryReader *self, PyObject *args) {
    Py_RETURN_TRUE;
}

static PyMethodDef PyLhasaEntryReader_methods[] = {
    {"read", (PyCFunction)PyLhasaEntryReader_read, METH_VARARGS, "Read bytes from entry"},
    {"readinto", (PyCFunction)PyLhasaEntryReader_readinto, METH_VARARGS, "Read into a buffer"},
    {"close", (PyCFunction)PyLhasaEntryReader_close, METH_NOARGS, "Close entry reader"},
    {"readable", (PyCFunction)PyLhasaEntryReader_readable, METH_NOARGS, "Return True if readable"},
    {NULL, NULL, 0, NULL}
};

static PyTypeObject PyLhasaEntryReader_Type = {
    PyVarObject_HEAD_INIT(NULL, 0)
    .tp_name = "_pylhasa.EntryReader",
    .tp_basicsize = sizeof(PyLhasaEntryReader),
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_dealloc = (destructor)PyLhasaEntryReader_dealloc,
    .tp_methods = PyLhasaEntryReader_methods,
};

static PyObject *pylhasa_open_path(PyObject *self, PyObject *args) {
    const char *path;
    if (!PyArg_ParseTuple(args, "s", &path)) {
        return NULL;
    }
    PyLhasaArchive *obj = PyObject_New(PyLhasaArchive, &PyLhasaArchive_Type);
    if (!obj) {
        return NULL;
    }
    obj->backend = BACKEND_PATH;
    obj->path = strdup(path);
    obj->bytes_owner = NULL;
    obj->entries_cache = NULL;
    obj->entry_count = 0;
    obj->closed = 0;
    if (!obj->path) {
        Py_DECREF(obj);
        PyErr_SetString(PyExc_MemoryError, "out of memory");
        return NULL;
    }
    return (PyObject *)obj;
}

static PyObject *pylhasa_open_bytes(PyObject *self, PyObject *args) {
    PyObject *bytes_obj;
    if (!PyArg_ParseTuple(args, "O", &bytes_obj)) {
        return NULL;
    }
    if (!PyBytes_Check(bytes_obj)) {
        PyErr_SetString(PyExc_TypeError, "expected bytes");
        return NULL;
    }
    PyLhasaArchive *obj = PyObject_New(PyLhasaArchive, &PyLhasaArchive_Type);
    if (!obj) {
        return NULL;
    }
    Py_INCREF(bytes_obj);
    obj->backend = BACKEND_BYTES;
    obj->path = NULL;
    obj->bytes_owner = bytes_obj;
    obj->entries_cache = NULL;
    obj->entry_count = 0;
    obj->closed = 0;
    return (PyObject *)obj;
}

static PyMethodDef module_methods[] = {
    {"open_path", (PyCFunction)pylhasa_open_path, METH_VARARGS, "Open an LHA archive from a path"},
    {"open_bytes", (PyCFunction)pylhasa_open_bytes, METH_VARARGS, "Open an LHA archive from bytes"},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    .m_name = "_pylhasa",
    .m_doc = "Low-level LHA archive reader",
    .m_size = -1,
    .m_methods = module_methods,
};

PyMODINIT_FUNC PyInit__pylhasa(void) {
    if (PyType_Ready(&PyLhasaArchive_Type) < 0) {
        return NULL;
    }
    if (PyType_Ready(&PyLhasaEntryReader_Type) < 0) {
        return NULL;
    }

    PyObject *module = PyModule_Create(&moduledef);
    if (!module) {
        return NULL;
    }

    PylhasaError = PyErr_NewException("_pylhasa.PylhasaError", NULL, NULL);
    BadArchiveError = PyErr_NewException("_pylhasa.BadArchiveError", PylhasaError, NULL);
    if (!PylhasaError || !BadArchiveError) {
        Py_DECREF(module);
        return NULL;
    }
    Py_INCREF(PylhasaError);
    Py_INCREF(BadArchiveError);
    PyModule_AddObject(module, "PylhasaError", PylhasaError);
    PyModule_AddObject(module, "BadArchiveError", BadArchiveError);

    Py_INCREF(&PyLhasaArchive_Type);
    PyModule_AddObject(module, "Archive", (PyObject *)&PyLhasaArchive_Type);

    Py_INCREF(&PyLhasaEntryReader_Type);
    PyModule_AddObject(module, "EntryReader", (PyObject *)&PyLhasaEntryReader_Type);

    return module;
}
