//! Thse pipelines do not take every input, but are allowed to drop some inputs
//! If the input stream stops, this pipeline will eventually take the final input
//! Useful for pipelines that take a lot of calculation and don't need to run on every input.
//! Prevents the rest of the pipeline structure from bogging down.
//!
//! This pipe also takes an optional configuration watch channel to tweak the configuration
//! mid-analysis.

use crate::pipe::{PipeSetup, PipeTeardown};
use crate::publisher::{MaybeInitialized, Publisher, Subscriber};
use crate::{
    ConfigData, PIPELINE_SIZE, PipeData, PipeOut, PipeResult, PipelineBase, PipelineError,
    PipelineOutput, PipelineSender, PipelineSubscriber, PipelineWatchReceiver, StateData,
};
use std::marker::PhantomData;
use tokio::sync::watch::error::RecvError;
use user_messages::UserMsgProvider;

pub trait UnsyncPipe1Generator<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData>:
    'static + Sync + Send + for<'a> Fn(Box<dyn UserMsgProvider>, &'a C, &'a mut S, A) -> PipeResult<T>
{
}
impl<
    I: PipeData,
    A: PipeOut<I>,
    T: PipeData,
    S: StateData,
    C: ConfigData,
    Z: 'static
        + Sync
        + Send
        + for<'a> Fn(Box<dyn UserMsgProvider>, &'a C, &'a mut S, A) -> PipeResult<T>,
> UnsyncPipe1Generator<I, A, T, S, C> for Z
{
}

async fn await_optional_watch<T>(
    watch: &mut Option<tokio::sync::watch::Receiver<T>>,
) -> Option<Result<T, RecvError>>
where
    T: Clone + Send + Sync + 'static,
{
    match watch {
        None => None,
        Some(w) => match w.changed().await {
            Ok(_) => Some(Ok(w.borrow_and_update().clone())),
            Err(e) => Some(Err(e)),
        },
    }
}

pub struct UnsyncPipe1<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData, G>
where
    G: UnsyncPipe1Generator<I, A, T, S, C>,
{
    name: String,
    generate: G,
    setup_fn: Option<PipeSetup<S>>,
    teardown_fn: Option<PipeTeardown<S>>,
    config_watch: Option<tokio::sync::watch::Receiver<C>>,
    state: S,
    publisher: PipelineSender<T>,
    phantom_data: PhantomData<I>,
    phantom_data2: PhantomData<A>,
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData, G> PipelineBase
    for UnsyncPipe1<I, A, T, S, C, G>
where
    G: UnsyncPipe1Generator<I, A, T, S, C>,
{
    type Output = T;

    fn name(&self) -> &str {
        self.name.as_str()
    }
}

enum PipeInputReceived<I: PipeData> {
    Some(PipelineOutput<I>),
    None,
    Close,
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, C: ConfigData + Default, G>
    UnsyncPipe1<I, A, T, S, C, G>
where
    G: UnsyncPipe1Generator<I, A, T, S, C>,
{
    async fn read_pipe_input(
        &mut self,
        config: &mut C,
        input_recv: &mut PipelineWatchReceiver<I>,
    ) -> PipeInputReceived<I> {
        tokio::select! {
            c = input_recv.changed() => {
                match c {
                    Ok(_) => {
                        match input_recv.borrow_and_update().clone() {
                            MaybeInitialized::Initialized(i) =>
                            {
                                PipeInputReceived::Some(i)
                            },
                            MaybeInitialized::Uninitialized => {
                                PipeInputReceived::None
                            }
                        }
                    },
                    Err(_) => {PipeInputReceived::Close},
                }
            },
            Some(cr) = await_optional_watch(&mut self.config_watch) => {
                match cr {
                    Ok(c) => {
                        *config = c;
                        // println!("got config");
                        match input_recv.borrow_and_update().clone() {
                            MaybeInitialized::Initialized(i) => PipeInputReceived::Some(i),
                            MaybeInitialized::Uninitialized => {
                                PipeInputReceived::None
                            }
                        }
                    },
                    Err(_) => {
                        PipeInputReceived::Close
                    },
                }
            }
        }
    }

    fn run(mut self, rc: Box<dyn UserMsgProvider>, mut input_recv: PipelineWatchReceiver<I>) {
        let rt = tokio::runtime::Handle::current();
        let rt2 = rt.clone();
        rt2.spawn_blocking(move || {
            if let Err(e) = self.setup() {
                let msg = format!(
                    "Aborted unsynchronized pipeline '{}' during setup: {}",
                    self.name(),
                    e
                );
                rc.user_message_handle().error(msg);
                return;
            }
            let mut config = match &self.config_watch {
                None => C::default(),
                Some(w) => w.borrow().clone(),
            };
            'main: loop {
                let input = match rt.block_on(self.read_pipe_input(&mut config, &mut input_recv)) {
                    PipeInputReceived::Some(i) => i,
                    PipeInputReceived::Close => break 'main,
                    PipeInputReceived::None => continue 'main,
                };

                #[allow(clippy::needless_borrow)]
                let out_vec = match (self.generate)(
                    rc.ump_clone(),
                    &config,
                    &mut self.state,
                    input.clone().into(),
                ) {
                    PipeResult::Output(x) => x,
                    PipeResult::Close => break 'main,
                };

                for out in out_vec.into_iter() {
                    // handle good input
                    if rt.block_on(self.publisher.send(out)).is_err() {
                        // no more receivers, quit
                        break 'main;
                    }
                }
            }
            self.teardown();
        });
    }

    /// # setup
    /// create a 1-input pipeline
    /// given a generator function, a setup function and teardown function
    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        generate: G,
        config_watch: Option<tokio::sync::watch::Receiver<C>>,
        state: S,
        setup_fn: Option<PipeSetup<S>>,
        teardown_fn: Option<PipeTeardown<S>>,
        input_sub: &PipelineSubscriber<I>,
    ) -> Result<Subscriber<PipelineOutput<T>>, PipelineError> {
        let (publisher, subscriber) = Publisher::create(PIPELINE_SIZE);
        let p = Self {
            name: name.into(),
            generate,
            setup_fn,
            teardown_fn,
            state,
            publisher,
            config_watch,
            phantom_data: PhantomData,
            phantom_data2: PhantomData,
        };
        p.run(rc.ump_clone(), input_sub.unsync_subscribe().await?);
        Ok(subscriber)
    }

    fn setup(&mut self) -> Result<(), PipelineError> {
        if let Some(setup) = &self.setup_fn {
            setup(&mut self.state)
        } else {
            Ok(())
        }
    }

    fn teardown(&mut self) {
        if let Some(teardown) = &self.teardown_fn {
            teardown(&mut self.state);
        }
    }
}

// # 2-input pipe

pub trait UnsyncPipe2Generator<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
    C: ConfigData,
>:
    'static
    + Sync
    + Send
    + for<'a> Fn(Box<dyn UserMsgProvider>, &'a C, &'a mut S, A, B) -> PipeResult<T>
{
}
impl<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
    C: ConfigData,
    Z: 'static
        + Sync
        + Send
        + for<'a> Fn(Box<dyn UserMsgProvider>, &'a C, &'a mut S, A, B) -> PipeResult<T>,
> UnsyncPipe2Generator<I, H, A, B, T, S, C> for Z
{
}

pub struct UnsyncPipe2<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
    C: ConfigData,
    G,
> where
    G: UnsyncPipe2Generator<I, H, A, B, T, S, C>,
{
    name: String,
    generate: G,
    setup_fn: Option<PipeSetup<S>>,
    teardown_fn: Option<PipeTeardown<S>>,
    config_watch: Option<tokio::sync::watch::Receiver<C>>,
    state: S,
    publisher: PipelineSender<T>,
    phantom_data: PhantomData<I>,
    phantom_data3: PhantomData<H>,
    phantom_data2: PhantomData<A>,
    phantom_data4: PhantomData<B>,
}

impl<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
    C: ConfigData,
    G,
> PipelineBase for UnsyncPipe2<I, H, A, B, T, S, C, G>
where
    G: UnsyncPipe2Generator<I, H, A, B, T, S, C>,
{
    type Output = T;

    fn name(&self) -> &str {
        self.name.as_str()
    }
}

impl<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
    C: ConfigData + Default,
    G,
> UnsyncPipe2<I, H, A, B, T, S, C, G>
where
    G: UnsyncPipe2Generator<I, H, A, B, T, S, C>,
{
    async fn read_pipe_inputs(
        &mut self,
        config: &mut C,
        input_recv1: &mut PipelineWatchReceiver<I>,
        input_recv2: &mut PipelineWatchReceiver<H>,
    ) -> (PipeInputReceived<I>, PipeInputReceived<H>) {
        tokio::select! {
            c = input_recv2.changed() => {
                match c {
                    Ok(_) => {
                        let input1 = input_recv1.borrow_and_update().clone();
                        let input2 = input_recv2.borrow_and_update().clone();
                        match (input1, input2) {
                            (MaybeInitialized::Initialized(i), MaybeInitialized::Initialized(h)) =>
                            {
                                (PipeInputReceived::Some(i), PipeInputReceived::Some(h))
                            },
                            (MaybeInitialized::Initialized(i), MaybeInitialized::Uninitialized) => {
                                (PipeInputReceived::Some(i), PipeInputReceived::None)
                            }
                            (MaybeInitialized::Uninitialized, MaybeInitialized::Initialized(h)) => {
                                (PipeInputReceived::None, PipeInputReceived::Some(h))
                            },
                            (MaybeInitialized::Uninitialized, MaybeInitialized::Uninitialized) => {
                                (PipeInputReceived::None, PipeInputReceived::None)
                            }
                        }
                    },
                    Err(_) => {(PipeInputReceived::Close, PipeInputReceived::Close)},
                }
            },
            c = input_recv1.changed() => {
                match c {
                    Ok(_) => {
                        let input1 = input_recv1.borrow_and_update().clone();
                        let input2 = input_recv2.borrow_and_update().clone();
                        match (input1, input2) {
                            (MaybeInitialized::Initialized(i), MaybeInitialized::Initialized(h)) =>
                            {
                                (PipeInputReceived::Some(i), PipeInputReceived::Some(h))
                            },
                            (MaybeInitialized::Initialized(i), MaybeInitialized::Uninitialized) => {
                                (PipeInputReceived::Some(i), PipeInputReceived::None)
                            }
                            (MaybeInitialized::Uninitialized, MaybeInitialized::Initialized(h)) => {
                                (PipeInputReceived::None, PipeInputReceived::Some(h))
                            },
                            (MaybeInitialized::Uninitialized, MaybeInitialized::Uninitialized) => {
                                (PipeInputReceived::None, PipeInputReceived::None)
                            }
                        }
                    },
                    Err(_) => {(PipeInputReceived::Close, PipeInputReceived::Close)},
                }
            },
            Some(cr) = await_optional_watch(&mut self.config_watch) => {
                match cr {
                    Ok(c) => {
                        *config = c;
                        // println!("got config");
                        let input1 = input_recv1.borrow_and_update().clone();
                        let input2 = input_recv2.borrow_and_update().clone();
                        match (input1, input2) {
                            (MaybeInitialized::Initialized(i), MaybeInitialized::Initialized(h)) =>
                            {
                                (PipeInputReceived::Some(i), PipeInputReceived::Some(h))
                            },
                            (MaybeInitialized::Initialized(i), MaybeInitialized::Uninitialized) => {
                                (PipeInputReceived::Some(i), PipeInputReceived::None)
                            }
                            (MaybeInitialized::Uninitialized, MaybeInitialized::Initialized(h)) => {
                                (PipeInputReceived::None, PipeInputReceived::Some(h))
                            },
                            (MaybeInitialized::Uninitialized, MaybeInitialized::Uninitialized) => {
                                (PipeInputReceived::None, PipeInputReceived::None)
                            }
                        }
                    },
                    Err(_) => {
                        (PipeInputReceived::Close, PipeInputReceived::Close)
                    },
                }
            }
        }
    }

    fn run(
        mut self,
        rc: Box<dyn UserMsgProvider>,
        mut input_recv1: PipelineWatchReceiver<I>,
        mut input_recv2: PipelineWatchReceiver<H>,
    ) {
        let rt = tokio::runtime::Handle::current();
        let rt2 = rt.clone();
        rt2.spawn_blocking(move || {
            if let Err(e) = self.setup() {
                let msg = format!(
                    "Aborted unsynchronized pipeline '{}' during setup: {}",
                    self.name(),
                    e
                );
                rc.user_message_handle().error(msg);
                return;
            }
            let mut config = match &self.config_watch {
                None => C::default(),
                Some(w) => w.borrow().clone(),
            };
            'main: loop {
                let (input1, input2) = match rt.block_on(self.read_pipe_inputs(
                    &mut config,
                    &mut input_recv1,
                    &mut input_recv2,
                )) {
                    (PipeInputReceived::Some(i), PipeInputReceived::Some(h)) => (i, h),
                    (PipeInputReceived::None, _) | (_, PipeInputReceived::None) => continue 'main,
                    (PipeInputReceived::Close, _) | (_, PipeInputReceived::Close) => break 'main,
                };

                #[allow(clippy::needless_borrow)]
                let out_vec = match (self.generate)(
                    rc.ump_clone(),
                    &config,
                    &mut self.state,
                    input1.clone().into(),
                    input2.clone().into(),
                ) {
                    PipeResult::Output(x) => x,
                    PipeResult::Close => break 'main,
                };

                for out in out_vec.into_iter() {
                    // handle good input
                    if rt.block_on(self.publisher.send(out)).is_err() {
                        // no more receivers, quit
                        break 'main;
                    }
                }
            }
            self.teardown();
        });
    }

    /// # setup
    /// create a 1-input pipeline
    /// given a generator function, a setup function and teardown function
    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        generate: G,
        config_watch: Option<tokio::sync::watch::Receiver<C>>,
        state: S,
        setup_fn: Option<PipeSetup<S>>,
        teardown_fn: Option<PipeTeardown<S>>,
        input1_sub: &PipelineSubscriber<I>,
        input2_sub: &PipelineSubscriber<H>,
    ) -> Result<Subscriber<PipelineOutput<T>>, PipelineError> {
        let (publisher, subscriber) = Publisher::create(PIPELINE_SIZE);
        let p = Self {
            name: name.into(),
            generate,
            setup_fn,
            teardown_fn,
            state,
            publisher,
            config_watch,
            phantom_data: PhantomData,
            phantom_data2: PhantomData,
            phantom_data3: PhantomData,
            phantom_data4: PhantomData,
        };
        p.run(
            rc.ump_clone(),
            input1_sub.unsync_subscribe().await?,
            input2_sub.unsync_subscribe().await?,
        );
        Ok(subscriber)
    }

    fn setup(&mut self) -> Result<(), PipelineError> {
        if let Some(setup) = &self.setup_fn {
            setup(&mut self.state)
        } else {
            Ok(())
        }
    }

    fn teardown(&mut self) {
        if let Some(teardown) = &self.teardown_fn {
            teardown(&mut self.state);
        }
    }
}
