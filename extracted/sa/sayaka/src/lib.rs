mod chacha20;
mod chacha_decryptor;
mod hgmmap;
mod lz4inv;
mod miki;
mod utils;

use pyo3::prelude::*;

#[pymodule]
mod sayaka {
    use pyo3::{ffi, types::PyBytes};

    use crate::lz4inv::decompress_impl;
    use crate::miki::{decrypt_old_to_impl, decrypt_to_impl};
    use crate::utils::get_python_buffer;

    #[pymodule_export]
    use crate::chacha20::ChaCha20;

    #[pymodule_export]
    use crate::hgmmap::ManifestDataBinary;

    #[pymodule_export]
    use crate::chacha_decryptor::ChaChaDecryptor;

    use super::*;

    #[pyfunction]
    fn miki_decrypt_and_decompress<'py>(
        py: pyo3::Python<'py>,
        encrypted: &Bound<'py, PyAny>,
        decompressed_size: usize,
    ) -> PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, decompressed_size, |decompressed| {
            // if encrypted[..32].iter().filter(|&&b| b == 0xa6).count() > 5 {
            //     miki::decrypt_impl(encrypted)?;
            // }
            miki::decrypt_impl(encrypted)?;

            decompress_impl(encrypted, decompressed)?;
            Ok(())
        });

        Python::with_gil(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn miki_decrypt_old_and_decompress<'py>(
        py: pyo3::Python<'py>,
        encrypted: &Bound<'py, PyAny>,
        decompressed_size: usize,
    ) -> PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, decompressed_size, |decompressed| {
            // if encrypted[..32].iter().filter(|&&b| b == 0xB7).count() > 5 {
            //     miki::decrypt_old_impl(encrypted)?;
            // }
            miki::decrypt_old_impl(encrypted)?;

            decompress_impl(encrypted, decompressed)?;
            Ok(())
        });

        Python::with_gil(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn miki_decrypt<'py>(
        py: pyo3::Python<'py>,
        encrypted: &Bound<'py, PyAny>,
    ) -> PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, encrypted.len(), |decrypted| {
            decrypt_to_impl(encrypted, decrypted)?;

            Ok(())
        });

        Python::with_gil(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn miki_decrypt_old<'py>(
        py: pyo3::Python<'py>,
        encrypted: &Bound<'py, PyAny>,
    ) -> PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(encrypted)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, encrypted.len(), |decrypted| {
            decrypt_old_to_impl(encrypted, decrypted)?;

            Ok(())
        });

        Python::with_gil(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[pyfunction]
    fn decompress_buffer<'py>(
        py: pyo3::Python<'py>,
        compressed: &Bound<'py, PyAny>,
        decompressed_size: usize,
    ) -> PyResult<pyo3::Bound<'py, pyo3::types::PyBytes>> {
        let mut buf = get_python_buffer(compressed)?;
        let compressed =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, decompressed_size, |decompressed| {
            decompress_impl(compressed, decompressed)?;
            Ok(())
        });

        Python::with_gil(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }
}
