use crate::datastream::DEFAULT_CODE_PAGE;
use crate::datastream::{
    parse_5250_record, DataStreamItem5250, ExtendedAttribute, FieldControlWord, OpCode, Order,
    Record5250, SohData,
};
use crate::ebcdic;
use crate::screen::{color_from_5250_attribute, Color5250, ScreenBuffer5250};

/// Helper: build a Record5250 directly from items (avoids byte-level construction).
fn make_record(opcode: OpCode, orders: Vec<DataStreamItem5250>) -> Record5250 {
    Record5250 {
        record_type: 0x04,
        opcode,
        orders,
    }
}

// -- Basic construction -------------------------------------------------

#[test]
fn test_new_screen() {
    let screen = ScreenBuffer5250::new(24, 80);
    assert_eq!(screen.rows(), 24);
    assert_eq!(screen.cols(), 80);
    assert_eq!(screen.cursor_pos(), (0, 0));
    assert!(screen.get_fields().is_empty());
}

#[test]
fn test_get_cell_default() {
    let screen = ScreenBuffer5250::new(24, 80);
    let cell = screen.get_cell(0, 0).unwrap();
    assert_eq!(cell.character, ' ');
    assert_eq!(cell.foreground, Color5250::Green);
    assert_eq!(cell.background, Color5250::Black);
    assert!(!cell.underline);
    assert!(!cell.field_start);
}

#[test]
fn test_get_cell_out_of_bounds() {
    let screen = ScreenBuffer5250::new(24, 80);
    assert!(screen.get_cell(24, 0).is_none());
    assert!(screen.get_cell(0, 80).is_none());
}

// -- ClearUnit ----------------------------------------------------------

#[test]
fn test_clear_unit() {
    let mut screen = ScreenBuffer5250::new(24, 80);

    let write = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Character(0xC8), // 'H'
        ],
    );
    screen.apply_record(&write);
    assert_eq!(screen.get_cell(0, 0).unwrap().character, 'H');

    let clear = make_record(OpCode::ClearUnit, vec![]);
    screen.apply_record(&clear);
    assert_eq!(screen.get_cell(0, 0).unwrap().character, ' ');
    assert_eq!(screen.cursor_pos(), (0, 0));
}

// -- SBA + character write ----------------------------------------------

#[test]
fn test_sba_and_characters() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(5, 10)),
            DataStreamItem5250::Character(0xC8), // 'H'
            DataStreamItem5250::Character(0xC9), // 'I'
        ],
    );
    screen.apply_record(&record);

    assert_eq!(screen.get_cell(5, 10).unwrap().character, 'H');
    assert_eq!(screen.get_cell(5, 11).unwrap().character, 'I');
    assert_eq!(screen.get_cell(5, 12).unwrap().character, ' ');
}

// -- Insert Cursor ------------------------------------------------------

#[test]
fn test_insert_cursor() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(10, 20)),
            DataStreamItem5250::Order(Order::Ic),
        ],
    );
    screen.apply_record(&record);
    assert_eq!(screen.cursor_pos(), (10, 20));
}

// -- Repeat to Address --------------------------------------------------

#[test]
fn test_repeat_to_address() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Ra(0, 4, 0x5C)),
        ],
    );
    screen.apply_record(&record);

    for col in 0..=4 {
        assert_eq!(
            screen.get_cell(0, col).unwrap().character,
            '*',
            "col {} should be '*'",
            col
        );
    }
    assert_eq!(screen.get_cell(0, 5).unwrap().character, ' ');
}

// -- Erase to Address ---------------------------------------------------

#[test]
fn test_erase_to_address() {
    let mut screen = ScreenBuffer5250::new(24, 80);

    let write = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Character(0xC1), // A
            DataStreamItem5250::Character(0xC2), // B
            DataStreamItem5250::Character(0xC3), // C
            DataStreamItem5250::Character(0xC4), // D
            DataStreamItem5250::Character(0xC5), // E
        ],
    );
    screen.apply_record(&write);
    assert_eq!(screen.get_cell(0, 0).unwrap().character, 'A');

    let erase = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 1)),
            DataStreamItem5250::Order(Order::Ea(0, 3)),
        ],
    );
    screen.apply_record(&erase);

    assert_eq!(screen.get_cell(0, 0).unwrap().character, 'A'); // untouched
    assert_eq!(screen.get_cell(0, 1).unwrap().character, ' '); // erased
    assert_eq!(screen.get_cell(0, 2).unwrap().character, ' '); // erased
    assert_eq!(screen.get_cell(0, 3).unwrap().character, ' '); // erased
    assert_eq!(screen.get_cell(0, 4).unwrap().character, 'E'); // untouched
}

// -- Start Field --------------------------------------------------------

#[test]
fn test_start_field() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw = FieldControlWord::from_bytes(0x00, 0x00);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(2, 10)),
            DataStreamItem5250::Order(Order::Sf(fcw)),
        ],
    );
    screen.apply_record(&record);

    assert!(screen.get_cell(2, 10).unwrap().field_start);
    assert_eq!(screen.get_fields().len(), 1);
    let field = &screen.get_fields()[0];
    assert_eq!(field.row, 2);
    assert_eq!(field.col, 10);
    assert!(!field.control.bypass);
}

// -- Multiple fields and field length -----------------------------------

#[test]
fn test_multiple_fields_length_computation() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_input = FieldControlWord::from_bytes(0x00, 0x00);
    let fcw_protected = FieldControlWord::from_bytes(0x80, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 5)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
            DataStreamItem5250::Order(Order::Sba(0, 15)),
            DataStreamItem5250::Order(Order::Sf(fcw_protected)),
        ],
    );
    screen.apply_record(&record);

    let fields = screen.get_fields();
    assert_eq!(fields.len(), 2);
    // Field 1: data from (0,6) to (0,14) = 9 characters
    assert_eq!(fields[0].length, 9);
}

// -- Tab forward --------------------------------------------------------

#[test]
fn test_tab_forward() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_input = FieldControlWord::from_bytes(0x00, 0x00);
    let fcw_protected = FieldControlWord::from_bytes(0x80, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Sf(fcw_protected)),
            DataStreamItem5250::Order(Order::Sba(0, 20)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
            DataStreamItem5250::Order(Order::Sba(0, 40)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
        ],
    );
    screen.apply_record(&record);

    assert!(screen.tab_forward());
    assert_eq!(screen.cursor_pos(), (0, 21));
}

// -- Tab backward -------------------------------------------------------

#[test]
fn test_tab_backward() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_input = FieldControlWord::from_bytes(0x00, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 10)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
            DataStreamItem5250::Order(Order::Sba(0, 30)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
            DataStreamItem5250::Order(Order::Sba(0, 35)),
            DataStreamItem5250::Order(Order::Ic),
        ],
    );
    screen.apply_record(&record);

    assert_eq!(screen.cursor_pos(), (0, 35));
    assert!(screen.tab_backward());
    assert_eq!(screen.cursor_pos(), (0, 11));
}

// -- Type character -----------------------------------------------------

#[test]
fn test_type_character() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_input = FieldControlWord::from_bytes(0x00, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 5)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
            DataStreamItem5250::Order(Order::Sba(0, 6)),
            DataStreamItem5250::Order(Order::Ic),
        ],
    );
    screen.apply_record(&record);

    assert!(screen.type_character('A'));
    assert_eq!(screen.get_cell(0, 6).unwrap().character, 'A');
    assert_eq!(screen.cursor_pos(), (0, 7));

    assert!(screen.get_fields()[0].modified);
}

#[test]
fn test_type_in_protected_field_rejected() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_protected = FieldControlWord::from_bytes(0x80, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 5)),
            DataStreamItem5250::Order(Order::Sf(fcw_protected)),
            DataStreamItem5250::Order(Order::Sba(0, 6)),
            DataStreamItem5250::Order(Order::Ic),
        ],
    );
    screen.apply_record(&record);

    assert!(!screen.type_character('X'));
    assert_eq!(screen.get_cell(0, 6).unwrap().character, ' ');
}

#[test]
fn test_type_numeric_only_rejects_alpha() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_num = FieldControlWord::from_bytes(0x0C, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 5)),
            DataStreamItem5250::Order(Order::Sf(fcw_num)),
            DataStreamItem5250::Order(Order::Sba(0, 6)),
            DataStreamItem5250::Order(Order::Ic),
        ],
    );
    screen.apply_record(&record);

    assert!(!screen.type_character('A')); // rejected
    assert!(screen.type_character('5')); // accepted
    assert_eq!(screen.get_cell(0, 6).unwrap().character, '5');
}

// -- Read modified fields -----------------------------------------------

#[test]
fn test_read_modified_fields() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_input = FieldControlWord::from_bytes(0x00, 0x00);
    let fcw_protected = FieldControlWord::from_bytes(0x80, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
            DataStreamItem5250::Order(Order::Sba(0, 10)),
            DataStreamItem5250::Order(Order::Sf(fcw_protected)),
            DataStreamItem5250::Order(Order::Sba(0, 1)),
            DataStreamItem5250::Order(Order::Ic),
        ],
    );
    screen.apply_record(&record);

    screen.type_character('H');
    screen.type_character('I');

    let modified = screen.read_modified_fields();
    assert_eq!(modified.len(), 1);
    assert_eq!(modified[0].0, 0); // row
    assert_eq!(modified[0].1, 0); // col

    let text = ebcdic::decode_string(&modified[0].2, DEFAULT_CODE_PAGE);
    assert!(text.starts_with("HI"));
}

// -- Read field ---------------------------------------------------------

#[test]
fn test_read_field() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_input = FieldControlWord::from_bytes(0x00, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
            DataStreamItem5250::Character(0xE3), // T
            DataStreamItem5250::Character(0xC5), // E
            DataStreamItem5250::Character(0xE2), // S
            DataStreamItem5250::Character(0xE3), // T
            DataStreamItem5250::Order(Order::Sba(0, 20)),
            DataStreamItem5250::Order(Order::Sf(fcw_input)),
        ],
    );
    screen.apply_record(&record);

    let text = screen.read_field(0).unwrap();
    assert!(text.starts_with("TEST"));
}

// -- Screen text --------------------------------------------------------

#[test]
fn test_screen_text() {
    let mut screen = ScreenBuffer5250::new(3, 10);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Character(0xC1), // A
            DataStreamItem5250::Character(0xC2), // B
        ],
    );
    screen.apply_record(&record);

    let text = screen.screen_text();
    let lines: Vec<&str> = text.lines().collect();
    assert_eq!(lines.len(), 3);
    assert!(lines[0].starts_with("AB"));
}

// -- ClearFormatTable ---------------------------------------------------

#[test]
fn test_clear_format_table() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw = FieldControlWord::from_bytes(0x00, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 5)),
            DataStreamItem5250::Order(Order::Sf(fcw)),
        ],
    );
    screen.apply_record(&record);
    assert_eq!(screen.get_fields().len(), 1);

    let clear = make_record(OpCode::ClearFormatTable, vec![]);
    screen.apply_record(&clear);
    assert!(screen.get_fields().is_empty());
    assert!(!screen.get_cell(0, 5).unwrap().field_start);
}

// -- Transparent Data ---------------------------------------------------

#[test]
fn test_transparent_data() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Td(vec![0xC8, 0xC5, 0xD3, 0xD3, 0xD6])),
        ],
    );
    screen.apply_record(&record);

    assert_eq!(screen.get_cell(0, 0).unwrap().character, 'H');
    assert_eq!(screen.get_cell(0, 1).unwrap().character, 'E');
    assert_eq!(screen.get_cell(0, 2).unwrap().character, 'L');
    assert_eq!(screen.get_cell(0, 3).unwrap().character, 'L');
    assert_eq!(screen.get_cell(0, 4).unwrap().character, 'O');
}

// -- WEA (extended attribute) -------------------------------------------

#[test]
fn test_wea_foreground_color() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Wea(ExtendedAttribute {
                attr_type: 0x01,
                attr_value: 0x04, // Red
            })),
        ],
    );
    screen.apply_record(&record);
    assert_eq!(screen.get_cell(0, 0).unwrap().foreground, Color5250::Red);
}

#[test]
fn test_wea_underline() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(1, 5)),
            DataStreamItem5250::Order(Order::Wea(ExtendedAttribute {
                attr_type: 0x03,
                attr_value: 0x01,
            })),
        ],
    );
    screen.apply_record(&record);
    assert!(screen.get_cell(1, 5).unwrap().underline);
}

// -- Color mapping ------------------------------------------------------

#[test]
fn test_color_mapping() {
    assert_eq!(color_from_5250_attribute(0x00), Color5250::Black);
    assert_eq!(color_from_5250_attribute(0x01), Color5250::Blue);
    assert_eq!(color_from_5250_attribute(0x02), Color5250::Green);
    assert_eq!(color_from_5250_attribute(0x03), Color5250::Turquoise);
    assert_eq!(color_from_5250_attribute(0x04), Color5250::Red);
    assert_eq!(color_from_5250_attribute(0x05), Color5250::Pink);
    assert_eq!(color_from_5250_attribute(0x06), Color5250::Yellow);
    assert_eq!(color_from_5250_attribute(0x07), Color5250::White);
    assert_eq!(color_from_5250_attribute(0x0F), Color5250::White);
    assert_eq!(color_from_5250_attribute(0xF4), Color5250::Red);
}

// -- Full round-trip: parse bytes then apply to screen ------------------

#[test]
fn test_parse_and_apply_roundtrip() {
    let payload = [
        0x10, 0x01, 0x01, // SBA row=1, col=1 (wire: 1-based)
        0xD6, // 'O'
        0xD2, // 'K'
        0x29, // IC
    ];
    let total = 5 + payload.len();
    let mut raw = Vec::with_capacity(total);
    raw.push((total >> 8) as u8);
    raw.push((total & 0xFF) as u8);
    raw.push(0x04); // record type
    raw.push(0x00); // reserved
    raw.push(0x01); // opcode: WTD
    raw.extend_from_slice(&payload);

    let record = parse_5250_record(&raw).unwrap();
    let mut screen = ScreenBuffer5250::new(24, 80);
    screen.apply_record(&record);

    assert_eq!(screen.get_cell(0, 0).unwrap().character, 'O');
    assert_eq!(screen.get_cell(0, 1).unwrap().character, 'K');
    assert_eq!(screen.cursor_pos(), (0, 2));
}

// -- SOH order ----------------------------------------------------------

#[test]
fn test_soh_does_not_crash() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![DataStreamItem5250::Order(Order::Soh(SohData {
            length: 3,
            data: vec![0x01, 0x02, 0x03],
        }))],
    );
    screen.apply_record(&record);
    assert_eq!(screen.get_cell(0, 0).unwrap().character, ' ');
}

// -- Tab with no fields -------------------------------------------------

#[test]
fn test_tab_forward_no_fields() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    assert!(!screen.tab_forward());
}

#[test]
fn test_tab_backward_no_fields() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    assert!(!screen.tab_backward());
}

// -- Tab with all protected fields --------------------------------------

#[test]
fn test_tab_all_protected() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let fcw_protected = FieldControlWord::from_bytes(0x80, 0x00);

    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Sf(fcw_protected)),
        ],
    );
    screen.apply_record(&record);
    assert!(!screen.tab_forward());
}

// -- 27x132 screen ------------------------------------------------------

#[test]
fn test_27x132_screen() {
    let screen = ScreenBuffer5250::new(27, 132);
    assert_eq!(screen.rows(), 27);
    assert_eq!(screen.cols(), 132);
    assert!(screen.get_cell(26, 131).is_some());
    assert!(screen.get_cell(27, 0).is_none());
}

// == Renderer tests =====================================================
//
// These live here because they need direct access to ScreenBuffer5250::buffer,
// which is pub(crate).

#[test]
fn test_render_empty_screen_produces_jpeg() {
    let screen = ScreenBuffer5250::new(24, 80);
    let result = crate::renderer::render_to_jpeg(&screen, 9, 18, 85);
    assert!(result.is_ok());
    assert!(result.unwrap().len() > 100);
}

#[test]
fn test_render_standard_screen_sizes() {
    for (rows, cols) in [(24u16, 80u16), (27, 132)] {
        let screen = ScreenBuffer5250::new(rows, cols);
        let result = crate::renderer::render_to_jpeg(&screen, 9, 18, 85);
        assert!(result.is_ok(), "render failed for {}x{}", rows, cols);
    }
}

#[test]
fn test_screen_to_buffer_dimensions() {
    let screen = ScreenBuffer5250::new(24, 80);
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.area.width, 80);
    assert_eq!(buffer.area.height, 24);
    assert_eq!(buffer.content.len(), 24 * 80);
}

#[test]
fn test_screen_to_buffer_character_appears() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    screen.buffer[0].character = 'H';
    screen.buffer[1].character = 'i';
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[0].symbol(), "H");
    assert_eq!(buffer.content[1].symbol(), "i");
}

#[test]
fn test_screen_to_buffer_field_start_stays_blank() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    screen.buffer[5].field_start = true;
    screen.buffer[5].character = 'X';
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[5].symbol(), " ");
}

#[test]
fn test_screen_to_buffer_space_char_stays_blank() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    screen.buffer[3].character = ' ';
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[3].symbol(), " ");
}

#[test]
fn test_screen_to_buffer_color_mapping() {
    use ratatui::style::Color;
    let cases = [
        (Color5250::Black, Color::Black),
        (Color5250::Green, Color::Green),
        (Color5250::White, Color::White),
        (Color5250::Red, Color::Red),
        (Color5250::Blue, Color::Blue),
        (Color5250::Turquoise, Color::Cyan),
        (Color5250::Yellow, Color::Yellow),
        (Color5250::Pink, Color::Magenta),
    ];
    for (fg, expected) in cases {
        let mut screen = ScreenBuffer5250::new(3, 10);
        screen.buffer[0].character = 'X';
        screen.buffer[0].foreground = fg;
        let buffer = crate::renderer::screen_to_buffer(&screen);
        assert_eq!(buffer.content[0].fg, expected, "Color5250::{:?}", fg);
    }
}

#[test]
fn test_screen_to_buffer_underline_maps_to_modifier() {
    use ratatui::style::Modifier;
    let mut screen = ScreenBuffer5250::new(3, 10);
    screen.buffer[0].character = 'X';
    screen.buffer[0].underline = true;
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert!(buffer.content[0].modifier.contains(Modifier::UNDERLINED));
}

#[test]
fn test_screen_to_buffer_no_underline_has_no_modifier() {
    use ratatui::style::Modifier;
    let mut screen = ScreenBuffer5250::new(3, 10);
    screen.buffer[0].character = 'X';
    screen.buffer[0].underline = false;
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert!(!buffer.content[0].modifier.contains(Modifier::UNDERLINED));
}

#[test]
fn test_screen_to_buffer_multirow_layout() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    screen.buffer[80].character = 'A'; // row 1, col 0
    screen.buffer[161].character = 'B'; // row 2, col 1
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[80].symbol(), "A");
    assert_eq!(buffer.content[161].symbol(), "B");
}

/// RA with a target behind the current position (out-of-bounds or same position)
/// must terminate within one full screen traversal, not loop forever.
/// Before the fix, RA/EA loops had no iteration limit and would hang if the
/// target was unreachable from the current write position.
#[test]
fn test_ra_order_terminates_when_target_behind_start() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    // Set write position to (0,0) and target to the same position.
    // The loop must stop after one full screen wrap at most.
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            // RA targeting (0,0) from (0,0): target == start, should fill 0 or 1 cell and stop
            DataStreamItem5250::Order(Order::Ra(0, 0, 0x40)), // 0x40 = EBCDIC space
        ],
    );
    // Must complete without hanging (no timeout mechanism needed if the fix is correct)
    screen.apply_record(&record);
}

#[test]
fn test_ea_order_terminates_when_target_behind_start() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(5, 10)),
            DataStreamItem5250::Order(Order::Ea(0, 0)), // target row 0 < current row 5
        ],
    );
    screen.apply_record(&record);
}

/// RA/EA with an out-of-bounds target must terminate in at most rows*cols steps.
/// Before the loop-count fix, target_row/col > screen bounds made the equality
/// check fire never, causing an infinite loop.
#[test]
fn test_ra_order_terminates_on_out_of_bounds_target() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Ra(255, 255, 0x40)),
        ],
    );
    screen.apply_record(&record);
}

#[test]
fn test_ea_order_terminates_on_out_of_bounds_target() {
    let mut screen = ScreenBuffer5250::new(24, 80);
    let record = make_record(
        OpCode::WriteToDisplay,
        vec![
            DataStreamItem5250::Order(Order::Sba(0, 0)),
            DataStreamItem5250::Order(Order::Ea(200, 200)),
        ],
    );
    screen.apply_record(&record);
}
