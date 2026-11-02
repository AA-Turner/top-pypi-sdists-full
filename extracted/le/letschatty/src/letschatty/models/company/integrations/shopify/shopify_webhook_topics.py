from enum import Enum

class ShopifyWebhookTopic(str, Enum):
    """Shopify webhook topics for products and orders"""
    
    # Product webhooks
    PRODUCTS_CREATE = "products/create"
    PRODUCTS_UPDATE = "products/update"
    PRODUCTS_DELETE = "products/delete"
    
    # Order webhooks
    ORDERS_CREATE = "orders/create"
    ORDERS_UPDATE = "orders/updated"
    ORDERS_DELETE = "orders/delete"
    ORDERS_FULFILLED = "orders/fulfilled"
    ORDERS_PARTIALLY_FULFILLED = "orders/partially_fulfilled"
    ORDERS_PAID = "orders/paid"
    ORDERS_CANCELLED = "orders/cancelled"
    
    @classmethod
    def get_product_topics(cls) -> list[str]:
        """Get all product-related webhook topics"""
        return [
            cls.PRODUCTS_CREATE.value,
            cls.PRODUCTS_UPDATE.value,
            cls.PRODUCTS_DELETE.value,
        ]
    
    @classmethod
    def get_order_topics(cls) -> list[str]:
        """Get all order-related webhook topics"""
        return [
            cls.ORDERS_CREATE.value,
            cls.ORDERS_UPDATE.value,
            cls.ORDERS_DELETE.value,
            cls.ORDERS_FULFILLED.value,
            cls.ORDERS_PARTIALLY_FULFILLED.value,
            cls.ORDERS_PAID.value,
            cls.ORDERS_CANCELLED.value,
        ]