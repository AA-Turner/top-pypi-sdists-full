mod attributes;
mod conversion;
mod id;
mod sse;

pub use attributes::{convert_attributes_to_proto_key_value, extract_attributes};
pub use conversion::json_value_to_any_value;
pub use id::{bytes_to_uuid_like_string, generate_span_id, parse_span_id, parse_trace_id};
pub use sse::parse_sse_events;

// /// Decompresses gzip-encoded data if the flag is set
// pub fn decompress_if_gzip(data: &[u8], is_gzip_encoded: bool) -> Result<String, std::io::Error> {
//     if is_gzip_encoded {
//         // Check if data actually starts with gzip magic number
//         let has_gzip_magic = data.len() >= 2 && data[0] == 0x1f && data[1] == 0x8b;

//         if !has_gzip_magic {
//             eprintln!(
//                 "Warning: Content-Encoding says gzip but data doesn't have gzip magic number"
//             );
//             // Try to parse as UTF-8 directly
//             return String::from_utf8(data.to_vec())
//                 .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e));
//         }

//         let mut decoder = GzDecoder::new(data);
//         let mut decompressed = String::new();
//         decoder.read_to_string(&mut decompressed)?;
//         Ok(decompressed)
//     } else {
//         // Not gzip-encoded, convert to string
//         String::from_utf8(data.to_vec())
//             .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))
//     }
// }

pub fn is_gzip_encoded(data: &[u8], has_gzip_content_encoding: bool) -> bool {
    return has_gzip_content_encoding && data.len() >= 2 && data[0] == 0x1f && data[1] == 0x8b;
}
