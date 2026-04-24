# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack111ll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack111ll11_opy_ (bstack1111l1_opy_):
    global bstack1llll11_opy_
    bstack1ll11l1_opy_ = ord (bstack1111l1_opy_ [-1])
    bstack11ll_opy_ = bstack1111l1_opy_ [:-1]
    bstack1llll1_opy_ = bstack1ll11l1_opy_ % len (bstack11ll_opy_)
    bstack1ll1_opy_ = bstack11ll_opy_ [:bstack1llll1_opy_] + bstack11ll_opy_ [bstack1llll1_opy_:]
    if bstack11llll_opy_:
        bstack1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1l1_opy_ = str () .join ([chr (ord (char) - bstack111ll1_opy_ - (bstack1l1l1l_opy_ + bstack1ll11l1_opy_) % bstack11ll1_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1l1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111l1ll11l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111lll11ll_opy_ as bstack1111ll1l111_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack1llllll1l11_opy_, bstack1lll1l1l11l_opy_, bstack11lll11l11_opy_, bstack1111l1ll1ll_opy_, \
  bstack1111ll1l1l1_opy_, bstack1l11111lll_opy_, get_host_info, bstack1111l1lllll_opy_, bstack111l1l1ll1_opy_, error_handler, bstack1111ll11l11_opy_, bstack1111l1lll11_opy_, bstack111lll1ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1lll1l1ll1_opy_ import bstack1ll1l11l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1lll1l1ll1_opy_ = bstack1ll1l11l1_opy_()
@error_handler(class_method=False)
def _1111ll1lll1_opy_(driver, bstack1ll11l1l1ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111ll11_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧᰩ"): caps.get(bstack111ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᰪ"), None),
        bstack111ll11_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᰫ"): bstack1ll11l1l1ll_opy_.get(bstack111ll11_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᰬ"), None),
        bstack111ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᰭ"): caps.get(bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᰮ"), None),
        bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᰯ"): caps.get(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᰰ"), None)
    }
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᰱ") + str(error))
  return response
def on():
    if os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᰲ"), None) is None or os.environ[bstack111ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᰳ")] == bstack111ll11_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᰴ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᰵ"), False) or any([p.get(bstack111ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᰶ"), False) == True for p in config.get(bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴ᰷ࠩ"), [])])
def is_enabled_platform(config, bstack1l1ll11l1l_opy_):
  try:
    bstack1lll11l1111_opy_ = config.get(bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᰸"), False)
    _1ll1l1lll1l_opy_ = int(bstack1l1ll11l1l_opy_)
    if _1ll1l1lll1l_opy_ < 0:
      _1ll1l1lll1l_opy_ = 0
    bstack11lll1l1ll_opy_ = config.get(bstack111ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᰹"), [])
    if _1ll1l1lll1l_opy_ < len(bstack11lll1l1ll_opy_) and bstack11lll1l1ll_opy_[_1ll1l1lll1l_opy_]:
      bstack1111l1l11ll_opy_ = bstack11lll1l1ll_opy_[_1ll1l1lll1l_opy_].get(bstack111ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᰺"), None)
    else:
      bstack1111l1l11ll_opy_ = config.get(bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᰻"), None)
    if bstack1111l1l11ll_opy_ != None:
      bstack1lll11l1111_opy_ = bstack1111l1l11ll_opy_
    bstack1111l1l1ll1_opy_ = os.getenv(bstack111ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᰼")) is not None and len(os.getenv(bstack111ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᰽"))) > 0 and os.getenv(bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᰾")) != bstack111ll11_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ᰿")
    return bstack1lll11l1111_opy_ and bstack1111l1l1ll1_opy_
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ᱀") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l1111ll1l1_opy_ = os.getenv(bstack111ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ᱁"))
  if bstack1l1111ll1l1_opy_ is None:
    return True
  bstack1l1111ll1l1_opy_ = json.loads(bstack1l1111ll1l1_opy_)
  try:
    include_tags = bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᱂")] if bstack111ll11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩ᱃") in bstack1l1111ll1l1_opy_ and isinstance(bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ᱄")], list) else []
    exclude_tags = bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᱅")] if bstack111ll11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᱆") in bstack1l1111ll1l1_opy_ and isinstance(bstack1l1111ll1l1_opy_[bstack111ll11_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᱇")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤ᱈") + str(error))
  return False
def bstack1111ll11111_opy_(config, bstack1111ll1llll_opy_, bstack1111l1l1l1l_opy_, bstack1111ll1ll1l_opy_):
  bstack1111ll11lll_opy_ = bstack1111l1ll1ll_opy_(config)
  bstack1111ll111l1_opy_ = bstack1111ll1l1l1_opy_(config)
  if bstack1111ll11lll_opy_ is None or bstack1111ll111l1_opy_ is None:
    logger.error(bstack111ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫ᱉"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᱊"), bstack111ll11_opy_ (u"ࠬࢁࡽࠨ᱋")))
    data = {
        bstack111ll11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ᱌"): config[bstack111ll11_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᱍ")],
        bstack111ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᱎ"): config.get(bstack111ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᱏ"), os.path.basename(os.getcwd())),
        bstack111ll11_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭᱐"): bstack1llllll1l11_opy_(),
        bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ᱑"): config.get(bstack111ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ᱒"), bstack111ll11_opy_ (u"࠭ࠧ᱓")),
        bstack111ll11_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧ᱔"): {
            bstack111ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ᱕"): bstack1111ll1llll_opy_,
            bstack111ll11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ᱖"): bstack1111l1l1l1l_opy_,
            bstack111ll11_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᱗"): __version__,
            bstack111ll11_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭᱘"): bstack111ll11_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ᱙"),
            bstack111ll11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᱚ"): bstack111ll11_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᱛ"),
            bstack111ll11_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᱜ"): bstack1111ll1ll1l_opy_
        },
        bstack111ll11_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᱝ"): settings,
        bstack111ll11_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᱞ"): bstack1111l1lllll_opy_(),
        bstack111ll11_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᱟ"): bstack1l11111lll_opy_(),
        bstack111ll11_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᱠ"): get_host_info(),
        bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᱡ"): bstack11lll11l11_opy_(config)
    }
    headers = {
        bstack111ll11_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᱢ"): bstack111ll11_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᱣ"),
    }
    config = {
        bstack111ll11_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᱤ"): (bstack1111ll11lll_opy_, bstack1111ll111l1_opy_),
        bstack111ll11_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᱥ"): headers
    }
    response = bstack111l1l1ll1_opy_(bstack111ll11_opy_ (u"ࠫࡕࡕࡓࡕࠩᱦ"), bstack1111ll1l111_opy_ + bstack111ll11_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᱧ"), data, config)
    bstack1111lll1lll_opy_ = response.json()
    if bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᱨ")]:
      parsed = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᱩ"), bstack111ll11_opy_ (u"ࠨࡽࢀࠫᱪ")))
      parsed[bstack111ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᱫ")] = bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"ࠪࡨࡦࡺࡡࠨᱬ")][bstack111ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᱭ")]
      os.environ[bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᱮ")] = json.dumps(parsed)
      accessibility_scripts.bstack1l1l1l1l11_opy_(bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫᱯ")][bstack111ll11_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᱰ")])
      accessibility_scripts.bstack1l11lll11ll_opy_(bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᱱ")][bstack111ll11_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᱲ")])
      accessibility_scripts.store()
      return bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"ࠪࡨࡦࡺࡡࠨᱳ")][bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᱴ")], bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"ࠬࡪࡡࡵࡣࠪᱵ")][bstack111ll11_opy_ (u"࠭ࡩࡥࠩᱶ")]
    else:
      logger.error(bstack111ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᱷ") + bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᱸ")])
      if bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᱹ")] == bstack111ll11_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᱺ"):
        for bstack1111l1l1111_opy_ in bstack1111lll1lll_opy_[bstack111ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᱻ")]:
          logger.error(bstack1111l1l1111_opy_[bstack111ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᱼ")])
      return None, None
  except Exception as error:
    logger.error(bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᱽ") +  str(error))
    return None, None
def bstack1111lll111l_opy_():
  if os.getenv(bstack111ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᱾")) is None:
    return {
        bstack111ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᱿"): bstack111ll11_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᲀ"),
        bstack111ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᲁ"): bstack111ll11_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᲂ")
    }
  data = {bstack111ll11_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᲃ"): bstack1llllll1l11_opy_()}
  headers = {
      bstack111ll11_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᲄ"): bstack111ll11_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᲅ") + os.getenv(bstack111ll11_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨᲆ")),
      bstack111ll11_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᲇ"): bstack111ll11_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᲈ")
  }
  response = bstack111l1l1ll1_opy_(bstack111ll11_opy_ (u"ࠫࡕ࡛ࡔࠨᲉ"), bstack1111ll1l111_opy_ + bstack111ll11_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᲊ"), data, { bstack111ll11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ᲋"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111ll11_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣ᲌") + bstack1lll1l1l11l_opy_().isoformat() + bstack111ll11_opy_ (u"ࠨ࡜ࠪ᲍"))
      return {bstack111ll11_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᲎"): bstack111ll11_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ᲏"), bstack111ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᲐ"): bstack111ll11_opy_ (u"ࠬ࠭Ბ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᲒ") + str(error))
    return {
        bstack111ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᲓ"): bstack111ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᲔ"),
        bstack111ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᲕ"): str(error)
    }
def bstack1111ll11ll1_opy_(bstack1111l1l1l11_opy_):
    return re.match(bstack111ll11_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫᲖ"), bstack1111l1l1l11_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1111l1ll111_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1111l1ll111_opy_ = desired_capabilities
        else:
          bstack1111l1ll111_opy_ = {}
        bstack11lllllll1l_opy_ = (bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᲗ"), bstack111ll11_opy_ (u"ࠬ࠭Ი")).lower() or caps.get(bstack111ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᲙ"), bstack111ll11_opy_ (u"ࠧࠨᲚ")).lower())
        if bstack11lllllll1l_opy_ == bstack111ll11_opy_ (u"ࠨ࡫ࡲࡷࠬᲛ"):
            return True
        if bstack11lllllll1l_opy_ == bstack111ll11_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᲜ"):
            bstack1111l1l1l11_opy_ = caps.get(bstack111ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲝ")) or bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᲞ"), {}).get(bstack111ll11_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲟ"), bstack111ll11_opy_ (u"࠭ࠧᲠ"))
            if bstack1111l1l1l11_opy_:
                try:
                    bstack1111ll111ll_opy_ = int(str(bstack1111l1l1l11_opy_).split(bstack111ll11_opy_ (u"ࠧ࠯ࠩᲡ"))[0])
                    min_version = int(float(bstack1111ll1l1ll_opy_))
                    if bstack1111ll111ll_opy_ < min_version:
                        logger.warning(bstack1111l1lll1l_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack111ll11_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠦࠧࠦࡵࠪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡲࡲ࠳ࠨᲢ"), bstack1111l1l1l11_opy_)
            return True
        bstack1l1111ll111_opy_ = caps.get(bstack111ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲣ"), {}).get(bstack111ll11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᲤ"), caps.get(bstack111ll11_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᲥ"), bstack111ll11_opy_ (u"ࠬ࠭Ღ")))
        if bstack1l1111ll111_opy_:
            logger.warning(bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᲧ"))
            return False
        browser = (caps.get(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᲨ"), bstack111ll11_opy_ (u"ࠨࠩᲩ")) or caps.get(bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᲪ"), bstack111ll11_opy_ (u"ࠪࠫᲫ"))).lower() or \
                  (bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᲬ"), bstack111ll11_opy_ (u"ࠬ࠭Ჭ")) or bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧᲮ"), bstack111ll11_opy_ (u"ࠧࠨᲯ"))).lower()
        if browser not in (bstack111ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᲰ"), bstack111ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫᲱ"), bstack111ll11_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩᲲ")):
            logger.warning(bstack111ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᲳ"))
            return False
        browser_version = caps.get(bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ჴ")) or caps.get(bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᲵ")) or bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲶ")) or bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲷ"), {}).get(bstack111ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᲸ")) or bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲹ"), {}).get(bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭Ჺ"))
        bstack1l111l1111l_opy_ = bstack1111l1ll11l_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack1111ll1ll11_opy_ = False
        if config is not None:
          bstack1111ll1ll11_opy_ = bstack111ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᲻") in config and str(config[bstack111ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᲼")]).lower() != bstack111ll11_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭Ჽ")
        if os.environ.get(bstack111ll11_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭Ჾ"), bstack111ll11_opy_ (u"ࠩࠪᲿ")).lower() == bstack111ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨ᳀") or bstack1111ll1ll11_opy_:
          bstack1l111l1111l_opy_ = bstack1111l1ll11l_opy_.bstack1l1111l1lll_opy_
        if browser_version and browser_version != bstack111ll11_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫ᳁") and int(browser_version.split(bstack111ll11_opy_ (u"ࠬ࠴ࠧ᳂"))[0]) <= bstack1l111l1111l_opy_:
          logger.warning(bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࠣ᳃") + str(bstack1l111l1111l_opy_) + bstack111ll11_opy_ (u"ࠢ࠯ࠤ᳄"))
          return False
        bstack1l111l1l1ll_opy_ = (caps.get(bstack111ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᳅"))
                         or bstack1111l1ll111_opy_.get(bstack111ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᳆"), {})
                         or caps.get(bstack111ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᳇"), {}))
        bstack1lll1111111_opy_ = bstack1l111l1l1ll_opy_.get(bstack111ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩ᳈"), []) if isinstance(bstack1l111l1l1ll_opy_, dict) else []
        if not isinstance(bstack1lll1111111_opy_, list):
            bstack1lll1111111_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack111ll11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩ᳉") or arg == bstack111ll11_opy_ (u"࠭ࡨࡦࡣࡧࡰࡪࡹࡳࠨ᳊") or (arg.startswith(bstack111ll11_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࠬ᳋")) and arg != bstack111ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࡂࡴࡥࡸࠩ᳌")))
               for arg in bstack1lll1111111_opy_):
            logger.warning(bstack111ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦ᳍"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack111ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧ᳎") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l111lllll1_opy_ = config.get(bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᳏"), {})
    bstack1l111lllll1_opy_[bstack111ll11_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨ᳐")] = os.getenv(bstack111ll11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᳑"))
    bstack1l1ll111ll_opy_ = json.loads(os.getenv(bstack111ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᳒"), bstack111ll11_opy_ (u"ࠨࡽࢀࠫ᳓"))).get(bstack111ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰ᳔ࠪ"))
    if not config[bstack111ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴ᳕ࠬ")].get(bstack111ll11_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧ᳖ࠥ")):
      if bstack111ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ᳗࠭") in caps:
        caps[bstack111ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹ᳘ࠧ")][bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ᳙ࠧ")] = bstack1l111lllll1_opy_
        caps[bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᳚")][bstack111ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳛")][bstack111ll11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱ᳜ࠫ")] = bstack1l1ll111ll_opy_
      else:
        caps[bstack111ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵ᳝ࠪ")] = bstack1l111lllll1_opy_
        caps[bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ᳞ࠫ")][bstack111ll11_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴ᳟ࠧ")] = bstack1l1ll111ll_opy_
  except Exception as error:
    logger.debug(bstack111ll11_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࠣ᳠") +  str(error))
def start_test_capture(driver, bstack1111lll1111_opy_):
  try:
    setattr(driver, bstack111ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ᳡"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack111ll11_opy_ (u"ࠩࡉࡖࡆࡓࡅࡘࡑࡕࡏࡤ࡛ࡓࡆࡆ᳢ࠪ")) == bstack111ll11_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰ࠰࡫ࡪࡴࡥࡳ࡫ࡦ᳣ࠫ")):
        bstack1111ll1111l_opy_ = bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ᳤࠭"), None)
        if bstack1111ll1111l_opy_:
          if bstack1111lll1111_opy_:
            logger.info(bstack111ll11_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡳࡴࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲࠳࠴᳥ࠢ"))
          return bstack1111lll1111_opy_
      bstack1111l1l11l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111l1l11l1_opy_ = False
      bstack1111l1l11l1_opy_ = url.scheme in [bstack111ll11_opy_ (u"ࠨࡨࡵࡶࡳ᳦ࠦ"), bstack111ll11_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨ᳧")]
      if bstack1111l1l11l1_opy_:
        if bstack1111lll1111_opy_:
          logger.info(bstack111ll11_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮᳨ࠣ"))
      return bstack1111lll1111_opy_
  except Exception as e:
    logger.error(bstack111ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᳩ") + str(e))
    return False
def bstack11111llll1_opy_(driver, name, path):
  try:
    bstack1l11111llll_opy_ = {
        bstack111ll11_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᳪ"): threading.current_thread().current_test_uuid,
        bstack111ll11_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᳫ"): os.environ.get(bstack111ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᳬ"), bstack111ll11_opy_ (u"᳭࠭ࠧ")),
        bstack111ll11_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫᳮ"): os.environ.get(bstack111ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᳯ"), bstack111ll11_opy_ (u"ࠩࠪᳰ"))
    }
    bstack11111l11ll_opy_ = bstack1lll1l1ll1_opy_.bstack11lllll1_opy_(EVENTS.bstack1lll11llll_opy_.value)
    logger.debug(bstack111ll11_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᳱ"))
    try:
      if (bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᳲ"), None) and bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᳳ"), None)):
        scripts = {bstack111ll11_opy_ (u"࠭ࡳࡤࡣࡱࠫ᳴"): accessibility_scripts.perform_scan}
        bstack1111lll1ll1_opy_ = json.loads(scripts[bstack111ll11_opy_ (u"ࠢࡴࡥࡤࡲࠧᳵ")].replace(bstack111ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᳶ"), bstack111ll11_opy_ (u"ࠤࠥ᳷")))
        bstack1111lll1ll1_opy_[bstack111ll11_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᳸")][bstack111ll11_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫ᳹")] = None
        scripts[bstack111ll11_opy_ (u"ࠧࡹࡣࡢࡰࠥᳺ")] = bstack111ll11_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᳻") + json.dumps(bstack1111lll1ll1_opy_)
        accessibility_scripts.bstack1l1l1l1l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack111ll11_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢ᳼"): name}))
      bstack1lll1l1ll1_opy_.end(EVENTS.bstack1lll11llll_opy_.value, bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᳽"), bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᳾"), True, None)
    except Exception as error:
      bstack1lll1l1ll1_opy_.end(EVENTS.bstack1lll11llll_opy_.value, bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᳿"), bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᴀ"), False, str(error))
    bstack11111l11ll_opy_ = bstack1lll1l1ll1_opy_.bstack1111lll11l1_opy_(EVENTS.bstack11lllll11ll_opy_.value)
    bstack1lll1l1ll1_opy_.mark(bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᴁ"))
    try:
      if (bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᴂ"), None) and bstack111lll1ll1_opy_(threading.current_thread(), bstack111ll11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᴃ"), None)):
        scripts = {bstack111ll11_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᴄ"): accessibility_scripts.perform_scan}
        bstack1111lll1ll1_opy_ = json.loads(scripts[bstack111ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢᴅ")].replace(bstack111ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᴆ"), bstack111ll11_opy_ (u"ࠦࠧᴇ")))
        bstack1111lll1ll1_opy_[bstack111ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᴈ")][bstack111ll11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᴉ")] = None
        scripts[bstack111ll11_opy_ (u"ࠢࡴࡥࡤࡲࠧᴊ")] = bstack111ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᴋ") + json.dumps(bstack1111lll1ll1_opy_)
        accessibility_scripts.bstack1l1l1l1l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l11111llll_opy_))
      bstack1lll1l1ll1_opy_.end(bstack11111l11ll_opy_, bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᴌ"), bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᴍ"),True, None)
    except Exception as error:
      bstack1lll1l1ll1_opy_.end(bstack11111l11ll_opy_, bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᴎ"), bstack11111l11ll_opy_ + bstack111ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᴏ"),False, str(error))
    logger.info(bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᴐ"))
    try:
      bstack1l111l11l1l_opy_ = {
        bstack111ll11_opy_ (u"ࠢࡳࡧࡴࡹࡪࡹࡴࠣᴑ"): {
          bstack111ll11_opy_ (u"ࠣࡥࡲࡱࡲࡧ࡮ࡥࠤᴒ"): bstack111ll11_opy_ (u"ࠤࡄ࠵࠶࡟࡟ࡔࡃ࡙ࡉࡤࡘࡅࡔࡗࡏࡘࡘࠨᴓ"),
        },
        bstack111ll11_opy_ (u"ࠥࡶࡪࡹࡰࡰࡰࡶࡩࠧᴔ"): {
          bstack111ll11_opy_ (u"ࠦࡧࡵࡤࡺࠤᴕ"): {
            bstack111ll11_opy_ (u"ࠧࡳࡳࡨࠤᴖ"): bstack111ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᴗ"),
            bstack111ll11_opy_ (u"ࠢࡴࡷࡦࡧࡪࡹࡳࠣᴘ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l111l11l1l_opy_, separators=(bstack111ll11_opy_ (u"ࠨ࠮ࠪᴙ"), bstack111ll11_opy_ (u"ࠩ࠽ࠫᴚ"))))
    except Exception as bstack11111111_opy_:
      logger.debug(bstack111ll11_opy_ (u"ࠥࡊࡦ࡯࡬ࡦࡦࠣࡸࡴࠦ࡬ࡰࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡦࡼࡥࠡࡴࡨࡷࡺࡲࡴࡴࠢࡧࡥࡹࡧ࠺ࠡࠤᴛ") + str(bstack11111111_opy_) + bstack111ll11_opy_ (u"ࠦࠧᴜ"))
  except Exception as bstack1l1111l1ll1_opy_:
    logger.error(bstack111ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡣࡰࡷ࡯ࡨࠥࡴ࡯ࡵࠢࡥࡩࠥࡶࡲࡰࡥࡨࡷࡸ࡫ࡤࠡࡨࡲࡶࠥࡺࡨࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᴝ") + str(path) + bstack111ll11_opy_ (u"ࠨࠠࡆࡴࡵࡳࡷࠦ࠺ࠣᴞ") + str(bstack1l1111l1ll1_opy_))
def bstack1111lll1l11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack111ll11_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᴟ")) and str(caps.get(bstack111ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᴠ"))).lower() == bstack111ll11_opy_ (u"ࠤࡤࡲࡩࡸ࡯ࡪࡦࠥᴡ"):
        bstack1l111ll11l1_opy_ = caps.get(bstack111ll11_opy_ (u"ࠥࡥࡵࡶࡩࡶ࡯࠽ࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᴢ")) or caps.get(bstack111ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᴣ"))
        if bstack1l111ll11l1_opy_:
            try:
              bstack1111l1l1l11_opy_ = str(bstack1l111ll11l1_opy_).split(bstack111ll11_opy_ (u"ࠬ࠴ࠧᴤ"))[0]
              min_version = int(float(bstack1111ll1l1ll_opy_))
              if int(bstack1111l1l1l11_opy_) < min_version:
                  logger.warning(bstack1111l1lll1l_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack111ll11_opy_ (u"ࠨࡕ࡯ࡣࡥࡰࡪࠦࡴࡰࠢࡳࡥࡷࡹࡥࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡢࡺࡪࡸࡳࡪࡱࡱࠤࠬࠫࡳࠨࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡶࡢ࡮࡬ࡨࡦࡺࡩࡰࡰ࠱ࠦᴥ"), bstack1l111ll11l1_opy_)
    return True
def bstack11111ll11_opy_(config):
  if bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴦ") in config:
        return config[bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴧ")]
  for platform in config.get(bstack111ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᴨ"), []):
      if bstack111ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴩ") in platform:
          return platform[bstack111ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴪ")]
  return None
def bstack11lll1l1_opy_(bstack1l1l111ll1_opy_):
  try:
    browser_name = bstack1l1l111ll1_opy_[bstack111ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᴫ")]
    browser_version = bstack1l1l111ll1_opy_[bstack111ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᴬ")]
    chrome_options = bstack1l1l111ll1_opy_[bstack111ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᴭ")]
    try:
        bstack1111l11llll_opy_ = int(browser_version.split(bstack111ll11_opy_ (u"ࠨ࠰ࠪᴮ"))[0])
    except ValueError as e:
        logger.error(bstack111ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨᴯ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack111ll11_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᴰ")):
        logger.warning(bstack111ll11_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᴱ"))
        return False
    if bstack1111l11llll_opy_ < bstack1111l1ll11l_opy_.bstack1l1111l1lll_opy_:
        logger.warning(bstack111ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࠨᴲ") + str(bstack1111l1ll11l_opy_.bstack1l1111l1lll_opy_) + bstack111ll11_opy_ (u"ࠨࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠦᴳ"))
        return False
    bstack1lll1111111_opy_ = chrome_options.get(bstack111ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᴴ"), []) if chrome_options else []
    if not isinstance(bstack1lll1111111_opy_, list):
        bstack1lll1111111_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack111ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᴵ") or arg == bstack111ll11_opy_ (u"ࠩ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᴶ") or (arg.startswith(bstack111ll11_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽ࠨᴷ")) and arg != bstack111ll11_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࡰࡨࡻࠬᴸ")))
           for arg in bstack1lll1111111_opy_):
        logger.warning(bstack111ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᴹ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack111ll11_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥ࡯࡮ࠡࡥ࡫ࡩࡨࡱࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡹࡵࡱࡲࡲࡶࡹࠦࡦࡰࡴࠣࡰࡴࡩࡡ࡭ࠢࡆ࡬ࡷࡵ࡭ࡦ࠼ࠣࠦᴺ") + str(e))
    return False
def bstack1l1ll1l1l1_opy_(bstack111111l1_opy_, config):
    try:
      bstack1l111l11ll1_opy_ = bstack111ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴻ") in config and config[bstack111ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᴼ")] == True
      bstack1111ll1ll11_opy_ = bstack111ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᴽ") in config and str(config[bstack111ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᴾ")]).lower() != bstack111ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᴿ")
      if not (bstack1l111l11ll1_opy_ and (not bstack11lll11l11_opy_(config) or bstack1111ll1ll11_opy_)):
        return bstack111111l1_opy_
      bstack1111ll11l1l_opy_ = accessibility_scripts.bstack1111l1llll1_opy_
      if bstack1111ll11l1l_opy_ is None:
        logger.debug(bstack111ll11_opy_ (u"ࠧࡍ࡯ࡰࡩ࡯ࡩࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࠦࡡࡳࡧࠣࡒࡴࡴࡥࠣᵀ"))
        return bstack111111l1_opy_
      bstack1111l1l111l_opy_ = int(str(bstack1111l1lll11_opy_()).split(bstack111ll11_opy_ (u"࠭࠮ࠨᵁ"))[0])
      logger.debug(bstack111ll11_opy_ (u"ࠢࡔࡧ࡯ࡩࡳ࡯ࡵ࡮ࠢࡹࡩࡷࡹࡩࡰࡰࠣࡨࡪࡺࡥࡤࡶࡨࡨ࠿ࠦࠢᵂ") + str(bstack1111l1l111l_opy_) + bstack111ll11_opy_ (u"ࠣࠤᵃ"))
      if bstack1111l1l111l_opy_ == 3 and isinstance(bstack111111l1_opy_, dict) and bstack111ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵄ") in bstack111111l1_opy_ and bstack1111ll11l1l_opy_ is not None:
        if bstack111ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵅ") not in bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵆ")]:
          bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵇ")][bstack111ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᵈ")] = {}
        if bstack111ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᵉ") in bstack1111ll11l1l_opy_:
          if bstack111ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵊ") not in bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵋ")][bstack111ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵌ")]:
            bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵍ")][bstack111ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵎ")][bstack111ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫᵏ")] = []
          for arg in bstack1111ll11l1l_opy_[bstack111ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᵐ")]:
            if arg not in bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᵑ")][bstack111ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᵒ")][bstack111ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᵓ")]:
              bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵔ")][bstack111ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵕ")][bstack111ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫᵖ")].append(arg)
        if bstack111ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᵗ") in bstack1111ll11l1l_opy_:
          if bstack111ll11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᵘ") not in bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵙ")][bstack111ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵚ")]:
            bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵛ")][bstack111ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵜ")][bstack111ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵝ")] = []
          for ext in bstack1111ll11l1l_opy_[bstack111ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᵞ")]:
            if ext not in bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᵟ")][bstack111ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᵠ")][bstack111ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵡ")]:
              bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵢ")][bstack111ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵣ")][bstack111ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵤ")].append(ext)
        if bstack111ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵥ") in bstack1111ll11l1l_opy_:
          if bstack111ll11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵦ") not in bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵧ")][bstack111ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵨ")]:
            bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵩ")][bstack111ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵪ")][bstack111ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵫ")] = {}
          bstack1111ll11l11_opy_(bstack111111l1_opy_[bstack111ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵬ")][bstack111ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵭ")][bstack111ll11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵮ")],
                    bstack1111ll11l1l_opy_[bstack111ll11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᵯ")])
        os.environ[bstack111ll11_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᵰ")] = bstack111ll11_opy_ (u"ࠬࡺࡲࡶࡧࠪᵱ")
        return bstack111111l1_opy_
      else:
        chrome_options = None
        if isinstance(bstack111111l1_opy_, ChromeOptions):
          chrome_options = bstack111111l1_opy_
        elif isinstance(bstack111111l1_opy_, dict):
          for value in bstack111111l1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack111111l1_opy_, dict):
            bstack111111l1_opy_[bstack111ll11_opy_ (u"࠭࡯ࡱࡶ࡬ࡳࡳࡹࠧᵲ")] = chrome_options
          else:
            bstack111111l1_opy_ = chrome_options
        if bstack1111ll11l1l_opy_ is not None:
          if bstack111ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᵳ") in bstack1111ll11l1l_opy_:
                bstack1111l1ll1l1_opy_ = chrome_options.arguments or []
                new_args = bstack1111ll11l1l_opy_[bstack111ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵴ")]
                for arg in new_args:
                    if arg not in bstack1111l1ll1l1_opy_:
                        chrome_options.add_argument(arg)
          if bstack111ll11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵵ") in bstack1111ll11l1l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack111ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵶ"), [])
                bstack1111l1l1lll_opy_ = bstack1111ll11l1l_opy_[bstack111ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᵷ")]
                for extension in bstack1111l1l1lll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack111ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵸ") in bstack1111ll11l1l_opy_:
                bstack1111lll1l1l_opy_ = chrome_options.experimental_options.get(bstack111ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵹ"), {})
                bstack1111ll1l11l_opy_ = bstack1111ll11l1l_opy_[bstack111ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵺ")]
                bstack1111ll11l11_opy_(bstack1111lll1l1l_opy_, bstack1111ll1l11l_opy_)
                chrome_options.add_experimental_option(bstack111ll11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵻ"), bstack1111lll1l1l_opy_)
        os.environ[bstack111ll11_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᵼ")] = bstack111ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨᵽ")
        return bstack111111l1_opy_
    except Exception as e:
      logger.error(bstack111ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡤࡨࡩ࡯࡮ࡨࠢࡱࡳࡳ࠳ࡂࡔࠢ࡬ࡲ࡫ࡸࡡࠡࡣ࠴࠵ࡾࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹ࠺ࠡࠤᵾ") + str(e))
      return bstack111111l1_opy_