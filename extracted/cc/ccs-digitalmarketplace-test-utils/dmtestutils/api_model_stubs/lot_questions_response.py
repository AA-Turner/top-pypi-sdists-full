from .base import BaseAPIModelStub


class LotQuestionsResponseStub(BaseAPIModelStub):
    resource_name = "lotQuestionsResponses"
    default_data = {
        "id": 123,
        "frameworkName": "Digital Outcomes and Specialists 7",
        "frameworkFamily": "digital-outcomes-and-specialists",
        "frameworkFramework": "digital-outcomes-and-specialists",
        "frameworkSlug": "digital-outcomes-and-specialists-7",
        "lotName": "Digital Capability and Delivery Partner",
        "lotNumber": "2",
        "lotSlug": "digital-capability-and-delivery-partner",
        "supplierId": 886665,
        "supplierName": "Rex's Mex",
        "status": "in_progress",
    }
    optional_keys = [
        ("supplierId", "supplier_id"),
        ("supplierName", "supplier_name"),
        ("frameworkName", "framework_name"),
        ("frameworkFamily", "framework_family"),
        ("frameworkFramework", "framework_framework"),
        ("frameworkSlug", "framework_slug"),
        ("lotSlug", "lot_slug"),
        ("lotName", "lot_name"),
        ("lotNumber", "lot_number"),
        ("status", "status"),
    ]
