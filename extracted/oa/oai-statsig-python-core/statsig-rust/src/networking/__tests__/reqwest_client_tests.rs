use super::{configured_reqwest_client_builder, root_store, tls_config};

const CUSTOM_CA: &[u8] = include_bytes!("../../../tests/data/event_upload_test_ca.pem");

#[test]
fn mozilla_anchor_constraints_are_preserved() {
    let roots = root_store(None, false).unwrap();
    assert_eq!(roots.roots.as_slice(), webpki_roots::TLS_SERVER_ROOTS);
    assert!(roots.roots.iter().any(|root| {
        root.name_constraints
            .as_ref()
            .is_some_and(|constraints| constraints.as_ref() == b"\xa0\x070\x05\x82\x03.tr")
    }));
}

#[test]
fn custom_ca_is_additive_without_changing_mozilla_anchors() {
    let roots = root_store(Some(CUSTOM_CA), false).unwrap();
    let bundled = webpki_roots::TLS_SERVER_ROOTS;
    assert_eq!(&roots.roots[..bundled.len()], bundled);
    assert_eq!(roots.len(), bundled.len() + 1);
    configured_reqwest_client_builder(Some(CUSTOM_CA), false)
        .unwrap()
        .build()
        .unwrap();
}

#[test]
fn alpn_preserves_normal_and_http2_only_modes() {
    assert_eq!(
        tls_config(None, false).unwrap().alpn_protocols,
        [b"h2".to_vec(), b"http/1.1".to_vec()]
    );
    assert_eq!(
        tls_config(None, true).unwrap().alpn_protocols,
        [b"h2".to_vec()]
    );
}

#[test]
fn custom_ca_validation_preserves_empty_bundle_policy() {
    assert!(root_store(Some(b""), false).is_ok());
    assert!(
        root_store(Some(b""), true)
            .unwrap_err()
            .contains("no certificates")
    );
    assert!(
        root_store(
            Some(b"-----BEGIN CERTIFICATE-----\n!!!!\n-----END CERTIFICATE-----"),
            false
        )
        .is_err()
    );
    assert!(
        root_store(
            Some(b"-----BEGIN CERTIFICATE-----\nAAAA\n-----END CERTIFICATE-----"),
            false
        )
        .is_err()
    );
}
