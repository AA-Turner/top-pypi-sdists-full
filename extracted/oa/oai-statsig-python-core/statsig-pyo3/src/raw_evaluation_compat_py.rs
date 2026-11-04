use std::collections::HashMap;

use pyo3::{
    Bound, IntoPyObject, Py, PyAny, PyResult, Python,
    pybacked::PyBackedStr,
    pyclass,
    types::{PyAnyMethods, PyDict, PyDictMethods, PyList, PyListMethods, PyModule, PyString},
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

/// Allocate the SDK's existing Python subclasses without invoking their
/// constructors or building a temporary mutable JSON tree. Keep these handles
/// scoped to one call, avoiding process-global references to interpreter objects.
pub(crate) struct FrozenJsonAllocator<'py> {
    dict_type: Bound<'py, PyAny>,
    list_type: Bound<'py, PyAny>,
    dict_new: Bound<'py, PyAny>,
    list_new: Bound<'py, PyAny>,
}

impl<'py> FrozenJsonAllocator<'py> {
    pub(crate) fn for_call(
        py: Python<'py>,
        requested: bool,
        cache_keys: Option<&Bound<'_, PyAny>>,
    ) -> PyResult<Option<Self>> {
        // EvaluationCache owns conversion, sizing, freezing and sharing when
        // enabled. Preserve that path, including its oversized-value bypass.
        if !requested || cache_keys.is_some() {
            return Ok(None);
        }

        let module = PyModule::import(py, "statsig_python_core._frozen_json")?;
        Ok(Some(Self {
            dict_type: module.getattr("_FrozenDict")?,
            list_type: module.getattr("_FrozenList")?,
            dict_new: py.get_type::<PyDict>().getattr("__new__")?,
            list_new: py.get_type::<PyList>().getattr("__new__")?,
        }))
    }
}

trait JsonContainerAllocator<'py> {
    fn new_dict(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>>;
    fn new_list(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>>;
}

struct MutableJsonAllocator;

impl<'py> JsonContainerAllocator<'py> for MutableJsonAllocator {
    #[inline]
    fn new_dict(&self, py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        Ok(PyDict::new(py))
    }

    #[inline]
    fn new_list(&self, py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        Ok(PyList::empty(py))
    }
}

impl<'py> JsonContainerAllocator<'py> for FrozenJsonAllocator<'py> {
    fn new_dict(&self, _py: Python<'py>) -> PyResult<Bound<'py, PyDict>> {
        Ok(self.dict_new.call1((&self.dict_type,))?.cast_into()?)
    }

    fn new_list(&self, _py: Python<'py>) -> PyResult<Bound<'py, PyList>> {
        Ok(self.list_new.call1((&self.list_type,))?.cast_into()?)
    }
}

#[gen_stub_pyclass]
#[pyclass(name = "LayerParamExposureData", module = "statsig_python_core")]
pub struct LayerParamExposureDataPy {
    pub(crate) inner: PartialLayerRaw,
}

/// Native fields consumed by FeatureGate._from_parts; the Python tuple shape
/// is inferred for generated stubs. Py handles preserve common-string reuse.
pub(crate) type FeatureGatePartsPy = (
    bool,                 // value
    Py<PyString>,         // rule_id
    Option<Py<PyString>>, // id_type
    Py<PyString>,         // reason
    Option<u64>,          // lcut
    Option<u64>,          // received_at
    Option<u32>,          // version
);

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

/// Trusted fields for FeatureGate._from_parts. Keep the existing dict API for
/// callers that consume its wire-shaped representation. The public result uses
/// the original Python name and needs neither an intermediate dict nor a copy.
pub(crate) fn raw_gate_to_py_parts(py: Python, raw: &FeatureGateRaw) -> FeatureGatePartsPy {
    (
        raw.value,
        py_intern_rule_id(py, &raw.rule_id).unbind(),
        py_intern_id_type(py, opt_interned_str(&raw.id_type)).map(Bound::unbind),
        py_intern_reason(py, &raw.details.reason).unbind(),
        raw.details.lcut,
        raw.details.received_at,
        raw.details.version,
    )
}

pub(crate) fn raw_dynamic_config_to_py_dict(
    py: Python,
    raw: &DynamicConfigRaw,
    cache_keys: Option<&Bound<PyAny>>,
    pending_cache: Option<&Bound<PyDict>>,
    frozen_json: Option<&FrozenJsonAllocator<'_>>,
) -> PyResult<Py<PyDict>> {
    let dict = PyDict::new(py);

    dict.set_item(pyo3::intern!(py, "name"), raw.name)?;

    if let Some(value) = raw.value {
        insert_dynamic_returnable(py, &dict, value, cache_keys, pending_cache, frozen_json)?;
    }

    insert_dynamic_config_provenance(py, &dict, raw)?;
    Ok(dict.unbind())
}

/// Project before constructing Python values. The enclosing evaluation callback
/// retains the native spec generation while selected subtrees are converted.
/// No partial value enters the full-returnable evaluation cache.
pub(crate) fn raw_dynamic_config_projection_to_py_dict<'py>(
    py: Python<'py>,
    raw: &DynamicConfigRaw,
    field_names: &[PyBackedStr],
    frozen: Option<&FrozenJsonAllocator<'py>>,
) -> PyResult<Py<PyDict>> {
    let dict = PyDict::new(py);
    dict.set_item(pyo3::intern!(py, "name"), raw.name)?;

    if let Some(allocator) = frozen {
        insert_selected_fields(py, &dict, raw.value, field_names, allocator)?;
    } else {
        insert_selected_fields(py, &dict, raw.value, field_names, &MutableJsonAllocator)?;
    }

    insert_dynamic_config_provenance(py, &dict, raw)?;
    Ok(dict.unbind())
}

fn insert_selected_fields<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    dict: &Bound<PyDict>,
    value: Option<&DynamicReturnable>,
    field_names: &[PyBackedStr],
    allocator: &A,
) -> PyResult<()> {
    let selected = allocator.new_dict(py)?;
    if let Some(map) = value.and_then(DynamicReturnable::get_json_archived_ref) {
        for name in field_names {
            let key = name.as_py_str().bind(py);
            if selected.contains(key)? {
                continue;
            }
            if let Some(value) = map.get(name.as_str()) {
                py_dict_insert_rkvy_archived_value(py, &selected, key, value, allocator)?;
            }
        }
    } else if let Some(map) = value.and_then(DynamicReturnable::get_json_pointer_ref) {
        for name in field_names {
            let key = name.as_py_str().bind(py);
            if selected.contains(key)? {
                continue;
            }
            if let Some(value) = map.get(name.as_str()) {
                py_dict_insert_rkvy_value(py, &selected, key, value, allocator)?;
            }
        }
    }
    dict.set_item(pyo3::intern!(py, "value"), selected)
}

fn insert_dynamic_config_provenance(
    py: Python,
    dict: &Bound<PyDict>,
    raw: &DynamicConfigRaw,
) -> PyResult<()> {
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

    Ok(())
}

fn insert_dynamic_returnable(
    py: Python,
    dict: &Bound<PyDict>,
    value: &DynamicReturnable,
    cache_keys: Option<&Bound<PyAny>>,
    pending_cache: Option<&Bound<PyDict>>,
    frozen_json: Option<&FrozenJsonAllocator<'_>>,
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

    let converted = if let Some(allocator) = frozen_json {
        convert_dynamic_returnable(py, value, allocator)?
    } else {
        convert_dynamic_returnable(py, value, &MutableJsonAllocator)?
    };
    let Some(converted) = converted else {
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

fn convert_dynamic_returnable<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    value: &DynamicReturnable,
    allocator: &A,
) -> PyResult<Option<Py<PyDict>>> {
    if let Some(value) = value.get_json_archived_ref() {
        rkvy_archived_object_to_py_dict(py, value, allocator).map(Some)
    } else if let Some(value) = value.get_json_pointer_ref() {
        rkyv_object_to_py_dict(py, value, allocator).map(Some)
    } else {
        Ok(None)
    }
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
        insert_dynamic_returnable(py, &dict, value, cache_keys, pending_cache, None)?;
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
        insert_dynamic_returnable(py, &dict, value, cache_keys, pending_cache, None)?;
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

fn rkvy_archived_object_to_py_dict<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    map: &ArchivedHashMap<ArchivedString, ArchivedRkyvValue>,
    allocator: &A,
) -> PyResult<Py<PyDict>> {
    let py_dict = allocator.new_dict(py)?;
    for (key, value) in map.iter() {
        py_dict_insert_rkvy_archived_value(py, &py_dict, key.as_str(), value, allocator)?;
    }
    Ok(py_dict.unbind())
}

fn py_dict_insert_rkvy_archived_value<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    py_dict: &Bound<'py, PyDict>,
    key: impl IntoPyObject<'py>,
    value: &ArchivedRkyvValue,
    allocator: &A,
) -> PyResult<()> {
    match value {
        ArchivedRkyvValue::Null => py_dict.set_item(key, py.None())?,
        ArchivedRkyvValue::Bool(v) => py_dict.set_item(key, v)?,
        ArchivedRkyvValue::Number(v) => py_dict_insert_rkyv_archived_num(py_dict, key, v)?,
        ArchivedRkyvValue::String(v) => py_dict.set_item(key, v.as_str())?,
        ArchivedRkyvValue::Array(v) => {
            py_dict.set_item(key, rkvy_archived_array_to_py_list(py, v, allocator)?)?
        }
        ArchivedRkyvValue::Object(v) => {
            py_dict.set_item(key, rkvy_archived_object_to_py_dict(py, v, allocator)?)?
        }
    }

    Ok(())
}

fn py_dict_insert_rkyv_archived_num<'py>(
    py_dict: &Bound<'py, PyDict>,
    key: impl IntoPyObject<'py>,
    value: &ArchivedRkyvNumber,
) -> PyResult<()> {
    match value {
        ArchivedRkyvNumber::PosInt(v) => py_dict.set_item(key, v.to_native())?,
        ArchivedRkyvNumber::NegInt(v) => py_dict.set_item(key, v.to_native())?,
        ArchivedRkyvNumber::Float(v) => py_dict.set_item(key, v.to_native())?,
    }
    Ok(())
}

fn rkvy_archived_array_to_py_list<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    values: &ArchivedVec<ArchivedRkyvValue>,
    allocator: &A,
) -> PyResult<Py<PyAny>> {
    let py_list = allocator.new_list(py)?;
    for value in values.iter() {
        py_list_insert_rkvy_archived_value(py, &py_list, value, allocator)?;
    }

    Ok(py_list.unbind().into())
}

fn py_list_insert_rkvy_archived_value<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    py_list: &Bound<PyList>,
    value: &ArchivedRkyvValue,
    allocator: &A,
) -> PyResult<()> {
    match value {
        ArchivedRkyvValue::Null => py_list.append(py.None())?,
        ArchivedRkyvValue::Bool(v) => py_list.append(v)?,
        ArchivedRkyvValue::Number(v) => py_list_insert_rkyv_archived_num(py_list, v)?,
        ArchivedRkyvValue::String(v) => py_list.append(v.as_str())?,
        ArchivedRkyvValue::Array(v) => {
            py_list.append(rkvy_archived_array_to_py_list(py, v, allocator)?)?
        }
        ArchivedRkyvValue::Object(v) => {
            py_list.append(rkvy_archived_object_to_py_dict(py, v, allocator)?)?
        }
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

fn rkyv_object_to_py_dict<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    map: &HashMap<String, RkyvValue>,
    allocator: &A,
) -> PyResult<Py<PyDict>> {
    let py_dict = allocator.new_dict(py)?;
    for (key, value) in map {
        py_dict_insert_rkvy_value(py, &py_dict, key, value, allocator)?;
    }
    Ok(py_dict.unbind())
}

fn py_dict_insert_rkvy_value<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    py_dict: &Bound<'py, PyDict>,
    key: impl IntoPyObject<'py>,
    value: &RkyvValue,
    allocator: &A,
) -> PyResult<()> {
    match value {
        RkyvValue::Null => py_dict.set_item(key, py.None())?,
        RkyvValue::Bool(v) => py_dict.set_item(key, v)?,
        RkyvValue::Number(v) => py_dict_insert_rkyv_num(py_dict, key, v)?,
        RkyvValue::String(v) => py_dict.set_item(key, v)?,
        RkyvValue::Array(v) => py_dict.set_item(key, rkyv_array_to_py_list(py, v, allocator)?)?,
        RkyvValue::Object(v) => py_dict.set_item(key, rkyv_object_to_py_dict(py, v, allocator)?)?,
    }

    Ok(())
}

fn py_dict_insert_rkyv_num<'py>(
    py_dict: &Bound<'py, PyDict>,
    key: impl IntoPyObject<'py>,
    value: &RkyvNumber,
) -> PyResult<()> {
    match value {
        RkyvNumber::PosInt(v) => py_dict.set_item(key, v)?,
        RkyvNumber::NegInt(v) => py_dict.set_item(key, v)?,
        RkyvNumber::Float(v) => py_dict.set_item(key, v)?,
    }
    Ok(())
}

fn rkyv_array_to_py_list<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    values: &Vec<RkyvValue>,
    allocator: &A,
) -> PyResult<Py<PyAny>> {
    let py_list = allocator.new_list(py)?;
    for value in values {
        py_list_insert_rkyv_value(py, &py_list, value, allocator)?;
    }
    Ok(py_list.unbind().into())
}

fn py_list_insert_rkyv_value<'py, A: JsonContainerAllocator<'py>>(
    py: Python<'py>,
    py_list: &Bound<PyList>,
    value: &RkyvValue,
    allocator: &A,
) -> PyResult<()> {
    match value {
        RkyvValue::Null => py_list.append(py.None())?,
        RkyvValue::Bool(v) => py_list.append(v)?,
        RkyvValue::Number(v) => py_list_insert_rkyv_num(py_list, v)?,
        RkyvValue::String(v) => py_list.append(v)?,
        RkyvValue::Array(v) => py_list.append(rkyv_array_to_py_list(py, v, allocator)?)?,
        RkyvValue::Object(v) => py_list.append(rkyv_object_to_py_dict(py, v, allocator)?)?,
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
