use super::*;
use crate::{IdListFileVersion, StatsigOptions};
use wiremock::matchers::{body_json, header, method, path};
use wiremock::{Mock, MockServer, ResponseTemplate};

const SDK_KEY: &str = "secret-test";
const ORIGINAL_ID: &str = "private-test/id ?#雪";

fn network_and_endpoint(proxy: &MockServer) -> (NetworkClient, String) {
    let options = StatsigOptions {
        id_lists_url: Some(proxy.uri()),
        ..Default::default()
    };
    (
        NetworkClient::with_sdk_headers(SDK_KEY, &options),
        membership_url(SDK_KEY, options.id_lists_url.as_deref())
            .unwrap()
            .into(),
    )
}

#[test]
fn uses_the_manifest_gateway_prefix_or_trusted_openai_default() {
    assert_eq!(
        membership_url(SDK_KEY, None).unwrap().as_str(),
        "https://statsigcdn.openai.com/v1/id_list_membership"
    );
    for (manifest, expected) in [
        ("/v1/get_id_lists?x=1#old", "/v1/id_list_membership"),
        (
            "/proxy/v1/get_id_lists/?x=1#old",
            "/proxy/v1/id_list_membership",
        ),
        (
            "/tenant/v1/get_id_lists/secret-test",
            "/tenant/v1/id_list_membership",
        ),
        (
            "/tenant/v1/get_id_lists/secret-test.json",
            "/tenant/v1/id_list_membership",
        ),
        ("/custom/manifest", "/v1/id_list_membership"),
    ] {
        let origin = "https://internal-sfp:5443";
        let url = membership_url("server-valid", Some(&format!("{origin}{manifest}"))).unwrap();
        assert_eq!(url.as_str(), format!("{origin}{expected}"));
        assert!(crate::networking::is_id_list_membership_endpoint(
            url.as_str()
        ));
    }
    assert!(membership_url("client-valid", None).is_none());
    assert!(membership_url(SDK_KEY, Some("https://user:secret@attacker")).is_none());
}

#[tokio::test]
async fn posts_the_typed_id_and_reads_a_versioned_nonmember_answer() {
    let proxy = MockServer::start().await;
    let (network, endpoint) = network_and_endpoint(&proxy);
    Mock::given(method("POST"))
        .and(path("/v1/id_list_membership"))
        .and(header("statsig-api-key", SDK_KEY))
        .and(header("content-type", "application/json"))
        .and(body_json(serde_json::json!({
            "list_id": "chosen", "id_type": "stableID", "id": ORIGINAL_ID
        })))
        .respond_with(ResponseTemplate::new(200).set_body_json(serde_json::json!({
            "is_member": false,
            "revision": "HPxFkGzYC6ezXqRigOYmZZK4or6jRlio6B7z4kyxNcA="
        })))
        .expect(1)
        .mount(&proxy)
        .await;

    let version = IdListFileVersion {
        file_id: Some("same-file"),
        creation_time: 1,
        size: 20,
    };
    assert_eq!(
        lookup_membership(&network, &endpoint, "chosen", "stableID", ORIGINAL_ID).await,
        Ok(Some(MembershipAnswer {
            is_member: false,
            revision: Some(version.membership_revision().unwrap()),
        }))
    );
}

#[test]
fn decodes_unknown_and_unversioned_answers_and_rejects_invalid_replies() {
    for (body, expected) in [
        ("{}", Ok(None)),
        (
            r#"{"is_member":true}"#,
            Ok(Some(MembershipAnswer {
                is_member: true,
                revision: None,
            })),
        ),
        (
            r#"{"is_member":true,"revision":"YQ=="}"#,
            Err(MembershipLookupError::Rejected),
        ),
        ("[true]", Err(MembershipLookupError::Rejected)),
    ] {
        assert_eq!(decode_membership_reply(body.as_bytes()), expected, "{body}");
    }
}

#[tokio::test]
async fn rejects_a_response_over_one_kib() {
    let proxy = MockServer::start().await;
    let (network, endpoint) = network_and_endpoint(&proxy);
    let answer = r#"{"is_member":true}"#;
    Mock::given(method("POST"))
        .respond_with(
            ResponseTemplate::new(200).set_body_raw(format!("{answer:<1025}"), "application/json"),
        )
        .expect(1)
        .mount(&proxy)
        .await;
    assert_eq!(
        lookup_membership(&network, &endpoint, "qa", "userID", ORIGINAL_ID).await,
        Err(MembershipLookupError::Rejected)
    );
}

#[test]
fn rejects_custom_streams_without_seeking_or_reading_on_the_sdk_runtime() {
    #[derive(Debug)]
    struct Unbuffered;
    impl std::io::Read for Unbuffered {
        fn read(&mut self, _: &mut [u8]) -> std::io::Result<usize> {
            panic!("a membership lookup cannot block on a provider stream")
        }
    }
    impl std::io::Seek for Unbuffered {
        fn seek(&mut self, _: std::io::SeekFrom) -> std::io::Result<u64> {
            panic!("a membership lookup cannot seek a provider stream")
        }
    }
    assert_eq!(
        decode_membership_body(ResponseData::from_stream(Box::new(Unbuffered))),
        Err(MembershipLookupError::Rejected)
    );
}

#[tokio::test]
async fn a_redirect_does_not_forward_ids_or_server_keys() {
    let origin = MockServer::start().await;
    let other = MockServer::start().await;
    let (network, endpoint) = network_and_endpoint(&origin);
    Mock::given(method("POST"))
        .respond_with(ResponseTemplate::new(307).insert_header("location", other.uri().as_str()))
        .expect(1)
        .mount(&origin)
        .await;
    assert_eq!(
        lookup_membership(&network, &endpoint, "qa", "userID", ORIGINAL_ID).await,
        Err(MembershipLookupError::Rejected)
    );
    assert!(other.received_requests().await.unwrap().is_empty());
}

#[tokio::test]
async fn echoed_ids_are_redacted_from_membership_errors() {
    let proxy = MockServer::start().await;
    let (network, endpoint) = network_and_endpoint(&proxy);
    let private_id = "fixture-private-id";
    Mock::given(method("POST"))
        .respond_with(ResponseTemplate::new(400).set_body_string(private_id))
        .expect(2)
        .mount(&proxy)
        .await;

    let request = RequestArgs {
        url: endpoint,
        body: Some(private_id.as_bytes().to_vec()),
        ..RequestArgs::new()
    };
    let membership = network
        .request_once_with_redacted_response(HttpMethod::POST, request, MAX_RESPONSE_BYTES)
        .await;
    assert!(
        matches!(membership, Err(NetworkError::RequestNotRetryable(_, Some(400), message)) if message.is_empty())
    );

    let manifest = network
        .request_once(
            HttpMethod::POST,
            RequestArgs {
                url: format!("{}/v1/get_id_lists", proxy.uri()),
                ..RequestArgs::new()
            },
            None,
            false,
            true,
            0,
        )
        .await;
    assert!(
        matches!(manifest, Err(NetworkError::RequestNotRetryable(_, Some(400), message)) if message.contains(private_id))
    );
}
