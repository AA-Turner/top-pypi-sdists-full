from typing import Optional
from abc import ABC
import logging
import locale


class LocaleSupport(ABC):
    """LocaleSupport.

    Adding Support for Encoding and Locale to every Component in FlowTask.
    """

    encoding: str = "UTF-8"
    _locale: Optional[str] = None

    def __init__(self, *args, **kwargs):
        self.encoding = kwargs.pop('encoding', "UTF-8")
        self._locale = kwargs.pop('l18n', None)
        # Localization
        if self._locale is None:
            newloc = (locale.getlocale())[0]
            self._locale = f"{newloc}.{self.encoding}"
        else:
            if self.encoding not in self._locale:
                self._locale = f"{self._locale}.{self.encoding}"
        try:
            # avoid errors on unsupported locales
            locale.setlocale(locale.LC_TIME, self._locale)
        except (RuntimeError, NameError, locale.Error) as err:
            logging.warning(
                f"Error on Locale Support: {err}"
            )
            newloc = (locale.getlocale())[0]
            self._locale = f"{newloc}.UTF-8"
            locale.setlocale(locale.LC_TIME, self._locale)
        # Call super only if there’s a next class in the MRO
        try:
            super().__init__(*args, **kwargs)
        except TypeError:
            super().__init__()
