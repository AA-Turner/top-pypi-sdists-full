use crate::datastream::{
    aid_byte_for_key, build_response_record, decode_address, encode_address, parse_5250_record,
    DataStreamItem5250, ExtendedAttribute, FieldControlWord, FieldShift, OpCode, Order,
    Tn5250Error, DEFAULT_CODE_PAGE, MIN_RECORD_LEN,
};
use crate::ebcdic;

/// Helper: build a minimal WTD record from a header and a payload.
fn make_wtd_record(payload: &[u8]) -> Vec<u8> {
    let total = MIN_RECORD_LEN + payload.len();
    let mut buf = Vec::with_capacity(total);
    buf.push((total >> 8) as u8); // length high
    buf.push((total & 0xFF) as u8); // length low
    buf.push(0x04); // record type: data
    buf.push(0x00); // reserved
    buf.push(0x01); // opcode: Write to Display
    buf.extend_from_slice(payload);
    buf
}

// -- Address decoding ---------------------------------------------------

#[test]
fn test_decode_address_basic() {
    assert_eq!(decode_address(1, 1).unwrap(), (0, 0));
    assert_eq!(decode_address(24, 80).unwrap(), (23, 79));
}

#[test]
fn test_decode_address_mid_screen() {
    assert_eq!(decode_address(12, 40).unwrap(), (11, 39));
}

#[test]
fn test_decode_address_zero_row_fails() {
    assert!(decode_address(0, 1).is_err());
}

#[test]
fn test_decode_address_zero_col_fails() {
    assert!(decode_address(1, 0).is_err());
}

#[test]
fn test_encode_address_roundtrip() {
    let (r, c) = encode_address(5, 10);
    assert_eq!(decode_address(r, c).unwrap(), (5, 10));
}

// -- OpCode parsing -----------------------------------------------------

#[test]
fn test_opcode_write_to_display() {
    assert_eq!(OpCode::from_byte(0x01).unwrap(), OpCode::WriteToDisplay);
}

#[test]
fn test_opcode_write_to_display_alt() {
    assert_eq!(OpCode::from_byte(0x11).unwrap(), OpCode::WriteToDisplayAlt);
}

#[test]
fn test_opcode_clear_unit() {
    assert_eq!(OpCode::from_byte(0x02).unwrap(), OpCode::ClearUnit);
}

#[test]
fn test_opcode_clear_format_table() {
    assert_eq!(OpCode::from_byte(0x04).unwrap(), OpCode::ClearFormatTable);
}

#[test]
fn test_opcode_unknown() {
    assert!(OpCode::from_byte(0xFF).is_err());
}

// -- Field Control Word -------------------------------------------------

#[test]
fn test_fcw_bypass_field() {
    let fcw = FieldControlWord::from_bytes(0x80, 0x00);
    assert!(fcw.bypass);
    assert!(!fcw.modified);
    assert_eq!(fcw.shift, FieldShift::Alpha);
    assert!(!fcw.mandatory_fill);
}

#[test]
fn test_fcw_modified_numeric() {
    let fcw = FieldControlWord::from_bytes(0x28, 0x00);
    assert!(!fcw.bypass);
    assert!(fcw.modified);
    assert_eq!(fcw.shift, FieldShift::Numeric);
}

#[test]
fn test_fcw_numeric_only() {
    let fcw = FieldControlWord::from_bytes(0x0C, 0x00);
    assert_eq!(fcw.shift, FieldShift::NumericOnly);
}

#[test]
fn test_fcw_signed_numeric() {
    let fcw = FieldControlWord::from_bytes(0x1C, 0x00);
    assert_eq!(fcw.shift, FieldShift::SignedNumeric);
}

#[test]
fn test_fcw_alpha_only() {
    let fcw = FieldControlWord::from_bytes(0x04, 0x00);
    assert_eq!(fcw.shift, FieldShift::AlphaOnly);
}

#[test]
fn test_fcw_mandatory_fill() {
    let fcw = FieldControlWord::from_bytes(0x00, 0x80);
    assert!(fcw.mandatory_fill);
    assert!(!fcw.right_adjust_zero);
    assert!(!fcw.mandatory_entry);
}

#[test]
fn test_fcw_right_adjust_zero() {
    let fcw = FieldControlWord::from_bytes(0x00, 0x40);
    assert!(fcw.right_adjust_zero);
}

#[test]
fn test_fcw_right_adjust_blank() {
    let fcw = FieldControlWord::from_bytes(0x00, 0x20);
    assert!(fcw.right_adjust_blank);
}

#[test]
fn test_fcw_mandatory_entry() {
    let fcw = FieldControlWord::from_bytes(0x00, 0x10);
    assert!(fcw.mandatory_entry);
}

#[test]
fn test_fcw_auto_enter() {
    let fcw = FieldControlWord::from_bytes(0x02, 0x00);
    assert!(fcw.auto_enter);
}

#[test]
fn test_fcw_field_exit_required() {
    let fcw = FieldControlWord::from_bytes(0x01, 0x00);
    assert!(fcw.field_exit_required);
}

#[test]
fn test_fcw_to_bytes_roundtrip() {
    let fcw = FieldControlWord::from_bytes(0xA8, 0xC0);
    let [b0, b1] = fcw.to_bytes();
    assert_eq!(b0, 0xA8);
    assert_eq!(b1, 0xC0);
}

// -- Record parsing: ClearUnit ------------------------------------------

#[test]
fn test_parse_clear_unit() {
    let data = [
        0x00, 0x05, // length = 5
        0x04, // record type
        0x00, // reserved
        0x02, // opcode: ClearUnit
    ];
    let rec = parse_5250_record(&data).unwrap();
    assert_eq!(rec.opcode, OpCode::ClearUnit);
    assert!(rec.orders.is_empty());
}

// -- Record parsing: ClearFormatTable -----------------------------------

#[test]
fn test_parse_clear_format_table() {
    let data = [
        0x00, 0x05, // length = 5
        0x04, // record type
        0x00, // reserved
        0x04, // opcode: ClearFormatTable
    ];
    let rec = parse_5250_record(&data).unwrap();
    assert_eq!(rec.opcode, OpCode::ClearFormatTable);
    assert!(rec.orders.is_empty());
}

// -- SBA parsing --------------------------------------------------------

#[test]
fn test_parse_sba() {
    let payload = [0x10, 0x05, 0x0A, 0xC1];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 2);
    assert_eq!(
        rec.orders[0],
        DataStreamItem5250::Order(Order::Sba(4, 9)) // 0-based
    );
    assert_eq!(rec.orders[1], DataStreamItem5250::Character(0xC1));
}

// -- SF parsing ---------------------------------------------------------

#[test]
fn test_parse_start_field() {
    let payload = [0x20, 0x80, 0x80];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 1);
    match &rec.orders[0] {
        DataStreamItem5250::Order(Order::Sf(fcw)) => {
            assert!(fcw.bypass);
            assert!(fcw.mandatory_fill);
        }
        other => panic!("Expected SF order, got {:?}", other),
    }
}

// -- RA parsing ---------------------------------------------------------

#[test]
fn test_parse_repeat_to_address() {
    let payload = [0x02, 0x01, 0x50, 0x40];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 1);
    assert_eq!(
        rec.orders[0],
        DataStreamItem5250::Order(Order::Ra(0, 79, 0x40))
    );
}

// -- EA parsing ---------------------------------------------------------

#[test]
fn test_parse_erase_to_address() {
    let payload = [0x03, 0x03, 0x14];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 1);
    assert_eq!(rec.orders[0], DataStreamItem5250::Order(Order::Ea(2, 19)));
}

// -- TD parsing ---------------------------------------------------------

#[test]
fn test_parse_transparent_data() {
    let payload = [0x04, 0x03, 0xAA, 0xBB, 0xCC];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 1);
    assert_eq!(
        rec.orders[0],
        DataStreamItem5250::Order(Order::Td(vec![0xAA, 0xBB, 0xCC]))
    );
}

// -- IC parsing ---------------------------------------------------------

#[test]
fn test_parse_insert_cursor() {
    let payload = [0x29];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 1);
    assert_eq!(rec.orders[0], DataStreamItem5250::Order(Order::Ic));
}

// -- WEA parsing --------------------------------------------------------

#[test]
fn test_parse_wea() {
    let payload = [0x11, 0x01, 0x22];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 1);
    assert_eq!(
        rec.orders[0],
        DataStreamItem5250::Order(Order::Wea(ExtendedAttribute {
            attr_type: 0x01,
            attr_value: 0x22,
        }))
    );
}

// -- SOH parsing --------------------------------------------------------

#[test]
fn test_parse_soh() {
    let payload = [0x01, 0x02, 0xAA, 0xBB];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 1);
    match &rec.orders[0] {
        DataStreamItem5250::Order(Order::Soh(soh)) => {
            assert_eq!(soh.length, 2);
            assert_eq!(soh.data, vec![0xAA, 0xBB]);
        }
        other => panic!("Expected SOH, got {:?}", other),
    }
}

// -- Mixed content ------------------------------------------------------

#[test]
fn test_parse_mixed_orders_and_characters() {
    let payload = [
        0x10, 0x01, 0x01, // SBA row=1, col=1
        0xC8, // 'H'
        0xC9, // 'I'
        0x29, // IC
    ];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.orders.len(), 4);
    assert_eq!(rec.orders[0], DataStreamItem5250::Order(Order::Sba(0, 0)));
    assert_eq!(rec.orders[1], DataStreamItem5250::Character(0xC8));
    assert_eq!(rec.orders[2], DataStreamItem5250::Character(0xC9));
    assert_eq!(rec.orders[3], DataStreamItem5250::Order(Order::Ic));
}

// -- Complex record: SBA + SF + characters + RA -------------------------

#[test]
fn test_parse_complex_record() {
    let payload = [
        0x10, 0x02, 0x05, // SBA row=2, col=5
        0x20, 0x00, 0x00, // SF: unprotected alpha
        0xC8, 0xC5, 0xD3, 0xD3, 0xD6, // "HELLO" in EBCDIC
        0x02, 0x02, 0x50, 0x40, // RA to (2,80) with space
    ];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();

    // SBA + SF + H + E + L + L + O + RA = 8 items
    assert_eq!(rec.orders.len(), 8);

    assert_eq!(rec.orders[0], DataStreamItem5250::Order(Order::Sba(1, 4)));
    match &rec.orders[1] {
        DataStreamItem5250::Order(Order::Sf(fcw)) => {
            assert!(!fcw.bypass);
            assert_eq!(fcw.shift, FieldShift::Alpha);
        }
        other => panic!("Expected SF, got {:?}", other),
    }
    assert_eq!(rec.orders[2], DataStreamItem5250::Character(0xC8)); // H
    assert_eq!(rec.orders[3], DataStreamItem5250::Character(0xC5)); // E
    assert_eq!(rec.orders[4], DataStreamItem5250::Character(0xD3)); // L
    assert_eq!(rec.orders[5], DataStreamItem5250::Character(0xD3)); // L
    assert_eq!(rec.orders[6], DataStreamItem5250::Character(0xD6)); // O

    assert_eq!(
        rec.orders[7],
        DataStreamItem5250::Order(Order::Ra(1, 79, 0x40))
    );
}

// -- Error cases --------------------------------------------------------

#[test]
fn test_record_too_short() {
    let data = [0x00, 0x03, 0x04];
    assert!(matches!(
        parse_5250_record(&data),
        Err(Tn5250Error::RecordTooShort(3))
    ));
}

#[test]
fn test_record_length_exceeds_data() {
    let data = [0x00, 0xFF, 0x04, 0x00, 0x01];
    assert!(matches!(
        parse_5250_record(&data),
        Err(Tn5250Error::RecordLengthMismatch { .. })
    ));
}

#[test]
fn test_truncated_sba() {
    let payload = [0x10, 0x01];
    let record = make_wtd_record(&payload);
    assert!(matches!(
        parse_5250_record(&record),
        Err(Tn5250Error::TruncatedOrder { order: 0x10, .. })
    ));
}

#[test]
fn test_truncated_sf() {
    let payload = [0x20, 0x00];
    let record = make_wtd_record(&payload);
    assert!(matches!(
        parse_5250_record(&record),
        Err(Tn5250Error::TruncatedOrder { order: 0x20, .. })
    ));
}

#[test]
fn test_truncated_ra() {
    let payload = [0x02, 0x01, 0x01];
    let record = make_wtd_record(&payload);
    assert!(matches!(
        parse_5250_record(&record),
        Err(Tn5250Error::TruncatedOrder { order: 0x02, .. })
    ));
}

#[test]
fn test_truncated_soh() {
    let payload = [0x01, 0x05, 0xAA, 0xBB];
    let record = make_wtd_record(&payload);
    assert!(matches!(
        parse_5250_record(&record),
        Err(Tn5250Error::TruncatedOrder { order: 0x01, .. })
    ));
}

#[test]
fn test_truncated_td() {
    let payload = [0x04, 0x04, 0xAA, 0xBB];
    let record = make_wtd_record(&payload);
    assert!(matches!(
        parse_5250_record(&record),
        Err(Tn5250Error::TruncatedOrder { order: 0x04, .. })
    ));
}

// -- Empty WTD ----------------------------------------------------------

#[test]
fn test_parse_empty_wtd() {
    let record = make_wtd_record(&[]);
    let rec = parse_5250_record(&record).unwrap();
    assert_eq!(rec.opcode, OpCode::WriteToDisplay);
    assert!(rec.orders.is_empty());
}

// -- Response builder ---------------------------------------------------

#[test]
fn test_build_response_record() {
    let response = build_response_record(&[0xF1, 0x01, 0x01]);
    assert_eq!(response.len(), 8); // 5 header + 3 payload
    assert_eq!(response[0], 0x00);
    assert_eq!(response[1], 0x08); // length = 8
    assert_eq!(response[2], 0x00); // record type: response
    assert_eq!(response[5], 0xF1); // AID
}

// -- AID key mapping ----------------------------------------------------

#[test]
fn test_aid_bytes() {
    assert_eq!(aid_byte_for_key("Enter"), Some(0xF1));
    assert_eq!(aid_byte_for_key("F1"), Some(0x31));
    assert_eq!(aid_byte_for_key("F12"), Some(0x3C));
    assert_eq!(aid_byte_for_key("PageUp"), Some(0xF4));
    assert_eq!(aid_byte_for_key("PageDown"), Some(0xF5));
    assert_eq!(aid_byte_for_key("Help"), Some(0xF3));
    assert_eq!(aid_byte_for_key("Clear"), Some(0xBD));
    assert_eq!(aid_byte_for_key("Unknown"), None);
}

// -- EBCDIC decode via shared codec -------------------------------------

#[test]
fn test_ebcdic_decode_of_parsed_characters() {
    let payload = [
        0x10, 0x01, 0x01, // SBA(1,1)
        0xE3, 0xC5, 0xE2, 0xE3, // "TEST" in EBCDIC
    ];
    let record = make_wtd_record(&payload);
    let rec = parse_5250_record(&record).unwrap();

    let text: String = rec
        .orders
        .iter()
        .filter_map(|item| match item {
            DataStreamItem5250::Character(b) => {
                Some(ebcdic::ebcdic_to_unicode(*b, DEFAULT_CODE_PAGE))
            }
            _ => None,
        })
        .collect();

    assert_eq!(text, "TEST");
}

// -- WriteToDisplayAlt --------------------------------------------------

#[test]
fn test_parse_wtd_alt() {
    let data = vec![
        0x00, 0x08, // length = 8
        0x04, // record type
        0x00, // reserved
        0x11, // opcode: WriteToDisplayAlt
        0x10, 0x01, 0x01, // SBA(1,1)
    ];
    assert_eq!(data.len(), 8);
    let rec = parse_5250_record(&data).unwrap();
    assert_eq!(rec.opcode, OpCode::WriteToDisplayAlt);
    assert_eq!(rec.orders.len(), 1);
}
