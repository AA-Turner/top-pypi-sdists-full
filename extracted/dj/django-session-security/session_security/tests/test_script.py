import datetime
import os
import time
import unittest

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .test_base import BaseLiveServerTestCase


class ScriptTestCase(BaseLiveServerTestCase):

    @unittest.skipIf(os.environ.get('CI'), 'flaky timing boundary in CI')
    def test_warning_shows_and_session_expires(self):
        start = datetime.datetime.now()

        for win in self.sel.window_handles:
            self.sel.switch_to.window(win)
            try:
                el = WebDriverWait(self.sel, self.max_warn_after).until(
                    expected_conditions.visibility_of_element_located(
                        (By.ID, "session_security_warning")
                    )
                )
                self.assertTrue(el.is_displayed())
            except Exception:
                self.fail('max_warn_after did not display session_security_warning')
        end = datetime.datetime.now()
        delta = end - start

        self.assertGreaterEqual(delta.seconds, self.min_warn_after)
        self.assertLessEqual(delta.seconds, self.max_warn_after)

        for win in self.sel.window_handles:
            self.sel.switch_to.window(win)
            try:
                el = WebDriverWait(self.sel, self.max_expire_after).until(
                    expected_conditions.visibility_of_element_located(
                        (By.ID, "id_password")
                    )
                )
                self.assertTrue(el.is_displayed())
                delta = datetime.datetime.now() - start
                self.assertGreaterEqual(delta.seconds, self.min_expire_after)
                self.assertLessEqual(delta.seconds, self.max_expire_after)
            except Exception:
                self.fail('session expired but login page did not appear')

    def test_activity_hides_warning(self):
        time.sleep(6 * .7)
        try:
            WebDriverWait(self.sel, self.max_warn_after).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "session_security_warning")
                )
            )

            self.press_space()

            for win in self.sel.window_handles:
                self.sel.switch_to.window(win)

            result = WebDriverWait(self.sel, 20).until(
                expected_conditions.invisibility_of_element_located(
                    (By.ID, "session_security_warning")
                )
            )
            self.assertTrue(result)
        except Exception:
            self.fail('warning did not appear before warn_after')

    def test_activity_prevents_warning(self):
        time.sleep(self.min_warn_after * .7)
        self.press_space()
        start = datetime.datetime.now()
        try:
            el = WebDriverWait(self.sel, self.max_warn_after).until(
                expected_conditions.visibility_of_element_located(
                    (By.ID, "session_security_warning")
                )
            )
            self.assertTrue(el.is_displayed())

            for win in self.sel.window_handles:
                self.sel.switch_to.window(win)

            delta = datetime.datetime.now() - start
            self.assertGreaterEqual(delta.seconds, self.min_warn_after)
        except Exception:
            self.fail('warning did not appear after activity reset')
