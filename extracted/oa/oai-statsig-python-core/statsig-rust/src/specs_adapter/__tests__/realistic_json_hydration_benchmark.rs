use super::*;
use serde::Deserialize;
use std::collections::{BTreeMap, BTreeSet};
use std::hint::black_box;
use std::path::Path;
use std::time::Instant;

#[derive(Deserialize)]
struct Manifest {
    schema_version: Option<u32>,
    scenarios: Vec<Scenario>,
    blobs: Vec<BlobFile>,
}

#[derive(Deserialize)]
struct Scenario {
    name: String,
    file: String,
    bytes: usize,
    sha256: String,
    configs: usize,
    entities: BTreeMap<String, usize>,
    rules: BTreeMap<String, usize>,
    references: usize,
    unique_references: usize,
    unique_shas: Vec<String>,
    remote_configs: usize,
}

#[derive(Deserialize)]
struct BlobFile {
    file: String,
    bytes: usize,
    sha256: String,
}

fn digest(bytes: &[u8]) -> String {
    Sha256::digest(bytes)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect()
}

fn has_number(value: &Value) -> bool {
    match value {
        Value::Number(_) => true,
        Value::Array(values) => values.iter().any(has_number),
        Value::Object(values) => values.values().any(has_number),
        _ => false,
    }
}

fn response(bytes: &Arc<[u8]>, shared: bool) -> ResponseData {
    if shared {
        ResponseData::from_shared_bytes_with_headers(Arc::clone(bytes), None)
    } else {
        ResponseData::from_stream(Box::new(Cursor::new(Arc::clone(bytes))))
    }
}

fn load_fixture(root: &Path, scenario: &Scenario) -> Arc<[u8]> {
    let bytes = std::fs::read(root.join(&scenario.file)).unwrap();
    assert_eq!(bytes.len(), scenario.bytes);
    assert_eq!(digest(&bytes), scenario.sha256);
    println!(
        "FIXTURE {}",
        json!({"name": scenario.name, "bytes": bytes.len(), "sha256": scenario.sha256})
    );
    bytes.into()
}

fn canonical_digest(encoded: &[u8]) -> String {
    let mut value: Value = serde_json::from_slice(encoded).unwrap();
    value.sort_all_objects();
    digest(&serde_json::to_vec(&value).unwrap())
}

fn check_snapshot(snapshot: &SpecsResponseFull, scenario: &Scenario) -> String {
    assert_eq!(snapshot.dynamic_configs.len(), scenario.configs);
    let encoded = serde_json::to_vec(snapshot).unwrap();
    for marker in [
        b"remoteConfigMetadata".as_slice(),
        b"/v1/dynamic_config_value/".as_slice(),
    ] {
        assert!(
            !encoded.windows(marker.len()).any(|window| window == marker),
            "unhydrated reference remains"
        );
    }
    for (name, entities) in [
        ("feature_gates", &snapshot.feature_gates),
        ("dynamic_configs", &snapshot.dynamic_configs),
        ("layer_configs", &snapshot.layer_configs),
    ] {
        assert_eq!(
            entities.len(),
            scenario.entities[name],
            "entity count: {name}"
        );
        let rule_count: usize = entities
            .iter()
            .map(|(_, spec)| spec.as_spec_ref().rules.len())
            .sum();
        assert_eq!(rule_count, scenario.rules[name], "rule count: {name}");
    }
    canonical_digest(&encoded)
}

#[tokio::test]
#[ignore = "explicit synthetic release benchmark; see benchmarking/json_hydration/README.md"]
async fn realistic_json_hydration_benchmark() {
    assert!(
        !black_box(cfg!(debug_assertions)),
        "benchmark requires --release"
    );
    let manifest_path = std::env::var("STATSIG_BENCH_MANIFEST").unwrap();
    let manifest_path = Path::new(&manifest_path);
    let root = manifest_path.parent().unwrap();
    let manifest: Manifest =
        serde_json::from_slice(&std::fs::read(manifest_path).unwrap()).unwrap();
    let case = std::env::var("STATSIG_BENCH_CASE").unwrap();
    // Older bundles have a dedicated seed. Keep its fixture identity when replaying them.
    let sequence_seed = if manifest.schema_version == Some(2)
        && !manifest.scenarios.iter().any(|s| s.name == "sequence_seed")
    {
        "remote_observed"
    } else {
        "sequence_seed"
    };
    // Each process measures precisely one case. Growth starts from the changed
    // snapshot, so its new-reference count matches the declared sequence.
    let (phase, target_name, seed_name, shared, capture) = match case.as_str() {
        "raw_shared" => ("raw_parse", "remote_observed", None, true, false),
        "raw_stream" => ("raw_parse", "remote_observed", None, false, false),
        "prepare_shared" => ("prepare", "remote_observed", None, true, false),
        "prepare_stream" => ("prepare", "remote_observed", None, false, false),
        "prepare_early" => ("prepare", "remote_early", None, true, false),
        "prepare_late" => ("prepare", "remote_late", None, true, false),
        "cold_shared" => ("snapshot", sequence_seed, None, true, false),
        "reuse_shared" => (
            "snapshot",
            "sequence_reuse",
            Some(sequence_seed),
            true,
            false,
        ),
        "reuse_stream" => (
            "snapshot",
            "sequence_reuse",
            Some(sequence_seed),
            false,
            false,
        ),
        "change_shared" => (
            "snapshot",
            "sequence_change",
            Some("sequence_reuse"),
            true,
            false,
        ),
        "growth_shared" => (
            "snapshot",
            "sequence_growth",
            Some("sequence_change"),
            true,
            false,
        ),
        "reuse_capture" => (
            "snapshot",
            "sequence_reuse",
            Some(sequence_seed),
            true,
            true,
        ),
        "ordinary_shared" => ("ordinary_fallback", "inline", None, true, false),
        "ordinary_stream" => ("ordinary_fallback", "inline", None, false, false),
        _ => panic!("unknown benchmark case: {case}"),
    };
    let find = |name: &str| {
        manifest
            .scenarios
            .iter()
            .find(|scenario| scenario.name == name)
            .unwrap()
    };
    let target = find(target_name);
    let bytes = load_fixture(root, target);
    let seed_scenario = seed_name.map(find);
    let seed_bytes = seed_scenario.map(|scenario| load_fixture(root, scenario));
    let server = MockServer::start().await;
    let hydrator = test_hydrator("realistic-json-benchmark");
    let source_url = format!("{}/v2/download_config_specs/key.json", server.uri());
    let mut numeric_shas = BTreeSet::new();
    let needed_shas: BTreeSet<_> = target
        .unique_shas
        .iter()
        .chain(
            seed_scenario
                .into_iter()
                .flat_map(|scenario| scenario.unique_shas.iter()),
        )
        .collect();
    // I/O, hashing, mock construction, and synthetic blob validation are untimed.
    for file in &manifest.blobs {
        if !needed_shas.contains(&file.sha256) {
            continue;
        }
        let body = std::fs::read(root.join(&file.file)).unwrap();
        assert_eq!(body.len(), file.bytes);
        assert_eq!(digest(&body), file.sha256);
        if has_number(&serde_json::from_slice::<Value>(&body).unwrap()) {
            numeric_shas.insert(file.sha256.as_str());
        }
        Mock::given(method("GET"))
            .and(path(format!("/v1/dynamic_config_value/{}", file.sha256)))
            .respond_with(
                ResponseTemplate::new(200)
                    .insert_header("content-type", "application/json")
                    .set_body_bytes(body),
            )
            .mount(&server)
            .await;
    }
    let empty = VerifiedRemoteConfigValues::new();
    let mut seed = None;
    let mut expected_paths = BTreeMap::<String, usize>::new();
    if let (Some(scenario), Some(seed_bytes)) = (seed_scenario, seed_bytes.as_ref()) {
        let mut data = response(seed_bytes, shared);
        let mut result = HydrationResult::new(&hydrator);
        let update = hydrate_response_for_store(
            &hydrator,
            &mut data,
            StoreHydrationOptions::new(
                &source_url,
                MmapProjectId::for_sdk_key("realistic-json-benchmark"),
            ),
            &empty,
            None,
            &mut result,
        )
        .await
        .unwrap()
        .unwrap();
        check_snapshot(&update.values, scenario);
        assert_eq!(update.verified_remote_values.len(), scenario.remote_configs);
        for sha in &scenario.unique_shas {
            *expected_paths
                .entry(format!("/v1/dynamic_config_value/{sha}"))
                .or_default() += 1;
        }
        seed = Some(update);
    }
    let current = seed
        .as_ref()
        .map(|update| &update.verified_remote_values)
        .unwrap_or(&empty);
    let seeded_shas: BTreeSet<_> = seed_scenario
        .into_iter()
        .flat_map(|scenario| scenario.unique_shas.iter())
        .collect();
    let missing: Vec<_> = target
        .unique_shas
        .iter()
        .filter(|sha| {
            !seeded_shas.contains(sha) || (capture && numeric_shas.contains(sha.as_str()))
        })
        .collect();
    let expected_downloads = if phase == "snapshot" {
        missing.len()
    } else {
        0
    };
    let mut previous_requests = server.received_requests().await.unwrap().len();
    assert_eq!(previous_requests, expected_paths.values().sum::<usize>());
    // Both warmup and measured operations start from the same retained seed.
    // Never feed warmup provenance into the measured churn/cold operation.
    for warmup in [true, false] {
        let mut data = response(&bytes, shared);
        let mut result = HydrationResult::new(&hydrator);
        let mut snapshot_sha256 = None;
        let mut persisted_sha256 = None;
        let started = Instant::now();
        let elapsed = match phase {
            "raw_parse" => {
                let parsed = black_box(
                    parse_raw_json_object_from_response(&mut data)
                        .unwrap()
                        .unwrap(),
                );
                let elapsed = started.elapsed();
                assert!(parsed.contains_key("dynamic_configs"));
                elapsed
            }
            "prepare" => {
                let input = black_box(
                    parse_json_hydration_input(&mut data, &source_url, &mut result)
                        .unwrap()
                        .unwrap(),
                );
                let elapsed = started.elapsed();
                assert_eq!(input.configs.len(), target.configs);
                assert_eq!(input.reference_count, target.references);
                assert_eq!(input.references.len(), target.unique_references);
                elapsed
            }
            _ => {
                let update = black_box(
                    hydrate_response_for_store(
                        &hydrator,
                        &mut data,
                        StoreHydrationOptions::new(
                            &source_url,
                            MmapProjectId::for_sdk_key("realistic-json-benchmark"),
                        )
                        .with_data_store_capture(capture),
                        current,
                        None,
                        &mut result,
                    )
                    .await
                    .unwrap(),
                );
                if phase == "ordinary_fallback" {
                    assert!(update.is_none());
                    let snapshot: SpecsResponseFull = black_box(data.deserialize_into().unwrap());
                    let elapsed = started.elapsed();
                    snapshot_sha256 = Some(check_snapshot(&snapshot, target));
                    elapsed
                } else {
                    let elapsed = started.elapsed();
                    let update = update.unwrap();
                    snapshot_sha256 = Some(check_snapshot(&update.values, target));
                    assert_eq!(update.verified_remote_values.len(), target.remote_configs);
                    assert_eq!(
                        update.spec_decode_stats.total,
                        target.entities.values().sum::<usize>()
                    );
                    if capture {
                        let persisted = data.read_to_bytes().unwrap();
                        persisted_sha256 = Some(canonical_digest(&persisted));
                        assert!(
                            !persisted
                                .windows(b"remoteConfigMetadata".len())
                                .any(|window| window == b"remoteConfigMetadata")
                        );
                        assert!(
                            !persisted
                                .windows(b"/v1/dynamic_config_value/".len())
                                .any(|window| window == b"/v1/dynamic_config_value/")
                        );
                    }
                    elapsed
                }
            }
        };
        let requests = server.received_requests().await.unwrap();
        assert_eq!(requests.len() - previous_requests, expected_downloads);
        previous_requests = requests.len();
        if phase == "snapshot" {
            for sha in &missing {
                *expected_paths
                    .entry(format!("/v1/dynamic_config_value/{sha}"))
                    .or_default() += 1;
            }
        }
        let mut actual_paths = BTreeMap::<String, usize>::new();
        for request in requests {
            *actual_paths
                .entry(request.url.path().to_owned())
                .or_default() += 1;
        }
        assert_eq!(actual_paths, expected_paths);
        if !warmup {
            println!(
                "BENCH {}",
                json!({"case": case, "phase": phase, "scenario": target_name,
                "ns": elapsed.as_nanos(), "downloads": expected_downloads,
                "shared": shared, "capture": capture, "bytes": target.bytes,
                "references": target.references, "unique_references": target.unique_references,
                    "snapshot_sha256": snapshot_sha256, "persisted_sha256": persisted_sha256})
            );
        }
    }
    // Keeping the original full snapshot alive models the currently serving
    // store and prevents provenance-only seeding from understating live memory.
    black_box(&seed);
}
