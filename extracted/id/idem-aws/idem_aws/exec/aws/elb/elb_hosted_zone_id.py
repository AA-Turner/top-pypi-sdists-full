"""Exec module to get AWS ELB route53 Hosted Zone ID based on the region specified"""
from typing import Any
from typing import Dict

AWS_REGION_TO_HOSTED_ZONE_MAP = {
    "af-south-1": "Z268VQBMOI5EKX",
    "ap-east-1": "Z3DQVH9N71FHZ0",
    "ap-northeast-1": "Z14GRHDCWA56QT",
    "ap-northeast-2": "ZWKZPGTI48KDX",
    "ap-northeast-3": "Z5LXEXXYW11ES",
    "ap-south-1": "ZP97RAFLXTNZK",
    "ap-southeast-1": "Z1LMS91P8CMLE5",
    "ap-southeast-2": "Z1GM3OXH4ZPM65",
    "ap-southeast-3": "Z08888821HLRG5A9ZRTER",
    "ca-central-1": "ZQSVJUPU6J1EY",
    "cn-north-1": "Z1GDH35T77C1KE",
    "cn-northwest-1": "ZM7IZAIOVVDZF",
    "eu-central-1": "Z215JYRZR1TBD5",
    "eu-north-1": "Z23TAZ6LKFMNIO",
    "eu-south-1": "Z3ULH7SSC9OV64",
    "eu-west-1": "Z32O12XQLNTSW2",
    "eu-west-2": "ZHURV8PSTC4K8",
    "eu-west-3": "Z3Q77PNBQS71R4",
    "me-south-1": "ZS929ML54UICD",
    "sa-east-1": "Z2P70J7HTTTPLU",
    "us-east-1": "Z35SXDOTRQ7X7K",
    "us-east-2": "Z3AADJGX6KTTL2",
    "us-gov-east-1": "Z166TLBEWOO7G0",
    "us-gov-west-1": "Z33AYJ8TM3BH4J",
    "us-west-1": "Z368ELLRRE2KJ0",
    "us-west-2": "Z1H1FL5HABSF5",
    "eu-south-2": "Z0956581394HF5D5LXGAP",
    "eu-central-2": "Z06391101F2ZOEP8P5EB3",
    "ap-south-2": "Z0173938T07WNTVAEPZN",
    "me-central-1": "Z08230872XQRWHG2XF6I",
}


async def get(hub, ctx, name, region: str = None) -> Dict[str, Any]:
    """
    Returns the AWS ELB route53 Hosted Zone ID of the current region whose credentials are used to call the operation.
    Refer-: https://docs.aws.amazon.com/general/latest/gr/elb.html

    Args:
        name(str): An Idem name of the resource.
        region(str, Optional): AWS region for which ELB route53 Hosted Zone ID is required.
            If not specified region specified in credentials file will be used.

    Request Syntax:
        [Idem-resource-state-name]:
          exec.run:
          - path: aws.elb.elb_hosted_zone_id.get
          - kwargs:
              region: 'string'

    Examples:

        my-elb-hosted_zone-id:
          exec.run:
            - path: aws.elb.elb_hosted_zone_id.get
            - kwargs:
                region: us-west-2

    Response Syntax:
          {
            'elb_hosted_zone_id': 'string',
            'name': 'string'
          }

    Response Structure:
        name(str): An Idem name of the resource.
        elb_hosted_zone_id(str): AWS ELB route53 Hosted Zone ID of the AWS region used in credentials

    """
    result = dict(comment=[], ret=None, result=True)
    region = region or ctx["acct"].get("region_name")
    region_elb_hosted_zone_id = AWS_REGION_TO_HOSTED_ZONE_MAP.get(region)
    if not region_elb_hosted_zone_id:
        result["result"] = False
        result["comment"] = [
            f"AWS ELB route53 Hosted Zone ID not found for region {region}"
        ]
        return result
    resource_translated = {
        "name": name,
        "elb_hosted_zone_id": region_elb_hosted_zone_id,
    }

    result["ret"] = resource_translated
    return result
