/*
 * Copyright © 2026 Contrast Security, Inc.
 * See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
 */
#ifndef _ASSESS_LOGGING_H_
#define _ASSESS_LOGGING_H_
/* Python requires its own header to always be included first */
#define PY_SSIZE_T_CLEAN
#include <Python.h>

typedef enum log_level {
    LOG_INFO = 0,
    LOG_WARNING,
    LOG_ERROR,
    LOG_CRITICAL,
    LOG_DEBUG,
} log_level_t;

#define log_info(...) log_message_at_level(LOG_INFO, __VA_ARGS__)
#define log_warning(...) log_message_at_level(LOG_WARNING, __VA_ARGS__)
#define log_error(...) log_message_at_level(LOG_ERROR, __VA_ARGS__)
#define log_critical(...) log_message_at_level(LOG_CRITICAL, __VA_ARGS__)

/* We want to avoid the performance penalty of log_debug if we don't need it */
#ifdef ASSESS_DEBUG
#define log_debug(...) log_message_at_level(LOG_DEBUG, __VA_ARGS__)
#else
#define log_debug(...) ((void)0)
#endif /* ASSESS_DEBUG */

#define log_exception(exp, ...)         \
    do {                                \
        log_error(__VA_ARGS__);         \
        PyErr_Format(exp, __VA_ARGS__); \
    } while (0);

PyObject *initialize_logger(PyObject *self, PyObject *agent_logger);

void teardown_logger(void);
void log_message_at_level(log_level_t level, const char *msg, ...);

#endif /* _ASSESS_LOGGING_H_ */
