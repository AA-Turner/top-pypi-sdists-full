# coding: UTF-8
import sys
bstack11ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1ll_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack1l1_opy_ (bstack1111l11_opy_):
    global bstack111l1ll_opy_
    bstack1l111l1_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1llll11_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l1l111_opy_ = bstack1l111l1_opy_ % len (bstack1llll11_opy_)
    bstack11l1l_opy_ = bstack1llll11_opy_ [:bstack1l1l111_opy_] + bstack1llll11_opy_ [bstack1l1l111_opy_:]
    if bstack11ll11_opy_:
        bstack11lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11lll11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1ll_opy_ - (bstack111l1l1_opy_ + bstack1l111l1_opy_) % bstack1ll11_opy_) for bstack111l1l1_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11lll11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111lll11111_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack111lll1ll1l_opy_ as bstack111ll1lllll_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import current_time, bstack1lllll11ll1_opy_, bstack111l11ll_opy_, bstack111ll1ll111_opy_, \
  bstack111ll1lll1l_opy_, bstack11l1l111ll_opy_, get_host_info, bstack111ll11l1l1_opy_, bstack1l111l1111_opy_, error_handler, bstack111lll11lll_opy_, bstack111ll11llll_opy_, bstack1l1lll111l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11l1l1ll_opy_ import bstack111l1111l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack11l1l1ll_opy_ = bstack111l1111l_opy_()
@error_handler(class_method=False)
def _111ll1ll1ll_opy_(driver, bstack1lll11lllll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧ᨜"): caps.get(bstack1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭᨝"), None),
        bstack1l1_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᨞"): bstack1lll11lllll_opy_.get(bstack1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᨟"), None),
        bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᨠ"): caps.get(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᨡ"), None),
        bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᨢ"): caps.get(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᨣ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᨤ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᨥ"), None) is None or os.environ[bstack1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᨦ")] == bstack1l1_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᨧ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᨨ"), False) or any([p.get(bstack1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨩ"), False) == True for p in config.get(bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᨪ"), [])])
def is_enabled_platform(config, bstack1ll11l11ll_opy_):
  try:
    bstack111ll1l1ll1_opy_ = config.get(bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨫ"), False)
    _111llll1111_opy_ = int(bstack1ll11l11ll_opy_)
    if _111llll1111_opy_ < 0:
      _111llll1111_opy_ = 0
    bstack1ll111ll_opy_ = config.get(bstack1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᨬ"), [])
    if _111llll1111_opy_ < len(bstack1ll111ll_opy_) and bstack1ll111ll_opy_[_111llll1111_opy_]:
      bstack111ll11ll1l_opy_ = bstack1ll111ll_opy_[_111llll1111_opy_].get(bstack1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᨭ"), None)
    else:
      bstack111ll11ll1l_opy_ = config.get(bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᨮ"), None)
    if bstack111ll11ll1l_opy_ != None:
      bstack111ll1l1ll1_opy_ = bstack111ll11ll1l_opy_
    bstack111ll11l111_opy_ = os.getenv(bstack1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᨯ")) is not None and len(os.getenv(bstack1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᨰ"))) > 0 and os.getenv(bstack1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᨱ")) != bstack1l1_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᨲ")
    return bstack111ll1l1ll1_opy_ and bstack111ll11l111_opy_
  except Exception as error:
    logger.debug(bstack1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᨳ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l11llll11l_opy_ = os.getenv(bstack1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᨴ"))
  if bstack1l11llll11l_opy_ is None:
    return True
  bstack1l11llll11l_opy_ = json.loads(bstack1l11llll11l_opy_)
  try:
    include_tags = bstack1l11llll11l_opy_[bstack1l1_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᨵ")] if bstack1l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᨶ") in bstack1l11llll11l_opy_ and isinstance(bstack1l11llll11l_opy_[bstack1l1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᨷ")], list) else []
    exclude_tags = bstack1l11llll11l_opy_[bstack1l1_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᨸ")] if bstack1l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᨹ") in bstack1l11llll11l_opy_ and isinstance(bstack1l11llll11l_opy_[bstack1l1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᨺ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᨻ") + str(error))
  return False
def bstack111ll1l1lll_opy_(config, bstack111ll11lll1_opy_, bstack111ll1l1111_opy_, bstack111ll1ll11l_opy_):
  bstack111ll1ll1l1_opy_ = bstack111ll1ll111_opy_(config)
  bstack111ll1lll11_opy_ = bstack111ll1lll1l_opy_(config)
  if bstack111ll1ll1l1_opy_ is None or bstack111ll1lll11_opy_ is None:
    logger.error(bstack1l1_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᨼ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᨽ"), bstack1l1_opy_ (u"ࠬࢁࡽࠨᨾ")))
    data = {
        bstack1l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᨿ"): config[bstack1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᩀ")],
        bstack1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᩁ"): config.get(bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᩂ"), os.path.basename(os.getcwd())),
        bstack1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᩃ"): current_time(),
        bstack1l1_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᩄ"): config.get(bstack1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᩅ"), bstack1l1_opy_ (u"࠭ࠧᩆ")),
        bstack1l1_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᩇ"): {
            bstack1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᩈ"): bstack111ll11lll1_opy_,
            bstack1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᩉ"): bstack111ll1l1111_opy_,
            bstack1l1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᩊ"): __version__,
            bstack1l1_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᩋ"): bstack1l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᩌ"),
            bstack1l1_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᩍ"): bstack1l1_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᩎ"),
            bstack1l1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᩏ"): bstack111ll1ll11l_opy_
        },
        bstack1l1_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᩐ"): settings,
        bstack1l1_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᩑ"): bstack111ll11l1l1_opy_(),
        bstack1l1_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᩒ"): bstack11l1l111ll_opy_(),
        bstack1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᩓ"): get_host_info(),
        bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᩔ"): bstack111l11ll_opy_(config)
    }
    headers = {
        bstack1l1_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᩕ"): bstack1l1_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᩖ"),
    }
    config = {
        bstack1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᩗ"): (bstack111ll1ll1l1_opy_, bstack111ll1lll11_opy_),
        bstack1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᩘ"): headers
    }
    response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠫࡕࡕࡓࡕࠩᩙ"), bstack111ll1lllll_opy_ + bstack1l1_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᩚ"), data, config)
    bstack111ll1l111l_opy_ = response.json()
    if bstack111ll1l111l_opy_[bstack1l1_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᩛ")]:
      parsed = json.loads(os.getenv(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᩜ"), bstack1l1_opy_ (u"ࠨࡽࢀࠫᩝ")))
      parsed[bstack1l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᩞ")] = bstack111ll1l111l_opy_[bstack1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨ᩟")][bstack1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ᩠ࠬ")]
      os.environ[bstack1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᩡ")] = json.dumps(parsed)
      accessibility_scripts.bstack1llll11ll_opy_(bstack111ll1l111l_opy_[bstack1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᩢ")][bstack1l1_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᩣ")])
      accessibility_scripts.bstack111llll11l1_opy_(bstack111ll1l111l_opy_[bstack1l1_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᩤ")][bstack1l1_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᩥ")])
      accessibility_scripts.store()
      return bstack111ll1l111l_opy_[bstack1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨᩦ")][bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᩧ")], bstack111ll1l111l_opy_[bstack1l1_opy_ (u"ࠬࡪࡡࡵࡣࠪᩨ")][bstack1l1_opy_ (u"࠭ࡩࡥࠩᩩ")]
    else:
      logger.error(bstack1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᩪ") + bstack111ll1l111l_opy_[bstack1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᩫ")])
      if bstack111ll1l111l_opy_[bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᩬ")] == bstack1l1_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᩭ"):
        for bstack111lll1l111_opy_ in bstack111ll1l111l_opy_[bstack1l1_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᩮ")]:
          logger.error(bstack111lll1l111_opy_[bstack1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᩯ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᩰ") +  str(error))
    return None, None
def bstack111llll111l_opy_():
  if os.getenv(bstack1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᩱ")) is None:
    return {
        bstack1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᩲ"): bstack1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᩳ"),
        bstack1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᩴ"): bstack1l1_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪ᩵")
    }
  data = {bstack1l1_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭᩶"): current_time()}
  headers = {
      bstack1l1_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᩷"): bstack1l1_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨ᩸") + os.getenv(bstack1l1_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨ᩹")),
      bstack1l1_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ᩺"): bstack1l1_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭᩻")
  }
  response = bstack1l111l1111_opy_(bstack1l1_opy_ (u"ࠫࡕ࡛ࡔࠨ᩼"), bstack111ll1lllll_opy_ + bstack1l1_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧ᩽"), data, { bstack1l1_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ᩾"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺ᩿ࠠࠣ") + bstack1lllll11ll1_opy_().isoformat() + bstack1l1_opy_ (u"ࠨ࡜ࠪ᪀"))
      return {bstack1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᪁"): bstack1l1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ᪂"), bstack1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᪃"): bstack1l1_opy_ (u"ࠬ࠭᪄")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤ᪅") + str(error))
    return {
        bstack1l1_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ᪆"): bstack1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᪇"),
        bstack1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᪈"): str(error)
    }
def bstack111lll11l11_opy_(bstack111lll111l1_opy_):
    return re.match(bstack1l1_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫ᪉"), bstack111lll111l1_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack111ll1llll1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack111ll1llll1_opy_ = desired_capabilities
        else:
          bstack111ll1llll1_opy_ = {}
        bstack1l11l1llll1_opy_ = (bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᪊"), bstack1l1_opy_ (u"ࠬ࠭᪋")).lower() or caps.get(bstack1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ᪌"), bstack1l1_opy_ (u"ࠧࠨ᪍")).lower())
        if bstack1l11l1llll1_opy_ == bstack1l1_opy_ (u"ࠨ࡫ࡲࡷࠬ᪎"):
            return True
        if bstack1l11l1llll1_opy_ == bstack1l1_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪ᪏"):
            bstack1l11ll1111l_opy_ = str(float(caps.get(bstack1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᪐")) or bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᪑"), {}).get(bstack1l1_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᪒"),bstack1l1_opy_ (u"࠭ࠧ᪓"))))
            if bstack1l11l1llll1_opy_ == bstack1l1_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨ᪔") and int(bstack1l11ll1111l_opy_.split(bstack1l1_opy_ (u"ࠨ࠰ࠪ᪕"))[0]) < float(bstack111ll11ll11_opy_):
                logger.warning(str(bstack111ll11l11l_opy_))
                return False
            return True
        bstack1l1l111l1l1_opy_ = caps.get(bstack1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᪖"), {}).get(bstack1l1_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ᪗"), caps.get(bstack1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ᪘"), bstack1l1_opy_ (u"ࠬ࠭᪙")))
        if bstack1l1l111l1l1_opy_:
            logger.warning(bstack1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᪚"))
            return False
        browser = (caps.get(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᪛"), bstack1l1_opy_ (u"ࠨࠩ᪜")) or caps.get(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ᪝"), bstack1l1_opy_ (u"ࠪࠫ᪞"))).lower() or \
                  (bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ᪟"), bstack1l1_opy_ (u"ࠬ࠭᪠")) or bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᪡"), bstack1l1_opy_ (u"ࠧࠨ᪢"))).lower()
        if browser not in (bstack1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ᪣"), bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫ᪤"), bstack1l1_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩ᪥")):
            logger.warning(bstack1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ᪦"))
            return False
        browser_version = caps.get(bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᪧ")) or caps.get(bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᪨")) or bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᪩")) or bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᪪"), {}).get(bstack1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᪫")) or bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᪬"), {}).get(bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᪭"))
        bstack1l1l1111111_opy_ = bstack111lll11111_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack111lll1llll_opy_ = False
        if config is not None:
          bstack111lll1llll_opy_ = bstack1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᪮") in config and str(config[bstack1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᪯")]).lower() != bstack1l1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭᪰")
        if os.environ.get(bstack1l1_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭᪱"), bstack1l1_opy_ (u"ࠩࠪ᪲")).lower() == bstack1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨ᪳") or bstack111lll1llll_opy_:
          bstack1l1l1111111_opy_ = bstack111lll11111_opy_.bstack1l11ll1l11l_opy_
        if browser_version and browser_version != bstack1l1_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫ᪴") and int(browser_version.split(bstack1l1_opy_ (u"ࠬ࠴᪵ࠧ"))[0]) <= bstack1l1l1111111_opy_:
          logger.warning(bstack1l1_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼࡿ࠱᪶ࠫ").format(bstack1l1l1111111_opy_))
          return False
        bstack1l1l1111ll1_opy_ = (caps.get(bstack1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷ᪷ࠬ"))
                         or bstack111ll1llll1_opy_.get(bstack1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ᪸࠭"), {})
                         or caps.get(bstack1l1_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ᪹ࠩ"), {}))
        bstack111lll111ll_opy_ = bstack1l1l1111ll1_opy_.get(bstack1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᪺"), []) if isinstance(bstack1l1l1111ll1_opy_, dict) else []
        if not isinstance(bstack111lll111ll_opy_, list):
            bstack111lll111ll_opy_ = []
        if any(isinstance(arg, str) and (arg == bstack1l1_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨ᪻") or arg == bstack1l1_opy_ (u"ࠬ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ᪼") or (arg.startswith(bstack1l1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀ᪽ࠫ")) and arg != bstack1l1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨ᪾")))
               for arg in bstack111lll111ll_opy_):
            logger.warning(bstack1l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ᪿࠥ"))
            return False
        return True
    except Exception as error:
        logger.debug(bstack1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ᫀࠦ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1l1l1ll11_opy_ = config.get(bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᫁"), {})
    bstack1l1l1l1ll11_opy_[bstack1l1_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧ᫂")] = os.getenv(bstack1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖ᫃ࠪ"))
    bstack11l1l1ll1_opy_ = json.loads(os.getenv(bstack1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒ᫄ࠧ"), bstack1l1_opy_ (u"ࠧࡼࡿࠪ᫅"))).get(bstack1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᫆"))
    if not config[bstack1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫ᫇")].get(bstack1l1_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤ᫈")):
      if bstack1l1_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᫉") in caps:
        caps[bstack1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ᫊࠭")][bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭᫋")] = bstack1l1l1l1ll11_opy_
        caps[bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᫌ")][bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᫍ")][bstack1l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᫎ")] = bstack11l1l1ll1_opy_
      else:
        caps[bstack1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫏")] = bstack1l1l1l1ll11_opy_
        caps[bstack1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᫐")][bstack1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᫑")] = bstack11l1l1ll1_opy_
  except Exception as error:
    logger.debug(bstack1l1_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢ᫒") +  str(error))
def start_test_capture(driver, bstack111lll1lll1_opy_):
  try:
    setattr(driver, bstack1l1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧ᫓"), True)
    session = driver.session_id
    if session:
      bstack111ll1l11ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111ll1l11ll_opy_ = False
      bstack111ll1l11ll_opy_ = url.scheme in [bstack1l1_opy_ (u"ࠣࡪࡷࡸࡵࠨ᫔"), bstack1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣ᫕")]
      if bstack111ll1l11ll_opy_:
        if bstack111lll1lll1_opy_:
          logger.info(bstack1l1_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥ᫖"))
      return bstack111lll1lll1_opy_
  except Exception as e:
    logger.error(bstack1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢ᫗") + str(e))
    return False
def bstack11l1lll1l_opy_(driver, name, path):
  try:
    bstack1l1l11ll1ll_opy_ = {
        bstack1l1_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬ᫘"): threading.current_thread().current_test_uuid,
        bstack1l1_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫ᫙"): os.environ.get(bstack1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬ᫚"), bstack1l1_opy_ (u"ࠨࠩ᫛")),
        bstack1l1_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭᫜"): os.environ.get(bstack1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧ᫝"), bstack1l1_opy_ (u"ࠫࠬ᫞"))
    }
    bstack111l1l111_opy_ = bstack11l1l1ll_opy_.bstack1ll1l1l1l_opy_(EVENTS.bstack11l1l11l11_opy_.value)
    logger.debug(bstack1l1_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨ᫟"))
    try:
      if (bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᫠"), None) and bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᫡"), None)):
        scripts = {bstack1l1_opy_ (u"ࠨࡵࡦࡥࡳ࠭᫢"): accessibility_scripts.perform_scan}
        bstack111ll1l1l1l_opy_ = json.loads(scripts[bstack1l1_opy_ (u"ࠤࡶࡧࡦࡴࠢ᫣")].replace(bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨ᫤"), bstack1l1_opy_ (u"ࠦࠧ᫥")))
        bstack111ll1l1l1l_opy_[bstack1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨ᫦")][bstack1l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭᫧")] = None
        scripts[bstack1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧ᫨")] = bstack1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᫩") + json.dumps(bstack111ll1l1l1l_opy_)
        accessibility_scripts.bstack1llll11ll_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1l1_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤ᫪"): name}))
      bstack11l1l1ll_opy_.end(EVENTS.bstack11l1l11l11_opy_.value, bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᫫"), bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᫬"), True, None)
    except Exception as error:
      bstack11l1l1ll_opy_.end(EVENTS.bstack11l1l11l11_opy_.value, bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᫭"), bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᫮"), False, str(error))
    bstack111l1l111_opy_ = bstack11l1l1ll_opy_.bstack111ll1l1l11_opy_(EVENTS.bstack1l1l111ll1l_opy_.value)
    bstack11l1l1ll_opy_.mark(bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᫯"))
    try:
      if (bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ᫰"), None) and bstack1l1lll111l_opy_(threading.current_thread(), bstack1l1_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᫱"), None)):
        scripts = {bstack1l1_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ᫲"): accessibility_scripts.perform_scan}
        bstack111ll1l1l1l_opy_ = json.loads(scripts[bstack1l1_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ᫳")].replace(bstack1l1_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣ᫴"), bstack1l1_opy_ (u"ࠨࠢ᫵")))
        bstack111ll1l1l1l_opy_[bstack1l1_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ᫶")][bstack1l1_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ᫷")] = None
        scripts[bstack1l1_opy_ (u"ࠤࡶࡧࡦࡴࠢ᫸")] = bstack1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨ᫹") + json.dumps(bstack111ll1l1l1l_opy_)
        accessibility_scripts.bstack1llll11ll_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l1l11ll1ll_opy_))
      bstack11l1l1ll_opy_.end(bstack111l1l111_opy_, bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᫺"), bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᫻"),True, None)
    except Exception as error:
      bstack11l1l1ll_opy_.end(bstack111l1l111_opy_, bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᫼"), bstack111l1l111_opy_ + bstack1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᫽"),False, str(error))
    logger.info(bstack1l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦ᫾"))
    try:
      bstack1l11l1ll11l_opy_ = {
        bstack1l1_opy_ (u"ࠤࡵࡩࡶࡻࡥࡴࡶࠥ᫿"): {
          bstack1l1_opy_ (u"ࠥࡧࡴࡳ࡭ࡢࡰࡧࠦᬀ"): bstack1l1_opy_ (u"ࠦࡆ࠷࠱࡚ࡡࡖࡅ࡛ࡋ࡟ࡓࡇࡖ࡙ࡑ࡚ࡓࠣᬁ"),
        },
        bstack1l1_opy_ (u"ࠧࡸࡥࡴࡲࡲࡲࡸ࡫ࠢᬂ"): {
          bstack1l1_opy_ (u"ࠨࡢࡰࡦࡼࠦᬃ"): {
            bstack1l1_opy_ (u"ࠢ࡮ࡵࡪࠦᬄ"): bstack1l1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᬅ"),
            bstack1l1_opy_ (u"ࠤࡶࡹࡨࡩࡥࡴࡵࠥᬆ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l11l1ll11l_opy_, separators=(bstack1l1_opy_ (u"ࠪ࠰ࠬᬇ"), bstack1l1_opy_ (u"ࠫ࠿࠭ᬈ"))))
    except Exception as bstack1111ll11ll_opy_:
      logger.debug(bstack1l1_opy_ (u"ࠧࡌࡡࡪ࡮ࡨࡨࠥࡺ࡯ࠡ࡮ࡲ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡡࡷࡧࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡩࡧࡴࡢ࠼ࠣࠦᬉ") + str(bstack1111ll11ll_opy_) + bstack1l1_opy_ (u"ࠨࠢᬊ"))
  except Exception as bstack1l11ll11l1l_opy_:
    logger.error(bstack1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᬋ") + str(path) + bstack1l1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᬌ") + str(bstack1l11ll11l1l_opy_))
def bstack111lll1111l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᬍ")) and str(caps.get(bstack1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᬎ"))).lower() == bstack1l1_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᬏ"):
        bstack1l11ll1111l_opy_ = caps.get(bstack1l1_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᬐ")) or caps.get(bstack1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᬑ"))
        if bstack1l11ll1111l_opy_ and int(str(bstack1l11ll1111l_opy_)) < bstack111ll11ll11_opy_:
            return False
    return True
def bstack1l11ll1l1_opy_(config):
  if bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᬒ") in config:
        return config[bstack1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᬓ")]
  for platform in config.get(bstack1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᬔ"), []):
      if bstack1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᬕ") in platform:
          return platform[bstack1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᬖ")]
  return None
def bstack1ll1111l1l_opy_(bstack111lll1l1l_opy_):
  try:
    browser_name = bstack111lll1l1l_opy_[bstack1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᬗ")]
    browser_version = bstack111lll1l1l_opy_[bstack1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᬘ")]
    chrome_options = bstack111lll1l1l_opy_[bstack1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᬙ")]
    try:
        bstack111lll1ll11_opy_ = int(browser_version.split(bstack1l1_opy_ (u"ࠨ࠰ࠪᬚ"))[0])
    except ValueError as e:
        logger.error(bstack1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨᬛ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᬜ")):
        logger.warning(bstack1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᬝ"))
        return False
    if bstack111lll1ll11_opy_ < bstack111lll11111_opy_.bstack1l11ll1l11l_opy_:
        logger.warning(bstack1l1_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡽࠡࡱࡵࠤ࡭࡯ࡧࡩࡧࡵ࠲ࠬᬞ").format(bstack111lll11111_opy_.bstack1l11ll1l11l_opy_))
        return False
    bstack111lll111ll_opy_ = chrome_options.get(bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫᬟ"), []) if chrome_options else []
    if not isinstance(bstack111lll111ll_opy_, list):
        bstack111lll111ll_opy_ = []
    if any(isinstance(arg, str) and (arg == bstack1l1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᬠ") or arg == bstack1l1_opy_ (u"ࠨࡪࡨࡥࡩࡲࡥࡴࡵࠪᬡ") or (arg.startswith(bstack1l1_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃࠧᬢ")) and arg != bstack1l1_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ࠽࡯ࡧࡺࠫᬣ")))
           for arg in bstack111lll111ll_opy_):
        logger.warning(bstack1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᬤ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥ࡬࡯ࡳࠢ࡯ࡳࡨࡧ࡬ࠡࡅ࡫ࡶࡴࡳࡥ࠻ࠢࠥᬥ") + str(e))
    return False
def bstack11111ll1l_opy_(bstack1lllll11l_opy_, config):
    try:
      bstack1l11ll11111_opy_ = bstack1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᬦ") in config and config[bstack1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᬧ")] == True
      bstack111lll1llll_opy_ = bstack1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᬨ") in config and str(config[bstack1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᬩ")]).lower() != bstack1l1_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩᬪ")
      if not (bstack1l11ll11111_opy_ and (not bstack111l11ll_opy_(config) or bstack111lll1llll_opy_)):
        return bstack1lllll11l_opy_
      bstack111lll1l11l_opy_ = accessibility_scripts.bstack111lll1l1ll_opy_
      if bstack111lll1l11l_opy_ is None:
        logger.debug(bstack1l1_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥࡧࡲࡦࠢࡑࡳࡳ࡫ࠢᬫ"))
        return bstack1lllll11l_opy_
      bstack111lll11l1l_opy_ = int(str(bstack111ll11llll_opy_()).split(bstack1l1_opy_ (u"ࠬ࠴ࠧᬬ"))[0])
      logger.debug(bstack1l1_opy_ (u"ࠨࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࠨᬭ") + str(bstack111lll11l1l_opy_) + bstack1l1_opy_ (u"ࠢࠣᬮ"))
      if bstack111lll11l1l_opy_ == 3 and isinstance(bstack1lllll11l_opy_, dict) and bstack1l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᬯ") in bstack1lllll11l_opy_ and bstack111lll1l11l_opy_ is not None:
        if bstack1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᬰ") not in bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬱ")]:
          bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᬲ")][bstack1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᬳ")] = {}
        if bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶ᬴ࠫ") in bstack111lll1l11l_opy_:
          if bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬᬵ") not in bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᬶ")][bstack1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᬷ")]:
            bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬸ")][bstack1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬹ")][bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᬺ")] = []
          for arg in bstack111lll1l11l_opy_[bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫᬻ")]:
            if arg not in bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᬼ")][bstack1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬽ")][bstack1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᬾ")]:
              bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬿ")][bstack1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᭀ")][bstack1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᭁ")].append(arg)
        if bstack1l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᭂ") in bstack111lll1l11l_opy_:
          if bstack1l1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᭃ") not in bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᭄")][bstack1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᭅ")]:
            bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᭆ")][bstack1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᭇ")][bstack1l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᭈ")] = []
          for ext in bstack111lll1l11l_opy_[bstack1l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᭉ")]:
            if ext not in bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᭊ")][bstack1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᭋ")][bstack1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᭌ")]:
              bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᭍")][bstack1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᭎")][bstack1l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᭏")].append(ext)
        if bstack1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᭐") in bstack111lll1l11l_opy_:
          if bstack1l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᭑") not in bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᭒")][bstack1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᭓")]:
            bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᭔")][bstack1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᭕")][bstack1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᭖")] = {}
          bstack111lll11lll_opy_(bstack1lllll11l_opy_[bstack1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᭗")][bstack1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᭘")][bstack1l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᭙")],
                    bstack111lll1l11l_opy_[bstack1l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᭚")])
        os.environ[bstack1l1_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨ᭛")] = bstack1l1_opy_ (u"ࠫࡹࡸࡵࡦࠩ᭜")
        return bstack1lllll11l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1lllll11l_opy_, ChromeOptions):
          chrome_options = bstack1lllll11l_opy_
        elif isinstance(bstack1lllll11l_opy_, dict):
          for value in bstack1lllll11l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1lllll11l_opy_, dict):
            bstack1lllll11l_opy_[bstack1l1_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭᭝")] = chrome_options
          else:
            bstack1lllll11l_opy_ = chrome_options
        if bstack111lll1l11l_opy_ is not None:
          if bstack1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫ᭞") in bstack111lll1l11l_opy_:
                bstack111lll11ll1_opy_ = chrome_options.arguments or []
                new_args = bstack111lll1l11l_opy_[bstack1l1_opy_ (u"ࠧࡢࡴࡪࡷࠬ᭟")]
                for arg in new_args:
                    if arg not in bstack111lll11ll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᭠") in bstack111lll1l11l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᭡"), [])
                bstack111lll1l1l1_opy_ = bstack111lll1l11l_opy_[bstack1l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᭢")]
                for extension in bstack111lll1l1l1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᭣") in bstack111lll1l11l_opy_:
                bstack111ll1l11l1_opy_ = chrome_options.experimental_options.get(bstack1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᭤"), {})
                bstack111ll11l1ll_opy_ = bstack111lll1l11l_opy_[bstack1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᭥")]
                bstack111lll11lll_opy_(bstack111ll1l11l1_opy_, bstack111ll11l1ll_opy_)
                chrome_options.add_experimental_option(bstack1l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᭦"), bstack111ll1l11l1_opy_)
        os.environ[bstack1l1_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭᭧")] = bstack1l1_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ᭨")
        return bstack1lllll11l_opy_
    except Exception as e:
      logger.error(bstack1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡧࡨ࡮ࡴࡧࠡࡰࡲࡲ࠲ࡈࡓࠡ࡫ࡱࡪࡷࡧࠠࡢ࠳࠴ࡽࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠣ᭩") + str(e))
      return bstack1lllll11l_opy_