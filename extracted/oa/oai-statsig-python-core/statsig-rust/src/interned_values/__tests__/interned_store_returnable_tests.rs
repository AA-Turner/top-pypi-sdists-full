use std::collections::HashMap;

use rusty_fork::rusty_fork_test;
use wiremock::{
    matchers::{method, path},
    Mock, MockServer, ResponseTemplate,
};

use crate::{
    evaluation::dynamic_returnable::DynamicReturnableValue,
    interned_string::{InternedString, InternedStringValue},
    interned_values::{InternedStore, MmapPreloadOptions},
    DynamicReturnable, StatsigOptions,
};

const EVAL_PROJ_JSON: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.json");
const DEMO_PROJ_PROTO: &[u8] = include_bytes!("../../../tests/data/demo_proj_dcs.pb.br");
const MMAP_ARCHIVED_EQ_SDK_KEY: &str = "interned-store-returnable-mmap-eq";
const MMAP_EAGER_HASH_SDK_KEY: &str = "interned-store-returnable-mmap-eager-hash";
const MMAP_FORK_SDK_KEY: &str = "interned-store-returnable-mmap-fork";

fn fetch_mmap_from_mock_specs(sdk_key: &'static str) {
    tokio::runtime::Runtime::new()
        .unwrap()
        .block_on(async move {
            let server = MockServer::start().await;
            Mock::given(method("GET"))
                .and(path(format!("/v2/download_config_specs/{sdk_key}.json")))
                .respond_with(
                    ResponseTemplate::new(200)
                        .insert_header("content-type", "application/json")
                        .set_body_bytes(EVAL_PROJ_JSON.to_vec()),
                )
                .mount(&server)
                .await;

            let options = StatsigOptions {
                specs_url: Some(format!("{}/v2/download_config_specs", server.uri())),
                ..StatsigOptions::default()
            };

            InternedStore::fetch_and_write_mmap_with_options(sdk_key, Some(&options))
                .await
                .unwrap();
        });
}

#[test]
fn test_interned_returnable_non_preloaded() {
    let bool_res = DynamicReturnable::from_bool(true);
    assert!(matches!(bool_res.value, DynamicReturnableValue::Bool(_)));

    let null_res = DynamicReturnable::empty();
    assert!(matches!(null_res.value, DynamicReturnableValue::Null));

    let json_res = DynamicReturnable::from_map(HashMap::from([(
        "key".to_string(),
        serde_json::Value::String("value".to_string()),
    )]));
    assert!(matches!(
        json_res.value,
        DynamicReturnableValue::JsonPointer(_)
    ));
}

rusty_fork_test! {
    #[test]
    fn test_interned_returnable_preloaded() {
        // test_experiment_no_targeting.rules[1]["returnValue"] -> {"value":"control"}
        assert!(InternedStore::preload(EVAL_PROJ_JSON).is_ok());

        let bool_res = DynamicReturnable::from_bool(true);
        assert!(matches!(bool_res.value, DynamicReturnableValue::Bool(_)));

        let null_res = DynamicReturnable::empty();
        assert!(matches!(null_res.value, DynamicReturnableValue::Null));

        let json_res = DynamicReturnable::from_map(HashMap::from([(
            "value".to_string(),
            serde_json::Value::String("control".to_string()),
        )]));
        assert!(matches!(json_res.value, DynamicReturnableValue::JsonStatic(_)));

        let again = json_res.get_json().unwrap();
        assert_eq!(again, HashMap::from([(
            "value".to_string(),
            serde_json::Value::String("control".to_string()),
        )]));
    }

    #[test]
    fn test_dynamic_returnable_value_eq_pointer_and_static_json_variants() {
        let value = HashMap::from([(
            "value".to_string(),
            serde_json::Value::String("control".to_string()),
        )]);
        let pointer = DynamicReturnable::from_map(value.clone());
        assert!(matches!(pointer.value, DynamicReturnableValue::JsonPointer(_)));
        assert!(pointer.has_inline_stable_hash());
        let pointer_hash = pointer.get_stable_hash();

        assert!(InternedStore::preload(EVAL_PROJ_JSON).is_ok());
        let static_value = DynamicReturnable::from_map(value.clone());
        assert!(matches!(static_value.value, DynamicReturnableValue::JsonStatic(_)));

        assert_eq!(&pointer.value, &static_value.value);
        assert_eq!(pointer_hash, static_value.get_stable_hash());
    }

    #[test]
    fn test_dynamic_returnable_value_eq_pointer_and_archived_json_variants() {
        let value = HashMap::from([(
            "value".to_string(),
            serde_json::Value::String("control".to_string()),
        )]);
        let pointer = DynamicReturnable::from_map(value.clone());
        assert!(matches!(pointer.value, DynamicReturnableValue::JsonPointer(_)));
        let pointer_hash = pointer.get_stable_hash();

        fetch_mmap_from_mock_specs(MMAP_ARCHIVED_EQ_SDK_KEY);
        assert!(InternedStore::preload_mmap(MMAP_ARCHIVED_EQ_SDK_KEY).is_ok());

        let archived = DynamicReturnable::from_map(value);
        assert!(matches!(
            archived.value,
            DynamicReturnableValue::JsonArchived(_)
        ));
        assert!(!archived.has_inline_stable_hash());
        assert_eq!(
            InternedStore::get_mmap_returnable_stable_hash(archived.get_hash()),
            None
        );

        assert_eq!(&pointer.value, &archived.value);
        assert_eq!(pointer, archived);
        assert_eq!(pointer_hash, archived.get_stable_hash());
        assert_eq!(
            serde_json::to_value(&archived).unwrap(),
            serde_json::json!({"value": "control"})
        );
    }

    #[test]
    fn test_mmap_preload_can_precompute_archived_returnable_stable_hashes() {
        let value = HashMap::from([(
            "value".to_string(),
            serde_json::Value::String("control".to_string()),
        )]);
        let pointer = DynamicReturnable::from_map(value.clone());
        let pointer_hash = pointer.get_stable_hash();

        fetch_mmap_from_mock_specs(MMAP_EAGER_HASH_SDK_KEY);
        InternedStore::preload_mmap_with_options(
            MMAP_EAGER_HASH_SDK_KEY,
            &MmapPreloadOptions {
                precompute_returnable_stable_hashes: true,
            },
        )
        .unwrap();

        let archived = DynamicReturnable::from_map(value);
        assert!(matches!(
            archived.value,
            DynamicReturnableValue::JsonArchived(_)
        ));
        assert!(!archived.has_inline_stable_hash());
        assert_eq!(
            InternedStore::get_mmap_returnable_stable_hash(archived.get_hash()),
            Some(pointer_hash)
        );
        assert_eq!(archived.get_stable_hash(), pointer_hash);
    }

    #[test]
    fn test_dynamic_returnable_value_eq_distinguishes_non_matching_variants() {
        let null_value = DynamicReturnable::empty();
        let true_value = DynamicReturnable::from_bool(true);
        let false_value = DynamicReturnable::from_bool(false);
        let json_value = DynamicReturnable::from_map(HashMap::from([(
            "key".to_string(),
            serde_json::Value::String("value".to_string()),
        )]));

        assert_eq!(&null_value.value, &DynamicReturnableValue::Null);
        assert_eq!(&true_value.value, &DynamicReturnableValue::Bool(true));
        assert_ne!(&true_value.value, &false_value.value);
        assert_ne!(&null_value.value, &true_value.value);
        assert_ne!(&null_value.value, &json_value.value);
    }

    #[test]
    fn test_interned_returnable_preloaded_multi_payload_json_and_proto() {
        assert!(InternedStore::preload_multi(&[EVAL_PROJ_JSON, DEMO_PROJ_PROTO]).is_ok());

        let eval_key = InternedString::from_str_ref("test_experiment_no_targeting");
        assert!(matches!(eval_key.value, InternedStringValue::Static(_)));
        assert_eq!(eval_key.as_str(), "test_experiment_no_targeting");

        let proto_key = InternedString::from_str_ref("three_groups");
        assert!(matches!(proto_key.value, InternedStringValue::Static(_)));
        assert_eq!(proto_key.as_str(), "three_groups");
    }

    #[test]
    fn test_interned_returnable_dropped() {
        let returnable = DynamicReturnable::from_map(HashMap::from([(
            "key".to_string(),
            serde_json::Value::String("value".to_string()),
        )]));
        assert_eq!(InternedStore::get_memoized_len().1, 1);

        let returnable2 = DynamicReturnable::from_map(HashMap::from([(
            "key".to_string(),
            serde_json::Value::String("value".to_string()),
        )]));
        assert_eq!(InternedStore::get_memoized_len().1, 1);

        drop(returnable);
        assert_eq!(InternedStore::get_memoized_len().1, 1);

        drop(returnable2);
        assert_eq!(InternedStore::get_memoized_len().1, 0);
    }

    #[test]
    fn test_preloading_mmap_across_forks() {
        fetch_mmap_from_mock_specs(MMAP_FORK_SDK_KEY);

        let pid = unsafe { libc::fork() };
        if pid == 0 {
            let result = InternedStore::preload_mmap(MMAP_FORK_SDK_KEY);
            assert!(result.is_ok());

            let json_res = DynamicReturnable::from_map(HashMap::from([(
                "value".to_string(),
                serde_json::Value::String("control".to_string()),
            )]));
            assert!(matches!(
                json_res.value,
                DynamicReturnableValue::JsonArchived(_)
            ));

            std::process::exit(0);
        }

        unsafe {
            let mut status: i32 = 0;
            libc::waitpid(pid, &mut status, 0);
            assert_eq!(libc::WEXITSTATUS(status), 0);
        };
    }

}
