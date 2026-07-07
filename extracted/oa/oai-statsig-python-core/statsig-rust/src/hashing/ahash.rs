use ahash::RandomState;
use std::{
    hash::{BuildHasher, Hash, Hasher},
    mem::size_of_val,
    slice,
};

lazy_static::lazy_static! {
    pub static ref HASHER: RandomState = RandomState::with_seeds(420, 42, 24, 4);
}

const INLINE_U64_HASH_CAPACITY: usize = 16;

/// Uses the ahash crate: https://crates.io/crates/ahash
/// - Faster than djb2.
/// - Randomized between each run of an application.
/// - Non-cryptographic.
/// - One way hash.
///
/// **Profiled**
///
/// djb2  time: 4.1869 ns
///
/// ahash time: 1.5757 ns
///
#[must_use]
pub fn ahash_str(input: &str) -> u64 {
    HASHER.hash_one(input)
}

pub fn hash_one<T: Hash>(x: T) -> u64 {
    HASHER.hash_one(x)
}

pub fn hash_u64_slice(values: &[u64]) -> u64 {
    let mut hasher = HASHER.build_hasher();
    hasher.write_usize(values.len());

    // Match `Hash for [u64]`: one native-endian contiguous byte write after the
    // length prefix. `u64` has no padding, and the byte slice is read-only.
    let bytes = unsafe { slice::from_raw_parts(values.as_ptr().cast::<u8>(), size_of_val(values)) };
    hasher.write(bytes);
    hasher.finish()
}

pub struct U64HashBuilder {
    inline: [u64; INLINE_U64_HASH_CAPACITY],
    len: usize,
    overflow: Option<Vec<u64>>,
}

impl Default for U64HashBuilder {
    fn default() -> Self {
        Self::new()
    }
}

impl U64HashBuilder {
    pub fn new() -> Self {
        Self::with_capacity(INLINE_U64_HASH_CAPACITY)
    }

    pub fn with_capacity(capacity: usize) -> Self {
        let overflow = if capacity > INLINE_U64_HASH_CAPACITY {
            Some(Vec::with_capacity(capacity))
        } else {
            None
        };

        Self {
            inline: [0; INLINE_U64_HASH_CAPACITY],
            len: 0,
            overflow,
        }
    }

    pub fn push(&mut self, value: u64) {
        if let Some(values) = &mut self.overflow {
            values.push(value);
            return;
        }

        if self.len < INLINE_U64_HASH_CAPACITY {
            self.inline[self.len] = value;
            self.len += 1;
            return;
        }

        let mut values = Vec::with_capacity(self.len + 1);
        values.extend_from_slice(&self.inline[..self.len]);
        values.push(value);
        self.overflow = Some(values);
    }

    pub fn finish(self) -> u64 {
        match self.overflow {
            Some(values) => hash_u64_slice(&values),
            None => hash_u64_slice(&self.inline[..self.len]),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashSet;
    #[test]
    fn test_gets_same_result_for_same_input() {
        let input = "some_random_input";
        let mut result = ahash_str(input);
        for _ in 0..1000 {
            let new_result = ahash_str(input);
            assert_eq!(result, new_result);
            result = new_result;
        }
    }

    #[test]
    fn test_gets_different_result_for_different_input() {
        let mut seen = HashSet::new();
        for i in 0..100_000 {
            let result = ahash_str(&format!("iter_{i}"));
            assert!(!seen.contains(&result));
            seen.insert(result);
        }
    }

    #[test]
    fn hash_u64_slice_matches_vec_hash() {
        let cases = [
            vec![],
            vec![1],
            vec![1, 2, 3],
            (0_u64..20).collect::<Vec<_>>(),
        ];

        for values in cases {
            assert_eq!(hash_u64_slice(&values), hash_one(values));
        }
    }

    #[test]
    fn u64_hash_builder_matches_vec_hash() {
        for len in [
            0,
            1,
            3,
            INLINE_U64_HASH_CAPACITY,
            INLINE_U64_HASH_CAPACITY + 1,
        ] {
            let values = (0..len).map(|value| value as u64 * 17).collect::<Vec<_>>();
            let mut builder = U64HashBuilder::with_capacity(values.len());
            for value in &values {
                builder.push(*value);
            }

            assert_eq!(builder.finish(), hash_one(values));
        }
    }
}
