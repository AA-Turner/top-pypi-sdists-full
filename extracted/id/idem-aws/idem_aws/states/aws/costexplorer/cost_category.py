"""State module for managing Amazon Cost Category."""
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
    rules: List[
        make_dataclass(
            "CostCategoryRule",
            [
                ("Value", str, field(default=None)),
                (
                    "Rule",
                    make_dataclass(
                        "Expression",
                        [
                            (
                                "Or",
                                List[
                                    make_dataclass(
                                        "Expressions",
                                        [
                                            ("Or", List[Any], field(default=None)),
                                            ("And", List[Any], field(default=None)),
                                            ("Not", Any, field(default=None)),
                                            (
                                                "Dimensions",
                                                make_dataclass(
                                                    "DimensionValues",
                                                    [
                                                        (
                                                            "Key",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "Values",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "MatchOptions",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "Tags",
                                                make_dataclass(
                                                    "TagValues",
                                                    [
                                                        (
                                                            "Key",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "Values",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "MatchOptions",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                            (
                                                "CostCategories",
                                                make_dataclass(
                                                    "CostCategoryValues",
                                                    [
                                                        (
                                                            "Key",
                                                            str,
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "Values",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                        (
                                                            "MatchOptions",
                                                            List[str],
                                                            field(default=None),
                                                        ),
                                                    ],
                                                ),
                                                field(default=None),
                                            ),
                                        ],
                                    )
                                ],
                                field(default=None),
                            ),
                            ("And", List[Any], field(default=None)),
                            ("Not", Any, field(default=None)),
                            ("Dimensions", Any, field(default=None)),
                            ("Tags", Any, field(default=None)),
                            ("CostCategories", Any, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                (
                    "InheritedValue",
                    make_dataclass(
                        "CostCategoryInheritedValueDimension",
                        [
                            ("DimensionName", str, field(default=None)),
                            ("DimensionKey", str, field(default=None)),
                        ],
                    ),
                    field(default=None),
                ),
                ("Type", str, field(default=None)),
            ],
        )
    ],
    cost_category_name: str,
    rule_version: str,
    resource_id: str = None,
    split_charge_rules: List[
        make_dataclass(
            "CostCategorySplitChargeRule",
            [
                ("Source", str),
                ("Targets", List[str]),
                ("Method", str),
                (
                    "Parameters",
                    List[
                        make_dataclass(
                            "CostCategorySplitChargeRuleParameter",
                            [("Type", str), ("Values", List[str])],
                        )
                    ],
                    field(default=None),
                ),
            ],
        )
    ] = None,
    default_value: str = None,
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Creates a new Cost Category with the requested name and rules.

    Args:
        name(str):
            The unique name of the Cost Category.
        rules(list[dict[str, Any]]):
            The Cost Category rules used to categorize costs.
                * Value (str, Optional):
                    The default value for the cost category.
                * Rule (dict[str, Any], Optional):
                    An Expression object used to categorize costs. This supports dimensions, tags, and nested expressions.
                    Currently the only dimensions supported are LINKED_ACCOUNT, SERVICE_CODE, RECORD_TYPE, and LINKED_ACCOUNT_NAME.
                    Root level OR isn't supported. We recommend that you create a separate rule instead.
                    RECORD_TYPE is a dimension used for Cost Explorer APIs, and is also supported for Cost Category expressions.
                    This dimension uses different terms, depending on whether you're using the console or API/JSON editor.
                    For a detailed comparison, see Term Comparisons in the Billing and Cost Management User Guide.
                        * Or (list[dict[str, Any]], Optional):
                            Return results that match either Dimension object.
                                * Or (list[Any], Optional):
                                    Return results that match either Dimension object.
                                * And (list[Any], Optional):
                                    Return results that match both Dimension objects.
                                * Not (Any, Optional):
                                    Return results that don't match a Dimension object.
                                * Dimensions (dict[str, Any], Optional):
                                    The specific Dimension to use for Expression.
                                        * Key (str, Optional):
                                            The names of the metadata types that you can use to filter and group your results. For example,
                                            AZ returns a list of Availability Zones.
                                        * Values (list[str], Optional):
                                            The metadata values that you can use to filter and group your results. You can use
                                            GetDimensionValues to find specific values.
                                        * MatchOptions (list[str], Optional):
                                            The match options that you can use to filter your results. MatchOptions is only applicable for
                                            actions related to Cost Category. The default values for MatchOptions are EQUALS and
                                            CASE_SENSITIVE.
                                * Tags (dict[str, Any], Optional):
                                    The specific Tag to use for Expression.
                                        * Key (str, Optional):
                                            The key for the tag.
                                        * Values (list[str], Optional):
                                            The specific value of the tag.
                                        * MatchOptions (list[str], Optional):
                                            The match options that you can use to filter your results. MatchOptions is only applicable for
                                            actions related to Cost Category. The default values for MatchOptions are EQUALS and
                                            CASE_SENSITIVE.
                                * CostCategories (dict[str, Any], Optional):
                                    The filter that's based on CostCategory values.
                                        * Key (str, Optional):
                                            The unique name of the Cost Category.
                                        * Values (list[str], Optional):
                                            The specific value of the Cost Category.
                                        * MatchOptions (list[str], Optional):
                                            The match options that you can use to filter your results. MatchOptions is only applicable for
                                            actions related to cost category. The default values for MatchOptions is EQUALS and
                                            CASE_SENSITIVE.
                        * And (list[Any], Optional):
                            Return results that match both Dimension objects.
                        * Not (Any, Optional):
                            Return results that don't match a Dimension object.
                        * Dimensions (Any, Optional):
                            The specific Dimension to use for Expression.
                        * Tags (Any, Optional):
                            The specific Tag to use for Expression.
                        * CostCategories (Any, Optional):
                            The filter that's based on CostCategory values.
                        * InheritedValue (dict[str, Any], Optional):
                            The value the line item is categorized as if the line item contains the matched dimension.
                                * DimensionName (str, Optional):
                                    The name of the dimension that's used to group costs. If you specify LINKED_ACCOUNT_NAME, the
                                    cost category value is based on account name. If you specify TAG, the cost category value is
                                    based on the value of the specified tag key.
                                * DimensionKey (str, Optional):
                                    The key to extract cost category values.
                        * Type (str, Optional):
                            You can define the CostCategoryRule rule type as either REGULAR or INHERITED_VALUE. The
                            INHERITED_VALUE rule type adds the flexibility to define a rule that dynamically inherits the
                            cost category value. This value is from the dimension value that's defined by
                            CostCategoryInheritedValueDimension. For example, suppose that you want to costs to be
                            dynamically grouped based on the value of a specific tag key. First, choose an inherited value
                            rule type, and then choose the tag dimension and specify the tag key to use.
        cost_category_name(str):
            Name of Cost Category.
        rule_version(str):
            The rule schema version in this particular Cost Category.
        tags (dict[str, Any]]):
            Each tag consists of a key and a value, and each key must be unique for the resource.
        resource_id(str, Optional):
            Cost Category ARN to identify the resource.
        split_charge_rules(list[dict[str, Any]], Optional):
            The split charge rules used to allocate your charges between your Cost Category values. Defaults to None.
                * Source (str):
                    The Cost Category value that you want to split. That value can't be used as a source or a target
                    in other split charge rules. To indicate uncategorized costs, you can use an empty string as the
                    source.
                * Targets (list[str]):
                    The Cost Category values that you want to split costs across. These values can't be used as a
                    source in other split charge rules.
                * Method (str):
                    The method that's used to define how to split your source costs across your targets.
                    Proportional - Allocates charges across your targets based on the proportional weighted cost of
                    each target.  Fixed - Allocates charges across your targets based on your defined allocation
                    percentage. >Even - Allocates costs evenly across all targets.
                * Parameters (list[dict[str, Any]], Optional):
                    The parameters for a split charge method. This is only required for the FIXED method.
                * Type (str):
                    The parameter type.
                * Values (list[str]):
                    The parameter values.
        default_value(str, Optional):
            The default value for the cost category.

    Request Syntax:
        .. code-block:: sls

          [monitor-resource-id]:
            aws.costexplorer.cost_category.present:
              - resource_id: "string"
              - tags: "dict"
              - cost_category_name: "string"
              - effective_start: "string"
              - rules:
                  - Rule:
                      Dimensions:
                        Key: "string"
                        MatchOptions:
                          - EQUALS
                        Values:
                          - "string"
                    Type: "string"
                    Value: "string"
              - split_charge_rules:
                  - Method: "string"
                    Parameters:
                      - Type: "string"
                        Values:
                          - "string"
                          - "string"
                    Source: "string"
                    Targets:
                      - "string"
                  - processing_status:
                      - Component: "string"
                        Status: "string"
                  - default_value: "string"

    Returns:
        Dict[str, str]

    Examples:
      .. code-block:: sls

        arn:aws:ce::1234567891012:costcategory/4e9662f0-5533-4fdf-8224-9bb9f82d0a39:
          aws.costexplorer.cost_category.present:
            - resource_id: arn:aws:ce::1234567891012:costcategory/4e9662f0-5533-4fdf-8224-9bb9f82d0a39
            - tags:
                name: test_category
            - cost_category_name: test_category
            - effective_start: "2022-06-01T00:00:00Z"
            - rule_version: CostCategoryExpression.v1
            - rules:
                - Rule:
                    Dimensions:
                      Key: LINKED_ACCOUNT
                      MatchOptions:
                        - EQUALS
                      Values:
                        - "107488843946"
                  Type: REGULAR
                  Value: Alpha
                - Rule:
                    Dimensions:
                      Key: LINKED_ACCOUNT
                      MatchOptions:
                        - EQUALS
                      Values:
                        - 011922870716
                  Type: REGULAR
                  Value: Beta
                - Rule:
                    Dimensions:
                      Key: LINKED_ACCOUNT
                      MatchOptions:
                        - EQUALS
                      Values:
                        - "332986752459"
                  Type: REGULAR
                  Value: Gamma
            - split_charge_rules:
                - Method: FIXED
                  Parameters:
                    - Type: ALLOCATION_PERCENTAGES
                      Values:
                        - "40"
                        - "60"
                  Source: Alpha
                  Targets:
                    - Beta
                    - Gamma
            - processing_status:
                - Component: COST_EXPLORER
                  Status: PROCESSING
            - default_value: Other
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.boto3.client.ce.describe_cost_category_definition(
            ctx, CostCategoryArn=resource_id
        )
        if not before["result"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

    if before:
        result[
            "old_state"
        ] = await hub.tool.aws.costexplorer.conversion_utils.convert_raw_cost_category_to_present_async(
            ctx,
            raw_resource=before["ret"]["CostCategory"],
            idem_resource_name=name,
        )
        plan_state = copy.deepcopy(result["old_state"])

        update_ret = await hub.tool.aws.costexplorer.cost_category.update_cost_category_definition(
            ctx,
            before=before["ret"]["CostCategory"],
            rules=rules,
            default_value=default_value,
            split_charge_rules=split_charge_rules,
        )
        result["comment"] += update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = resource_updated or bool(update_ret["ret"])
        if update_ret["ret"] and ctx.get("test", False):
            plan_state = update_ret["ret"]

        if tags is not None and tags != result["old_state"].get("tags"):
            # Update tags
            update_ret = await hub.tool.aws.costexplorer.cost_category.update_tags(
                ctx,
                resource_id=resource_id,
                old_tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(
                    result["old_state"].get("tags")
                ),
                new_tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
            )
            result["result"] = result["result"] and update_ret["result"]
            result["comment"] += update_ret["comment"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if ctx.get("test", False) and update_ret["ret"] is not None:
                plan_state["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    update_ret["ret"].get("tags")
                )

        if resource_updated:
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.costexplorer.cost_category", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.costexplorer.cost_category", name=name
                )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "cost_category_name": cost_category_name,
                    "rules": rules,
                    "split_charge_rules": split_charge_rules,
                    "default_value": default_value,
                    "tags": tags,
                    "rule_version": rule_version,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.costexplorer.cost_category", name=name
            )
            return result

        ret = await hub.exec.boto3.client.ce.create_cost_category_definition(
            ctx,
            Name=cost_category_name,
            RuleVersion=rule_version,
            Rules=rules,
            DefaultValue=default_value,
            SplitChargeRules=split_charge_rules,
            ResourceTags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.costexplorer.cost_category", name=name
        )
        resource_id = ret["ret"]["CostCategoryArn"]

    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.boto3.client.ce.describe_cost_category_definition(
                ctx, CostCategoryArn=resource_id
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result[
                "new_state"
            ] = await hub.tool.aws.costexplorer.conversion_utils.convert_raw_cost_category_to_present_async(
                ctx,
                raw_resource=after["ret"]["CostCategory"],
                idem_resource_name=name,
            )
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a cost category.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            Cost Category ARN to identify the resource. Idem automatically considers this resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.costexplorer.cost_category.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.costexplorer.cost_category", name=name
        )
        return result

    before = await hub.exec.boto3.client.ce.describe_cost_category_definition(
        ctx, CostCategoryArn=resource_id
    )

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.costexplorer.cost_category", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = await hub.tool.aws.costexplorer.conversion_utils.convert_raw_cost_category_to_present_async(
            ctx, raw_resource=before["ret"]["CostCategory"], idem_resource_name=name
        )
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.costexplorer.cost_category", name=name
        )
        return result
    else:
        result[
            "old_state"
        ] = await hub.tool.aws.costexplorer.conversion_utils.convert_raw_cost_category_to_present_async(
            ctx, raw_resource=before["ret"]["CostCategory"], idem_resource_name=name
        )
        ret = await hub.exec.boto3.client.ce.delete_cost_category_definition(
            ctx, CostCategoryArn=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.costexplorer.cost_category", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Returns a list of aws cost categories.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.costexplorer.cost_category
    """
    result = {}
    ret = await hub.exec.boto3.client.ce.list_cost_category_definitions(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not list Cost Category Definitions {ret['comment']}")
        return {}

    for costcategory in ret["ret"]["CostCategoryReferences"]:
        resource_id = costcategory.get("CostCategoryArn")
        ret = await hub.exec.boto3.client.ce.describe_cost_category_definition(
            ctx, CostCategoryArn=resource_id
        )

        if not ret["result"]:
            hub.log.warning(
                f"Could not describe Cost Category Definitions {ret['comment']}"
            )
            return {}

        resource_translated = await hub.tool.aws.costexplorer.conversion_utils.convert_raw_cost_category_to_present_async(
            ctx,
            raw_resource=ret["ret"].get("CostCategory"),
            idem_resource_name=resource_id,
        )
        result[resource_id] = {
            "aws.costexplorer.cost_category.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
