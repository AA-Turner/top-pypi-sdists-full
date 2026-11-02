from enum import StrEnum
from typing import Optional

from channel_advisor_api.models import restricted_words
from channel_advisor_api.models.channel_advisor import (
    MinProduct,
    BaseProduct,
)
from channel_advisor_api.models.channel_advisor_attributes import (
    BaseAttributes,
    ChildOptimizeAttributes,
    ParentOptimizeAttributes,
)
from channel_advisor_api.utils.aws import AwsClient
from pydantic import BaseModel, Field

from channel_advisor_api.utils.logger import get_logger

logger = get_logger(__name__)


class Models(StrEnum):
    CLAUDE_3_5_SONNET_V2 = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
    CLAUDE_3_7_SONNET = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"


class BaseProductWithAttributes(BaseModel):
    product: BaseProduct
    attributes: BaseAttributes


class ParentProductWithAttributes(BaseProductWithAttributes):
    product: MinProduct = Field(description="product information core properties")
    attributes: ParentOptimizeAttributes = Field(
        description="Product attributes including specifications, features, and metadata"
    )


class ChildProductWithAttributes(ParentProductWithAttributes):
    attributes: ChildOptimizeAttributes = Field(
        description="Product attributes including specifications, features, and metadata"
    )


def llm_product(
    product: MinProduct,
    is_parent: bool,
    xtra_context: Optional[str] = None,
    temperature: float = 0.7,
    model: Models = Models.CLAUDE_3_7_SONNET,
) -> BaseProductWithAttributes:

    if is_parent:
        product_with_attributes = ParentProductWithAttributes(product=product, attributes=product.attributes)
        response_model = ParentProductWithAttributes
    else:
        product_with_attributes = ChildProductWithAttributes(product=product, attributes=product.attributes)
        response_model = ChildProductWithAttributes

    # Build message sequence
    messages = [
        {
            "role": "system",
            "content": "\n".join(
                [
                    "You are an expert product manager and marketer for a powersports gear and accessories company.",
                    "Clean up and enhance the Product Info and Attributes:",
                    "- Improve fields that could be improved",
                    "- Fill in missing data especially Titles, Descriptions, Bullets and Search terms",
                    "- Parent products should not have size or color attributes",
                    "- Retain any notes attributes",
                    "- Avoid these categories of words/phrases in your response: ",
                    restricted_words.get_restricted_words_context(),
                ]
            ),
        }
    ]

    if xtra_context:
        messages.append({"role": "user", "content": f"Additional context: {xtra_context}"})

    messages.append(
        {
            "role": "user",
            "content": f"Product Info: {product_with_attributes.model_dump_json(exclude_none=True)}",
        }
    )

    try:
        # Make API call with retry logic
        product_with_attributes, completion = AwsClient().claude_client.completions.create_with_completion(
            model=model.value,
            max_tokens=1024 * 10,
            max_retries=2,
            messages=messages,
            response_model=response_model,
            temperature=temperature,
        )
    except Exception as e:
        logger.error(
            "Error creating product_with_attributes",
            extra={"product_id": product.id, "error": str(e)},
            exc_info=True,
        )
        raise e

    logger.info(
        f"Llm created product_with_attributes for product_id: {product.id}",
        extra={
            "product": product_with_attributes.product.model_dump(exclude_none=True),
            "attributes": product_with_attributes.attributes.model_dump(exclude_none=True),
            "completion": completion,
        },
    )

    # Update product with new attributes
    new_product = product_with_attributes.product
    new_product.attributes = product_with_attributes.attributes
    # new_product.attributes.product_id = new_product.id

    # remove restricted words from description
    new_product.description = new_product.description.replace("™", "").replace("©", "")

    return new_product
