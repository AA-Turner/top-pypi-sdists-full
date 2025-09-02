from typing import Union
from .other_source import OtherSource
from .pure_ad import PureAd
from .whatsapp_default_source import WhatsAppDefaultSource
from .topic_default_source import TopicDefaultSource
from .utm_source import UTMSource
from .helpers import SourceHelpers
from .source_base import SourceBase
from .pure_ad_utm_source import PureAdUtmSource
from .google_ad_utm_source import GoogleAdUtmSource
from .template_source import TemplateSource
Source = Union[OtherSource, PureAd, WhatsAppDefaultSource, TopicDefaultSource, UTMSource, PureAdUtmSource, GoogleAdUtmSource, TemplateSource]