use crate::server::GuacdHandshake;

#[tokio::test]
async fn test_handshake_mock() {
    use tokio::io::duplex;

    let (client, server) = duplex(1024);
    let mut handshake = GuacdHandshake::new(server);

    // Simulate client sending select
    let mut client = client;
    tokio::spawn(async move {
        use tokio::io::AsyncWriteExt;
        client.write_all(b"6.select,3.ssh;").await.unwrap();
        client.flush().await.unwrap();
    });

    // Read select on server side
    let select = handshake.read_select().await.unwrap();
    assert_eq!(select.protocol, "ssh");
    assert!(select.connection_id.is_none());
}

/// The string table here and guacr-protocol's numeric one are the same codes; a handler and
/// the guacd server must never report one failure under two numbers.
#[test]
fn status_strings_match_guacr_protocol() {
    use crate::server::status;
    let pairs = [
        (status::SUCCESS, guacr_protocol::STATUS_SUCCESS),
        (status::UNSUPPORTED, guacr_protocol::STATUS_UNSUPPORTED),
        (status::SERVER_ERROR, guacr_protocol::STATUS_SERVER_ERROR),
        (status::SERVER_BUSY, guacr_protocol::STATUS_SERVER_BUSY),
        (
            status::UPSTREAM_TIMEOUT,
            guacr_protocol::STATUS_UPSTREAM_TIMEOUT,
        ),
        (
            status::UPSTREAM_ERROR,
            guacr_protocol::STATUS_UPSTREAM_ERROR,
        ),
        (
            status::RESOURCE_NOT_FOUND,
            guacr_protocol::STATUS_RESOURCE_NOT_FOUND,
        ),
        (
            status::RESOURCE_CONFLICT,
            guacr_protocol::STATUS_RESOURCE_CONFLICT,
        ),
        (
            status::RESOURCE_CLOSED,
            guacr_protocol::STATUS_RESOURCE_CLOSED,
        ),
        (
            status::UPSTREAM_NOT_FOUND,
            guacr_protocol::STATUS_UPSTREAM_NOT_FOUND,
        ),
        (
            status::UPSTREAM_UNAVAILABLE,
            guacr_protocol::STATUS_UPSTREAM_UNAVAILABLE,
        ),
        (
            status::SESSION_CONFLICT,
            guacr_protocol::STATUS_SESSION_CONFLICT,
        ),
        (
            status::SESSION_TIMEOUT,
            guacr_protocol::STATUS_SESSION_TIMEOUT,
        ),
        (
            status::SESSION_CLOSED,
            guacr_protocol::STATUS_SESSION_CLOSED,
        ),
        (
            status::CLIENT_BAD_REQUEST,
            guacr_protocol::STATUS_CLIENT_BAD_REQUEST,
        ),
        (
            status::CLIENT_UNAUTHORIZED,
            guacr_protocol::STATUS_CLIENT_UNAUTHORIZED,
        ),
        (
            status::CLIENT_FORBIDDEN,
            guacr_protocol::STATUS_CLIENT_FORBIDDEN,
        ),
        (
            status::CLIENT_TIMEOUT,
            guacr_protocol::STATUS_CLIENT_TIMEOUT,
        ),
        (
            status::CLIENT_OVERRUN,
            guacr_protocol::STATUS_CLIENT_OVERRUN,
        ),
        (
            status::CLIENT_BAD_TYPE,
            guacr_protocol::STATUS_CLIENT_BAD_TYPE,
        ),
        (
            status::CLIENT_TOO_MANY,
            guacr_protocol::STATUS_CLIENT_TOO_MANY,
        ),
    ];
    for (text, code) in pairs {
        assert_eq!(text, code.to_string());
    }
}
