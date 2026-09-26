use std::{collections::HashMap, io::Write};

use prost::Message;
use rusty_fork::rusty_fork_test;

use crate::{
    interned_string::InternedString,
    interned_values::InternedStore,
    specs_response::{spec_types::SpecsResponseFull, statsig_config_specs as pb},
};

const EVAL_PROJ_JSON: &[u8] = include_bytes!("../../../tests/data/eval_proj_dcs.json");

fn json_with_remote_configs() -> Vec<u8> {
    let mut response: serde_json::Value = serde_json::from_slice(EVAL_PROJ_JSON).unwrap();
    response["feature_gates"]["segment:best_engineers"]["checksum"] = serde_json::json!("101");
    response["layer_configs"]["test_layer_with_no_exp"]["checksum"] = serde_json::json!("103");
    let configs = response["dynamic_configs"].as_object_mut().unwrap();
    configs.get_mut("test_experiment_no_targeting").unwrap()["checksum"] = serde_json::json!("107");
    configs.get_mut("test_exp_random_id").unwrap()["remoteConfigMetadata"] =
        serde_json::json!({ "default": { "url": "https://example.com/default" } });
    configs.get_mut("an_experiment1").unwrap()["rules"][0]["remoteConfigMetadata"] =
        serde_json::json!({ "url": "https://example.com/rule" });
    serde_json::to_vec(&response).unwrap()
}

fn envelope(
    kind: pb::SpecsEnvelopeKind,
    name: &str,
    checksum: &str,
    spec: pb::Spec,
) -> pb::SpecsEnvelope {
    pb::SpecsEnvelope {
        kind: kind as i32,
        name: name.to_owned(),
        checksum: checksum.to_owned(),
        data: Some(spec.encode_to_vec()),
    }
}

fn protobuf_with_remote_configs(
    dynamic_checksum: u64,
    remote_marker: Option<bool>,
    followup: Option<pb::SpecsEnvelope>,
) -> Vec<u8> {
    let remote_default = pb::Spec {
        entity: pb::EntityType::EntityDynamicConfig as i32,
        remote_config_metadata: Some(pb::RemoteConfigValueMetadata::default()),
        ..pb::Spec::default()
    };
    let remote_rule = pb::Spec {
        entity: pb::EntityType::EntityDynamicConfig as i32,
        rules: vec![pb::Rule {
            remote_config_metadata: Some(pb::RemoteConfigValueMetadata::default()),
            ..pb::Rule::default()
        }],
        ..pb::Spec::default()
    };
    let mut envelopes = vec![
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::TopLevel as i32,
            data: Some(
                pb::SpecsTopLevel {
                    time: 1,
                    has_updates: true,
                    may_have_remote_config_metadata: remote_marker,
                    rest: br#"{"experiment_to_layer":{}}"#.to_vec(),
                    ..pb::SpecsTopLevel::default()
                }
                .encode_to_vec(),
            ),
            ..pb::SpecsEnvelope::default()
        },
        envelope(
            pb::SpecsEnvelopeKind::FeatureGate,
            "ordinary_gate",
            "19",
            pb::Spec {
                entity: pb::EntityType::EntityFeatureGate as i32,
                ..pb::Spec::default()
            },
        ),
        envelope(
            pb::SpecsEnvelopeKind::DynamicConfig,
            "ordinary_config",
            "11",
            pb::Spec {
                entity: pb::EntityType::EntityDynamicConfig as i32,
                ..pb::Spec::default()
            },
        ),
        envelope(
            pb::SpecsEnvelopeKind::DynamicConfig,
            "remote_default",
            "13",
            remote_default,
        ),
        envelope(
            pb::SpecsEnvelopeKind::DynamicConfig,
            "remote_rule",
            "17",
            remote_rule,
        ),
        envelope(
            pb::SpecsEnvelopeKind::LayerConfig,
            "ordinary_layer",
            "23",
            pb::Spec {
                entity: pb::EntityType::EntityLayer as i32,
                ..pb::Spec::default()
            },
        ),
    ];
    envelopes.extend(followup);
    envelopes.extend([
        pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Checksums as i32,
            data: Some(
                pb::RulesetsChecksums {
                    field_checksums: HashMap::from([
                        ("condition_map".to_owned(), 0),
                        ("dynamic_configs".to_owned(), dynamic_checksum),
                        ("feature_gates".to_owned(), 19),
                        ("layer_configs".to_owned(), 23),
                        ("param_stores".to_owned(), 0),
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
    ]);

    let mut encoded = Vec::new();
    for envelope in envelopes {
        envelope.encode_length_delimited(&mut encoded).unwrap();
    }
    let mut compressed = Vec::new();
    {
        let mut compressor = brotli::CompressorWriter::new(&mut compressed, 4096, 5, 22);
        compressor.write_all(&encoded).unwrap();
    }
    compressed
}

fn assert_shared_ordinary_specs() {
    let ordinary = InternedString::from_str_ref("ordinary_config");
    assert!(InternedStore::try_get_preloaded_dynamic_config(&ordinary).is_some());
    let gate = InternedString::from_str_ref("ordinary_gate");
    assert!(InternedStore::try_get_preloaded_feature_gate(&gate).is_some());
    let layer = InternedString::from_str_ref("ordinary_layer");
    assert!(InternedStore::try_get_preloaded_layer_config(&layer).is_some());
    for name in ["remote_default", "remote_rule"] {
        assert!(
            InternedStore::try_get_preloaded_dynamic_config(&InternedString::from_str_ref(name))
                .is_none()
        );
    }
}

rusty_fork_test! {
    #[test]
    fn normal_json_decode_still_rejects_unhydrated_dynamic_config() {
        assert!(serde_json::from_slice::<SpecsResponseFull>(&json_with_remote_configs())
            .unwrap_err().to_string().contains("before hydration"));
    }

    #[test]
    fn json_preload_does_not_skip_remote_metadata_in_feature_gates() {
        let mut response: serde_json::Value = serde_json::from_slice(&json_with_remote_configs()).unwrap();
        response["feature_gates"]["segment:best_engineers"]["remoteConfigMetadata"] =
            serde_json::json!({"url": "https://example.com/gate"});
        assert!(InternedStore::preload(&serde_json::to_vec(&response).unwrap()).is_err());
    }

    #[test]
    fn json_preload_keeps_ordinary_specs_when_default_and_rule_values_are_remote() {
        InternedStore::preload(&json_with_remote_configs()).unwrap();
        assert!(InternedStore::try_get_preloaded_dynamic_config(
            &InternedString::from_str_ref("test_experiment_no_targeting")
        ).is_some());
        assert!(InternedStore::try_get_preloaded_feature_gate(
            &InternedString::from_str_ref("segment:best_engineers")
        ).is_some());
        assert!(InternedStore::try_get_preloaded_layer_config(
            &InternedString::from_str_ref("test_layer_with_no_exp")
        ).is_some());
        for name in ["test_exp_random_id", "an_experiment1"] {
            assert!(InternedStore::try_get_preloaded_dynamic_config(
                &InternedString::from_str_ref(name)
            ).is_none());
        }
    }

    #[test]
    fn protobuf_preload_keeps_ordinary_specs_and_validates_remote_checksums() {
        let protobuf = protobuf_with_remote_configs(11 + 13 + 17, Some(true), None);
        InternedStore::preload(&protobuf).unwrap();
        assert_shared_ordinary_specs();
    }

    #[test]
    fn multi_project_preload_keeps_ordinary_specs_from_json_and_protobuf() {
        let json = json_with_remote_configs();
        let protobuf = protobuf_with_remote_configs(11 + 13 + 17, Some(true), None);
        InternedStore::preload_multi(&[&json, &protobuf]).unwrap();
        assert_shared_ordinary_specs();
        assert!(InternedStore::try_get_preloaded_dynamic_config(
            &InternedString::from_str_ref("test_experiment_no_targeting")
        ).is_some());
        for name in ["test_exp_random_id", "an_experiment1"] {
            assert!(InternedStore::try_get_preloaded_dynamic_config(
                &InternedString::from_str_ref(name)
            ).is_none());
        }
    }

    #[test]
    fn protobuf_preload_rejects_bad_checksum_even_when_remote_configs_are_skipped() {
        let protobuf = protobuf_with_remote_configs(11, Some(true), None);
        assert!(InternedStore::preload(&protobuf).is_err());
        assert!(InternedStore::try_get_preloaded_feature_gate(
            &InternedString::from_str_ref("ordinary_gate")
        ).is_none());
    }

    #[test]
    fn protobuf_preload_requires_remote_metadata_marker_for_selective_skip() {
        for marker in [None, Some(false)] {
            let protobuf = protobuf_with_remote_configs(11 + 13 + 17, marker, None);
            assert!(InternedStore::preload(&protobuf).is_err());
        }
    }

    #[test]
    fn protobuf_preload_replaces_skipped_remote_checksum_with_ordinary_config() {
        let followup = envelope(
            pb::SpecsEnvelopeKind::DynamicConfig,
            "remote_default",
            "29",
            pb::Spec {
                entity: pb::EntityType::EntityDynamicConfig as i32,
                ..pb::Spec::default()
            },
        );
        InternedStore::preload(&protobuf_with_remote_configs(11 + 29 + 17, Some(true), Some(followup))).unwrap();
        assert!(InternedStore::try_get_preloaded_dynamic_config(
            &InternedString::from_str_ref("remote_default")
        ).is_some());
    }

    #[test]
    fn protobuf_preload_replaces_skipped_remote_checksum_with_new_remote_config() {
        let followup = envelope(
            pb::SpecsEnvelopeKind::DynamicConfig,
            "remote_default",
            "29",
            pb::Spec {
                entity: pb::EntityType::EntityDynamicConfig as i32,
                remote_config_metadata: Some(pb::RemoteConfigValueMetadata::default()),
                ..pb::Spec::default()
            },
        );
        InternedStore::preload(&protobuf_with_remote_configs(11 + 29 + 17, Some(true), Some(followup))).unwrap();
        assert!(InternedStore::try_get_preloaded_dynamic_config(
            &InternedString::from_str_ref("remote_default")
        ).is_none());
    }

    #[test]
    fn protobuf_preload_removes_skipped_remote_checksum_on_deletion() {
        let followup = pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Deletions as i32,
            data: Some(
                pb::RulesetsResponseDeletions {
                    dynamic_configs: vec!["remote_default".to_owned()],
                    ..pb::RulesetsResponseDeletions::default()
                }
                .encode_to_vec(),
            ),
            ..pb::SpecsEnvelope::default()
        };
        InternedStore::preload(&protobuf_with_remote_configs(11 + 17, Some(true), Some(followup))).unwrap();
        assert!(InternedStore::try_get_preloaded_dynamic_config(
            &InternedString::from_str_ref("ordinary_config")
        ).is_some());
        assert!(InternedStore::try_get_preloaded_dynamic_config(
            &InternedString::from_str_ref("remote_default")
        ).is_none());
    }

    #[test]
    fn protobuf_preload_ignores_malformed_deletion_without_losing_remote_checksum() {
        let malformed = pb::SpecsEnvelope {
            kind: pb::SpecsEnvelopeKind::Deletions as i32,
            data: Some(vec![0xff]),
            ..pb::SpecsEnvelope::default()
        };
        InternedStore::preload(&protobuf_with_remote_configs(
            11 + 13 + 17,
            Some(true),
            Some(malformed),
        ))
        .unwrap();
        assert_shared_ordinary_specs();
    }
}
