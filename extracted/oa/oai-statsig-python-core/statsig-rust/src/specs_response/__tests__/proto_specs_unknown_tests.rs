use crate::{
    StatsigErr,
    interned_string::InternedString,
    networking::ResponseData,
    observability::ops_stats::{OpsStatsEvent, OpsStatsForInstance},
    specs_response::{proto_specs::deserialize_protobuf, spec_types::SpecsResponseFull},
};

// Generated from cli/src/commands/make-test-proto.ts
// run `tore make-test-proto` to generate the unknown_enum.pb.br file
const UNKNOWN_ENUM_PROTO_BYTES: &[u8] = include_bytes!("../../../tests/data/unknown_enum.pb.br");

#[test]
fn test_it_can_parse_response_with_unknown_fields() {
    let result = get_deserialized_spec_result(&OpsStatsForInstance::new());
    assert!(result.is_ok());
}

#[test]
fn test_unknown_enum_reports_parse_error() {
    let ops_stats = OpsStatsForInstance::new();
    let mut events = ops_stats.subscribe_for_test();

    get_deserialized_spec_result(&ops_stats).expect("unknown enum should not abort parsing");

    let error = std::iter::from_fn(|| events.try_recv().ok())
        .find_map(|event| match event {
            OpsStatsEvent::SDKError(error) => Some(error),
            _ => None,
        })
        .expect("unknown enum should emit an SDK error");
    assert_eq!(error.exception, "ProtobufParseError");
}

#[test]
fn test_it_parsed_the_gate_without_unexpected_field() {
    let result = get_deserialized_spec_result(&OpsStatsForInstance::new())
        .expect("Failed to deserialize specs");

    let supported_gate = result
        .feature_gates
        .get(&InternedString::from_str_ref(
            "gate_without_unexpected_field",
        ))
        .expect("Gate not found")
        .as_spec_ref();

    assert_eq!(supported_gate.default_value.get_bool(), Some(true));
    assert_eq!(supported_gate.entity, "feature_gate");
    assert_eq!(supported_gate.id_type, "userID");
    assert_eq!(*supported_gate.rules, Vec::new());
    assert_eq!(supported_gate.version, Some(8));
    assert_eq!(
        supported_gate.salt,
        "test_salt_for_gate_without_unexpected_field"
    );
}

#[test]
fn test_it_ignored_the_gate_with_unexpected_field() {
    let result = get_deserialized_spec_result(&OpsStatsForInstance::new())
        .expect("Failed to deserialize specs");

    let count = result.feature_gates.len();
    assert_eq!(count, 1);
}

#[test]
fn test_it_extracted_known_top_level_fields() {
    let result = get_deserialized_spec_result(&OpsStatsForInstance::new())
        .expect("Failed to deserialize specs");

    assert_eq!(result.company_id, Some("test_company_id".to_string()));
    assert_eq!(
        result.response_format,
        Some("test_response_format".to_string())
    );
    assert_eq!(result.checksum, Some("test_checksum".to_string()));
}

fn get_deserialized_spec_result(
    ops_stats: &OpsStatsForInstance,
) -> Result<SpecsResponseFull, StatsigErr> {
    let left = SpecsResponseFull::default();
    let mut right = SpecsResponseFull::default();

    let mut data = ResponseData::from_bytes(UNKNOWN_ENUM_PROTO_BYTES.to_vec());

    deserialize_protobuf(ops_stats, &left, &mut right, &mut data)?;
    Ok(right)
}
