// FileSink: writes an encrypted fMP4 recording to a local file.

use crate::encryptor::Encryptor;
use crate::{Fmp4Writer, RecorderError, RecordingSink, Result, VideoRecordingConfig};
use async_trait::async_trait;
use guacr_handlers::EncodedFrame;
use log::{debug, warn};
use std::path::PathBuf;
use tokio::fs::File;
use tokio::io::AsyncWriteExt;

pub struct FileSink {
    file: File,
    encryptor: Option<Encryptor>,
    muxer: Fmp4Writer,
    pending_events: Vec<(u64, String)>,
    session_start_ms: u64,
}

impl FileSink {
    pub async fn new(config: VideoRecordingConfig, path: PathBuf) -> Result<Self> {
        if let Some(parent) = path.parent() {
            tokio::fs::create_dir_all(parent).await?;
        }

        let mut file = File::create(&path).await?;

        // Write the unencrypted header (metadata + nonce) before ciphertext
        let header = config.header_bytes();
        file.write_all(&header).await?;

        let encryptor = Encryptor::new(
            &config.recording_secret,
            &config.recording_nonce,
            &config.recording_associated,
        )
        .map_err(|e: String| RecorderError::Encryption(e))?;

        let session_start_ms = std::time::SystemTime::now()
            .duration_since(std::time::UNIX_EPOCH)
            .unwrap_or_default()
            .as_millis() as u64;

        debug!("FileSink: recording to {:?}", path);
        Ok(Self {
            file,
            encryptor: Some(encryptor),
            muxer: Fmp4Writer::new(1920, 1080),
            pending_events: Vec::new(),
            session_start_ms,
        })
    }

    /// Encrypt `data` in-place and write to file — zero extra allocation.
    async fn write_encrypted(&mut self, mut data: Vec<u8>) -> Result<()> {
        self.encryptor
            .as_mut()
            .expect("encryptor used after finalize")
            .update_in_place(&mut data);
        self.file.write_all(&data).await?;
        Ok(())
    }
}

#[async_trait]
impl RecordingSink for FileSink {
    async fn write_frame(&mut self, frame: &EncodedFrame) -> Result<()> {
        if !self.muxer.is_initialized() {
            if !frame.is_keyframe {
                return Ok(());
            }
            match self.muxer.init_segment(&frame.data) {
                Some(init) => self.write_encrypted(init).await?,
                None => {
                    warn!("FileSink: could not extract SPS/PPS from first IDR, dropping");
                    return Ok(());
                }
            }
        }

        if !self.pending_events.is_empty() {
            let events = std::mem::take(&mut self.pending_events);
            let data_frag = self.muxer.write_data_fragment(&events);
            if !data_frag.is_empty() {
                self.write_encrypted(data_frag).await?;
            }
        }

        let pts = frame.pts;
        let is_keyframe = frame.is_keyframe;
        if let Some(mp4_frame) = self.muxer.prepare_frame(&frame.data, pts, is_keyframe) {
            let video_frag = self.muxer.write_video_fragment(&mp4_frame);
            self.write_encrypted(video_frag).await?;
        }

        Ok(())
    }

    async fn write_input(&mut self, instruction: &str, timestamp_ms: u64) -> Result<()> {
        let relative_ms = timestamp_ms.saturating_sub(self.session_start_ms);
        self.pending_events
            .push((relative_ms, instruction.to_string()));
        Ok(())
    }

    async fn finalize(mut self: Box<Self>) -> Result<()> {
        if !self.pending_events.is_empty() {
            let events = std::mem::take(&mut self.pending_events);
            let data_frag = self.muxer.write_data_fragment(&events);
            if !data_frag.is_empty() {
                self.write_encrypted(data_frag).await?;
            }
        }

        let tag = self
            .encryptor
            .take()
            .expect("encryptor already consumed")
            .finalize();
        self.file.write_all(&tag).await?;
        self.file.flush().await?;

        debug!("FileSink: finalized");
        Ok(())
    }
}
