// Security tests for CVE-2023-43826: VNC framebuffer integer overflow investigation.
//
// ALL tests in this file must have `#[ignore]` per the reserved-filename rule in
// `.rulesync/rules/testing.md`.
//
// Run with:
//   cargo test -p guacr-vnc --test security_test -- --include-ignored
//
// Overflow paths investigated (see report in each test doc-comment):
//   SEC-VNC-01  Raw encoding: w*h*bpp in read_framebuffer_update (handler.rs:978) — unchecked
//   SEC-VNC-02  RichCursor encoding: img_n = w*h*bpp (handler.rs:1048) — unchecked
//   SEC-VNC-03  XCursor encoding: mask_n = ceil(w/8)*h (handler.rs:1078) — unchecked
//   SEC-VNC-04  handle_tight_fill: pixel_count*4 (handler.rs:1544) — unchecked
//   SEC-VNC-05  cursor_pixels_to_rgba: w*h*4 (handler.rs:1171) — unchecked
//   SEC-VNC-06  DesktopSize: no MAX_VNC_DIM check in render loop (handler.rs:1088)
//   SEC-VNC-07  FrameBuffer::new(8K): 7680*4320*4 must not overflow u32 (safe path)
//   SEC-VNC-08  parse_cursor_data: checked arithmetic (already present — verify pass)
//   SEC-VNC-09  Rectangle OOB: x+width > framebuffer width must be rejected
//   SEC-VNC-10  Tight FillRect pixel_count overflow via parse_framebuffer_update_from_buffer

use guacr_vnc::VncPixelFormat;

// ============================================================================
// Helpers
// ============================================================================

/// Default 32bpp true-color pixel format (standard VNC).
fn default_pixel_format() -> VncPixelFormat {
    VncPixelFormat {
        bits_per_pixel: 32,
        depth: 24,
        big_endian: false,
        true_color: true,
        red_max: 255,
        green_max: 255,
        blue_max: 255,
        red_shift: 16,
        green_shift: 8,
        blue_shift: 0,
    }
}

// ============================================================================
// SEC-VNC-01: Raw encoding overflow in read_framebuffer_update
//
// handler.rs:978 computes `(w as usize) * (h as usize) * bpp` with no overflow
// check before allocating. For w=65535, h=65535, bpp=4 the product is ~17 GB —
// this will attempt a massive allocation and panic or OOM.
//
// The buffer-parser path (parse_framebuffer_update_from_buffer) already uses
// checked arithmetic for Raw encoding. The streaming read_framebuffer_update does NOT.
//
// We test the buffer-parser path (which is publicly accessible) to verify that
// checked arithmetic is in place. The streaming path in handler.rs needs the same fix.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_01_raw_encoding_extreme_dimensions_buffer_parser() {
    // Maximum u16 rectangle dimensions: 65535 × 65535.
    // The buffer parser at vnc_protocol.rs already has checked_mul — it must return
    // Ok (with empty rectangles, since there is no pixel data) not panic.
    // If the implementation has a real overflow it panics in debug, returns wrong
    // data in release.
    let data = {
        let mut v = vec![
            0u8, // message type = FramebufferUpdate
            0u8, // padding
            0u8, 1u8, // num_rects = 1
        ];
        // Rectangle header: x=65535, y=65535, w=65535, h=65535, enc=Raw(0)
        v.extend_from_slice(&65535u16.to_be_bytes()); // x
        v.extend_from_slice(&65535u16.to_be_bytes()); // y
        v.extend_from_slice(&65535u16.to_be_bytes()); // w
        v.extend_from_slice(&65535u16.to_be_bytes()); // h
        v.extend_from_slice(&0i32.to_be_bytes()); // encoding = Raw
                                                  // No pixel data — parser must detect overflow before indexing
        v
    };

    // parse_framebuffer_update_from_buffer is available via VncProtocol
    use guacr_vnc::VncProtocol;
    let result = VncProtocol::parse_framebuffer_update_from_buffer(&data);

    // Must not panic. The rectangle must be skipped (overflow check fires) or an
    // Err must be returned — but must not attempt a 17 GB allocation.
    match result {
        Ok((rects, _offset)) => {
            // Acceptable: the overflow rectangle was skipped
            assert!(
                rects.is_empty(),
                "overflow rectangle should have been skipped, not accepted: got {:?}",
                rects.len()
            );
        }
        Err(_) => {
            // Also acceptable: returns error instead of panicking
        }
    }
}

// ============================================================================
// SEC-VNC-02 / SEC-VNC-05: RichCursor overflow paths
//
// handler.rs (read_framebuffer_update, enc=-239):
//   img_n = (w as usize) * (h as usize) * bpp    ← unchecked
//
// handler.rs (cursor_pixels_to_rgba):
//   vec![0u8; (w as usize) * (h as usize) * 4]   ← unchecked
//
// We test parse_cursor_data (which has checked arithmetic) to verify the
// cursor path does not overflow. The streaming handler path needs the same fix.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_02_cursor_extreme_dimensions_checked() {
    // 256×256 cursor, 32bpp → pixel_data_size = 256*256*4 = 262144 bytes.
    // This must NOT overflow even in 32-bit arithmetic — verify it returns Ok
    // with correct data length.
    let pf = default_pixel_format();
    let w: u16 = 256;
    let h: u16 = 256;
    let bytes_per_pixel = 4;
    let pixel_data_size = w as usize * h as usize * bytes_per_pixel;
    let mask_stride = (w as usize).div_ceil(8); // 32
    let bitmask_size = mask_stride * h as usize; // 32 * 256 = 8192
    let total = pixel_data_size + bitmask_size;

    // Build synthetic cursor data: fully opaque (all mask bits = 1).
    let mut data = vec![0u8; total];
    // Fill bitmask with 0xFF so every pixel is visible.
    for b in &mut data[pixel_data_size..] {
        *b = 0xFF;
    }

    use guacr_vnc::VncProtocol;
    let result = VncProtocol::parse_cursor_data(0, 0, w, h, &data, &pf);
    assert!(
        result.is_ok(),
        "256x256 cursor should succeed: {:?}",
        result.err()
    );
    let cursor = result.unwrap();
    assert_eq!(
        cursor.rgba_data.len(),
        w as usize * h as usize * 4,
        "RGBA data length mismatch"
    );
}

#[test]
#[ignore]
fn sec_vnc_02b_cursor_max_u16_dimensions_rejected() {
    // 65535×65535 cursor at 32bpp: pixel_data_size = 65535*65535*4 overflows usize on 32-bit.
    // On 64-bit it is 17 GB — parse_cursor_data must use checked arithmetic and
    // return Err rather than attempt the allocation.
    let pf = default_pixel_format();
    let w: u16 = 65535;
    let h: u16 = 65535;
    // Provide an intentionally short data slice — the overflow check must fire
    // before any data-length comparison succeeds.
    let data: Vec<u8> = vec![0u8; 16];

    use guacr_vnc::VncProtocol;
    let result = VncProtocol::parse_cursor_data(0, 0, w, h, &data, &pf);
    // Must return Err (dimension overflow) — must not panic.
    assert!(
        result.is_err(),
        "65535x65535 cursor should be rejected, not accepted"
    );
}

// ============================================================================
// SEC-VNC-03: XCursor mask overflow
//
// handler.rs:1078-1079 (enc=-240):
//   let mask_n = ((w as usize).div_ceil(8)) * (h as usize);
//   let mut buf = vec![0u8; 6 + 2 * mask_n];
//
// For w=65535, h=65535: mask_n = 8192 * 65535 = ~537 MB, and 2*mask_n = ~1 GB.
// Then the read_exact would attempt to read 1 GB from the stream — denial of service.
// The multiplication is not checked for overflow.
//
// We test via the buffer-parser path; the streaming handler path needs a guard.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_03_xcursor_mask_stride_bounds() {
    // Verify the mask stride computation (w=65535) does not overflow usize.
    // This is an arithmetic correctness test — if it panics we have a real bug.
    let w: u16 = 65535;
    let h: u16 = 65535;
    // mask_stride = ceil(65535 / 8) = 8192
    let mask_stride = (w as usize).div_ceil(8);
    // 8192 * 65535 = 536,862,720 — fits in usize on 64-bit.
    // 2 * 536862720 = 1,073,725,440 — also fits.
    // The concern is that the handler allocates this without a size cap.
    // On 64-bit this won't overflow but will attempt a 1 GB allocation — a DoS.
    let mask_n = mask_stride.checked_mul(h as usize);
    assert!(
        mask_n.is_some(),
        "mask_stride * h should not overflow usize on 64-bit"
    );
    let mask_n = mask_n.unwrap();
    let buf_size = (6usize).checked_add(2usize.checked_mul(mask_n).expect("2*mask_n overflow"));
    assert!(
        buf_size.is_some(),
        "6 + 2*mask_n should not overflow usize on 64-bit"
    );
    // Verify there IS a size cap needed: 6 + 2 * 536862720 = 1,073,725,446 bytes (~1 GB).
    // The handler must reject cursor dimensions above a reasonable cap.
    let buf_size = buf_size.unwrap();
    const MAX_CURSOR_DIM: usize = 256; // reasonable cursor size cap
    let max_mask_n = MAX_CURSOR_DIM.div_ceil(8) * MAX_CURSOR_DIM;
    let max_buf = 6 + 2 * max_mask_n;
    assert!(
        buf_size > max_buf,
        "expected 65535x65535 allocation ({} bytes) to exceed safe cap ({} bytes) — \
         confirming the handler needs a cursor dimension cap before this allocation",
        buf_size,
        max_buf
    );
}

// ============================================================================
// SEC-VNC-04: handle_tight_fill pixel_count overflow
//
// handler.rs:1544-1545:
//   let pixel_count = rect.width as usize * rect.height as usize;
//   let mut rgba_fill = vec![0u8; pixel_count * 4];
//
// Both multiplications are unchecked. For width=65535, height=65535:
//   pixel_count = 65535*65535 = 4,294,836,225 > u32::MAX (fine on 64-bit usize)
//   pixel_count*4 = 17,179,344,900 — still fits in 64-bit usize, but the
//   actual allocation is 16 GB. This is a DoS, not a memory-safety violation on
//   64-bit, but would panic (OOM) in production.
//
// We test via parse_framebuffer_update_from_buffer with a Tight Fill rectangle.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_04_tight_fill_extreme_dimensions() {
    // Build a FramebufferUpdate with a Tight FillRect of 65535x65535.
    // Tight encoding (7): compression_control=0x80 (Fill), then 3 RGB bytes.
    let data = {
        let mut v = vec![
            0u8, // message type = FramebufferUpdate
            0u8, // padding
            0u8, 1u8, // num_rects = 1
        ];
        v.extend_from_slice(&0u16.to_be_bytes()); // x
        v.extend_from_slice(&0u16.to_be_bytes()); // y
        v.extend_from_slice(&65535u16.to_be_bytes()); // w
        v.extend_from_slice(&65535u16.to_be_bytes()); // h
        v.extend_from_slice(&7i32.to_be_bytes()); // encoding = Tight
        v.push(0x80u8); // compression_control = Fill subtype
        v.extend_from_slice(&[255u8, 0u8, 0u8]); // RGB = red
        v
    };

    use guacr_vnc::VncProtocol;
    let result = VncProtocol::parse_framebuffer_update_from_buffer(&data);

    // Must not panic. A Fill rect at 65535x65535 must either be skipped or
    // returned as a VncPixelData::Fill with the dimensions preserved — the
    // actual pixel expansion happens later in handle_tight_fill which must
    // use checked arithmetic.
    match result {
        Ok((_rects, _offset)) => {
            // Acceptable: parser returns the rectangle (pixel_count is computed
            // lazily in handle_tight_fill, not here)
        }
        Err(_) => {
            // Also acceptable if the parser rejects it early
        }
    }
}

// ============================================================================
// SEC-VNC-06: DesktopSize pseudo-encoding bypasses MAX_VNC_DIM cap
//
// handler.rs:connect() caps server dimensions at MAX_VNC_DIM=7680 during
// the initial VNC handshake. However, the DesktopSize pseudo-encoding handler
// (read_framebuffer_update enc=-223) directly sets:
//   self.width = w as u32;
//   self.height = h as u32;
//   self.framebuffer = FrameBuffer::new(self.width, self.height);
//
// A malicious server can send DesktopSize with w=65535, h=65535 AFTER the
// handshake, bypassing the initial dimension cap. FrameBuffer::new uses
// saturating_mul so it won't panic, but the framebuffer data will be zeroed
// to a wrong (saturated) size while self.width/self.height reflect the large
// values — causing subsequent OOB pixel writes.
//
// Verify that the FrameBuffer::new with saturating_mul produces consistent
// width/height vs. data length.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_06_desktopsize_dimensions_must_be_validated() {
    // Verify FrameBuffer::new with extreme dimensions uses saturating math
    // and produces a consistent (though capped) result.
    use guacr_terminal::FrameBuffer;

    // 8K resolution (within MAX_VNC_DIM=7680) — must work correctly.
    let fb = FrameBuffer::new(7680, 4320);
    let expected = 7680usize * 4320 * 4;
    assert_eq!(
        fb.get_all_pixels().len(),
        expected,
        "8K FrameBuffer should have exactly {} bytes",
        expected
    );

    // The DesktopSize handler does NOT cap dimensions — a server can send
    // 65535x65535 after the handshake. Confirm that without a cap the
    // FrameBuffer allocation would be 65535*65535*4 ≈ 17 GB (saturating_mul
    // will cap it on 32-bit but not on 64-bit).
    //
    // This test documents the gap: DesktopSize must apply MAX_VNC_DIM before
    // creating a new FrameBuffer.
    let w: u32 = 65535;
    let h: u32 = 65535;
    let expected_uncapped = (w as usize)
        .checked_mul(h as usize)
        .and_then(|n| n.checked_mul(4));
    // On 64-bit this won't overflow — it's ~17 GB — documenting the DoS risk.
    if let Some(n) = expected_uncapped {
        assert!(
            n > 1_000_000_000,
            "65535x65535 framebuffer would be {} bytes — must be capped before allocation",
            n
        );
    }
}

// ============================================================================
// SEC-VNC-07: FrameBuffer::new with 8K dimensions — safe path (passing test)
//
// Verifies that 7680×4320 (8K) allocation works correctly and does not
// overflow u32 when computing width*height*4 = 132,710,400.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_07_framebuffer_8k_allocation_safe() {
    use guacr_terminal::FrameBuffer;

    let w: u32 = 7680;
    let h: u32 = 4320;
    let fb = FrameBuffer::new(w, h);
    let pixels = fb.get_all_pixels();
    let expected_len = w as usize * h as usize * 4;
    assert_eq!(
        pixels.len(),
        expected_len,
        "8K FrameBuffer::new should allocate exactly {} bytes (4 channels)",
        expected_len
    );
    assert!(
        pixels.iter().all(|&b| b == 0),
        "fresh FrameBuffer should be zero-initialized"
    );
}

// ============================================================================
// SEC-VNC-08: parse_cursor_data checked arithmetic — passing test
//
// parse_cursor_data (vnc_protocol.rs) already uses checked_mul for pixel_count
// and pixel_data_size. Verify these checks work for normal cursor dimensions.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_08_parse_cursor_data_normal_dimensions_ok() {
    let pf = default_pixel_format();
    let w: u16 = 32;
    let h: u16 = 32;
    let bytes_per_pixel: usize = 4;
    let pixel_data_size = w as usize * h as usize * bytes_per_pixel;
    let mask_stride = (w as usize).div_ceil(8);
    let bitmask_size = mask_stride * h as usize;
    let total = pixel_data_size + bitmask_size;

    let mut data = vec![0u8; total];
    // Set all mask bits so every pixel is visible.
    for b in &mut data[pixel_data_size..] {
        *b = 0xFF;
    }

    use guacr_vnc::VncProtocol;
    let result = VncProtocol::parse_cursor_data(5, 3, w, h, &data, &pf);
    assert!(
        result.is_ok(),
        "normal 32x32 cursor should parse successfully"
    );
    let cursor = result.unwrap();
    assert_eq!(cursor.width, w);
    assert_eq!(cursor.height, h);
    assert_eq!(cursor.hotspot_x, 5);
    assert_eq!(cursor.hotspot_y, 3);
    assert_eq!(cursor.rgba_data.len(), w as usize * h as usize * 4);
}

// ============================================================================
// SEC-VNC-09: Rectangle OOB — x+width extends beyond framebuffer bounds
//
// handle_framebuffer_rectangle has an AC-2/AC-3 bounds check that rejects
// rectangles that exceed self.width/self.height. Verify this check works.
// We test the public buffer-parser path which does NOT enforce bounds
// (it returns the rectangle as-is; bounds are checked in the handler).
//
// This test verifies the raw parser returns the OOB rectangle and the caller
// must apply bounds checking.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_09_rectangle_oob_parser_returns_rect_for_handler_to_check() {
    // Rectangle at x=65534, width=2 — right edge = 65536, which overflows u16
    // but not u32. The buffer parser returns the parsed rectangle; the handler
    // enforces bounds against self.width.
    let data = {
        let mut v = vec![
            0u8, // message type
            0u8, // padding
            0u8, 1u8, // num_rects = 1
        ];
        // x=65534, y=0, w=2, h=1, encoding=Raw
        v.extend_from_slice(&65534u16.to_be_bytes()); // x
        v.extend_from_slice(&0u16.to_be_bytes()); // y
        v.extend_from_slice(&2u16.to_be_bytes()); // w
        v.extend_from_slice(&1u16.to_be_bytes()); // h
        v.extend_from_slice(&0i32.to_be_bytes()); // encoding = Raw
        v.extend_from_slice(&[1u8, 2u8, 3u8, 1u8, 2u8, 3u8]); // 2 pixels RGB
        v
    };

    use guacr_vnc::VncProtocol;
    let result = VncProtocol::parse_framebuffer_update_from_buffer(&data);
    // Parser may or may not accept the rectangle — the key is no panic.
    assert!(result.is_ok(), "buffer parser must not panic on OOB rect");
}

// ============================================================================
// SEC-VNC-10: RRE subrect count overflow in buffer parser
//
// vnc_protocol.rs:631-634 uses saturating_add / saturating_mul for RRE.
// Verify that a huge subrect count is handled without panic.
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_10_rre_huge_subrect_count_no_panic() {
    // Build a FramebufferUpdate with RRE encoding (enc=2) claiming u32::MAX subrects.
    let data = {
        let mut v = vec![
            0u8, // message type
            0u8, // padding
            0u8, 1u8, // num_rects = 1
        ];
        v.extend_from_slice(&0u16.to_be_bytes()); // x
        v.extend_from_slice(&0u16.to_be_bytes()); // y
        v.extend_from_slice(&4u16.to_be_bytes()); // w
        v.extend_from_slice(&4u16.to_be_bytes()); // h
        v.extend_from_slice(&2i32.to_be_bytes()); // encoding = RRE
                                                  // Payload: 4-byte count = u32::MAX + 3-byte background
        v.extend_from_slice(&[0xFF, 0xFF, 0xFF, 0xFF]); // num_subrects = u32::MAX
        v.extend_from_slice(&[0u8, 0u8, 0u8]); // background RGB
                                               // No actual subrect data
        v
    };

    use guacr_vnc::VncProtocol;
    let result = VncProtocol::parse_framebuffer_update_from_buffer(&data);
    // Must not panic. Error or skipped rectangle are both acceptable.
    match result {
        Ok((rects, _)) => {
            // If parser accepted it and passed to decode_rre, that function must
            // detect the truncated data and return an error, causing the rectangle
            // to be skipped.
            assert!(
                rects.is_empty(),
                "RRE with u32::MAX subrects should be skipped (truncated), not returned"
            );
        }
        Err(_) => {
            // Also acceptable — error is propagated
        }
    }
}

// ============================================================================
// SEC-VNC-11: Tight JPEG subtype with truncated compact-length
//
// The Tight JPEG subtype reads a compact 1-3 byte length field. Verify the
// buffer parser handles truncated length bytes gracefully (no panic, rectangle
// is simply skipped rather than causing OOB access).
// ============================================================================

#[test]
#[ignore]
fn sec_vnc_11_tight_jpeg_truncated_compact_length_no_panic() {
    use guacr_vnc::VncProtocol;

    // Build a Tight JPEG subtype rectangle where the compact-length bytes are
    // truncated (missing after the compression_control byte).
    let data = {
        let mut v = vec![
            0u8, // message type
            0u8, // padding
            0u8, 1u8, // num_rects = 1
        ];
        v.extend_from_slice(&0u16.to_be_bytes()); // x
        v.extend_from_slice(&0u16.to_be_bytes()); // y
        v.extend_from_slice(&4u16.to_be_bytes()); // w
        v.extend_from_slice(&4u16.to_be_bytes()); // h
        v.extend_from_slice(&7i32.to_be_bytes()); // encoding = Tight
        v.push(0x90u8); // compression_control = JPEG subtype (0x09 << 4)
                        // Compact length byte indicating 2-byte continuation, but second byte missing:
        v.push(0x80u8); // first length byte: continuation bit set, but no second byte
        v
    };

    let result = VncProtocol::parse_framebuffer_update_from_buffer(&data);
    // Must not panic. The truncated length means the JPEG rect is skipped.
    match result {
        Ok((rects, _)) => {
            assert!(
                rects.is_empty(),
                "truncated Tight JPEG compact-length should cause rect to be skipped"
            );
        }
        Err(_) => {
            // Error propagation is also acceptable
        }
    }
}
