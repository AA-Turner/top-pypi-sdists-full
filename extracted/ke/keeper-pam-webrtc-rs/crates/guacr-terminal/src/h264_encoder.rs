use bytes::Bytes;
use openh264::{
    encoder::{BitRate, Encoder, EncoderConfig, FrameType, IntraFramePeriod, UsageType},
    formats::{RgbaSliceU8, YUVBuffer},
    OpenH264API,
};

pub struct SoftwareH264Encoder {
    encoder: Encoder,
    width: u32,
    height: u32,
    frame_count: u64,
}

impl SoftwareH264Encoder {
    pub fn new(width: u32, height: u32) -> anyhow::Result<Self> {
        let api = OpenH264API::from_source();
        let config = EncoderConfig::new()
            .usage_type(UsageType::ScreenContentRealTime)
            .bitrate(BitRate::from_bps(2_000_000))
            .skip_frames(false)
            .debug(false)
            .intra_frame_period(IntraFramePeriod::from_num_frames(150));
        let encoder = Encoder::with_api_config(api, config)
            .map_err(|e| anyhow::anyhow!("openh264 encoder init failed: {}", e))?;

        Ok(Self {
            encoder,
            width,
            height,
            frame_count: 0,
        })
    }

    /// Encode a full-framebuffer RGBA frame.
    ///
    /// Returns `(annex_b_bytes, is_keyframe)`. Call with `force_keyframe = true`
    /// when a PLI arrives from the browser. Periodic IDR frames are handled
    /// automatically by the encoder via the `intra_frame_period` config.
    pub fn encode_rgba(
        &mut self,
        pixels: &[u8],
        force_keyframe: bool,
    ) -> anyhow::Result<(Bytes, bool)> {
        let expected = (self.width * self.height * 4) as usize;
        if pixels.len() != expected {
            anyhow::bail!(
                "expected {} bytes for {}x{} RGBA, got {}",
                expected,
                self.width,
                self.height,
                pixels.len()
            );
        }

        if force_keyframe {
            self.encoder.force_intra_frame();
        }

        let rgba = RgbaSliceU8::new(pixels, (self.width as usize, self.height as usize));
        let yuv = YUVBuffer::from_rgb_source(rgba);

        let bitstream = self
            .encoder
            .encode(&yuv)
            .map_err(|e| anyhow::anyhow!("openh264 encode failed: {}", e))?;

        let is_keyframe = matches!(bitstream.frame_type(), FrameType::IDR | FrameType::I);
        let data = Bytes::from(bitstream.to_vec());

        self.frame_count += 1;

        Ok((data, is_keyframe))
    }

    /// No-op: openh264 0.9.x does not expose a public dynamic bitrate API on the
    /// high-level `Encoder`. The initial 2 Mbps target and the encoder's own rate
    /// control handle adaptation.
    pub fn update_bitrate(&mut self, _bps: u32) {}

    pub fn frame_count(&self) -> u64 {
        self.frame_count
    }
}
