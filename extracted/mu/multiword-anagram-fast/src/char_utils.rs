use std::collections::HashMap;

pub const ALPHABET_SIZE: usize = 26;

#[inline]
pub fn char_to_index(c: char) -> Option<usize> {
    // Made public
    if c.is_ascii_lowercase() {
        Some((c as u8 - b'a') as usize)
    } else {
        None
    }
}

#[inline]
#[allow(dead_code)]
pub fn index_to_char(i: usize) -> char {
    // Made public (though not directly used by solver logic shown, might be useful)
    (b'a' + i as u8) as char
}

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct CharCounts([usize; ALPHABET_SIZE]); // Inner field remains private

#[allow(dead_code)]
impl CharCounts {
    pub fn new() -> Self {
        CharCounts([0; ALPHABET_SIZE])
    }

    pub fn from_str(s: &str) -> Result<Self, String> {
        let mut counts = [0; ALPHABET_SIZE];
        let mut _total_chars = 0; // Marked as unused as its value is not used later
        for c in s.chars() {
            if c.is_alphabetic() {
                let lower_c = c.to_ascii_lowercase();
                if let Some(idx) = char_to_index(lower_c) {
                    counts[idx] += 1;
                    _total_chars += 1;
                } else {
                    // This case should ideally not be hit if c.is_alphabetic() and c.to_ascii_lowercase() works
                    return Err(format!(
                        "Non-ASCII alphabetic character found after lowercase: {}",
                        lower_c
                    ));
                }
            } else if !c.is_whitespace() {
                // Ignoring non-alphabetic, non-whitespace.
                // Consider erroring: return Err(format!("Invalid character in input string: {}", c));
            }
        }
        Ok(CharCounts(counts))
    }

    pub fn total(&self) -> usize {
        self.0.iter().sum()
    }

    pub fn is_empty(&self) -> bool {
        self.0.iter().all(|&count| count == 0)
    }

    pub fn get(&self, c: char) -> Option<usize> {
        char_to_index(c).map(|idx| self.0[idx])
    }

    pub fn can_subtract(&self, other: &Self) -> bool {
        for i in 0..ALPHABET_SIZE {
            if self.0[i] < other.0[i] {
                return false;
            }
        }
        true
    }

    pub fn subtract_mut(&mut self, other: &Self) -> Result<(), String> {
        if !self.can_subtract(other) {
            return Err("Cannot subtract, insufficient characters.".to_string());
        }
        for i in 0..ALPHABET_SIZE {
            self.0[i] -= other.0[i];
        }
        Ok(())
    }

    pub fn add_mut(&mut self, other: &Self) {
        for i in 0..ALPHABET_SIZE {
            self.0[i] += other.0[i];
        }
    }

    // New methods for solver to use
    pub fn increment_char(&mut self, c: char) -> Result<(), String> {
        if let Some(idx) = char_to_index(c) {
            self.0[idx] += 1;
            Ok(())
        } else {
            Err(format!("Cannot increment count for invalid char: {}", c))
        }
    }

    pub fn decrement_char(&mut self, c: char) -> Result<(), String> {
        if let Some(idx) = char_to_index(c) {
            if self.0[idx] > 0 {
                self.0[idx] -= 1;
                Ok(())
            } else {
                Err(format!(
                    "Cannot decrement count for char '{}', count is already 0.",
                    c
                ))
            }
        } else {
            Err(format!("Cannot decrement count for invalid char: {}", c))
        }
    }
}

pub fn normalize_word(word: &str) -> String {
    word.trim()
        .to_ascii_lowercase()
        .chars()
        .filter(|c| c.is_ascii_alphabetic())
        .collect()
}

pub fn parse_char_list_to_set(s: Option<&str>) -> Option<std::collections::HashSet<char>> {
    s.map(|st| st.to_ascii_lowercase().chars().collect())
}

pub fn parse_char_list_to_counts(s: Option<&str>) -> Option<HashMap<char, usize>> {
    s.map(|st| {
        let mut counts = HashMap::new();
        for char_code in st.to_ascii_lowercase().chars() {
            *counts.entry(char_code).or_insert(0) += 1;
        }
        counts
    })
}

#[cfg(test)]
mod tests {
    use super::*; // Import items from the outer module

    #[test]
    fn test_char_counts_from_str() {
        let counts = CharCounts::from_str("apple!").unwrap();
        assert_eq!(counts.get('a'), Some(1));
        assert_eq!(counts.get('p'), Some(2));
        assert_eq!(counts.get('l'), Some(1));
        assert_eq!(counts.get('e'), Some(1));
        assert_eq!(counts.get('z'), Some(0)); // Or use get('!').is_none() if strict
        assert_eq!(counts.total(), 5);
    }

    #[test]
    fn test_normalize_word() {
        assert_eq!(normalize_word("  Apple Pie!  "), "applepie");
    }
}
