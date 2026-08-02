use crate::PipelineError;
use crate::publisher::{Publisher, Subscriber};
use crate::{
    PIPELINE_SIZE, PipeData, PipeOut, PipeResult, PipelineBase, PipelineOutput, PipelineReceiver,
    PipelineSender, PipelineSubscriber, StateData,
};
use futures::future::BoxFuture;
use std::marker::PhantomData;
use user_messages::UserMsgProvider;

/// # types defining setup and tear down functions
pub(crate) type PipeSetup<S> = fn(&mut S) -> Result<(), PipelineError>;
pub(crate) type PipeTeardown<S> = fn(&mut S);

/// Pipeline with 0 inputs, a data source
///
///
pub trait Pipe0Generator<T: PipeData, S: StateData>:
    'static + Sync + Send + Fn(Box<dyn UserMsgProvider>, &mut S) -> BoxFuture<PipeResult<T>>
{
}
impl<
    T: PipeData,
    S: StateData,
    Z: 'static + Sync + Send + Fn(Box<dyn UserMsgProvider>, &mut S) -> BoxFuture<PipeResult<T>>,
> Pipe0Generator<T, S> for Z
{
}

/// Implement Pipeline traits in a convenient way
pub struct Pipe0<T: PipeData, S: StateData, G>
where
    G: Pipe0Generator<T, S>,
{
    name: String,
    generate: G,
    setup_fn: Option<PipeSetup<S>>,
    teardown_fn: Option<PipeTeardown<S>>,
    state: S,
    publisher: PipelineSender<T>,
}

impl<T: PipeData, S: StateData, G> PipelineBase for Pipe0<T, S, G>
where
    G: Pipe0Generator<T, S>,
{
    type Output = T;

    fn name(&self) -> &str {
        self.name.as_str()
    }
}

impl<T: PipeData, S: StateData, G> Pipe0<T, S, G>
where
    G: Pipe0Generator<T, S>,
{
    fn run(mut self, rc: Box<dyn UserMsgProvider>) {
        tokio::runtime::Handle::current().spawn(async move {
            if let Err(e) = self.setup() {
                let msg = format!("Aborted pipeline '{}' during setup: {}", self.name(), e);
                rc.user_message_handle().error(msg);
                return;
            }
            'main: loop {
                let out = (self.generate)(rc.ump_clone(), &mut self.state).await;
                match out {
                    PipeResult::Output(pipe_out) => {
                        // close on zero sized output
                        if pipe_out.is_empty() {
                            break 'main;
                        }

                        for po in pipe_out {
                            if self.publisher.send(po).await.is_err() {
                                break 'main;
                            }
                        }
                    }
                    PipeResult::Close => {
                        break 'main;
                    } // data source responsible for closing by issuing a none
                }
            }
            self.teardown();
        });
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

    /// # Creation of pipeline
    /// create a 0-input pipeline, a pipeline data source
    /// given a generator function, a setup function and teardown function
    pub fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        generate: G,
        state: S,
        setup_fn: Option<PipeSetup<S>>,
        teardown_fn: Option<PipeTeardown<S>>,
    ) -> PipelineSubscriber<T> {
        let (publisher, subscriber) = Publisher::create(PIPELINE_SIZE);
        let pipe = Self {
            name: name.into(),
            generate,
            setup_fn,
            teardown_fn,
            state,
            publisher,
        };
        pipe.run(rc);
        subscriber
    }
}

/// # Pipeline with 1 input
///
/// # Some supported pipe 1 generators
/// standard async generator
/// Implemented as trait, a hack:
/// https://stackoverflow.com/questions/57937436/how-to-alias-an-impl-trait
///
/// should be an alias!, but traits aren't aliasable.
/// Have to also implement it.
pub trait Pipe1Generator<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData>:
    'static + Sync + Send + Fn(Box<dyn UserMsgProvider>, &mut S, A) -> BoxFuture<PipeResult<T>>
{
}
impl<
    I: PipeData,
    A: PipeOut<I>,
    T: PipeData,
    S: StateData,
    Z: 'static + Sync + Send + Fn(Box<dyn UserMsgProvider>, &mut S, A) -> BoxFuture<PipeResult<T>>,
> Pipe1Generator<I, A, T, S> for Z
{
}

/// Implement Pipeline traits in a convenient way
pub struct Pipe1<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, G>
where
    G: Pipe1Generator<I, A, T, S>,
{
    name: String,
    generate: G,
    setup_fn: Option<PipeSetup<S>>,
    teardown_fn: Option<PipeTeardown<S>>,
    state: S,
    publisher: PipelineSender<T>,
    phantom_data: PhantomData<I>,
    phantom_data2: PhantomData<A>,
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, G> PipelineBase for Pipe1<I, A, T, S, G>
where
    G: Pipe1Generator<I, A, T, S>,
{
    type Output = T;

    fn name(&self) -> &str {
        self.name.as_str()
    }
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, S: StateData, G> Pipe1<I, A, T, S, G>
where
    G: Pipe1Generator<I, A, T, S>,
{
    fn run(mut self, rc: Box<dyn UserMsgProvider>, mut input_recv: PipelineReceiver<I>) {
        tokio::runtime::Handle::current().spawn(async move {
            if let Err(e) = self.setup() {
                let msg = format!("Aborted pipeline '{}' during setup: {}", self.name(), e);
                rc.user_message_handle().error(msg);
                return;
            }
            'main: loop {
                //println!("{} input backlog = {}", self.name, input_recv.len());
                let input = match input_recv.recv().await {
                    Some(i) => i,
                    None => break 'main,
                };

                #[allow(clippy::needless_borrow)]
                let out_vec =
                    match (self.generate)(rc.ump_clone(), &mut self.state, input.clone().into())
                        .await
                    {
                        PipeResult::Output(x) => x,
                        PipeResult::Close => break 'main,
                    };

                for out in out_vec.into_iter() {
                    // handle good input
                    if self.publisher.send(out).await.is_err() {
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
            phantom_data: PhantomData,
            phantom_data2: PhantomData,
        };
        p.run(rc.ump_clone(), input_sub.subscribe().await?);
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

/// # Pipeline with 2 inputs
/// Pipeline 2 input generator func
pub trait Pipe2Generator<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
>:
    'static + Sync + Send + Fn(Box<dyn UserMsgProvider>, &mut S, A, B) -> BoxFuture<PipeResult<T>>
{
}
impl<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
    Z: 'static + Sync + Send + Fn(Box<dyn UserMsgProvider>, &mut S, A, B) -> BoxFuture<PipeResult<T>>,
> Pipe2Generator<I, H, A, B, T, S> for Z
{
}

/// Implement Pipeline traits in a convenient way
pub struct Pipe2<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    S: StateData,
    G,
> where
    G: Pipe2Generator<I, H, A, B, T, S>,
{
    name: String,
    generate: G,
    setup_fn: Option<PipeSetup<S>>,
    teardown_fn: Option<PipeTeardown<S>>,
    state: S,
    publisher: PipelineSender<T>,
    phantom_data: PhantomData<I>,
    phantom_data2: PhantomData<H>,
    phantom_data3: PhantomData<A>,
    phantom_data4: PhantomData<B>,
}

impl<I: PipeData, H: PipeData, A: PipeOut<I>, B: PipeOut<H>, T: PipeData, S: StateData, G>
    PipelineBase for Pipe2<I, H, A, B, T, S, G>
where
    G: Pipe2Generator<I, H, A, B, T, S>,
{
    type Output = T;

    fn name(&self) -> &str {
        self.name.as_str()
    }
}

impl<I: PipeData, H: PipeData, A: PipeOut<I>, B: PipeOut<H>, T: PipeData, S: StateData, G>
    Pipe2<I, H, A, B, T, S, G>
where
    G: Pipe2Generator<I, H, A, B, T, S>,
{
    fn run(
        mut self,
        rc: Box<dyn UserMsgProvider>,
        mut in1_recv: PipelineReceiver<I>,
        mut in2_recv: PipelineReceiver<H>,
    ) {
        tokio::spawn(async move {
            'main: loop {
                if let Err(e) = self.setup() {
                    let msg = format!("Aborted pipeline '{}' during setup: {}", self.name(), e);
                    rc.user_message_handle().error(msg);
                    return;
                }
                // process input1
                let inp1 = match in1_recv.recv().await {
                    Some(i) => i,
                    None => break,
                };

                // process input2
                let inp2 = match in2_recv.recv().await {
                    Some(i) => i,
                    None => break,
                };
                let out_vec = match (self.generate)(
                    rc.ump_clone(),
                    &mut self.state,
                    inp1.clone().into(),
                    inp2.clone().into(),
                )
                .await
                {
                    PipeResult::Output(x) => x,
                    PipeResult::Close => break 'main,
                };
                for out in out_vec.into_iter() {
                    // handle good input
                    if self.publisher.send(out).await.is_err() {
                        // no more receivers, quit
                        break 'main;
                    }
                }
            }
            self.teardown();
        });
    }

    /// create a 1-input pipeline
    /// given a generator function, a setup function and teardown function
    #[allow(clippy::too_many_arguments)]
    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: impl Into<String>,
        generate: G,
        state: S,
        setup_fn: Option<PipeSetup<S>>,
        teardown_fn: Option<PipeTeardown<S>>,
        input_sub1: &PipelineSubscriber<I>,
        input_sub2: &PipelineSubscriber<H>,
    ) -> Result<Subscriber<PipelineOutput<T>>, PipelineError> {
        let (publisher, subscriber) = Publisher::create(PIPELINE_SIZE);
        let p = Self {
            name: name.into(),
            generate,
            setup_fn,
            teardown_fn,
            state,
            publisher,
            phantom_data: PhantomData,
            phantom_data2: PhantomData,
            phantom_data3: PhantomData,
            phantom_data4: PhantomData,
        };
        p.run(
            rc.ump_clone(),
            input_sub1.subscribe().await?,
            input_sub2.subscribe().await?,
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
