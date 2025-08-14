from .base import BaseAPIModelStub


class LotPricingStub(BaseAPIModelStub):
    resource_name = "lotPricings"
    default_data = {
        "id": 123,
        "frameworkName": "G-Cloud 15",
        "frameworkFamily": "g-cloud",
        "frameworkFramework": "g-cloud",
        "frameworkSlug": "g-cloud-15",
        "frameworkStatus": "open",
        "route": "saas",
        "supplierId": 886665,
        "supplierName": "Noah's Ark",
        "status": "in_progress",
        "links": {},
        "createdAt": "2017-04-07T12:34:00.000000Z",
        "updatedAt": "2017-04-07T12:34:00.000000Z",
    }
    optional_keys = [
        ("supplierId", "supplier_id"),
        ("supplierName", "supplier_name"),
        ("frameworkName", "framework_name"),
        ("frameworkFamily", "framework_family"),
        ("frameworkFramework", "framework_framework"),
        ("frameworkSlug", "framework_slug"),
        ("status", "status"),
        ("createdAt", "created_at"),
        ("updatedAt", "updated_at"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.response_data["links"]["self"] = f"http://localhost:8000/lot-pricings/{self.response_data['id']}"
