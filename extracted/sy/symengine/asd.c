#define Py_LIMITED_API
#include <Python.h>
#include <stdio.h>

void foo() {
    char* ver = Py_GetVersion();
    printf("Py version: %s", ver);
}

