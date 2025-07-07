use std::fmt::Display;

use base64::{Engine as _, prelude::BASE64_STANDARD};
use pyo3::{Bound, PyAny, PyErr, PyResult, Python, ffi, pyclass, pymethods, types::PyBytes};

use crate::{chacha20::ChaCha20, utils::get_python_buffer};

#[derive(Debug)]
pub enum ChaChaDecryptorError {
    InvalidCommonKey,
    Base64Error(base64::DecodeError),
}

impl Display for ChaChaDecryptorError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ChaChaDecryptorError::InvalidCommonKey => {
                write!(f, "Invalid common key")
            }
            ChaChaDecryptorError::Base64Error(err) => {
                write!(f, "Base64 decoding error: {err}")
            }
        }
    }
}

impl From<ChaChaDecryptorError> for PyErr {
    fn from(err: ChaChaDecryptorError) -> PyErr {
        PyErr::new::<pyo3::exceptions::PyValueError, _>(err.to_string())
    }
}

const CHACHA_KEY: &str = "=";
const CHACHA_KEYS: [&str; 8] = [
    "K9Ca5igncsk",
    "uOVtMpqHxFv",
    "OnQrV02thA",
    "MkdeyU95BJa",
    "SjpNhdKK89V",
    "rl6OrLALPQh",
    "oXafvEwR54",
    "4ZzYokf5I7Z",
];

#[derive(Clone, Debug)]
#[pyclass(frozen)]
pub struct ChaChaDecryptor {
    #[pyo3(get)]
    common_chacha_key_bs: Vec<u8>,
}

#[pymethods]
impl ChaChaDecryptor {
    #[new]
    pub fn new() -> PyResult<Self> {
        let common_key_str = format!(
            "{}{}{}{}{}",
            CHACHA_KEYS[0], CHACHA_KEYS[3], CHACHA_KEYS[5], CHACHA_KEYS[2], CHACHA_KEY
        );

        let common_key = BASE64_STANDARD
            .decode(common_key_str)
            .map_err(ChaChaDecryptorError::Base64Error)?;

        let common_chacha_key_bs =
            Self::key_decrypt_impl(&common_key, "Build/Json/GameplayConfig/");

        Ok(Self {
            common_chacha_key_bs,
        })
    }

    pub fn decrypt<'py>(
        &self,
        py: pyo3::Python<'py>,
        file_bytes: &Bound<'py, PyAny>,
        iv_seed: u64,
    ) -> PyResult<Bound<'py, PyBytes>> {
        let mut buf = get_python_buffer(file_bytes)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let result = PyBytes::new_with(py, encrypted.len(), |data| {
            self.decrypt_impl(encrypted, iv_seed)?;
            data.copy_from_slice(encrypted);
            Ok(())
        });

        Python::with_gil(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }

    #[staticmethod]
    pub fn key_decrypt<'py>(
        py: pyo3::Python<'py>,
        data: &Bound<'py, PyAny>,
        key: &str,
    ) -> PyResult<Bound<'py, PyBytes>> {
        let mut buf = get_python_buffer(data)?;
        let encrypted =
            unsafe { std::slice::from_raw_parts_mut(buf.buf as *mut u8, buf.len as usize) };

        let decrypted_data = Self::key_decrypt_impl(encrypted, key);
        let result = PyBytes::new_with(py, decrypted_data.len(), |data| {
            data.copy_from_slice(&decrypted_data);
            Ok(())
        });

        Python::with_gil(|_| unsafe { ffi::PyBuffer_Release(&mut buf) });
        result
    }
}

impl ChaChaDecryptor {
    fn decrypt_impl(&self, file_bytes: &mut [u8], iv_seed: u64) -> PyResult<()> {
        if self.common_chacha_key_bs.is_empty() {
            return Err(ChaChaDecryptorError::InvalidCommonKey.into());
        }

        let mut nonce = [0u8; 12];
        nonce[0..4].copy_from_slice(&3u32.to_le_bytes());
        nonce[4..12].copy_from_slice(&iv_seed.to_le_bytes());

        let mut cha = ChaCha20::new(&self.common_chacha_key_bs, &nonce, 1)?;
        cha.work_bytes_impl(file_bytes);

        Ok(())
    }

    fn key_decrypt_impl(data: &[u8], key: &str) -> Vec<u8> {
        let u8_key = key.as_bytes();
        let mut decrypted_data = data.to_vec();
        for i in 0..decrypted_data.len() {
            decrypted_data[i] -= u8_key[i % u8_key.len()];
        }
        decrypted_data
    }
}
