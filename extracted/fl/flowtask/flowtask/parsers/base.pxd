# cython: embedsignature=True
# Copyright (C) 2018-present Jesus Lara
#
cdef class TaskParser:
    cdef public object filename
    cdef public object content
