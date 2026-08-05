use brotli::enc::BrotliEncoderParams;
use prost::Message;
use rusty_fork::rusty_fork_test;
use serde_json::json;
use std::{collections::HashMap, io::Write, sync::Arc, time::Instant};

use crate::{
    DynamicReturnable, OverrideAdapter, SpecStore, SpecsSource, SpecsUpdate, StatsigErr,
    StatsigLocalOverrideAdapter, StatsigRuntime, StatsigUser, dyn_value,
    evaluation::{
        comparisons::{
            compare_arrays, compare_numbers, compare_str_with_regex, compare_strings_in_array,
            compare_time, compare_versions,
        },
        dynamic_returnable::DynamicReturnableValue,
        evaluator::{Evaluator, Recognition, SpecType},
        evaluator_context::{EvaluatorContext, IdListResolution},
        evaluator_value::{
            EvaluatorValue, EvaluatorValueInner, EvaluatorValueRef, MemoizedEvaluatorValue,
        },
    },
    hashing::{self, HashUtil},
    interned_string::InternedStringValue,
    interned_values::{
        InternedStore, MmapPreloadOptions,
        interned_store::{
            preload_mmap_v2_for_test, preload_mmap_v2_multi_for_test,
            preload_mmap_v2_multi_with_options_for_test, write_mmap_v2_for_test,
        },
        mmap_data_v2::{
            ArchivedMmapDataV2, MmapDataV2, MmapEvaluatorValue, MmapEvaluatorValueType,
            MmapReturnable, MmapSpec, spec_content_hash,
        },
    },
    networking::ResponseData,
    observability::{
        observability_client_adapter::MetricType,
        ops_stats::{OPS_STATS, OpsStatsEvent, OpsStatsForInstance},
    },
    sdk_event_emitter::SdkEventEmitter,
    specs_response::{
        parse_options::SpecsResponseParseOptions,
        proto_specs::{deserialize_protobuf, deserialize_protobuf_with_options},
        proto_stream_reader::BUFFER_SIZE,
        spec_types::{ConditionOperator, Spec, SpecsResponseFull},
        statsig_config_specs as pb,
    },
    user::{StatsigUserInternal, user_value::UserValueRef},
};

const EVAL_PROJ_JSON: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.json");
const EVAL_PROJ_PROTO: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.pb.br");
const DEMO_PROJ_PROTO: &[u8] = include_bytes!("../../../tests/data/demo_proj_dcs.pb.br");

fn receive_spec_decode_tags(
    receiver: &mut tokio::sync::broadcast::Receiver<OpsStatsEvent>,
) -> HashMap<String, String> {
    loop {
        let event = receiver
            .try_recv()
            .expect("spec decode metric should be emitted synchronously");
        let OpsStatsEvent::Observability(event) = event else {
            continue;
        };
        if event.metric_name == "interned_mmap.spec_decode.count" {
            assert!(matches!(event.metric_type, MetricType::Increment));
            return event.tags.expect("spec decode metric should have tags");
        }
    }
}

fn apply_json_specs(store: &SpecStore, data: Vec<u8>) {
    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(data),
            source: SpecsSource::Network,
            received_at: 2_000,
            source_api: None,
            has_updates: None,
        })
        .unwrap();
}

fn materialized_delta(current: &SpecsResponseFull, lcut: u64) -> ResponseData {
    let serialized = serde_json::to_value(current).unwrap();
    let sum_field_checksums = |field: &str| {
        serialized
            .get(field)
            .and_then(serde_json::Value::as_object)
            .into_iter()
            .flatten()
            .fold(0u64, |sum, (_, value)| {
                let checksum = value
                    .get("checksum")
                    .and_then(serde_json::Value::as_str)
                    .and_then(|checksum| checksum.parse::<u32>().ok())
                    .unwrap_or_default();
                sum.wrapping_add(checksum as u64)
            })
    };
    let field_checksums = [
        "condition_map",
        "dynamic_configs",
        "feature_gates",
        "layer_configs",
        "param_stores",
    ]
    .into_iter()
    .map(|field| (field.to_string(), sum_field_checksums(field)))
    .collect();

    let mut common_fields = serialized;
    let fields = common_fields.as_object_mut().unwrap();
    for field in [
        "checksum",
        "company_id",
        "condition_map",
        "dynamic_configs",
        "feature_gates",
        "has_updates",
        "layer_configs",
        "param_stores",
        "response_format",
        "time",
    ] {
        fields.remove(field);
    }
    fields.insert(
        "default_environment".to_string(),
        json!("delta-environment"),
    );

    let envelopes = [
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(
                pb::SpecsTopLevel {
                    has_updates: true,
                    time: lcut,
                    company_id: current.company_id.clone().unwrap_or_default(),
                    response_format: current.response_format.clone().unwrap_or_default(),
                    checksum: "spec-decode-mmap-delta".to_string(),
                    rest: serde_json::to_vec(&common_fields).unwrap(),
                    may_have_remote_config_metadata: None,
                }
                .encode_to_vec(),
            ),
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Checksums as i32,
            data: Some(pb::RulesetsChecksums { field_checksums }.encode_to_vec()),
            ..pb::SpecsEnvelope::default()
        },
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Done as i32,
            ..pb::SpecsEnvelope::default()
        },
    ];
    let mut encoded = Vec::new();
    for envelope in envelopes {
        envelope.encode_length_delimited(&mut encoded).unwrap();
    }

    let mut compressed = Vec::new();
    {
        let mut writer = brotli::CompressorWriter::with_params(
            &mut compressed,
            BUFFER_SIZE,
            &BrotliEncoderParams::default(),
        );
        writer.write_all(&encoded).unwrap();
        writer.flush().unwrap();
    }

    ResponseData::from_bytes_with_headers(
        compressed,
        Some(HashMap::from([
            (
                "content-type".to_string(),
                "application/octet-stream".to_string(),
            ),
            ("content-encoding".to_string(), "statsig-br".to_string()),
            ("x-deltas-used".to_string(), "true".to_string()),
        ])),
    )
}

fn multi_sdk_payload(checksum: &str, salt: &str, enabled: bool) -> Vec<u8> {
    serde_json::to_vec(&json!({
        "experiment_to_layer": {},
        "condition_map": {},
        "dynamic_configs": {
            "project_config": {
                "checksum": format!("config-{checksum}"),
                "type": "dynamic_config",
                "salt": format!("config-{salt}"),
                "defaultValue": {"project": salt},
                "enabled": true,
                "rules": [],
                "idType": "userID",
                "entity": "dynamic_config"
            }
        },
        "feature_gates": {
            "shared_gate": {
                "checksum": checksum,
                "type": "feature_gate",
                "salt": salt,
                "defaultValue": false,
                "enabled": enabled,
                "rules": [],
                "idType": "userID",
                "entity": "feature_gate"
            }
        },
        "layer_configs": {},
        "has_updates": true,
        "time": 1
    }))
    .unwrap()
}

fn test_spec_store(sdk_key: &str) -> SpecStore {
    SpecStore::new(
        sdk_key,
        sdk_key.to_string(),
        StatsigRuntime::get_runtime(),
        Arc::new(SdkEventEmitter::default()),
        None,
    )
}

fn apply_payload(store: &SpecStore, payload: Vec<u8>) {
    store
        .set_values(SpecsUpdate {
            data: ResponseData::from_bytes(payload),
            source: SpecsSource::Network,
            received_at: 2_000,
            source_api: Some("multi-sdk-test".to_string()),
            has_updates: None,
        })
        .unwrap();
}

rusty_fork_test! {
    #[test]
    fn v2_spec_decode_metric_reports_mmap_delta_and_mixed_roots() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-spec-decode-metric.mmap");
        let sdk_key = "secret-mmap-metric-test";
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_multi_for_test(&[(sdk_key, &path)]).unwrap();

        let ops_stats = OPS_STATS.get_for_instance(sdk_key);
        let mut receiver = ops_stats.subscribe_for_test();
        let store = SpecStore::new(
            sdk_key,
            sdk_key.to_string(),
            StatsigRuntime::get_runtime(),
            Arc::new(SdkEventEmitter::default()),
            None,
        );

        apply_json_specs(&store, EVAL_PROJ_JSON.to_vec());
        let tags = receive_spec_decode_tags(&mut receiver);
        assert_eq!(tags.get("source").map(String::as_str), Some("mmap"));
        assert_eq!(tags.get("reason").map(String::as_str), Some("preloaded"));

        let current = store.load_data();
        store
            .set_values(SpecsUpdate {
                data: materialized_delta(current.snapshot.as_ref(), current.lcut() + 1),
                source: SpecsSource::Network,
                received_at: 2_001,
                source_api: None,
                has_updates: None,
            })
            .unwrap();
        let tags = receive_spec_decode_tags(&mut receiver);
        assert_eq!(tags.get("source").map(String::as_str), Some("mmap"));
        assert_eq!(tags.get("reason").map(String::as_str), Some("preloaded"));

        let mut mixed: serde_json::Value = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        let gate = mixed["feature_gates"]
            .as_object_mut()
            .and_then(|gates| gates.values_mut().next())
            .expect("fixture should contain a feature gate");
        gate["checksum"] = json!("spec-decode-mismatch");
        mixed["checksum"] = json!("spec-decode-mixed-response");
        mixed["time"] = json!(mixed["time"].as_u64().unwrap_or_default() + 2);

        apply_json_specs(&store, serde_json::to_vec(&mixed).unwrap());
        let tags = receive_spec_decode_tags(&mut receiver);
        assert_eq!(tags.get("source").map(String::as_str), Some("mixed"));
        assert_eq!(
            tags.get("reason").map(String::as_str),
            Some("partial_match")
        );
    }

    #[test]
    fn multi_sdk_keys_scope_specs_share_leaves_and_preserve_owned_fallback() {
        let directory = tempfile::tempdir().unwrap();
        let path_a = directory.path().join("interned-store-multi-a.mmap");
        let path_b = directory.path().join("interned-store-multi-b.mmap");
        let payload_a = multi_sdk_payload("checksum-a", "salt-a", true);
        let payload_b = multi_sdk_payload("checksum-b", "salt-b", false);

        write_mmap_v2_for_test(&payload_a, &path_a).unwrap();
        write_mmap_v2_for_test(&payload_b, &path_b).unwrap();
        let project_b_value = HashMap::from([(
            "project".to_string(),
            serde_json::Value::String("salt-b".to_string()),
        )]);
        let owned_project_b = DynamicReturnable::from_map(project_b_value.clone());
        let project_b_content_hash = owned_project_b.get_hash();
        let project_b_stable_hash = owned_project_b.get_stable_hash();
        assert!(matches!(
            owned_project_b.value,
            DynamicReturnableValue::JsonPointer(_)
        ));
        // "Aa" and "BB" intentionally share the 32-bit artifact filename hash.
        assert_eq!(hashing::djb2_number("Aa"), hashing::djb2_number("BB"));
        let collision =
            preload_mmap_v2_multi_for_test(&[("Aa", &path_a), ("BB", &path_b)]).unwrap_err();
        assert!(collision
            .to_string()
            .contains("Duplicate or colliding interned mmap SDK key identifier"));
        assert!(!InternedStore::has_preloaded_mmap_v2());

        preload_mmap_v2_multi_with_options_for_test(
            &[("Aa", &path_a), ("sdk-b", &path_b)],
            &MmapPreloadOptions {
                precompute_returnable_stable_hashes: true,
            },
        )
        .unwrap();

        let memory = InternedStore::mmap_reader_memory_snapshot()
            .unwrap()
            .unwrap();
        assert_eq!(
            memory.mapped_bytes,
            std::fs::metadata(&path_a).unwrap().len()
                + std::fs::metadata(&path_b).unwrap().len()
        );
        assert_eq!(memory.loaded_generation_count, 2);

        let mapped_project_b = DynamicReturnable::from_map(project_b_value);
        assert!(matches!(
            mapped_project_b.value,
            DynamicReturnableValue::JsonArchived(_)
        ));
        assert_eq!(
            InternedStore::get_mmap_returnable_stable_hash(project_b_content_hash),
            Some(project_b_stable_hash)
        );
        assert_eq!(mapped_project_b.get_stable_hash(), project_b_stable_hash);

        let store_a = test_spec_store("Aa");
        let store_b = test_spec_store("sdk-b");
        let unloaded_store = test_spec_store("BB");
        apply_payload(&store_a, payload_a.clone());
        apply_payload(&store_b, payload_b);
        apply_payload(&unloaded_store, payload_a);

        let data_a = store_a.load_data();
        let data_b = store_b.load_data();
        let unloaded_data = unloaded_store.load_data();
        let (name_a, gate_a) = data_a.snapshot.feature_gates.iter().next().unwrap();
        let (name_b, gate_b) = data_b.snapshot.feature_gates.iter().next().unwrap();
        let (unloaded_name, unloaded_gate) =
            unloaded_data.snapshot.feature_gates.iter().next().unwrap();

        assert!(gate_a.is_mmap());
        assert!(gate_b.is_mmap());
        assert!(gate_a.view().enabled());
        assert!(!gate_b.view().enabled());
        assert_eq!(gate_a.view().salt().as_str(), "salt-a");
        assert_eq!(gate_b.view().salt().as_str(), "salt-b");

        assert!(!unloaded_gate.is_mmap());
        assert!(unloaded_gate.view().enabled());
        assert_eq!(unloaded_gate.view().salt().as_str(), "salt-a");

        assert!(matches!(name_a.value, InternedStringValue::Static(_)));
        assert!(matches!(name_b.value, InternedStringValue::Static(_)));
        assert!(matches!(unloaded_name.value, InternedStringValue::Static(_)));
        assert!(std::ptr::eq(name_a.as_str(), name_b.as_str()));
        assert!(std::ptr::eq(name_a.as_str(), unloaded_name.as_str()));
    }

    #[test]
    fn multi_sdk_preload_rejects_conflicting_global_hashes_atomically() {
        let directory = tempfile::tempdir().unwrap();
        let path_a = directory.path().join("interned-store-conflict-a.mmap");
        let path_b = directory.path().join("interned-store-conflict-b.mmap");
        let data_a = MmapDataV2 {
            strings: vec![(7, Arc::new("alpha".to_string()))],
            ..MmapDataV2::default()
        };
        let data_b = MmapDataV2 {
            strings: vec![(7, Arc::new("beta".to_string()))],
            ..MmapDataV2::default()
        };
        std::fs::write(
            &path_a,
            rkyv::to_bytes::<rkyv::rancor::Error>(&data_a).unwrap(),
        )
        .unwrap();
        std::fs::write(
            &path_b,
            rkyv::to_bytes::<rkyv::rancor::Error>(&data_b).unwrap(),
        )
        .unwrap();

        let error = preload_mmap_v2_multi_for_test(&[("sdk-a", &path_a), ("sdk-b", &path_b)])
            .unwrap_err();

        assert!(error
            .to_string()
            .contains("conflicting string hash 7"));
        assert!(!InternedStore::has_preloaded_mmap_v2());
    }

    #[test]
    fn v2_write_after_byte_preload_includes_immortal_references() {
        InternedStore::preload_multi(&[EVAL_PROJ_JSON, DEMO_PROJ_PROTO]).unwrap();

        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-after-byte-preload.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();

        let bytes = std::fs::read(&path).unwrap();
        let archived =
            rkyv::access::<ArchivedMmapDataV2, rkyv::rancor::Error>(&bytes).unwrap();
        let demo_only_hash = rkyv::primitive::ArchivedU64::from_native(hashing::hash_one(b"a_gate"));
        assert!(!archived.strings.contains_key(&demo_only_hash));

        preload_mmap_v2_for_test(&path).unwrap();

        let array = EvaluatorValue::from_json_value(json!(["@statsig", "@stotseg"]));
        assert!(matches!(array.inner, EvaluatorValueInner::Mmap(_)));
    }

    #[test]
    fn v2_evaluator_values_are_read_directly_from_mmap() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let array = EvaluatorValue::from_json_value(json!(["@statsig", "@stotseg"]));
        assert!(matches!(array.inner, EvaluatorValueInner::Mmap(_)));
        let array_value = dyn_value!(json!(["@statsig", "@stotseg"]));
        assert!(array
            .as_value_ref()
            .is_equal_to_user_value(UserValueRef::Dynamic(&array_value)));
        assert_eq!(
            serde_json::to_value(&array).unwrap(),
            json!(["@statsig", "@stotseg"])
        );

        let number = EvaluatorValue::from_json_value(json!(1000));
        assert!(matches!(number.inner, EvaluatorValueInner::Mmap(_)));
        let number_value = dyn_value!(1000);
        assert!(number
            .as_value_ref()
            .is_equal_to_user_value(UserValueRef::Dynamic(&number_value)));
        assert_eq!(serde_json::to_value(&number).unwrap(), json!(1000.0));

        let object = EvaluatorValue::from_json_value(json!({"-1": true}));
        assert!(matches!(object.inner, EvaluatorValueInner::Mmap(_)));
        let object_value = dyn_value!(json!({"-1": true}));
        assert!(object
            .as_value_ref()
            .is_equal_to_user_value(UserValueRef::Dynamic(&object_value)));
        assert_eq!(serde_json::to_value(&object).unwrap(), json!({"-1": true}));
    }

    #[test]
    fn v2_evaluator_value_equality_matches_owned_values_in_both_directions() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-equality.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();

        let owned_array = EvaluatorValue::from_json_value(json!(["@statsig", "@stotseg"]));
        let unequal_array = EvaluatorValue::from_json_value(json!(["@statsig", "different"]));
        let owned_object = EvaluatorValue::from_json_value(json!({"-1": true}));
        let unequal_object = EvaluatorValue::from_json_value(json!({"-1": false}));
        assert!(matches!(owned_array.inner, EvaluatorValueInner::Pointer(_)));
        assert!(matches!(owned_object.inner, EvaluatorValueInner::Pointer(_)));

        preload_mmap_v2_for_test(&path).unwrap();

        let mapped_array = EvaluatorValue::from_json_value(json!(["@statsig", "@stotseg"]));
        let mapped_object = EvaluatorValue::from_json_value(json!({"-1": true}));
        assert!(matches!(mapped_array.inner, EvaluatorValueInner::Mmap(_)));
        assert!(matches!(mapped_object.inner, EvaluatorValueInner::Mmap(_)));

        assert_eq!(owned_array, mapped_array);
        assert_eq!(mapped_array, owned_array);
        assert_ne!(unequal_array, mapped_array);
        assert_ne!(mapped_array, unequal_array);
        assert_eq!(owned_object, mapped_object);
        assert_eq!(mapped_object, owned_object);
        assert_ne!(unequal_object, mapped_object);
        assert_ne!(mapped_object, unequal_object);
        assert_eq!(mapped_array, mapped_array.clone());
    }

    #[test]
    fn v2_regexes_are_compiled_once_during_preload() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-regex.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let regex = EvaluatorValue::from_json_value(json!("@.*mail"));
        assert!(matches!(regex.inner, EvaluatorValueInner::Mmap(_)));
        let value = dyn_value!("test@statsigmail");
        assert!(compare_str_with_regex((&value).into(), regex.as_value_ref()));

        assert_eq!(serde_json::to_value(&regex).unwrap(), json!("@.*mail"));
        assert_eq!(regex.as_ref().string_value.as_ref().unwrap().value, "@.*mail");
    }

    #[test]
    fn v2_mapped_string_can_be_compiled_after_preload() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-late-regex.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let mut regex = EvaluatorValue::from_json_value(json!("1.2.3"));
        assert!(matches!(regex.inner, EvaluatorValueInner::Mmap(_)));
        assert!(regex.as_value_ref().regex_value().is_none());

        regex.compile_regex();

        assert!(matches!(regex.inner, EvaluatorValueInner::Pointer(_)));
        let value = dyn_value!("1x2y3");
        assert!(compare_str_with_regex((&value).into(), regex.as_value_ref()));

        let reused = EvaluatorValue::from_json_value(json!("1.2.3"));
        match (&regex.inner, &reused.inner) {
            (EvaluatorValueInner::Pointer(regex), EvaluatorValueInner::Pointer(reused)) => {
                assert!(Arc::ptr_eq(regex, reused));
            }
            _ => panic!("late-compiled mmap regex was not reused"),
        }
    }

    #[test]
    fn v2_comparisons_match_owned_evaluator_values() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-comparisons.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let assert_same = |owned: &MemoizedEvaluatorValue,
                           mapped: EvaluatorValueRef<'_>,
                           comparison: &dyn Fn(EvaluatorValueRef<'_>) -> bool| {
            assert_eq!(comparison(owned.into()), comparison(mapped));
        };

        let mapped_number = EvaluatorValue::from_json_value(json!(1000));
        let owned_number = MemoizedEvaluatorValue::from(json!(1000));
        let number = dyn_value!(1001);
        assert_same(&owned_number, mapped_number.as_value_ref(), &|target| {
            compare_numbers((&number).into(), target, ConditionOperator::Gt)
        });

        let mapped_version = EvaluatorValue::from_json_value(json!("1.2.3"));
        let owned_version = MemoizedEvaluatorValue::from(json!("1.2.3"));
        let version = dyn_value!("1.2.4");
        assert_same(&owned_version, mapped_version.as_value_ref(), &|target| {
            compare_versions((&version).into(), target, ConditionOperator::VersionGt)
        });

        let target_json = json!(["@statsig", "@stotseg"]);
        let mapped_array = EvaluatorValue::from_json_value(target_json.clone());
        let owned_array = MemoizedEvaluatorValue::from(target_json);
        let string = dyn_value!("@STATSIG");
        assert_same(&owned_array, mapped_array.as_value_ref(), &|target| {
            compare_strings_in_array((&string).into(), target, ConditionOperator::Any)
        });
        let array = dyn_value!(json!(["@statsig", "@stotseg", "other"]));
        assert_same(&owned_array, mapped_array.as_value_ref(), &|target| {
            compare_arrays(
                (&array).into(),
                target,
                ConditionOperator::ArrayContainsAll,
            )
        });

        let timestamp = dyn_value!(2000);
        assert_same(&owned_number, mapped_number.as_value_ref(), &|target| {
            compare_time((&timestamp).into(), target, ConditionOperator::After)
        });
    }

    #[test]
    fn v2_loader_rejects_wrong_format_version() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-wrong-version.mmap");
        let data = MmapDataV2 {
            format_version: 99,
            ..MmapDataV2::default()
        };
        let archived = rkyv::to_bytes::<rkyv::rancor::Error>(&data).unwrap();
        std::fs::write(&path, archived).unwrap();

        assert!(matches!(
            preload_mmap_v2_for_test(&path),
            Err(StatsigErr::SerializationError(message))
                if message == "Unsupported interned mmap format version 99; expected 2"
        ));
    }

    #[test]
    fn v2_loader_rejects_dangling_evaluator_string_hash() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-dangling-string.mmap");
        let mut data = MmapDataV2::default();
        data.evaluator_values.insert(
            7,
            MmapEvaluatorValue {
                value_type: MmapEvaluatorValueType::String,
                bool_value: None,
                float_value: None,
                string_value: Some(42),
                regex_value: None,
                timestamp_value: None,
                object_value: None,
                array_value: None,
            },
        );
        let archived = rkyv::to_bytes::<rkyv::rancor::Error>(&data).unwrap();
        std::fs::write(&path, archived).unwrap();

        assert!(matches!(
            preload_mmap_v2_for_test(&path),
            Err(StatsigErr::SerializationError(message))
                if message.contains("evaluator string references missing string hash 42")
        ));
    }

    #[test]
    fn v2_loader_rejects_dangling_spec_string_hash() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-dangling-spec-string.mmap");
        let mut data = MmapDataV2::default();
        data.strings.push((1, "present".to_string().into()));
        data.feature_gates.insert(
            1,
            MmapSpec {
                content_hash: 0,
                checksum: Some(1),
                spec_type: 1,
                salt: 42,
                default_value: MmapReturnable::Null,
                enabled: true,
                rules: vec![],
                id_type: 1,
                explicit_parameters: None,
                entity: 1,
                has_shared_params: None,
                is_active: None,
                version: None,
                target_app_ids: None,
                forward_all_exposures: None,
                fields_used: None,
                use_new_layer_eval: None,
            },
        );
        let archived = rkyv::to_bytes::<rkyv::rancor::Error>(&data).unwrap();
        std::fs::write(&path, archived).unwrap();

        assert!(matches!(
            preload_mmap_v2_for_test(&path),
            Err(StatsigErr::SerializationError(message))
                if message.contains("spec salt references missing string hash 42")
        ));
    }

    #[test]
    fn v2_protobuf_specs_reuse_mmap_graph() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-protobuf.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_PROTO, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let current = SpecsResponseFull::default();
        let mut next = SpecsResponseFull::default();
        let mut response = ResponseData::from_bytes(EVAL_PROJ_PROTO.to_vec());
        deserialize_protobuf(
            &OpsStatsForInstance::new(),
            &current,
            &mut next,
            &mut response,
        )
        .unwrap();

        assert_specs_are_mmap_backed(&next);
    }

    #[test]
    fn v2_json_artifact_does_not_discard_protobuf_checksums() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-json-to-protobuf.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let current = SpecsResponseFull::default();
        let mut next = SpecsResponseFull::default();
        let mut response = ResponseData::from_bytes(EVAL_PROJ_PROTO.to_vec());
        deserialize_protobuf(
            &OpsStatsForInstance::new(),
            &current,
            &mut next,
            &mut response,
        )
        .unwrap();

        assert!(next
            .feature_gates
            .iter()
            .chain(next.dynamic_configs.iter())
            .chain(next.layer_configs.iter())
            .all(|(_, spec)| !spec.is_mmap()));
        assert!(next
            .feature_gates
            .iter()
            .chain(next.dynamic_configs.iter())
            .chain(next.layer_configs.iter())
            .all(|(_, spec)| spec.view().checksum().is_some()));
    }

    #[test]
    fn v2_spec_fingerprint_ignores_returnable_object_order_and_whitespace() {
        let left: Spec = serde_json::from_str(
            r#"{
                "type":"dynamic_config",
                "salt":"salt",
                "defaultValue":{"a":1,"b":{"x":true,"y":[1,2]}},
                "enabled":true,
                "rules":[],
                "idType":"userID",
                "entity":"dynamic_config"
            }"#,
        )
        .unwrap();
        let right: Spec = serde_json::from_str(
            r#"{"entity":"dynamic_config","idType":"userID","rules":[],"enabled":true,
                "defaultValue":{"b":{"y":[1,2],"x":true},"a":1},"salt":"salt",
                "type":"dynamic_config"}"#,
        )
        .unwrap();

        assert_eq!(spec_content_hash(&left), spec_content_hash(&right));
    }

    #[test]
    fn v2_changed_json_spec_stays_owned_while_unchanged_specs_reuse_mmap() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-mixed-update.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let mut payload: serde_json::Value = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        let gates = payload["feature_gates"].as_object_mut().unwrap();
        let mut names = gates.keys().cloned().collect::<Vec<_>>();
        names.sort();
        let changed_name = &names[0];
        let unchanged_name = &names[1];
        let enabled = gates[changed_name]["enabled"].as_bool().unwrap();
        gates[changed_name]["enabled"] = serde_json::Value::Bool(!enabled);

        let specs: SpecsResponseFull = serde_json::from_value(payload).unwrap();
        let changed = crate::interned_string::InternedString::from_str_ref(changed_name);
        let unchanged = crate::interned_string::InternedString::from_str_ref(unchanged_name);
        assert!(!specs.feature_gates.get(&changed).unwrap().is_mmap());
        assert!(specs.feature_gates.get(&unchanged).unwrap().is_mmap());
    }

    #[test]
    fn v2_materialized_delta_preserves_mmap_reuse_and_owned_fallback_semantics() {
        let condition = |checksum: &str, email: &str| {
            json!({
                "type": "user_field",
                "targetValue": [email],
                "operator": "any",
                "field": "email",
                "additionalValues": {},
                "idType": "userID",
                "checksum": checksum
            })
        };
        let gate =
            |checksum: &str, salt: &str, condition_name: &str, return_value: bool, version: u32| {
                json!({
                    "checksum": checksum,
                    "type": "feature_gate",
                    "salt": salt,
                    "defaultValue": false,
                    "enabled": true,
                    "rules": [{
                        "name": format!("{salt}-rule"),
                        "passPercentage": 100,
                        "returnValue": return_value,
                        "id": format!("{salt}-rule"),
                        "salt": "",
                        "conditions": [condition_name],
                        "idType": "userID"
                    }],
                    "idType": "userID",
                    "entity": "feature_gate",
                    "version": version
                })
            };

        let baseline_json = json!({
            "checksum": "delta-baseline",
            "company_id": "delta-company",
            "response_format": "delta-test",
            "experiment_to_layer": {},
            "condition_map": {
                "retained_condition": condition("11", "retained@example.com"),
                "replaced_condition": condition("12", "before@example.com"),
                "obsolete_condition": condition("13", "obsolete@example.com")
            },
            "dynamic_configs": {},
            "feature_gates": {
                "retained_gate": gate(
                    "101",
                    "retained",
                    "retained_condition",
                    true,
                    1
                ),
                "changed_gate": gate(
                    "102",
                    "changed-v1",
                    "replaced_condition",
                    false,
                    1
                ),
                "deleted_gate": gate(
                    "103",
                    "deleted",
                    "obsolete_condition",
                    true,
                    1
                )
            },
            "has_updates": true,
            "layer_configs": {},
            "time": 1
        });
        let final_json = json!({
            "checksum": "delta-final",
            "company_id": "delta-company",
            "response_format": "delta-test",
            "experiment_to_layer": {},
            "condition_map": {
                "retained_condition": condition("11", "retained@example.com"),
                "replaced_condition": condition("22", "after@example.com"),
                "added_condition": condition("33", "added@example.com")
            },
            "dynamic_configs": {},
            "feature_gates": {
                "retained_gate": gate(
                    "101",
                    "retained",
                    "retained_condition",
                    true,
                    1
                ),
                "changed_gate": gate(
                    "202",
                    "changed-v2",
                    "replaced_condition",
                    true,
                    2
                ),
                "added_gate": gate(
                    "303",
                    "added",
                    "added_condition",
                    true,
                    1
                )
            },
            "has_updates": true,
            "layer_configs": {},
            "time": 2
        });
        let baseline = serde_json::to_vec(&baseline_json).unwrap();
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-materialized-delta.mmap");
        let sdk_key = "secret-materialized-delta";
        write_mmap_v2_for_test(&baseline, &path).unwrap();

        // Parse the expected snapshot after writing (so it is not captured in the artifact) and
        // before preloading (so its representation is independently owned).
        let expected_final: SpecsResponseFull = serde_json::from_value(final_json).unwrap();
        assert!(expected_final
            .feature_gates
            .iter()
            .all(|(_, spec)| !spec.is_mmap()));
        assert!(expected_final
            .condition_map
            .values()
            .filter_map(|condition| condition.target_value.as_ref())
            .all(|value| matches!(value.inner, EvaluatorValueInner::Pointer(_))));

        let expected_feature_gates =
            serde_json::to_value(&expected_final.feature_gates).unwrap();
        let expected_condition_map =
            serde_json::to_value(&expected_final.condition_map).unwrap();
        let mut common_fields = serde_json::to_value(&expected_final).unwrap();
        let fields = common_fields.as_object_mut().unwrap();
        for field in [
            "checksum",
            "company_id",
            "condition_map",
            "dynamic_configs",
            "feature_gates",
            "has_updates",
            "layer_configs",
            "param_stores",
            "response_format",
            "time",
        ] {
            fields.remove(field);
        }
        let expected_evaluations = [
            ("retained_gate", "retained@example.com", true),
            ("retained_gate", "no-match@example.com", false),
            ("changed_gate", "after@example.com", true),
            ("changed_gate", "before@example.com", false),
            ("added_gate", "added@example.com", true),
            ("added_gate", "no-match@example.com", false),
        ]
        .map(|(gate_name, email, expected_bool)| {
            let mut user = StatsigUser::with_user_id("delta-test-user");
            user.set_email(email);
            let snapshot = evaluate(&expected_final, &user, gate_name, SpecType::Gate);
            assert_eq!(snapshot.bool_value, expected_bool);
            (gate_name, email, snapshot)
        });
        // Do not let independently owned target-value Arcs participate in delta interning.
        drop(expected_final);

        preload_mmap_v2_multi_for_test(&[(sdk_key, &path)]).unwrap();

        let store = test_spec_store(sdk_key);
        apply_payload(&store, baseline);
        {
            let current = store.load_data();
            assert_eq!(current.lcut(), 1);
            assert_eq!(current.snapshot.checksum.as_deref(), Some("delta-baseline"));
            assert_specs_are_mmap_backed(current.snapshot.as_ref());
            assert!(current
                .snapshot
                .condition_map
                .values()
                .filter_map(|condition| condition.target_value.as_ref())
                .all(|value| matches!(value.inner, EvaluatorValueInner::Mmap(_))));
        }

        let user_id = || pb::IdType {
            id_type: Some(pb::id_type::IdType::KnownIdType(
                pb::KnownIdType::UserId as i32,
            )),
        };
        let protobuf_gate =
            |salt: &str, condition_name: &str, return_value: bool, version: u32| pb::Spec {
                salt: salt.to_string(),
                enabled: true,
                default_value: Some(pb::ReturnValue {
                    value: Some(pb::return_value::Value::BoolValue(false)),
                }),
                entity: pb::EntityType::EntityFeatureGate as i32,
                id_type: Some(user_id()),
                version,
                rules: vec![pb::Rule {
                    name: format!("{salt}-rule"),
                    pass_percentage: 100,
                    id: format!("{salt}-rule"),
                    salt: Some(String::new()),
                    conditions: vec![condition_name.to_string()],
                    id_type: Some(user_id()),
                    return_value: Some(pb::ReturnValue {
                        value: Some(pb::return_value::Value::BoolValue(return_value)),
                    }),
                    ..pb::Rule::default()
                }],
                ..pb::Spec::default()
            };
        let protobuf_condition = |email: &str| pb::Condition {
            condition_type: pb::ConditionType::UserField as i32,
            id_type: Some(user_id()),
            target_value: Some(pb::AnyValue {
                value: Some(pb::any_value::Value::RawValue(
                    serde_json::to_vec(&json!([email])).unwrap(),
                )),
            }),
            operator: Some(pb::Operator::Any as i32),
            field: Some("email".to_string()),
            additional_values: Some(serde_json::to_vec(&json!({})).unwrap()),
        };

        let envelopes = vec![
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::CopyPrev as i32,
                ..pb::SpecsEnvelope::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::TopLevel as i32,
                data: Some(
                    pb::SpecsTopLevel {
                        has_updates: true,
                        time: 2,
                        company_id: "delta-company".to_string(),
                        response_format: "delta-test".to_string(),
                        checksum: "delta-final".to_string(),
                        rest: serde_json::to_vec(&common_fields).unwrap(),
                        may_have_remote_config_metadata: None,
                    }
                    .encode_to_vec(),
                ),
                ..pb::SpecsEnvelope::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::FeatureGate as i32,
                name: "changed_gate".to_string(),
                checksum: "202".to_string(),
                data: Some(protobuf_gate("changed-v2", "replaced_condition", true, 2).encode_to_vec()),
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::FeatureGate as i32,
                name: "added_gate".to_string(),
                checksum: "303".to_string(),
                data: Some(protobuf_gate("added", "added_condition", true, 1).encode_to_vec()),
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Condition as i32,
                name: "replaced_condition".to_string(),
                checksum: "22".to_string(),
                data: Some(protobuf_condition("after@example.com").encode_to_vec()),
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Condition as i32,
                name: "added_condition".to_string(),
                checksum: "33".to_string(),
                data: Some(protobuf_condition("added@example.com").encode_to_vec()),
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Deletions as i32,
                data: Some(
                    pb::RulesetsResponseDeletions {
                        feature_gates: vec!["deleted_gate".to_string()],
                        condition_map: vec!["obsolete_condition".to_string()],
                        ..pb::RulesetsResponseDeletions::default()
                    }
                    .encode_to_vec(),
                ),
                ..pb::SpecsEnvelope::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Checksums as i32,
                data: Some(
                    pb::RulesetsChecksums {
                        field_checksums: HashMap::from([
                            ("condition_map".to_string(), 66),
                            ("dynamic_configs".to_string(), 0),
                            ("feature_gates".to_string(), 606),
                            ("layer_configs".to_string(), 0),
                            ("param_stores".to_string(), 0),
                        ]),
                    }
                    .encode_to_vec(),
                ),
                ..pb::SpecsEnvelope::default()
            },
            pb::SpecsEnvelope {
                kind: pb::SpecsEnvelopeKind::Done as i32,
                ..pb::SpecsEnvelope::default()
            },
        ];
        let mut encoded = Vec::new();
        for envelope in envelopes {
            envelope.encode_length_delimited(&mut encoded).unwrap();
        }
        let mut compressed = Vec::new();
        {
            let mut writer = brotli::CompressorWriter::with_params(
                &mut compressed,
                BUFFER_SIZE,
                &BrotliEncoderParams::default(),
            );
            writer.write_all(&encoded).unwrap();
            writer.flush().unwrap();
        }
        store
            .set_values(SpecsUpdate {
                data: ResponseData::from_bytes_with_headers(
                    compressed,
                    Some(HashMap::from([
                        (
                            "content-type".to_string(),
                            "application/octet-stream".to_string(),
                        ),
                        ("content-encoding".to_string(), "statsig-br".to_string()),
                        ("x-deltas-used".to_string(), "true".to_string()),
                    ])),
                ),
                source: SpecsSource::Network,
                received_at: 3_000,
                source_api: Some("materialized-delta-test".to_string()),
                has_updates: None,
            })
            .unwrap();

        let updated = store.load_data();
        assert_eq!(updated.lcut(), 2);
        assert_eq!(updated.snapshot.checksum.as_deref(), Some("delta-final"));

        let retained_gate =
            crate::interned_string::InternedString::from_str_ref("retained_gate");
        let changed_gate = crate::interned_string::InternedString::from_str_ref("changed_gate");
        let added_gate = crate::interned_string::InternedString::from_str_ref("added_gate");
        let deleted_gate = crate::interned_string::InternedString::from_str_ref("deleted_gate");
        assert!(updated
            .snapshot
            .feature_gates
            .get(&retained_gate)
            .unwrap()
            .is_mmap());
        assert!(!updated
            .snapshot
            .feature_gates
            .get(&changed_gate)
            .unwrap()
            .is_mmap());
        assert!(!updated
            .snapshot
            .feature_gates
            .get(&added_gate)
            .unwrap()
            .is_mmap());
        assert!(updated.snapshot.feature_gates.get(&deleted_gate).is_none());

        let retained_condition =
            crate::interned_string::InternedString::from_str_ref("retained_condition");
        let replaced_condition =
            crate::interned_string::InternedString::from_str_ref("replaced_condition");
        let added_condition =
            crate::interned_string::InternedString::from_str_ref("added_condition");
        let obsolete_condition =
            crate::interned_string::InternedString::from_str_ref("obsolete_condition");
        assert!(matches!(
            updated.snapshot.condition_map[&retained_condition]
                .target_value
                .as_ref()
                .unwrap()
                .inner,
            EvaluatorValueInner::Mmap(_)
        ));
        assert!(matches!(
            updated.snapshot.condition_map[&replaced_condition]
                .target_value
                .as_ref()
                .unwrap()
                .inner,
            EvaluatorValueInner::Pointer(_)
        ));
        assert!(matches!(
            updated.snapshot.condition_map[&added_condition]
                .target_value
                .as_ref()
                .unwrap()
                .inner,
            EvaluatorValueInner::Pointer(_)
        ));
        assert!(!updated
            .snapshot
            .condition_map
            .contains_key(&obsolete_condition));

        assert_eq!(
            serde_json::to_value(&updated.snapshot.feature_gates).unwrap(),
            expected_feature_gates
        );
        assert_eq!(
            serde_json::to_value(&updated.snapshot.condition_map).unwrap(),
            expected_condition_map
        );

        for (gate_name, email, expected) in expected_evaluations {
            let mut user = StatsigUser::with_user_id("delta-test-user");
            user.set_email(email);
            assert_eq!(
                evaluate(updated.snapshot.as_ref(), &user, gate_name, SpecType::Gate),
                expected
            );
        }
    }

    #[test]
    fn v2_json_session_update_mode_is_only_preserved_by_opt_in_parser() {
        let mut payload: serde_json::Value = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        let gates = payload["feature_gates"].as_object_mut().unwrap();
        let mut names = gates.keys().cloned().collect::<Vec<_>>();
        names.sort();
        let live_name = &names[0];
        let unchanged_name = &names[1];
        gates[live_name]["sessionUpdateMode"] = json!("live");
        let payload = serde_json::to_vec(&payload).unwrap();

        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-session-update-mode.mmap");
        write_mmap_v2_for_test(&payload, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let live = crate::interned_string::InternedString::from_str_ref(live_name);
        let unchanged = crate::interned_string::InternedString::from_str_ref(unchanged_name);

        let default_specs: SpecsResponseFull = serde_json::from_slice(&payload).unwrap();
        let default_live_spec = default_specs.feature_gates.get(&live).unwrap();
        assert!(default_live_spec.is_mmap());
        assert_eq!(default_live_spec.session_update_mode(), None);

        let specs = SpecsResponseFull::deserialize_json_with_options(
            &payload,
            SpecsResponseParseOptions::preserving_session_update_mode(),
        )
        .unwrap();
        let live_spec = specs.feature_gates.get(&live).unwrap();
        assert!(live_spec.is_mmap());
        assert_eq!(live_spec.session_update_mode(), Some("live"));
        assert_ne!(live_spec, default_live_spec);
        assert_eq!(live_spec, &live_spec.clone());
        assert!(live_spec.clone().into_pointer().is_none());
        assert_eq!(
            live_spec.as_spec_ref().session_update_mode.as_deref(),
            Some("live")
        );
        assert_eq!(
            serde_json::to_value(live_spec).unwrap()["sessionUpdateMode"],
            json!("live")
        );
        assert!(specs.feature_gates.get(&unchanged).unwrap().is_mmap());

        let mut response = materialized_delta(&specs, specs.time + 1);
        let mut next = SpecsResponseFull::default();
        deserialize_protobuf_with_options(
            &OpsStatsForInstance::new(),
            &specs,
            &mut next,
            &mut response,
            SpecsResponseParseOptions::preserving_session_update_mode(),
        )
        .unwrap();

        let copied_live_spec = next.feature_gates.get(&live).unwrap();
        assert!(copied_live_spec.is_mmap());
        assert_eq!(copied_live_spec.session_update_mode(), Some("live"));
    }

    #[test]
    fn v2_json_checksum_presence_mismatch_stays_owned() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-json-checksum.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let mut payload: serde_json::Value = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        let gates = payload["feature_gates"].as_object_mut().unwrap();
        let name = gates.keys().next().unwrap().clone();
        gates[&name]["checksum"] = serde_json::Value::String("new-checksum".to_string());

        let specs: SpecsResponseFull = serde_json::from_value(payload).unwrap();
        let name = crate::interned_string::InternedString::from_str_ref(&name);
        let spec = specs.feature_gates.get(&name).unwrap();
        assert!(!spec.is_mmap());
        assert_eq!(
            spec.view().checksum().map(|value| value.as_str()),
            Some("new-checksum")
        );
    }

    #[test]
    fn v2_gate_override_does_not_materialize_mmap_spec() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-gate-override.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();
        let specs: SpecsResponseFull = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();

        let adapter = StatsigLocalOverrideAdapter::new();
        adapter.override_gate("test_public", false, None);
        let adapter: Arc<dyn OverrideAdapter> = Arc::new(adapter);
        let public_user = test_user();
        let user = StatsigUserInternal::new(&public_user, None);
        let id_lists = HashMap::new();
        let hashing = HashUtil::new();
        let mut context = EvaluatorContext::new(
            &user,
            &specs,
            IdListResolution::MapLookup(&id_lists),
            &hashing,
            None,
            Some(&adapter),
            false,
            None,
            true,
        );

        assert_eq!(
            Evaluator::evaluate(&mut context, "test_public", &SpecType::Gate).unwrap(),
            Recognition::Recognized
        );
        assert!(!context.result.bool_value);
        assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);
    }

    #[cfg(unix)]
    #[test]
    fn v2_preloaded_graph_is_reused_after_fork() {
        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-parent-preload.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let pid = unsafe { libc::fork() };
        if pid == 0 {
            let specs: SpecsResponseFull = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
            assert_specs_are_mmap_backed(&specs);
            let result = evaluate(&specs, &test_user(), "test_email_regex", SpecType::Gate);
            assert!(result.bool_value);
            assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);
            std::process::exit(0);
        }

        unsafe {
            let mut status = 0;
            libc::waitpid(pid, &mut status, 0);
            assert!(libc::WIFEXITED(status));
            assert_eq!(libc::WEXITSTATUS(status), 0);
        }
    }

    #[test]
    #[ignore = "manual benchmark; run with --release --ignored --nocapture"]
    fn benchmark_owned_vs_v2_mmap_evaluation() {
        let iterations = std::env::var("STATSIG_MMAP_BENCH_ITERATIONS")
            .ok()
            .and_then(|value| value.parse::<usize>().ok())
            .unwrap_or(10_000);
        let user = test_user();
        let owned_specs: SpecsResponseFull = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        let expected = evaluate(&owned_specs, &user, "test_email_regex", SpecType::Gate);
        let started = Instant::now();
        let mut owned_result = None;
        for _ in 0..iterations {
            owned_result = Some(std::hint::black_box(evaluate(
                &owned_specs,
                &user,
                "test_email_regex",
                SpecType::Gate,
            )));
        }
        let owned_elapsed = started.elapsed();
        assert_eq!(owned_result.as_ref(), Some(&expected));
        drop(owned_specs);

        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-benchmark.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();
        let mapped_specs: SpecsResponseFull = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        let started = Instant::now();
        let mut mapped_result = None;
        for _ in 0..iterations {
            mapped_result = Some(std::hint::black_box(evaluate(
                &mapped_specs,
                &user,
                "test_email_regex",
                SpecType::Gate,
            )));
        }
        let mapped_elapsed = started.elapsed();
        assert_eq!(mapped_result, Some(expected));

        println!(
            "interned_mmap_v2_bench iterations={iterations} owned_ms={:.3} mapped_ms={:.3} ratio={:.3}",
            owned_elapsed.as_secs_f64() * 1000.0,
            mapped_elapsed.as_secs_f64() * 1000.0,
            mapped_elapsed.as_secs_f64() / owned_elapsed.as_secs_f64(),
        );
        assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);
    }

    #[test]
    fn v2_preserves_optional_spec_fields_and_reuses_explicit_parameters() {
        let payload = serde_json::to_vec(&json!({
            "experiment_to_layer": {},
            "condition_map": {},
            "dynamic_configs": {
                "full_fields_config": {
                    "type": "dynamic_config",
                    "salt": "full-fields-salt",
                    "defaultValue": {"value": "default"},
                    "enabled": true,
                    "rules": [{
                        "name": "full-fields-rule",
                        "passPercentage": 100,
                        "returnValue": {"value": "treatment"},
                        "id": "full-fields-rule-id",
                        "salt": "full-fields-rule-salt",
                        "conditions": [],
                        "idType": "userID",
                        "samplingRate": 17
                    }],
                    "idType": "userID",
                    "explicitParameters": ["value"],
                    "entity": "experiment",
                    "targetAppIDs": ["target-app"],
                    "forwardAllExposures": true,
                    "fieldsUsed": ["email"],
                    "useNewLayerEval": true
                }
            },
            "feature_gates": {},
            "has_updates": true,
            "layer_configs": {},
            "time": 1
        }))
        .unwrap();
        let baseline: SpecsResponseFull = serde_json::from_slice(&payload).unwrap();

        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-full-fields.mmap");
        write_mmap_v2_for_test(&payload, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let mapped: SpecsResponseFull = serde_json::from_slice(&payload).unwrap();
        let name = crate::interned_string::InternedString::from_str_ref("full_fields_config");
        let spec = mapped.dynamic_configs.get(&name).unwrap();
        assert!(spec.is_mmap());
        let view = spec.view();

        assert_eq!(view.target_app_ids_contains("target-app"), Some(true));
        assert_eq!(view.forward_all_exposures(), Some(true));
        assert_eq!(view.fields_used(), vec!["email"]);
        assert!(view.uses_new_layer_eval());
        assert_eq!(view.rule(0).sampling_rate(), Some(17));

        let first = view.explicit_parameters().unwrap();
        let second = view.explicit_parameters().unwrap();
        assert!(std::ptr::eq(first.as_slice(), second.as_slice()));
        assert!(first.contains("value"));

        assert_eq!(
            serde_json::to_value(&mapped.dynamic_configs).unwrap(),
            serde_json::to_value(&baseline.dynamic_configs).unwrap()
        );
    }

    #[test]
    fn v2_targets_match_owned_end_to_end_evaluation() {
        let user = test_user();
        let baseline_specs: SpecsResponseFull = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        let baseline = [
            evaluate(&baseline_specs, &user, "test_nested_gate_condition", SpecType::Gate),
            evaluate(&baseline_specs, &user, "test_email_regex", SpecType::Gate),
            evaluate(&baseline_specs, &user, "Basic_test_layer", SpecType::Layer),
        ];
        let baseline_serialized = serde_json::to_value(&baseline_specs).unwrap();
        drop(baseline_specs);

        let directory = tempfile::tempdir().unwrap();
        let path = directory.path().join("interned-store-v2-evaluation.mmap");
        write_mmap_v2_for_test(EVAL_PROJ_JSON, &path).unwrap();
        preload_mmap_v2_for_test(&path).unwrap();

        let mapped_specs: SpecsResponseFull = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
        assert_specs_are_mmap_backed(&mapped_specs);
        assert!(mapped_specs
            .condition_map
            .values()
            .filter_map(|condition| condition.target_value.as_ref())
            .all(|value| matches!(value.inner, EvaluatorValueInner::Mmap(_))));

        assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);
        let serialized = serde_json::to_value(&mapped_specs).unwrap();
        assert_eq!(InternedStore::get_mmap_spec_materialization_len(), 0);
        for field in [
            "condition_map",
            "feature_gates",
            "dynamic_configs",
            "layer_configs",
        ] {
            assert_eq!(serialized[field], baseline_serialized[field]);
        }

        let mapped = [
            evaluate(&mapped_specs, &user, "test_nested_gate_condition", SpecType::Gate),
            evaluate(&mapped_specs, &user, "test_email_regex", SpecType::Gate),
            evaluate(&mapped_specs, &user, "Basic_test_layer", SpecType::Layer),
        ];

        assert_eq!(mapped, baseline);
        assert!(mapped[2].config_delegate.is_some());
    }
}

fn assert_specs_are_mmap_backed(specs: &SpecsResponseFull) {
    for (kind, specs) in [
        ("feature gates", &specs.feature_gates),
        ("dynamic configs", &specs.dynamic_configs),
        ("layer configs", &specs.layer_configs),
    ] {
        let owned = specs
            .iter()
            .filter(|(_, spec)| !spec.is_mmap())
            .map(|(name, _)| name.as_str())
            .collect::<Vec<_>>();
        assert!(owned.is_empty(), "{kind} remained owned: {owned:?}");
    }
}

#[derive(Debug, PartialEq)]
struct EvaluationSnapshot {
    bool_value: bool,
    rule_id: Option<String>,
    group_name: Option<String>,
    config_delegate: Option<String>,
    json_value: Option<HashMap<String, serde_json::Value>>,
}

fn evaluate(
    specs: &SpecsResponseFull,
    user: &StatsigUser,
    name: &str,
    spec_type: SpecType,
) -> EvaluationSnapshot {
    let user = StatsigUserInternal::new(user, None);
    let id_lists = HashMap::new();
    let hashing = HashUtil::new();
    let mut context = EvaluatorContext::new(
        &user,
        specs,
        IdListResolution::MapLookup(&id_lists),
        &hashing,
        None,
        None,
        false,
        None,
        true,
    );
    assert_eq!(
        Evaluator::evaluate(&mut context, name, &spec_type).unwrap(),
        Recognition::Recognized
    );

    EvaluationSnapshot {
        bool_value: context.result.bool_value,
        rule_id: context.result.rule_id.map(|value| value.to_string()),
        group_name: context.result.group_name.map(|value| value.to_string()),
        config_delegate: context
            .result
            .config_delegate
            .map(|value| value.to_string()),
        json_value: context.result.json_value.and_then(|value| value.get_json()),
    }
}

fn test_user() -> StatsigUser {
    let mut user = StatsigUser::with_user_id("user-not-in-layer-holdout");
    user.set_email("a_user@statsigmail");
    user.set_custom_ids(HashMap::from([
        ("companyID".to_string(), "123".to_string()),
        ("stableID".to_string(), String::new()),
    ]));
    user
}
