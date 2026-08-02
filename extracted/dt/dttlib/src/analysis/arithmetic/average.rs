//! Average the successive values of a frequency domain function

use crate::analysis::types::linear::Linear;
use crate::analysis::types::{AccumulationStats, MutableAccumulation};
use crate::errors::DTTError;
use pipelines::accumulator::Accumulator;
use pipelines::{PipeData, PipeResult, PipelineSubscriber};
use std::sync::Arc;
use user_messages::UserMsgProvider;

fn average<'a, T>(
    rc: Box<dyn UserMsgProvider>,
    input: Arc<T>,
    accum: Option<Arc<T>>,
    n: f64,
) -> (Arc<T>, f64, PipeResult<T>)
where
    T: Clone + Linear<'a, T> + 'static + MutableAccumulation + PipeData,
{
    let in_stats = input.get_accumulation_stats();

    let (avg, n) = match accum {
        None => {
            let output = input.as_ref().clone();
            output.set_accumulation_stats(AccumulationStats::default());
            (Arc::new(output), 2.0)
        }
        Some(t) => {
            if in_stats.sequence_size > 0 && in_stats.sequence_index == 0 {
                let output = input.as_ref().clone();
                output.set_accumulation_stats(AccumulationStats::default());
                (Arc::new(output), 2.0)
            } else {
                let a = 1.0 / n;
                let b = 1.0 - a;

                let scaled_inp = input.as_ref().clone() * (a / b);
                let backup_t = t.clone();

                // have to make sure we can actually add these
                let avg = match scaled_inp + t {
                    Ok(v) => {
                        let output = v * b; // need to normalize so the total factor is 1.
                        let output_accum = output.set_accumulation_stats(AccumulationStats {
                            n,
                            ..AccumulationStats::default()
                        });
                        Arc::new(output_accum)
                    }
                    Err(e) => {
                        let msg =
                            format!("Error when trying to accumulate a value: {}", e.to_string());
                        rc.user_message_handle().error(msg);
                        backup_t
                    }
                };

                (avg, n + 1.0)
            }
        }
    };

    if in_stats.sequence_size > 0 {
        if in_stats.sequence_index + 1 >= in_stats.sequence_size {
            (avg.clone(), 1.0, avg.into())
        } else {
            (avg.clone(), n, Vec::new().into())
        }
    } else {
        (avg.clone(), n, avg.into())
    }
}

pub async fn create<'a, T>(
    rc: Box<dyn UserMsgProvider>,
    name: impl Into<String>,
    input: &PipelineSubscriber<T>,
) -> Result<PipelineSubscriber<T>, DTTError>
where
    T: PipeData + Linear<'a, T> + MutableAccumulation,
{
    Ok(Accumulator::start(rc, name.into(), input, average).await?)
}
