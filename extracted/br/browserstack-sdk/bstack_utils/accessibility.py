# coding: UTF-8
import sys
bstack11l1l1l_opy_ = sys.version_info [0] == 2
bstack1111ll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack111l_opy_ (bstack11lll11_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l1l1_opy_ = ord (bstack11lll11_opy_ [-1])
    bstack1l111_opy_ = bstack11lll11_opy_ [:-1]
    bstack11llll_opy_ = bstack1l1l1l1_opy_ % len (bstack1l111_opy_)
    bstack1l111l_opy_ = bstack1l111_opy_ [:bstack11llll_opy_] + bstack1l111_opy_ [bstack11llll_opy_:]
    if bstack11l1l1l_opy_:
        bstack1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    else:
        bstack1_opy_ = str () .join ([chr (ord (char) - bstack1111ll_opy_ - (bstack11l_opy_ + bstack1l1l1l1_opy_) % bstack111l1ll_opy_) for bstack11l_opy_, char in enumerate (bstack1l111l_opy_)])
    return eval (bstack1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111l1llll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111ll1lll1_opy_ as bstack1111l1ll1ll_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack1lllllllll_opy_, bstack1lll11lll11_opy_, bstack11l1111l1l_opy_, bstack1111lll1l1l_opy_, \
  bstack1111ll1llll_opy_, bstack1l11111l1l_opy_, get_host_info, bstack1111ll11ll1_opy_, bstack11111l1ll_opy_, error_handler, bstack1111l1lll1l_opy_, bstack1111ll1l111_opy_, bstack1llll11111_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack111111lll1_opy_ import bstack11lll11111_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack111111lll1_opy_ = bstack11lll11111_opy_()
@error_handler(class_method=False)
def _1111ll11l1l_opy_(driver, bstack1ll11l1lll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111l_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᰌ"): caps.get(bstack111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᰍ"), None),
        bstack111l_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᰎ"): bstack1ll11l1lll1_opy_.get(bstack111l_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᰏ"), None),
        bstack111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᰐ"): caps.get(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᰑ"), None),
        bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᰒ"): caps.get(bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᰓ"), None)
    }
  except Exception as error:
    logger.debug(bstack111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᰔ") + str(error))
  return response
def on():
    if os.environ.get(bstack111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᰕ"), None) is None or os.environ[bstack111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᰖ")] == bstack111l_opy_ (u"ࠤࡱࡹࡱࡲࠢᰗ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᰘ"), False) or any([p.get(bstack111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᰙ"), False) == True for p in config.get(bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᰚ"), [])])
def is_enabled_platform(config, bstack11l111lll_opy_):
  try:
    bstack1ll1ll1ll1l_opy_ = config.get(bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᰛ"), False)
    _1ll1l1llll1_opy_ = int(bstack11l111lll_opy_)
    if _1ll1l1llll1_opy_ < 0:
      _1ll1l1llll1_opy_ = 0
    bstack1ll11ll1_opy_ = config.get(bstack111l_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᰜ"), [])
    if _1ll1l1llll1_opy_ < len(bstack1ll11ll1_opy_) and bstack1ll11ll1_opy_[_1ll1l1llll1_opy_]:
      bstack1111lll1lll_opy_ = bstack1ll11ll1_opy_[_1ll1l1llll1_opy_].get(bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᰝ"), None)
    else:
      bstack1111lll1lll_opy_ = config.get(bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᰞ"), None)
    if bstack1111lll1lll_opy_ != None:
      bstack1ll1ll1ll1l_opy_ = bstack1111lll1lll_opy_
    bstack1111l1lllll_opy_ = os.getenv(bstack111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᰟ")) is not None and len(os.getenv(bstack111l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᰠ"))) > 0 and os.getenv(bstack111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᰡ")) != bstack111l_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᰢ")
    return bstack1ll1ll1ll1l_opy_ and bstack1111l1lllll_opy_
  except Exception as error:
    logger.debug(bstack111l_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᰣ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack11ll1lllll1_opy_ = os.getenv(bstack111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᰤ"))
  if bstack11ll1lllll1_opy_ is None:
    return True
  bstack11ll1lllll1_opy_ = json.loads(bstack11ll1lllll1_opy_)
  try:
    include_tags = bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᰥ")] if bstack111l_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᰦ") in bstack11ll1lllll1_opy_ and isinstance(bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᰧ")], list) else []
    exclude_tags = bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᰨ")] if bstack111l_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᰩ") in bstack11ll1lllll1_opy_ and isinstance(bstack11ll1lllll1_opy_[bstack111l_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᰪ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᰫ") + str(error))
  return False
def bstack1111llllll1_opy_(config, bstack1111llll1ll_opy_, bstack1111ll1l11l_opy_, bstack1111ll111l1_opy_):
  bstack1111ll111ll_opy_ = bstack1111lll1l1l_opy_(config)
  bstack1111lll1ll1_opy_ = bstack1111ll1llll_opy_(config)
  if bstack1111ll111ll_opy_ is None or bstack1111lll1ll1_opy_ is None:
    logger.error(bstack111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᰬ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᰭ"), bstack111l_opy_ (u"ࠫࢀࢃࠧᰮ")))
    data = {
        bstack111l_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᰯ"): config[bstack111l_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᰰ")],
        bstack111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᰱ"): config.get(bstack111l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᰲ"), os.path.basename(os.getcwd())),
        bstack111l_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬᰳ"): bstack1lllllllll_opy_(),
        bstack111l_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᰴ"): config.get(bstack111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᰵ"), bstack111l_opy_ (u"ࠬ࠭ᰶ")),
        bstack111l_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ᰷࠭"): {
            bstack111l_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ᰸"): bstack1111llll1ll_opy_,
            bstack111l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ᰹"): bstack1111ll1l11l_opy_,
            bstack111l_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᰺"): __version__,
            bstack111l_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ᰻"): bstack111l_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᰼"),
            bstack111l_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ᰽"): bstack111l_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᰾"),
            bstack111l_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᰿"): bstack1111ll111l1_opy_
        },
        bstack111l_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ᱀"): settings,
        bstack111l_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪ᱁"): bstack1111ll11ll1_opy_(),
        bstack111l_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪ᱂"): bstack1l11111l1l_opy_(),
        bstack111l_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭᱃"): get_host_info(),
        bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᱄"): bstack11l1111l1l_opy_(config)
    }
    headers = {
        bstack111l_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ᱅"): bstack111l_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ᱆"),
    }
    config = {
        bstack111l_opy_ (u"ࠨࡣࡸࡸ࡭࠭᱇"): (bstack1111ll111ll_opy_, bstack1111lll1ll1_opy_),
        bstack111l_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᱈"): headers
    }
    response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ᱉"), bstack1111l1ll1ll_opy_ + bstack111l_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫ᱊"), data, config)
    bstack1111l1ll11l_opy_ = response.json()
    if bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭᱋")]:
      parsed = json.loads(os.getenv(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ᱌"), bstack111l_opy_ (u"ࠧࡼࡿࠪᱍ")))
      parsed[bstack111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᱎ")] = bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠩࡧࡥࡹࡧࠧᱏ")][bstack111l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᱐")]
      os.environ[bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᱑")] = json.dumps(parsed)
      accessibility_scripts.bstack1l11l1l1_opy_(bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠬࡪࡡࡵࡣࠪ᱒")][bstack111l_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ᱓")])
      accessibility_scripts.bstack1l11l11l1l1_opy_(bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠧࡥࡣࡷࡥࠬ᱔")][bstack111l_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᱕")])
      accessibility_scripts.store()
      return bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠩࡧࡥࡹࡧࠧ᱖")][bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ᱗")], bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠫࡩࡧࡴࡢࠩ᱘")][bstack111l_opy_ (u"ࠬ࡯ࡤࠨ᱙")]
    else:
      logger.error(bstack111l_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧᱚ") + bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᱛ")])
      if bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᱜ")] == bstack111l_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫᱝ"):
        for bstack1111lllllll_opy_ in bstack1111l1ll11l_opy_[bstack111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᱞ")]:
          logger.error(bstack1111lllllll_opy_[bstack111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᱟ")])
      return None, None
  except Exception as error:
    logger.error(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨᱠ") +  str(error))
    return None, None
def bstack1111llll1l1_opy_():
  if os.getenv(bstack111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᱡ")) is None:
    return {
        bstack111l_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᱢ"): bstack111l_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᱣ"),
        bstack111l_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᱤ"): bstack111l_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩᱥ")
    }
  data = {bstack111l_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬᱦ"): bstack1lllllllll_opy_()}
  headers = {
      bstack111l_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᱧ"): bstack111l_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧᱨ") + os.getenv(bstack111l_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧᱩ")),
      bstack111l_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᱪ"): bstack111l_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᱫ")
  }
  response = bstack11111l1ll_opy_(bstack111l_opy_ (u"ࠪࡔ࡚࡚ࠧᱬ"), bstack1111l1ll1ll_opy_ + bstack111l_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ᱭ"), data, { bstack111l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᱮ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111l_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢᱯ") + bstack1lll11lll11_opy_().isoformat() + bstack111l_opy_ (u"࡛ࠧࠩᱰ"))
      return {bstack111l_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᱱ"): bstack111l_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᱲ"), bstack111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᱳ"): bstack111l_opy_ (u"ࠫࠬᱴ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣᱵ") + str(error))
    return {
        bstack111l_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᱶ"): bstack111l_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᱷ"),
        bstack111l_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᱸ"): str(error)
    }
def bstack1111lll111l_opy_(bstack1111lll1l11_opy_):
    return re.match(bstack111l_opy_ (u"ࡴࠪࡢࡡࡪࠫࠩ࡞࠱ࡠࡩ࠱ࠩࡀࠦࠪᱹ"), bstack1111lll1l11_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1111llll11l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1111llll11l_opy_ = desired_capabilities
        else:
          bstack1111llll11l_opy_ = {}
        bstack11ll1llll1l_opy_ = (bstack1111llll11l_opy_.get(bstack111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᱺ"), bstack111l_opy_ (u"ࠫࠬᱻ")).lower() or caps.get(bstack111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᱼ"), bstack111l_opy_ (u"࠭ࠧᱽ")).lower())
        if bstack11ll1llll1l_opy_ == bstack111l_opy_ (u"ࠧࡪࡱࡶࠫ᱾"):
            return True
        if bstack11ll1llll1l_opy_ == bstack111l_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩ᱿"):
            bstack1111lll1l11_opy_ = caps.get(bstack111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᲀ")) or bstack1111llll11l_opy_.get(bstack111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲁ"), {}).get(bstack111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᲂ"), bstack111l_opy_ (u"ࠬ࠭ᲃ"))
            if bstack1111lll1l11_opy_:
                try:
                    bstack1111l1ll111_opy_ = int(str(bstack1111lll1l11_opy_).split(bstack111l_opy_ (u"࠭࠮ࠨᲄ"))[0])
                    min_version = int(float(bstack1111l1ll1l1_opy_))
                    if bstack1111l1ll111_opy_ < min_version:
                        logger.warning(bstack1111l1l1lll_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack111l_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࠭ࠥࡴࠩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡱࡱ࠲ࠧᲅ"), bstack1111lll1l11_opy_)
            return True
        bstack11lll111l1l_opy_ = caps.get(bstack111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲆ"), {}).get(bstack111l_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᲇ"), caps.get(bstack111l_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᲈ"), bstack111l_opy_ (u"ࠫࠬᲉ")))
        if bstack11lll111l1l_opy_:
            logger.warning(bstack111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᲊ"))
            return False
        browser = (caps.get(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᲋"), bstack111l_opy_ (u"ࠧࠨ᲌")) or caps.get(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᲍"), bstack111l_opy_ (u"ࠩࠪ᲎"))).lower() or \
                  (bstack1111llll11l_opy_.get(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᲏"), bstack111l_opy_ (u"ࠫࠬᲐ")) or bstack1111llll11l_opy_.get(bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭Ბ"), bstack111l_opy_ (u"࠭ࠧᲒ"))).lower()
        if browser not in (bstack111l_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᲓ"), bstack111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠪᲔ"), bstack111l_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨᲕ")):
            logger.warning(bstack111l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᲖ"))
            return False
        browser_version = caps.get(bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲗ")) or caps.get(bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᲘ")) or bstack1111llll11l_opy_.get(bstack111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᲙ")) or bstack1111llll11l_opy_.get(bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᲚ"), {}).get(bstack111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲛ")) or bstack1111llll11l_opy_.get(bstack111l_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲜ"), {}).get(bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᲝ"))
        bstack11lll1llll1_opy_ = bstack1111l1llll1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack1111ll1ll11_opy_ = False
        if config is not None:
          bstack1111ll1ll11_opy_ = bstack111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᲞ") in config and str(config[bstack111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᲟ")]).lower() != bstack111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᲠ")
        if os.environ.get(bstack111l_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᲡ"), bstack111l_opy_ (u"ࠨࠩᲢ")).lower() == bstack111l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᲣ") or bstack1111ll1ll11_opy_:
          bstack11lll1llll1_opy_ = bstack1111l1llll1_opy_.bstack11llll1l1ll_opy_
        if browser_version and browser_version != bstack111l_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪᲤ") and int(browser_version.split(bstack111l_opy_ (u"ࠫ࠳࠭Ქ"))[0]) <= bstack11lll1llll1_opy_:
          logger.warning(bstack111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࠢᲦ") + str(bstack11lll1llll1_opy_) + bstack111l_opy_ (u"ࠨ࠮ࠣᲧ"))
          return False
        bstack11lll1l111l_opy_ = (caps.get(bstack111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᲨ"))
                         or bstack1111llll11l_opy_.get(bstack111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ჩ"), {})
                         or caps.get(bstack111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲪ"), {}))
        bstack1ll1ll11111_opy_ = bstack11lll1l111l_opy_.get(bstack111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᲫ"), []) if isinstance(bstack11lll1l111l_opy_, dict) else []
        if not isinstance(bstack1ll1ll11111_opy_, list):
            bstack1ll1ll11111_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack111l_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᲬ") or arg == bstack111l_opy_ (u"ࠬ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᲭ") or (arg.startswith(bstack111l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࠫᲮ")) and arg != bstack111l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨᲯ")))
               for arg in bstack1ll1ll11111_opy_):
            logger.warning(bstack111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᲰ"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᲱ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l11l111ll1_opy_ = config.get(bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᲲ"), {})
    bstack1l11l111ll1_opy_[bstack111l_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᲳ")] = os.getenv(bstack111l_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᲴ"))
    bstack1lll11111l_opy_ = json.loads(os.getenv(bstack111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᲵ"), bstack111l_opy_ (u"ࠧࡼࡿࠪᲶ"))).get(bstack111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲷ"))
    if not config[bstack111l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᲸ")].get(bstack111l_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᲹ")):
      if bstack111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᲺ") in caps:
        caps[bstack111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᲻")][bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᲼")] = bstack1l11l111ll1_opy_
        caps[bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᲽ")][bstack111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᲾ")][bstack111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᲿ")] = bstack1lll11111l_opy_
      else:
        caps[bstack111l_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳀")] = bstack1l11l111ll1_opy_
        caps[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳁")][bstack111l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᳂")] = bstack1lll11111l_opy_
  except Exception as error:
    logger.debug(bstack111l_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢ᳃") +  str(error))
def start_test_capture(driver, bstack1111ll11111_opy_):
  try:
    setattr(driver, bstack111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ᳄"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack111l_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ᳅")) == bstack111l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ᳆")):
        bstack1111ll1l1ll_opy_ = bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᳇"), None)
        if bstack1111ll1l1ll_opy_:
          if bstack1111ll11111_opy_:
            logger.info(bstack111l_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱࠲࠳ࠨ᳈"))
          return bstack1111ll11111_opy_
      bstack1111llll111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111llll111_opy_ = False
      bstack1111llll111_opy_ = url.scheme in [bstack111l_opy_ (u"ࠧ࡮ࡴࡵࡲࠥ᳉"), bstack111l_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ᳊")]
      if bstack1111llll111_opy_:
        if bstack1111ll11111_opy_:
          logger.info(bstack111l_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢ᳋"))
      return bstack1111ll11111_opy_
  except Exception as e:
    logger.error(bstack111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ᳌") + str(e))
    return False
def bstack111lll111l_opy_(driver, name, path):
  try:
    bstack11llll11111_opy_ = {
        bstack111l_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩ᳍"): threading.current_thread().current_test_uuid,
        bstack111l_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᳎"): os.environ.get(bstack111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᳏"), bstack111l_opy_ (u"ࠬ࠭᳐")),
        bstack111l_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪ᳑"): os.environ.get(bstack111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᳒"), bstack111l_opy_ (u"ࠨࠩ᳓"))
    }
    bstack1l1l111lll_opy_ = bstack111111lll1_opy_.bstack111111l11l_opy_(EVENTS.bstack11l1111111_opy_.value)
    logger.debug(bstack111l_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷ᳔ࠬ"))
    try:
      if (bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶ᳕ࠪ"), None) and bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ᳖࠭"), None)):
        scripts = {bstack111l_opy_ (u"ࠬࡹࡣࡢࡰ᳗ࠪ"): accessibility_scripts.perform_scan}
        bstack1111ll11lll_opy_ = json.loads(scripts[bstack111l_opy_ (u"ࠨࡳࡤࡣࡱ᳘ࠦ")].replace(bstack111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻᳙ࠢࠥ"), bstack111l_opy_ (u"ࠣࠤ᳚")))
        bstack1111ll11lll_opy_[bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᳛")][bstack111l_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦ᳜ࠪ")] = None
        scripts[bstack111l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ᳝")] = bstack111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀ᳞ࠠࠣ") + json.dumps(bstack1111ll11lll_opy_)
        accessibility_scripts.bstack1l11l1l1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack111l_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ᳟"): name}))
      bstack111111lll1_opy_.end(EVENTS.bstack11l1111111_opy_.value, bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᳠"), bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᳡"), True, None)
    except Exception as error:
      bstack111111lll1_opy_.end(EVENTS.bstack11l1111111_opy_.value, bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᳢"), bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠥ࠾ࡪࡴࡤ᳣ࠣ"), False, str(error))
    bstack1l1l111lll_opy_ = bstack111111lll1_opy_.bstack1111lllll1l_opy_(EVENTS.bstack11ll1lll11l_opy_.value)
    bstack111111lll1_opy_.mark(bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ᳤ࠦ"))
    try:
      if (bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸ᳥ࠬ"), None) and bstack1llll11111_opy_(threading.current_thread(), bstack111l_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᳦"), None)):
        scripts = {bstack111l_opy_ (u"ࠧࡴࡥࡤࡲ᳧ࠬ"): accessibility_scripts.perform_scan}
        bstack1111ll11lll_opy_ = json.loads(scripts[bstack111l_opy_ (u"ࠣࡵࡦࡥࡳࠨ᳨")].replace(bstack111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᳩ"), bstack111l_opy_ (u"ࠥࠦᳪ")))
        bstack1111ll11lll_opy_[bstack111l_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᳫ")][bstack111l_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᳬ")] = None
        scripts[bstack111l_opy_ (u"ࠨࡳࡤࡣࡱ᳭ࠦ")] = bstack111l_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᳮ") + json.dumps(bstack1111ll11lll_opy_)
        accessibility_scripts.bstack1l11l1l1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack11llll11111_opy_))
      bstack111111lll1_opy_.end(bstack1l1l111lll_opy_, bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᳯ"), bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᳰ"),True, None)
    except Exception as error:
      bstack111111lll1_opy_.end(bstack1l1l111lll_opy_, bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᳱ"), bstack1l1l111lll_opy_ + bstack111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᳲ"),False, str(error))
    logger.info(bstack111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᳳ"))
    try:
      bstack11lll11l1l1_opy_ = {
        bstack111l_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ᳴"): {
          bstack111l_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣᳵ"): bstack111l_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧᳶ"),
        },
        bstack111l_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ᳷"): {
          bstack111l_opy_ (u"ࠥࡦࡴࡪࡹࠣ᳸"): {
            bstack111l_opy_ (u"ࠦࡲࡹࡧࠣ᳹"): bstack111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᳺ"),
            bstack111l_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ᳻"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack11lll11l1l1_opy_, separators=(bstack111l_opy_ (u"ࠧ࠭ࠩ᳼"), bstack111l_opy_ (u"ࠨ࠼ࠪ᳽"))))
    except Exception as bstack1111ll111l_opy_:
      logger.debug(bstack111l_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣ᳾") + str(bstack1111ll111l_opy_) + bstack111l_opy_ (u"ࠥࠦ᳿"))
  except Exception as bstack11llll11l11_opy_:
    logger.error(bstack111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᴀ") + str(path) + bstack111l_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᴁ") + str(bstack11llll11l11_opy_))
def bstack1111lll1111_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᴂ")) and str(caps.get(bstack111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᴃ"))).lower() == bstack111l_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᴄ"):
        bstack11lll111111_opy_ = caps.get(bstack111l_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᴅ")) or caps.get(bstack111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᴆ"))
        if bstack11lll111111_opy_:
            try:
              bstack1111lll1l11_opy_ = str(bstack11lll111111_opy_).split(bstack111l_opy_ (u"ࠫ࠳࠭ᴇ"))[0]
              min_version = int(float(bstack1111l1ll1l1_opy_))
              if int(bstack1111lll1l11_opy_) < min_version:
                  logger.warning(bstack1111l1l1lll_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack111l_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠣࠫࠪࡹࠧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡯࡯࠰ࠥᴈ"), bstack11lll111111_opy_)
    return True
def bstack1lllll1l1ll_opy_(config):
  if bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴉ") in config:
        return config[bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴊ")]
  for platform in config.get(bstack111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᴋ"), []):
      if bstack111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴌ") in platform:
          return platform[bstack111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴍ")]
  return None
def bstack11l1l1l11l_opy_(bstack11l1lll11l_opy_):
  try:
    browser_name = bstack11l1lll11l_opy_[bstack111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᴎ")]
    browser_version = bstack11l1lll11l_opy_[bstack111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᴏ")]
    chrome_options = bstack11l1lll11l_opy_[bstack111l_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧᴐ")]
    try:
        bstack1111lll11ll_opy_ = int(browser_version.split(bstack111l_opy_ (u"ࠧ࠯ࠩᴑ"))[0])
    except ValueError as e:
        logger.error(bstack111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡣࡰࡰࡹࡩࡷࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠧᴒ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᴓ")):
        logger.warning(bstack111l_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᴔ"))
        return False
    if bstack1111lll11ll_opy_ < bstack1111l1llll1_opy_.bstack11llll1l1ll_opy_:
        logger.warning(bstack111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡯ࡲࡦࡵࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡺࡪࡸࡳࡪࡱࡱࠤࠧᴕ") + str(bstack1111l1llll1_opy_.bstack11llll1l1ll_opy_) + bstack111l_opy_ (u"ࠧࠦ࡯ࡳࠢ࡫࡭࡬࡮ࡥࡳ࠰ࠥᴖ"))
        return False
    bstack1ll1ll11111_opy_ = chrome_options.get(bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᴗ"), []) if chrome_options else []
    if not isinstance(bstack1ll1ll11111_opy_, list):
        bstack1ll1ll11111_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack111l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᴘ") or arg == bstack111l_opy_ (u"ࠨࡪࡨࡥࡩࡲࡥࡴࡵࠪᴙ") or (arg.startswith(bstack111l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧᴚ")) and arg != bstack111l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫᴛ")))
           for arg in bstack1ll1ll11111_opy_):
        logger.warning(bstack111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᴜ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack111l_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥ࡬࡯ࡳࠢ࡯ࡳࡨࡧ࡬ࠡࡅ࡫ࡶࡴࡳࡥ࠻ࠢࠥᴝ") + str(e))
    return False
def bstack11l1l1lll_opy_(bstack1ll1111l1_opy_, config):
    try:
      bstack11lll11llll_opy_ = bstack111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴞ") in config and config[bstack111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴟ")] == True
      bstack1111ll1ll11_opy_ = bstack111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᴠ") in config and str(config[bstack111l_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᴡ")]).lower() != bstack111l_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᴢ")
      if not (bstack11lll11llll_opy_ and (not bstack11l1111l1l_opy_(config) or bstack1111ll1ll11_opy_)):
        return bstack1ll1111l1_opy_
      bstack1111ll11l11_opy_ = accessibility_scripts.bstack1111ll1ll1l_opy_
      if bstack1111ll11l11_opy_ is None:
        logger.debug(bstack111l_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥࡧࡲࡦࠢࡑࡳࡳ࡫ࠢᴣ"))
        return bstack1ll1111l1_opy_
      bstack1111lllll11_opy_ = int(str(bstack1111ll1l111_opy_()).split(bstack111l_opy_ (u"ࠬ࠴ࠧᴤ"))[0])
      logger.debug(bstack111l_opy_ (u"ࠨࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࠨᴥ") + str(bstack1111lllll11_opy_) + bstack111l_opy_ (u"ࠢࠣᴦ"))
      if bstack1111lllll11_opy_ == 3 and isinstance(bstack1ll1111l1_opy_, dict) and bstack111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴧ") in bstack1ll1111l1_opy_ and bstack1111ll11l11_opy_ is not None:
        if bstack111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴨ") not in bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴩ")]:
          bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᴪ")][bstack111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᴫ")] = {}
        if bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᴬ") in bstack1111ll11l11_opy_:
          if bstack111l_opy_ (u"ࠧࡢࡴࡪࡷࠬᴭ") not in bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴮ")][bstack111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴯ")]:
            bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴰ")][bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴱ")][bstack111l_opy_ (u"ࠬࡧࡲࡨࡵࠪᴲ")] = []
          for arg in bstack1111ll11l11_opy_[bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᴳ")]:
            if arg not in bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᴴ")][bstack111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴵ")][bstack111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᴶ")]:
              bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴷ")][bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴸ")][bstack111l_opy_ (u"ࠬࡧࡲࡨࡵࠪᴹ")].append(arg)
        if bstack111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᴺ") in bstack1111ll11l11_opy_:
          if bstack111l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᴻ") not in bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴼ")][bstack111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴽ")]:
            bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴾ")][bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴿ")][bstack111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᵀ")] = []
          for ext in bstack1111ll11l11_opy_[bstack111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵁ")]:
            if ext not in bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵂ")][bstack111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵃ")][bstack111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵄ")]:
              bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵅ")][bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵆ")][bstack111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᵇ")].append(ext)
        if bstack111l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵈ") in bstack1111ll11l11_opy_:
          if bstack111l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵉ") not in bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᵊ")][bstack111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᵋ")]:
            bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵌ")][bstack111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵍ")][bstack111l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵎ")] = {}
          bstack1111l1lll1l_opy_(bstack1ll1111l1_opy_[bstack111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵏ")][bstack111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵐ")][bstack111l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵑ")],
                    bstack1111ll11l11_opy_[bstack111l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵒ")])
        os.environ[bstack111l_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᵓ")] = bstack111l_opy_ (u"ࠫࡹࡸࡵࡦࠩᵔ")
        return bstack1ll1111l1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1111l1_opy_, ChromeOptions):
          chrome_options = bstack1ll1111l1_opy_
        elif isinstance(bstack1ll1111l1_opy_, dict):
          for value in bstack1ll1111l1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1111l1_opy_, dict):
            bstack1ll1111l1_opy_[bstack111l_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᵕ")] = chrome_options
          else:
            bstack1ll1111l1_opy_ = chrome_options
        if bstack1111ll11l11_opy_ is not None:
          if bstack111l_opy_ (u"࠭ࡡࡳࡩࡶࠫᵖ") in bstack1111ll11l11_opy_:
                bstack1111ll1111l_opy_ = chrome_options.arguments or []
                new_args = bstack1111ll11l11_opy_[bstack111l_opy_ (u"ࠧࡢࡴࡪࡷࠬᵗ")]
                for arg in new_args:
                    if arg not in bstack1111ll1111l_opy_:
                        chrome_options.add_argument(arg)
          if bstack111l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᵘ") in bstack1111ll11l11_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵙ"), [])
                bstack1111lll11l1_opy_ = bstack1111ll11l11_opy_[bstack111l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵚ")]
                for extension in bstack1111lll11l1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᵛ") in bstack1111ll11l11_opy_:
                bstack1111ll1l1l1_opy_ = chrome_options.experimental_options.get(bstack111l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵜ"), {})
                bstack1111l1lll11_opy_ = bstack1111ll11l11_opy_[bstack111l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵝ")]
                bstack1111l1lll1l_opy_(bstack1111ll1l1l1_opy_, bstack1111l1lll11_opy_)
                chrome_options.add_experimental_option(bstack111l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵞ"), bstack1111ll1l1l1_opy_)
        os.environ[bstack111l_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᵟ")] = bstack111l_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᵠ")
        return bstack1ll1111l1_opy_
    except Exception as e:
      logger.error(bstack111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡧࡨ࡮ࡴࡧࠡࡰࡲࡲ࠲ࡈࡓࠡ࡫ࡱࡪࡷࡧࠠࡢ࠳࠴ࡽࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠣᵡ") + str(e))
      return bstack1ll1111l1_opy_