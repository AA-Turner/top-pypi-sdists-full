# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1lll_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack1ll1l11_opy_ (bstack11l1lll_opy_):
    global bstack1l11ll1_opy_
    bstack111lll_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1l11_opy_ = bstack11l1lll_opy_ [:-1]
    bstack111111_opy_ = bstack111lll_opy_ % len (bstack1l1l11_opy_)
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ [:bstack111111_opy_] + bstack1l1l11_opy_ [bstack111111_opy_:]
    if bstack1ll11_opy_:
        bstack1llllll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    else:
        bstack1llllll_opy_ = str () .join ([chr (ord (char) - bstack1lll_opy_ - (bstack1l1l1_opy_ + bstack111lll_opy_) % bstack1111ll1_opy_) for bstack1l1l1_opy_, char in enumerate (bstack1ll1l1l_opy_)])
    return eval (bstack1llllll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111lll1ll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111llll11l_opy_ as bstack1111l1l1lll_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack111ll1ll1l_opy_, bstack1lll1l11ll1_opy_, bstack111l1lll1l_opy_, bstack1111ll11lll_opy_, \
  bstack1111l1ll1l1_opy_, bstack1111l1111l_opy_, get_host_info, bstack1111l1lll11_opy_, bstack11llll11ll_opy_, error_handler, bstack1111ll1l1ll_opy_, bstack1111l1lllll_opy_, bstack11l11l1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1111llll1l_opy_ import bstack11l1111l1l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1111llll1l_opy_ = bstack11l1111l1l_opy_()
@error_handler(class_method=False)
def _1111l1ll1ll_opy_(driver, bstack1ll11l11ll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1l11_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᰌ"): caps.get(bstack1ll1l11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᰍ"), None),
        bstack1ll1l11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᰎ"): bstack1ll11l11ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᰏ"), None),
        bstack1ll1l11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᰐ"): caps.get(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᰑ"), None),
        bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᰒ"): caps.get(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᰓ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᰔ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᰕ"), None) is None or os.environ[bstack1ll1l11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᰖ")] == bstack1ll1l11_opy_ (u"ࠤࡱࡹࡱࡲࠢᰗ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᰘ"), False) or any([p.get(bstack1ll1l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᰙ"), False) == True for p in config.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᰚ"), [])])
def is_enabled_platform(config, bstack11ll1l111_opy_):
  try:
    bstack1ll1ll1ll1l_opy_ = config.get(bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᰛ"), False)
    _1lll111l11l_opy_ = int(bstack11ll1l111_opy_)
    if _1lll111l11l_opy_ < 0:
      _1lll111l11l_opy_ = 0
    bstack1llll11ll1_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᰜ"), [])
    if _1lll111l11l_opy_ < len(bstack1llll11ll1_opy_) and bstack1llll11ll1_opy_[_1lll111l11l_opy_]:
      bstack1111ll1lll1_opy_ = bstack1llll11ll1_opy_[_1lll111l11l_opy_].get(bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᰝ"), None)
    else:
      bstack1111ll1lll1_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᰞ"), None)
    if bstack1111ll1lll1_opy_ != None:
      bstack1ll1ll1ll1l_opy_ = bstack1111ll1lll1_opy_
    bstack1111ll111l1_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᰟ")) is not None and len(os.getenv(bstack1ll1l11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᰠ"))) > 0 and os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᰡ")) != bstack1ll1l11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᰢ")
    return bstack1ll1ll1ll1l_opy_ and bstack1111ll111l1_opy_
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᰣ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l111l1llll_opy_ = os.getenv(bstack1ll1l11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᰤ"))
  if bstack1l111l1llll_opy_ is None:
    return True
  bstack1l111l1llll_opy_ = json.loads(bstack1l111l1llll_opy_)
  try:
    include_tags = bstack1l111l1llll_opy_[bstack1ll1l11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᰥ")] if bstack1ll1l11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᰦ") in bstack1l111l1llll_opy_ and isinstance(bstack1l111l1llll_opy_[bstack1ll1l11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᰧ")], list) else []
    exclude_tags = bstack1l111l1llll_opy_[bstack1ll1l11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᰨ")] if bstack1ll1l11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᰩ") in bstack1l111l1llll_opy_ and isinstance(bstack1l111l1llll_opy_[bstack1ll1l11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᰪ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᰫ") + str(error))
  return False
def bstack1111ll1l1l1_opy_(config, bstack1111l1ll111_opy_, bstack1111ll1l11l_opy_, bstack1111lll111l_opy_):
  bstack1111lllll11_opy_ = bstack1111ll11lll_opy_(config)
  bstack1111ll1ll1l_opy_ = bstack1111l1ll1l1_opy_(config)
  if bstack1111lllll11_opy_ is None or bstack1111ll1ll1l_opy_ is None:
    logger.error(bstack1ll1l11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᰬ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᰭ"), bstack1ll1l11_opy_ (u"ࠫࢀࢃࠧᰮ")))
    data = {
        bstack1ll1l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᰯ"): config[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᰰ")],
        bstack1ll1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᰱ"): config.get(bstack1ll1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᰲ"), os.path.basename(os.getcwd())),
        bstack1ll1l11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬᰳ"): bstack111ll1ll1l_opy_(),
        bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᰴ"): config.get(bstack1ll1l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᰵ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᰶ")),
        bstack1ll1l11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ᰷࠭"): {
            bstack1ll1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ᰸"): bstack1111l1ll111_opy_,
            bstack1ll1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ᰹"): bstack1111ll1l11l_opy_,
            bstack1ll1l11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᰺"): __version__,
            bstack1ll1l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ᰻"): bstack1ll1l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᰼"),
            bstack1ll1l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ᰽"): bstack1ll1l11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᰾"),
            bstack1ll1l11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᰿"): bstack1111lll111l_opy_
        },
        bstack1ll1l11_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ᱀"): settings,
        bstack1ll1l11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪ᱁"): bstack1111l1lll11_opy_(),
        bstack1ll1l11_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪ᱂"): bstack1111l1111l_opy_(),
        bstack1ll1l11_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭᱃"): get_host_info(),
        bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᱄"): bstack111l1lll1l_opy_(config)
    }
    headers = {
        bstack1ll1l11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ᱅"): bstack1ll1l11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ᱆"),
    }
    config = {
        bstack1ll1l11_opy_ (u"ࠨࡣࡸࡸ࡭࠭᱇"): (bstack1111lllll11_opy_, bstack1111ll1ll1l_opy_),
        bstack1ll1l11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᱈"): headers
    }
    response = bstack11llll11ll_opy_(bstack1ll1l11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ᱉"), bstack1111l1l1lll_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫ᱊"), data, config)
    bstack1111ll11ll1_opy_ = response.json()
    if bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭᱋")]:
      parsed = json.loads(os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ᱌"), bstack1ll1l11_opy_ (u"ࠧࡼࡿࠪᱍ")))
      parsed[bstack1ll1l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᱎ")] = bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡧࡥࡹࡧࠧᱏ")][bstack1ll1l11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᱐")]
      os.environ[bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᱑")] = json.dumps(parsed)
      accessibility_scripts.bstack11l1lll11_opy_(bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠬࡪࡡࡵࡣࠪ᱒")][bstack1ll1l11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ᱓")])
      accessibility_scripts.bstack1l1l1ll11ll_opy_(bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠧࡥࡣࡷࡥࠬ᱔")][bstack1ll1l11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᱕")])
      accessibility_scripts.store()
      return bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠩࡧࡥࡹࡧࠧ᱖")][bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ᱗")], bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠫࡩࡧࡴࡢࠩ᱘")][bstack1ll1l11_opy_ (u"ࠬ࡯ࡤࠨ᱙")]
    else:
      logger.error(bstack1ll1l11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧᱚ") + bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᱛ")])
      if bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᱜ")] == bstack1ll1l11_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫᱝ"):
        for bstack1111ll1l111_opy_ in bstack1111ll11ll1_opy_[bstack1ll1l11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪᱞ")]:
          logger.error(bstack1111ll1l111_opy_[bstack1ll1l11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᱟ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨᱠ") +  str(error))
    return None, None
def bstack1111ll111ll_opy_():
  if os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᱡ")) is None:
    return {
        bstack1ll1l11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᱢ"): bstack1ll1l11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᱣ"),
        bstack1ll1l11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᱤ"): bstack1ll1l11_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩᱥ")
    }
  data = {bstack1ll1l11_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬᱦ"): bstack111ll1ll1l_opy_()}
  headers = {
      bstack1ll1l11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬᱧ"): bstack1ll1l11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧᱨ") + os.getenv(bstack1ll1l11_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧᱩ")),
      bstack1ll1l11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᱪ"): bstack1ll1l11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᱫ")
  }
  response = bstack11llll11ll_opy_(bstack1ll1l11_opy_ (u"ࠪࡔ࡚࡚ࠧᱬ"), bstack1111l1l1lll_opy_ + bstack1ll1l11_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭ᱭ"), data, { bstack1ll1l11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᱮ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1l11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢᱯ") + bstack1lll1l11ll1_opy_().isoformat() + bstack1ll1l11_opy_ (u"࡛ࠧࠩᱰ"))
      return {bstack1ll1l11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᱱ"): bstack1ll1l11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᱲ"), bstack1ll1l11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᱳ"): bstack1ll1l11_opy_ (u"ࠫࠬᱴ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣᱵ") + str(error))
    return {
        bstack1ll1l11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᱶ"): bstack1ll1l11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᱷ"),
        bstack1ll1l11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᱸ"): str(error)
    }
def bstack1111ll1llll_opy_(bstack1111l1lll1l_opy_):
    return re.match(bstack1ll1l11_opy_ (u"ࡴࠪࡢࡡࡪࠫࠩ࡞࠱ࡠࡩ࠱ࠩࡀࠦࠪᱹ"), bstack1111l1lll1l_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1111lll1lll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1111lll1lll_opy_ = desired_capabilities
        else:
          bstack1111lll1lll_opy_ = {}
        bstack1l11111ll1l_opy_ = (bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᱺ"), bstack1ll1l11_opy_ (u"ࠫࠬᱻ")).lower() or caps.get(bstack1ll1l11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᱼ"), bstack1ll1l11_opy_ (u"࠭ࠧᱽ")).lower())
        if bstack1l11111ll1l_opy_ == bstack1ll1l11_opy_ (u"ࠧࡪࡱࡶࠫ᱾"):
            return True
        if bstack1l11111ll1l_opy_ == bstack1ll1l11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩ᱿"):
            bstack1111l1lll1l_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠫᲀ")) or bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲁ"), {}).get(bstack1ll1l11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᲂ"), bstack1ll1l11_opy_ (u"ࠬ࠭ᲃ"))
            if bstack1111l1lll1l_opy_:
                try:
                    bstack1111llllll1_opy_ = int(str(bstack1111l1lll1l_opy_).split(bstack1ll1l11_opy_ (u"࠭࠮ࠨᲄ"))[0])
                    min_version = int(float(bstack1111ll11l1l_opy_))
                    if bstack1111llllll1_opy_ < min_version:
                        logger.warning(bstack1111lll11ll_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack1ll1l11_opy_ (u"ࠢࡖࡰࡤࡦࡱ࡫ࠠࡵࡱࠣࡴࡦࡸࡳࡦࠢࡳࡰࡦࡺࡦࡰࡴࡰࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࠭ࠥࡴࠩࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡱࡱ࠲ࠧᲅ"), bstack1111l1lll1l_opy_)
            return True
        bstack1l1111lll11_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲆ"), {}).get(bstack1ll1l11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪ࠭ᲇ"), caps.get(bstack1ll1l11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪᲈ"), bstack1ll1l11_opy_ (u"ࠫࠬᲉ")))
        if bstack1l1111lll11_opy_:
            logger.warning(bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᲊ"))
            return False
        browser = (caps.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᲋"), bstack1ll1l11_opy_ (u"ࠧࠨ᲌")) or caps.get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᲍"), bstack1ll1l11_opy_ (u"ࠩࠪ᲎"))).lower() or \
                  (bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᲏"), bstack1ll1l11_opy_ (u"ࠫࠬᲐ")) or bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭Ბ"), bstack1ll1l11_opy_ (u"࠭ࠧᲒ"))).lower()
        if browser not in (bstack1ll1l11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᲓ"), bstack1ll1l11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠪᲔ"), bstack1ll1l11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨᲕ")):
            logger.warning(bstack1ll1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᲖ"))
            return False
        browser_version = caps.get(bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲗ")) or caps.get(bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᲘ")) or bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᲙ")) or bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᲚ"), {}).get(bstack1ll1l11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲛ")) or bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲜ"), {}).get(bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᲝ"))
        bstack1l1111l1ll1_opy_ = bstack1111lll1ll1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack1111lllllll_opy_ = False
        if config is not None:
          bstack1111lllllll_opy_ = bstack1ll1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᲞ") in config and str(config[bstack1ll1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᲟ")]).lower() != bstack1ll1l11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᲠ")
        if os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᲡ"), bstack1ll1l11_opy_ (u"ࠨࠩᲢ")).lower() == bstack1ll1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᲣ") or bstack1111lllllll_opy_:
          bstack1l1111l1ll1_opy_ = bstack1111lll1ll1_opy_.bstack11llllllll1_opy_
        if browser_version and browser_version != bstack1ll1l11_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪᲤ") and int(browser_version.split(bstack1ll1l11_opy_ (u"ࠫ࠳࠭Ქ"))[0]) <= bstack1l1111l1ll1_opy_:
          logger.warning(bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࠢᲦ") + str(bstack1l1111l1ll1_opy_) + bstack1ll1l11_opy_ (u"ࠨ࠮ࠣᲧ"))
          return False
        bstack11lllll1ll1_opy_ = (caps.get(bstack1ll1l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᲨ"))
                         or bstack1111lll1lll_opy_.get(bstack1ll1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ჩ"), {})
                         or caps.get(bstack1ll1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲪ"), {}))
        bstack1ll1ll1111l_opy_ = bstack11lllll1ll1_opy_.get(bstack1ll1l11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᲫ"), []) if isinstance(bstack11lllll1ll1_opy_, dict) else []
        if not isinstance(bstack1ll1ll1111l_opy_, list):
            bstack1ll1ll1111l_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack1ll1l11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᲬ") or arg == bstack1ll1l11_opy_ (u"ࠬ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᲭ") or (arg.startswith(bstack1ll1l11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࠫᲮ")) and arg != bstack1ll1l11_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨᲯ")))
               for arg in bstack1ll1ll1111l_opy_):
            logger.warning(bstack1ll1l11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᲰ"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack1ll1l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᲱ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l11llll1l1_opy_ = config.get(bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᲲ"), {})
    bstack1l11llll1l1_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᲳ")] = os.getenv(bstack1ll1l11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᲴ"))
    bstack1l1l111l1_opy_ = json.loads(os.getenv(bstack1ll1l11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᲵ"), bstack1ll1l11_opy_ (u"ࠧࡼࡿࠪᲶ"))).get(bstack1ll1l11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲷ"))
    if not config[bstack1ll1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᲸ")].get(bstack1ll1l11_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᲹ")):
      if bstack1ll1l11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᲺ") in caps:
        caps[bstack1ll1l11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᲻")][bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᲼")] = bstack1l11llll1l1_opy_
        caps[bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᲽ")][bstack1ll1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᲾ")][bstack1ll1l11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᲿ")] = bstack1l1l111l1_opy_
      else:
        caps[bstack1ll1l11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳀")] = bstack1l11llll1l1_opy_
        caps[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳁")][bstack1ll1l11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᳂")] = bstack1l1l111l1_opy_
  except Exception as error:
    logger.debug(bstack1ll1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢ᳃") +  str(error))
def start_test_capture(driver, bstack1111lllll1l_opy_):
  try:
    setattr(driver, bstack1ll1l11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ᳄"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack1ll1l11_opy_ (u"ࠨࡈࡕࡅࡒࡋࡗࡐࡔࡎࡣ࡚࡙ࡅࡅࠩ᳅")) == bstack1ll1l11_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯࠯ࡪࡩࡳ࡫ࡲࡪࡥࠪ᳆")):
        bstack1111ll11111_opy_ = bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᳇"), None)
        if bstack1111ll11111_opy_:
          if bstack1111lllll1l_opy_:
            logger.info(bstack1ll1l11_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡲࡳࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱࠲࠳ࠨ᳈"))
          return bstack1111lllll1l_opy_
      bstack1111llll111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111llll111_opy_ = False
      bstack1111llll111_opy_ = url.scheme in [bstack1ll1l11_opy_ (u"ࠧ࡮ࡴࡵࡲࠥ᳉"), bstack1ll1l11_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ᳊")]
      if bstack1111llll111_opy_:
        if bstack1111lllll1l_opy_:
          logger.info(bstack1ll1l11_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢ᳋"))
      return bstack1111lllll1l_opy_
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ᳌") + str(e))
    return False
def bstack11l1l11l11_opy_(driver, name, path):
  try:
    bstack1l111111l11_opy_ = {
        bstack1ll1l11_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩ᳍"): threading.current_thread().current_test_uuid,
        bstack1ll1l11_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ᳎"): os.environ.get(bstack1ll1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ᳏"), bstack1ll1l11_opy_ (u"ࠬ࠭᳐")),
        bstack1ll1l11_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪ᳑"): os.environ.get(bstack1ll1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ᳒"), bstack1ll1l11_opy_ (u"ࠨࠩ᳓"))
    }
    bstack1l111ll1ll_opy_ = bstack1111llll1l_opy_.bstack1l11llll1_opy_(EVENTS.bstack1ll1l1l1ll_opy_.value)
    logger.debug(bstack1ll1l11_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷ᳔ࠬ"))
    try:
      if (bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶ᳕ࠪ"), None) and bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ᳖࠭"), None)):
        scripts = {bstack1ll1l11_opy_ (u"ࠬࡹࡣࡢࡰ᳗ࠪ"): accessibility_scripts.perform_scan}
        bstack1111l1ll11l_opy_ = json.loads(scripts[bstack1ll1l11_opy_ (u"ࠨࡳࡤࡣࡱ᳘ࠦ")].replace(bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻᳙ࠢࠥ"), bstack1ll1l11_opy_ (u"ࠣࠤ᳚")))
        bstack1111l1ll11l_opy_[bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ᳛")][bstack1ll1l11_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦ᳜ࠪ")] = None
        scripts[bstack1ll1l11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ᳝")] = bstack1ll1l11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀ᳞ࠠࠣ") + json.dumps(bstack1111l1ll11l_opy_)
        accessibility_scripts.bstack11l1lll11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll1l11_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ᳟"): name}))
      bstack1111llll1l_opy_.end(EVENTS.bstack1ll1l1l1ll_opy_.value, bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᳠"), bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᳡"), True, None)
    except Exception as error:
      bstack1111llll1l_opy_.end(EVENTS.bstack1ll1l1l1ll_opy_.value, bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᳢"), bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠾ࡪࡴࡤ᳣ࠣ"), False, str(error))
    bstack1l111ll1ll_opy_ = bstack1111llll1l_opy_.bstack1111llll1ll_opy_(EVENTS.bstack1l111l11l1l_opy_.value)
    bstack1111llll1l_opy_.mark(bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ᳤ࠦ"))
    try:
      if (bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸ᳥ࠬ"), None) and bstack11l11l1ll_opy_(threading.current_thread(), bstack1ll1l11_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᳦"), None)):
        scripts = {bstack1ll1l11_opy_ (u"ࠧࡴࡥࡤࡲ᳧ࠬ"): accessibility_scripts.perform_scan}
        bstack1111l1ll11l_opy_ = json.loads(scripts[bstack1ll1l11_opy_ (u"ࠣࡵࡦࡥࡳࠨ᳨")].replace(bstack1ll1l11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᳩ"), bstack1ll1l11_opy_ (u"ࠥࠦᳪ")))
        bstack1111l1ll11l_opy_[bstack1ll1l11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᳫ")][bstack1ll1l11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᳬ")] = None
        scripts[bstack1ll1l11_opy_ (u"ࠨࡳࡤࡣࡱ᳭ࠦ")] = bstack1ll1l11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᳮ") + json.dumps(bstack1111l1ll11l_opy_)
        accessibility_scripts.bstack11l1lll11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l111111l11_opy_))
      bstack1111llll1l_opy_.end(bstack1l111ll1ll_opy_, bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᳯ"), bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᳰ"),True, None)
    except Exception as error:
      bstack1111llll1l_opy_.end(bstack1l111ll1ll_opy_, bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᳱ"), bstack1l111ll1ll_opy_ + bstack1ll1l11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᳲ"),False, str(error))
    logger.info(bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᳳ"))
    try:
      bstack1l111111l1l_opy_ = {
        bstack1ll1l11_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ᳴"): {
          bstack1ll1l11_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣᳵ"): bstack1ll1l11_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧᳶ"),
        },
        bstack1ll1l11_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ᳷"): {
          bstack1ll1l11_opy_ (u"ࠥࡦࡴࡪࡹࠣ᳸"): {
            bstack1ll1l11_opy_ (u"ࠦࡲࡹࡧࠣ᳹"): bstack1ll1l11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᳺ"),
            bstack1ll1l11_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ᳻"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l111111l1l_opy_, separators=(bstack1ll1l11_opy_ (u"ࠧ࠭ࠩ᳼"), bstack1ll1l11_opy_ (u"ࠨ࠼ࠪ᳽"))))
    except Exception as bstack11lll1llll_opy_:
      logger.debug(bstack1ll1l11_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣ᳾") + str(bstack11lll1llll_opy_) + bstack1ll1l11_opy_ (u"ࠥࠦ᳿"))
  except Exception as bstack11lllll1lll_opy_:
    logger.error(bstack1ll1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᴀ") + str(path) + bstack1ll1l11_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᴁ") + str(bstack11lllll1lll_opy_))
def bstack1111ll11l11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll1l11_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᴂ")) and str(caps.get(bstack1ll1l11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᴃ"))).lower() == bstack1ll1l11_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᴄ"):
        bstack1l111l1l111_opy_ = caps.get(bstack1ll1l11_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᴅ")) or caps.get(bstack1ll1l11_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᴆ"))
        if bstack1l111l1l111_opy_:
            try:
              bstack1111l1lll1l_opy_ = str(bstack1l111l1l111_opy_).split(bstack1ll1l11_opy_ (u"ࠫ࠳࠭ᴇ"))[0]
              min_version = int(float(bstack1111ll11l1l_opy_))
              if int(bstack1111l1lll1l_opy_) < min_version:
                  logger.warning(bstack1111lll11ll_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack1ll1l11_opy_ (u"࡛ࠧ࡮ࡢࡤ࡯ࡩࠥࡺ࡯ࠡࡲࡤࡶࡸ࡫ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡡࡹࡩࡷࡹࡩࡰࡰࠣࠫࠪࡹࠧࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡯࡯࠰ࠥᴈ"), bstack1l111l1l111_opy_)
    return True
def bstack1l111l111_opy_(config):
  if bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴉ") in config:
        return config[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴊ")]
  for platform in config.get(bstack1ll1l11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᴋ"), []):
      if bstack1ll1l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴌ") in platform:
          return platform[bstack1ll1l11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴍ")]
  return None
def bstack1lll1l11_opy_(bstack11l1llll_opy_):
  try:
    browser_name = bstack11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᴎ")]
    browser_version = bstack11l1llll_opy_[bstack1ll1l11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᴏ")]
    chrome_options = bstack11l1llll_opy_[bstack1ll1l11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧᴐ")]
    try:
        bstack1111lll11l1_opy_ = int(browser_version.split(bstack1ll1l11_opy_ (u"ࠧ࠯ࠩᴑ"))[0])
    except ValueError as e:
        logger.error(bstack1ll1l11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡣࡰࡰࡹࡩࡷࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠧᴒ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1ll1l11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᴓ")):
        logger.warning(bstack1ll1l11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᴔ"))
        return False
    if bstack1111lll11l1_opy_ < bstack1111lll1ll1_opy_.bstack11llllllll1_opy_:
        logger.warning(bstack1ll1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡯ࡲࡦࡵࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡺࡪࡸࡳࡪࡱࡱࠤࠧᴕ") + str(bstack1111lll1ll1_opy_.bstack11llllllll1_opy_) + bstack1ll1l11_opy_ (u"ࠧࠦ࡯ࡳࠢ࡫࡭࡬࡮ࡥࡳ࠰ࠥᴖ"))
        return False
    bstack1ll1ll1111l_opy_ = chrome_options.get(bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᴗ"), []) if chrome_options else []
    if not isinstance(bstack1ll1ll1111l_opy_, list):
        bstack1ll1ll1111l_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack1ll1l11_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᴘ") or arg == bstack1ll1l11_opy_ (u"ࠨࡪࡨࡥࡩࡲࡥࡴࡵࠪᴙ") or (arg.startswith(bstack1ll1l11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧᴚ")) and arg != bstack1ll1l11_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫᴛ")))
           for arg in bstack1ll1ll1111l_opy_):
        logger.warning(bstack1ll1l11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᴜ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1ll1l11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥ࡬࡯ࡳࠢ࡯ࡳࡨࡧ࡬ࠡࡅ࡫ࡶࡴࡳࡥ࠻ࠢࠥᴝ") + str(e))
    return False
def bstack11llll1ll_opy_(bstack1111lll111_opy_, config):
    try:
      bstack11lllll1l1l_opy_ = bstack1ll1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴞ") in config and config[bstack1ll1l11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴟ")] == True
      bstack1111lllllll_opy_ = bstack1ll1l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᴠ") in config and str(config[bstack1ll1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᴡ")]).lower() != bstack1ll1l11_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᴢ")
      if not (bstack11lllll1l1l_opy_ and (not bstack111l1lll1l_opy_(config) or bstack1111lllllll_opy_)):
        return bstack1111lll111_opy_
      bstack1111lll1l11_opy_ = accessibility_scripts.bstack1111lll1111_opy_
      if bstack1111lll1l11_opy_ is None:
        logger.debug(bstack1ll1l11_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥࡧࡲࡦࠢࡑࡳࡳ࡫ࠢᴣ"))
        return bstack1111lll111_opy_
      bstack1111llll1l1_opy_ = int(str(bstack1111l1lllll_opy_()).split(bstack1ll1l11_opy_ (u"ࠬ࠴ࠧᴤ"))[0])
      logger.debug(bstack1ll1l11_opy_ (u"ࠨࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࠨᴥ") + str(bstack1111llll1l1_opy_) + bstack1ll1l11_opy_ (u"ࠢࠣᴦ"))
      if bstack1111llll1l1_opy_ == 3 and isinstance(bstack1111lll111_opy_, dict) and bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴧ") in bstack1111lll111_opy_ and bstack1111lll1l11_opy_ is not None:
        if bstack1ll1l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴨ") not in bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴩ")]:
          bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᴪ")][bstack1ll1l11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᴫ")] = {}
        if bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᴬ") in bstack1111lll1l11_opy_:
          if bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬᴭ") not in bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴮ")][bstack1ll1l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴯ")]:
            bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴰ")][bstack1ll1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴱ")][bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪᴲ")] = []
          for arg in bstack1111lll1l11_opy_[bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᴳ")]:
            if arg not in bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᴴ")][bstack1ll1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴵ")][bstack1ll1l11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᴶ")]:
              bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴷ")][bstack1ll1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴸ")][bstack1ll1l11_opy_ (u"ࠬࡧࡲࡨࡵࠪᴹ")].append(arg)
        if bstack1ll1l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᴺ") in bstack1111lll1l11_opy_:
          if bstack1ll1l11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᴻ") not in bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴼ")][bstack1ll1l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴽ")]:
            bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᴾ")][bstack1ll1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᴿ")][bstack1ll1l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᵀ")] = []
          for ext in bstack1111lll1l11_opy_[bstack1ll1l11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵁ")]:
            if ext not in bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵂ")][bstack1ll1l11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵃ")][bstack1ll1l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵄ")]:
              bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵅ")][bstack1ll1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵆ")][bstack1ll1l11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᵇ")].append(ext)
        if bstack1ll1l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵈ") in bstack1111lll1l11_opy_:
          if bstack1ll1l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵉ") not in bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᵊ")][bstack1ll1l11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᵋ")]:
            bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵌ")][bstack1ll1l11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵍ")][bstack1ll1l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵎ")] = {}
          bstack1111ll1l1ll_opy_(bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵏ")][bstack1ll1l11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵐ")][bstack1ll1l11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵑ")],
                    bstack1111lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵒ")])
        os.environ[bstack1ll1l11_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᵓ")] = bstack1ll1l11_opy_ (u"ࠫࡹࡸࡵࡦࠩᵔ")
        return bstack1111lll111_opy_
      else:
        chrome_options = None
        if isinstance(bstack1111lll111_opy_, ChromeOptions):
          chrome_options = bstack1111lll111_opy_
        elif isinstance(bstack1111lll111_opy_, dict):
          for value in bstack1111lll111_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1111lll111_opy_, dict):
            bstack1111lll111_opy_[bstack1ll1l11_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭ᵕ")] = chrome_options
          else:
            bstack1111lll111_opy_ = chrome_options
        if bstack1111lll1l11_opy_ is not None:
          if bstack1ll1l11_opy_ (u"࠭ࡡࡳࡩࡶࠫᵖ") in bstack1111lll1l11_opy_:
                bstack1111lll1l1l_opy_ = chrome_options.arguments or []
                new_args = bstack1111lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠧࡢࡴࡪࡷࠬᵗ")]
                for arg in new_args:
                    if arg not in bstack1111lll1l1l_opy_:
                        chrome_options.add_argument(arg)
          if bstack1ll1l11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᵘ") in bstack1111lll1l11_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1ll1l11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵙ"), [])
                bstack1111l1llll1_opy_ = bstack1111lll1l11_opy_[bstack1ll1l11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵚ")]
                for extension in bstack1111l1llll1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1ll1l11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᵛ") in bstack1111lll1l11_opy_:
                bstack1111ll1ll11_opy_ = chrome_options.experimental_options.get(bstack1ll1l11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵜ"), {})
                bstack1111ll1111l_opy_ = bstack1111lll1l11_opy_[bstack1ll1l11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵝ")]
                bstack1111ll1l1ll_opy_(bstack1111ll1ll11_opy_, bstack1111ll1111l_opy_)
                chrome_options.add_experimental_option(bstack1ll1l11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵞ"), bstack1111ll1ll11_opy_)
        os.environ[bstack1ll1l11_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᵟ")] = bstack1ll1l11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᵠ")
        return bstack1111lll111_opy_
    except Exception as e:
      logger.error(bstack1ll1l11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡧࡨ࡮ࡴࡧࠡࡰࡲࡲ࠲ࡈࡓࠡ࡫ࡱࡪࡷࡧࠠࡢ࠳࠴ࡽࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠣᵡ") + str(e))
      return bstack1111lll111_opy_