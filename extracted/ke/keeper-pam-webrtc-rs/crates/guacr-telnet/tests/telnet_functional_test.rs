//! Functional tests for Telnet handler — no external services required.
//!
//! These tests cover terminal emulation and handler construction using only
//! in-process state. They run in CI without any Docker containers.
//!
//! Run with:
//!   cargo test --package guacr-telnet --test telnet_functional_test

mod terminal_tests {
    use guacr_terminal::{
        mouse_event_to_x11_sequence, DirtyTracker, ModifierState, TerminalEmulator,
    };

    #[test]
    fn test_scrollback_buffer() {
        let mut terminal = TerminalEmulator::new_with_scrollback(24, 80, 150);
        let data = b"Hello, World!\n";
        terminal.process(data).unwrap();
        assert!(terminal.is_dirty());
    }

    #[test]
    fn test_mouse_event_x11_sequence() {
        let sequence = mouse_event_to_x11_sequence(10, 20, 1, 8, 16);
        // X11 mouse sequences start with ESC [
        assert!(sequence.starts_with(&[0x1b, b'[']));
    }

    #[test]
    fn test_modifier_state_tracking() {
        let mut state = ModifierState::default();

        assert!(!state.control);
        assert!(!state.shift);
        assert!(!state.alt);

        state.control = true;
        assert!(state.control);

        state.shift = true;
        assert!(state.shift);

        state.alt = true;
        assert!(state.alt);
    }

    #[test]
    fn test_dirty_tracker_basic() {
        let mut tracker = DirtyTracker::new(24, 80);
        let _ = tracker.find_dirty_region(TerminalEmulator::new(24, 80).screen());
        // Test passes if no panic
    }
}

mod handler_creation_tests {
    use guacr_handlers::ProtocolHandler;
    use guacr_telnet::TelnetHandler;

    #[test]
    fn test_telnet_handler_creation() {
        let handler = TelnetHandler::with_defaults();
        assert_eq!(handler.name(), "telnet");
    }

    #[tokio::test]
    async fn test_telnet_handler_health_check() {
        let handler = TelnetHandler::with_defaults();
        let health = handler.health_check().await;
        assert!(health.is_ok());
    }
}
