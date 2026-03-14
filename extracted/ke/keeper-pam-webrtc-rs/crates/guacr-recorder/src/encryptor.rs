// Streaming AES-256-GCM encryptor compatible with Python's StreamEncryptor.
//
// Python uses:
//   encryptor = Cipher(AES(key), GCM(nonce)).encryptor()
//   encryptor.authenticate_additional_data(aad)
//   ct_chunk = encryptor.update(plaintext_chunk)   # repeatable
//   final_bytes = encryptor.finalize()              # remaining + 16-byte tag
//
// AES-256-GCM construction:
//   H       = AES_K(0^128)             (GHASH subkey)
//   J0      = nonce || 0x00000001      (pre-counter)
//   E_K(J0) = AES_K(J0)               (encrypted J0, used to compute final tag)
//   CTR     = Ctr32BE starting at nonce || 0x00000002  (J0+1)
//
//   ciphertext = plaintext XOR CTR_keystream
//   GHASH chain: [AAD padded to 16B] → [ciphertext padded to 16B] → [8B len_aad_bits || 8B len_ct_bits]
//   S = GHASH_result
//   tag = S XOR E_K(J0)  (16 bytes)

use aes::cipher::generic_array::GenericArray;
use aes::cipher::{BlockEncrypt, KeyInit, KeyIvInit, StreamCipher};
use aes::Aes256;
use ctr::Ctr32BE;
use ghash::universal_hash::UniversalHash;
use ghash::GHash;

pub struct Encryptor {
    ctr: Ctr32BE<Aes256>,
    ghash: StreamGhash,
    encrypted_j0: [u8; 16],
    aad_len: u64,
    ct_len: u64,
}

impl Encryptor {
    /// Create a new streaming encryptor.
    ///
    /// * `key`  — 32-byte AES-256 key
    /// * `nonce` — 12-byte GCM nonce
    /// * `aad`  — associated data (authenticated, not encrypted)
    pub fn new(key: &[u8], nonce: &[u8], aad: &[u8]) -> Result<Self, String> {
        if key.len() != 32 {
            return Err(format!("key must be 32 bytes, got {}", key.len()));
        }
        if nonce.len() != 12 {
            return Err(format!("nonce must be 12 bytes, got {}", nonce.len()));
        }

        // H = AES_K(0^128)
        let block_cipher =
            Aes256::new_from_slice(key).map_err(|e| format!("AES key init failed: {}", e))?;
        let mut h_block: GenericArray<u8, _> = GenericArray::default();
        block_cipher.encrypt_block(&mut h_block);
        let h: [u8; 16] = {
            let mut arr = [0u8; 16];
            arr.copy_from_slice(h_block.as_slice());
            arr
        };

        // E_K(J0) where J0 = nonce || 0x00000001
        let mut j0 = [0u8; 16];
        j0[..12].copy_from_slice(nonce);
        j0[12..16].copy_from_slice(&1u32.to_be_bytes());
        let mut j0_block: GenericArray<u8, _> = j0.into();
        block_cipher.encrypt_block(&mut j0_block);
        let encrypted_j0: [u8; 16] = {
            let mut arr = [0u8; 16];
            arr.copy_from_slice(j0_block.as_slice());
            arr
        };

        // CTR stream starts at J0+1 = nonce || 0x00000002
        let mut ctr_iv = [0u8; 16];
        ctr_iv[..12].copy_from_slice(nonce);
        ctr_iv[12..16].copy_from_slice(&2u32.to_be_bytes());
        let ctr: Ctr32BE<Aes256> =
            KeyIvInit::new_from_slices(key, &ctr_iv).map_err(|e| format!("CTR init: {}", e))?;

        // GHASH: process AAD first, then pad, then CT will follow
        let mut ghash = StreamGhash::new(&h);
        ghash.update(aad);
        let aad_len = aad.len() as u64;
        ghash.pad_to_block(); // pad AAD to 16-byte boundary

        Ok(Self {
            ctr,
            ghash,
            encrypted_j0,
            aad_len,
            ct_len: 0,
        })
    }

    /// Encrypt plaintext in-place. The buffer is XORed with the CTR keystream and
    /// GHASH-authenticated. No allocation — caller owns the buffer.
    pub fn update_in_place(&mut self, buf: &mut [u8]) {
        self.ctr.apply_keystream(buf);
        self.ghash.update(buf);
        self.ct_len += buf.len() as u64;
    }

    /// Encrypt a chunk of plaintext. Returns ciphertext of the same length.
    /// Prefer `update_in_place` when the caller already owns a mutable buffer.
    pub fn update(&mut self, plaintext: &[u8]) -> Vec<u8> {
        let mut ct = plaintext.to_vec();
        self.update_in_place(&mut ct);
        ct
    }

    /// Finalize: compute and return the 16-byte GCM authentication tag.
    /// All plaintext must have been passed through `update` before calling this.
    pub fn finalize(mut self) -> [u8; 16] {
        // Pad ciphertext to 16-byte boundary
        self.ghash.pad_to_block();

        // Process length block: 8-byte BE len_aad_bits || 8-byte BE len_ct_bits
        let mut len_block = [0u8; 16];
        len_block[..8].copy_from_slice(&(self.aad_len * 8).to_be_bytes());
        len_block[8..].copy_from_slice(&(self.ct_len * 8).to_be_bytes());
        let block: ghash::Block = len_block.into();
        self.ghash.inner.update(core::slice::from_ref(&block));

        // S = GHASH result
        let output = self.ghash.inner.finalize();
        let mut s = [0u8; 16];
        s.copy_from_slice(output.as_slice());

        // Tag = S XOR E_K(J0)
        let mut tag = [0u8; 16];
        for i in 0..16 {
            tag[i] = s[i] ^ self.encrypted_j0[i];
        }
        tag
    }
}

// ---------------------------------------------------------------------------
// StreamGhash: feeds arbitrary-length data into GHASH one 16-byte block at a time
// ---------------------------------------------------------------------------

pub(crate) struct StreamGhash {
    pub(crate) inner: GHash,
    buf: [u8; 16],
    buf_len: usize,
}

impl StreamGhash {
    pub(crate) fn new(h_key: &[u8; 16]) -> Self {
        let key: ghash::Key = (*h_key).into();
        Self {
            inner: GHash::new(&key),
            buf: [0u8; 16],
            buf_len: 0,
        }
    }

    pub(crate) fn update(&mut self, data: &[u8]) {
        let mut pos = 0;
        while pos < data.len() {
            let space = 16 - self.buf_len;
            let take = space.min(data.len() - pos);
            self.buf[self.buf_len..self.buf_len + take].copy_from_slice(&data[pos..pos + take]);
            self.buf_len += take;
            pos += take;
            if self.buf_len == 16 {
                let block: ghash::Block = self.buf.into();
                self.inner.update(core::slice::from_ref(&block));
                self.buf = [0u8; 16];
                self.buf_len = 0;
            }
        }
    }

    /// Flush any partial block (zero-padded) to complete a logical boundary (AAD or CT).
    pub(crate) fn pad_to_block(&mut self) {
        if self.buf_len > 0 {
            // buf[buf_len..] is already zero (reset on each full-block flush)
            let block: ghash::Block = self.buf.into();
            self.inner.update(core::slice::from_ref(&block));
            self.buf = [0u8; 16];
            self.buf_len = 0;
        }
    }
}
