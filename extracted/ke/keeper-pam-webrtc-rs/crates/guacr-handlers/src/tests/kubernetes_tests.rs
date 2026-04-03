#![cfg(feature = "kubernetes")]
use crate::kubernetes::{
    build_config_from_kubeconfig, build_config_from_server_cert, build_config_from_token,
    detect_auth_method, format_age, format_pod_description, format_volume_source, param_keys,
    AuthMethod, PodInfo,
};
use base64::Engine;
use k8s_openapi::api::core::v1::Pod;
use std::collections::HashMap;

// -- PodInfo tests --

#[test]
fn test_pod_info_columns() {
    let cols = PodInfo::columns();
    assert_eq!(cols.len(), 7);
    assert_eq!(cols[0].0, "NAMESPACE");
    assert_eq!(cols[1].0, "NAME");
    assert_eq!(cols[2].0, "CONTAINERS");
    assert_eq!(cols[3].0, "STATUS");
    assert_eq!(cols[4].0, "RESTARTS");
    assert_eq!(cols[5].0, "AGE");
    assert_eq!(cols[6].0, "NODE");
}

#[test]
fn test_pod_info_to_row() {
    let info = PodInfo {
        namespace: "default".to_string(),
        name: "nginx-abc123".to_string(),
        containers: vec!["nginx".to_string(), "sidecar".to_string()],
        status: "Running".to_string(),
        restarts: 3,
        age: "5d".to_string(),
        node: "node-1".to_string(),
    };

    let row = info.to_row();
    assert_eq!(row.len(), 7);
    assert_eq!(row[0], "default");
    assert_eq!(row[1], "nginx-abc123");
    assert_eq!(row[2], "nginx,sidecar");
    assert_eq!(row[3], "Running");
    assert_eq!(row[4], "3");
    assert_eq!(row[5], "5d");
    assert_eq!(row[6], "node-1");
}

#[test]
fn test_pod_info_to_row_empty_containers() {
    let info = PodInfo {
        namespace: "kube-system".to_string(),
        name: "pending-pod".to_string(),
        containers: vec![],
        status: "Pending".to_string(),
        restarts: 0,
        age: "12m".to_string(),
        node: "".to_string(),
    };

    let row = info.to_row();
    assert_eq!(row[2], ""); // empty containers join
    assert_eq!(row[4], "0");
    assert_eq!(row[6], ""); // no node yet
}

#[test]
fn test_pod_info_to_row_matches_column_count() {
    let info = PodInfo {
        namespace: "ns".to_string(),
        name: "pod".to_string(),
        containers: vec!["c1".to_string()],
        status: "Running".to_string(),
        restarts: 0,
        age: "1h".to_string(),
        node: "n1".to_string(),
    };

    let cols = PodInfo::columns();
    let row = info.to_row();
    assert_eq!(
        cols.len(),
        row.len(),
        "Column count must match row field count"
    );
}

// -- Age formatting tests --

#[test]
fn test_format_age_seconds() {
    let now = chrono::Utc::now();
    let created = now - chrono::Duration::seconds(30);
    let age = format_age(&created);
    assert_eq!(age, "30s");
}

#[test]
fn test_format_age_minutes() {
    let now = chrono::Utc::now();
    let created = now - chrono::Duration::minutes(15);
    let age = format_age(&created);
    assert_eq!(age, "15m");
}

#[test]
fn test_format_age_hours() {
    let now = chrono::Utc::now();
    let created = now - chrono::Duration::hours(7);
    let age = format_age(&created);
    assert_eq!(age, "7h");
}

#[test]
fn test_format_age_days() {
    let now = chrono::Utc::now();
    let created = now - chrono::Duration::days(42);
    let age = format_age(&created);
    assert_eq!(age, "42d");
}

#[test]
fn test_format_age_years() {
    let now = chrono::Utc::now();
    let created = now - chrono::Duration::days(800);
    let age = format_age(&created);
    assert_eq!(age, "2y");
}

#[test]
fn test_format_age_zero() {
    let now = chrono::Utc::now();
    let age = format_age(&now);
    assert_eq!(age, "0s");
}

#[test]
fn test_format_age_future_timestamp() {
    // If the timestamp is somehow in the future, we should not panic
    let future = chrono::Utc::now() + chrono::Duration::seconds(60);
    let age = format_age(&future);
    // Duration will be negative; our code clamps seconds to 0
    assert_eq!(age, "0s");
}

// -- Auth method detection tests --

#[test]
fn test_detect_auth_kubeconfig() {
    let mut params = HashMap::new();
    params.insert("kubeconfig".to_string(), "base64data".to_string());
    assert_eq!(detect_auth_method(&params), AuthMethod::Kubeconfig);
}

#[test]
fn test_detect_auth_token() {
    let mut params = HashMap::new();
    params.insert("token".to_string(), "eyJhbGci...".to_string());
    assert_eq!(detect_auth_method(&params), AuthMethod::Token);
}

#[test]
fn test_detect_auth_server_cert() {
    let mut params = HashMap::new();
    params.insert(
        "server".to_string(),
        "https://k8s.example.com:6443".to_string(),
    );
    params.insert("ca_cert".to_string(), "base64cert".to_string());
    assert_eq!(detect_auth_method(&params), AuthMethod::ServerCert);
}

#[test]
fn test_detect_auth_default() {
    let params = HashMap::new();
    assert_eq!(detect_auth_method(&params), AuthMethod::Default);
}

#[test]
fn test_detect_auth_precedence_kubeconfig_over_token() {
    let mut params = HashMap::new();
    params.insert("kubeconfig".to_string(), "base64data".to_string());
    params.insert("token".to_string(), "some-token".to_string());
    // kubeconfig takes precedence
    assert_eq!(detect_auth_method(&params), AuthMethod::Kubeconfig);
}

#[test]
fn test_detect_auth_precedence_token_over_server() {
    let mut params = HashMap::new();
    params.insert("token".to_string(), "some-token".to_string());
    params.insert("server".to_string(), "https://k8s.example.com".to_string());
    // token takes precedence over bare server
    assert_eq!(detect_auth_method(&params), AuthMethod::Token);
}

// -- Namespace filtering tests --

#[test]
fn test_namespace_from_params() {
    let mut params = HashMap::new();
    params.insert("namespace".to_string(), "production".to_string());
    let ns = params.get("namespace").cloned();
    assert_eq!(ns, Some("production".to_string()));
}

#[test]
fn test_namespace_absent_means_all() {
    let params: HashMap<String, String> = HashMap::new();
    let ns = params.get("namespace").cloned();
    assert!(ns.is_none()); // None means all namespaces
}

// -- Config building tests (unit-testable portions) --

#[test]
fn test_build_config_from_token_missing_token() {
    let params = HashMap::new();
    let result = build_config_from_token(&params);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Missing 'token'"));
}

#[test]
fn test_build_config_from_token_default_server() {
    let mut params = HashMap::new();
    params.insert("token".to_string(), "test-token-value".to_string());
    let result = build_config_from_token(&params);
    // Should succeed with default server URL
    assert!(result.is_ok(), "Token config should succeed: {:?}", result);
}

#[test]
fn test_build_config_from_token_custom_server() {
    let mut params = HashMap::new();
    params.insert("token".to_string(), "test-token-value".to_string());
    params.insert(
        "server".to_string(),
        "https://custom-k8s.example.com:6443".to_string(),
    );
    let result = build_config_from_token(&params);
    assert!(result.is_ok());
}

#[test]
fn test_build_config_from_token_with_ca_cert() {
    let mut params = HashMap::new();
    params.insert("token".to_string(), "test-token-value".to_string());
    // A valid base64-encoded "test cert" (not a real cert, just valid base64)
    params.insert("ca_cert".to_string(), "dGVzdCBjZXJ0".to_string());
    let result = build_config_from_token(&params);
    assert!(result.is_ok());
}

#[test]
fn test_build_config_from_token_invalid_ca_cert_base64() {
    let mut params = HashMap::new();
    params.insert("token".to_string(), "test-token-value".to_string());
    params.insert("ca_cert".to_string(), "not-valid-base64!!!".to_string());
    let result = build_config_from_token(&params);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Invalid base64 in ca_cert"));
}

#[test]
fn test_build_config_from_server_cert_missing_server() {
    let params = HashMap::new();
    let result = build_config_from_server_cert(&params);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Missing 'server'"));
}

#[test]
fn test_build_config_from_server_cert_valid() {
    let mut params = HashMap::new();
    params.insert(
        "server".to_string(),
        "https://k8s.example.com:6443".to_string(),
    );
    params.insert("ca_cert".to_string(), "dGVzdCBjZXJ0".to_string());
    let result = build_config_from_server_cert(&params);
    assert!(result.is_ok());
}

#[test]
fn test_build_config_from_server_cert_no_ca() {
    let mut params = HashMap::new();
    params.insert(
        "server".to_string(),
        "https://k8s.example.com:6443".to_string(),
    );
    // No CA cert - should still work but with insecure TLS
    let result = build_config_from_server_cert(&params);
    assert!(result.is_ok());
}

#[test]
fn test_build_config_from_server_cert_invalid_url() {
    let mut params = HashMap::new();
    params.insert("server".to_string(), "not a url".to_string());
    let result = build_config_from_server_cert(&params);
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Invalid server URL"));
}

// -- Kubeconfig base64 parsing tests --

#[tokio::test]
async fn test_build_config_from_kubeconfig_invalid_base64() {
    let mut params = HashMap::new();
    params.insert("kubeconfig".to_string(), "not-base64!!!".to_string());
    let result = build_config_from_kubeconfig(&params).await;
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Invalid base64"));
}

#[tokio::test]
async fn test_build_config_from_kubeconfig_invalid_yaml() {
    let mut params = HashMap::new();
    // Valid base64 of "not yaml at all: {{{"
    let bad_yaml = base64::engine::general_purpose::STANDARD.encode("not yaml at all: {{{");
    params.insert("kubeconfig".to_string(), bad_yaml);
    let result = build_config_from_kubeconfig(&params).await;
    assert!(result.is_err());
    // Should fail during YAML parse or kubeconfig interpretation
    let err = result.unwrap_err();
    assert!(
        err.contains("parse") || err.contains("Failed"),
        "Error should mention parsing: {}",
        err
    );
}

#[tokio::test]
async fn test_build_config_from_kubeconfig_missing_param() {
    let params = HashMap::new();
    let result = build_config_from_kubeconfig(&params).await;
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Missing 'kubeconfig'"));
}

// -- Pod description formatting tests --

#[test]
fn test_format_pod_description_minimal() {
    let pod = Pod {
        metadata: k8s_openapi::apimachinery::pkg::apis::meta::v1::ObjectMeta {
            name: Some("test-pod".to_string()),
            namespace: Some("test-ns".to_string()),
            ..Default::default()
        },
        spec: Some(k8s_openapi::api::core::v1::PodSpec {
            containers: vec![k8s_openapi::api::core::v1::Container {
                name: "main".to_string(),
                image: Some("nginx:latest".to_string()),
                ..Default::default()
            }],
            ..Default::default()
        }),
        status: Some(k8s_openapi::api::core::v1::PodStatus {
            phase: Some("Running".to_string()),
            pod_ip: Some("10.0.0.5".to_string()),
            ..Default::default()
        }),
    };

    let desc = format_pod_description(&pod);
    assert!(desc.contains("Name:         test-pod"));
    assert!(desc.contains("Namespace:    test-ns"));
    assert!(desc.contains("Status:       Running"));
    assert!(desc.contains("IP:           10.0.0.5"));
    assert!(desc.contains("nginx:latest"));
    assert!(desc.contains("Containers:"));
    assert!(desc.contains("  main:"));
}

#[test]
fn test_format_pod_description_with_labels() {
    let mut labels = std::collections::BTreeMap::new();
    labels.insert("app".to_string(), "web".to_string());
    labels.insert("tier".to_string(), "frontend".to_string());

    let pod = Pod {
        metadata: k8s_openapi::apimachinery::pkg::apis::meta::v1::ObjectMeta {
            name: Some("labeled-pod".to_string()),
            labels: Some(labels),
            ..Default::default()
        },
        spec: Some(k8s_openapi::api::core::v1::PodSpec {
            containers: vec![k8s_openapi::api::core::v1::Container {
                name: "app".to_string(),
                ..Default::default()
            }],
            ..Default::default()
        }),
        status: None,
    };

    let desc = format_pod_description(&pod);
    assert!(desc.contains("Labels:"));
    assert!(desc.contains("app=web"));
    assert!(desc.contains("tier=frontend"));
}

#[test]
fn test_format_pod_description_no_labels() {
    let pod = Pod {
        metadata: k8s_openapi::apimachinery::pkg::apis::meta::v1::ObjectMeta {
            name: Some("no-labels".to_string()),
            ..Default::default()
        },
        spec: None,
        status: None,
    };

    let desc = format_pod_description(&pod);
    assert!(desc.contains("Labels:       <none>"));
}

// -- PodInfo::from_pod tests --

#[test]
fn test_pod_info_from_pod_minimal() {
    let pod = Pod {
        metadata: k8s_openapi::apimachinery::pkg::apis::meta::v1::ObjectMeta::default(),
        spec: None,
        status: None,
    };

    let info = PodInfo::from_pod(&pod);
    assert_eq!(info.namespace, "default");
    assert_eq!(info.name, "<unknown>");
    assert!(info.containers.is_empty());
    assert_eq!(info.status, "Unknown");
    assert_eq!(info.restarts, 0);
    assert_eq!(info.age, "<unknown>");
    assert_eq!(info.node, "");
}

// -- Param keys tests --

#[test]
fn test_param_key_constants() {
    assert_eq!(param_keys::KUBECONFIG, "kubeconfig");
    assert_eq!(param_keys::TOKEN, "token");
    assert_eq!(param_keys::SERVER, "server");
    assert_eq!(param_keys::CA_CERT, "ca_cert");
    assert_eq!(param_keys::NAMESPACE, "namespace");
    assert_eq!(param_keys::CONTEXT, "context");
}

// -- Volume source formatting tests --

#[test]
fn test_format_volume_source_configmap() {
    use k8s_openapi::api::core::v1::*;
    let vol = Volume {
        name: "config-vol".to_string(),
        config_map: Some(ConfigMapVolumeSource {
            name: "my-config".to_string(),
            ..Default::default()
        }),
        ..Default::default()
    };
    let mut out = String::new();
    format_volume_source(&mut out, &vol);
    assert!(out.contains("ConfigMap"));
    assert!(out.contains("my-config"));
}

#[test]
fn test_format_volume_source_secret() {
    use k8s_openapi::api::core::v1::*;
    let vol = Volume {
        name: "secret-vol".to_string(),
        secret: Some(SecretVolumeSource {
            secret_name: Some("my-secret".to_string()),
            ..Default::default()
        }),
        ..Default::default()
    };
    let mut out = String::new();
    format_volume_source(&mut out, &vol);
    assert!(out.contains("Secret"));
    assert!(out.contains("my-secret"));
}

#[test]
fn test_format_volume_source_emptydir() {
    use k8s_openapi::api::core::v1::*;
    let vol = Volume {
        name: "tmp".to_string(),
        empty_dir: Some(EmptyDirVolumeSource::default()),
        ..Default::default()
    };
    let mut out = String::new();
    format_volume_source(&mut out, &vol);
    assert!(out.contains("EmptyDir"));
}

#[test]
fn test_format_volume_source_pvc() {
    use k8s_openapi::api::core::v1::*;
    let vol = Volume {
        name: "data".to_string(),
        persistent_volume_claim: Some(PersistentVolumeClaimVolumeSource {
            claim_name: "my-pvc".to_string(),
            ..Default::default()
        }),
        ..Default::default()
    };
    let mut out = String::new();
    format_volume_source(&mut out, &vol);
    assert!(out.contains("PersistentVolumeClaim"));
    assert!(out.contains("my-pvc"));
}

#[test]
fn test_format_volume_source_hostpath() {
    use k8s_openapi::api::core::v1::*;
    let vol = Volume {
        name: "host".to_string(),
        host_path: Some(HostPathVolumeSource {
            path: "/var/log".to_string(),
            ..Default::default()
        }),
        ..Default::default()
    };
    let mut out = String::new();
    format_volume_source(&mut out, &vol);
    assert!(out.contains("HostPath"));
    assert!(out.contains("/var/log"));
}
