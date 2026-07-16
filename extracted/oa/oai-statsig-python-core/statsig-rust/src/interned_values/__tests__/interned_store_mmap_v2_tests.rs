use rusty_fork::rusty_fork_test;
use serde_json::json;
use std::{collections::HashMap, sync::Arc, time::Instant};

use crate::{
    dyn_value,
    evaluation::{
        comparisons::{
            compare_arrays, compare_numbers, compare_str_with_regex, compare_strings_in_array,
            compare_time, compare_versions,
        },
        evaluator::{Evaluator, Recognition, SpecType},
        evaluator_context::{EvaluatorContext, IdListResolution},
        evaluator_value::{
            EvaluatorValue, EvaluatorValueInner, EvaluatorValueRef, MemoizedEvaluatorValue,
        },
    },
    hashing::{self, HashUtil},
    interned_values::{
        interned_store::{preload_mmap_v2_for_test, write_mmap_v2_for_test},
        mmap_data_v2::{
            spec_content_hash, ArchivedMmapDataV2, MmapDataV2, MmapEvaluatorValue,
            MmapEvaluatorValueType, MmapReturnable, MmapSpec,
        },
        InternedStore,
    },
    networking::ResponseData,
    observability::ops_stats::OpsStatsForInstance,
    specs_response::proto_specs::deserialize_protobuf,
    specs_response::spec_types::{ConditionOperator, Spec, SpecsResponseFull},
    user::{user_value::UserValueRef, StatsigUserInternal},
    OverrideAdapter, StatsigErr, StatsigLocalOverrideAdapter, StatsigUser,
};

const EVAL_PROJ_JSON: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.json");
const EVAL_PROJ_PROTO: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.pb.br");
const DEMO_PROJ_PROTO: &[u8] = include_bytes!("../../../tests/data/demo_proj_dcs.pb.br");

rusty_fork_test! {
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
        for field in ["feature_gates", "dynamic_configs", "layer_configs"] {
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
