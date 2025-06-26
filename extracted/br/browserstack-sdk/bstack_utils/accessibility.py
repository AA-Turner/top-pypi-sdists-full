# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll1ll111l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1ll11ll_opy_ as bstack11lll111111_opy_, EVENTS
from bstack_utils.bstack1ll111ll11_opy_ import bstack1ll111ll11_opy_
from bstack_utils.helper import bstack1ll1l11l11_opy_, bstack111ll111ll_opy_, bstack1ll1l1lll1_opy_, bstack11lll1111l1_opy_, \
  bstack11ll1llll11_opy_, bstack1l1l1l111l_opy_, get_host_info, bstack11ll1l1l11l_opy_, bstack11lll1111_opy_, bstack111l1llll1_opy_, bstack11ll1l1l1l1_opy_, bstack11ll1l1lll1_opy_, bstack11111ll1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11l1l1l111_opy_ import get_logger
from bstack_utils.bstack1l1ll1111_opy_ import bstack1llll11lll1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1l1ll1111_opy_ = bstack1llll11lll1_opy_()
@bstack111l1llll1_opy_(class_method=False)
def _11lll11ll11_opy_(driver, bstack1111l1l111_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll1l1_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᗐ"): caps.get(bstack11ll1l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᗑ"), None),
        bstack11ll1l1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᗒ"): bstack1111l1l111_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᗓ"), None),
        bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᗔ"): caps.get(bstack11ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᗕ"), None),
        bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᗖ"): caps.get(bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗗ"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll1l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᗘ") + str(error))
  return response
def on():
    if os.environ.get(bstack11ll1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᗙ"), None) is None or os.environ[bstack11ll1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᗚ")] == bstack11ll1l1_opy_ (u"ࠤࡱࡹࡱࡲࠢᗛ"):
        return False
    return True
def bstack1l111l1111_opy_(config):
  return config.get(bstack11ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗜ"), False) or any([p.get(bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᗝ"), False) == True for p in config.get(bstack11ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᗞ"), [])])
def bstack1ll11l11ll_opy_(config, bstack1l1l111l_opy_):
  try:
    bstack11ll1lll11l_opy_ = config.get(bstack11ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᗟ"), False)
    if int(bstack1l1l111l_opy_) < len(config.get(bstack11ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᗠ"), [])) and config[bstack11ll1l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᗡ")][bstack1l1l111l_opy_]:
      bstack11ll1lll111_opy_ = config[bstack11ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᗢ")][bstack1l1l111l_opy_].get(bstack11ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗣ"), None)
    else:
      bstack11ll1lll111_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᗤ"), None)
    if bstack11ll1lll111_opy_ != None:
      bstack11ll1lll11l_opy_ = bstack11ll1lll111_opy_
    bstack11ll1lll1ll_opy_ = os.getenv(bstack11ll1l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᗥ")) is not None and len(os.getenv(bstack11ll1l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᗦ"))) > 0 and os.getenv(bstack11ll1l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᗧ")) != bstack11ll1l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᗨ")
    return bstack11ll1lll11l_opy_ and bstack11ll1lll1ll_opy_
  except Exception as error:
    logger.debug(bstack11ll1l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᗩ") + str(error))
  return False
def bstack1lll11l1l1_opy_(test_tags):
  bstack1ll11l1l1l1_opy_ = os.getenv(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᗪ"))
  if bstack1ll11l1l1l1_opy_ is None:
    return True
  bstack1ll11l1l1l1_opy_ = json.loads(bstack1ll11l1l1l1_opy_)
  try:
    include_tags = bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᗫ")] if bstack11ll1l1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᗬ") in bstack1ll11l1l1l1_opy_ and isinstance(bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᗭ")], list) else []
    exclude_tags = bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᗮ")] if bstack11ll1l1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᗯ") in bstack1ll11l1l1l1_opy_ and isinstance(bstack1ll11l1l1l1_opy_[bstack11ll1l1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᗰ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll1l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᗱ") + str(error))
  return False
def bstack11ll1l1l111_opy_(config, bstack11ll1l11lll_opy_, bstack11lll11l1ll_opy_, bstack11ll1l1ll1l_opy_):
  bstack11ll1ll1l11_opy_ = bstack11lll1111l1_opy_(config)
  bstack11ll1ll1ll1_opy_ = bstack11ll1llll11_opy_(config)
  if bstack11ll1ll1l11_opy_ is None or bstack11ll1ll1ll1_opy_ is None:
    logger.error(bstack11ll1l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᗲ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᗳ"), bstack11ll1l1_opy_ (u"࠭ࡻࡾࠩᗴ")))
    data = {
        bstack11ll1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᗵ"): config[bstack11ll1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᗶ")],
        bstack11ll1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᗷ"): config.get(bstack11ll1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᗸ"), os.path.basename(os.getcwd())),
        bstack11ll1l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧᗹ"): bstack1ll1l11l11_opy_(),
        bstack11ll1l1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᗺ"): config.get(bstack11ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᗻ"), bstack11ll1l1_opy_ (u"ࠧࠨᗼ")),
        bstack11ll1l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᗽ"): {
            bstack11ll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᗾ"): bstack11ll1l11lll_opy_,
            bstack11ll1l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗿ"): bstack11lll11l1ll_opy_,
            bstack11ll1l1_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘀ"): __version__,
            bstack11ll1l1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᘁ"): bstack11ll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᘂ"),
            bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᘃ"): bstack11ll1l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᘄ"),
            bstack11ll1l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᘅ"): bstack11ll1l1ll1l_opy_
        },
        bstack11ll1l1_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬᘆ"): settings,
        bstack11ll1l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡈࡵ࡮ࡵࡴࡲࡰࠬᘇ"): bstack11ll1l1l11l_opy_(),
        bstack11ll1l1_opy_ (u"ࠬࡩࡩࡊࡰࡩࡳࠬᘈ"): bstack1l1l1l111l_opy_(),
        bstack11ll1l1_opy_ (u"࠭ࡨࡰࡵࡷࡍࡳ࡬࡯ࠨᘉ"): get_host_info(),
        bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᘊ"): bstack1ll1l1lll1_opy_(config)
    }
    headers = {
        bstack11ll1l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᘋ"): bstack11ll1l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᘌ"),
    }
    config = {
        bstack11ll1l1_opy_ (u"ࠪࡥࡺࡺࡨࠨᘍ"): (bstack11ll1ll1l11_opy_, bstack11ll1ll1ll1_opy_),
        bstack11ll1l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᘎ"): headers
    }
    response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠬࡖࡏࡔࡖࠪᘏ"), bstack11lll111111_opy_ + bstack11ll1l1_opy_ (u"࠭࠯ࡷ࠴࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭ᘐ"), data, config)
    bstack11ll1ll1l1l_opy_ = response.json()
    if bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᘑ")]:
      parsed = json.loads(os.getenv(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᘒ"), bstack11ll1l1_opy_ (u"ࠩࡾࢁࠬᘓ")))
      parsed[bstack11ll1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᘔ")] = bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᘕ")][bstack11ll1l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘖ")]
      os.environ[bstack11ll1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᘗ")] = json.dumps(parsed)
      bstack1ll111ll11_opy_.bstack1lll1lll11_opy_(bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᘘ")][bstack11ll1l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᘙ")])
      bstack1ll111ll11_opy_.bstack11lll111l11_opy_(bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᘚ")][bstack11ll1l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᘛ")])
      bstack1ll111ll11_opy_.store()
      return bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᘜ")][bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪᘝ")], bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᘞ")][bstack11ll1l1_opy_ (u"ࠧࡪࡦࠪᘟ")]
    else:
      logger.error(bstack11ll1l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩᘠ") + bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᘡ")])
      if bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘢ")] == bstack11ll1l1_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ᘣ"):
        for bstack11lll111lll_opy_ in bstack11ll1ll1l1l_opy_[bstack11ll1l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᘤ")]:
          logger.error(bstack11lll111lll_opy_[bstack11ll1l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘥ")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣᘦ") +  str(error))
    return None, None
def bstack11ll1l111ll_opy_():
  if os.getenv(bstack11ll1l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘧ")) is None:
    return {
        bstack11ll1l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᘨ"): bstack11ll1l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᘩ"),
        bstack11ll1l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘪ"): bstack11ll1l1_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫᘫ")
    }
  data = {bstack11ll1l1_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧᘬ"): bstack1ll1l11l11_opy_()}
  headers = {
      bstack11ll1l1_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᘭ"): bstack11ll1l1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩᘮ") + os.getenv(bstack11ll1l1_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢᘯ")),
      bstack11ll1l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᘰ"): bstack11ll1l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᘱ")
  }
  response = bstack11lll1111_opy_(bstack11ll1l1_opy_ (u"ࠬࡖࡕࡕࠩᘲ"), bstack11lll111111_opy_ + bstack11ll1l1_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨᘳ"), data, { bstack11ll1l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᘴ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll1l1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤᘵ") + bstack111ll111ll_opy_().isoformat() + bstack11ll1l1_opy_ (u"ࠩ࡝ࠫᘶ"))
      return {bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᘷ"): bstack11ll1l1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᘸ"), bstack11ll1l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘹ"): bstack11ll1l1_opy_ (u"࠭ࠧᘺ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥᘻ") + str(error))
    return {
        bstack11ll1l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᘼ"): bstack11ll1l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᘽ"),
        bstack11ll1l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᘾ"): str(error)
    }
def bstack11ll1l11l11_opy_(bstack11ll1llllll_opy_):
    return re.match(bstack11ll1l1_opy_ (u"ࡶࠬࡤ࡜ࡥ࠭ࠫࡠ࠳ࡢࡤࠬࠫࡂࠨࠬᘿ"), bstack11ll1llllll_opy_.strip()) is not None
def bstack11l11l1l1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11lll11l111_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll11l111_opy_ = desired_capabilities
        else:
          bstack11lll11l111_opy_ = {}
        bstack1ll11llll11_opy_ = (bstack11lll11l111_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᙀ"), bstack11ll1l1_opy_ (u"࠭ࠧᙁ")).lower() or caps.get(bstack11ll1l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᙂ"), bstack11ll1l1_opy_ (u"ࠨࠩᙃ")).lower())
        if bstack1ll11llll11_opy_ == bstack11ll1l1_opy_ (u"ࠩ࡬ࡳࡸ࠭ᙄ"):
            return True
        if bstack1ll11llll11_opy_ == bstack11ll1l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᙅ"):
            bstack1ll111ll1l1_opy_ = str(float(caps.get(bstack11ll1l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙆ")) or bstack11lll11l111_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙇ"), {}).get(bstack11ll1l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᙈ"),bstack11ll1l1_opy_ (u"ࠧࠨᙉ"))))
            if bstack1ll11llll11_opy_ == bstack11ll1l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᙊ") and int(bstack1ll111ll1l1_opy_.split(bstack11ll1l1_opy_ (u"ࠩ࠱ࠫᙋ"))[0]) < float(bstack11lll111l1l_opy_):
                logger.warning(str(bstack11lll11111l_opy_))
                return False
            return True
        bstack1ll1l11ll1l_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᙌ"), {}).get(bstack11ll1l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᙍ"), caps.get(bstack11ll1l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᙎ"), bstack11ll1l1_opy_ (u"࠭ࠧᙏ")))
        if bstack1ll1l11ll1l_opy_:
            logger.warning(bstack11ll1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᙐ"))
            return False
        browser = caps.get(bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᙑ"), bstack11ll1l1_opy_ (u"ࠩࠪᙒ")).lower() or bstack11lll11l111_opy_.get(bstack11ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᙓ"), bstack11ll1l1_opy_ (u"ࠫࠬᙔ")).lower()
        if browser != bstack11ll1l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᙕ"):
            logger.warning(bstack11ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᙖ"))
            return False
        browser_version = caps.get(bstack11ll1l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙗ")) or caps.get(bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᙘ")) or bstack11lll11l111_opy_.get(bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙙ")) or bstack11lll11l111_opy_.get(bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᙚ"), {}).get(bstack11ll1l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙛ")) or bstack11lll11l111_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙜ"), {}).get(bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᙝ"))
        bstack1ll1l11l1l1_opy_ = bstack11ll1ll111l_opy_.bstack1ll11ll1l11_opy_
        bstack11ll1lll1l1_opy_ = False
        if config is not None:
          bstack11ll1lll1l1_opy_ = bstack11ll1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᙞ") in config and str(config[bstack11ll1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᙟ")]).lower() != bstack11ll1l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᙠ")
        if os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᙡ"), bstack11ll1l1_opy_ (u"ࠫࠬᙢ")).lower() == bstack11ll1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪᙣ") or bstack11ll1lll1l1_opy_:
          bstack1ll1l11l1l1_opy_ = bstack11ll1ll111l_opy_.bstack1ll11lll1l1_opy_
        if browser_version and browser_version != bstack11ll1l1_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᙤ") and int(browser_version.split(bstack11ll1l1_opy_ (u"ࠧ࠯ࠩᙥ"))[0]) <= bstack1ll1l11l1l1_opy_:
          logger.warning(bstack1llll1111l1_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࡱ࡮ࡴ࡟ࡢ࠳࠴ࡽࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡠࡥ࡫ࡶࡴࡳࡥࡠࡸࡨࡶࡸ࡯࡯࡯ࡿ࠱ࠫᙦ"))
          return False
        if not options:
          bstack1ll11ll1l1l_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᙧ")) or bstack11lll11l111_opy_.get(bstack11ll1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᙨ"), {})
          if bstack11ll1l1_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᙩ") in bstack1ll11ll1l1l_opy_.get(bstack11ll1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᙪ"), []):
              logger.warning(bstack11ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᙫ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᙬ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll11l111l_opy_ = config.get(bstack11ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᙭"), {})
    bstack1lll11l111l_opy_[bstack11ll1l1_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬ᙮")] = os.getenv(bstack11ll1l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᙯ"))
    bstack11ll1l1ll11_opy_ = json.loads(os.getenv(bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᙰ"), bstack11ll1l1_opy_ (u"ࠬࢁࡽࠨᙱ"))).get(bstack11ll1l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᙲ"))
    if not config[bstack11ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᙳ")].get(bstack11ll1l1_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᙴ")):
      if bstack11ll1l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᙵ") in caps:
        caps[bstack11ll1l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᙶ")][bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᙷ")] = bstack1lll11l111l_opy_
        caps[bstack11ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙸ")][bstack11ll1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙹ")][bstack11ll1l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙺ")] = bstack11ll1l1ll11_opy_
      else:
        caps[bstack11ll1l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᙻ")] = bstack1lll11l111l_opy_
        caps[bstack11ll1l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᙼ")][bstack11ll1l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᙽ")] = bstack11ll1l1ll11_opy_
  except Exception as error:
    logger.debug(bstack11ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧᙾ") +  str(error))
def bstack111ll1l1l_opy_(driver, bstack11lll111ll1_opy_):
  try:
    setattr(driver, bstack11ll1l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᙿ"), True)
    session = driver.session_id
    if session:
      bstack11ll1l11ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1l11ll1_opy_ = False
      bstack11ll1l11ll1_opy_ = url.scheme in [bstack11ll1l1_opy_ (u"ࠨࡨࡵࡶࡳࠦ "), bstack11ll1l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᚁ")]
      if bstack11ll1l11ll1_opy_:
        if bstack11lll111ll1_opy_:
          logger.info(bstack11ll1l1_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣᚂ"))
      return bstack11lll111ll1_opy_
  except Exception as e:
    logger.error(bstack11ll1l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᚃ") + str(e))
    return False
def bstack11l1l1l1l1_opy_(driver, name, path):
  try:
    bstack1ll111ll111_opy_ = {
        bstack11ll1l1_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᚄ"): threading.current_thread().current_test_uuid,
        bstack11ll1l1_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᚅ"): os.environ.get(bstack11ll1l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᚆ"), bstack11ll1l1_opy_ (u"࠭ࠧᚇ")),
        bstack11ll1l1_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫᚈ"): os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᚉ"), bstack11ll1l1_opy_ (u"ࠩࠪᚊ"))
    }
    bstack1ll11l111ll_opy_ = bstack1l1ll1111_opy_.bstack1ll111ll1ll_opy_(EVENTS.bstack1ll1ll111l_opy_.value)
    logger.debug(bstack11ll1l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᚋ"))
    try:
      if (bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᚌ"), None) and bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᚍ"), None)):
        scripts = {bstack11ll1l1_opy_ (u"࠭ࡳࡤࡣࡱࠫᚎ"): bstack1ll111ll11_opy_.perform_scan}
        bstack11ll1ll11l1_opy_ = json.loads(scripts[bstack11ll1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᚏ")].replace(bstack11ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᚐ"), bstack11ll1l1_opy_ (u"ࠤࠥᚑ")))
        bstack11ll1ll11l1_opy_[bstack11ll1l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᚒ")][bstack11ll1l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᚓ")] = None
        scripts[bstack11ll1l1_opy_ (u"ࠧࡹࡣࡢࡰࠥᚔ")] = bstack11ll1l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᚕ") + json.dumps(bstack11ll1ll11l1_opy_)
        bstack1ll111ll11_opy_.bstack1lll1lll11_opy_(scripts)
        bstack1ll111ll11_opy_.store()
        logger.debug(driver.execute_script(bstack1ll111ll11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll111ll11_opy_.perform_scan, {bstack11ll1l1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᚖ"): name}))
      bstack1l1ll1111_opy_.end(EVENTS.bstack1ll1ll111l_opy_.value, bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᚗ"), bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᚘ"), True, None)
    except Exception as error:
      bstack1l1ll1111_opy_.end(EVENTS.bstack1ll1ll111l_opy_.value, bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᚙ"), bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᚚ"), False, str(error))
    bstack1ll11l111ll_opy_ = bstack1l1ll1111_opy_.bstack11ll1l1llll_opy_(EVENTS.bstack1ll11l1l11l_opy_.value)
    bstack1l1ll1111_opy_.mark(bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᚛"))
    try:
      if (bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭᚜"), None) and bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ᚝"), None)):
        scripts = {bstack11ll1l1_opy_ (u"ࠨࡵࡦࡥࡳ࠭᚞"): bstack1ll111ll11_opy_.perform_scan}
        bstack11ll1ll11l1_opy_ = json.loads(scripts[bstack11ll1l1_opy_ (u"ࠤࡶࡧࡦࡴࠢ᚟")].replace(bstack11ll1l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᚠ"), bstack11ll1l1_opy_ (u"ࠦࠧᚡ")))
        bstack11ll1ll11l1_opy_[bstack11ll1l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᚢ")][bstack11ll1l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᚣ")] = None
        scripts[bstack11ll1l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᚤ")] = bstack11ll1l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᚥ") + json.dumps(bstack11ll1ll11l1_opy_)
        bstack1ll111ll11_opy_.bstack1lll1lll11_opy_(scripts)
        bstack1ll111ll11_opy_.store()
        logger.debug(driver.execute_script(bstack1ll111ll11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1ll111ll11_opy_.bstack11ll1l1l1ll_opy_, bstack1ll111ll111_opy_))
      bstack1l1ll1111_opy_.end(bstack1ll11l111ll_opy_, bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᚦ"), bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᚧ"),True, None)
    except Exception as error:
      bstack1l1ll1111_opy_.end(bstack1ll11l111ll_opy_, bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᚨ"), bstack1ll11l111ll_opy_ + bstack11ll1l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᚩ"),False, str(error))
    logger.info(bstack11ll1l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᚪ"))
  except Exception as bstack1ll111l1ll1_opy_:
    logger.error(bstack11ll1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᚫ") + str(path) + bstack11ll1l1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥᚬ") + str(bstack1ll111l1ll1_opy_))
def bstack11ll1l11l1l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11ll1l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᚭ")) and str(caps.get(bstack11ll1l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤᚮ"))).lower() == bstack11ll1l1_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᚯ"):
        bstack1ll111ll1l1_opy_ = caps.get(bstack11ll1l1_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᚰ")) or caps.get(bstack11ll1l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᚱ"))
        if bstack1ll111ll1l1_opy_ and int(str(bstack1ll111ll1l1_opy_)) < bstack11lll111l1l_opy_:
            return False
    return True
def bstack11llll1111_opy_(config):
  if bstack11ll1l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᚲ") in config:
        return config[bstack11ll1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᚳ")]
  for platform in config.get(bstack11ll1l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᚴ"), []):
      if bstack11ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚵ") in platform:
          return platform[bstack11ll1l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚶ")]
  return None
def bstack11l1l11ll_opy_(bstack11ll1111_opy_):
  try:
    browser_name = bstack11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᚷ")]
    browser_version = bstack11ll1111_opy_[bstack11ll1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᚸ")]
    chrome_options = bstack11ll1111_opy_[bstack11ll1l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᚹ")]
    try:
        bstack11ll1llll1l_opy_ = int(browser_version.split(bstack11ll1l1_opy_ (u"ࠨ࠰ࠪᚺ"))[0])
    except ValueError as e:
        logger.error(bstack11ll1l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨᚻ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11ll1l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪᚼ")):
        logger.warning(bstack11ll1l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᚽ"))
        return False
    if bstack11ll1llll1l_opy_ < bstack11ll1ll111l_opy_.bstack1ll11lll1l1_opy_:
        logger.warning(bstack1llll1111l1_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡃࡐࡐࡖࡘࡆࡔࡔࡔ࠰ࡐࡍࡓࡏࡍࡖࡏࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘ࡛ࡐࡑࡑࡕࡘࡊࡊ࡟ࡄࡊࡕࡓࡒࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࡾࠢࡲࡶࠥ࡮ࡩࡨࡪࡨࡶ࠳࠭ᚾ"))
        return False
    if chrome_options and any(bstack11ll1l1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᚿ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11ll1l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᛀ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11ll1l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨᛁ") + str(e))
    return False
def bstack1l1l1l11ll_opy_(bstack1l111ll11_opy_, config):
    try:
      bstack1ll11l1ll1l_opy_ = bstack11ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᛂ") in config and config[bstack11ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᛃ")] == True
      bstack11ll1lll1l1_opy_ = bstack11ll1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᛄ") in config and str(config[bstack11ll1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᛅ")]).lower() != bstack11ll1l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᛆ")
      if not (bstack1ll11l1ll1l_opy_ and (not bstack1ll1l1lll1_opy_(config) or bstack11ll1lll1l1_opy_)):
        return bstack1l111ll11_opy_
      bstack11ll1lllll1_opy_ = bstack1ll111ll11_opy_.bstack11lll11l11l_opy_
      if bstack11ll1lllll1_opy_ is None:
        logger.debug(bstack11ll1l1_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥᛇ"))
        return bstack1l111ll11_opy_
      bstack11lll1111ll_opy_ = int(str(bstack11ll1l1lll1_opy_()).split(bstack11ll1l1_opy_ (u"ࠨ࠰ࠪᛈ"))[0])
      logger.debug(bstack11ll1l1_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤᛉ") + str(bstack11lll1111ll_opy_) + bstack11ll1l1_opy_ (u"ࠥࠦᛊ"))
      if bstack11lll1111ll_opy_ == 3 and isinstance(bstack1l111ll11_opy_, dict) and bstack11ll1l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᛋ") in bstack1l111ll11_opy_ and bstack11ll1lllll1_opy_ is not None:
        if bstack11ll1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛌ") not in bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛍ")]:
          bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᛎ")][bstack11ll1l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᛏ")] = {}
        if bstack11ll1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᛐ") in bstack11ll1lllll1_opy_:
          if bstack11ll1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᛑ") not in bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᛒ")][bstack11ll1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛓ")]:
            bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛔ")][bstack11ll1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛕ")][bstack11ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᛖ")] = []
          for arg in bstack11ll1lllll1_opy_[bstack11ll1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᛗ")]:
            if arg not in bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᛘ")][bstack11ll1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛙ")][bstack11ll1l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᛚ")]:
              bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛛ")][bstack11ll1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛜ")][bstack11ll1l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᛝ")].append(arg)
        if bstack11ll1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᛞ") in bstack11ll1lllll1_opy_:
          if bstack11ll1l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᛟ") not in bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᛠ")][bstack11ll1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛡ")]:
            bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛢ")][bstack11ll1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛣ")][bstack11ll1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᛤ")] = []
          for ext in bstack11ll1lllll1_opy_[bstack11ll1l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᛥ")]:
            if ext not in bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᛦ")][bstack11ll1l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᛧ")][bstack11ll1l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᛨ")]:
              bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛩ")][bstack11ll1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛪ")][bstack11ll1l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᛫")].append(ext)
        if bstack11ll1l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ᛬") in bstack11ll1lllll1_opy_:
          if bstack11ll1l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ᛭") not in bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᛮ")][bstack11ll1l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛯ")]:
            bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛰ")][bstack11ll1l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛱ")][bstack11ll1l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᛲ")] = {}
          bstack11ll1l1l1l1_opy_(bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᛳ")][bstack11ll1l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᛴ")][bstack11ll1l1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᛵ")],
                    bstack11ll1lllll1_opy_[bstack11ll1l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᛶ")])
        os.environ[bstack11ll1l1_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᛷ")] = bstack11ll1l1_opy_ (u"ࠧࡵࡴࡸࡩࠬᛸ")
        return bstack1l111ll11_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l111ll11_opy_, ChromeOptions):
          chrome_options = bstack1l111ll11_opy_
        elif isinstance(bstack1l111ll11_opy_, dict):
          for value in bstack1l111ll11_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l111ll11_opy_, dict):
            bstack1l111ll11_opy_[bstack11ll1l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᛹")] = chrome_options
          else:
            bstack1l111ll11_opy_ = chrome_options
        if bstack11ll1lllll1_opy_ is not None:
          if bstack11ll1l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᛺") in bstack11ll1lllll1_opy_:
                bstack11lll11l1l1_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1lllll1_opy_[bstack11ll1l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᛻")]
                for arg in new_args:
                    if arg not in bstack11lll11l1l1_opy_:
                        chrome_options.add_argument(arg)
          if bstack11ll1l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᛼") in bstack11ll1lllll1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11ll1l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᛽"), [])
                bstack11ll1ll1111_opy_ = bstack11ll1lllll1_opy_[bstack11ll1l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᛾")]
                for extension in bstack11ll1ll1111_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11ll1l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᛿") in bstack11ll1lllll1_opy_:
                bstack11ll1ll1lll_opy_ = chrome_options.experimental_options.get(bstack11ll1l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᜀ"), {})
                bstack11lll11ll1l_opy_ = bstack11ll1lllll1_opy_[bstack11ll1l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᜁ")]
                bstack11ll1l1l1l1_opy_(bstack11ll1ll1lll_opy_, bstack11lll11ll1l_opy_)
                chrome_options.add_experimental_option(bstack11ll1l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᜂ"), bstack11ll1ll1lll_opy_)
        os.environ[bstack11ll1l1_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᜃ")] = bstack11ll1l1_opy_ (u"ࠬࡺࡲࡶࡧࠪᜄ")
        return bstack1l111ll11_opy_
    except Exception as e:
      logger.error(bstack11ll1l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦᜅ") + str(e))
      return bstack1l111ll11_opy_