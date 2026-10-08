use std::collections::HashSet;

/// Exact ID-list membership storage.
///
/// The evaluator's eight-byte hash prefixes are stored inline. Other strings
/// keep their full contents, so this representation does not add hashing or
/// truncation to the ID-list protocol.
#[derive(Clone, Debug, Default, PartialEq, Eq)]
pub struct IdListIds {
    inline: HashSet<[u8; 8]>,
    other: HashSet<String>,
}

impl IdListIds {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn contains(&self, value: &str) -> bool {
        match <[u8; 8]>::try_from(value.as_bytes()) {
            Ok(key) => self.inline.contains(&key),
            Err(_) => self.other.contains(value),
        }
    }

    pub fn insert(&mut self, value: String) -> bool {
        match <[u8; 8]>::try_from(value.as_bytes()) {
            Ok(key) => self.inline.insert(key),
            Err(_) => self.other.insert(value),
        }
    }

    /// Inserts a borrowed ID without allocating a string for an eight-byte ID.
    pub fn insert_str(&mut self, value: &str) -> bool {
        match <[u8; 8]>::try_from(value.as_bytes()) {
            Ok(key) => self.inline.insert(key),
            Err(_) => self.other.insert(value.to_owned()),
        }
    }

    pub fn remove(&mut self, value: &str) -> bool {
        match <[u8; 8]>::try_from(value.as_bytes()) {
            Ok(key) => self.inline.remove(&key),
            Err(_) => self.other.remove(value),
        }
    }

    pub fn len(&self) -> usize {
        self.inline.len() + self.other.len()
    }

    pub fn is_empty(&self) -> bool {
        self.inline.is_empty() && self.other.is_empty()
    }

    /// Iterates over the original strings in arbitrary order.
    pub fn iter(&self) -> impl Iterator<Item = &str> {
        self.inline
            .iter()
            // Inline keys can only be inserted from valid UTF-8 strings.
            .map(|key| std::str::from_utf8(key).expect("ID-list keys are valid UTF-8"))
            .chain(self.other.iter().map(String::as_str))
    }
}

impl FromIterator<String> for IdListIds {
    fn from_iter<T: IntoIterator<Item = String>>(values: T) -> Self {
        let mut ids = Self::new();
        for value in values {
            ids.insert(value);
        }
        ids
    }
}

impl<const N: usize> From<[String; N]> for IdListIds {
    fn from(values: [String; N]) -> Self {
        values.into_iter().collect()
    }
}
