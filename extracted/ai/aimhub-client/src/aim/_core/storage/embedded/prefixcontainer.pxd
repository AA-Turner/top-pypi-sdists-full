# distutils: language = c++
# cython: language_level = 3
cimport cython

from aim._core.storage.embedded.container cimport Container
from aim._core.storage.embedded.container cimport ContainerItemsIterator
from aim._core.storage.embedded.containertreeview cimport ContainerTreeView

cdef class PrefixContainer(Container):
    cdef public bytes prefix
    # TODO cdef public Container parent after all container bindings are ready
    cdef public parent
    cdef public bint read_only

    cpdef bytes absolute_path(self, bytes path = *)
    cpdef ContainerTreeView tree(self)

cdef class PrefixContainerItemsIterator(ContainerItemsIterator):
    cdef PrefixContainer prefix_container
    cdef bytes begin
    cdef bytes end
    cdef int prefix_len
    cdef ContainerItemsIterator it

    @cython.locals(item=tuple, keys=bytes)
    cpdef object next(self)
    cpdef void seek(self, bytes position)
