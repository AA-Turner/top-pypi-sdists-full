use crate::{EncodedFrame, EncoderBackendKind, RgbaFrame, VideoEncoder};
use anyhow::Result;
use bytes::Bytes;
use openh264::{
    encoder::{
        BitRate, Encoder, EncoderConfig, FrameRate, FrameType, IntraFramePeriod, RateControlMode,
        UsageType,
    },
    formats::{RgbSliceU8, YUVBuffer},
    OpenH264API,
};

pub struct OpenH264Encoder {
    encoder: Encoder,
    /// Reused RGBA->I420 conversion target. `from_rgb_source` allocated a fresh
    /// YUV buffer (~width*height*1.5 bytes) on every frame; `read_rgb8` converts
    /// into this one in place, so the conversion allocates nothing after startup.
    yuv: YUVBuffer,
    /// Reused alpha-stripped RGB8 staging buffer — see the comment in `encode()` on
    /// why this exists instead of feeding RGBA straight to the YUV conversion.
    rgb_scratch: Vec<u8>,
    width: u32,
    height: u32,
    frame_count: u64,
}

impl OpenH264Encoder {
    pub fn new(width: u32, height: u32) -> Result<Self> {
        let n_threads = (std::thread::available_parallelism().map_or(1, |n| n.get()) as u16).min(4);

        let api = OpenH264API::from_source();
        let config = EncoderConfig::new()
            .usage_type(UsageType::ScreenContentRealTime)
            // Scaled to frame size — a fixed rate starves large desktops. See
            // crate::initial_bitrate_bps. BWE adapts from here via set_target_bitrate.
            .bitrate(BitRate::from_bps(crate::initial_bitrate_bps(
                width, height, 30,
            )))
            // RateControlMode::Bitrate + skip_frames(true): openh264 itself warns that
            // bitrate control does not function in Quality/Bitrate/Timestamp RC modes
            // without skip_frames enabled. Measured live on a Precision 5540 (2026-08-04)
            // with the crate's previous defaults (Quality mode, skip_frames(false)): 3.5-5x
            // target bitrate overshoot regardless of resolution or content — both
            // `initial_bitrate_bps`'s pixel-scaled target and BWE's `set_target_bitrate`
            // were largely decorative. A tuning sweep confirmed this combination costs
            // nothing in fps (native 3292x1724: 7.1-7.3fps range either way) while
            // FFmpeg/NVENC, which already tracks its target within ~10%, was the
            // comparison point for "actually works".
            .rate_control_mode(RateControlMode::Bitrate)
            .skip_frames(true)
            .max_frame_rate(FrameRate::from_hz(30.0))
            .debug(false)
            .num_threads(n_threads)
            .intra_frame_period(IntraFramePeriod::from_num_frames(150));

        let mut encoder = Encoder::with_api_config(api, config)
            .map_err(|e| anyhow::anyhow!("openh264 init failed: {}", e))?;

        // SM_FIXEDSLCNUM_SLICE enables parallel macroblock encoding.
        // EncoderConfig always sets SM_SINGLE_SLICE which prevents per-MB parallelism.
        // Override via raw API; uiSliceNum=0 auto-matches slice count to thread count.
        if n_threads > 1 {
            use openh264_sys2::{
                SEncParamExt, ENCODER_OPTION_SVC_ENCODE_PARAM_EXT, SM_FIXEDSLCNUM_SLICE,
            };
            // SAFETY: EncoderRawAPI is Send+Sync (openh264 crate asserts this).
            // ENCODER_OPTION_SVC_ENCODE_PARAM_EXT expects *mut SEncParamExt.
            // params is stack-allocated and exclusively owned by this block.
            unsafe {
                let raw = encoder.raw_api();
                let mut params = SEncParamExt::default();
                raw.get_option(
                    ENCODER_OPTION_SVC_ENCODE_PARAM_EXT,
                    (&raw mut params).cast(),
                );
                params.sSpatialLayers[0].sSliceArgument.uiSliceMode = SM_FIXEDSLCNUM_SLICE;
                params.sSpatialLayers[0].sSliceArgument.uiSliceNum = 0;
                raw.set_option(
                    ENCODER_OPTION_SVC_ENCODE_PARAM_EXT,
                    (&raw mut params).cast(),
                );
            }
        }

        Ok(Self {
            encoder,
            yuv: YUVBuffer::new(width as usize, height as usize),
            rgb_scratch: vec![0u8; (width as usize) * (height as usize) * 3],
            width,
            height,
            frame_count: 0,
        })
    }
}

impl VideoEncoder for OpenH264Encoder {
    fn encode(&mut self, frame: &RgbaFrame) -> Result<EncodedFrame> {
        let expected = (self.width * self.height * 4) as usize;
        anyhow::ensure!(
            frame.data.len() == expected,
            "expected {} RGBA bytes for {}x{}, got {}",
            expected,
            self.width,
            self.height,
            frame.data.len()
        );

        // Strip alpha into the reused RGB8 scratch buffer, then use openh264's `read_rgb8`
        // (integer, chunked — the crate's own docs call it "the faster version... you
        // should generally use this one") instead of `read_rgb` (per-pixel `pixel_f32`
        // float conversion), which is what this used to call directly on RGBA.
        // Measured on a Precision 5540 (2026-08-04), real desktop-shaped content at the
        // current 1918x1004 RDP encode clamp: 23.5 -> 52.0 fps. At native 3292x1724 the
        // conversion was the dominant per-frame cost, not H.264 mode decision — neither
        // thread count nor encoder complexity moved fps at all, while this change alone
        // roughly doubled it (7.6 -> 16.5 fps). Both paths use the same BT.601-derived
        // coefficients (0.2578125*256=66, 0.50390625*256=129, 0.09765625*256=25), so this
        // is not a quality tradeoff, only a faster equivalent conversion.
        for (dst, src) in self
            .rgb_scratch
            .as_chunks_mut::<3>()
            .0
            .iter_mut()
            .zip(frame.data.as_chunks::<4>().0.iter())
        {
            dst[0] = src[0];
            dst[1] = src[1];
            dst[2] = src[2];
        }
        let rgb = RgbSliceU8::new(
            &self.rgb_scratch,
            (self.width as usize, self.height as usize),
        );
        self.yuv.read_rgb8(rgb);

        let bitstream = self
            .encoder
            .encode(&self.yuv)
            .map_err(|e| anyhow::anyhow!("openh264 encode failed: {}", e))?;

        let is_keyframe = matches!(bitstream.frame_type(), FrameType::IDR | FrameType::I);
        let pts = self.frame_count * 3000;
        self.frame_count += 1;

        Ok(EncodedFrame {
            data: Bytes::from(bitstream.to_vec()),
            is_keyframe,
            pts,
        })
    }

    fn request_keyframe(&mut self) {
        self.encoder.force_intra_frame();
    }

    fn set_target_bitrate(&mut self, bps: u32) {
        use openh264_sys2::{SBitrateInfo, ENCODER_OPTION_BITRATE, SPATIAL_LAYER_ALL};
        // SAFETY: ENCODER_OPTION_BITRATE expects *mut SBitrateInfo.
        // info is stack-allocated and exclusively owned by this call.
        unsafe {
            let mut info = SBitrateInfo {
                iLayer: SPATIAL_LAYER_ALL,
                iBitrate: bps.min(i32::MAX as u32) as i32,
            };
            self.encoder
                .raw_api()
                .set_option(ENCODER_OPTION_BITRATE, (&raw mut info).cast());
        }
    }

    fn frame_count(&self) -> u64 {
        self.frame_count
    }

    fn dimensions(&self) -> (u32, u32) {
        (self.width, self.height)
    }

    fn backend_kind(&self) -> EncoderBackendKind {
        EncoderBackendKind::Software
    }
}

impl OpenH264Encoder {
    /// Address of the RGB8 scratch buffer's backing storage. Test-only observability —
    /// unchanged across `encode()` calls proves the buffer is reused, not reallocated
    /// per frame.
    #[cfg(test)]
    pub(crate) fn rgb_scratch_ptr(&self) -> *const u8 {
        self.rgb_scratch.as_ptr()
    }
}
