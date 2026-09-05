use crate::networking::ResponseData;

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub(crate) enum ProtoCompression {
    Brotli,
    Zstd,
}

impl ProtoCompression {
    pub(crate) fn from_response(data: &ResponseData) -> Option<Self> {
        let content_type = data.get_header_ref("content-type")?;
        if !content_type.contains("application/octet-stream") {
            return None;
        }

        let content_encoding = data.get_header_ref("content-encoding")?;
        if content_encoding.contains("statsig-br") {
            return Some(Self::Brotli);
        }

        if content_encoding.trim().eq_ignore_ascii_case("statsig-zstd") {
            return Some(Self::Zstd);
        }

        None
    }

    pub(crate) const fn content_encoding(self) -> &'static str {
        match self {
            Self::Brotli => "statsig-br",
            Self::Zstd => "statsig-zstd",
        }
    }
}

pub(crate) fn is_compressed_protobuf_response(data: &ResponseData) -> bool {
    ProtoCompression::from_response(data).is_some()
}

#[cfg(test)]
mod tests {
    use super::{ProtoCompression, is_compressed_protobuf_response};
    use crate::networking::ResponseData;
    use std::collections::HashMap;

    fn response(content_encoding: &str, deltas_used: Option<&str>) -> ResponseData {
        let mut headers = HashMap::from([
            (
                "content-type".to_string(),
                "application/octet-stream".to_string(),
            ),
            ("content-encoding".to_string(), content_encoding.to_string()),
        ]);
        if let Some(deltas_used) = deltas_used {
            headers.insert("x-deltas-used".to_string(), deltas_used.to_string());
        }

        ResponseData::from_bytes_with_headers(Vec::new(), Some(headers))
    }

    #[test]
    fn recognizes_existing_statsig_brotli() {
        let data = response("statsig-br", None);

        assert_eq!(
            ProtoCompression::from_response(&data),
            Some(ProtoCompression::Brotli)
        );
        assert!(is_compressed_protobuf_response(&data));
    }

    #[test]
    fn recognizes_statsig_zstd_for_delta_and_full_responses() {
        let delta = response("statsig-zstd", Some("true"));
        let full = response("statsig-zstd", None);
        let stacked = response("statsig-zstd, gzip", Some("true"));

        assert_eq!(
            ProtoCompression::from_response(&delta),
            Some(ProtoCompression::Zstd)
        );
        assert_eq!(
            ProtoCompression::from_response(&full),
            Some(ProtoCompression::Zstd)
        );
        assert_eq!(ProtoCompression::from_response(&stacked), None);
    }

    #[test]
    fn rejects_standard_zstd_and_non_proto_content_type() {
        let standard_zstd = response("zstd", Some("true"));
        let mut headers = HashMap::from([
            ("content-type".to_string(), "application/json".to_string()),
            ("content-encoding".to_string(), "statsig-zstd".to_string()),
            ("x-deltas-used".to_string(), "true".to_string()),
        ]);
        let json = ResponseData::from_bytes_with_headers(Vec::new(), Some(headers.clone()));

        assert_eq!(ProtoCompression::from_response(&standard_zstd), None);
        assert_eq!(ProtoCompression::from_response(&json), None);

        headers.insert("x-deltas-used".to_string(), "false".to_string());
        let false_delta = ResponseData::from_bytes_with_headers(Vec::new(), Some(headers));
        assert_eq!(ProtoCompression::from_response(&false_delta), None);
    }
}
