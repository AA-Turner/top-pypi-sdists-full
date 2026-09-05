use crate::{
    StatsigErr,
    networking::ResponseData,
    specs_response::{
        proto_compression::is_compressed_protobuf_response, spec_types::SpecsResponseNoUpdates,
    },
};

#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum SpecsResponseFormat {
    Json,
    PlainText,
    Protobuf,
    Unknown,
}

impl SpecsResponseFormat {
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Json => "json",
            Self::PlainText => "plain_text",
            Self::Protobuf => "protobuf",
            Self::Unknown => "unknown",
        }
    }
}

fn is_response_protobuf(response_data: &ResponseData) -> bool {
    is_compressed_protobuf_response(response_data)
}

pub fn get_specs_response_format(response_data: &ResponseData) -> SpecsResponseFormat {
    if is_response_protobuf(response_data) {
        return SpecsResponseFormat::Protobuf;
    }

    let content_type = match response_data.get_header_ref("content-type") {
        Some(content_type) => content_type.to_ascii_lowercase(),
        None => return SpecsResponseFormat::Unknown,
    };

    if content_type.contains("application/json") || content_type.contains("+json") {
        return SpecsResponseFormat::Json;
    }

    if content_type.contains("text/plain") {
        return SpecsResponseFormat::PlainText;
    }

    SpecsResponseFormat::Unknown
}

/// Older DCS responses can retain statsig-br headers while returning the
/// legacy JSON no-update body. Callers that hydrate before parsing need to
/// preserve that body instead of asking the protobuf hydrator to decode it.
pub(super) fn is_legacy_json_no_update_under_protobuf_headers(
    data: &mut ResponseData,
) -> Result<bool, StatsigErr> {
    if get_specs_response_format(data) != SpecsResponseFormat::Protobuf {
        return Ok(false);
    }

    let is_no_update = data
        .deserialize_into::<SpecsResponseNoUpdates>()
        .is_ok_and(|response| !response.has_updates);
    data.rewind()?;
    Ok(is_no_update)
}
