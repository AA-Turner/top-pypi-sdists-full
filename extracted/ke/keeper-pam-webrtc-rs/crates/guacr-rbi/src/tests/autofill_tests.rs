use crate::autofill::{
    generate_autofill_js, generate_totp, hotp, AutofillCredentials, AutofillManager, AutofillRule,
    TotpAlgorithm, TotpConfig,
};

fn base32_decode(s: &str) -> Option<Vec<u8>> {
    crate::autofill::base32_decode(s)
}

#[test]
fn test_base32_decode() {
    let decoded = base32_decode("ORSXG5A").unwrap();
    assert_eq!(decoded, b"test");

    let decoded2 = base32_decode("GEZDGNBVGY3TQOJQ").unwrap();
    assert!(!decoded2.is_empty());
}

#[test]
fn test_base32_decode_with_padding() {
    let decoded = base32_decode("ORSXG5A=").unwrap();
    assert_eq!(decoded, b"test");

    let decoded2 = base32_decode("ORSXG5A").unwrap();
    assert_eq!(decoded2, b"test");
}

#[test]
fn test_base32_decode_invalid() {
    assert!(base32_decode("!!!").is_none());
    assert!(base32_decode("12345678").is_none());
}

#[test]
fn test_base32_decode_case_insensitive() {
    let upper = base32_decode("ORSXG5A").unwrap();
    let lower = base32_decode("orsxg5a").unwrap();
    assert_eq!(upper, lower);
}

#[test]
fn test_autofill_rule_parse() {
    let json = r##"{"page-pattern": "https://example.com/login", "username-field": "#username", "password-field": "#password", "submit": "button[type=submit]"}"##;

    let rule: AutofillRule = serde_json::from_str(json).unwrap();
    assert_eq!(
        rule.page_pattern.as_deref(),
        Some("https://example.com/login")
    );
    assert_eq!(rule.username_field.as_deref(), Some("#username"));
    assert_eq!(rule.password_field.as_deref(), Some("#password"));
    assert_eq!(rule.submit.as_deref(), Some("button[type=submit]"));
}

#[test]
fn test_autofill_rule_parse_with_cannot_submit() {
    let json = r##"{"page-pattern": ".*", "username-field": "#user", "cannot-submit": ["#captcha", ".recaptcha"]}"##;

    let rule: AutofillRule = serde_json::from_str(json).unwrap();
    assert!(rule.cannot_submit.is_some());
    let cannot = rule.cannot_submit.unwrap();
    assert_eq!(cannot.len(), 2);
    assert!(cannot.contains(&"#captcha".to_string()));
    assert!(cannot.contains(&".recaptcha".to_string()));
}

#[test]
fn test_autofill_rule_xpath() {
    let json = r##"{"username-field": "//input[@name='email']", "password-field": "//input[@type='password']"}"##;

    let rule: AutofillRule = serde_json::from_str(json).unwrap();
    assert!(rule.username_field.as_deref().unwrap().starts_with("/"));
    assert!(rule.password_field.as_deref().unwrap().starts_with("/"));
}

#[test]
fn test_generate_autofill_js() {
    let rules = vec![AutofillRule {
        page_pattern: Some(".*".to_string()),
        username_field: Some("#user".to_string()),
        password_field: Some("#pass".to_string()),
        totp_field: None,
        submit: Some("#login".to_string()),
        cannot_submit: None,
    }];

    let credentials = AutofillCredentials {
        username: Some("testuser".to_string()),
        password: Some("secret".to_string()),
        totp_config: None,
    };

    let js = generate_autofill_js(&rules, &credentials, None, None);
    assert!(js.contains("testuser"));
    assert!(js.contains("#user"));
    assert!(js.contains("#login"));
}

#[test]
fn test_generate_autofill_js_with_totp() {
    let rules = vec![AutofillRule {
        page_pattern: None,
        username_field: Some("#email".to_string()),
        password_field: Some("#password".to_string()),
        totp_field: Some("#otp".to_string()),
        submit: None,
        cannot_submit: None,
    }];

    let credentials = AutofillCredentials {
        username: Some("user@example.com".to_string()),
        password: Some("password123".to_string()),
        totp_config: None,
    };

    let js = generate_autofill_js(&rules, &credentials, Some("123456"), Some(1234567890));
    assert!(js.contains("123456"));
    assert!(js.contains("1234567890"));
    assert!(js.contains("#otp"));
}

#[test]
fn test_generate_autofill_js_escapes_quotes() {
    let rules = vec![];
    let credentials = AutofillCredentials {
        username: Some("user'name".to_string()),
        password: Some("pass'word".to_string()),
        totp_config: None,
    };

    let js = generate_autofill_js(&rules, &credentials, None, None);
    assert!(js.contains(r"user\'name"));
    assert!(js.contains(r"pass\'word"));
}

#[test]
fn test_generate_autofill_js_iframe_traversal() {
    let rules = vec![AutofillRule {
        page_pattern: None,
        username_field: Some("#user".to_string()),
        password_field: None,
        totp_field: None,
        submit: None,
        cannot_submit: None,
    }];

    let credentials = AutofillCredentials::default();

    let js = generate_autofill_js(&rules, &credentials, None, None);

    assert!(js.contains("iframe"));
    assert!(js.contains("contentDocument"));
    assert!(js.contains("searchInDocument"));
    assert!(js.contains("getMatchingElements"));
}

#[test]
fn test_totp_config_default() {
    let config = TotpConfig::default();
    assert_eq!(config.period, 30);
    assert_eq!(config.digits, 6);
    assert_eq!(config.algorithm, TotpAlgorithm::Sha1);
    assert!(config.secret.is_empty());
}

#[test]
fn test_totp_algorithm_from_str() {
    assert_eq!(TotpAlgorithm::parse("SHA1"), TotpAlgorithm::Sha1);
    assert_eq!(TotpAlgorithm::parse("sha1"), TotpAlgorithm::Sha1);
    assert_eq!(TotpAlgorithm::parse("SHA256"), TotpAlgorithm::Sha256);
    assert_eq!(TotpAlgorithm::parse("SHA512"), TotpAlgorithm::Sha512);
    assert_eq!(TotpAlgorithm::parse("unknown"), TotpAlgorithm::Sha1);
}

#[test]
fn test_autofill_manager_not_configured() {
    let manager = AutofillManager::new();
    assert!(!manager.is_configured());
}

#[test]
fn test_autofill_manager_with_rules_only() {
    let mut manager = AutofillManager::new();
    manager.set_rules(vec![AutofillRule {
        page_pattern: Some(".*".to_string()),
        username_field: Some("#user".to_string()),
        password_field: None,
        totp_field: None,
        submit: None,
        cannot_submit: None,
    }]);

    assert!(!manager.is_configured());
}

#[test]
fn test_autofill_manager_configured() {
    let mut manager = AutofillManager::new();
    manager.set_rules(vec![AutofillRule {
        page_pattern: Some(".*".to_string()),
        username_field: Some("#user".to_string()),
        password_field: None,
        totp_field: None,
        submit: None,
        cannot_submit: None,
    }]);
    manager.set_credentials(AutofillCredentials {
        username: Some("test".to_string()),
        password: None,
        totp_config: None,
    });

    assert!(manager.is_configured());
}

#[test]
fn test_autofill_manager_generate_js() {
    let mut manager = AutofillManager::new();
    manager.set_rules(vec![AutofillRule {
        page_pattern: None,
        username_field: Some("#email".to_string()),
        password_field: Some("#password".to_string()),
        totp_field: None,
        submit: Some("form".to_string()),
        cannot_submit: None,
    }]);
    manager.set_credentials(AutofillCredentials {
        username: Some("admin@test.com".to_string()),
        password: Some("admin123".to_string()),
        totp_config: None,
    });

    let js = manager.generate_js();
    assert!(js.contains("admin@test.com"));
    assert!(js.contains("#email"));
    assert!(js.contains("form"));
}

#[test]
fn test_generate_totp() {
    let config = TotpConfig {
        secret: "GEZDGNBVGY3TQOJQ".to_string(),
        period: 30,
        digits: 6,
        algorithm: TotpAlgorithm::Sha1,
    };

    let result = generate_totp(&config);
    assert!(result.is_ok());

    let (code, expiration) = result.unwrap();
    assert_eq!(code.len(), 6);
    assert!(expiration > 0);
    assert!(code.chars().all(|c| c.is_ascii_digit()));
}

#[test]
fn test_generate_totp_invalid_secret() {
    let config = TotpConfig {
        secret: "!!!invalid!!!".to_string(),
        period: 30,
        digits: 6,
        algorithm: TotpAlgorithm::Sha1,
    };

    let result = generate_totp(&config);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Invalid base32"));
}

/// RFC 6238 Appendix B test vectors
#[test]
fn test_totp_rfc6238_test_vectors() {
    fn totp_at_time(secret_bytes: &[u8], timestamp: u64, algorithm: TotpAlgorithm) -> String {
        let time_step = timestamp / 30;
        hotp(secret_bytes, time_step, 8, algorithm)
    }

    let secret_sha1 = b"12345678901234567890";

    assert_eq!(
        totp_at_time(secret_sha1, 59, TotpAlgorithm::Sha1),
        "94287082"
    );
    assert_eq!(
        totp_at_time(secret_sha1, 1111111109, TotpAlgorithm::Sha1),
        "07081804"
    );
    assert_eq!(
        totp_at_time(secret_sha1, 1111111111, TotpAlgorithm::Sha1),
        "14050471"
    );
    assert_eq!(
        totp_at_time(secret_sha1, 1234567890, TotpAlgorithm::Sha1),
        "89005924"
    );
    assert_eq!(
        totp_at_time(secret_sha1, 2000000000, TotpAlgorithm::Sha1),
        "69279037"
    );
    assert_eq!(
        totp_at_time(secret_sha1, 20000000000, TotpAlgorithm::Sha1),
        "65353130"
    );

    let secret_sha256 = b"12345678901234567890123456789012";

    assert_eq!(
        totp_at_time(secret_sha256, 59, TotpAlgorithm::Sha256),
        "46119246"
    );
    assert_eq!(
        totp_at_time(secret_sha256, 1111111109, TotpAlgorithm::Sha256),
        "68084774"
    );
    assert_eq!(
        totp_at_time(secret_sha256, 1111111111, TotpAlgorithm::Sha256),
        "67062674"
    );
    assert_eq!(
        totp_at_time(secret_sha256, 1234567890, TotpAlgorithm::Sha256),
        "91819424"
    );
    assert_eq!(
        totp_at_time(secret_sha256, 2000000000, TotpAlgorithm::Sha256),
        "90698825"
    );
    assert_eq!(
        totp_at_time(secret_sha256, 20000000000, TotpAlgorithm::Sha256),
        "77737706"
    );

    let secret_sha512 = b"1234567890123456789012345678901234567890123456789012345678901234";

    assert_eq!(
        totp_at_time(secret_sha512, 59, TotpAlgorithm::Sha512),
        "90693936"
    );
    assert_eq!(
        totp_at_time(secret_sha512, 1111111109, TotpAlgorithm::Sha512),
        "25091201"
    );
    assert_eq!(
        totp_at_time(secret_sha512, 1111111111, TotpAlgorithm::Sha512),
        "99943326"
    );
    assert_eq!(
        totp_at_time(secret_sha512, 1234567890, TotpAlgorithm::Sha512),
        "93441116"
    );
    assert_eq!(
        totp_at_time(secret_sha512, 2000000000, TotpAlgorithm::Sha512),
        "38618901"
    );
    assert_eq!(
        totp_at_time(secret_sha512, 20000000000, TotpAlgorithm::Sha512),
        "47863826"
    );
}

#[test]
fn test_credentials_default() {
    let creds = AutofillCredentials::default();
    assert!(creds.username.is_none());
    assert!(creds.password.is_none());
    assert!(creds.totp_config.is_none());
}
