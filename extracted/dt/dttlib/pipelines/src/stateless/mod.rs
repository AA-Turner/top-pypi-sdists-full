use crate::publisher::Publisher;
use crate::{
    ConfigData, PIPELINE_SIZE, PipeData, PipeOut, PipeResult, PipelineBase, PipelineError,
    PipelineOutput, PipelineReceiver, PipelineSender, PipelineSubscriber,
};
use futures::future::BoxFuture;
use std::marker::PhantomData;
use tokio::sync::mpsc;
use user_messages::UserMsgProvider;

pub mod pure;

type GenOutputSender<T> = mpsc::Sender<PipelineOutput<T>>;
type GenOutputReceiver<T> = mpsc::Receiver<PipelineOutput<T>>;

type GenOutputReceiverReceiver<T> = mpsc::Receiver<GenOutputReceiver<T>>;

/// # Some supported 1-input stateless generators
/// standard async generator
/// Implemented as trait with a hack:
/// https://stackoverflow.com/questions/57937436/how-to-alias-an-impl-trait
///
/// should be an alias!, but traits aren't aliasable.
/// Have to also implement it.
pub trait Stateless1Gen<I: PipeData, A: PipeOut<I>, T: PipeData, C: ConfigData>:
    'static
    + Sync
    + Send
    + Clone
    + Fn(Box<dyn UserMsgProvider>, String, &C, A) -> BoxFuture<PipeResult<T>>
{
}
impl<
    I: PipeData,
    A: PipeOut<I>,
    T: PipeData,
    C: ConfigData,
    Z: 'static
        + Sync
        + Send
        + Clone
        + Fn(Box<dyn UserMsgProvider>, String, &C, A) -> BoxFuture<PipeResult<T>>,
> Stateless1Gen<I, A, T, C> for Z
{
}

/// 1 input stateless pipe
/// These can run in parallel, unlink the stateful Pipe1
pub struct Stateless1<I: PipeData, A: PipeOut<I>, T: PipeData, C: ConfigData, G>
where
    G: Stateless1Gen<I, A, T, C>,
{
    phantom_data1: PhantomData<I>,
    phantom_data3: PhantomData<A>,
    config: C,
    generate: G,
    name: String,
    publisher: PipelineSender<T>,
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, C: ConfigData, G> PipelineBase
    for Stateless1<I, A, T, C, G>
where
    G: Stateless1Gen<I, A, T, C>,
{
    type Output = T;

    fn name(&self) -> &str {
        self.name.as_str()
    }
}

impl<I: PipeData, A: PipeOut<I>, T: PipeData, C: ConfigData, G> Stateless1<I, A, T, C, G>
where
    G: Stateless1Gen<I, A, T, C>,
{
    fn run(self, rc: Box<dyn UserMsgProvider>, mut input_recv: PipelineReceiver<I>) {
        tokio::runtime::Handle::current().spawn(async move {
            let (gors, gorr) = mpsc::channel(4);

            let name = self.name().to_string();
            tokio::spawn(process_gen_out(
                name.clone(),
                rc.ump_clone(),
                self.publisher,
                gorr,
            ));

            'main: loop {
                let input = match input_recv.recv().await {
                    Some(i) => i,
                    None => {
                        break;
                    }
                };

                let (gos, gor) = mpsc::channel(10);

                let gener = self.generate.clone();
                let rg = Self::run_gen(
                    gener,
                    rc.ump_clone(),
                    name.clone(),
                    self.config.clone(),
                    input,
                    gos,
                );
                tokio::spawn(rg);
                if gors.send(gor).await.is_err() {
                    break 'main;
                }
            }
        });
    }

    async fn run_gen(
        gen_fn: G,
        rc: Box<dyn UserMsgProvider>,
        name: String,
        config: C,
        input: PipelineOutput<I>,
        out_send: GenOutputSender<T>,
    ) {
        let pipe_res = gen_fn(rc, name, &config, input.into()).await;
        match pipe_res {
            PipeResult::Close => (), //needs to be Option type to match send on Output
            PipeResult::Output(out_vec) => {
                for out in out_vec.into_iter() {
                    if out_send.send(out).await.is_err() {
                        break;
                    }
                }
            }
        };
    }

    /// # setup
    /// create a 1-input pipeline
    /// given a generator function, a setup function and teardown function
    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: String,
        generate: G,
        config: C,
        input_sub: &PipelineSubscriber<I>,
    ) -> Result<PipelineSubscriber<T>, PipelineError> {
        let (publisher, subscriber) = Publisher::create(PIPELINE_SIZE);
        let p = Self {
            phantom_data1: PhantomData,
            phantom_data3: PhantomData,
            config,
            name,
            generate,
            publisher,
        };
        p.run(rc.ump_clone(), input_sub.subscribe().await?);
        Ok(subscriber)
    }
}

pub trait Stateless2Gen<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    C: ConfigData,
>:
    'static
    + Sync
    + Send
    + Clone
    + Fn(Box<dyn UserMsgProvider>, String, &C, A, B) -> BoxFuture<PipeResult<T>>
{
}
impl<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    C: ConfigData,
    Z: 'static
        + Sync
        + Send
        + Clone
        + Fn(Box<dyn UserMsgProvider>, String, &C, A, B) -> BoxFuture<PipeResult<T>>,
> Stateless2Gen<I, H, A, B, T, C> for Z
{
}

/// # 2 input stateless pipes
/// These can run in parallel, unlinke the stateful Pipe2.
pub struct Stateless2<
    I: PipeData,
    H: PipeData,
    A: PipeOut<I>,
    B: PipeOut<H>,
    T: PipeData,
    C: ConfigData,
    G,
> where
    G: Stateless2Gen<I, H, A, B, T, C>,
{
    phantom_data: PhantomData<I>,
    phantom_data2: PhantomData<H>,
    phantom_data5: PhantomData<A>,
    phantom_data6: PhantomData<B>,
    generate: G,
    name: String,
    config: C,
    publisher: PipelineSender<T>,
}

impl<I: PipeData, H: PipeData, A: PipeOut<I>, B: PipeOut<H>, T: PipeData, C: ConfigData, G>
    PipelineBase for Stateless2<I, H, A, B, T, C, G>
where
    G: Stateless2Gen<I, H, A, B, T, C>,
{
    type Output = T;

    fn name(&self) -> &str {
        self.name.as_str()
    }
}

impl<I: PipeData, H: PipeData, A: PipeOut<I>, B: PipeOut<H>, T: PipeData, C: ConfigData, G>
    Stateless2<I, H, A, B, T, C, G>
where
    G: Stateless2Gen<I, H, A, B, T, C>,
{
    fn run(
        self,
        rc: Box<dyn UserMsgProvider>,
        mut input_recv1: PipelineReceiver<I>,
        mut input_recv2: PipelineReceiver<H>,
    ) {
        tokio::spawn(async move {
            let (gors, gorr) = mpsc::channel(4);

            let name = self.name().to_string();
            tokio::spawn(process_gen_out(
                name.clone(),
                rc.ump_clone(),
                self.publisher,
                gorr,
            ));

            'main: loop {
                let input1 = match input_recv1.recv().await {
                    Some(i) => i,
                    None => {
                        break;
                    }
                };
                let input2 = match input_recv2.recv().await {
                    Some(i) => i,
                    None => {
                        break;
                    }
                };

                let (gos, gor) = mpsc::channel(10);

                let gener = self.generate.clone();
                tokio::spawn(Self::run_gen(
                    gener,
                    rc.ump_clone(),
                    name.clone(),
                    self.config.clone(),
                    input1,
                    input2,
                    gos,
                ));
                if gors.send(gor).await.is_err() {
                    break 'main;
                }
            }
        });
    }
}

impl<I: PipeData, H: PipeData, A: PipeOut<I>, B: PipeOut<H>, T: PipeData, C: ConfigData, G>
    Stateless2<I, H, A, B, T, C, G>
where
    G: Stateless2Gen<I, H, A, B, T, C>,
{
    async fn run_gen(
        gener: G,
        rc: Box<dyn UserMsgProvider>,
        name: String,
        config: C,
        input1: PipelineOutput<I>,
        input2: PipelineOutput<H>,
        out_send: GenOutputSender<T>,
    ) -> Result<(), ()> {
        let pipe_res = gener(rc, name, &config, input1.into(), input2.into()).await;
        match pipe_res {
            PipeResult::Close => (), //needs to be Option type to match send on Output
            PipeResult::Output(out_vec) => {
                for out in out_vec.into_iter() {
                    if out_send.send(out).await.is_err() {
                        return Err(());
                    };
                }
            }
        };
        Ok(())
    }

    /// # setup
    /// create a 1-input pipeline
    /// given a generator function, a setup function and teardown function
    pub async fn create(
        rc: Box<dyn UserMsgProvider>,
        name: String,
        generate: G,
        config: C,
        input_sub1: &PipelineSubscriber<I>,
        input_sub2: &PipelineSubscriber<H>,
    ) -> Result<PipelineSubscriber<T>, PipelineError> {
        let (publisher, subscriber) = Publisher::create(PIPELINE_SIZE);
        let p = Self {
            phantom_data: PhantomData,
            phantom_data2: PhantomData,
            phantom_data5: PhantomData,
            phantom_data6: PhantomData,
            config,
            name,
            generate,
            publisher,
        };
        p.run(
            rc.ump_clone(),
            input_sub1.subscribe().await?,
            input_sub2.subscribe().await?,
        );
        Ok(subscriber)
    }
}

#[allow(clippy::manual_async_fn)]
fn process_gen_out<T: PipeData>(
    _pipe_name: String,
    _rc: Box<dyn UserMsgProvider>,
    sender: PipelineSender<T>,
    mut gen_out_recv_recv: GenOutputReceiverReceiver<T>,
) -> impl Future<Output = ()> + Send {
    async move {
        'outer: loop {
            if let Some(mut gen_out_recv) = gen_out_recv_recv.recv().await {
                if let Some(out) = gen_out_recv.recv().await {
                    if sender.send(out).await.is_err() {
                        break 'outer; // just drop out.  Downstream pipeline is broken.
                    }
                } else {
                    //rc.user_messages.error("Channel closed from generate function without value".to_string());
                }
            } else {
                break 'outer;
            }
        }
    }
}
