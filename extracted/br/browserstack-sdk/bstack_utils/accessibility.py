# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack1lll1111l1l1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack1lll1111ll11_opy_ as bstack1lll11111l1l_opy_, EVENTS
from bstack_utils.bstack1l1l1l1lll_opy_ import bstack1l1l1l1lll_opy_
from bstack_utils.helper import current_time, bstack1lllllll1ll_opy_, bstack1l111l111_opy_, bstack11l111111ll_opy_, \
  bstack111llll11l1_opy_, bstack1ll1lll111_opy_, get_host_info, bstack111l1l1111l_opy_, bstack11111l1l_opy_, error_handler, bstack11l1111ll11_opy_, bstack111ll111lll_opy_, bstack11llll11l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.logger_utils import get_logger
from bstack_utils.bstack11lll11l1l_opy_ import bstack111ll11111_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import logger_utils
logger = get_logger(__name__)
bstack1l11llll_opy_ = logger_utils.bstack1111l1ll1_opy_(__name__)
bstack11lll11l1l_opy_ = bstack111ll11111_opy_()
@error_handler(class_method=False)
def _1lll111l11l1_opy_(driver, bstack1lll1l1l11l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1ll111_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬ⃰"): caps.get(bstack1ll111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫ⃱"), None),
        bstack1ll111_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪ⃲"): bstack1lll1l1l11l_opy_.get(bstack1ll111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ⃳"), None),
        bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ⃴"): caps.get(bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧ⃵"), None),
        bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⃶"): caps.get(bstack1ll111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ⃷"), None)
    }
  except Exception as error:
    logger.debug(bstack1ll111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩ⃸") + str(error))
  return response
def on():
    if os.environ.get(bstack1ll111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ⃹"), None) is None or os.environ[bstack1ll111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬ⃺")] == bstack1ll111_opy_ (u"ࠣࡰࡸࡰࡱࠨ⃻"):
        return False
    return True
def bstack1l1lll1111_opy_(config):
  return config.get(bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⃼"), False) or any([p.get(bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⃽"), False) == True for p in config.get(bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ⃾"), [])])
def bstack1111l1ll1l_opy_(config, bstack1l1ll1l1l_opy_):
  try:
    bstack1ll1lllllll1_opy_ = config.get(bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃿"), False)
    if int(bstack1l1ll1l1l_opy_) < len(config.get(bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ℀"), [])) and config[bstack1ll111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪ℁")][bstack1l1ll1l1l_opy_]:
      bstack1lll1111llll_opy_ = config[bstack1ll111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫℂ")][bstack1l1ll1l1l_opy_].get(bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ℃"), None)
    else:
      bstack1lll1111llll_opy_ = config.get(bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ℄"), None)
    if bstack1lll1111llll_opy_ != None:
      bstack1ll1lllllll1_opy_ = bstack1lll1111llll_opy_
    bstack1lll111111ll_opy_ = os.getenv(bstack1ll111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ℅")) is not None and len(os.getenv(bstack1ll111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ℆"))) > 0 and os.getenv(bstack1ll111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫℇ")) != bstack1ll111_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬ℈")
    return bstack1ll1lllllll1_opy_ and bstack1lll111111ll_opy_
  except Exception as error:
    logger.debug(bstack1ll111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨ℉") + str(error))
  return False
def bstack11l1llll11_opy_(test_tags):
  bstack1l1l1l1l1ll_opy_ = os.getenv(bstack1ll111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪℊ"))
  if bstack1l1l1l1l1ll_opy_ is None:
    return True
  bstack1l1l1l1l1ll_opy_ = json.loads(bstack1l1l1l1l1ll_opy_)
  try:
    include_tags = bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨℋ")] if bstack1ll111_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩℌ") in bstack1l1l1l1l1ll_opy_ and isinstance(bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪℍ")], list) else []
    exclude_tags = bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫℎ")] if bstack1ll111_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬℏ") in bstack1l1l1l1l1ll_opy_ and isinstance(bstack1l1l1l1l1ll_opy_[bstack1ll111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ℐ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1ll111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤℑ") + str(error))
  return False
def bstack1ll1lllll1ll_opy_(config, bstack1lll1111l111_opy_, bstack1ll1lllll1l1_opy_, bstack1lll1111ll1l_opy_):
  bstack1lll1l1111ll_opy_ = bstack11l111111ll_opy_(config)
  bstack1lll11ll1lll_opy_ = bstack111llll11l1_opy_(config)
  if bstack1lll1l1111ll_opy_ is None or bstack1lll11ll1lll_opy_ is None:
    logger.error(bstack1ll111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫℒ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬℓ"), bstack1ll111_opy_ (u"ࠬࢁࡽࠨ℔")))
    data = {
        bstack1ll111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫℕ"): config[bstack1ll111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬ№")],
        bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ℗"): config.get(bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ℘"), os.path.basename(os.getcwd())),
        bstack1ll111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ℙ"): current_time(),
        bstack1ll111_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩℚ"): config.get(bstack1ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨℛ"), bstack1ll111_opy_ (u"࠭ࠧℜ")),
        bstack1ll111_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧℝ"): {
            bstack1ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ℞"): bstack1lll1111l111_opy_,
            bstack1ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ℟"): bstack1ll1lllll1l1_opy_,
            bstack1ll111_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ℠"): __version__,
            bstack1ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭℡"): bstack1ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ™"),
            bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭℣"): bstack1ll111_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩℤ"),
            bstack1ll111_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ℥"): bstack1lll1111ll1l_opy_
        },
        bstack1ll111_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫΩ"): settings,
        bstack1ll111_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫ℧"): bstack111l1l1111l_opy_(),
        bstack1ll111_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫℨ"): bstack1ll1lll111_opy_(),
        bstack1ll111_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧ℩"): get_host_info(),
        bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨK"): bstack1l111l111_opy_(config)
    }
    headers = {
        bstack1ll111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭Å"): bstack1ll111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫℬ"),
    }
    config = {
        bstack1ll111_opy_ (u"ࠩࡤࡹࡹ࡮ࠧℭ"): (bstack1lll1l1111ll_opy_, bstack1lll11ll1lll_opy_),
        bstack1ll111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫ℮"): headers
    }
    response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠫࡕࡕࡓࡕࠩℯ"), bstack1lll11111l1l_opy_ + bstack1ll111_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬℰ"), data, config)
    bstack1lll1l1111l1_opy_ = response.json()
    if bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧℱ")]:
      parsed = json.loads(os.getenv(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨℲ"), bstack1ll111_opy_ (u"ࠨࡽࢀࠫℳ")))
      parsed[bstack1ll111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪℴ")] = bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"ࠪࡨࡦࡺࡡࠨℵ")][bstack1ll111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬℶ")]
      os.environ[bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ℷ")] = json.dumps(parsed)
      bstack1l1l1l1lll_opy_.bstack1lllll1l1_opy_(bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"࠭ࡤࡢࡶࡤࠫℸ")][bstack1ll111_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨℹ")])
      bstack1l1l1l1lll_opy_.bstack1lll11lll1ll_opy_(bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"ࠨࡦࡤࡸࡦ࠭℺")][bstack1ll111_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫ℻")])
      bstack1l1l1l1lll_opy_.store()
      return bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"ࠪࡨࡦࡺࡡࠨℼ")][bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩℽ")], bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"ࠬࡪࡡࡵࡣࠪℾ")][bstack1ll111_opy_ (u"࠭ࡩࡥࠩℿ")]
    else:
      logger.error(bstack1ll111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨ⅀") + bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ⅁")])
      if bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⅂")] == bstack1ll111_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬ⅃"):
        for bstack1ll1lllll11l_opy_ in bstack1lll1l1111l1_opy_[bstack1ll111_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫ⅄")]:
          logger.error(bstack1ll1lllll11l_opy_[bstack1ll111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ⅅ")])
      return None, None
  except Exception as error:
    logger.error(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢⅆ") +  str(error))
    return None, None
def bstack1lll1111l1ll_opy_():
  if os.getenv(bstack1ll111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬⅇ")) is None:
    return {
        bstack1ll111_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨⅈ"): bstack1ll111_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨⅉ"),
        bstack1ll111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ⅊"): bstack1ll111_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪ⅋")
    }
  data = {bstack1ll111_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭⅌"): current_time()}
  headers = {
      bstack1ll111_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭⅍"): bstack1ll111_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨⅎ") + os.getenv(bstack1ll111_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨ⅏")),
      bstack1ll111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ⅐"): bstack1ll111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭⅑")
  }
  response = bstack11111l1l_opy_(bstack1ll111_opy_ (u"ࠫࡕ࡛ࡔࠨ⅒"), bstack1lll11111l1l_opy_ + bstack1ll111_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧ⅓"), data, { bstack1ll111_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧ⅔"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1ll111_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣ⅕") + bstack1lllllll1ll_opy_().isoformat() + bstack1ll111_opy_ (u"ࠨ࡜ࠪ⅖"))
      return {bstack1ll111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩ⅗"): bstack1ll111_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫ⅘"), bstack1ll111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ⅙"): bstack1ll111_opy_ (u"ࠬ࠭⅚")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤ⅛") + str(error))
    return {
        bstack1ll111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧ⅜"): bstack1ll111_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧ⅝"),
        bstack1ll111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ⅞"): str(error)
    }
def bstack1lll111l1l11_opy_(bstack1lll111111l1_opy_):
    return re.match(bstack1ll111_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫ⅟"), bstack1lll111111l1_opy_.strip()) is not None
def bstack1l1l1l1l1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack1lll111l1ll1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack1lll111l1ll1_opy_ = desired_capabilities
        else:
          bstack1lll111l1ll1_opy_ = {}
        bstack1l1l1l11ll1_opy_ = (bstack1lll111l1ll1_opy_.get(bstack1ll111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪⅠ"), bstack1ll111_opy_ (u"ࠬ࠭Ⅱ")).lower() or caps.get(bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬⅢ"), bstack1ll111_opy_ (u"ࠧࠨⅣ")).lower())
        if bstack1l1l1l11ll1_opy_ == bstack1ll111_opy_ (u"ࠨ࡫ࡲࡷࠬⅤ"):
            return True
        if bstack1l1l1l11ll1_opy_ == bstack1ll111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪⅥ"):
            bstack1l1l1111lll_opy_ = str(float(caps.get(bstack1ll111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬⅦ")) or bstack1lll111l1ll1_opy_.get(bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬⅧ"), {}).get(bstack1ll111_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨⅨ"),bstack1ll111_opy_ (u"࠭ࠧⅩ"))))
            if bstack1l1l1l11ll1_opy_ == bstack1ll111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨⅪ") and int(bstack1l1l1111lll_opy_.split(bstack1ll111_opy_ (u"ࠨ࠰ࠪⅫ"))[0]) < float(bstack1lll111l111l_opy_):
                logger.warning(str(bstack1lll11111111_opy_))
                return False
            return True
        bstack1l11llll1ll_opy_ = caps.get(bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪⅬ"), {}).get(bstack1ll111_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧⅭ"), caps.get(bstack1ll111_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫⅮ"), bstack1ll111_opy_ (u"ࠬ࠭Ⅿ")))
        if bstack1l11llll1ll_opy_:
            logger.warning(bstack1ll111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥⅰ"))
            return False
        browser = caps.get(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬⅱ"), bstack1ll111_opy_ (u"ࠨࠩⅲ")).lower() or bstack1lll111l1ll1_opy_.get(bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧⅳ"), bstack1ll111_opy_ (u"ࠪࠫⅴ")).lower()
        if browser != bstack1ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫⅵ"):
            logger.warning(bstack1ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣⅶ"))
            return False
        browser_version = caps.get(bstack1ll111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧⅷ")) or caps.get(bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩⅸ")) or bstack1lll111l1ll1_opy_.get(bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩⅹ")) or bstack1lll111l1ll1_opy_.get(bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪⅺ"), {}).get(bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫⅻ")) or bstack1lll111l1ll1_opy_.get(bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬⅼ"), {}).get(bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧⅽ"))
        bstack1l1l1l1l111_opy_ = bstack1lll1111l1l1_opy_.bstack1l1l1l1l1l1_opy_
        bstack1lll111l1l1l_opy_ = False
        if config is not None:
          bstack1lll111l1l1l_opy_ = bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪⅾ") in config and str(config[bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫⅿ")]).lower() != bstack1ll111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧↀ")
        if os.environ.get(bstack1ll111_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧↁ"), bstack1ll111_opy_ (u"ࠪࠫↂ")).lower() == bstack1ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩↃ") or bstack1lll111l1l1l_opy_:
          bstack1l1l1l1l111_opy_ = bstack1lll1111l1l1_opy_.bstack1l1l1111ll1_opy_
        if browser_version and browser_version != bstack1ll111_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬↄ") and int(browser_version.split(bstack1ll111_opy_ (u"࠭࠮ࠨↅ"))[0]) <= bstack1l1l1l1l111_opy_:
          logger.warning(bstack1ll1l11llll_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࡽࡰ࡭ࡳࡥࡡ࠲࠳ࡼࡣࡸࡻࡰࡱࡱࡵࡸࡪࡪ࡟ࡤࡪࡵࡳࡲ࡫࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡾ࠰ࠪↆ"))
          return False
        if not options:
          bstack1l1l1l1lll1_opy_ = caps.get(bstack1ll111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ↇ")) or bstack1lll111l1ll1_opy_.get(bstack1ll111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧↈ"), {})
          if bstack1ll111_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ↉") in bstack1l1l1l1lll1_opy_.get(bstack1ll111_opy_ (u"ࠫࡦࡸࡧࡴࠩ↊"), []):
              logger.warning(bstack1ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢ↋"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1ll111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣ↌") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l1ll11l1ll_opy_ = config.get(bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ↍"), {})
    bstack1l1ll11l1ll_opy_[bstack1ll111_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫ↎")] = os.getenv(bstack1ll111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ↏"))
    bstack111l1lll11l_opy_ = json.loads(os.getenv(bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ←"), bstack1ll111_opy_ (u"ࠫࢀࢃࠧ↑"))).get(bstack1ll111_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭→"))
    if not config[bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨ↓")].get(bstack1ll111_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨ↔")):
      if bstack1ll111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ↕") in caps:
        caps[bstack1ll111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ↖")][bstack1ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ↗")] = bstack1l1ll11l1ll_opy_
        caps[bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬ↘")][bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ↙")][bstack1ll111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧ↚")] = bstack111l1lll11l_opy_
      else:
        caps[bstack1ll111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭↛")] = bstack1l1ll11l1ll_opy_
        caps[bstack1ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ↜")][bstack1ll111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ↝")] = bstack111l1lll11l_opy_
  except Exception as error:
    logger.debug(bstack1ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦ↞") +  str(error))
def bstack11ll1l1l_opy_(driver, bstack1lll1111l11l_opy_):
  try:
    setattr(driver, bstack1ll111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫ↟"), True)
    session = driver.session_id
    if session:
      bstack1lll1111111l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack1lll1111111l_opy_ = False
      bstack1lll1111111l_opy_ = url.scheme in [bstack1ll111_opy_ (u"ࠧ࡮ࡴࡵࡲࠥ↠"), bstack1ll111_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧ↡")]
      if bstack1lll1111111l_opy_:
        if bstack1lll1111l11l_opy_:
          logger.info(bstack1ll111_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢ↢"))
      return bstack1lll1111l11l_opy_
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ↣") + str(e))
    return False
def bstack11lll1lll1_opy_(driver, name, path):
  try:
    bstack1l1l1l111ll_opy_ = {
        bstack1ll111_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩ↤"): threading.current_thread().current_test_uuid,
        bstack1ll111_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨ↥"): os.environ.get(bstack1ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩ↦"), bstack1ll111_opy_ (u"ࠬ࠭↧")),
        bstack1ll111_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪ↨"): os.environ.get(bstack1ll111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫ↩"), bstack1ll111_opy_ (u"ࠨࠩ↪"))
    }
    bstack1l1l1l111_opy_ = bstack11lll11l1l_opy_.bstack111l11l11_opy_(EVENTS.bstack1ll1l11ll1_opy_.value)
    logger.debug(bstack1ll111_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬ↫"))
    try:
      if (bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ↬"), None) and bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭↭"), None)):
        scripts = {bstack1ll111_opy_ (u"ࠬࡹࡣࡢࡰࠪ↮"): bstack1l1l1l1lll_opy_.perform_scan}
        bstack1lll111l1111_opy_ = json.loads(scripts[bstack1ll111_opy_ (u"ࠨࡳࡤࡣࡱࠦ↯")].replace(bstack1ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ↰"), bstack1ll111_opy_ (u"ࠣࠤ↱")))
        bstack1lll111l1111_opy_[bstack1ll111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ↲")][bstack1ll111_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪ↳")] = None
        scripts[bstack1ll111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ↴")] = bstack1ll111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣ↵") + json.dumps(bstack1lll111l1111_opy_)
        bstack1l1l1l1lll_opy_.bstack1lllll1l1_opy_(scripts)
        bstack1l1l1l1lll_opy_.store()
        logger.debug(driver.execute_script(bstack1l1l1l1lll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1l1l1lll_opy_.perform_scan, {bstack1ll111_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨ↶"): name}))
      bstack11lll11l1l_opy_.end(EVENTS.bstack1ll1l11ll1_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ↷"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ↸"), True, None)
    except Exception as error:
      bstack11lll11l1l_opy_.end(EVENTS.bstack1ll1l11ll1_opy_.value, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ↹"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣ↺"), False, str(error))
    bstack1l1l1l111_opy_ = bstack11lll11l1l_opy_.bstack1111l1ll1ll_opy_(EVENTS.bstack1l1l11l1lll_opy_.value)
    bstack11lll11l1l_opy_.mark(bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ↻"))
    try:
      if (bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬ↼"), None) and bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨ↽"), None)):
        scripts = {bstack1ll111_opy_ (u"ࠧࡴࡥࡤࡲࠬ↾"): bstack1l1l1l1lll_opy_.perform_scan}
        bstack1lll111l1111_opy_ = json.loads(scripts[bstack1ll111_opy_ (u"ࠣࡵࡦࡥࡳࠨ↿")].replace(bstack1ll111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧ⇀"), bstack1ll111_opy_ (u"ࠥࠦ⇁")))
        bstack1lll111l1111_opy_[bstack1ll111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧ⇂")][bstack1ll111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬ⇃")] = None
        scripts[bstack1ll111_opy_ (u"ࠨࡳࡤࡣࡱࠦ⇄")] = bstack1ll111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ⇅") + json.dumps(bstack1lll111l1111_opy_)
        bstack1l1l1l1lll_opy_.bstack1lllll1l1_opy_(scripts)
        bstack1l1l1l1lll_opy_.store()
        logger.debug(driver.execute_script(bstack1l1l1l1lll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1l1l1lll_opy_.bstack1lll1111lll1_opy_, bstack1l1l1l111ll_opy_))
      bstack11lll11l1l_opy_.end(bstack1l1l1l111_opy_, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ⇆"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ⇇"),True, None)
    except Exception as error:
      bstack11lll11l1l_opy_.end(bstack1l1l1l111_opy_, bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥ⇈"), bstack1l1l1l111_opy_ + bstack1ll111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤ⇉"),False, str(error))
    logger.info(bstack1ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣ⇊"))
    try:
      bstack1l1l1l11l11_opy_ = {
        bstack1ll111_opy_ (u"ࠨࡲࡦࡳࡸࡩࡸࡺࠢ⇋"): {
          bstack1ll111_opy_ (u"ࠢࡤࡱࡰࡱࡦࡴࡤࠣ⇌"): bstack1ll111_opy_ (u"ࠣࡃ࠴࠵࡞ࡥࡓࡂࡘࡈࡣࡗࡋࡓࡖࡎࡗࡗࠧ⇍"),
        },
        bstack1ll111_opy_ (u"ࠤࡵࡩࡸࡶ࡯࡯ࡵࡨࠦ⇎"): {
          bstack1ll111_opy_ (u"ࠥࡦࡴࡪࡹࠣ⇏"): {
            bstack1ll111_opy_ (u"ࠦࡲࡹࡧࠣ⇐"): bstack1ll111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣ⇑"),
            bstack1ll111_opy_ (u"ࠨࡳࡶࡥࡦࡩࡸࡹࠢ⇒"): True
          }
        }
      }
      bstack1l11llll_opy_.info(json.dumps(bstack1l1l1l11l11_opy_, separators=(bstack1ll111_opy_ (u"ࠧ࠭ࠩ⇓"), bstack1ll111_opy_ (u"ࠨ࠼ࠪ⇔"))))
    except Exception as bstack111ll1ll1l_opy_:
      logger.debug(bstack1ll111_opy_ (u"ࠤࡉࡥ࡮ࡲࡥࡥࠢࡷࡳࠥࡲ࡯ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡥࡻ࡫ࠠࡳࡧࡶࡹࡱࡺࡳࠡࡦࡤࡸࡦࡀࠠࠣ⇕") + str(bstack111ll1ll1l_opy_) + bstack1ll111_opy_ (u"ࠥࠦ⇖"))
  except Exception as bstack1l1l11111ll_opy_:
    logger.error(bstack1ll111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ⇗") + str(path) + bstack1ll111_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢ⇘") + str(bstack1l1l11111ll_opy_))
def bstack1lll111l11ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1ll111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧ⇙")) and str(caps.get(bstack1ll111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨ⇚"))).lower() == bstack1ll111_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤ⇛"):
        bstack1l1l1111lll_opy_ = caps.get(bstack1ll111_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦ⇜")) or caps.get(bstack1ll111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧ⇝"))
        if bstack1l1l1111lll_opy_ and int(str(bstack1l1l1111lll_opy_)) < bstack1lll111l111l_opy_:
            return False
    return True
def bstack1111llll1_opy_(config):
  if bstack1ll111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⇞") in config:
        return config[bstack1ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⇟")]
  for platform in config.get(bstack1ll111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ⇠"), []):
      if bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⇡") in platform:
          return platform[bstack1ll111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⇢")]
  return None
def bstack111l1l1lll_opy_(bstack11ll111l_opy_):
  try:
    browser_name = bstack11ll111l_opy_[bstack1ll111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨ⇣")]
    browser_version = bstack11ll111l_opy_[bstack1ll111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⇤")]
    chrome_options = bstack11ll111l_opy_[bstack1ll111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࡣࡴࡶࡴࡪࡱࡱࡷࠬ⇥")]
    try:
        bstack1ll1llllll1l_opy_ = int(browser_version.split(bstack1ll111_opy_ (u"ࠬ࠴ࠧ⇦"))[0])
    except ValueError as e:
        logger.error(bstack1ll111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡨࡵ࡮ࡷࡧࡵࡸ࡮ࡴࡧࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠥ⇧") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1ll111_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧ⇨")):
        logger.warning(bstack1ll111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦ⇩"))
        return False
    if bstack1ll1llllll1l_opy_ < bstack1lll1111l1l1_opy_.bstack1l1l1111ll1_opy_:
        logger.warning(bstack1ll1l11llll_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡲࡦࡳࡸ࡭ࡷ࡫ࡳࠡࡅ࡫ࡶࡴࡳࡥࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡾࡇࡔࡔࡓࡕࡃࡑࡘࡘ࠴ࡍࡊࡐࡌࡑ࡚ࡓ࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡘࡔࡕࡕࡒࡕࡇࡇࡣࡈࡎࡒࡐࡏࡈࡣ࡛ࡋࡒࡔࡋࡒࡒࢂࠦ࡯ࡳࠢ࡫࡭࡬࡮ࡥࡳ࠰ࠪ⇪"))
        return False
    if chrome_options and any(bstack1ll111_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧ⇫") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1ll111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨ⇬"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1ll111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤ࡮ࡴࠠࡤࡪࡨࡧࡰ࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡸࡻࡰࡱࡱࡵࡸࠥ࡬࡯ࡳࠢ࡯ࡳࡨࡧ࡬ࠡࡅ࡫ࡶࡴࡳࡥ࠻ࠢࠥ⇭") + str(e))
    return False
def bstack1l11llll1_opy_(bstack111llll1l_opy_, config):
    try:
      bstack1l11lll11l1_opy_ = bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⇮") in config and config[bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⇯")] == True
      bstack1lll111l1l1l_opy_ = bstack1ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⇰") in config and str(config[bstack1ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⇱")]).lower() != bstack1ll111_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ⇲")
      if not (bstack1l11lll11l1_opy_ and (not bstack1l111l111_opy_(config) or bstack1lll111l1l1l_opy_)):
        return bstack111llll1l_opy_
      bstack1lll11111ll1_opy_ = bstack1l1l1l1lll_opy_.bstack1lll11ll111l_opy_
      if bstack1lll11111ll1_opy_ is None:
        logger.debug(bstack1ll111_opy_ (u"ࠦࡌࡵ࡯ࡨ࡮ࡨࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷࠥࡧࡲࡦࠢࡑࡳࡳ࡫ࠢ⇳"))
        return bstack111llll1l_opy_
      bstack1lll11111lll_opy_ = int(str(bstack111ll111lll_opy_()).split(bstack1ll111_opy_ (u"ࠬ࠴ࠧ⇴"))[0])
      logger.debug(bstack1ll111_opy_ (u"ࠨࡓࡦ࡮ࡨࡲ࡮ࡻ࡭ࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡧࡩࡹ࡫ࡣࡵࡧࡧ࠾ࠥࠨ⇵") + str(bstack1lll11111lll_opy_) + bstack1ll111_opy_ (u"ࠢࠣ⇶"))
      if bstack1lll11111lll_opy_ == 3 and isinstance(bstack111llll1l_opy_, dict) and bstack1ll111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⇷") in bstack111llll1l_opy_ and bstack1lll11111ll1_opy_ is not None:
        if bstack1ll111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ⇸") not in bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ⇹")]:
          bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ⇺")][bstack1ll111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ⇻")] = {}
        if bstack1ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫ⇼") in bstack1lll11111ll1_opy_:
          if bstack1ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬ⇽") not in bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ⇾")][bstack1ll111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ⇿")]:
            bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ∀")][bstack1ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ∁")][bstack1ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪ∂")] = []
          for arg in bstack1lll11111ll1_opy_[bstack1ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫ∃")]:
            if arg not in bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ∄")][bstack1ll111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭∅")][bstack1ll111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ∆")]:
              bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ∇")][bstack1ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ∈")][bstack1ll111_opy_ (u"ࠬࡧࡲࡨࡵࠪ∉")].append(arg)
        if bstack1ll111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ∊") in bstack1lll11111ll1_opy_:
          if bstack1ll111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ∋") not in bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ∌")][bstack1ll111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ∍")]:
            bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ∎")][bstack1ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ∏")][bstack1ll111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ∐")] = []
          for ext in bstack1lll11111ll1_opy_[bstack1ll111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ∑")]:
            if ext not in bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ−")][bstack1ll111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭∓")][bstack1ll111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭∔")]:
              bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ∕")][bstack1ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ∖")][bstack1ll111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ∗")].append(ext)
        if bstack1ll111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ∘") in bstack1lll11111ll1_opy_:
          if bstack1ll111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭∙") not in bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ√")][bstack1ll111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧ∛")]:
            bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ∜")][bstack1ll111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ∝")][bstack1ll111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ∞")] = {}
          bstack11l1111ll11_opy_(bstack111llll1l_opy_[bstack1ll111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭∟")][bstack1ll111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ∠")][bstack1ll111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ∡")],
                    bstack1lll11111ll1_opy_[bstack1ll111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ∢")])
        os.environ[bstack1ll111_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨ∣")] = bstack1ll111_opy_ (u"ࠫࡹࡸࡵࡦࠩ∤")
        return bstack111llll1l_opy_
      else:
        chrome_options = None
        if isinstance(bstack111llll1l_opy_, ChromeOptions):
          chrome_options = bstack111llll1l_opy_
        elif isinstance(bstack111llll1l_opy_, dict):
          for value in bstack111llll1l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack111llll1l_opy_, dict):
            bstack111llll1l_opy_[bstack1ll111_opy_ (u"ࠬࡵࡰࡵ࡫ࡲࡲࡸ࠭∥")] = chrome_options
          else:
            bstack111llll1l_opy_ = chrome_options
        if bstack1lll11111ll1_opy_ is not None:
          if bstack1ll111_opy_ (u"࠭ࡡࡳࡩࡶࠫ∦") in bstack1lll11111ll1_opy_:
                bstack1ll1llllll11_opy_ = chrome_options.arguments or []
                new_args = bstack1lll11111ll1_opy_[bstack1ll111_opy_ (u"ࠧࡢࡴࡪࡷࠬ∧")]
                for arg in new_args:
                    if arg not in bstack1ll1llllll11_opy_:
                        chrome_options.add_argument(arg)
          if bstack1ll111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ∨") in bstack1lll11111ll1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1ll111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭∩"), [])
                bstack1lll111l1lll_opy_ = bstack1lll11111ll1_opy_[bstack1ll111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ∪")]
                for extension in bstack1lll111l1lll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1ll111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ∫") in bstack1lll11111ll1_opy_:
                bstack1lll11111l11_opy_ = chrome_options.experimental_options.get(bstack1ll111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ∬"), {})
                bstack1ll1llllllll_opy_ = bstack1lll11111ll1_opy_[bstack1ll111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ∭")]
                bstack11l1111ll11_opy_(bstack1lll11111l11_opy_, bstack1ll1llllllll_opy_)
                chrome_options.add_experimental_option(bstack1ll111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭∮"), bstack1lll11111l11_opy_)
        os.environ[bstack1ll111_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭∯")] = bstack1ll111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧ∰")
        return bstack111llll1l_opy_
    except Exception as e:
      logger.error(bstack1ll111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡣࡧࡨ࡮ࡴࡧࠡࡰࡲࡲ࠲ࡈࡓࠡ࡫ࡱࡪࡷࡧࠠࡢ࠳࠴ࡽࠥࡩࡨࡳࡱࡰࡩࠥࡵࡰࡵ࡫ࡲࡲࡸࡀࠠࠣ∱") + str(e))
      return bstack111llll1l_opy_