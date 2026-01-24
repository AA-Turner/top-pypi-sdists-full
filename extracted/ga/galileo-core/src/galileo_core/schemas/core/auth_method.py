from enum import Enum


class AuthMethod(str, Enum):
    email = "email"
    google = "google"
    github = "github"
    okta = "okta"
    azure_ad = "azure-ad"
    custom = "custom"
