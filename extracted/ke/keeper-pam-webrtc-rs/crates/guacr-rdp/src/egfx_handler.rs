// EGFX passthrough handler: intercepts H.264 PDUs from the MS-RDPEGFX DVC channel
// and queues them for direct delivery to RTCRtpSender.
//
// The Windows GPU encoder embeds H.264 bitstreams in WireToSurface1 PDUs with
// codec_id Avc420 or Avc444.  We extract the AVC (length-prefixed) payload,
// convert it to Annex B (start-code prefixed), and push it onto a bounded queue
// that the RDP session loop drains after each ActiveStage::process() call.

use crossbeam_queue::ArrayQueue;
use ironrdp_egfx::client::GraphicsPipelineHandler;
use ironrdp_egfx::pdu::{
    CapabilitiesV81Flags, CapabilitiesV8Flags, CapabilitySet, Codec1Type, GfxPdu,
};
use log::{debug, trace, warn};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

/// A single H.264 frame extracted from EGFX, ready for WebRTC delivery.
pub struct H264Frame {
    /// Complete Annex B bitstream (00 00 00 01 prefixed NAL units).
    pub data: Vec<u8>,
    /// True if the stream contains an IDR NAL unit (NAL type 5).
    pub is_keyframe: bool,
}

/// EGFX handler that intercepts AVC420 / AVC444 H.264 frames from the Windows
/// GPU encoder and queues them for zero-re-encoding delivery to WebRTC.
///
/// Queue capacity is 4.  When full, `force_push` evicts the oldest frame so
/// the WebRTC track always receives the most recent content.
///
/// `egfx_active` is set to `true` on the first successfully queued frame and
/// never reset.  The session uses it to decide whether to suppress the JPEG
/// fallback path: before any EGFX frame arrives (e.g. during capability
/// negotiation, or for servers that never use EGFX such as xrdp), JPEG still
/// runs normally.
pub struct EgfxPassthroughHandler {
    pub frames: Arc<ArrayQueue<H264Frame>>,
    egfx_active: Arc<AtomicBool>,
}

impl EgfxPassthroughHandler {
    pub fn new(frames: Arc<ArrayQueue<H264Frame>>, egfx_active: Arc<AtomicBool>) -> Self {
        Self {
            frames,
            egfx_active,
        }
    }
}

impl GraphicsPipelineHandler for EgfxPassthroughHandler {
    fn capabilities(&self) -> Vec<CapabilitySet> {
        // Advertise V8.1 with AVC420_ENABLED so the Windows server uses its GPU
        // H.264 encoder instead of sending uncompressed or RemoteFX bitmaps.
        // V8 is included as a fallback for servers that do not support V8.1.
        vec![
            CapabilitySet::V8_1 {
                flags: CapabilitiesV81Flags::AVC420_ENABLED | CapabilitiesV81Flags::SMALL_CACHE,
            },
            CapabilitySet::V8 {
                flags: CapabilitiesV8Flags::SMALL_CACHE,
            },
        ]
    }

    fn handle_pdu(&mut self, pdu: GfxPdu) {
        if let GfxPdu::WireToSurface1(w) = pdu {
            let annex_b = match w.codec_id {
                Codec1Type::Avc420 => match avc420_payload(&w.bitmap_data) {
                    Some(avc) => avc_to_annex_b(avc),
                    None => {
                        warn!(
                            "EGFX: Failed to parse Avc420BitmapStream header ({} bytes)",
                            w.bitmap_data.len()
                        );
                        return;
                    }
                },
                Codec1Type::Avc444 | Codec1Type::Avc444v2 => {
                    match avc444_stream1_payload(&w.bitmap_data) {
                        Some(avc) => avc_to_annex_b(avc),
                        None => {
                            warn!(
                                "EGFX: Failed to parse Avc444BitmapStream header ({} bytes)",
                                w.bitmap_data.len()
                            );
                            return;
                        }
                    }
                }
                _ => return,
            };

            if annex_b.is_empty() {
                debug!("EGFX: Empty Annex B frame after AVC conversion, skipping");
                return;
            }

            let data_len = annex_b.len();
            let is_keyframe = contains_idr_nal(&annex_b);
            let frame = H264Frame {
                data: annex_b,
                is_keyframe,
            };
            // Discard oldest frame if queue is full — always prefer latest content.
            let _ = self.frames.force_push(frame);
            // Signal to the session that EGFX is active; the JPEG path will be
            // suppressed from this point forward for this session.
            self.egfx_active.store(true, Ordering::Release);
            trace!(
                "EGFX: Queued H.264 frame ({} bytes, keyframe={})",
                data_len,
                is_keyframe
            );
        }
    }
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/// Extract the raw AVC payload from an `Avc420BitmapStream`.
///
/// Wire format (all integers LE per MS-RDPEGFX §2.2.4.1.1):
///   nRect:      u32
///   rectangles: nRect × InclusiveRectangle (4 × u16 = 8 bytes each)
///   quant_qual: nRect × QuantQuality (2 bytes each)
///   data:       remaining bytes (AVC length-prefixed H.264)
fn avc420_payload(bitmap_data: &[u8]) -> Option<&[u8]> {
    if bitmap_data.len() < 4 {
        return None;
    }
    let n_rect = u32::from_le_bytes([
        bitmap_data[0],
        bitmap_data[1],
        bitmap_data[2],
        bitmap_data[3],
    ]) as usize;
    // InclusiveRectangle: 4 × u16 = 8 bytes.  QuantQuality: 1 byte flags + 1 byte quality = 2 bytes.
    let header = 4 + n_rect * 8 + n_rect * 2;
    if bitmap_data.len() < header {
        return None;
    }
    Some(&bitmap_data[header..])
}

/// Extract the AVC payload from stream1 of an `Avc444BitmapStream`.
///
/// Wire format (MS-RDPEGFX §2.2.4.1.2):
///   streamInfo: u32 LE  (bits 0..30 = stream1 byte length; bits 30..32 = encoding)
///   stream1:    Avc420BitmapStream (stream1_size bytes, or rest-of-data if size == 0)
///   stream2:    optional Avc420BitmapStream
fn avc444_stream1_payload(bitmap_data: &[u8]) -> Option<&[u8]> {
    if bitmap_data.len() < 4 {
        return None;
    }
    let stream_info = u32::from_le_bytes([
        bitmap_data[0],
        bitmap_data[1],
        bitmap_data[2],
        bitmap_data[3],
    ]);
    let stream1_size = (stream_info & 0x3FFF_FFFF) as usize;
    let rest = &bitmap_data[4..];
    let stream1 = if stream1_size == 0 {
        rest
    } else {
        if stream1_size > rest.len() {
            return None;
        }
        &rest[..stream1_size]
    };
    avc420_payload(stream1)
}

/// Convert an AVC (length-prefixed) bitstream to Annex B (start-code prefixed).
///
/// AVC:     [4-byte BE length][NAL data][4-byte BE length][NAL data]...
/// Annex B: [00 00 00 01][NAL data][00 00 00 01][NAL data]...
fn avc_to_annex_b(avc: &[u8]) -> Vec<u8> {
    let mut out = Vec::with_capacity(avc.len() + 16);
    let mut pos = 0;
    while pos + 4 <= avc.len() {
        let len = u32::from_be_bytes([avc[pos], avc[pos + 1], avc[pos + 2], avc[pos + 3]]) as usize;
        pos += 4;
        if len == 0 || pos + len > avc.len() {
            break;
        }
        out.extend_from_slice(&[0x00, 0x00, 0x00, 0x01]);
        out.extend_from_slice(&avc[pos..pos + len]);
        pos += len;
    }
    out
}

/// Returns true if the Annex B stream contains at least one IDR NAL unit
/// (NAL unit type 5, i.e. the low 5 bits of the first byte after the start code).
fn contains_idr_nal(annex_b: &[u8]) -> bool {
    let mut pos = 0;
    while pos + 5 <= annex_b.len() {
        if annex_b[pos..pos + 4] == [0x00, 0x00, 0x00, 0x01] {
            if annex_b[pos + 4] & 0x1f == 5 {
                return true;
            }
            pos += 5;
        } else {
            pos += 1;
        }
    }
    false
}

#[cfg(test)]
mod tests {
    use super::*;

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

    #[test]
    fn avc420_payload_basic() {
        // nRect=0, so header is 4 bytes, rest is AVC data
        let mut data = vec![0x00, 0x00, 0x00, 0x00]; // nRect=0
        data.extend_from_slice(&[0xAA, 0xBB]); // fake AVC data
        assert_eq!(avc420_payload(&data), Some([0xAA, 0xBB].as_ref()));
    }
}
