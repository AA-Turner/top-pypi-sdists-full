#![cfg(feature = "vsphere")]
use crate::vsphere::{
    ConsoleTicketJson, HostInfo, HostSummaryJson, PowerState, VSphereClient, VmDetailJson, VmInfo,
    VmSummaryJson,
};
use reqwest::header::CONTENT_TYPE;

// -- PowerState tests --

#[test]
fn test_power_state_display() {
    assert_eq!(PowerState::PoweredOn.to_string(), "POWERED_ON");
    assert_eq!(PowerState::PoweredOff.to_string(), "POWERED_OFF");
    assert_eq!(PowerState::Suspended.to_string(), "SUSPENDED");
}

#[test]
fn test_power_state_from_api_str() {
    assert_eq!(
        PowerState::from_api_str("POWERED_ON"),
        PowerState::PoweredOn
    );
    assert_eq!(
        PowerState::from_api_str("POWERED_OFF"),
        PowerState::PoweredOff
    );
    assert_eq!(PowerState::from_api_str("SUSPENDED"), PowerState::Suspended);
    // Unknown values default to PoweredOff
    assert_eq!(
        PowerState::from_api_str("UNKNOWN_STATE"),
        PowerState::PoweredOff
    );
}

#[test]
fn test_power_state_roundtrip() {
    for state in &[
        PowerState::PoweredOn,
        PowerState::PoweredOff,
        PowerState::Suspended,
    ] {
        let display = state.to_string();
        let parsed = PowerState::from_api_str(&display);
        assert_eq!(&parsed, state);
    }
}

// -- VmInfo tests --

fn sample_vm_info() -> VmInfo {
    VmInfo {
        vm_id: "vm-42".to_string(),
        name: "test-server".to_string(),
        power_state: PowerState::PoweredOn,
        guest_os: "UBUNTU_64".to_string(),
        num_cpus: 4,
        memory_mb: 8192,
    }
}

#[test]
fn test_vm_info_to_row() {
    let vm = sample_vm_info();
    let row = vm.to_row();
    assert_eq!(row.len(), 6);
    assert_eq!(row[0], "vm-42");
    assert_eq!(row[1], "test-server");
    assert_eq!(row[2], "POWERED_ON");
    assert_eq!(row[3], "UBUNTU_64");
    assert_eq!(row[4], "4");
    assert_eq!(row[5], "8192");
}

#[test]
fn test_vm_info_to_row_powered_off() {
    let vm = VmInfo {
        vm_id: "vm-99".to_string(),
        name: "offline-box".to_string(),
        power_state: PowerState::PoweredOff,
        guest_os: "WINDOWS_9_SERVER_64".to_string(),
        num_cpus: 2,
        memory_mb: 4096,
    };
    let row = vm.to_row();
    assert_eq!(row[2], "POWERED_OFF");
    assert_eq!(row[4], "2");
    assert_eq!(row[5], "4096");
}

#[test]
fn test_vm_info_columns() {
    let cols = VmInfo::columns();
    assert_eq!(cols.len(), 6);
    assert_eq!(cols[0].0, "VM ID");
    assert_eq!(cols[1].0, "Name");
    assert_eq!(cols[2].0, "Power State");
    assert_eq!(cols[3].0, "Guest OS");
    assert_eq!(cols[4].0, "CPUs");
    assert_eq!(cols[5].0, "Memory (MB)");
}

#[test]
fn test_vm_info_columns_row_alignment() {
    // The number of columns must match the number of row elements
    let cols = VmInfo::columns();
    let vm = sample_vm_info();
    let row = vm.to_row();
    assert_eq!(cols.len(), row.len());
}

// -- API URL construction --

#[test]
fn test_api_url_construction() {
    let client = VSphereClient {
        client: reqwest::Client::new(),
        base_url: "https://vcenter.example.com".to_string(),
        session_id: Some("test-session-id".to_string()),
    };

    assert_eq!(
        client.api_url("/api/session"),
        "https://vcenter.example.com/api/session"
    );
    assert_eq!(
        client.api_url("/api/vcenter/vm"),
        "https://vcenter.example.com/api/vcenter/vm"
    );
    assert_eq!(
        client.api_url("/api/vcenter/vm/vm-42"),
        "https://vcenter.example.com/api/vcenter/vm/vm-42"
    );
    assert_eq!(
        client.api_url("/api/vcenter/host"),
        "https://vcenter.example.com/api/vcenter/host"
    );
}

#[test]
fn test_api_url_vm_power() {
    let base = "https://vc.local";
    let vm_id = "vm-123";
    let url = format!("{}/api/vcenter/vm/{}/power?action=start", base, vm_id);
    assert_eq!(
        url,
        "https://vc.local/api/vcenter/vm/vm-123/power?action=start"
    );

    let url = format!("{}/api/vcenter/vm/{}/power?action=stop", base, vm_id);
    assert_eq!(
        url,
        "https://vc.local/api/vcenter/vm/vm-123/power?action=stop"
    );
}

#[test]
fn test_api_url_console_tickets() {
    let base = "https://vc.local";
    let vm_id = "vm-456";
    let url = format!("{}/api/vcenter/vm/{}/console/tickets", base, vm_id);
    assert_eq!(
        url,
        "https://vc.local/api/vcenter/vm/vm-456/console/tickets"
    );
}

// -- Session header injection --

#[test]
fn test_auth_headers_with_session() {
    let client = VSphereClient {
        client: reqwest::Client::new(),
        base_url: "https://vcenter.example.com".to_string(),
        session_id: Some("abc-session-123".to_string()),
    };

    let headers = client.auth_headers().unwrap();
    assert_eq!(
        headers
            .get("vmware-api-session-id")
            .unwrap()
            .to_str()
            .unwrap(),
        "abc-session-123"
    );
    assert_eq!(
        headers.get(CONTENT_TYPE).unwrap().to_str().unwrap(),
        "application/json"
    );
}

#[test]
fn test_auth_headers_without_session() {
    let client = VSphereClient {
        client: reqwest::Client::new(),
        base_url: "https://vcenter.example.com".to_string(),
        session_id: None,
    };

    let result = client.auth_headers();
    assert!(result.is_err());
    assert!(result.unwrap_err().contains("Not authenticated"));
}

// -- JSON response parsing --

#[test]
fn test_parse_vm_list_response() {
    let json = r#"[
        {
            "vm": "vm-42",
            "name": "web-server-01",
            "power_state": "POWERED_ON",
            "guest_OS": "UBUNTU_64",
            "cpu_count": 4,
            "memory_size_MiB": 8192
        },
        {
            "vm": "vm-43",
            "name": "db-server-01",
            "power_state": "POWERED_OFF",
            "guest_OS": "RHEL_8_64",
            "cpu_count": 8,
            "memory_size_MiB": 16384
        }
    ]"#;

    let summaries: Vec<VmSummaryJson> = serde_json::from_str(json).unwrap();
    assert_eq!(summaries.len(), 2);

    let vms: Vec<VmInfo> = summaries
        .into_iter()
        .map(|s| VmInfo {
            vm_id: s.vm_id,
            name: s.name,
            power_state: PowerState::from_api_str(&s.power_state),
            guest_os: if s.guest_os.is_empty() {
                "Unknown".to_string()
            } else {
                s.guest_os
            },
            num_cpus: s.cpu_count.unwrap_or(0),
            memory_mb: s.memory_size_mib.unwrap_or(0),
        })
        .collect();

    assert_eq!(vms[0].vm_id, "vm-42");
    assert_eq!(vms[0].name, "web-server-01");
    assert_eq!(vms[0].power_state, PowerState::PoweredOn);
    assert_eq!(vms[0].guest_os, "UBUNTU_64");
    assert_eq!(vms[0].num_cpus, 4);
    assert_eq!(vms[0].memory_mb, 8192);

    assert_eq!(vms[1].vm_id, "vm-43");
    assert_eq!(vms[1].name, "db-server-01");
    assert_eq!(vms[1].power_state, PowerState::PoweredOff);
    assert_eq!(vms[1].guest_os, "RHEL_8_64");
    assert_eq!(vms[1].num_cpus, 8);
    assert_eq!(vms[1].memory_mb, 16384);
}

#[test]
fn test_parse_vm_list_minimal_fields() {
    // The API may omit optional fields
    let json = r#"[
        {
            "vm": "vm-1",
            "name": "minimal",
            "power_state": "POWERED_OFF"
        }
    ]"#;

    let summaries: Vec<VmSummaryJson> = serde_json::from_str(json).unwrap();
    assert_eq!(summaries.len(), 1);
    assert_eq!(summaries[0].vm_id, "vm-1");
    assert_eq!(summaries[0].guest_os, "");
    assert_eq!(summaries[0].cpu_count, None);
    assert_eq!(summaries[0].memory_size_mib, None);
}

#[test]
fn test_parse_vm_detail_response() {
    let json = r#"{
        "name": "web-server-01",
        "guest_OS": "UBUNTU_64",
        "power_state": "POWERED_ON",
        "cpu": {"count": 4},
        "memory": {"size_MiB": 8192},
        "identity": {"ip_address": "10.0.1.50"},
        "host": "host-10",
        "disks": {
            "2000": {
                "label": "Hard disk 1",
                "capacity": 107374182400
            },
            "2001": {
                "label": "Hard disk 2",
                "capacity": 53687091200
            }
        },
        "nics": {
            "4000": {
                "label": "Network adapter 1",
                "mac_address": "00:50:56:ab:cd:ef",
                "backing": {
                    "network": "network-15",
                    "type": "STANDARD_PORTGROUP"
                }
            }
        }
    }"#;

    let detail: VmDetailJson = serde_json::from_str(json).unwrap();
    assert_eq!(detail.name.as_deref(), Some("web-server-01"));
    assert_eq!(detail.guest_os.as_deref(), Some("UBUNTU_64"));
    assert_eq!(detail.power_state.as_deref(), Some("POWERED_ON"));
    assert_eq!(detail.cpu.as_ref().unwrap().count, Some(4));
    assert_eq!(detail.memory.as_ref().unwrap().size_mib, Some(8192));
    assert_eq!(
        detail.identity.as_ref().unwrap().ip_address.as_deref(),
        Some("10.0.1.50")
    );
    assert_eq!(detail.host.as_deref(), Some("host-10"));

    let disks = VSphereClient::parse_disks(&detail.disks);
    assert_eq!(disks.len(), 2);
    let labels: Vec<&str> = disks.iter().map(|d| d.label.as_str()).collect();
    assert!(labels.contains(&"Hard disk 1"));
    assert!(labels.contains(&"Hard disk 2"));

    let nics = VSphereClient::parse_nics(&detail.nics);
    assert_eq!(nics.len(), 1);
    assert_eq!(nics[0].label, "Network adapter 1");
    assert_eq!(nics[0].mac_address, "00:50:56:ab:cd:ef");
    assert_eq!(nics[0].network.as_deref(), Some("network-15"));
}

#[test]
fn test_parse_vm_detail_minimal() {
    let json = r#"{}"#;

    let detail: VmDetailJson = serde_json::from_str(json).unwrap();
    assert!(detail.name.is_none());
    assert!(detail.guest_os.is_none());
    assert!(detail.power_state.is_none());
    assert!(detail.cpu.is_none());
    assert!(detail.memory.is_none());
    assert!(detail.identity.is_none());
    assert!(detail.host.is_none());

    let disks = VSphereClient::parse_disks(&detail.disks);
    assert!(disks.is_empty());

    let nics = VSphereClient::parse_nics(&detail.nics);
    assert!(nics.is_empty());
}

#[test]
fn test_parse_console_ticket_response() {
    let json = r#"{
        "ticket": "cst-VCT-52067f42-7e60-2c44-e87a-))VMware-):f))VM-cert",
        "host": "esxi-01.example.com",
        "port": 443,
        "ssl_thumbprint": "AB:CD:EF:12:34:56:78:90:AB:CD:EF:12:34:56:78:90:AB:CD:EF:20"
    }"#;

    let ticket: ConsoleTicketJson = serde_json::from_str(json).unwrap();
    assert_eq!(
        ticket.ticket,
        "cst-VCT-52067f42-7e60-2c44-e87a-))VMware-):f))VM-cert"
    );
    assert_eq!(ticket.host, "esxi-01.example.com");
    assert_eq!(ticket.port, 443);
    assert!(ticket.ssl_thumbprint.is_some());
}

#[test]
fn test_parse_console_ticket_no_thumbprint() {
    let json = r#"{
        "ticket": "ticket-abc-123",
        "host": "esxi-02.local",
        "port": 902
    }"#;

    let ticket: ConsoleTicketJson = serde_json::from_str(json).unwrap();
    assert_eq!(ticket.ticket, "ticket-abc-123");
    assert_eq!(ticket.host, "esxi-02.local");
    assert_eq!(ticket.port, 902);
    assert!(ticket.ssl_thumbprint.is_none());
}

#[test]
fn test_parse_host_list_response() {
    let json = r#"[
        {
            "host": "host-10",
            "name": "esxi-01.example.com",
            "connection_state": "CONNECTED",
            "power_state": "POWERED_ON"
        },
        {
            "host": "host-11",
            "name": "esxi-02.example.com",
            "connection_state": "DISCONNECTED",
            "power_state": "POWERED_OFF"
        }
    ]"#;

    let summaries: Vec<HostSummaryJson> = serde_json::from_str(json).unwrap();
    assert_eq!(summaries.len(), 2);

    let hosts: Vec<HostInfo> = summaries
        .into_iter()
        .map(|h| HostInfo {
            host_id: h.host_id,
            name: h.name,
            connection_state: h.connection_state,
            power_state: h.power_state,
        })
        .collect();

    assert_eq!(hosts[0].host_id, "host-10");
    assert_eq!(hosts[0].name, "esxi-01.example.com");
    assert_eq!(hosts[0].connection_state, "CONNECTED");
    assert_eq!(hosts[0].power_state, "POWERED_ON");

    assert_eq!(hosts[1].host_id, "host-11");
    assert_eq!(hosts[1].name, "esxi-02.example.com");
    assert_eq!(hosts[1].connection_state, "DISCONNECTED");
    assert_eq!(hosts[1].power_state, "POWERED_OFF");
}

// -- Disk/NIC parsing edge cases --

#[test]
fn test_parse_disks_empty_map() {
    let val = Some(serde_json::json!({}));
    let disks = VSphereClient::parse_disks(&val);
    assert!(disks.is_empty());
}

#[test]
fn test_parse_disks_none() {
    let disks = VSphereClient::parse_disks(&None);
    assert!(disks.is_empty());
}

#[test]
fn test_parse_disks_non_object() {
    let val = Some(serde_json::json!("not an object"));
    let disks = VSphereClient::parse_disks(&val);
    assert!(disks.is_empty());
}

#[test]
fn test_parse_disks_missing_fields() {
    let val = Some(serde_json::json!({
        "2000": {}
    }));
    let disks = VSphereClient::parse_disks(&val);
    assert_eq!(disks.len(), 1);
    assert_eq!(disks[0].label, "Unknown");
    assert_eq!(disks[0].capacity, 0);
}

#[test]
fn test_parse_nics_empty_map() {
    let val = Some(serde_json::json!({}));
    let nics = VSphereClient::parse_nics(&val);
    assert!(nics.is_empty());
}

#[test]
fn test_parse_nics_none() {
    let nics = VSphereClient::parse_nics(&None);
    assert!(nics.is_empty());
}

#[test]
fn test_parse_nics_no_backing() {
    let val = Some(serde_json::json!({
        "4000": {
            "label": "Network adapter 1",
            "mac_address": "00:50:56:00:00:01"
        }
    }));
    let nics = VSphereClient::parse_nics(&val);
    assert_eq!(nics.len(), 1);
    assert_eq!(nics[0].label, "Network adapter 1");
    assert_eq!(nics[0].mac_address, "00:50:56:00:00:01");
    assert!(nics[0].network.is_none());
}

// -- Client state tests --

#[test]
fn test_is_authenticated() {
    let client = VSphereClient {
        client: reqwest::Client::new(),
        base_url: "https://vc.local".to_string(),
        session_id: Some("session-123".to_string()),
    };
    assert!(client.is_authenticated());

    let client = VSphereClient {
        client: reqwest::Client::new(),
        base_url: "https://vc.local".to_string(),
        session_id: None,
    };
    assert!(!client.is_authenticated());
}

#[test]
fn test_base_url() {
    let client = VSphereClient {
        client: reqwest::Client::new(),
        base_url: "https://vcenter.example.com".to_string(),
        session_id: None,
    };
    assert_eq!(client.base_url(), "https://vcenter.example.com");
}

// -- Error handling tests --

#[test]
fn test_parse_vm_list_invalid_json() {
    let json = r#"not valid json"#;
    let result: Result<Vec<VmSummaryJson>, _> = serde_json::from_str(json);
    assert!(result.is_err());
}

#[test]
fn test_parse_vm_detail_invalid_json() {
    let json = r#"[1, 2, 3]"#;
    let result: Result<VmDetailJson, _> = serde_json::from_str(json);
    assert!(result.is_err());
}

#[test]
fn test_parse_console_ticket_missing_required() {
    // Missing "port" should fail
    let json = r#"{
        "ticket": "abc",
        "host": "esxi.local"
    }"#;
    let result: Result<ConsoleTicketJson, _> = serde_json::from_str(json);
    assert!(result.is_err());
}

#[test]
fn test_parse_host_list_empty() {
    let json = r#"[]"#;
    let summaries: Vec<HostSummaryJson> = serde_json::from_str(json).unwrap();
    assert!(summaries.is_empty());
}
