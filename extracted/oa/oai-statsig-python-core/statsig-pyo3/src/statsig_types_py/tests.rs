use super::ParameterStorePy;
use pyo3::{
    prelude::*,
    types::{PyFloat, PyList},
};
use statsig_rust::{Statsig, StatsigOptions, StatsigUser};
use std::sync::Arc;

#[test]
fn parameter_store_arrays_preserve_configured_and_fallback_numbers() {
    Python::initialize();
    Python::attach(|py| {
        let sdk = Arc::new(Statsig::new(
            "test-key",
            Some(Arc::new(StatsigOptions {
                disable_network: Some(true),
                ..Default::default()
            })),
        ));
        sdk.override_parameter_store(
            "store",
            serde_json::from_value(serde_json::json!({
                "numbers": [1.5, 1.0, u64::MAX, [-2.25]]
            }))
            .unwrap(),
            None,
        );
        let store = Py::new(
            py,
            ParameterStorePy {
                name: "store".into(),
                inner_statsig: Arc::downgrade(&sdk),
                user: StatsigUser::with_user_id("test-user"),
                options: Default::default(),
            },
        )
        .unwrap();
        let expected = py
            .eval(c"[1.5, 1.0, 18446744073709551615, [-2.25]]", None, None)
            .unwrap();

        // Exercise the Python-exposed getter, including conversion of its fallback argument.
        for (name, fallback) in [
            ("numbers", PyList::empty(py).into_any()),
            ("missing", expected.clone()),
        ] {
            let actual = store
                .call_method1(py, "get_array", (name, fallback))
                .unwrap();
            let actual = actual.bind(py);
            assert!(
                actual.eq(&expected).unwrap(),
                "parameter={name}, actual={actual}"
            );
            // Python numeric equality alone would not detect 1.0 becoming an integer.
            assert!(actual.get_item(1).unwrap().is_instance_of::<PyFloat>());
        }
    });
}
