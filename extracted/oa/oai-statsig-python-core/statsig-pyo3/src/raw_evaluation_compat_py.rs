use std::collections::HashMap;

use pyo3::{
    Bound, Py, PyAny, PyResult, Python, pyclass,
    types::{PyAnyMethods, PyDict, PyDictMethods, PyList, PyListMethods, PyString},
};
use pyo3_stub_gen::derive::gen_stub_pyclass;
use rkyv::{collections::swiss_table::ArchivedHashMap, string::ArchivedString, vec::ArchivedVec};
use statsig_rust::{
    DynamicReturnable, EvaluationDetails,
    evaluation::rkyv_value::{ArchivedRkyvNumber, ArchivedRkyvValue, RkyvNumber, RkyvValue},
    interned_string::InternedString,
    statsig_types_raw::{
        DynamicConfigRaw, ExperimentRaw, FeatureGateRaw, LayerRaw, PartialLayerRaw, SuffixedRuleId,
    },
};

const VALUE_CACHE_KEY_FIELD: &str = "__statsig_dynamic_returnable_cache_key";
const VALUE_CACHE_HIT_FIELD: &str = "__statsig_dynamic_returnable_cache_hit";

#[gen_stub_pyclass]
#[pyclass(name = "LayerParamExposureData", module = "statsig_python_core")]
pub struct LayerParamExposureDataPy {
    pub(crate) inner: PartialLayerRaw,
}

pub(crate) fn raw_gate_to_py_dict(py: Python, raw: &FeatureGateRaw) -> PyResult<Py<PyDict>> {
    let dict = PyDict::new(py);

    dict.set_item(pyo3::intern!(py, "name"), raw.name)?;
    dict.set_item(pyo3::intern!(py, "value"), raw.value)?;

    dict.set_item(
        pyo3::intern!(py, "ruleID"),
        py_intern_rule_id(py, &raw.rule_id),
    )?;
    dict.set_item(
        pyo3::intern!(py, "idType"),
        py_intern_id_type(py, opt_interned_str(&raw.id_type)),
    )?;
    dict.set_item(
        pyo3::intern!(py, "details"),
        evaluation_details_to_py_dict(py, raw.details)?,
    )?;

    Ok(dict.unbind())
}

pub(crate) fn raw_dynamic_config_to_py_dict(
    py: Python,
    raw: &DynamicConfigRaw,
    cache_keys: Option<&Bound<PyAny>>,
    pending_cache: Option<&Bound<PyDict>>,
) -> PyResult<Py<PyDict>> {
    let dict = PyDict::new(py);

    dict.set_item(pyo3::intern!(py, "name"), raw.name)?;

    if let Some(value) = raw.value {
        insert_dynamic_returnable(py, &dict, value, cache_keys, pending_cache)?;
    }

    dict.set_item(
        pyo3::intern!(py, "ruleID"),
        py_intern_rule_id(py, &raw.rule_id),
    )?;
    dict.set_item(
        pyo3::intern!(py, "idType"),
        py_intern_id_type(py, opt_interned_str(&raw.id_type)),
    )?;
    dict.set_item(
        pyo3::intern!(py, "details"),
        evaluation_details_to_py_dict(py, raw.details)?,
    )?;

    Ok(dict.unbind())
}

fn insert_dynamic_returnable(
    py: Python,
    dict: &Bound<PyDict>,
    value: &DynamicReturnable,
    cache_keys: Option<&Bound<PyAny>>,
    pending_cache: Option<&Bound<PyDict>>,
) -> PyResult<()> {
    let cache_key = value.get_hash();
    if has_cached_dynamic_returnable(cache_keys, cache_key)? {
        dict.set_item(pyo3::intern!(py, VALUE_CACHE_KEY_FIELD), cache_key)?;
        dict.set_item(pyo3::intern!(py, VALUE_CACHE_HIT_FIELD), true)?;
        return Ok(());
    }

    if let Some(cached) = get_pending_dynamic_returnable(pending_cache, cache_key)? {
        dict.set_item(pyo3::intern!(py, "value"), cached)?;
        dict.set_item(pyo3::intern!(py, VALUE_CACHE_KEY_FIELD), cache_key)?;
        dict.set_item(pyo3::intern!(py, VALUE_CACHE_HIT_FIELD), true)?;
        return Ok(());
    }

    let converted = if let Some(value) = value.get_json_archived_ref() {
        rkvy_archived_object_to_py_dict(py, value)?
    } else if let Some(value) = value.get_json_pointer_ref() {
        rkyv_object_to_py_dict(py, value)?
    } else {
        return Ok(());
    };

    dict.set_item(pyo3::intern!(py, "value"), &converted)?;
    if cache_keys.is_some() {
        dict.set_item(pyo3::intern!(py, VALUE_CACHE_KEY_FIELD), cache_key)?;
        dict.set_item(pyo3::intern!(py, VALUE_CACHE_HIT_FIELD), false)?;
        if let Some(pending_cache) = pending_cache {
            pending_cache.set_item(cache_key, converted)?;
        }
    }

    Ok(())
}

fn has_cached_dynamic_returnable(
    cache_keys: Option<&Bound<PyAny>>,
    cache_key: u64,
) -> PyResult<bool> {
    let Some(cache_keys) = cache_keys else {
        return Ok(false);
    };
    cache_keys.contains(cache_key)
}

fn get_pending_dynamic_returnable<'py>(
    pending_cache: Option<&Bound<'py, PyDict>>,
    cache_key: u64,
) -> PyResult<Option<Bound<'py, PyDict>>> {
    let Some(pending_cache) = pending_cache else {
        return Ok(None);
    };
    let Some(cached) = pending_cache.get_item(cache_key)? else {
        return Ok(None);
    };
    Ok(cached.cast_into::<PyDict>().ok())
}

pub(crate) fn raw_experiment_to_py_dict(
    py: Python,
    raw: &ExperimentRaw,
    cache_keys: Option<&Bound<PyAny>>,
    pending_cache: Option<&Bound<PyDict>>,
) -> PyResult<Py<PyDict>> {
    let dict = PyDict::new(py);

    dict.set_item(pyo3::intern!(py, "name"), raw.name)?;

    if let Some(value) = raw.value {
        insert_dynamic_returnable(py, &dict, value, cache_keys, pending_cache)?;
    }

    dict.set_item(
        pyo3::intern!(py, "ruleID"),
        py_intern_rule_id(py, &raw.rule_id),
    )?;
    dict.set_item(
        pyo3::intern!(py, "idType"),
        py_intern_id_type(py, opt_interned_str(&raw.id_type)),
    )?;
    dict.set_item(
        pyo3::intern!(py, "details"),
        evaluation_details_to_py_dict(py, raw.details)?,
    )?;
    dict.set_item(
        pyo3::intern!(py, "groupName"),
        opt_interned_str(&raw.group_name),
    )?;
    dict.set_item(
        pyo3::intern!(py, "isExperimentActive"),
        raw.is_experiment_active,
    )?;

    Ok(dict.unbind())
}

pub(crate) fn raw_layer_to_py_dict(
    py: Python,
    raw: &LayerRaw,
    cache_keys: Option<&Bound<PyAny>>,
    pending_cache: Option<&Bound<PyDict>>,
) -> PyResult<Py<PyDict>> {
    let dict = PyDict::new(py);

    dict.set_item(pyo3::intern!(py, "name"), raw.name)?;

    if let Some(value) = raw.value {
        insert_dynamic_returnable(py, &dict, value, cache_keys, pending_cache)?;
    }

    dict.set_item(
        pyo3::intern!(py, "ruleID"),
        py_intern_rule_id(py, &raw.rule_id),
    )?;
    dict.set_item(
        pyo3::intern!(py, "idType"),
        py_intern_id_type(py, opt_interned_str(&raw.id_type)),
    )?;
    dict.set_item(
        pyo3::intern!(py, "details"),
        evaluation_details_to_py_dict(py, raw.details)?,
    )?;
    dict.set_item(
        pyo3::intern!(py, "groupName"),
        opt_interned_str(&raw.group_name),
    )?;
    dict.set_item(
        pyo3::intern!(py, "isExperimentActive"),
        raw.is_experiment_active,
    )?;
    dict.set_item(
        pyo3::intern!(py, "allocatedExperimentName"),
        opt_interned_str(&raw.allocated_experiment_name),
    )?;

    // Exposure state includes the evaluated user and must remain per-call.
    dict.set_item(
        pyo3::intern!(py, "__exposure"),
        Py::new(
            py,
            LayerParamExposureDataPy {
                inner: PartialLayerRaw::from(raw),
            },
        )?,
    )?;

    Ok(dict.unbind())
}

fn evaluation_details_to_py_dict(py: Python, details: &EvaluationDetails) -> PyResult<Py<PyDict>> {
    let raw = PyDict::new(py);
    raw.set_item(
        pyo3::intern!(py, "reason"),
        py_intern_reason(py, &details.reason),
    )?;
    raw.set_item(pyo3::intern!(py, "lcut"), details.lcut)?;
    raw.set_item(pyo3::intern!(py, "received_at"), details.received_at)?;
    raw.set_item(pyo3::intern!(py, "version"), details.version)?;

    Ok(raw.unbind())
}

fn opt_interned_str<'a>(value: &'a Option<&'a InternedString>) -> Option<&'a str> {
    value.as_ref().map(|value| value.as_str())
}

fn py_intern_rule_id<'py>(py: Python<'py>, rule_id: &SuffixedRuleId) -> Bound<'py, PyString> {
    if let Some(rule_id) = rule_id.try_as_unprefixed_str() {
        py_intern_rule_id_value(py, rule_id)
    } else {
        PyString::new(py, &rule_id.unperformant_to_string())
    }
}

fn py_intern_id_type<'py>(py: Python<'py>, value: Option<&str>) -> Option<Bound<'py, PyString>> {
    value.map(|value| match value {
        "userID" => pyo3::intern!(py, "userID").clone(),
        "stableID" => pyo3::intern!(py, "stableID").clone(),
        "ads_segment_id" => pyo3::intern!(py, "ads_segment_id").clone(),
        "workspace_id" => pyo3::intern!(py, "workspace_id").clone(),
        value => PyString::new(py, value),
    })
}

fn py_intern_reason<'py>(py: Python<'py>, value: &str) -> Bound<'py, PyString> {
    match value {
        "Network:Recognized" => pyo3::intern!(py, "Network:Recognized").clone(),
        "Network:Unrecognized" => pyo3::intern!(py, "Network:Unrecognized").clone(),
        "Network:Unsupported" => pyo3::intern!(py, "Network:Unsupported").clone(),
        "Bootstrap:Recognized" => pyo3::intern!(py, "Bootstrap:Recognized").clone(),
        "Adapter(DataStore):Recognized" => {
            pyo3::intern!(py, "Adapter(DataStore):Recognized").clone()
        }
        "LocalOverride:Recognized" => pyo3::intern!(py, "LocalOverride:Recognized").clone(),
        "Uninitialized" => pyo3::intern!(py, "Uninitialized").clone(),
        "NoValues" => pyo3::intern!(py, "NoValues").clone(),
        _ => PyString::new(py, value),
    }
}

fn py_intern_rule_id_value<'py>(py: Python<'py>, value: &str) -> Bound<'py, PyString> {
    if value == "default" {
        pyo3::intern!(py, "default").clone()
    } else {
        PyString::new(py, value)
    }
}

// ------------------------------------------------------------------------------- [ Rkyv(Archived) to Pyo3 ]

fn rkvy_archived_object_to_py_dict(
    py: Python,
    map: &ArchivedHashMap<ArchivedString, ArchivedRkyvValue>,
) -> PyResult<Py<PyDict>> {
    let py_dict = PyDict::new(py);
    for (key, value) in map.iter() {
        py_dict_insert_rkvy_archived_value(py, &py_dict, key.as_str(), value)?;
    }
    Ok(py_dict.unbind())
}

fn py_dict_insert_rkvy_archived_value(
    py: Python,
    py_dict: &Bound<PyDict>,
    key: &str,
    value: &ArchivedRkyvValue,
) -> PyResult<()> {
    match value {
        ArchivedRkyvValue::Null => py_dict.set_item(key, py.None())?,
        ArchivedRkyvValue::Bool(v) => py_dict.set_item(key, v)?,
        ArchivedRkyvValue::Number(v) => py_dict_insert_rkyv_archived_num(py_dict, key, v)?,
        ArchivedRkyvValue::String(v) => py_dict.set_item(key, v.as_str())?,
        ArchivedRkyvValue::Array(v) => {
            py_dict.set_item(key, rkvy_archived_array_to_py_list(py, v)?)?
        }
        ArchivedRkyvValue::Object(v) => {
            py_dict.set_item(key, rkvy_archived_object_to_py_dict(py, v)?)?
        }
    }

    Ok(())
}

fn py_dict_insert_rkyv_archived_num(
    py_dict: &Bound<PyDict>,
    key: &str,
    value: &ArchivedRkyvNumber,
) -> PyResult<()> {
    match value {
        ArchivedRkyvNumber::PosInt(v) => py_dict.set_item(key, v.to_native())?,
        ArchivedRkyvNumber::NegInt(v) => py_dict.set_item(key, v.to_native())?,
        ArchivedRkyvNumber::Float(v) => py_dict.set_item(key, v.to_native())?,
    }
    Ok(())
}

fn rkvy_archived_array_to_py_list(
    py: Python,
    values: &ArchivedVec<ArchivedRkyvValue>,
) -> PyResult<Py<PyAny>> {
    let py_list = PyList::empty(py);
    for value in values.iter() {
        py_list_insert_rkvy_archived_value(py, &py_list, value)?;
    }

    Ok(py_list.unbind().into())
}

fn py_list_insert_rkvy_archived_value(
    py: Python,
    py_list: &Bound<PyList>,
    value: &ArchivedRkyvValue,
) -> PyResult<()> {
    match value {
        ArchivedRkyvValue::Null => py_list.append(py.None())?,
        ArchivedRkyvValue::Bool(v) => py_list.append(v)?,
        ArchivedRkyvValue::Number(v) => py_list_insert_rkyv_archived_num(py_list, v)?,
        ArchivedRkyvValue::String(v) => py_list.append(v.as_str())?,
        ArchivedRkyvValue::Array(v) => py_list.append(rkvy_archived_array_to_py_list(py, v)?)?,
        ArchivedRkyvValue::Object(v) => py_list.append(rkvy_archived_object_to_py_dict(py, v)?)?,
    }
    Ok(())
}

fn py_list_insert_rkyv_archived_num(
    py_list: &Bound<PyList>,
    value: &ArchivedRkyvNumber,
) -> PyResult<()> {
    match value {
        ArchivedRkyvNumber::PosInt(v) => py_list.append(v.to_native())?,
        ArchivedRkyvNumber::NegInt(v) => py_list.append(v.to_native())?,
        ArchivedRkyvNumber::Float(v) => py_list.append(v.to_native())?,
    }
    Ok(())
}

// ------------------------------------------------------------------------------- [ Rkyv to Pyo3 ]

fn rkyv_object_to_py_dict(py: Python, map: &HashMap<String, RkyvValue>) -> PyResult<Py<PyDict>> {
    let py_dict = PyDict::new(py);
    for (key, value) in map {
        py_dict_insert_rkvy_value(py, &py_dict, key, value)?;
    }
    Ok(py_dict.unbind())
}

fn py_dict_insert_rkvy_value(
    py: Python,
    py_dict: &Bound<PyDict>,
    key: &str,
    value: &RkyvValue,
) -> PyResult<()> {
    match value {
        RkyvValue::Null => py_dict.set_item(key, py.None())?,
        RkyvValue::Bool(v) => py_dict.set_item(key, v)?,
        RkyvValue::Number(v) => py_dict_insert_rkyv_num(py_dict, key, v)?,
        RkyvValue::String(v) => py_dict.set_item(key, v)?,
        RkyvValue::Array(v) => py_dict.set_item(key, rkyv_array_to_py_list(py, v)?)?,
        RkyvValue::Object(v) => py_dict.set_item(key, rkyv_object_to_py_dict(py, v)?)?,
    }

    Ok(())
}

fn py_dict_insert_rkyv_num(py_dict: &Bound<PyDict>, key: &str, value: &RkyvNumber) -> PyResult<()> {
    match value {
        RkyvNumber::PosInt(v) => py_dict.set_item(key, v)?,
        RkyvNumber::NegInt(v) => py_dict.set_item(key, v)?,
        RkyvNumber::Float(v) => py_dict.set_item(key, v)?,
    }
    Ok(())
}

fn rkyv_array_to_py_list(py: Python, values: &Vec<RkyvValue>) -> PyResult<Py<PyAny>> {
    let py_list = PyList::empty(py);
    for value in values {
        py_list_insert_rkyv_value(py, &py_list, value)?;
    }
    Ok(py_list.unbind().into())
}

fn py_list_insert_rkyv_value(
    py: Python,
    py_list: &Bound<PyList>,
    value: &RkyvValue,
) -> PyResult<()> {
    match value {
        RkyvValue::Null => py_list.append(py.None())?,
        RkyvValue::Bool(v) => py_list.append(v)?,
        RkyvValue::Number(v) => py_list_insert_rkyv_num(py_list, v)?,
        RkyvValue::String(v) => py_list.append(v)?,
        RkyvValue::Array(v) => py_list.append(rkyv_array_to_py_list(py, v)?)?,
        RkyvValue::Object(v) => py_list.append(rkyv_object_to_py_dict(py, v)?)?,
    }
    Ok(())
}

fn py_list_insert_rkyv_num(py_list: &Bound<PyList>, value: &RkyvNumber) -> PyResult<()> {
    match value {
        RkyvNumber::PosInt(v) => py_list.append(v)?,
        RkyvNumber::NegInt(v) => py_list.append(v)?,
        RkyvNumber::Float(v) => py_list.append(v)?,
    };

    Ok(())
}
