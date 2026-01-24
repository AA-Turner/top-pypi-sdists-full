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
    /* Part of this solution was found on SO
    https://stackoverflow.com/questions/5356773/python-get-string-representation-of-pyobject
  */
    PyObject *repr = PyObject_Repr(obj);
    PyObject *str = PyUnicode_AsEncodedString(repr, "utf-8", "~E~");
    const char *bytes = PyBytes_AS_STRING(str);

    fprintf(stderr, msg_fmt, bytes);

    Py_XDECREF(repr);
    Py_XDECREF(str);
}

void log_message_at_level(log_level_t level, const char *msg, ...) {
    PyObject *string_obj = NULL;
    PyObject *result = NULL;
    va_list argptr;

    if (logger == NULL) {
        return;
    }

    va_start(argptr, msg);

    string_obj = PyUnicode_FromFormatV(msg, argptr);

    va_end(argptr);

    if (string_obj == NULL) {
        fprintf(stderr, "Failed to format log message : %s\n", msg ? msg : "");
        return;
    }

    result = PyObject_CallMethod(logger, (char *)log_level_map[level], "O", string_obj);
    if (result == NULL) {
        printf_err("Failed to call log method : %s\n", string_obj);
    }
}
