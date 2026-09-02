#![cfg(feature = "docker")]
use crate::docker_handler::{
    detect_connection_mode, format_port_mappings, ContainerInfo, CONNECTION_TIMEOUT_SECS,
    DEFAULT_SOCKET_PATH, DEFAULT_TLS_PORT,
};
use std::collections::HashMap;

// -- ContainerInfo::to_row tests --

#[test]
fn test_to_row_returns_correct_order() {
    let info = ContainerInfo {
        id: "abc123def456".to_string(),
        name: "my-app".to_string(),
        image: "nginx:latest".to_string(),
        status: "Up 3 hours".to_string(),
        ports: "0.0.0.0:8080->80/tcp".to_string(),
        created: "3 hours ago".to_string(),
    };

    let row = info.to_row();
    assert_eq!(row.len(), 6);
    assert_eq!(row[0], "abc123def456");
    assert_eq!(row[1], "my-app");
    assert_eq!(row[2], "nginx:latest");
    assert_eq!(row[3], "Up 3 hours");
    assert_eq!(row[4], "0.0.0.0:8080->80/tcp");
    assert_eq!(row[5], "3 hours ago");
}

#[test]
fn test_to_row_matches_columns_count() {
    let columns = ContainerInfo::columns();
    let info = ContainerInfo {
        id: "a".to_string(),
        name: "b".to_string(),
        image: "c".to_string(),
        status: "d".to_string(),
        ports: "e".to_string(),
        created: "f".to_string(),
    };
    assert_eq!(info.to_row().len(), columns.len());
}

#[test]
fn test_columns_are_nonempty() {
    for (header, width) in ContainerInfo::columns() {
        assert!(!header.is_empty(), "Column header must not be empty");
        assert!(width > 0, "Column width must be positive for '{}'", header);
    }
}

// -- Port formatting tests --

#[test]
fn test_format_port_mappings_empty() {
    assert_eq!(format_port_mappings(&[]), "");
}

#[test]
fn test_format_port_mappings_host_bound() {
    let ports = vec![bollard::models::Port {
        ip: Some("0.0.0.0".to_string()),
        private_port: 80,
        public_port: Some(8080),
        typ: Some(bollard::models::PortTypeEnum::TCP),
    }];
    assert_eq!(format_port_mappings(&ports), "0.0.0.0:8080->80/tcp");
}

#[test]
fn test_format_port_mappings_no_host_ip() {
    let ports = vec![bollard::models::Port {
        ip: None,
        private_port: 443,
        public_port: Some(8443),
        typ: Some(bollard::models::PortTypeEnum::TCP),
    }];
    assert_eq!(format_port_mappings(&ports), "8443->443/tcp");
}

#[test]
fn test_format_port_mappings_container_only() {
    let ports = vec![bollard::models::Port {
        ip: None,
        private_port: 3306,
        public_port: None,
        typ: Some(bollard::models::PortTypeEnum::TCP),
    }];
    assert_eq!(format_port_mappings(&ports), "3306/tcp");
}

#[test]
fn test_format_port_mappings_udp() {
    let ports = vec![bollard::models::Port {
        ip: Some("0.0.0.0".to_string()),
        private_port: 53,
        public_port: Some(53),
        typ: Some(bollard::models::PortTypeEnum::UDP),
    }];
    assert_eq!(format_port_mappings(&ports), "0.0.0.0:53->53/udp");
}

#[test]
fn test_format_port_mappings_multiple() {
    let ports = vec![
        bollard::models::Port {
            ip: Some("0.0.0.0".to_string()),
            private_port: 80,
            public_port: Some(8080),
            typ: Some(bollard::models::PortTypeEnum::TCP),
        },
        bollard::models::Port {
            ip: None,
            private_port: 443,
            public_port: None,
            typ: Some(bollard::models::PortTypeEnum::TCP),
        },
    ];
    assert_eq!(
        format_port_mappings(&ports),
        "0.0.0.0:8080->80/tcp, 443/tcp"
    );
}

#[test]
fn test_format_port_mappings_no_type() {
    let ports = vec![bollard::models::Port {
        ip: None,
        private_port: 9090,
        public_port: None,
        typ: None,
    }];
    // Falls through to default "tcp"
    assert_eq!(format_port_mappings(&ports), "9090/tcp");
}

#[test]
fn test_format_port_mappings_sctp() {
    let ports = vec![bollard::models::Port {
        ip: Some("127.0.0.1".to_string()),
        private_port: 9999,
        public_port: Some(9999),
        typ: Some(bollard::models::PortTypeEnum::SCTP),
    }];
    assert_eq!(format_port_mappings(&ports), "127.0.0.1:9999->9999/sctp");
}

// -- Age formatting tests --

#[test]
fn test_format_age_seconds() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now), "1 second ago");
    assert_eq!(format_age(now - 30), "30 seconds ago");
}

#[test]
fn test_format_age_minutes() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - 60), "1 minute ago");
    assert_eq!(format_age(now - 300), "5 minutes ago");
    assert_eq!(format_age(now - 3540), "59 minutes ago");
}

#[test]
fn test_format_age_hours() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - 3600), "1 hour ago");
    assert_eq!(format_age(now - 10800), "3 hours ago");
    assert_eq!(format_age(now - 82800), "23 hours ago");
}

#[test]
fn test_format_age_days() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - 86400), "1 day ago");
    assert_eq!(format_age(now - 172800), "2 days ago");
    assert_eq!(format_age(now - (86400 * 15)), "15 days ago");
}

#[test]
fn test_format_age_months() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - (86400 * 30)), "1 month ago");
    assert_eq!(format_age(now - (86400 * 90)), "3 months ago");
}

#[test]
fn test_format_age_years() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - (86400 * 365)), "1 year ago");
    assert_eq!(format_age(now - (86400 * 730)), "2 years ago");
}

#[test]
fn test_format_age_future_timestamp() {
    use crate::docker_handler::format_age;
    let future = chrono::Utc::now().timestamp() + 3600;
    assert_eq!(format_age(future), "just now");
}

#[test]
fn test_format_age_boundary_59_seconds() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - 59), "59 seconds ago");
}

#[test]
fn test_format_age_boundary_23_hours() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - (23 * 3600)), "23 hours ago");
}

#[test]
fn test_format_age_boundary_29_days() {
    use crate::docker_handler::format_age;
    let now = chrono::Utc::now().timestamp();
    assert_eq!(format_age(now - (29 * 86400)), "29 days ago");
}

// -- Connection mode detection tests --

#[test]
fn test_detect_tls_mode() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "docker.example.com".to_string());
    params.insert("docker-ca-cert".to_string(), "/path/ca.pem".to_string());
    params.insert(
        "docker-client-cert".to_string(),
        "/path/cert.pem".to_string(),
    );
    params.insert("docker-client-key".to_string(), "/path/key.pem".to_string());
    assert_eq!(detect_connection_mode(&params), "TCP with TLS");
}

#[test]
fn test_detect_tls_mode_partial_certs() {
    // Even a single TLS param triggers TLS mode detection
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "docker.example.com".to_string());
    params.insert("docker-ca-cert".to_string(), "/path/ca.pem".to_string());
    assert_eq!(detect_connection_mode(&params), "TCP with TLS");
}

#[test]
fn test_detect_tcp_unencrypted_mode() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "docker.example.com".to_string());
    assert_eq!(detect_connection_mode(&params), "TCP (unencrypted)");
}

#[test]
fn test_detect_socket_mode_default() {
    let params = HashMap::new();
    assert_eq!(detect_connection_mode(&params), "Unix socket");
}

#[test]
fn test_detect_socket_mode_explicit() {
    let mut params = HashMap::new();
    params.insert(
        "docker-socket".to_string(),
        "/run/podman/podman.sock".to_string(),
    );
    assert_eq!(detect_connection_mode(&params), "Unix socket");
}

#[test]
fn test_detect_hostname_takes_priority_over_socket() {
    let mut params = HashMap::new();
    params.insert("hostname".to_string(), "docker.example.com".to_string());
    params.insert(
        "docker-socket".to_string(),
        "/var/run/docker.sock".to_string(),
    );
    // hostname takes priority
    assert_eq!(detect_connection_mode(&params), "TCP (unencrypted)");
}

// -- Constant tests --

#[test]
fn test_default_tls_port() {
    assert_eq!(DEFAULT_TLS_PORT, 2376);
}

#[test]
fn test_default_socket_path() {
    assert_eq!(DEFAULT_SOCKET_PATH, "/var/run/docker.sock");
}

#[test]
fn test_connection_timeout() {
    assert_eq!(CONNECTION_TIMEOUT_SECS, 120);
}

// -- ContainerInfo edge cases --

#[test]
fn test_container_info_empty_fields() {
    let info = ContainerInfo {
        id: String::new(),
        name: String::new(),
        image: String::new(),
        status: String::new(),
        ports: String::new(),
        created: String::new(),
    };
    let row = info.to_row();
    assert_eq!(row.len(), 6);
    for field in &row {
        assert_eq!(field, "");
    }
}

#[test]
fn test_container_info_clone() {
    let info = ContainerInfo {
        id: "abc123def456".to_string(),
        name: "test".to_string(),
        image: "alpine:latest".to_string(),
        status: "Up".to_string(),
        ports: String::new(),
        created: "1 hour ago".to_string(),
    };
    let cloned = info.clone();
    assert_eq!(info.id, cloned.id);
    assert_eq!(info.name, cloned.name);
}

// -- Port formatting edge cases --

#[test]
fn test_format_port_mappings_empty_type() {
    let ports = vec![bollard::models::Port {
        ip: None,
        private_port: 8080,
        public_port: None,
        typ: Some(bollard::models::PortTypeEnum::EMPTY),
    }];
    // EMPTY type produces empty string for proto
    assert_eq!(format_port_mappings(&ports), "8080/");
}

#[test]
fn test_format_port_mappings_localhost_binding() {
    let ports = vec![bollard::models::Port {
        ip: Some("127.0.0.1".to_string()),
        private_port: 5432,
        public_port: Some(5432),
        typ: Some(bollard::models::PortTypeEnum::TCP),
    }];
    assert_eq!(format_port_mappings(&ports), "127.0.0.1:5432->5432/tcp");
}

#[test]
fn test_format_port_mappings_ipv6() {
    let ports = vec![bollard::models::Port {
        ip: Some("::".to_string()),
        private_port: 80,
        public_port: Some(80),
        typ: Some(bollard::models::PortTypeEnum::TCP),
    }];
    assert_eq!(format_port_mappings(&ports), ":::80->80/tcp");
}

#[test]
fn test_format_port_mappings_three_ports() {
    let ports = vec![
        bollard::models::Port {
            ip: Some("0.0.0.0".to_string()),
            private_port: 80,
            public_port: Some(80),
            typ: Some(bollard::models::PortTypeEnum::TCP),
        },
        bollard::models::Port {
            ip: Some("0.0.0.0".to_string()),
            private_port: 443,
            public_port: Some(443),
            typ: Some(bollard::models::PortTypeEnum::TCP),
        },
        bollard::models::Port {
            ip: None,
            private_port: 8443,
            public_port: None,
            typ: Some(bollard::models::PortTypeEnum::TCP),
        },
    ];
    assert_eq!(
        format_port_mappings(&ports),
        "0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp, 8443/tcp"
    );
}
