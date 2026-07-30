"""Cloud-only GitHub sync-back for the github-documents-cloud source.

This subpackage implements the DataHub -> GitHub direction (writing DataHub
document edits back to a GitHub repository). It is intentionally isolated from
the OSS ``github_documents`` source, which only handles GitHub -> DataHub
import. Nothing here is imported by the OSS source.
"""
