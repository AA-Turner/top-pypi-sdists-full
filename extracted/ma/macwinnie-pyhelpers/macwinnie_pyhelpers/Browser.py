#!/usr/bin/env python3
import atexit
import copy
import gc
import logging
import os
import pickle
from datetime import datetime
from typing import Callable
from urllib.parse import urlparse

import requests
from selenium.webdriver.remote.webdriver import WebDriver as SeleniumBrowser

session_file = os.getenv("BROWSER_SESSION_FILE", "session.pickle")


def helper_set_value_at_key(dictionary, dotted_key_string, value):
    keys = dotted_key_string.split(".")
    for key in keys[:-1]:
        dictionary = dictionary.setdefault(key, {})
    dictionary[keys[-1]] = value


class Browser:
    __basic_attributes = {  # private class attribute to determine all basic attributes to be allowed to be used
        "base_url": {  # ToDo: base url where the selenium browser and the `requests.session` is starting to operate from
            "types": [
                str,
            ]
        },
        "dump_session": {  # default: True ... wether the session information should be dumped to a session pickle file or not
            "types": [
                bool,
            ]
        },
        "ssl_ignore_error": {  # ignore SSL errors in `requests.session` – has to be applied on webdriver creation for selenium!
            "types": [
                bool,
            ]
        },
        "keep_selenium_alive": {  # set True to keep selenium alive after Browser instance was closed / deleted
            "types": [
                bool,
            ]
        },
        "selenium": {  # selenium webdriver to be used in Browser instance
            "types": [
                SeleniumBrowser,
            ]
        },
        "session_user_agent": {  # user agent to be used in `requests.session`
            "types": [
                str,
            ]
        },
    }

    def __init__(self, **basic_attributes):
        """method to initialize a Browser instance"""
        self.logger = logging.getLogger(__name__)
        self.__last_url = ""
        self.__cookies = {}
        self.__cookie_updated = {}

        for ba, bav in basic_attributes.items():
            self.set_basic(ba, bav)

        try:
            self.load_session()
        except FileNotFoundError as e:
            self.logger.info(str(e))
        except Exception as e:
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.logger.exception(str(e))
            else:
                self.logger.error(str(e))

        if not hasattr(self, "session"):
            self.logger.info("new session started")
            self.session = requests.Session()

        if hasattr(self, "session_user_agent"):
            self.session.headers.update({"user-agent": self.session_user_agent})

        if hasattr(self, "selenium"):
            self.sync_user_agent()
            self.session_transfer()

        if hasattr(self, "ssl_ignore_error") and self.ssl_ignore_error:
            import urllib3

            urllib3.disable_warnings()
            if hasattr(self, "selenium"):
                self.logger.info(
                    "Remember to set `acceptInsecureCerts` option for your selenium browser as well!"
                )

        atexit.register(self.__cleanup)

    def __cleanup(self):  # pragma: no cover
        """close browser instance

        magic function to close the browser and session instance
        """
        self.save_session()
        if hasattr(self, "selenium") and not (
            hasattr(self, "keep_selenium_alive") and not self.keep_selenium_alive
        ):
            self.logger.info("quitting selenium instance")
            self.selenium.quit()

    def load_session(self):
        """load requests session from Pickel dump

        Raises:
            FileNotFoundError: session dump file not found
            TypeError: non-session was stored in session dump file
        """
        if not hasattr(self, "dump_session") or self.dump_session:
            try:
                st = os.stat(session_file)
                with open(session_file, "rb") as f:
                    self.session = pickle.load(f)
                if not isinstance(self.session, requests.sessions.Session):
                    t = type(self.session)
                    try:
                        del self.session
                    except:  # pragma: no cover
                        pass
                    raise TypeError(
                        f"No Session object stored in {session_file} but an object of type {t}"
                    )
                else:
                    self.logger.info(f"Session loaded from {session_file}")
            except os.error:
                raise FileNotFoundError(f"No session file {session_file} found.")
        else:
            self.logger.info("Session file disabled by `dump_session` attribute.")

    def set_basic(self, attribute, value):
        """set basic attribute as in `__basic_attributes`

        Args:
            attribute (str): name of attribute, valid are ["base_url", "dump_session", "ssl_ignore_error",]
            value (str): value of attribute

        Raises:
            KeyError: attribute not part of the `__basic_attributes` list was given ...
            TypeError: attribute value type is not allowed
        """
        if attribute in self.__basic_attributes.keys():
            t = type(value)
            allowed = False
            if (
                "types" not in self.__basic_attributes[attribute]
                or t in self.__basic_attributes[attribute]["types"]
            ):
                allowed = True
            else:
                for at in self.__basic_attributes[attribute]["types"]:
                    if isinstance(value, at):
                        allowed = True
                        break

            if allowed:
                setattr(self, attribute, value)
            else:
                raise TypeError(
                    f"Type {t} not in allowed types {self.__basic_attributes[ attribute ]['types']} for attribute `{attribute}` ..."
                )
        else:
            raise KeyError(f"Invalid basic attribute `{attribute}` given ...")

    def save_session(self):  # pragma: no cover
        """save session as Pickel dump"""
        if not hasattr(self, "dump_session") or self.dump_session:
            with open(session_file, "wb") as f:
                pickle.dump(self.session, f)
            self.logger.info(f"Session saved in {session_file}")
        else:
            self.logger.info("Session file disabled by `dump_session` attribute.")

    def session_exec(self, method, *args, **kwargs):  # pragma: no cover
        """method proxy for requests session

        Args:
            method (str): name of method to be called on session
            *args: Variable length argument list to be passed to method
            **kwargs: Arbitrary keyword arguments to be passed to method

        Raises:
            AttributeError: method not found
            Exception: exception raised during method calling
        """
        try:
            mthd = getattr(self.session, method)
        except AttributeError as e:
            log = f"method `{method}` not found on session ..."
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.logger.exception(log)
            else:
                self.logger.error(log)
        else:
            try:
                rv = mthd(*args, **kwargs)
                if hasattr(rv, "url") and not isinstance(rv.url, Callable):
                    self.__last_url = rv.url
                self.session_transfer()
                return rv
            except Exception as e:
                raise e

    def selenium_exec(self, method, *args, **kwargs):  # pragma: no cover
        """method proxy for selenium browser

        Args:
            method (str): name of method to be called on selenium
            *args: Variable length argument list to be passed to method
            **kwargs: Arbitrary keyword arguments to be passed to method

        Raises:
            KeyError: selenium not defined for Browser instance
            AttributeError: method not found
            Exception: exception raised during method calling
        """
        if not hasattr(self, "selenium"):
            raise KeyError("No Selenium WebDriver defined in this Browser instance!")

        try:
            mthd = getattr(self.selenium, method)
        except AttributeError as e:
            log = f"method `{method}` not found on selenium webdriver ..."
            if self.logger.getEffectiveLevel() == logging.DEBUG:
                self.logger.exception(log)
            else:
                self.logger.error(log)
        else:
            try:
                rv = mthd(*args, **kwargs)
                self.__last_url = self.selenium.current_url
                self.selenium_transfer()
                return rv
            except Exception as e:
                raise e
        finally:
            gc.collect()

    def sync_user_agent(self):  # pragma: no cover
        """method syncing the user agent between requests session and selenium"""
        if hasattr(self, "selenium"):
            if not hasattr(self, "session_user_agent"):
                self.session.headers.update(
                    {
                        "user-agent": self.selenium.execute_script(
                            "return navigator.userAgent;"
                        )
                    }
                )

    def __update_cookies_cache(self, cookies):  # pragma: no cover
        """update private cookies cache of object

        Args:
            cookies (list): list of dictionaries like given of selenium webdriver by calling `.get_cookies()`.

        Returns:
            list: list of all cookies that were changed
        """
        changed = []
        for c in cookies:
            name = c["name"]
            domain = c["domain"][1:] if c["domain"].startswith(".") else c["domain"]
            value = c["value"]
            if domain not in self.__cookies:
                self.__cookies.update({domain: {}})
            if domain not in self.__cookie_updated:
                self.__cookie_updated.update({domain: {}})
            if (
                name in self.__cookies[domain]
                and self.__cookies[domain][name]["value"] != value
            ):
                del self.__cookies[domain][name]
            if name not in self.__cookies[domain]:
                self.__cookies[domain].update({name: c})
                self.__cookie_updated[domain].update({name: datetime.utcnow()})
                changed.append(c)
        return changed

    __cookie_keep_keys = [
        "name",
        "value",
        "path",
        "domain",
        "secure",
        "expires",
        "rest",
    ]
    __cookie_selenium_session_translate = {
        "expiry": "expires",
        "httpOnly": "rest.HttpOnly",
        "sameSite": "rest.SameSite",
    }

    def selenium_transfer(self):  # pragma: no cover
        """transfer data back from selenium to session"""
        self.sync_user_agent()
        cookies = self.selenium.get_cookies()
        to_update = self.__update_cookies_cache(cookies)
        ltu = len(to_update)
        if ltu > 0:
            self.logger.info(
                f"There are {ltu} Cookies that will be transferred to Session from Selenium now ..."
            )
            # check cookies on session and update
            for c in to_update:
                cookie = {k: c[k] for k in self.__cookie_keep_keys if k in c}
                for k, v in self.__cookie_selenium_session_translate.items():
                    if k in c:
                        helper_set_value_at_key(cookie, v, c[k])
                if cookie["domain"].startswith("."):
                    cookie["domain"] = cookie["domain"][1:]
                self.session.cookies.set(**cookie)

    def session_transfer(self):  # pragma: no cover
        """transfer data back from session to selenium"""
        cookies = []
        for c in self.session.cookies:
            cookie = {
                "name": c.name,
                "value": c.value,
                "path": c.path,
                "domain": c.domain,
                "secure": c.secure,
                "httpOnly": (
                    False
                    if "HttpOnly" not in c._rest
                    else True if c._rest["HttpOnly"] == None else c._rest["HttpOnly"]
                ),
                "sameSite": (
                    "None" if "sameSite" not in c._rest else c._rest["sameSite"]
                ),
                "expiry": c.expires,
            }
            cookies.append(cookie)
        to_update = self.__update_cookies_cache(cookies)
        ltu = len(to_update)
        if hasattr(self, "selenium") and ltu > 0:
            self.logger.info(
                f"There are {ltu} Cookies that will be transferred to Selenium from Session now ..."
            )
            # check cookies on selenium and update
            for c in to_update:
                selurl = urlparse(self.selenium.current_url)
                cd = copy.deepcopy(c["domain"])
                if cd.startswith("."):
                    cd = cd[1:]

                if selurl.netloc != cd:
                    self.selenium.get(f"http://{cd}")

                try:
                    self.selenium.delete_cookie(c["name"])
                except:
                    pass

                self.selenium.add_cookie(c)
