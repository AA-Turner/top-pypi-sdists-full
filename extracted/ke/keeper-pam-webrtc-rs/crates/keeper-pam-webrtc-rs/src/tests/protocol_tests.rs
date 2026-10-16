//! Protocol frame and message tests
use crate::buffer_pool::BufferPool;
use crate::runtime::get_runtime;
use crate::tube_protocol::{try_parse_frame, ControlMessage, Frame};

#[test]
fn test_protocol_frame_handling() {
    let runtime = get_runtime();
    runtime.block_on(async {
        // Create a buffer pool for the test
        let pool = BufferPool::default();

        // Test ping/pong control message parsing
        let ping_data = vec![0, 0, 0, 42]; // Connection number 42
        let ping_frame = Frame::new_control_with_pool(ControlMessage::Ping, &ping_data, &pool);

        // Verify frame construction
        assert_eq!(
            ping_frame.connection_no, 0,
            "Control frames should have connection_no = 0"
        );

        // The control message is stored as an u16 in the payload
        // ControlMessage::Ping has value 1, so the u16 bytes would be [0, 1]
        assert_eq!(ping_frame.payload[0], 0);
        assert_eq!(ping_frame.payload[1], ControlMessage::Ping as u8);

        // Verify that ping data is properly included
        assert_eq!(&ping_frame.payload[2..], &ping_data);

        // Test frame encoding/decoding
        let encoded = ping_frame.encode_with_pool(&pool);
        let encoded_slice = encoded.as_ref(); // Convert Bytes to &[u8] for testing

        // Verify frame encoding format
        assert_eq!(encoded_slice[0], 0); // connection_no (4 bytes)
        assert_eq!(encoded_slice[1], 0);
        assert_eq!(encoded_slice[2], 0);
        assert_eq!(encoded_slice[3], 0);

        // Test timestamp (8 bytes, skipping exact value)
        // Bytes 4-11 are the timestamp

        // Test payload length (4 bytes)
        // With 8-byte timestamp, payload length starts at byte 12
        let payload_len = (ping_frame.payload.len() as u32).to_be_bytes();
        assert_eq!(encoded_slice[12], payload_len[0]);
        assert_eq!(encoded_slice[13], payload_len[1]);
        assert_eq!(encoded_slice[14], payload_len[2]);
        assert_eq!(encoded_slice[15], payload_len[3]);
    });
}

#[test]
fn test_frame_parsing() {
    let runtime = get_runtime();
    runtime.block_on(async {
        // Create a buffer pool for the test
        let pool = BufferPool::default();

        // Test basic frame parsing functionality
        let data_payload = b"Hello, WebRTC!".to_vec();
        let data_frame = Frame::new_data_with_pool(1, &data_payload, &pool);

        // Verify frame construction
        assert_eq!(data_frame.connection_no, 1);
        assert_eq!(data_frame.payload, data_payload);

        // Test encoding
        let encoded = data_frame.encode_with_pool(&pool);
        let mut bytes = bytes::BytesMut::from(&encoded[..]);

        // Test parsing
        let parsed_frame = try_parse_frame(&mut bytes)
            .expect("no parse error")
            .expect("Should parse valid frame");

        // Verify parsed frame matches original
        assert_eq!(parsed_frame.connection_no, data_frame.connection_no);
        assert_eq!(parsed_frame.payload, data_frame.payload);
    });
}

#[test]
fn test_protocol_ping_pong() {
    let runtime = get_runtime();
    runtime.block_on(async {
        // Create a buffer pool for the test
        let pool = BufferPool::default();

        // Create a ping control message
        let conn_no: u32 = 0; // Control connection
        let ping_data = conn_no.to_be_bytes().to_vec();

        // Create a ping frame
        let ping_frame = Frame::new_control_with_pool(ControlMessage::Ping, &ping_data, &pool);

        // Verify the frame has the correct control message type
        assert_eq!(ping_frame.payload[0], 0);
        assert_eq!(ping_frame.payload[1], ControlMessage::Ping as u8);

        // Verify the connection number is 0 (for control messages)
        assert_eq!(ping_frame.connection_no, 0);

        // Test encoding/decoding roundtrip
        let encoded = ping_frame.encode_with_pool(&pool);
        let mut bytes = bytes::BytesMut::from(&encoded[..]);

        // Use the proper frame parsing function
        let decoded_frame = try_parse_frame(&mut bytes)
            .expect("no parse error")
            .expect("Should parse a valid frame");

        // Verify the decoded frame matches the original
        assert_eq!(decoded_frame.connection_no, ping_frame.connection_no);
        assert_eq!(decoded_frame.payload, ping_frame.payload);

        // Create a pong response with latency information
        let receive_latency = 15u64; // 15 ms simulated processing time
        let mut pong_data = conn_no.to_be_bytes().to_vec();
        pong_data.extend_from_slice(&receive_latency.to_be_bytes());

        let pong_frame = Frame::new_control_with_pool(ControlMessage::Pong, &pong_data, &pool);

        // Verify pong frame
        assert_eq!(pong_frame.payload[0], 0);
        assert_eq!(pong_frame.payload[1], ControlMessage::Pong as u8);

        // Verify pong contains expected data
        assert_eq!(pong_frame.payload.len(), 2 + 4 + 8); // control msg + conn_no + latency

        // Test basic frame parsing for pong
        let pong_encoded = pong_frame.encode_with_pool(&pool);
        let mut pong_bytes = bytes::BytesMut::from(&pong_encoded[..]);
        let parsed_pong = try_parse_frame(&mut pong_bytes)
            .expect("no parse error")
            .expect("Should parse pong frame");

        assert_eq!(parsed_pong.connection_no, 0);
        assert_eq!(parsed_pong.payload, pong_frame.payload);

        // Note: In our simplified system, we rely on WebRTC native stats
        // instead of custom ConnectionStats tracking
        println!("Frame parsing test completed - custom stats replaced with WebRTC native stats");
    });
}

/// Guacd routing decision.
///
/// The load-bearing case is `use_guacr=true` with no handler registry: falling
/// through to external guacd there produces a session that connects and paints
/// nothing, because the client is running a guacr viewer that reads
/// terminal-data/IMAGE frames guacd never sends. That has to fail loudly, which
/// matters now that `builtin-handlers` is opt-in rather than a default feature.
mod guacd_route_tests {
    use crate::channel::protocol::{decide_guacd_route, GuacdRoute};

    #[test]
    fn guacr_requested_without_registry_is_unavailable_not_external_guacd() {
        assert_eq!(
            decide_guacd_route(true, false, true),
            GuacdRoute::GuacrUnavailable,
            "a guacr session must not be silently served by external guacd"
        );
    }

    #[test]
    fn guacr_requested_without_conversation_type_is_unavailable() {
        assert_eq!(
            decide_guacd_route(true, true, false),
            GuacdRoute::GuacrUnavailable,
            "without a conversation type there is no handler to pick"
        );
    }

    #[test]
    fn guacr_requested_with_registry_uses_builtin() {
        assert_eq!(decide_guacd_route(true, true, true), GuacdRoute::Builtin);
    }

    #[test]
    fn guacr_not_requested_uses_external_guacd() {
        // Registry presence is irrelevant when the session did not ask for guacr.
        assert_eq!(
            decide_guacd_route(false, true, true),
            GuacdRoute::ExternalGuacd
        );
        assert_eq!(
            decide_guacd_route(false, false, false),
            GuacdRoute::ExternalGuacd
        );
    }
}

/// Which shipped wheel carries the handler registry.
///
/// `builtin-handlers` is opt-in, so the registry a session needs is decided in the wheels'
/// manifests rather than in code, and `decide_guacd_route` above only reports the
/// consequence at runtime. Both directions are load-bearing and neither fails at build
/// time, which is why they are asserted here:
///
/// - The gateway wheel (`keeper-pam-connections-py`, crates/python-bindings) must enable it.
///   Without it every guacr session on a gateway hits `GuacrUnavailable` and refuses to
///   connect -- a total outage for guacr users, with a build that compiled cleanly.
/// - The transport-only wheel (`keeper-pam-webrtc-rs-py`, crates/webrtc-bindings) must not.
///   It ships transport, not protocol handling; pulling in the guacr tree would bloat the
///   wheel and silently make it look like a gateway. A guacr session reaching it fails
///   loudly instead, which is the behaviour the tests above pin.
mod wheel_feature_tests {
    /// The dependency edge each wheel declares on this crate.
    fn webrtc_dep_line(wheel_dir: &str) -> String {
        let manifest = std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .parent()
            .expect("crates/ is the parent of this crate")
            .join(wheel_dir)
            .join("Cargo.toml");
        let text = std::fs::read_to_string(&manifest)
            .unwrap_or_else(|e| panic!("{} must be readable: {e}", manifest.display()));

        text.lines()
            .find(|l| l.contains(r#"path = "../keeper-pam-webrtc-rs""#))
            .unwrap_or_else(|| {
                panic!(
                    "{} must depend on this crate by path; if that edge moved, this guard \
                     no longer checks anything",
                    manifest.display()
                )
            })
            .to_string()
    }

    #[test]
    fn the_gateway_wheel_enables_the_builtin_handlers() {
        assert!(
            webrtc_dep_line("python-bindings").contains("builtin-handlers"),
            "crates/python-bindings is the gateway wheel: without `builtin-handlers` it \
             builds fine and then refuses every guacr session at runtime"
        );
    }

    #[test]
    fn the_transport_only_wheel_does_not_enable_the_builtin_handlers() {
        let dep = webrtc_dep_line("webrtc-bindings");
        assert!(
            !dep.contains("builtin-handlers"),
            "crates/webrtc-bindings ships transport only; enabling `builtin-handlers` \
             pulls the whole guacr protocol tree into a wheel that does not serve \
             protocol sessions. Got: {dep}"
        );
        assert!(
            dep.contains("default-features = false"),
            "the transport-only wheel must opt out of defaults explicitly, or a future \
             default feature silently pulls the guacr tree back in. Got: {dep}"
        );
    }
}
