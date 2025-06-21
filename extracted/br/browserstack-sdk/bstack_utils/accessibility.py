# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11lll111l1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1ll1111_opy_ as bstack11ll1ll1l1l_opy_, EVENTS
from bstack_utils.bstack1111ll1l1_opy_ import bstack1111ll1l1_opy_
from bstack_utils.helper import bstack1lllll1l1l_opy_, bstack111ll111l1_opy_, bstack11l1l1l1_opy_, bstack11ll1lll11l_opy_, \
  bstack11ll1l1llll_opy_, bstack1l1l1ll11_opy_, get_host_info, bstack11lll1l111l_opy_, bstack1l1llll1ll_opy_, bstack111ll11111_opy_, bstack11lll11lll1_opy_, bstack11ll1lll1l1_opy_, bstack111l1ll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1llll1l111_opy_ import get_logger
from bstack_utils.bstack11ll1ll1_opy_ import bstack1lll1ll11l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack11ll1ll1_opy_ = bstack1lll1ll11l1_opy_()
@bstack111ll11111_opy_(class_method=False)
def _11ll1ll111l_opy_(driver, bstack1111l11111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1l1l1_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩᖰ"): caps.get(bstack1l1l1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᖱ"), None),
        bstack1l1l1l1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᖲ"): bstack1111l11111_opy_.get(bstack1l1l1l1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᖳ"), None),
        bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᖴ"): caps.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᖵ"), None),
        bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᖶ"): caps.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᖷ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᖸ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1l1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖹ"), None) is None or os.environ[bstack1l1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᖺ")] == bstack1l1l1l1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᖻ"):
        return False
    return True
def bstack111lll11_opy_(config):
  return config.get(bstack1l1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᖼ"), False) or any([p.get(bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᖽ"), False) == True for p in config.get(bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᖾ"), [])])
def bstack1l1l1ll1_opy_(config, bstack1ll111l111_opy_):
  try:
    bstack11lll111lll_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᖿ"), False)
    if int(bstack1ll111l111_opy_) < len(config.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᗀ"), [])) and config[bstack1l1l1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᗁ")][bstack1ll111l111_opy_]:
      bstack11lll11l11l_opy_ = config[bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᗂ")][bstack1ll111l111_opy_].get(bstack1l1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᗃ"), None)
    else:
      bstack11lll11l11l_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᗄ"), None)
    if bstack11lll11l11l_opy_ != None:
      bstack11lll111lll_opy_ = bstack11lll11l11l_opy_
    bstack11ll1ll1lll_opy_ = os.getenv(bstack1l1l1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᗅ")) is not None and len(os.getenv(bstack1l1l1l1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᗆ"))) > 0 and os.getenv(bstack1l1l1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᗇ")) != bstack1l1l1l1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᗈ")
    return bstack11lll111lll_opy_ and bstack11ll1ll1lll_opy_
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᗉ") + str(error))
  return False
def bstack11lll1llll_opy_(test_tags):
  bstack1ll11lllll1_opy_ = os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᗊ"))
  if bstack1ll11lllll1_opy_ is None:
    return True
  bstack1ll11lllll1_opy_ = json.loads(bstack1ll11lllll1_opy_)
  try:
    include_tags = bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᗋ")] if bstack1l1l1l1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᗌ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᗍ")], list) else []
    exclude_tags = bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᗎ")] if bstack1l1l1l1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᗏ") in bstack1ll11lllll1_opy_ and isinstance(bstack1ll11lllll1_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᗐ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᗑ") + str(error))
  return False
def bstack11ll1lll1ll_opy_(config, bstack11ll1l1l1ll_opy_, bstack11lll111111_opy_, bstack11ll1l1ll1l_opy_):
  bstack11ll1l1lll1_opy_ = bstack11ll1lll11l_opy_(config)
  bstack11ll1llllll_opy_ = bstack11ll1l1llll_opy_(config)
  if bstack11ll1l1lll1_opy_ is None or bstack11ll1llllll_opy_ is None:
    logger.error(bstack1l1l1l1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᗒ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᗓ"), bstack1l1l1l1_opy_ (u"ࠩࡾࢁࠬᗔ")))
    data = {
        bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᗕ"): config[bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᗖ")],
        bstack1l1l1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᗗ"): config.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᗘ"), os.path.basename(os.getcwd())),
        bstack1l1l1l1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪᗙ"): bstack1lllll1l1l_opy_(),
        bstack1l1l1l1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᗚ"): config.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᗛ"), bstack1l1l1l1_opy_ (u"ࠪࠫᗜ")),
        bstack1l1l1l1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᗝ"): {
            bstack1l1l1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᗞ"): bstack11ll1l1l1ll_opy_,
            bstack1l1l1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᗟ"): bstack11lll111111_opy_,
            bstack1l1l1l1_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᗠ"): __version__,
            bstack1l1l1l1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᗡ"): bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᗢ"),
            bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᗣ"): bstack1l1l1l1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᗤ"),
            bstack1l1l1l1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᗥ"): bstack11ll1l1ll1l_opy_
        },
        bstack1l1l1l1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᗦ"): settings,
        bstack1l1l1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨᗧ"): bstack11lll1l111l_opy_(),
        bstack1l1l1l1_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨᗨ"): bstack1l1l1ll11_opy_(),
        bstack1l1l1l1_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫᗩ"): get_host_info(),
        bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᗪ"): bstack11l1l1l1_opy_(config)
    }
    headers = {
        bstack1l1l1l1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᗫ"): bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᗬ"),
    }
    config = {
        bstack1l1l1l1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᗭ"): (bstack11ll1l1lll1_opy_, bstack11ll1llllll_opy_),
        bstack1l1l1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᗮ"): headers
    }
    response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᗯ"), bstack11ll1ll1l1l_opy_ + bstack1l1l1l1_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩᗰ"), data, config)
    bstack11lll111l11_opy_ = response.json()
    if bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᗱ")]:
      parsed = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᗲ"), bstack1l1l1l1_opy_ (u"ࠬࢁࡽࠨᗳ")))
      parsed[bstack1l1l1l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗴ")] = bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᗵ")][bstack1l1l1l1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗶ")]
      os.environ[bstack1l1l1l1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᗷ")] = json.dumps(parsed)
      bstack1111ll1l1_opy_.bstack11ll111ll1_opy_(bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠪࡨࡦࡺࡡࠨᗸ")][bstack1l1l1l1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᗹ")])
      bstack1111ll1l1_opy_.bstack11lll111ll1_opy_(bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠬࡪࡡࡵࡣࠪᗺ")][bstack1l1l1l1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᗻ")])
      bstack1111ll1l1_opy_.store()
      return bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᗼ")][bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᗽ")], bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᗾ")][bstack1l1l1l1_opy_ (u"ࠪ࡭ࡩ࠭ᗿ")]
    else:
      logger.error(bstack1l1l1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬᘀ") + bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘁ")])
      if bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘂ")] == bstack1l1l1l1_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩᘃ"):
        for bstack11lll11ll11_opy_ in bstack11lll111l11_opy_[bstack1l1l1l1_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᘄ")]:
          logger.error(bstack11lll11ll11_opy_[bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᘅ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦᘆ") +  str(error))
    return None, None
def bstack11ll1ll11ll_opy_():
  if os.getenv(bstack1l1l1l1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᘇ")) is None:
    return {
        bstack1l1l1l1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᘈ"): bstack1l1l1l1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᘉ"),
        bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘊ"): bstack1l1l1l1_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧᘋ")
    }
  data = {bstack1l1l1l1_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪᘌ"): bstack1lllll1l1l_opy_()}
  headers = {
      bstack1l1l1l1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᘍ"): bstack1l1l1l1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬᘎ") + os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥᘏ")),
      bstack1l1l1l1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᘐ"): bstack1l1l1l1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᘑ")
  }
  response = bstack1l1llll1ll_opy_(bstack1l1l1l1_opy_ (u"ࠨࡒࡘࡘࠬᘒ"), bstack11ll1ll1l1l_opy_ + bstack1l1l1l1_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫᘓ"), data, { bstack1l1l1l1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᘔ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1l1l1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧᘕ") + bstack111ll111l1_opy_().isoformat() + bstack1l1l1l1_opy_ (u"ࠬࡠࠧᘖ"))
      return {bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᘗ"): bstack1l1l1l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᘘ"), bstack1l1l1l1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᘙ"): bstack1l1l1l1_opy_ (u"ࠩࠪᘚ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨᘛ") + str(error))
    return {
        bstack1l1l1l1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᘜ"): bstack1l1l1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᘝ"),
        bstack1l1l1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘞ"): str(error)
    }
def bstack11ll1lllll1_opy_(bstack11ll1l1ll11_opy_):
    return re.match(bstack1l1l1l1_opy_ (u"ࡲࠨࡠ࡟ࡨ࠰࠮࡜࠯࡞ࡧ࠯࠮ࡅࠤࠨᘟ"), bstack11ll1l1ll11_opy_.strip()) is not None
def bstack11ll1l1l1_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11lll1111l1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll1111l1_opy_ = desired_capabilities
        else:
          bstack11lll1111l1_opy_ = {}
        bstack11ll1llll1l_opy_ = (bstack11lll1111l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᘠ"), bstack1l1l1l1_opy_ (u"ࠩࠪᘡ")).lower() or caps.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᘢ"), bstack1l1l1l1_opy_ (u"ࠫࠬᘣ")).lower())
        if bstack11ll1llll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠬ࡯࡯ࡴࠩᘤ"):
            return True
        if bstack11ll1llll1l_opy_ == bstack1l1l1l1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧᘥ"):
            bstack11lll11l1ll_opy_ = str(float(caps.get(bstack1l1l1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᘦ")) or bstack11lll1111l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘧ"), {}).get(bstack1l1l1l1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘨ"),bstack1l1l1l1_opy_ (u"ࠪࠫᘩ"))))
            if bstack11ll1llll1l_opy_ == bstack1l1l1l1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᘪ") and int(bstack11lll11l1ll_opy_.split(bstack1l1l1l1_opy_ (u"ࠬ࠴ࠧᘫ"))[0]) < float(bstack11lll1l1l1l_opy_):
                logger.warning(str(bstack11lll1l1111_opy_))
                return False
            return True
        bstack1ll1l11l11l_opy_ = caps.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘬ"), {}).get(bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᘭ"), caps.get(bstack1l1l1l1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᘮ"), bstack1l1l1l1_opy_ (u"ࠩࠪᘯ")))
        if bstack1ll1l11l11l_opy_:
            logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᘰ"))
            return False
        browser = caps.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᘱ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ᘲ")).lower() or bstack11lll1111l1_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᘳ"), bstack1l1l1l1_opy_ (u"ࠧࠨᘴ")).lower()
        if browser != bstack1l1l1l1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᘵ"):
            logger.warning(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᘶ"))
            return False
        browser_version = caps.get(bstack1l1l1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᘷ")) or caps.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᘸ")) or bstack11lll1111l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘹ")) or bstack11lll1111l1_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᘺ"), {}).get(bstack1l1l1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘻ")) or bstack11lll1111l1_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᘼ"), {}).get(bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᘽ"))
        bstack1ll1l11l1ll_opy_ = bstack11lll111l1l_opy_.bstack1ll11ll11l1_opy_
        bstack11ll1ll1l11_opy_ = False
        if config is not None:
          bstack11ll1ll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᘾ") in config and str(config[bstack1l1l1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᘿ")]).lower() != bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᙀ")
        if os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᙁ"), bstack1l1l1l1_opy_ (u"ࠧࠨᙂ")).lower() == bstack1l1l1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᙃ") or bstack11ll1ll1l11_opy_:
          bstack1ll1l11l1ll_opy_ = bstack11lll111l1l_opy_.bstack1ll11llll1l_opy_
        if browser_version and browser_version != bstack1l1l1l1_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᙄ") and int(browser_version.split(bstack1l1l1l1_opy_ (u"ࠪ࠲ࠬᙅ"))[0]) <= bstack1ll1l11l1ll_opy_:
          logger.warning(bstack1llll1l11l1_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥࢁ࡭ࡪࡰࡢࡥ࠶࠷ࡹࡠࡵࡸࡴࡵࡵࡲࡵࡧࡧࡣࡨ࡮ࡲࡰ࡯ࡨࡣࡻ࡫ࡲࡴ࡫ࡲࡲࢂ࠴ࠧᙆ"))
          return False
        if not options:
          bstack1ll1l111l11_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᙇ")) or bstack11lll1111l1_opy_.get(bstack1l1l1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᙈ"), {})
          if bstack1l1l1l1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᙉ") in bstack1ll1l111l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᙊ"), []):
              logger.warning(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᙋ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᙌ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll1l11ll1_opy_ = config.get(bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᙍ"), {})
    bstack1lll1l11ll1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᙎ")] = os.getenv(bstack1l1l1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᙏ"))
    bstack11ll1llll11_opy_ = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᙐ"), bstack1l1l1l1_opy_ (u"ࠨࡽࢀࠫᙑ"))).get(bstack1l1l1l1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙒ"))
    if not config[bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᙓ")].get(bstack1l1l1l1_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥᙔ")):
      if bstack1l1l1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙕ") in caps:
        caps[bstack1l1l1l1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᙖ")][bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᙗ")] = bstack1lll1l11ll1_opy_
        caps[bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᙘ")][bstack1l1l1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᙙ")][bstack1l1l1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᙚ")] = bstack11ll1llll11_opy_
      else:
        caps[bstack1l1l1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᙛ")] = bstack1lll1l11ll1_opy_
        caps[bstack1l1l1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᙜ")][bstack1l1l1l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᙝ")] = bstack11ll1llll11_opy_
  except Exception as error:
    logger.debug(bstack1l1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࠣᙞ") +  str(error))
def bstack1l1l1l111l_opy_(driver, bstack11lll1111ll_opy_):
  try:
    setattr(driver, bstack1l1l1l1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨᙟ"), True)
    session = driver.session_id
    if session:
      bstack11lll11l1l1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll11l1l1_opy_ = False
      bstack11lll11l1l1_opy_ = url.scheme in [bstack1l1l1l1_opy_ (u"ࠤ࡫ࡸࡹࡶࠢᙠ"), bstack1l1l1l1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᙡ")]
      if bstack11lll11l1l1_opy_:
        if bstack11lll1111ll_opy_:
          logger.info(bstack1l1l1l1_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦᙢ"))
      return bstack11lll1111ll_opy_
  except Exception as e:
    logger.error(bstack1l1l1l1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᙣ") + str(e))
    return False
def bstack1ll1lll111_opy_(driver, name, path):
  try:
    bstack1ll11l11lll_opy_ = {
        bstack1l1l1l1_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭ᙤ"): threading.current_thread().current_test_uuid,
        bstack1l1l1l1_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᙥ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᙦ"), bstack1l1l1l1_opy_ (u"ࠩࠪᙧ")),
        bstack1l1l1l1_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧᙨ"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᙩ"), bstack1l1l1l1_opy_ (u"ࠬ࠭ᙪ"))
    }
    bstack1ll111ll1l1_opy_ = bstack11ll1ll1_opy_.bstack1ll11l1ll1l_opy_(EVENTS.bstack1111l11l_opy_.value)
    logger.debug(bstack1l1l1l1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᙫ"))
    try:
      if (bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᙬ"), None) and bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ᙭"), None)):
        scripts = {bstack1l1l1l1_opy_ (u"ࠩࡶࡧࡦࡴࠧ᙮"): bstack1111ll1l1_opy_.perform_scan}
        bstack11ll1lll111_opy_ = json.loads(scripts[bstack1l1l1l1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᙯ")].replace(bstack1l1l1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᙰ"), bstack1l1l1l1_opy_ (u"ࠧࠨᙱ")))
        bstack11ll1lll111_opy_[bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᙲ")][bstack1l1l1l1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᙳ")] = None
        scripts[bstack1l1l1l1_opy_ (u"ࠣࡵࡦࡥࡳࠨᙴ")] = bstack1l1l1l1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᙵ") + json.dumps(bstack11ll1lll111_opy_)
        bstack1111ll1l1_opy_.bstack11ll111ll1_opy_(scripts)
        bstack1111ll1l1_opy_.store()
        logger.debug(driver.execute_script(bstack1111ll1l1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1111ll1l1_opy_.perform_scan, {bstack1l1l1l1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥᙶ"): name}))
      bstack11ll1ll1_opy_.end(EVENTS.bstack1111l11l_opy_.value, bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᙷ"), bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᙸ"), True, None)
    except Exception as error:
      bstack11ll1ll1_opy_.end(EVENTS.bstack1111l11l_opy_.value, bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᙹ"), bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᙺ"), False, str(error))
    bstack1ll111ll1l1_opy_ = bstack11ll1ll1_opy_.bstack11lll1l11ll_opy_(EVENTS.bstack1ll11lll1ll_opy_.value)
    bstack11ll1ll1_opy_.mark(bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᙻ"))
    try:
      if (bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᙼ"), None) and bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᙽ"), None)):
        scripts = {bstack1l1l1l1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᙾ"): bstack1111ll1l1_opy_.perform_scan}
        bstack11ll1lll111_opy_ = json.loads(scripts[bstack1l1l1l1_opy_ (u"ࠧࡹࡣࡢࡰࠥᙿ")].replace(bstack1l1l1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ "), bstack1l1l1l1_opy_ (u"ࠢࠣᚁ")))
        bstack11ll1lll111_opy_[bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᚂ")][bstack1l1l1l1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩᚃ")] = None
        scripts[bstack1l1l1l1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᚄ")] = bstack1l1l1l1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᚅ") + json.dumps(bstack11ll1lll111_opy_)
        bstack1111ll1l1_opy_.bstack11ll111ll1_opy_(scripts)
        bstack1111ll1l1_opy_.store()
        logger.debug(driver.execute_script(bstack1111ll1l1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1111ll1l1_opy_.bstack11lll1l1l11_opy_, bstack1ll11l11lll_opy_))
      bstack11ll1ll1_opy_.end(bstack1ll111ll1l1_opy_, bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᚆ"), bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᚇ"),True, None)
    except Exception as error:
      bstack11ll1ll1_opy_.end(bstack1ll111ll1l1_opy_, bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᚈ"), bstack1ll111ll1l1_opy_ + bstack1l1l1l1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᚉ"),False, str(error))
    logger.info(bstack1l1l1l1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧᚊ"))
  except Exception as bstack1ll11ll111l_opy_:
    logger.error(bstack1l1l1l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᚋ") + str(path) + bstack1l1l1l1_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᚌ") + str(bstack1ll11ll111l_opy_))
def bstack11ll1l1l1l1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1l1l1_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᚍ")) and str(caps.get(bstack1l1l1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᚎ"))).lower() == bstack1l1l1l1_opy_ (u"ࠢࡢࡰࡧࡶࡴ࡯ࡤࠣᚏ"):
        bstack11lll11l1ll_opy_ = caps.get(bstack1l1l1l1_opy_ (u"ࠣࡣࡳࡴ࡮ࡻ࡭࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᚐ")) or caps.get(bstack1l1l1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᚑ"))
        if bstack11lll11l1ll_opy_ and int(str(bstack11lll11l1ll_opy_)) < bstack11lll1l1l1l_opy_:
            return False
    return True
def bstack111llll1_opy_(config):
  if bstack1l1l1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚒ") in config:
        return config[bstack1l1l1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚓ")]
  for platform in config.get(bstack1l1l1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᚔ"), []):
      if bstack1l1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚕ") in platform:
          return platform[bstack1l1l1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚖ")]
  return None
def bstack1l1ll1l11_opy_(bstack1lll1l111l_opy_):
  try:
    browser_name = bstack1lll1l111l_opy_[bstack1l1l1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᚗ")]
    browser_version = bstack1lll1l111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᚘ")]
    chrome_options = bstack1lll1l111l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫᚙ")]
    try:
        bstack11lll11ll1l_opy_ = int(browser_version.split(bstack1l1l1l1_opy_ (u"ࠫ࠳࠭ᚚ"))[0])
    except ValueError as e:
        logger.error(bstack1l1l1l1_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡴࡶࡦࡴࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠤ᚛") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l1l1l1_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭᚜")):
        logger.warning(bstack1l1l1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᚝"))
        return False
    if bstack11lll11ll1l_opy_ < bstack11lll111l1l_opy_.bstack1ll11llll1l_opy_:
        logger.warning(bstack1llll1l11l1_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷ࡬ࡶࡪࡹࠠࡄࡪࡵࡳࡲ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡽࡆࡓࡓ࡙ࡔࡂࡐࡗࡗ࠳ࡓࡉࡏࡋࡐ࡙ࡒࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡗࡓࡔࡔࡘࡔࡆࡆࡢࡇࡍࡘࡏࡎࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࢁࠥࡵࡲࠡࡪ࡬࡫࡭࡫ࡲ࠯ࠩ᚞"))
        return False
    if chrome_options and any(bstack1l1l1l1_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭᚟") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1l1l1l1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᚠ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l1l1l1_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡺࡶࡰࡰࡴࡷࠤ࡫ࡵࡲࠡ࡮ࡲࡧࡦࡲࠠࡄࡪࡵࡳࡲ࡫࠺ࠡࠤᚡ") + str(e))
    return False
def bstack1l1ll11l_opy_(bstack11lll111l_opy_, config):
    try:
      bstack1ll111lllll_opy_ = bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚢ") in config and config[bstack1l1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚣ")] == True
      bstack11ll1ll1l11_opy_ = bstack1l1l1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᚤ") in config and str(config[bstack1l1l1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᚥ")]).lower() != bstack1l1l1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᚦ")
      if not (bstack1ll111lllll_opy_ and (not bstack11l1l1l1_opy_(config) or bstack11ll1ll1l11_opy_)):
        return bstack11lll111l_opy_
      bstack11ll1ll11l1_opy_ = bstack1111ll1l1_opy_.bstack11lll1l11l1_opy_
      if bstack11ll1ll11l1_opy_ is None:
        logger.debug(bstack1l1l1l1_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶࠤࡦࡸࡥࠡࡐࡲࡲࡪࠨᚧ"))
        return bstack11lll111l_opy_
      bstack11lll11l111_opy_ = int(str(bstack11ll1lll1l1_opy_()).split(bstack1l1l1l1_opy_ (u"ࠫ࠳࠭ᚨ"))[0])
      logger.debug(bstack1l1l1l1_opy_ (u"࡙ࠧࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡦࡨࡸࡪࡩࡴࡦࡦ࠽ࠤࠧᚩ") + str(bstack11lll11l111_opy_) + bstack1l1l1l1_opy_ (u"ࠨࠢᚪ"))
      if bstack11lll11l111_opy_ == 3 and isinstance(bstack11lll111l_opy_, dict) and bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚫ") in bstack11lll111l_opy_ and bstack11ll1ll11l1_opy_ is not None:
        if bstack1l1l1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚬ") not in bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᚭ")]:
          bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᚮ")][bstack1l1l1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚯ")] = {}
        if bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᚰ") in bstack11ll1ll11l1_opy_:
          if bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫᚱ") not in bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᚲ")][bstack1l1l1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚳ")]:
            bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᚴ")][bstack1l1l1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚵ")][bstack1l1l1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩᚶ")] = []
          for arg in bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᚷ")]:
            if arg not in bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚸ")][bstack1l1l1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚹ")][bstack1l1l1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᚺ")]:
              bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᚻ")][bstack1l1l1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚼ")][bstack1l1l1l1_opy_ (u"ࠫࡦࡸࡧࡴࠩᚽ")].append(arg)
        if bstack1l1l1l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᚾ") in bstack11ll1ll11l1_opy_:
          if bstack1l1l1l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᚿ") not in bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᛀ")][bstack1l1l1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛁ")]:
            bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᛂ")][bstack1l1l1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᛃ")][bstack1l1l1l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᛄ")] = []
          for ext in bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᛅ")]:
            if ext not in bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛆ")][bstack1l1l1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛇ")][bstack1l1l1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᛈ")]:
              bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᛉ")][bstack1l1l1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᛊ")][bstack1l1l1l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᛋ")].append(ext)
        if bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᛌ") in bstack11ll1ll11l1_opy_:
          if bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᛍ") not in bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᛎ")][bstack1l1l1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛏ")]:
            bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᛐ")][bstack1l1l1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᛑ")][bstack1l1l1l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᛒ")] = {}
          bstack11lll11lll1_opy_(bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᛓ")][bstack1l1l1l1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᛔ")][bstack1l1l1l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᛕ")],
                    bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᛖ")])
        os.environ[bstack1l1l1l1_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧᛗ")] = bstack1l1l1l1_opy_ (u"ࠪࡸࡷࡻࡥࠨᛘ")
        return bstack11lll111l_opy_
      else:
        chrome_options = None
        if isinstance(bstack11lll111l_opy_, ChromeOptions):
          chrome_options = bstack11lll111l_opy_
        elif isinstance(bstack11lll111l_opy_, dict):
          for value in bstack11lll111l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11lll111l_opy_, dict):
            bstack11lll111l_opy_[bstack1l1l1l1_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬᛙ")] = chrome_options
          else:
            bstack11lll111l_opy_ = chrome_options
        if bstack11ll1ll11l1_opy_ is not None:
          if bstack1l1l1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᛚ") in bstack11ll1ll11l1_opy_:
                bstack11ll1ll1ll1_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"࠭ࡡࡳࡩࡶࠫᛛ")]
                for arg in new_args:
                    if arg not in bstack11ll1ll1ll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l1l1l1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᛜ") in bstack11ll1ll11l1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l1l1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᛝ"), [])
                bstack11lll1l1ll1_opy_ = bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᛞ")]
                for extension in bstack11lll1l1ll1_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l1l1l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᛟ") in bstack11ll1ll11l1_opy_:
                bstack11lll11111l_opy_ = chrome_options.experimental_options.get(bstack1l1l1l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᛠ"), {})
                bstack11lll11llll_opy_ = bstack11ll1ll11l1_opy_[bstack1l1l1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᛡ")]
                bstack11lll11lll1_opy_(bstack11lll11111l_opy_, bstack11lll11llll_opy_)
                chrome_options.add_experimental_option(bstack1l1l1l1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᛢ"), bstack11lll11111l_opy_)
        os.environ[bstack1l1l1l1_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᛣ")] = bstack1l1l1l1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᛤ")
        return bstack11lll111l_opy_
    except Exception as e:
      logger.error(bstack1l1l1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡦࡧ࡭ࡳ࡭ࠠ࡯ࡱࡱ࠱ࡇ࡙ࠠࡪࡰࡩࡶࡦࠦࡡ࠲࠳ࡼࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࠢᛥ") + str(e))
      return bstack11lll111l_opy_