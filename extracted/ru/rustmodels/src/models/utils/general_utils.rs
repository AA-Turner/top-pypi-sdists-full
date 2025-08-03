use pyo3::prelude::*;

/// Function to check if a term is numeric.
/// 
/// Args:
/// - `term`: A string representing the term to check.
/// 
/// Returns:
/// - `true` if the term is numeric, `false` otherwise.
#[pyfunction]
#[pyo3(name = "_is_numeric")]
pub fn is_numeric(string: &str) -> bool {
    // Check if the term is a valid numeric value
    string.parse::<f64>().is_ok()
}

#[cfg(test)]
mod tests {
    use crate::models::utils::general_utils;

    #[test]
    fn test_is_numeric() {
        let mut result: bool = general_utils::is_numeric(&"5");
        assert_eq!(result, true);
        result = general_utils::is_numeric(&"823489735".to_string());
        assert_eq!(result, true);
        result = general_utils::is_numeric(&"abcdefg".to_string());
        assert_eq!(result, false);
    }
}

