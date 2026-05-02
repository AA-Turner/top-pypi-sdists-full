from pydantic import BaseModel

class MetaProductItem(BaseModel):
    product_retailer_id: str
    quantity: str
    item_price: str
    currency: str

class MetaOrderContent(BaseModel):
    """Included in the messages object when a customer has placed an order. Order objects have the following properties:


        catalog_id — String. ID for the catalog the ordered item belongs to.
        text — String. Text message from the user sent along with the order.
        product_items — Array of product item objects containing the following fields:
            product_retailer_id — String. Unique identifier of the product in a catalog.
            quantity — String. Number of items.
            item_price — String. Price of each item.
            currency — String. Price currency.
    """
    catalog_id: str
    text: str
    product_items: list[MetaProductItem]