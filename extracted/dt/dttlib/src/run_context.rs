//! A collection of handles to various process
//! that run permanently in the library

use crate::user::{UserOutputHandle, UserOutputSender, UserOutputSenderWrapper};
use user_messages::{UserMessageProviderBase, UserMessagesHandle};

#[derive(Clone)]
pub struct RunContext {
    /// All output to the user goes through this handle.
    pub output_handle: UserOutputHandle,
    /// Set of error messages and other log messages through this handle
    pub user_messages: UserMessagesHandle,
}

impl RunContext {
    pub async fn new(output_handle: UserOutputHandle, user_messages: UserMessagesHandle) -> Self {
        RunContext {
            output_handle,
            user_messages,
        }
    }

    pub async fn create(out_send: UserOutputSender) -> Self {
        RunContext::new(
            UserOutputHandle::new(out_send.clone()),
            UserMessagesHandle::new(UserOutputSenderWrapper::new(out_send)).await,
        )
        .await
    }
}

impl UserMessageProviderBase for RunContext {
    fn user_message_handle(self: Box<Self>) -> UserMessagesHandle {
        self.user_messages.clone()
    }
}

#[cfg(test)]
pub(crate) mod tests {

    use lazy_static::lazy_static;

    lazy_static! {
        static ref TEST_RUNTIME: tokio::runtime::Runtime = tokio::runtime::Runtime::new().unwrap();
    }

    use super::*;
    use crate::user::{DTT, UserOutputReceiver};

    pub(crate) fn start_runtime() -> (DTT, UserOutputReceiver, Box<RunContext>) {
        let uc_items = DTT::create(TEST_RUNTIME.handle().clone());
        let uc = uc_items.0;
        let rc = uc.runtime.block_on(RunContext::create(uc_items.2));
        (uc, uc_items.3, Box::new(rc))
    }
}
