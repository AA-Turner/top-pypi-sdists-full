use statsig_id_list_ef::{encode_prefix_v1, packed, validate_v1};

#[test]
fn id_list_codec_counts_duplicate_raw_records_and_stops_before_the_tail() {
    let mut bytes = b"+AAAAAAAA\n".repeat(1001);
    bytes.extend_from_slice(b"+////////\n-AAAAAAAA\n+BBBBBBBB\n");
    let (raw_end, image) = encode_prefix_v1(&bytes, 0).unwrap().unwrap();
    assert_eq!(raw_end, 10020);
    let ef = validate_v1(&image).unwrap();
    assert_eq!(ef.count, 2);
    assert!(ef.contains(&image, 0));
    assert!(ef.contains(&image, (1 << 48) - 1));
    assert!(!ef.contains(&image, 1));
    for cut in 0..image.len() {
        assert!(validate_v1(&image[..cut]).is_err());
    }
    let mut invalid = image.clone();
    invalid[8] = 1;
    assert!(validate_v1(&invalid).is_err());
    assert!(encode_prefix_v1(&bytes[16..], 0).unwrap().is_none());
    let ranks: Vec<_> = (0..2048u64)
        .map(|i| (i * 0x9e37_79b9_7f4b) & ((1 << 48) - 1))
        .collect();
    let mut raw = Vec::new();
    for rank in &ranks {
        raw.push(b'+');
        raw.extend_from_slice(&packed::encode(*rank));
        raw.push(b'\n');
    }
    raw.extend_from_slice(b"+partial");
    let (end, image) = encode_prefix_v1(&raw, 0).unwrap().unwrap();
    assert_eq!(end, ranks.len() * 10);
    let ef = validate_v1(&image).unwrap();
    assert!(ranks.iter().all(|r| ef.contains(&image, *r)));
}

#[test]
fn duplicate_heavy_input_stops_at_the_scratch_limit_with_a_raw_byte_cursor() {
    use statsig_id_list_ef::{MAX_PREFIX_RECORDS, RECORD_BYTES};
    let mut raw = b"+AAAAAAAA\n".repeat(MAX_PREFIX_RECORDS);
    raw.extend_from_slice(b"+BBBBBBBB\n");
    let (end, image) = encode_prefix_v1(&raw, 0).unwrap().unwrap();
    assert_eq!(end, MAX_PREFIX_RECORDS * RECORD_BYTES);
    assert_eq!(&raw[end..], b"+BBBBBBBB\n");
    assert_eq!(validate_v1(&image).unwrap().count, 1);
}
