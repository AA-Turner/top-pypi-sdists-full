import json
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

import click
import requests
from click import Context

from tinybird.tb.client import TinyB
from tinybird.tb.modules.cli import CLIException, cli
from tinybird.tb.modules.common import echo_safe_humanfriendly_tables_format_smart_table
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.feedback_manager import FeedbackManager

from .common import ask_for_organization, get_organizations_by_user

K8S_YML = """
---
apiVersion: v1
kind: Namespace
metadata:
  name: %(kubernetes_namespace)s
  labels:
    name: tinybird
---
apiVersion: v1
kind: ServiceAccount
metadata:
  name: tinybird
  namespace:  %(kubernetes_namespace)s
  labels:
    name: tinybird
automountServiceAccountToken: true
---
apiVersion: v1
kind: Service
metadata:
  name: tinybird
  namespace:  %(kubernetes_namespace)s
  labels:
    name: tinybird
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: http
      protocol: TCP
      name: http
  selector:
    name: tinybird
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  namespace: %(kubernetes_namespace)s
  name: tinybird
  annotations:
    external-dns.alpha.kubernetes.io/aws-evaluate-target-health: "false"
    alb.ingress.kubernetes.io/listen-ports: '[{"HTTPS":443}]'
    alb.ingress.kubernetes.io/scheme: internet-facing
    alb.ingress.kubernetes.io/ssl-policy: ELBSecurityPolicy-TLS13-1-2-2021-06
    alb.ingress.kubernetes.io/ssl-redirect: '443'
    alb.ingress.kubernetes.io/target-type: 'ip'
    alb.ingress.kubernetes.io/load-balancer-name: %(kubernetes_namespace)s
    alb.ingress.kubernetes.io/success-codes: '200,301,302'
spec:
  ingressClassName: alb
  tls:
    - hosts:
        - %(full_dns_name)s
  rules:
    - http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: tinybird
                port:
                  name: http
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: tinybird
  namespace: %(kubernetes_namespace)s
spec:
  serviceName: "tinybird"
  replicas: 1
  selector:
    matchLabels:
      name: tinybird
  template:
    metadata:
      labels:
        name: tinybird
    spec:
      serviceAccountName: tinybird
      containers:
        - name: tinybird
          image: "tinybirdco/tinybird-local:beta"
          imagePullPolicy: Always
          ports:
            - name: http
              containerPort: 7181
              protocol: TCP
          env:
            - name: TB_INFRA_TOKEN
              value: "%(infra_token)s"
            - name: TB_INFRA_WORKSPACE
              value: "%(infra_workspace)s"
            - name: TB_INFRA_ORGANIZATION
              value: "%(infra_organization)s"
            - name: TB_INFRA_USER
              value: "%(infra_user)s"
          volumeMounts:
          - name: clickhouse-data
            mountPath: /var/lib/clickhouse
          - name: redis-data
            mountPath: /redis-data
  volumeClaimTemplates:
  - metadata:
      name: clickhouse-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 100Gi%(storage_class_line)s
  - metadata:
      name: redis-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 50Gi%(storage_class_line)s
"""

TERRAFORM_TEMPLATE = """
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "%(aws_region)s"
}

# Get the hosted zone data
data "aws_route53_zone" "selected" {
  name = "%(dns_zone_name)s"
}

# Create ACM certificate
resource "aws_acm_certificate" "cert" {
  domain_name               = "%(dns_record)s.${data.aws_route53_zone.selected.name}"
  validation_method         = "DNS"
  subject_alternative_names = [data.aws_route53_zone.selected.name]

  lifecycle {
    create_before_destroy = true
  }
}

# Create DNS records for certificate validation
resource "aws_route53_record" "cert_validation" {
  for_each = {
    for dvo in aws_acm_certificate.cert.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  allow_overwrite = true
  name            = each.value.name
  records         = [each.value.record]
  ttl             = 60
  type            = each.value.type
  zone_id         = data.aws_route53_zone.selected.zone_id
}

# Certificate validation
resource "aws_acm_certificate_validation" "cert" {
  certificate_arn         = aws_acm_certificate.cert.arn
  validation_record_fqdns = [for record in aws_route53_record.cert_validation : record.fqdn]
}
"""

TERRAFORM_SECOND_TEMPLATE = """
# Create Route 53 record for the load balancer
data "aws_alb" "tinybird" {
  name = "%(kubernetes_namespace)s"
}

resource "aws_route53_record" "tinybird" {
  zone_id = data.aws_route53_zone.selected.zone_id
  name    = "%(full_dns_name)s"
  type    = "A"
  alias {
    name                   = data.aws_alb.tinybird.dns_name
    zone_id                = data.aws_alb.tinybird.zone_id
    evaluate_target_health = true
  }
}

output "tinybird_dns" {
  description = "The DNS name for Tinybird"
  value       = aws_route53_record.tinybird.fqdn
}
"""


class Infrastructure:
    """Class to manage Tinybird infrastructure operations."""

    def __init__(self, client: TinyB):
        self.client = client

    def get_organizations_info(self, config: CLIConfig):
        self.orgs = get_organizations_by_user(config)

    def create_infra(self, name: str, host: str, organization_id: str) -> Dict[str, Any]:
        """Create a new infrastructure."""
        infra = self.client.infra_create(organization_id=organization_id, name=name, host=host)
        return infra

    def list_infras(self) -> None:
        """List all self-managed regions for the admin organization."""

        infras = self.get_infra_list()
        columns = [
            "name",
            "host",
            "organization",
        ]
        table_human_readable = []
        table_machine_readable = []

        for infra in infras:
            name = infra["name"]
            host = infra["host"]
            organization = infra["organization"]

            table_human_readable.append((name, host, organization))
            table_machine_readable.append({"name": name, "host": host, "organization": organization})

        click.echo(FeedbackManager.info(message="\n** Infras:"))
        echo_safe_humanfriendly_tables_format_smart_table(table_human_readable, column_names=columns)
        click.echo("\n")

    def remove_infra(self, name: str):
        try:
            click.echo(FeedbackManager.highlight(message=f"» Deleting infrastructure '{name}' from Tinybird..."))
            infras = self.get_infra_list()
            infra = next((infra for infra in infras if infra["name"] == name), None)
            if not infra:
                raise CLIException(f"Infrastructure '{name}' not found")
            self.client.infra_delete(infra["id"], infra["organization_id"])
            click.echo(FeedbackManager.success(message=f"\n✓ Infrastructure '{name}' deleted"))
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"✗ Error: {e}"))

    def update(self, infra_name: str, name: str, host: str):
        infras_list = self.get_infra_list()
        infra = next((infra for infra in infras_list if infra["name"] == infra_name), None)
        if not infra:
            return None
        self.client.infra_update(
            infra_id=infra["id"],
            organization_id=infra["organization_id"],
            name=name,
            host=host,
        )
        return infra

    def get_infra_list(self) -> List[Dict[str, str]]:
        """Get a list of all infrastructures across organizations.

        Returns:
            List[Dict[str, Any]]: List of infrastructure objects, each containing:
                - id: str
                - name: str
                - host: str
                - organization: str
        """
        try:
            all_infras = []
            for org in self.orgs:
                org_id = org.get("id") or ""
                org_name = org.get("name")
                try:
                    infras = self.client.infra_list(organization_id=org_id)
                    for infra in infras:
                        infra["organization"] = org_name
                        all_infras.append(infra)
                except Exception as e:
                    click.echo(
                        FeedbackManager.warning(message=f"Could not fetch infras for organization {org_name}: {str(e)}")
                    )
                    continue
            return all_infras
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"Failed to list infrastructures: {str(e)}"))
            return []


@cli.group()
@click.pass_context
def infra(ctx: Context) -> None:
    """Infra commands."""
    if "--help" in sys.argv or "-h" in sys.argv:
        return
    client: TinyB = ctx.ensure_object(dict)["client"]
    config = CLIConfig.get_project_config()
    infra = Infrastructure(client)
    infra.get_organizations_info(config)
    ctx.ensure_object(dict)["infra"] = infra


@infra.command(name="init")
@click.option("--name", type=str, help="Name for identifying the self-managed region in Tinybird")
@click.option("--cloud-provider", type=str, help="Infrastructure provider. Possible values are: aws, gcp, azure)")
@click.option("--cloud-region", type=str, help="AWS region, when using aws as the provider")
@click.option("--dns-zone-name", type=str, help="DNS zone name")
@click.option("--dns-record", type=str, help="DNS record name to create, without domain. For example, 'tinybird'")
@click.option("--kubernetes-namespace", type=str, help="Kubernetes namespace for the deployment")
@click.option("--kubernetes-storage-class", type=str, help="Storage class for the k8s StatefulSet")
@click.option(
    "--auto-apply", is_flag=True, help="Automatically apply Terraform and kubectl configuration without prompting"
)
@click.option("--skip-apply", is_flag=True, help="Skip Terraform and kubectl configuration and application")
@click.option("--organization-id", type=str, help="Organization ID for the self-managed region")
@click.pass_context
def infra_init(
    ctx: Context,
    name: str,
    cloud_provider: str,
    cloud_region: Optional[str] = None,
    dns_zone_name: Optional[str] = None,
    kubernetes_namespace: Optional[str] = None,
    dns_record: Optional[str] = None,
    kubernetes_storage_class: Optional[str] = None,
    auto_apply: bool = False,
    skip_apply: bool = False,
    organization_id: Optional[str] = None,
) -> None:
    """Init infra"""
    # Check if provider is specified
    if not cloud_provider:
        click.echo(
            FeedbackManager.error(
                message="✗ Error: --cloud-provider option is required. Specify a cloud provider. Possible values are: aws, gcp, azure."
            )
        )
        return

    # AWS-specific Terraform template creation
    if cloud_provider.lower() != "aws":
        click.echo(FeedbackManager.error(message="✗ Error: Provider not supported yet."))
        return

    # Create infra directory if it doesn't exist
    infra_dir = Path(f"infra/{cloud_provider}")
    infra_dir.mkdir(parents=True, exist_ok=True)
    yaml_path = infra_dir / "k8s.yaml"
    tf_path = infra_dir / "main.tf"
    config_path = infra_dir / "config.json"

    # Load existing configuration if available
    config = {}
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config = json.load(f)
            click.echo(FeedbackManager.info(message="** Loaded existing configuration from config.json"))
        except json.JSONDecodeError:
            click.echo(
                FeedbackManager.warning(
                    message="** Warning: Could not parse existing config.json. Creating a new file..."
                )
            )

    # Generate a random ID for default values
    random_id = str(uuid.uuid4())[:8]

    # Get or prompt for configuration values
    name = name or config.get("name") or click.prompt("** Enter the name for your self-managed region", type=str)
    cloud_region = (
        cloud_region
        or config.get("cloud_region")
        or click.prompt("** Enter the AWS region", default="us-east-1", type=str)
    )
    dns_zone_name = dns_zone_name or config.get("dns_zone_name") or click.prompt("** Enter the DNS zone name", type=str)
    dns_record = (
        dns_record
        or config.get("dns_record")
        or click.prompt("** Enter the DNS record name, without domain", default=f"tinybird-{random_id}", type=str)
    )
    kubernetes_namespace = (
        kubernetes_namespace
        or config.get("kubernetes_namespace")
        or click.prompt("** Enter the Kubernetes namespace", default=f"tinybird-{random_id}", type=str)
    )

    # Special handling for kubernetes_storage_class to handle None values
    if kubernetes_storage_class is not None:
        # Use the provided value
        pass
    elif "kubernetes_storage_class" in config:
        # Use the value from config, even if it's None
        kubernetes_storage_class = config["kubernetes_storage_class"]
    else:
        # Prompt the user
        kubernetes_storage_class = click.prompt(
            "** Enter the Kubernetes storage class (leave empty for None)", default="", show_default=False, type=str
        )
        # Convert empty string to None
        if kubernetes_storage_class == "":
            kubernetes_storage_class = None

    kubernetes_context = config.get("kubernetes_context")

    # Save configuration
    config = {
        "name": name,
        "cloud_provider": cloud_provider,
        "cloud_region": cloud_region,
        "dns_zone_name": dns_zone_name,
        "dns_record": dns_record,
        "kubernetes_namespace": kubernetes_namespace,
        "kubernetes_storage_class": kubernetes_storage_class,
        "kubernetes_context": kubernetes_context,
    }

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

    click.echo(FeedbackManager.info(message=f"** Configuration saved to {config_path}"))

    infra: Infrastructure = ctx.ensure_object(dict)["infra"]
    cli_config = CLIConfig.get_project_config()

    infras = infra.get_infra_list()
    infra_name = next((infra for infra in infras if infra["name"] == name), None)
    if not infra_name:
        # Handle organization if not provided
        organization_id, organization_name = ask_for_organization(infra.orgs, organization_id)
        if not organization_id:
            return
        click.echo(FeedbackManager.highlight(message=f"\n» Creating infrastructure '{name}' in Tinybird..."))
        host = f"https://{dns_record}.{dns_zone_name}"
        infra_obj = infra.create_infra(name, host, organization_id)
    else:
        click.echo(FeedbackManager.highlight(message=f"» Infrastructure '{name}' already exists."))
        if infra_name["host"] != f"https://{dns_record}.{dns_zone_name}":
            click.echo(
                FeedbackManager.highlight(
                    message="» Infrastructure host is different in the current config than the one provisioned at Tinybird"
                )
            )
            if click.confirm("Would you like to update the host in the infra provisioned at Tinybird?"):
                infra.update(infra_name=name, name=name, host=f"https://{dns_record}.{dns_zone_name}")
        organization_name = infra_name["organization"]
        infra_obj = infra_name

    # Write the Terraform template
    terraform_content = TERRAFORM_TEMPLATE % {
        "aws_region": cloud_region,
        "dns_zone_name": dns_zone_name,
        "dns_record": dns_record,
    }

    with open(tf_path, "w") as f:
        f.write(terraform_content.lstrip())

    click.echo(FeedbackManager.info(message=f"** Created Terraform configuration in {tf_path}"))

    # Prepare the storage class line based on whether kubernetes_storage_class is None
    storage_class_line = f"\n      storageClassName: {kubernetes_storage_class}" if kubernetes_storage_class else ""

    new_content = K8S_YML % {
        "kubernetes_namespace": kubernetes_namespace,
        "storage_class_line": storage_class_line,
        "full_dns_name": f"{dns_record}.{dns_zone_name}",
        "infra_token": infra_obj["token"],
        "infra_workspace": cli_config.get("name", ""),
        "infra_organization": organization_name,
        "infra_user": cli_config.get_user_email() or "",
    }

    with open(yaml_path, "w") as f:
        f.write(new_content.lstrip())

    click.echo(FeedbackManager.info(message=f"** Created Kubernetes configuration in {yaml_path}"))

    # Apply Terraform configuration if user confirms
    if not skip_apply:
        # Initialize Terraform
        click.echo(FeedbackManager.info(message="** Initializing Terraform..."))
        command = f"terraform -chdir={infra_dir} init"
        click.echo(FeedbackManager.highlight(message=f"» Executing: {command}"))

        init_result = subprocess.run(["terraform", f"-chdir={infra_dir}", "init"], capture_output=True, text=True)

        if init_result.returncode != 0:
            click.echo(FeedbackManager.error(message="✗ Error: Terraform initialization failed:"))
            click.echo(init_result.stderr)
            return

        # Run terraform plan
        click.echo(FeedbackManager.info(message="** Running Terraform plan..."))
        command = f"terraform -chdir={infra_dir} plan"
        click.echo(FeedbackManager.highlight(message=f"» Executing: {command}"))
        plan_result = subprocess.run(command.split(), capture_output=True, text=True)

        if plan_result.returncode != 0:
            click.echo(FeedbackManager.error(message="✗ Error: Terraform plan failed:"))
            click.echo(format_terraform_error(plan_result.stderr, "TERRAFORM PLAN"))
            return

        # Display formatted plan output
        click.echo(format_terraform_output(plan_result.stdout, "TERRAFORM PLAN"))

        # Apply Terraform configuration if user confirms
        if auto_apply or click.confirm("Would you like to apply the Terraform configuration now?"):
            click.echo(FeedbackManager.info(message="** Applying Terraform configuration..."))
            command = f"terraform -chdir={infra_dir} apply -auto-approve"
            click.echo(FeedbackManager.highlight(message=f"» Executing: {command}"))
            apply_result = subprocess.run(command.split(), capture_output=True, text=True)

            if apply_result.returncode != 0:
                click.echo(FeedbackManager.error(message="✗ Error: Terraform apply failed:"))
                click.echo(format_terraform_error(apply_result.stderr, "TERRAFORM APPLY"))
                return

            # Display formatted apply output
            click.echo(format_terraform_output(apply_result.stdout, "TERRAFORM APPLY"))

        # Prompt to apply the k8s configuration
        if not skip_apply and (
            auto_apply or click.confirm("Would you like to apply the Kubernetes configuration now?")
        ):
            # Get current kubectl context
            command = "kubectl config current-context"
            click.echo(FeedbackManager.highlight(message=f"» Executing: {command}"))
            current_context_result = subprocess.run(command.split(), capture_output=True, text=True)

            current_context = (
                current_context_result.stdout.strip() if current_context_result.returncode == 0 else "unknown"
            )

            # Get available contexts
            command = "kubectl config get-contexts -o name"
            click.echo(FeedbackManager.highlight(message=f"» Executing: {command}"))

            contexts_result = subprocess.run(command.split(), capture_output=True, text=True)

            if contexts_result.returncode != 0:
                click.echo(FeedbackManager.error(message="✗ Error: Failed to get kubectl contexts:"))
                click.echo(contexts_result.stderr)
                return

            available_contexts = [context.strip() for context in contexts_result.stdout.splitlines() if context.strip()]

            if not available_contexts:
                click.echo("No kubectl contexts found. Configure kubectl first.")
                return

            # Prompt user to select a context
            if config["kubernetes_context"]:
                selected_context = config["kubernetes_context"]
                click.echo(f"Using the kubectl context specified in the config: {selected_context}")
            elif len(available_contexts) == 1:
                selected_context = available_contexts[0]
                click.echo(f"Using the only available kubectl context: {selected_context}")
            else:
                click.echo("\nAvailable kubectl contexts:")
                for i, context in enumerate(available_contexts):
                    marker = " (current)" if context == current_context else ""
                    click.echo(f"  {i + 1}. {context}{marker}")

                click.echo("")
                default_index = (
                    available_contexts.index(current_context) + 1 if current_context in available_contexts else 1
                )

                selected_index = click.prompt(
                    "Select kubectl context number to apply configuration",
                    type=click.IntRange(1, len(available_contexts)),
                    default=default_index,
                )

                selected_context = available_contexts[selected_index - 1]
                click.echo(f"Selected context: {selected_context}")

            # Update the config with the selected context
            config["kubernetes_context"] = selected_context
            with open(config_path, "w") as f:
                json.dump(config, f, indent=2)
            click.echo(f"Updated configuration with selected Kubernetes context: {selected_context}")

            # Apply the configuration to the selected context
            click.echo(f"Applying Kubernetes configuration to context '{selected_context}'...")

            # First show a diff of what will be applied
            command = f"kubectl --context {selected_context} diff -f {str(yaml_path)}"
            click.echo(FeedbackManager.highlight(message=f"» Executing: {command}"))

            diff_result = subprocess.run(command.split(), capture_output=True, text=True)

            if diff_result.returncode not in [0, 1]:  # kubectl diff returns 1 when there are differences
                if (
                    "Error from server (NotFound): namespaces" in diff_result.stderr
                    or f'namespace "{kubernetes_namespace}" not found' in diff_result.stderr
                ):
                    click.echo("\nThis appears to be the first deployment - namespace doesn't exist yet.")
                    click.echo("No diff available for the initial deployment.")
                else:
                    click.echo("Failed to get diff for Kubernetes configuration:")
                    click.echo(diff_result.stderr)
            else:
                if diff_result.stdout:
                    click.echo("\nChanges that will be applied:")
                    click.echo(diff_result.stdout)
                else:
                    click.echo("\nNo changes detected or resources don't exist yet.")

            # Now apply the configuration
            command = f"kubectl --context {selected_context} apply -f {str(yaml_path)}"
            click.echo(FeedbackManager.highlight(message=f"» Executing: {command}"))
            apply_result = subprocess.run(command.split(), capture_output=True, text=True)

            if apply_result.returncode != 0:
                click.echo(FeedbackManager.error(message="✗ Error: Failed to apply Kubernetes configuration:"))
                click.echo(apply_result.stderr)
            else:
                click.echo(FeedbackManager.success(message="✓ Kubernetes configuration applied successfully:"))
                click.echo(apply_result.stdout)

                click.echo(FeedbackManager.info(message="Waiting for load balancer and DNS to be provisioned..."))

                max_attempts = 30  # 30 attempts * 10 seconds = 5 minutes
                endpoint_url = f"https://{dns_record}.{dns_zone_name}"

                click.echo(f"Checking endpoint availability: {endpoint_url}")

                for attempt in range(max_attempts):
                    progress = "#" * (attempt + 1)
                    click.echo(
                        f"\rAttempt {attempt + 1}/{max_attempts}: Checking if endpoint is ready... [{progress}]",
                        nl=False,
                    )

                    try:
                        response = requests.get(endpoint_url, allow_redirects=False, timeout=5)
                        if response.status_code < 400:  # Consider any non-error response as success
                            click.echo(
                                "\n" + click.style("✅ HTTPS endpoint is now accessible!", fg="green", bold=True)
                            )
                            break
                    except (requests.RequestException, requests.Timeout):
                        pass

                    if attempt == max_attempts - 1:
                        click.echo(
                            "\n"
                            + click.style("⚠️  HTTPS endpoint not accessible after 5 minutes", fg="yellow", bold=True)
                        )
                        click.echo("  This might be due to DNS propagation or the Load Balancer provisioning delays")
                        click.echo(f"  Try accessing {endpoint_url} manually in a few minutes")
                    else:
                        time.sleep(10)

    if not skip_apply:
        # Print a summary with the endpoint URL
        click.echo("\n" + "=" * 60)
        click.echo("DEPLOYMENT SUMMARY".center(60))
        click.echo("=" * 60)
        click.echo("✅ Load balancer provisioned")

        click.echo(f"\n🔗 Tinybird is available at: https://{dns_record}.{dns_zone_name}")

        click.echo(
            "\n📌 Note: It may take a few minutes for DNS to propagate and the HTTPS certificate to be fully provisioned."
        )


@infra.command(name="rm")
@click.argument("name")
@click.pass_context
def infra_remove(ctx: click.Context, name: str):
    """Delete an infrastructure from Tinybird"""
    infra: Infrastructure = ctx.ensure_object(dict)["infra"]
    infra.remove_infra(name)


@infra.command(name="ls")
@click.pass_context
def infra_list(ctx: click.Context):
    """List self-managed infrastructures"""
    infra: Infrastructure = ctx.ensure_object(dict)["infra"]
    infra.list_infras()


@infra.command(name="add")
@click.option("--name", type=str, help="Name for identifying the self-managed region in Tinybird")
@click.option("--host", type=str, help="Host for the self-managed region")
@click.option("--organization-id", type=str, help="Organization ID for the self-managed region")
@click.pass_context
def infra_add(ctx: click.Context, name: str, host: Optional[str] = None, organization_id: Optional[str] = None):
    """Creates a new self-managed region from an existing infrastructure URL."""
    infra: Infrastructure = ctx.ensure_object(dict)["infra"]

    organization_id, organization_name = ask_for_organization(infra.orgs, organization_id)
    if not organization_id:
        return

    name = name or click.prompt("Enter name", type=str)
    host = host or click.prompt(
        "Enter host URL (e.g., https://tinybird.example.com) (leave empty for None)",
        type=str,
        default="",
        show_default=False,
    )

    click.echo(FeedbackManager.highlight(message=f"» Adding self-managed region '{name}' in Tinybird..."))
    new_infra = infra.create_infra(name, host, organization_id)
    infra_token = new_infra["token"]
    click.echo(
        FeedbackManager.success(message=f"\n✓ Self-managed region '{name}' added in '{organization_name}' Organization")
    )

    # Get CLI config to access workspace and user information
    cli_config = CLIConfig.get_project_config()

    # Print environment variables needed for self-managed infrastructure
    click.echo(FeedbackManager.highlight(message="» Required environment variables:"))
    click.echo(f"TB_INFRA_TOKEN={infra_token}")
    click.echo(f"TB_INFRA_WORKSPACE={cli_config.get('name', '')}")
    click.echo(f"TB_INFRA_ORGANIZATION={organization_name}")
    click.echo(f"TB_INFRA_USER={cli_config.get_user_email() or ''}")


@infra.command(name="update")
@click.argument("infra_name")
@click.option("--name", type=str, help="Name for identifying the self-managed region in Tinybird")
@click.option("--host", type=str, help="Host for the self-managed region")
@click.pass_context
def infra_update(ctx: click.Context, infra_name: str, name: str, host: str):
    """Updates the URL of an existing self-managed region."""
    infra: Infrastructure = ctx.ensure_object(dict)["infra"]
    if not name and not host:
        click.echo(FeedbackManager.warning(message="No name or host provided. Provide either a name or a host."))
        return

    if name or host:
        try:
            click.echo(
                FeedbackManager.highlight(message=f"» Updating self-managed region'{infra_name}' in Tinybird...")
            )
            infra_id = infra.update(infra_name, name, host)
            if not infra_id:
                raise CLIException(f"Self-managed region '{infra_name}' not found")
        except Exception as e:
            click.echo(FeedbackManager.error(message=f"✗ Error: {str(e)}"))


def format_terraform_output(output, command_name="Terraform"):
    """Format Terraform command output with colors and styling.

    Args:
        output: The stdout string from the Terraform command
        command_name: The name of the command (e.g., "PLAN", "APPLY")

    Returns:
        Formatted output ready to be displayed
    """
    if not output:
        return FeedbackManager.info(message=f"No output from {command_name} command.")

    # Add a header
    formatted_lines = [
        "\n" + "=" * 80,
        FeedbackManager.highlight(message=f"{command_name.upper()} OUTPUT"),
        "=" * 80 + "\n",
    ]

    # Process and format the output
    for line in output.splitlines():
        # Highlight resource changes
        if line.strip().startswith("+ "):
            formatted_lines.append(click.style(line, fg="green"))
        elif line.strip().startswith("- "):
            formatted_lines.append(click.style(line, fg="red"))
        elif line.strip().startswith("~ "):
            formatted_lines.append(click.style(line, fg="yellow"))
        # Highlight plan/apply summary
        elif any(keyword in line for keyword in ["Plan:", "Apply complete", "Destroy complete"]):
            formatted_lines.append("\n" + click.style(line, bold=True, fg="cyan"))
        else:
            formatted_lines.append(line)

    # Add a footer
    formatted_lines.append("\n" + "=" * 80)

    return "\n".join(formatted_lines)


def format_terraform_error(error_output, command_name="Terraform"):
    """Format Terraform command error output with colors and styling.

    Args:
        error_output: The stderr string from the Terraform command
        command_name: The name of the command (e.g., "PLAN", "APPLY")

    Returns:
        Formatted error output ready to be displayed
    """
    if not error_output:
        return FeedbackManager.error(message=f"Unknown error in {command_name} command.")

    # Add a header
    formatted_lines = ["\n" + "=" * 80, FeedbackManager.error(message=f"{command_name.upper()} ERROR"), "=" * 80 + "\n"]

    # Process and format the error output
    for line in error_output.splitlines():
        # Highlight error messages
        if any(keyword in line.lower() for keyword in ["error", "failed", "fatal"]):
            formatted_lines.append(click.style(line, fg="red", bold=True))
        # Highlight warnings
        elif any(keyword in line.lower() for keyword in ["warning", "deprecated"]):
            formatted_lines.append(click.style(line, fg="yellow"))
        else:
            formatted_lines.append(line)

    # Add a footer
    formatted_lines.append("\n" + "=" * 80)

    return "\n".join(formatted_lines)
