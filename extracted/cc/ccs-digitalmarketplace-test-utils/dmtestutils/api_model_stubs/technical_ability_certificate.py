from .base import BaseAPIModelStub


class TechnicalAbilityCertificateStub(BaseAPIModelStub):
    resource_name = "technicalAbilityCertificates"
    default_data = {
        "id": 123,
        "frameworkName": "G-Cloud 15",
        "frameworkFamily": "g-cloud",
        "frameworkFramework": "g-cloud",
        "frameworkSlug": "g-cloud-15",
        "frameworkStatus": "open",
        "route": "saas",
        "supplierId": 886665,
        "supplierName": "Elma B.L.A.D.E",
        "status": "in_progress",
        "authenticationId": None,
        "sentAt": None,
        "electronicSignature": None,
        "approvedAt": None,
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
        ("authenticationId", "authentication_id"),
        ("electronicSignature", "electronic_signature"),
        ("sentAt", "sent_at"),
        ("approvedAt", "approved_at"),
        ("createdAt", "created_at"),
        ("updatedAt", "updated_at"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.response_data["links"][
            "self"
        ] = f"http://localhost:8000/technical-ability-certificates/{self.response_data['id']}"

        if kwargs.get("status") in ["awaiting_approval", "approved"]:
            if self.response_data["authenticationId"] is None:
                self.response_data["authenticationId"] = "AAABBBCCC"
            if self.response_data["sentAt"] is None:
                self.response_data["sentAt"] = "2025-05-16T12:00:00.000000Z"

        if kwargs.get("status") == "approved":
            if self.response_data["electronicSignature"] is None:
                self.response_data["electronicSignature"] = "Jack Vandham"
            if self.response_data["approvedAt"] is None:
                self.response_data["approvedAt"] = "2025-05-17T12:00:00.000000Z"
