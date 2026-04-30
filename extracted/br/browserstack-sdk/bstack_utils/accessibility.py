# coding: UTF-8
import sys
bstack1l11ll1_opy_ = sys.version_info [0] == 2
bstack1lll1l1_opy_ = 2048
bstack11lllll_opy_ = 7
def bstack1l1111l_opy_ (bstack1llllll1_opy_):
    global bstack1ll111_opy_
    bstack11l1l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack11l11l_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1ll11_opy_ = bstack11l1l_opy_ % len (bstack11l11l_opy_)
    bstack11ll1_opy_ = bstack11l11l_opy_ [:bstack1ll11_opy_] + bstack11l11l_opy_ [bstack1ll11_opy_:]
    if bstack1l11ll1_opy_:
        bstack11l1l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack11l1l11_opy_ = str () .join ([chr (ord (char) - bstack1lll1l1_opy_ - (bstack111l1_opy_ + bstack11l1l_opy_) % bstack11lllll_opy_) for bstack111l1_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack11l1l11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1111l1ll1ll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1111l1l1ll1_opy_ as bstack1111l1l111l_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import bstack1l111l1ll_opy_, bstack1lll11ll1ll_opy_, bstack11lllllll_opy_, bstack1111l1lll11_opy_, \
  bstack1111ll11lll_opy_, bstack1ll1lll1ll_opy_, get_host_info, bstack1111l1l1lll_opy_, bstack11ll111l1l_opy_, error_handler, bstack1111l1ll1l1_opy_, bstack1111l1llll1_opy_, bstack11l11l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11l11lll_opy_ import bstack11lll1111_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack11l11lll_opy_ = bstack11lll1111_opy_()
@error_handler(class_method=False)
def _1111l1l11ll_opy_(driver, bstack1ll11l1ll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1111l_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩᰫ"): caps.get(bstack1l1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᰬ"), None),
        bstack1l1111l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᰭ"): bstack1ll11l1ll11_opy_.get(bstack1l1111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᰮ"), None),
        bstack1l1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᰯ"): caps.get(bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᰰ"), None),
        bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᰱ"): caps.get(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᰲ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᰳ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᰴ"), None) is None or os.environ[bstack1l1111l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᰵ")] == bstack1l1111l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᰶ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ᰷࠭"), False) or any([p.get(bstack1l1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᰸"), False) == True for p in config.get(bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᰹"), [])])
def is_enabled_platform(config, bstack11l1lllll1_opy_):
  try:
    bstack1ll1l1l11ll_opy_ = config.get(bstack1l1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᰺"), False)
    _1lll111l1l1_opy_ = int(bstack11l1lllll1_opy_)
    if _1lll111l1l1_opy_ < 0:
      _1lll111l1l1_opy_ = 0
    bstack1llll11l11_opy_ = config.get(bstack1l1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᰻"), [])
    if _1lll111l1l1_opy_ < len(bstack1llll11l11_opy_) and bstack1llll11l11_opy_[_1lll111l1l1_opy_]:
      bstack1111ll111ll_opy_ = bstack1llll11l11_opy_[_1lll111l1l1_opy_].get(bstack1l1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᰼"), None)
    else:
      bstack1111ll111ll_opy_ = config.get(bstack1l1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᰽"), None)
    if bstack1111ll111ll_opy_ != None:
      bstack1ll1l1l11ll_opy_ = bstack1111ll111ll_opy_
    bstack1111lll11l1_opy_ = os.getenv(bstack1l1111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᰾")) is not None and len(os.getenv(bstack1l1111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᰿"))) > 0 and os.getenv(bstack1l1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᱀")) != bstack1l1111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ᱁")
    return bstack1ll1l1l11ll_opy_ and bstack1111lll11l1_opy_
  except Exception as error:
    logger.debug(bstack1l1111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪ᱂") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l111l1lll1_opy_ = os.getenv(bstack1l1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᱃"))
  if bstack1l111l1lll1_opy_ is None:
    return True
  bstack1l111l1lll1_opy_ = json.loads(bstack1l111l1lll1_opy_)
  try:
    include_tags = bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ᱄")] if bstack1l1111l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᱅") in bstack1l111l1lll1_opy_ and isinstance(bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᱆")], list) else []
    exclude_tags = bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᱇")] if bstack1l1111l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᱈") in bstack1l111l1lll1_opy_ and isinstance(bstack1l111l1lll1_opy_[bstack1l1111l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᱉")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦ᱊") + str(error))
  return False
def bstack1111ll1l1ll_opy_(config, bstack1111ll1lll1_opy_, bstack1111l1l1111_opy_, bstack1111ll1ll1l_opy_):
  bstack1111lll11ll_opy_ = bstack1111l1lll11_opy_(config)
  bstack1111ll11ll1_opy_ = bstack1111ll11lll_opy_(config)
  if bstack1111lll11ll_opy_ is None or bstack1111ll11ll1_opy_ is None:
    logger.error(bstack1l1111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭᱋"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ᱌"), bstack1l1111l_opy_ (u"ࠧࡼࡿࠪᱍ")))
    data = {
        bstack1l1111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᱎ"): config[bstack1l1111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᱏ")],
        bstack1l1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᱐"): config.get(bstack1l1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᱑"), os.path.basename(os.getcwd())),
        bstack1l1111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨ᱒"): bstack1l111l1ll_opy_(),
        bstack1l1111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᱓"): config.get(bstack1l1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᱔"), bstack1l1111l_opy_ (u"ࠨࠩ᱕")),
        bstack1l1111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ᱖"): {
            bstack1l1111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ᱗"): bstack1111ll1lll1_opy_,
            bstack1l1111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᱘"): bstack1111l1l1111_opy_,
            bstack1l1111l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ᱙"): __version__,
            bstack1l1111l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᱚ"): bstack1l1111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᱛ"),
            bstack1l1111l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᱜ"): bstack1l1111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᱝ"),
            bstack1l1111l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᱞ"): bstack1111ll1ll1l_opy_
        },
        bstack1l1111l_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᱟ"): settings,
        bstack1l1111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭ᱠ"): bstack1111l1l1lll_opy_(),
        bstack1l1111l_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭ᱡ"): bstack1ll1lll1ll_opy_(),
        bstack1l1111l_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩᱢ"): get_host_info(),
        bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᱣ"): bstack11lllllll_opy_(config)
    }
    headers = {
        bstack1l1111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᱤ"): bstack1l1111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᱥ"),
    }
    config = {
        bstack1l1111l_opy_ (u"ࠫࡦࡻࡴࡩࠩᱦ"): (bstack1111lll11ll_opy_, bstack1111ll11ll1_opy_),
        bstack1l1111l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᱧ"): headers
    }
    response = bstack11ll111l1l_opy_(bstack1l1111l_opy_ (u"࠭ࡐࡐࡕࡗࠫᱨ"), bstack1111l1l111l_opy_ + bstack1l1111l_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧᱩ"), data, config)
    bstack1111ll1l111_opy_ = response.json()
    if bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᱪ")]:
      parsed = json.loads(os.getenv(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᱫ"), bstack1l1111l_opy_ (u"ࠪࡿࢂ࠭ᱬ")))
      parsed[bstack1l1111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᱭ")] = bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠬࡪࡡࡵࡣࠪᱮ")][bstack1l1111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᱯ")]
      os.environ[bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᱰ")] = json.dumps(parsed)
      accessibility_scripts.bstack1l111l1l11_opy_(bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᱱ")][bstack1l1111l_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᱲ")])
      accessibility_scripts.bstack1l11ll1lll1_opy_(bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠪࡨࡦࡺࡡࠨᱳ")][bstack1l1111l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᱴ")])
      accessibility_scripts.store()
      return bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠬࡪࡡࡵࡣࠪᱵ")][bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫᱶ")], bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠧࡥࡣࡷࡥࠬᱷ")][bstack1l1111l_opy_ (u"ࠨ࡫ࡧࠫᱸ")]
    else:
      logger.error(bstack1l1111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪᱹ") + bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᱺ")])
      if bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᱻ")] == bstack1l1111l_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧᱼ"):
        for bstack1111lll1111_opy_ in bstack1111ll1l111_opy_[bstack1l1111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᱽ")]:
          logger.error(bstack1111lll1111_opy_[bstack1l1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᱾")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤ᱿") +  str(error))
    return None, None
def bstack1111l1ll111_opy_():
  if os.getenv(bstack1l1111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᲀ")) is None:
    return {
        bstack1l1111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᲁ"): bstack1l1111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᲂ"),
        bstack1l1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᲃ"): bstack1l1111l_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬᲄ")
    }
  data = {bstack1l1111l_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨᲅ"): bstack1l111l1ll_opy_()}
  headers = {
      bstack1l1111l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᲆ"): bstack1l1111l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪᲇ") + os.getenv(bstack1l1111l_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣᲈ")),
      bstack1l1111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᲉ"): bstack1l1111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᲊ")
  }
  response = bstack11ll111l1l_opy_(bstack1l1111l_opy_ (u"࠭ࡐࡖࡖࠪ᲋"), bstack1111l1l111l_opy_ + bstack1l1111l_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩ᲌"), data, { bstack1l1111l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩ᲍"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1111l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥ᲎") + bstack1lll11ll1ll_opy_().isoformat() + bstack1l1111l_opy_ (u"ࠪ࡞ࠬ᲏"))
      return {bstack1l1111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᲐ"): bstack1l1111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭Ბ"), bstack1l1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᲒ"): bstack1l1111l_opy_ (u"ࠧࠨᲓ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦᲔ") + str(error))
    return {
        bstack1l1111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᲕ"): bstack1l1111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᲖ"),
        bstack1l1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᲗ"): str(error)
    }
def bstack1111l1l1l1l_opy_(bstack1111ll1l1l1_opy_):
    return re.match(bstack1l1111l_opy_ (u"ࡷ࠭࡞࡝ࡦ࠮ࠬࡡ࠴࡜ࡥ࠭ࠬࡃࠩ࠭Ი"), bstack1111ll1l1l1_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1111ll1ll11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1111ll1ll11_opy_ = desired_capabilities
        else:
          bstack1111ll1ll11_opy_ = {}
        bstack1l1111l11ll_opy_ = (bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᲙ"), bstack1l1111l_opy_ (u"ࠧࠨᲚ")).lower() or caps.get(bstack1l1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᲛ"), bstack1l1111l_opy_ (u"ࠩࠪᲜ")).lower())
        if bstack1l1111l11ll_opy_ == bstack1l1111l_opy_ (u"ࠪ࡭ࡴࡹࠧᲝ"):
            return True
        if bstack1l1111l11ll_opy_ == bstack1l1111l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᲞ"):
            bstack1111ll1l1l1_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᲟ")) or bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᲠ"), {}).get(bstack1l1111l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᲡ"), bstack1l1111l_opy_ (u"ࠨࠩᲢ"))
            if bstack1111ll1l1l1_opy_:
                try:
                    bstack1111ll111l1_opy_ = int(str(bstack1111ll1l1l1_opy_).split(bstack1l1111l_opy_ (u"ࠩ࠱ࠫᲣ"))[0])
                    min_version = int(float(bstack1111lll1l1l_opy_))
                    if bstack1111ll111l1_opy_ < min_version:
                        logger.warning(bstack1111ll1l11l_opy_ % str(min_version))
                        return False
                except (ValueError, TypeError):
                    logger.warning(bstack1l1111l_opy_ (u"࡙ࠥࡳࡧࡢ࡭ࡧࠣࡸࡴࠦࡰࡢࡴࡶࡩࠥࡶ࡬ࡢࡶࡩࡳࡷࡳ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠡࠩࠨࡷࠬࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡴࡴ࠮ࠣᲤ"), bstack1111ll1l1l1_opy_)
            return True
        bstack1l111ll1111_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᲥ"), {}).get(bstack1l1111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᲦ"), caps.get(bstack1l1111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭Ყ"), bstack1l1111l_opy_ (u"ࠧࠨᲨ")))
        if bstack1l111ll1111_opy_:
            logger.warning(bstack1l1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᲩ"))
            return False
        browser = (caps.get(bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᲪ"), bstack1l1111l_opy_ (u"ࠪࠫᲫ")) or caps.get(bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᲬ"), bstack1l1111l_opy_ (u"ࠬ࠭Ჭ"))).lower() or \
                  (bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᲮ"), bstack1l1111l_opy_ (u"ࠧࠨᲯ")) or bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᲰ"), bstack1l1111l_opy_ (u"ࠩࠪᲱ"))).lower()
        if browser not in (bstack1l1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᲲ"), bstack1l1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭Ჳ"), bstack1l1111l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠯ࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫᲴ")):
            logger.warning(bstack1l1111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᲵ"))
            return False
        browser_version = caps.get(bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᲶ")) or caps.get(bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᲷ")) or bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᲸ")) or bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᲹ"), {}).get(bstack1l1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᲺ")) or bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᲻"), {}).get(bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᲼"))
        bstack1l11111lll1_opy_ = bstack1111l1ll1ll_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack1111ll1llll_opy_ = False
        if config is not None:
          bstack1111ll1llll_opy_ = bstack1l1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᲽ") in config and str(config[bstack1l1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᲾ")]).lower() != bstack1l1111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᲿ")
        if os.environ.get(bstack1l1111l_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨ᳀"), bstack1l1111l_opy_ (u"ࠫࠬ᳁")).lower() == bstack1l1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪ᳂") or bstack1111ll1llll_opy_:
          bstack1l11111lll1_opy_ = bstack1111l1ll1ll_opy_.bstack1l1111l1lll_opy_
        if browser_version and browser_version != bstack1l1111l_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭᳃") and int(browser_version.split(bstack1l1111l_opy_ (u"ࠧ࠯ࠩ᳄"))[0]) <= bstack1l11111lll1_opy_:
          logger.warning(bstack1l1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࠥ᳅") + str(bstack1l11111lll1_opy_) + bstack1l1111l_opy_ (u"ࠤ࠱ࠦ᳆"))
          return False
        bstack11llllll1l1_opy_ = (caps.get(bstack1l1111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᳇"))
                         or bstack1111ll1ll11_opy_.get(bstack1l1111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳈"), {})
                         or caps.get(bstack1l1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᳉"), {}))
        bstack1lll11111ll_opy_ = bstack11llllll1l1_opy_.get(bstack1l1111l_opy_ (u"࠭ࡡࡳࡩࡶࠫ᳊"), []) if isinstance(bstack11llllll1l1_opy_, dict) else []
        if not isinstance(bstack1lll11111ll_opy_, list):
            bstack1lll11111ll_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack1l1111l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫ᳋") or arg == bstack1l1111l_opy_ (u"ࠨࡪࡨࡥࡩࡲࡥࡴࡵࠪ᳌") or (arg.startswith(bstack1l1111l_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧ᳍")) and arg != bstack1l1111l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫ᳎")))
               for arg in bstack1lll11111ll_opy_):
            logger.warning(bstack1l1111l_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨ᳏"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack1l1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢ᳐") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l11l11l1ll_opy_ = config.get(bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᳑"), {})
    bstack1l11l11l1ll_opy_[bstack1l1111l_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ᳒")] = os.getenv(bstack1l1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᳓"))
    bstack1l1l1l1l11_opy_ = json.loads(os.getenv(bstack1l1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎ᳔ࠪ"), bstack1l1111l_opy_ (u"ࠪࡿࢂ᳕࠭"))).get(bstack1l1111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ᳖ࠬ"))
    if not config[bstack1l1111l_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶ᳗ࠧ")].get(bstack1l1111l_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩ᳘ࠧ")):
      if bstack1l1111l_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᳙") in caps:
        caps[bstack1l1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᳚")][bstack1l1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᳛")] = bstack1l11l11l1ll_opy_
        caps[bstack1l1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶ᳜ࠫ")][bstack1l1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶ᳝ࠫ")][bstack1l1111l_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ᳞࠭")] = bstack1l1l1l1l11_opy_
      else:
        caps[bstack1l1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ᳟ࠬ")] = bstack1l11l11l1ll_opy_
        caps[bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᳠")][bstack1l1111l_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᳡")] = bstack1l1l1l1l11_opy_
  except Exception as error:
    logger.debug(bstack1l1111l_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻᳢ࠢࠥ") +  str(error))
def start_test_capture(driver, bstack1111ll11l1l_opy_):
  try:
    setattr(driver, bstack1l1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰ᳣ࠪ"), True)
    session = driver.session_id
    if session:
      if(os.environ.get(bstack1l1111l_opy_ (u"ࠫࡋࡘࡁࡎࡇ࡚ࡓࡗࡑ࡟ࡖࡕࡈࡈ᳤ࠬ")) == bstack1l1111l_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲ࠲࡭ࡥ࡯ࡧࡵ࡭ࡨ᳥࠭")):
        bstack1111l1l1l11_opy_ = bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᳦"), None)
        if bstack1111l1l1l11_opy_:
          if bstack1111ll11l1l_opy_:
            logger.info(bstack1l1111l_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡵࡶࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴࠮࠯ࠤ᳧"))
          return bstack1111ll11l1l_opy_
      bstack1111l1l11l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1111l1l11l1_opy_ = False
      bstack1111l1l11l1_opy_ = url.scheme in [bstack1l1111l_opy_ (u"ࠣࡪࡷࡸࡵࠨ᳨"), bstack1l1111l_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᳩ")]
      if bstack1111l1l11l1_opy_:
        if bstack1111ll11l1l_opy_:
          logger.info(bstack1l1111l_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥᳪ"))
      return bstack1111ll11l1l_opy_
  except Exception as e:
    logger.error(bstack1l1111l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᳫ") + str(e))
    return False
def bstack1l11llll11_opy_(driver, name, path):
  try:
    bstack1l111l1l1ll_opy_ = {
        bstack1l1111l_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᳬ"): threading.current_thread().current_test_uuid,
        bstack1l1111l_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧ᳭ࠫ"): os.environ.get(bstack1l1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᳮ"), bstack1l1111l_opy_ (u"ࠨࠩᳯ")),
        bstack1l1111l_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ᳰ"): os.environ.get(bstack1l1111l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᳱ"), bstack1l1111l_opy_ (u"ࠫࠬᳲ"))
    }
    bstack1l11l1l11_opy_ = bstack11l11lll_opy_.bstack1l11l1ll_opy_(EVENTS.bstack11lllll1_opy_.value)
    logger.debug(bstack1l1111l_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᳳ"))
    try:
      if (bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᳴"), None) and bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᳵ"), None)):
        scripts = {bstack1l1111l_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᳶ"): accessibility_scripts.perform_scan}
        bstack1111lll1l11_opy_ = json.loads(scripts[bstack1l1111l_opy_ (u"ࠤࡶࡧࡦࡴࠢ᳷")].replace(bstack1l1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨ᳸"), bstack1l1111l_opy_ (u"ࠦࠧ᳹")))
        bstack1111lll1l11_opy_[bstack1l1111l_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᳺ")][bstack1l1111l_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭᳻")] = None
        scripts[bstack1l1111l_opy_ (u"ࠢࡴࡥࡤࡲࠧ᳼")] = bstack1l1111l_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᳽") + json.dumps(bstack1111lll1l11_opy_)
        accessibility_scripts.bstack1l111l1l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1l1111l_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ᳾"): name}))
      bstack11l11lll_opy_.end(EVENTS.bstack11lllll1_opy_.value, bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᳿"), bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᴀ"), True, None)
    except Exception as error:
      bstack11l11lll_opy_.end(EVENTS.bstack11lllll1_opy_.value, bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᴁ"), bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᴂ"), False, str(error))
    bstack1l11l1l11_opy_ = bstack11l11lll_opy_.bstack1111lll111l_opy_(EVENTS.bstack1l1111llll1_opy_.value)
    bstack11l11lll_opy_.mark(bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᴃ"))
    try:
      if (bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᴄ"), None) and bstack11l11l11_opy_(threading.current_thread(), bstack1l1111l_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᴅ"), None)):
        scripts = {bstack1l1111l_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᴆ"): accessibility_scripts.perform_scan}
        bstack1111lll1l11_opy_ = json.loads(scripts[bstack1l1111l_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᴇ")].replace(bstack1l1111l_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᴈ"), bstack1l1111l_opy_ (u"ࠨࠢᴉ")))
        bstack1111lll1l11_opy_[bstack1l1111l_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᴊ")][bstack1l1111l_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᴋ")] = None
        scripts[bstack1l1111l_opy_ (u"ࠤࡶࡧࡦࡴࠢᴌ")] = bstack1l1111l_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᴍ") + json.dumps(bstack1111lll1l11_opy_)
        accessibility_scripts.bstack1l111l1l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l111l1l1ll_opy_))
      bstack11l11lll_opy_.end(bstack1l11l1l11_opy_, bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᴎ"), bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᴏ"),True, None)
    except Exception as error:
      bstack11l11lll_opy_.end(bstack1l11l1l11_opy_, bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᴐ"), bstack1l11l1l11_opy_ + bstack1l1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᴑ"),False, str(error))
    logger.info(bstack1l1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᴒ"))
    try:
      bstack1l111l11ll1_opy_ = {
        bstack1l1111l_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥᴓ"): {
          bstack1l1111l_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᴔ"): bstack1l1111l_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣᴕ"),
        },
        bstack1l1111l_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᴖ"): {
          bstack1l1111l_opy_ (u"ࠨࡢࡰࡦࡼࠦᴗ"): {
            bstack1l1111l_opy_ (u"ࠢ࡮ࡵࡪࠦᴘ"): bstack1l1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᴙ"),
            bstack1l1111l_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᴚ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l111l11ll1_opy_, separators=(bstack1l1111l_opy_ (u"ࠪ࠰ࠬᴛ"), bstack1l1111l_opy_ (u"ࠫ࠿࠭ᴜ"))))
    except Exception as bstack11l111ll11_opy_:
      logger.debug(bstack1l1111l_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦᴝ") + str(bstack11l111ll11_opy_) + bstack1l1111l_opy_ (u"ࠨࠢᴞ"))
  except Exception as bstack1l111l11111_opy_:
    logger.error(bstack1l1111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᴟ") + str(path) + bstack1l1111l_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᴠ") + str(bstack1l111l11111_opy_))
def bstack1111ll1111l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1111l_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᴡ")) and str(caps.get(bstack1l1111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᴢ"))).lower() == bstack1l1111l_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᴣ"):
        bstack1l1111l1l11_opy_ = caps.get(bstack1l1111l_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᴤ")) or caps.get(bstack1l1111l_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᴥ"))
        if bstack1l1111l1l11_opy_:
            try:
              bstack1111ll1l1l1_opy_ = str(bstack1l1111l1l11_opy_).split(bstack1l1111l_opy_ (u"ࠧ࠯ࠩᴦ"))[0]
              min_version = int(float(bstack1111lll1l1l_opy_))
              if int(bstack1111ll1l1l1_opy_) < min_version:
                  logger.warning(bstack1111ll1l11l_opy_ % str(min_version))
                  return False
            except (ValueError, TypeError):
                logger.warning(bstack1l1111l_opy_ (u"ࠣࡗࡱࡥࡧࡲࡥࠡࡶࡲࠤࡵࡧࡲࡴࡧࠣࡴࡱࡧࡴࡧࡱࡵࡱࡤࡼࡥࡳࡵ࡬ࡳࡳࠦࠧࠦࡵࠪࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡲࡲ࠳ࠨᴧ"), bstack1l1111l1l11_opy_)
    return True
def bstack1lll11l11l_opy_(config):
  if bstack1l1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴨ") in config:
        return config[bstack1l1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴩ")]
  for platform in config.get(bstack1l1111l_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᴪ"), []):
      if bstack1l1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᴫ") in platform:
          return platform[bstack1l1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᴬ")]
  return None
def bstack111llll1ll_opy_(bstack111ll1l111_opy_):
  try:
    browser_name = bstack111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᴭ")]
    browser_version = bstack111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᴮ")]
    chrome_options = bstack111ll1l111_opy_[bstack1l1111l_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪᴯ")]
    try:
        bstack1111ll11l11_opy_ = int(browser_version.split(bstack1l1111l_opy_ (u"ࠪ࠲ࠬᴰ"))[0])
    except ValueError as e:
        logger.error(bstack1l1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡳࡼࡥࡳࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠣᴱ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l1111l_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᴲ")):
        logger.warning(bstack1l1111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᴳ"))
        return False
    if bstack1111ll11l11_opy_ < bstack1111l1ll1ll_opy_.bstack1l1111l1lll_opy_:
        logger.warning(bstack1l1111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡸࠦࡃࡩࡴࡲࡱࡪࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࠣᴴ") + str(bstack1111l1ll1ll_opy_.bstack1l1111l1lll_opy_) + bstack1l1111l_opy_ (u"ࠣࠢࡲࡶࠥ࡮ࡩࡨࡪࡨࡶ࠳ࠨᴵ"))
        return False
    bstack1lll11111ll_opy_ = chrome_options.get(bstack1l1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᴶ"), []) if chrome_options else []
    if not isinstance(bstack1lll11111ll_opy_, list):
        bstack1lll11111ll_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack1l1111l_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᴷ") or arg == bstack1l1111l_opy_ (u"ࠫ࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᴸ") or (arg.startswith(bstack1l1111l_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࠪᴹ")) and arg != bstack1l1111l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࡲࡪࡽࠧᴺ")))
           for arg in bstack1lll11111ll_opy_):
        logger.warning(bstack1l1111l_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᴻ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l1111l_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨᴼ") + str(e))
    return False
def bstack1lll111l_opy_(bstack1l1l1ll111_opy_, config):
    try:
      bstack1l111l1111l_opy_ = bstack1l1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᴽ") in config and config[bstack1l1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᴾ")] == True
      bstack1111ll1llll_opy_ = bstack1l1111l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᴿ") in config and str(config[bstack1l1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᵀ")]).lower() != bstack1l1111l_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᵁ")
      if not (bstack1l111l1111l_opy_ and (not bstack11lllllll_opy_(config) or bstack1111ll1llll_opy_)):
        return bstack1l1l1ll111_opy_
      bstack1111l1ll11l_opy_ = accessibility_scripts.bstack1111l1lllll_opy_
      if bstack1111l1ll11l_opy_ is None:
        logger.debug(bstack1l1111l_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥᵂ"))
        return bstack1l1l1ll111_opy_
      bstack1111l11llll_opy_ = int(str(bstack1111l1llll1_opy_()).split(bstack1l1111l_opy_ (u"ࠨ࠰ࠪᵃ"))[0])
      logger.debug(bstack1l1111l_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤᵄ") + str(bstack1111l11llll_opy_) + bstack1l1111l_opy_ (u"ࠥࠦᵅ"))
      if bstack1111l11llll_opy_ == 3 and isinstance(bstack1l1l1ll111_opy_, dict) and bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵆ") in bstack1l1l1ll111_opy_ and bstack1111l1ll11l_opy_ is not None:
        if bstack1l1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵇ") not in bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵈ")]:
          bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᵉ")][bstack1l1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᵊ")] = {}
        if bstack1l1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᵋ") in bstack1111l1ll11l_opy_:
          if bstack1l1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᵌ") not in bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵍ")][bstack1l1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵎ")]:
            bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵏ")][bstack1l1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵐ")][bstack1l1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵑ")] = []
          for arg in bstack1111l1ll11l_opy_[bstack1l1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᵒ")]:
            if arg not in bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵓ")][bstack1l1111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵔ")][bstack1l1111l_opy_ (u"ࠬࡧࡲࡨࡵࠪᵕ")]:
              bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵖ")][bstack1l1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵗ")][bstack1l1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᵘ")].append(arg)
        if bstack1l1111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵙ") in bstack1111l1ll11l_opy_:
          if bstack1l1111l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᵚ") not in bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵛ")][bstack1l1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵜ")]:
            bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵝ")][bstack1l1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵞ")][bstack1l1111l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᵟ")] = []
          for ext in bstack1111l1ll11l_opy_[bstack1l1111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᵠ")]:
            if ext not in bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᵡ")][bstack1l1111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᵢ")][bstack1l1111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᵣ")]:
              bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵤ")][bstack1l1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵥ")][bstack1l1111l_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᵦ")].append(ext)
        if bstack1l1111l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵧ") in bstack1111l1ll11l_opy_:
          if bstack1l1111l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᵨ") not in bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᵩ")][bstack1l1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᵪ")]:
            bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᵫ")][bstack1l1111l_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᵬ")][bstack1l1111l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵭ")] = {}
          bstack1111l1ll1l1_opy_(bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᵮ")][bstack1l1111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᵯ")][bstack1l1111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᵰ")],
                    bstack1111l1ll11l_opy_[bstack1l1111l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᵱ")])
        os.environ[bstack1l1111l_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᵲ")] = bstack1l1111l_opy_ (u"ࠧࡵࡴࡸࡩࠬᵳ")
        return bstack1l1l1ll111_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l1l1ll111_opy_, ChromeOptions):
          chrome_options = bstack1l1l1ll111_opy_
        elif isinstance(bstack1l1l1ll111_opy_, dict):
          for value in bstack1l1l1ll111_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l1l1ll111_opy_, dict):
            bstack1l1l1ll111_opy_[bstack1l1111l_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩᵴ")] = chrome_options
          else:
            bstack1l1l1ll111_opy_ = chrome_options
        if bstack1111l1ll11l_opy_ is not None:
          if bstack1l1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᵵ") in bstack1111l1ll11l_opy_:
                bstack1111l1lll1l_opy_ = chrome_options.arguments or []
                new_args = bstack1111l1ll11l_opy_[bstack1l1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᵶ")]
                for arg in new_args:
                    if arg not in bstack1111l1lll1l_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l1111l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᵷ") in bstack1111l1ll11l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l1111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᵸ"), [])
                bstack1111l11lll1_opy_ = bstack1111l1ll11l_opy_[bstack1l1111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᵹ")]
                for extension in bstack1111l11lll1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l1111l_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᵺ") in bstack1111l1ll11l_opy_:
                bstack1111l11ll1l_opy_ = chrome_options.experimental_options.get(bstack1l1111l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᵻ"), {})
                bstack1111ll11111_opy_ = bstack1111l1ll11l_opy_[bstack1l1111l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᵼ")]
                bstack1111l1ll1l1_opy_(bstack1111l11ll1l_opy_, bstack1111ll11111_opy_)
                chrome_options.add_experimental_option(bstack1l1111l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᵽ"), bstack1111l11ll1l_opy_)
        os.environ[bstack1l1111l_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᵾ")] = bstack1l1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪᵿ")
        return bstack1l1l1ll111_opy_
    except Exception as e:
      logger.error(bstack1l1111l_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦᶀ") + str(e))
      return bstack1l1l1ll111_opy_