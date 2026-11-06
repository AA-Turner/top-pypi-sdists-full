use super::{StatsigOptionsPy, safe_convert_to_statsig_options};
use pyo3::{
    Python,
    types::{PyAnyMethods, PyDict, PyDictMethods},
};

#[test]
fn id_list_init_build_concurrency_reaches_native_options() {
    Python::initialize();
    Python::attach(|py| {
        for input in [
            None,
            Some(1_i64),
            Some(2),
            Some(32),
            Some(33),
            Some(i64::MAX),
        ] {
            let kwargs = PyDict::new(py);
            if let Some(value) = input {
                kwargs
                    .set_item("id_list_init_build_concurrency", value)
                    .unwrap();
            }
            let options = py
                .get_type::<StatsigOptionsPy>()
                .call((), Some(&kwargs))
                .unwrap()
                .extract::<StatsigOptionsPy>()
                .unwrap();
            let (native, _) = safe_convert_to_statsig_options(py, Some(options));
            assert_eq!(
                native.unwrap().id_list_init_build_concurrency,
                input.and_then(|n| i32::try_from(n).ok())
            );
        }
    });
}

#[test]
fn id_list_elias_fano_reaches_native_options() {
    Python::initialize();
    Python::attach(|py| {
        for enabled in [Some(true), Some(false), None] {
            let kwargs = PyDict::new(py);
            if let Some(value) = enabled {
                kwargs.set_item("enable_id_list_elias_fano", value).unwrap();
            }
            let options = py
                .get_type::<StatsigOptionsPy>()
                .call((), Some(&kwargs))
                .unwrap()
                .extract::<StatsigOptionsPy>()
                .unwrap();
            let (native, _) = safe_convert_to_statsig_options(py, Some(options));
            assert_eq!(native.unwrap().enable_id_list_elias_fano, enabled);
        }
    });
}

#[test]
fn id_list_access_metrics_reaches_native_options() {
    Python::initialize();
    Python::attach(|py| {
        for enabled in [Some(true), Some(false), None] {
            let kwargs = PyDict::new(py);
            if let Some(value) = enabled {
                kwargs
                    .set_item("enable_id_list_access_metrics", value)
                    .unwrap();
            }
            let options = py
                .get_type::<StatsigOptionsPy>()
                .call((), Some(&kwargs))
                .unwrap()
                .extract::<StatsigOptionsPy>()
                .unwrap();
            let (native, _) = safe_convert_to_statsig_options(py, Some(options));
            assert_eq!(native.unwrap().enable_id_list_access_metrics, enabled);
        }
    });
}

#[test]
fn python_lookup_wait_options_reach_native_independently() {
    Python::initialize();
    Python::attach(|py| {
        for (country, user_agent) in [(true, false), (false, true)] {
            let kwargs = PyDict::new(py);
            kwargs
                .set_item("wait_for_country_lookup_init", country)
                .unwrap();
            kwargs
                .set_item("wait_for_user_agent_init", user_agent)
                .unwrap();
            let options = py
                .get_type::<StatsigOptionsPy>()
                .call((), Some(&kwargs))
                .unwrap()
                .extract::<StatsigOptionsPy>()
                .unwrap();
            let (native, _) = safe_convert_to_statsig_options(py, Some(options));
            let native = native.unwrap();
            assert_eq!(
                (
                    native.wait_for_country_lookup_init,
                    native.wait_for_user_agent_init
                ),
                (Some(country), Some(user_agent)),
            );
        }
    });
}
