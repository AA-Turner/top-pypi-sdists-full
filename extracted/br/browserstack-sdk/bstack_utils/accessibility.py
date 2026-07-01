# coding: UTF-8
import sys
bstack1lll_opy_ = sys.version_info [0] == 2
bstack111l11l_opy_ = 2048
bstack11l_opy_ = 7
def bstack1l1llll_opy_ (bstack11ll1l1_opy_):
    global bstack111111l_opy_
    bstack111lll_opy_ = ord (bstack11ll1l1_opy_ [-1])
    bstack11llll_opy_ = bstack11ll1l1_opy_ [:-1]
    bstack1l11_opy_ = bstack111lll_opy_ % len (bstack11llll_opy_)
    bstackl_opy_ = bstack11llll_opy_ [:bstack1l11_opy_] + bstack11llll_opy_ [bstack1l11_opy_:]
    if bstack1lll_opy_:
        bstack11l111_opy_ = unicode () .join ([unichr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    else:
        bstack11l111_opy_ = str () .join ([chr (ord (char) - bstack111l11l_opy_ - (bstack1ll1l11_opy_ + bstack111lll_opy_) % bstack11l_opy_) for bstack1ll1l11_opy_, char in enumerate (bstackl_opy_)])
    return eval (bstack11l111_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111l111lll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111l1l1ll1_opy_ as bstack11111ll11l1_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack1l1111ll_opy_, bstack1llllllll_opy_, bstack111l11l11l_opy_, bstack11111ll111l_opy_, \
  bstack1111l11111l_opy_, bstack11111l1lll_opy_, get_host_info, bstack1111l111111_opy_, bstack1111ll1111_opy_, error_handler, bstack11111lllll1_opy_, bstack1111l11l11l_opy_, bstack11llll11_opy_, bstack1111l111l1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.performance_tester import PerformanceTester
from selenium.webdriver.chrome.options import Options as ChromeOptions
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
performance_tester = PerformanceTester()
def is_browser_supported_for_accessibility(browser_name):
    if not browser_name:
        return False
    return browser_name.lower() in bstack1111l111lll_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS
def get_browser_a11y_config(browser_name):
    if not browser_name:
        return None
    return bstack1111l111lll_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS.get(browser_name.lower())
def get_min_version_for_browser(browser_name, bstack1111l1l11ll_opy_=True, bstack11ll1ll1ll1_opy_=False):
    config = get_browser_a11y_config(browser_name)
    if not config:
        return None
    if bstack11ll1ll1ll1_opy_:
        return config.get(bstack1l1llll_opy_ (u"ࠬࡳࡩ࡯ࡡࡹࡩࡷࡹࡩࡰࡰࡢࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧỤ"), config[bstack1l1llll_opy_ (u"࠭࡭ࡪࡰࡢࡺࡪࡸࡳࡪࡱࡱࡣࡳࡵ࡮ࡠࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࠧụ")])
    if bstack1111l1l11ll_opy_:
        return config[bstack1l1llll_opy_ (u"ࠧ࡮࡫ࡱࡣࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࠫỦ")]
    else:
        return config[bstack1l1llll_opy_ (u"ࠨ࡯࡬ࡲࡤࡼࡥࡳࡵ࡬ࡳࡳࡥ࡮ࡰࡰࡢࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࠩủ")]
def get_browser_display_name(browser_name):
    config = get_browser_a11y_config(browser_name)
    return config[bstack1l1llll_opy_ (u"ࠩࡧ࡭ࡸࡶ࡬ࡢࡻࡢࡲࡦࡳࡥࠨỨ")] if config else browser_name
def requires_chrome_options_validation(browser_name):
    config = get_browser_a11y_config(browser_name)
    return config.get(bstack1l1llll_opy_ (u"ࠪࡶࡪࡷࡵࡪࡴࡨࡷࡤࡩࡨࡳࡱࡰࡩࡤࡵࡰࡵ࡫ࡲࡲࡸࡥࡣࡩࡧࡦ࡯ࠬứ"), False) if config else False
def is_version_supported(bstack11111lll111_opy_, min_version):
    try:
        result = bstack1111l111l1l_opy_(str(bstack11111lll111_opy_), str(min_version))
        return result >= 0
    except Exception as e:
        logger.debug(bstack1l1llll_opy_ (u"࡛ࠦ࡫ࡲࡴ࡫ࡲࡲࠥࡩ࡯࡮ࡲࡤࡶ࡮ࡹ࡯࡯ࠢࡩࡥ࡮ࡲࡥࡥࠢࡩࡳࡷࠦࡻࡶࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳࢃࠠࡷࡵࠣࡿࡲ࡯࡮ࡠࡸࡨࡶࡸ࡯࡯࡯ࡿ࠽ࠤࠧỪ") + str(e) + bstack1l1llll_opy_ (u"ࠧࠨừ"))
        return False
@error_handler(class_method=False)
def _11111lll1l1_opy_(driver, bstack11lll1111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1llll_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧỬ"): caps.get(bstack1l1llll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ử"), None),
        bstack1l1llll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬỮ"): bstack11lll1111_opy_.get(bstack1l1llll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬữ"), None),
        bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩỰ"): caps.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩự"), None),
        bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧỲ"): caps.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧỳ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1llll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫỴ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ỵ"), None) is None or os.environ[bstack1l1llll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧỶ")] == bstack1l1llll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣỷ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫỸ"), False) or any([p.get(bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬỹ"), False) == True for p in config.get(bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩỺ"), [])])
def is_enabled_platform(config, bstack1ll1l111l1_opy_):
  try:
    bstack1ll1lllll_opy_ = config.get(bstack1l1llll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧỻ"), False)
    _1ll111111_opy_ = int(bstack1ll1l111l1_opy_)
    if _1ll111111_opy_ < 0:
      _1ll111111_opy_ = 0
    bstack1ll11ll1_opy_ = config.get(bstack1l1llll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫỼ"), [])
    if _1ll111111_opy_ < len(bstack1ll11ll1_opy_) and bstack1ll11ll1_opy_[_1ll111111_opy_]:
      bstack11111llll11_opy_ = bstack1ll11ll1_opy_[_1ll111111_opy_].get(bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩỽ"), None)
    else:
      bstack11111llll11_opy_ = config.get(bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪỾ"), None)
    if bstack11111llll11_opy_ != None:
      bstack1ll1lllll_opy_ = bstack11111llll11_opy_
    bstack1111l1l1111_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩỿ")) is not None and len(os.getenv(bstack1l1llll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪἀ"))) > 0 and os.getenv(bstack1l1llll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫἁ")) != bstack1l1llll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬἂ")
    return bstack1ll1lllll_opy_ and bstack1111l1l1111_opy_
  except Exception as error:
    logger.debug(bstack1l1llll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨἃ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack11ll1l1llll_opy_ = os.getenv(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪἄ"))
  if bstack11ll1l1llll_opy_ is None:
    return True
  bstack11ll1l1llll_opy_ = json.loads(bstack11ll1l1llll_opy_)
  try:
    include_tags = bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨἅ")] if bstack1l1llll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩἆ") in bstack11ll1l1llll_opy_ and isinstance(bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪἇ")], list) else []
    exclude_tags = bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫἈ")] if bstack1l1llll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬἉ") in bstack11ll1l1llll_opy_ and isinstance(bstack11ll1l1llll_opy_[bstack1l1llll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭Ἂ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤἋ") + str(error))
  return False
def bstack1111l1l1l1l_opy_(config, bstack11111lll1ll_opy_, bstack11111ll1l11_opy_, bstack1111l11llll_opy_):
  bstack11111ll1l1l_opy_ = bstack11111ll111l_opy_(config)
  bstack1111l1l1lll_opy_ = bstack1111l11111l_opy_(config)
  if bstack11111ll1l1l_opy_ is None or bstack1111l1l1lll_opy_ is None:
    logger.error(bstack1l1llll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫἌ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬἍ"), bstack1l1llll_opy_ (u"ࠬࢁࡽࠨἎ")))
    data = {
        bstack1l1llll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫἏ"): config[bstack1l1llll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬἐ")],
        bstack1l1llll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫἑ"): config.get(bstack1l1llll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬἒ"), os.path.basename(os.getcwd())),
        bstack1l1llll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ἓ"): bstack1l1111ll_opy_(),
        bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩἔ"): config.get(bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨἕ"), bstack1l1llll_opy_ (u"࠭ࠧ἖")),
        bstack1l1llll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ἗"): {
            bstack1l1llll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨἘ"): bstack11111lll1ll_opy_,
            bstack1l1llll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬἙ"): bstack11111ll1l11_opy_,
            bstack1l1llll_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧἚ"): __version__,
            bstack1l1llll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭Ἓ"): bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬἜ"),
            bstack1l1llll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭Ἕ"): bstack1l1llll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ἞"),
            bstack1l1llll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ἟"): bstack1111l11llll_opy_
        },
        bstack1l1llll_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫἠ"): settings,
        bstack1l1llll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫἡ"): bstack1111l111111_opy_(),
        bstack1l1llll_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫἢ"): bstack11111l1lll_opy_(),
        bstack1l1llll_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧἣ"): get_host_info(),
        bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨἤ"): bstack111l11l11l_opy_(config)
    }
    headers = {
        bstack1l1llll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ἥ"): bstack1l1llll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫἦ"),
    }
    config = {
        bstack1l1llll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧἧ"): (bstack11111ll1l1l_opy_, bstack1111l1l1lll_opy_),
        bstack1l1llll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫἨ"): headers
    }
    response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠫࡕࡕࡓࡕࠩἩ"), bstack11111ll11l1_opy_ + bstack1l1llll_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬἪ"), data, config)
    bstack1111l11l1ll_opy_ = response.json()
    if bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧἫ")]:
      parsed = json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨἬ"), bstack1l1llll_opy_ (u"ࠨࡽࢀࠫἭ")))
      parsed[bstack1l1llll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪἮ")] = bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠪࡨࡦࡺࡡࠨἯ")][bstack1l1llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬἰ")]
      os.environ[bstack1l1llll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ἱ")] = json.dumps(parsed)
      accessibility_scripts.bstack1ll1l1ll1l_opy_(bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"࠭ࡤࡢࡶࡤࠫἲ")][bstack1l1llll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨἳ")])
      accessibility_scripts.bstack11lll1l1l1l_opy_(bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ἴ")][bstack1l1llll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫἵ")])
      accessibility_scripts.store()
      return bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠪࡨࡦࡺࡡࠨἶ")][bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩἷ")], bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠬࡪࡡࡵࡣࠪἸ")][bstack1l1llll_opy_ (u"࠭ࡩࡥࠩἹ")]
    else:
      logger.error(bstack1l1llll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨἺ") + bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩἻ")])
      if bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪἼ")] == bstack1l1llll_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬἽ"):
        for bstack11111ll1ll1_opy_ in bstack1111l11l1ll_opy_[bstack1l1llll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫἾ")]:
          logger.error(bstack11111ll1ll1_opy_[bstack1l1llll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭Ἷ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢὀ") +  str(error))
    return None, None
def bstack11111l1llll_opy_():
  if os.getenv(bstack1l1llll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬὁ")) is None:
    return {
        bstack1l1llll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨὂ"): bstack1l1llll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨὃ"),
        bstack1l1llll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫὄ"): bstack1l1llll_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪὅ")
    }
  data = {bstack1l1llll_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭὆"): bstack1l1111ll_opy_()}
  headers = {
      bstack1l1llll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭὇"): bstack1l1llll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨὈ") + os.getenv(bstack1l1llll_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨὉ")),
      bstack1l1llll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨὊ"): bstack1l1llll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭Ὃ")
  }
  response = bstack1111ll1111_opy_(bstack1l1llll_opy_ (u"ࠫࡕ࡛ࡔࠨὌ"), bstack11111ll11l1_opy_ + bstack1l1llll_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧὍ"), data, { bstack1l1llll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ὎"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1llll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣ὏") + bstack1llllllll_opy_().isoformat() + bstack1l1llll_opy_ (u"ࠨ࡜ࠪὐ"))
      return {bstack1l1llll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩὑ"): bstack1l1llll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫὒ"), bstack1l1llll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬὓ"): bstack1l1llll_opy_ (u"ࠬ࠭ὔ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1llll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤὕ") + str(error))
    return {
        bstack1l1llll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧὖ"): bstack1l1llll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧὗ"),
        bstack1l1llll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ὘"): str(error)
    }
def bstack1111l11ll11_opy_(bstack11111llll1l_opy_):
    return re.match(bstack1l1llll_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫὙ"), bstack11111llll1l_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11111lll11l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11111lll11l_opy_ = desired_capabilities
        else:
          bstack11111lll11l_opy_ = {}
        platform_name = (bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ὚"), bstack1l1llll_opy_ (u"ࠬ࠭Ὓ")).lower() or caps.get(bstack1l1llll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ὜"), bstack1l1llll_opy_ (u"ࠧࠨὝ")).lower())
        if platform_name == bstack1l1llll_opy_ (u"ࠨ࡫ࡲࡷࠬ὞"):
            return True
        if platform_name == bstack1l1llll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪὟ"):
            bstack11111llll1l_opy_ = caps.get(bstack1l1llll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬὠ")) or bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬὡ"), {}).get(bstack1l1llll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨὢ"), bstack1l1llll_opy_ (u"࠭ࠧὣ"))
            if bstack11111llll1l_opy_:
                try:
                    bstack11111l1lll1_opy_ = int(str(bstack11111llll1l_opy_).split(bstack1l1llll_opy_ (u"ࠧ࠯ࠩὤ"))[0])
                    min_version = int(float(bstack1111l11lll1_opy_))
                    if bstack11111l1lll1_opy_ < min_version:
                        logger.warning(bstack1111l1l11l1_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack1l1llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠦࠧࠦࡵࠪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡲࡲ࠳ࠨὥ"), bstack11111llll1l_opy_)
            return True
        device_name = caps.get(bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪὦ"), {}).get(bstack1l1llll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧὧ"), caps.get(bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫὨ"), bstack1l1llll_opy_ (u"ࠬ࠭Ὡ")))
        if device_name:
            logger.warning(bstack1l1llll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥὪ"))
            return False
        browser = (caps.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬὫ"), bstack1l1llll_opy_ (u"ࠨࠩὬ")) or caps.get(bstack1l1llll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪὭ"), bstack1l1llll_opy_ (u"ࠪࠫὮ"))).lower() or \
                  (bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩὯ"), bstack1l1llll_opy_ (u"ࠬ࠭ὰ")) or bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧά"), bstack1l1llll_opy_ (u"ࠧࠨὲ"))).lower()
        if not is_browser_supported_for_accessibility(browser):
            bstack11ll11lllll_opy_ = bstack1l1llll_opy_ (u"ࠨ࠮ࠣࠫέ").join([get_browser_display_name(b) for b in bstack1111l111lll_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS.keys()])
            logger.warning(bstack1l1llll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࠥὴ") + str(bstack11ll11lllll_opy_) + bstack1l1llll_opy_ (u"ࠥࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢή"))
            return False
        bstack1ll1l1l1l_opy_ = config.get(bstack1l1llll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ὶ"), True) if config is not None else True
        bstack11ll1ll1ll1_opy_ = False
        if config is not None:
          bstack11ll1ll1ll1_opy_ = bstack1l1llll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩί") in config and str(config[bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪὸ")]).lower() != bstack1l1llll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ό")
        if os.environ.get(bstack1l1llll_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ὺ"), bstack1l1llll_opy_ (u"ࠩࠪύ")).lower() == bstack1l1llll_opy_ (u"ࠪࡸࡷࡻࡥࠨὼ") or bstack11ll1ll1ll1_opy_:
            bstack1ll1l1l1l_opy_ = False
        min_version = get_min_version_for_browser(browser, bstack1ll1l1l1l_opy_, bstack11ll1ll1ll1_opy_)
        if not min_version:
            logger.warning(bstack1l1llll_opy_ (u"ࠦࡈࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡥࡧࡷࡩࡷࡳࡩ࡯ࡧࠣࡱ࡮ࡴࡩ࡮ࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡬࡯ࡳࠢࠥώ") + str(browser) + bstack1l1llll_opy_ (u"ࠧࠨ὾"))
            return False
        browser_version = (caps.get(bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ὿"))
                          or caps.get(bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᾀ"))
                          or bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᾁ"))
                          or bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᾂ"), {}).get(bstack1l1llll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᾃ"))
                          or bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᾄ"), {}).get(bstack1l1llll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᾅ")))
        if browser_version and browser_version != bstack1l1llll_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᾆ"):
            bstack11ll1lll1ll_opy_ = str(browser_version)
            if not is_version_supported(bstack11ll1lll1ll_opy_, min_version):
                display_name = get_browser_display_name(browser)
                logger.warning(bstack1l1llll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࠣᾇ") + str(display_name) + bstack1l1llll_opy_ (u"ࠣࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤࠧᾈ") + str(min_version) + bstack1l1llll_opy_ (u"ࠤࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠢᾉ"))
                return False
        if requires_chrome_options_validation(browser):
            bstack11ll1ll11l1_opy_ = (caps.get(bstack1l1llll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᾊ"))
                             or bstack11111lll11l_opy_.get(bstack1l1llll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᾋ"), {})
                             or caps.get(bstack1l1llll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᾌ"), {}))
            bstack1l1ll1lll_opy_ = bstack11ll1ll11l1_opy_.get(bstack1l1llll_opy_ (u"࠭ࡡࡳࡩࡶࠫᾍ"), []) if isinstance(bstack11ll1ll11l1_opy_, dict) else []
            if not isinstance(bstack1l1ll1lll_opy_, list):
                bstack1l1ll1lll_opy_ = []
            if any(isinstance(arg, str) and (arg == bstack1l1llll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᾎ") or arg == bstack1l1llll_opy_ (u"ࠨࡪࡨࡥࡩࡲࡥࡴࡵࠪᾏ") or (arg.startswith(bstack1l1llll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧᾐ")) and arg != bstack1l1llll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫᾑ")))
                   for arg in bstack1l1ll1lll_opy_):
                logger.warning(bstack1l1llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᾒ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack1l1llll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢᾓ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack11llll1lll1_opy_ = config.get(bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᾔ"), {})
    bstack11llll1lll1_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᾕ")] = os.getenv(bstack1l1llll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᾖ"))
    bstack11111lll1_opy_ = json.loads(os.getenv(bstack1l1llll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᾗ"), bstack1l1llll_opy_ (u"ࠪࡿࢂ࠭ᾘ"))).get(bstack1l1llll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᾙ"))
    if not config[bstack1l1llll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧᾚ")].get(bstack1l1llll_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧᾛ")):
      if bstack1l1llll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᾜ") in caps:
        caps[bstack1l1llll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᾝ")][bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᾞ")] = bstack11llll1lll1_opy_
        caps[bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᾟ")][bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᾠ")][bstack1l1llll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᾡ")] = bstack11111lll1_opy_
      else:
        caps[bstack1l1llll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᾢ")] = bstack11llll1lll1_opy_
        caps[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᾣ")][bstack1l1llll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᾤ")] = bstack11111lll1_opy_
  except Exception as error:
    logger.debug(bstack1l1llll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥᾥ") +  str(error))
def start_test_capture(driver, bstack11111ll11ll_opy_):
  try:
    setattr(driver, bstack1l1llll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪᾦ"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack1l1llll_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈࠬᾧ")) == bstack1l1llll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ࠭ᾨ")):
        bstack1111l11l111_opy_ = bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᾩ"), None)
        if bstack1111l11l111_opy_:
          if bstack11111ll11ll_opy_:
            logger.info(bstack1l1llll_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴࠮࠯ࠤᾪ"))
          return bstack11111ll11ll_opy_
      bstack1111l111l11_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111l111l11_opy_ = False
      bstack1111l111l11_opy_ = url.scheme in [bstack1l1llll_opy_ (u"ࠣࡪࡷࡸࡵࠨᾫ"), bstack1l1llll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᾬ")]
      if bstack1111l111l11_opy_:
        if bstack11111ll11ll_opy_:
          logger.info(bstack1l1llll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥᾭ"))
      return bstack11111ll11ll_opy_
  except Exception as e:
    logger.error(bstack1l1llll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᾮ") + str(e))
    return False
def bstack11ll11lll_opy_(driver, name, path):
  try:
    bstack11ll1l11111_opy_ = {
        bstack1l1llll_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᾯ"): threading.current_thread().current_test_uuid,
        bstack1l1llll_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᾰ"): os.environ.get(bstack1l1llll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᾱ"), bstack1l1llll_opy_ (u"ࠨࠩᾲ")),
        bstack1l1llll_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ᾳ"): os.environ.get(bstack1l1llll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᾴ"), bstack1l1llll_opy_ (u"ࠫࠬ᾵"))
    }
    random_label = performance_tester.mark_start(EVENTS.bstack11l111llll_opy_.value)
    logger.debug(bstack1l1llll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᾶ"))
    try:
      if (bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᾷ"), None) and bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᾸ"), None)):
        scripts = {bstack1l1llll_opy_ (u"ࠨࡵࡦࡥࡳ࠭Ᾱ"): accessibility_scripts.perform_scan}
        bstack1111l1111l1_opy_ = json.loads(scripts[bstack1l1llll_opy_ (u"ࠤࡶࡧࡦࡴࠢᾺ")].replace(bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨΆ"), bstack1l1llll_opy_ (u"ࠦࠧᾼ")))
        bstack1111l1111l1_opy_[bstack1l1llll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ᾽")][bstack1l1llll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ι")] = None
        scripts[bstack1l1llll_opy_ (u"ࠢࡴࡥࡤࡲࠧ᾿")] = bstack1l1llll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ῀") + json.dumps(bstack1111l1111l1_opy_)
        accessibility_scripts.bstack1ll1l1ll1l_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1l1llll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ῁"): name}))
      performance_tester.end(EVENTS.bstack11l111llll_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥῂ"), random_label + bstack1l1llll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤῃ"), True, None)
    except Exception as error:
      performance_tester.end(EVENTS.bstack11l111llll_opy_.value, random_label + bstack1l1llll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧῄ"), random_label + bstack1l1llll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ῅"), False, str(error))
    random_label = performance_tester.bstack11111ll1111_opy_(EVENTS.bstack11ll1ll1111_opy_.value)
    performance_tester.mark(random_label + bstack1l1llll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢῆ"))
    try:
      if (bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨῇ"), None) and bstack11llll11_opy_(threading.current_thread(), bstack1l1llll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫῈ"), None)):
        scripts = {bstack1l1llll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨΈ"): accessibility_scripts.perform_scan}
        bstack1111l1111l1_opy_ = json.loads(scripts[bstack1l1llll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤῊ")].replace(bstack1l1llll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣΉ"), bstack1l1llll_opy_ (u"ࠨࠢῌ")))
        bstack1111l1111l1_opy_[bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ῍")][bstack1l1llll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ῎")] = None
        scripts[bstack1l1llll_opy_ (u"ࠤࡶࡧࡦࡴࠢ῏")] = bstack1l1llll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨῐ") + json.dumps(bstack1111l1111l1_opy_)
        accessibility_scripts.bstack1ll1l1ll1l_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack11ll1l11111_opy_))
      performance_tester.end(random_label, random_label + bstack1l1llll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦῑ"), random_label + bstack1l1llll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥῒ"),True, None)
    except Exception as error:
      performance_tester.end(random_label, random_label + bstack1l1llll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨΐ"), random_label + bstack1l1llll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ῔"),False, str(error))
    logger.info(bstack1l1llll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦ῕"))
    try:
      bstack11ll1lll111_opy_ = {
        bstack1l1llll_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥῖ"): {
          bstack1l1llll_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦῗ"): bstack1l1llll_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣῘ"),
        },
        bstack1l1llll_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢῙ"): {
          bstack1l1llll_opy_ (u"ࠨࡢࡰࡦࡼࠦῚ"): {
            bstack1l1llll_opy_ (u"ࠢ࡮ࡵࡪࠦΊ"): bstack1l1llll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦ῜"),
            bstack1l1llll_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥ῝"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack11ll1lll111_opy_, separators=(bstack1l1llll_opy_ (u"ࠪ࠰ࠬ῞"), bstack1l1llll_opy_ (u"ࠫ࠿࠭῟"))))
    except Exception as bstack1ll1111ll1l_opy_:
      logger.debug(bstack1l1llll_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦῠ") + str(bstack1ll1111ll1l_opy_) + bstack1l1llll_opy_ (u"ࠨࠢῡ"))
  except Exception as bstack11ll1l1l1ll_opy_:
    logger.error(bstack1l1llll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤῢ") + str(path) + bstack1l1llll_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥΰ") + str(bstack11ll1l1l1ll_opy_))
def bstack1111l1l1l11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1llll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣῤ")) and str(caps.get(bstack1l1llll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤῥ"))).lower() == bstack1l1llll_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧῦ"):
        platform_version = caps.get(bstack1l1llll_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢῧ")) or caps.get(bstack1l1llll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣῨ"))
        if platform_version:
            try:
              bstack11111llll1l_opy_ = str(platform_version).split(bstack1l1llll_opy_ (u"ࠧ࠯ࠩῩ"))[0]
              min_version = int(float(bstack1111l11lll1_opy_))
              if int(bstack11111llll1l_opy_) < min_version:
                  logger.warning(bstack1111l1l11l1_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack1l1llll_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠦࠧࠦࡵࠪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡲࡲ࠳ࠨῪ"), platform_version)
    return True
def bstack1l11lll111_opy_(config):
  if bstack1l1llll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩΎ") in config:
        return config[bstack1l1llll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪῬ")]
  for platform in config.get(bstack1l1llll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ῭"), []):
      if bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ΅") in platform:
          return platform[bstack1l1llll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭`")]
  return None
def bstack1l1lll111l1_opy_(bstack1111l111ll_opy_):
    try:
        browser_name = bstack1111l111ll_opy_[bstack1l1llll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭῰")]
        browser_version = bstack1111l111ll_opy_[bstack1l1llll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ῱")]
        chrome_options = bstack1111l111ll_opy_[bstack1l1llll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪῲ")]
        if not is_browser_supported_for_accessibility(browser_name):
            bstack11ll11lllll_opy_ = bstack1l1llll_opy_ (u"ࠪ࠰ࠥ࠭ῳ").join([get_browser_display_name(b) for b in bstack1111l111lll_opy_.ACCESSIBILITY_SUPPORTED_BROWSERS.keys()])
            logger.warning(bstack1l1llll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࠧῴ") + str(bstack11ll11lllll_opy_) + bstack1l1llll_opy_ (u"ࠧࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ῵"))
            return False
        min_version = get_min_version_for_browser(browser_name, bstack1111l1l11ll_opy_=False)
        if not min_version:
            logger.warning(bstack1l1llll_opy_ (u"ࠨࡃࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡧࡩࡹ࡫ࡲ࡮࡫ࡱࡩࠥࡳࡩ࡯࡫ࡰࡹࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡧࡱࡵࠤࠧῶ") + str(browser_name) + bstack1l1llll_opy_ (u"ࠢࠣῷ"))
            return False
        if not is_version_supported(browser_version, min_version):
            display_name = get_browser_display_name(browser_name)
            logger.warning(bstack1l1llll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷ࡬ࡶࡪࡹࠠࠣῸ") + str(display_name) + bstack1l1llll_opy_ (u"ࠤࠣࡺࡪࡸࡳࡪࡱࡱࠤࠧΌ") + str(min_version) + bstack1l1llll_opy_ (u"ࠥࠤࡴࡸࠠࡩ࡫ࡪ࡬ࡪࡸ࠮ࠣῺ"))
            return False
        if requires_chrome_options_validation(browser_name):
            bstack1l1ll1lll_opy_ = chrome_options.get(bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡴࠩΏ"), []) if chrome_options else []
            if not isinstance(bstack1l1ll1lll_opy_, list):
                bstack1l1ll1lll_opy_ = []
            if any(isinstance(arg, str) and (arg == bstack1l1llll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩῼ") or arg == bstack1l1llll_opy_ (u"࠭ࡨࡦࡣࡧࡰࡪࡹࡳࠨ´") or (arg.startswith(bstack1l1llll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࠬ῾")) and arg != bstack1l1llll_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࡂࡴࡥࡸࠩ῿")))
                   for arg in bstack1l1ll1lll_opy_):
                logger.warning(bstack1l1llll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦ "))
                return False
        return True
    except Exception as e:
        logger.error(bstack1l1llll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡪࡴࡸࠠࡣࡴࡲࡻࡸ࡫ࡲ࠻ࠢࠥ ") + str(e))
        return False
def bstack1l1l1l11ll_opy_(bstack1ll1l11ll11_opy_, config):
    try:
      bstack11ll1l111ll_opy_ = bstack1l1llll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ ") in config and config[bstack1l1llll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ ")] == True
      bstack11ll1ll1ll1_opy_ = bstack1l1llll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ ") in config and str(config[bstack1l1llll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ ")]).lower() != bstack1l1llll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ ")
      if not (bstack11ll1l111ll_opy_ and (not bstack111l11l11l_opy_(config) or bstack11ll1ll1ll1_opy_)):
        return bstack1ll1l11ll11_opy_
      bstack1111l1l111l_opy_ = accessibility_scripts.bstack11111ll1lll_opy_
      if bstack1111l1l111l_opy_ is None:
        logger.debug(bstack1l1llll_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡫ࠠࡏࡱࡱࡩࠧ "))
        return bstack1ll1l11ll11_opy_
      bstack1111l11ll1l_opy_ = int(str(bstack1111l11l11l_opy_()).split(bstack1l1llll_opy_ (u"ࠪ࠲ࠬ "))[0])
      logger.debug(bstack1l1llll_opy_ (u"ࠦࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࠦ ") + str(bstack1111l11ll1l_opy_) + bstack1l1llll_opy_ (u"ࠧࠨ "))
      if bstack1111l11ll1l_opy_ == 3 and isinstance(bstack1ll1l11ll11_opy_, dict) and bstack1l1llll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭​") in bstack1ll1l11ll11_opy_ and bstack1111l1l111l_opy_ is not None:
        if bstack1l1llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ‌") not in bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ‍")]:
          bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ‎")][bstack1l1llll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ‏")] = {}
        if bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ‐") in bstack1111l1l111l_opy_:
          if bstack1l1llll_opy_ (u"ࠬࡧࡲࡨࡵࠪ‑") not in bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭‒")][bstack1l1llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ–")]:
            bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ—")][bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ―")][bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ‖")] = []
          for arg in bstack1111l1l111l_opy_[bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ‗")]:
            if arg not in bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ‘")][bstack1l1llll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ’")][bstack1l1llll_opy_ (u"ࠧࡢࡴࡪࡷࠬ‚")]:
              bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ‛")][bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ“")][bstack1l1llll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ”")].append(arg)
        if bstack1l1llll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ„") in bstack1111l1l111l_opy_:
          if bstack1l1llll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ‟") not in bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭†")][bstack1l1llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ‡")]:
            bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ•")][bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ‣")][bstack1l1llll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ․")] = []
          for ext in bstack1111l1l111l_opy_[bstack1l1llll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ‥")]:
            if ext not in bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ…")][bstack1l1llll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ‧")][bstack1l1llll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ ")]:
              bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ ")][bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ‪")][bstack1l1llll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ‫")].append(ext)
        if bstack1l1llll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ‬") in bstack1111l1l111l_opy_:
          if bstack1l1llll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ‭") not in bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭‮")][bstack1l1llll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ ")]:
            bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ‰")][bstack1l1llll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ‱")][bstack1l1llll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ′")] = {}
          bstack11111lllll1_opy_(bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ″")][bstack1l1llll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ‴")][bstack1l1llll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ‵")],
                    bstack1111l1l111l_opy_[bstack1l1llll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭‶")])
        os.environ[bstack1l1llll_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭‷")] = bstack1l1llll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ‸")
        return bstack1ll1l11ll11_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1l11ll11_opy_, ChromeOptions):
          chrome_options = bstack1ll1l11ll11_opy_
        elif isinstance(bstack1ll1l11ll11_opy_, dict):
          for value in bstack1ll1l11ll11_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1l11ll11_opy_, dict):
            bstack1ll1l11ll11_opy_[bstack1l1llll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫ‹")] = chrome_options
          else:
            bstack1ll1l11ll11_opy_ = chrome_options
        if bstack1111l1l111l_opy_ is not None:
          if bstack1l1llll_opy_ (u"ࠫࡦࡸࡧࡴࠩ›") in bstack1111l1l111l_opy_:
                bstack11111llllll_opy_ = chrome_options.arguments or []
                new_args = bstack1111l1l111l_opy_[bstack1l1llll_opy_ (u"ࠬࡧࡲࡨࡵࠪ※")]
                for arg in new_args:
                    if arg not in bstack11111llllll_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l1llll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ‼") in bstack1111l1l111l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l1llll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ‽"), [])
                bstack1111l11l1l1_opy_ = bstack1111l1l111l_opy_[bstack1l1llll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ‾")]
                for extension in bstack1111l11l1l1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l1llll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ‿") in bstack1111l1l111l_opy_:
                bstack1111l1111ll_opy_ = chrome_options.experimental_options.get(bstack1l1llll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ⁀"), {})
                bstack1111l111ll1_opy_ = bstack1111l1l111l_opy_[bstack1l1llll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ⁁")]
                bstack11111lllll1_opy_(bstack1111l1111ll_opy_, bstack1111l111ll1_opy_)
                chrome_options.add_experimental_option(bstack1l1llll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ⁂"), bstack1111l1111ll_opy_)
        os.environ[bstack1l1llll_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫ⁃")] = bstack1l1llll_opy_ (u"ࠧࡵࡴࡸࡩࠬ⁄")
        return bstack1ll1l11ll11_opy_
    except Exception as e:
      logger.error(bstack1l1llll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡥࡦ࡬ࡲ࡬ࠦ࡮ࡰࡰ࠰ࡆࡘࠦࡩ࡯ࡨࡵࡥࠥࡧ࠱࠲ࡻࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠨ⁅") + str(e))
      return bstack1ll1l11ll11_opy_