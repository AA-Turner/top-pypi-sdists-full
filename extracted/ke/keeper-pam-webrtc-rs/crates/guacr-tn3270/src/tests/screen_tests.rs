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
    assert_eq!(screen.cursor_pos(), 5);
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
    assert_eq!(screen.cursor_pos(), 161);
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
    assert_eq!(screen.cursor_pos(), 20);
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

    screen.cursor_position = 15;
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

    screen.cursor_position = 1;
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

    screen.cursor_position = 1;
    assert!(!screen.input_char('A'));
    assert_eq!(screen.buffer[1].character, ' ');
}

// -- Cursor position tests --

#[test]
fn test_cursor_row_col() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.cursor_position = 163; // row 2, col 3
    assert_eq!(screen.cursor_row_col(), (2, 3));
}

#[test]
fn test_cursor_wraps_at_end() {
    let mut screen = ScreenBuffer::new(24, 80);
    screen.cursor_position = 1919; // last position
    screen.advance();
    assert_eq!(screen.cursor_pos(), 0); // wrapped to beginning
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
