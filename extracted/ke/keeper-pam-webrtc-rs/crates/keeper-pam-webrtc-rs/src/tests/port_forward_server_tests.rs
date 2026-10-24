use crate::buffer_pool::BufferPool;
use crate::channel::Channel;
use crate::tube_protocol::{try_parse_frame, ControlMessage, Frame};
use anyhow::Result;
use bytes::{Bytes, BytesMut};
use parking_lot::Mutex;
use std::collections::HashMap;
use std::sync::Arc;
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpStream;
use tokio::sync::mpsc;
use tokio::time::timeout;

#[tokio::test]
async fn loopback_listener_forwards_both_directions() -> Result<()> {
    let (frame_tx, mut frame_rx) = mpsc::channel::<Bytes>(16);
    let webrtc = crate::tests::common_tests::create_test_webrtc_data_channel().await;
    webrtc.set_test_send_hook(move |data| {
        let frame_tx = frame_tx.clone();
        Box::pin(async move {
            let _ = frame_tx.send(data).await;
        })
    });

    let (to_channel_tx, to_channel_rx) = mpsc::unbounded_channel::<Bytes>();
    let input_sender = to_channel_tx.clone();
    let mut settings = HashMap::new();
    settings.insert("conversationType".to_string(), serde_json::json!("tunnel"));
    let shutdown_notify = Arc::new(tokio::sync::Notify::new());
    let mut channel = Channel::new(crate::channel::core::ChannelParams {
        webrtc: webrtc.clone(),
        rx_from_dc: to_channel_rx,
        tx_from_dc: Arc::new(Mutex::new(Some(to_channel_tx))),
        channel_id: "port-forward-loopback-test".to_string(),
        conversation_id: "port-forward-loopback-test".to_string(),
        timeouts: None,
        protocol_settings: settings,
        server_mode: true,
        shutdown_notify: Arc::clone(&shutdown_notify),
        callback_token: None,
        ksm_config: None,
        client_version: "test".to_string(),
        capabilities: crate::tube_protocol::Capabilities::NONE,
        python_handler_tx: None,
    })
    .await?;

    let addr = channel.start_server("127.0.0.1:0").await?;
    let channel_task = tokio::spawn(async move { channel.run().await });
    let mut client = timeout(Duration::from_secs(2), TcpStream::connect(addr)).await??;

    let open = timeout(Duration::from_secs(2), frame_rx.recv())
        .await?
        .ok_or_else(|| anyhow::anyhow!("listener did not send OpenConnection"))?;
    let mut open_bytes = BytesMut::from(open.as_ref());
    let open = try_parse_frame(&mut open_bytes)?.expect("complete OpenConnection frame");
    assert_eq!(open.connection_no, 0);
    assert_eq!(
        u16::from_be_bytes([open.payload[0], open.payload[1]]),
        ControlMessage::OpenConnection as u16
    );
    let conn_no = u32::from_be_bytes(open.payload[2..6].try_into()?);
    assert!(conn_no > 0);

    let outbound = b"loopback to WebRTC";
    client.write_all(outbound).await?;
    let data = timeout(Duration::from_secs(2), frame_rx.recv())
        .await?
        .ok_or_else(|| anyhow::anyhow!("listener did not forward TCP payload"))?;
    let mut data_bytes = BytesMut::from(data.as_ref());
    let data = try_parse_frame(&mut data_bytes)?.expect("complete PortForward data frame");
    assert_eq!(data.connection_no, conn_no);
    assert_eq!(&data.payload[..], outbound);

    let inbound = Frame::new_data_with_pool(
        conn_no,
        b"WebRTC back to loopback",
        &BufferPool::default(),
    );
    input_sender
        .send(inbound.encode_with_pool(&BufferPool::default()))
        .expect("channel run loop is active");
    let mut response = vec![0; b"WebRTC back to loopback".len()];
    timeout(Duration::from_secs(2), client.read_exact(&mut response)).await??;
    assert_eq!(&response, b"WebRTC back to loopback");

    client.shutdown().await?;
    shutdown_notify.notify_one();
    let _ = timeout(Duration::from_secs(2), channel_task).await??;
    Ok(())
}
