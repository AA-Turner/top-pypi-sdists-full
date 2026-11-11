use super::*;
use oai_statsig_grpc::mock_forward_proxy::{MockForwardProxy, api::ConfigSpecResponse};
use tokio::sync::mpsc;
use wiremock::{Mock, MockServer, ResponseTemplate, matchers::method};

struct UpdateSender(mpsc::UnboundedSender<SpecsUpdate>);

impl SpecsUpdateListener for UpdateSender {
    fn did_receive_specs_update(&self, update: SpecsUpdate) -> Result<(), StatsigErr> {
        self.0.send(update).unwrap();
        Ok(())
    }

    fn get_current_specs_info(&self) -> SpecsInfo {
        SpecsInfo::empty()
    }
}

fn make_adapter(proxy: &MockForwardProxy, http: &MockServer) -> Arc<StatsigGrpcSpecsAdapter> {
    let config = SpecAdapterConfig {
        adapter_type: crate::SpecsAdapterType::NetworkGrpcWebsocket,
        specs_url: Some(format!("http://{}", proxy.proxy_address)),
        init_timeout_ms: 3_000,
        authentication_mode: None,
        ca_cert_path: None,
        client_cert_path: None,
        client_key_path: None,
        domain_name: None,
    };
    let options = StatsigOptions {
        specs_url: Some(http.uri()),
        ..StatsigOptions::new()
    };
    Arc::new(StatsigGrpcSpecsAdapter::new(
        "secret-key",
        &config,
        Some(&options),
    ))
}

#[tokio::test]
async fn recovery_cancels_only_the_current_fallback_even_during_http() {
    let proxy = MockForwardProxy::spawn().await;
    let http = MockServer::start().await;
    let entered = Arc::new(Notify::new());
    let (release_tx, release_rx) = std::sync::mpsc::channel();
    let release_rx = Mutex::new(Some(release_rx));
    let request_entered = entered.clone();
    Mock::given(method("GET"))
        .respond_with(move |_: &wiremock::Request| {
            if let Some(release) = release_rx.lock().take() {
                request_entered.notify_one();
                // Hold the first response until gRPC recovery has been delivered.
                release.recv_timeout(Duration::from_secs(5)).unwrap();
            }
            ResponseTemplate::new(200).set_body_string("fallback")
        })
        .mount(&http)
        .await;
    let adapter = make_adapter(&proxy, &http);
    let (updates_tx, mut updates_rx) = mpsc::unbounded_channel();
    adapter.initialize(Arc::new(UpdateSender(updates_tx)));
    let stream_adapter = adapter.clone();
    let stream_task =
        tokio::spawn(async move { stream_adapter.handle_grpc_request_stream().await });

    for last_updated in [1, 2] {
        proxy
            .send_stream_update(Ok(ConfigSpecResponse {
                spec: format!("streaming-{last_updated}"),
                last_updated,
                zstd_dict_id: None,
            }))
            .await;
        let mut update = timeout(Duration::from_secs(2), updates_rx.recv())
            .await
            .unwrap()
            .unwrap();
        assert_eq!(update.source, SpecsSource::Adapter("GRPC".into()));
        assert_eq!(
            update.data.read_to_string().unwrap(),
            format!("streaming-{last_updated}")
        );

        if last_updated == 1 {
            // Enter at the outage's fallback-spawn boundary, after a healthy update.
            // A retained cancellation permit must not suppress this new HTTP poller.
            adapter
                .retry_state
                .is_retrying
                .store(true, Ordering::SeqCst);
            StatsigGrpcSpecsAdapter::spawn_poll_from_statsig_thread(
                adapter.http_specs_adapter.clone(),
                adapter.cancel_poll_notify.clone(),
            );
            timeout(Duration::from_secs(5), entered.notified())
                .await
                .expect("a later outage must start HTTP fallback");
        }
    }
    assert!(!adapter.retry_state.is_retrying.load(Ordering::SeqCst));
    release_tx.send(()).unwrap();
    // The in-flight HTTP request may finish; recovery must prevent its next poll.
    let mut update = timeout(Duration::from_secs(2), updates_rx.recv())
        .await
        .unwrap()
        .unwrap();
    assert_eq!(update.source, SpecsSource::Network);
    assert_eq!(update.data.read_to_string().unwrap(), "fallback");
    let next_update = timeout(Duration::from_secs(4), updates_rx.recv()).await;

    adapter.cancel_poll_notify.notify_waiters();
    stream_task.abort();
    let _ = stream_task.await;
    proxy.stop().await;
    assert!(
        next_update.is_err(),
        "HTTP polling continued after gRPC recovery"
    );
    assert_eq!(http.received_requests().await.unwrap().len(), 1);
}

#[tokio::test(flavor = "multi_thread", worker_threads = 2)]
async fn start_accepts_updates_before_recording_the_worker_handle() {
    let proxy = MockForwardProxy::spawn().await;
    let http = MockServer::start().await;
    let adapter = make_adapter(&proxy, &http);
    let runtime = StatsigRuntime::get_runtime();
    let (updates_tx, mut updates_rx) = mpsc::unbounded_channel();
    adapter.initialize(Arc::new(UpdateSender(updates_tx)));
    let mut published = adapter.initialization_tx.subscribe();

    let start = tokio::task::block_in_place(|| {
        let _guard = adapter.task_handle_id.lock();
        let stream = adapter.clone();
        let runtime = runtime.clone();
        let start = tokio::task::spawn_blocking(move || {
            tokio::runtime::Handle::current().block_on(stream.start(&runtime))
        });
        // Pause startup while two stream results are published to its one-slot channel.
        tokio::runtime::Handle::current()
            .block_on(timeout(Duration::from_secs(4), async {
                for version in [1, 2] {
                    proxy
                        .send_stream_update(Ok(ConfigSpecResponse {
                            spec: version.to_string(),
                            last_updated: version,
                            zstd_dict_id: None,
                        }))
                        .await;
                    published.recv().await.unwrap().unwrap();
                }
            }))
            .unwrap();
        start
    });
    for expected in ["1", "2"] {
        assert_eq!(
            updates_rx
                .try_recv()
                .unwrap()
                .data
                .read_to_string()
                .unwrap(),
            expected
        );
    }
    let result = start.await.unwrap();
    adapter
        .shutdown(Duration::from_secs(1), &runtime)
        .await
        .unwrap();
    result.unwrap();
}

#[tokio::test]
async fn shutdown_joins_retrying_stream_and_stops_active_fallback() {
    let proxy = MockForwardProxy::spawn().await;
    let http = MockServer::start().await;
    Mock::given(method("GET"))
        .respond_with(ResponseTemplate::new(200).set_body_string("fallback"))
        .mount(&http)
        .await;
    let adapter = make_adapter(&proxy, &http);
    let runtime = StatsigRuntime::get_runtime();
    let (updates_tx, mut updates_rx) = mpsc::unbounded_channel();
    adapter.initialize(Arc::new(UpdateSender(updates_tx)));
    proxy
        .send_stream_update(Ok(ConfigSpecResponse {
            spec: "healthy".into(),
            last_updated: 1,
            zstd_dict_id: None,
        }))
        .await;
    adapter
        .clone()
        .schedule_background_sync(&runtime)
        .await
        .unwrap();
    let update = timeout(Duration::from_secs(2), updates_rx.recv())
        .await
        .unwrap()
        .unwrap();
    assert_eq!(update.source, SpecsSource::Adapter("GRPC".into()));

    // Enter the real outage handler at its fallback threshold and capped backoff.
    // Shutdown must interrupt the retry sleep, not wait for its next attempt.
    adapter
        .retry_state
        .retry_attempts
        .store(FALL_BACK_TO_POLLING_THREASHOLD, Ordering::SeqCst);
    adapter
        .retry_state
        .backoff_interval_ms
        .store(MAX_BACKOFF_INTERVAL_MS, Ordering::SeqCst);
    proxy.stop().await;
    let mut update = timeout(Duration::from_secs(5), updates_rx.recv())
        .await
        .unwrap()
        .unwrap();
    assert_eq!(update.source, SpecsSource::Network);
    assert_eq!(update.data.read_to_string().unwrap(), "fallback");

    adapter
        .shutdown(Duration::from_secs(3), &runtime)
        .await
        .expect("shutdown must join the retrying stream while fallback is active");
    assert!(
        timeout(Duration::from_secs(4), updates_rx.recv())
            .await
            .is_err(),
        "HTTP fallback continued after the stream shut down"
    );
    assert_eq!(http.received_requests().await.unwrap().len(), 1);

    // An empty runtime task map alone would miss a detached stream task.
    let weak_adapter = Arc::downgrade(&adapter);
    drop(adapter);
    assert!(
        weak_adapter.upgrade().is_none(),
        "stream task retained the adapter after shutdown"
    );
    assert_eq!(runtime.get_num_active_tasks(), 0);
    runtime.shutdown();
}
