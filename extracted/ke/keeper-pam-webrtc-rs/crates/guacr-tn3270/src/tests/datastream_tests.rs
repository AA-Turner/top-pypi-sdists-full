use crate::datastream::{
    decode_buffer_address, encode_buffer_address, encode_buffer_address_14bit, parse_data_stream,
    Aid, Color3270, DataStreamItem, ExtendedAttribute, FieldAttribute, Highlighting, Intensity,
    Order, Wcc, WriteCommand, CMD_ERASE_WRITE, CMD_ERASE_WRITE_SNA, CMD_WRITE,
    CMD_WRITE_STRUCTURED_FIELD, ORDER_EUA, ORDER_IC, ORDER_PT, ORDER_RA, ORDER_SA, ORDER_SBA,
    ORDER_SF, ORDER_SFE,
};

// -- WriteCommand tests --

#[test]
fn test_write_command_standard() {
    assert_eq!(WriteCommand::from_byte(0x01).unwrap(), WriteCommand::Write);
    assert_eq!(
        WriteCommand::from_byte(0x05).unwrap(),
        WriteCommand::EraseWrite
    );
    assert_eq!(
        WriteCommand::from_byte(0x0D).unwrap(),
        WriteCommand::EraseWriteAlternate
    );
    assert_eq!(
        WriteCommand::from_byte(0x11).unwrap(),
        WriteCommand::WriteStructuredField
    );
}

#[test]
fn test_write_command_sna() {
    assert_eq!(WriteCommand::from_byte(0xF1).unwrap(), WriteCommand::Write);
    assert_eq!(
        WriteCommand::from_byte(0xF5).unwrap(),
        WriteCommand::EraseWrite
    );
    assert_eq!(
        WriteCommand::from_byte(0x7E).unwrap(),
        WriteCommand::EraseWriteAlternate
    );
    assert_eq!(
        WriteCommand::from_byte(0xF3).unwrap(),
        WriteCommand::WriteStructuredField
    );
}

#[test]
fn test_write_command_unknown() {
    assert!(WriteCommand::from_byte(0xFF).is_err());
    assert!(WriteCommand::from_byte(0x00).is_err());
}

// -- WCC tests --

#[test]
fn test_wcc_all_bits_set() {
    let wcc = Wcc::from_byte(0x62);
    assert!(wcc.reset_mdt);
    assert!(wcc.restore_keyboard);
    assert!(wcc.alarm);
}

#[test]
fn test_wcc_no_bits_set() {
    let wcc = Wcc::from_byte(0x00);
    assert!(!wcc.reset_mdt);
    assert!(!wcc.restore_keyboard);
    assert!(!wcc.alarm);
}

#[test]
fn test_wcc_reset_mdt_only() {
    let wcc = Wcc::from_byte(0x40);
    assert!(wcc.reset_mdt);
    assert!(!wcc.restore_keyboard);
    assert!(!wcc.alarm);
}

#[test]
fn test_wcc_restore_keyboard_only() {
    let wcc = Wcc::from_byte(0x20);
    assert!(!wcc.reset_mdt);
    assert!(wcc.restore_keyboard);
    assert!(!wcc.alarm);
}

#[test]
fn test_wcc_alarm_only() {
    let wcc = Wcc::from_byte(0x02);
    assert!(!wcc.reset_mdt);
    assert!(!wcc.restore_keyboard);
    assert!(wcc.alarm);
}

#[test]
fn test_wcc_roundtrip() {
    let original = Wcc {
        reset_mdt: true,
        restore_keyboard: true,
        alarm: true,
    };
    let byte = original.to_byte();
    let parsed = Wcc::from_byte(byte);
    assert_eq!(parsed, original);
}

// -- FieldAttribute tests --

#[test]
fn test_field_attribute_unprotected_normal() {
    let attr = FieldAttribute::from_byte(0x00);
    assert!(!attr.protected);
    assert!(!attr.numeric);
    assert_eq!(attr.intensity, Intensity::Normal);
    assert!(!attr.modified);
}

#[test]
fn test_field_attribute_protected() {
    let attr = FieldAttribute::from_byte(0x20);
    assert!(attr.protected);
    assert!(!attr.numeric);
}

#[test]
fn test_field_attribute_numeric() {
    let attr = FieldAttribute::from_byte(0x10);
    assert!(!attr.protected);
    assert!(attr.numeric);
}

#[test]
fn test_field_attribute_skip() {
    // Protected + numeric = skip field
    let attr = FieldAttribute::from_byte(0x30);
    assert!(attr.protected);
    assert!(attr.numeric);
    assert!(attr.is_skip());
}

#[test]
fn test_field_attribute_intensified() {
    // Intensity bits 10 = intensified (bit positions 2-3)
    let attr = FieldAttribute::from_byte(0x08);
    assert_eq!(attr.intensity, Intensity::Intensified);
}

#[test]
fn test_field_attribute_invisible() {
    // Intensity bits 11 = invisible (bit positions 2-3)
    let attr = FieldAttribute::from_byte(0x0C);
    assert_eq!(attr.intensity, Intensity::Invisible);
}

#[test]
fn test_field_attribute_modified() {
    let attr = FieldAttribute::from_byte(0x01);
    assert!(attr.modified);
}

#[test]
fn test_field_attribute_roundtrip() {
    let original = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Intensified,
        modified: true,
    };
    let byte = original.to_byte();
    let parsed = FieldAttribute::from_byte(byte);
    assert_eq!(parsed, original);
}

#[test]
fn test_field_attribute_all_combinations() {
    // Verify roundtrip for all reasonable combinations
    for &prot in &[false, true] {
        for &num in &[false, true] {
            for &intensity in &[
                Intensity::Normal,
                Intensity::Intensified,
                Intensity::Invisible,
            ] {
                for &modified in &[false, true] {
                    let original = FieldAttribute {
                        protected: prot,
                        numeric: num,
                        intensity,
                        modified,
                    };
                    let byte = original.to_byte();
                    let parsed = FieldAttribute::from_byte(byte);
                    assert_eq!(parsed, original, "Roundtrip failed for {:?}", original);
                }
            }
        }
    }
}

// -- Buffer address tests --

#[test]
fn test_decode_buffer_address_12bit() {
    assert_eq!(decode_buffer_address(0x40, 0x40), 0);
    assert_eq!(decode_buffer_address(0xC1, 0x50), 80);
}

#[test]
fn test_decode_buffer_address_14bit() {
    assert_eq!(decode_buffer_address(0x01, 0x00), 256);
    assert_eq!(decode_buffer_address(0x07, 0x80), 1920);
}

#[test]
fn test_encode_buffer_address_12bit() {
    let (b1, b2) = encode_buffer_address(0);
    assert_eq!(decode_buffer_address(b1, b2), 0);

    let (b1, b2) = encode_buffer_address(80);
    assert_eq!(decode_buffer_address(b1, b2), 80);

    let (b1, b2) = encode_buffer_address(1919);
    assert_eq!(decode_buffer_address(b1, b2), 1919);
}

#[test]
fn test_encode_buffer_address_14bit() {
    let (b1, b2) = encode_buffer_address_14bit(256);
    assert_eq!(decode_buffer_address(b1, b2), 256);

    let (b1, b2) = encode_buffer_address_14bit(1920);
    assert_eq!(decode_buffer_address(b1, b2), 1920);
}

#[test]
fn test_encode_decode_address_roundtrip() {
    // Test all valid 12-bit addresses (0-4095)
    for addr in 0..4096u16 {
        let (b1, b2) = encode_buffer_address(addr);
        let decoded = decode_buffer_address(b1, b2);
        assert_eq!(decoded, addr, "Roundtrip failed for address {}", addr);
    }
}

// -- Data stream parsing tests --

#[test]
fn test_parse_empty() {
    assert!(parse_data_stream(&[]).is_err());
}

#[test]
fn test_parse_write_no_data() {
    let data = [CMD_WRITE, 0x00];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.command, WriteCommand::Write);
    assert!(!ds.wcc.reset_mdt);
    assert!(!ds.wcc.restore_keyboard);
    assert!(!ds.wcc.alarm);
    assert!(ds.orders.is_empty());
}

#[test]
fn test_parse_erase_write_with_wcc() {
    let data = [CMD_ERASE_WRITE, 0x62];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.command, WriteCommand::EraseWrite);
    assert!(ds.wcc.reset_mdt);
    assert!(ds.wcc.restore_keyboard);
    assert!(ds.wcc.alarm);
}

#[test]
fn test_parse_character_data() {
    let data = [CMD_WRITE, 0x00, 0xC8, 0xC5, 0xD3, 0xD3, 0xD6]; // "HELLO"
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 5);
    assert_eq!(ds.orders[0], DataStreamItem::Character(0xC8));
    assert_eq!(ds.orders[1], DataStreamItem::Character(0xC5));
    assert_eq!(ds.orders[2], DataStreamItem::Character(0xD3));
    assert_eq!(ds.orders[3], DataStreamItem::Character(0xD3));
    assert_eq!(ds.orders[4], DataStreamItem::Character(0xD6));
}

#[test]
fn test_parse_sba_order() {
    let data = [CMD_WRITE, 0x00, ORDER_SBA, 0xC1, 0x50];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    assert_eq!(ds.orders[0], DataStreamItem::Order(Order::Sba(80)));
}

#[test]
fn test_parse_sf_order() {
    let data = [CMD_WRITE, 0x00, ORDER_SF, 0x20];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    match &ds.orders[0] {
        DataStreamItem::Order(Order::Sf(attr)) => {
            assert!(attr.protected);
            assert!(!attr.numeric);
            assert_eq!(attr.intensity, Intensity::Normal);
            assert!(!attr.modified);
        }
        other => panic!("Expected SF order, got {:?}", other),
    }
}

#[test]
fn test_parse_ic_order() {
    let data = [CMD_WRITE, 0x00, ORDER_IC];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    assert_eq!(ds.orders[0], DataStreamItem::Order(Order::Ic));
}

#[test]
fn test_parse_pt_order() {
    let data = [CMD_WRITE, 0x00, ORDER_PT];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    assert_eq!(ds.orders[0], DataStreamItem::Order(Order::Pt));
}

#[test]
fn test_parse_ra_order() {
    let (b1, b2) = encode_buffer_address(160);
    let data = [CMD_WRITE, 0x00, ORDER_RA, b1, b2, 0x00];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    assert_eq!(ds.orders[0], DataStreamItem::Order(Order::Ra(160, 0x00)));
}

#[test]
fn test_parse_eua_order() {
    let (b1, b2) = encode_buffer_address(240);
    let data = [CMD_WRITE, 0x00, ORDER_EUA, b1, b2];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    assert_eq!(ds.orders[0], DataStreamItem::Order(Order::Eua(240)));
}

#[test]
fn test_parse_sfe_order() {
    let data = [CMD_WRITE, 0x00, ORDER_SFE, 0x01, 0xC0, 0x20];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    match &ds.orders[0] {
        DataStreamItem::Order(Order::Sfe(attrs)) => {
            assert_eq!(attrs.len(), 1);
            match attrs[0] {
                ExtendedAttribute::FieldAttribute(fa) => {
                    assert!(fa.protected);
                }
                _ => panic!("Expected FieldAttribute"),
            }
        }
        other => panic!("Expected SFE order, got {:?}", other),
    }
}

#[test]
fn test_parse_sfe_multiple_pairs() {
    let data = [
        CMD_WRITE, 0x00, ORDER_SFE, 0x02, // count=2
        0xC0, 0x20, // field attr: protected
        0x42, 0xF2, // foreground: red
    ];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    match &ds.orders[0] {
        DataStreamItem::Order(Order::Sfe(attrs)) => {
            assert_eq!(attrs.len(), 2);
            match attrs[0] {
                ExtendedAttribute::FieldAttribute(fa) => assert!(fa.protected),
                _ => panic!("Expected FieldAttribute"),
            }
            match attrs[1] {
                ExtendedAttribute::ForegroundColor(c) => assert_eq!(c, Color3270::Red),
                _ => panic!("Expected ForegroundColor"),
            }
        }
        other => panic!("Expected SFE order, got {:?}", other),
    }
}

#[test]
fn test_parse_sa_order() {
    let data = [CMD_WRITE, 0x00, ORDER_SA, 0x42, 0xF4];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.orders.len(), 1);
    match &ds.orders[0] {
        DataStreamItem::Order(Order::Sa(ExtendedAttribute::ForegroundColor(c))) => {
            assert_eq!(*c, Color3270::Green);
        }
        other => panic!("Expected SA order with green, got {:?}", other),
    }
}

#[test]
fn test_parse_complex_stream() {
    let (sba0_b1, sba0_b2) = encode_buffer_address(0);
    let (sba80_b1, sba80_b2) = encode_buffer_address(80);
    let data = [
        CMD_ERASE_WRITE,
        0x60,
        ORDER_SBA,
        sba0_b1,
        sba0_b2,
        ORDER_SF,
        0x20,
        0xD3,
        0xD6,
        0xC7,
        0xD6,
        0xD5,
        ORDER_SBA,
        sba80_b1,
        sba80_b2,
        ORDER_SF,
        0x00,
        ORDER_IC,
    ];

    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.command, WriteCommand::EraseWrite);
    assert!(ds.wcc.reset_mdt);
    assert!(ds.wcc.restore_keyboard);
    assert!(!ds.wcc.alarm);

    assert_eq!(ds.orders.len(), 10);
    assert_eq!(ds.orders[0], DataStreamItem::Order(Order::Sba(0)));
    match &ds.orders[1] {
        DataStreamItem::Order(Order::Sf(attr)) => assert!(attr.protected),
        other => panic!("Expected SF, got {:?}", other),
    }
    assert_eq!(ds.orders[2], DataStreamItem::Character(0xD3));
    assert_eq!(ds.orders[3], DataStreamItem::Character(0xD6));
    assert_eq!(ds.orders[4], DataStreamItem::Character(0xC7));
    assert_eq!(ds.orders[5], DataStreamItem::Character(0xD6));
    assert_eq!(ds.orders[6], DataStreamItem::Character(0xD5));
    assert_eq!(ds.orders[7], DataStreamItem::Order(Order::Sba(80)));
    match &ds.orders[8] {
        DataStreamItem::Order(Order::Sf(attr)) => assert!(!attr.protected),
        other => panic!("Expected SF, got {:?}", other),
    }
    assert_eq!(ds.orders[9], DataStreamItem::Order(Order::Ic));
}

#[test]
fn test_parse_sna_erase_write() {
    let data = [CMD_ERASE_WRITE_SNA, 0x00];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.command, WriteCommand::EraseWrite);
}

#[test]
fn test_parse_wsf() {
    let data = [CMD_WRITE_STRUCTURED_FIELD, 0xAA, 0xBB, 0xCC];
    let ds = parse_data_stream(&data).unwrap();
    assert_eq!(ds.command, WriteCommand::WriteStructuredField);
    assert_eq!(ds.orders.len(), 3);
    assert_eq!(ds.orders[0], DataStreamItem::Character(0xAA));
}

#[test]
fn test_parse_truncated_sba() {
    let data = [CMD_WRITE, 0x00, ORDER_SBA, 0x40];
    assert!(parse_data_stream(&data).is_err());
}

#[test]
fn test_parse_truncated_sf() {
    let data = [CMD_WRITE, 0x00, ORDER_SF];
    assert!(parse_data_stream(&data).is_err());
}

#[test]
fn test_parse_truncated_ra() {
    let data = [CMD_WRITE, 0x00, ORDER_RA, 0x40, 0x40];
    assert!(parse_data_stream(&data).is_err());
}

// -- AID tests --

#[test]
fn test_aid_enter() {
    assert_eq!(Aid::from_byte(Aid::ENTER), Aid::Enter);
    assert_eq!(Aid::Enter.to_byte(), Aid::ENTER);
}

#[test]
fn test_aid_clear() {
    assert_eq!(Aid::from_byte(Aid::CLEAR), Aid::Clear);
    assert_eq!(Aid::Clear.to_byte(), Aid::CLEAR);
}

#[test]
fn test_aid_pa_keys() {
    assert_eq!(Aid::from_byte(Aid::PA1), Aid::Pa(1));
    assert_eq!(Aid::from_byte(Aid::PA2), Aid::Pa(2));
    assert_eq!(Aid::from_byte(Aid::PA3), Aid::Pa(3));
    assert_eq!(Aid::Pa(1).to_byte(), Aid::PA1);
    assert_eq!(Aid::Pa(2).to_byte(), Aid::PA2);
    assert_eq!(Aid::Pa(3).to_byte(), Aid::PA3);
}

#[test]
fn test_aid_pf_keys() {
    assert_eq!(Aid::from_byte(0xF1), Aid::Pf(1));
    assert_eq!(Aid::Pf(1).to_byte(), 0xF1);

    assert_eq!(Aid::from_byte(0x7C), Aid::Pf(12));
    assert_eq!(Aid::Pf(12).to_byte(), 0x7C);

    assert_eq!(Aid::from_byte(0xC1), Aid::Pf(13));
    assert_eq!(Aid::Pf(13).to_byte(), 0xC1);

    assert_eq!(Aid::from_byte(0x4C), Aid::Pf(24));
    assert_eq!(Aid::Pf(24).to_byte(), 0x4C);
}

#[test]
fn test_aid_roundtrip_all_pf() {
    for n in 1..=24u8 {
        let byte = Aid::Pf(n).to_byte();
        let parsed = Aid::from_byte(byte);
        assert_eq!(parsed, Aid::Pf(n), "PF{} roundtrip failed", n);
    }
}

// -- Color tests --

#[test]
fn test_color_from_byte() {
    assert_eq!(Color3270::from_byte(0x00), Color3270::Default);
    assert_eq!(Color3270::from_byte(0xF1), Color3270::Blue);
    assert_eq!(Color3270::from_byte(0xF2), Color3270::Red);
    assert_eq!(Color3270::from_byte(0xF3), Color3270::Pink);
    assert_eq!(Color3270::from_byte(0xF4), Color3270::Green);
    assert_eq!(Color3270::from_byte(0xF5), Color3270::Turquoise);
    assert_eq!(Color3270::from_byte(0xF6), Color3270::Yellow);
    assert_eq!(Color3270::from_byte(0xF7), Color3270::White);
}

#[test]
fn test_color_roundtrip() {
    let colors = [
        Color3270::Blue,
        Color3270::Red,
        Color3270::Pink,
        Color3270::Green,
        Color3270::Turquoise,
        Color3270::Yellow,
        Color3270::White,
    ];
    for &color in &colors {
        assert_eq!(Color3270::from_byte(color.to_byte()), color);
    }
}

// -- Highlighting tests --

#[test]
fn test_highlighting_from_byte() {
    assert_eq!(Highlighting::from_byte(0x00), Highlighting::Default);
    assert_eq!(Highlighting::from_byte(0xF0), Highlighting::Default);
    assert_eq!(Highlighting::from_byte(0xF1), Highlighting::Blink);
    assert_eq!(Highlighting::from_byte(0xF2), Highlighting::ReverseVideo);
    assert_eq!(Highlighting::from_byte(0xF4), Highlighting::Underscore);
    assert_eq!(Highlighting::from_byte(0xF8), Highlighting::Intensified);
}

// -- Extended attribute tests --

#[test]
fn test_extended_attribute_field() {
    let ea = ExtendedAttribute::from_pair(0xC0, 0x20);
    match ea {
        ExtendedAttribute::FieldAttribute(fa) => {
            assert!(fa.protected);
        }
        other => panic!("Expected FieldAttribute, got {:?}", other),
    }
}

#[test]
fn test_extended_attribute_highlighting() {
    let ea = ExtendedAttribute::from_pair(0x41, 0xF2);
    match ea {
        ExtendedAttribute::Highlighting(h) => {
            assert_eq!(h, Highlighting::ReverseVideo);
        }
        other => panic!("Expected Highlighting, got {:?}", other),
    }
}

#[test]
fn test_extended_attribute_foreground() {
    let ea = ExtendedAttribute::from_pair(0x42, 0xF4);
    match ea {
        ExtendedAttribute::ForegroundColor(c) => {
            assert_eq!(c, Color3270::Green);
        }
        other => panic!("Expected ForegroundColor, got {:?}", other),
    }
}

#[test]
fn test_extended_attribute_background() {
    let ea = ExtendedAttribute::from_pair(0x45, 0xF1);
    match ea {
        ExtendedAttribute::BackgroundColor(c) => {
            assert_eq!(c, Color3270::Blue);
        }
        other => panic!("Expected BackgroundColor, got {:?}", other),
    }
}

#[test]
fn test_extended_attribute_charset() {
    let ea = ExtendedAttribute::from_pair(0x43, 0xF1);
    match ea {
        ExtendedAttribute::CharacterSet(v) => {
            assert_eq!(v, 0xF1);
        }
        other => panic!("Expected CharacterSet, got {:?}", other),
    }
}

#[test]
fn test_extended_attribute_unknown() {
    let ea = ExtendedAttribute::from_pair(0xFF, 0xAB);
    match ea {
        ExtendedAttribute::Unknown { attr_type, value } => {
            assert_eq!(attr_type, 0xFF);
            assert_eq!(value, 0xAB);
        }
        other => panic!("Expected Unknown, got {:?}", other),
    }
}
