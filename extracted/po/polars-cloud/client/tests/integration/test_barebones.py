# mypy: disable-error-code="return-value,no-untyped-def,no-any-return,no-untyped-call"
import logging
import time
import uuid

import boto3
import polars as pl
import polars_cloud as pc
import pytest
from polars_cloud.constants import API_CLIENT

from .conftest import authenticate  # noqa: TID252

pytestmark = pytest.mark.barebones


logger = logging.getLogger(__name__)


def setup_network(ec2):
    # Create VPC
    vpc = ec2.create_vpc(CidrBlock="10.0.0.0/16")
    vpc_id = vpc["Vpc"]["VpcId"]
    ec2.create_tags(
        Resources=[vpc_id], Tags=[{"Key": "Name", "Value": "test-barebones-vpc"}]
    )
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsSupport={"Value": True})
    ec2.modify_vpc_attribute(VpcId=vpc_id, EnableDnsHostnames={"Value": True})

    # Create and attach Internet Gateway
    igw_id = ec2.create_internet_gateway()["InternetGateway"]["InternetGatewayId"]
    ec2.attach_internet_gateway(InternetGatewayId=igw_id, VpcId=vpc_id)

    # Create Subnet
    az = ec2.describe_availability_zones()["AvailabilityZones"][0]["ZoneName"]
    subnet_id = ec2.create_subnet(
        VpcId=vpc_id, CidrBlock="10.0.1.0/24", AvailabilityZone=az
    )["Subnet"]["SubnetId"]
    ec2.modify_subnet_attribute(SubnetId=subnet_id, MapPublicIpOnLaunch={"Value": True})

    # Create Route Table, add route to IGW, and associate with subnet
    rtb_id = ec2.create_route_table(VpcId=vpc_id)["RouteTable"]["RouteTableId"]
    ec2.create_route(
        RouteTableId=rtb_id, DestinationCidrBlock="0.0.0.0/0", GatewayId=igw_id
    )
    ec2.associate_route_table(RouteTableId=rtb_id, SubnetId=subnet_id)
    return vpc_id, subnet_id


def teardown_network(ec2, vpc_id):
    # Detach and delete Internet Gateway
    igws = ec2.describe_internet_gateways(
        Filters=[{"Name": "attachment.vpc-id", "Values": [vpc_id]}]
    )["InternetGateways"]
    for igw in igws:
        ec2.detach_internet_gateway(
            InternetGatewayId=igw["InternetGatewayId"], VpcId=vpc_id
        )
        ec2.delete_internet_gateway(InternetGatewayId=igw["InternetGatewayId"])

    # Get and delete subnets
    subnets = ec2.describe_subnets(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])[
        "Subnets"
    ]
    for subnet in subnets:
        ec2.delete_subnet(SubnetId=subnet["SubnetId"])

    # Get and delete route tables (skip the main route table)
    rtbs = ec2.describe_route_tables(Filters=[{"Name": "vpc-id", "Values": [vpc_id]}])[
        "RouteTables"
    ]
    for rtb in rtbs:
        if any(assoc.get("Main", False) for assoc in rtb["Associations"]):
            continue
        try:
            ec2.delete_route_table(RouteTableId=rtb["RouteTableId"])
        except ec2.exceptions.ClientError as e:
            if "InvalidRouteTableID.NotFound" not in str(e):
                raise

    # Finally, delete the VPC and retry a couple of times due to async
    for _ in range(5):
        try:
            ec2.delete_vpc(VpcId=vpc_id)
        except:  # noqa: E722
            time.sleep(5)
        else:
            return


def setup_stack(vpc_id, subnet_id) -> pc.Workspace:
    # suffix = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    suffix = str(uuid.uuid4()).split("-")[0]

    organization_name = f"polars-ci-org-{suffix}"
    organization_schema = API_CLIENT.create_organization(organization_name)
    logger.info("Successfully created Organization")

    workspace_name = f"polars-ci-{suffix}"

    workspace_schema = API_CLIENT.create_workspace(
        workspace_name, organization_schema.id
    )
    logger.info("Successfully created workspace in database")

    schema = API_CLIENT.get_workspace_setup_url(workspace_schema.workspace.id)
    url = schema.barebones_template_url

    parameters = [
        {"ParameterKey": "WorkerVPCId", "ParameterValue": vpc_id},
        {"ParameterKey": "PublicSubnetIds", "ParameterValue": subnet_id},
    ]

    cf = boto3.client("cloudformation")
    cf.create_stack(
        StackName=workspace_name,
        TemplateURL=url,
        Capabilities=["CAPABILITY_IAM"],
        Parameters=parameters,
    )
    w = pc.Workspace._from_api_schema(workspace_schema.workspace)
    logger.info("Waiting on workspace deployment")
    w.wait_until_active()
    return w


def teardown_stack(stack_name):
    cf = boto3.client("cloudformation")
    cf.delete_stack(StackName=stack_name)


def run_cluster(w: pc.Workspace):
    ctx = pc.ComputeContext(workspace=w, instance_type="t3.micro")
    ctx.start(wait=True)

    lf = pl.LazyFrame({"a": [1, 2, 3, 4, 5], "b": [9, 9, 9, 0, 0]})
    lf = lf.with_columns(pl.col("a").max().over("b").alias("ab_max"))
    lf.remote(ctx).show()

    ctx.stop()


def all_instances_terminated(workspace_id):
    ec2 = boto3.client("ec2")
    filters = [
        {"Name": "tag:PolarsWorkspaceId", "Values": [str(workspace_id)]},
        {
            "Name": "instance-state-name",
            "Values": ["pending", "running", "stopping", "stopped", "shutting-down"],
        },
    ]
    response = ec2.describe_instances(Filters=filters)
    for reservation in response["Reservations"]:
        for _instance in reservation["Instances"]:
            return False
    return True


def wait_for_termination(workspace_id, timeout=300, interval=15):
    start_time = time.time()

    while time.time() - start_time < timeout:
        if all_instances_terminated(workspace_id):
            logger.info("All instances terminated!")
            return True
        logger.debug("Waiting %s seconds before next check...", interval)
        time.sleep(interval)

    logger.warning("Timeout reached. Some instances are still not terminated.")
    return False


def test_barebones_template(request: pytest.FixtureRequest):
    ec2 = boto3.client("ec2")
    vpc_id, subnet_id = setup_network(ec2)
    authenticate(request)
    try:
        workspace = setup_stack(vpc_id, subnet_id)
        try:
            run_cluster(workspace)
            wait_for_termination(workspace.id)
        finally:
            teardown_stack(workspace.name)
    finally:
        teardown_network(ec2, vpc_id)
