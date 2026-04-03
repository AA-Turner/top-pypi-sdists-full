// Autofill support for RBI
//
// Provides automatic credential filling for web pages, including:
// - Username/password injection
// - TOTP code generation and injection
// - Configurable field selectors (CSS or XPath)
// - Auto-submit support
//
// Ported from KCM's autofill.c with Rust improvements.

use log::{debug, info, warn};
use serde::{Deserialize, Serialize};
use std::time::{SystemTime, UNIX_EPOCH};

/// Autofill configuration for a single page
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AutofillRule {
    /// URL pattern to match (regex)
    #[serde(rename = "page-pattern")]
    pub page_pattern: Option<String>,

    /// CSS or XPath selector for username field
    #[serde(rename = "username-field")]
    pub username_field: Option<String>,

    /// CSS or XPath selector for password field
    #[serde(rename = "password-field")]
    pub password_field: Option<String>,

    /// CSS or XPath selector for TOTP field
    #[serde(rename = "totp-field")]
    pub totp_field: Option<String>,

    /// CSS or XPath selector for submit button/form
    pub submit: Option<String>,

    /// Selectors for elements that prevent auto-submit (e.g., captchas)
    #[serde(rename = "cannot-submit")]
    pub cannot_submit: Option<Vec<String>>,
}

/// TOTP configuration
#[derive(Debug, Clone)]
pub struct TotpConfig {
    /// Base32-encoded secret
    pub secret: String,
    /// Period in seconds (default: 30)
    pub period: u32,
    /// Number of digits (default: 6)
    pub digits: u8,
    /// Algorithm (SHA1, SHA256, SHA512)
    pub algorithm: TotpAlgorithm,
}

impl Default for TotpConfig {
    fn default() -> Self {
        Self {
            secret: String::new(),
            period: 30,
            digits: 6,
            algorithm: TotpAlgorithm::Sha1,
        }
    }
}

/// TOTP algorithm
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TotpAlgorithm {
    Sha1,
    Sha256,
    Sha512,
}

impl TotpAlgorithm {
    pub fn parse(s: &str) -> Self {
        match s.to_uppercase().as_str() {
            "SHA256" => Self::Sha256,
            "SHA512" => Self::Sha512,
            _ => Self::Sha1,
        }
    }
}

/// Autofill credentials
#[derive(Debug, Clone, Default)]
pub struct AutofillCredentials {
    pub username: Option<String>,
    pub password: Option<String>,
    pub totp_config: Option<TotpConfig>,
}

/// Generate TOTP code using RFC 6238 standard
///
/// This implementation uses proper HMAC-SHA1/SHA256/SHA512 as specified
/// in RFC 4226 (HOTP) and RFC 6238 (TOTP).
///
/// # Returns
/// * `Ok((code, expiration))` - The TOTP code and Unix timestamp when it expires
/// * `Err(String)` - Error message if generation fails
pub fn generate_totp(config: &TotpConfig) -> Result<(String, u64), String> {
    // Decode base32 secret
    let secret =
        base32_decode(&config.secret).ok_or_else(|| "Invalid base32 secret".to_string())?;

    // Get current time step
    let now = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .map_err(|e| format!("Time error: {}", e))?;
    let time_step = now.as_secs() / config.period as u64;

    // Calculate expiration
    let expiration = (time_step + 1) * config.period as u64;

    // Generate TOTP code using RFC 4226 HOTP with proper HMAC
    let code = hotp(&secret, time_step, config.digits, config.algorithm);

    Ok((code, expiration))
}

/// Simple base32 decode (RFC 4648)
pub(crate) fn base32_decode(input: &str) -> Option<Vec<u8>> {
    const ALPHABET: &[u8] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567";

    let input = input.to_uppercase();
    let input = input.trim_end_matches('=');

    let mut output = Vec::new();
    let mut buffer: u64 = 0;
    let mut bits = 0;

    for c in input.bytes() {
        let value = ALPHABET.iter().position(|&x| x == c)? as u64;
        buffer = (buffer << 5) | value;
        bits += 5;

        if bits >= 8 {
            bits -= 8;
            output.push((buffer >> bits) as u8);
            buffer &= (1 << bits) - 1;
        }
    }

    Some(output)
}

/// RFC 4226 HOTP implementation with proper HMAC
///
/// Generates a One-Time Password using HMAC-based algorithm.
/// This implementation follows RFC 4226 for HOTP and RFC 6238 for TOTP.
pub(crate) fn hotp(secret: &[u8], counter: u64, digits: u8, algorithm: TotpAlgorithm) -> String {
    use hmac::{Hmac, Mac};
    use sha1::Sha1;
    use sha2::{Sha256, Sha512};

    // Counter as 8-byte big-endian array (RFC 4226)
    let counter_bytes = counter.to_be_bytes();

    // Compute HMAC with selected algorithm
    let hmac_result = match algorithm {
        TotpAlgorithm::Sha1 => {
            let mut mac =
                Hmac::<Sha1>::new_from_slice(secret).expect("HMAC can take key of any size");
            mac.update(&counter_bytes);
            mac.finalize().into_bytes().to_vec()
        }
        TotpAlgorithm::Sha256 => {
            let mut mac =
                Hmac::<Sha256>::new_from_slice(secret).expect("HMAC can take key of any size");
            mac.update(&counter_bytes);
            mac.finalize().into_bytes().to_vec()
        }
        TotpAlgorithm::Sha512 => {
            let mut mac =
                Hmac::<Sha512>::new_from_slice(secret).expect("HMAC can take key of any size");
            mac.update(&counter_bytes);
            mac.finalize().into_bytes().to_vec()
        }
    };

    // Dynamic truncation (RFC 4226 Section 5.3)
    let offset = (hmac_result[hmac_result.len() - 1] & 0x0f) as usize;
    let binary = ((hmac_result[offset] & 0x7f) as u32) << 24
        | (hmac_result[offset + 1] as u32) << 16
        | (hmac_result[offset + 2] as u32) << 8
        | (hmac_result[offset + 3] as u32);

    // Generate code with specified number of digits
    let code = binary % 10u32.pow(digits as u32);
    format!("{:0width$}", code, width = digits as usize)
}

/// Generate autofill JavaScript
///
/// Creates JavaScript code that will fill credentials into a web page.
pub fn generate_autofill_js(
    rules: &[AutofillRule],
    credentials: &AutofillCredentials,
    totp_code: Option<&str>,
    totp_expiration: Option<u64>,
) -> String {
    let rules_json = serde_json::to_string(rules).unwrap_or_else(|_| "[]".to_string());

    let username = credentials.username.as_deref().unwrap_or("");
    let password = credentials.password.as_deref().unwrap_or("");
    let totp = totp_code.unwrap_or("");
    let expiration = totp_expiration.unwrap_or(0);

    format!(
        r#"
(function() {{
    const rules = {rules_json};
    const username = '{username}';
    const password = '{password}';
    const totpCode = '{totp}';
    const totpExpiration = {expiration};

    // Check if TOTP has expired
    if (totpExpiration > 0 && Date.now() / 1000 > totpExpiration) {{
        console.log('Guacamole autofill: TOTP expired');
        return;
    }}

    // Search in a single document (main or iframe)
    function searchInDocument(doc, query) {{
        try {{
            // XPath selector (starts with /)
            if (query.startsWith('/')) {{
                const result = doc.evaluate(query, doc, null,
                    XPathResult.ORDERED_NODE_ITERATOR_TYPE, null);
                const elements = [];
                let node;
                while ((node = result.iterateNext())) {{
                    elements.push(node);
                }}
                return elements;
            }}
            // CSS selector
            return Array.from(doc.querySelectorAll(query));
        }} catch (e) {{
            // Cross-origin iframes will throw
            return [];
        }}
    }}

    // Find all elements matching selector, including in same-origin iframes (KCM-481)
    function getMatchingElements(selector) {{
        if (!selector) return [];

        // Search main document
        let elements = searchInDocument(document, selector);

        // Also search in all iframes (same-origin only)
        const iframes = document.querySelectorAll('iframe');
        for (const iframe of iframes) {{
            try {{
                const iframeDoc = iframe.contentDocument || iframe.contentWindow?.document;
                if (iframeDoc) {{
                    elements = elements.concat(searchInDocument(iframeDoc, selector));
                }}
            }} catch (e) {{
                // Cross-origin iframe, skip
            }}
        }}

        return elements;
    }}

    function findElement(selector) {{
        const elements = getMatchingElements(selector);
        return elements.length > 0 ? elements[0] : null;
    }}

    function fillField(selector, value, isPassword) {{
        if (!selector || !value) return false;

        const element = findElement(selector);
        if (!element) return false;

        // Focus and fill
        element.focus();
        element.value = value;

        // Trigger events
        element.dispatchEvent(new Event('input', {{ bubbles: true }}));
        element.dispatchEvent(new Event('change', {{ bubbles: true }}));

        console.log('Guacamole autofill: Filled ' + (isPassword ? 'password' : 'field'));
        return true;
    }}

    function checkCanSubmit(cannotSubmitSelectors) {{
        if (!cannotSubmitSelectors) return true;

        const selectors = Array.isArray(cannotSubmitSelectors)
            ? cannotSubmitSelectors
            : [cannotSubmitSelectors];

        for (const selector of selectors) {{
            if (findElement(selector)) {{
                console.log('Guacamole autofill: Cannot submit - blocking element found');
                return false;
            }}
        }}
        return true;
    }}

    function submitForm(selector) {{
        if (!selector) return false;

        const element = findElement(selector);
        if (!element) return false;

        if (element.tagName === 'FORM') {{
            element.submit();
        }} else {{
            element.click();
        }}

        console.log('Guacamole autofill: Submitted');
        return true;
    }}

    // Apply matching rules
    const pageUrl = window.location.href;
    let filled = false;

    for (const rule of rules) {{
        // Check page pattern
        if (rule['page-pattern']) {{
            const pattern = new RegExp(rule['page-pattern']);
            if (!pattern.test(pageUrl)) continue;
        }}

        // Fill fields
        if (fillField(rule['username-field'], username, false)) filled = true;
        if (fillField(rule['password-field'], password, true)) filled = true;
        if (fillField(rule['totp-field'], totpCode, false)) filled = true;

        // Auto-submit if allowed
        if (filled && rule.submit && checkCanSubmit(rule['cannot-submit'])) {{
            setTimeout(() => submitForm(rule.submit), 500);
        }}
    }}

    if (filled) {{
        console.log('Guacamole autofill: Complete');
    }}
}})();
"#,
        rules_json = rules_json,
        username = username.replace('\'', "\\'"),
        password = password.replace('\'', "\\'"),
        totp = totp.replace('\'', "\\'"),
        expiration = expiration,
    )
}

/// Autofill manager
#[derive(Debug, Default)]
pub struct AutofillManager {
    rules: Vec<AutofillRule>,
    credentials: AutofillCredentials,
    last_totp_code: Option<String>,
    last_totp_expiration: Option<u64>,
}

impl AutofillManager {
    pub fn new() -> Self {
        Self::default()
    }

    /// Set autofill rules from JSON/YAML
    pub fn set_rules(&mut self, rules: Vec<AutofillRule>) {
        self.rules = rules;
        info!("RBI: Loaded {} autofill rules", self.rules.len());
    }

    /// Set credentials
    pub fn set_credentials(&mut self, credentials: AutofillCredentials) {
        self.credentials = credentials;
    }

    /// Generate autofill JavaScript for current page
    pub fn generate_js(&mut self) -> String {
        // Regenerate TOTP if configured and expired
        if let Some(ref config) = self.credentials.totp_config {
            let should_regenerate = self
                .last_totp_expiration
                .map(|exp| {
                    let now = SystemTime::now()
                        .duration_since(UNIX_EPOCH)
                        .map(|d| d.as_secs())
                        .unwrap_or(0);
                    now >= exp
                })
                .unwrap_or(true);

            if should_regenerate {
                match generate_totp(config) {
                    Ok((code, expiration)) => {
                        debug!("RBI: Generated TOTP code (expires at {})", expiration);
                        self.last_totp_code = Some(code);
                        self.last_totp_expiration = Some(expiration);
                    }
                    Err(e) => {
                        warn!("RBI: Failed to generate TOTP: {}", e);
                    }
                }
            }
        }

        generate_autofill_js(
            &self.rules,
            &self.credentials,
            self.last_totp_code.as_deref(),
            self.last_totp_expiration,
        )
    }

    /// Check if autofill is configured
    pub fn is_configured(&self) -> bool {
        !self.rules.is_empty()
            && (self.credentials.username.is_some()
                || self.credentials.password.is_some()
                || self.credentials.totp_config.is_some())
    }
}
