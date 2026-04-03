// guacr-handlers: vSphere REST API client
//
// Provides a Rust client for the VMware vSphere REST API (vCenter 7.0+).
// Handles session-based authentication, VM lifecycle management, and
// console ticket acquisition for WMKS-based remote display.
//
// All API calls go through reqwest with TLS support. The session ID
// obtained from POST /api/session is injected into every subsequent
// request via the `vmware-api-session-id` header.

use reqwest::header::{HeaderMap, HeaderValue, AUTHORIZATION, CONTENT_TYPE};
use serde::{Deserialize, Serialize};
use std::fmt;

// ---------------------------------------------------------------------------
// Data types
// ---------------------------------------------------------------------------

/// Power state of a virtual machine.
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum PowerState {
    PoweredOn,
    PoweredOff,
    Suspended,
}

impl fmt::Display for PowerState {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            PowerState::PoweredOn => write!(f, "POWERED_ON"),
            PowerState::PoweredOff => write!(f, "POWERED_OFF"),
            PowerState::Suspended => write!(f, "SUSPENDED"),
        }
    }
}

impl PowerState {
    /// Parse from the vSphere API string representation.
    pub(crate) fn from_api_str(s: &str) -> Self {
        match s {
            "POWERED_ON" => PowerState::PoweredOn,
            "POWERED_OFF" => PowerState::PoweredOff,
            "SUSPENDED" => PowerState::Suspended,
            _ => PowerState::PoweredOff,
        }
    }
}

/// Summary information about a virtual machine, as returned by the list endpoint.
#[derive(Debug, Clone)]
pub struct VmInfo {
    pub vm_id: String,
    pub name: String,
    pub power_state: PowerState,
    pub guest_os: String,
    pub num_cpus: u32,
    pub memory_mb: u64,
}

impl VmInfo {
    /// Column definitions for tabular display: (header, width).
    pub fn columns() -> Vec<(&'static str, usize)> {
        vec![
            ("VM ID", 16),
            ("Name", 30),
            ("Power State", 14),
            ("Guest OS", 20),
            ("CPUs", 6),
            ("Memory (MB)", 12),
        ]
    }

    /// Format this VM as a row of strings matching the column order from `columns()`.
    pub fn to_row(&self) -> Vec<String> {
        vec![
            self.vm_id.clone(),
            self.name.clone(),
            self.power_state.to_string(),
            self.guest_os.clone(),
            self.num_cpus.to_string(),
            self.memory_mb.to_string(),
        ]
    }
}

/// Disk information attached to a VM.
#[derive(Debug, Clone, Deserialize)]
pub struct DiskInfo {
    /// Disk label (e.g. "Hard disk 1").
    pub label: String,
    /// Capacity in bytes.
    pub capacity: u64,
}

/// Network interface information attached to a VM.
#[derive(Debug, Clone, Deserialize)]
pub struct NicInfo {
    /// NIC label (e.g. "Network adapter 1").
    pub label: String,
    /// MAC address.
    pub mac_address: String,
    /// Backing network name or ID.
    pub network: Option<String>,
}

/// Detailed information about a virtual machine, including hardware inventory.
#[derive(Debug, Clone)]
pub struct VmDetail {
    pub info: VmInfo,
    pub ip_address: Option<String>,
    pub host: Option<String>,
    pub disks: Vec<DiskInfo>,
    pub nics: Vec<NicInfo>,
}

/// Console ticket for WMKS (WebMKS) remote display connection.
#[derive(Debug, Clone)]
pub struct ConsoleTicket {
    /// The one-time ticket string.
    pub ticket: String,
    /// The ESXi host to connect to.
    pub host: String,
    /// The port for the WMKS connection.
    pub port: u16,
    /// SSL thumbprint of the target host (if available).
    pub ssl_thumbprint: Option<String>,
}

/// Summary information about an ESXi host managed by vCenter.
#[derive(Debug, Clone)]
pub struct HostInfo {
    pub host_id: String,
    pub name: String,
    pub connection_state: String,
    pub power_state: String,
}

// ---------------------------------------------------------------------------
// Internal JSON response shapes (map directly to vSphere REST API JSON)
// ---------------------------------------------------------------------------

/// JSON shape returned by GET /api/vcenter/vm (array element).
#[derive(Deserialize)]
pub(crate) struct VmSummaryJson {
    #[serde(rename = "vm")]
    pub(crate) vm_id: String,
    pub(crate) name: String,
    pub(crate) power_state: String,
    #[serde(default, rename = "guest_OS")]
    pub(crate) guest_os: String,
    #[serde(default)]
    pub(crate) cpu_count: Option<u32>,
    #[serde(default, rename = "memory_size_MiB")]
    pub(crate) memory_size_mib: Option<u64>,
}

/// JSON shape returned by GET /api/vcenter/vm/{vm}.
#[derive(Deserialize)]
pub(crate) struct VmDetailJson {
    #[serde(default)]
    pub(crate) name: Option<String>,
    #[serde(default, rename = "guest_OS")]
    pub(crate) guest_os: Option<String>,
    #[serde(default)]
    pub(crate) power_state: Option<String>,
    #[serde(default)]
    pub(crate) cpu: Option<CpuJson>,
    #[serde(default)]
    pub(crate) memory: Option<MemoryJson>,
    #[serde(default)]
    pub(crate) disks: Option<serde_json::Value>,
    #[serde(default)]
    pub(crate) nics: Option<serde_json::Value>,
    #[serde(default)]
    pub(crate) identity: Option<IdentityJson>,
    #[serde(default)]
    pub(crate) host: Option<String>,
}

#[derive(Deserialize)]
pub(crate) struct CpuJson {
    #[serde(default)]
    pub(crate) count: Option<u32>,
}

#[derive(Deserialize)]
pub(crate) struct MemoryJson {
    #[serde(default, rename = "size_MiB")]
    pub(crate) size_mib: Option<u64>,
}

#[derive(Deserialize)]
pub(crate) struct IdentityJson {
    #[serde(default)]
    pub(crate) ip_address: Option<String>,
}

/// JSON shape returned by POST /api/vcenter/vm/{vm}/console/tickets.
#[derive(Deserialize)]
pub(crate) struct ConsoleTicketJson {
    pub(crate) ticket: String,
    pub(crate) host: String,
    pub(crate) port: u16,
    #[serde(default)]
    pub(crate) ssl_thumbprint: Option<String>,
}

/// JSON shape returned by GET /api/vcenter/host (array element).
#[derive(Deserialize)]
pub(crate) struct HostSummaryJson {
    #[serde(rename = "host")]
    pub(crate) host_id: String,
    pub(crate) name: String,
    pub(crate) connection_state: String,
    pub(crate) power_state: String,
}

// ---------------------------------------------------------------------------
// VSphereClient
// ---------------------------------------------------------------------------

/// Client for the VMware vSphere REST API.
///
/// Manages session-based authentication and provides methods for VM lifecycle
/// management, host enumeration, and console ticket acquisition.
///
/// # Usage
///
/// ```no_run
/// # async fn example() -> Result<(), String> {
/// use guacr_handlers::VSphereClient;
///
/// let mut client = VSphereClient::connect(
///     "vcenter.example.com",
///     "administrator@vsphere.local",
///     "password",
///     true,
/// ).await?;
///
/// let vms = client.list_vms().await?;
/// for vm in &vms {
///     println!("{}: {} ({})", vm.vm_id, vm.name, vm.power_state);
/// }
///
/// client.logout().await?;
/// # Ok(())
/// # }
/// ```
pub struct VSphereClient {
    pub(crate) client: reqwest::Client,
    pub(crate) base_url: String,
    pub(crate) session_id: Option<String>,
}

impl VSphereClient {
    /// Create a new vSphere client and authenticate against the given vCenter host.
    ///
    /// - `hostname`: vCenter FQDN or IP (e.g. "vcenter.example.com")
    /// - `username`: vSphere SSO username (e.g. "administrator@vsphere.local")
    /// - `password`: vSphere SSO password
    /// - `verify_ssl`: whether to verify the server TLS certificate
    pub async fn connect(
        hostname: &str,
        username: &str,
        password: &str,
        verify_ssl: bool,
    ) -> Result<Self, String> {
        let client = reqwest::Client::builder()
            .danger_accept_invalid_certs(!verify_ssl)
            .timeout(std::time::Duration::from_secs(30))
            .build()
            .map_err(|e| format!("Failed to build HTTP client: {}", e))?;

        let base_url = format!("https://{}", hostname);

        let mut instance = VSphereClient {
            client,
            base_url,
            session_id: None,
        };

        instance.authenticate(username, password).await?;
        Ok(instance)
    }

    /// Authenticate via POST /api/session with HTTP Basic auth.
    ///
    /// The vSphere REST API returns a session ID as a plain JSON string in the
    /// response body. This session ID is used for all subsequent requests in the
    /// `vmware-api-session-id` header.
    async fn authenticate(&mut self, username: &str, password: &str) -> Result<(), String> {
        let url = format!("{}/api/session", self.base_url);

        let credentials = format!("{}:{}", username, password);
        let encoded = base64::Engine::encode(
            &base64::engine::general_purpose::STANDARD,
            credentials.as_bytes(),
        );

        let mut headers = HeaderMap::new();
        headers.insert(
            AUTHORIZATION,
            HeaderValue::from_str(&format!("Basic {}", encoded))
                .map_err(|e| format!("Invalid auth header: {}", e))?,
        );
        headers.insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));

        let response = self
            .client
            .post(&url)
            .headers(headers)
            .send()
            .await
            .map_err(|e| format!("Authentication request failed: {}", e))?;

        let status = response.status();
        if !status.is_success() {
            let body = response
                .text()
                .await
                .unwrap_or_else(|_| String::from("<no body>"));
            return Err(format!(
                "Authentication failed (HTTP {}): {}",
                status.as_u16(),
                body
            ));
        }

        // The session ID comes back as a JSON string (quoted).
        let session_id: String = response
            .json()
            .await
            .map_err(|e| format!("Failed to parse session ID: {}", e))?;

        if session_id.is_empty() {
            return Err("Server returned empty session ID".to_string());
        }

        self.session_id = Some(session_id);
        Ok(())
    }

    /// Build the standard headers for an authenticated API request.
    pub(crate) fn auth_headers(&self) -> Result<HeaderMap, String> {
        let session_id = self
            .session_id
            .as_ref()
            .ok_or_else(|| "Not authenticated (no session ID)".to_string())?;

        let mut headers = HeaderMap::new();
        headers.insert(
            "vmware-api-session-id",
            HeaderValue::from_str(session_id)
                .map_err(|e| format!("Invalid session ID header value: {}", e))?,
        );
        headers.insert(CONTENT_TYPE, HeaderValue::from_static("application/json"));
        Ok(headers)
    }

    /// Build the full URL for an API path (e.g. "/api/vcenter/vm").
    pub(crate) fn api_url(&self, path: &str) -> String {
        format!("{}{}", self.base_url, path)
    }

    /// List all virtual machines managed by vCenter.
    ///
    /// Calls GET /api/vcenter/vm and returns a vector of `VmInfo` summaries.
    pub async fn list_vms(&self) -> Result<Vec<VmInfo>, String> {
        let url = self.api_url("/api/vcenter/vm");
        let headers = self.auth_headers()?;

        let response = self
            .client
            .get(&url)
            .headers(headers)
            .send()
            .await
            .map_err(|e| format!("Failed to list VMs: {}", e))?;

        let status = response.status();
        if !status.is_success() {
            let body = response
                .text()
                .await
                .unwrap_or_else(|_| String::from("<no body>"));
            return Err(format!(
                "List VMs failed (HTTP {}): {}",
                status.as_u16(),
                body
            ));
        }

        let summaries: Vec<VmSummaryJson> = response
            .json()
            .await
            .map_err(|e| format!("Failed to parse VM list: {}", e))?;

        let vms = summaries
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

        Ok(vms)
    }

    /// Get detailed information about a specific VM.
    ///
    /// Calls GET /api/vcenter/vm/{vm} and returns hardware details including
    /// disks, NICs, IP address, and host placement.
    pub async fn get_vm(&self, vm_id: &str) -> Result<VmDetail, String> {
        let url = self.api_url(&format!("/api/vcenter/vm/{}", vm_id));
        let headers = self.auth_headers()?;

        let response = self
            .client
            .get(&url)
            .headers(headers)
            .send()
            .await
            .map_err(|e| format!("Failed to get VM {}: {}", vm_id, e))?;

        let status = response.status();
        if !status.is_success() {
            let body = response
                .text()
                .await
                .unwrap_or_else(|_| String::from("<no body>"));
            return Err(format!(
                "Get VM failed (HTTP {}): {}",
                status.as_u16(),
                body
            ));
        }

        let detail: VmDetailJson = response
            .json()
            .await
            .map_err(|e| format!("Failed to parse VM detail: {}", e))?;

        let disks = Self::parse_disks(&detail.disks);
        let nics = Self::parse_nics(&detail.nics);

        let info = VmInfo {
            vm_id: vm_id.to_string(),
            name: detail.name.unwrap_or_else(|| "Unknown".to_string()),
            power_state: PowerState::from_api_str(
                detail.power_state.as_deref().unwrap_or("POWERED_OFF"),
            ),
            guest_os: detail.guest_os.unwrap_or_else(|| "Unknown".to_string()),
            num_cpus: detail.cpu.and_then(|c| c.count).unwrap_or(0),
            memory_mb: detail.memory.and_then(|m| m.size_mib).unwrap_or(0),
        };

        let ip_address = detail.identity.and_then(|id| id.ip_address);

        Ok(VmDetail {
            info,
            ip_address,
            host: detail.host,
            disks,
            nics,
        })
    }

    /// Parse the disks map from the vSphere JSON response.
    ///
    /// The vSphere API returns disks as a JSON object keyed by disk ID (e.g.
    /// `{"2000": {"label": "Hard disk 1", "capacity": 10737418240}}`).
    pub(crate) fn parse_disks(disks_value: &Option<serde_json::Value>) -> Vec<DiskInfo> {
        let Some(value) = disks_value else {
            return Vec::new();
        };
        let Some(obj) = value.as_object() else {
            return Vec::new();
        };

        let mut result = Vec::with_capacity(obj.len());
        for (_key, disk_val) in obj {
            let label = disk_val
                .get("label")
                .and_then(|v| v.as_str())
                .unwrap_or("Unknown")
                .to_string();
            let capacity = disk_val
                .get("capacity")
                .and_then(|v| v.as_u64())
                .unwrap_or(0);
            result.push(DiskInfo { label, capacity });
        }
        result
    }

    /// Parse the NICs map from the vSphere JSON response.
    ///
    /// The vSphere API returns NICs as a JSON object keyed by NIC ID (e.g.
    /// `{"4000": {"label": "Network adapter 1", "mac_address": "00:50:56:...", ...}}`).
    pub(crate) fn parse_nics(nics_value: &Option<serde_json::Value>) -> Vec<NicInfo> {
        let Some(value) = nics_value else {
            return Vec::new();
        };
        let Some(obj) = value.as_object() else {
            return Vec::new();
        };

        let mut result = Vec::with_capacity(obj.len());
        for (_key, nic_val) in obj {
            let label = nic_val
                .get("label")
                .and_then(|v| v.as_str())
                .unwrap_or("Unknown")
                .to_string();
            let mac_address = nic_val
                .get("mac_address")
                .and_then(|v| v.as_str())
                .unwrap_or("00:00:00:00:00:00")
                .to_string();
            let network = nic_val
                .get("backing")
                .and_then(|b| b.get("network"))
                .and_then(|v| v.as_str())
                .map(|s| s.to_string());
            result.push(NicInfo {
                label,
                mac_address,
                network,
            });
        }
        result
    }

    /// Power on a virtual machine.
    ///
    /// Calls POST /api/vcenter/vm/{vm}/power?action=start.
    pub async fn power_on(&self, vm_id: &str) -> Result<(), String> {
        self.power_action(vm_id, "start").await
    }

    /// Power off a virtual machine.
    ///
    /// Calls POST /api/vcenter/vm/{vm}/power?action=stop.
    pub async fn power_off(&self, vm_id: &str) -> Result<(), String> {
        self.power_action(vm_id, "stop").await
    }

    /// Execute a VM power action (start, stop, suspend, reset).
    async fn power_action(&self, vm_id: &str, action: &str) -> Result<(), String> {
        let url = format!(
            "{}/api/vcenter/vm/{}/power?action={}",
            self.base_url, vm_id, action
        );
        let headers = self.auth_headers()?;

        let response = self
            .client
            .post(&url)
            .headers(headers)
            .send()
            .await
            .map_err(|e| format!("Power {} for VM {} failed: {}", action, vm_id, e))?;

        let status = response.status();
        if !status.is_success() {
            let body = response
                .text()
                .await
                .unwrap_or_else(|_| String::from("<no body>"));
            return Err(format!(
                "Power {} failed (HTTP {}): {}",
                action,
                status.as_u16(),
                body
            ));
        }

        Ok(())
    }

    /// Acquire a console ticket for WMKS (Web Machine Key Sequence) remote display.
    ///
    /// Calls POST /api/vcenter/vm/{vm}/console/tickets with a WEBMKS ticket type.
    /// The returned ticket, host, and port can be used to establish a WebSocket
    /// connection for remote console access.
    pub async fn get_console_ticket(&self, vm_id: &str) -> Result<ConsoleTicket, String> {
        let url = self.api_url(&format!("/api/vcenter/vm/{}/console/tickets", vm_id));
        let headers = self.auth_headers()?;

        let body = serde_json::json!({
            "spec": {
                "type": "WEBMKS"
            }
        });

        let response = self
            .client
            .post(&url)
            .headers(headers)
            .json(&body)
            .send()
            .await
            .map_err(|e| format!("Get console ticket for VM {} failed: {}", vm_id, e))?;

        let status = response.status();
        if !status.is_success() {
            let body_text = response
                .text()
                .await
                .unwrap_or_else(|_| String::from("<no body>"));
            return Err(format!(
                "Console ticket request failed (HTTP {}): {}",
                status.as_u16(),
                body_text
            ));
        }

        let ticket_json: ConsoleTicketJson = response
            .json()
            .await
            .map_err(|e| format!("Failed to parse console ticket: {}", e))?;

        Ok(ConsoleTicket {
            ticket: ticket_json.ticket,
            host: ticket_json.host,
            port: ticket_json.port,
            ssl_thumbprint: ticket_json.ssl_thumbprint,
        })
    }

    /// List all ESXi hosts managed by vCenter.
    ///
    /// Calls GET /api/vcenter/host and returns a vector of `HostInfo` summaries.
    pub async fn list_hosts(&self) -> Result<Vec<HostInfo>, String> {
        let url = self.api_url("/api/vcenter/host");
        let headers = self.auth_headers()?;

        let response = self
            .client
            .get(&url)
            .headers(headers)
            .send()
            .await
            .map_err(|e| format!("Failed to list hosts: {}", e))?;

        let status = response.status();
        if !status.is_success() {
            let body = response
                .text()
                .await
                .unwrap_or_else(|_| String::from("<no body>"));
            return Err(format!(
                "List hosts failed (HTTP {}): {}",
                status.as_u16(),
                body
            ));
        }

        let summaries: Vec<HostSummaryJson> = response
            .json()
            .await
            .map_err(|e| format!("Failed to parse host list: {}", e))?;

        let hosts = summaries
            .into_iter()
            .map(|h| HostInfo {
                host_id: h.host_id,
                name: h.name,
                connection_state: h.connection_state,
                power_state: h.power_state,
            })
            .collect();

        Ok(hosts)
    }

    /// Terminate the vSphere session.
    ///
    /// Calls DELETE /api/session. After logout, the client can no longer make
    /// authenticated requests. It is safe to call logout multiple times.
    pub async fn logout(&mut self) -> Result<(), String> {
        if self.session_id.is_none() {
            return Ok(());
        }

        let url = self.api_url("/api/session");
        let headers = self.auth_headers()?;

        let response = self
            .client
            .delete(&url)
            .headers(headers)
            .send()
            .await
            .map_err(|e| format!("Logout request failed: {}", e))?;

        let status = response.status();
        // Clear session regardless of response -- the session may have already
        // expired on the server side.
        self.session_id = None;

        if !status.is_success() {
            let body = response
                .text()
                .await
                .unwrap_or_else(|_| String::from("<no body>"));
            return Err(format!(
                "Logout failed (HTTP {}): {}",
                status.as_u16(),
                body
            ));
        }

        Ok(())
    }

    /// Returns the base URL this client is configured to use.
    pub fn base_url(&self) -> &str {
        &self.base_url
    }

    /// Returns true if the client currently holds a valid session ID.
    pub fn is_authenticated(&self) -> bool {
        self.session_id.is_some()
    }
}
