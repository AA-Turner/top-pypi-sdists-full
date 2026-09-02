// Unit tests for GuacrCliprdrBackend clipboard format negotiation (T-028 to T-031).
//
// Verifies that capability and format-list methods handle gracefully with no panic.

use crate::clipboard_backend::{create_backend, PendingClipboardData};
use ironrdp::cliprdr::backend::CliprdrBackend;
use ironrdp::cliprdr::pdu::ClipboardFormat;

fn make_backend() -> (
    crate::clipboard_backend::GuacrCliprdrBackend,
    tokio::sync::mpsc::UnboundedReceiver<ironrdp::cliprdr::backend::ClipboardMessage>,
    std::sync::Arc<parking_lot::Mutex<PendingClipboardData>>,
) {
    create_backend("/tmp".to_string())
}

// AC-3: client_capabilities() returns a valid flags value without panicking.
#[test]
fn test_client_capabilities_returns_ok() {
    let (backend, _rx, _data) = make_backend();
    let caps = backend.client_capabilities();
    // The return value is a bitflags type; just verify the call completes.
    let _ = caps;
}

// AC-3: on_request_format_list() with no prior clipboard data does not panic.
#[test]
fn test_on_request_format_list_empty_does_not_panic() {
    let (mut backend, _rx, _data) = make_backend();
    // No client text is set — the method must handle the empty-clipboard case gracefully.
    backend.on_request_format_list();
}

// AC-3: on_remote_copy() with empty format list does not panic.
#[test]
fn test_on_remote_copy_empty_format_list_does_not_panic() {
    let (mut backend, _rx, _data) = make_backend();
    backend.on_remote_copy(&[]);
}

// AC-3: on_remote_copy() with a populated format list does not panic.
#[test]
fn test_on_remote_copy_with_formats_does_not_panic() {
    use ironrdp::cliprdr::pdu::ClipboardFormatId;
    let (mut backend, _rx, _data) = make_backend();
    // CF_UNICODETEXT = 13; CF_TEXT = 1.
    let formats = vec![
        ClipboardFormat::new(ClipboardFormatId::new(13)),
        ClipboardFormat::new(ClipboardFormatId::new(1)),
    ];
    backend.on_remote_copy(&formats);
}

// AC-4: on_ready() when clipboard has no pending data does not panic.
#[test]
fn test_on_ready_no_pending_data_does_not_panic() {
    let (mut backend, _rx, _data) = make_backend();
    backend.on_ready();
}

// AC-3: on_process_negotiated_capabilities() does not panic.
#[test]
fn test_on_process_negotiated_capabilities_does_not_panic() {
    use ironrdp::cliprdr::pdu::ClipboardGeneralCapabilityFlags;
    let (mut backend, _rx, _data) = make_backend();
    backend
        .on_process_negotiated_capabilities(ClipboardGeneralCapabilityFlags::USE_LONG_FORMAT_NAMES);
}

// AC-1 / AC-2: temporary_directory() returns the path passed at construction.
#[test]
fn test_temporary_directory_matches_constructor() {
    let (backend, _rx, _data) = create_backend("/tmp/rdp-test".to_string());
    assert_eq!(backend.temporary_directory(), "/tmp/rdp-test");
}
