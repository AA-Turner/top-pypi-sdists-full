use std::collections::HashMap;
use std::future::poll_fn;
use std::sync::{
    Arc,
    atomic::{AtomicUsize, Ordering},
};
use std::task::Poll;
use std::time::Duration;

use async_trait::async_trait;
use futures::{Future, poll};
use serde_json::json;
use sha2::{Digest, Sha256};
use tokio::sync::Semaphore;

use super::download::ResponseHydrationBudget;
use super::errors::HydrationFailureReason;
use super::{HYDRATION_TIMEOUT, RemoteConfigValueHydrator, StoreHydrationOptions};
use crate::interned_values::interned_store::MmapProjectId;
use crate::networking::{
    HttpMethod, NetworkClient, NetworkProvider, RequestArgs, Response, ResponseData,
    ResponseLimitOutcome,
};
use crate::observability::ops_stats::OpsStatsForInstance;
use crate::specs_response::proto_specs::VerifiedRemoteConfigValues;
use crate::specs_response::spec_types::SpecsResponseFull;

const BODY: &[u8] = br#"{"marker":"writer-hydration-deadline"}"#;

struct BlockedBlobProvider {
    requests: AtomicUsize,
    responses: Semaphore,
}

#[async_trait]
impl NetworkProvider for BlockedBlobProvider {
    async fn send(&self, _: &HttpMethod, _: &RequestArgs) -> Response {
        self.requests.fetch_add(1, Ordering::SeqCst);
        self.responses.acquire().await.unwrap().forget();
        Response {
            status_code: Some(200),
            data: Some(ResponseData::from_bytes_with_headers(
                BODY.to_vec(),
                Some(HashMap::from([(
                    "content-type".to_owned(),
                    "application/json".to_owned(),
                )])),
            )),
            error: None,
        }
    }

    async fn send_with_response_limit(
        &self,
        method: &HttpMethod,
        args: &RequestArgs,
        limit: u64,
    ) -> ResponseLimitOutcome {
        assert_eq!(limit, BODY.len() as u64);
        ResponseLimitOutcome::Response(self.send(method, args).await)
    }
}

#[tokio::test(start_paused = true)]
async fn json_download_deadline_releases_response_budget() {
    tokio::time::resume();
    let provider = Arc::new(BlockedBlobProvider {
        requests: AtomicUsize::new(0),
        responses: Semaphore::new(0),
    });
    let network_provider: Arc<dyn NetworkProvider> = provider.clone();
    let mut network = NetworkClient::new("secret-writer-hydration-deadline", None, None);
    network.set_network_provider_for_test(Arc::downgrade(&network_provider));
    let budget = Arc::new(ResponseHydrationBudget::new(BODY.len()));
    let mut hydrator = RemoteConfigValueHydrator::new_with_ops_stats(
        Arc::new(network),
        Arc::new(OpsStatsForInstance::new()),
    );
    hydrator.response_budget = Arc::clone(&budget);
    let sha: String = Sha256::digest(BODY)
        .iter()
        .map(|byte| format!("{byte:02x}"))
        .collect();
    let mut specs = serde_json::to_value(SpecsResponseFull::default()).unwrap();
    specs["dynamic_configs"] = json!({"deadline": {
        "type": "dynamic_config", "entity": "dynamic_config", "enabled": true,
        "salt": "writer-deadline", "idType": "userID", "rules": [],
        "defaultValue": {"value": format!("/v1/dynamic_config_value/{sha}")},
        "remoteConfigMetadata": {
            "sha256": sha, "byteLength": BODY.len(),
            "contentType": "application/json", "compression": "none",
        },
    }});
    let mut data = ResponseData::from_bytes(serde_json::to_vec(&specs).unwrap());
    let current = VerifiedRemoteConfigValues::new();
    let mut update = Box::pin(hydrator.prepare_json_store_update(
        &mut data,
        StoreHydrationOptions::new(
            "https://statsigcdn.openai.com/v2/download_config_specs/key.json",
            MmapProjectId::for_sdk_key("writer-hydration-deadline"),
        ),
        &current,
        None,
    ));
    poll_fn(|cx| {
        assert!(update.as_mut().poll(cx).is_pending());
        if provider.requests.load(Ordering::SeqCst) == 1 {
            Poll::Ready(())
        } else {
            Poll::Pending
        }
    })
    .await;
    assert_eq!(budget.bytes.available_permits(), 0);
    tokio::time::pause();
    tokio::time::advance(HYDRATION_TIMEOUT + Duration::from_secs(1)).await;
    let error = match poll!(update.as_mut()) {
        Poll::Ready(Err(error)) => error,
        _ => panic!("a blocked blob download must time out"),
    };
    assert_eq!(
        HydrationFailureReason::from_error(&error),
        Some(HydrationFailureReason::TotalTimeout)
    );
    assert_eq!(budget.bytes.available_permits(), BODY.len());
}
