use crate::pyo_utils::py_dict_to_json_value_map;
use crate::raw_evaluation_compat_py::{
    raw_dynamic_config_to_py_dict, raw_experiment_to_py_dict, raw_gate_to_py_dict,
    raw_layer_to_py_dict, LayerParamExposureDataPy,
};
use crate::safe_gil::SafeGil;
use crate::statsig_options_py::{safe_convert_to_statsig_options, StatsigOptionsPy};
use crate::statsig_persistent_storage_override_adapter_py::convert_dict_to_user_persisted_values;
use crate::statsig_types_py::{
    BulkEvaluationOptionsPy, InitializeDetailsPy, ParameterStoreEvaluationOptionsPy,
    ParameterStorePy,
};
use crate::{
    statsig_types_py::{
        DynamicConfigEvaluationOptionsPy, ExperimentEvaluationOptionsPy,
        FeatureGateEvaluationOptionsPy, LayerEvaluationOptionsPy,
    },
    statsig_user_py::StatsigUserPy,
};
use parking_lot::Mutex;
use pyo3::{
    call::PyCallArgs,
    prelude::*,
    types::{PyDict, PyModule},
};
use pyo3_stub_gen::derive::*;
use serde_json::Value;
use statsig_rust::interned_string::InternedString;
use statsig_rust::user::StatsigUserInternal;
use statsig_rust::{
    log_e, sdk_event_emitter::SubscriptionID, BulkEvaluationOptions, ClientInitResponseOptions,
    DynamicConfigEvaluationOptions, ExperimentEvaluationOptions, FeatureGateEvaluationOptions,
    HashAlgorithm, LayerEvaluationOptions, ObservabilityClient, ParameterStoreEvaluationOptions,
    Statsig, UserPersistedValues,
};
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;

const TAG: &str = stringify!(StatsigBasePy);

#[gen_stub_pyclass]
#[pyclass(module = "statsig_python_core", subclass)]
pub struct StatsigBasePy {
    inner: Arc<Statsig>,
    observability_client: Mutex<Option<Arc<dyn ObservabilityClient>>>,
}

#[gen_stub_pymethods]
#[pymethods]
impl StatsigBasePy {
    #[new]
    #[pyo3(signature = (sdk_key, options=None))]
    pub fn new(sdk_key: &str, options: Option<StatsigOptionsPy>, py: Python) -> Self {
        let (opts, ob_client) = safe_convert_to_statsig_options(py, options);

        Self {
            inner: Arc::new(Statsig::new(sdk_key, opts.map(Arc::new))),
            observability_client: Mutex::new(ob_client),
        }
    }

    pub fn initialize(&self, py: Python) -> PyResult<Py<PyAny>> {
        let (completion_event, event_clone) = get_completion_event(py)?;

        let inst = self.inner.clone();
        let spawn_result = self.inner.statsig_runtime.spawn(TAG, |_| async move {
            if let Err(e) = inst.initialize().await {
                log_e!(TAG, "Failed to initialize Statsig: {}", e);
            }

            SafeGil::run(|py| {
                let py = match py {
                    Some(py) => py,
                    None => return,
                };

                call_completion_event(&event_clone, py);
            });
        });

        if let Err(e) = spawn_result {
            log_e!(TAG, "Failed to spawn statsig initialize task: {e}");
            call_completion_event(&completion_event, py);
        }

        Ok(completion_event)
    }

    pub fn initialize_with_details(&self, py: Python) -> PyResult<Py<PyAny>> {
        let (future, future_clone) = create_python_future(py)?;

        let inst = self.inner.clone();
        let spawn_result = self.inner.statsig_runtime.spawn(TAG, |_| async move {
            let result = inst.initialize_with_details().await;

            SafeGil::run(|py| {
                let py = match py {
                    Some(py) => py,
                    None => return,
                };

                match result {
                    Ok(details) => {
                        let py_details = InitializeDetailsPy::from(details);
                        call_completion_future(&future_clone, py, (py_details,));
                    }
                    Err(e) => {
                        let error_details = InitializeDetailsPy::from_error(
                            "initialize_failed",
                            Some(e.to_string()),
                        );
                        call_completion_future(&future_clone, py, (error_details,));
                    }
                };
            });
        });

        if let Err(e) = spawn_result {
            log_e!(
                TAG,
                "Failed to spawn statsig initialize with details task: {e}"
            );
            let error_details =
                InitializeDetailsPy::from_error("initialize_failed", Some(e.to_string()));
            call_completion_future(&future, py, (error_details,));
        }

        Ok(future)
    }

    pub fn get_initialize_details(&self) -> PyResult<InitializeDetailsPy> {
        let details = self.inner.get_initialize_details();
        let py_details = InitializeDetailsPy::from(details);
        Ok(py_details)
    }

    pub fn is_initialized(&self) -> bool {
        self.inner.is_initialized()
    }

    pub fn flush_events(&self, py: Python) -> PyResult<Py<PyAny>> {
        let (completion_event, event_clone) = get_completion_event(py)?;

        let inst = self.inner.clone();
        let spawn_result = self.inner.statsig_runtime.spawn(TAG, |_| async move {
            inst.flush_events().await;

            SafeGil::run(|py| {
                let py = match py {
                    Some(py) => py,
                    None => return,
                };

                call_completion_event(&event_clone, py);
            });
        });

        if let Err(e) = spawn_result {
            log_e!(TAG, "Failed to spawn statsig flush events task: {e}");
            call_completion_event(&completion_event, py);
        }

        Ok(completion_event)
    }

    pub fn shutdown(&self, py: Python) -> PyResult<Py<PyAny>> {
        let (completion_event, event_clone) = get_completion_event(py)?;

        let inst = self.inner.clone();
        let obs_client = match self
            .observability_client
            .try_lock_for(Duration::from_secs(5))
        {
            Some(mut lock) => lock.take(),
            None => {
                log_e!(TAG, "Failed to lock observability client");
                None
            }
        };

        let spawn_result = self.inner.statsig_runtime.spawn(TAG, |_| async move {
            if let Err(e) = inst.shutdown().await {
                log_e!(TAG, "Failed to gracefully shutdown StatsigPy: {}", e);
            }

            SafeGil::run(|py| {
                let py = match py {
                    Some(py) => py,
                    None => return,
                };

                call_completion_event(&event_clone, py);
            });

            // held until the shutdown is complete
            drop(obs_client);
        });

        if let Err(e) = spawn_result {
            log_e!(TAG, "Failed to spawn statsig shutdown task: {e}");
            call_completion_event(&completion_event, py);
        }

        Ok(completion_event)
    }

    #[pyo3(name="_INTERNAL_subscribe", signature = (event_name, callback))]
    pub fn _internal_subscribe(&self, event_name: &str, callback: Py<PyAny>) -> String {
        let sub_id = self
            .inner
            .event_emitter
            .subscribe(event_name, move |event| {
                let raw_event = match event.to_raw_json_string() {
                    Some(value) => value,
                    None => return,
                };

                SafeGil::run(|py| {
                    let py = match py {
                        Some(py) => py,
                        None => return,
                    };

                    if let Err(e) = callback.as_ref().call1(py, (raw_event,)) {
                        log_e!(TAG, "Failed to call SDK event callback: {:?}", e);
                    }
                });
            });

        sub_id.encode()
    }

    #[pyo3(name="_INTERNAL_subscribe_internal", signature = (event_name, callback))]
    pub fn _internal_subscribe_internal(&self, event_name: &str, callback: Py<PyAny>) {
        self.inner
            .event_emitter
            .subscribe_internal(event_name, move |event| {
                let raw_event = match event.to_raw_json_string() {
                    Some(value) => value,
                    None => return true,
                };

                SafeGil::run(|py| {
                    let py = match py {
                        Some(py) => py,
                        None => return false,
                    };

                    match callback.as_ref().call1(py, (raw_event,)) {
                        Ok(value) => value.extract::<bool>(py).unwrap_or(true),
                        Err(e) => {
                            log_e!(TAG, "Failed to call internal SDK event callback: {:?}", e);
                            true
                        }
                    }
                })
            });
    }

    #[pyo3(signature = (event_name))]
    pub fn unsubscribe(&self, event_name: &str) {
        self.inner.event_emitter.unsubscribe(event_name);
    }

    #[pyo3(signature = (subscription_id))]
    pub fn unsubscribe_by_id(&self, subscription_id: &str) {
        let sub_id = match SubscriptionID::decode(subscription_id) {
            Some(sub_id) => sub_id,
            None => {
                log_e!(TAG, "Invalid subscription ID: {}", subscription_id);
                return;
            }
        };

        self.inner.event_emitter.unsubscribe_by_id(&sub_id);
    }

    #[pyo3(signature = ())]
    pub fn unsubscribe_all(&self) {
        self.inner.event_emitter.unsubscribe_all();
    }

    #[pyo3(signature = (user, event_name, value=None, metadata=None))]
    pub fn log_event(
        &self,
        user: &StatsigUserPy,
        event_name: &str,
        value: Option<Bound<PyAny>>,
        metadata: Option<Bound<PyDict>>,
    ) -> PyResult<()> {
        let local_metadata = extract_event_metadata(metadata);
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));

        if let Some(num_value) = convert_to_number(value.as_ref()) {
            self.inner
                .log_event_with_number_and_typed_metadata_for_internal_user(
                    &user_internal,
                    event_name,
                    Some(num_value),
                    local_metadata,
                );
        } else {
            self.inner.log_event_with_typed_metadata_for_internal_user(
                &user_internal,
                event_name,
                convert_to_string(value.as_ref()),
                local_metadata,
            );
        }

        Ok(())
    }

    #[pyo3(signature = (user, name, options=None))]
    pub fn check_gate(
        &self,
        user: &StatsigUserPy,
        name: &str,
        options: Option<FeatureGateEvaluationOptionsPy>,
    ) -> bool {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        self.inner.check_gate_with_options_for_internal_user(
            &user_internal,
            name,
            options.map_or(FeatureGateEvaluationOptions::default(), |o| o.into()),
        )
    }

    #[pyo3(name="_INTERNAL_get_feature_gate", signature = (user, name, options=None))]
    pub fn _internal_get_feature_gate(
        &self,
        py: Python,
        user: &StatsigUserPy,
        name: &str,
        options: Option<FeatureGateEvaluationOptionsPy>,
    ) -> PyResult<Py<PyDict>> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        self.inner
            .use_raw_feature_gate_with_options_for_internal_user(
                &user_internal,
                name,
                options.map_or(FeatureGateEvaluationOptions::default(), |o| o.into()),
                |raw| raw_gate_to_py_dict(py, raw),
            )
    }

    #[pyo3(signature = (user, name))]
    pub fn manually_log_gate_exposure(&self, user: &StatsigUserPy, name: &str) -> PyResult<()> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        let interned_name = InternedString::from_str_ref(name);
        self.inner
            .manually_log_gate_exposure_for_internal_user(&user_internal, &interned_name);
        Ok(())
    }

    #[pyo3(name="_INTERNAL_get_dynamic_config", signature = (user, name, options=None))]
    pub fn _internal_get_dynamic_config(
        &self,
        py: Python,
        user: &StatsigUserPy,
        name: &str,
        options: Option<DynamicConfigEvaluationOptionsPy>,
    ) -> PyResult<Py<PyDict>> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        self.inner
            .use_raw_dynamic_config_with_options_for_internal_user(
                &user_internal,
                name,
                options.map_or(DynamicConfigEvaluationOptions::default(), |o| o.into()),
                |raw| raw_dynamic_config_to_py_dict(py, raw),
            )
    }

    #[pyo3(signature = (user, name))]
    pub fn manually_log_dynamic_config_exposure(
        &self,
        user: &StatsigUserPy,
        name: &str,
    ) -> PyResult<()> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        let interned_name = InternedString::from_str_ref(name);
        self.inner
            .manually_log_dynamic_config_exposure_for_internal_user(&user_internal, &interned_name);
        Ok(())
    }

    #[pyo3(name="_INTERNAL_get_experiment", signature = (user, name, options=None, exposure_metadata=None))]
    pub fn _internal_get_experiment(
        &self,
        user: &StatsigUserPy,
        name: &str,
        options: Option<ExperimentEvaluationOptionsPy>,
        exposure_metadata: Option<Bound<PyDict>>,
        py: Python,
    ) -> PyResult<Py<PyDict>> {
        let mut options_actual = options
            .as_ref()
            .map_or(ExperimentEvaluationOptions::default(), |o| o.into());

        options_actual.user_persisted_values = options
            .and_then(|o| o.user_persisted_values)
            .and_then(|v| extract_user_persisted_values(py, name, v));

        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        self.inner
            .use_raw_experiment_with_options_for_internal_user_with_metadata(
                &user_internal,
                name,
                options_actual,
                extract_event_metadata(exposure_metadata),
                |raw| raw_experiment_to_py_dict(py, raw),
            )
    }

    #[pyo3(signature = (user, name))]
    pub fn manually_log_experiment_exposure(
        &self,
        user: &StatsigUserPy,
        name: &str,
    ) -> PyResult<()> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        let interned_name = InternedString::from_str_ref(name);
        self.inner
            .manually_log_experiment_exposure_for_internal_user(&user_internal, &interned_name);
        Ok(())
    }

    #[pyo3(name="_INTERNAL_manually_log_experiment_exposure", signature = (user, name, exposure_metadata=None))]
    pub fn _internal_manually_log_experiment_exposure(
        &self,
        user: &StatsigUserPy,
        name: &str,
        exposure_metadata: Option<Bound<PyDict>>,
    ) -> PyResult<()> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        let interned_name = InternedString::from_str_ref(name);
        self.inner
            .manually_log_experiment_exposure_for_internal_user_with_metadata(
                &user_internal,
                &interned_name,
                extract_event_metadata(exposure_metadata),
            );
        Ok(())
    }

    #[pyo3(name="_INTERNAL_get_layer", signature = (user, name, options=None))]
    pub fn _internal_get_layer(
        &self,
        user: &StatsigUserPy,
        name: &str,
        options: Option<LayerEvaluationOptionsPy>,
        py: Python,
    ) -> PyResult<Py<PyDict>> {
        let mut options_actual = options
            .as_ref()
            .map_or(LayerEvaluationOptions::default(), |o| o.into());

        options_actual.user_persisted_values = options
            .and_then(|o| o.user_persisted_values)
            .and_then(|v| extract_user_persisted_values(py, name, v));

        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        self.inner.use_raw_layer_with_options_for_internal_user(
            &user_internal,
            name,
            options_actual,
            |raw| raw_layer_to_py_dict(py, raw),
        )
    }

    #[pyo3(name="_INTERNAL_log_layer_param_exposure", signature = (raw, param_name, exposure_metadata=None))]
    pub fn _internal_log_layer_param_exposure(
        &self,
        raw: PyRef<LayerParamExposureDataPy>,
        param_name: String,
        exposure_metadata: Option<Bound<PyDict>>,
    ) {
        self.inner
            .log_layer_param_exposure_from_partial_raw_with_metadata(
                raw.inner.clone(),
                param_name,
                extract_event_metadata(exposure_metadata),
            );
    }

    #[pyo3(signature = (user, name, param_name))]
    pub fn manually_log_layer_parameter_exposure(
        &self,
        user: &StatsigUserPy,
        name: &str,
        param_name: String,
    ) -> PyResult<()> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        let interned_name = InternedString::from_str_ref(name);
        self.inner
            .manually_log_layer_parameter_exposure_for_internal_user(
                &user_internal,
                &interned_name,
                InternedString::from_string(param_name),
            );
        Ok(())
    }

    #[pyo3(name="_INTERNAL_manually_log_layer_parameter_exposure", signature = (user, name, param_name, exposure_metadata=None))]
    pub fn _internal_manually_log_layer_parameter_exposure(
        &self,
        user: &StatsigUserPy,
        name: &str,
        param_name: String,
        exposure_metadata: Option<Bound<PyDict>>,
    ) -> PyResult<()> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        let interned_name = InternedString::from_str_ref(name);
        self.inner
            .manually_log_layer_parameter_exposure_for_internal_user_with_metadata(
                &user_internal,
                &interned_name,
                InternedString::from_string(param_name),
                extract_event_metadata(exposure_metadata),
            );
        Ok(())
    }

    #[pyo3(signature = (user, name, options=None))]
    pub fn get_parameter_store(
        &self,
        user: &StatsigUserPy,
        name: &str,
        options: Option<ParameterStoreEvaluationOptionsPy>,
    ) -> ParameterStorePy {
        let options_actual =
            options.map_or(ParameterStoreEvaluationOptions::default(), |o| o.into());
        ParameterStorePy {
            name: name.to_string(),
            inner_statsig: Arc::downgrade(&self.inner),
            user: user.inner.to_public_user(),
            options: options_actual,
        }
    }

    #[pyo3(signature = (user, hash=None, client_sdk_key=None, include_local_overrides=None))]
    pub fn get_client_initialize_response(
        &self,
        user: &StatsigUserPy,
        hash: Option<&str>,
        client_sdk_key: Option<&str>,
        include_local_overrides: Option<bool>,
    ) -> String {
        let mut opts = ClientInitResponseOptions::default();
        if hash == Some("none") {
            opts.hash_algorithm = Some(HashAlgorithm::None);
        }
        if hash == Some("sha256") {
            opts.hash_algorithm = Some(HashAlgorithm::Sha256);
        }
        if let Some(client_sdk_key) = client_sdk_key {
            opts.client_sdk_key = Some(client_sdk_key.to_string());
        }
        opts.include_local_overrides = include_local_overrides;
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        self.inner
            .get_client_init_response_with_options_as_string_for_internal_user(
                &user_internal,
                &opts,
            )
    }

    #[pyo3(signature = (user, options=None))]
    pub fn bulk_evaluate(
        &self,
        py: Python,
        user: &StatsigUserPy,
        options: Option<BulkEvaluationOptionsPy>,
    ) -> PyResult<Py<PyDict>> {
        let options = options.map_or_else(
            || BulkEvaluationOptions {
                include_local_override: true,
                ..BulkEvaluationOptions::default()
            },
            Into::into,
        );
        let resolved = self.inner.resolve_bulk_evaluation_options(options);
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        bulk_evaluate_to_py_dict(py, &self.inner, &user_internal, resolved)
    }

    #[pyo3(signature = (token))]
    pub fn log_delayed_exposure(&self, token: &str) -> bool {
        self.inner.log_delayed_exposure(token)
    }

    #[pyo3(signature = (token, parameter_name))]
    pub fn log_delayed_layer_parameter_exposure(&self, token: &str, parameter_name: &str) -> bool {
        self.inner
            .log_delayed_layer_parameter_exposure(token, parameter_name)
    }

    #[pyo3(signature = (token))]
    pub fn release_delayed_exposure(&self, token: &str) -> bool {
        self.inner.release_delayed_exposure(token)
    }

    #[pyo3(signature = (tokens))]
    pub fn release_delayed_exposures(&self, tokens: Vec<String>) -> usize {
        self.inner.release_delayed_exposures(&tokens)
    }

    #[pyo3(signature = (gate_name, value, id=None))]
    pub fn override_gate(&self, gate_name: &str, value: bool, id: Option<&str>) -> PyResult<()> {
        self.inner.override_gate(gate_name, value, id);
        Ok(())
    }

    #[pyo3(signature = (config_name, value, id=None))]
    pub fn override_dynamic_config(
        &self,
        config_name: &str,
        value: Bound<PyDict>,
        id: Option<&str>,
    ) -> PyResult<()> {
        let value_inner = py_dict_to_json_value_map(&value);
        self.inner
            .override_dynamic_config(config_name, value_inner, id);
        Ok(())
    }

    #[pyo3(signature = (experiment_name, value, id=None))]
    pub fn override_experiment(
        &self,
        experiment_name: &str,
        value: Bound<PyDict>,
        id: Option<&str>,
    ) -> PyResult<()> {
        let value_inner = py_dict_to_json_value_map(&value);
        self.inner
            .override_experiment(experiment_name, value_inner, id);
        Ok(())
    }

    #[pyo3(signature = (layer_name, value, id=None))]
    pub fn override_layer(
        &self,
        layer_name: &str,
        value: Bound<PyDict>,
        id: Option<&str>,
    ) -> PyResult<()> {
        let value_inner = py_dict_to_json_value_map(&value);
        self.inner.override_layer(layer_name, value_inner, id);
        Ok(())
    }

    #[pyo3(signature = (parameter_store_name, value, id=None))]
    pub fn override_parameter_store(
        &self,
        parameter_store_name: &str,
        value: Bound<PyDict>,
        id: Option<&str>,
    ) -> PyResult<()> {
        let value_inner = py_dict_to_json_value_map(&value);
        self.inner
            .override_parameter_store(parameter_store_name, value_inner, id);
        Ok(())
    }

    #[pyo3(signature = (experiment_name, group_name, id=None))]
    pub fn override_experiment_by_group_name(
        &self,
        experiment_name: &str,
        group_name: &str,
        id: Option<&str>,
    ) -> PyResult<()> {
        self.inner
            .override_experiment_by_group_name(experiment_name, group_name, id);
        Ok(())
    }

    #[pyo3(signature = (gate_name, id=None))]
    pub fn remove_gate_override(&self, gate_name: &str, id: Option<&str>) -> PyResult<()> {
        self.inner.remove_gate_override(gate_name, id);
        Ok(())
    }

    #[pyo3(signature = (config_name, id=None))]
    pub fn remove_dynamic_config_override(
        &self,
        config_name: &str,
        id: Option<&str>,
    ) -> PyResult<()> {
        self.inner.remove_dynamic_config_override(config_name, id);
        Ok(())
    }

    #[pyo3(signature = (experiment_name, id=None))]
    pub fn remove_experiment_override(
        &self,
        experiment_name: &str,
        id: Option<&str>,
    ) -> PyResult<()> {
        self.inner.remove_experiment_override(experiment_name, id);
        Ok(())
    }

    #[pyo3(signature = (layer_name, id=None))]
    pub fn remove_layer_override(&self, layer_name: &str, id: Option<&str>) -> PyResult<()> {
        self.inner.remove_layer_override(layer_name, id);
        Ok(())
    }

    #[pyo3(signature = (parameter_store_name, id=None))]
    pub fn remove_parameter_store_override(
        &self,
        parameter_store_name: &str,
        id: Option<&str>,
    ) -> PyResult<()> {
        self.inner
            .remove_parameter_store_override(parameter_store_name, id);
        Ok(())
    }

    #[pyo3(signature = ())]
    pub fn remove_all_overrides(&self) -> PyResult<()> {
        self.inner.remove_all_overrides();
        Ok(())
    }

    #[pyo3(name = "get_feature_gate_list")]
    pub fn get_feature_gate_list(&self) -> Vec<String> {
        self.inner.get_feature_gate_list()
    }

    #[pyo3(name = "get_dynamic_config_list")]
    pub fn get_dynamic_config_list(&self) -> Vec<String> {
        self.inner.get_dynamic_config_list()
    }

    #[pyo3(name = "get_experiment_list")]
    pub fn get_experiment_list(&self) -> Vec<String> {
        self.inner.get_experiment_list()
    }

    #[pyo3(name = "get_parameter_store_list")]
    pub fn get_parameter_store_list(&self) -> Vec<String> {
        self.inner.get_parameter_store_list()
    }

    #[pyo3(signature = (user))]
    pub fn identify(&self, user: &StatsigUserPy) -> PyResult<()> {
        let user_internal = StatsigUserInternal::from_fast_user(&user.inner, Some(&self.inner));
        self.inner.identify_internal_user(&user_internal);
        Ok(())
    }
}

fn get_completion_event(py: Python) -> PyResult<(Py<PyAny>, Py<PyAny>)> {
    let threading = PyModule::import(py, "threading")?;
    let event = threading.call_method0("Event")?;
    let event_clone: Py<PyAny> = event.clone().unbind();

    Ok((event.unbind(), event_clone))
}

fn create_python_future(py: Python) -> PyResult<(Py<PyAny>, Py<PyAny>)> {
    let concurrent = PyModule::import(py, "concurrent.futures")?;
    let future = concurrent.getattr("Future")?.call0()?;
    let future_clone: Py<PyAny> = future.clone().unbind();

    Ok((future.unbind(), future_clone))
}

fn convert_to_number(value: Option<&Bound<PyAny>>) -> Option<f64> {
    let value = value?;

    value.extract::<f64>().ok()
}

fn convert_to_string(value: Option<&Bound<PyAny>>) -> Option<String> {
    let value = value?;

    value.extract::<String>().ok()
}

fn extract_event_metadata(metadata: Option<Bound<PyDict>>) -> Option<HashMap<String, Value>> {
    metadata.map(|m| py_dict_to_json_value_map(&m))
}

fn bulk_evaluate_to_py_dict(
    py: Python,
    statsig: &Statsig,
    user_internal: &StatsigUserInternal<'_, '_>,
    resolved: statsig_rust::ResolvedBulkEvaluationOptions,
) -> PyResult<Py<PyDict>> {
    let result = PyDict::new(py);
    let include_local_override = resolved.include_local_override;

    let gates = PyDict::new(py);
    for name in resolved.feature_gates {
        let (dict, exposure_token) = statsig
            .use_raw_feature_gate_with_delayed_exposure_with_options_for_internal_user(
                user_internal,
                &name,
                include_local_override,
                |raw| raw_gate_to_py_dict(py, raw),
            );
        let dict = dict?;
        set_exposure_token(py, &dict, exposure_token.as_deref())?;
        gates.set_item(name, dict)?;
    }
    result.set_item("feature_gates", gates)?;

    let configs = PyDict::new(py);
    for name in resolved.dynamic_configs {
        let (dict, exposure_token) = statsig
            .use_raw_dynamic_config_with_delayed_exposure_with_options_for_internal_user(
                user_internal,
                &name,
                include_local_override,
                |raw| raw_dynamic_config_to_py_dict(py, raw),
            );
        let dict = dict?;
        set_exposure_token(py, &dict, exposure_token.as_deref())?;
        configs.set_item(name, dict)?;
    }
    result.set_item("dynamic_configs", configs)?;

    let experiments = PyDict::new(py);
    for name in resolved.experiments {
        let options = ExperimentEvaluationOptions::default();
        let (dict, exposure_token) = statsig
            .use_raw_experiment_with_delayed_exposure_with_options_for_internal_user(
                user_internal,
                &name,
                options,
                include_local_override,
                |raw| raw_experiment_to_py_dict(py, raw),
            );
        let dict = dict?;
        set_exposure_token(py, &dict, exposure_token.as_deref())?;
        experiments.set_item(name, dict)?;
    }
    result.set_item("experiments", experiments)?;

    let layers = PyDict::new(py);
    for name in resolved.layers {
        let options = LayerEvaluationOptions::default();
        let (dict, exposure_token) = statsig
            .use_raw_layer_with_delayed_exposure_with_options_for_internal_user(
                user_internal,
                &name,
                options,
                include_local_override,
                |raw| raw_layer_to_py_dict(py, raw),
            );
        let dict = dict?;
        set_exposure_token(py, &dict, exposure_token.as_deref())?;
        layers.set_item(name, dict)?;
    }
    result.set_item("layer_configs", layers)?;

    Ok(result.unbind())
}

fn set_exposure_token(py: Python, dict: &Py<PyDict>, exposure_token: Option<&str>) -> PyResult<()> {
    dict.bind(py).set_item("exposureToken", exposure_token)?;
    Ok(())
}

fn extract_user_persisted_values(
    py: Python,
    spec_name: &str,
    values: Py<PyDict>,
) -> Option<UserPersistedValues> {
    match convert_dict_to_user_persisted_values(py, values, spec_name) {
        Ok(persisted) => Some(persisted),
        Err(e) => {
            log_e!(
                TAG,
                "Failed to convert persisted values from pydict to rust: {} {:?}",
                spec_name,
                e
            );
            None
        }
    }
}

fn call_completion_event(event: &Py<PyAny>, py: Python) {
    if let Err(e) = event.as_ref().call_method0(py, "set") {
        log_e!(TAG, "Failed to set event: {}", e);
    }
}

fn call_completion_future<'py, A>(future: &Py<PyAny>, py: Python<'py>, args: A)
where
    A: PyCallArgs<'py>,
{
    if let Err(e) = future.as_ref().call_method1(py, "set_result", args) {
        log_e!(TAG, "Failed to set future result: {}", e);
    }
}
