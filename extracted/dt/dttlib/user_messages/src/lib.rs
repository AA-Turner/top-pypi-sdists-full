//! Store and transmit messages to the user
//! Error messages, warnings, other notifications should be sent with this module
//! Create a UserMessagesHandle and call its methods to create messages.
//!
//! The module keeps track of set messages.  The calling module is expected to clear
//! the message if it's no longer valid.  The user therefore doesn't have to guess if a particular
//! message is still valid.
//! As a convenience, the caller can "notify" a message instead of "set"ing a message.
//! A "notify" sets and immediately clears the same message.
//!
//! The module guarantees that the user is notified at least once if a message was set,
//! even if it was immediately cleared.
//!
//! The module is purely async.  Setting messages is fast.

use std::collections::HashMap;
use std::fmt;
use std::fmt::{Debug, Display, Formatter};
use std::sync::{Arc, Mutex};
use std::time::{Duration, Instant};
use tokio::runtime::Handle;
use tokio::sync::mpsc;
use tokio::time::sleep;

#[cfg(feature = "python")]
use pyo3::{pyclass, pymethods};
#[cfg(all(feature = "python"))]
use pyo3_stub_gen::{
    derive::gen_stub_pyclass, derive::gen_stub_pyclass_complex_enum, derive::gen_stub_pyclass_enum,
    derive::gen_stub_pymethods,
};

/// Is able to send message updates to the application.
/// The application must implement this trait then pass
/// one such while creating a new UserMessageHandle
#[allow(refining_impl_trait)]
pub trait Sender: Sync + Send + 'static {
    fn update_all(&mut self, messages: MessageHash) -> Result<(), String>;
    fn set_message(&mut self, tag: String, msg: UserMessage) -> Result<(), String>;
    fn clear_message(&mut self, tag: &str) -> Result<(), String>;
}

#[derive(Clone, Debug, Copy, PartialEq, PartialOrd)]
#[cfg_attr(all(feature = "python"), gen_stub_pyclass_enum)]
#[cfg_attr(feature = "python", pyclass(eq, eq_int, frozen, ord))]
pub enum Severity {
    Debug,
    Notice,
    ConfigurationWarning, // A possible problem with test setup
    Warning,
    Error,              // A problem that will prevent a test from succeeding
    ConfigurationError, // A problem that will prevent a test from starting
    FatalError,         // A problem fatal to the application.  It will need to be restarted.
    SystemError,
}

impl fmt::Display for Severity {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Severity::Debug => write!(f, "Debug"),
            Severity::Notice => write!(f, "Notice"),
            Severity::ConfigurationWarning => write!(f, "Config. Warning"),
            Severity::Warning => write!(f, "Warning"),
            Severity::Error => write!(f, "Error"),
            Severity::ConfigurationError => write!(f, "Config. Error"),
            Severity::FatalError => write!(f, "Fatal Error"),
            Severity::SystemError => write!(f, "System Error"),
        }
    }
}

#[derive(Clone, Debug)]
#[cfg_attr(all(feature = "python"), gen_stub_pyclass)]
#[cfg_attr(feature = "python", pyclass(frozen, str))]
pub struct UserMessage {
    pub severity: Severity,
    pub message: String,
    #[allow(dead_code)]
    pub time_last_set: Instant,
}

impl Display for UserMessage {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        write!(
            f,
            "UserMessage(severity={}, message={})",
            self.severity, self.message
        )
    }
}

#[cfg(feature = "python")]
#[gen_stub_pymethods]
#[pymethods]
impl UserMessage {
    fn __repr__(&self) -> String {
        format!(
            "UserMessage(severity={}, message={})",
            self.severity, self.message
        )
    }

    #[getter]
    fn severity(&self) -> Severity {
        self.severity
    }

    #[getter]
    fn message(&self) -> String {
        self.message.clone()
    }
}

pub type MessageHash = HashMap<String, UserMessage>;

#[derive(Debug, Clone)]
#[cfg_attr(all(feature = "python"), gen_stub_pyclass_complex_enum)]
#[cfg_attr(feature = "python", pyclass(frozen, str))]
pub enum MessageJob {
    SetMessage { tag: String, msg: UserMessage },
    ClearMessage { tag: String },
}

impl Display for MessageJob {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        match self {
            MessageJob::SetMessage { tag, msg } => write!(f, "SetMessage({}, {})", tag, msg),
            MessageJob::ClearMessage { tag } => write!(f, "ClearMessage({})", tag),
        }
    }
}

#[cfg_attr(all(feature = "python"), gen_stub_pymethods)]
#[cfg_attr(feature = "python", pymethods)]
impl MessageJob {
    /// Helps with sorting messages without having to match on them first
    pub fn get_tag(&self) -> &str {
        match self {
            MessageJob::SetMessage { tag, .. } | MessageJob::ClearMessage { tag } => tag,
        }
    }
}

/// This class tracks messages to the user.
/// When a message is set, it is displayed at least once to the user
/// even if it is cleared before the user sees it.
///
/// Messages that are set but not cleared will appear in a list of messages
/// e.g., if a gui wants to display all extant notifications constantly
struct UserMessenger {
    messages: MessageHash,
    receiver: mpsc::Receiver<MessageJob>,
    output_sender: Box<dyn Sender>,
}

impl UserMessenger {
    /// set a message from within the thread from a UserMessage structure
    fn set(&mut self, tag: String, um: UserMessage) {
        log::trace!("UserMessenger::set_internal");
        let sev = &um.severity;
        match sev {
            Severity::Debug => log::debug!("[{}] {}", tag, um.message),
            Severity::Notice => log::info!("[{}] {}", tag, um.message),
            Severity::Warning | Severity::ConfigurationWarning => {
                log::warn!("[{}] {}", tag, um.message)
            }
            Severity::Error | Severity::ConfigurationError => {
                log::error!("[{}] {}", tag, um.message)
            }
            Severity::FatalError | Severity::SystemError => log::error!("[{}] {}", tag, um.message),
        }

        let update = match self.messages.get(&tag) {
            None => true,
            Some(m) => um.severity >= m.severity,
        };
        if update {
            self.messages.insert(tag.clone(), um.clone());
            //self.output_sender.set_message(tag, um).unwrap_or_else(|e| log::error!("UserMessenger channel closed: {}", e));
            let res = self.output_sender.update_all(self.messages.clone());
            res.unwrap_or_else(|e| log::error!("UserMessenger channel closed: {}", e));
            self.output_sender
                .set_message(tag, um)
                .unwrap_or_else(|e| log::error!("Output sender could not set message: {}", e));
        }
    }

    /// clear a message form within the thread from a tag
    fn clear(&mut self, tag: &String) {
        log::trace!("UserMessenger::clear_internal");
        if self.messages.contains_key(tag) {
            self.messages.remove(tag);
            self.output_sender
                .clear_message(tag)
                .unwrap_or_else(|e| log::error!("UserMessenger channel closed: {}", e));
            let _res = self.output_sender.update_all(self.messages.clone());
            //res.unwrap_or_else(|e| log::error!("UserMessenger channel closed: {}", e));
        }
    }

    /// handle a job fromm the message queue
    fn handle_message(&mut self, msg: MessageJob) {
        log::trace!("UserMessenger::handle_message()");
        match msg {
            MessageJob::SetMessage { tag, msg } => self.set(tag, msg),
            MessageJob::ClearMessage { tag } => self.clear(&tag),
        }
    }

    // self is not a reference.  self is owned by this loop.
    async fn msg_loop(mut self) {
        log::trace!("UserMessenger::msg_loop()");

        while let Some(m) = self.receiver.recv().await {
            self.handle_message(m);
        }
        log::trace!("UserMessenger::msg_loop() is done");
    }
}

/// Public, clonable handler
/// All message setting and clearing should pass through here.
#[derive(Clone, Debug)]
pub struct UserMessagesHandle {
    sender: mpsc::Sender<MessageJob>,
}
impl UserMessagesHandle {
    pub async fn new(output_sender: impl Sender) -> Self {
        // max out so we don't fill memory with a runaway process.
        // instead, send functions will just fail silently if we fill up.
        let (sender, receiver) = mpsc::channel(1024);
        let um = UserMessenger {
            messages: HashMap::new(),
            receiver,
            output_sender: Box::new(output_sender),
        };
        let rt = Handle::current();
        rt.spawn(UserMessenger::msg_loop(um));
        UserMessagesHandle { sender }
    }

    /// # public functions
    /// ## basic functions for setting and clearing messages
    pub fn set_message(&self, severity: Severity, tag: &'static str, message: impl Into<String>) {
        let msg = UserMessage {
            severity,
            message: message.into(),
            time_last_set: Instant::now(),
        };
        let res = self.sender.try_send(MessageJob::SetMessage {
            tag: tag.into(),
            msg,
        });
        res.unwrap_or_else(|e| log::error!("UserMessenger channel was closed: {}", e))
    }

    pub fn clear_message(&self, tag: &'static str) {
        let res = self
            .sender
            .try_send(MessageJob::ClearMessage { tag: tag.into() });
        res.unwrap_or_else(|e| log::error!("UserMessenger channel closed: {}", e))
    }

    pub fn notify_message(
        &self,
        severity: Severity,
        tag: &'static str,
        message: impl Into<String>,
    ) {
        self.set_message(severity, tag, message);
        self.clear_message(tag);
    }

    /// ## Helpers for setting and clearing specific types of messages
    /// These can be called either form synchronous or asynchronous
    /// contexts.  They are non-blocking.
    pub fn set_debug(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::Debug, tag, message);
    }

    pub fn set_notice(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::Notice, tag, message)
    }

    pub fn set_warning(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::Warning, tag, message)
    }

    pub fn set_config_warning(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::ConfigurationWarning, tag, message)
    }

    pub fn set_error(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::Error, tag, message)
    }

    pub fn set_fatal_error(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::FatalError, tag, message)
    }

    pub fn set_system_error(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::SystemError, tag, message)
    }

    pub fn set_config_error(&self, tag: &'static str, message: impl Into<String>) {
        self.set_message(Severity::ConfigurationError, tag, message)
    }

    /// ### These helpers immediately clear the set message
    /// They are 'one-shot' errors.rs that don't need to be sustained.
    pub fn debug(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::Debug, tag, message);
    }

    pub fn notice(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::Notice, tag, message);
    }

    pub fn warning(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::Warning, tag, message);
    }

    // probably not needed
    pub fn config_warning(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::ConfigurationWarning, tag, message);
    }

    pub fn error(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::Error, tag, message);
    }

    pub fn fatal_error(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::FatalError, tag, message);
    }

    pub fn system_error(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::SystemError, tag, message);
    }

    //probably not needed
    pub fn config_error(&self, message: impl Into<String>) {
        let tag = "__temp__";
        self.notify_message(Severity::ConfigurationError, tag, message);
    }
}

/// Application should implement this trait
/// and pass the object around throughout for reporting errors
pub trait UserMessageProviderBase {
    fn user_message_handle(self: Box<Self>) -> UserMessagesHandle;
}

/// this trait is necessary to make UserMessageProvider types clonable
/// Thanks to daboross at rust-lang.org for the tip
/// https://users.rust-lang.org/t/why-cant-traits-require-clone/23686/3
pub trait UserMsgProvider: UserMessageProviderBase + Sync + Send + 'static {
    fn ump_clone(&self) -> Box<dyn UserMsgProvider>;
}

impl<T> UserMsgProvider for T
where
    T: UserMessageProviderBase + Clone + Sync + Send + 'static,
{
    fn ump_clone(&self) -> Box<dyn UserMsgProvider> {
        Box::new(self.clone())
    }
}

// This provides a test UserMessageProvider
#[derive(Clone, Debug)]
pub struct TestUserMessageProvider {
    umh: UserMessagesHandle,
}

impl UserMessageProviderBase for TestUserMessageProvider {
    fn user_message_handle(self: Box<Self>) -> UserMessagesHandle {
        self.umh.clone()
    }
}

impl TestUserMessageProvider {
    pub async fn new(output_sender: impl Sender) -> Self {
        Self {
            umh: UserMessagesHandle::new(output_sender).await,
        }
    }
    pub async fn default() -> Self {
        Self {
            umh: UserMessagesHandle::new(TestSender::default()).await,
        }
    }
}

/// This is a test Sender that
/// builds up a vector of MessageHashes
/// that can be popped out
#[derive(Clone, Debug)]
pub struct TestSender {
    pub last_message: Arc<Mutex<Vec<MessageHash>>>,
}

impl Sender for TestSender {
    fn update_all(&mut self, messages: MessageHash) -> Result<(), String> {
        let mut x = self.last_message.lock().unwrap();
        x.push(messages);
        Ok(())
    }

    fn set_message(&mut self, _tag: String, _msg: UserMessage) -> Result<(), String> {
        Ok(())
    }

    fn clear_message(&mut self, _tag: &str) -> Result<(), String> {
        Ok(())
    }
}

impl Default for TestSender {
    fn default() -> Self {
        Self {
            last_message: Arc::new(Mutex::new(Vec::new())),
        }
    }
}

impl TestSender {
    pub fn pop(&mut self) -> MessageHash {
        let mut lm = self.last_message.lock().unwrap();
        lm.remove(0)
    }

    pub async fn wait_first(&mut self) -> MessageHash {
        let count = 0i32;
        loop {
            {
                let mut x = self.last_message.lock().unwrap();
                if !x.is_empty() {
                    return x.remove(0);
                }
            }

            if count > 100 {
                panic!("Timed out waiting for messages in a TestSender");
            }

            sleep(Duration::from_millis(100)).await
        }
    }
}

/// panic on a formatted string,
/// but first report the string as an error
/// to a UserMessageHandle
///
/// Usefule in the pipe  line functions.
/// Unrecoverable errors there should be paniced to kill the pipeline
#[macro_export]
macro_rules! panic_report {
    ($ump:expr, $fmt:expr $(,$args:expr)*) => {
        {
            let msg = format!($fmt, $($args,)*);
            $ump.error(msg.clone());
            panic!("{}", msg);
        }
    };
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::thread::sleep;
    use std::time::Duration;
    use tokio::runtime::Runtime;

    #[test]
    fn test_test() {
        let rt = Runtime::new().unwrap();
        let _rt_guard = rt.enter();

        let mut user_channel = TestSender::default();

        let umh = rt.block_on(UserMessagesHandle::new(user_channel.clone()));

        pretty_env_logger::init();

        let umh_h = &umh;
        umh_h.system_error("This is a test system error".to_string());

        umh.set_warning("TEST_WARN", "This is a test warning".to_string());

        sleep(Duration::from_millis(500));
        let hm = user_channel.pop();
        assert!(hm.contains_key("__temp__"));

        let hm = user_channel.pop();
        assert!(!hm.contains_key("__temp__"));

        let hm = user_channel.pop();
        assert!(hm.contains_key("TEST_WARN"));
        drop(umh);
    }
}
