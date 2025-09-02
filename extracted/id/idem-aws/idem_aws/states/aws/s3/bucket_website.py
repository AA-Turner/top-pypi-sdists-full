"""State module for managing AWS S3 bucket website."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools import data

__contracts__ = ["resource"]

STATE_NAME = "aws.s3.bucket_website"


async def present(
    hub,
    ctx,
    name: str,
    bucket: str,
    website_configuration: make_dataclass(
        "WebsiteConfiguration",
        [
            (
                "ErrorDocument",
                make_dataclass("ErrorDocument", [("Key", str)]),
                field(default=None),
            ),
            (
                "IndexDocument",
                make_dataclass("IndexDocument", [("Suffix", str)]),
                field(default=None),
            ),
            (
                "RedirectAllRequestsTo",
                make_dataclass(
                    "RedirectAllRequestsTo",
                    [("HostName", str), ("Protocol", str, field(default=None))],
                ),
                field(default=None),
            ),
            (
                "RoutingRules",
                List[
                    make_dataclass(
                        "RoutingRule",
                        [
                            (
                                "Redirect",
                                make_dataclass(
                                    "Redirect",
                                    [
                                        ("HostName", str, field(default=None)),
                                        ("HttpRedirectCode", str, field(default=None)),
                                        ("Protocol", str, field(default=None)),
                                        (
                                            "ReplaceKeyPrefixWith",
                                            str,
                                            field(default=None),
                                        ),
                                        ("ReplaceKeyWith", str, field(default=None)),
                                    ],
                                ),
                            ),
                            (
                                "Condition",
                                make_dataclass(
                                    "Condition",
                                    [
                                        (
                                            "HttpErrorCodeReturnedEquals",
                                            str,
                                            field(default=None),
                                        ),
                                        ("KeyPrefixEquals", str, field(default=None)),
                                    ],
                                ),
                                field(default=None),
                            ),
                        ],
                    )
                ],
                field(default=None),
            ),
        ],
    ),
    resource_id: str = None,
    checksum_algorithm: str = None,
    expected_bucket_owner: str = None,
) -> Dict[str, Any]:
    """Sets the configuration of the website that is specified in the website subresource. To configure a bucket as a
    website, you can add this subresource on the bucket with website configuration information such as the file name
    of the index document and any redirect rules. For more information, see Hosting Websites on Amazon S3. This PUT
    action requires the S3:PutBucketWebsite permission. By default, only the bucket owner can configure the website
    attached to a bucket; however, bucket owners can allow other users to set the website configuration by writing a
    bucket policy that grants them the S3:PutBucketWebsite permission. To redirect all website requests sent to the
    bucket's website endpoint, you add a website configuration with the following elements. Because all requests are
    sent to another website, you don't need to provide index document name for the bucket.    WebsiteConfiguration
    RedirectAllRequestsTo     HostName     Protocol    If you want granular control over redirects, you can use the
    following elements to add routing rules that describe conditions for redirecting requests and information about
    the redirect destination. In this case, the website configuration must provide an index document for the bucket,
    because some requests might not be redirected.     WebsiteConfiguration     IndexDocument     Suffix
    ErrorDocument     Key     RoutingRules     RoutingRule     Condition     HttpErrorCodeReturnedEquals
    KeyPrefixEquals     Redirect     Protocol     HostName     ReplaceKeyPrefixWith     ReplaceKeyWith
    HttpRedirectCode    Amazon S3 has a limitation of 50 routing rules per website configuration. If you require
    more than 50 routing rules, you can use object redirect. For more information, see Configuring an Object
    Redirect in the Amazon S3 User Guide.

        Args:
            name(str):
                An Idem name of the resource.

            bucket(str):
                The bucket name.

            resource_id(str, Optional):
                The bucket name.

            checksum_algorithm(str, Optional):
                Indicates the algorithm used to create the checksum for the object when using the SDK. This
                header will not provide any additional functionality if not using the SDK. When sending this
                header, there must be a corresponding x-amz-checksum or x-amz-trailer header sent. Otherwise,
                Amazon S3 fails the request with the HTTP status code 400 Bad Request. For more information, see
                Checking object integrity in the Amazon S3 User Guide. If you provide an individual checksum,
                Amazon S3 ignores any provided ChecksumAlgorithm parameter. Defaults to None.

            website_configuration(Dict[str, Any]):
                Container for the request.

                * ErrorDocument (dict[str, any], Optional):
                    The name of the error document for the website.

                    * Key (str):
                        The object key name to use when a 4XX class error occurs.  Replacement must be made for object
                keys containing special characters (such as carriage returns) when using XML requests. For more
                information, see  XML related object key constraints.

                * IndexDocument (dict[str, any], Optional):
                    The name of the index document for the website.

                    * Suffix (str):
                        A suffix that is appended to a request that is for a directory on the website endpoint (for
                example,if the suffix is index.html and you make a request to samplebucket/images/ the data that
                is returned will be for the object with the key name images/index.html) The suffix must not be
                empty and must not include a slash character.  Replacement must be made for object keys
                containing special characters (such as carriage returns) when using XML requests. For more
                information, see  XML related object key constraints.

                * RedirectAllRequestsTo (dict[str, any], Optional):
                    The redirect behavior for every request to this bucket's website endpoint.  If you specify this
                property, you can't specify any other property.

                    * HostName (str):
                        Name of the host where requests are redirected.

                    * Protocol (str, Optional):
                        Protocol to use when redirecting requests. The default is the protocol that is used in the
                original request.

                * RoutingRules (list[dict[str, any]], Optional):
                    Rules that define when a redirect is applied and the redirect behavior.

                    * Condition (dict[str, any], Optional):
                        A container for describing a condition that must be met for the specified redirect to apply. For
                example, 1. If request is for pages in the /docs folder, redirect to the /documents folder. 2.
                If request results in HTTP error 4xx, redirect request to another host where you might process
                the error.

                        * HttpErrorCodeReturnedEquals (str, Optional):
                            The HTTP error code when the redirect is applied. In the event of an error, if the error code
                equals this value, then the specified redirect is applied. Required when parent element
                Condition is specified and sibling KeyPrefixEquals is not specified. If both are specified, then
                both must be true for the redirect to be applied.

                        * KeyPrefixEquals (str, Optional):
                            The object key name prefix when the redirect is applied. For example, to redirect requests for
                ExamplePage.html, the key prefix will be ExamplePage.html. To redirect request for all pages
                with the prefix docs/, the key prefix will be /docs, which identifies all objects in the docs/
                folder. Required when the parent element Condition is specified and sibling
                HttpErrorCodeReturnedEquals is not specified. If both conditions are specified, both must be
                true for the redirect to be applied.  Replacement must be made for object keys containing
                special characters (such as carriage returns) when using XML requests. For more information, see
                XML related object key constraints.

                    * Redirect (dict[str, any]):
                        Container for redirect information. You can redirect requests to another host, to another page,
                or with another protocol. In the event of an error, you can specify a different error code to
                return.

                        * HostName (str, Optional):
                            The host name to use in the redirect request.

                        * HttpRedirectCode (str, Optional):
                            The HTTP redirect code to use on the response. Not required if one of the siblings is present.

                        * Protocol (str, Optional):
                            Protocol to use when redirecting requests. The default is the protocol that is used in the
                original request.

                        * ReplaceKeyPrefixWith (str, Optional):
                            The object key prefix to use in the redirect request. For example, to redirect requests for all
                pages with prefix docs/ (objects in the docs/ folder) to documents/, you can set a condition
                block with KeyPrefixEquals set to docs/ and in the Redirect set ReplaceKeyPrefixWith to
                /documents. Not required if one of the siblings is present. Can be present only if
                ReplaceKeyWith is not provided.  Replacement must be made for object keys containing special
                characters (such as carriage returns) when using XML requests. For more information, see  XML
                related object key constraints.

                        * ReplaceKeyWith (str, Optional):
                            The specific object key to use in the redirect request. For example, redirect request to
                error.html. Not required if one of the siblings is present. Can be present only if
                ReplaceKeyPrefixWith is not provided.  Replacement must be made for object keys containing
                special characters (such as carriage returns) when using XML requests. For more information, see
                XML related object key constraints.

            expected_bucket_owner(str, Optional):
                The account ID of the expected bucket owner. If the bucket is owned by a different account, the
                request fails with the HTTP status code 403 Forbidden (access denied). Defaults to None.

        Request Syntax:
            .. code-block:: sls

                resource_is_present:
                  aws.s3.bucket_website.present:
                    - name: "str"
                    - resource_id: "str"
                    - bucket: "string"
                    - checksum_algorithm: "string"
                    - website_configuration: "Dict"
                    - expected_bucket_owner: "string"

        Returns:
            Dict[str, Any]


        Examples:
            .. code-block:: sls

                resource_is_present:
                  aws.s3.bucket_website.present:
                    - name: value
                    - bucket: value
                    - website_configuration:
                        ErrorDocument:
                            Key: "index.html"
                        IndexDocument:
                            Suffix: "index.html"
                        RedirectAllRequestsTo:
                            HostName: 'test.com'
                            Protocol: https
                        RoutingRules:
                            Condition:
                                HttpErrorCodeReturnedEquals: '400'
                                KeyPrefixEquals: 'test'
                            Redirect:
                                HostName: 'test.example.com'
                                HttpRedirectCode: 500
                                Protocol: https
                                ReplaceKeyPrefixWith: 'test1'
                                ReplaceKeyWith: 'test'


    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    if resource_id:
        if resource_id != bucket:
            result["result"] = False
            result["comment"].append(
                f"Bucket '{bucket}' and resource_id '{resource_id}' parameters must be the same",
            )
            return result

        before = await hub.exec.aws.s3.bucket_website.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        result["comment"] += list(
            hub.tool.aws.comment_utils.already_exists_comment("aws.s3.bucket", name)
        )
        if not data.recursive_diff(
            website_configuration,
            result["old_state"]["website_configuration"],
            ignore_missing_keys=True,
            ignore_order=True,
        ):
            # no updates to make. return from here
            return result

        if ctx.get("test", False):
            result["new_state"]["website_configuration"] = website_configuration
            result["comment"] += list(
                hub.tool.aws.comment_utils.would_update_comment(
                    resource_type=STATE_NAME, name=name
                )
            )
            return result
        else:
            result["comment"] += list(
                hub.tool.aws.comment_utils.update_comment(
                    resource_type=STATE_NAME, name=name
                )
            )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "bucket": bucket,
                    "website_configuration": website_configuration,
                    "checksum_algorithm": checksum_algorithm,
                    "expected_bucket_owner": expected_bucket_owner,
                },
            )
            result["comment"] = list(
                hub.tool.aws.comment_utils.would_create_comment(
                    resource_type=STATE_NAME, name=name
                )
            )
            return result

        result["comment"] = list(
            hub.tool.aws.comment_utils.create_comment(
                resource_type=STATE_NAME, name=name
            )
        )

    put_ret = await hub.exec.boto3.client.s3.put_bucket_website(
        ctx,
        Bucket=bucket,
        ChecksumAlgorithm=checksum_algorithm,
        WebsiteConfiguration=website_configuration,
        ExpectedBucketOwner=expected_bucket_owner,
    )
    if not put_ret["result"]:
        result["result"] = False
        result["comment"] += list(put_ret["comment"])
        return result
    resource_id = bucket
    after = await hub.exec.aws.s3.bucket_website.get(
        ctx, name=name, resource_id=resource_id
    )
    if not after["result"] or not after["ret"]:
        result["comment"] += after["comment"]
        result["result"] = False
        return result

    result["new_state"] = after["ret"]

    return result


async def absent(
    hub, ctx, name: str, expected_bucket_owner: str = None, resource_id: str = None
) -> Dict[str, Any]:
    """This action removes the website configuration for a bucket. Amazon S3 returns a 200 OK response upon
    successfully deleting a website configuration on the specified bucket. You will get a 200 OK response if the
    website configuration you are trying to delete does not exist on the bucket. Amazon S3 returns a 404 response if
    the bucket specified in the request does not exist. This DELETE action requires the S3:DeleteBucketWebsite
    permission. By default, only the bucket owner can delete the website configuration attached to a bucket.
    However, bucket owners can grant other users permission to delete the website configuration by writing a bucket
    policy granting them the S3:DeleteBucketWebsite permission.  For more information about hosting websites, see
    Hosting Websites on Amazon S3.  The following operations are related to DeleteBucketWebsite:    GetBucketWebsite
    PutBucketWebsite

        Args:
            name(str):
                An Idem name of the resource.

            expected_bucket_owner(str, Optional):
                The account ID of the expected bucket owner. If the bucket is owned by a different account, the
                request fails with the HTTP status code 403 Forbidden (access denied). Defaults to None.

            resource_id(str, Optional):
                The bucket name for which you want to remove the website configuration.


        Request Syntax:
            .. code-block:: sls

                resource_is_absent:
                  aws.s3.bucket_website.absent:
                    - name: "str"
                    - resource_id: "str"

        Returns:
            Dict[str, Any]

        Examples:
            .. code-block:: sls

                resource_is_absent:
                  aws.s3.bucket_website.absent:
                    - name: value
                    - resource_id: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type=STATE_NAME, name=name
            )
        )
        return result

    before = await hub.exec.aws.s3.bucket_website.get(
        ctx, name=name, resource_id=resource_id
    )
    if not before["result"]:
        if "NoSuchBucket" in str(before["comment"]):
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type=STATE_NAME, name=name
            )
            return result
        result["result"] = False
        result["comment"] += before["comment"]
        return result

    if not before["ret"]:
        result["comment"] += list(
            hub.tool.aws.comment_utils.already_absent_comment(
                resource_type=STATE_NAME, name=name
            )
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] += list(
            hub.tool.aws.comment_utils.would_delete_comment(
                resource_type=STATE_NAME, name=name
            )
        )
        return result
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.s3.delete_bucket_website(
            ctx, Bucket=resource_id, ExpectedBucketOwner=expected_bucket_owner
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(
            hub.tool.aws.comment_utils.delete_comment(
                resource_type=STATE_NAME, name=name
            )
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Gets the website configuration for each S3 bucket under the given AWS account.

    Returns:
        dict[str, dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.s3.bucket_website
    """
    result = {}

    list_buckets_ret = await hub.exec.boto3.client.s3.list_buckets(ctx)
    if not list_buckets_ret["result"]:
        hub.log.warning(f"Could not list S3 buckets: {list_buckets_ret['comment']}")
        return result

    for bucket in list_buckets_ret["ret"]["Buckets"]:
        bucket_name = bucket.get("Name")

        get_bucket_website_ret = await hub.exec.aws.s3.bucket_website.get(
            ctx, name=bucket_name, resource_id=bucket_name
        )
        if not get_bucket_website_ret["result"] or not get_bucket_website_ret["ret"]:
            hub.log.debug(
                f"Could not get website configuration for S3 bucket '{bucket_name}': "
                f"{get_bucket_website_ret['comment']}. Describe will skip this S3 bucket and continue."
            )
            continue

        resource_translated = get_bucket_website_ret["ret"]

        result[resource_translated["name"]] = {
            f"{STATE_NAME}.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
