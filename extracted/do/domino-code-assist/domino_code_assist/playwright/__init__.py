from playwright.sync_api import Page


def mouse_move_middle(page: Page, locator):
    page.wait_for_timeout(100)  # seems less flakey if we wait 100msec
    box = locator.bounding_box()
    x, y = box["x"] + box["width"] / 2, box["y"] + box["height"] / 2
    # move 100 pixels above the cell...
    page.mouse.move(x, box["y"] - 100)
    page.wait_for_timeout(100)
    # and move to the middle of the cell, in 10 steps
    page.mouse.move(x, y, steps=10)
