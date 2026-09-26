use crate::{
    pyo_utils::{opt_py_dict_ref_to_unit_id_hashmap, opt_py_dict_ref_to_user_value_map},
    statsig_user_py::StatsigUserPy,
};
use pyo3::{
    exceptions::{PyRuntimeError, PyValueError},
    prelude::*,
    types::PyDict,
};
use pyo3_stub_gen::derive::*;
use statsig_rust::{
    StatsigUserValue,
    user::{
        fast_statsig_user::FastUserData,
        prepared_user::{PreparedRequestFields, PreparedUser, PreparedUserInput},
        random_user_id::RandomUserId,
    },
};
use std::sync::Arc;

/// An immutable snapshot of targeting metadata, reusable across identities.
/// Per-evaluation custom and custom-ID overlays do not modify the snapshot. This object owns
/// its data and does not retain the source dictionaries or an SDK/config snapshot.
#[gen_stub_pyclass]
#[pyclass(name = "StatsigUserContext", module = "statsig_python_core", frozen)]
pub struct StatsigUserContextPy {
    pub inner: Arc<FastUserData>,
}

/// Immutable policy for fresh cryptographic alphanumeric IDs. A nonempty prefix
/// is followed by '-'. Each evaluation fetches OS entropy; no generated ID or
/// userspace RNG state is retained. This is an evaluation identity, not a secret.
#[gen_stub_pyclass]
#[pyclass(name = "StatsigRandomUserID", module = "statsig_python_core", frozen)]
pub struct StatsigRandomUserIDPy {
    inner: RandomUserId,
}

#[gen_stub_pymethods]
#[pymethods]
impl StatsigRandomUserIDPy {
    #[new]
    fn new(prefix: &str, length: i64) -> PyResult<Self> {
        if !(1..=1024).contains(&length) {
            return Err(PyValueError::new_err(
                "Random ID length must be between 1 and 1024",
            ));
        }
        if prefix.len() > 1024 {
            return Err(PyValueError::new_err(
                "Random ID prefix must be at most 1024 UTF-8 bytes",
            ));
        }
        Ok(Self {
            inner: RandomUserId::new(prefix.to_owned(), length as usize)
                .map_err(PyValueError::new_err)?,
        })
    }
}

#[gen_stub_pymethods]
#[pymethods]
impl StatsigUserContextPy {
    #[new]
    #[pyo3(signature = (*, email=None, ip=None, country=None, locale=None, app_version=None, user_agent=None, custom=None, custom_ids=None, private_attributes=None, statsig_environment=None))]
    #[allow(clippy::too_many_arguments)]
    fn new(
        email: Option<&str>,
        ip: Option<&str>,
        country: Option<&str>,
        locale: Option<&str>,
        app_version: Option<&str>,
        user_agent: Option<&str>,
        #[gen_stub(override_type(type_repr = "typing.Optional[AttributesDict]"))] custom: Option<
            &Bound<'_, PyDict>,
        >,
        #[gen_stub(override_type(type_repr = "typing.Optional[CustomIdsDict]"))] custom_ids: Option<
            &Bound<'_, PyDict>,
        >,
        #[gen_stub(override_type(type_repr = "typing.Optional[AttributesDict]"))]
        private_attributes: Option<&Bound<'_, PyDict>>,
        #[gen_stub(override_type(type_repr = "typing.Optional[EnvironmentDict]"))]
        statsig_environment: Option<&Bound<'_, PyDict>>,
    ) -> PyResult<Self> {
        // Share the constructor's conversion contract, including nested values,
        // numeric custom IDs, nulls, and invalid-value behavior.
        let user = StatsigUserPy::new(
            Some(""),
            email,
            ip,
            country,
            locale,
            app_version,
            user_agent,
            custom,
            custom_ids,
            private_attributes,
            statsig_environment,
        )?;
        Ok(Self {
            inner: user.inner.data,
        })
    }
}

pub(crate) fn prepare_user(
    context: Option<&StatsigUserContextPy>,
    user_id: Option<&str>,
    custom: Option<&Bound<'_, PyDict>>,
) -> PreparedUser {
    PreparedUser::new(
        context.map(|context| context.inner.clone()),
        // StatsigUser(None) has always represented userID as the empty string.
        Some(StatsigUserValue::from(user_id.unwrap_or_default())),
        opt_py_dict_ref_to_user_value_map(custom),
    )
}

#[allow(clippy::too_many_arguments)]
pub(crate) fn prepare_anonymous_user(
    id_options: &StatsigRandomUserIDPy,
    context: Option<&StatsigUserContextPy>,
    custom: Option<&Bound<'_, PyDict>>,
    custom_ids: Option<&Bound<'_, PyDict>>,
    ip: Option<&str>,
    country: Option<&str>,
    locale: Option<&str>,
    user_agent: Option<&str>,
) -> PyResult<PreparedUser> {
    // Convert mutable Python data before any detached evaluation. Standard
    // fields and custom values share the ordinary StatsigUser conversion rules.
    let input = PreparedUserInput {
        user_id: Some(StatsigUserValue::from(
            id_options.inner.generate().map_err(|error| {
                PyRuntimeError::new_err(format!(
                    "Failed to generate random evaluation identity: {error}"
                ))
            })?,
        )),
        custom: opt_py_dict_ref_to_user_value_map(custom),
        custom_ids: opt_py_dict_ref_to_unit_id_hashmap(custom_ids).map(Arc::new),
        request: if ip.is_some() || country.is_some() || locale.is_some() || user_agent.is_some() {
            Some(Arc::new(PreparedRequestFields {
                ip: ip.map(StatsigUserValue::from),
                country: country.map(StatsigUserValue::from),
                locale: locale.map(StatsigUserValue::from),
                user_agent: user_agent.map(StatsigUserValue::from),
            }))
        } else {
            None
        },
    };
    Ok(PreparedUser::with_input(
        context.map(|context| context.inner.clone()),
        input,
    ))
}
