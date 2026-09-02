"""Nested model classes for Artifact Hosting SDK V2.

These dataclasses represent nested objects within Project and Deployment responses.
All classes support construction from API response dictionaries.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class AccountInfo:
    """Account information (populated by backend).
    
    Attributes:
        account_id: Account identifier.
        team_id: Team identifier (optional).
        member_id: Member identifier (optional).
    """
    account_id: str
    team_id: Optional[str] = None
    member_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountInfo":
        """Create AccountInfo from API response dictionary.
        
        Args:
            data: Dictionary with keys: accountId, teamId, memberId
        
        Returns:
            AccountInfo instance.
        """
        return cls(
            account_id=data.get("accountId", ""),
            team_id=data.get("teamId"),
            member_id=data.get("memberId"),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        result: Dict[str, Any] = {"accountId": self.account_id}
        if self.team_id is not None:
            result["teamId"] = self.team_id
        if self.member_id is not None:
            result["memberId"] = self.member_id
        return result


@dataclass
class Endpoint:
    """Endpoint information for accessing the deployed application.
    
    Attributes:
        default_url: Default URL (e.g., https://{project_name}.novita.space).
        custom_url: Custom domain URL (reserved for future use).
    """
    default_url: Optional[str] = None
    custom_url: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Endpoint":
        """Create Endpoint from API response dictionary.
        
        Args:
            data: Dictionary with keys: defaultUrl, customUrl
        
        Returns:
            Endpoint instance.
        """
        return cls(
            default_url=data.get("defaultUrl"),
            custom_url=data.get("customUrl"),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        result: Dict[str, Any] = {}
        if self.default_url is not None:
            result["defaultUrl"] = self.default_url
        if self.custom_url is not None:
            result["customUrl"] = self.custom_url
        return result


@dataclass
class EndpointConfig:
    """Endpoint configuration settings.
    
    Attributes:
        custom_domain: Custom domain (reserved for future use).
        request_timeout_seconds: Request timeout in seconds.
    """
    custom_domain: Optional[str] = None
    request_timeout_seconds: Optional[int] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EndpointConfig":
        """Create EndpointConfig from API response dictionary.
        
        Args:
            data: Dictionary with keys: customDomain, requestTimeoutSeconds
        
        Returns:
            EndpointConfig instance.
        """
        return cls(
            custom_domain=data.get("customDomain"),
            request_timeout_seconds=data.get("requestTimeoutSeconds"),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        result: Dict[str, Any] = {}
        if self.custom_domain is not None:
            result["customDomain"] = self.custom_domain
        if self.request_timeout_seconds is not None:
            result["requestTimeoutSeconds"] = self.request_timeout_seconds
        return result


@dataclass
class ArtifactsSource:
    """Source of deployment artifacts.
    
    Attributes:
        sandbox_id: ID of the sandbox containing the source code.
        path: Path to the source code directory within the sandbox.
    """
    sandbox_id: str
    path: str
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ArtifactsSource":
        """Create ArtifactsSource from API response dictionary.
        
        Args:
            data: Dictionary with keys: sandboxId, path
        
        Returns:
            ArtifactsSource instance.
        """
        return cls(
            sandbox_id=data.get("sandboxId", ""),
            path=data.get("path", ""),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            "sandboxId": self.sandbox_id,
            "path": self.path,
        }


@dataclass
class ReplicaSpec:
    """Replica resource specification.
    
    Attributes:
        cpu: CPU quota (e.g., "1", "0.5", "2").
        memory: Memory quota (e.g., "512Mi", "1Gi").
        max_replicas: Maximum number of replicas (current version: fixed to 1).
        min_replicas: Minimum number of replicas (current version: fixed to 0).
    """
    cpu: str = "1"
    memory: str = "1Gi"
    max_replicas: int = 1
    min_replicas: int = 0
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReplicaSpec":
        """Create ReplicaSpec from API response dictionary.
        
        Args:
            data: Dictionary with keys: cpu, memory, maxReplicas, minReplicas
        
        Returns:
            ReplicaSpec instance.
        """
        return cls(
            cpu=data.get("cpu", "1"),
            memory=data.get("memory", "1Gi"),
            max_replicas=data.get("maxReplicas", 1),
            min_replicas=data.get("minReplicas", 0),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        return {
            "cpu": self.cpu,
            "memory": self.memory,
            "maxReplicas": self.max_replicas,
            "minReplicas": self.min_replicas,
        }


@dataclass
class DeploymentMetadata:
    """Deployment metadata and configuration.
    
    Attributes:
        environment_variables: Environment variables for the deployment.
        http_port: HTTP port the application listens on (default: 3000).
        check_health_path: HTTP path for health checks (e.g., "/health").
        replica_spec: Replica resource specification.
        database: Whether this deployment requested a project database.
    """
    environment_variables: Dict[str, str] = field(default_factory=dict)
    http_port: int = 3000
    check_health_path: Optional[str] = None
    replica_spec: ReplicaSpec = field(default_factory=ReplicaSpec)
    database: bool = False
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DeploymentMetadata":
        """Create DeploymentMetadata from API response dictionary.
        
        Args:
            data: Dictionary with keys: environmentVariables, httpPort,
                  checkHealthPath, replicaSpec, database
        
        Returns:
            DeploymentMetadata instance.
        """
        replica_spec_data = data.get("replicaSpec", {})
        return cls(
            environment_variables=data.get("environmentVariables", {}),
            http_port=data.get("httpPort", 3000),
            check_health_path=data.get("checkHealthPath"),
            replica_spec=ReplicaSpec.from_dict(replica_spec_data) if replica_spec_data else ReplicaSpec(),
            database=data.get("database", False),
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests."""
        result: Dict[str, Any] = {
            "httpPort": self.http_port,
            "replicaSpec": self.replica_spec.to_dict(),
        }
        if self.environment_variables:
            result["environmentVariables"] = self.environment_variables
        if self.check_health_path is not None:
            result["checkHealthPath"] = self.check_health_path
        if self.database:
            result["database"] = self.database
        return result


@dataclass
class DatabaseInfo:
    """Database information for projects with TiDB Cloud integration.

    Attributes:
        status: Database status (PROVISIONING, ACTIVE, FAILED).
        provider: Database provider (e.g., "tidb_cloud").
        host: Database host.
        port: Database port.
        database_name: Database name.
        database_url: Full connection string.
        created_at: Creation timestamp.
    """

    status: str
    provider: str = "tidb_cloud"
    host: Optional[str] = None
    port: Optional[int] = None
    database_name: Optional[str] = None
    database_url: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatabaseInfo":
        """Create DatabaseInfo from API response dictionary."""
        return cls(
            status=data.get("status", ""),
            provider=data.get("provider", "tidb_cloud"),
            host=data.get("host"),
            port=data.get("port"),
            database_name=data.get("databaseName"),
            database_url=data.get("databaseUrl"),
            created_at=data.get("createdAt"),
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        result: Dict[str, Any] = {
            "status": self.status,
            "provider": self.provider,
        }
        if self.host is not None:
            result["host"] = self.host
        if self.port is not None:
            result["port"] = self.port
        if self.database_name is not None:
            result["databaseName"] = self.database_name
        if self.database_url is not None:
            result["databaseUrl"] = self.database_url
        if self.created_at is not None:
            result["createdAt"] = self.created_at
        return result
