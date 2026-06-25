from abstra_internals.controllers.main import MainController


class TestIsBrowserSessionDead:
    """_browser_call tears down + rebuilds the browser only on whole-session
    death, never on a per-page error (which would needlessly discard other
    open tabs and then retry against an empty session)."""

    def test_browser_closed_is_session_dead(self):
        assert MainController._is_browser_session_dead(
            RuntimeError(
                "Browser has closed. Cannot create new pages. "
                "The browser session may have expired."
            )
        )

    def test_single_page_crash_is_not_session_dead(self):
        # Regression (review #3): a per-page crash must NOT nuke the session.
        assert not MainController._is_browser_session_dead(
            RuntimeError(
                "Browser page has closed or crashed. "
                "Call navigate_to_url to start a new session."
            )
        )

    def test_target_closed_on_single_tab_is_not_session_dead(self):
        assert not MainController._is_browser_session_dead(
            Exception("Page.title: Target page, context or browser has been closed")
        )

    def test_unrelated_error_is_not_session_dead(self):
        assert not MainController._is_browser_session_dead(
            ValueError("Page 'dummy' does not exist.")
        )
