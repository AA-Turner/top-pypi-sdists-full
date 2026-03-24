# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack1ll1lll_opy_ (bstack11l11_opy_):
    global bstack11l1ll1_opy_
    bstack11l1111_opy_ = ord (bstack11l11_opy_ [-1])
    bstack1l111l1_opy_ = bstack11l11_opy_ [:-1]
    bstack111_opy_ = bstack11l1111_opy_ % len (bstack1l111l1_opy_)
    bstack11111l1_opy_ = bstack1l111l1_opy_ [:bstack111_opy_] + bstack1l111l1_opy_ [bstack111_opy_:]
    if bstack1ll1l1l_opy_:
        bstack11llll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    else:
        bstack11llll_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack1l111_opy_ + bstack11l1111_opy_) % bstack11l111l_opy_) for bstack1l111_opy_, char in enumerate (bstack11111l1_opy_)])
    return eval (bstack11llll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111lll11ll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack111llll11l1_opy_ as bstack111lll111ll_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import current_time, bstack1llll1ll111_opy_, bstack1l111llll_opy_, bstack111ll11l11l_opy_, \
  bstack111lll1llll_opy_, bstack1l1l1ll1l_opy_, get_host_info, bstack111lll11lll_opy_, bstack111l1l111l_opy_, error_handler, bstack111ll1l1l1l_opy_, bstack111ll11l1ll_opy_, bstack111l1lll11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack1ll11111_opy_ import bstack1lll1lll11_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack1ll11111_opy_ = bstack1lll1lll11_opy_()
@error_handler(class_method=False)
def _111ll11l1l1_opy_(driver, bstack1lll11lllll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll1lll_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧ᨜"): caps.get(bstack1ll1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭᨝"), None),
        bstack1ll1lll_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ᨞"): bstack1lll11lllll_opy_.get(bstack1ll1lll_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᨟"), None),
        bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᨠ"): caps.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᨡ"), None),
        bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᨢ"): caps.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᨣ"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᨤ") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᨥ"), None) is None or os.environ[bstack1ll1lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᨦ")] == bstack1ll1lll_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᨧ"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᨨ"), False) or any([p.get(bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᨩ"), False) == True for p in config.get(bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᨪ"), [])])
def is_enabled_platform(config, bstack111111lll1_opy_):
  try:
    bstack111lll1l11l_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᨫ"), False)
    _111lll1l111_opy_ = int(bstack111111lll1_opy_)
    if _111lll1l111_opy_ < 0:
      _111lll1l111_opy_ = 0
    bstack111lll1lll_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᨬ"), [])
    if _111lll1l111_opy_ < len(bstack111lll1lll_opy_) and bstack111lll1lll_opy_[_111lll1l111_opy_]:
      bstack111ll1l1l11_opy_ = bstack111lll1lll_opy_[_111lll1l111_opy_].get(bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᨭ"), None)
    else:
      bstack111ll1l1l11_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᨮ"), None)
    if bstack111ll1l1l11_opy_ != None:
      bstack111lll1l11l_opy_ = bstack111ll1l1l11_opy_
    bstack111lll11l11_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᨯ")) is not None and len(os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᨰ"))) > 0 and os.getenv(bstack1ll1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᨱ")) != bstack1ll1lll_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᨲ")
    return bstack111lll1l11l_opy_ and bstack111lll11l11_opy_
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᨳ") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l1l11l1111_opy_ = os.getenv(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᨴ"))
  if bstack1l1l11l1111_opy_ is None:
    return True
  bstack1l1l11l1111_opy_ = json.loads(bstack1l1l11l1111_opy_)
  try:
    include_tags = bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᨵ")] if bstack1ll1lll_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᨶ") in bstack1l1l11l1111_opy_ and isinstance(bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᨷ")], list) else []
    exclude_tags = bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᨸ")] if bstack1ll1lll_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᨹ") in bstack1l1l11l1111_opy_ and isinstance(bstack1l1l11l1111_opy_[bstack1ll1lll_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᨺ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᨻ") + str(error))
  return False
def bstack111ll1lll1l_opy_(config, bstack111ll1ll11l_opy_, bstack111lll1ll11_opy_, bstack111llll1111_opy_):
  bstack111lll11l1l_opy_ = bstack111ll11l11l_opy_(config)
  bstack111llll111l_opy_ = bstack111lll1llll_opy_(config)
  if bstack111lll11l1l_opy_ is None or bstack111llll111l_opy_ is None:
    logger.error(bstack1ll1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᨼ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᨽ"), bstack1ll1lll_opy_ (u"ࠬࢁࡽࠨᨾ")))
    data = {
        bstack1ll1lll_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᨿ"): config[bstack1ll1lll_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᩀ")],
        bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᩁ"): config.get(bstack1ll1lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᩂ"), os.path.basename(os.getcwd())),
        bstack1ll1lll_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᩃ"): current_time(),
        bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᩄ"): config.get(bstack1ll1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᩅ"), bstack1ll1lll_opy_ (u"࠭ࠧᩆ")),
        bstack1ll1lll_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᩇ"): {
            bstack1ll1lll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᩈ"): bstack111ll1ll11l_opy_,
            bstack1ll1lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᩉ"): bstack111lll1ll11_opy_,
            bstack1ll1lll_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᩊ"): __version__,
            bstack1ll1lll_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᩋ"): bstack1ll1lll_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᩌ"),
            bstack1ll1lll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᩍ"): bstack1ll1lll_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᩎ"),
            bstack1ll1lll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᩏ"): bstack111llll1111_opy_
        },
        bstack1ll1lll_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᩐ"): settings,
        bstack1ll1lll_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᩑ"): bstack111lll11lll_opy_(),
        bstack1ll1lll_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᩒ"): bstack1l1l1ll1l_opy_(),
        bstack1ll1lll_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᩓ"): get_host_info(),
        bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᩔ"): bstack1l111llll_opy_(config)
    }
    headers = {
        bstack1ll1lll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᩕ"): bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᩖ"),
    }
    config = {
        bstack1ll1lll_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᩗ"): (bstack111lll11l1l_opy_, bstack111llll111l_opy_),
        bstack1ll1lll_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᩘ"): headers
    }
    response = bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"ࠫࡕࡕࡓࡕࠩᩙ"), bstack111lll111ll_opy_ + bstack1ll1lll_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᩚ"), data, config)
    bstack111ll11ll1l_opy_ = response.json()
    if bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᩛ")]:
      parsed = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᩜ"), bstack1ll1lll_opy_ (u"ࠨࡽࢀࠫᩝ")))
      parsed[bstack1ll1lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᩞ")] = bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡨࡦࡺࡡࠨ᩟")][bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ᩠ࠬ")]
      os.environ[bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᩡ")] = json.dumps(parsed)
      accessibility_scripts.bstack11lll1ll_opy_(bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᩢ")][bstack1ll1lll_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᩣ")])
      accessibility_scripts.bstack111ll1ll1l1_opy_(bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᩤ")][bstack1ll1lll_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᩥ")])
      accessibility_scripts.store()
      return bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"ࠪࡨࡦࡺࡡࠨᩦ")][bstack1ll1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᩧ")], bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡡࡵࡣࠪᩨ")][bstack1ll1lll_opy_ (u"࠭ࡩࡥࠩᩩ")]
    else:
      logger.error(bstack1ll1lll_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᩪ") + bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᩫ")])
      if bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᩬ")] == bstack1ll1lll_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᩭ"):
        for bstack111lll1l1ll_opy_ in bstack111ll11ll1l_opy_[bstack1ll1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᩮ")]:
          logger.error(bstack111lll1l1ll_opy_[bstack1ll1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᩯ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᩰ") +  str(error))
    return None, None
def bstack111ll11ll11_opy_():
  if os.getenv(bstack1ll1lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᩱ")) is None:
    return {
        bstack1ll1lll_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᩲ"): bstack1ll1lll_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᩳ"),
        bstack1ll1lll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᩴ"): bstack1ll1lll_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪ᩵")
    }
  data = {bstack1ll1lll_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭᩶"): current_time()}
  headers = {
      bstack1ll1lll_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭᩷"): bstack1ll1lll_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨ᩸") + os.getenv(bstack1ll1lll_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨ᩹")),
      bstack1ll1lll_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ᩺"): bstack1ll1lll_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭᩻")
  }
  response = bstack111l1l111l_opy_(bstack1ll1lll_opy_ (u"ࠫࡕ࡛ࡔࠨ᩼"), bstack111lll111ll_opy_ + bstack1ll1lll_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧ᩽"), data, { bstack1ll1lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ᩾"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll1lll_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺ᩿ࠠࠣ") + bstack1llll1ll111_opy_().isoformat() + bstack1ll1lll_opy_ (u"ࠨ࡜ࠪ᪀"))
      return {bstack1ll1lll_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ᪁"): bstack1ll1lll_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ᪂"), bstack1ll1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᪃"): bstack1ll1lll_opy_ (u"ࠬ࠭᪄")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤ᪅") + str(error))
    return {
        bstack1ll1lll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ᪆"): bstack1ll1lll_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ᪇"),
        bstack1ll1lll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᪈"): str(error)
    }
def bstack111ll1ll1ll_opy_(bstack111ll1l1ll1_opy_):
    return re.match(bstack1ll1lll_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫ᪉"), bstack111ll1l1ll1_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack111ll1l1111_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack111ll1l1111_opy_ = desired_capabilities
        else:
          bstack111ll1l1111_opy_ = {}
        bstack1l1l111ll1l_opy_ = (bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪ᪊"), bstack1ll1lll_opy_ (u"ࠬ࠭᪋")).lower() or caps.get(bstack1ll1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ᪌"), bstack1ll1lll_opy_ (u"ࠧࠨ᪍")).lower())
        if bstack1l1l111ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠨ࡫ࡲࡷࠬ᪎"):
            return True
        if bstack1l1l111ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪ᪏"):
            bstack1l11l1ll11l_opy_ = str(float(caps.get(bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᪐")) or bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᪑"), {}).get(bstack1ll1lll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᪒"),bstack1ll1lll_opy_ (u"࠭ࠧ᪓"))))
            if bstack1l1l111ll1l_opy_ == bstack1ll1lll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨ᪔") and int(bstack1l11l1ll11l_opy_.split(bstack1ll1lll_opy_ (u"ࠨ࠰ࠪ᪕"))[0]) < float(bstack111lll111l1_opy_):
                logger.warning(str(bstack111lll1l1l1_opy_))
                return False
            return True
        bstack1l1l11l1lll_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ᪖"), {}).get(bstack1ll1lll_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧ᪗"), caps.get(bstack1ll1lll_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫ᪘"), bstack1ll1lll_opy_ (u"ࠬ࠭᪙")))
        if bstack1l1l11l1lll_opy_:
            logger.warning(bstack1ll1lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᪚"))
            return False
        browser = (caps.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬ᪛"), bstack1ll1lll_opy_ (u"ࠨࠩ᪜")) or caps.get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࠪ᪝"), bstack1ll1lll_opy_ (u"ࠪࠫ᪞"))).lower() or \
                  (bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩ᪟"), bstack1ll1lll_opy_ (u"ࠬ࠭᪠")) or bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࠧ᪡"), bstack1ll1lll_opy_ (u"ࠧࠨ᪢"))).lower()
        if browser not in (bstack1ll1lll_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨ᪣"), bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫ᪤"), bstack1ll1lll_opy_ (u"ࠪࡴࡱࡧࡹࡸࡴ࡬࡫࡭ࡺ࠭ࡤࡪࡵࡳࡲ࡯ࡵ࡮ࠩ᪥")):
            logger.warning(bstack1ll1lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ᪦"))
            return False
        browser_version = caps.get(bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᪧ")) or caps.get(bstack1ll1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᪨")) or bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᪩")) or bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᪪"), {}).get(bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᪫")) or bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᪬"), {}).get(bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭᪭"))
        bstack1l11lllll11_opy_ = bstack111lll11ll1_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack111ll1l11l1_opy_ = False
        if config is not None:
          bstack111ll1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᪮") in config and str(config[bstack1ll1lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᪯")]).lower() != bstack1ll1lll_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭᪰")
        if os.environ.get(bstack1ll1lll_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭᪱"), bstack1ll1lll_opy_ (u"ࠩࠪ᪲")).lower() == bstack1ll1lll_opy_ (u"ࠪࡸࡷࡻࡥࠨ᪳") or bstack111ll1l11l1_opy_:
          bstack1l11lllll11_opy_ = bstack111lll11ll1_opy_.bstack1l11lll1ll1_opy_
        if browser_version and browser_version != bstack1ll1lll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫ᪴") and int(browser_version.split(bstack1ll1lll_opy_ (u"ࠬ࠴᪵ࠧ"))[0]) <= bstack1l11lllll11_opy_:
          logger.warning(bstack1ll1lll_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠࡼࡿ࠱᪶ࠫ").format(bstack1l11lllll11_opy_))
          return False
        if not options:
          bstack1l11l1ll1ll_opy_ = (caps.get(bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷ᪷ࠬ"))
                           or bstack111ll1l1111_opy_.get(bstack1ll1lll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ᪸࠭"), {})
                           or caps.get(bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴ᪹ࠩ"), {}))
          if any(arg == bstack1ll1lll_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹ᪺ࠧ") or (arg.startswith(bstack1ll1lll_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳ࠾ࠩ᪻")) and arg != bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴ࠿ࡱࡩࡼ࠭᪼"))
                 for arg in bstack1l11l1ll1ll_opy_.get(bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡶ᪽ࠫ"), [])):
              logger.warning(bstack1ll1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ᪾"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1ll1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ᪿࠥ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1llll1lll_opy_ = config.get(bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴᫀࠩ"), {})
    bstack1l1llll1lll_opy_[bstack1ll1lll_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭᫁")] = os.getenv(bstack1ll1lll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᫂"))
    bstack1llll111ll_opy_ = json.loads(os.getenv(bstack1ll1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ᫃࠭"), bstack1ll1lll_opy_ (u"࠭ࡻࡾ᫄ࠩ"))).get(bstack1ll1lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᫅"))
    if not config[bstack1ll1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪ᫆")].get(bstack1ll1lll_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣ᫇")):
      if bstack1ll1lll_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᫈") in caps:
        caps[bstack1ll1lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ᫉")][bstack1ll1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷ᫊ࠬ")] = bstack1l1llll1lll_opy_
        caps[bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᫋")][bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᫌ")][bstack1ll1lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᫍ")] = bstack1llll111ll_opy_
      else:
        caps[bstack1ll1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᫎ")] = bstack1l1llll1lll_opy_
        caps[bstack1ll1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᫏")][bstack1ll1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ᫐")] = bstack1llll111ll_opy_
  except Exception as error:
    logger.debug(bstack1ll1lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨ᫑") +  str(error))
def start_test_capture(driver, bstack111ll1l11ll_opy_):
  try:
    setattr(driver, bstack1ll1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭᫒"), True)
    session = driver.session_id
    if session:
      bstack111ll1ll111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack111ll1ll111_opy_ = False
      bstack111ll1ll111_opy_ = url.scheme in [bstack1ll1lll_opy_ (u"ࠢࡩࡶࡷࡴࠧ᫓"), bstack1ll1lll_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ᫔")]
      if bstack111ll1ll111_opy_:
        if bstack111ll1l11ll_opy_:
          logger.info(bstack1ll1lll_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤ᫕"))
      return bstack111ll1l11ll_opy_
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ᫖") + str(e))
    return False
def bstack1ll1ll11ll_opy_(driver, name, path):
  try:
    bstack1l11l1lll11_opy_ = {
        bstack1ll1lll_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫ᫗"): threading.current_thread().current_test_uuid,
        bstack1ll1lll_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᫘"): os.environ.get(bstack1ll1lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᫙"), bstack1ll1lll_opy_ (u"ࠧࠨ᫚")),
        bstack1ll1lll_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬ᫛"): os.environ.get(bstack1ll1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᫜"), bstack1ll1lll_opy_ (u"ࠪࠫ᫝"))
    }
    bstack11ll1ll1l_opy_ = bstack1ll11111_opy_.bstack11l1llllll_opy_(EVENTS.bstack11llll1l1_opy_.value)
    logger.debug(bstack1ll1lll_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧ᫞"))
    try:
      if (bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ᫟"), None) and bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ᫠"), None)):
        scripts = {bstack1ll1lll_opy_ (u"ࠧࡴࡥࡤࡲࠬ᫡"): accessibility_scripts.perform_scan}
        bstack111ll1llll1_opy_ = json.loads(scripts[bstack1ll1lll_opy_ (u"ࠣࡵࡦࡥࡳࠨ᫢")].replace(bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧ᫣"), bstack1ll1lll_opy_ (u"ࠥࠦ᫤")))
        bstack111ll1llll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ᫥")][bstack1ll1lll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ᫦")] = None
        scripts[bstack1ll1lll_opy_ (u"ࠨࡳࡤࡣࡱࠦ᫧")] = bstack1ll1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ᫨") + json.dumps(bstack111ll1llll1_opy_)
        accessibility_scripts.bstack11lll1ll_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1ll1lll_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣ᫩"): name}))
      bstack1ll11111_opy_.end(EVENTS.bstack11llll1l1_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ᫪"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ᫫"), True, None)
    except Exception as error:
      bstack1ll11111_opy_.end(EVENTS.bstack11llll1l1_opy_.value, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᫬"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᫭"), False, str(error))
    bstack11ll1ll1l_opy_ = bstack1ll11111_opy_.bstack111lll1111l_opy_(EVENTS.bstack1l1l11l11l1_opy_.value)
    bstack1ll11111_opy_.mark(bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᫮"))
    try:
      if (bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ᫯"), None) and bstack111l1lll11_opy_(threading.current_thread(), bstack1ll1lll_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᫰"), None)):
        scripts = {bstack1ll1lll_opy_ (u"ࠩࡶࡧࡦࡴࠧ᫱"): accessibility_scripts.perform_scan}
        bstack111ll1llll1_opy_ = json.loads(scripts[bstack1ll1lll_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᫲")].replace(bstack1ll1lll_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢ᫳"), bstack1ll1lll_opy_ (u"ࠧࠨ᫴")))
        bstack111ll1llll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ᫵")][bstack1ll1lll_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ᫶")] = None
        scripts[bstack1ll1lll_opy_ (u"ࠣࡵࡦࡥࡳࠨ᫷")] = bstack1ll1lll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧ᫸") + json.dumps(bstack111ll1llll1_opy_)
        accessibility_scripts.bstack11lll1ll_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l11l1lll11_opy_))
      bstack1ll11111_opy_.end(bstack11ll1ll1l_opy_, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ᫹"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ᫺"),True, None)
    except Exception as error:
      bstack1ll11111_opy_.end(bstack11ll1ll1l_opy_, bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᫻"), bstack11ll1ll1l_opy_ + bstack1ll1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᫼"),False, str(error))
    logger.info(bstack1ll1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥ᫽"))
    try:
      bstack1l11ll1l1l1_opy_ = {
        bstack1ll1lll_opy_ (u"ࠣࡴࡨࡵࡺ࡫ࡳࡵࠤ᫾"): {
          bstack1ll1lll_opy_ (u"ࠤࡦࡳࡲࡳࡡ࡯ࡦࠥ᫿"): bstack1ll1lll_opy_ (u"ࠥࡅ࠶࠷࡙ࡠࡕࡄ࡚ࡊࡥࡒࡆࡕࡘࡐ࡙࡙ࠢᬀ"),
        },
        bstack1ll1lll_opy_ (u"ࠦࡷ࡫ࡳࡱࡱࡱࡷࡪࠨᬁ"): {
          bstack1ll1lll_opy_ (u"ࠧࡨ࡯ࡥࡻࠥᬂ"): {
            bstack1ll1lll_opy_ (u"ࠨ࡭ࡴࡩࠥᬃ"): bstack1ll1lll_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥᬄ"),
            bstack1ll1lll_opy_ (u"ࠣࡵࡸࡧࡨ࡫ࡳࡴࠤᬅ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l11ll1l1l1_opy_, separators=(bstack1ll1lll_opy_ (u"ࠩ࠯ࠫᬆ"), bstack1ll1lll_opy_ (u"ࠪ࠾ࠬᬇ"))))
    except Exception as bstack1l1l1ll1l1_opy_:
      logger.debug(bstack1ll1lll_opy_ (u"ࠦࡋࡧࡩ࡭ࡧࡧࠤࡹࡵࠠ࡭ࡱࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸࡧࡶࡦࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡨࡦࡺࡡ࠻ࠢࠥᬈ") + str(bstack1l1l1ll1l1_opy_) + bstack1ll1lll_opy_ (u"ࠧࠨᬉ"))
  except Exception as bstack1l11ll1l111_opy_:
    logger.error(bstack1ll1lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᬊ") + str(path) + bstack1ll1lll_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᬋ") + str(bstack1l11ll1l111_opy_))
def bstack111lll11111_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll1lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᬌ")) and str(caps.get(bstack1ll1lll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᬍ"))).lower() == bstack1ll1lll_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦᬎ"):
        bstack1l11l1ll11l_opy_ = caps.get(bstack1ll1lll_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᬏ")) or caps.get(bstack1ll1lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᬐ"))
        if bstack1l11l1ll11l_opy_ and int(str(bstack1l11l1ll11l_opy_)) < bstack111lll111l1_opy_:
            return False
    return True
def bstack1l1ll111ll_opy_(config):
  if bstack1ll1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᬑ") in config:
        return config[bstack1ll1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᬒ")]
  for platform in config.get(bstack1ll1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᬓ"), []):
      if bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᬔ") in platform:
          return platform[bstack1ll1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᬕ")]
  return None
def bstack1111l1ll11_opy_(bstack1l1llll1_opy_):
  try:
    browser_name = bstack1l1llll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᬖ")]
    browser_version = bstack1l1llll1_opy_[bstack1ll1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᬗ")]
    chrome_options = bstack1l1llll1_opy_[bstack1ll1lll_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧᬘ")]
    try:
        bstack111ll11llll_opy_ = int(browser_version.split(bstack1ll1lll_opy_ (u"ࠧ࠯ࠩᬙ"))[0])
    except ValueError as e:
        logger.error(bstack1ll1lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡣࡰࡰࡹࡩࡷࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠧᬚ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1ll1lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᬛ")):
        logger.warning(bstack1ll1lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᬜ"))
        return False
    if bstack111ll11llll_opy_ < bstack111lll11ll1_opy_.bstack1l11lll1ll1_opy_:
        logger.warning(bstack1ll1lll_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡯ࡲࡦࡵࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡺࡪࡸࡳࡪࡱࡱࠤࢀࢃࠠࡰࡴࠣ࡬࡮࡭ࡨࡦࡴ࠱ࠫᬝ").format(bstack111lll11ll1_opy_.bstack1l11lll1ll1_opy_))
        return False
    if chrome_options and any(bstack1ll1lll_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᬞ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1ll1lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᬟ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1ll1lll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡶࡲࡳࡳࡷࡺࠠࡧࡱࡵࠤࡱࡵࡣࡢ࡮ࠣࡇ࡭ࡸ࡯࡮ࡧ࠽ࠤࠧᬠ") + str(e))
    return False
def bstack1lll1l111_opy_(bstack1ll1llll11_opy_, config):
    try:
      bstack1l1l111l111_opy_ = bstack1ll1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᬡ") in config and config[bstack1ll1lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᬢ")] == True
      bstack111ll1l11l1_opy_ = bstack1ll1lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᬣ") in config and str(config[bstack1ll1lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᬤ")]).lower() != bstack1ll1lll_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᬥ")
      if not (bstack1l1l111l111_opy_ and (not bstack1l111llll_opy_(config) or bstack111ll1l11l1_opy_)):
        return bstack1ll1llll11_opy_
      bstack111ll11lll1_opy_ = accessibility_scripts.bstack111ll1lll11_opy_
      if bstack111ll11lll1_opy_ is None:
        logger.debug(bstack1ll1lll_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹࠠࡢࡴࡨࠤࡓࡵ࡮ࡦࠤᬦ"))
        return bstack1ll1llll11_opy_
      bstack111ll1l1lll_opy_ = int(str(bstack111ll11l1ll_opy_()).split(bstack1ll1lll_opy_ (u"ࠧ࠯ࠩᬧ"))[0])
      logger.debug(bstack1ll1lll_opy_ (u"ࠣࡕࡨࡰࡪࡴࡩࡶ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡩ࡫ࡴࡦࡥࡷࡩࡩࡀࠠࠣᬨ") + str(bstack111ll1l1lll_opy_) + bstack1ll1lll_opy_ (u"ࠤࠥᬩ"))
      if bstack111ll1l1lll_opy_ == 3 and isinstance(bstack1ll1llll11_opy_, dict) and bstack1ll1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬪ") in bstack1ll1llll11_opy_ and bstack111ll11lll1_opy_ is not None:
        if bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬫ") not in bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᬬ")]:
          bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᬭ")][bstack1ll1lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᬮ")] = {}
        if bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᬯ") in bstack111ll11lll1_opy_:
          if bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᬰ") not in bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬱ")][bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬲ")]:
            bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᬳ")][bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶ᬴ࠫ")][bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᬵ")] = []
          for arg in bstack111ll11lll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᬶ")]:
            if arg not in bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᬷ")][bstack1ll1lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᬸ")][bstack1ll1lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᬹ")]:
              bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᬺ")][bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᬻ")][bstack1ll1lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᬼ")].append(arg)
        if bstack1ll1lll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᬽ") in bstack111ll11lll1_opy_:
          if bstack1ll1lll_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᬾ") not in bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬿ")][bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᭀ")]:
            bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᭁ")][bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᭂ")][bstack1ll1lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᭃ")] = []
          for ext in bstack111ll11lll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷ᭄ࠬ")]:
            if ext not in bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᭅ")][bstack1ll1lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᭆ")][bstack1ll1lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᭇ")]:
              bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᭈ")][bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᭉ")][bstack1ll1lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᭊ")].append(ext)
        if bstack1ll1lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᭋ") in bstack111ll11lll1_opy_:
          if bstack1ll1lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᭌ") not in bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᭍")][bstack1ll1lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᭎")]:
            bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᭏")][bstack1ll1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᭐")][bstack1ll1lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᭑")] = {}
          bstack111ll1l1l1l_opy_(bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᭒")][bstack1ll1lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᭓")][bstack1ll1lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᭔")],
                    bstack111ll11lll1_opy_[bstack1ll1lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ᭕")])
        os.environ[bstack1ll1lll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ᭖")] = bstack1ll1lll_opy_ (u"࠭ࡴࡳࡷࡨࠫ᭗")
        return bstack1ll1llll11_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1llll11_opy_, ChromeOptions):
          chrome_options = bstack1ll1llll11_opy_
        elif isinstance(bstack1ll1llll11_opy_, dict):
          for value in bstack1ll1llll11_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1llll11_opy_, dict):
            bstack1ll1llll11_opy_[bstack1ll1lll_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ᭘")] = chrome_options
          else:
            bstack1ll1llll11_opy_ = chrome_options
        if bstack111ll11lll1_opy_ is not None:
          if bstack1ll1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᭙") in bstack111ll11lll1_opy_:
                bstack111lll1lll1_opy_ = chrome_options.arguments or []
                new_args = bstack111ll11lll1_opy_[bstack1ll1lll_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᭚")]
                for arg in new_args:
                    if arg not in bstack111lll1lll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack1ll1lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᭛") in bstack111ll11lll1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1ll1lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᭜"), [])
                bstack111ll1lllll_opy_ = bstack111ll11lll1_opy_[bstack1ll1lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᭝")]
                for extension in bstack111ll1lllll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1ll1lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᭞") in bstack111ll11lll1_opy_:
                bstack111ll1l111l_opy_ = chrome_options.experimental_options.get(bstack1ll1lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᭟"), {})
                bstack111lll1ll1l_opy_ = bstack111ll11lll1_opy_[bstack1ll1lll_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᭠")]
                bstack111ll1l1l1l_opy_(bstack111ll1l111l_opy_, bstack111lll1ll1l_opy_)
                chrome_options.add_experimental_option(bstack1ll1lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᭡"), bstack111ll1l111l_opy_)
        os.environ[bstack1ll1lll_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨ᭢")] = bstack1ll1lll_opy_ (u"ࠫࡹࡸࡵࡦࠩ᭣")
        return bstack1ll1llll11_opy_
    except Exception as e:
      logger.error(bstack1ll1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡩࡪࡩ࡯ࡩࠣࡲࡴࡴ࠭ࡃࡕࠣ࡭ࡳ࡬ࡲࡢࠢࡤ࠵࠶ࡿࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠥ᭤") + str(e))
      return bstack1ll1llll11_opy_