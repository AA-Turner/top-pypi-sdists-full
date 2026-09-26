//! Per-call cryptographic identities; no buffered userspace RNG state or IDs.
use rand::{RngCore, rngs::OsRng};

const ALPHABET: &[u8; 62] = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
const MAX_COMPONENT_SIZE: usize = 1024;

/// Immutable formatting policy. Entropy is fetched from the OS on every call,
/// so forking cannot duplicate cached identities or a userspace generator state.
pub struct RandomUserId {
    prefix: String,
    length: usize,
}

impl RandomUserId {
    pub fn new(prefix: String, length: usize) -> Result<Self, &'static str> {
        if length == 0 || length > MAX_COMPONENT_SIZE {
            return Err("Random ID length must be between 1 and 1024");
        }
        if prefix.len() > MAX_COMPONENT_SIZE {
            return Err("Random ID prefix must be at most 1024 UTF-8 bytes");
        }
        Ok(Self { prefix, length })
    }

    pub fn generate(&self) -> Result<String, rand::Error> {
        self.generate_with_rng(&mut OsRng)
    }

    fn generate_with_rng(&self, rng: &mut impl RngCore) -> Result<String, rand::Error> {
        let mut output = String::with_capacity(self.prefix.len() + 1 + self.length);
        output.push_str(&self.prefix);
        if !self.prefix.is_empty() {
            output.push('-');
        }
        let target = output.len() + self.length;
        let mut entropy = [0u8; 64];
        while output.len() < target {
            let count = (target - output.len()).saturating_add(8).min(entropy.len());
            rng.try_fill_bytes(&mut entropy[..count])?;
            for byte in &entropy[..count] {
                // 248 is exactly four alphabets: rejection avoids modulo bias.
                if *byte < 248 {
                    output.push(ALPHABET[(*byte % 62) as usize] as char);
                    if output.len() == target {
                        break;
                    }
                }
            }
        }
        Ok(output)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::num::NonZeroU32;

    struct FixedEntropy {
        fail: bool,
    }

    impl RngCore for FixedEntropy {
        fn next_u32(&mut self) -> u32 {
            unreachable!()
        }
        fn next_u64(&mut self) -> u64 {
            unreachable!()
        }
        fn fill_bytes(&mut self, _: &mut [u8]) {
            unreachable!()
        }
        fn try_fill_bytes(&mut self, bytes: &mut [u8]) -> Result<(), rand::Error> {
            if self.fail {
                return Err(rand::Error::from(
                    NonZeroU32::new(rand::Error::CUSTOM_START).unwrap(),
                ));
            }
            let input = [
                248, 249, 250, 251, 252, 253, 254, 255, 0, 61, 62, 123, 124, 185, 186, 247,
            ];
            bytes.copy_from_slice(&input[..bytes.len()]);
            Ok(())
        }
    }

    #[test]
    fn rejects_biased_bytes_and_preserves_prefix() {
        let options = RandomUserId::new("匿名".into(), 8).unwrap();
        assert_eq!(
            options
                .generate_with_rng(&mut FixedEntropy { fail: false })
                .unwrap(),
            "匿名-A9A9A9A9"
        );
    }

    #[test]
    fn entropy_failure_returns_error_without_identity_fallback() {
        let options = RandomUserId::new("anon".into(), 8).unwrap();
        assert!(
            options
                .generate_with_rng(&mut FixedEntropy { fail: true })
                .is_err()
        );
    }
}
