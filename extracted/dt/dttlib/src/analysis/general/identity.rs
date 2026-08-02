//! This pipeline returns its input
//! Useful in those cases when you need to have a pipeline, no matter what it does.
#![allow(dead_code)]
use pipelines::PipeData;
use std::sync::Arc;
use user_messages::UserMsgProvider;

pub(crate) fn generate<T: PipeData>(_rc: Box<dyn UserMsgProvider>, input: Arc<T>) -> Arc<T> {
    input
}
