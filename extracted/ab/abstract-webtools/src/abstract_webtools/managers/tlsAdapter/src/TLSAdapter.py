from .imports import *
from .functions import *

class TLSAdapter(HTTPAdapter):
    """
    Requests adapter that injects a preconfigured SSLContext (from SSLManager)
    into both the main pool and any HTTPS proxy pools.
    """
    def __init__(
        self,
        ssl_manager: Optional[SSLManager] = None,
        ciphers: Optional[Union[str, Sequence[str]]] = None,
        certification: Optional[int] = None,   # e.g., ssl.CERT_REQUIRED
        ssl_options: Optional[int] = None
    ) -> None:
        ciphers_str = normalize_ciphers(ciphers)

        self.ssl_manager = ssl_manager or SSLManager(
            ciphers=ciphers_str,
            ssl_options=ssl_options,
            certification=certification,
        )
        # Expose normalized/canonical values for singleton comparisons
        self.ciphers: Optional[str] = getattr(self.ssl_manager, "ciphers", ciphers_str)
        self.certification: int = getattr(self.ssl_manager, "certification", ssl.CERT_REQUIRED)
        self.ssl_options: Optional[int] = getattr(self.ssl_manager, "ssl_options", None)
        self.ssl_context: ssl.SSLContext = self.ssl_manager.ssl_context

        super().__init__()

    # Use canonical signature for clarity across urllib3 versions
    def init_poolmanager(self, connections: int, maxsize: int, block: bool = False, **pool_kwargs) -> None:
        pool_kwargs["ssl_context"] = self.ssl_context
        super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

    def proxy_manager_for(self, proxy: str, **proxy_kwargs) -> ProxyManager:
        # only attach context for HTTPS proxies
        if proxy and str(proxy).lower().startswith("https://"):
            proxy_kwargs["ssl_context"] = self.ssl_context
        return super().proxy_manager_for(proxy, **proxy_kwargs)



