async def get_dhcp_vpc_association_details(hub, ctx, dhcp_id: str, vpc_id: str):
    result = dict(comment=[], result=True, ret=None)
    vpc_ret = await hub.exec.boto3.client.ec2.describe_vpcs(ctx, VpcIds=[vpc_id])
    if not vpc_ret["result"]:
        result["comment"] = vpc_ret["comment"]
        result["result"] = vpc_ret["result"]
        return result

    for vpc_dhcp in vpc_ret["ret"]["Vpcs"]:
        if vpc_dhcp.get("VpcId") == vpc_id and vpc_dhcp["DhcpOptionsId"] == dhcp_id:
            result["ret"] = vpc_dhcp
            return result
    result["result"] = False
    return result
