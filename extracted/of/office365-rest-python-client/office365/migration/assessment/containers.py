from enum import Enum


class ScanContainer(Enum):
    """Where a scan runs in the product object tree — the dispatch + report container.

    Follows the container hierarchy (``TENANT -> SITE -> WEB -> LIST`` with
    ``FIELDS`` / ``ITEMS`` / ``FILES`` as list sub-resources) for SharePoint;
    Outlook adds ``MAILBOX -> MAIL_FOLDER``. Scans declare the container(s)
    they consume; the per-product assessor walker loads each container's data
    once and dispatches to the matching scans.
    """

    TENANT = "tenant"  # reserved — tenant assessor (site enumeration)
    SITE = "site"  # the site collection
    WEB = "web"  # subsite
    LIST = "list"  # list / library container
    FIELDS = "fields"  # a list's column schema
    ITEMS = "items"  # list items
    FILES = "files"  # list files / folders

    # Outlook (mail)
    MAILBOX = "mailbox"  # the mailbox root
    MAIL_FOLDER = "mail_folder"  # a mail folder
