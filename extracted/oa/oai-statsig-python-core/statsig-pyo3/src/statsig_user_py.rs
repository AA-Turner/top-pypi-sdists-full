use crate::{
    pyo_utils::{
        opt_py_dict_ref_to_hashmap, opt_py_dict_ref_to_unit_id_hashmap,
        opt_py_dict_ref_to_user_value_map,
    },
    unit_id_py::UnitIdPy,
    valid_primitives_py::{ValidPrimitivesPy, ValidPrimitivesPyRef},
};
use pyo3::types::PyBytes;
use pyo3::{prelude::*, types::PyDict};
use pyo3_stub_gen::derive::*;
use statsig_rust::user::fast_statsig_user::{FastStatsigUser, FastUserCustomMap, FastUserData};
use statsig_rust::{log_e, log_w, DynamicValue, StatsigUserDataMap, StatsigUserValue};
use std::{collections::HashMap, str};

const TAG: &str = stringify!(StatsigUserPy);

#[gen_stub_pyclass]
#[pyclass(name = "StatsigUser", module = "statsig_python_core")]
pub struct StatsigUserPy {
    pub inner: FastStatsigUser,
}

gen_type_alias_from_python!(
    "statsig_python_core",
    r#"
    import typing
    from typing import TypeAlias

    ValidPrimitives: TypeAlias = builtins.str | builtins.int | builtins.float | builtins.bool
    ValidNestedPrimitives: TypeAlias = ValidPrimitives | typing.List[ValidPrimitives] | typing.Mapping[builtins.str, ValidPrimitives]

    CustomIdsDict: TypeAlias = typing.Mapping[builtins.str, builtins.str | builtins.int | builtins.float]
    EnvironmentDict: TypeAlias = typing.Mapping[builtins.str, builtins.str]
    AttributesDict: TypeAlias = typing.Mapping[builtins.str, ValidNestedPrimitives]
    "#
);

#[gen_stub_pymethods]
#[pymethods]
impl StatsigUserPy {
    #[new]
    #[pyo3(signature = (
        user_id=None,
        email=None,
        ip=None,
        country=None,
        locale=None,
        app_version=None,
        user_agent=None,
        custom=None,
        custom_ids=None,
        private_attributes=None,
        statsig_environment=None
    ))]
    #[allow(clippy::too_many_arguments)]
    pub fn new(
        user_id: Option<&str>,
        email: Option<&str>,
        ip: Option<&str>,
        country: Option<&str>,
        locale: Option<&str>,
        app_version: Option<&str>,
        user_agent: Option<&str>,

        #[gen_stub(override_type(type_repr = "typing.Optional[AttributesDict]"))] //
        custom: Option<&Bound<'_, PyDict>>,

        #[gen_stub(override_type(type_repr = "typing.Optional[CustomIdsDict]"))] //
        custom_ids: Option<&Bound<'_, PyDict>>,

        #[gen_stub(override_type(type_repr = "typing.Optional[AttributesDict]"))] //
        private_attributes: Option<&Bound<'_, PyDict>>,

        #[gen_stub(override_type(type_repr = "typing.Optional[EnvironmentDict]"))] //
        statsig_environment: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<Self> {
        if user_id.is_none() && custom_ids.is_none() {
            log_w!(TAG, "Either `user_id` or `custom_ids` must be provided.");
        }

        let internal_user_id = StatsigUserValue::from(user_id.unwrap_or_default());
        let user_data = FastUserData {
            user_id: Some(internal_user_id),
            email: opt_str_to_user_value(email),
            ip: opt_str_to_user_value(ip),
            country: opt_str_to_user_value(country),
            locale: opt_str_to_user_value(locale),
            app_version: opt_str_to_user_value(app_version),
            user_agent: opt_str_to_user_value(user_agent),
            custom: opt_py_dict_ref_to_user_value_map(custom),
            custom_ids: opt_py_dict_ref_to_unit_id_hashmap(custom_ids),
            private_attributes: opt_py_dict_ref_to_hashmap(private_attributes),
            statsig_environment: opt_py_dict_ref_to_hashmap(statsig_environment),
        };

        let user = FastStatsigUser::new(user_data);
        let instance = Self { inner: user };
        Ok(instance)
    }

    // ---------------------------------------- [UserID]

    #[getter]
    fn get_user_id(&self) -> &str {
        self.inner.get_user_id().unwrap_or_default()
    }

    #[setter]
    fn set_user_id(&mut self, value: Option<String>) {
        self.inner.set_user_id(value.unwrap_or_default());
    }

    // ---------------------------------------- [Email]

    #[getter]
    fn get_email(&self) -> Option<&str> {
        self.inner.get_email()
    }

    #[setter]
    fn set_email(&mut self, value: Option<String>) {
        self.inner.set_email(value);
    }

    // ---------------------------------------- [IP]

    #[getter]
    fn get_ip(&self) -> Option<&str> {
        self.inner.get_ip()
    }

    #[setter]
    fn set_ip(&mut self, value: Option<String>) {
        self.inner.set_ip(value);
    }

    // ---------------------------------------- [Country]

    #[getter]
    fn get_country(&self) -> Option<&str> {
        self.inner.get_country()
    }

    #[setter]
    fn set_country(&mut self, value: Option<String>) {
        self.inner.set_country(value);
    }

    // ---------------------------------------- [Locale]

    #[getter]
    fn get_locale(&self) -> Option<&str> {
        self.inner.get_locale()
    }

    #[setter]
    fn set_locale(&mut self, value: Option<String>) {
        self.inner.set_locale(value);
    }

    // ---------------------------------------- [App Version]

    #[getter]
    fn get_app_version(&self) -> Option<&str> {
        self.inner.get_app_version()
    }

    #[setter]
    fn set_app_version(&mut self, value: Option<String>) {
        self.inner.set_app_version(value);
    }

    // ---------------------------------------- [User Agent]

    #[getter]
    fn get_user_agent(&self) -> Option<&str> {
        self.inner.get_user_agent()
    }

    #[setter]
    fn set_user_agent(&mut self, value: Option<String>) {
        self.inner.set_user_agent(value);
    }

    // ---------------------------------------- [Custom IDs]

    #[getter]
    fn get_custom_ids(&self) -> Option<HashMap<&str, &str>> {
        self.inner.get_custom_ids()
    }

    #[setter]
    fn set_custom_ids(&mut self, value: Option<HashMap<String, UnitIdPy>>) {
        let converted = match value {
            Some(v) => v.into_iter().map(|(k, v)| (k, v.into_unit_id())).collect(),
            None => HashMap::new(),
        };
        self.inner.set_custom_ids(converted);
    }

    // ---------------------------------------- [Custom]

    #[getter]
    fn get_custom(&self) -> Option<HashMap<&str, Option<ValidPrimitivesPyRef<'_>>>> {
        get_custom_map_field_ref(self.inner.get_custom())
    }

    #[setter]
    fn set_custom(&mut self, value: Option<HashMap<String, Option<ValidPrimitivesPy>>>) {
        let mut converted: Option<HashMap<String, StatsigUserValue>> = None;

        if let Some(v) = value {
            converted = Some(
                v.into_iter()
                    .map(|(k, v)| {
                        (
                            k,
                            match v {
                                Some(v) => v.into_user_value(),
                                None => StatsigUserValue::new(),
                            },
                        )
                    })
                    .collect(),
            );
        }

        self.inner.set_custom(converted);
    }

    // ---------------------------------------- [Private Attributes]

    #[getter]
    fn get_private_attributes(&self) -> Option<HashMap<&str, Option<ValidPrimitivesPyRef<'_>>>> {
        get_map_field_ref(self.inner.get_private_attributes())
    }

    #[setter]
    fn set_private_attributes(
        &mut self,
        value: Option<HashMap<String, Option<ValidPrimitivesPy>>>,
    ) {
        let mut converted: Option<HashMap<String, DynamicValue>> = None;

        if let Some(v) = value {
            converted = Some(
                v.into_iter()
                    .map(|(k, v)| {
                        (
                            k,
                            match v {
                                Some(v) => v.into_dynamic_value(),
                                None => DynamicValue::new(),
                            },
                        )
                    })
                    .collect(),
            );
        }

        self.inner.set_private_attributes(converted);
    }

    // ---------------------------------------- [Statsig Environment]

    #[getter]
    fn get_statsig_environment(&self) -> Option<HashMap<&str, &str>> {
        self.inner.get_statsig_environment()
    }

    #[setter]
    fn set_statsig_environment(&mut self, value: Option<HashMap<String, String>>) {
        self.inner.set_statsig_environment(value);
    }

    // ---------------------------------------- [Pickling]

    pub fn __getstate__<'py>(&self, py: Python<'py>) -> PyResult<Bound<'py, PyBytes>> {
        let bytes = match self.inner.to_bytes() {
            Some(bytes) => bytes,
            None => {
                log_e!(TAG, "Failed to serialize StatsigUser.");
                vec![]
            }
        };

        Ok(PyBytes::new(py, &bytes))
    }

    pub fn __setstate__(&mut self, state: Bound<'_, PyBytes>) -> PyResult<()> {
        let bytes = state.as_bytes();
        let user_data = match serde_json::from_slice::<FastUserData>(bytes) {
            Ok(user_data) => user_data,
            Err(e) => {
                log_e!(TAG, "Failed to deserialize StatsigUser: {}", e);
                FastUserData::default()
            }
        };

        let inner = FastStatsigUser::new(user_data);
        *self = StatsigUserPy { inner };
        Ok(())
    }
}

fn get_map_field_ref<'a>(
    value: Option<&'a StatsigUserDataMap>,
) -> Option<HashMap<&'a str, Option<ValidPrimitivesPyRef<'a>>>> {
    let value = value?;
    let mapped: HashMap<&'a str, Option<ValidPrimitivesPyRef<'a>>> = value
        .iter()
        .map(|(k, v)| {
            let value = ValidPrimitivesPyRef::from_dynamic_value(v);
            (k.as_str(), value)
        })
        .collect();

    Some(mapped)
}

fn get_custom_map_field_ref<'a>(
    value: Option<&'a FastUserCustomMap>,
) -> Option<HashMap<&'a str, Option<ValidPrimitivesPyRef<'a>>>> {
    let value = value?;
    let mapped = value
        .iter()
        .map(|(key, value)| (key.as_str(), ValidPrimitivesPyRef::from_user_value(value)))
        .collect();

    Some(mapped)
}

#[allow(clippy::manual_map)] // perf reasons
fn opt_str_to_user_value(value: Option<&str>) -> Option<StatsigUserValue> {
    match value {
        Some(value) => Some(StatsigUserValue::from(value)),
        None => None,
    }
}
