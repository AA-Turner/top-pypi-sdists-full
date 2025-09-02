"""State module for managing Route53 Hosted zones."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    hosted_zone_name: str,
    caller_reference: str,
    resource_id: str = None,
    vpcs: List[
        make_dataclass(
            "VPC",
            [
                ("VPCRegion", str, field(default=None)),
                ("VPCId", str, field(default=None)),
            ],
        )
    ] = None,
    config: make_dataclass(
        "HostedZoneConfig",
        [
            ("Comment", str, field(default=None)),
            ("PrivateZone", bool, field(default=None)),
        ],
    ) = None,
    delegation_set_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates a new public or private hosted zone.

    You create records in a public hosted zone to define how you want to route traffic on the internet for a domain, such
    as example.com, and its subdomains (apex.example.com, acme.example.com). You create records in a private hosted zone
    to define how you want to route traffic for a domain and its subdomains within one or more Amazon Virtual Private Clouds
    (Amazon VPCs). You can't convert a public hosted zone to a private hosted zone or vice versa. Instead, you must
    create a new hosted zone with the same name and create new resource record sets.  For more information about charges
    for hosted zones, see Amazon Route 53 Pricing.

    Note the following: You can't create a hosted zone for a top-level domain (TLD) such as .com.   For public hosted
    zones, Route 53 automatically creates a default SOA record and four NS records for the zone. For more information
    about SOA and NS records, see NS and SOA Records that Route 53 Creates for a Hosted Zone in the Amazon Route 53
    Developer Guide. If you want to use the same name servers for multiple public hosted zones, you can optionally
    associate a reusable delegation set with the hosted zone. See the DelegationSetId element.   If your domain is
    registered with a registrar other than Route 53, you must update the name servers with your registrar to make Route 53
    the DNS service for the domain. For more information, see Migrating DNS Service for an Existing Domain to Amazon
    Route 53 in the Amazon Route 53 Developer Guide. When you submit a CreateHostedZone request, the initial status of
    the hosted zone is PENDING. For public hosted zones, this means that the NS and SOA records are not yet available on
    all Route 53 DNS servers. When the NS and SOA records are available, the status of the zone changes to INSYNC. The
    CreateHostedZone request requires the caller to have an ec2:DescribeVpcs permission.

    Args:
        name(str):
            An Idem name of the hosted zone resource.

        hosted_zone_name(str):
            A unique string that identifies a hosted zone.

        caller_reference(str):
            A unique string that identifies the request and that allows failed CreateHostedZone
            requests to be retried without the risk of executing the operation twice.
            You must use a unique CallerReference string every time you submit a CreateHostedZone request.
            CallerReference can be any unique string, for example, a date/time stamp.,

        resource_id(str, Optional):
            AWS route53 hosted zone ID.

        config(dict[str, Any], Optional):
            A complex type that contains the following optional values:   For public and private
            hosted zones, an optional comment   For private hosted zones, an optional PrivateZone element
            If you don't specify a comment or the PrivateZone element, omit HostedZoneConfig and the other
            elements. Defaults to None.

            * Comment (str, Optional):
                Any comments that you want to include about the hosted zone.
            * PrivateZone (bool, Optional):
                A value that indicates whether this is a private hosted zone.

        vpcs(list, Optional):
            (Private hosted zones only) A list that contains information about the Amazon VPC's that
            you're associating with this hosted zone. If you are associating VPC's with a hosted zone with this request, the
            paramaters VPCId and VPCRegion are also required. To associate additional Amazon VPCs with the
            hosted zone, use AssociateVPCWithHostedZone after you create a hosted zone. Defaults to None.

            * VPCRegion (str, Optional):
                (Private hosted zones only) The region that an Amazon VPC was created in.
            * VPCId (str, Optional):
                (Private hosted zones only) The ID of an Amazon VPC.

        delegation_set_id(str, Optional):
            Id of a reusable delegation set,

        tags(list or dict, Optional):
            list of tags in the format of ``[{"Key": tag-key, "Value": tag-value}]`` or dict in the format of
            ``{tag-key: tag-value}`` The tags to assign to the hosted zone. Defaults to None.

            * Key (str):
                The key of the tag. Tag keys are case-sensitive and accept a maximum of 127 Unicode characters. May not begin with aws: .
            * Value (str):
                The value of the tag. Tag values are case-sensitive and accept a maximum of 255 Unicode characters.


    Request Syntax:
        .. code-block:: sls

            [hosted_zone_id]:
              aws.route53.hosted_zone.present:
                - name: 'string'
                - hosted_zone_name: 'string'
                - resource_id: 'string'
                - caller_reference: 'string'
                - config:
                    PrivateZone: 'string'
                    Comment: 'string'
                - vpcs:
                  - VPCId: 'string'
                    VPCRegion: 'string'
                - delegation_set_id: 'string'
                - tags:
                    - Key: 'string'
                      Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.route53.hosted_zone.present:
                - name: value
                - hosted_zone_name: value
                - resource_id: value
                - caller_reference: value
                - config:
                    PrivateZone: True
                    Comment: 'description of hosted zone config'
                - vpcs:
                    - VPCId: 'vpc id'
                      VPCRegion: 'us-east1'
                - delegation_set_id: 'string'
                - tags:
                    - Key: 'tag key'
                      Value: 'tag value'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.route53.hosted_zone.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        result["comment"] += [f"aws.route53.hosted_zone '{name}' already exists."]
        plan_state = copy.deepcopy(result["old_state"])
        # Check if comments needs to be updated.
        if (
            config is not None
            and config.get("Comment")
            and config.get("Comment") != plan_state["config"].get("Comment")
        ):
            if ctx.get("test", False):
                result["comment"] += [f"Would update aws.route53.hosted_zone '{name}'"]
                resource_updated = True
                plan_state["config"] = config
            else:
                update_ret_comment = (
                    await hub.exec.boto3.client.route53.update_hosted_zone_comment(
                        ctx,
                        Id=resource_id,
                        Comment=config.get("Comment"),
                    )
                )
                if update_ret_comment["result"]:
                    resource_updated = True
                    comment = config.get("Comment")
                    result["comment"] += [f"Updated comment to '{comment}'"]
                else:
                    result["comment"] = update_ret_comment["comment"]
                    result["result"] = False
                    return result

        # Check if tags needs to be updated
        if tags is not None:
            update_ret_tags = await hub.tool.aws.route53.tag.update_tags(
                ctx,
                resource_type="hostedzone",
                resource_id=resource_id,
                old_tags=result["old_state"]["tags"],
                new_tags=tags,
            )
            result["comment"] += update_ret_tags["comment"]
            if not update_ret_tags["result"]:
                result["result"] = False
                return result
            resource_updated = resource_updated or bool(update_ret_tags["ret"])
            if ctx.get("test", False) and update_ret_tags["ret"]:
                plan_state["tags"] = update_ret_tags["ret"]
    else:
        tags_dict = None
        if tags is not None:
            if isinstance(tags, List):
                tags_dict = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
            else:
                tags_dict = tags
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "hosted_zone_name": hosted_zone_name,
                    "caller_reference": caller_reference,
                    "config": config,
                    "vpcs": vpcs,
                    "delegation_set_id": delegation_set_id,
                    "tags": tags_dict,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.route53.hosted_zone", name=name
            )
            return result

        # Private Route53 Hosted Zones can only be created with their first VPC association,
        # however we need to associate the remaining after creation.

        vpc = None
        if vpcs is not None and len(vpcs) > 0:
            vpc = vpcs[0]

        ret = await hub.exec.boto3.client.route53.create_hosted_zone(
            ctx,
            Name=hosted_zone_name,
            VPC=vpc,
            CallerReference=caller_reference,
            HostedZoneConfig=config,
            DelegationSetId=delegation_set_id,
        )
        if not ret["result"]:
            result["result"] = False
            result["comment"] = ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.route53.hosted_zone", name=name
        )
        resource_id = ret["ret"]["HostedZone"]["Id"].split("/")[-1]
        if vpcs is not None and len(vpcs) > 1:
            for i in range(1, len(vpcs)):
                vpc_ret = (
                    await hub.exec.boto3.client.route53.associate_vpc_with_hosted_zone(
                        ctx, HostedZoneId=resource_id, VPC=vpcs[i]
                    )
                )
                if not vpc_ret["result"]:
                    result["result"] = False
                    result["comment"] = vpc_ret["comment"]
                    hub.log.debug(
                        f"Could not associate vpc with hosted zone {vpc_ret['comment']}"
                    )
                    return result
        if tags is not None:
            add_tags = await hub.tool.aws.route53.tag.update_tags(
                ctx,
                resource_type="hostedzone",
                resource_id=resource_id,
                old_tags=None,
                new_tags=tags_dict,
            )
            if not add_tags["result"]:
                error = add_tags["comment"]
                result["result"] = False
                hub.log.debug(
                    f"Tag addition failed for hosted_zone {name} with error {error}"
                )
                result["comment"] += error
                return result

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif result["old_state"] is None or resource_updated:
        after = await hub.exec.aws.route53.hosted_zone.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not after["result"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a hosted zone.

    If the hosted zone was created by another service, such as Cloud Map, see Deleting Public Hosted Zones That Were
    Created by Another Service in the Amazon Route 53 Developer Guide for information about how to delete it.
    (The process is the same for public and private hosted zones that were created by another service.) If you want to
    keep your domain registration but you want to stop routing internet traffic to your website or web application, we
    recommend that you delete resource record sets in the hosted zone instead of deleting the hosted zone.  If you delete
    a hosted zone, you can't undelete it. You must create a new hosted zone and update the name servers for your domain
    registration, which can require up to 48 hours to take effect. (If you delegated responsibility for a subdomain to a
    hosted zone and you delete the child hosted zone, you must update the name servers in the parent hosted zone.)

    In addition, if you delete a hosted zone, someone could hijack the domain and route traffic to their own resources using
    your domain name.  If you want to avoid the monthly charge for the hosted zone, you can transfer DNS service for the
    domain to a free DNS service. When you transfer DNS service, you have to update the name servers for the domain
    registration. If the domain is registered with Route 53, see UpdateDomainNameservers for information about how to replace
    Route 53 name servers with name servers for the new DNS service. If the domain is registered with another registrar,
    use the method provided by the registrar to update name servers for the domain registration.

    For more information, perform an internet search on "free DNS service." You can delete a hosted zone only if it
    contains only the default SOA record and NS resource record sets. If the hosted zone contains other resource record
    sets, you must delete them before you can delete the hosted zone. If you try to delete a hosted zone that contains
    other resource record sets, the request fails, and Route 53 returns a HostedZoneNotEmpty error. For information about
    deleting records from your hosted zone, see ChangeResourceRecordSets. To verify that the hosted zone has been deleted,
    do one of the following:   Use the GetHostedZone action to request information about the hosted zone.   Use the
    ListHostedZones action to get a list of the hosted zones associated with the current Amazon Web Services
    account.

    Args:
        name(str):
            An Idem name of the hosted zone resource.
        resource_id(str, Optional):
            AWS route53 hosted zone ID. Idem automatically considers this resource being absent if this field is not specified.

    Request Syntax:
        .. code-block:: sls

            [hosted-zone-name]:
              aws.route53.hosted_zone.present:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.route53.hosted_zone.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.route53.hosted_zone", name=name
        )
        return result
    before = await hub.exec.aws.route53.hosted_zone.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.route53.hosted_zone", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.route53.hosted_zone", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.route53.delete_hosted_zone(
            ctx, Id=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.route53.hosted_zone", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Retrieves a list of the public and private hosted zones that are associated with the current Amazon Web Services
    account.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.route53.hosted_zone
    """

    result = {}

    ret = await hub.exec.boto3.client.route53.list_hosted_zones(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe hosted_zone {ret['comment']}")
        return result

    for hosted_zone in ret["ret"]["HostedZones"]:
        resource_id = hosted_zone.get("Id")
        name = hosted_zone.get("Name")
        resource_id = resource_id.split("/")[-1]
        resource = await hub.exec.aws.route53.hosted_zone.get(
            ctx, name=name, resource_id=resource_id
        )

        if not resource["result"]:
            hub.log.info(
                f"Failed to retrieve aws.route53.hosted_zone {name}: {resource['comment']}"
            )
            continue

        result[resource_id] = {
            "aws.route53.hosted_zone.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource["ret"].items()
            ]
        }

    return result
