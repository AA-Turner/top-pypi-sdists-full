use crate::{statsig_base_py::StatsigBasePy, statsig_user_py::StatsigUserPy};
use pyo3::{exceptions::PyValueError, prelude::*};
use pyo3_stub_gen::derive::gen_stub_pyfunction;
use serde_json::json;
use statsig_rust::user::StatsigUserInternal;

#[gen_stub_pyfunction]
#[pyfunction]
pub fn _evaluate_layer_for_deferred_experiment_exposure(
    sdk: &StatsigBasePy,
    user: &StatsigUserPy,
    layer_name: &str,
) -> PyResult<(String, Option<String>)> {
    let user = StatsigUserInternal::from_fast_user(&user.inner, Some(&sdk.inner));
    let (layer, payload) = sdk
        .inner
        .evaluate_layer_for_deferred_experiment_exposure(&user, layer_name)
        .map_err(|error| PyValueError::new_err(error.to_string()))?;
    let public_layer = json!({
        "value": layer.__value, "ruleID": layer.rule_id, "idType": layer.id_type,
        "groupName": layer.group_name, "allocatedExperimentName": layer.allocated_experiment_name,
        "details": layer.details,
    });
    Ok((public_layer.to_string(), payload))
}
