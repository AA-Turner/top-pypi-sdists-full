from channel_advisor_api.utils.logger import get_logger

logger = get_logger(__name__)

"""
class ProductCleanup(BaseModel):
    id: int = Field(description="The channel advisor id of the product. This is the sku", frozen=True)
    sku: str = Field(description="The sku of the product. Preferred length is 100 characters. Max is 200", frozen=True)
    asin: Optional[str] = Field(description="Amazon Standard Identification Number", frozen=True, default=None)
    title: str = Field(description="Product title. ")
    is_parent: bool = Field(description="Whether the product is a parent or a child", frozen=True)
    description: Optional[str] = Field(
        default=None,
        description="Product description in html. May not contain trademark (™) or copyright (©) symbols. "
        "2000 characters max. Do not remove any html tags.",
    )
    attributes: Optional[CleanupAttributes] = Field(
        default=None, description="The attributes of the product that need to be cleaned up"
    )

    @property
    def table(self):
        self_dict = self.model_dump()
        attrs = self_dict.pop("attributes")
        # for the description field, word wrap at <br> tags
        self_dict["description"] = self_dict["description"].replace("<br>", "<br>\n")
        table_dict = {**self_dict, **attrs}
        return tabulate(table_dict.items(), headers=["Field", "Value"])

    def comparison_table(self, other: "ProductCleanup"):
        self_dict = self.model_dump()
        self_attrs = self_dict.pop("attributes")
        other_dict = other.model_dump()
        other_attrs = other_dict.pop("attributes")
        self_dict["description"] = (
            self_dict["description"].replace("<br>", "<br>\n") if self_dict["description"] else ""
        )
        other_dict["description"] = (
            other_dict["description"].replace("<br>", "<br>\n") if other_dict["description"] else ""
        )
        # add the attributes to the dict
        self_dict = {**self_dict, **self_attrs}
        other_dict = {**other_dict, **other_attrs}
        # create one table with 3 columns: Field, Self, Other
        new_table = []
        for field in self_dict.keys():
            new_table.append((field, self_dict[field], other_dict[field]))
        return tabulate(new_table, headers=["Field", "Self", "Other"], tablefmt="fancy_grid")

    @staticmethod
    def from_channel_advisor_product(product: ProductBase) -> "ProductCleanup":
        return ProductCleanup(**{**product.model_dump(), "attributes": product.attributes})

    def clean_product(self) -> "ProductCleanup":
        return get_claude_client().completions.create(
            model="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
            max_tokens=2048,
            max_retries=2,
            messages=[
                {
                    "role": "system",
                    "content": "We need to clean up and enhance the product attributes for a powersports product. "
                    "The attributes are provided in a dictionary. "
                    "Your job is to clean up, enhance and fill in the missing attributes and return a new dictionary. ",
                },
                {
                    "role": "user",
                    "content": f"Product Info: {self.model_dump_json()}",
                },
            ],
            response_model=ProductCleanup,
        )

"""
