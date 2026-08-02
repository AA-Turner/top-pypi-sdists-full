import logging

from playwright.sync_api import sync_playwright

import agentql

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
URL = "https://www.youtube.com/"

if __name__ == "__main__":
    SEARCH_QUERY = """
    {
        search_input
        search_btn
    }
    """
    VIDEO_QUERY = """
    {
        videos[] {
            video_link
            video_title
            channel_name
        }
    }
    """
    DESCRIPTION_QUERY = """
    {
        description_text
    }
    """
    COMMENT_QUERY = """
    {
        comments[] {
            comment_author_name
            comment_text
        }
    }
    """
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        page = agentql.wrap(browser.new_page())
        session = page.goto(URL)
        try:
            # search query
            response = page.query_elements(SEARCH_QUERY)
            response.search_input.type("Oreo Separation Pump Gun JoergSprave", delay=75)
            response.search_btn.click()

            # video query
            response = page.query_elements(VIDEO_QUERY)
            log.debug(f"Clicking Youtube Video: {response.videos[0].video_title.text_content()}")
            response.videos[0].video_link.click()  # click the first youtube video

            # Scroll down to load comments
            page.wait_for_page_ready_state()
            for _ in range(3):
                page.mouse.wheel(delta_x=0, delta_y=300)
                page.wait_for_timeout(1000)

            # description query
            response = page.query_data(DESCRIPTION_QUERY)
            log.debug(f"Captured the following description: \n{response['description_text']}")

            # comment query
            response = page.query_data(COMMENT_QUERY)
            comments = response.get("comments", [])
            log.debug(f"Captured {len(comments)} comments! Here are top 5:")
            for item in comments[:5]:
                log.debug(f"Comment from {item['comment_author_name']}': {item['comment_text']}")

        except Exception as e:
            log.error(f"Found Error: {e}")
            raise e

        page.wait_for_timeout(10000)
