//! Fnq transport using the controller-mounted working JWT. The exchange
//! credential stays outside the workload; opening the file per RPC observes
//! Kubernetes Secret-volume rotation.
use std::collections::HashSet;
use std::path::PathBuf;
use std::time::{Duration, Instant};

use chalk_remote_call_proto::chalk::runtime::v1::fnq_consumer_service_client::FnqConsumerServiceClient;
use chalk_remote_call_proto::chalk::runtime::v1::{
    AcquireWorkRequest, FnqWork, RenewWorkRequest, ReportResultsRequest,
};
use tonic::transport::{Channel, ClientTlsConfig, Endpoint};
use tonic::{Request, Status};

pub const MESSAGE_LIMIT: usize = 64 * 1024 * 1024;

#[derive(Clone)]
pub struct FnqClient {
    client: FnqConsumerServiceClient<Channel>,
    token_file: PathBuf,
}

#[allow(
    clippy::result_large_err,
    reason = "Keep the native tonic status type at the RPC boundary"
)]
impl FnqClient {
    pub fn new(endpoint: &str, token_file: PathBuf) -> Result<Self, tonic::transport::Error> {
        let mut endpoint = Endpoint::from_shared(endpoint.to_owned())?
            .connect_timeout(Duration::from_secs(5))
            .timeout(Duration::from_secs(5));
        if endpoint.uri().scheme_str() == Some("https") {
            endpoint = endpoint.tls_config(ClientTlsConfig::new().with_native_roots())?;
        }
        Ok(Self {
            client: FnqConsumerServiceClient::new(endpoint.connect_lazy())
                .max_decoding_message_size(MESSAGE_LIMIT)
                .max_encoding_message_size(MESSAGE_LIMIT),
            token_file,
        })
    }

    async fn request<T>(&self, message: T) -> Result<Request<T>, Status> {
        let token = tokio::fs::read_to_string(&self.token_file)
            .await
            .map_err(|_| Status::unauthenticated("Fnq working-token file unavailable"))?;
        if token.trim().is_empty() {
            return Err(Status::unauthenticated("Fnq working-token file is empty"));
        }
        let mut authorization: tonic::metadata::MetadataValue<tonic::metadata::Ascii> =
            format!("Bearer {}", token.trim())
                .parse()
                .map_err(|_| Status::unauthenticated("invalid Fnq working-token file"))?;
        authorization.set_sensitive(true);
        let mut request = Request::new(message);
        request
            .metadata_mut()
            .insert("authorization", authorization);
        Ok(request)
    }

    pub async fn acquire(
        &self,
        request: AcquireWorkRequest,
        mut dispatch: impl FnMut(FnqWork),
    ) -> Result<usize, Status> {
        let started = Instant::now();
        let retry_window = Duration::from_secs(u64::from(request.lease_duration_seconds));
        let mut delivered = HashSet::new();
        let mut backoff = Duration::from_millis(200);
        loop {
            if started.elapsed() >= retry_window {
                return Err(Status::failed_precondition(
                    "Fnq acquisition replay window expired",
                ));
            }
            let result = async {
                let mut stream = self
                    .client
                    .clone()
                    .acquire_work(self.request(request.clone()).await?)
                    .await?
                    .into_inner();

                while let Some(response) =
                    tokio::time::timeout(Duration::from_secs(5), stream.message())
                        .await
                        .map_err(|_| {
                            Status::deadline_exceeded("Fnq acquisition stream stalled")
                        })??
                {
                    // Redis's recorded deadline accounts for transit time. Renew
                    // before dispatch if less than half the requested lease remains.
                    let now = std::time::SystemTime::now()
                        .duration_since(std::time::UNIX_EPOCH)
                        .map_err(|_| Status::internal("system clock before Unix epoch"))?
                        .as_millis() as i128;
                    let mut response = response;
                    if let Some(work) = response
                        .work
                        .as_mut()
                        .filter(|work| !delivered.contains(&work.work_handle))
                    {
                        let deadline = work
                            .lease_expires_at
                            .as_ref()
                            .ok_or_else(|| Status::internal("missing lease expiration"))?;
                        let expires_ms = i128::from(deadline.seconds) * 1000
                            + i128::from(deadline.nanos) / 1_000_000;
                        if expires_ms - now <= i128::from(request.lease_duration_seconds) * 500 {
                            let renewed =
                                self.renew_response(vec![work.work_handle.clone()]).await?;
                            work.lease_expires_at =
                                Some(*renewed.lease_expires_at.get(&work.work_handle).ok_or_else(
                                    || {
                                        Status::failed_precondition(
                                            "Fnq delivery lease expired in transit",
                                        )
                                    },
                                )?);
                        }
                    }
                    if let Some(work) = response.work {
                        if delivered.insert(work.work_handle.clone()) {
                            dispatch(work);
                        }
                    }
                }
                Ok::<_, Status>(delivered.len())
            }
            .await;
            match result {
                Ok(work) => return Ok(work),
                Err(error) if retryable(&error) || error.code() == tonic::Code::Unauthenticated => {
                    // A lost response may already have dequeued work. Keep
                    // this request ID until the server returns work or rejects its lease.
                    if started.elapsed() >= retry_window {
                        return Err(Status::failed_precondition(
                            "Fnq acquisition replay window expired",
                        ));
                    }
                    tracing::warn!(%error, "Fnq acquisition failed; retrying the same request");
                    tokio::time::sleep(backoff).await;
                    backoff = (backoff * 2).min(Duration::from_secs(2));
                }
                Err(error) => return Err(error),
            }
        }
    }

    pub async fn renew(&self, handles: Vec<String>) -> Result<Vec<String>, Status> {
        Ok(self.renew_response(handles).await?.lost_work_handles)
    }

    async fn renew_response(
        &self,
        handles: Vec<String>,
    ) -> Result<chalk_remote_call_proto::chalk::runtime::v1::RenewWorkResponse, Status> {
        let response = self
            .client
            .clone()
            .renew_work(
                self.request(RenewWorkRequest {
                    work_handles: handles,
                })
                .await?,
            )
            .await?;
        Ok(response.into_inner())
    }

    pub async fn report(&self, request: ReportResultsRequest) -> Result<(), Status> {
        let started = Instant::now();
        loop {
            let result = match self.request(request.clone()).await {
                Ok(request) => self
                    .client
                    .clone()
                    .report_results(request)
                    .await
                    .map(|_| ()),
                Err(error) => Err(error),
            };
            match result {
                Ok(()) => return Ok(()),
                Err(error)
                    if (retryable(&error) || error.code() == tonic::Code::Unauthenticated)
                        && started.elapsed() < Duration::from_secs(15) =>
                {
                    tokio::time::sleep(Duration::from_millis(200)).await;
                }
                Err(error) => return Err(error),
            }
        }
    }
}

fn retryable(error: &Status) -> bool {
    matches!(
        error.code(),
        tonic::Code::Unavailable | tonic::Code::DeadlineExceeded | tonic::Code::Cancelled
    )
}
