use statsig_rust::hashing::HashUtil;

#[test]
fn test_evaluation_hash_matches_sha256_prefix() {
    let hasher = HashUtil::new();

    // expect first 8 bytes of SHA-256 digest as big-endian u64:
    assert_eq!(
        hasher.evaluation_hash(&"".to_string()).unwrap(),
        0xE3B0C44298FC1C14_u64
    );
    assert_eq!(
        hasher.evaluation_hash(&"blargh".to_string()).unwrap(),
        0x0AC33512D18E20D5_u64
    );
    assert_eq!(
        hasher.evaluation_hash(&"unicode 🗻".to_string()).unwrap(),
        0xD460740C12959D83_u64
    );
}

#[test]
fn test_string_hash_uses_padded_base64_and_encoded_prefix() {
    let hasher = HashUtil::new();
    let input = "unicode 🗻";
    let expected = "1GB0DBKVnYM8Xt/rahVuF8DyatT9CpoErSZrWkK1ZrQ=";

    assert_eq!(hasher.sha256(input), expected);
    assert_eq!(
        hasher.hash(input, &statsig_rust::hashing::HashAlgorithm::Sha256),
        expected
    );
    assert_eq!(
        hasher.sha256_to_u64(input),
        u64::from_be_bytes(*b"1GB0DBKV")
    );
}
