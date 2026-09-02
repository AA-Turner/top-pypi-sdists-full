// EGFX passthrough handler: intercepts H.264 PDUs from the MS-RDPEGFX DVC channel
// and queues them for direct delivery to RTCRtpSender.
//
// The Windows GPU encoder embeds H.264 bitstreams in WireToSurface1 PDUs with
// codec_id Avc420 or Avc444. Under the new ironrdp-egfx API, the pipeline parses
// the bitmap streams and calls our H264Decoder::decode() with the raw AVC payload.
// We convert AVC → Annex B and queue the frame for WebRTC while returning a
// surface-sized dummy DecodedFrame so IronRDP's size check passes.
//
// Non-H.264 bitmaps (ClearCodec, Planar, Uncompressed) arrive via on_bitmap_updated
// with pre-decoded RGBA data; we queue them in `clearcodec_frames` for the main
// loop to deliver as Guacamole img instructions.
//
// Architecture:
//   EgfxPassthroughHandler  - GraphicsPipelineHandler: tracks surface dimensions,
//                             routes non-H.264 bitmaps to clearcodec_frames.
//   PassthroughH264Decoder  - H264Decoder: captures AVC frames for WebRTC.
//
// Both share `frames`, `egfx_active`, and `surface_dims` via Arc.
// `surface_dims` packs width in the high 32 bits and height in the low 32 bits.
// The decoder reads it to size the dummy DecodedFrame so decode_avc420's size
// check (frame >= dest_rect) passes.

use crossbeam_queue::ArrayQueue;
use ironrdp_egfx::client::{BitmapUpdate, GraphicsPipelineHandler, Surface};
use ironrdp_egfx::decode::{DecodedFrame, DecoderError, DecoderResult, H264Decoder};
use ironrdp_egfx::pdu::{
    CapabilitiesV81Flags, CapabilitiesV8Flags, CapabilitySet, Codec1Type, GfxPdu,
};
use log::{debug, trace, warn};
use std::sync::atomic::{AtomicBool, AtomicU64, Ordering};
use std::sync::Arc;

/// A single H.264 frame extracted from EGFX, ready for WebRTC delivery.
pub struct H264Frame {
    /// Complete Annex B bitstream (00 00 00 01 prefixed NAL units).
    pub data: Vec<u8>,
    /// True if the stream contains an IDR NAL unit (NAL type 5).
    pub is_keyframe: bool,
}

/// A decoded ClearCodec bitmap ready for Guacamole image instruction delivery (T-023 to T-027).
///
/// These bitmaps carry crisp text and UI elements that would be lossy if encoded
/// through the H.264 video path. They are rendered as Guacamole img instructions
/// overlaid on the session display.
pub struct ClearCodecFrame {
    /// RGBA pixel data (4 bytes per pixel, row-major, top-left origin).
    pub rgba: Vec<u8>,
    /// Destination rectangle on the EGFX surface.
    pub x: u16,
    pub y: u16,
    pub width: u32,
    pub height: u32,
}

/// EGFX GraphicsPipelineHandler.
///
/// H.264 frames go directly to the WebRTC video track; `on_bitmap_updated` queues
/// non-H.264 bitmaps (ClearCodec, Planar, Uncompressed) in `clearcodec_frames` for
/// delivery as Guacamole img instructions.
pub struct EgfxPassthroughHandler {
    /// Queue for non-H.264 decoded bitmaps. The main loop drains this and encodes
    /// each as a Guacamole img instruction.
    clearcodec_frames: Arc<ArrayQueue<ClearCodecFrame>>,
    /// Surface dimensions shared with PassthroughH264Decoder.
    /// Packed: width in high 32 bits, height in low 32 bits.
    surface_dims: Arc<AtomicU64>,
}

/// H264Decoder implementation that captures AVC frames for WebRTC passthrough.
pub struct PassthroughH264Decoder {
    frames: Arc<ArrayQueue<H264Frame>>,
    egfx_active: Arc<AtomicBool>,
    /// Surface dimensions shared with EgfxPassthroughHandler.
    /// Packed: width in high 32 bits, height in low 32 bits.
    surface_dims: Arc<AtomicU64>,
    /// Delta frames discarded because the queue was full. Only ever incremented, so
    /// a rising count in the logs points at a consumer that cannot keep up.
    dropped_frames: AtomicU64,
}

impl EgfxPassthroughHandler {
    /// Creates both the handler and its paired decoder. Pass the decoder to
    /// `GraphicsPipelineClient::new(handler, Some(Box::new(decoder)))`.
    ///
    /// The returned `clearcodec_frames` queue is drained by the main RDP loop
    /// and each frame is encoded as a Guacamole image instruction.
    ///
    /// Returns `(handler, decoder, clearcodec_frames)`. In test builds, use
    /// `set_surface_dims_for_test` to simulate `on_surface_created` without
    /// constructing the `#[non_exhaustive]` `Surface` struct.
    pub fn new(
        frames: Arc<ArrayQueue<H264Frame>>,
        egfx_active: Arc<AtomicBool>,
    ) -> (
        Self,
        PassthroughH264Decoder,
        Arc<ArrayQueue<ClearCodecFrame>>,
    ) {
        let clearcodec_frames = Arc::new(ArrayQueue::new(64));
        let surface_dims = Arc::new(AtomicU64::new(0));
        (
            Self {
                clearcodec_frames: Arc::clone(&clearcodec_frames),
                surface_dims: Arc::clone(&surface_dims),
            },
            PassthroughH264Decoder {
                frames,
                egfx_active,
                surface_dims,
                dropped_frames: AtomicU64::new(0),
            },
            clearcodec_frames,
        )
    }

    /// Store surface dimensions without constructing the `#[non_exhaustive]` `Surface`.
    /// Used by unit tests to simulate `on_surface_created`.
    #[cfg(test)]
    pub(crate) fn set_surface_dims_for_test(&self, width: u32, height: u32) {
        let packed = (u64::from(width) << 32) | u64::from(height);
        self.surface_dims.store(packed, Ordering::Release);
    }

    /// Simulate `on_bitmap_updated` without constructing the `#[non_exhaustive]` `BitmapUpdate`.
    /// Mirrors the routing logic exactly: non-H.264 codecs queue a frame, H.264 codecs do not.
    /// Used by unit tests to verify Bug B (on_bitmap_updated routes non-H.264 bitmaps).
    #[cfg(test)]
    pub(crate) fn route_bitmap_for_test(
        &mut self,
        codec_id: Codec1Type,
        rgba: Vec<u8>,
        x: u16,
        y: u16,
        width: u16,
        height: u16,
    ) {
        match codec_id {
            Codec1Type::Avc420 | Codec1Type::Avc444 | Codec1Type::Avc444v2 => {}
            _ => {
                let frame = ClearCodecFrame {
                    rgba,
                    x,
                    y,
                    width: u32::from(width),
                    height: u32::from(height),
                };
                if self.clearcodec_frames.force_push(frame).is_some() {
                    debug!("EGFX: bitmap queue full, old frame displaced");
                }
            }
        }
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
        let packed = (u64::from(surface.width) << 32) | u64::from(surface.height);
        self.surface_dims.store(packed, Ordering::Release);
        debug!(
            "EGFX: Surface {} created {}×{}",
            surface.id, surface.width, surface.height
        );
    }

    /// Routes non-H.264 bitmaps to the clearcodec_frames queue for Guacamole delivery.
    ///
    /// IronRDP decodes ClearCodec, Planar, and Uncompressed PDUs internally and calls
    /// this method with the RGBA8888 result. H.264 (Avc420/Avc444) goes through
    /// H264Decoder::decode() instead and never reaches this path.
    fn on_bitmap_updated(&mut self, update: &BitmapUpdate) {
        match update.codec_id {
            Codec1Type::Avc420 | Codec1Type::Avc444 | Codec1Type::Avc444v2 => {
                // H.264 delivered through H264Decoder::decode(); nothing to do here.
            }
            _ => {
                let dest = &update.destination_rectangle;
                let frame = ClearCodecFrame {
                    rgba: update.data.clone(),
                    x: dest.left,
                    y: dest.top,
                    width: u32::from(update.width),
                    height: u32::from(update.height),
                };
                if self.clearcodec_frames.force_push(frame).is_some() {
                    debug!("EGFX: bitmap queue full, old frame displaced");
                }
                trace!(
                    "EGFX: bitmap {:?} {}×{} at ({}, {})",
                    update.codec_id,
                    update.width,
                    update.height,
                    dest.left,
                    dest.top
                );
            }
        }
    }

    fn on_unhandled_pdu(&mut self, pdu: &GfxPdu) {
        trace!("EGFX: unhandled PDU: {:?}", std::mem::discriminant(pdu));
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

        // Queue policy matters for an inter-coded stream: evicting an already-queued
        // frame (what force_push did) leaves the consumer decoding frame N+1 after
        // N-1, so the reference chain breaks and the picture stays corrupt until the
        // next IDR — which on the passthrough path the RDP *server* controls, not us.
        //
        // A keyframe is self-contained, so it is a free resync point: drop the
        // backlog and start from it. Otherwise, when full, discard the newest delta
        // frame instead of an older one — that keeps the queued sequence contiguous
        // and decodable, trading freshness (recoverable on the next frame) for
        // correctness (not recoverable without an IDR).
        if is_keyframe {
            let mut discarded = 0usize;
            while self.frames.pop().is_some() {
                discarded += 1;
            }
            if discarded > 0 {
                debug!(
                    "EGFX: keyframe resync, dropped {} queued frame(s)",
                    discarded
                );
            }
            let _ = self.frames.push(frame);
        } else if self.frames.push(frame).is_err() {
            let dropped = self.dropped_frames.fetch_add(1, Ordering::Relaxed) + 1;
            warn!(
                "EGFX: frame queue full ({} slots), dropped newest delta frame \
                 (total dropped: {}) — consumer is not keeping up",
                self.frames.capacity(),
                dropped
            );
        }
        self.egfx_active.store(true, Ordering::Release);

        trace!(
            "EGFX: Queued H.264 frame ({} bytes, keyframe={})",
            data_len,
            is_keyframe
        );

        // Return a surface-sized dummy frame so decode_avc420's size check passes:
        //   if frame.width() < dest_width { return Err(...) }
        // With dims=0, 0 < any real dest_width → session-fatal error on first frame.
        // IronRDP still runs crop_decoded_frame and compositor.apply_bitmap on this
        // zeroed buffer before calling on_bitmap_updated (which no-ops for Avc420).
        // That means ~surface_w * surface_h * 4 bytes are allocated and memcpy'd per
        // H.264 frame. Eliminating this requires an upstream skip-bitmap hook in
        // ironrdp-egfx. DecodedFrame::new requires data.len() == w * h * 4.
        let packed = self.surface_dims.load(Ordering::Acquire);
        if packed == 0 {
            return Err(DecoderError::msg(
                "H.264 frame arrived before EGFX surface was created",
            ));
        }
        let w = (packed >> 32) as u32;
        let h = (packed & 0xffff_ffff) as u32;
        Ok(DecodedFrame::new(vec![0u8; (w * h * 4) as usize], w, h))
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
