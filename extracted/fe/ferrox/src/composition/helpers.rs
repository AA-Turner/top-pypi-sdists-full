use super::{AMOUNT_TOLERANCE, ELEMENT_AMOUNT_RE, PAREN_GROUP_RE};
use crate::element::Element;
use crate::error::{FerroxError, Result};
use crate::species::Species;
use indexmap::IndexMap;

// === Helper Functions ===

/// Parse a formula string recursively, expanding parentheses.
pub(crate) fn parse_formula_recursive(formula: &str) -> Result<Vec<(Species, f64)>> {
    let mut formula = formula.to_string();
    let mut parse_error: Option<FerroxError> = None;

    // Recursively expand parentheses from innermost to outermost
    while PAREN_GROUP_RE.is_match(&formula) {
        let new_formula = PAREN_GROUP_RE.replace(&formula, |caps: &regex::Captures| {
            let inner = &caps[1];
            let mult_str = &caps[2];
            let multiplier: f64 = if mult_str.is_empty() {
                1.0
            } else {
                match mult_str.parse() {
                    Ok(v) => v,
                    Err(_) => {
                        parse_error = Some(FerroxError::ParseError {
                            path: "formula".into(),
                            reason: format!("Invalid multiplier '{mult_str}' for group ({inner})"),
                        });
                        1.0 // Dummy value, error will be returned after replace
                    }
                }
            };

            // Parse inner content and multiply amounts
            match parse_flat_formula(inner) {
                Ok(inner_species) => inner_species
                    .iter()
                    .map(|(sp, amt)| format!("{}{}", sp.element.symbol(), amt * multiplier))
                    .collect::<Vec<_>>()
                    .join(""),
                Err(err) => {
                    parse_error = Some(err);
                    inner.to_string()
                }
            }
        });
        formula = new_formula.to_string();

        // Propagate any error from inner parsing
        if let Some(err) = parse_error {
            return Err(err);
        }
    }

    let results = parse_flat_formula(&formula)?;
    if results.is_empty() {
        return Err(FerroxError::ParseError {
            path: "formula".into(),
            reason: "No elements found in formula".into(),
        });
    }
    Ok(results)
}

/// Parse a flat formula (no parentheses) into species-amount pairs.
fn parse_flat_formula(formula: &str) -> Result<Vec<(Species, f64)>> {
    let mut results: IndexMap<Species, f64> = IndexMap::new();

    for cap in ELEMENT_AMOUNT_RE.captures_iter(formula) {
        let symbol = &cap[1];
        let amt_str = &cap[2];
        let amt: f64 = if amt_str.is_empty() {
            1.0
        } else {
            amt_str.parse().map_err(|_| FerroxError::ParseError {
                path: "formula".into(),
                reason: format!("Invalid amount '{amt_str}' for element {symbol}"),
            })?
        };

        let element = Element::from_symbol(symbol).ok_or_else(|| FerroxError::ParseError {
            path: "formula".into(),
            reason: format!("Unknown element symbol: {symbol}"),
        })?;

        *results.entry(Species::neutral(element)).or_insert(0.0) += amt;
    }

    Ok(results.into_iter().collect())
}

/// Hill formula sort key: C=0, H=1 (only if carbon present), rest alphabetical.
pub(crate) fn hill_sort_key(sym: &str, has_carbon: bool) -> (u8, &str) {
    match sym {
        "C" => (0, sym),
        "H" if has_carbon => (1, sym),
        _ => (2, sym),
    }
}

/// Format a symbol-amount pair for display.
pub(crate) fn format_amount(symbol: &str, amt: f64) -> String {
    if (amt - 1.0).abs() < AMOUNT_TOLERANCE {
        symbol.to_string()
    } else if (amt - amt.round()).abs() < AMOUNT_TOLERANCE {
        format!("{}{}", symbol, amt.round() as i64)
    } else {
        format!("{}{:.2}", symbol, amt)
    }
}

/// Compute GCD of two integers.
pub fn gcd_i64(mut left: i64, mut right: i64) -> i64 {
    left = left.abs();
    right = right.abs();
    while right != 0 {
        let temp = right;
        right = left % right;
        left = temp;
    }
    left
}

/// Compute GCD of two floating point numbers.
pub(crate) fn gcd_float(mut a: f64, mut b: f64) -> f64 {
    const MAX_ITER: usize = 100;

    a = a.abs();
    b = b.abs();

    for _ in 0..MAX_ITER {
        if b < AMOUNT_TOLERANCE {
            return a;
        }
        let temp = b;
        b = a % b;
        a = temp;
    }

    1.0 // Fallback
}
