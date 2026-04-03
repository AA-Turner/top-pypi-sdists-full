use crate::handshake::{
    Socks5Address, Socks5Handshake, SOCKS5_ADDR_TYPE_IPV4, SOCKS5_AUTH_FAILED,
    SOCKS5_AUTH_METHOD_NONE, SOCKS5_SUCCESS_RESPONSE, SOCKS5_VERSION,
};

#[test]
fn test_socks5_constants() {
    assert_eq!(SOCKS5_VERSION, 0x05);
    assert_eq!(SOCKS5_AUTH_METHOD_NONE, 0x00);
    assert_eq!(SOCKS5_AUTH_FAILED, 0xFF);
    use crate::handshake::SOCKS5_CMD_CONNECT;
    assert_eq!(SOCKS5_CMD_CONNECT, 0x01);
    assert_eq!(SOCKS5_ADDR_TYPE_IPV4, 0x01);
    use crate::handshake::{SOCKS5_ATYP_DOMAIN, SOCKS5_ATYP_IPV6};
    assert_eq!(SOCKS5_ATYP_DOMAIN, 0x03);
    assert_eq!(SOCKS5_ATYP_IPV6, 0x04);
}

#[test]
fn test_socks5_success_response() {
    assert_eq!(SOCKS5_SUCCESS_RESPONSE.len(), 10);
    assert_eq!(SOCKS5_SUCCESS_RESPONSE[0], 0x05); // SOCKS version 5
    assert_eq!(SOCKS5_SUCCESS_RESPONSE[1], 0x00); // Success
    assert_eq!(SOCKS5_SUCCESS_RESPONSE[2], 0x00); // Reserved
    assert_eq!(SOCKS5_SUCCESS_RESPONSE[3], 0x01); // IPv4
    assert_eq!(&SOCKS5_SUCCESS_RESPONSE[4..8], &[0x00, 0x00, 0x00, 0x00]);
    assert_eq!(&SOCKS5_SUCCESS_RESPONSE[8..10], &[0x00, 0x00]);
}

#[test]
fn test_socks5_address_as_str() {
    let ipv4 = Socks5Address::IPv4("127.0.0.1".to_string());
    assert_eq!(ipv4.as_str(), "127.0.0.1");

    let domain = Socks5Address::Domain("example.com".to_string());
    assert_eq!(domain.as_str(), "example.com");

    let ipv6 = Socks5Address::IPv6("::1".to_string());
    assert_eq!(ipv6.as_str(), "::1");
}

#[tokio::test]
async fn test_handshake_auth_negotiation() {
    // Simulate a SOCKS5 client: send greeting, receive auth response
    let (client, server) = tokio::io::duplex(1024);

    let server_task = tokio::spawn(async move {
        let mut hs = Socks5Handshake::new(server);
        hs.negotiate_auth().await
    });

    let client_task = tokio::spawn(async move {
        let (mut reader, mut writer) = tokio::io::split(client);
        // Send greeting: version=5, 1 method, method=0 (no auth)
        use tokio::io::AsyncWriteExt;
        writer.write_all(&[0x05, 0x01, 0x00]).await.unwrap();
        // Read response
        let mut buf = [0u8; 2];
        tokio::io::AsyncReadExt::read_exact(&mut reader, &mut buf)
            .await
            .unwrap();
        buf
    });

    let response = client_task.await.unwrap();
    assert_eq!(response, [0x05, 0x00]); // version 5, no auth
    server_task.await.unwrap().unwrap();
}

#[tokio::test]
async fn test_handshake_invalid_version() {
    let (client, server) = tokio::io::duplex(1024);

    let server_task = tokio::spawn(async move {
        let mut hs = Socks5Handshake::new(server);
        hs.negotiate_auth().await
    });

    let client_task = tokio::spawn(async move {
        let (mut reader, mut writer) = tokio::io::split(client);
        // Send invalid version
        use tokio::io::AsyncWriteExt;
        writer.write_all(&[0x04, 0x01, 0x00]).await.unwrap();
        // Read response (auth failed)
        let mut buf = [0u8; 2];
        tokio::io::AsyncReadExt::read_exact(&mut reader, &mut buf)
            .await
            .unwrap();
        buf
    });

    let response = client_task.await.unwrap();
    assert_eq!(response, [0x05, 0xFF]); // version 5, auth failed
    assert!(server_task.await.unwrap().is_err());
}

#[tokio::test]
async fn test_full_handshake_connect_domain() {
    let (client, server) = tokio::io::duplex(1024);

    let server_task = tokio::spawn(async move {
        let mut hs = Socks5Handshake::new(server);
        hs.handshake().await
    });

    let client_task = tokio::spawn(async move {
        let (mut reader, mut writer) = tokio::io::split(client);
        // Greeting: version=5, 1 method, no auth
        use tokio::io::AsyncWriteExt;
        writer.write_all(&[0x05, 0x01, 0x00]).await.unwrap();
        // Read auth response
        let mut buf = [0u8; 2];
        tokio::io::AsyncReadExt::read_exact(&mut reader, &mut buf)
            .await
            .unwrap();
        assert_eq!(buf, [0x05, 0x00]);

        // Request: CONNECT to example.com:80
        let domain = b"example.com";
        let mut request = vec![0x05, 0x01, 0x00, 0x03]; // ver, cmd=connect, rsv, atyp=domain
        request.push(domain.len() as u8);
        request.extend_from_slice(domain);
        request.extend_from_slice(&80u16.to_be_bytes());
        writer.write_all(&request).await.unwrap();
    });

    client_task.await.unwrap();
    let (address, port) = server_task.await.unwrap().unwrap();
    assert_eq!(address, Socks5Address::Domain("example.com".to_string()));
    assert_eq!(port, 80);
}

#[tokio::test]
async fn test_full_handshake_connect_ipv4() {
    let (client, server) = tokio::io::duplex(1024);

    let server_task = tokio::spawn(async move {
        let mut hs = Socks5Handshake::new(server);
        hs.handshake().await
    });

    let client_task = tokio::spawn(async move {
        let (mut reader, mut writer) = tokio::io::split(client);
        // Greeting
        use tokio::io::AsyncWriteExt;
        writer.write_all(&[0x05, 0x01, 0x00]).await.unwrap();
        let mut buf = [0u8; 2];
        tokio::io::AsyncReadExt::read_exact(&mut reader, &mut buf)
            .await
            .unwrap();

        // Request: CONNECT to 192.168.1.1:443
        let request = [
            0x05, 0x01, 0x00, 0x01, // ver, cmd=connect, rsv, atyp=ipv4
            192, 168, 1, 1, // address
            0x01, 0xBB, // port 443
        ];
        writer.write_all(&request).await.unwrap();
    });

    client_task.await.unwrap();
    let (address, port) = server_task.await.unwrap().unwrap();
    assert_eq!(address, Socks5Address::IPv4("192.168.1.1".to_string()));
    assert_eq!(port, 443);
}
