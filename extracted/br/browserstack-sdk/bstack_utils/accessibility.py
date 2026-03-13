# coding: UTF-8
import sys
bstack11llll1_opy_ = sys.version_info [0] == 2
bstack11ll11_opy_ = 2048
bstack1ll11ll_opy_ = 7
def bstack1111l_opy_ (bstack1l1l11l_opy_):
    global bstack1l1ll11_opy_
    bstack1llll11_opy_ = ord (bstack1l1l11l_opy_ [-1])
    bstack11ll111_opy_ = bstack1l1l11l_opy_ [:-1]
    bstack1l11ll_opy_ = bstack1llll11_opy_ % len (bstack11ll111_opy_)
    bstack1lllll1_opy_ = bstack11ll111_opy_ [:bstack1l11ll_opy_] + bstack11ll111_opy_ [bstack1l11ll_opy_:]
    if bstack11llll1_opy_:
        bstack1l11l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    else:
        bstack1l11l1l_opy_ = str () .join ([chr (ord (char) - bstack11ll11_opy_ - (bstack1l1l1ll_opy_ + bstack1llll11_opy_) % bstack1ll11ll_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack1lllll1_opy_)])
    return eval (bstack1l11l1l_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack111llllllll_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1111l111_opy_ as bstack11l1111l11l_opy_, EVENTS
from bstack_utils.accessibility_scripts import accessibility_scripts
from bstack_utils.helper import current_time, bstack1lllll1111l_opy_, bstack11l1ll11ll_opy_, bstack111lll1ll11_opy_, \
  bstack111lll11lll_opy_, bstack11llll111_opy_, get_host_info, bstack111llll11ll_opy_, bstack1llll1ll1_opy_, error_handler, bstack111lll1lll1_opy_, bstack11l1111111l_opy_, bstack1l11l11l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack111l1l1ll1_opy_ import bstack1l11ll1l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
automation_logger = logger_utils.get_automation_logger(__name__)
bstack111l1l1ll1_opy_ = bstack1l11ll1l1_opy_()
@error_handler(class_method=False)
def _111lllll1ll_opy_(driver, bstack1lll1ll1111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1111l_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩ᧑"): caps.get(bstack1111l_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨ᧒"), None),
        bstack1111l_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᧓"): bstack1lll1ll1111_opy_.get(bstack1111l_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧ᧔"), None),
        bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫ᧕"): caps.get(bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫ᧖"), None),
        bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᧗"): caps.get(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩ᧘"), None)
    }
  except Exception as error:
    logger.debug(bstack1111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭᧙") + str(error))
  return response
def on():
    if os.environ.get(bstack1111l_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᧚"), None) is None or os.environ[bstack1111l_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᧛")] == bstack1111l_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᧜"):
        return False
    return True
def is_enabled_root(config):
  return config.get(bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᧝"), False) or any([p.get(bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᧞"), False) == True for p in config.get(bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᧟"), [])])
def is_enabled_platform(config, bstack111l11l1ll_opy_):
  try:
    bstack111lll1ll1l_opy_ = config.get(bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᧠"), False)
    _111llll1111_opy_ = int(bstack111l11l1ll_opy_)
    if _111llll1111_opy_ < 0:
      _111llll1111_opy_ = 0
    bstack1111l11l11_opy_ = config.get(bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᧡"), [])
    if _111llll1111_opy_ < len(bstack1111l11l11_opy_) and bstack1111l11l11_opy_[_111llll1111_opy_]:
      bstack11l1111ll1l_opy_ = bstack1111l11l11_opy_[_111llll1111_opy_].get(bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᧢"), None)
    else:
      bstack11l1111ll1l_opy_ = config.get(bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᧣"), None)
    if bstack11l1111ll1l_opy_ != None:
      bstack111lll1ll1l_opy_ = bstack11l1111ll1l_opy_
    bstack111llllll1l_opy_ = os.getenv(bstack1111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᧤")) is not None and len(os.getenv(bstack1111l_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ᧥"))) > 0 and os.getenv(bstack1111l_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᧦")) != bstack1111l_opy_ (u"ࠩࡱࡹࡱࡲࠧ᧧")
    return bstack111lll1ll1l_opy_ and bstack111llllll1l_opy_
  except Exception as error:
    logger.debug(bstack1111l_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪ᧨") + str(error))
  return False
def is_enabled_testcase(test_tags):
  bstack1l1l11l111l_opy_ = os.getenv(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ᧩"))
  if bstack1l1l11l111l_opy_ is None:
    return True
  bstack1l1l11l111l_opy_ = json.loads(bstack1l1l11l111l_opy_)
  try:
    include_tags = bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪ᧪")] if bstack1111l_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫ᧫") in bstack1l1l11l111l_opy_ and isinstance(bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬ᧬")], list) else []
    exclude_tags = bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᧭")] if bstack1111l_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧ᧮") in bstack1l1l11l111l_opy_ and isinstance(bstack1l1l11l111l_opy_[bstack1111l_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨ᧯")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1111l_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦ᧰") + str(error))
  return False
def bstack111lll1llll_opy_(config, bstack111lllll11l_opy_, bstack111lllll111_opy_, bstack11l1111l1ll_opy_):
  bstack111llllll11_opy_ = bstack111lll1ll11_opy_(config)
  bstack111llll1ll1_opy_ = bstack111lll11lll_opy_(config)
  if bstack111llllll11_opy_ is None or bstack111llll1ll1_opy_ is None:
    logger.error(bstack1111l_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭᧱"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1111l_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ᧲"), bstack1111l_opy_ (u"ࠧࡼࡿࠪ᧳")))
    data = {
        bstack1111l_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᧴"): config[bstack1111l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᧵")],
        bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᧶"): config.get(bstack1111l_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ᧷"), os.path.basename(os.getcwd())),
        bstack1111l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨ᧸"): current_time(),
        bstack1111l_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ᧹"): config.get(bstack1111l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ᧺"), bstack1111l_opy_ (u"ࠨࠩ᧻")),
        bstack1111l_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩ᧼"): {
            bstack1111l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ᧽"): bstack111lllll11l_opy_,
            bstack1111l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ᧾"): bstack111lllll111_opy_,
            bstack1111l_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ᧿"): __version__,
            bstack1111l_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᨀ"): bstack1111l_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᨁ"),
            bstack1111l_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨᨂ"): bstack1111l_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫᨃ"),
            bstack1111l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᨄ"): bstack11l1111l1ll_opy_
        },
        bstack1111l_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭ᨅ"): settings,
        bstack1111l_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭ᨆ"): bstack111llll11ll_opy_(),
        bstack1111l_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭ᨇ"): bstack11llll111_opy_(),
        bstack1111l_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩᨈ"): get_host_info(),
        bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᨉ"): bstack11l1ll11ll_opy_(config)
    }
    headers = {
        bstack1111l_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᨊ"): bstack1111l_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᨋ"),
    }
    config = {
        bstack1111l_opy_ (u"ࠫࡦࡻࡴࡩࠩᨌ"): (bstack111llllll11_opy_, bstack111llll1ll1_opy_),
        bstack1111l_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᨍ"): headers
    }
    response = bstack1llll1ll1_opy_(bstack1111l_opy_ (u"࠭ࡐࡐࡕࡗࠫᨎ"), bstack11l1111l11l_opy_ + bstack1111l_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧᨏ"), data, config)
    bstack111lllll1l1_opy_ = response.json()
    if bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᨐ")]:
      parsed = json.loads(os.getenv(bstack1111l_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᨑ"), bstack1111l_opy_ (u"ࠪࡿࢂ࠭ᨒ")))
      parsed[bstack1111l_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᨓ")] = bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠬࡪࡡࡵࡣࠪᨔ")][bstack1111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᨕ")]
      os.environ[bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᨖ")] = json.dumps(parsed)
      accessibility_scripts.bstack1llll11ll1_opy_(bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᨗ")][bstack1111l_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵᨘࠪ")])
      accessibility_scripts.bstack11l11111l1l_opy_(bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠪࡨࡦࡺࡡࠨᨙ")][bstack1111l_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᨚ")])
      accessibility_scripts.store()
      return bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠬࡪࡡࡵࡣࠪᨛ")][bstack1111l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫ᨜")], bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠧࡥࡣࡷࡥࠬ᨝")][bstack1111l_opy_ (u"ࠨ࡫ࡧࠫ᨞")]
    else:
      logger.error(bstack1111l_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪ᨟") + bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᨠ")])
      if bstack111lllll1l1_opy_[bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᨡ")] == bstack1111l_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧᨢ"):
        for bstack111llll1lll_opy_ in bstack111lllll1l1_opy_[bstack1111l_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭ᨣ")]:
          logger.error(bstack111llll1lll_opy_[bstack1111l_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᨤ")])
      return None, None
  except Exception as error:
    logger.error(bstack1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤᨥ") +  str(error))
    return None, None
def bstack111lllllll1_opy_():
  if os.getenv(bstack1111l_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᨦ")) is None:
    return {
        bstack1111l_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᨧ"): bstack1111l_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᨨ"),
        bstack1111l_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᨩ"): bstack1111l_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬᨪ")
    }
  data = {bstack1111l_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨᨫ"): current_time()}
  headers = {
      bstack1111l_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᨬ"): bstack1111l_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪᨭ") + os.getenv(bstack1111l_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣᨮ")),
      bstack1111l_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᨯ"): bstack1111l_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᨰ")
  }
  response = bstack1llll1ll1_opy_(bstack1111l_opy_ (u"࠭ࡐࡖࡖࠪᨱ"), bstack11l1111l11l_opy_ + bstack1111l_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩᨲ"), data, { bstack1111l_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᨳ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1111l_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥᨴ") + bstack1lllll1111l_opy_().isoformat() + bstack1111l_opy_ (u"ࠪ࡞ࠬᨵ"))
      return {bstack1111l_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᨶ"): bstack1111l_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᨷ"), bstack1111l_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᨸ"): bstack1111l_opy_ (u"ࠧࠨᨹ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1111l_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦᨺ") + str(error))
    return {
        bstack1111l_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᨻ"): bstack1111l_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᨼ"),
        bstack1111l_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᨽ"): str(error)
    }
def bstack111lll1l1ll_opy_(bstack11l1111l1l1_opy_):
    return re.match(bstack1111l_opy_ (u"ࡷ࠭࡞࡝ࡦ࠮ࠬࡡ࠴࡜ࡥ࠭ࠬࡃࠩ࠭ᨾ"), bstack11l1111l1l1_opy_.strip()) is not None
def is_platform_supported(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack111llll1l11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack111llll1l11_opy_ = desired_capabilities
        else:
          bstack111llll1l11_opy_ = {}
        bstack1l1l111ll11_opy_ = (bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᨿ"), bstack1111l_opy_ (u"ࠧࠨᩀ")).lower() or caps.get(bstack1111l_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᩁ"), bstack1111l_opy_ (u"ࠩࠪᩂ")).lower())
        if bstack1l1l111ll11_opy_ == bstack1111l_opy_ (u"ࠪ࡭ࡴࡹࠧᩃ"):
            return True
        if bstack1l1l111ll11_opy_ == bstack1111l_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᩄ"):
            bstack1l1l11l1111_opy_ = str(float(caps.get(bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧᩅ")) or bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᩆ"), {}).get(bstack1111l_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᩇ"),bstack1111l_opy_ (u"ࠨࠩᩈ"))))
            if bstack1l1l111ll11_opy_ == bstack1111l_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᩉ") and int(bstack1l1l11l1111_opy_.split(bstack1111l_opy_ (u"ࠪ࠲ࠬᩊ"))[0]) < float(bstack111lll11ll1_opy_):
                logger.warning(str(bstack111lll1l1l1_opy_))
                return False
            return True
        bstack1l1l11ll11l_opy_ = caps.get(bstack1111l_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᩋ"), {}).get(bstack1111l_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᩌ"), caps.get(bstack1111l_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᩍ"), bstack1111l_opy_ (u"ࠧࠨᩎ")))
        if bstack1l1l11ll11l_opy_:
            logger.warning(bstack1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᩏ"))
            return False
        browser = (caps.get(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᩐ"), bstack1111l_opy_ (u"ࠪࠫᩑ")) or caps.get(bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࠬᩒ"), bstack1111l_opy_ (u"ࠬ࠭ᩓ"))).lower() or \
                  (bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᩔ"), bstack1111l_opy_ (u"ࠧࠨᩕ")) or bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࠩᩖ"), bstack1111l_opy_ (u"ࠩࠪᩗ"))).lower()
        if browser not in (bstack1111l_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᩘ"), bstack1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯࡬ࡹࡲ࠭ᩙ"), bstack1111l_opy_ (u"ࠬࡶ࡬ࡢࡻࡺࡶ࡮࡭ࡨࡵ࠯ࡦ࡬ࡷࡵ࡭ࡪࡷࡰࠫᩚ")):
            logger.warning(bstack1111l_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᩛ"))
            return False
        browser_version = caps.get(bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᩜ")) or caps.get(bstack1111l_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᩝ")) or bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᩞ")) or bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫ᩟"), {}).get(bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲ᩠ࠬ")) or bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᩡ"), {}).get(bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᩢ"))
        bstack1l11lll11l1_opy_ = bstack111llllllll_opy_.MINIMUM_ACCESSIBILITY_SUPPORTED_CHROME_VERSION
        bstack111llll11l1_opy_ = False
        if config is not None:
          bstack111llll11l1_opy_ = bstack1111l_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᩣ") in config and str(config[bstack1111l_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᩤ")]).lower() != bstack1111l_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᩥ")
        if os.environ.get(bstack1111l_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᩦ"), bstack1111l_opy_ (u"ࠫࠬᩧ")).lower() == bstack1111l_opy_ (u"ࠬࡺࡲࡶࡧࠪᩨ") or bstack111llll11l1_opy_:
          bstack1l11lll11l1_opy_ = bstack111llllllll_opy_.bstack1l1l11l1l11_opy_
        if browser_version and browser_version != bstack1111l_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᩩ") and int(browser_version.split(bstack1111l_opy_ (u"ࠧ࠯ࠩᩪ"))[0]) <= bstack1l11lll11l1_opy_:
          logger.warning(bstack1ll1l11l1ll_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࡱ࡮ࡴ࡟ࡢ࠳࠴ࡽࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡠࡥ࡫ࡶࡴࡳࡥࡠࡸࡨࡶࡸ࡯࡯࡯ࡿ࠱ࠫᩫ"))
          return False
        if not options:
          bstack1l1l1111lll_opy_ = (caps.get(bstack1111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᩬ"))
                           or bstack111llll1l11_opy_.get(bstack1111l_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᩭ"), {})
                           or caps.get(bstack1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᩮ"), {}))
          if any(arg == bstack1111l_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩᩯ") or (arg.startswith(bstack1111l_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࡀࠫᩰ")) and arg != bstack1111l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࡁࡳ࡫ࡷࠨᩱ"))
                 for arg in bstack1l1l1111lll_opy_.get(bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᩲ"), [])):
              logger.warning(bstack1111l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᩳ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1111l_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᩴ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1ll11l111_opy_ = config.get(bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᩵"), {})
    bstack1l1ll11l111_opy_[bstack1111l_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨ᩶")] = os.getenv(bstack1111l_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ᩷"))
    bstack1llll111_opy_ = json.loads(os.getenv(bstack1111l_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᩸"), bstack1111l_opy_ (u"ࠨࡽࢀࠫ᩹"))).get(bstack1111l_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ᩺"))
    if not config[bstack1111l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ᩻")].get(bstack1111l_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ᩼")):
      if bstack1111l_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᩽") in caps:
        caps[bstack1111l_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᩾")][bstack1111l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹ᩿ࠧ")] = bstack1l1ll11l111_opy_
        caps[bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᪀")][bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᪁")][bstack1111l_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ᪂")] = bstack1llll111_opy_
      else:
        caps[bstack1111l_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ᪃")] = bstack1l1ll11l111_opy_
        caps[bstack1111l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ᪄")][bstack1111l_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ᪅")] = bstack1llll111_opy_
  except Exception as error:
    logger.debug(bstack1111l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࠣ᪆") +  str(error))
def start_test_capture(driver, bstack11l11111111_opy_):
  try:
    setattr(driver, bstack1111l_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ᪇"), True)
    session = driver.session_id
    if session:
      bstack11l11111ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l11111ll1_opy_ = False
      bstack11l11111ll1_opy_ = url.scheme in [bstack1111l_opy_ (u"ࠤ࡫ࡸࡹࡶࠢ᪈"), bstack1111l_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ᪉")]
      if bstack11l11111ll1_opy_:
        if bstack11l11111111_opy_:
          logger.info(bstack1111l_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦ᪊"))
      return bstack11l11111111_opy_
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ᪋") + str(e))
    return False
def bstack1l1l1ll11_opy_(driver, name, path):
  try:
    bstack1l1l1l1l1ll_opy_ = {
        bstack1111l_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭᪌"): threading.current_thread().current_test_uuid,
        bstack1111l_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ᪍"): os.environ.get(bstack1111l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭᪎"), bstack1111l_opy_ (u"ࠩࠪ᪏")),
        bstack1111l_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧ᪐"): os.environ.get(bstack1111l_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ᪑"), bstack1111l_opy_ (u"ࠬ࠭᪒"))
    }
    bstack1l1llll1_opy_ = bstack111l1l1ll1_opy_.bstack11ll11l1ll_opy_(EVENTS.bstack1l11llll_opy_.value)
    logger.debug(bstack1111l_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩ᪓"))
    try:
      if (bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ᪔"), None) and bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᪕"), None)):
        scripts = {bstack1111l_opy_ (u"ࠩࡶࡧࡦࡴࠧ᪖"): accessibility_scripts.perform_scan}
        bstack11l111111l1_opy_ = json.loads(scripts[bstack1111l_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᪗")].replace(bstack1111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢ᪘"), bstack1111l_opy_ (u"ࠧࠨ᪙")))
        bstack11l111111l1_opy_[bstack1111l_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ᪚")][bstack1111l_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ᪛")] = None
        scripts[bstack1111l_opy_ (u"ࠣࡵࡦࡥࡳࠨ᪜")] = bstack1111l_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧ᪝") + json.dumps(bstack11l111111l1_opy_)
        accessibility_scripts.bstack1llll11ll1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.perform_scan, {bstack1111l_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥ᪞"): name}))
      bstack111l1l1ll1_opy_.end(EVENTS.bstack1l11llll_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ᪟"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ᪠"), True, None)
    except Exception as error:
      bstack111l1l1ll1_opy_.end(EVENTS.bstack1l11llll_opy_.value, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ᪡"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ᪢"), False, str(error))
    bstack1l1llll1_opy_ = bstack111l1l1ll1_opy_.bstack111lll1l11l_opy_(EVENTS.bstack1l1l111ll1l_opy_.value)
    bstack111l1l1ll1_opy_.mark(bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ᪣"))
    try:
      if (bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ᪤"), None) and bstack1l11l11l11_opy_(threading.current_thread(), bstack1111l_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ᪥"), None)):
        scripts = {bstack1111l_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ᪦"): accessibility_scripts.perform_scan}
        bstack11l111111l1_opy_ = json.loads(scripts[bstack1111l_opy_ (u"ࠧࡹࡣࡢࡰࠥᪧ")].replace(bstack1111l_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ᪨"), bstack1111l_opy_ (u"ࠢࠣ᪩")))
        bstack11l111111l1_opy_[bstack1111l_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ᪪")][bstack1111l_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩ᪫")] = None
        scripts[bstack1111l_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ᪬")] = bstack1111l_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢ᪭") + json.dumps(bstack11l111111l1_opy_)
        accessibility_scripts.bstack1llll11ll1_opy_(scripts)
        accessibility_scripts.store()
        logger.debug(driver.execute_script(accessibility_scripts.perform_scan))
      else:
        logger.debug(driver.execute_async_script(accessibility_scripts.save_test_results, bstack1l1l1l1l1ll_opy_))
      bstack111l1l1ll1_opy_.end(bstack1l1llll1_opy_, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᪮"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᪯"),True, None)
    except Exception as error:
      bstack111l1l1ll1_opy_.end(bstack1l1llll1_opy_, bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᪰"), bstack1l1llll1_opy_ + bstack1111l_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᪱"),False, str(error))
    logger.info(bstack1111l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᪲"))
    try:
      bstack1l1l1111ll1_opy_ = {
        bstack1111l_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ᪳"): {
          bstack1111l_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ᪴"): bstack1111l_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡆ࡜ࡅࡠࡔࡈࡗ࡚ࡒࡔࡔࠤ᪵"),
        },
        bstack1111l_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥ᪶ࠣ"): {
          bstack1111l_opy_ (u"ࠢࡣࡱࡧࡽ᪷ࠧ"): {
            bstack1111l_opy_ (u"ࠣ࡯ࡶ࡫᪸ࠧ"): bstack1111l_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲᪹ࠧ"),
            bstack1111l_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶ᪺ࠦ"): True
          }
        }
      }
      automation_logger.info(json.dumps(bstack1l1l1111ll1_opy_, separators=(bstack1111l_opy_ (u"ࠫ࠱࠭᪻"), bstack1111l_opy_ (u"ࠬࡀࠧ᪼"))))
    except Exception as bstack1l11111l1_opy_:
      logger.debug(bstack1111l_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡢࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡪࡡࡵࡣ࠽ࠤ᪽ࠧ") + str(bstack1l11111l1_opy_) + bstack1111l_opy_ (u"ࠢࠣ᪾"))
  except Exception as bstack1l1l11l1ll1_opy_:
    logger.error(bstack1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ᪿࠢࠥ") + str(path) + bstack1111l_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ᫀࠦ") + str(bstack1l1l11l1ll1_opy_))
def bstack111llll111l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1111l_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ᫁")) and str(caps.get(bstack1111l_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ᫂"))).lower() == bstack1111l_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨ᫃"):
        bstack1l1l11l1111_opy_ = caps.get(bstack1111l_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮᫄ࠣ")) or caps.get(bstack1111l_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ᫅"))
        if bstack1l1l11l1111_opy_ and int(str(bstack1l1l11l1111_opy_)) < bstack111lll11ll1_opy_:
            return False
    return True
def bstack1l1l1l1ll1_opy_(config):
  if bstack1111l_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᫆") in config:
        return config[bstack1111l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᫇")]
  for platform in config.get(bstack1111l_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᫈"), []):
      if bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᫉") in platform:
          return platform[bstack1111l_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ᫊ࠬ")]
  return None
def bstack111ll111_opy_(bstack1l1lll11ll_opy_):
  try:
    browser_name = bstack1l1lll11ll_opy_[bstack1111l_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬ᫋")]
    browser_version = bstack1l1lll11ll_opy_[bstack1111l_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᫌ")]
    chrome_options = bstack1l1lll11ll_opy_[bstack1111l_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩᫍ")]
    try:
        bstack11l11111l11_opy_ = int(browser_version.split(bstack1111l_opy_ (u"ࠩ࠱ࠫᫎ"))[0])
    except ValueError as e:
        logger.error(bstack1111l_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡲࡻ࡫ࡲࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠢ᫏") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1111l_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫ᫐")):
        logger.warning(bstack1111l_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣ᫑"))
        return False
    if bstack11l11111l11_opy_ < bstack111llllllll_opy_.bstack1l1l11l1l11_opy_:
        logger.warning(bstack1ll1l11l1ll_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡪࡴࡨࡷࠥࡉࡨࡳࡱࡰࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡻࡄࡑࡑࡗ࡙ࡇࡎࡕࡕ࠱ࡑࡎࡔࡉࡎࡗࡐࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡕࡑࡒࡒࡖ࡙ࡋࡄࡠࡅࡋࡖࡔࡓࡅࡠࡘࡈࡖࡘࡏࡏࡏࡿࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠧ᫒"))
        return False
    if chrome_options and any(bstack1111l_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫ᫓") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1111l_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥ᫔"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1111l_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡩࡳࡷࠦ࡬ࡰࡥࡤࡰࠥࡉࡨࡳࡱࡰࡩ࠿ࠦࠢ᫕") + str(e))
    return False
def bstack111l1l11ll_opy_(bstack111ll11l1_opy_, config):
    try:
      bstack1l11lll1ll1_opy_ = bstack1111l_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᫖") in config and config[bstack1111l_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᫗")] == True
      bstack111llll11l1_opy_ = bstack1111l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ᫘") in config and str(config[bstack1111l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᫙")]).lower() != bstack1111l_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭᫚")
      if not (bstack1l11lll1ll1_opy_ and (not bstack11l1ll11ll_opy_(config) or bstack111llll11l1_opy_)):
        return bstack111ll11l1_opy_
      bstack111llll1l1l_opy_ = accessibility_scripts.bstack11l111111ll_opy_
      if bstack111llll1l1l_opy_ is None:
        logger.debug(bstack1111l_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶࡪࠦࡎࡰࡰࡨࠦ᫛"))
        return bstack111ll11l1_opy_
      bstack11l11111lll_opy_ = int(str(bstack11l1111111l_opy_()).split(bstack1111l_opy_ (u"ࠩ࠱ࠫ᫜"))[0])
      logger.debug(bstack1111l_opy_ (u"ࠥࡗࡪࡲࡥ࡯࡫ࡸࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࠥ᫝") + str(bstack11l11111lll_opy_) + bstack1111l_opy_ (u"ࠦࠧ᫞"))
      if bstack11l11111lll_opy_ == 3 and isinstance(bstack111ll11l1_opy_, dict) and bstack1111l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᫟") in bstack111ll11l1_opy_ and bstack111llll1l1l_opy_ is not None:
        if bstack1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᫠") not in bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᫡")]:
          bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᫢")][bstack1111l_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ᫣")] = {}
        if bstack1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᫤") in bstack111llll1l1l_opy_:
          if bstack1111l_opy_ (u"ࠫࡦࡸࡧࡴࠩ᫥") not in bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᫦")][bstack1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᫧")]:
            bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᫨")][bstack1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫩")][bstack1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᫪")] = []
          for arg in bstack111llll1l1l_opy_[bstack1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᫫")]:
            if arg not in bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᫬")][bstack1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᫭")][bstack1111l_opy_ (u"࠭ࡡࡳࡩࡶࠫ᫮")]:
              bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᫯")][bstack1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫰")][bstack1111l_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᫱")].append(arg)
        if bstack1111l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᫲") in bstack111llll1l1l_opy_:
          if bstack1111l_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᫳") not in bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᫴")][bstack1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᫵")]:
            bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᫶")][bstack1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫷")][bstack1111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᫸")] = []
          for ext in bstack111llll1l1l_opy_[bstack1111l_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᫹")]:
            if ext not in bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ᫺")][bstack1111l_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ᫻")][bstack1111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᫼")]:
              bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ᫽")][bstack1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭᫾")][bstack1111l_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᫿")].append(ext)
        if bstack1111l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᬀ") in bstack111llll1l1l_opy_:
          if bstack1111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᬁ") not in bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᬂ")][bstack1111l_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᬃ")]:
            bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᬄ")][bstack1111l_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᬅ")][bstack1111l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᬆ")] = {}
          bstack111lll1lll1_opy_(bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᬇ")][bstack1111l_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᬈ")][bstack1111l_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᬉ")],
                    bstack111llll1l1l_opy_[bstack1111l_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᬊ")])
        os.environ[bstack1111l_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᬋ")] = bstack1111l_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᬌ")
        return bstack111ll11l1_opy_
      else:
        chrome_options = None
        if isinstance(bstack111ll11l1_opy_, ChromeOptions):
          chrome_options = bstack111ll11l1_opy_
        elif isinstance(bstack111ll11l1_opy_, dict):
          for value in bstack111ll11l1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack111ll11l1_opy_, dict):
            bstack111ll11l1_opy_[bstack1111l_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᬍ")] = chrome_options
          else:
            bstack111ll11l1_opy_ = chrome_options
        if bstack111llll1l1l_opy_ is not None:
          if bstack1111l_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᬎ") in bstack111llll1l1l_opy_:
                bstack111lll1l111_opy_ = chrome_options.arguments or []
                new_args = bstack111llll1l1l_opy_[bstack1111l_opy_ (u"ࠫࡦࡸࡧࡴࠩᬏ")]
                for arg in new_args:
                    if arg not in bstack111lll1l111_opy_:
                        chrome_options.add_argument(arg)
          if bstack1111l_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᬐ") in bstack111llll1l1l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1111l_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᬑ"), [])
                bstack111lll11l1l_opy_ = bstack111llll1l1l_opy_[bstack1111l_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᬒ")]
                for extension in bstack111lll11l1l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1111l_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᬓ") in bstack111llll1l1l_opy_:
                bstack11l1111lll1_opy_ = chrome_options.experimental_options.get(bstack1111l_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᬔ"), {})
                bstack11l1111ll11_opy_ = bstack111llll1l1l_opy_[bstack1111l_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᬕ")]
                bstack111lll1lll1_opy_(bstack11l1111lll1_opy_, bstack11l1111ll11_opy_)
                chrome_options.add_experimental_option(bstack1111l_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᬖ"), bstack11l1111lll1_opy_)
        os.environ[bstack1111l_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᬗ")] = bstack1111l_opy_ (u"࠭ࡴࡳࡷࡨࠫᬘ")
        return bstack111ll11l1_opy_
    except Exception as e:
      logger.error(bstack1111l_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡴ࡯࡯࠯ࡅࡗࠥ࡯࡮ࡧࡴࡤࠤࡦ࠷࠱ࡺࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧᬙ") + str(e))
      return bstack111ll11l1_opy_