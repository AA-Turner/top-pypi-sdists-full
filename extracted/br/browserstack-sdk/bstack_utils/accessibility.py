# coding: UTF-8
import sys
bstack1l11lll_opy_ = sys.version_info [0] == 2
bstack11ll1ll_opy_ = 2048
bstack1111l11_opy_ = 7
def bstack1ll1lll_opy_ (bstack1l11ll_opy_):
    global bstack1lllll1_opy_
    bstack11llll_opy_ = ord (bstack1l11ll_opy_ [-1])
    bstack111l1ll_opy_ = bstack1l11ll_opy_ [:-1]
    bstack1ll1111_opy_ = bstack11llll_opy_ % len (bstack111l1ll_opy_)
    bstack1ll1l1_opy_ = bstack111l1ll_opy_ [:bstack1ll1111_opy_] + bstack111l1ll_opy_ [bstack1ll1111_opy_:]
    if bstack1l11lll_opy_:
        bstack11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    else:
        bstack11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll1ll_opy_ - (bstack11ll11l_opy_ + bstack11llll_opy_) % bstack1111l11_opy_) for bstack11ll11l_opy_, char in enumerate (bstack1ll1l1_opy_)])
    return eval (bstack11l1l_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111ll11ll1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack111lll11l1l_opy_ as bstack111ll1lll11_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import current_time, bstack1llll1l1111_opy_, bstack1111111l11_opy_, bstack111lll111ll_opy_, \
  bstack111ll111lll_opy_, bstack1ll11l1l11_opy_, get_host_info, bstack111ll1l1ll1_opy_, bstack111lll1l11_opy_, error_handler, bstack111ll111ll1_opy_, bstack111ll1lll1l_opy_, bstack1l11lll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1l111ll111_opy_ import bstack1l1l11ll1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1l111ll111_opy_ = bstack1l1l11ll1_opy_()
@error_handler(class_method=False)
def _111ll1lllll_opy_(driver, bstack1lll11l1l1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1lll_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪᨴ"): caps.get(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᨵ"), None),
        bstack1ll1lll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᨶ"): bstack1lll11l1l1l_opy_.get(bstack1ll1lll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᨷ"), None),
        bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᨸ"): caps.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᨹ"), None),
        bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᨺ"): caps.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᨻ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᨼ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᨽ"), None) is None or os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᨾ")] == bstack1ll1lll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᨿ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᩀ"), False) or any([p.get(bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᩁ"), False) == True for p in config.get(bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᩂ"), [])])
def is_enabled_platform(config, bstack11111lll_opy_):
  try:
    bstack111ll11lll1_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᩃ"), False)
    _111ll1l1l1l_opy_ = int(bstack11111lll_opy_)
    if _111ll1l1l1l_opy_ < 0:
      _111ll1l1l1l_opy_ = 0
    bstack111l11l111_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᩄ"), [])
    if _111ll1l1l1l_opy_ < len(bstack111l11l111_opy_) and bstack111l11l111_opy_[_111ll1l1l1l_opy_]:
      bstack111lll1l1l1_opy_ = bstack111l11l111_opy_[_111ll1l1l1l_opy_].get(bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᩅ"), None)
    else:
      bstack111lll1l1l1_opy_ = config.get(bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᩆ"), None)
    if bstack111lll1l1l1_opy_ != None:
      bstack111ll11lll1_opy_ = bstack111lll1l1l1_opy_
    bstack111ll11l111_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᩇ")) is not None and len(os.getenv(bstack1ll1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᩈ"))) > 0 and os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᩉ")) != bstack1ll1lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᩊ")
    return bstack111ll11lll1_opy_ and bstack111ll11l111_opy_
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᩋ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l1l11l11ll_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᩌ"))
  if bstack1l1l11l11ll_opy_ is None:
    return True
  bstack1l1l11l11ll_opy_ = json.loads(bstack1l1l11l11ll_opy_)
  try:
    include_tags = bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᩍ")] if bstack1ll1lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᩎ") in bstack1l1l11l11ll_opy_ and isinstance(bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᩏ")], list) else []
    exclude_tags = bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᩐ")] if bstack1ll1lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᩑ") in bstack1l1l11l11ll_opy_ and isinstance(bstack1l1l11l11ll_opy_[bstack1ll1lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᩒ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᩓ") + str(error))
  return False
def bstack111lll11ll1_opy_(config, bstack111lll1l111_opy_, bstack111ll1l11ll_opy_, bstack111ll1ll11l_opy_):
  bstack111ll1ll1ll_opy_ = bstack111lll111ll_opy_(config)
  bstack111ll11l1ll_opy_ = bstack111ll111lll_opy_(config)
  if bstack111ll1ll1ll_opy_ is None or bstack111ll11l1ll_opy_ is None:
    logger.error(bstack1ll1lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᩔ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᩕ"), bstack1ll1lll_opy_ (u"ࠨࡽࢀࠫᩖ")))
    data = {
        bstack1ll1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᩗ"): config[bstack1ll1lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᩘ")],
        bstack1ll1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᩙ"): config.get(bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᩚ"), os.path.basename(os.getcwd())),
        bstack1ll1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᩛ"): current_time(),
        bstack1ll1lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᩜ"): config.get(bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᩝ"), bstack1ll1lll_opy_ (u"ࠩࠪᩞ")),
        bstack1ll1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪ᩟"): {
            bstack1ll1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨ᩠ࠫ"): bstack111lll1l111_opy_,
            bstack1ll1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᩡ"): bstack111ll1l11ll_opy_,
            bstack1ll1lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᩢ"): __version__,
            bstack1ll1lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᩣ"): bstack1ll1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᩤ"),
            bstack1ll1lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᩥ"): bstack1ll1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᩦ"),
            bstack1ll1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᩧ"): bstack111ll1ll11l_opy_
        },
        bstack1ll1lll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᩨ"): settings,
        bstack1ll1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᩩ"): bstack111ll1l1ll1_opy_(),
        bstack1ll1lll_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᩪ"): bstack1ll11l1l11_opy_(),
        bstack1ll1lll_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᩫ"): get_host_info(),
        bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᩬ"): bstack1111111l11_opy_(config)
    }
    headers = {
        bstack1ll1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᩭ"): bstack1ll1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᩮ"),
    }
    config = {
        bstack1ll1lll_opy_ (u"ࠬࡧࡵࡵࡪࠪᩯ"): (bstack111ll1ll1ll_opy_, bstack111ll11l1ll_opy_),
        bstack1ll1lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᩰ"): headers
    }
    response = bstack111lll1l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡑࡑࡖࡘࠬᩱ"), bstack111ll1lll11_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᩲ"), data, config)
    bstack111lll1l11l_opy_ = response.json()
    if bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᩳ")]:
      parsed = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᩴ"), bstack1ll1lll_opy_ (u"ࠫࢀࢃࠧ᩵")))
      parsed[bstack1ll1lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᩶")] = bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫ᩷")][bstack1ll1lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᩸")]
      os.environ[bstack1ll1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ᩹")] = json.dumps(parsed)
      accessibility_scripts.bstack111lll1111_opy_(bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠩࡧࡥࡹࡧࠧ᩺")][bstack1ll1lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫ᩻")])
      accessibility_scripts.bstack111ll1llll1_opy_(bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠫࡩࡧࡴࡢࠩ᩼")][bstack1ll1lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧ᩽")])
      accessibility_scripts.store()
      return bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫ᩾")][bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲ᩿ࠬ")], bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭᪀")][bstack1ll1lll_opy_ (u"ࠩ࡬ࡨࠬ᪁")]
    else:
      logger.error(bstack1ll1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫ᪂") + bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᪃")])
      if bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᪄")] == bstack1ll1lll_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨ᪅"):
        for bstack111ll1l11l1_opy_ in bstack111lll1l11l_opy_[bstack1ll1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧ᪆")]:
          logger.error(bstack111ll1l11l1_opy_[bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᪇")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥ᪈") +  str(error))
    return None, None
def bstack111lll1111l_opy_():
  if os.getenv(bstack1ll1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᪉")) is None:
    return {
        bstack1ll1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ᪊"): bstack1ll1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᪋"),
        bstack1ll1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᪌"): bstack1ll1lll_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭᪍")
    }
  data = {bstack1ll1lll_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩ᪎"): current_time()}
  headers = {
      bstack1ll1lll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩ᪏"): bstack1ll1lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫ᪐") + os.getenv(bstack1ll1lll_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤ᪑")),
      bstack1ll1lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ᪒"): bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩ᪓")
  }
  response = bstack111lll1l11_opy_(bstack1ll1lll_opy_ (u"ࠧࡑࡗࡗࠫ᪔"), bstack111ll1lll11_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪ᪕"), data, { bstack1ll1lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪ᪖"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦ᪗") + bstack1llll1l1111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠫ࡟࠭᪘"))
      return {bstack1ll1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬ᪙"): bstack1ll1lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧ᪚"), bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᪛"): bstack1ll1lll_opy_ (u"ࠨࠩ᪜")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧ᪝") + str(error))
    return {
        bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᪞"): bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪ᪟"),
        bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᪠"): str(error)
    }
def bstack111ll1111ll_opy_(bstack111ll1111l1_opy_):
    return re.match(bstack1ll1lll_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧ᪡"), bstack111ll1111l1_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack111ll1l1lll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack111ll1l1lll_opy_ = desired_capabilities
        else:
          bstack111ll1l1lll_opy_ = {}
        bstack1l11lll11ll_opy_ = (bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭᪢"), bstack1ll1lll_opy_ (u"ࠨࠩ᪣")).lower() or caps.get(bstack1ll1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᪤"), bstack1ll1lll_opy_ (u"ࠪࠫ᪥")).lower())
        if bstack1l11lll11ll_opy_ == bstack1ll1lll_opy_ (u"ࠫ࡮ࡵࡳࠨ᪦"):
            return True
        if bstack1l11lll11ll_opy_ == bstack1ll1lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᪧ"):
            bstack1l1l1111l11_opy_ = str(float(caps.get(bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᪨")) or bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᪩"), {}).get(bstack1ll1lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫ᪪"),bstack1ll1lll_opy_ (u"ࠩࠪ᪫"))))
            if bstack1l11lll11ll_opy_ == bstack1ll1lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫ᪬") and int(bstack1l1l1111l11_opy_.split(bstack1ll1lll_opy_ (u"ࠫ࠳࠭᪭"))[0]) < float(bstack111ll11l11l_opy_):
                logger.warning(str(bstack111ll11llll_opy_))
                return False
            return True
        bstack1l11lll1ll1_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᪮"), {}).get(bstack1ll1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪ᪯"), caps.get(bstack1ll1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧ᪰"), bstack1ll1lll_opy_ (u"ࠨࠩ᪱")))
        if bstack1l11lll1ll1_opy_:
            logger.warning(bstack1ll1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ᪲"))
            return False
        browser = (caps.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨ᪳"), bstack1ll1lll_opy_ (u"ࠫࠬ᪴")) or caps.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ᪵࠭"), bstack1ll1lll_opy_ (u"᪶࠭ࠧ"))).lower() or \
                  (bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩ᪷ࠬ"), bstack1ll1lll_opy_ (u"ࠨ᪸ࠩ")) or bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ᪹ࠪ"), bstack1ll1lll_opy_ (u"᪺ࠪࠫ"))).lower()
        if browser not in (bstack1ll1lll_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ᪻"), bstack1ll1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰ࡭ࡺࡳࠧ᪼"), bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡼࡻࡷ࡯ࡧࡩࡶ࠰ࡧ࡭ࡸ࡯࡮࡫ࡸࡱ᪽ࠬ")):
            logger.warning(bstack1ll1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᪾"))
            return False
        browser_version = caps.get(bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ᪿࠩ")) or caps.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱᫀࠫ")) or bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᫁")) or bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᫂"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ᫃࠭")) or bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹ᫄ࠧ"), {}).get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᫅"))
        bstack1l11lll111l_opy_ = bstack111ll11ll1l_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack111ll1l1111_opy_ = False
        if config is not None:
          bstack111ll1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᫆") in config and str(config[bstack1ll1lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᫇")]).lower() != bstack1ll1lll_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ᫈")
        if os.environ.get(bstack1ll1lll_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩ᫉"), bstack1ll1lll_opy_ (u"᫊ࠬ࠭")).lower() == bstack1ll1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᫋") or bstack111ll1l1111_opy_:
          bstack1l11lll111l_opy_ = bstack111ll11ll1l_opy_.bstack1l11ll1llll_opy_
        if browser_version and browser_version != bstack1ll1lll_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧᫌ") and int(browser_version.split(bstack1ll1lll_opy_ (u"ࠨ࠰ࠪᫍ"))[0]) <= bstack1l11lll111l_opy_:
          logger.warning(bstack1ll1lll_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࢂ࠴ࠧᫎ").format(bstack1l11lll111l_opy_))
          return False
        bstack1l11l1l1l1l_opy_ = (caps.get(bstack1ll1lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᫏"))
                         or bstack111ll1l1lll_opy_.get(bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫐"), {})
                         or caps.get(bstack1ll1lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᫑"), {}))
        bstack111ll11111l_opy_ = bstack1l11l1l1l1l_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶࠫ᫒"), []) if isinstance(bstack1l11l1l1l1l_opy_, dict) else []
        if not isinstance(bstack111ll11111l_opy_, list):
            bstack111ll11111l_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack1ll1lll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫ᫓") or arg == bstack1ll1lll_opy_ (u"ࠨࡪࡨࡥࡩࡲࡥࡴࡵࠪ᫔") or (arg.startswith(bstack1ll1lll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧ᫕")) and arg != bstack1ll1lll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫ᫖")))
               for arg in bstack111ll11111l_opy_):
            logger.warning(bstack1ll1lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨ᫗"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢ᫘") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1l1lll1ll_opy_ = config.get(bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᫙"), {})
    bstack1l1l1lll1ll_opy_[bstack1ll1lll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ᫚")] = os.getenv(bstack1ll1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᫛"))
    bstack11111l11_opy_ = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ᫜"), bstack1ll1lll_opy_ (u"ࠪࡿࢂ࠭᫝"))).get(bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᫞"))
    if not config[bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶࠧ᫟")].get(bstack1ll1lll_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠧ᫠")):
      if bstack1ll1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᫡") in caps:
        caps[bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᫢")][bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫣")] = bstack1l1l1lll1ll_opy_
        caps[bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᫤")][bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᫥")][bstack1ll1lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᫦")] = bstack11111l11_opy_
      else:
        caps[bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᫧")] = bstack1l1l1lll1ll_opy_
        caps[bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᫨")][bstack1ll1lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᫩")] = bstack11111l11_opy_
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥ᫪") +  str(error))
def start_test_capture(driver, bstack111lll11l11_opy_):
  try:
    setattr(driver, bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ᫫"), True)
    session = driver.session_id
    if session:
      bstack111lll111l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111lll111l1_opy_ = False
      bstack111lll111l1_opy_ = url.scheme in [bstack1ll1lll_opy_ (u"ࠦ࡭ࡺࡴࡱࠤ᫬"), bstack1ll1lll_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ᫭")]
      if bstack111lll111l1_opy_:
        if bstack111lll11l11_opy_:
          logger.info(bstack1ll1lll_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨ᫮"))
      return bstack111lll11l11_opy_
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ᫯") + str(e))
    return False
def bstack1111l1ll_opy_(driver, name, path):
  try:
    bstack1l11ll111ll_opy_ = {
        bstack1ll1lll_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨ᫰"): threading.current_thread().current_test_uuid,
        bstack1ll1lll_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᫱"): os.environ.get(bstack1ll1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᫲"), bstack1ll1lll_opy_ (u"ࠫࠬ᫳")),
        bstack1ll1lll_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩ᫴"): os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ᫵"), bstack1ll1lll_opy_ (u"ࠧࠨ᫶"))
    }
    bstack111l1l1l1_opy_ = bstack1l111ll111_opy_.bstack11l1llllll_opy_(EVENTS.bstack1l1l1l1111_opy_.value)
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ᫷"))
    try:
      if (bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ᫸"), None) and bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᫹"), None)):
        scripts = {bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ᫺"): accessibility_scripts.perform_scan}
        bstack111ll1l1l11_opy_ = json.loads(scripts[bstack1ll1lll_opy_ (u"ࠧࡹࡣࡢࡰࠥ᫻")].replace(bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᫼"), bstack1ll1lll_opy_ (u"ࠢࠣ᫽")))
        bstack111ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᫾")][bstack1ll1lll_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩ᫿")] = None
        scripts[bstack1ll1lll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᬀ")] = bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᬁ") + json.dumps(bstack111ll1l1l11_opy_)
        accessibility_scripts.bstack111lll1111_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll1lll_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧᬂ"): name}))
      bstack1l111ll111_opy_.end(EVENTS.bstack1l1l1l1111_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᬃ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᬄ"), True, None)
    except Exception as error:
      bstack1l111ll111_opy_.end(EVENTS.bstack1l1l1l1111_opy_.value, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᬅ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᬆ"), False, str(error))
    bstack111l1l1l1_opy_ = bstack1l111ll111_opy_.bstack111lll11lll_opy_(EVENTS.bstack1l1l1111111_opy_.value)
    bstack1l111ll111_opy_.mark(bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᬇ"))
    try:
      if (bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᬈ"), None) and bstack1l11lll1_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᬉ"), None)):
        scripts = {bstack1ll1lll_opy_ (u"࠭ࡳࡤࡣࡱࠫᬊ"): accessibility_scripts.perform_scan}
        bstack111ll1l1l11_opy_ = json.loads(scripts[bstack1ll1lll_opy_ (u"ࠢࡴࡥࡤࡲࠧᬋ")].replace(bstack1ll1lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᬌ"), bstack1ll1lll_opy_ (u"ࠤࠥᬍ")))
        bstack111ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᬎ")][bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᬏ")] = None
        scripts[bstack1ll1lll_opy_ (u"ࠧࡹࡣࡢࡰࠥᬐ")] = bstack1ll1lll_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᬑ") + json.dumps(bstack111ll1l1l11_opy_)
        accessibility_scripts.bstack111lll1111_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l11ll111ll_opy_))
      bstack1l111ll111_opy_.end(bstack111l1l1l1_opy_, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᬒ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᬓ"),True, None)
    except Exception as error:
      bstack1l111ll111_opy_.end(bstack111l1l1l1_opy_, bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᬔ"), bstack111l1l1l1_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᬕ"),False, str(error))
    logger.info(bstack1ll1lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᬖ"))
    try:
      bstack1l1l111l111_opy_ = {
        bstack1ll1lll_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨᬗ"): {
          bstack1ll1lll_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢᬘ"): bstack1ll1lll_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡁࡗࡇࡢࡖࡊ࡙ࡕࡍࡖࡖࠦᬙ"),
        },
        bstack1ll1lll_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥᬚ"): {
          bstack1ll1lll_opy_ (u"ࠤࡥࡳࡩࡿࠢᬛ"): {
            bstack1ll1lll_opy_ (u"ࠥࡱࡸ࡭ࠢᬜ"): bstack1ll1lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᬝ"),
            bstack1ll1lll_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᬞ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l1l111l111_opy_, separators=(bstack1ll1lll_opy_ (u"࠭ࠬࠨᬟ"), bstack1ll1lll_opy_ (u"ࠧ࠻ࠩᬠ"))))
    except Exception as bstack1lll1l11ll_opy_:
      logger.debug(bstack1ll1lll_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡤࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹࠠࡥࡣࡷࡥ࠿ࠦࠢᬡ") + str(bstack1lll1l11ll_opy_) + bstack1ll1lll_opy_ (u"ࠤࠥᬢ"))
  except Exception as bstack1l11ll11l11_opy_:
    logger.error(bstack1ll1lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᬣ") + str(path) + bstack1ll1lll_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᬤ") + str(bstack1l11ll11l11_opy_))
def bstack111ll1ll1l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᬥ")) and str(caps.get(bstack1ll1lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᬦ"))).lower() == bstack1ll1lll_opy_ (u"ࠢࡢࡰࡧࡶࡴ࡯ࡤࠣᬧ"):
        bstack1l1l1111l11_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠣࡣࡳࡴ࡮ࡻ࡭࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᬨ")) or caps.get(bstack1ll1lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᬩ"))
        if bstack1l1l1111l11_opy_ and int(str(bstack1l1l1111l11_opy_)) < bstack111ll11l11l_opy_:
            return False
    return True
def bstack11ll11ll_opy_(config):
  if bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᬪ") in config:
        return config[bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᬫ")]
  for platform in config.get(bstack1ll1lll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᬬ"), []):
      if bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᬭ") in platform:
          return platform[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᬮ")]
  return None
def bstack11ll1ll11l_opy_(bstack1ll1l1l11_opy_):
  try:
    browser_name = bstack1ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᬯ")]
    browser_version = bstack1ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᬰ")]
    chrome_options = bstack1ll1l1l11_opy_[bstack1ll1lll_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫᬱ")]
    try:
        bstack111lll11111_opy_ = int(browser_version.split(bstack1ll1lll_opy_ (u"ࠫ࠳࠭ᬲ"))[0])
    except ValueError as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡴࡶࡦࡴࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠤᬳ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1ll1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ᬴࠭")):
        logger.warning(bstack1ll1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᬵ"))
        return False
    if bstack111lll11111_opy_ < bstack111ll11ll1l_opy_.bstack1l11ll1llll_opy_:
        logger.warning(bstack1ll1lll_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷ࡬ࡶࡪࡹࠠࡄࡪࡵࡳࡲ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡽࢀࠤࡴࡸࠠࡩ࡫ࡪ࡬ࡪࡸ࠮ࠨᬶ").format(bstack111ll11ll1l_opy_.bstack1l11ll1llll_opy_))
        return False
    bstack111ll11111l_opy_ = chrome_options.get(bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᬷ"), []) if chrome_options else []
    if not isinstance(bstack111ll11111l_opy_, list):
        bstack111ll11111l_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack1ll1lll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᬸ") or arg == bstack1ll1lll_opy_ (u"ࠫ࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᬹ") or (arg.startswith(bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࠪᬺ")) and arg != bstack1ll1lll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࡲࡪࡽࠧᬻ")))
           for arg in bstack111ll11111l_opy_):
        logger.warning(bstack1ll1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᬼ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨᬽ") + str(e))
    return False
def bstack1l1lllll1_opy_(bstack11lll1l111_opy_, config):
    try:
      bstack1l11l1lll11_opy_ = bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᬾ") in config and config[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᬿ")] == True
      bstack111ll1l1111_opy_ = bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᭀ") in config and str(config[bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᭁ")]).lower() != bstack1ll1lll_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᭂ")
      if not (bstack1l11l1lll11_opy_ and (not bstack1111111l11_opy_(config) or bstack111ll1l1111_opy_)):
        return bstack11lll1l111_opy_
      bstack111ll1l111l_opy_ = accessibility_scripts.bstack111ll111l11_opy_
      if bstack111ll1l111l_opy_ is None:
        logger.debug(bstack1ll1lll_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥᭃ"))
        return bstack11lll1l111_opy_
      bstack111ll111111_opy_ = int(str(bstack111ll1lll1l_opy_()).split(bstack1ll1lll_opy_ (u"ࠨ࠰᭄ࠪ"))[0])
      logger.debug(bstack1ll1lll_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤᭅ") + str(bstack111ll111111_opy_) + bstack1ll1lll_opy_ (u"ࠥࠦᭆ"))
      if bstack111ll111111_opy_ == 3 and isinstance(bstack11lll1l111_opy_, dict) and bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᭇ") in bstack11lll1l111_opy_ and bstack111ll1l111l_opy_ is not None:
        if bstack1ll1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᭈ") not in bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᭉ")]:
          bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᭊ")][bstack1ll1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᭋ")] = {}
        if bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᭌ") in bstack111ll1l111l_opy_:
          if bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᭍") not in bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᭎")][bstack1ll1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᭏")]:
            bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᭐")][bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭑")][bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᭒")] = []
          for arg in bstack111ll1l111l_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᭓")]:
            if arg not in bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᭔")][bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᭕")][bstack1ll1lll_opy_ (u"ࠬࡧࡲࡨࡵࠪ᭖")]:
              bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᭗")][bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭘")][bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᭙")].append(arg)
        if bstack1ll1lll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᭚") in bstack111ll1l111l_opy_:
          if bstack1ll1lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᭛") not in bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᭜")][bstack1ll1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᭝")]:
            bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᭞")][bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭟")][bstack1ll1lll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᭠")] = []
          for ext in bstack111ll1l111l_opy_[bstack1ll1lll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᭡")]:
            if ext not in bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᭢")][bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᭣")][bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᭤")]:
              bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᭥")][bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭦")][bstack1ll1lll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᭧")].append(ext)
        if bstack1ll1lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᭨") in bstack111ll1l111l_opy_:
          if bstack1ll1lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᭩") not in bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᭪")][bstack1ll1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᭫")]:
            bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ᭬࠭")][bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭭")][bstack1ll1lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᭮")] = {}
          bstack111ll111ll1_opy_(bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᭯")][bstack1ll1lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭰")][bstack1ll1lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᭱")],
                    bstack111ll1l111l_opy_[bstack1ll1lll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᭲")])
        os.environ[bstack1ll1lll_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫ᭳")] = bstack1ll1lll_opy_ (u"ࠧࡵࡴࡸࡩࠬ᭴")
        return bstack11lll1l111_opy_
      else:
        chrome_options = None
        if isinstance(bstack11lll1l111_opy_, ChromeOptions):
          chrome_options = bstack11lll1l111_opy_
        elif isinstance(bstack11lll1l111_opy_, dict):
          for value in bstack11lll1l111_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11lll1l111_opy_, dict):
            bstack11lll1l111_opy_[bstack1ll1lll_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᭵")] = chrome_options
          else:
            bstack11lll1l111_opy_ = chrome_options
        if bstack111ll1l111l_opy_ is not None:
          if bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᭶") in bstack111ll1l111l_opy_:
                bstack111ll1ll111_opy_ = chrome_options.arguments or []
                new_args = bstack111ll1l111l_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᭷")]
                for arg in new_args:
                    if arg not in bstack111ll1ll111_opy_:
                        chrome_options.add_argument(arg)
          if bstack1ll1lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᭸") in bstack111ll1l111l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᭹"), [])
                bstack111ll11l1l1_opy_ = bstack111ll1l111l_opy_[bstack1ll1lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᭺")]
                for extension in bstack111ll11l1l1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1ll1lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᭻") in bstack111ll1l111l_opy_:
                bstack111ll111l1l_opy_ = chrome_options.experimental_options.get(bstack1ll1lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᭼"), {})
                bstack111ll11ll11_opy_ = bstack111ll1l111l_opy_[bstack1ll1lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᭽")]
                bstack111ll111ll1_opy_(bstack111ll111l1l_opy_, bstack111ll11ll11_opy_)
                chrome_options.add_experimental_option(bstack1ll1lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᭾"), bstack111ll111l1l_opy_)
        os.environ[bstack1ll1lll_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩ᭿")] = bstack1ll1lll_opy_ (u"ࠬࡺࡲࡶࡧࠪᮀ")
        return bstack11lll1l111_opy_
    except Exception as e:
      logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦᮁ") + str(e))
      return bstack11lll1l111_opy_