use crate::handler::{extract_record, Tn5250Handler, EOR, IAC};
use guacr_handlers::ProtocolHandler;

#[test]
fn test_handler_name() {
    assert_eq!(Tn5250Handler::new().name(), "tn5250");
}

#[test]
fn test_extract_record_simple() {
    let mut buf = vec![0x00, 0x07, 0x00, 0x00, 0x01, IAC, EOR];
    let record = extract_record(&mut buf).unwrap();
    assert_eq!(record, vec![0x00, 0x07, 0x00, 0x00, 0x01]);
    assert!(buf.is_empty());
}

#[test]
fn test_extract_record_incomplete() {
    let mut buf = vec![0x00, 0x07, 0x00];
    assert!(extract_record(&mut buf).is_none());
}

#[tokio::test]
async fn test_health_check() {
    assert!(Tn5250Handler::new().health_check().await.is_ok());
}
