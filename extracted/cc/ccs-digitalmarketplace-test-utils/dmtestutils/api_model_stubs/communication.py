from datetime import datetime, timedelta

from .base import BaseAPIModelStub


DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DEFAULT_TIME = datetime(2024, 3, 14, 14, 30)


class CommunicationStub(BaseAPIModelStub):
    resource_name = "communications"

    admin_user = {
        "id": 123,
        "email": "test+123@digital.cabinet-office.gov.uk",
    }
    supplier_user = {
        "id": 456,
        "email": "test+456@digital.gov.uk",
    }
    default_data = {
        "id": 1234,
        "subject": "Communication Subject",
        "category": "Compliance",
        "supplierId": 1234,
        "supplierName": "My Little Company",
        "frameworkSlug": "g-cloud-14",
        "frameworkFramework": "g-cloud",
        "frameworkFamily": "g-cloud",
        "frameworkName": "G-Cloud 14",
        "frameworkStatus": "pending",
        "createdAt": DEFAULT_TIME.strftime(DATETIME_FORMAT),
        "updatedAt": DEFAULT_TIME.strftime(DATETIME_FORMAT),
        "links": {},
        "messages": [],
    }
    optional_keys = [
        ("supplierName", "supplier_name"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if kwargs.get("resolved"):
            self.response_data.update(
                **{
                    "resolvedByUserEmail": self.admin_user["email"],
                    "resolvedByUserId": self.admin_user["id"],
                    "resolution": kwargs.get("resolution", "archived"),
                }
            )

        message_data = {
            "id": int(f"{self.response_data['id']}1"),
            "communicationId": self.response_data["id"],
            "text": "This is the communication message sent by CCS",
            "sentAt": DEFAULT_TIME.strftime(DATETIME_FORMAT),
            "sentByUserId": self.admin_user["id"],
            "sentByUserEmail": self.admin_user["email"],
            "target": "for_supplier",
        }

        message_data["attachments"] = [
            {"id": int(f"{message_data['id']}{index + 1}")} | attachment
            for index, attachment in enumerate(kwargs.get("attachments", []))
        ]

        if kwargs.get("read") or kwargs.get("last_message_target", "for_admin") == "for_admin":
            message_data.update(
                **{
                    "readAt": (DEFAULT_TIME + timedelta(minutes=self.response_data["id"])).strftime(DATETIME_FORMAT),
                    "readByUserId": self.supplier_user["id"],
                    "readByUserEmail": self.supplier_user["email"],
                }
            )

        self.response_data["messages"].append(message_data)

        if kwargs.get("last_message_target", "for_admin") == "for_admin":
            message_data = {
                "id": int(f"{self.response_data['id']}2"),
                "communicationId": self.response_data["id"],
                "text": "This is the communication message sent by Supplier",
                "sentAt": (DEFAULT_TIME + timedelta(days=self.response_data["id"])).strftime(DATETIME_FORMAT),
                "sentByUserId": self.supplier_user["id"],
                "sentByUserEmail": self.supplier_user["email"],
                "target": "for_admin",
                "attachments": [],
            }

            if kwargs.get("read"):
                message_data.update(
                    **{
                        "readAt": (
                            DEFAULT_TIME + timedelta(days=self.response_data["id"], minutes=self.response_data["id"])
                        ).strftime(DATETIME_FORMAT),
                        "readByUserId": self.admin_user["id"],
                        "readByUserEmail": self.admin_user["email"],
                    }
                )

            self.response_data["messages"].append(message_data)


class CommunicationMessageStub(BaseAPIModelStub):
    resource_name = "communicationMessages"

    default_data = {
        "id": 1231,
        "communicationId": 123,
        "text": "This is the communication message",
        "sentAt": DEFAULT_TIME.strftime(DATETIME_FORMAT),
        "sentByUserId": 123,
        "sentByUserEmail": "test+123@digital.cabinet-office.gov.uk",
        "target": "for_supplier",
    }
    optional_keys = [
        ("communicationId", "communication_id"),
        ("sentAt", "sent_at"),
        ("sentByUserId", "sent_by_user_id"),
        ("sentByUserEmail", "sent_by_user_email"),
        ("readAt", "read_at"),
        ("readByUserId", "read_by_user_id"),
        ("readByUserEmail", "read_by_user_email"),
    ]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.response_data.update(
            attachments=[
                {"id": int(f"{self.response_data['id']}{index + 1}")} | attachment
                for index, attachment in enumerate(kwargs.get("attachments", []))
            ]
        )
