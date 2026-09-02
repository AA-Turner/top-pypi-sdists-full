use crate::multi_channel::{SimpleMultiChannelSender, WebRTCDataChannel};
use bytes::Bytes;
use std::sync::{
    atomic::{AtomicUsize, Ordering},
    Arc,
};

struct MockChannel {
    sent: Arc<AtomicUsize>,
}

impl WebRTCDataChannel for MockChannel {
    fn send(&self, _data: Bytes) -> Result<(), String> {
        self.sent.fetch_add(1, Ordering::Relaxed);
        Ok(())
    }
}

#[test]
fn test_round_robin() {
    let sent1 = Arc::new(AtomicUsize::new(0));
    let sent2 = Arc::new(AtomicUsize::new(0));
    let sent3 = Arc::new(AtomicUsize::new(0));

    let channels: Vec<Arc<dyn WebRTCDataChannel>> = vec![
        Arc::new(MockChannel {
            sent: sent1.clone(),
        }),
        Arc::new(MockChannel {
            sent: sent2.clone(),
        }),
        Arc::new(MockChannel {
            sent: sent3.clone(),
        }),
    ];

    let sender = SimpleMultiChannelSender::new(channels);

    // Send 3 frames - should round-robin
    for _ in 0..3 {
        sender.send_frame(Bytes::from(vec![0u8; 1000])).unwrap();
    }

    assert_eq!(sent1.load(Ordering::Relaxed), 1);
    assert_eq!(sent2.load(Ordering::Relaxed), 1);
    assert_eq!(sent3.load(Ordering::Relaxed), 1);
}

#[test]
fn test_oversized_frame_dropped() {
    let sent = Arc::new(AtomicUsize::new(0));
    let channels: Vec<Arc<dyn WebRTCDataChannel>> =
        vec![Arc::new(MockChannel { sent: sent.clone() })];

    let sender = SimpleMultiChannelSender::new(channels);

    // Send oversized frame (> 60KB)
    let oversized = Bytes::from(vec![0u8; 100 * 1024]); // 100KB
    sender.send_frame(oversized).unwrap(); // Should drop, not error

    // Should not have sent anything
    assert_eq!(sent.load(Ordering::Relaxed), 0);
}

#[test]
fn test_empty_channels() {
    let channels: Vec<Arc<dyn WebRTCDataChannel>> = vec![];
    let sender = SimpleMultiChannelSender::new(channels);

    let result = sender.send_frame(Bytes::from(vec![0u8; 1000]));
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("No channels"));
}
