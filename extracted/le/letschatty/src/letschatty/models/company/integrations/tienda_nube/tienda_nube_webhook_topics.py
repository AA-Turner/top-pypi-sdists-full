from enum import Enum

class TiendaNubeWebhookTopic(str, Enum):
    """Tienda Nube webhook topics for products and orders"""
    
    # Product webhooks
    PRODUCT_CREATED = "product/created"
    PRODUCT_UPDATED = "product/updated"
    PRODUCT_DELETED = "product/deleted"
    
    # Order webhooks
    ORDER_CREATED = "order/created"
    ORDER_UPDATED = "order/updated"
    ORDER_PAID = "order/paid"
    ORDER_PACKED = "order/packed"
    ORDER_FULFILLED = "order/fulfilled"
    ORDER_CANCELLED = "order/cancelled"
    ORDER_EDITED = "order/edited"
    ORDER_PENDING = "order/pending"
    ORDER_VOIDED = "order/voided"
    ORDER_UNPACKED = "order/unpacked"
    
    @classmethod
    def get_product_topics(cls) -> list[str]:
        """Get all product-related webhook topics"""
        return [
            cls.PRODUCT_CREATED.value,
            cls.PRODUCT_UPDATED.value,
            cls.PRODUCT_DELETED.value,
        ]
    
    @classmethod
    def get_order_topics(cls) -> list[str]:
        """Get all order-related webhook topics"""
        return [
            cls.ORDER_CREATED.value,
            cls.ORDER_UPDATED.value,
            cls.ORDER_PAID.value,
            cls.ORDER_PACKED.value,
            cls.ORDER_FULFILLED.value,
            cls.ORDER_CANCELLED.value,
            cls.ORDER_EDITED.value,
            cls.ORDER_PENDING.value,
            cls.ORDER_VOIDED.value,
            cls.ORDER_UNPACKED.value,
        ]
