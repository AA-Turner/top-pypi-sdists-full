from pydantic import BaseModel, Field

class MetaProductItem(BaseModel):
    # Meta manda cantidad y precio como NÚMEROS (`"quantity": 1, "item_price": 7.99`), no
    # como texto: con `str` cualquier pedido real anulaba el webhook entero (CONTAINER,
    # 2026-10-28). El modo lax de pydantic sigue aceptando "1" / "7.99" si alguna vez llegan así.
    product_retailer_id: str
    quantity: int
    item_price: float
    currency: str

class MetaOrderContent(BaseModel):
    """Included in the messages object when a customer has placed an order. Order objects have the following properties:
    https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks/reference/messages/order

        catalog_id — String. ID for the catalog the ordered item belongs to.
        text — String. Text message from the user sent along with the order.
        product_items — Array of product item objects containing the following fields:
            product_retailer_id — String. Unique identifier of the product in a catalog.
            quantity — Integer. Number of items.
            item_price — Number. Price of each item (Meta's own example is 7.99).
            currency — String. Price currency.

    Meta no manda el nombre ni la foto del producto: sólo el id del catálogo de Meta.
    `text` puede venir vacío; si faltara, el pedido no se pierde por eso.
    """
    catalog_id: str
    text: str = Field(default="")
    product_items: list[MetaProductItem] = Field(default_factory=list)
