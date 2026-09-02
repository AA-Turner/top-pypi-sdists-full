use crate::text_optimized::TextProtocolEncoder;

#[test]
fn test_format_img_instruction() {
    let mut encoder = TextProtocolEncoder::new();
    let instr = encoder.format_img_instruction(1, 0, 10, 20, "image/jpeg");

    let instr_str = String::from_utf8_lossy(&instr);
    assert!(instr_str.contains("img"));
    assert!(instr_str.contains("image/jpeg"));
}

#[test]
fn test_format_blob_instruction() {
    let mut encoder = TextProtocolEncoder::new();
    let base64_data = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==";
    let instr = encoder.format_blob_instruction(1, base64_data);

    let instr_str = String::from_utf8_lossy(&instr);
    assert!(instr_str.contains("blob"));
    assert!(instr_str.contains(base64_data));
}
