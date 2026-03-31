# coding: UTF-8
import sys
bstack11lll11_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack11l1l11_opy_ = 7
def bstack1ll11_opy_ (bstack111lll1_opy_):
    global bstack1ll111l_opy_
    bstack1llll11_opy_ = ord (bstack111lll1_opy_ [-1])
    bstack1_opy_ = bstack111lll1_opy_ [:-1]
    bstack111l1ll_opy_ = bstack1llll11_opy_ % len (bstack1_opy_)
    bstack1l11lll_opy_ = bstack1_opy_ [:bstack111l1ll_opy_] + bstack1_opy_ [bstack111l1ll_opy_:]
    if bstack11lll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack11_opy_ + bstack1llll11_opy_) % bstack11l1l11_opy_) for bstack11_opy_, char in enumerate (bstack1l11lll_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111ll111l1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack111ll1ll111_opy_ as bstack111lll111l1_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import current_time, bstack1lll1ll1ll1_opy_, bstack1ll11l1l11_opy_, bstack111ll11llll_opy_, \
  bstack111lll11l11_opy_, bstack11ll11l1l1_opy_, get_host_info, bstack111ll1lllll_opy_, bstack1ll11l111l_opy_, error_handler, bstack111ll1lll11_opy_, bstack111ll1111l1_opy_, bstack1l1111l111_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1ll1lll11l_opy_ import bstack11ll11l1ll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1ll1lll11l_opy_ = bstack11ll11l1ll_opy_()
@error_handler(class_method=False)
def _111ll111l11_opy_(driver, bstack1ll1lllll11_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll11_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᩅ"): caps.get(bstack1ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᩆ"), None),
        bstack1ll11_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᩇ"): bstack1ll1lllll11_opy_.get(bstack1ll11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᩈ"), None),
        bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᩉ"): caps.get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᩊ"), None),
        bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᩋ"): caps.get(bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᩌ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᩍ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᩎ"), None) is None or os.environ[bstack1ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᩏ")] == bstack1ll11_opy_ (u"ࠤࡱࡹࡱࡲࠢᩐ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᩑ"), False) or any([p.get(bstack1ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᩒ"), False) == True for p in config.get(bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᩓ"), [])])
def is_enabled_platform(config, bstack11111lll1_opy_):
  try:
    bstack111ll11l111_opy_ = config.get(bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᩔ"), False)
    _111ll1111ll_opy_ = int(bstack11111lll1_opy_)
    if _111ll1111ll_opy_ < 0:
      _111ll1111ll_opy_ = 0
    bstack111ll1l111_opy_ = config.get(bstack1ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᩕ"), [])
    if _111ll1111ll_opy_ < len(bstack111ll1l111_opy_) and bstack111ll1l111_opy_[_111ll1111ll_opy_]:
      bstack111ll1l1111_opy_ = bstack111ll1l111_opy_[_111ll1111ll_opy_].get(bstack1ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᩖ"), None)
    else:
      bstack111ll1l1111_opy_ = config.get(bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᩗ"), None)
    if bstack111ll1l1111_opy_ != None:
      bstack111ll11l111_opy_ = bstack111ll1l1111_opy_
    bstack111ll11ll1l_opy_ = os.getenv(bstack1ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᩘ")) is not None and len(os.getenv(bstack1ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᩙ"))) > 0 and os.getenv(bstack1ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᩚ")) != bstack1ll11_opy_ (u"࠭࡮ࡶ࡮࡯ࠫᩛ")
    return bstack111ll11l111_opy_ and bstack111ll11ll1l_opy_
  except Exception as error:
    logger.debug(bstack1ll11_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡦࡴ࡬ࡪࡾ࡯࡮ࡨࠢࡷ࡬ࡪࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡦࡵࡶ࡭ࡴࡴࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᩜ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l1l111l1l1_opy_ = os.getenv(bstack1ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᩝ"))
  if bstack1l1l111l1l1_opy_ is None:
    return True
  bstack1l1l111l1l1_opy_ = json.loads(bstack1l1l111l1l1_opy_)
  try:
    include_tags = bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᩞ")] if bstack1ll11_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᩟") in bstack1l1l111l1l1_opy_ and isinstance(bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦ᩠ࠩ")], list) else []
    exclude_tags = bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᩡ")] if bstack1ll11_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᩢ") in bstack1l1l111l1l1_opy_ and isinstance(bstack1l1l111l1l1_opy_[bstack1ll11_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᩣ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡶࡢ࡮࡬ࡨࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡦࡰࡴࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡨࡧ࡮࡯࡫ࡱ࡫࠳ࠦࡅࡳࡴࡲࡶࠥࡀࠠࠣᩤ") + str(error))
  return False
def bstack111ll1l1l11_opy_(config, bstack111ll111lll_opy_, bstack111l1lllll1_opy_, bstack111ll1llll1_opy_):
  bstack111ll111ll1_opy_ = bstack111ll11llll_opy_(config)
  bstack111ll1l11l1_opy_ = bstack111lll11l11_opy_(config)
  if bstack111ll111ll1_opy_ is None or bstack111ll1l11l1_opy_ is None:
    logger.error(bstack1ll11_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࡐ࡭ࡸࡹࡩ࡯ࡩࠣࡥࡺࡺࡨࡦࡰࡷ࡭ࡨࡧࡴࡪࡱࡱࠤࡹࡵ࡫ࡦࡰࠪᩥ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᩦ"), bstack1ll11_opy_ (u"ࠫࢀࢃࠧᩧ")))
    data = {
        bstack1ll11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᩨ"): config[bstack1ll11_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᩩ")],
        bstack1ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᩪ"): config.get(bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᩫ"), os.path.basename(os.getcwd())),
        bstack1ll11_opy_ (u"ࠩࡶࡸࡦࡸࡴࡕ࡫ࡰࡩࠬᩬ"): current_time(),
        bstack1ll11_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᩭ"): config.get(bstack1ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᩮ"), bstack1ll11_opy_ (u"ࠬ࠭ᩯ")),
        bstack1ll11_opy_ (u"࠭ࡳࡰࡷࡵࡧࡪ࠭ᩰ"): {
            bstack1ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧᩱ"): bstack111ll111lll_opy_,
            bstack1ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᩲ"): bstack111l1lllll1_opy_,
            bstack1ll11_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᩳ"): __version__,
            bstack1ll11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬᩴ"): bstack1ll11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ᩵"),
            bstack1ll11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ᩶"): bstack1ll11_opy_ (u"࠭ࡳࡦ࡮ࡨࡲ࡮ࡻ࡭ࠨ᩷"),
            bstack1ll11_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᩸"): bstack111ll1llll1_opy_
        },
        bstack1ll11_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵࠪ᩹"): settings,
        bstack1ll11_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡆࡳࡳࡺࡲࡰ࡮ࠪ᩺"): bstack111ll1lllll_opy_(),
        bstack1ll11_opy_ (u"ࠪࡧ࡮ࡏ࡮ࡧࡱࠪ᩻"): bstack11ll11l1l1_opy_(),
        bstack1ll11_opy_ (u"ࠫ࡭ࡵࡳࡵࡋࡱࡪࡴ࠭᩼"): get_host_info(),
        bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ᩽"): bstack1ll11l1l11_opy_(config)
    }
    headers = {
        bstack1ll11_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ᩾"): bstack1ll11_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰ᩿ࠪ"),
    }
    config = {
        bstack1ll11_opy_ (u"ࠨࡣࡸࡸ࡭࠭᪀"): (bstack111ll111ll1_opy_, bstack111ll1l11l1_opy_),
        bstack1ll11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᪁"): headers
    }
    response = bstack1ll11l111l_opy_(bstack1ll11_opy_ (u"ࠪࡔࡔ࡙ࡔࠨ᪂"), bstack111lll111l1_opy_ + bstack1ll11_opy_ (u"ࠫ࠴ࡼ࠲࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶࠫ᪃"), data, config)
    bstack111ll1ll11l_opy_ = response.json()
    if bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭᪄")]:
      parsed = json.loads(os.getenv(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ᪅"), bstack1ll11_opy_ (u"ࠧࡼࡿࠪ᪆")))
      parsed[bstack1ll11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᪇")] = bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧ᪈")][bstack1ll11_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᪉")]
      os.environ[bstack1ll11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᪊")] = json.dumps(parsed)
      accessibility_scripts.bstack11111l111_opy_(bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠬࡪࡡࡵࡣࠪ᪋")][bstack1ll11_opy_ (u"࠭ࡳࡤࡴ࡬ࡴࡹࡹࠧ᪌")])
      accessibility_scripts.bstack111lll1l111_opy_(bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠧࡥࡣࡷࡥࠬ᪍")][bstack1ll11_opy_ (u"ࠨࡥࡲࡱࡲࡧ࡮ࡥࡵࠪ᪎")])
      accessibility_scripts.store()
      return bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧ᪏")][bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡗࡳࡰ࡫࡮ࠨ᪐")], bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠫࡩࡧࡴࡢࠩ᪑")][bstack1ll11_opy_ (u"ࠬ࡯ࡤࠨ᪒")]
    else:
      logger.error(bstack1ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡴࡸࡲࡳ࡯࡮ࡨࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠧ᪓") + bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᪔")])
      if bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᪕")] == bstack1ll11_opy_ (u"ࠩࡌࡲࡻࡧ࡬ࡪࡦࠣࡧࡴࡴࡦࡪࡩࡸࡶࡦࡺࡩࡰࡰࠣࡴࡦࡹࡳࡦࡦ࠱ࠫ᪖"):
        for bstack111ll1l111l_opy_ in bstack111ll1ll11l_opy_[bstack1ll11_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࡵࠪ᪗")]:
          logger.error(bstack111ll1l111l_opy_[bstack1ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᪘")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࠨ᪙") +  str(error))
    return None, None
def bstack111lll11lll_opy_():
  if os.getenv(bstack1ll11_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᪚")) is None:
    return {
        bstack1ll11_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ᪛"): bstack1ll11_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᪜"),
        bstack1ll11_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᪝"): bstack1ll11_opy_ (u"ࠪࡆࡺ࡯࡬ࡥࠢࡦࡶࡪࡧࡴࡪࡱࡱࠤ࡭ࡧࡤࠡࡨࡤ࡭ࡱ࡫ࡤ࠯ࠩ᪞")
    }
  data = {bstack1ll11_opy_ (u"ࠫࡪࡴࡤࡕ࡫ࡰࡩࠬ᪟"): current_time()}
  headers = {
      bstack1ll11_opy_ (u"ࠬࡇࡵࡵࡪࡲࡶ࡮ࢀࡡࡵ࡫ࡲࡲࠬ᪠"): bstack1ll11_opy_ (u"࠭ࡂࡦࡣࡵࡩࡷࠦࠧ᪡") + os.getenv(bstack1ll11_opy_ (u"ࠢࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠧ᪢")),
      bstack1ll11_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧ᪣"): bstack1ll11_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬ᪤")
  }
  response = bstack1ll11l111l_opy_(bstack1ll11_opy_ (u"ࠪࡔ࡚࡚ࠧ᪥"), bstack111lll111l1_opy_ + bstack1ll11_opy_ (u"ࠫ࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳ࠰ࡵࡷࡳࡵ࠭᪦"), data, { bstack1ll11_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᪧ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll11_opy_ (u"ࠨࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱࠤࡲࡧࡲ࡬ࡧࡧࠤࡦࡹࠠࡤࡱࡰࡴࡱ࡫ࡴࡦࡦࠣࡥࡹࠦࠢ᪨") + bstack1lll1ll1ll1_opy_().isoformat() + bstack1ll11_opy_ (u"࡛ࠧࠩ᪩"))
      return {bstack1ll11_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨ᪪"): bstack1ll11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪ᪫"), bstack1ll11_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᪬"): bstack1ll11_opy_ (u"ࠫࠬ᪭")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠ࡮ࡣࡵ࡯࡮ࡴࡧࠡࡥࡲࡱࡵࡲࡥࡵ࡫ࡲࡲࠥࡵࡦࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࡀࠠࠣ᪮") + str(error))
    return {
        bstack1ll11_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᪯"): bstack1ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᪰"),
        bstack1ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᪱"): str(error)
    }
def bstack111lll11ll1_opy_(bstack111ll1l1ll1_opy_):
    return re.match(bstack1ll11_opy_ (u"ࡴࠪࡢࡡࡪࠫࠩ࡞࠱ࡠࡩ࠱ࠩࡀࠦࠪ᪲"), bstack111ll1l1ll1_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack111ll11lll1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack111ll11lll1_opy_ = desired_capabilities
        else:
          bstack111ll11lll1_opy_ = {}
        bstack1l11l1ll11l_opy_ = (bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ᪳"), bstack1ll11_opy_ (u"ࠫࠬ᪴")).lower() or caps.get(bstack1ll11_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨ᪵ࠫ"), bstack1ll11_opy_ (u"᪶࠭ࠧ")).lower())
        if bstack1l11l1ll11l_opy_ == bstack1ll11_opy_ (u"ࠧࡪࡱࡶ᪷ࠫ"):
            return True
        if bstack1l11l1ll11l_opy_ == bstack1ll11_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥ᪸ࠩ"):
            bstack1l11ll1l11l_opy_ = str(float(caps.get(bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱ᪹ࠫ")) or bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶ᪺ࠫ"), {}).get(bstack1ll11_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᪻"),bstack1ll11_opy_ (u"ࠬ࠭᪼"))))
            if bstack1l11l1ll11l_opy_ == bstack1ll11_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪ᪽ࠧ") and int(bstack1l11ll1l11l_opy_.split(bstack1ll11_opy_ (u"ࠧ࠯ࠩ᪾"))[0]) < float(bstack111ll1l1l1l_opy_):
                logger.warning(str(bstack111ll11l1l1_opy_))
                return False
            return True
        bstack1l11lll1l1l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴᪿࠩ"), {}).get(bstack1ll11_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࡐࡤࡱࡪᫀ࠭"), caps.get(bstack1ll11_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࠪ᫁"), bstack1ll11_opy_ (u"ࠫࠬ᫂")))
        if bstack1l11lll1l1l_opy_:
            logger.warning(bstack1ll11_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡊࡥࡴ࡭ࡷࡳࡵࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ᫃"))
            return False
        browser = (caps.get(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨ᫄ࠫ"), bstack1ll11_opy_ (u"ࠧࠨ᫅")) or caps.get(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩ᫆"), bstack1ll11_opy_ (u"ࠩࠪ᫇"))).lower() or \
                  (bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᫈"), bstack1ll11_opy_ (u"ࠫࠬ᫉")) or bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ᫊࠭"), bstack1ll11_opy_ (u"࠭ࠧ᫋"))).lower()
        if browser not in (bstack1ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᫌ"), bstack1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡩࡶ࡯ࠪᫍ"), bstack1ll11_opy_ (u"ࠩࡳࡰࡦࡿࡷࡳ࡫ࡪ࡬ࡹ࠳ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨᫎ")):
            logger.warning(bstack1ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ᫏"))
            return False
        browser_version = caps.get(bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᫐")) or caps.get(bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᫑")) or bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᫒")) or bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᫓"), {}).get(bstack1ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᫔")) or bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᫕"), {}).get(bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᫖"))
        bstack1l11lll111l_opy_ = bstack111ll111l1l_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack111ll11111l_opy_ = False
        if config is not None:
          bstack111ll11111l_opy_ = bstack1ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ᫗") in config and str(config[bstack1ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᫘")]).lower() != bstack1ll11_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ᫙")
        if os.environ.get(bstack1ll11_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ᫚"), bstack1ll11_opy_ (u"ࠨࠩ᫛")).lower() == bstack1ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᫜") or bstack111ll11111l_opy_:
          bstack1l11lll111l_opy_ = bstack111ll111l1l_opy_.bstack1l1l11l1111_opy_
        if browser_version and browser_version != bstack1ll11_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪ᫝") and int(browser_version.split(bstack1ll11_opy_ (u"ࠫ࠳࠭᫞"))[0]) <= bstack1l11lll111l_opy_:
          logger.warning(bstack1ll11_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻࡾ࠰ࠪ᫟").format(bstack1l11lll111l_opy_))
          return False
        bstack1l1l111l11l_opy_ = (caps.get(bstack1ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᫠"))
                         or bstack111ll11lll1_opy_.get(bstack1ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᫡"), {})
                         or caps.get(bstack1ll11_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᫢"), {}))
        bstack111ll1lll1l_opy_ = bstack1l1l111l11l_opy_.get(bstack1ll11_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᫣"), []) if isinstance(bstack1l1l111l11l_opy_, dict) else []
        if not isinstance(bstack111ll1lll1l_opy_, list):
            bstack111ll1lll1l_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack1ll11_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ᫤") or arg == bstack1ll11_opy_ (u"ࠫ࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭᫥") or (arg.startswith(bstack1ll11_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࠪ᫦")) and arg != bstack1ll11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࡲࡪࡽࠧ᫧")))
               for arg in bstack111ll1lll1l_opy_):
            logger.warning(bstack1ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ᫨"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack1ll11_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥ᫩") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1111l1l1_opy_ = config.get(bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫪"), {})
    bstack1ll1111l1l1_opy_[bstack1ll11_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭᫫")] = os.getenv(bstack1ll11_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᫬"))
    bstack111lllll_opy_ = json.loads(os.getenv(bstack1ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭᫭"), bstack1ll11_opy_ (u"࠭ࡻࡾࠩ᫮"))).get(bstack1ll11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫯"))
    if not config[bstack1ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᫰")].get(bstack1ll11_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣ᫱")):
      if bstack1ll11_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᫲") in caps:
        caps[bstack1ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᫳")][bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᫴")] = bstack1ll1111l1l1_opy_
        caps[bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᫵")][bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ᫶")][bstack1ll11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᫷")] = bstack111lllll_opy_
      else:
        caps[bstack1ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᫸")] = bstack1ll1111l1l1_opy_
        caps[bstack1ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫹")][bstack1ll11_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᫺")] = bstack111lllll_opy_
  except Exception as error:
    logger.debug(bstack1ll11_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨ᫻") +  str(error))
def start_test_capture(driver, bstack111ll1ll1l1_opy_):
  try:
    setattr(driver, bstack1ll11_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭᫼"), True)
    session = driver.session_id
    if session:
      bstack111lll11l1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111lll11l1l_opy_ = False
      bstack111lll11l1l_opy_ = url.scheme in [bstack1ll11_opy_ (u"ࠢࡩࡶࡷࡴࠧ᫽"), bstack1ll11_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ᫾")]
      if bstack111lll11l1l_opy_:
        if bstack111ll1ll1l1_opy_:
          logger.info(bstack1ll11_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤ᫿"))
      return bstack111ll1ll1l1_opy_
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᬀ") + str(e))
    return False
def bstack1l1l1ll1l_opy_(driver, name, path):
  try:
    bstack1l11ll1ll11_opy_ = {
        bstack1ll11_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫᬁ"): threading.current_thread().current_test_uuid,
        bstack1ll11_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪᬂ"): os.environ.get(bstack1ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫᬃ"), bstack1ll11_opy_ (u"ࠧࠨᬄ")),
        bstack1ll11_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬᬅ"): os.environ.get(bstack1ll11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭ᬆ"), bstack1ll11_opy_ (u"ࠪࠫᬇ"))
    }
    bstack1l11ll1ll1_opy_ = bstack1ll1lll11l_opy_.bstack11l11l111_opy_(EVENTS.bstack11ll1ll1l1_opy_.value)
    logger.debug(bstack1ll11_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧᬈ"))
    try:
      if (bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᬉ"), None) and bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᬊ"), None)):
        scripts = {bstack1ll11_opy_ (u"ࠧࡴࡥࡤࡲࠬᬋ"): accessibility_scripts.perform_scan}
        bstack111lll111ll_opy_ = json.loads(scripts[bstack1ll11_opy_ (u"ࠣࡵࡦࡥࡳࠨᬌ")].replace(bstack1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᬍ"), bstack1ll11_opy_ (u"ࠥࠦᬎ")))
        bstack111lll111ll_opy_[bstack1ll11_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᬏ")][bstack1ll11_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᬐ")] = None
        scripts[bstack1ll11_opy_ (u"ࠨࡳࡤࡣࡱࠦᬑ")] = bstack1ll11_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᬒ") + json.dumps(bstack111lll111ll_opy_)
        accessibility_scripts.bstack11111l111_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll11_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣᬓ"): name}))
      bstack1ll1lll11l_opy_.end(EVENTS.bstack11ll1ll1l1_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᬔ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᬕ"), True, None)
    except Exception as error:
      bstack1ll1lll11l_opy_.end(EVENTS.bstack11ll1ll1l1_opy_.value, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᬖ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᬗ"), False, str(error))
    bstack1l11ll1ll1_opy_ = bstack1ll1lll11l_opy_.bstack111l1llllll_opy_(EVENTS.bstack1l11l1ll1ll_opy_.value)
    bstack1ll1lll11l_opy_.mark(bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᬘ"))
    try:
      if (bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᬙ"), None) and bstack1l1111l111_opy_(threading.current_thread(), bstack1ll11_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᬚ"), None)):
        scripts = {bstack1ll11_opy_ (u"ࠩࡶࡧࡦࡴࠧᬛ"): accessibility_scripts.perform_scan}
        bstack111lll111ll_opy_ = json.loads(scripts[bstack1ll11_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᬜ")].replace(bstack1ll11_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᬝ"), bstack1ll11_opy_ (u"ࠧࠨᬞ")))
        bstack111lll111ll_opy_[bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᬟ")][bstack1ll11_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᬠ")] = None
        scripts[bstack1ll11_opy_ (u"ࠣࡵࡦࡥࡳࠨᬡ")] = bstack1ll11_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᬢ") + json.dumps(bstack111lll111ll_opy_)
        accessibility_scripts.bstack11111l111_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l11ll1ll11_opy_))
      bstack1ll1lll11l_opy_.end(bstack1l11ll1ll1_opy_, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᬣ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᬤ"),True, None)
    except Exception as error:
      bstack1ll1lll11l_opy_.end(bstack1l11ll1ll1_opy_, bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᬥ"), bstack1l11ll1ll1_opy_ + bstack1ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᬦ"),False, str(error))
    logger.info(bstack1ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᬧ"))
    try:
      bstack1l1l1111111_opy_ = {
        bstack1ll11_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤᬨ"): {
          bstack1ll11_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥᬩ"): bstack1ll11_opy_ (u"ࠥࡅ࠶࠷࡙ࡠࡕࡄ࡚ࡊࡥࡒࡆࡕࡘࡐ࡙࡙ࠢᬪ"),
        },
        bstack1ll11_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᬫ"): {
          bstack1ll11_opy_ (u"ࠧࡨ࡯ࡥࡻࠥᬬ"): {
            bstack1ll11_opy_ (u"ࠨ࡭ࡴࡩࠥᬭ"): bstack1ll11_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᬮ"),
            bstack1ll11_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᬯ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l1l1111111_opy_, separators=(bstack1ll11_opy_ (u"ࠩ࠯ࠫᬰ"), bstack1ll11_opy_ (u"ࠪ࠾ࠬᬱ"))))
    except Exception as bstack1ll1l1llll_opy_:
      logger.debug(bstack1ll11_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡭ࡱࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡧࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡨࡦࡺࡡ࠻ࠢࠥᬲ") + str(bstack1ll1l1llll_opy_) + bstack1ll11_opy_ (u"ࠧࠨᬳ"))
  except Exception as bstack1l11ll111l1_opy_:
    logger.error(bstack1ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀ᬴ࠠࠣ") + str(path) + bstack1ll11_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᬵ") + str(bstack1l11ll111l1_opy_))
def bstack111ll1l11ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᬶ")) and str(caps.get(bstack1ll11_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᬷ"))).lower() == bstack1ll11_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦᬸ"):
        bstack1l11ll1l11l_opy_ = caps.get(bstack1ll11_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᬹ")) or caps.get(bstack1ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᬺ"))
        if bstack1l11ll1l11l_opy_ and int(str(bstack1l11ll1l11l_opy_)) < bstack111ll1l1l1l_opy_:
            return False
    return True
def bstack1111l1llll_opy_(config):
  if bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᬻ") in config:
        return config[bstack1ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᬼ")]
  for platform in config.get(bstack1ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᬽ"), []):
      if bstack1ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᬾ") in platform:
          return platform[bstack1ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᬿ")]
  return None
def bstack11ll111ll1_opy_(bstack11l1111ll1_opy_):
  try:
    browser_name = bstack11l1111ll1_opy_[bstack1ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᭀ")]
    browser_version = bstack11l1111ll1_opy_[bstack1ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᭁ")]
    chrome_options = bstack11l1111ll1_opy_[bstack1ll11_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧᭂ")]
    try:
        bstack111ll11l1ll_opy_ = int(browser_version.split(bstack1ll11_opy_ (u"ࠧ࠯ࠩᭃ"))[0])
    except ValueError as e:
        logger.error(bstack1ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡣࡰࡰࡹࡩࡷࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲ᭄ࠧ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᭅ")):
        logger.warning(bstack1ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᭆ"))
        return False
    if bstack111ll11l1ll_opy_ < bstack111ll111l1l_opy_.bstack1l1l11l1111_opy_:
        logger.warning(bstack1ll11_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡯ࡲࡦࡵࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡺࡪࡸࡳࡪࡱࡱࠤࢀࢃࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠫᭇ").format(bstack111ll111l1l_opy_.bstack1l1l11l1111_opy_))
        return False
    bstack111ll1lll1l_opy_ = chrome_options.get(bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪᭈ"), []) if chrome_options else []
    if not isinstance(bstack111ll1lll1l_opy_, list):
        bstack111ll1lll1l_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack1ll11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᭉ") or arg == bstack1ll11_opy_ (u"ࠧࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᭊ") or (arg.startswith(bstack1ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࡂ࠭ᭋ")) and arg != bstack1ll11_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃ࡮ࡦࡹࠪᭌ")))
           for arg in bstack111ll1lll1l_opy_):
        logger.warning(bstack1ll11_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧ᭍"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡺࡶࡰࡰࡴࡷࠤ࡫ࡵࡲࠡ࡮ࡲࡧࡦࡲࠠࡄࡪࡵࡳࡲ࡫࠺ࠡࠤ᭎") + str(e))
    return False
def bstack1l1ll1l111_opy_(bstack1l1lll1l1_opy_, config):
    try:
      bstack1l1l1111l1l_opy_ = bstack1ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᭏") in config and config[bstack1ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᭐")] == True
      bstack111ll11111l_opy_ = bstack1ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᭑") in config and str(config[bstack1ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᭒")]).lower() != bstack1ll11_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ᭓")
      if not (bstack1l1l1111l1l_opy_ and (not bstack1ll11l1l11_opy_(config) or bstack111ll11111l_opy_)):
        return bstack1l1lll1l1_opy_
      bstack111ll1l1lll_opy_ = accessibility_scripts.bstack111lll11111_opy_
      if bstack111ll1l1lll_opy_ is None:
        logger.debug(bstack1ll11_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶࠤࡦࡸࡥࠡࡐࡲࡲࡪࠨ᭔"))
        return bstack1l1lll1l1_opy_
      bstack111ll1ll1ll_opy_ = int(str(bstack111ll1111l1_opy_()).split(bstack1ll11_opy_ (u"ࠫ࠳࠭᭕"))[0])
      logger.debug(bstack1ll11_opy_ (u"࡙ࠧࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡦࡨࡸࡪࡩࡴࡦࡦ࠽ࠤࠧ᭖") + str(bstack111ll1ll1ll_opy_) + bstack1ll11_opy_ (u"ࠨࠢ᭗"))
      if bstack111ll1ll1ll_opy_ == 3 and isinstance(bstack1l1lll1l1_opy_, dict) and bstack1ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᭘") in bstack1l1lll1l1_opy_ and bstack111ll1l1lll_opy_ is not None:
        if bstack1ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᭙") not in bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᭚")]:
          bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᭛")][bstack1ll11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᭜")] = {}
        if bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪ᭝") in bstack111ll1l1lll_opy_:
          if bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫ᭞") not in bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᭟")][bstack1ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᭠")]:
            bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᭡")][bstack1ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭢")][bstack1ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩ᭣")] = []
          for arg in bstack111ll1l1lll_opy_[bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪ᭤")]:
            if arg not in bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᭥")][bstack1ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭦")][bstack1ll11_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᭧")]:
              bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᭨")][bstack1ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭩")][bstack1ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩ᭪")].append(arg)
        if bstack1ll11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᭫") in bstack111ll1l1lll_opy_:
          if bstack1ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵ᭬ࠪ") not in bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᭭")][bstack1ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᭮")]:
            bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᭯")][bstack1ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭰")][bstack1ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᭱")] = []
          for ext in bstack111ll1l1lll_opy_[bstack1ll11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᭲")]:
            if ext not in bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᭳")][bstack1ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭴")][bstack1ll11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᭵")]:
              bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᭶")][bstack1ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭷")][bstack1ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᭸")].append(ext)
        if bstack1ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᭹") in bstack111ll1l1lll_opy_:
          if bstack1ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᭺") not in bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᭻")][bstack1ll11_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᭼")]:
            bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᭽")][bstack1ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭾")][bstack1ll11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᭿")] = {}
          bstack111ll1lll11_opy_(bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᮀ")][bstack1ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᮁ")][bstack1ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᮂ")],
                    bstack111ll1l1lll_opy_[bstack1ll11_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᮃ")])
        os.environ[bstack1ll11_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᮄ")] = bstack1ll11_opy_ (u"ࠪࡸࡷࡻࡥࠨᮅ")
        return bstack1l1lll1l1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l1lll1l1_opy_, ChromeOptions):
          chrome_options = bstack1l1lll1l1_opy_
        elif isinstance(bstack1l1lll1l1_opy_, dict):
          for value in bstack1l1lll1l1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l1lll1l1_opy_, dict):
            bstack1l1lll1l1_opy_[bstack1ll11_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᮆ")] = chrome_options
          else:
            bstack1l1lll1l1_opy_ = chrome_options
        if bstack111ll1l1lll_opy_ is not None:
          if bstack1ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪᮇ") in bstack111ll1l1lll_opy_:
                bstack111ll11ll11_opy_ = chrome_options.arguments or []
                new_args = bstack111ll1l1lll_opy_[bstack1ll11_opy_ (u"࠭ࡡࡳࡩࡶࠫᮈ")]
                for arg in new_args:
                    if arg not in bstack111ll11ll11_opy_:
                        chrome_options.add_argument(arg)
          if bstack1ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᮉ") in bstack111ll1l1lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1ll11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᮊ"), [])
                bstack111ll11l11l_opy_ = bstack111ll1l1lll_opy_[bstack1ll11_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᮋ")]
                for extension in bstack111ll11l11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1ll11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᮌ") in bstack111ll1l1lll_opy_:
                bstack111ll111111_opy_ = chrome_options.experimental_options.get(bstack1ll11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᮍ"), {})
                bstack111lll1111l_opy_ = bstack111ll1l1lll_opy_[bstack1ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᮎ")]
                bstack111ll1lll11_opy_(bstack111ll111111_opy_, bstack111lll1111l_opy_)
                chrome_options.add_experimental_option(bstack1ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᮏ"), bstack111ll111111_opy_)
        os.environ[bstack1ll11_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᮐ")] = bstack1ll11_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᮑ")
        return bstack1l1lll1l1_opy_
    except Exception as e:
      logger.error(bstack1ll11_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡦࡧ࡭ࡳ࡭ࠠ࡯ࡱࡱ࠱ࡇ࡙ࠠࡪࡰࡩࡶࡦࠦࡡ࠲࠳ࡼࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࠢᮒ") + str(e))
      return bstack1l1lll1l1_opy_