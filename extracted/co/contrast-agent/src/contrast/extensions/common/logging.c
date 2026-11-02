/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include <stdarg.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

#include <contrast/assess/logging.h>

#define CONTRAST_MODULE_STR "contrast.extensions"
#define CONTRAST_LOGGER_STR "logger"
#define CONTRAST_LOG_METHOD_STR "log"

static PyObject *logger = NULL;
static const char *log_level_map[] = {
    "info",
    "warning",
    "error",
    "critical",
    "debug",
};

PyObject *initialize_logger(PyObject *self, PyObject *agent_logger) {
    /* Called in the scenario this function is called more than once.
        We decref the previously set logger if there was one set */
    teardown_logger();

    Py_XINCREF(agent_logger);
    logger = agent_logger;

    Py_RETURN_NONE;
}

void teardown_logger() {
    Py_XDECREF(logger);
    logger = NULL;
}

static void printf_err(const char *msg_fmt, PyObject *obj) {
    PyObject *repr = PyObject_Repr(obj);
    PyObject *str =
        repr == NULL ? NULL : PyUnicode_AsEncodedString(repr, "utf-8", "~E~");

    if (str == NULL) {
        PyErr_Clear();
        fprintf(stderr, msg_fmt, "<unrepresentable>");
    } else {
        fprintf(stderr, msg_fmt, PyBytes_AS_STRING(str));
    }

    Py_XDECREF(repr);
    Py_XDECREF(str);
}

/* PyErr_Fetch/PyErr_Restore are deprecated as of Python 3.12 */
typedef struct {
#if PY_MINOR_VERSION < 12
    PyObject *type;
    PyObject *value;
    PyObject *traceback;
#else
    PyObject *exc;
#endif
} saved_exception_t;

static void save_exception(saved_exception_t *saved) {
#if PY_MINOR_VERSION < 12
    PyErr_Fetch(&saved->type, &saved->value, &saved->traceback);
#else
    saved->exc = PyErr_GetRaisedException();
#endif
}

static void restore_exception(saved_exception_t *saved) {
#if PY_MINOR_VERSION < 12
    PyErr_Restore(saved->type, saved->value, saved->traceback);
#else
    PyErr_SetRaisedException(saved->exc);
#endif
}

void log_message_at_level(log_level_t level, const char *msg, ...) {
    PyObject *string_obj = NULL;
    PyObject *result = NULL;
    saved_exception_t saved;
    va_list argptr;

    if (logger == NULL) {
        return;
    }

    /* Callers may log while an exception is set, before returning NULL to propagate
     * it. Calling into Python with an exception set isn't allowed, so set it aside
     * while logging, and restore it afterwards. Any exception raised while logging is
     * cleared, so that logging never changes the caller's error state. */
    save_exception(&saved);

    va_start(argptr, msg);

    string_obj = PyUnicode_FromFormatV(msg, argptr);

    va_end(argptr);

    if (string_obj == NULL) {
        PyErr_Clear();
        fprintf(stderr, "Failed to format log message : %s\n", msg ? msg : "");
        goto cleanup;
    }

    result = PyObject_CallMethod(logger, (char *)log_level_map[level], "O", string_obj);
    if (result == NULL) {
        PyErr_Clear();
        printf_err("Failed to call log method : %s\n", string_obj);
    }

cleanup:
    Py_XDECREF(result);
    Py_XDECREF(string_obj);
    restore_exception(&saved);
}
