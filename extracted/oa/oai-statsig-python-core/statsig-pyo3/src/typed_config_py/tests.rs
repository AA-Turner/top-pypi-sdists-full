use super::*;
use statsig_rust::{DynamicReturnable, EvaluationDetails};

#[test]
fn typed_usability_excludes_incomplete_lookup_results_and_preserves_overrides() {
    let value = DynamicReturnable::from_map(Default::default());
    for (source, accepted) in [
        ("Network", true),
        ("Bootstrap", true),
        ("LocalOverride", true),
        ("CountryLookupNotLoaded", false),
        ("UAParserNotLoaded", false),
        ("Error", false),
        ("Loading", false),
        ("Uninitialized", false),
        ("NoValues", false),
    ] {
        let details = EvaluationDetails {
            reason: format!("{source}:Recognized"),
            lcut: None,
            received_at: None,
            version: None,
        };
        let mut raw = DynamicConfigRaw::empty("config", &details);
        assert!(!is_usable(&raw, source));
        for invalid_value in [
            DynamicReturnable::empty(),
            DynamicReturnable::from_bool(true),
        ] {
            let mut raw = DynamicConfigRaw::empty("config", &details);
            raw.value = Some(&invalid_value);
            assert!(!is_usable(&raw, source));
        }
        raw.value = Some(&value);
        assert_eq!(is_usable(&raw, source), accepted, "source={source}");
    }
    let details = EvaluationDetails {
        reason: "Network:Unrecognized".to_string(),
        lcut: None,
        received_at: None,
        version: None,
    };
    let mut raw = DynamicConfigRaw::empty("config", &details);
    raw.value = Some(&value);
    assert!(!is_usable(&raw, "Network"));
}
