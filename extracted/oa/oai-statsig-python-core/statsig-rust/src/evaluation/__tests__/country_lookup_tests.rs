use super::{COUNTRY_RANGES, CountryLookup};
use rusty_fork::rusty_fork_test;
use std::sync::Barrier;

fn assert_lookup(ip: &str, country: Option<&str>, reason: Option<&str>) {
    for initial_reason in [None, Some("existing override")] {
        let mut override_reason = initial_reason;
        let actual = CountryLookup::lookup(ip, &mut override_reason)
            .and_then(|value| value.string_value.map(|country| country.value));
        assert_eq!(
            (actual.as_deref(), override_reason),
            (country, reason.or(initial_reason)),
            "{ip:?} with {initial_reason:?}"
        );
    }
}

rusty_fork_test! {
    #[test]
    fn concurrent_country_lookup_initialization_marks_it_loaded() {
        assert!(!CountryLookup::is_loaded());
        let barrier = Barrier::new(16);
        std::thread::scope(|scope| {
            for _ in 0..16 {
                scope.spawn(|| {
                    barrier.wait();
                    CountryLookup::load_country_lookup();
                });
            }
        });

        assert!(CountryLookup::is_loaded());
    }

    #[test]
    fn compact_country_codebook_preserves_known_ipv4_ranges_and_boundaries() {
        CountryLookup::load_country_lookup();
        assert_eq!(COUNTRY_RANGES.len(), 198_578);

        let country_for = |ip: [u8; 4]| {
            let address = u32::from_be_bytes(ip);
            CountryLookup::lookup_numeric(address)
                .and_then(|value| value.string_value.map(|country| country.value))
        };

        assert_eq!(country_for([8, 8, 8, 8]).as_deref(), Some("US"));
        assert_eq!(country_for([31, 13, 64, 1]).as_deref(), Some("NL"));
        assert_eq!(country_for([127, 0, 0, 1]), None);
        assert_eq!(country_for([255, 255, 255, 255]), None);

        assert_eq!(country_for([0, 255, 255, 255]), None);
        assert_eq!(country_for([1, 0, 0, 0]).as_deref(), Some("US"));
        assert_eq!(country_for([1, 0, 0, 255]).as_deref(), Some("US"));
        assert_eq!(country_for([1, 0, 1, 0]).as_deref(), Some("CN"));
    }

    #[test]
    fn country_lookup_ipv4_parser_preserves_readiness_and_octet_syntax() {
        assert!(!CountryLookup::is_loaded());
        for ip in ["8.8.8", "8.8.8.8.", "::1"] {
            assert_lookup(ip, None, None);
        }
        for ip in ["8.8.8.8", "a.b.c.d", "8.8.8."] {
            assert_lookup(ip, None, Some("CountryLookupNotLoaded"));
        }

        CountryLookup::load_country_lookup();
        for ip in ["8.8.8.8", "008.008.008.008", "+8.8.8.8"] {
            assert_lookup(ip, Some("US"), None);
        }
        assert_lookup("31.13.64.1", Some("NL"), None);
        for ip in [
            "8.8.8", "8.8.8.8.", "8.8.8.", "256.0.0.0",
            "8.8.7.264", "8.-1.0.0", "a.b.c.d", "::1",
        ] {
            assert_lookup(ip, None, None);
        }
    }
}

#[test]
fn country_parser_matches_scalar_for_octet_widths_and_malformed_inputs() {
    let check = |bytes: &[u8]| {
        let ip = std::str::from_utf8(bytes).unwrap();
        let expected = CountryLookup::parse_scalar(ip);
        assert_eq!(CountryLookup::parse_address(ip), expected, "{ip:?}");
        expected.is_some()
    };

    #[repr(align(16))]
    struct Aligned([u8; 16]);
    for len in 7..=15 {
        // Includes all 81 valid layouts and invalid masks sharing a hash slot.
        for mask in 0..1 << len {
            let mut padded = Aligned([b'1'; 16]);
            let ip = &mut padded.0[1..=len];
            for (offset, byte) in ip.iter_mut().enumerate() {
                if mask & (1 << offset) != 0 {
                    *byte = b'.';
                }
            }
            if !check(ip) {
                continue;
            }
            // Tag each digit in turn so a misplaced shuffle lane changes the result.
            for offset in 0..len {
                if ip[offset] == b'1' {
                    ip[offset] = b'2';
                    check(ip);
                    ip[offset] = b'1';
                }
            }
        }
    }
    for octet in [
        "009", "255", "256", "999", "0000", "+2", "+99", "-", "²", "６", "\0",
    ] {
        for part in 0..4 {
            let mut octets = ["21"; 4];
            octets[part] = octet;
            check(octets.join(".").as_bytes());
        }
    }
}
