use std::mem;

use pyo3::{
    PyResult,
    exceptions::PyBufferError,
    ffi::{self, Py_buffer},
};

#[inline(always)]
pub fn get_python_buffer<'py>(obj: &pyo3::Bound<'py, pyo3::types::PyAny>) -> PyResult<Py_buffer> {
    // https://github.com/milesgranger/cramjam/blob/c09d2aea008dcc445bf16f1ee7350e25c50163a8/src/io.rs#L265
    let mut buf = Box::new(mem::MaybeUninit::uninit());
    let rc =
        unsafe { ffi::PyObject_GetBuffer(obj.as_ptr(), buf.as_mut_ptr(), ffi::PyBUF_CONTIG_RO) };
    if rc != 0 {
        return Err(PyBufferError::new_err(
            "Failed to get buffer, is it C contiguous, and shape is not null?",
        ));
    }
    let buf = unsafe { mem::MaybeUninit::<ffi::Py_buffer>::assume_init(*buf) };
    if buf.shape.is_null() {
        return Err(PyBufferError::new_err("shape is null"));
    }
    let is_c_contiguous = unsafe {
        ffi::PyBuffer_IsContiguous(&buf as *const ffi::Py_buffer, b'C' as std::os::raw::c_char) == 1
    };
    if !is_c_contiguous {
        return Err(PyBufferError::new_err("Buffer is not C contiguous"));
    }
    Ok(buf)
}
