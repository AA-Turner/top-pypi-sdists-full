use serde_json::{Map, Value};
use std::fs;
use std::path::PathBuf;

pub async fn bootstrap_from_specs_updated(source: &statsig_rust::Statsig) -> statsig_rust::Statsig {
    use statsig_rust::{
        Statsig, StatsigBootstrapSpecsAdapter, StatsigOptions, sdk_event_emitter::SdkEvent,
    };
    use std::sync::Arc;

    let adapter = Arc::new(StatsigBootstrapSpecsAdapter::new(
        serde_json::to_string(source.specs_snapshot().as_ref()).unwrap(),
    ));
    let replica = Statsig::new(
        "secret-replay",
        Some(Arc::new(StatsigOptions {
            specs_adapter: Some(adapter.clone()),
            disable_network: Some(true),
            disable_all_logging: Some(true),
            ..Default::default()
        })),
    );
    replica.initialize().await.unwrap();
    source.subscribe(SdkEvent::SPECS_UPDATED, move |event| {
        if let SdkEvent::SpecsUpdated { values, .. } = event {
            adapter
                .set_data(serde_json::to_string(values).unwrap())
                .unwrap();
        }
    });
    replica
}

pub fn enforce_array(value: &Value) -> Vec<Value> {
    value.as_array().unwrap().clone()
}

pub fn enforce_object(value: &Value) -> Map<String, Value> {
    value.as_object().unwrap().clone()
}

pub fn enforce_string(value: &Value) -> String {
    value.as_str().unwrap().to_string()
}

pub fn enforce_u64(value: &Value) -> u64 {
    value.as_u64().unwrap()
}

pub fn load_contents(resource_file_name: &str) -> String {
    let mut path = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    path.push(format!("tests/data/{resource_file_name}"));
    fs::read_to_string(path).expect("Unable to read resource file")
}

#[macro_export]
macro_rules! assert_eventually_eq {
    ($actual:expr, $expected:expr) => {
        $crate::assert_eventually_eq!($actual, $expected, std::time::Duration::from_secs(5))
    };

    ($actual:expr, $expected:expr, $timeout:expr) => {
        async {
            let start = std::time::Instant::now();
            let mut actual_value = $actual();
            while start.elapsed().as_millis() < $timeout.as_millis() {
                if actual_value == $expected {
                    return;
                }
                tokio::time::sleep(std::time::Duration::from_millis(10)).await;
                actual_value = $actual();
            }

            if actual_value != $expected {
                panic!("actual {:?} != expected {:?}", actual_value, $expected);
            }
        }
        .await
    };
}

#[macro_export]
macro_rules! assert_eventually {
    ($actual:expr) => {
        $crate::assert_eventually!($actual, std::time::Duration::from_secs(5))
    };

    ($actual:expr, $timeout:expr) => {
        $crate::assert_eventually_eq!($actual, true, $timeout)
    };
}
