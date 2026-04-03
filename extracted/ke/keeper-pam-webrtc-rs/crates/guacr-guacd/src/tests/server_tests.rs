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
