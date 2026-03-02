from .kb_article import KBArticle
from pydantic import BaseModel

class Remediation(BaseModel):
    """
    The Remediation object describes the recommended remediation steps to address
    identified issue(s).
    """
    desc: str # The description of the remediation strategy.

    # Optional:
    references: list[str] | None = None # A list of supporting URL/s, references that help describe the
                                        # remediation strategy.
    kb_articles: list[str] | None = None
    kb_article_list: list[KBArticle] | None = None
