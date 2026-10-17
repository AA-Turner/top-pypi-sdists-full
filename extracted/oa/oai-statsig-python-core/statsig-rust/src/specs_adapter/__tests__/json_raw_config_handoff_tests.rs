use super::*;
use crate::specs_response::specs_hash_map::SpecsHashMap;
use serde_json::json;

fn response(configs: &str, extra: &str) -> String {
    format!(
        r#"{{"feature_gates":{{}},"layer_configs":{{}},"condition_map":{{}},"experiment_to_layer":{{}},"has_updates":true,"time":1{extra},"dynamic_configs":{{{configs}}}}}"#
    )
}

fn ordinary(value: &str) -> String {
    format!(
        r#"{{"type":"dynamic_config","salt":"handoff","enabled":true,"defaultValue":{value},"rules":[],"idType":"userID","entity":"dynamic_config","sessionUpdateMode":"on_exposure"}}"#
    )
}

fn input(source: &str) -> JsonHydrationInput {
    let mut payload: RawJsonObject = serde_json::from_str(source).unwrap();
    let configs = payload.remove("dynamic_configs").unwrap();
    let configs: RawJsonObject = serde_json::from_str(configs.get()).unwrap();
    JsonHydrationInput {
        payload,
        configs: configs
            .0
            .into_iter()
            .map(|(name, raw_spec)| JsonConfigEntry {
                name,
                raw_spec,
                use_remote_decoder: false,
            })
            .collect(),
        references: Vec::new(),
        reference_count: 0,
        total_bytes: 0,
    }
}

// The old roundtrip is the oracle, including its deduplicated raw map and
// dynamic_configs-last order. All other production decoding stays shared.
fn previous_roundtrip(source: &str) -> Result<Box<SpecsResponseFull>, StatsigErr> {
    let input = input(source);
    let mut payload = input.payload;
    let ordinary = RawJsonObject(
        input
            .configs
            .into_iter()
            .map(|config| (config.name, config.raw_spec))
            .collect(),
    );
    payload.insert("dynamic_configs".to_owned(), raw_json_value(&ordinary)?);
    let bytes = serde_json::to_vec(&payload).unwrap();
    serde_json::from_slice(&bytes)
        .map_err(|error| StatsigErr::JsonParseError(TAG.to_owned(), error.to_string()))
}

fn scoped<T>(
    options: SpecsResponseParseOptions,
    callback: impl FnOnce() -> T,
) -> (T, SpecDecodeStats) {
    track_spec_decodes(|| {
        InternedStore::with_mmap_project(
            MmapProjectId::for_sdk_key("raw-config-handoff-test"),
            || with_parse_options(options, callback),
        )
    })
}

fn candidate(
    source: &str,
    capture: bool,
) -> Result<(Box<SpecsResponseFull>, ResponseData), StatsigErr> {
    let mut data = ResponseData::from_bytes(source.as_bytes().to_vec());
    let (snapshot, verified) = build_hydrated_json_snapshot(
        input(source),
        &mut data,
        VerifiedRemoteValues::new(),
        HashMap::new(),
        capture,
    )?;
    assert!(verified.is_empty());
    Ok((snapshot, data))
}

#[test]
fn ordinary_handoff_preserves_malformed_skips_session_mode_and_decode_counts() {
    let source = response(
        &format!(
            r#""valid":{},"malformed":{{"enabled":true}},"scalar":42"#,
            ordinary("{\"value\":1}")
        ),
        "",
    );
    for options in [
        SpecsResponseParseOptions::default(),
        SpecsResponseParseOptions::preserving_session_update_mode(),
    ] {
        let (expected, expected_stats) = scoped(options, || previous_roundtrip(&source));
        let ((actual, _), actual_stats) = {
            let (actual, stats) = scoped(options, || candidate(&source, false));
            (actual.unwrap(), stats)
        };
        assert_eq!(actual, expected.unwrap());
        assert_eq!(actual_stats, expected_stats);
        assert_eq!(actual_stats.total, 1);
        assert_eq!(actual.dynamic_configs.len(), 1);
    }
}

#[test]
fn ordinary_handoff_preserves_root_and_spec_depth_boundaries() {
    let mut accepted_root = false;
    let mut rejected_root = false;
    for depth in 123..=129 {
        let nested = format!("{}0{}", "[".repeat(depth), "]".repeat(depth));
        for root in [false, true] {
            let ordinary_value = format!(r#"{{"nested":{nested}}}"#);
            let value = if root { "{}" } else { &ordinary_value };
            let extra = if root {
                format!(r#", "sdk_configs":{{"nested":{nested}}}"#)
            } else {
                String::new()
            };
            let source = response(&format!(r#""ordinary":{}"#, ordinary(value)), &extra);
            let options = SpecsResponseParseOptions::default();
            let (expected, expected_stats) = scoped(options, || previous_roundtrip(&source));
            let (actual, actual_stats) = scoped(options, || candidate(&source, false));
            assert_eq!(actual_stats, expected_stats, "root={root}, depth={depth}");
            match (expected, actual) {
                (Ok(expected), Ok((actual, _))) => {
                    assert_eq!(actual, expected, "root={root}, depth={depth}");
                    accepted_root |= root;
                }
                (
                    Err(StatsigErr::JsonParseError(expected_tag, expected)),
                    Err(StatsigErr::JsonParseError(actual_tag, actual)),
                ) => {
                    assert_eq!(actual_tag, expected_tag);
                    assert!(expected.contains("recursion limit exceeded"));
                    assert!(actual.contains("recursion limit exceeded"));
                    rejected_root |= root;
                }
                _ => panic!("parse acceptance changed: root={root}, depth={depth}"),
            }
        }
    }
    assert!(accepted_root && rejected_root);
}

#[test]
fn ordinary_handoff_collapses_escaped_aliases_before_decoding() {
    for (first, last, expected_count) in [
        (ordinary(r#"{"value":1}"#), ordinary(r#"{"value":2}"#), 1),
        (ordinary(r#"{"value":1}"#), "{}".to_owned(), 0),
        ("{}".to_owned(), ordinary(r#"{"value":2}"#), 1),
    ] {
        let source = response(&format!(r#""alias":{first},"\u0061lias":{last}"#), "");
        let options = SpecsResponseParseOptions::default();
        let (expected, expected_stats) = scoped(options, || previous_roundtrip(&source));
        let (actual, actual_stats) = scoped(options, || candidate(&source, false));
        let (actual, _) = actual.unwrap();
        assert_eq!(actual, expected.unwrap());
        assert_eq!(actual.dynamic_configs.len(), expected_count);
        assert_eq!(actual_stats, expected_stats);
        assert_eq!(actual_stats.total, expected_count);
    }
}

#[test]
fn ordinary_handoff_persists_lexemes_and_omits_skipped_specs() {
    const LEXEMES: &str = r#"{"negative_zero":-0.0,"large":123456789012345678901234567890.00001,"exponent":1.25000e+02}"#;
    let source = response(
        &format!(r#""ordinary":{},"malformed":{{}}"#, ordinary(LEXEMES)),
        "",
    );
    let ((snapshot, mut data), _) = {
        let (result, stats) = scoped(SpecsResponseParseOptions::default(), || {
            candidate(&source, true)
        });
        (result.unwrap(), stats)
    };
    data.rewind().unwrap();
    let mut persisted = String::new();
    data.get_stream_mut()
        .read_to_string(&mut persisted)
        .unwrap();
    assert!(persisted.contains(LEXEMES));
    assert!(!persisted.contains("malformed"));
    let (reloaded, _) = scoped(SpecsResponseParseOptions::default(), || {
        serde_json::from_str::<SpecsResponseFull>(&persisted).unwrap()
    });
    assert_eq!(*snapshot, reloaded);
}

#[test]
fn raw_dynamic_config_helper_preserves_metadata_rejection_and_preload_policy() {
    let raw = to_raw_value(&json!({"remoteConfigMetadata": {}})).unwrap();
    let raw_map = || {
        [(InternedString::from_str_ref("unhydrated"), raw.as_ref())]
            .into_iter()
            .collect()
    };
    for options in [
        SpecsResponseParseOptions::default(),
        SpecsResponseParseOptions::preserving_session_update_mode(),
    ] {
        let (actual, _) = scoped(options, || {
            decode_raw_dynamic_configs::<serde_json::Error, _>(raw_map())
        });
        let error = actual.unwrap_err();
        assert!(
            error
                .to_string()
                .contains("Remote config metadata reached the JSON decoder before hydration")
        );
        let encoded = format!(r#"{{"unhydrated":{}}}"#, raw.get());
        let expected = serde_json::from_str::<SpecsHashMap>(&encoded).unwrap_err();
        assert_eq!(error.classify(), expected.classify());
    }
    let (actual, stats) = scoped(SpecsResponseParseOptions::for_shared_preload(), || {
        decode_raw_dynamic_configs::<serde_json::Error, _>(raw_map())
    });
    assert!(actual.unwrap().is_empty());
    assert_eq!(stats.total, 0);
}
