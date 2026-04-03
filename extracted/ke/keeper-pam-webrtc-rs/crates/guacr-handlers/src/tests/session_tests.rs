use crate::recording::MultiFormatRecorder;
use crate::session::{
    record_client_input, send_and_record, send_bell, send_disconnect, send_name, send_ready,
};
use bytes::Bytes;
use tokio::sync::mpsc;

#[tokio::test]
async fn test_send_ready() {
    let (tx, mut rx) = mpsc::channel(16);
    send_ready(&tx, "ssh-ready").await.unwrap();
    let msg = rx.recv().await.unwrap();
    let s = String::from_utf8(msg.to_vec()).unwrap();
    assert_eq!(s, "5.ready,9.ssh-ready;");
}

#[tokio::test]
async fn test_send_name() {
    let (tx, mut rx) = mpsc::channel(16);
    send_name(&tx, "SSH").await.unwrap();
    let msg = rx.recv().await.unwrap();
    let s = String::from_utf8(msg.to_vec()).unwrap();
    assert_eq!(s, "4.name,3.SSH;");
}

#[tokio::test]
async fn test_send_disconnect() {
    let (tx, mut rx) = mpsc::channel(16);
    send_disconnect(&tx).await;
    let msg = rx.recv().await.unwrap();
    let s = String::from_utf8(msg.to_vec()).unwrap();
    assert_eq!(s, "10.disconnect;");
}

#[tokio::test]
async fn test_send_bell() {
    let (tx, mut rx) = mpsc::channel(16);
    send_bell(&tx, 100).await.unwrap();
    // Should produce 3 instructions: audio, blob, end
    let audio = rx.recv().await.unwrap();
    let blob = rx.recv().await.unwrap();
    let end = rx.recv().await.unwrap();
    let audio_s = String::from_utf8(audio.to_vec()).unwrap();
    let end_s = String::from_utf8(end.to_vec()).unwrap();
    assert!(audio_s.contains("audio"));
    assert!(audio_s.contains("audio/wav"));
    let blob_s = String::from_utf8(blob.to_vec()).unwrap();
    assert!(blob_s.contains("blob"));
    assert!(end_s.contains("end"));
}

#[tokio::test]
async fn test_send_ready_closed_channel() {
    let (tx, rx) = mpsc::channel(16);
    drop(rx);
    let result = send_ready(&tx, "test").await;
    assert!(result.is_err());
}

#[tokio::test]
async fn test_send_disconnect_closed_channel() {
    let (tx, rx) = mpsc::channel(16);
    drop(rx);
    // Should not panic, just log debug
    send_disconnect(&tx).await;
}

#[tokio::test]
async fn test_send_and_record_without_recorder() {
    let (tx, mut rx) = mpsc::channel(16);
    let mut recorder: Option<MultiFormatRecorder> = None;
    let instr = Bytes::from("5.ready,4.test;");
    send_and_record(&tx, &mut recorder, instr).await.unwrap();
    let msg = rx.recv().await.unwrap();
    assert_eq!(&msg[..], b"5.ready,4.test;");
}

#[tokio::test]
async fn test_send_and_record_closed_channel() {
    let (tx, rx) = mpsc::channel(16);
    drop(rx);
    let mut recorder: Option<MultiFormatRecorder> = None;
    let result = send_and_record(&tx, &mut recorder, Bytes::from("test")).await;
    assert!(result.is_err());
}

#[test]
fn test_record_client_input_without_recorder() {
    let mut recorder: Option<MultiFormatRecorder> = None;
    // Should not panic when recorder is None
    record_client_input(&mut recorder, &Bytes::from("3.key,1.1,5.65536;"));
}
