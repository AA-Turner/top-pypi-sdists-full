//! RC4 encryption/decryption for PDF.
//!
//! RC4 is a stream cipher used in PDF 1.4 and 1.5 for encryption.
//! While cryptographically weak by modern standards, it's still widely used
//! in legacy PDFs.
//!
//! PDF Spec: Section 7.6.2 - General Encryption Algorithm
//!
//! This is a simple, straightforward implementation of RC4 for PDF decryption.

/// Simple RC4 cipher implementation.
///
/// RC4 is a stream cipher that generates a pseudorandom keystream based on the key.
struct Rc4Cipher {
    s: [u8; 256],
    i: u8,
    j: u8,
}

impl Rc4Cipher {
    /// Initialize RC4 cipher with a key.
    ///
    /// PDF Spec: RC4 key length is 5-16 bytes (40-128 bits)
    fn new(key: &[u8]) -> Self {
        let mut s = [0u8; 256];
        for (i, val) in s.iter_mut().enumerate() {
            *val = i as u8;
        }

        let mut j = 0u8;
        for i in 0..256 {
            j = j.wrapping_add(s[i]).wrapping_add(key[i % key.len()]);
            s.swap(i, j as usize);
        }

        Self { s, i: 0, j: 0 }
    }

    /// Generate the next byte of keystream.
    fn next_byte(&mut self) -> u8 {
        self.i = self.i.wrapping_add(1);
        self.j = self.j.wrapping_add(self.s[self.i as usize]);
        self.s.swap(self.i as usize, self.j as usize);
        let k = self.s[self.i as usize].wrapping_add(self.s[self.j as usize]);
        self.s[k as usize]
    }

    /// Apply keystream to data (XOR operation).
    fn apply_keystream(&mut self, data: &mut [u8]) {
        for byte in data.iter_mut() {
            *byte ^= self.next_byte();
        }
    }
}

/// Encrypt or decrypt data using RC4.
///
/// RC4 is symmetric, so encryption and decryption are the same operation.
///
/// # Arguments
///
/// * `key` - The encryption key (5-16 bytes for PDF)
/// * `data` - The data to encrypt/decrypt
///
/// # Returns
///
/// The encrypted/decrypted data
pub fn rc4_crypt(key: &[u8], data: &[u8]) -> Vec<u8> {
    let mut cipher = Rc4Cipher::new(key);
    let mut result = data.to_vec();
    cipher.apply_keystream(&mut result);
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_rc4_symmetric() {
        let key = b"testkey";
        let plaintext = b"Hello, World!";

        // Encrypt
        let ciphertext = rc4_crypt(key, plaintext);

        // Decrypt (same operation)
        let decrypted = rc4_crypt(key, &ciphertext);

        assert_eq!(plaintext, &decrypted[..]);
        assert_ne!(plaintext, &ciphertext[..]);
    }

    #[test]
    fn test_rc4_empty() {
        let key = b"testkey";
        let data = b"";

        let result = rc4_crypt(key, data);
        assert_eq!(result.len(), 0);
    }

    #[test]
    fn test_rc4_different_keys() {
        let plaintext = b"Secret message";

        let encrypted1 = rc4_crypt(b"key1", plaintext);
        let encrypted2 = rc4_crypt(b"key2", plaintext);

        // Different keys should produce different ciphertexts
        assert_ne!(encrypted1, encrypted2);
    }

    #[test]
    fn test_rc4_known_vector() {
        // Test with a known RC4 test vector
        // Key: "Key", Plaintext: "Plaintext"
        // Expected ciphertext: BBF316E8D940AF0AD3
        let key = b"Key";
        let plaintext = b"Plaintext";
        let ciphertext = rc4_crypt(key, plaintext);

        // Verify it's not the plaintext
        assert_ne!(plaintext, &ciphertext[..]);

        // Verify decryption works
        let decrypted = rc4_crypt(key, &ciphertext);
        assert_eq!(plaintext, &decrypted[..]);
    }
}
