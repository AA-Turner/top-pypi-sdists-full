# coding: UTF-8
import sys
bstack11l11ll_opy_ = sys.version_info [0] == 2
bstack1l1ll11_opy_ = 2048
bstack1ll1l_opy_ = 7
def bstack1ll_opy_ (bstack1l11l1_opy_):
    global bstack1l1l1l1_opy_
    bstack111_opy_ = ord (bstack1l11l1_opy_ [-1])
    bstack11111l_opy_ = bstack1l11l1_opy_ [:-1]
    bstack11l111_opy_ = bstack111_opy_ % len (bstack11111l_opy_)
    bstack1lll11_opy_ = bstack11111l_opy_ [:bstack11l111_opy_] + bstack11111l_opy_ [bstack11l111_opy_:]
    if bstack11l11ll_opy_:
        bstack1ll1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    else:
        bstack1ll1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1ll11_opy_ - (bstack1l1lll_opy_ + bstack111_opy_) % bstack1ll1l_opy_) for bstack1l1lll_opy_, char in enumerate (bstack1lll11_opy_)])
    return eval (bstack1ll1l1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111llll111_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111ll1l111_opy_ as bstack1111ll1llll_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack11l1ll1ll_opy_, bstack1lll1l111l1_opy_, bstack1lll1111ll_opy_, bstack1111l1l111l_opy_, \
  bstack1111ll1l11l_opy_, bstack1lll11l1ll_opy_, get_host_info, bstack1111lll1l11_opy_, bstack1l1111l111_opy_, error_handler, bstack1111l1lll11_opy_, bstack1111l1l1lll_opy_, bstack1llll1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1l11ll1lll_opy_ import bstack1l11l1ll11_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1l11ll1lll_opy_ = bstack1l11l1ll11_opy_()
@error_handler(class_method=False)
def _1111l1ll111_opy_(driver, bstack1ll11l1l11l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪᰐ"): caps.get(bstack1ll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᰑ"), None),
        bstack1ll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᰒ"): bstack1ll11l1l11l_opy_.get(bstack1ll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᰓ"), None),
        bstack1ll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᰔ"): caps.get(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᰕ"), None),
        bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᰖ"): caps.get(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᰗ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᰘ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᰙ"), None) is None or os.environ[bstack1ll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᰚ")] == bstack1ll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᰛ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᰜ"), False) or any([p.get(bstack1ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᰝ"), False) == True for p in config.get(bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᰞ"), [])])
def is_enabled_platform(config, bstack11l11ll1_opy_):
  try:
    bstack1lll1111ll1_opy_ = config.get(bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᰟ"), False)
    _1ll1ll11lll_opy_ = int(bstack11l11ll1_opy_)
    if _1ll1ll11lll_opy_ < 0:
      _1ll1ll11lll_opy_ = 0
    bstack1lll1lll1_opy_ = config.get(bstack1ll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᰠ"), [])
    if _1ll1ll11lll_opy_ < len(bstack1lll1lll1_opy_) and bstack1lll1lll1_opy_[_1ll1ll11lll_opy_]:
      bstack1111l1l1l11_opy_ = bstack1lll1lll1_opy_[_1ll1ll11lll_opy_].get(bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᰡ"), None)
    else:
      bstack1111l1l1l11_opy_ = config.get(bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᰢ"), None)
    if bstack1111l1l1l11_opy_ != None:
      bstack1lll1111ll1_opy_ = bstack1111l1l1l11_opy_
    bstack1111ll1lll1_opy_ = os.getenv(bstack1ll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᰣ")) is not None and len(os.getenv(bstack1ll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᰤ"))) > 0 and os.getenv(bstack1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᰥ")) != bstack1ll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᰦ")
    return bstack1lll1111ll1_opy_ and bstack1111ll1lll1_opy_
  except Exception as error:
    logger.debug(bstack1ll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᰧ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l111ll11ll_opy_ = os.getenv(bstack1ll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᰨ"))
  if bstack1l111ll11ll_opy_ is None:
    return True
  bstack1l111ll11ll_opy_ = json.loads(bstack1l111ll11ll_opy_)
  try:
    include_tags = bstack1l111ll11ll_opy_[bstack1ll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᰩ")] if bstack1ll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᰪ") in bstack1l111ll11ll_opy_ and isinstance(bstack1l111ll11ll_opy_[bstack1ll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᰫ")], list) else []
    exclude_tags = bstack1l111ll11ll_opy_[bstack1ll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᰬ")] if bstack1ll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᰭ") in bstack1l111ll11ll_opy_ and isinstance(bstack1l111ll11ll_opy_[bstack1ll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᰮ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᰯ") + str(error))
  return False
def bstack1111ll111ll_opy_(config, bstack1111l1lll1l_opy_, bstack1111ll11ll1_opy_, bstack1111ll11111_opy_):
  bstack1111ll11l1l_opy_ = bstack1111l1l111l_opy_(config)
  bstack1111lll1l1l_opy_ = bstack1111ll1l11l_opy_(config)
  if bstack1111ll11l1l_opy_ is None or bstack1111lll1l1l_opy_ is None:
    logger.error(bstack1ll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᰰ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᰱ"), bstack1ll_opy_ (u"ࠨࡽࢀࠫᰲ")))
    data = {
        bstack1ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᰳ"): config[bstack1ll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᰴ")],
        bstack1ll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᰵ"): config.get(bstack1ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᰶ"), os.path.basename(os.getcwd())),
        bstack1ll_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦ᰷ࠩ"): bstack11l1ll1ll_opy_(),
        bstack1ll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ᰸"): config.get(bstack1ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᰹"), bstack1ll_opy_ (u"ࠩࠪ᰺")),
        bstack1ll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ᰻"): {
            bstack1ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫ᰼"): bstack1111l1lll1l_opy_,
            bstack1ll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᰽"): bstack1111ll11ll1_opy_,
            bstack1ll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ᰾"): __version__,
            bstack1ll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ᰿"): bstack1ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ᱀"),
            bstack1ll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ᱁"): bstack1ll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬ᱂"),
            bstack1ll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ᱃"): bstack1111ll11111_opy_
        },
        bstack1ll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ᱄"): settings,
        bstack1ll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧ᱅"): bstack1111lll1l11_opy_(),
        bstack1ll_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧ᱆"): bstack1lll11l1ll_opy_(),
        bstack1ll_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪ᱇"): get_host_info(),
        bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫ᱈"): bstack1lll1111ll_opy_(config)
    }
    headers = {
        bstack1ll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩ᱉"): bstack1ll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧ᱊"),
    }
    config = {
        bstack1ll_opy_ (u"ࠬࡧࡵࡵࡪࠪ᱋"): (bstack1111ll11l1l_opy_, bstack1111lll1l1l_opy_),
        bstack1ll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ᱌"): headers
    }
    response = bstack1l1111l111_opy_(bstack1ll_opy_ (u"ࠧࡑࡑࡖࡘࠬᱍ"), bstack1111ll1llll_opy_ + bstack1ll_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᱎ"), data, config)
    bstack1111ll1ll11_opy_ = response.json()
    if bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᱏ")]:
      parsed = json.loads(os.getenv(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ᱐"), bstack1ll_opy_ (u"ࠫࢀࢃࠧ᱑")))
      parsed[bstack1ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᱒")] = bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫ᱓")][bstack1ll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᱔")]
      os.environ[bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ᱕")] = json.dumps(parsed)
      accessibility_scripts.bstack11lll1l1_opy_(bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"ࠩࡧࡥࡹࡧࠧ᱖")][bstack1ll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᱗")])
      accessibility_scripts.bstack1l1l1l1l111_opy_(bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"ࠫࡩࡧࡴࡢࠩ᱘")][bstack1ll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ᱙")])
      accessibility_scripts.store()
      return bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"࠭ࡤࡢࡶࡤࠫᱚ")][bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᱛ")], bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᱜ")][bstack1ll_opy_ (u"ࠩ࡬ࡨࠬᱝ")]
    else:
      logger.error(bstack1ll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᱞ") + bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᱟ")])
      if bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᱠ")] == bstack1ll_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᱡ"):
        for bstack1111ll1ll1l_opy_ in bstack1111ll1ll11_opy_[bstack1ll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᱢ")]:
          logger.error(bstack1111ll1ll1l_opy_[bstack1ll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᱣ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᱤ") +  str(error))
    return None, None
def bstack1111l1l1ll1_opy_():
  if os.getenv(bstack1ll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᱥ")) is None:
    return {
        bstack1ll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᱦ"): bstack1ll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᱧ"),
        bstack1ll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᱨ"): bstack1ll_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᱩ")
    }
  data = {bstack1ll_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᱪ"): bstack11l1ll1ll_opy_()}
  headers = {
      bstack1ll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᱫ"): bstack1ll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᱬ") + os.getenv(bstack1ll_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᱭ")),
      bstack1ll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᱮ"): bstack1ll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᱯ")
  }
  response = bstack1l1111l111_opy_(bstack1ll_opy_ (u"ࠧࡑࡗࡗࠫᱰ"), bstack1111ll1llll_opy_ + bstack1ll_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᱱ"), data, { bstack1ll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᱲ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᱳ") + bstack1lll1l111l1_opy_().isoformat() + bstack1ll_opy_ (u"ࠫ࡟࠭ᱴ"))
      return {bstack1ll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᱵ"): bstack1ll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᱶ"), bstack1ll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᱷ"): bstack1ll_opy_ (u"ࠨࠩᱸ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᱹ") + str(error))
    return {
        bstack1ll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᱺ"): bstack1ll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᱻ"),
        bstack1ll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᱼ"): str(error)
    }
def bstack1111lll11l1_opy_(bstack1111l1llll1_opy_):
    return re.match(bstack1ll_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᱽ"), bstack1111l1llll1_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1111l1l1l1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1111l1l1l1l_opy_ = desired_capabilities
        else:
          bstack1111l1l1l1l_opy_ = {}
        bstack1l111l11ll1_opy_ = (bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭᱾"), bstack1ll_opy_ (u"ࠨࠩ᱿")).lower() or caps.get(bstack1ll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᲀ"), bstack1ll_opy_ (u"ࠪࠫᲁ")).lower())
        if bstack1l111l11ll1_opy_ == bstack1ll_opy_ (u"ࠫ࡮ࡵࡳࠨᲂ"):
            return True
        if bstack1l111l11ll1_opy_ == bstack1ll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᲃ"):
            bstack1111l1llll1_opy_ = caps.get(bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲄ")) or bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᲅ"), {}).get(bstack1ll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᲆ"), bstack1ll_opy_ (u"ࠩࠪᲇ"))
            if bstack1111l1llll1_opy_:
                try:
                    bstack1111lll1111_opy_ = int(str(bstack1111l1llll1_opy_).split(bstack1ll_opy_ (u"ࠪ࠲ࠬᲈ"))[0])
                    min_version = int(float(bstack1111l1l11ll_opy_))
                    if bstack1111lll1111_opy_ < min_version:
                        logger.warning(bstack1111ll1111l_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack1ll_opy_ (u"࡚ࠦࡴࡡࡣ࡮ࡨࠤࡹࡵࠠࡱࡣࡵࡷࡪࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡠࡸࡨࡶࡸ࡯࡯࡯ࠢࠪࠩࡸ࠭ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡵ࡮࠯ࠤᲉ"), bstack1111l1llll1_opy_)
            return True
        bstack1l11111l111_opy_ = caps.get(bstack1ll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᲊ"), {}).get(bstack1ll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ᲋"), caps.get(bstack1ll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ᲌"), bstack1ll_opy_ (u"ࠨࠩ᲍")))
        if bstack1l11111l111_opy_:
            logger.warning(bstack1ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ᲎"))
            return False
        browser = (caps.get(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᲏"), bstack1ll_opy_ (u"ࠫࠬᲐ")) or caps.get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࠭Ბ"), bstack1ll_opy_ (u"࠭ࠧᲒ"))).lower() or \
                  (bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᲓ"), bstack1ll_opy_ (u"ࠨࠩᲔ")) or bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪᲕ"), bstack1ll_opy_ (u"ࠪࠫᲖ"))).lower()
        if browser not in (bstack1ll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᲗ"), bstack1ll_opy_ (u"ࠬࡩࡨࡳࡱࡰ࡭ࡺࡳࠧᲘ"), bstack1ll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠰ࡧ࡭ࡸ࡯࡮࡫ࡸࡱࠬᲙ")):
            logger.warning(bstack1ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᲚ"))
            return False
        browser_version = caps.get(bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᲛ")) or caps.get(bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᲜ")) or bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᲝ")) or bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᲞ"), {}).get(bstack1ll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭Ჟ")) or bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᲠ"), {}).get(bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᲡ"))
        bstack1l111l1l1l1_opy_ = bstack1111llll111_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack1111lll1ll1_opy_ = False
        if config is not None:
          bstack1111lll1ll1_opy_ = bstack1ll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᲢ") in config and str(config[bstack1ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭Უ")]).lower() != bstack1ll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᲤ")
        if os.environ.get(bstack1ll_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᲥ"), bstack1ll_opy_ (u"ࠬ࠭Ღ")).lower() == bstack1ll_opy_ (u"࠭ࡴࡳࡷࡨࠫᲧ") or bstack1111lll1ll1_opy_:
          bstack1l111l1l1l1_opy_ = bstack1111llll111_opy_.bstack1l11111l11l_opy_
        if browser_version and browser_version != bstack1ll_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᲨ") and int(browser_version.split(bstack1ll_opy_ (u"ࠨ࠰ࠪᲩ"))[0]) <= bstack1l111l1l1l1_opy_:
          logger.warning(bstack1ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࠦᲪ") + str(bstack1l111l1l1l1_opy_) + bstack1ll_opy_ (u"ࠥ࠲ࠧᲫ"))
          return False
        bstack1l111l11lll_opy_ = (caps.get(bstack1ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᲬ"))
                         or bstack1111l1l1l1l_opy_.get(bstack1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᲭ"), {})
                         or caps.get(bstack1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭Ხ"), {}))
        bstack1ll1lll111l_opy_ = bstack1l111l11lll_opy_.get(bstack1ll_opy_ (u"ࠧࡢࡴࡪࡷࠬᲯ"), []) if isinstance(bstack1l111l11lll_opy_, dict) else []
        if not isinstance(bstack1ll1lll111l_opy_, list):
            bstack1ll1lll111l_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack1ll_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᲰ") or arg == bstack1ll_opy_ (u"ࠩ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᲱ") or (arg.startswith(bstack1ll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽ࠨᲲ")) and arg != bstack1ll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࡰࡨࡻࠬᲳ")))
               for arg in bstack1ll1lll111l_opy_):
            logger.warning(bstack1ll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᲴ"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack1ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᲵ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1l11ll1ll_opy_ = config.get(bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᲶ"), {})
    bstack1l1l11ll1ll_opy_[bstack1ll_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᲷ")] = os.getenv(bstack1ll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᲸ"))
    bstack111ll1ll1l_opy_ = json.loads(os.getenv(bstack1ll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᲹ"), bstack1ll_opy_ (u"ࠫࢀࢃࠧᲺ"))).get(bstack1ll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᲻"))
    if not config[bstack1ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ᲼")].get(bstack1ll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᲽ")):
      if bstack1ll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᲾ") in caps:
        caps[bstack1ll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᲿ")][bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᳀")] = bstack1l1l11ll1ll_opy_
        caps[bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᳁")][bstack1ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᳂")][bstack1ll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᳃")] = bstack111ll1ll1l_opy_
      else:
        caps[bstack1ll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᳄")] = bstack1l1l11ll1ll_opy_
        caps[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᳅")][bstack1ll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᳆")] = bstack111ll1ll1l_opy_
  except Exception as error:
    logger.debug(bstack1ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦ᳇") +  str(error))
def start_test_capture(driver, bstack1111ll1l1l1_opy_):
  try:
    setattr(driver, bstack1ll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ᳈"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack1ll_opy_ (u"ࠬࡌࡒࡂࡏࡈ࡛ࡔࡘࡋࡠࡗࡖࡉࡉ࠭᳉")) == bstack1ll_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠳ࡧࡦࡰࡨࡶ࡮ࡩࠧ᳊")):
        bstack1111l1ll11l_opy_ = bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᳋"), None)
        if bstack1111l1ll11l_opy_:
          if bstack1111ll1l1l1_opy_:
            logger.info(bstack1ll_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡶࡰࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮࠯࠰ࠥ᳌"))
          return bstack1111ll1l1l1_opy_
      bstack1111ll1l1ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111ll1l1ll_opy_ = False
      bstack1111ll1l1ll_opy_ = url.scheme in [bstack1ll_opy_ (u"ࠤ࡫ࡸࡹࡶࠢ᳍"), bstack1ll_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ᳎")]
      if bstack1111ll1l1ll_opy_:
        if bstack1111ll1l1l1_opy_:
          logger.info(bstack1ll_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦ᳏"))
      return bstack1111ll1l1l1_opy_
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ᳐") + str(e))
    return False
def bstack1111l111_opy_(driver, name, path):
  try:
    bstack1l1111lllll_opy_ = {
        bstack1ll_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭᳑"): threading.current_thread().current_test_uuid,
        bstack1ll_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᳒"): os.environ.get(bstack1ll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᳓"), bstack1ll_opy_ (u"᳔ࠩࠪ")),
        bstack1ll_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴ᳕ࠧ"): os.environ.get(bstack1ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ᳖"), bstack1ll_opy_ (u"᳗ࠬ࠭"))
    }
    bstack1lll1lll11_opy_ = bstack1l11ll1lll_opy_.bstack1111ll1111_opy_(EVENTS.bstack11l1ll1111_opy_.value)
    logger.debug(bstack1ll_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴ᳘ࠩ"))
    try:
      if (bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺ᳙ࠧ"), None) and bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᳚"), None)):
        scripts = {bstack1ll_opy_ (u"ࠩࡶࡧࡦࡴࠧ᳛"): accessibility_scripts.perform_scan}
        bstack1111l1ll1ll_opy_ = json.loads(scripts[bstack1ll_opy_ (u"ࠥࡷࡨࡧ࡮᳜ࠣ")].replace(bstack1ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿᳝ࠦࠢ"), bstack1ll_opy_ (u"ࠧࠨ᳞")))
        bstack1111l1ll1ll_opy_[bstack1ll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴ᳟ࠩ")][bstack1ll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ᳠")] = None
        scripts[bstack1ll_opy_ (u"ࠣࡵࡦࡥࡳࠨ᳡")] = bstack1ll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤ᳢ࠧ") + json.dumps(bstack1111l1ll1ll_opy_)
        accessibility_scripts.bstack11lll1l1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦ᳣ࠥ"): name}))
      bstack1l11ll1lll_opy_.end(EVENTS.bstack11l1ll1111_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷ᳤ࠦ"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠧࡀࡥ࡯ࡦ᳥ࠥ"), True, None)
    except Exception as error:
      bstack1l11ll1lll_opy_.end(EVENTS.bstack11l1ll1111_opy_.value, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᳦"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡧࡱࡨ᳧ࠧ"), False, str(error))
    bstack1lll1lll11_opy_ = bstack1l11ll1lll_opy_.bstack1111lll111l_opy_(EVENTS.bstack1l11111llll_opy_.value)
    bstack1l11ll1lll_opy_.mark(bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴ᳨ࠣ"))
    try:
      if (bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᳩ"), None) and bstack1llll1lll_opy_(threading.current_thread(), bstack1ll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᳪ"), None)):
        scripts = {bstack1ll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᳫ"): accessibility_scripts.perform_scan}
        bstack1111l1ll1ll_opy_ = json.loads(scripts[bstack1ll_opy_ (u"ࠧࡹࡣࡢࡰࠥᳬ")].replace(bstack1ll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᳭"), bstack1ll_opy_ (u"ࠢࠣᳮ")))
        bstack1111l1ll1ll_opy_[bstack1ll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᳯ")][bstack1ll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩᳰ")] = None
        scripts[bstack1ll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᳱ")] = bstack1ll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᳲ") + json.dumps(bstack1111l1ll1ll_opy_)
        accessibility_scripts.bstack11lll1l1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l1111lllll_opy_))
      bstack1l11ll1lll_opy_.end(bstack1lll1lll11_opy_, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᳳ"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᳴"),True, None)
    except Exception as error:
      bstack1l11ll1lll_opy_.end(bstack1lll1lll11_opy_, bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᳵ"), bstack1lll1lll11_opy_ + bstack1ll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᳶ"),False, str(error))
    logger.info(bstack1ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᳷"))
    try:
      bstack1l11111ll1l_opy_ = {
        bstack1ll_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ᳸"): {
          bstack1ll_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ᳹"): bstack1ll_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡆ࡜ࡅࡠࡔࡈࡗ࡚ࡒࡔࡔࠤᳺ"),
        },
        bstack1ll_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣ᳻"): {
          bstack1ll_opy_ (u"ࠢࡣࡱࡧࡽࠧ᳼"): {
            bstack1ll_opy_ (u"ࠣ࡯ࡶ࡫ࠧ᳽"): bstack1ll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᳾"),
            bstack1ll_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ᳿"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l11111ll1l_opy_, separators=(bstack1ll_opy_ (u"ࠫ࠱࠭ᴀ"), bstack1ll_opy_ (u"ࠬࡀࠧᴁ"))))
    except Exception as bstack11111111_opy_:
      logger.debug(bstack1ll_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡢࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡪࡡࡵࡣ࠽ࠤࠧᴂ") + str(bstack11111111_opy_) + bstack1ll_opy_ (u"ࠢࠣᴃ"))
  except Exception as bstack11llllll1ll_opy_:
    logger.error(bstack1ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥᴄ") + str(path) + bstack1ll_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦᴅ") + str(bstack11llllll1ll_opy_))
def bstack1111l1ll1l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᴆ")) and str(caps.get(bstack1ll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᴇ"))).lower() == bstack1ll_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨᴈ"):
        bstack1l111111l11_opy_ = caps.get(bstack1ll_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᴉ")) or caps.get(bstack1ll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᴊ"))
        if bstack1l111111l11_opy_:
            try:
              bstack1111l1llll1_opy_ = str(bstack1l111111l11_opy_).split(bstack1ll_opy_ (u"ࠨ࠰ࠪᴋ"))[0]
              min_version = int(float(bstack1111l1l11ll_opy_))
              if int(bstack1111l1llll1_opy_) < min_version:
                  logger.warning(bstack1111ll1111l_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack1ll_opy_ (u"ࠤࡘࡲࡦࡨ࡬ࡦࠢࡷࡳࠥࡶࡡࡳࡵࡨࠤࡵࡲࡡࡵࡨࡲࡶࡲࡥࡶࡦࡴࡶ࡭ࡴࡴࠠࠨࠧࡶࠫࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡳࡳ࠴ࠢᴌ"), bstack1l111111l11_opy_)
    return True
def bstack1l111l111l_opy_(config):
  if bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴍ") in config:
        return config[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴎ")]
  for platform in config.get(bstack1ll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᴏ"), []):
      if bstack1ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴐ") in platform:
          return platform[bstack1ll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᴑ")]
  return None
def bstack11ll11ll1_opy_(bstack11ll1l11l_opy_):
  try:
    browser_name = bstack11ll1l11l_opy_[bstack1ll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᴒ")]
    browser_version = bstack11ll1l11l_opy_[bstack1ll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᴓ")]
    chrome_options = bstack11ll1l11l_opy_[bstack1ll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫᴔ")]
    try:
        bstack1111l1l11l1_opy_ = int(browser_version.split(bstack1ll_opy_ (u"ࠫ࠳࠭ᴕ"))[0])
    except ValueError as e:
        logger.error(bstack1ll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡴࡶࡦࡴࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠤᴖ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1ll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᴗ")):
        logger.warning(bstack1ll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᴘ"))
        return False
    if bstack1111l1l11l1_opy_ < bstack1111llll111_opy_.bstack1l11111l11l_opy_:
        logger.warning(bstack1ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷ࡬ࡶࡪࡹࠠࡄࡪࡵࡳࡲ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠤᴙ") + str(bstack1111llll111_opy_.bstack1l11111l11l_opy_) + bstack1ll_opy_ (u"ࠤࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠢᴚ"))
        return False
    bstack1ll1lll111l_opy_ = chrome_options.get(bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᴛ"), []) if chrome_options else []
    if not isinstance(bstack1ll1lll111l_opy_, list):
        bstack1ll1lll111l_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack1ll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᴜ") or arg == bstack1ll_opy_ (u"ࠬ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᴝ") or (arg.startswith(bstack1ll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࠫᴞ")) and arg != bstack1ll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨᴟ")))
           for arg in bstack1ll1lll111l_opy_):
        logger.warning(bstack1ll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᴠ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1ll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡩࡳࡷࠦ࡬ࡰࡥࡤࡰࠥࡉࡨࡳࡱࡰࡩ࠿ࠦࠢᴡ") + str(e))
    return False
def bstack1l1ll11ll1_opy_(bstack11l1lll1ll_opy_, config):
    try:
      bstack1l111l1l111_opy_ = bstack1ll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴢ") in config and config[bstack1ll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᴣ")] == True
      bstack1111lll1ll1_opy_ = bstack1ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᴤ") in config and str(config[bstack1ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᴥ")]).lower() != bstack1ll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᴦ")
      if not (bstack1l111l1l111_opy_ and (not bstack1lll1111ll_opy_(config) or bstack1111lll1ll1_opy_)):
        return bstack11l1lll1ll_opy_
      bstack1111l1lllll_opy_ = accessibility_scripts.bstack1111ll11l11_opy_
      if bstack1111l1lllll_opy_ is None:
        logger.debug(bstack1ll_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶࡪࠦࡎࡰࡰࡨࠦᴧ"))
        return bstack11l1lll1ll_opy_
      bstack1111lll11ll_opy_ = int(str(bstack1111l1l1lll_opy_()).split(bstack1ll_opy_ (u"ࠩ࠱ࠫᴨ"))[0])
      logger.debug(bstack1ll_opy_ (u"ࠥࡗࡪࡲࡥ࡯࡫ࡸࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࠥᴩ") + str(bstack1111lll11ll_opy_) + bstack1ll_opy_ (u"ࠦࠧᴪ"))
      if bstack1111lll11ll_opy_ == 3 and isinstance(bstack11l1lll1ll_opy_, dict) and bstack1ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᴫ") in bstack11l1lll1ll_opy_ and bstack1111l1lllll_opy_ is not None:
        if bstack1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᴬ") not in bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᴭ")]:
          bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᴮ")][bstack1ll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᴯ")] = {}
        if bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᴰ") in bstack1111l1lllll_opy_:
          if bstack1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩᴱ") not in bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᴲ")][bstack1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᴳ")]:
            bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᴴ")][bstack1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴵ")][bstack1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᴶ")] = []
          for arg in bstack1111l1lllll_opy_[bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᴷ")]:
            if arg not in bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᴸ")][bstack1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᴹ")][bstack1ll_opy_ (u"࠭ࡡࡳࡩࡶࠫᴺ")]:
              bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᴻ")][bstack1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᴼ")][bstack1ll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᴽ")].append(arg)
        if bstack1ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᴾ") in bstack1111l1lllll_opy_:
          if bstack1ll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᴿ") not in bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵀ")][bstack1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᵁ")]:
            bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵂ")][bstack1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵃ")][bstack1ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵄ")] = []
          for ext in bstack1111l1lllll_opy_[bstack1ll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵅ")]:
            if ext not in bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵆ")][bstack1ll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵇ")][bstack1ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵈ")]:
              bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵉ")][bstack1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵊ")][bstack1ll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵋ")].append(ext)
        if bstack1ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᵌ") in bstack1111l1lllll_opy_:
          if bstack1ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᵍ") not in bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᵎ")][bstack1ll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᵏ")]:
            bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵐ")][bstack1ll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵑ")][bstack1ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵒ")] = {}
          bstack1111l1lll11_opy_(bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵓ")][bstack1ll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵔ")][bstack1ll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵕ")],
                    bstack1111l1lllll_opy_[bstack1ll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᵖ")])
        os.environ[bstack1ll_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᵗ")] = bstack1ll_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᵘ")
        return bstack11l1lll1ll_opy_
      else:
        chrome_options = None
        if isinstance(bstack11l1lll1ll_opy_, ChromeOptions):
          chrome_options = bstack11l1lll1ll_opy_
        elif isinstance(bstack11l1lll1ll_opy_, dict):
          for value in bstack11l1lll1ll_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11l1lll1ll_opy_, dict):
            bstack11l1lll1ll_opy_[bstack1ll_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᵙ")] = chrome_options
          else:
            bstack11l1lll1ll_opy_ = chrome_options
        if bstack1111l1lllll_opy_ is not None:
          if bstack1ll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᵚ") in bstack1111l1lllll_opy_:
                bstack1111lll1lll_opy_ = chrome_options.arguments or []
                new_args = bstack1111l1lllll_opy_[bstack1ll_opy_ (u"ࠫࡦࡸࡧࡴࠩᵛ")]
                for arg in new_args:
                    if arg not in bstack1111lll1lll_opy_:
                        chrome_options.add_argument(arg)
          if bstack1ll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᵜ") in bstack1111l1lllll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1ll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵝ"), [])
                bstack1111ll11lll_opy_ = bstack1111l1lllll_opy_[bstack1ll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᵞ")]
                for extension in bstack1111ll11lll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1ll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵟ") in bstack1111l1lllll_opy_:
                bstack1111ll111l1_opy_ = chrome_options.experimental_options.get(bstack1ll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵠ"), {})
                bstack1111llll11l_opy_ = bstack1111l1lllll_opy_[bstack1ll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᵡ")]
                bstack1111l1lll11_opy_(bstack1111ll111l1_opy_, bstack1111llll11l_opy_)
                chrome_options.add_experimental_option(bstack1ll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᵢ"), bstack1111ll111l1_opy_)
        os.environ[bstack1ll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᵣ")] = bstack1ll_opy_ (u"࠭ࡴࡳࡷࡨࠫᵤ")
        return bstack11l1lll1ll_opy_
    except Exception as e:
      logger.error(bstack1ll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡴ࡯࡯࠯ࡅࡗࠥ࡯࡮ࡧࡴࡤࠤࡦ࠷࠱ࡺࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧᵥ") + str(e))
      return bstack11l1lll1ll_opy_