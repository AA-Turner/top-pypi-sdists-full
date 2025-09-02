from __future__ import annotations
from pydantic import BaseModel, Field, field_validator, ConfigDict
from urllib.parse import urlparse, parse_qs
import logging

logger, highlights = logging.getLogger("logger"), logging.getLogger("highlights")
class QueryUTMParams(BaseModel):
    """
    UTM campaign structure with the following parameters:
    - Source: the source of the campaign (whatsapp, facebook, etc.)
    - Medium: the medium of the campaign (social, email, etc.)
    - Campaign: the campaign name (black_friday, summer_sale, etc.)
    - Term: campaign terms/keywords
    - Content: campaign content details (ad copy, image, etc.)
    """
    base_url: str
    utm_campaign: str = Field(default="")
    utm_source: str = Field(default="")
    utm_medium: str = Field(default="")
    utm_term: str = Field(default="")
    utm_content: str = Field(default="")
    utm_id: str = Field(default="")  # Meta uses it as the ad_id
    fbclid: str = Field(default="")
    gclid: str = Field(default="")

    model_config = ConfigDict(ignore_extra=True)

    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v: str) -> str:
        if v.startswith("https://"):
            return v.split("https://")[1]
        return v

    @classmethod
    def from_url(cls, url: str) -> QueryUTMParams:
        """Create UTM parameters from a URL string"""
        try:
            parsed_url = urlparse(url)
            base_url = parsed_url.netloc + parsed_url.path
            query_params = parse_qs(parsed_url.query)

            # Extract single values from lists returned by parse_qs
            for key in query_params:
                if isinstance(query_params[key], list):
                    query_params[key] = query_params[key][0]

            query_params["base_url"] = base_url

            return cls(**query_params)
        except Exception as e:
            logger.error(f"Invalid URL {url}")
            raise ValueError(f"Invalid URL {url}, must follow format 'https://www.example.com/path' - {e}")


    def __eq__(self, other: QueryUTMParams) -> bool:
        if not isinstance(other, QueryUTMParams):
            return False
        return self.base_url == other.base_url and self.utm_campaign == other.utm_campaign and self.utm_source == other.utm_source and self.utm_medium == other.utm_medium and self.utm_term == other.utm_term and self.utm_content == other.utm_content and self.utm_id == other.utm_id

    def __hash__(self) -> int:
        return hash((self.base_url, self.utm_campaign, self.utm_source, self.utm_medium, self.utm_term, self.utm_content, self.utm_id))

    def get_utm(self) -> str:
        """Generate full UTM URL with URI-encoded parameters"""
        from urllib.parse import quote

        utm = f"https://{self.base_url}?"

        # Build parameter list with URI encoding, excluding empty values
        params = [
            f"{param}={quote(str(getattr(self, param)))}"
            for param in ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'utm_id', 'fbclid', 'gclid']
            if getattr(self, param)
        ]

        return utm + "&".join(params)