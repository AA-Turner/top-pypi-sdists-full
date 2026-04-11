use crate::handler::Tn3270Handler;
use guacr_handlers::ProtocolHandler;
use guacr_protocol::telnet::{extract_record, DO, EOR, IAC, OPT_BINARY};

#[test]
fn test_handler_name() {
    assert_eq!(Tn3270Handler::new().name(), "tn3270");
}

#[test]
fn test_extract_record_simple() {
    // Single complete record terminated by IAC EOR
    let mut buf = vec![0xF5, 0x40, IAC, EOR];
    let record = extract_record(&mut buf);
    assert_eq!(record, Some(vec![0xF5, 0x40]));
    assert!(buf.is_empty());
}

#[test]
fn test_extract_record_incomplete() {
    // No EOR yet — should return None and leave buffer intact
    let mut buf = vec![0xF5, 0x40, 0xC8];
    assert!(extract_record(&mut buf).is_none());
}

#[test]
fn test_extract_record_iac_escaped() {
    // IAC IAC in data should become a single 0xFF byte in the record
    let mut buf = vec![IAC, IAC, 0x42, IAC, EOR];
    let record = extract_record(&mut buf).unwrap();
    assert_eq!(record, vec![IAC, 0x42]);
    assert!(buf.is_empty());
}

#[test]
fn test_extract_record_strips_telnet_option() {
    // IAC DO BINARY before the actual data — option should be stripped
    let mut buf = vec![IAC, DO, OPT_BINARY, 0xC8, IAC, EOR];
    let record = extract_record(&mut buf).unwrap();
    assert_eq!(record, vec![0xC8]);
}

#[test]
fn test_extract_record_multiple() {
    // Two back-to-back records
    let mut buf = vec![0x01, IAC, EOR, 0x02, IAC, EOR];
    assert_eq!(extract_record(&mut buf), Some(vec![0x01]));
    assert_eq!(extract_record(&mut buf), Some(vec![0x02]));
    assert!(buf.is_empty());
}

#[tokio::test]
async fn test_health_check() {
    let h = Tn3270Handler::new();
    assert!(h.health_check().await.is_ok());
}
