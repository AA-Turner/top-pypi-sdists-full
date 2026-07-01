from enum import Enum

class AccountProvider(str, Enum):
    Google = "google",
    Microsoft = "microsoft",
    Dropbox = "dropbox",
    Box = "box",
    Github = "github",
    Gitlab = "gitlab",
    Slack = "slack",
    Hubspot = "hubspot",
    Notion = "notion",
    Atlassian = "atlassian",
    Attio = "attio",
    Intercom = "intercom",
    Zendesk = "zendesk",
    Salesforce = "salesforce",
    Linear = "linear",
    Twitter = "twitter",
    Zoom = "zoom",
    Linkedin = "linkedin",

