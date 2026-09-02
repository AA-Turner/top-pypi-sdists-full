use crate::egfx_handler::{avc_to_annex_b, contains_idr_nal, EgfxPassthroughHandler, H264Frame};
use crossbeam_queue::ArrayQueue;
use ironrdp_egfx::decode::H264Decoder;
use ironrdp_egfx::pdu::Codec1Type;
use std::sync::atomic::AtomicBool;
use std::sync::Arc;

fn make_handler_and_decoder(
    capacity: usize,
) -> (
    EgfxPassthroughHandler,
    crate::egfx_handler::PassthroughH264Decoder,
    Arc<crossbeam_queue::ArrayQueue<crate::egfx_handler::ClearCodecFrame>>,
    Arc<ArrayQueue<H264Frame>>,
) {
    let frames = Arc::new(ArrayQueue::new(capacity));
    let (handler, decoder, cc) =
        EgfxPassthroughHandler::new(Arc::clone(&frames), Arc::new(AtomicBool::new(false)));
    (handler, decoder, cc, frames)
}

/// One AVC-format NAL unit (4-byte BE length prefix) with a distinguishing marker
/// byte, so tests can tell queued frames apart. `nal_header` picks IDR vs delta.
fn avc_frame(nal_header: u8, marker: u8) -> Vec<u8> {
    vec![0x00, 0x00, 0x00, 0x02, nal_header, marker]
}

fn delta(marker: u8) -> Vec<u8> {
    avc_frame(0x41, marker) // NAL type 1 = non-IDR slice
}

fn keyframe(marker: u8) -> Vec<u8> {
    avc_frame(0x65, marker) // NAL type 5 = IDR
}

fn make_decoder(
    capacity: usize,
) -> (
    crate::egfx_handler::PassthroughH264Decoder,
    Arc<ArrayQueue<H264Frame>>,
) {
    let frames = Arc::new(ArrayQueue::new(capacity));
    let (handler, decoder, _cc) =
        EgfxPassthroughHandler::new(Arc::clone(&frames), Arc::new(AtomicBool::new(false)));
    // Default surface size so decode() doesn't Err; queue-behavior tests don't
    // care about frame dimensions, only what the frames queue contains.
    handler.set_surface_dims_for_test(1920, 1080);
    (decoder, frames)
}

/// Marker byte of each queued frame, oldest first.
fn queued_markers(q: &ArrayQueue<H264Frame>) -> Vec<u8> {
    let mut out = Vec::new();
    while let Some(f) = q.pop() {
        // Annex B: 00 00 00 01 <nal_header> <marker>
        out.push(f.data[5]);
    }
    out
}

/// An IDR is self-contained, so it is a free resync point: the stale backlog is
/// dropped rather than delivered ahead of it.
#[test]
fn keyframe_flushes_the_backlog() {
    let (mut decoder, frames) = make_decoder(4);
    decoder.decode(&delta(1)).unwrap();
    decoder.decode(&delta(2)).unwrap();
    assert_eq!(frames.len(), 2);

    decoder.decode(&keyframe(9)).unwrap();

    assert_eq!(
        queued_markers(&frames),
        vec![9],
        "a keyframe must replace the queued backlog, not join it"
    );
}

/// The original bug: `force_push` evicted the OLDEST queued frame, so the consumer
/// decoded frame N+1 straight after N-1. That breaks the H.264 reference chain and
/// the picture stays corrupt until the next IDR — which on the passthrough path the
/// RDP server controls, not us. Dropping the newest instead keeps the queued
/// sequence contiguous and decodable.
#[test]
fn full_queue_drops_newest_delta_and_keeps_the_chain_intact() {
    let (mut decoder, frames) = make_decoder(2);
    decoder.decode(&delta(1)).unwrap();
    decoder.decode(&delta(2)).unwrap();
    assert_eq!(frames.len(), 2, "queue should be full");

    // Overflow with a third delta frame.
    decoder.decode(&delta(3)).unwrap();

    assert_eq!(
        queued_markers(&frames),
        vec![1, 2],
        "the contiguous queued sequence must survive; the newest frame is the casualty"
    );
}

/// Overflow must not be silent, and must not error out the EGFX channel.
#[test]
fn overflow_is_reported_without_failing_the_channel() {
    let (mut decoder, _frames) = make_decoder(1);
    decoder.decode(&delta(1)).unwrap();
    // Still Ok: a dropped frame is a quality event, not a protocol failure.
    assert!(decoder.decode(&delta(2)).is_ok());
}

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

// ---------------------------------------------------------------------------
// Bug A: H.264 session-fatal crash on first frame (surface_dims not stored)
// ---------------------------------------------------------------------------
//
// IronRDP's decode_avc420 checks: frame.width() < dest_width → Err.
// Without the fix, decode() returns DecodedFrame::new(Vec::new(), 0, 0), so
// 0 < any real dest_width → fatal error on the first frame from a Windows GPU
// RDP server. These tests must FAIL until surface_dims is implemented.

/// Bug A regression: decode() must return a frame at least as large as the surface
/// so IronRDP's size check (frame >= dest_rect) passes on every subsequent frame.
///
/// Surface is #[non_exhaustive]; use the test accessor instead of on_surface_created.
#[test]
fn decode_returns_surface_sized_dummy_frame_after_surface_dims_stored() {
    let (handler, mut decoder, _cc, _frames) = make_handler_and_decoder(4);
    handler.set_surface_dims_for_test(1920, 1080);

    let frame = decoder
        .decode(&keyframe(0x65))
        .expect("decode must succeed after surface dims stored");

    assert!(
        frame.width() >= 1920 && frame.height() >= 1080,
        "frame must be at least surface-sized; got {}×{}",
        frame.width(),
        frame.height()
    );
    assert_eq!(
        frame.data().len(),
        frame.width() as usize * frame.height() as usize * 4,
        "data must be width*height*4 (required by DecodedFrame invariant)"
    );
}

/// Without a prior on_surface_created, decode() must not succeed with a 0×0 frame.
/// decode_avc420 would check 0 < dest_width and return Err, making the zero-pixel
/// frame indistinguishable from a genuine pipeline error. Return our own Err to
/// surface the real cause immediately.
#[test]
fn decode_before_surface_created_returns_err() {
    let (_handler, mut decoder, _cc, _frames) = make_handler_and_decoder(4);
    assert!(
        decoder.decode(&keyframe(0x65)).is_err(),
        "decode before on_surface_created must return Err"
    );
}

/// Server resizes: on_surface_created fires again at the new dimensions.
/// The decoder must update so it doesn't return a frame too small for the new surface.
#[test]
fn surface_dims_update_on_resize() {
    let (handler, mut decoder, _cc, _frames) = make_handler_and_decoder(4);
    handler.set_surface_dims_for_test(1280, 720);
    let frame = decoder.decode(&keyframe(0x65)).unwrap();
    assert!(frame.width() >= 1280 && frame.height() >= 720);

    handler.set_surface_dims_for_test(3840, 2160);
    let frame = decoder.decode(&keyframe(0x65)).unwrap();
    assert!(
        frame.width() >= 3840 && frame.height() >= 2160,
        "must use updated surface dims after resize; got {}×{}",
        frame.width(),
        frame.height()
    );
}

// ---------------------------------------------------------------------------
// Bug B: on_bitmap_updated no-op — non-H.264 bitmaps silently discarded
// ---------------------------------------------------------------------------
//
// IronRDP calls on_bitmap_updated with decoded RGBA data for ClearCodec,
// Planar, and Uncompressed PDUs. The default GraphicsPipelineHandler impl is
// a no-op; without an override, the clearcodec_frames queue is never populated
// and Guacamole img instructions are never sent for those bitmaps.

fn rgba_4x4() -> Vec<u8> {
    vec![0u8; 4 * 4 * 4] // 4×4 RGBA8888
}

/// Bug B regression: a non-H.264 bitmap must appear in clearcodec_frames.
#[test]
fn non_h264_bitmap_is_queued_for_guacamole_delivery() {
    let (mut handler, _decoder, cc, _frames) = make_handler_and_decoder(4);
    handler.route_bitmap_for_test(Codec1Type::Uncompressed, rgba_4x4(), 10, 20, 4, 4);
    assert_eq!(
        cc.len(),
        1,
        "non-H.264 bitmap must be queued in clearcodec_frames"
    );
    let frame = cc.pop().unwrap();
    assert_eq!(frame.x, 10);
    assert_eq!(frame.y, 20);
    assert_eq!(frame.width, 4);
    assert_eq!(frame.height, 4);
    assert_eq!(frame.rgba.len(), 4 * 4 * 4);
}

/// H.264 bitmaps are delivered through H264Decoder::decode(), not on_bitmap_updated.
/// Routing an Avc420 update must leave clearcodec_frames empty.
#[test]
fn h264_bitmap_is_not_queued_in_clearcodec_frames() {
    let (mut handler, _decoder, cc, _frames) = make_handler_and_decoder(4);
    handler.route_bitmap_for_test(Codec1Type::Avc420, rgba_4x4(), 0, 0, 4, 4);
    assert_eq!(cc.len(), 0, "Avc420 must not appear in clearcodec_frames");
    handler.route_bitmap_for_test(Codec1Type::Avc444, rgba_4x4(), 0, 0, 4, 4);
    assert_eq!(cc.len(), 0, "Avc444 must not appear in clearcodec_frames");
}

/// Multiple non-H.264 bitmaps all land in the queue.
#[test]
fn multiple_non_h264_bitmaps_are_all_queued() {
    let (mut handler, _decoder, cc, _frames) = make_handler_and_decoder(4);
    handler.route_bitmap_for_test(Codec1Type::Uncompressed, rgba_4x4(), 0, 0, 4, 4);
    handler.route_bitmap_for_test(Codec1Type::Uncompressed, rgba_4x4(), 4, 0, 4, 4);
    handler.route_bitmap_for_test(Codec1Type::Uncompressed, rgba_4x4(), 8, 0, 4, 4);
    assert_eq!(
        cc.len(),
        3,
        "each non-H.264 bitmap must be individually queued"
    );
}
