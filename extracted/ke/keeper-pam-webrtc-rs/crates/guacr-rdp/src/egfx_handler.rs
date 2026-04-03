// EGFX passthrough handler: intercepts H.264 PDUs from the MS-RDPEGFX DVC channel
// and queues them for direct delivery to RTCRtpSender.
//
// The Windows GPU encoder embeds H.264 bitstreams in WireToSurface1 PDUs with
// codec_id Avc420 or Avc444. Under the new ironrdp-egfx API, the pipeline parses
// the bitmap streams and calls our H264Decoder::decode() with the raw AVC payload.
// We convert AVC → Annex B and queue the frame for WebRTC while returning a
// zero-pixel dummy DecodedFrame so the pipeline can complete its bookkeeping
// without actually rendering anything (on_bitmap_updated is a no-op since the
// client receives H.264 via the WebRTC video track, not Guacamole img instructions).
//
// Architecture:
//   EgfxPassthroughHandler  - GraphicsPipelineHandler: tracks surface dimensions,
//                             suppresses decoded-pixel rendering.
//   PassthroughH264Decoder  - H264Decoder: captures AVC frames for WebRTC.
//
// Both share `frames`, `egfx_active`, and `surface_dims` via Arc.
// `surface_dims` is an AtomicU64 with width packed in the high 32 bits and
// height in the low 32 bits. The decoder reads it to size the dummy DecodedFrame
// so the pipeline's size check (frame >= dest_rect) passes.

use crossbeam_queue::ArrayQueue;
use ironrdp_egfx::client::{GraphicsPipelineHandler, Surface};
use ironrdp_egfx::decode::{DecodedFrame, DecoderError, DecoderResult, H264Decoder};
use ironrdp_egfx::pdu::{CapabilitiesV81Flags, CapabilitiesV8Flags, CapabilitySet};
use log::{debug, trace};
use std::sync::atomic::{AtomicBool, Ordering};
use std::sync::Arc;

/// A single H.264 frame extracted from EGFX, ready for WebRTC delivery.
pub struct H264Frame {
    /// Complete Annex B bitstream (00 00 00 01 prefixed NAL units).
    pub data: Vec<u8>,
    /// True if the stream contains an IDR NAL unit (NAL type 5).
    pub is_keyframe: bool,
}

/// EGFX GraphicsPipelineHandler.
///
/// on_bitmap_updated is a no-op and wants_decoded_bitmap returns false: we send
/// H.264 directly over the WebRTC video track so decoded pixels are never needed.
pub struct EgfxPassthroughHandler;

/// H264Decoder implementation that captures AVC frames for WebRTC passthrough.
pub struct PassthroughH264Decoder {
    frames: Arc<ArrayQueue<H264Frame>>,
    egfx_active: Arc<AtomicBool>,
}

impl EgfxPassthroughHandler {
    /// Creates both the handler and its paired decoder. Pass the decoder to
    /// `GraphicsPipelineClient::new(handler, Some(Box::new(decoder)))`.
    pub fn new(
        frames: Arc<ArrayQueue<H264Frame>>,
        egfx_active: Arc<AtomicBool>,
    ) -> (Self, PassthroughH264Decoder) {
        (
            Self,
            PassthroughH264Decoder {
                frames,
                egfx_active,
            },
        )
    }
}

impl GraphicsPipelineHandler for EgfxPassthroughHandler {
    fn capabilities(&self) -> Vec<CapabilitySet> {
        // Advertise V8.1 AVC420 so the Windows GPU encoder activates.
        // V8 is included as a fallback for servers that don't support V8.1.
        vec![
            CapabilitySet::V8_1 {
                flags: CapabilitiesV81Flags::AVC420_ENABLED | CapabilitiesV81Flags::SMALL_CACHE,
            },
            CapabilitySet::V8 {
                flags: CapabilitiesV8Flags::SMALL_CACHE,
            },
        ]
    }

    fn on_surface_created(&mut self, surface: &Surface) {
        debug!(
            "EGFX: Surface {} created {}x{}",
            surface.id, surface.width, surface.height
        );
    }

    fn wants_decoded_bitmap(&self) -> bool {
        // We forward H.264 over the WebRTC video track. Decoded RGBA pixels are
        // never used, so opt out to skip crop+callback and save two allocations
        // per frame.
        false
    }
}

impl H264Decoder for PassthroughH264Decoder {
    /// Called by the pipeline with the raw AVC payload from a WireToSurface1 PDU.
    /// The pipeline has already parsed Avc420BitmapStream; `data` is the H.264 NAL
    /// units in AVC format (4-byte BE length prefix per NAL unit).
    fn decode(&mut self, data: &[u8]) -> DecoderResult<DecodedFrame> {
        let annex_b = avc_to_annex_b(data);

        if annex_b.is_empty() {
            return Err(DecoderError::msg(
                "empty AVC payload after Annex B conversion",
            ));
        }

        let data_len = annex_b.len();
        let is_keyframe = contains_idr_nal(&annex_b);
        let frame = H264Frame {
            data: annex_b,
            is_keyframe,
        };

        let _ = self.frames.force_push(frame);
        self.egfx_active.store(true, Ordering::Release);

        trace!(
            "EGFX: Queued H.264 frame ({} bytes, keyframe={})",
            data_len,
            is_keyframe
        );

        // The handler sets wants_decoded_bitmap() = false, so the pipeline skips
        // the size check and crop entirely after decode() returns. Return a
        // zero-allocation empty frame — the pixel data is never read.
        Ok(DecodedFrame {
            data: Vec::new(),
            width: 0,
            height: 0,
        })
    }

    fn reset(&mut self) {
        self.egfx_active.store(false, Ordering::Release);
    }
}

// ---------------------------------------------------------------------------
// Internal helpers
// ---------------------------------------------------------------------------

/// Convert an AVC (length-prefixed) bitstream to Annex B (start-code prefixed).
///
/// AVC:     [4-byte BE length][NAL data][4-byte BE length][NAL data]...
/// Annex B: [00 00 00 01][NAL data][00 00 00 01][NAL data]...
pub(crate) fn avc_to_annex_b(avc: &[u8]) -> Vec<u8> {
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
pub(crate) fn contains_idr_nal(annex_b: &[u8]) -> bool {
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
