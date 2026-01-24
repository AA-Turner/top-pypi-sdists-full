from .src import *
class TLSAdapterSingleton:
    _instance: Optional[TLSAdapter] = None
    _config: Optional[Tuple[Optional[str], Optional[int], Optional[int]]] = None
    
    @staticmethod
    def get_instance(
        ciphers: Optional[Union[str, Sequence[str]]] = None,
        certification: Optional[int] = None,
        ssl_options: Optional[int] = None
    ) -> TLSAdapter:
        ciphers_str = normalize_ciphers(ciphers)
        config = (ciphers_str, certification, ssl_options)

        if TLSAdapterSingleton._instance is None or TLSAdapterSingleton._config != config:
            TLSAdapterSingleton._instance = TLSAdapter(
                ciphers=ciphers_str,
                certification=certification,
                ssl_options=ssl_options,
            )
            TLSAdapterSingleton._config = config

        return TLSAdapterSingleton._instance
