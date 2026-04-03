//! SOCKS5 OpenConnection payload encoding and decoding.
//!
//! The SOCKS5 OpenConnection payload format:
//! `[conn_no: 4 bytes (u32 BE)] [host_len: 4 bytes (u32 BE)] [host: N bytes] [port: 2 bytes (u16 BE)]`

use anyhow::{anyhow, Result};
use bytes::{Buf, BufMut, BytesMut};

/// Parsed SOCKS5 target destination.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Socks5Target {
    pub host: String,
    pub port: u16,
}

/// Encode a SOCKS5 OpenConnection payload.
///
/// Format: `[conn_no(4) | host_len(4) | host(N) | port(2)]`
pub fn encode_open_connection_payload(conn_no: u32, target: &Socks5Target) -> BytesMut {
    let host_bytes = target.host.as_bytes();
    let capacity = 4 + 4 + host_bytes.len() + 2;
    let mut buf = BytesMut::with_capacity(capacity);
    buf.put_u32(conn_no);
    buf.put_u32(host_bytes.len() as u32);
    buf.extend_from_slice(host_bytes);
    buf.put_u16(target.port);
    buf
}

/// Decode a SOCKS5 OpenConnection payload.
///
/// The payload starts AFTER the conn_no has already been consumed by the caller.
/// Input: `[host_len(4) | host(N) | port(2)]`
///
/// Returns the target host and port.
pub fn decode_open_connection_payload(data: &[u8]) -> Result<Socks5Target> {
    if data.len() < 4 {
        return Err(anyhow!("SOCKS5 payload missing host length"));
    }

    let mut cursor = std::io::Cursor::new(data);
    let host_len = cursor.get_u32() as usize;

    if cursor.remaining() < host_len + 2 {
        return Err(anyhow!(
            "SOCKS5 payload too short for host and port data (need {} + 2, have {})",
            host_len,
            cursor.remaining()
        ));
    }

    let mut host_bytes = vec![0u8; host_len];
    cursor.copy_to_slice(&mut host_bytes);
    let host =
        String::from_utf8(host_bytes).map_err(|e| anyhow!("Invalid UTF-8 in SOCKS host: {}", e))?;

    let port = cursor.get_u16();

    Ok(Socks5Target { host, port })
}
