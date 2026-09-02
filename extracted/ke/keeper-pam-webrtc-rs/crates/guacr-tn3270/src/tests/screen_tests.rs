use crate::datastream::{
    encode_buffer_address, parse_data_stream, Aid, Color3270, DataStream, DataStreamItem,
    ExtendedAttribute, FieldAttribute, Intensity, Order, Wcc, WriteCommand,
};
use crate::ebcdic::CodePage;
use crate::screen::{Highlight3270, ScreenBuffer};

fn make_stream(command: WriteCommand, wcc: Wcc, orders: Vec<DataStreamItem>) -> DataStream {
    DataStream {
        command,
        wcc,
        orders,
    }
}

fn default_wcc() -> Wcc {
    Wcc {
        reset_mdt: false,
        restore_keyboard: false,
        alarm: false,
    }
}

fn reset_wcc() -> Wcc {
    Wcc {
        reset_mdt: true,
        restore_keyboard: true,
        alarm: false,
    }
}

// -- Basic construction tests --

#[test]
fn test_new_screen_buffer() {
    let screen = ScreenBuffer::new(24, 80);
    assert_eq!(screen.rows(), 24);
    assert_eq!(screen.cols(), 80);
    assert_eq!(screen.size(), 1920);
    assert_eq!(screen.cursor_pos(), 0);
}

#[test]
fn test_initial_cells_are_spaces() {
    let screen = ScreenBuffer::new(24, 80);
    for row in 0..24 {
        for col in 0..80 {
            let cell = screen.get_cell(row, col).unwrap();
            assert_eq!(cell.character, ' ');
            assert_eq!(cell.attribute.field_attribute, None);
        }
    }
}

#[test]
fn test_get_cell_out_of_range() {
    let screen = ScreenBuffer::new(24, 80);
    assert!(screen.get_cell(24, 0).is_none());
    assert!(screen.get_cell(0, 80).is_none());
}

#[test]
fn test_clear() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.buffer[0].character = 'X';
    screen.cursor_position = 100;
    screen.clear();
    assert_eq!(screen.buffer[0].character, ' ');
    assert_eq!(screen.cursor_pos(), 0);
}

// -- Erase/Write tests --

#[test]
fn test_erase_write_clears_screen() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.buffer[0].character = 'X';
    screen.buffer[100].character = 'Y';

    let stream = make_stream(WriteCommand::EraseWrite, reset_wcc(), vec![]);
    screen.apply_data_stream(&stream);

    assert_eq!(screen.buffer[0].character, ' ');
    assert_eq!(screen.buffer[100].character, ' ');
}

#[test]
fn test_write_preserves_existing_content() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.buffer[50].character = 'X';

    let stream = make_stream(WriteCommand::Write, default_wcc(), vec![]);
    screen.apply_data_stream(&stream);

    assert_eq!(screen.buffer[50].character, 'X');
}

// -- Character data tests --

#[test]
fn test_write_characters() {
    let mut screen = ScreenBuffer::new(24, 80);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Character(0xC8), // H
            DataStreamItem::Character(0xC5), // E
            DataStreamItem::Character(0xD3), // L
            DataStreamItem::Character(0xD3), // L
            DataStreamItem::Character(0xD6), // O
        ],
    );
    screen.apply_data_stream(&stream);

    assert_eq!(screen.buffer[0].character, 'H');
    assert_eq!(screen.buffer[1].character, 'E');
    assert_eq!(screen.buffer[2].character, 'L');
    assert_eq!(screen.buffer[3].character, 'L');
    assert_eq!(screen.buffer[4].character, 'O');
    assert_eq!(screen.write_pos(), 5); // write address advanced past last char
}

// -- SBA order tests --

#[test]
fn test_sba_positions_cursor() {
    let mut screen = ScreenBuffer::new(24, 80);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(160)),
            DataStreamItem::Character(0xC8), // H
        ],
    );
    screen.apply_data_stream(&stream);

    assert_eq!(screen.buffer[160].character, 'H');
    assert_eq!(screen.write_pos(), 161); // write address advanced past SBA(160)+char
}

// -- SF order tests --

#[test]
fn test_sf_creates_field() {
    let mut screen = ScreenBuffer::new(24, 80);

    let fa = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(10)),
            DataStreamItem::Order(Order::Sf(fa)),
            DataStreamItem::Character(0xD3), // L
            DataStreamItem::Character(0xD6), // O
            DataStreamItem::Character(0xC7), // G
            DataStreamItem::Character(0xD6), // O
            DataStreamItem::Character(0xD5), // N
        ],
    );
    screen.apply_data_stream(&stream);

    assert!(screen.buffer[10].attribute.field_attribute.is_some());
    assert!(
        screen.buffer[10]
            .attribute
            .field_attribute
            .unwrap()
            .protected
    );

    assert_eq!(screen.buffer[11].character, 'L');
    assert_eq!(screen.buffer[15].character, 'N');
}

// -- Field discovery tests --

#[test]
fn test_get_fields_single_field() {
    let mut screen = ScreenBuffer::new(24, 80);

    let fa = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![DataStreamItem::Order(Order::Sf(fa))],
    );
    screen.apply_data_stream(&stream);

    let fields = screen.get_fields();
    assert_eq!(fields.len(), 1);
    assert_eq!(fields[0].start, 0);
    assert!(!fields[0].attribute.protected);
}

#[test]
fn test_get_fields_two_fields() {
    let mut screen = ScreenBuffer::new(24, 80);

    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(prot)),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
            DataStreamItem::Character(0xC7),
            DataStreamItem::Character(0xD6),
            DataStreamItem::Character(0xD5),
            DataStreamItem::Order(Order::Sf(unprot)),
        ],
    );
    screen.apply_data_stream(&stream);

    let fields = screen.get_fields();
    assert_eq!(fields.len(), 2);
    assert!(fields[0].attribute.protected);
    assert!(!fields[1].attribute.protected);
}

// -- IC (Insert Cursor) test --

#[test]
fn test_ic_sets_cursor() {
    let mut screen = ScreenBuffer::new(24, 80);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(100)),
            DataStreamItem::Order(Order::Ic),
        ],
    );
    screen.apply_data_stream(&stream);

    assert_eq!(screen.cursor_pos(), 100);
}

// -- RA (Repeat to Address) test --

#[test]
fn test_ra_fills_range() {
    let mut screen = ScreenBuffer::new(24, 80);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(10)),
            DataStreamItem::Order(Order::Ra(20, 0x60)), // EBCDIC '-' = 0x60
        ],
    );
    screen.apply_data_stream(&stream);

    for i in 10..20 {
        assert_eq!(
            screen.buffer[i].character, '-',
            "Position {} should be '-'",
            i
        );
    }
    assert_eq!(screen.write_pos(), 20); // RA moved write address to target
}

// -- EUA (Erase Unprotected to Address) test --

#[test]
fn test_eua_clears_unprotected() {
    let mut screen = ScreenBuffer::new(24, 80);

    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(unprot)),
            DataStreamItem::Character(0xC8),
            DataStreamItem::Character(0xC5),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
        ],
    );
    screen.apply_data_stream(&stream);

    let eua_stream = make_stream(
        WriteCommand::Write,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(1)),
            DataStreamItem::Order(Order::Eua(6)),
        ],
    );
    screen.apply_data_stream(&eua_stream);

    for i in 1..6 {
        assert_eq!(
            screen.buffer[i].character, ' ',
            "Position {} should be cleared",
            i
        );
    }
}

// -- Tab navigation tests --

#[test]
fn test_tab_forward() {
    let mut screen = ScreenBuffer::new(24, 80);

    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(prot)),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
            DataStreamItem::Character(0xC7),
            DataStreamItem::Character(0xD6),
            DataStreamItem::Character(0xD5),
            DataStreamItem::Order(Order::Sf(unprot)),
        ],
    );
    screen.apply_data_stream(&stream);

    screen.cursor_position = 0;
    screen.tab_forward();

    assert_eq!(screen.cursor_pos(), 7);
}

#[test]
fn test_tab_backward() {
    let mut screen = ScreenBuffer::new(24, 80);

    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(unprot)),
            DataStreamItem::Character(0x40),
            DataStreamItem::Character(0x40),
            DataStreamItem::Character(0x40),
            DataStreamItem::Character(0x40),
            DataStreamItem::Character(0x40),
            DataStreamItem::Order(Order::Sf(prot)),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
            DataStreamItem::Order(Order::Sf(unprot)),
        ],
    );
    screen.apply_data_stream(&stream);

    screen.display_cursor = 15; // place interactive cursor mid-screen for test
    screen.tab_backward();

    assert_eq!(screen.cursor_pos(), 10);
}

// -- WCC reset MDT test --

#[test]
fn test_wcc_reset_mdt() {
    let mut screen = ScreenBuffer::new(24, 80);

    let modified_fa = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: true,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![DataStreamItem::Order(Order::Sf(modified_fa))],
    );
    screen.apply_data_stream(&stream);

    assert!(screen.buffer[0].attribute.field_attribute.unwrap().modified);

    let reset_stream = make_stream(
        WriteCommand::Write,
        Wcc {
            reset_mdt: true,
            restore_keyboard: false,
            alarm: false,
        },
        vec![],
    );
    screen.apply_data_stream(&reset_stream);

    assert!(!screen.buffer[0].attribute.field_attribute.unwrap().modified);
}

// -- Read Modified test --

#[test]
fn test_read_modified_fields_enter() {
    let mut screen = ScreenBuffer::new(24, 80);

    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    let modified_unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: true,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(prot)),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
            DataStreamItem::Character(0xC7),
            DataStreamItem::Order(Order::Sf(modified_unprot)),
            DataStreamItem::Character(0xE4),
            DataStreamItem::Character(0xE2),
            DataStreamItem::Character(0xC5),
            DataStreamItem::Character(0xD9),
        ],
    );
    screen.apply_data_stream(&stream);

    screen.cursor_position = 5;
    let response = screen.read_modified_fields(Aid::Enter);

    assert!(!response.is_empty());
    assert_eq!(response[0], Aid::ENTER);
    assert!(response.len() > 3);
}

#[test]
fn test_read_modified_pa_key_short_response() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.cursor_position = 0;

    let response = screen.read_modified_fields(Aid::Pa(1));
    assert_eq!(response.len(), 3);
    assert_eq!(response[0], Aid::PA1);
}

// -- Row text extraction tests --

#[test]
fn test_get_row_text() {
    let mut screen = ScreenBuffer::new(24, 80);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Character(0xC8),
            DataStreamItem::Character(0xC5),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
        ],
    );
    screen.apply_data_stream(&stream);

    let text = screen.get_row_text(0);
    assert!(text.starts_with("HELLO"));
    assert_eq!(text.len(), 80);
}

#[test]
fn test_get_row_text_field_attr_as_space() {
    let mut screen = ScreenBuffer::new(24, 80);

    let fa = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(fa)),
            DataStreamItem::Character(0xC8),
            DataStreamItem::Character(0xC9),
        ],
    );
    screen.apply_data_stream(&stream);

    let text = screen.get_row_text(0);
    assert_eq!(&text[0..3], " HI");
}

// -- Input test --

#[test]
fn test_input_char_unprotected() {
    let mut screen = ScreenBuffer::new(24, 80);

    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(unprot)),
        ],
    );
    screen.apply_data_stream(&stream);

    screen.display_cursor = 1; // position interactive cursor in the field's data area
    assert!(screen.input_char('A'));
    assert_eq!(screen.buffer[1].character, 'A');
    assert_eq!(screen.cursor_pos(), 2);

    assert!(screen.buffer[0].attribute.field_attribute.unwrap().modified);
}

#[test]
fn test_input_char_protected_rejected() {
    let mut screen = ScreenBuffer::new(24, 80);

    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(prot)),
        ],
    );
    screen.apply_data_stream(&stream);

    screen.display_cursor = 1;
    assert!(!screen.input_char('A'));
    assert_eq!(screen.buffer[1].character, ' ');
}

// -- Cursor position tests --

#[test]
fn test_cursor_row_col() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.display_cursor = 163; // row 2, col 3
    assert_eq!(screen.cursor_row_col(), (2, 3));
}

#[test]
fn test_cursor_wraps_at_end() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.cursor_position = 1919; // last write address
    screen.advance();
    assert_eq!(screen.write_pos(), 0); // write address wrapped to beginning
}

// -- Full data stream parse + apply integration test --

#[test]
fn test_parse_and_apply_login_screen() {
    let (sba0_b1, sba0_b2) = encode_buffer_address(0);
    let (sba80_b1, sba80_b2) = encode_buffer_address(80);

    let raw_data = [
        0x05, // Erase/Write
        0x60, // WCC: reset_mdt + restore_keyboard
        0x11, sba0_b1, sba0_b2, // SBA(0)
        0x1D, 0x20, // SF(protected)
        0xD3, 0xD6, 0xC7, 0xD6, 0xD5, // "LOGON"
        0x11, sba80_b1, sba80_b2, // SBA(80)
        0x1D, 0x00, // SF(unprotected)
        0x13, // IC
    ];

    let ds = parse_data_stream(&raw_data).unwrap();
    let mut screen = ScreenBuffer::new(24, 80);
    screen.apply_data_stream(&ds);

    let row0 = screen.get_row_text(0);
    assert!(row0.starts_with(" LOGON"), "Row 0: '{}'", &row0[..10]);

    assert!(screen.buffer[0].attribute.field_attribute.is_some());
    assert!(
        screen.buffer[0]
            .attribute
            .field_attribute
            .unwrap()
            .protected
    );

    assert!(screen.buffer[80].attribute.field_attribute.is_some());
    assert!(
        !screen.buffer[80]
            .attribute
            .field_attribute
            .unwrap()
            .protected
    );

    assert_eq!(screen.cursor_pos(), 81);
}

// -- Alternate screen size test --

#[test]
fn test_alternate_screen_size() {
    let screen = ScreenBuffer::new(43, 80);
    assert_eq!(screen.size(), 3440);

    let screen132 = ScreenBuffer::new(27, 132);
    assert_eq!(screen132.size(), 3564);
}

// -- SFE order test on screen --

#[test]
fn test_sfe_with_color() {
    let mut screen = ScreenBuffer::new(24, 80);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sfe(vec![
                ExtendedAttribute::FieldAttribute(FieldAttribute {
                    protected: true,
                    numeric: false,
                    intensity: Intensity::Normal,
                    modified: false,
                }),
                ExtendedAttribute::ForegroundColor(Color3270::Red),
            ])),
            DataStreamItem::Character(0xC8),
            DataStreamItem::Character(0xC9),
        ],
    );
    screen.apply_data_stream(&stream);

    assert!(screen.buffer[0].attribute.field_attribute.is_some());
    assert_eq!(screen.buffer[0].attribute.foreground, Color3270::Red);
}

// -- SA (Set Attribute) test on screen --

#[test]
fn test_sa_changes_subsequent_characters() {
    let mut screen = ScreenBuffer::new(24, 80);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Character(0xC8), // H - default color
            DataStreamItem::Order(Order::Sa(ExtendedAttribute::ForegroundColor(
                Color3270::Green,
            ))),
            DataStreamItem::Character(0xC9), // I - green
            DataStreamItem::Character(0x5A), // ! - green
        ],
    );
    screen.apply_data_stream(&stream);

    assert_eq!(screen.buffer[0].attribute.foreground, Color3270::Default);
    assert_eq!(screen.buffer[1].attribute.foreground, Color3270::Green);
    assert_eq!(screen.buffer[2].attribute.foreground, Color3270::Green);
}

// -- get_field_at test --

#[test]
fn test_get_field_at() {
    let mut screen = ScreenBuffer::new(24, 80);

    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(prot)),
            DataStreamItem::Character(0xC8),
            DataStreamItem::Character(0xC5),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
            DataStreamItem::Order(Order::Sf(unprot)),
        ],
    );
    screen.apply_data_stream(&stream);

    let field_at_0 = screen.get_field_at(0).unwrap();
    assert!(field_at_0.attribute.protected);

    let field_at_6 = screen.get_field_at(6).unwrap();
    assert!(!field_at_6.attribute.protected);
}

// -- Code page test --

#[test]
fn test_with_code_page_cp500() {
    let mut screen = ScreenBuffer::with_code_page(24, 80, CodePage::Cp500);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Character(0xC8),
            DataStreamItem::Character(0xC9),
        ],
    );
    screen.apply_data_stream(&stream);

    assert_eq!(screen.buffer[0].character, 'H');
    assert_eq!(screen.buffer[1].character, 'I');
}

// -- Screen text extraction test --

#[test]
fn test_get_screen_text() {
    let mut screen = ScreenBuffer::new(3, 10);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Character(0xC8),
            DataStreamItem::Character(0xC5),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD3),
            DataStreamItem::Character(0xD6),
        ],
    );
    screen.apply_data_stream(&stream);

    let text = screen.get_screen_text();
    let lines: Vec<&str> = text.lines().collect();
    assert_eq!(lines.len(), 3);
    assert!(lines[0].starts_with("HELLO"));
}

// == Renderer tests =====================================================
//
// These live here because they need direct access to ScreenBuffer::buffer,
// which is pub(crate).

#[test]
fn test_render_empty_screen_produces_jpeg() {
    let screen = ScreenBuffer::new(24, 80);
    let result = crate::renderer::render_to_jpeg(&screen, 9, 18, 85);
    assert!(result.is_ok());
    assert!(result.unwrap().len() > 100);
}

#[test]
fn test_render_standard_screen_sizes() {
    for (rows, cols) in [(24u16, 80u16), (32, 80), (43, 80), (27, 132)] {
        let screen = ScreenBuffer::new(rows, cols);
        let result = crate::renderer::render_to_jpeg(&screen, 9, 18, 85);
        assert!(result.is_ok(), "render failed for {}x{}", rows, cols);
    }
}

#[test]
fn test_screen_to_buffer_dimensions() {
    let screen = ScreenBuffer::new(24, 80);
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.area.width, 80);
    assert_eq!(buffer.area.height, 24);
    assert_eq!(buffer.content.len(), 24 * 80);
}

#[test]
fn test_screen_to_buffer_character_appears() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.buffer[0].character = 'H';
    screen.buffer[1].character = 'i';
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[0].symbol(), "H");
    assert_eq!(buffer.content[1].symbol(), "i");
}

#[test]
fn test_screen_to_buffer_null_char_stays_blank() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.buffer[5].character = '\0';
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[5].symbol(), " ");
}

#[test]
fn test_screen_to_buffer_field_attribute_stays_blank() {
    let mut screen = ScreenBuffer::new(24, 80);
    let fa = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    screen.buffer[10].attribute.field_attribute = Some(fa);
    screen.buffer[10].character = 'X';
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[10].symbol(), " ");
}

#[test]
fn test_screen_to_buffer_color_mapping() {
    use ratatui::style::Color;
    let cases = [
        (Color3270::Default, Color::Green),
        (Color3270::Blue, Color::Blue),
        (Color3270::Red, Color::Red),
        (Color3270::Pink, Color::Magenta),
        (Color3270::Green, Color::Green),
        (Color3270::Turquoise, Color::Cyan),
        (Color3270::Yellow, Color::Yellow),
        (Color3270::White, Color::White),
    ];
    for (fg, expected) in cases {
        let mut screen = ScreenBuffer::new(3, 10);
        screen.buffer[0].character = 'X';
        screen.buffer[0].attribute.foreground = fg;
        let buffer = crate::renderer::screen_to_buffer(&screen);
        assert_eq!(buffer.content[0].fg, expected, "Color3270::{:?}", fg);
    }
}

#[test]
fn test_screen_to_buffer_highlight_mapping() {
    use ratatui::style::Modifier;
    let cases = [
        (Highlight3270::Normal, Modifier::empty()),
        (Highlight3270::Blink, Modifier::SLOW_BLINK),
        (Highlight3270::ReverseVideo, Modifier::REVERSED),
        (Highlight3270::Underscore, Modifier::UNDERLINED),
        (Highlight3270::Intensified, Modifier::BOLD),
    ];
    for (hl, expected) in cases {
        let mut screen = ScreenBuffer::new(3, 10);
        screen.buffer[0].character = 'X';
        screen.buffer[0].attribute.highlight = hl;
        let buffer = crate::renderer::screen_to_buffer(&screen);
        assert!(
            buffer.content[0].modifier.contains(expected),
            "Highlight3270::{:?} should produce modifier {:?}",
            hl,
            expected,
        );
    }
}

#[test]
fn test_screen_to_buffer_multirow_layout() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.buffer[80].character = 'A'; // row 1, col 0
    screen.buffer[161].character = 'B'; // row 2, col 1
    let buffer = crate::renderer::screen_to_buffer(&screen);
    assert_eq!(buffer.content[80].symbol(), "A");
    assert_eq!(buffer.content[161].symbol(), "B");
}

// -- MDT tracking tests --

/// set_field_modified() directly marks the field attribute at the given position.
/// After calling it, get_fields() must report that field as modified.
#[test]
fn test_set_field_modified_direct() {
    let mut screen = ScreenBuffer::new(24, 80);

    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![DataStreamItem::Order(Order::Sf(unprot))],
    );
    screen.apply_data_stream(&stream);

    // Field attribute is at position 0; initially not modified.
    assert!(!screen.buffer[0].attribute.field_attribute.unwrap().modified);

    // Call set_field_modified directly.
    screen.set_field_modified(0);
    assert!(
        screen.buffer[0].attribute.field_attribute.unwrap().modified,
        "set_field_modified must mark the field attribute as modified"
    );

    // The field returned by get_fields() must also report modified.
    let fields = screen.get_fields();
    assert_eq!(fields.len(), 1);
    assert!(fields[0].modified, "get_fields() must report modified=true");
}

/// input_char() on an unprotected field must set the MDT flag on the governing field attribute.
#[test]
fn test_mdt_set_after_input_char() {
    let mut screen = ScreenBuffer::new(24, 80);

    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![DataStreamItem::Order(Order::Sf(unprot))],
    );
    screen.apply_data_stream(&stream);

    // Cursor at position 1 (data area of field starting at 0).
    screen.display_cursor = 1;
    screen.input_char('Z');

    assert!(
        screen.buffer[0].attribute.field_attribute.unwrap().modified,
        "input_char must set MDT on the governing field attribute"
    );
}

/// read_modified_fields() must exclude fields that have not been modified.
/// Only fields with modified=true should appear in the response.
#[test]
fn test_read_modified_excludes_unmodified_fields() {
    let mut screen = ScreenBuffer::new(24, 80);

    let unprot_unmodified = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    let unprot_modified = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: true,
    };

    // Layout: field at 0 (unmodified), field at 40 (modified with 'A').
    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(unprot_unmodified)),
            DataStreamItem::Order(Order::Sba(40)),
            DataStreamItem::Order(Order::Sf(unprot_modified)),
            DataStreamItem::Character(0xC1), // 'A' in EBCDIC
            DataStreamItem::Character(0xC2), // 'B'
        ],
    );
    screen.apply_data_stream(&stream);

    let response = screen.read_modified_fields(Aid::Enter);
    // Response: AID(1) + cursor(2) + SBA(3) + data(>=1) = at least 7 bytes.
    // The unmodified field at 0 must NOT appear (no SBA at position 1).
    // The modified field at 40 must appear (SBA at position 41, then data).
    assert!(
        response.len() >= 7,
        "response must include modified field data"
    );

    // AID byte must be Enter.
    assert_eq!(response[0], Aid::ENTER);

    // Verify no SBA pointing at position 1 (the unmodified field's data start).
    let (sba1_b1, sba1_b2) = encode_buffer_address(1);
    let has_unmodified_sba = response.windows(3).any(|w| w == [0x11, sba1_b1, sba1_b2]);
    assert!(
        !has_unmodified_sba,
        "unmodified field must not appear in read_modified_fields output"
    );
}

/// read_modified_fields() for Enter must include the EBCDIC field data that the
/// user typed. After input_char() sets characters in the buffer, they must be
/// reflected in the response sent to the host.
#[test]
fn test_read_modified_field_data_after_input() {
    let mut screen = ScreenBuffer::new(24, 80);

    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(unprot)),
        ],
    );
    screen.apply_data_stream(&stream);

    // Type "HI" into the unprotected field.
    screen.display_cursor = 1;
    screen.input_char('H');
    screen.input_char('I');

    let response = screen.read_modified_fields(Aid::Enter);
    // Response must have: AID(1) + cursor(2) + SBA(3) + 'H' + 'I' + spaces_to_end
    // At minimum it contains data bytes; the field starts at pos 1 and is 79 chars wide.
    assert!(
        response.len() > 3,
        "response must include field data bytes, got {} bytes",
        response.len()
    );
    assert_eq!(response[0], Aid::ENTER, "first byte must be AID::ENTER");

    // Find the SBA pointing to position 1 (data start after field attr at 0).
    let (sba_b1, sba_b2) = encode_buffer_address(1);
    let sba_pos = response
        .windows(3)
        .position(|w| w == [0x11, sba_b1, sba_b2]);
    assert!(
        sba_pos.is_some(),
        "response must contain SBA(1) for the field"
    );

    // Data follows immediately after the SBA(1).
    let data_start = sba_pos.unwrap() + 3;
    assert!(
        response.len() > data_start,
        "data must follow SBA in response"
    );

    // The first data bytes must be EBCDIC 'H' and 'I'.
    use crate::ebcdic::{unicode_to_ebcdic, CodePage};
    let h_ebcdic = unicode_to_ebcdic('H', CodePage::Cp037).unwrap();
    let i_ebcdic = unicode_to_ebcdic('I', CodePage::Cp037).unwrap();
    assert_eq!(
        response[data_start], h_ebcdic,
        "first data byte must be EBCDIC 'H' (0x{:02X}), got 0x{:02X}",
        h_ebcdic, response[data_start]
    );
    assert_eq!(
        response[data_start + 1],
        i_ebcdic,
        "second data byte must be EBCDIC 'I' (0x{:02X}), got 0x{:02X}",
        i_ebcdic,
        response[data_start + 1]
    );
}

/// PA key read_modified_fields must return only AID + cursor (3 bytes, short form).
/// The 3-byte form must hold for PA1, PA2, and PA3 and must not include field data
/// even when modified fields exist on the screen.
#[test]
fn test_read_modified_pa_all_three() {
    let mut screen = ScreenBuffer::new(24, 80);

    // Place a modified field with some content.
    let unprot_mod = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: true,
    };
    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sf(unprot_mod)),
            DataStreamItem::Character(0xC8), // 'H'
        ],
    );
    screen.apply_data_stream(&stream);

    for (aid, expected_byte) in [
        (Aid::Pa(1), Aid::PA1),
        (Aid::Pa(2), Aid::PA2),
        (Aid::Pa(3), Aid::PA3),
    ] {
        let response = screen.read_modified_fields(aid);
        assert_eq!(
            response.len(),
            3,
            "PA{} must produce exactly 3 bytes (AID + cursor), got {}",
            match aid {
                Aid::Pa(n) => n,
                _ => 0,
            },
            response.len()
        );
        assert_eq!(
            response[0], expected_byte,
            "PA byte mismatch: expected 0x{:02X}, got 0x{:02X}",
            expected_byte, response[0]
        );
    }
}

/// Clear key read_modified_fields must also return only 3 bytes (short form).
#[test]
fn test_read_modified_clear_short_response() {
    let screen = ScreenBuffer::new(24, 80);
    let response = screen.read_modified_fields(Aid::Clear);
    assert_eq!(response.len(), 3, "Clear must produce exactly 3 bytes");
    assert_eq!(response[0], Aid::CLEAR);
}

// -- delete_at_cursor tests --

/// delete_at_cursor() on an unprotected field must clear the character and return true.
#[test]
fn test_delete_at_cursor_unprotected() {
    let mut screen = ScreenBuffer::new(24, 80);

    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sf(unprot)),
            DataStreamItem::Character(0xC8), // 'H' at pos 1
        ],
    );
    screen.apply_data_stream(&stream);

    screen.display_cursor = 1;
    assert_eq!(screen.buffer[1].character, 'H');
    let result = screen.delete_at_cursor();
    assert!(
        result,
        "delete_at_cursor must return true for unprotected cell"
    );
    assert_eq!(
        screen.buffer[1].character, ' ',
        "cell must be cleared to space"
    );
}

/// delete_at_cursor() on a protected field must return false and leave the cell unchanged.
#[test]
fn test_delete_at_cursor_protected() {
    let mut screen = ScreenBuffer::new(24, 80);

    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        default_wcc(),
        vec![
            DataStreamItem::Order(Order::Sf(prot)),
            DataStreamItem::Character(0xC8), // 'H' at pos 1 (protected)
        ],
    );
    screen.apply_data_stream(&stream);

    screen.display_cursor = 1;
    assert_eq!(screen.buffer[1].character, 'H');
    let result = screen.delete_at_cursor();
    assert!(
        !result,
        "delete_at_cursor must return false for protected cell"
    );
    assert_eq!(
        screen.buffer[1].character, 'H',
        "protected cell must remain unchanged"
    );
}

// -- Code page tests --

/// ScreenBuffer::with_code_page(CP1047) must decode the bracket bytes correctly.
/// CP1047 places '[' at 0xAD and ']' at 0xBD, differing from CP037.
#[test]
fn test_with_code_page_cp1047_brackets() {
    use crate::ebcdic::CodePage;

    let mut screen = ScreenBuffer::with_code_page(24, 80, CodePage::Cp1047);

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Character(0xAD), // '[' in CP1047
            DataStreamItem::Character(0xBD), // ']' in CP1047
        ],
    );
    screen.apply_data_stream(&stream);

    assert_eq!(
        screen.buffer[0].character, '[',
        "CP1047 byte 0xAD must decode as '['"
    );
    assert_eq!(
        screen.buffer[1].character, ']',
        "CP1047 byte 0xBD must decode as ']'"
    );
}

/// CP037 and CP500 differ for the bracket byte positions.
/// This test documents the cross-code-page character rendering difference.
#[test]
fn test_code_page_selection_affects_rendering() {
    use crate::ebcdic::CodePage;

    // In CP037, byte 0x4A is cent-sign (U+00A2).
    // In CP500, byte 0x4A is '['.
    let mut screen_037 = ScreenBuffer::with_code_page(24, 80, CodePage::Cp037);
    let stream_037 = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![DataStreamItem::Character(0x4A)],
    );
    screen_037.apply_data_stream(&stream_037);

    let mut screen_500 = ScreenBuffer::with_code_page(24, 80, CodePage::Cp500);
    let stream_500 = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![DataStreamItem::Character(0x4A)],
    );
    screen_500.apply_data_stream(&stream_500);

    assert_eq!(
        screen_037.buffer[0].character, '\u{00A2}',
        "CP037 0x4A = cent-sign"
    );
    assert_eq!(
        screen_500.buffer[0].character, '[',
        "CP500 0x4A = left bracket"
    );
    assert_ne!(
        screen_037.buffer[0].character, screen_500.buffer[0].character,
        "same byte must decode differently across code pages"
    );
}

// -- tab_backward wrap test --

/// tab_backward() must wrap around to the last unprotected field when the cursor
/// is at or before the first field on screen.
#[test]
fn test_tab_backward_wraps_around() {
    let mut screen = ScreenBuffer::new(24, 80);

    // Layout: prot field at 0, unprot field at 20, prot field at 40.
    let prot = FieldAttribute {
        protected: true,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };
    let unprot = FieldAttribute {
        protected: false,
        numeric: false,
        intensity: Intensity::Normal,
        modified: false,
    };

    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Order(Order::Sf(prot)),
            DataStreamItem::Order(Order::Sba(20)),
            DataStreamItem::Order(Order::Sf(unprot)),
            DataStreamItem::Order(Order::Sba(40)),
            DataStreamItem::Order(Order::Sf(prot)),
        ],
    );
    screen.apply_data_stream(&stream);

    // Place cursor early in the screen, before the unprotected field.
    // Tab backward must wrap around and land in the unprotected field.
    screen.display_cursor = 5; // inside the first prot field
    screen.tab_backward();

    // The unprotected field starts at 20; data area starts at 21.
    assert_eq!(
        screen.cursor_pos(),
        21,
        "tab_backward from before the unprotected field must wrap to its data area"
    );
}

// -- screen_to_buffer known-state test --

/// screen_to_buffer() must produce a ratatui Buffer whose cells exactly match
/// the Unicode characters written by apply_data_stream(). Verifies that the
/// renderer correctly maps screen cell characters to buffer symbols for a
/// multi-character, known screen state.
#[test]
fn test_screen_to_buffer_known_screen_state() {
    let mut screen = ScreenBuffer::new(3, 10);

    // Write "HELLO" at row 0 positions 0-4.
    let stream = make_stream(
        WriteCommand::EraseWrite,
        reset_wcc(),
        vec![
            DataStreamItem::Order(Order::Sba(0)),
            DataStreamItem::Character(0xC8), // H
            DataStreamItem::Character(0xC5), // E
            DataStreamItem::Character(0xD3), // L
            DataStreamItem::Character(0xD3), // L
            DataStreamItem::Character(0xD6), // O
        ],
    );
    screen.apply_data_stream(&stream);

    let buffer = crate::renderer::screen_to_buffer(&screen);

    // Row 0 must have "HELLO" followed by spaces.
    assert_eq!(buffer.content[0].symbol(), "H");
    assert_eq!(buffer.content[1].symbol(), "E");
    assert_eq!(buffer.content[2].symbol(), "L");
    assert_eq!(buffer.content[3].symbol(), "L");
    assert_eq!(buffer.content[4].symbol(), "O");
    // Position 5 should be blank (space).
    assert_eq!(buffer.content[5].symbol(), " ");

    // Rows 1 and 2 should be entirely blank.
    for idx in 10..30 {
        assert_eq!(
            buffer.content[idx].symbol(),
            " ",
            "row 1-2 cell {idx} must be blank"
        );
    }
}

/// ScreenBuffer::size() must not overflow for large dimensions.
///
/// 256 * 256 = 65536 which wraps to 0 as u16, causing a divide-by-zero panic
/// in any code that uses `% size()`. The constructor must cap rows/cols so
/// the product stays within u16::MAX (65535).
///
/// This test is the regression guard for the DoS: a crafted connection param
/// with rows=256 must not crash the gateway.
#[test]
fn test_screen_size_no_overflow() {
    // 255 * 255 = 65025 — fits in u16; must not panic.
    let s = ScreenBuffer::new(255, 255);
    let sz = s.size();
    assert!(sz > 0, "size() must be nonzero for 255x255");
    // The product must equal rows * cols without overflow.
    assert_eq!(sz as u32, 255u32 * 255, "size() must match rows*cols");

    // 256 * 256 = 65536 — overflows u16 to 0 before the fix.
    // After the fix, rows/cols must be capped so size() > 0.
    let s_capped = ScreenBuffer::new(256, 256);
    let sz_capped = s_capped.size();
    assert!(
        sz_capped > 0,
        "size() must be nonzero even when rows=256, cols=256 (got 0 — overflow not fixed)"
    );

    // Cursor arithmetic must not divide-by-zero after the size fix.
    let size = s_capped.size();
    let _ = 1u16 % size; // would panic before the fix if size were 0
}
