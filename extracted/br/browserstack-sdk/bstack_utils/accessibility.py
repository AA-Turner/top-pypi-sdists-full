# coding: UTF-8
import sys
bstack1l11_opy_ = sys.version_info [0] == 2
bstack11_opy_ = 2048
bstackl_opy_ = 7
def bstack111ll_opy_ (bstack1ll1ll1_opy_):
    global bstack1ll111_opy_
    bstack1l11l1l_opy_ = ord (bstack1ll1ll1_opy_ [-1])
    bstack1llll_opy_ = bstack1ll1ll1_opy_ [:-1]
    bstack1l1lll_opy_ = bstack1l11l1l_opy_ % len (bstack1llll_opy_)
    bstack1_opy_ = bstack1llll_opy_ [:bstack1l1lll_opy_] + bstack1llll_opy_ [bstack1l1lll_opy_:]
    if bstack1l11_opy_:
        bstack11l1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    else:
        bstack11l1lll_opy_ = str () .join ([chr (ord (char) - bstack11_opy_ - (bstack11l11l1_opy_ + bstack1l11l1l_opy_) % bstackl_opy_) for bstack11l11l1_opy_, char in enumerate (bstack1_opy_)])
    return eval (bstack11l1lll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111ll1ll1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111l1l1lll_opy_ as bstack1111l1l1l11_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack1111l1l1l_opy_, bstack1lll11ll11l_opy_, bstack11l1ll1l_opy_, bstack1111ll11lll_opy_, \
  bstack1111l1l1111_opy_, bstack1l11ll1111_opy_, get_host_info, bstack1111ll11l11_opy_, bstack1ll11l11l_opy_, error_handler, bstack1111l1ll11l_opy_, bstack1111ll111ll_opy_, bstack1ll11l1ll1_opy_, bstack1111l1lllll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11ll1l1l_opy_ import bstack111l1l1l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack11ll1l1l_opy_ = bstack111l1l1l_opy_()
def is_browser_supported_for_accessibility(browser_name):
    if not browser_name:
        return False
    return browser_name.lower() in bstack1111ll1ll1l_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS
def get_browser_a11y_config(browser_name):
    if not browser_name:
        return None
    return bstack1111ll1ll1l_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS.get(browser_name.lower())
def get_min_version_for_browser(browser_name, bstack1111l1l11ll_opy_=True, bstack1l1111111ll_opy_=False):
    config = get_browser_a11y_config(browser_name)
    if not config:
        return None
    if bstack1l1111111ll_opy_:
        return config.get(bstack111ll_opy_ (u"ࠩࡰ࡭ࡳࡥࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ᰺"), config[bstack111ll_opy_ (u"ࠪࡱ࡮ࡴ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡰࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫ᰻")])
    if bstack1111l1l11ll_opy_:
        return config[bstack111ll_opy_ (u"ࠫࡲ࡯࡮ࡠࡸࡨࡶࡸ࡯࡯࡯ࡡࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࠨ᰼")]
    else:
        return config[bstack111ll_opy_ (u"ࠬࡳࡩ࡯ࡡࡹࡩࡷࡹࡩࡰࡰࡢࡲࡴࡴ࡟ࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠭᰽")]
def get_browser_display_name(browser_name):
    config = get_browser_a11y_config(browser_name)
    return config[bstack111ll_opy_ (u"࠭ࡤࡪࡵࡳࡰࡦࡿ࡟࡯ࡣࡰࡩࠬ᰾")] if config else browser_name
def requires_chrome_options_validation(browser_name):
    config = get_browser_a11y_config(browser_name)
    return config.get(bstack111ll_opy_ (u"ࠧࡳࡧࡴࡹ࡮ࡸࡥࡴࡡࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࡢࡧ࡭࡫ࡣ࡬ࠩ᰿"), False) if config else False
def is_version_supported(bstack1111l11l11l_opy_, min_version):
    try:
        result = bstack1111l1lllll_opy_(str(bstack1111l11l11l_opy_), str(min_version))
        return result >= 0
    except Exception as e:
        logger.debug(bstack111ll_opy_ (u"ࠣࡘࡨࡶࡸ࡯࡯࡯ࠢࡦࡳࡲࡶࡡࡳ࡫ࡶࡳࡳࠦࡦࡢ࡫࡯ࡩࡩࠦࡦࡰࡴࠣࡿࡺࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࢀࠤࡻࡹࠠࡼ࡯࡬ࡲࡤࡼࡥࡳࡵ࡬ࡳࡳࢃ࠺ࠡࠤ᱀") + str(e) + bstack111ll_opy_ (u"ࠤࠥ᱁"))
        return False
@error_handler(class_method=False)
def _1111l1ll1ll_opy_(driver, bstack1ll11ll11ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111ll_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫ᱂"): caps.get(bstack111ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᱃"), None),
        bstack111ll_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᱄"): bstack1ll11ll11ll_opy_.get(bstack111ll_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ᱅"), None),
        bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭᱆"): caps.get(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᱇"), None),
        bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᱈"): caps.get(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᱉"), None)
    }
  except Exception as error:
    logger.debug(bstack111ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ᱊") + str(error))
  return response
def on():
    if os.environ.get(bstack111ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᱋"), None) is None or os.environ[bstack111ll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᱌")] == bstack111ll_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᱍ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᱎ"), False) or any([p.get(bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᱏ"), False) == True for p in config.get(bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᱐"), [])])
def is_enabled_platform(config, bstack1l1l11111_opy_):
  try:
    bstack1ll1ll1ll1l_opy_ = config.get(bstack111ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᱑"), False)
    _1ll1lll111l_opy_ = int(bstack1l1l11111_opy_)
    if _1ll1lll111l_opy_ < 0:
      _1ll1lll111l_opy_ = 0
    bstack11llllllll_opy_ = config.get(bstack111ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᱒"), [])
    if _1ll1lll111l_opy_ < len(bstack11llllllll_opy_) and bstack11llllllll_opy_[_1ll1lll111l_opy_]:
      bstack1111l11l1ll_opy_ = bstack11llllllll_opy_[_1ll1lll111l_opy_].get(bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᱓"), None)
    else:
      bstack1111l11l1ll_opy_ = config.get(bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᱔"), None)
    if bstack1111l11l1ll_opy_ != None:
      bstack1ll1ll1ll1l_opy_ = bstack1111l11l1ll_opy_
    bstack1111l1llll1_opy_ = os.getenv(bstack111ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᱕")) is not None and len(os.getenv(bstack111ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᱖"))) > 0 and os.getenv(bstack111ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᱗")) != bstack111ll_opy_ (u"ࠫࡳࡻ࡬࡭ࠩ᱘")
    return bstack1ll1ll1ll1l_opy_ and bstack1111l1llll1_opy_
  except Exception as error:
    logger.debug(bstack111ll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬ᱙") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l111111l11_opy_ = os.getenv(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᱚ"))
  if bstack1l111111l11_opy_ is None:
    return True
  bstack1l111111l11_opy_ = json.loads(bstack1l111111l11_opy_)
  try:
    include_tags = bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᱛ")] if bstack111ll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᱜ") in bstack1l111111l11_opy_ and isinstance(bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᱝ")], list) else []
    exclude_tags = bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᱞ")] if bstack111ll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᱟ") in bstack1l111111l11_opy_ and isinstance(bstack1l111111l11_opy_[bstack111ll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᱠ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111ll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᱡ") + str(error))
  return False
def bstack1111lll111l_opy_(config, bstack1111l1l1l1l_opy_, bstack1111l1l11l1_opy_, bstack1111ll11111_opy_):
  bstack1111l1l111l_opy_ = bstack1111ll11lll_opy_(config)
  bstack1111ll1l111_opy_ = bstack1111l1l1111_opy_(config)
  if bstack1111l1l111l_opy_ is None or bstack1111ll1l111_opy_ is None:
    logger.error(bstack111ll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᱢ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᱣ"), bstack111ll_opy_ (u"ࠩࡾࢁࠬᱤ")))
    data = {
        bstack111ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᱥ"): config[bstack111ll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᱦ")],
        bstack111ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᱧ"): config.get(bstack111ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᱨ"), os.path.basename(os.getcwd())),
        bstack111ll_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪᱩ"): bstack1111l1l1l_opy_(),
        bstack111ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᱪ"): config.get(bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᱫ"), bstack111ll_opy_ (u"ࠪࠫᱬ")),
        bstack111ll_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᱭ"): {
            bstack111ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᱮ"): bstack1111l1l1l1l_opy_,
            bstack111ll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᱯ"): bstack1111l1l11l1_opy_,
            bstack111ll_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᱰ"): __version__,
            bstack111ll_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᱱ"): bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᱲ"),
            bstack111ll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᱳ"): bstack111ll_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᱴ"),
            bstack111ll_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᱵ"): bstack1111ll11111_opy_
        },
        bstack111ll_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᱶ"): settings,
        bstack111ll_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨᱷ"): bstack1111ll11l11_opy_(),
        bstack111ll_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨᱸ"): bstack1l11ll1111_opy_(),
        bstack111ll_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫᱹ"): get_host_info(),
        bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᱺ"): bstack11l1ll1l_opy_(config)
    }
    headers = {
        bstack111ll_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᱻ"): bstack111ll_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᱼ"),
    }
    config = {
        bstack111ll_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᱽ"): (bstack1111l1l111l_opy_, bstack1111ll1l111_opy_),
        bstack111ll_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨ᱾"): headers
    }
    response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠨࡒࡒࡗ࡙࠭᱿"), bstack1111l1l1l11_opy_ + bstack111ll_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩᲀ"), data, config)
    bstack1111lll11l1_opy_ = response.json()
    if bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᲁ")]:
      parsed = json.loads(os.getenv(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᲂ"), bstack111ll_opy_ (u"ࠬࢁࡽࠨᲃ")))
      parsed[bstack111ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᲄ")] = bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠧࡥࡣࡷࡥࠬᲅ")][bstack111ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲆ")]
      os.environ[bstack111ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᲇ")] = json.dumps(parsed)
      accessibility_scripts.bstack11ll111l11_opy_(bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠪࡨࡦࡺࡡࠨᲈ")][bstack111ll_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᲉ")])
      accessibility_scripts.bstack1l1l1111l11_opy_(bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠬࡪࡡࡵࡣࠪᲊ")][bstack111ll_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᲋")])
      accessibility_scripts.store()
      return bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠧࡥࡣࡷࡥࠬ᲌")][bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭᲍")], bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ᲎")][bstack111ll_opy_ (u"ࠪ࡭ࡩ࠭᲏")]
    else:
      logger.error(bstack111ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬᲐ") + bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ბ")])
      if bstack1111lll11l1_opy_[bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᲒ")] == bstack111ll_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩᲓ"):
        for bstack1111ll11ll1_opy_ in bstack1111lll11l1_opy_[bstack111ll_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᲔ")]:
          logger.error(bstack1111ll11ll1_opy_[bstack111ll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᲕ")])
      return None, None
  except Exception as error:
    logger.error(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦᲖ") +  str(error))
    return None, None
def bstack1111l1ll111_opy_():
  if os.getenv(bstack111ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᲗ")) is None:
    return {
        bstack111ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᲘ"): bstack111ll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᲙ"),
        bstack111ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᲚ"): bstack111ll_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧᲛ")
    }
  data = {bstack111ll_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪᲜ"): bstack1111l1l1l_opy_()}
  headers = {
      bstack111ll_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᲝ"): bstack111ll_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬᲞ") + os.getenv(bstack111ll_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥᲟ")),
      bstack111ll_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᲠ"): bstack111ll_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᲡ")
  }
  response = bstack1ll11l11l_opy_(bstack111ll_opy_ (u"ࠨࡒࡘࡘࠬᲢ"), bstack1111l1l1l11_opy_ + bstack111ll_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫᲣ"), data, { bstack111ll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᲤ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111ll_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧᲥ") + bstack1lll11ll11l_opy_().isoformat() + bstack111ll_opy_ (u"ࠬࡠࠧᲦ"))
      return {bstack111ll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭Ყ"): bstack111ll_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᲨ"), bstack111ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᲩ"): bstack111ll_opy_ (u"ࠩࠪᲪ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨᲫ") + str(error))
    return {
        bstack111ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᲬ"): bstack111ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᲭ"),
        bstack111ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᲮ"): str(error)
    }
def bstack1111l11ll11_opy_(bstack1111l1lll11_opy_):
    return re.match(bstack111ll_opy_ (u"ࡲࠨࡠ࡟ࡨ࠰࠮࡜࠯࡞ࡧ࠯࠮ࡅࠤࠨᲯ"), bstack1111l1lll11_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1111ll111l1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1111ll111l1_opy_ = desired_capabilities
        else:
          bstack1111ll111l1_opy_ = {}
        bstack11llllll11l_opy_ = (bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᲰ"), bstack111ll_opy_ (u"ࠩࠪᲱ")).lower() or caps.get(bstack111ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᲲ"), bstack111ll_opy_ (u"ࠫࠬᲳ")).lower())
        if bstack11llllll11l_opy_ == bstack111ll_opy_ (u"ࠬ࡯࡯ࡴࠩᲴ"):
            return True
        if bstack11llllll11l_opy_ == bstack111ll_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧᲵ"):
            bstack1111l1lll11_opy_ = caps.get(bstack111ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᲶ")) or bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲷ"), {}).get(bstack111ll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲸ"), bstack111ll_opy_ (u"ࠪࠫᲹ"))
            if bstack1111l1lll11_opy_:
                try:
                    bstack1111l1l1ll1_opy_ = int(str(bstack1111l1lll11_opy_).split(bstack111ll_opy_ (u"ࠫ࠳࠭Ჺ"))[0])
                    min_version = int(float(bstack1111l11llll_opy_))
                    if bstack1111l1l1ll1_opy_ < min_version:
                        logger.warning(bstack1111l11l1l1_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack111ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠣࠫࠪࡹࠧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡯࡯࠰ࠥ᲻"), bstack1111l1lll11_opy_)
            return True
        bstack1l1111l1l11_opy_ = caps.get(bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᲼"), {}).get(bstack111ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᲽ"), caps.get(bstack111ll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᲾ"), bstack111ll_opy_ (u"ࠩࠪᲿ")))
        if bstack1l1111l1l11_opy_:
            logger.warning(bstack111ll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ᳀"))
            return False
        browser = (caps.get(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ᳁"), bstack111ll_opy_ (u"ࠬ࠭᳂")) or caps.get(bstack111ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᳃"), bstack111ll_opy_ (u"ࠧࠨ᳄"))).lower() or \
                  (bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᳅"), bstack111ll_opy_ (u"ࠩࠪ᳆")) or bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ᳇"), bstack111ll_opy_ (u"ࠫࠬ᳈"))).lower()
        if not is_browser_supported_for_accessibility(browser):
            bstack11lllll1111_opy_ = bstack111ll_opy_ (u"ࠬ࠲ࠠࠨ᳉").join([get_browser_display_name(b) for b in bstack1111ll1ll1l_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS.keys()])
            logger.warning(bstack111ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࠢ᳊") + str(bstack11lllll1111_opy_) + bstack111ll_opy_ (u"ࠢࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ᳋"))
            return False
        bstack1ll1lll1111_opy_ = config.get(bstack111ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ᳌"), True) if config is not None else True
        bstack1l1111111ll_opy_ = False
        if config is not None:
          bstack1l1111111ll_opy_ = bstack111ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᳍") in config and str(config[bstack111ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᳎")]).lower() != bstack111ll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ᳏")
        if os.environ.get(bstack111ll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ᳐"), bstack111ll_opy_ (u"࠭ࠧ᳑")).lower() == bstack111ll_opy_ (u"ࠧࡵࡴࡸࡩࠬ᳒") or bstack1l1111111ll_opy_:
            bstack1ll1lll1111_opy_ = False
        min_version = get_min_version_for_browser(browser, bstack1ll1lll1111_opy_, bstack1l1111111ll_opy_)
        if not min_version:
            logger.warning(bstack111ll_opy_ (u"ࠣࡅࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡩ࡫ࡴࡦࡴࡰ࡭ࡳ࡫ࠠ࡮࡫ࡱ࡭ࡲࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡩࡳࡷࠦࠢ᳓") + str(browser) + bstack111ll_opy_ (u"ࠤ᳔ࠥ"))
            return False
        browser_version = (caps.get(bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱ᳕ࠫ"))
                          or caps.get(bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ᳖࠭"))
                          or bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ᳗࠭"))
                          or bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹ᳘ࠧ"), {}).get(bstack111ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᳙"))
                          or bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᳚"), {}).get(bstack111ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᳛")))
        if browser_version and browser_version != bstack111ll_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶ᳜ࠪ"):
            bstack1l111l1l111_opy_ = str(browser_version)
            if not is_version_supported(bstack1l111l1l111_opy_, min_version):
                display_name = get_browser_display_name(browser)
                logger.warning(bstack111ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤ᳝ࠧ") + str(display_name) + bstack111ll_opy_ (u"ࠧࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠤ᳞") + str(min_version) + bstack111ll_opy_ (u"ࠨࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱᳟ࠦ"))
                return False
        if requires_chrome_options_validation(browser):
            bstack1l111l1ll1l_opy_ = (caps.get(bstack111ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᳠"))
                             or bstack1111ll111l1_opy_.get(bstack111ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᳡"), {})
                             or caps.get(bstack111ll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ᳢ࠩ"), {}))
            bstack1ll1l11lll1_opy_ = bstack1l111l1ll1l_opy_.get(bstack111ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᳣"), []) if isinstance(bstack1l111l1ll1l_opy_, dict) else []
            if not isinstance(bstack1ll1l11lll1_opy_, list):
                bstack1ll1l11lll1_opy_ = []
            if any(isinstance(arg, str) and (arg == bstack111ll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ᳤") or arg == bstack111ll_opy_ (u"ࠬ࡮ࡥࡢࡦ࡯ࡩࡸࡹ᳥ࠧ") or (arg.startswith(bstack111ll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀ᳦ࠫ")) and arg != bstack111ll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨ᳧")))
                   for arg in bstack1ll1l11lll1_opy_):
                logger.warning(bstack111ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰᳨ࠥ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack111ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᳩ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1l1ll1111_opy_ = config.get(bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᳪ"), {})
    bstack1l1l1ll1111_opy_[bstack111ll_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᳫ")] = os.getenv(bstack111ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᳬ"))
    bstack1l11111l_opy_ = json.loads(os.getenv(bstack111ll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒ᳭ࠧ"), bstack111ll_opy_ (u"ࠧࡼࡿࠪᳮ"))).get(bstack111ll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᳯ"))
    if not config[bstack111ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᳰ")].get(bstack111ll_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᳱ")):
      if bstack111ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᳲ") in caps:
        caps[bstack111ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᳳ")][bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᳴")] = bstack1l1l1ll1111_opy_
        caps[bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᳵ")][bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᳶ")][bstack111ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᳷")] = bstack1l11111l_opy_
      else:
        caps[bstack111ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳸")] = bstack1l1l1ll1111_opy_
        caps[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳹")][bstack111ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᳺ")] = bstack1l11111l_opy_
  except Exception as error:
    logger.debug(bstack111ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢ᳻") +  str(error))
def start_test_capture(driver, bstack1111lll1111_opy_):
  try:
    setattr(driver, bstack111ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ᳼"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack111ll_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ᳽")) == bstack111ll_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ᳾")):
        bstack1111ll1lll1_opy_ = bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᳿"), None)
        if bstack1111ll1lll1_opy_:
          if bstack1111lll1111_opy_:
            logger.info(bstack111ll_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱࠲࠳ࠨᴀ"))
          return bstack1111lll1111_opy_
      bstack1111ll1111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111ll1111l_opy_ = False
      bstack1111ll1111l_opy_ = url.scheme in [bstack111ll_opy_ (u"ࠧ࡮ࡴࡵࡲࠥᴁ"), bstack111ll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᴂ")]
      if bstack1111ll1111l_opy_:
        if bstack1111lll1111_opy_:
          logger.info(bstack111ll_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢᴃ"))
      return bstack1111lll1111_opy_
  except Exception as e:
    logger.error(bstack111ll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᴄ") + str(e))
    return False
def bstack11l1ll11l_opy_(driver, name, path):
  try:
    bstack1l111l11l1l_opy_ = {
        bstack111ll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᴅ"): threading.current_thread().current_test_uuid,
        bstack111ll_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᴆ"): os.environ.get(bstack111ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᴇ"), bstack111ll_opy_ (u"ࠬ࠭ᴈ")),
        bstack111ll_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪᴉ"): os.environ.get(bstack111ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᴊ"), bstack111ll_opy_ (u"ࠨࠩᴋ"))
    }
    bstack11111l11l_opy_ = bstack11ll1l1l_opy_.bstack1ll1111l1_opy_(EVENTS.bstack1lll1ll1ll_opy_.value)
    logger.debug(bstack111ll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᴌ"))
    try:
      if (bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᴍ"), None) and bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᴎ"), None)):
        scripts = {bstack111ll_opy_ (u"ࠬࡹࡣࡢࡰࠪᴏ"): accessibility_scripts.perform_scan}
        bstack1111l11lll1_opy_ = json.loads(scripts[bstack111ll_opy_ (u"ࠨࡳࡤࡣࡱࠦᴐ")].replace(bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᴑ"), bstack111ll_opy_ (u"ࠣࠤᴒ")))
        bstack1111l11lll1_opy_[bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᴓ")][bstack111ll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᴔ")] = None
        scripts[bstack111ll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᴕ")] = bstack111ll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᴖ") + json.dumps(bstack1111l11lll1_opy_)
        accessibility_scripts.bstack11ll111l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack111ll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᴗ"): name}))
      bstack11ll1l1l_opy_.end(EVENTS.bstack1lll1ll1ll_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᴘ"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᴙ"), True, None)
    except Exception as error:
      bstack11ll1l1l_opy_.end(EVENTS.bstack1lll1ll1ll_opy_.value, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᴚ"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᴛ"), False, str(error))
    bstack11111l11l_opy_ = bstack11ll1l1l_opy_.bstack1111ll1ll11_opy_(EVENTS.bstack1l1111lllll_opy_.value)
    bstack11ll1l1l_opy_.mark(bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᴜ"))
    try:
      if (bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᴝ"), None) and bstack1ll11l1ll1_opy_(threading.current_thread(), bstack111ll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᴞ"), None)):
        scripts = {bstack111ll_opy_ (u"ࠧࡴࡥࡤࡲࠬᴟ"): accessibility_scripts.perform_scan}
        bstack1111l11lll1_opy_ = json.loads(scripts[bstack111ll_opy_ (u"ࠣࡵࡦࡥࡳࠨᴠ")].replace(bstack111ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᴡ"), bstack111ll_opy_ (u"ࠥࠦᴢ")))
        bstack1111l11lll1_opy_[bstack111ll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᴣ")][bstack111ll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᴤ")] = None
        scripts[bstack111ll_opy_ (u"ࠨࡳࡤࡣࡱࠦᴥ")] = bstack111ll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᴦ") + json.dumps(bstack1111l11lll1_opy_)
        accessibility_scripts.bstack11ll111l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l111l11l1l_opy_))
      bstack11ll1l1l_opy_.end(bstack11111l11l_opy_, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᴧ"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᴨ"),True, None)
    except Exception as error:
      bstack11ll1l1l_opy_.end(bstack11111l11l_opy_, bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᴩ"), bstack11111l11l_opy_ + bstack111ll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᴪ"),False, str(error))
    logger.info(bstack111ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᴫ"))
    try:
      bstack11lllll1l1l_opy_ = {
        bstack111ll_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢᴬ"): {
          bstack111ll_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣᴭ"): bstack111ll_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧᴮ"),
        },
        bstack111ll_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦᴯ"): {
          bstack111ll_opy_ (u"ࠥࡦࡴࡪࡹࠣᴰ"): {
            bstack111ll_opy_ (u"ࠦࡲࡹࡧࠣᴱ"): bstack111ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᴲ"),
            bstack111ll_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢᴳ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack11lllll1l1l_opy_, separators=(bstack111ll_opy_ (u"ࠧ࠭ࠩᴴ"), bstack111ll_opy_ (u"ࠨ࠼ࠪᴵ"))))
    except Exception as bstack1111l1llll_opy_:
      logger.debug(bstack111ll_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣᴶ") + str(bstack1111l1llll_opy_) + bstack111ll_opy_ (u"ࠥࠦᴷ"))
  except Exception as bstack1l111111l1l_opy_:
    logger.error(bstack111ll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᴸ") + str(path) + bstack111ll_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᴹ") + str(bstack1l111111l1l_opy_))
def bstack1111l11ll1l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack111ll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᴺ")) and str(caps.get(bstack111ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᴻ"))).lower() == bstack111ll_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᴼ"):
        bstack11lllllllll_opy_ = caps.get(bstack111ll_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᴽ")) or caps.get(bstack111ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᴾ"))
        if bstack11lllllllll_opy_:
            try:
              bstack1111l1lll11_opy_ = str(bstack11lllllllll_opy_).split(bstack111ll_opy_ (u"ࠫ࠳࠭ᴿ"))[0]
              min_version = int(float(bstack1111l11llll_opy_))
              if int(bstack1111l1lll11_opy_) < min_version:
                  logger.warning(bstack1111l11l1l1_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack111ll_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠣࠫࠪࡹࠧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡯࡯࠰ࠥᵀ"), bstack11lllllllll_opy_)
    return True
def bstack111lll11ll_opy_(config):
  if bstack111ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᵁ") in config:
        return config[bstack111ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᵂ")]
  for platform in config.get(bstack111ll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᵃ"), []):
      if bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᵄ") in platform:
          return platform[bstack111ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᵅ")]
  return None
def bstack1lll1l1l1_opy_(bstack11l1l11l_opy_):
    try:
        browser_name = bstack11l1l11l_opy_[bstack111ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᵆ")]
        browser_version = bstack11l1l11l_opy_[bstack111ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᵇ")]
        chrome_options = bstack11l1l11l_opy_[bstack111ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧᵈ")]
        if not is_browser_supported_for_accessibility(browser_name):
            bstack11lllll1111_opy_ = bstack111ll_opy_ (u"ࠧ࠭ࠢࠪᵉ").join([get_browser_display_name(b) for b in bstack1111ll1ll1l_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS.keys()])
            logger.warning(bstack111ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࠤᵊ") + str(bstack11lllll1111_opy_) + bstack111ll_opy_ (u"ࠤࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᵋ"))
            return False
        min_version = get_min_version_for_browser(browser_name, bstack1111l1l11ll_opy_=False)
        if not min_version:
            logger.warning(bstack111ll_opy_ (u"ࠥࡇࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡤࡦࡶࡨࡶࡲ࡯࡮ࡦࠢࡰ࡭ࡳ࡯࡭ࡶ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡫ࡵࡲࠡࠤᵌ") + str(browser_name) + bstack111ll_opy_ (u"ࠦࠧᵍ"))
            return False
        if not is_version_supported(browser_version, min_version):
            display_name = get_browser_display_name(browser_name)
            logger.warning(bstack111ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࠧᵎ") + str(display_name) + bstack111ll_opy_ (u"ࠨࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠤᵏ") + str(min_version) + bstack111ll_opy_ (u"ࠢࠡࡱࡵࠤ࡭࡯ࡧࡩࡧࡵ࠲ࠧᵐ"))
            return False
        if requires_chrome_options_validation(browser_name):
            bstack1ll1l11lll1_opy_ = chrome_options.get(bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵑ"), []) if chrome_options else []
            if not isinstance(bstack1ll1l11lll1_opy_, list):
                bstack1ll1l11lll1_opy_ = []
            if any(isinstance(arg, str) and (arg == bstack111ll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᵒ") or arg == bstack111ll_opy_ (u"ࠪ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᵓ") or (arg.startswith(bstack111ll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࠩᵔ")) and arg != bstack111ll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࡱࡩࡼ࠭ᵕ")))
                   for arg in bstack1ll1l11lll1_opy_):
                logger.warning(bstack111ll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᵖ"))
                return False
        return True
    except Exception as e:
        logger.error(bstack111ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡶࡲࡳࡳࡷࡺࠠࡧࡱࡵࠤࡧࡸ࡯ࡸࡵࡨࡶ࠿ࠦࠢᵗ") + str(e))
        return False
def bstack1l1lll1ll_opy_(bstack1ll1lll1ll_opy_, config):
    try:
      bstack11lllll11l1_opy_ = bstack111ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᵘ") in config and config[bstack111ll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᵙ")] == True
      bstack1l1111111ll_opy_ = bstack111ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᵚ") in config and str(config[bstack111ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᵛ")]).lower() != bstack111ll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᵜ")
      if not (bstack11lllll11l1_opy_ and (not bstack11l1ll1l_opy_(config) or bstack1l1111111ll_opy_)):
        return bstack1ll1lll1ll_opy_
      bstack1111ll1l1l1_opy_ = accessibility_scripts.bstack1111ll1l1ll_opy_
      if bstack1111ll1l1l1_opy_ is None:
        logger.debug(bstack111ll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹࠠࡢࡴࡨࠤࡓࡵ࡮ࡦࠤᵝ"))
        return bstack1ll1lll1ll_opy_
      bstack1111ll11l1l_opy_ = int(str(bstack1111ll111ll_opy_()).split(bstack111ll_opy_ (u"ࠧ࠯ࠩᵞ"))[0])
      logger.debug(bstack111ll_opy_ (u"ࠣࡕࡨࡰࡪࡴࡩࡶ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡩ࡫ࡴࡦࡥࡷࡩࡩࡀࠠࠣᵟ") + str(bstack1111ll11l1l_opy_) + bstack111ll_opy_ (u"ࠤࠥᵠ"))
      if bstack1111ll11l1l_opy_ == 3 and isinstance(bstack1ll1lll1ll_opy_, dict) and bstack111ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵡ") in bstack1ll1lll1ll_opy_ and bstack1111ll1l1l1_opy_ is not None:
        if bstack111ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵢ") not in bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵣ")]:
          bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵤ")][bstack111ll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵥ")] = {}
        if bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵦ") in bstack1111ll1l1l1_opy_:
          if bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᵧ") not in bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵨ")][bstack111ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵩ")]:
            bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵪ")][bstack111ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᵫ")][bstack111ll_opy_ (u"ࠧࡢࡴࡪࡷࠬᵬ")] = []
          for arg in bstack1111ll1l1l1_opy_[bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵭ")]:
            if arg not in bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵮ")][bstack111ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵯ")][bstack111ll_opy_ (u"ࠫࡦࡸࡧࡴࠩᵰ")]:
              bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵱ")][bstack111ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᵲ")][bstack111ll_opy_ (u"ࠧࡢࡴࡪࡷࠬᵳ")].append(arg)
        if bstack111ll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᵴ") in bstack1111ll1l1l1_opy_:
          if bstack111ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵵ") not in bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵶ")][bstack111ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵷ")]:
            bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵸ")][bstack111ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᵹ")][bstack111ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᵺ")] = []
          for ext in bstack1111ll1l1l1_opy_[bstack111ll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᵻ")]:
            if ext not in bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵼ")][bstack111ll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵽ")][bstack111ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᵾ")]:
              bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵿ")][bstack111ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᶀ")][bstack111ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᶁ")].append(ext)
        if bstack111ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᶂ") in bstack1111ll1l1l1_opy_:
          if bstack111ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᶃ") not in bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᶄ")][bstack111ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᶅ")]:
            bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᶆ")][bstack111ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᶇ")][bstack111ll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᶈ")] = {}
          bstack1111l1ll11l_opy_(bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᶉ")][bstack111ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᶊ")][bstack111ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᶋ")],
                    bstack1111ll1l1l1_opy_[bstack111ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᶌ")])
        os.environ[bstack111ll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᶍ")] = bstack111ll_opy_ (u"࠭ࡴࡳࡷࡨࠫᶎ")
        return bstack1ll1lll1ll_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1lll1ll_opy_, ChromeOptions):
          chrome_options = bstack1ll1lll1ll_opy_
        elif isinstance(bstack1ll1lll1ll_opy_, dict):
          for value in bstack1ll1lll1ll_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1lll1ll_opy_, dict):
            bstack1ll1lll1ll_opy_[bstack111ll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨᶏ")] = chrome_options
          else:
            bstack1ll1lll1ll_opy_ = chrome_options
        if bstack1111ll1l1l1_opy_ is not None:
          if bstack111ll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᶐ") in bstack1111ll1l1l1_opy_:
                bstack1111l1lll1l_opy_ = chrome_options.arguments or []
                new_args = bstack1111ll1l1l1_opy_[bstack111ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᶑ")]
                for arg in new_args:
                    if arg not in bstack1111l1lll1l_opy_:
                        chrome_options.add_argument(arg)
          if bstack111ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᶒ") in bstack1111ll1l1l1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack111ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᶓ"), [])
                bstack1111l1ll1l1_opy_ = bstack1111ll1l1l1_opy_[bstack111ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᶔ")]
                for extension in bstack1111l1ll1l1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack111ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᶕ") in bstack1111ll1l1l1_opy_:
                bstack1111ll1llll_opy_ = chrome_options.experimental_options.get(bstack111ll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᶖ"), {})
                bstack1111ll1l11l_opy_ = bstack1111ll1l1l1_opy_[bstack111ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᶗ")]
                bstack1111l1ll11l_opy_(bstack1111ll1llll_opy_, bstack1111ll1l11l_opy_)
                chrome_options.add_experimental_option(bstack111ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᶘ"), bstack1111ll1llll_opy_)
        os.environ[bstack111ll_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᶙ")] = bstack111ll_opy_ (u"ࠫࡹࡸࡵࡦࠩᶚ")
        return bstack1ll1lll1ll_opy_
    except Exception as e:
      logger.error(bstack111ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡩࡪࡩ࡯ࡩࠣࡲࡴࡴ࠭ࡃࡕࠣ࡭ࡳ࡬ࡲࡢࠢࡤ࠵࠶ࡿࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠥᶛ") + str(e))
      return bstack1ll1lll1ll_opy_