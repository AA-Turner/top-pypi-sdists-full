use crate::transport::{
    ChannelRecordingTransport, FileRecordingTransport, MultiTransportRecorder, RecordingTransport,
};

// Buffered actual sinks commit their pending tail during finalization.
struct Buffered<T: RecordingTransport> {
    file: T,
    pending: Vec<u8>,
}

#[async_trait::async_trait]
impl<T: RecordingTransport> RecordingTransport for Buffered<T> {
    async fn write(&mut self, data: &[u8]) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        self.pending.extend_from_slice(data);
        Ok(())
    }
    async fn flush(&mut self) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        self.file.write(&self.pending).await?;
        self.file.flush().await?;
        self.pending.clear();
        Ok(())
    }
    async fn finalize(&mut self) -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
        self.flush().await
    }
}

#[cfg(target_os = "linux")]
#[tokio::test(flavor = "current_thread")]
async fn failing_sink_finalize_still_flushes_later_actual_file() {
    let dir = tempfile::TempDir::new().unwrap();
    let path = dir.path().join("tail.h264");
    let failing = Buffered {
        file: FileRecordingTransport::new(std::path::Path::new("/dev/full")).unwrap(),
        pending: b"unwritable".to_vec(),
    };
    let tail = b"\0\0\0\x01\x65accepted-recording-tail";
    let surviving = Buffered {
        file: FileRecordingTransport::new(&path).unwrap(),
        pending: tail.to_vec(),
    };
    let mut recorder = MultiTransportRecorder::new();
    recorder.add_transport(Box::new(failing));
    recorder.add_transport(Box::new(surviving));
    let error = recorder.finalize().await.expect_err("first sink must fail");
    assert_eq!(
        error
            .downcast_ref::<std::io::Error>()
            .unwrap()
            .raw_os_error(),
        Some(28)
    );
    assert!(
        error.to_string().contains("space"),
        "original /dev/full error: {error}"
    );
    assert_eq!(std::fs::read(&path).unwrap(), tail);
}

#[tokio::test(flavor = "current_thread")]
async fn closed_channel_finalize_still_commits_later_actual_file() {
    let dir = tempfile::TempDir::new().unwrap();
    let path = dir.path().join("tail.h264");
    let (sender, receiver) = tokio::sync::mpsc::channel(1);
    drop(receiver);
    let failing = Buffered {
        file: ChannelRecordingTransport::new(sender),
        pending: b"unwritable".to_vec(),
    };
    let tail = b"\0\0\0\x01\x65accepted-recording-tail";
    let surviving = Buffered {
        file: FileRecordingTransport::new(&path).unwrap(),
        pending: tail.to_vec(),
    };
    let mut recorder = MultiTransportRecorder::new();
    recorder.add_transport(Box::new(failing));
    recorder.add_transport(Box::new(surviving));
    let error = recorder
        .finalize()
        .await
        .expect_err("closed first sink must fail");
    assert_eq!(
        error.downcast_ref::<std::io::Error>().unwrap().kind(),
        std::io::ErrorKind::BrokenPipe
    );
    assert_eq!(std::fs::read(&path).unwrap(), tail);
}
