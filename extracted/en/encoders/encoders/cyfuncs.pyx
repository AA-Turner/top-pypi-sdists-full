from cython cimport nogil, view
from libcpp.map cimport map
from libcpp.string cimport string
from libcpp.unordered_map cimport unordered_map
from libcpp.utility cimport pair
from libcpp.vector cimport vector

from typing import Iterable

import numpy as np

from cpython.ref cimport PyObject

from .pyunicode cimport PyUnicodeSmartPtr


cdef class BytesLabelEncoder:

	cdef map[string, size_t] _labels
	cdef vector[string] _classes

	def __cinit__(self):
		self._labels = map[string, size_t]()
		self._classes = vector[string]()

	def __init__(self):
		pass

	def partial_fit(self, seq):
		cdef string item

		for item in seq:
			self._labels.insert(pair[string, size_t](item, self._labels.size()))

	def fit(self, seq):
		self.partial_fit(seq)

	def transform(self, seq):
		cdef string item
		cdef int i

		cdef size_t[::1] out = view.array(shape=(len(seq), ), itemsize=sizeof(size_t), format="Q")

		for i, item in enumerate(seq):
			out[i] = self._labels.at(item)

		return np.asarray(out)

	def finalize(self):
		cdef pair[string, size_t] item
		with nogil:
			self._classes.resize(self._labels.size())

			for item in self._labels:
				self._classes[item.second] = item.first

	def inverse_transform(self, size_t[::1] seq):
		cdef size_t i, item

		if self._classes.size() == 0 and self._labels.size() > 0:
			self.finalize()

		cdef object[::1] out = view.array(shape=(len(seq), ), itemsize=sizeof(PyObject *), format="O")

		for i, item in enumerate(seq):
			out[i] = self._classes[item]

		return np.asarray(out)

	@property
	def labels(self):
		return self._labels

	@property
	def classes(self):
		return self._classes

	def __getstate__(self):
		return self.labels, self.classes

	def __setstate__(self, state):
		cdef bytes k
		cdef int v
		for k, v in state[0].items():
			self._labels.insert(pair[string, size_t](k, v))

cdef class StringLabelEncoder:

	cdef unordered_map[PyUnicodeSmartPtr, size_t] _labels
	cdef vector[PyUnicodeSmartPtr] _classes

	def __cinit__(self):
		self._labels = unordered_map[PyUnicodeSmartPtr, size_t]()
		self._classes = vector[PyUnicodeSmartPtr]()

	def __init__(self):
		pass

	def partial_fit(self, seq: Iterable[str]) -> None:
		cdef object item

		for item in seq:
			if not isinstance(item, str):
				raise TypeError(f"expected str, {type(item).__name__} found")

			self._labels.insert(pair[PyUnicodeSmartPtr, size_t](PyUnicodeSmartPtr(<PyObject *>item), self._labels.size()))

	def fit(self, seq):
		self.partial_fit(seq)

	def transform(self, seq):
		cdef object item
		cdef int i

		cdef size_t[::1] out = view.array(shape=(len(seq), ), itemsize=sizeof(size_t), format="Q")

		for i, item in enumerate(seq):
			if not isinstance(item, str):
				raise TypeError(f"expected bytes, {type(item)} found")

			out[i] = self._labels.at(PyUnicodeSmartPtr(<PyObject *>item))

		return np.asarray(out)

	def finalize(self):
		cdef pair[PyUnicodeSmartPtr, size_t] item
		with nogil:
			self._classes.resize(self._labels.size())

			for item in self._labels:
				self._classes[item.second] = item.first

	def inverse_transform(self, size_t[::1] seq):
		cdef size_t item
		cdef size_t i

		if self._classes.size() == 0 and self._labels.size() > 0:
			self.finalize()

		cdef object[::1] out = view.array(shape=(len(seq), ), itemsize=sizeof(PyObject *), format="O")

		for i, item in enumerate(seq):
			out[i] = <object>self._classes[item].get()

		return np.asarray(out)

	@property
	def labels(self):
		cdef dict d = dict()
		cdef pair[PyUnicodeSmartPtr, size_t] item

		for item in self._labels:
			d[<object>item.first.get()] = item.second

		return d

	@property
	def classes(self):
		if self._classes.size() == 0:
			return np.array([])

		cdef object[::1] out = view.array(shape=(self._classes.size(), ), itemsize=sizeof(PyObject *), format="O")
		cdef size_t i

		for i in range(self._classes.size()):
			out[i] = <object>self._classes[i].get()

		return np.asarray(out)

	def __getstate__(self):
		return self.labels, self.classes

	def __setstate__(self, state):
		cdef str k
		cdef int v
		for k, v in state[0].items():
			self._labels.insert(pair[PyUnicodeSmartPtr, size_t](PyUnicodeSmartPtr(<PyObject *>k), v))
