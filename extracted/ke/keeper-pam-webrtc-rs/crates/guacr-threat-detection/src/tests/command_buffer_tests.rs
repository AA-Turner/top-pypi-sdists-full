use crate::command_buffer::CommandBuffer;
use std::time::Duration;

#[test]
fn test_command_buffer_new() {
    let buffer = CommandBuffer::new();
    assert!(buffer.is_empty());
    assert!(!buffer.is_pending_approval());
    assert!(buffer.elapsed().is_none());
}

#[test]
fn test_command_buffer_append() {
    let mut buffer = CommandBuffer::new();
    buffer.append(b"ls");
    assert_eq!(buffer.as_str(), "ls");
    assert_eq!(buffer.len(), 2);
    assert!(!buffer.is_empty());
}

#[test]
fn test_command_buffer_append_str() {
    let mut buffer = CommandBuffer::new();
    buffer.append_str("ls");
    buffer.append_str(" -la");
    assert_eq!(buffer.as_str(), "ls -la");
}

#[test]
fn test_command_buffer_backspace() {
    let mut buffer = CommandBuffer::new();
    buffer.append_str("ls");
    buffer.backspace();
    assert_eq!(buffer.as_str(), "l");
    buffer.backspace();
    assert!(buffer.is_empty());
}

#[test]
fn test_command_buffer_clear() {
    let mut buffer = CommandBuffer::new();
    buffer.append_str("ls -la");
    buffer.set_pending_approval(true);
    buffer.clear();
    assert!(buffer.is_empty());
    assert!(!buffer.is_pending_approval());
}

#[test]
fn test_command_buffer_take() {
    let mut buffer = CommandBuffer::new();
    buffer.append_str("ls -la");
    let command = buffer.take();
    assert_eq!(command, "ls -la");
    assert!(buffer.is_empty());
}

#[test]
fn test_command_buffer_elapsed() {
    let mut buffer = CommandBuffer::new();
    assert!(buffer.elapsed().is_none());
    buffer.append_str("ls");
    assert!(buffer.elapsed().is_some());
    std::thread::sleep(Duration::from_millis(10));
    assert!(buffer.elapsed().unwrap() >= Duration::from_millis(10));
}

#[test]
fn test_command_buffer_expired() {
    let mut buffer = CommandBuffer::with_max_buffer_time(Duration::from_millis(10));
    buffer.append_str("ls");
    assert!(!buffer.is_expired());
    std::thread::sleep(Duration::from_millis(20));
    assert!(buffer.is_expired());
}
