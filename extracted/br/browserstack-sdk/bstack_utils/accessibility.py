# coding: UTF-8
import sys
bstack11ll_opy_ = sys.version_info [0] == 2
bstack11lllll_opy_ = 2048
bstack1llll_opy_ = 7
def bstack11ll11_opy_ (bstack111l1l_opy_):
    global bstack11111ll_opy_
    bstack1llll11_opy_ = ord (bstack111l1l_opy_ [-1])
    bstack1111l11_opy_ = bstack111l1l_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1111l11_opy_)
    bstack11111l_opy_ = bstack1111l11_opy_ [:bstack111l1ll_opy_] + bstack1111l11_opy_ [bstack111l1ll_opy_:]
    if bstack11ll_opy_:
        bstack1l11lll_opy_ = unicode () .join ([unichr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    else:
        bstack1l11lll_opy_ = str () .join ([chr (ord (char) - bstack11lllll_opy_ - (bstack1l11ll_opy_ + bstack1llll11_opy_) % bstack1llll_opy_) for bstack1l11ll_opy_, char in enumerate (bstack11111l_opy_)])
    return eval (bstack1l11lll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111ll111l1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111ll1ll11_opy_ as bstack1111llll1ll_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack1l1l111l1l_opy_, bstack1lll1ll1l11_opy_, bstack1llll1l1l_opy_, bstack1111ll11ll1_opy_, \
  bstack1111llllll1_opy_, bstack1ll1l1l11l_opy_, get_host_info, bstack1111l1lllll_opy_, bstack1l11lll11l_opy_, error_handler, bstack1111l1llll1_opy_, bstack1111lll1lll_opy_, bstack11ll1l11l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1l11l1l11_opy_ import bstack1ll111lll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1l11l1l11_opy_ = bstack1ll111lll_opy_()
@error_handler(class_method=False)
def _1111l1ll1l1_opy_(driver, bstack1ll11l11l11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll11_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧᰍ"): caps.get(bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᰎ"), None),
        bstack11ll11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᰏ"): bstack1ll11l11l11_opy_.get(bstack11ll11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᰐ"), None),
        bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᰑ"): caps.get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᰒ"), None),
        bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᰓ"): caps.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᰔ"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᰕ") + str(error))
  return response
def on():
    if os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᰖ"), None) is None or os.environ[bstack11ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᰗ")] == bstack11ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᰘ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᰙ"), False) or any([p.get(bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᰚ"), False) == True for p in config.get(bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᰛ"), [])])
def is_enabled_platform(config, bstack1l11l11ll_opy_):
  try:
    bstack1ll1lll11l1_opy_ = config.get(bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᰜ"), False)
    _1lll111111l_opy_ = int(bstack1l11l11ll_opy_)
    if _1lll111111l_opy_ < 0:
      _1lll111111l_opy_ = 0
    bstack1l1ll1111_opy_ = config.get(bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᰝ"), [])
    if _1lll111111l_opy_ < len(bstack1l1ll1111_opy_) and bstack1l1ll1111_opy_[_1lll111111l_opy_]:
      bstack1111ll1l11l_opy_ = bstack1l1ll1111_opy_[_1lll111111l_opy_].get(bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᰞ"), None)
    else:
      bstack1111ll1l11l_opy_ = config.get(bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᰟ"), None)
    if bstack1111ll1l11l_opy_ != None:
      bstack1ll1lll11l1_opy_ = bstack1111ll1l11l_opy_
    bstack1111ll1lll1_opy_ = os.getenv(bstack11ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᰠ")) is not None and len(os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᰡ"))) > 0 and os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᰢ")) != bstack11ll11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᰣ")
    return bstack1ll1lll11l1_opy_ and bstack1111ll1lll1_opy_
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᰤ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l1111lll1l_opy_ = os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᰥ"))
  if bstack1l1111lll1l_opy_ is None:
    return True
  bstack1l1111lll1l_opy_ = json.loads(bstack1l1111lll1l_opy_)
  try:
    include_tags = bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᰦ")] if bstack11ll11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᰧ") in bstack1l1111lll1l_opy_ and isinstance(bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᰨ")], list) else []
    exclude_tags = bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᰩ")] if bstack11ll11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᰪ") in bstack1l1111lll1l_opy_ and isinstance(bstack1l1111lll1l_opy_[bstack11ll11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᰫ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᰬ") + str(error))
  return False
def bstack1111l1lll1l_opy_(config, bstack1111lll1ll1_opy_, bstack1111l1l1lll_opy_, bstack1111lll1l11_opy_):
  bstack1111llll11l_opy_ = bstack1111ll11ll1_opy_(config)
  bstack1111l1lll11_opy_ = bstack1111llllll1_opy_(config)
  if bstack1111llll11l_opy_ is None or bstack1111l1lll11_opy_ is None:
    logger.error(bstack11ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᰭ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᰮ"), bstack11ll11_opy_ (u"ࠬࢁࡽࠨᰯ")))
    data = {
        bstack11ll11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᰰ"): config[bstack11ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᰱ")],
        bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᰲ"): config.get(bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᰳ"), os.path.basename(os.getcwd())),
        bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᰴ"): bstack1l1l111l1l_opy_(),
        bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᰵ"): config.get(bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᰶ"), bstack11ll11_opy_ (u"᰷࠭ࠧ")),
        bstack11ll11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ᰸"): {
            bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ᰹"): bstack1111lll1ll1_opy_,
            bstack11ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ᰺"): bstack1111l1l1lll_opy_,
            bstack11ll11_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᰻"): __version__,
            bstack11ll11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭᰼"): bstack11ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᰽"),
            bstack11ll11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭᰾"): bstack11ll11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩ᰿"),
            bstack11ll11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᱀"): bstack1111lll1l11_opy_
        },
        bstack11ll11_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ᱁"): settings,
        bstack11ll11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫ᱂"): bstack1111l1lllll_opy_(),
        bstack11ll11_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫ᱃"): bstack1ll1l1l11l_opy_(),
        bstack11ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧ᱄"): get_host_info(),
        bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ᱅"): bstack1llll1l1l_opy_(config)
    }
    headers = {
        bstack11ll11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭᱆"): bstack11ll11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫ᱇"),
    }
    config = {
        bstack11ll11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧ᱈"): (bstack1111llll11l_opy_, bstack1111l1lll11_opy_),
        bstack11ll11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ᱉"): headers
    }
    response = bstack1l11lll11l_opy_(bstack11ll11_opy_ (u"ࠫࡕࡕࡓࡕࠩ᱊"), bstack1111llll1ll_opy_ + bstack11ll11_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬ᱋"), data, config)
    bstack1111ll11111_opy_ = response.json()
    if bstack1111ll11111_opy_[bstack11ll11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ᱌")]:
      parsed = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᱍ"), bstack11ll11_opy_ (u"ࠨࡽࢀࠫᱎ")))
      parsed[bstack11ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᱏ")] = bstack1111ll11111_opy_[bstack11ll11_opy_ (u"ࠪࡨࡦࡺࡡࠨ᱐")][bstack11ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᱑")]
      os.environ[bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᱒")] = json.dumps(parsed)
      accessibility_scripts.bstack1ll1ll1l1_opy_(bstack1111ll11111_opy_[bstack11ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫ᱓")][bstack11ll11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨ᱔")])
      accessibility_scripts.bstack1l1l111l11l_opy_(bstack1111ll11111_opy_[bstack11ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭᱕")][bstack11ll11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ᱖")])
      accessibility_scripts.store()
      return bstack1111ll11111_opy_[bstack11ll11_opy_ (u"ࠪࡨࡦࡺࡡࠨ᱗")][bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩ᱘")], bstack1111ll11111_opy_[bstack11ll11_opy_ (u"ࠬࡪࡡࡵࡣࠪ᱙")][bstack11ll11_opy_ (u"࠭ࡩࡥࠩᱚ")]
    else:
      logger.error(bstack11ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᱛ") + bstack1111ll11111_opy_[bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᱜ")])
      if bstack1111ll11111_opy_[bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᱝ")] == bstack11ll11_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᱞ"):
        for bstack1111l1ll111_opy_ in bstack1111ll11111_opy_[bstack11ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᱟ")]:
          logger.error(bstack1111l1ll111_opy_[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᱠ")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᱡ") +  str(error))
    return None, None
def bstack1111ll1l111_opy_():
  if os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᱢ")) is None:
    return {
        bstack11ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᱣ"): bstack11ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᱤ"),
        bstack11ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᱥ"): bstack11ll11_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᱦ")
    }
  data = {bstack11ll11_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᱧ"): bstack1l1l111l1l_opy_()}
  headers = {
      bstack11ll11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᱨ"): bstack11ll11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᱩ") + os.getenv(bstack11ll11_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᱪ")),
      bstack11ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᱫ"): bstack11ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᱬ")
  }
  response = bstack1l11lll11l_opy_(bstack11ll11_opy_ (u"ࠫࡕ࡛ࡔࠨᱭ"), bstack1111llll1ll_opy_ + bstack11ll11_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᱮ"), data, { bstack11ll11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᱯ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᱰ") + bstack1lll1ll1l11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠨ࡜ࠪᱱ"))
      return {bstack11ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᱲ"): bstack11ll11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᱳ"), bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᱴ"): bstack11ll11_opy_ (u"ࠬ࠭ᱵ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᱶ") + str(error))
    return {
        bstack11ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᱷ"): bstack11ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᱸ"),
        bstack11ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᱹ"): str(error)
    }
def bstack1111ll111ll_opy_(bstack1111ll11l11_opy_):
    return re.match(bstack11ll11_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫᱺ"), bstack1111ll11l11_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1111lll111l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1111lll111l_opy_ = desired_capabilities
        else:
          bstack1111lll111l_opy_ = {}
        bstack1l1111l11ll_opy_ = (bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᱻ"), bstack11ll11_opy_ (u"ࠬ࠭ᱼ")).lower() or caps.get(bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᱽ"), bstack11ll11_opy_ (u"ࠧࠨ᱾")).lower())
        if bstack1l1111l11ll_opy_ == bstack11ll11_opy_ (u"ࠨ࡫ࡲࡷࠬ᱿"):
            return True
        if bstack1l1111l11ll_opy_ == bstack11ll11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᲀ"):
            bstack1111ll11l11_opy_ = caps.get(bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲁ")) or bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᲂ"), {}).get(bstack11ll11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲃ"), bstack11ll11_opy_ (u"࠭ࠧᲄ"))
            if bstack1111ll11l11_opy_:
                try:
                    bstack1111l1ll1ll_opy_ = int(str(bstack1111ll11l11_opy_).split(bstack11ll11_opy_ (u"ࠧ࠯ࠩᲅ"))[0])
                    min_version = int(float(bstack1111ll1llll_opy_))
                    if bstack1111l1ll1ll_opy_ < min_version:
                        logger.warning(bstack1111llll111_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack11ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠦࠧࠦࡵࠪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡲࡲ࠳ࠨᲆ"), bstack1111ll11l11_opy_)
            return True
        bstack11lllll1l1l_opy_ = caps.get(bstack11ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲇ"), {}).get(bstack11ll11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᲈ"), caps.get(bstack11ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᲉ"), bstack11ll11_opy_ (u"ࠬ࠭ᲊ")))
        if bstack11lllll1l1l_opy_:
            logger.warning(bstack11ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᲋"))
            return False
        browser = (caps.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᲌"), bstack11ll11_opy_ (u"ࠨࠩ᲍")) or caps.get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ᲎"), bstack11ll11_opy_ (u"ࠪࠫ᲏"))).lower() or \
                  (bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᲐ"), bstack11ll11_opy_ (u"ࠬ࠭Ბ")) or bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᲒ"), bstack11ll11_opy_ (u"ࠧࠨᲓ"))).lower()
        if browser not in (bstack11ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᲔ"), bstack11ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫᲕ"), bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩᲖ")):
            logger.warning(bstack11ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᲗ"))
            return False
        browser_version = caps.get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ი")) or caps.get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲙ")) or bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲚ")) or bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲛ"), {}).get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᲜ")) or bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲝ"), {}).get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Პ"))
        bstack1l111111l11_opy_ = bstack1111ll111l1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack1111l1ll11l_opy_ = False
        if config is not None:
          bstack1111l1ll11l_opy_ = bstack11ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᲟ") in config and str(config[bstack11ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᲠ")]).lower() != bstack11ll11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭Ს")
        if os.environ.get(bstack11ll11_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭Ტ"), bstack11ll11_opy_ (u"ࠩࠪᲣ")).lower() == bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨᲤ") or bstack1111l1ll11l_opy_:
          bstack1l111111l11_opy_ = bstack1111ll111l1_opy_.bstack1l111l11lll_opy_
        if browser_version and browser_version != bstack11ll11_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᲥ") and int(browser_version.split(bstack11ll11_opy_ (u"ࠬ࠴ࠧᲦ"))[0]) <= bstack1l111111l11_opy_:
          logger.warning(bstack11ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࠣᲧ") + str(bstack1l111111l11_opy_) + bstack11ll11_opy_ (u"ࠢ࠯ࠤᲨ"))
          return False
        bstack11lllll1ll1_opy_ = (caps.get(bstack11ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ჩ"))
                         or bstack1111lll111l_opy_.get(bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᲪ"), {})
                         or caps.get(bstack11ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᲫ"), {}))
        bstack1ll1lll11ll_opy_ = bstack11lllll1ll1_opy_.get(bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩᲬ"), []) if isinstance(bstack11lllll1ll1_opy_, dict) else []
        if not isinstance(bstack1ll1lll11ll_opy_, list):
            bstack1ll1lll11ll_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack11ll11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᲭ") or arg == bstack11ll11_opy_ (u"࠭ࡨࡦࡣࡧࡰࡪࡹࡳࠨᲮ") or (arg.startswith(bstack11ll11_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࠬᲯ")) and arg != bstack11ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࡂࡴࡥࡸࠩᲰ")))
               for arg in bstack1ll1lll11ll_opy_):
            logger.warning(bstack11ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᲱ"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack11ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᲲ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1l1llll1l_opy_ = config.get(bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᲳ"), {})
    bstack1l1l1llll1l_opy_[bstack11ll11_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᲴ")] = os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᲵ"))
    bstack11ll1l111_opy_ = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᲶ"), bstack11ll11_opy_ (u"ࠨࡽࢀࠫᲷ"))).get(bstack11ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᲸ"))
    if not config[bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᲹ")].get(bstack11ll11_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥᲺ")):
      if bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᲻") in caps:
        caps[bstack11ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᲼")][bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᲽ")] = bstack1l1l1llll1l_opy_
        caps[bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲾ")][bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲿ")][bstack11ll11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᳀")] = bstack11ll1l111_opy_
      else:
        caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳁")] = bstack1l1l1llll1l_opy_
        caps[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᳂")][bstack11ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᳃")] = bstack11ll1l111_opy_
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࠣ᳄") +  str(error))
def start_test_capture(driver, bstack1111ll1l1l1_opy_):
  try:
    setattr(driver, bstack11ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ᳅"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack11ll11_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆࠪ᳆")) == bstack11ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦࠫ᳇")):
        bstack1111l1l1ll1_opy_ = bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭᳈"), None)
        if bstack1111l1l1ll1_opy_:
          if bstack1111ll1l1l1_opy_:
            logger.info(bstack11ll11_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲࠳࠴ࠢ᳉"))
          return bstack1111ll1l1l1_opy_
      bstack1111lllll1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111lllll1l_opy_ = False
      bstack1111lllll1l_opy_ = url.scheme in [bstack11ll11_opy_ (u"ࠨࡨࡵࡶࡳࠦ᳊"), bstack11ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ᳋")]
      if bstack1111lllll1l_opy_:
        if bstack1111ll1l1l1_opy_:
          logger.info(bstack11ll11_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣ᳌"))
      return bstack1111ll1l1l1_opy_
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ᳍") + str(e))
    return False
def bstack1111l1l111_opy_(driver, name, path):
  try:
    bstack11lllllllll_opy_ = {
        bstack11ll11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪ᳎"): threading.current_thread().current_test_uuid,
        bstack11ll11_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩ᳏"): os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪ᳐"), bstack11ll11_opy_ (u"࠭ࠧ᳑")),
        bstack11ll11_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫ᳒"): os.environ.get(bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬ᳓"), bstack11ll11_opy_ (u"᳔ࠩࠪ"))
    }
    bstack1111l1ll1l_opy_ = bstack1l11l1l11_opy_.bstack1ll11l11_opy_(EVENTS.bstack1lll1l1ll1_opy_.value)
    logger.debug(bstack11ll11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ᳕࠭"))
    try:
      if (bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷ᳖ࠫ"), None) and bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳ᳗ࠧ"), None)):
        scripts = {bstack11ll11_opy_ (u"࠭ࡳࡤࡣࡱ᳘ࠫ"): accessibility_scripts.perform_scan}
        bstack1111ll1111l_opy_ = json.loads(scripts[bstack11ll11_opy_ (u"ࠢࡴࡥࡤࡲ᳙ࠧ")].replace(bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᳚"), bstack11ll11_opy_ (u"ࠤࠥ᳛")))
        bstack1111ll1111l_opy_[bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ᳜࠭")][bstack11ll11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧ᳝ࠫ")] = None
        scripts[bstack11ll11_opy_ (u"ࠧࡹࡣࡢࡰ᳞ࠥ")] = bstack11ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᳟") + json.dumps(bstack1111ll1111l_opy_)
        accessibility_scripts.bstack1ll1ll1l1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack11ll11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ᳠"): name}))
      bstack1l11l1l11_opy_.end(EVENTS.bstack1lll1l1ll1_opy_.value, bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᳡"), bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠤ࠽ࡩࡳࡪ᳢ࠢ"), True, None)
    except Exception as error:
      bstack1l11l1l11_opy_.end(EVENTS.bstack1lll1l1ll1_opy_.value, bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶ᳣ࠥ"), bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᳤"), False, str(error))
    bstack1111l1ll1l_opy_ = bstack1l11l1l11_opy_.bstack1111ll11l1l_opy_(EVENTS.bstack1l111l1ll11_opy_.value)
    bstack1l11l1l11_opy_.mark(bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸ᳥ࠧ"))
    try:
      if (bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ᳦࠭"), None) and bstack11ll1l11l_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮᳧ࠩ"), None)):
        scripts = {bstack11ll11_opy_ (u"ࠨࡵࡦࡥࡳ᳨࠭"): accessibility_scripts.perform_scan}
        bstack1111ll1111l_opy_ = json.loads(scripts[bstack11ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢᳩ")].replace(bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᳪ"), bstack11ll11_opy_ (u"ࠦࠧᳫ")))
        bstack1111ll1111l_opy_[bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᳬ")][bstack11ll11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ᳭࠭")] = None
        scripts[bstack11ll11_opy_ (u"ࠢࡴࡥࡤࡲࠧᳮ")] = bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᳯ") + json.dumps(bstack1111ll1111l_opy_)
        accessibility_scripts.bstack1ll1ll1l1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack11lllllllll_opy_))
      bstack1l11l1l11_opy_.end(bstack1111l1ll1l_opy_, bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᳰ"), bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᳱ"),True, None)
    except Exception as error:
      bstack1l11l1l11_opy_.end(bstack1111l1ll1l_opy_, bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᳲ"), bstack1111l1ll1l_opy_ + bstack11ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᳳ"),False, str(error))
    logger.info(bstack11ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤ᳴"))
    try:
      bstack1l111l1111l_opy_ = {
        bstack11ll11_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᳵ"): {
          bstack11ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᳶ"): bstack11ll11_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨ᳷"),
        },
        bstack11ll11_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧ᳸"): {
          bstack11ll11_opy_ (u"ࠦࡧࡵࡤࡺࠤ᳹"): {
            bstack11ll11_opy_ (u"ࠧࡳࡳࡨࠤᳺ"): bstack11ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤ᳻"),
            bstack11ll11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣ᳼"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l111l1111l_opy_, separators=(bstack11ll11_opy_ (u"ࠨ࠮ࠪ᳽"), bstack11ll11_opy_ (u"ࠩ࠽ࠫ᳾"))))
    except Exception as bstack1ll1l1l1ll_opy_:
      logger.debug(bstack11ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤ᳿") + str(bstack1ll1l1l1ll_opy_) + bstack11ll11_opy_ (u"ࠦࠧᴀ"))
  except Exception as bstack11llllll11l_opy_:
    logger.error(bstack11ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᴁ") + str(path) + bstack11ll11_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᴂ") + str(bstack11llllll11l_opy_))
def bstack1111ll1ll1l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᴃ")) and str(caps.get(bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᴄ"))).lower() == bstack11ll11_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᴅ"):
        bstack1l11111l11l_opy_ = caps.get(bstack11ll11_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᴆ")) or caps.get(bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᴇ"))
        if bstack1l11111l11l_opy_:
            try:
              bstack1111ll11l11_opy_ = str(bstack1l11111l11l_opy_).split(bstack11ll11_opy_ (u"ࠬ࠴ࠧᴈ"))[0]
              min_version = int(float(bstack1111ll1llll_opy_))
              if int(bstack1111ll11l11_opy_) < min_version:
                  logger.warning(bstack1111llll111_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack11ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠤࠬࠫࡳࠨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡶࡢ࡮࡬ࡨࡦࡺࡩࡰࡰ࠱ࠦᴉ"), bstack1l11111l11l_opy_)
    return True
def bstack1llll1llll_opy_(config):
  if bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴊ") in config:
        return config[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴋ")]
  for platform in config.get(bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᴌ"), []):
      if bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴍ") in platform:
          return platform[bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴎ")]
  return None
def bstack1l1ll1l1ll_opy_(bstack1l1l1l11_opy_):
  try:
    browser_name = bstack1l1l1l11_opy_[bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᴏ")]
    browser_version = bstack1l1l1l11_opy_[bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᴐ")]
    chrome_options = bstack1l1l1l11_opy_[bstack11ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᴑ")]
    try:
        bstack1111llll1l1_opy_ = int(browser_version.split(bstack11ll11_opy_ (u"ࠨ࠰ࠪᴒ"))[0])
    except ValueError as e:
        logger.error(bstack11ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨᴓ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᴔ")):
        logger.warning(bstack11ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᴕ"))
        return False
    if bstack1111llll1l1_opy_ < bstack1111ll111l1_opy_.bstack1l111l11lll_opy_:
        logger.warning(bstack11ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࠨᴖ") + str(bstack1111ll111l1_opy_.bstack1l111l11lll_opy_) + bstack11ll11_opy_ (u"ࠨࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠦᴗ"))
        return False
    bstack1ll1lll11ll_opy_ = chrome_options.get(bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᴘ"), []) if chrome_options else []
    if not isinstance(bstack1ll1lll11ll_opy_, list):
        bstack1ll1lll11ll_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack11ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᴙ") or arg == bstack11ll11_opy_ (u"ࠩ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᴚ") or (arg.startswith(bstack11ll11_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽ࠨᴛ")) and arg != bstack11ll11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࡰࡨࡻࠬᴜ")))
           for arg in bstack1ll1lll11ll_opy_):
        logger.warning(bstack11ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᴝ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡵࡱࡲࡲࡶࡹࠦࡦࡰࡴࠣࡰࡴࡩࡡ࡭ࠢࡆ࡬ࡷࡵ࡭ࡦ࠼ࠣࠦᴞ") + str(e))
    return False
def bstack11ll11l1_opy_(bstack1l111ll11_opy_, config):
    try:
      bstack1l1111l1l11_opy_ = bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴟ") in config and config[bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴠ")] == True
      bstack1111l1ll11l_opy_ = bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᴡ") in config and str(config[bstack11ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᴢ")]).lower() != bstack11ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᴣ")
      if not (bstack1l1111l1l11_opy_ and (not bstack1llll1l1l_opy_(config) or bstack1111l1ll11l_opy_)):
        return bstack1l111ll11_opy_
      bstack1111ll11lll_opy_ = accessibility_scripts.bstack1111lll11ll_opy_
      if bstack1111ll11lll_opy_ is None:
        logger.debug(bstack11ll11_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡧࠣࡒࡴࡴࡥࠣᴤ"))
        return bstack1l111ll11_opy_
      bstack1111lllll11_opy_ = int(str(bstack1111lll1lll_opy_()).split(bstack11ll11_opy_ (u"࠭࠮ࠨᴥ"))[0])
      logger.debug(bstack11ll11_opy_ (u"ࠢࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡨࡪࡺࡥࡤࡶࡨࡨ࠿ࠦࠢᴦ") + str(bstack1111lllll11_opy_) + bstack11ll11_opy_ (u"ࠣࠤᴧ"))
      if bstack1111lllll11_opy_ == 3 and isinstance(bstack1l111ll11_opy_, dict) and bstack11ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᴨ") in bstack1l111ll11_opy_ and bstack1111ll11lll_opy_ is not None:
        if bstack11ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᴩ") not in bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᴪ")]:
          bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᴫ")][bstack11ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᴬ")] = {}
        if bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᴭ") in bstack1111ll11lll_opy_:
          if bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᴮ") not in bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᴯ")][bstack11ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᴰ")]:
            bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᴱ")][bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᴲ")][bstack11ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫᴳ")] = []
          for arg in bstack1111ll11lll_opy_[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᴴ")]:
            if arg not in bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴵ")][bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴶ")][bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᴷ")]:
              bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᴸ")][bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᴹ")][bstack11ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫᴺ")].append(arg)
        if bstack11ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᴻ") in bstack1111ll11lll_opy_:
          if bstack11ll11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᴼ") not in bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᴽ")][bstack11ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᴾ")]:
            bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᴿ")][bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵀ")][bstack11ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵁ")] = []
          for ext in bstack1111ll11lll_opy_[bstack11ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᵂ")]:
            if ext not in bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᵃ")][bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᵄ")][bstack11ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵅ")]:
              bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵆ")][bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵇ")][bstack11ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵈ")].append(ext)
        if bstack11ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵉ") in bstack1111ll11lll_opy_:
          if bstack11ll11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵊ") not in bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵋ")][bstack11ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵌ")]:
            bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵍ")][bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵎ")][bstack11ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵏ")] = {}
          bstack1111l1llll1_opy_(bstack1l111ll11_opy_[bstack11ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵐ")][bstack11ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵑ")][bstack11ll11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵒ")],
                    bstack1111ll11lll_opy_[bstack11ll11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᵓ")])
        os.environ[bstack11ll11_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᵔ")] = bstack11ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪᵕ")
        return bstack1l111ll11_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l111ll11_opy_, ChromeOptions):
          chrome_options = bstack1l111ll11_opy_
        elif isinstance(bstack1l111ll11_opy_, dict):
          for value in bstack1l111ll11_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l111ll11_opy_, dict):
            bstack1l111ll11_opy_[bstack11ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᵖ")] = chrome_options
          else:
            bstack1l111ll11_opy_ = chrome_options
        if bstack1111ll11lll_opy_ is not None:
          if bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᵗ") in bstack1111ll11lll_opy_:
                bstack1111lll1l1l_opy_ = chrome_options.arguments or []
                new_args = bstack1111ll11lll_opy_[bstack11ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵘ")]
                for arg in new_args:
                    if arg not in bstack1111lll1l1l_opy_:
                        chrome_options.add_argument(arg)
          if bstack11ll11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵙ") in bstack1111ll11lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵚ"), [])
                bstack1111lll11l1_opy_ = bstack1111ll11lll_opy_[bstack11ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᵛ")]
                for extension in bstack1111lll11l1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵜ") in bstack1111ll11lll_opy_:
                bstack1111ll1l1ll_opy_ = chrome_options.experimental_options.get(bstack11ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵝ"), {})
                bstack1111lll1111_opy_ = bstack1111ll11lll_opy_[bstack11ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵞ")]
                bstack1111l1llll1_opy_(bstack1111ll1l1ll_opy_, bstack1111lll1111_opy_)
                chrome_options.add_experimental_option(bstack11ll11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵟ"), bstack1111ll1l1ll_opy_)
        os.environ[bstack11ll11_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᵠ")] = bstack11ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨᵡ")
        return bstack1l111ll11_opy_
    except Exception as e:
      logger.error(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡨࡩ࡯࡮ࡨࠢࡱࡳࡳ࠳ࡂࡔࠢ࡬ࡲ࡫ࡸࡡࠡࡣ࠴࠵ࡾࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠤᵢ") + str(e))
      return bstack1l111ll11_opy_