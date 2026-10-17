use super::*;
use crate::networking::NetworkClient;
use crate::observability::ops_stats::OPS_STATS;
use std::io::Cursor;

use serde_json::{Value, json};
use sha2::{Digest, Sha256};
use wiremock::matchers::{method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

#[path = "json_hydration_discovery_filter_tests.rs"]
mod discovery_filter;

#[derive(Clone, Copy, Debug)]
enum Entrypoint {
    Rewrite,
    Store,
}

#[test]
fn json_preparation_shared_and_stream_parsers_preserve_raw_values() {
    for (input, expected) in [
        (
            r#" {"zero":-0,"precise":0.123456789012345678901,"exponent":1e140} "#,
            Some(r#"{"zero":-0,"precise":0.123456789012345678901,"exponent":1e140}"#),
        ),
        (
            r#"{"first":null,"second":2,"first":-0,"nested":{ "a":1,"a":2,"array":[1e140, -0] }}"#,
            Some(r#"{"first":-0,"second":2,"nested":{ "a":1,"a":2,"array":[1e140, -0] }}"#),
        ),
        ("{}", Some("{}")),
        (r#" [ {"remoteConfigMetadata":null} ] "#, None),
        (r#""remoteConfigMetadata""#, None),
        ("null", None),
        ("true", None),
        ("-0", None),
    ] {
        for mut data in [
            ResponseData::from_shared_bytes_with_headers(Arc::from(input.as_bytes()), None),
            ResponseData::from_stream(Box::new(Cursor::new(input.as_bytes().to_vec()))),
        ] {
            // Parsing starts at the beginning even if an earlier probe read bytes.
            data.get_stream_mut().read_exact(&mut [0; 1]).unwrap();
            let parsed = parse_raw_json_object_from_response(&mut data)
                .unwrap()
                .map(|object| serde_json::to_string(&object).unwrap());
            assert_eq!(parsed.as_deref(), expected, "input: {input}");
        }
    }
}

#[test]
fn json_preparation_shared_and_stream_parsers_reject_invalid_json() {
    for input in [
        "",
        "   ",
        r#"{"value":}"#,
        r#"{"value":1"#,
        r#"{"value":01}"#,
        r#"{"value":1,}"#,
        r#"{"value":"\uZZZZ"}"#,
        r#"{} trailing"#,
        r#"{} {}"#,
        "[1,]",
        "null trailing",
    ] {
        for mut data in [
            ResponseData::from_shared_bytes_with_headers(Arc::from(input.as_bytes()), None),
            ResponseData::from_stream(Box::new(Cursor::new(input.as_bytes().to_vec()))),
        ] {
            assert!(
                matches!(
                    parse_raw_json_object_from_response(&mut data),
                    Err(StatsigErr::JsonParseError(ref tag, _)) if tag == TAG
                ),
                "input must fail with the hydration JSON error tag: {input}",
            );
        }
    }
}

fn test_hydrator(instance_id: &str) -> RemoteConfigValueHydrator {
    RemoteConfigValueHydrator::new_with_ops_stats(
        Arc::new(NetworkClient::new("secret-json-preparation", None, None)),
        OPS_STATS.get_for_instance(instance_id),
    )
}

struct Blob {
    body: Vec<u8>,
    sha: String,
}

impl Blob {
    fn new(body: &[u8]) -> Self {
        Self {
            body: body.to_vec(),
            sha: Sha256::digest(body)
                .iter()
                .map(|byte| format!("{byte:02x}"))
                .collect(),
        }
    }

    fn path(&self) -> String {
        format!("/v1/dynamic_config_value/{}", self.sha)
    }

    fn metadata(&self) -> Value {
        json!({
            "sha256": self.sha,
            "byteLength": self.body.len(),
            "contentType": "application/json",
            "compression": "none",
        })
    }

    fn placeholder(&self) -> Value {
        json!({"value": self.path()})
    }

    async fn mount(&self, server: &MockServer, expected_requests: u64) {
        Mock::given(method("GET"))
            .and(path(self.path()))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(self.body.clone()),
            )
            .expect(expected_requests)
            .mount(server)
            .await;
    }
}

fn rule(id: &str, value: Value) -> Value {
    json!({
        "name": id,
        "id": id,
        "salt": "json-preparation",
        "idType": "userID",
        "passPercentage": 100,
        "conditions": [],
        "returnValue": value,
    })
}

fn config(value: Value, rules: Vec<Value>) -> Value {
    json!({
        "type": "dynamic_config",
        "salt": "json-preparation",
        "enabled": true,
        "idType": "userID",
        "entity": "dynamic_config",
        "defaultValue": value,
        "rules": rules,
    })
}

fn remote_config(blob: &Blob) -> Value {
    let mut config = config(blob.placeholder(), Vec::new());
    config["remoteConfigMetadata"] = blob.metadata();
    config
}

fn full_wire(raw_configs: &str) -> Vec<u8> {
    // Supply the full-response fields without parsing the caller's raw values.
    serde_json::to_string(&SpecsResponseFull::default())
        .unwrap()
        .replace(
            r#""dynamic_configs":{}"#,
            &format!(r#""before":-0,"dynamic_configs":{raw_configs},"after":1e140"#),
        )
        .into_bytes()
}

async fn hydrate(
    entrypoint: Entrypoint,
    hydrator: &RemoteConfigValueHydrator,
    data: &mut ResponseData,
    source_url: &str,
    current_verified_values: &VerifiedRemoteConfigValues,
    capture_data_store_bytes: bool,
) -> Result<Option<(Value, VerifiedRemoteConfigValues)>, StatsigErr> {
    let mut result = HydrationResult::new(hydrator);
    match entrypoint {
        Entrypoint::Rewrite => {
            if hydrate_response(hydrator, data, source_url, &mut result).await? {
                Ok(Some((
                    data.deserialize_into()?,
                    VerifiedRemoteConfigValues::new(),
                )))
            } else {
                Ok(None)
            }
        }
        Entrypoint::Store => hydrate_response_for_store(
            hydrator,
            data,
            JsonStoreHydrationContext {
                source_url,
                current_verified_values,
                mmap_project_id: MmapProjectId::for_sdk_key("json-preparation"),
                preserve_session_update_mode: false,
                capture_data_store_bytes,
                response_has_updates: None,
            },
            &mut result,
        )
        .await
        .map(|update| {
            update.map(|update| {
                (
                    serde_json::to_value(update.values).unwrap(),
                    update.verified_remote_values,
                )
            })
        }),
    }
}

#[tokio::test]
async fn json_preparation_noop_rewinds_both_entrypoints_without_changing_bytes() {
    let server = MockServer::start().await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("json-preparation-noop");
    let current = VerifiedRemoteConfigValues::new();
    let payloads = [
        br#" {"dynamic_configs":{"inline":{"defaultValue":{"number":-0},"rules":[]}}} "#.as_slice(),
        br#"{"message":"remote\u0043onfigMetadata","dynamic_configs":null}"#.as_slice(),
        br#"{"nested":{"remoteConfigMetadata":null},"dynamic_configs":[]}"#.as_slice(),
        br#" [ {"remoteConfigMetadata":null} ] "#.as_slice(),
    ];

    for entrypoint in [Entrypoint::Rewrite, Entrypoint::Store] {
        for original in payloads {
            let mut data = ResponseData::from_stream(Box::new(Cursor::new(original.to_vec())));
            data.get_stream_mut().read_exact(&mut [0; 3]).unwrap();
            assert!(
                hydrate(
                    entrypoint,
                    &hydrator,
                    &mut data,
                    &source_url,
                    &current,
                    true
                )
                .await
                .unwrap()
                .is_none(),
                "{entrypoint:?}: payload had no dynamic-config references",
            );

            // Read directly: ResponseData::read_to_bytes would hide a missing rewind.
            let mut remaining = Vec::new();
            data.get_stream_mut().read_to_end(&mut remaining).unwrap();
            assert_eq!(remaining, original, "{entrypoint:?}: no-op must rewind");
        }
    }
    assert!(server.received_requests().await.unwrap().is_empty());
}

#[tokio::test]
async fn json_preparation_validates_later_metadata_before_either_entrypoint_downloads() {
    let server = MockServer::start().await;
    let blob = Blob::new(br#"{"value":"valid-first-reference"}"#);
    blob.mount(&server, 0).await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("json-preparation-validation");
    let current = VerifiedRemoteConfigValues::new();

    let mut invalid_default = config(blob.placeholder(), Vec::new());
    invalid_default["remoteConfigMetadata"] = Value::Null;
    let mut invalid_rule = rule("invalid-rule", blob.placeholder());
    invalid_rule["remoteConfigMetadata"] = blob.metadata();
    invalid_rule["remoteConfigMetadata"]["sha256"] = json!("bad-sha");
    let invalid_rule = config(json!({"default": "inline"}), vec![invalid_rule]);

    for entrypoint in [Entrypoint::Rewrite, Entrypoint::Store] {
        for (invalid_config, expected_reason) in [
            (&invalid_default, "invalid_default_metadata"),
            (&invalid_rule, "invalid_sha256"),
        ] {
            let original = full_wire(
                &serde_json::to_string(&json!({
                    "first": remote_config(&blob),
                    "later": invalid_config,
                }))
                .unwrap(),
            );
            let mut data = ResponseData::from_bytes(original.clone());
            let error = hydrate(
                entrypoint,
                &hydrator,
                &mut data,
                &source_url,
                &current,
                true,
            )
            .await
            .unwrap_err();
            assert!(
                matches!(error, StatsigErr::CustomError(ref message) if message.contains(expected_reason)),
                "{entrypoint:?}: unexpected validation error: {error:?}",
            );
            assert_eq!(data.read_to_bytes().unwrap(), original);
        }
    }
    server.verify().await;
    assert!(server.received_requests().await.unwrap().is_empty());
}

#[tokio::test]
async fn json_preparation_duplicate_keys_use_last_values_in_both_entrypoints() {
    for entrypoint in [Entrypoint::Rewrite, Entrypoint::Store] {
        let server = MockServer::start().await;
        let blob = Blob::new(br#"{"chosen":"last-value"}"#);
        blob.mount(&server, 1).await;
        let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
        let hydrator = test_hydrator("json-preparation-duplicates");
        let current = VerifiedRemoteConfigValues::new();
        let raw_config = format!(
            r#"{{"type":"dynamic_config","salt":"json-preparation","enabled":true,"idType":"userID","entity":"dynamic_config","rules":[],"defaultValue":null,"defaultValue":{{"value":"{path}"}},"remoteConfigMetadata":null,"remoteConfigMetadata":{{"sha256":"{sha}","byteLength":{length},"contentType":"application/json","compression":"none"}}}}"#,
            path = blob.path(),
            sha = blob.sha,
            length = blob.body.len(),
        );
        let raw_configs = format!(r#"{{"selected":null,"selected":{raw_config}}}"#);
        let original = String::from_utf8(full_wire(&raw_configs))
            .unwrap()
            .replace(
                r#""before":-0,"dynamic_configs":"#,
                r#""before":-0,"dynamic_configs":{"discarded":{"remoteConfigMetadata":null}},"dynamic_configs":"#,
            );
        let mut data = ResponseData::from_bytes(original.into_bytes());
        let (hydrated, _) = hydrate(
            entrypoint,
            &hydrator,
            &mut data,
            &source_url,
            &current,
            true,
        )
        .await
        .unwrap()
        .unwrap();

        assert_eq!(hydrated["dynamic_configs"].as_object().unwrap().len(), 1);
        assert_eq!(
            hydrated["dynamic_configs"]["selected"]["defaultValue"],
            json!({"chosen": "last-value"}),
        );
        assert!(
            hydrated["dynamic_configs"]["selected"]
                .get("remoteConfigMetadata")
                .is_none()
        );
        if matches!(entrypoint, Entrypoint::Rewrite) {
            let rewritten = data.read_to_string().unwrap();
            let before = rewritten.find(r#""before":-0"#).unwrap();
            let configs = rewritten.find(r#""dynamic_configs":"#).unwrap();
            let after = rewritten.find(r#""after":1e140"#).unwrap();
            assert!(before < configs && configs < after);
        }
        server.verify().await;
        assert_eq!(server.received_requests().await.unwrap().len(), 1);
    }
}

#[tokio::test]
async fn json_preparation_collects_malformed_rule_references_but_preserves_tolerant_classification()
{
    let server = MockServer::start().await;
    let blob = Blob::new(br#"{"value":"remote-rule"}"#);
    blob.mount(&server, 8).await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("json-preparation-malformed-rules");
    let current = VerifiedRemoteConfigValues::new();

    for (default_is_remote, malformed_rule_first) in
        [(false, false), (false, true), (true, false), (true, true)]
    {
        let mut remote_rule = rule("remote-rule", blob.placeholder());
        remote_rule["remoteConfigMetadata"] = blob.metadata();
        let malformed_rule = json!("not-a-rule-object");
        let rules = if malformed_rule_first {
            vec![malformed_rule, remote_rule]
        } else {
            vec![remote_rule, malformed_rule]
        };
        let mut malformed_config = config(json!({"default": "inline"}), rules);
        if default_is_remote {
            malformed_config["defaultValue"] = blob.placeholder();
            malformed_config["remoteConfigMetadata"] = blob.metadata();
        }
        let raw_unknown =
            r#"{ "precise": 0.123456789012345678901, "negativeZero": -0, "exponent": 1e140 }"#;
        let mut ordinary_config = config(json!({"kept": true}), Vec::new());
        ordinary_config["unknown"] = json!("__raw_malformed_neighbor__");
        let original = full_wire(
            &serde_json::to_string(&json!({
                "malformed": malformed_config,
                "ordinary": ordinary_config,
            }))
            .unwrap(),
        );
        let original = String::from_utf8(original)
            .unwrap()
            .replace(r#""__raw_malformed_neighbor__""#, raw_unknown)
            .into_bytes();
        let mut probe = ResponseData::from_bytes(original.clone());
        let mut result = HydrationResult::new(&hydrator);
        let prepared = parse_json_hydration_input(&mut probe, &source_url, &mut result)
            .unwrap()
            .unwrap();
        assert_eq!(prepared.references.len(), 1);
        assert_eq!(
            prepared.reference_count,
            if default_is_remote { 2 } else { 1 }
        );
        let malformed = prepared
            .configs
            .iter()
            .find(|config| config.name == "malformed")
            .unwrap();
        assert_eq!(malformed.use_remote_decoder, default_is_remote);

        for capture_data_store_bytes in [false, true] {
            let mut data = ResponseData::from_bytes(original.clone());
            let (hydrated, verified) = hydrate(
                Entrypoint::Store,
                &hydrator,
                &mut data,
                &source_url,
                &current,
                capture_data_store_bytes,
            )
            .await
            .unwrap()
            .unwrap();
            assert!(hydrated["dynamic_configs"].get("malformed").is_none());
            assert_eq!(
                hydrated["dynamic_configs"]["ordinary"]["defaultValue"],
                json!({"kept": true})
            );
            assert!(
                verified.is_empty(),
                "skipped configs must not publish provenance"
            );
            if capture_data_store_bytes {
                let persisted = data.read_to_string().unwrap();
                assert!(
                    !persisted.contains("remoteConfigMetadata"),
                    "writable snapshot retained remote metadata in skipped malformed config \
                     (default_is_remote={default_is_remote}, malformed_rule_first={malformed_rule_first})",
                );
                assert!(
                    !persisted.contains(&blob.path()),
                    "writable snapshot retained a remote placeholder in skipped malformed config",
                );
                let persisted = serde_json::from_str::<RawJsonObject>(&persisted).unwrap();
                let configs =
                    parse_optional_raw_json_object(persisted.get("dynamic_configs").unwrap())
                        .unwrap()
                        .unwrap();
                assert!(!configs.contains_key("malformed"));
                let ordinary = parse_optional_raw_json_object(configs.get("ordinary").unwrap())
                    .unwrap()
                    .unwrap();
                assert_eq!(ordinary.get("unknown").unwrap().get(), raw_unknown);
            } else {
                assert_eq!(data.read_to_bytes().unwrap(), original);
            }
        }
    }
    server.verify().await;
    assert_eq!(server.received_requests().await.unwrap().len(), 8);
}

#[tokio::test]
async fn json_hydration_remote_specs_skip_invalid_fields_without_dropping_neighbors() {
    let server = MockServer::start().await;
    let blob = Blob::new(br#"{"remote":"hydrated"}"#);
    blob.mount(&server, 4).await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("json-hydration-invalid-fields");
    let mut invalid_type = remote_config(&blob);
    invalid_type["enabled"] = json!("true");
    let mut missing_field = remote_config(&blob);
    missing_field.as_object_mut().unwrap().remove("idType");

    for capture_data_store_bytes in [false, true] {
        for malformed in [&invalid_type, &missing_field] {
            let original = full_wire(
                &serde_json::to_string(&json!({
                    "malformed": malformed,
                    "remote": remote_config(&blob),
                    "ordinary": config(json!({"kept": true}), Vec::new()),
                }))
                .unwrap(),
            );
            let mut data = ResponseData::from_bytes(original.clone());
            let (hydrated, verified) = hydrate(
                Entrypoint::Store,
                &hydrator,
                &mut data,
                &source_url,
                &VerifiedRemoteConfigValues::new(),
                capture_data_store_bytes,
            )
            .await
            .unwrap()
            .unwrap();

            assert_eq!(hydrated["dynamic_configs"].as_object().unwrap().len(), 2);
            assert!(hydrated["dynamic_configs"].get("malformed").is_none());
            assert_eq!(
                hydrated["dynamic_configs"]["ordinary"]["defaultValue"],
                json!({"kept": true}),
            );
            assert_eq!(
                hydrated["dynamic_configs"]["remote"]["defaultValue"],
                json!({"remote": "hydrated"}),
            );
            assert_eq!(verified.len(), 1);
            assert!(!verified.contains_key(&InternedString::from_str_ref("malformed")));

            if capture_data_store_bytes {
                let persisted: Value = data.deserialize_into().unwrap();
                assert!(persisted["dynamic_configs"].get("malformed").is_none());
            } else {
                assert_eq!(data.read_to_bytes().unwrap(), original);
            }
        }
    }
    server.verify().await;
}

#[tokio::test]
async fn json_hydration_remote_default_preserves_ordinary_rule_array_bytes() {
    let server = MockServer::start().await;
    let blob = Blob::new(br#"{"remote":"hydrated"}"#);
    blob.mount(&server, 2).await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("json-hydration-ordinary-rule-bytes");
    let raw_rules = r#"[
  { "name" : "inline", "id" : "inline", "salt" : "json-preparation",
    "idType" : "userID", "passPercentage" : 100, "conditions" : [],
    "returnValue" : { "precise" : 0.123456789012345678901, "negativeZero" : -0,
                      "duplicate" : "first", "duplicate" : "last" },
    "unknown" : { "number" : 1e140, "number" : 1e9999 } }
]"#;
    let raw_unknown = r#"{ "number" : -0, "duplicate" : 1, "duplicate" : 1e140 }"#;
    let raw_config = serde_json::to_string(&remote_config(&blob))
        .unwrap()
        .replace(
            r#""rules":[]"#,
            &format!(r#""rules":{raw_rules},"unknown":{raw_unknown}"#),
        );
    let original = full_wire(&format!(r#"{{"remote_default":{raw_config}}}"#));

    for capture_data_store_bytes in [false, true] {
        let mut data = ResponseData::from_bytes(original.clone());
        let (hydrated, verified) = hydrate(
            Entrypoint::Store,
            &hydrator,
            &mut data,
            &source_url,
            &VerifiedRemoteConfigValues::new(),
            capture_data_store_bytes,
        )
        .await
        .unwrap()
        .unwrap();

        let hydrated = &hydrated["dynamic_configs"]["remote_default"];
        assert_eq!(hydrated["defaultValue"], json!({"remote": "hydrated"}));
        assert_eq!(hydrated["rules"][0]["returnValue"]["duplicate"], "last");
        assert_eq!(verified.len(), 1);
        if capture_data_store_bytes {
            let persisted =
                serde_json::from_slice::<RawJsonObject>(&data.read_to_bytes().unwrap()).unwrap();
            let configs = parse_optional_raw_json_object(persisted.get("dynamic_configs").unwrap())
                .unwrap()
                .unwrap();
            let config = parse_optional_raw_json_object(configs.get("remote_default").unwrap())
                .unwrap()
                .unwrap();
            assert_eq!(config.get("rules").unwrap().get(), raw_rules);
            assert_eq!(config.get("unknown").unwrap().get(), raw_unknown);
            assert!(!config.contains_key("remoteConfigMetadata"));
        } else {
            assert_eq!(data.read_to_bytes().unwrap(), original);
        }
    }
    server.verify().await;
}

#[test]
fn json_hydration_store_preserves_full_response_recursion_boundary() {
    let blob = Blob::new(br#"{"remote":"hydrated"}"#);
    let hydrator = test_hydrator("json-hydration-root-depth");
    let source_url = "https://example.com/v2/download_config_specs/key.json";
    let downloaded_bodies = HashMap::from([(blob.sha.clone(), Arc::new(blob.body.clone()))]);
    let incoming_configs = serde_json::to_string(&json!({
        "remote": remote_config(&blob),
        "ordinary": config(json!({"kept": true}), Vec::new()),
    }))
    .unwrap();
    let hydrated_configs = serde_json::to_string(&json!({
        "remote": config(json!({"remote": "hydrated"}), Vec::new()),
        "ordinary": config(json!({"kept": true}), Vec::new()),
    }))
    .unwrap();

    for depth in [126, 127, 128] {
        let nested = format!("{}0{}", "[".repeat(depth), "]".repeat(depth));
        let wire = |configs: &str| {
            String::from_utf8(full_wire(configs))
                .unwrap()
                .replace(
                    r#""before":-0,"#,
                    &format!(r#""before":-0,"app_id":{nested},"#),
                )
                .into_bytes()
        };
        // app_id is a typed root field; its arrays share the response object's
        // recursion budget even while the remote specs are decoded separately.
        let baseline = serde_json::from_slice::<SpecsResponseFull>(&wire(&hydrated_configs));
        assert_eq!(baseline.is_ok(), depth == 126, "baseline depth {depth}");

        let original = wire(&incoming_configs);
        let mut data = ResponseData::from_bytes(original.clone());
        let mut result = HydrationResult::new(&hydrator);
        let input = parse_json_hydration_input(&mut data, source_url, &mut result)
            .unwrap()
            .unwrap();
        let candidate = build_hydrated_json_snapshot(
            input,
            &mut data,
            VerifiedRemoteValues::new(),
            downloaded_bodies.clone(),
            false,
        );
        assert_eq!(candidate.is_ok(), baseline.is_ok(), "store depth {depth}");
        if let Err(error) = candidate {
            assert!(
                matches!(error, StatsigErr::JsonParseError(_, ref message) if message.contains("recursion limit exceeded")),
                "store depth {depth}: unexpected error: {error:?}",
            );
        }
        assert_eq!(data.read_to_bytes().unwrap(), original);
    }
}

#[tokio::test]
async fn json_preparation_sparse_remote_rules_keep_positions_and_raw_numeric_sidecar() {
    let server = MockServer::start().await;
    let first =
        Blob::new(br#"{"remote":"first","precise":0.123456789012345678901,"negativeZero":-0}"#);
    let second = Blob::new(br#"{"remote":"second","exponent":1e140}"#);
    first.mount(&server, 1).await;
    second.mount(&server, 1).await;
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let hydrator = test_hydrator("json-preparation-sparse-rules");
    let mut first_remote = rule("remote-first", first.placeholder());
    first_remote["remoteConfigMetadata"] = first.metadata();
    let mut second_remote = rule("remote-second", second.placeholder());
    second_remote["remoteConfigMetadata"] = second.metadata();
    let raw_configs = serde_json::to_string(&json!({
        "mixed": config(json!({"default": "inline"}), vec![
            rule("inline-first", json!({"inline": "first", "inlineNumber": "__raw_negative_zero__"})),
            first_remote,
            rule("inline-second", json!({"inline": "second"})),
            second_remote,
        ]),
    }))
    .unwrap()
    .replace(r#""__raw_negative_zero__""#, "-0");
    let original = full_wire(&raw_configs);
    let mut data = ResponseData::from_shared_bytes_with_headers(Arc::from(original.clone()), None);
    let (first_snapshot, verified) = hydrate(
        Entrypoint::Store,
        &hydrator,
        &mut data,
        &source_url,
        &VerifiedRemoteConfigValues::new(),
        true,
    )
    .await
    .unwrap()
    .unwrap();
    let rules = &first_snapshot["dynamic_configs"]["mixed"]["rules"];
    assert_eq!(rules.as_array().unwrap().len(), 4);
    for (index, id, field, value) in [
        (0, "inline-first", "inline", "first"),
        (1, "remote-first", "remote", "first"),
        (2, "inline-second", "inline", "second"),
        (3, "remote-second", "remote", "second"),
    ] {
        assert_eq!(rules[index]["id"], id);
        assert_eq!(rules[index]["returnValue"][field], value);
    }
    assert_eq!(
        first_snapshot["dynamic_configs"]["mixed"]["defaultValue"],
        json!({"default": "inline"})
    );
    assert_eq!(
        rules[1]["returnValue"]["precise"].as_f64(),
        serde_json::from_slice::<Value>(&first.body).unwrap()["precise"].as_f64(),
    );
    let sidecar = data.read_to_string().unwrap();
    for lexeme in [
        r#""inlineNumber":-0"#,
        r#""precise":0.123456789012345678901"#,
        r#""negativeZero":-0"#,
        r#""exponent":1e140"#,
    ] {
        assert!(sidecar.contains(lexeme), "sidecar changed {lexeme}");
    }
    assert!(!sidecar.contains("remoteConfigMetadata"));
    let sidecar: Value = serde_json::from_str(&sidecar).unwrap();
    for index in 0..4 {
        assert_eq!(
            sidecar["dynamic_configs"]["mixed"]["rules"][index]["id"],
            rules[index]["id"]
        );
        // Compare decoded SDK values separately from the exact wire numbers above.
        let sidecar_value: crate::DynamicReturnable = serde_json::from_str(
            &sidecar["dynamic_configs"]["mixed"]["rules"][index]["returnValue"].to_string(),
        )
        .unwrap();
        assert_eq!(
            serde_json::to_value(sidecar_value).unwrap(),
            rules[index]["returnValue"]
        );
    }

    // A read-only update can reuse numeric parsed values without fetching bodies
    // solely for their original numeric spelling.
    let mut data = ResponseData::from_shared_bytes_with_headers(Arc::from(original.clone()), None);
    let (next_snapshot, _) = hydrate(
        Entrypoint::Store,
        &hydrator,
        &mut data,
        &source_url,
        &verified,
        false,
    )
    .await
    .unwrap()
    .unwrap();
    assert_eq!(next_snapshot, first_snapshot);
    assert_eq!(data.read_to_bytes().unwrap(), original);
    server.verify().await;
    assert_eq!(server.received_requests().await.unwrap().len(), 2);
}
