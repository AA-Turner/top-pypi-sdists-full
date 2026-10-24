// Read-only viewer for the owner's existing broadcast stream.
// Lag is terminal: Guacamole instructions may be deltas, not replaceable full frames.

use bytes::Bytes;
use log::{info, warn};
use tokio::sync::{broadcast, mpsc};

use crate::session_sharing::{self, SessionSubscription};

pub struct SessionViewer {
    to_client: mpsc::Sender<Bytes>,
    subscription: SessionSubscription,
    session_id: String,
}

impl SessionViewer {
    /// Subscribe and send the existing cached frame, interruptibly on terminal close.
    /// Returns None if the generation ends or the transport closes during join.
    pub async fn join(session_id: &str, to_client: mpsc::Sender<Bytes>) -> Option<Self> {
        let (mut subscription, last) = {
            let handle = session_sharing::lookup(session_id)?;
            handle.subscribe_viewer()?
        };
        if let Some(last) = last {
            tokio::select! {
                biased;
                _ = subscription.ended.cancelled() => return None,
                result = to_client.send(last) => if result.is_err() { return None; },
            }
        }
        info!("Session viewer joined session {session_id:?}");
        Some(Self {
            to_client,
            subscription,
            session_id: session_id.to_string(),
        })
    }

    /// Stream until end, transport close, or lag; terminal close interrupts blocked sends.
    pub async fn run(mut self) {
        loop {
            let frame = tokio::select! {
                biased;
                _ = self.subscription.ended.cancelled() => return,
                _ = self.to_client.closed() => return,
                frame = self.subscription.rx.recv() => frame,
            };
            match frame {
                Ok(frame) => {
                    tokio::select! {
                        biased;
                        _ = self.subscription.ended.cancelled() => return,
                        result = self.to_client.send(frame) => if result.is_err() { return; },
                    }
                }
                Err(broadcast::error::RecvError::Lagged(n)) => {
                    warn!(
                        "Session viewer failed after losing {n} instructions (session: {:?})",
                        self.session_id
                    );
                    return;
                }
                Err(broadcast::error::RecvError::Closed) => return,
            }
        }
    }

    /// Read-only viewer input is never forwarded to the owner.
    pub fn discard_input(_msg: &Bytes) {}
}
