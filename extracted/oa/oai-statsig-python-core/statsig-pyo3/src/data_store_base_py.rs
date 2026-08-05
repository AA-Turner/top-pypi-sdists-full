use async_trait::async_trait;
use pyo3::exceptions::PyTypeError;
use pyo3::types::{PyAny, PyAnyMethods, PyBytes, PyDict, PyModule};
use pyo3::{FromPyObject, Py, PyResult, prelude::Bound, pyclass, pymethods};
use pyo3_stub_gen::derive::*;
use statsig_rust::{
    StatsigErr,
    data_store_interface::{
        DataStoreBytesResponse, DataStoreGetBytesRequest, DataStoreResponse, DataStoreTrait,
        RequestPath,
    },
    log_e, log_w,
};

use crate::safe_gil::SafeGil;

const TAG: &str = "DataStoreBasey";

#[gen_stub_pyclass]
#[pyclass(name = "DataStoreBase", module = "statsig_python_core", subclass)]
#[derive(FromPyObject, Default)]
pub struct DataStoreBasePy {
    initialize_fn: Option<Py<PyAny>>,
    shutdown_fn: Option<Py<PyAny>>,
    get_fn: Option<Py<PyAny>>,
    get_bytes_fn: Option<Py<PyAny>>,
    set_fn: Option<Py<PyAny>>,
    set_bytes_fn: Option<Py<PyAny>>,
    support_polling_updates_for_fn: Option<Py<PyAny>>,
}

#[gen_stub_pymethods]
#[pymethods]
impl DataStoreBasePy {
    #[new]
    pub fn new() -> Self {
        Self::default()
    }
}

#[async_trait]
impl DataStoreTrait for DataStoreBasePy {
    async fn initialize(&self) -> Result<(), StatsigErr> {
        SafeGil::run(|py| {
            let py = match py {
                Some(py) => py,
                None => return Ok(()),
            };

            let initialize_fn = match &self.initialize_fn {
                Some(f) => f,
                None => return Ok(()),
            };

            initialize_fn.as_ref().call0(py).map_err(|e| {
                log_e!(TAG, "Failed to call DataStoreBasePy.initialize: {:?}", e);
                StatsigErr::DataStoreFailure("Failed to initialize DataStoreBasePy".to_string())
            })?;

            Ok(())
        })
    }

    async fn shutdown(&self) -> Result<(), StatsigErr> {
        SafeGil::run(|py| {
            let py = match py {
                Some(py) => py,
                None => return Ok(()),
            };

            let shutdown_fn = match &self.shutdown_fn {
                Some(f) => f,
                None => return Ok(()),
            };

            shutdown_fn.as_ref().call0(py).map_err(|e| {
                log_e!(TAG, "Failed to call DataStoreBasePy.shutdown: {:?}", e);
                StatsigErr::DataStoreFailure("Failed to shutdown DataStoreBasePy".to_string())
            })?;

            Ok(())
        })
    }

    async fn get(&self, key: &str) -> Result<DataStoreResponse, StatsigErr> {
        SafeGil::run(|py| {
            let py = match py {
                Some(py) => py,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "Python interpreter has been shutdown".to_string(),
                    ));
                }
            };

            let get_fn = match &self.get_fn {
                Some(f) => f,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "No 'get' function provided".to_string(),
                    ));
                }
            };

            let result = get_fn.as_ref().call(py, (key.to_string(),), None);

            match result {
                Ok(py_obj) => {
                    let py_obj = py_obj.bind(py);
                    // Manual extraction of fields from Python object
                    let result: Option<String> = match py_obj.getattr("result") {
                        Ok(result_attr) => {
                            if result_attr.is_none() {
                                None
                            } else {
                                extract_to_string(&result_attr)
                            }
                        }
                        Err(_) => None,
                    };

                    let time: Option<u64> = match py_obj.getattr("time") {
                        Ok(time_attr) => {
                            if time_attr.is_none() {
                                None
                            } else {
                                match time_attr.extract::<u64>() {
                                    Ok(t) => Some(t),
                                    Err(_) => match time_attr.extract::<i64>() {
                                        Ok(t) if t >= 0 => Some(t as u64),
                                        Ok(_) => None,
                                        Err(_) => None,
                                    },
                                }
                            }
                        }
                        Err(_) => None,
                    };

                    let checksum: Option<String> = match py_obj.getattr("checksum") {
                        Ok(checksum_attr) => {
                            if checksum_attr.is_none() {
                                None
                            } else {
                                checksum_attr.extract::<String>().ok()
                            }
                        }
                        Err(_) => None,
                    };

                    let has_updates: Option<bool> = match py_obj.getattr("has_updates") {
                        Ok(has_updates_attr) => {
                            if has_updates_attr.is_none() {
                                None
                            } else {
                                has_updates_attr.extract::<bool>().ok()
                            }
                        }
                        Err(_) => None,
                    };

                    Ok(DataStoreResponse {
                        result,
                        time,
                        checksum,
                        has_updates,
                    })
                }
                Err(e) => Err(StatsigErr::DataStoreFailure(e.to_string())),
            }
        })
    }

    async fn set(&self, key: &str, value: &str, time: Option<u64>) -> Result<(), StatsigErr> {
        SafeGil::run(|py| {
            let py = match py {
                Some(py) => py,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "Python interpreter has been shutdown".to_string(),
                    ));
                }
            };

            let set_fn = match &self.set_fn {
                Some(f) => f,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "No 'set' function provided".to_string(),
                    ));
                }
            };

            set_fn
                .as_ref()
                .call(py, (String::from(key), String::from(value), time), None)
                .map_err(|e| {
                    log_e!(TAG, "Failed to call DataStoreBasePy.set: {:?}", e);
                    StatsigErr::DataStoreFailure("Failed to set in DataStoreBasePy".to_string())
                })?;

            Ok(())
        })
    }

    async fn get_bytes(
        &self,
        key: &str,
        request: DataStoreGetBytesRequest,
    ) -> Result<DataStoreBytesResponse, StatsigErr> {
        if self.get_bytes_fn.is_none() {
            return Err(StatsigErr::BytesNotImplemented);
        }

        let DataStoreGetBytesRequest {
            since_time,
            checksum,
        } = request;

        let get_bytes_fn = self.get_bytes_fn.as_ref();
        SafeGil::run(|py| {
            let py = match py {
                Some(py) => py,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "Python interpreter has been shutdown".to_string(),
                    ));
                }
            };

            let get_bytes_fn = match get_bytes_fn {
                Some(f) => f,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "No 'get_bytes' function provided".to_string(),
                    ));
                }
            };

            let request_dict = PyDict::new(py);
            request_dict
                .set_item("since_time", since_time)
                .map_err(|e| {
                    log_e!(TAG, "Failed to build get_bytes request dict: {:?}", e);
                    StatsigErr::DataStoreFailure("Failed to build get_bytes request".to_string())
                })?;
            request_dict
                .set_item("checksum", checksum.as_ref())
                .map_err(|e| {
                    log_e!(TAG, "Failed to build get_bytes request dict: {:?}", e);
                    StatsigErr::DataStoreFailure("Failed to build get_bytes request".to_string())
                })?;

            let request_payload = PyModule::import(py, "statsig_python_core.data_store")
                .or_else(|_| PyModule::import(py, "statsig_python_core"))
                .and_then(|module| module.getattr("DataStoreGetBytesRequest"))
                .and_then(|request_type| request_type.call1((since_time, checksum.as_ref())));

            if request_payload.is_err() {
                log_w!(
                    TAG,
                    "Failed to construct DataStoreGetBytesRequest. Falling back to legacy get_bytes signature."
                );
            }

            let result = match request_payload {
                Ok(request_payload) => {
                    get_bytes_fn.call(py, (key.to_string(), request_payload), None)
                }
                Err(_) => match since_time {
                    Some(since_time) => {
                        get_bytes_fn.call(py, (key.to_string(), Some(since_time)), None)
                    }
                    None => get_bytes_fn.call(py, (key.to_string(),), None),
                },
            };

            let result = match result {
                Ok(result) => Ok(result),
                Err(err) => {
                    if err.is_instance_of::<PyTypeError>(py) {
                        match since_time {
                            Some(since_time) => {
                                get_bytes_fn.call(py, (key.to_string(), Some(since_time)), None)
                            }
                            None => get_bytes_fn.call(py, (key.to_string(),), None),
                        }
                    } else {
                        Err(err)
                    }
                }
            };

            match result {
                Ok(py_obj) => {
                    let result_obj = py_obj.bind(py);
                    let result: Option<Vec<u8>> = match result_obj.getattr("result") {
                        Ok(result_attr) => {
                            if result_attr.is_none() {
                                None
                            } else {
                                result_attr.extract::<Vec<u8>>().ok()
                            }
                        }
                        Err(_) => None,
                    };

                    let time: Option<u64> = match result_obj.getattr("time") {
                        Ok(time_attr) => {
                            if time_attr.is_none() {
                                None
                            } else {
                                match time_attr.extract::<u64>() {
                                    Ok(t) => Some(t),
                                    Err(_) => match time_attr.extract::<i64>() {
                                        Ok(t) if t >= 0 => Some(t as u64),
                                        _ => None,
                                    },
                                }
                            }
                        }
                        Err(_) => None,
                    };

                    let checksum: Option<String> = match result_obj.getattr("checksum") {
                        Ok(checksum_attr) => {
                            if checksum_attr.is_none() {
                                None
                            } else {
                                checksum_attr.extract::<String>().ok()
                            }
                        }
                        Err(_) => None,
                    };

                    let has_updates: Option<bool> = match result_obj.getattr("has_updates") {
                        Ok(has_updates_attr) => {
                            if has_updates_attr.is_none() {
                                None
                            } else {
                                has_updates_attr.extract::<bool>().ok()
                            }
                        }
                        Err(_) => None,
                    };

                    Ok(DataStoreBytesResponse {
                        result,
                        time,
                        checksum,
                        has_updates,
                    })
                }
                Err(e) => Err(StatsigErr::DataStoreFailure(e.to_string())),
            }
        })
    }

    async fn set_bytes(
        &self,
        key: &str,
        value: &[u8],
        time: Option<u64>,
        checksum: Option<String>,
    ) -> Result<(), StatsigErr> {
        if self.set_bytes_fn.is_none() {
            return Err(StatsigErr::BytesNotImplemented);
        }

        SafeGil::run(|py| {
            let py = match py {
                Some(py) => py,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "Python interpreter has been shutdown".to_string(),
                    ));
                }
            };

            let set_bytes_fn = match &self.set_bytes_fn {
                Some(f) => f,
                None => {
                    return Err(StatsigErr::DataStoreFailure(
                        "No 'set_bytes' function provided".to_string(),
                    ));
                }
            };

            let key = String::from(key);
            let result: PyResult<Py<PyAny>> = match set_bytes_fn.call(
                py,
                (key.clone(), PyBytes::new(py, value), time, checksum.clone()),
                None,
            ) {
                Ok(result) => Ok(result),
                Err(err) if err.is_instance_of::<PyTypeError>(py) => {
                    set_bytes_fn.call(py, (key, PyBytes::new(py, value), time), None)
                }
                Err(err) => Err(err),
            };

            result.map_err(|e| {
                log_e!(TAG, "Failed to call DataStoreBasePy.set_bytes: {:?}", e);
                StatsigErr::DataStoreFailure("Failed to set_bytes in DataStoreBasePy".to_string())
            })?;

            Ok(())
        })
    }

    async fn support_polling_updates_for(&self, path: RequestPath) -> bool {
        SafeGil::run(|py| {
            let py = match py {
                Some(py) => py,
                None => {
                    return false;
                }
            };

            let support_polling_updates_for_fn = match &self.support_polling_updates_for_fn {
                Some(f) => f,
                None => {
                    return false;
                }
            };

            let result =
                support_polling_updates_for_fn
                    .as_ref()
                    .call(py, (path.to_string(),), None);
            match result {
                Ok(value) => value.extract::<bool>(py).unwrap_or_default(),
                Err(e) => {
                    log_e!(
                        TAG,
                        "Failed to call DataStoreBasePy.support_polling_updates_for: {:?}",
                        e
                    );
                    false
                }
            }
        })
    }
}

fn extract_to_string(result_attr: &Bound<'_, PyAny>) -> Option<String> {
    if let Ok(result) = result_attr.extract::<String>() {
        return Some(result);
    }

    let py = result_attr.py();
    let encoded = PyModule::import(py, "json").ok()?;
    let encoded = encoded.call_method1("dumps", (result_attr,)).ok()?;

    if let Ok(result) = encoded.extract::<String>() {
        return Some(result);
    }

    if let Ok(result_str) = result_attr.str() {
        if let Ok(result) = result_str.extract::<String>() {
            return Some(result);
        }
    }

    None
}
