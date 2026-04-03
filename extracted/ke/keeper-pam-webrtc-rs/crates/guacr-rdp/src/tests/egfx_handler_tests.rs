use crate::egfx_handler::{avc_to_annex_b, contains_idr_nal};

#[test]
fn avc_to_annex_b_single_nal() {
    // [0,0,0,3] len=3, [0x67,0x42,0x00] NAL data
    let avc = [0x00, 0x00, 0x00, 0x03, 0x67, 0x42, 0x00];
    let ab = avc_to_annex_b(&avc);
    assert_eq!(&ab[0..4], &[0x00, 0x00, 0x00, 0x01]);
    assert_eq!(&ab[4..], &[0x67, 0x42, 0x00]);
}

#[test]
fn avc_to_annex_b_empty() {
    assert!(avc_to_annex_b(&[]).is_empty());
}

#[test]
fn contains_idr_detects_type5() {
    let annex_b = [0x00, 0x00, 0x00, 0x01, 0x65]; // NAL type 5 = IDR
    assert!(contains_idr_nal(&annex_b));
}

#[test]
fn contains_idr_rejects_non_idr() {
    let annex_b = [0x00, 0x00, 0x00, 0x01, 0x41]; // NAL type 1 = non-IDR slice
    assert!(!contains_idr_nal(&annex_b));
}
