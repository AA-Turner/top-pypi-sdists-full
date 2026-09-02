// Security tests for TN5250 handler.
// Run with: cargo test -p guacr-tn5250 --test security_test -- --include-ignored
#[cfg(test)]
mod security_tests {
    #[tokio::test]
    #[ignore]
    async fn test_tn5250_invalid_credentials_rejected() {
        // Requires a running TN5250 server that enforces authentication
        // pub400.com:23 is a public AS/400 for manual testing
        println!("Invalid credential rejection — implement with actual TN5250 session");
        println!("Verify that invalid user/password results in CPF1107 message");
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_credential_not_logged() {
        // Verify that credentials typed into TN5250 password fields are not
        // logged in plaintext by the guacr handler
        println!("Credential logging test — implement with log capture");
        println!("Verify bypass (protected) fields with no-display attribute are not logged");
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_malformed_record_handled() {
        // Verify that malformed 5250 records do not cause panics or information disclosure
        use guacr_tn5250::datastream::{parse_5250_record, Tn5250Error};

        let malformed: &[&[u8]] = &[
            &[],
            &[0x00],
            &[0x00, 0x03, 0x04],             // Too short (RecordTooShort)
            &[0x00, 0xFF, 0x04, 0x00, 0x01], // Length mismatch
            &[0x00, 0x07, 0x04, 0x00, 0x01, 0x10, 0x01], // Truncated SBA
            &[0x00, 0x07, 0x04, 0x00, 0x01, 0x20, 0x00], // Truncated SF
        ];

        for input in malformed {
            let result = parse_5250_record(input);
            assert!(
                result.is_err(),
                "Expected error for malformed input {:02X?}, got Ok",
                input
            );
            // Verify it's a known error variant, not a panic
            match result.unwrap_err() {
                Tn5250Error::RecordTooShort(_)
                | Tn5250Error::RecordLengthMismatch { .. }
                | Tn5250Error::TruncatedOrder { .. }
                | Tn5250Error::UnknownOpCode(_)
                | Tn5250Error::InvalidAddress { .. }
                | Tn5250Error::UnexpectedEnd(_) => {}
            }
        }

        println!("All malformed inputs returned structured errors without panic");
    }

    #[tokio::test]
    #[ignore]
    async fn test_tn5250_protected_field_input_blocked() {
        // Verify that bypass (protected) fields reject character input
        use guacr_tn5250::datastream::{
            DataStreamItem5250, FieldControlWord, OpCode, Order, Record5250,
        };
        use guacr_tn5250::screen::ScreenBuffer5250;

        // bypass=true → protected field
        let fcw = FieldControlWord::from_bytes(0x80, 0x00);

        let record = Record5250 {
            record_type: 0x04,
            opcode: OpCode::WriteToDisplay,
            orders: vec![
                DataStreamItem5250::Order(Order::Sba(0, 0)),
                DataStreamItem5250::Order(Order::Sf(fcw)),
                // Cursor at data position
                DataStreamItem5250::Order(Order::Sba(0, 1)),
                DataStreamItem5250::Order(Order::Ic),
            ],
        };

        let mut screen = ScreenBuffer5250::new(24, 80);
        screen.apply_record(&record);

        let accepted = screen.type_character('X');
        assert!(
            !accepted,
            "Input into bypass (protected) field must be rejected"
        );
        assert_eq!(
            screen.get_cell(0, 1).unwrap().character,
            ' ',
            "Protected field character must remain blank"
        );

        println!("Bypass field input correctly rejected");
    }
}
