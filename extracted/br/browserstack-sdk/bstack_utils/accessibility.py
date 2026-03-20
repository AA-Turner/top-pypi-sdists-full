# coding: UTF-8
import sys
bstack111l1l_opy_ = sys.version_info [0] == 2
bstack1111l11_opy_ = 2048
bstackl_opy_ = 7
def bstack11lll1_opy_ (bstack1l1l111_opy_):
    global bstack11l1l1_opy_
    bstack1111l_opy_ = ord (bstack1l1l111_opy_ [-1])
    bstack1l111_opy_ = bstack1l1l111_opy_ [:-1]
    bstack11111ll_opy_ = bstack1111l_opy_ % len (bstack1l111_opy_)
    bstack111l_opy_ = bstack1l111_opy_ [:bstack11111ll_opy_] + bstack1l111_opy_ [bstack11111ll_opy_:]
    if bstack111l1l_opy_:
        bstack1llll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    else:
        bstack1llll11_opy_ = str () .join ([chr (ord (char) - bstack1111l11_opy_ - (bstack111llll_opy_ + bstack1111l_opy_) % bstackl_opy_) for bstack111llll_opy_, char in enumerate (bstack111l_opy_)])
    return eval (bstack1llll11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111ll1ll1ll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack111lll1llll_opy_ as bstack111ll11llll_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import current_time, bstack1lllll111l1_opy_, bstack1ll111l11l_opy_, bstack111llll11l1_opy_, \
  bstack111ll1l1l11_opy_, bstack11l111111_opy_, get_host_info, bstack111ll1ll111_opy_, bstack11l1lll11_opy_, error_handler, bstack111lll11111_opy_, bstack111lll1l11l_opy_, bstack111ll1ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1lll11lll_opy_ import bstack1llll11l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1lll11lll_opy_ = bstack1llll11l_opy_()
@error_handler(class_method=False)
def _111ll1lllll_opy_(driver, bstack1lll111l1ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11lll1_opy_ (u"ࠪࡳࡸࡥ࡮ࡢ࡯ࡨࠫᨙ"): caps.get(bstack11lll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᨚ"), None),
        bstack11lll1_opy_ (u"ࠬࡵࡳࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᨛ"): bstack1lll111l1ll_opy_.get(bstack11lll1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩ᨜"), None),
        bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭᨝"): caps.get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᨞"), None),
        bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᨟"): caps.get(bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᨠ"), None)
    }
  except Exception as error:
    logger.debug(bstack11lll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡪࡪࡺࡣࡩ࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡥࡧࡷࡥ࡮ࡲࡳࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᨡ") + str(error))
  return response
def on():
    if os.environ.get(bstack11lll1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᨢ"), None) is None or os.environ[bstack11lll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᨣ")] == bstack11lll1_opy_ (u"ࠢ࡯ࡷ࡯ࡰࠧᨤ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᨥ"), False) or any([p.get(bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᨦ"), False) == True for p in config.get(bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᨧ"), [])])
def is_enabled_platform(config, bstack11l111lll1_opy_):
  try:
    bstack111ll1l1l1l_opy_ = config.get(bstack11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᨨ"), False)
    _111ll11ll11_opy_ = int(bstack11l111lll1_opy_)
    if _111ll11ll11_opy_ < 0:
      _111ll11ll11_opy_ = 0
    bstack11l1l1ll11_opy_ = config.get(bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᨩ"), [])
    if _111ll11ll11_opy_ < len(bstack11l1l1ll11_opy_) and bstack11l1l1ll11_opy_[_111ll11ll11_opy_]:
      bstack111ll1llll1_opy_ = bstack11l1l1ll11_opy_[_111ll11ll11_opy_].get(bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᨪ"), None)
    else:
      bstack111ll1llll1_opy_ = config.get(bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨫ"), None)
    if bstack111ll1llll1_opy_ != None:
      bstack111ll1l1l1l_opy_ = bstack111ll1llll1_opy_
    bstack111lll1l1l1_opy_ = os.getenv(bstack11lll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᨬ")) is not None and len(os.getenv(bstack11lll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᨭ"))) > 0 and os.getenv(bstack11lll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᨮ")) != bstack11lll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᨯ")
    return bstack111ll1l1l1l_opy_ and bstack111lll1l1l1_opy_
  except Exception as error:
    logger.debug(bstack11lll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᨰ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l11lll1l1l_opy_ = os.getenv(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᨱ"))
  if bstack1l11lll1l1l_opy_ is None:
    return True
  bstack1l11lll1l1l_opy_ = json.loads(bstack1l11lll1l1l_opy_)
  try:
    include_tags = bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᨲ")] if bstack11lll1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᨳ") in bstack1l11lll1l1l_opy_ and isinstance(bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᨴ")], list) else []
    exclude_tags = bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᨵ")] if bstack11lll1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᨶ") in bstack1l11lll1l1l_opy_ and isinstance(bstack1l11lll1l1l_opy_[bstack11lll1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᨷ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11lll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᨸ") + str(error))
  return False
def bstack111ll1lll1l_opy_(config, bstack111lll11l11_opy_, bstack111lll1l1ll_opy_, bstack111lll1l111_opy_):
  bstack111ll11lll1_opy_ = bstack111llll11l1_opy_(config)
  bstack111llll111l_opy_ = bstack111ll1l1l11_opy_(config)
  if bstack111ll11lll1_opy_ is None or bstack111llll111l_opy_ is None:
    logger.error(bstack11lll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᨹ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11lll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᨺ"), bstack11lll1_opy_ (u"ࠩࡾࢁࠬᨻ")))
    data = {
        bstack11lll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᨼ"): config[bstack11lll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᨽ")],
        bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᨾ"): config.get(bstack11lll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᨿ"), os.path.basename(os.getcwd())),
        bstack11lll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪᩀ"): current_time(),
        bstack11lll1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᩁ"): config.get(bstack11lll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᩂ"), bstack11lll1_opy_ (u"ࠪࠫᩃ")),
        bstack11lll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᩄ"): {
            bstack11lll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᩅ"): bstack111lll11l11_opy_,
            bstack11lll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᩆ"): bstack111lll1l1ll_opy_,
            bstack11lll1_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᩇ"): __version__,
            bstack11lll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᩈ"): bstack11lll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᩉ"),
            bstack11lll1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᩊ"): bstack11lll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᩋ"),
            bstack11lll1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᩌ"): bstack111lll1l111_opy_
        },
        bstack11lll1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᩍ"): settings,
        bstack11lll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨᩎ"): bstack111ll1ll111_opy_(),
        bstack11lll1_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨᩏ"): bstack11l111111_opy_(),
        bstack11lll1_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫᩐ"): get_host_info(),
        bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᩑ"): bstack1ll111l11l_opy_(config)
    }
    headers = {
        bstack11lll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᩒ"): bstack11lll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᩓ"),
    }
    config = {
        bstack11lll1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᩔ"): (bstack111ll11lll1_opy_, bstack111llll111l_opy_),
        bstack11lll1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᩕ"): headers
    }
    response = bstack11l1lll11_opy_(bstack11lll1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᩖ"), bstack111ll11llll_opy_ + bstack11lll1_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩᩗ"), data, config)
    bstack111llll1l11_opy_ = response.json()
    if bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᩘ")]:
      parsed = json.loads(os.getenv(bstack11lll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᩙ"), bstack11lll1_opy_ (u"ࠬࢁࡽࠨᩚ")))
      parsed[bstack11lll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᩛ")] = bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠧࡥࡣࡷࡥࠬᩜ")][bstack11lll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᩝ")]
      os.environ[bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᩞ")] = json.dumps(parsed)
      accessibility_scripts.bstack11lll1l11_opy_(bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠪࡨࡦࡺࡡࠨ᩟")][bstack11lll1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷ᩠ࠬ")])
      accessibility_scripts.bstack111ll1lll11_opy_(bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠬࡪࡡࡵࡣࠪᩡ")][bstack11lll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᩢ")])
      accessibility_scripts.store()
      return bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠧࡥࡣࡷࡥࠬᩣ")][bstack11lll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᩤ")], bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠩࡧࡥࡹࡧࠧᩥ")][bstack11lll1_opy_ (u"ࠪ࡭ࡩ࠭ᩦ")]
    else:
      logger.error(bstack11lll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬᩧ") + bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᩨ")])
      if bstack111llll1l11_opy_[bstack11lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᩩ")] == bstack11lll1_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩᩪ"):
        for bstack111ll1l11ll_opy_ in bstack111llll1l11_opy_[bstack11lll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᩫ")]:
          logger.error(bstack111ll1l11ll_opy_[bstack11lll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᩬ")])
      return None, None
  except Exception as error:
    logger.error(bstack11lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦᩭ") +  str(error))
    return None, None
def bstack111ll1l111l_opy_():
  if os.getenv(bstack11lll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᩮ")) is None:
    return {
        bstack11lll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᩯ"): bstack11lll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᩰ"),
        bstack11lll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᩱ"): bstack11lll1_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧᩲ")
    }
  data = {bstack11lll1_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪᩳ"): current_time()}
  headers = {
      bstack11lll1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᩴ"): bstack11lll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬ᩵") + os.getenv(bstack11lll1_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥ᩶")),
      bstack11lll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬ᩷"): bstack11lll1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪ᩸")
  }
  response = bstack11l1lll11_opy_(bstack11lll1_opy_ (u"ࠨࡒࡘࡘࠬ᩹"), bstack111ll11llll_opy_ + bstack11lll1_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫ᩺"), data, { bstack11lll1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ᩻"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11lll1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧ᩼") + bstack1lllll111l1_opy_().isoformat() + bstack11lll1_opy_ (u"ࠬࡠࠧ᩽"))
      return {bstack11lll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᩾"): bstack11lll1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨ᩿"), bstack11lll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᪀"): bstack11lll1_opy_ (u"ࠩࠪ᪁")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11lll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨ᪂") + str(error))
    return {
        bstack11lll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫ᪃"): bstack11lll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫ᪄"),
        bstack11lll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᪅"): str(error)
    }
def bstack111ll1l1lll_opy_(bstack111llll1111_opy_):
    return re.match(bstack11lll1_opy_ (u"ࡲࠨࡠ࡟ࡨ࠰࠮࡜࠯࡞ࡧ࠯࠮ࡅࠤࠨ᪆"), bstack111llll1111_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack111llll1l1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack111llll1l1l_opy_ = desired_capabilities
        else:
          bstack111llll1l1l_opy_ = {}
        bstack1l1l111l1ll_opy_ = (bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ᪇"), bstack11lll1_opy_ (u"ࠩࠪ᪈")).lower() or caps.get(bstack11lll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩ᪉"), bstack11lll1_opy_ (u"ࠫࠬ᪊")).lower())
        if bstack1l1l111l1ll_opy_ == bstack11lll1_opy_ (u"ࠬ࡯࡯ࡴࠩ᪋"):
            return True
        if bstack1l1l111l1ll_opy_ == bstack11lll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧ᪌"):
            bstack1l1l111ll1l_opy_ = str(float(caps.get(bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩ᪍")) or bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᪎"), {}).get(bstack11lll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᪏"),bstack11lll1_opy_ (u"ࠪࠫ᪐"))))
            if bstack1l1l111l1ll_opy_ == bstack11lll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬ᪑") and int(bstack1l1l111ll1l_opy_.split(bstack11lll1_opy_ (u"ࠬ࠴ࠧ᪒"))[0]) < float(bstack111ll11ll1l_opy_):
                logger.warning(str(bstack111lll111ll_opy_))
                return False
            return True
        bstack1l1l111llll_opy_ = caps.get(bstack11lll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᪓"), {}).get(bstack11lll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫ᪔"), caps.get(bstack11lll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨ᪕"), bstack11lll1_opy_ (u"ࠩࠪ᪖")))
        if bstack1l1l111llll_opy_:
            logger.warning(bstack11lll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ᪗"))
            return False
        browser = (caps.get(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ᪘"), bstack11lll1_opy_ (u"ࠬ࠭᪙")) or caps.get(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᪚"), bstack11lll1_opy_ (u"ࠧࠨ᪛"))).lower() or \
                  (bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭᪜"), bstack11lll1_opy_ (u"ࠩࠪ᪝")) or bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࠫ᪞"), bstack11lll1_opy_ (u"ࠫࠬ᪟"))).lower()
        if browser not in (bstack11lll1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ᪠"), bstack11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱ࡮ࡻ࡭ࠨ᪡"), bstack11lll1_opy_ (u"ࠧࡱ࡮ࡤࡽࡼࡸࡩࡨࡪࡷ࠱ࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭᪢")):
            logger.warning(bstack11lll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ᪣"))
            return False
        browser_version = caps.get(bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᪤")) or caps.get(bstack11lll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᪥")) or bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᪦")) or bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᪧ"), {}).get(bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᪨")) or bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᪩"), {}).get(bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ᪪"))
        bstack1l11llllll1_opy_ = bstack111ll1ll1ll_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack111ll1ll1l1_opy_ = False
        if config is not None:
          bstack111ll1ll1l1_opy_ = bstack11lll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᪫") in config and str(config[bstack11lll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ᪬")]).lower() != bstack11lll1_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪ᪭")
        if os.environ.get(bstack11lll1_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ᪮"), bstack11lll1_opy_ (u"࠭ࠧ᪯")).lower() == bstack11lll1_opy_ (u"ࠧࡵࡴࡸࡩࠬ᪰") or bstack111ll1ll1l1_opy_:
          bstack1l11llllll1_opy_ = bstack111ll1ll1ll_opy_.bstack1l1l11l1lll_opy_
        if browser_version and browser_version != bstack11lll1_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨ᪱") and int(browser_version.split(bstack11lll1_opy_ (u"ࠩ࠱ࠫ᪲"))[0]) <= bstack1l11llllll1_opy_:
          logger.warning(bstack1ll11ll1ll1_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࡳࡩ࡯ࡡࡤ࠵࠶ࡿ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡢࡧ࡭ࡸ࡯࡮ࡧࡢࡺࡪࡸࡳࡪࡱࡱࢁ࠳࠭᪳"))
          return False
        if not options:
          bstack1l11ll11lll_opy_ = (caps.get(bstack11lll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᪴"))
                           or bstack111llll1l1l_opy_.get(bstack11lll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵ᪵ࠪ"), {})
                           or caps.get(bstack11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ᪶࠭"), {}))
          if any(arg == bstack11lll1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶ᪷ࠫ") or (arg.startswith(bstack11lll1_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࡂ᪸࠭")) and arg != bstack11lll1_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸࡃ࡮ࡦࡹ᪹ࠪ"))
                 for arg in bstack1l11ll11lll_opy_.get(bstack11lll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᪺"), [])):
              logger.warning(bstack11lll1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨ᪻"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11lll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢ᪼") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1ll1ll1ll_opy_ = config.get(bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ᪽࠭"), {})
    bstack1l1ll1ll1ll_opy_[bstack11lll1_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪ᪾")] = os.getenv(bstack11lll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ᪿ࠭"))
    bstack1lll11l1l1_opy_ = json.loads(os.getenv(bstack11lll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎᫀࠪ"), bstack11lll1_opy_ (u"ࠪࡿࢂ࠭᫁"))).get(bstack11lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᫂"))
    if not config[bstack11lll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡔࡷࡵࡤࡶࡥࡷࡑࡦࡶ᫃ࠧ")].get(bstack11lll1_opy_ (u"ࠨࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩ᫄ࠧ")):
      if bstack11lll1_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ᫅") in caps:
        caps[bstack11lll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᫆")][bstack11lll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫇")] = bstack1l1ll1ll1ll_opy_
        caps[bstack11lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᫈")][bstack11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᫉")][bstack11lll1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ᫊࠭")] = bstack1lll11l1l1_opy_
      else:
        caps[bstack11lll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᫋")] = bstack1l1ll1ll1ll_opy_
        caps[bstack11lll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᫌ")][bstack11lll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᫍ")] = bstack1lll11l1l1_opy_
  except Exception as error:
    logger.debug(bstack11lll1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡸ࡫ࡴࡵ࡫ࡱ࡫ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳ࠯ࠢࡈࡶࡷࡵࡲ࠻ࠢࠥᫎ") +  str(error))
def start_test_capture(driver, bstack111lll1111l_opy_):
  try:
    setattr(driver, bstack11lll1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭ࡄ࠵࠶ࡿࡓࡩࡱࡸࡰࡩ࡙ࡣࡢࡰࠪ᫏"), True)
    session = driver.session_id
    if session:
      bstack111ll1l1ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111ll1l1ll1_opy_ = False
      bstack111ll1l1ll1_opy_ = url.scheme in [bstack11lll1_opy_ (u"ࠦ࡭ࡺࡴࡱࠤ᫐"), bstack11lll1_opy_ (u"ࠧ࡮ࡴࡵࡲࡶࠦ᫑")]
      if bstack111ll1l1ll1_opy_:
        if bstack111lll1111l_opy_:
          logger.info(bstack11lll1_opy_ (u"ࠨࡓࡦࡶࡸࡴࠥ࡬࡯ࡳࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣ࡬ࡦࡹࠠࡴࡶࡤࡶࡹ࡫ࡤ࠯ࠢࡄࡹࡹࡵ࡭ࡢࡶࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡦࡺࡨࡧࡺࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡤࡨ࡫࡮ࡴࠠ࡮ࡱࡰࡩࡳࡺࡡࡳ࡫࡯ࡽ࠳ࠨ᫒"))
      return bstack111lll1111l_opy_
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡳࡵࡣࡵࡸ࡮ࡴࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡣࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡹࡣࡢࡰࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ᫓") + str(e))
    return False
def bstack111lll1l1_opy_(driver, name, path):
  try:
    bstack1l1l11l1ll1_opy_ = {
        bstack11lll1_opy_ (u"ࠨࡶ࡫ࡘࡪࡹࡴࡓࡷࡱ࡙ࡺ࡯ࡤࠨ᫔"): threading.current_thread().current_test_uuid,
        bstack11lll1_opy_ (u"ࠩࡷ࡬ࡇࡻࡩ࡭ࡦࡘࡹ࡮ࡪࠧ᫕"): os.environ.get(bstack11lll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢ࡙࡚ࡏࡄࠨ᫖"), bstack11lll1_opy_ (u"ࠫࠬ᫗")),
        bstack11lll1_opy_ (u"ࠬࡺࡨࡋࡹࡷࡘࡴࡱࡥ࡯ࠩ᫘"): os.environ.get(bstack11lll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡊࡘࡖࠪ᫙"), bstack11lll1_opy_ (u"ࠧࠨ᫚"))
    }
    bstack11lllll1_opy_ = bstack1lll11lll_opy_.bstack11ll11l1l_opy_(EVENTS.bstack1ll11ll1l_opy_.value)
    logger.debug(bstack11lll1_opy_ (u"ࠨࡒࡨࡶ࡫ࡵࡲ࡮࡫ࡱ࡫ࠥࡹࡣࡢࡰࠣࡦࡪ࡬࡯ࡳࡧࠣࡷࡦࡼࡩ࡯ࡩࠣࡶࡪࡹࡵ࡭ࡶࡶࠫ᫛"))
    try:
      if (bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ᫜"), None) and bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᫝"), None)):
        scripts = {bstack11lll1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ᫞"): accessibility_scripts.perform_scan}
        bstack111lll1ll1l_opy_ = json.loads(scripts[bstack11lll1_opy_ (u"ࠧࡹࡣࡢࡰࠥ᫟")].replace(bstack11lll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᫠"), bstack11lll1_opy_ (u"ࠢࠣ᫡")))
        bstack111lll1ll1l_opy_[bstack11lll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᫢")][bstack11lll1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩ᫣")] = None
        scripts[bstack11lll1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᫤")] = bstack11lll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢ᫥") + json.dumps(bstack111lll1ll1l_opy_)
        accessibility_scripts.bstack11lll1l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack11lll1_opy_ (u"ࠧࡳࡥࡵࡪࡲࡨࠧ᫦"): name}))
      bstack1lll11lll_opy_.end(EVENTS.bstack1ll11ll1l_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᫧"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᫨"), True, None)
    except Exception as error:
      bstack1lll11lll_opy_.end(EVENTS.bstack1ll11ll1l_opy_.value, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᫩"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ᫪"), False, str(error))
    bstack11lllll1_opy_ = bstack1lll11lll_opy_.bstack111lll1lll1_opy_(EVENTS.bstack1l1l11111l1_opy_.value)
    bstack1lll11lll_opy_.mark(bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᫫"))
    try:
      if (bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫ᫬"), None) and bstack111ll1ll_opy_(threading.current_thread(), bstack11lll1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ᫭"), None)):
        scripts = {bstack11lll1_opy_ (u"࠭ࡳࡤࡣࡱࠫ᫮"): accessibility_scripts.perform_scan}
        bstack111lll1ll1l_opy_ = json.loads(scripts[bstack11lll1_opy_ (u"ࠢࡴࡥࡤࡲࠧ᫯")].replace(bstack11lll1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦ᫰"), bstack11lll1_opy_ (u"ࠤࠥ᫱")))
        bstack111lll1ll1l_opy_[bstack11lll1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭᫲")][bstack11lll1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫ᫳")] = None
        scripts[bstack11lll1_opy_ (u"ࠧࡹࡣࡢࡰࠥ᫴")] = bstack11lll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᫵") + json.dumps(bstack111lll1ll1l_opy_)
        accessibility_scripts.bstack11lll1l11_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l1l11l1ll1_opy_))
      bstack1lll11lll_opy_.end(bstack11lllll1_opy_, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᫶"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᫷"),True, None)
    except Exception as error:
      bstack1lll11lll_opy_.end(bstack11lllll1_opy_, bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᫸"), bstack11lllll1_opy_ + bstack11lll1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᫹"),False, str(error))
    logger.info(bstack11lll1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢ᫺"))
    try:
      bstack1l11l1ll1l1_opy_ = {
        bstack11lll1_opy_ (u"ࠧࡸࡥࡲࡷࡨࡷࡹࠨ᫻"): {
          bstack11lll1_opy_ (u"ࠨࡣࡰ࡯ࡰࡥࡳࡪࠢ᫼"): bstack11lll1_opy_ (u"ࠢࡂ࠳࠴࡝ࡤ࡙ࡁࡗࡇࡢࡖࡊ࡙ࡕࡍࡖࡖࠦ᫽"),
        },
        bstack11lll1_opy_ (u"ࠣࡴࡨࡷࡵࡵ࡮ࡴࡧࠥ᫾"): {
          bstack11lll1_opy_ (u"ࠤࡥࡳࡩࡿࠢ᫿"): {
            bstack11lll1_opy_ (u"ࠥࡱࡸ࡭ࠢᬀ"): bstack11lll1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣ࡬ࡦࡹࠠࡦࡰࡧࡩࡩ࠴ࠢᬁ"),
            bstack11lll1_opy_ (u"ࠧࡹࡵࡤࡥࡨࡷࡸࠨᬂ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l11l1ll1l1_opy_, separators=(bstack11lll1_opy_ (u"࠭ࠬࠨᬃ"), bstack11lll1_opy_ (u"ࠧ࠻ࠩᬄ"))))
    except Exception as bstack1l1l1l1l1l_opy_:
      logger.debug(bstack11lll1_opy_ (u"ࠣࡈࡤ࡭ࡱ࡫ࡤࠡࡶࡲࠤࡱࡵࡧࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡤࡺࡪࠦࡲࡦࡵࡸࡰࡹࡹࠠࡥࡣࡷࡥ࠿ࠦࠢᬅ") + str(bstack1l1l1l1l1l_opy_) + bstack11lll1_opy_ (u"ࠤࠥᬆ"))
  except Exception as bstack1l11lllllll_opy_:
    logger.error(bstack11lll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᬇ") + str(path) + bstack11lll1_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᬈ") + str(bstack1l11lllllll_opy_))
def bstack111lll111l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11lll1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᬉ")) and str(caps.get(bstack11lll1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᬊ"))).lower() == bstack11lll1_opy_ (u"ࠢࡢࡰࡧࡶࡴ࡯ࡤࠣᬋ"):
        bstack1l1l111ll1l_opy_ = caps.get(bstack11lll1_opy_ (u"ࠣࡣࡳࡴ࡮ࡻ࡭࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᬌ")) or caps.get(bstack11lll1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᬍ"))
        if bstack1l1l111ll1l_opy_ and int(str(bstack1l1l111ll1l_opy_)) < bstack111ll11ll1l_opy_:
            return False
    return True
def bstack111ll11l11_opy_(config):
  if bstack11lll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᬎ") in config:
        return config[bstack11lll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᬏ")]
  for platform in config.get(bstack11lll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᬐ"), []):
      if bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᬑ") in platform:
          return platform[bstack11lll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᬒ")]
  return None
def bstack11ll11l11_opy_(bstack1lll1l1ll_opy_):
  try:
    browser_name = bstack1lll1l1ll_opy_[bstack11lll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᬓ")]
    browser_version = bstack1lll1l1ll_opy_[bstack11lll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᬔ")]
    chrome_options = bstack1lll1l1ll_opy_[bstack11lll1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫᬕ")]
    try:
        bstack111ll1l11l1_opy_ = int(browser_version.split(bstack11lll1_opy_ (u"ࠫ࠳࠭ᬖ"))[0])
    except ValueError as e:
        logger.error(bstack11lll1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡴࡶࡦࡴࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠤᬗ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11lll1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᬘ")):
        logger.warning(bstack11lll1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᬙ"))
        return False
    if bstack111ll1l11l1_opy_ < bstack111ll1ll1ll_opy_.bstack1l1l11l1lll_opy_:
        logger.warning(bstack1ll11ll1ll1_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷ࡬ࡶࡪࡹࠠࡄࡪࡵࡳࡲ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡽࡆࡓࡓ࡙ࡔࡂࡐࡗࡗ࠳ࡓࡉࡏࡋࡐ࡙ࡒࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡗࡓࡔࡔࡘࡔࡆࡆࡢࡇࡍࡘࡏࡎࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࢁࠥࡵࡲࠡࡪ࡬࡫࡭࡫ࡲ࠯ࠩᬚ"))
        return False
    if chrome_options and any(bstack11lll1_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᬛ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11lll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᬜ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11lll1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡺࡶࡰࡰࡴࡷࠤ࡫ࡵࡲࠡ࡮ࡲࡧࡦࡲࠠࡄࡪࡵࡳࡲ࡫࠺ࠡࠤᬝ") + str(e))
    return False
def bstack1l1111111_opy_(bstack1l1lll111l_opy_, config):
    try:
      bstack1l11lll1l11_opy_ = bstack11lll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᬞ") in config and config[bstack11lll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᬟ")] == True
      bstack111ll1ll1l1_opy_ = bstack11lll1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᬠ") in config and str(config[bstack11lll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᬡ")]).lower() != bstack11lll1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᬢ")
      if not (bstack1l11lll1l11_opy_ and (not bstack1ll111l11l_opy_(config) or bstack111ll1ll1l1_opy_)):
        return bstack1l1lll111l_opy_
      bstack111lll11l1l_opy_ = accessibility_scripts.bstack111ll1l1111_opy_
      if bstack111lll11l1l_opy_ is None:
        logger.debug(bstack11lll1_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶࠤࡦࡸࡥࠡࡐࡲࡲࡪࠨᬣ"))
        return bstack1l1lll111l_opy_
      bstack111lll1ll11_opy_ = int(str(bstack111lll1l11l_opy_()).split(bstack11lll1_opy_ (u"ࠫ࠳࠭ᬤ"))[0])
      logger.debug(bstack11lll1_opy_ (u"࡙ࠧࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡦࡨࡸࡪࡩࡴࡦࡦ࠽ࠤࠧᬥ") + str(bstack111lll1ll11_opy_) + bstack11lll1_opy_ (u"ࠨࠢᬦ"))
      if bstack111lll1ll11_opy_ == 3 and isinstance(bstack1l1lll111l_opy_, dict) and bstack11lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᬧ") in bstack1l1lll111l_opy_ and bstack111lll11l1l_opy_ is not None:
        if bstack11lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬨ") not in bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᬩ")]:
          bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬪ")][bstack11lll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬫ")] = {}
        if bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡵࠪᬬ") in bstack111lll11l1l_opy_:
          if bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫᬭ") not in bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᬮ")][bstack11lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬯ")]:
            bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᬰ")][bstack11lll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᬱ")][bstack11lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩᬲ")] = []
          for arg in bstack111lll11l1l_opy_[bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡵࠪᬳ")]:
            if arg not in bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ᬴࠭")][bstack11lll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᬵ")][bstack11lll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᬶ")]:
              bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᬷ")][bstack11lll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᬸ")][bstack11lll1_opy_ (u"ࠫࡦࡸࡧࡴࠩᬹ")].append(arg)
        if bstack11lll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᬺ") in bstack111lll11l1l_opy_:
          if bstack11lll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᬻ") not in bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᬼ")][bstack11lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬽ")]:
            bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᬾ")][bstack11lll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᬿ")][bstack11lll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᭀ")] = []
          for ext in bstack111lll11l1l_opy_[bstack11lll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᭁ")]:
            if ext not in bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᭂ")][bstack11lll1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᭃ")][bstack11lll1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷ᭄ࠬ")]:
              bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᭅ")][bstack11lll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᭆ")][bstack11lll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᭇ")].append(ext)
        if bstack11lll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᭈ") in bstack111lll11l1l_opy_:
          if bstack11lll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᭉ") not in bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᭊ")][bstack11lll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᭋ")]:
            bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᭌ")][bstack11lll1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᭍")][bstack11lll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᭎")] = {}
          bstack111lll11111_opy_(bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᭏")][bstack11lll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᭐")][bstack11lll1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᭑")],
                    bstack111lll11l1l_opy_[bstack11lll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᭒")])
        os.environ[bstack11lll1_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧ᭓")] = bstack11lll1_opy_ (u"ࠪࡸࡷࡻࡥࠨ᭔")
        return bstack1l1lll111l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l1lll111l_opy_, ChromeOptions):
          chrome_options = bstack1l1lll111l_opy_
        elif isinstance(bstack1l1lll111l_opy_, dict):
          for value in bstack1l1lll111l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l1lll111l_opy_, dict):
            bstack1l1lll111l_opy_[bstack11lll1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ᭕")] = chrome_options
          else:
            bstack1l1lll111l_opy_ = chrome_options
        if bstack111lll11l1l_opy_ is not None:
          if bstack11lll1_opy_ (u"ࠬࡧࡲࡨࡵࠪ᭖") in bstack111lll11l1l_opy_:
                bstack111lll11lll_opy_ = chrome_options.arguments or []
                new_args = bstack111lll11l1l_opy_[bstack11lll1_opy_ (u"࠭ࡡࡳࡩࡶࠫ᭗")]
                for arg in new_args:
                    if arg not in bstack111lll11lll_opy_:
                        chrome_options.add_argument(arg)
          if bstack11lll1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ᭘") in bstack111lll11l1l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11lll1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᭙"), [])
                bstack111llll11ll_opy_ = bstack111lll11l1l_opy_[bstack11lll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᭚")]
                for extension in bstack111llll11ll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11lll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᭛") in bstack111lll11l1l_opy_:
                bstack111ll1ll11l_opy_ = chrome_options.experimental_options.get(bstack11lll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᭜"), {})
                bstack111lll11ll1_opy_ = bstack111lll11l1l_opy_[bstack11lll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᭝")]
                bstack111lll11111_opy_(bstack111ll1ll11l_opy_, bstack111lll11ll1_opy_)
                chrome_options.add_experimental_option(bstack11lll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᭞"), bstack111ll1ll11l_opy_)
        os.environ[bstack11lll1_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ᭟")] = bstack11lll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭᭠")
        return bstack1l1lll111l_opy_
    except Exception as e:
      logger.error(bstack11lll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡦࡧ࡭ࡳ࡭ࠠ࡯ࡱࡱ࠱ࡇ࡙ࠠࡪࡰࡩࡶࡦࠦࡡ࠲࠳ࡼࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࠢ᭡") + str(e))
      return bstack1l1lll111l_opy_