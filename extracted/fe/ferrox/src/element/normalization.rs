use super::Element;
use std::collections::HashMap;

// === Symbol Normalization ===

/// Result of normalizing an element symbol string.
///
/// Contains the parsed element, optional oxidation state, and any metadata
/// extracted from non-standard symbol formats (POTCAR suffixes, labels, etc.).
#[derive(Debug, Clone)]
pub struct NormalizedSymbol {
    /// The normalized element.
    pub element: Element,
    /// Oxidation state extracted from the symbol (e.g., "Fe2+" -> Some(2)).
    pub oxidation_state: Option<i8>,
    /// Additional metadata extracted from the symbol.
    pub metadata: HashMap<String, serde_json::Value>,
}

impl NormalizedSymbol {
    /// Create a new normalized symbol with no metadata.
    pub fn new(element: Element, oxidation_state: Option<i8>) -> Self {
        Self {
            element,
            oxidation_state,
            metadata: HashMap::new(),
        }
    }

    /// Create with metadata.
    pub fn with_metadata(
        element: Element,
        oxidation_state: Option<i8>,
        metadata: HashMap<String, serde_json::Value>,
    ) -> Self {
        Self {
            element,
            oxidation_state,
            metadata,
        }
    }
}

/// Normalize an element symbol string to extract the element and any metadata.
///
/// Handles various non-standard symbol formats:
/// - Standard elements: "Fe", "Ca", "O"
/// - Pseudo-elements: "X", "D", "T", "Vac"
/// - Oxidation states: "Fe2+", "O2-", "Na+", "Cl-"
/// - POTCAR suffixes: "Ca_pv", "Fe_sv", "O_s"
/// - Hash suffixes: "Fe/hash123" (stripped)
/// - CIF-style labels: "Fe1", "Fe1_oct"
///
/// # Returns
///
/// - `Ok(NormalizedSymbol)` with the parsed element and extracted data
/// - `Err(String)` for empty strings
///
/// Unknown symbols are mapped to `Element::Dummy` with original stored in metadata.
///
/// # Examples
///
/// ```
/// use ferrox::element::{normalize_symbol, Element};
///
/// let norm = normalize_symbol("Fe2+").unwrap();
/// assert_eq!(norm.element, Element::Fe);
/// assert_eq!(norm.oxidation_state, Some(2));
///
/// let norm = normalize_symbol("Ca_pv").unwrap();
/// assert_eq!(norm.element, Element::Ca);
/// assert_eq!(norm.metadata.get("potcar_suffix").unwrap(), "_pv");
///
/// let norm = normalize_symbol("Unknown123").unwrap();
/// assert_eq!(norm.element, Element::Dummy);
/// ```
pub fn normalize_symbol(symbol: &str) -> Result<NormalizedSymbol, String> {
    let symbol = symbol.trim();
    if symbol.is_empty() {
        return Err("Empty symbol".to_string());
    }

    // Fast path: exact match with known element
    if let Some(elem) = Element::from_symbol(symbol) {
        return Ok(NormalizedSymbol::new(elem, None));
    }

    // Check for oxidation state suffix: Fe2+, O2-, Na+, Cl-
    if let Some(result) = try_parse_oxidation_state(symbol) {
        return Ok(result);
    }

    // Check for POTCAR suffix: Ca_pv, Fe_sv, O_s
    if let Some(result) = try_parse_potcar_suffix(symbol) {
        return Ok(result);
    }

    // Check for hash suffix: Fe/hash123
    if let Some(pos) = symbol.find('/') {
        let base = &symbol[..pos];
        if let Some(elem) = Element::from_symbol(base) {
            return Ok(NormalizedSymbol::new(elem, None));
        }
    }

    // Check for CIF-style label: Fe1, Fe1_oct, Na2a
    if let Some(result) = try_parse_cif_label(symbol) {
        return Ok(result);
    }

    // Fallback: treat as Dummy atom
    let mut metadata = HashMap::new();
    metadata.insert(
        "original_symbol".to_string(),
        serde_json::Value::String(symbol.to_string()),
    );
    Ok(NormalizedSymbol::with_metadata(
        Element::Dummy,
        None,
        metadata,
    ))
}

/// Try to parse oxidation state from symbol like "Fe2+", "O2-", "Na+", "Cl-".
fn try_parse_oxidation_state(symbol: &str) -> Option<NormalizedSymbol> {
    let last_char = symbol.chars().last()?;
    if last_char != '+' && last_char != '-' {
        return None;
    }

    let sign: i8 = if last_char == '+' { 1 } else { -1 };
    let without_sign = &symbol[..symbol.len() - 1];

    // Find where digits start (from the end)
    let mut digit_start = without_sign.len();
    for (idx, ch) in without_sign.char_indices().rev() {
        if ch.is_ascii_digit() {
            digit_start = idx;
        } else {
            break;
        }
    }

    let elem_str = &without_sign[..digit_start];
    let elem = Element::from_symbol(elem_str)?;

    let oxi = if digit_start == without_sign.len() {
        // No digits, just sign: Na+ -> +1, Cl- -> -1
        sign
    } else {
        let digit_str = &without_sign[digit_start..];
        let magnitude: i8 = digit_str.parse().ok()?;
        sign * magnitude
    };

    Some(NormalizedSymbol::new(elem, Some(oxi)))
}

/// Try to parse POTCAR suffix: Ca_pv, Fe_sv, O_s, etc.
fn try_parse_potcar_suffix(symbol: &str) -> Option<NormalizedSymbol> {
    // Known POTCAR suffixes
    const POTCAR_SUFFIXES: &[&str] = &[
        "_pv", "_sv", "_s", "_h", "_d", "_f", "_sv_GW", "_pv_GW", "_GW",
    ];

    for suffix in POTCAR_SUFFIXES {
        if let Some(base) = symbol.strip_suffix(suffix)
            && let Some(elem) = Element::from_symbol(base)
        {
            let mut metadata = HashMap::new();
            metadata.insert(
                "potcar_suffix".to_string(),
                serde_json::Value::String(suffix.to_string()),
            );
            return Some(NormalizedSymbol::with_metadata(elem, None, metadata));
        }
    }
    None
}

/// Try to parse CIF-style label: Fe1, Fe1_oct, Na2a, etc.
fn try_parse_cif_label(symbol: &str) -> Option<NormalizedSymbol> {
    // Extract alphabetic prefix as element symbol
    let elem_str: String = symbol.chars().take_while(|c| c.is_alphabetic()).collect();
    if elem_str.is_empty() {
        return None;
    }

    let elem = Element::from_symbol(&elem_str)?;

    // Store the full label if it differs from the element symbol
    if symbol.len() > elem_str.len() {
        let mut metadata = HashMap::new();
        metadata.insert(
            "label".to_string(),
            serde_json::Value::String(symbol.to_string()),
        );
        Some(NormalizedSymbol::with_metadata(elem, None, metadata))
    } else {
        Some(NormalizedSymbol::new(elem, None))
    }
}
