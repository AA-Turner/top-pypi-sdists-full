use super::*;

#[test]
fn json_preparation_preserves_ordinary_raw_specs_beside_escaped_remote_metadata() {
    let blob = Blob::new(br#"{"remote":"value"}"#);
    let remote = serde_json::to_string(&remote_config(&blob))
        .unwrap()
        .replace("remoteConfigMetadata", r#"\u0072emoteConfigMetadata"#);
    let ordinary = [
        ("scalar", "null"),
        (
            "malformed_rules",
            r#"{"rules":[null,7,{}],"defaultValue":-0}"#,
        ),
        (
            "precise",
            r#"{"defaultValue":0.123456789012345678901,"rules":[]}"#,
        ),
        (
            "marker_value",
            r#"{"defaultValue":"remoteConfigMetadata","rules":[]}"#,
        ),
        ("unicode_value", r#"{"defaultValue":"\u0061","rules":[]}"#),
    ];
    let configs = ordinary
        .iter()
        .map(|(name, raw)| format!(r#""{name}":{raw}"#))
        .chain(std::iter::once(format!(r#""remote":{remote}"#)))
        .collect::<Vec<_>>()
        .join(",");
    let wire = full_wire(&format!("{{{configs}}}"));
    let hydrator = test_hydrator("json-discovery-filter");
    for mut data in [
        ResponseData::from_shared_bytes_with_headers(Arc::from(wire.as_slice()), None),
        ResponseData::from_stream(Box::new(Cursor::new(wire.clone()))),
    ] {
        let mut result = HydrationResult::new(&hydrator);
        let input = parse_json_hydration_input(
            &mut data,
            "https://example.com/v2/download_config_specs/key.json",
            &mut result,
        )
        .unwrap()
        .unwrap();
        assert_eq!(input.references.len(), 1);
        assert_eq!(input.references[0].metadata.sha256.as_str(), blob.sha);
        assert_eq!(input.configs.len(), ordinary.len() + 1);
        for (name, raw) in ordinary {
            let config = input
                .configs
                .iter()
                .find(|entry| entry.name == name)
                .unwrap();
            assert!(!config.use_remote_decoder, "ordinary config: {name}");
            assert_eq!(config.raw_spec.get(), raw);
        }
        assert!(input.configs.last().unwrap().use_remote_decoder);
    }
}
