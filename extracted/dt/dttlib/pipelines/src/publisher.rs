use crate::PipelineError;
use crate::publisher::MaybeInitialized::Initialized;
use std::marker::PhantomData;
use tokio::sync::mpsc::error::SendError;
use tokio::sync::oneshot;
use tokio::sync::{mpsc, watch};
use user_messages::UserMsgProvider;

/// sequentially publish values from the input channel to
/// A publisher will not really start running until all Subscriber structs have been dropped!
/// it first waits for subscriptions.  When all Subscriber structs have been dropped,
/// it stops looking for Subscriptions (there can't be any more), and starts running.
///
/// The publisher also dies if *any* of the subscribers close their ends.  This is meant for
/// easy cleanup of a fixed set of pipelines.  The whole set can be cleaned up by closing a single pipeline
/// at any point
pub struct Publisher<T> {
    input_sender: mpsc::Sender<T>,
}

impl<T: Clone + Sync + Send + 'static> Publisher<T> {
    pub async fn send(&self, value: T) -> Result<(), SendError<T>> {
        self.input_sender.send(value).await
    }

    pub fn create(queue_size: usize) -> (Self, Subscriber<T>) {
        let (tx, rx) = mpsc::channel(queue_size);
        let (stx, srx) = mpsc::channel(1);
        let publisher = Publisher { input_sender: tx };
        let subscriber = Subscriber {
            sender: stx,
            phantom_data: PhantomData,
        };
        tokio::spawn(run_publisher(srx, rx, queue_size));
        (publisher, subscriber)
    }
}

/// read the input and send
/// to all subscribed outputs
/// Doesn't allow disconnections.
/// quits immediately if either the input closes
/// or *any* subscriber closes.
async fn run_publisher<T: Clone + Sync + Send + 'static>(
    mut subscription_receiver: mpsc::Receiver<PublisherSender<T>>,
    mut input_receiver: mpsc::Receiver<T>,
    queue_size: usize,
) {
    let mut outputs: Vec<mpsc::Sender<T>> = Vec::new();

    let mut output_watch = None;

    // get subscriptions first
    while let Some(sender) = subscription_receiver.recv().await {
        match sender {
            PublisherSender::Subscribe(sendback) => {
                let (tx, rx) = mpsc::channel(queue_size);
                outputs.push(tx);
                sendback.send(rx).unwrap_or(());
            }
            PublisherSender::UnsyncSubscribe(sendback) => {
                let (tx, rx) = watch::channel(MaybeInitialized::Uninitialized);
                output_watch = Some(tx);
                sendback.send(rx).unwrap_or(());
            }
        }
    }

    // start reading input
    while let Some(data) = input_receiver.recv().await {
        let spawn_joins: Vec<_> = outputs
            .clone()
            .into_iter()
            .map(|c| {
                let d = data.clone();
                tokio::spawn(async move { c.send(d).await })
            })
            .collect();
        for spawn_join in spawn_joins.into_iter() {
            let result = spawn_join.await;
            if result.is_err() {
                break;
            }
        }
        if let Some(w) = output_watch.as_ref() {
            if w.send(data.into()).is_err() {
                break;
            };
        }
    }
}

enum PublisherSender<T: Clone> {
    Subscribe(oneshot::Sender<mpsc::Receiver<T>>),
    UnsyncSubscribe(oneshot::Sender<watch::Receiver<MaybeInitialized<T>>>),
}

#[derive(Debug, Clone)]
pub struct Subscriber<T: Clone> {
    sender: mpsc::Sender<PublisherSender<T>>,
    phantom_data: PhantomData<T>,
}

/// represents an uninitialized value in watch channel
/// separate from Option because option runs into trait implementation conflicts with Pipedata elsewhere
#[derive(Clone)]
pub enum MaybeInitialized<T: Clone> {
    Uninitialized,
    Initialized(T),
}

impl<T: Clone> From<T> for MaybeInitialized<T> {
    fn from(value: T) -> Self {
        Initialized(value)
    }
}

impl<T: Clone> Subscriber<T> {
    /// Subscribe to the given publisher
    /// When publishers start publishing, they first close their subscription channel.
    /// An Err(()) return means the subscription channel was already closed.
    pub async fn subscribe(&self) -> Result<mpsc::Receiver<T>, PipelineError> {
        let (tx, rx) = oneshot::channel();
        self.sender
            .send(PublisherSender::Subscribe(tx))
            .await
            .map_err(|_| PipelineError::Subscription("Couldn't send subscription request"))?;
        rx.await
            .map_err(|_| PipelineError::Subscription("Never received subscription"))
    }

    /// Get a subscription or just kill the task
    /// We should always get a subscription unless something is drastically wrong elsewhere
    /// In that case, there's nothing to do but log a message and abort the test.
    pub async fn subscribe_or_die(&self, rc: Box<dyn UserMsgProvider>) -> mpsc::Receiver<T> {
        match self.subscribe().await {
            Ok(i) => i,
            Err(_) => {
                let msg = "Couldn't subscribe to upstream pipeline";
                rc.user_message_handle().error(msg.to_string());
                panic!("{}", msg);
            }
        }
    }

    /// use a watch channel instead of a mpsc.  This subscriber is not
    /// guaranteed to get ever output of the publisher
    /// but will always eventually get the last output.
    pub async fn unsync_subscribe(
        &self,
    ) -> Result<watch::Receiver<MaybeInitialized<T>>, PipelineError> {
        let (tx, rx) = oneshot::channel();
        self.sender
            .send(PublisherSender::UnsyncSubscribe(tx))
            .await
            .map_err(|_| {
                PipelineError::Subscription("Couldn't send unsync subscription request")
            })?;
        rx.await
            .map_err(|_| PipelineError::Subscription("Never received unsync subscription"))
    }

    /// Get a subscription to a non-synchronized output or just kill the task
    /// We should always get a subscription unless something is drastically wrong elsewhere
    /// In that case, there's nothing to do but log a message and abort the test.
    pub async fn unsync_subscribe_or_die(
        &self,
        rc: Box<dyn UserMsgProvider>,
    ) -> watch::Receiver<MaybeInitialized<T>> {
        match self.unsync_subscribe().await {
            Ok(i) => i,
            Err(_) => {
                let msg = "Couldn't subscribe to upstream pipeline";
                rc.user_message_handle().error(msg.to_string());
                panic!("{}", msg);
            }
        }
    }
}
