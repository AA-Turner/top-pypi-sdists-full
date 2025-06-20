# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11lll11lll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1l1llll_opy_ as bstack11ll1ll1l1l_opy_, EVENTS
from bstack_utils.bstack11llll1l1l_opy_ import bstack11llll1l1l_opy_
from bstack_utils.helper import bstack1l11l11ll_opy_, bstack1111llll11_opy_, bstack1l111lll1l_opy_, bstack11ll1l1ll1l_opy_, \
  bstack11ll1ll11ll_opy_, bstack11l1l1l1l_opy_, get_host_info, bstack11ll1ll1111_opy_, bstack1llll1ll_opy_, bstack111l1lll11_opy_, bstack11ll1ll11l1_opy_, bstack11ll1lll1ll_opy_, bstack111ll1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1111l1ll1_opy_ import get_logger
from bstack_utils.bstack1ll11ll1_opy_ import bstack1ll1l1ll1l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1ll11ll1_opy_ = bstack1ll1l1ll1l1_opy_()
@bstack111l1lll11_opy_(class_method=False)
def _11ll1llll1l_opy_(driver, bstack1111l11ll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11ll11_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᖯ"): caps.get(bstack11ll11_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᖰ"), None),
        bstack11ll11_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᖱ"): bstack1111l11ll1_opy_.get(bstack11ll11_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖲ"), None),
        bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᖳ"): caps.get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᖴ"), None),
        bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᖵ"): caps.get(bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖶ"), None)
    }
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᖷ") + str(error))
  return response
def on():
    if os.environ.get(bstack11ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᖸ"), None) is None or os.environ[bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖹ")] == bstack11ll11_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᖺ"):
        return False
    return True
def bstack1l11l11l11_opy_(config):
  return config.get(bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᖻ"), False) or any([p.get(bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᖼ"), False) == True for p in config.get(bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᖽ"), [])])
def bstack11lll11l1l_opy_(config, bstack1l111l111l_opy_):
  try:
    bstack11ll1l1l1l1_opy_ = config.get(bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᖾ"), False)
    if int(bstack1l111l111l_opy_) < len(config.get(bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᖿ"), [])) and config[bstack11ll11_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᗀ")][bstack1l111l111l_opy_]:
      bstack11lll11ll11_opy_ = config[bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᗁ")][bstack1l111l111l_opy_].get(bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᗂ"), None)
    else:
      bstack11lll11ll11_opy_ = config.get(bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᗃ"), None)
    if bstack11lll11ll11_opy_ != None:
      bstack11ll1l1l1l1_opy_ = bstack11lll11ll11_opy_
    bstack11ll1lll1l1_opy_ = os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᗄ")) is not None and len(os.getenv(bstack11ll11_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᗅ"))) > 0 and os.getenv(bstack11ll11_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᗆ")) != bstack11ll11_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᗇ")
    return bstack11ll1l1l1l1_opy_ and bstack11ll1lll1l1_opy_
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᗈ") + str(error))
  return False
def bstack1ll1lllll_opy_(test_tags):
  bstack1ll11ll1ll1_opy_ = os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᗉ"))
  if bstack1ll11ll1ll1_opy_ is None:
    return True
  bstack1ll11ll1ll1_opy_ = json.loads(bstack1ll11ll1ll1_opy_)
  try:
    include_tags = bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᗊ")] if bstack11ll11_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᗋ") in bstack1ll11ll1ll1_opy_ and isinstance(bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᗌ")], list) else []
    exclude_tags = bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᗍ")] if bstack11ll11_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᗎ") in bstack1ll11ll1ll1_opy_ and isinstance(bstack1ll11ll1ll1_opy_[bstack11ll11_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᗏ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᗐ") + str(error))
  return False
def bstack11lll11l111_opy_(config, bstack11lll111111_opy_, bstack11ll1lll111_opy_, bstack11lll1l111l_opy_):
  bstack11ll1lll11l_opy_ = bstack11ll1l1ll1l_opy_(config)
  bstack11ll1ll111l_opy_ = bstack11ll1ll11ll_opy_(config)
  if bstack11ll1lll11l_opy_ is None or bstack11ll1ll111l_opy_ is None:
    logger.error(bstack11ll11_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᗑ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᗒ"), bstack11ll11_opy_ (u"ࠨࡽࢀࠫᗓ")))
    data = {
        bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᗔ"): config[bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᗕ")],
        bstack11ll11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᗖ"): config.get(bstack11ll11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᗗ"), os.path.basename(os.getcwd())),
        bstack11ll11_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᗘ"): bstack1l11l11ll_opy_(),
        bstack11ll11_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᗙ"): config.get(bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᗚ"), bstack11ll11_opy_ (u"ࠩࠪᗛ")),
        bstack11ll11_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᗜ"): {
            bstack11ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᗝ"): bstack11lll111111_opy_,
            bstack11ll11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗞ"): bstack11ll1lll111_opy_,
            bstack11ll11_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᗟ"): __version__,
            bstack11ll11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᗠ"): bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᗡ"),
            bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᗢ"): bstack11ll11_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᗣ"),
            bstack11ll11_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᗤ"): bstack11lll1l111l_opy_
        },
        bstack11ll11_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᗥ"): settings,
        bstack11ll11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᗦ"): bstack11ll1ll1111_opy_(),
        bstack11ll11_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᗧ"): bstack11l1l1l1l_opy_(),
        bstack11ll11_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᗨ"): get_host_info(),
        bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᗩ"): bstack1l111lll1l_opy_(config)
    }
    headers = {
        bstack11ll11_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᗪ"): bstack11ll11_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᗫ"),
    }
    config = {
        bstack11ll11_opy_ (u"ࠬࡧࡵࡵࡪࠪᗬ"): (bstack11ll1lll11l_opy_, bstack11ll1ll111l_opy_),
        bstack11ll11_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᗭ"): headers
    }
    response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠧࡑࡑࡖࡘࠬᗮ"), bstack11ll1ll1l1l_opy_ + bstack11ll11_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᗯ"), data, config)
    bstack11lll11111l_opy_ = response.json()
    if bstack11lll11111l_opy_[bstack11ll11_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᗰ")]:
      parsed = json.loads(os.getenv(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᗱ"), bstack11ll11_opy_ (u"ࠫࢀࢃࠧᗲ")))
      parsed[bstack11ll11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗳ")] = bstack11lll11111l_opy_[bstack11ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫᗴ")][bstack11ll11_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗵ")]
      os.environ[bstack11ll11_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᗶ")] = json.dumps(parsed)
      bstack11llll1l1l_opy_.bstack11ll1ll1ll_opy_(bstack11lll11111l_opy_[bstack11ll11_opy_ (u"ࠩࡧࡥࡹࡧࠧᗷ")][bstack11ll11_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᗸ")])
      bstack11llll1l1l_opy_.bstack11lll111lll_opy_(bstack11lll11111l_opy_[bstack11ll11_opy_ (u"ࠫࡩࡧࡴࡢࠩᗹ")][bstack11ll11_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᗺ")])
      bstack11llll1l1l_opy_.store()
      return bstack11lll11111l_opy_[bstack11ll11_opy_ (u"࠭ࡤࡢࡶࡤࠫᗻ")][bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᗼ")], bstack11lll11111l_opy_[bstack11ll11_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᗽ")][bstack11ll11_opy_ (u"ࠩ࡬ࡨࠬᗾ")]
    else:
      logger.error(bstack11ll11_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᗿ") + bstack11lll11111l_opy_[bstack11ll11_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᘀ")])
      if bstack11lll11111l_opy_[bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘁ")] == bstack11ll11_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᘂ"):
        for bstack11lll1l11l1_opy_ in bstack11lll11111l_opy_[bstack11ll11_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᘃ")]:
          logger.error(bstack11lll1l11l1_opy_[bstack11ll11_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᘄ")])
      return None, None
  except Exception as error:
    logger.error(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᘅ") +  str(error))
    return None, None
def bstack11ll1ll1ll1_opy_():
  if os.getenv(bstack11ll11_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᘆ")) is None:
    return {
        bstack11ll11_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᘇ"): bstack11ll11_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᘈ"),
        bstack11ll11_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᘉ"): bstack11ll11_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᘊ")
    }
  data = {bstack11ll11_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᘋ"): bstack1l11l11ll_opy_()}
  headers = {
      bstack11ll11_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᘌ"): bstack11ll11_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᘍ") + os.getenv(bstack11ll11_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᘎ")),
      bstack11ll11_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᘏ"): bstack11ll11_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᘐ")
  }
  response = bstack1llll1ll_opy_(bstack11ll11_opy_ (u"ࠧࡑࡗࡗࠫᘑ"), bstack11ll1ll1l1l_opy_ + bstack11ll11_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᘒ"), data, { bstack11ll11_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᘓ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11ll11_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᘔ") + bstack1111llll11_opy_().isoformat() + bstack11ll11_opy_ (u"ࠫ࡟࠭ᘕ"))
      return {bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᘖ"): bstack11ll11_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᘗ"), bstack11ll11_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘘ"): bstack11ll11_opy_ (u"ࠨࠩᘙ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᘚ") + str(error))
    return {
        bstack11ll11_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᘛ"): bstack11ll11_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᘜ"),
        bstack11ll11_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘝ"): str(error)
    }
def bstack11lll1l11ll_opy_(bstack11ll1l1l1ll_opy_):
    return re.match(bstack11ll11_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᘞ"), bstack11ll1l1l1ll_opy_.strip()) is not None
def bstack1ll1ll111_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11lll1l1l11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll1l1l11_opy_ = desired_capabilities
        else:
          bstack11lll1l1l11_opy_ = {}
        bstack11ll1ll1lll_opy_ = (bstack11lll1l1l11_opy_.get(bstack11ll11_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᘟ"), bstack11ll11_opy_ (u"ࠨࠩᘠ")).lower() or caps.get(bstack11ll11_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᘡ"), bstack11ll11_opy_ (u"ࠪࠫᘢ")).lower())
        if bstack11ll1ll1lll_opy_ == bstack11ll11_opy_ (u"ࠫ࡮ࡵࡳࠨᘣ"):
            return True
        if bstack11ll1ll1lll_opy_ == bstack11ll11_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᘤ"):
            bstack11ll1lllll1_opy_ = str(float(caps.get(bstack11ll11_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘥ")) or bstack11lll1l1l11_opy_.get(bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘦ"), {}).get(bstack11ll11_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᘧ"),bstack11ll11_opy_ (u"ࠩࠪᘨ"))))
            if bstack11ll1ll1lll_opy_ == bstack11ll11_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᘩ") and int(bstack11ll1lllll1_opy_.split(bstack11ll11_opy_ (u"ࠫ࠳࠭ᘪ"))[0]) < float(bstack11ll1llll11_opy_):
                logger.warning(str(bstack11lll111l11_opy_))
                return False
            return True
        bstack1ll1l1l111l_opy_ = caps.get(bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘫ"), {}).get(bstack11ll11_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᘬ"), caps.get(bstack11ll11_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᘭ"), bstack11ll11_opy_ (u"ࠨࠩᘮ")))
        if bstack1ll1l1l111l_opy_:
            logger.warning(bstack11ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᘯ"))
            return False
        browser = caps.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᘰ"), bstack11ll11_opy_ (u"ࠫࠬᘱ")).lower() or bstack11lll1l1l11_opy_.get(bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᘲ"), bstack11ll11_opy_ (u"࠭ࠧᘳ")).lower()
        if browser != bstack11ll11_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᘴ"):
            logger.warning(bstack11ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᘵ"))
            return False
        browser_version = caps.get(bstack11ll11_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᘶ")) or caps.get(bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᘷ")) or bstack11lll1l1l11_opy_.get(bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘸ")) or bstack11lll1l1l11_opy_.get(bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘹ"), {}).get(bstack11ll11_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᘺ")) or bstack11lll1l1l11_opy_.get(bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘻ"), {}).get(bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᘼ"))
        bstack1ll1l111lll_opy_ = bstack11lll11lll1_opy_.bstack1ll11l11l11_opy_
        bstack11lll11l1ll_opy_ = False
        if config is not None:
          bstack11lll11l1ll_opy_ = bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᘽ") in config and str(config[bstack11ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᘾ")]).lower() != bstack11ll11_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᘿ")
        if os.environ.get(bstack11ll11_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᙀ"), bstack11ll11_opy_ (u"࠭ࠧᙁ")).lower() == bstack11ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬᙂ") or bstack11lll11l1ll_opy_:
          bstack1ll1l111lll_opy_ = bstack11lll11lll1_opy_.bstack1ll11l1ll11_opy_
        if browser_version and browser_version != bstack11ll11_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᙃ") and int(browser_version.split(bstack11ll11_opy_ (u"ࠩ࠱ࠫᙄ"))[0]) <= bstack1ll1l111lll_opy_:
          logger.warning(bstack1lll11ll111_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࡳࡩ࡯ࡡࡤ࠵࠶ࡿ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡢࡧ࡭ࡸ࡯࡮ࡧࡢࡺࡪࡸࡳࡪࡱࡱࢁ࠳࠭ᙅ"))
          return False
        if not options:
          bstack1ll11l1lll1_opy_ = caps.get(bstack11ll11_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᙆ")) or bstack11lll1l1l11_opy_.get(bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᙇ"), {})
          if bstack11ll11_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᙈ") in bstack1ll11l1lll1_opy_.get(bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᙉ"), []):
              logger.warning(bstack11ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᙊ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᙋ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1llll1l1_opy_ = config.get(bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᙌ"), {})
    bstack1ll1llll1l1_opy_[bstack11ll11_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᙍ")] = os.getenv(bstack11ll11_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᙎ"))
    bstack11ll1ll1l11_opy_ = json.loads(os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᙏ"), bstack11ll11_opy_ (u"ࠧࡼࡿࠪᙐ"))).get(bstack11ll11_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᙑ"))
    if not config[bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᙒ")].get(bstack11ll11_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᙓ")):
      if bstack11ll11_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᙔ") in caps:
        caps[bstack11ll11_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙕ")][bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙖ")] = bstack1ll1llll1l1_opy_
        caps[bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᙗ")][bstack11ll11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᙘ")][bstack11ll11_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙙ")] = bstack11ll1ll1l11_opy_
      else:
        caps[bstack11ll11_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᙚ")] = bstack1ll1llll1l1_opy_
        caps[bstack11ll11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᙛ")][bstack11ll11_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙜ")] = bstack11ll1ll1l11_opy_
  except Exception as error:
    logger.debug(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢᙝ") +  str(error))
def bstack1l1111l1l1_opy_(driver, bstack11lll111l1l_opy_):
  try:
    setattr(driver, bstack11ll11_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᙞ"), True)
    session = driver.session_id
    if session:
      bstack11lll11l11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll11l11l_opy_ = False
      bstack11lll11l11l_opy_ = url.scheme in [bstack11ll11_opy_ (u"ࠣࡪࡷࡸࡵࠨᙟ"), bstack11ll11_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᙠ")]
      if bstack11lll11l11l_opy_:
        if bstack11lll111l1l_opy_:
          logger.info(bstack11ll11_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥᙡ"))
      return bstack11lll111l1l_opy_
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᙢ") + str(e))
    return False
def bstack1ll1l1l111_opy_(driver, name, path):
  try:
    bstack1ll111ll1ll_opy_ = {
        bstack11ll11_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᙣ"): threading.current_thread().current_test_uuid,
        bstack11ll11_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᙤ"): os.environ.get(bstack11ll11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᙥ"), bstack11ll11_opy_ (u"ࠨࠩᙦ")),
        bstack11ll11_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ᙧ"): os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᙨ"), bstack11ll11_opy_ (u"ࠫࠬᙩ"))
    }
    bstack1ll11ll111l_opy_ = bstack1ll11ll1_opy_.bstack1ll11ll11l1_opy_(EVENTS.bstack1lllll1l11_opy_.value)
    logger.debug(bstack11ll11_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᙪ"))
    try:
      if (bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᙫ"), None) and bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙬ"), None)):
        scripts = {bstack11ll11_opy_ (u"ࠨࡵࡦࡥࡳ࠭᙭"): bstack11llll1l1l_opy_.perform_scan}
        bstack11ll1l1lll1_opy_ = json.loads(scripts[bstack11ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢ᙮")].replace(bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᙯ"), bstack11ll11_opy_ (u"ࠦࠧᙰ")))
        bstack11ll1l1lll1_opy_[bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᙱ")][bstack11ll11_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᙲ")] = None
        scripts[bstack11ll11_opy_ (u"ࠢࡴࡥࡤࡲࠧᙳ")] = bstack11ll11_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᙴ") + json.dumps(bstack11ll1l1lll1_opy_)
        bstack11llll1l1l_opy_.bstack11ll1ll1ll_opy_(scripts)
        bstack11llll1l1l_opy_.store()
        logger.debug(driver.execute_script(bstack11llll1l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11llll1l1l_opy_.perform_scan, {bstack11ll11_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᙵ"): name}))
      bstack1ll11ll1_opy_.end(EVENTS.bstack1lllll1l11_opy_.value, bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᙶ"), bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᙷ"), True, None)
    except Exception as error:
      bstack1ll11ll1_opy_.end(EVENTS.bstack1lllll1l11_opy_.value, bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᙸ"), bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᙹ"), False, str(error))
    bstack1ll11ll111l_opy_ = bstack1ll11ll1_opy_.bstack11ll1l1ll11_opy_(EVENTS.bstack1ll1l1111l1_opy_.value)
    bstack1ll11ll1_opy_.mark(bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᙺ"))
    try:
      if (bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᙻ"), None) and bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᙼ"), None)):
        scripts = {bstack11ll11_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᙽ"): bstack11llll1l1l_opy_.perform_scan}
        bstack11ll1l1lll1_opy_ = json.loads(scripts[bstack11ll11_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᙾ")].replace(bstack11ll11_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᙿ"), bstack11ll11_opy_ (u"ࠨࠢ ")))
        bstack11ll1l1lll1_opy_[bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᚁ")][bstack11ll11_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᚂ")] = None
        scripts[bstack11ll11_opy_ (u"ࠤࡶࡧࡦࡴࠢᚃ")] = bstack11ll11_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᚄ") + json.dumps(bstack11ll1l1lll1_opy_)
        bstack11llll1l1l_opy_.bstack11ll1ll1ll_opy_(scripts)
        bstack11llll1l1l_opy_.store()
        logger.debug(driver.execute_script(bstack11llll1l1l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11llll1l1l_opy_.bstack11lll1l1111_opy_, bstack1ll111ll1ll_opy_))
      bstack1ll11ll1_opy_.end(bstack1ll11ll111l_opy_, bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᚅ"), bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᚆ"),True, None)
    except Exception as error:
      bstack1ll11ll1_opy_.end(bstack1ll11ll111l_opy_, bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᚇ"), bstack1ll11ll111l_opy_ + bstack11ll11_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᚈ"),False, str(error))
    logger.info(bstack11ll11_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᚉ"))
  except Exception as bstack1ll11l111l1_opy_:
    logger.error(bstack11ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᚊ") + str(path) + bstack11ll11_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᚋ") + str(bstack1ll11l111l1_opy_))
def bstack11ll1llllll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11ll11_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᚌ")) and str(caps.get(bstack11ll11_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᚍ"))).lower() == bstack11ll11_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢᚎ"):
        bstack11ll1lllll1_opy_ = caps.get(bstack11ll11_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᚏ")) or caps.get(bstack11ll11_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᚐ"))
        if bstack11ll1lllll1_opy_ and int(str(bstack11ll1lllll1_opy_)) < bstack11ll1llll11_opy_:
            return False
    return True
def bstack1l1ll111ll_opy_(config):
  if bstack11ll11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚑ") in config:
        return config[bstack11ll11_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚒ")]
  for platform in config.get(bstack11ll11_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᚓ"), []):
      if bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚔ") in platform:
          return platform[bstack11ll11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚕ")]
  return None
def bstack1l1l111l1_opy_(bstack1l1lllll_opy_):
  try:
    browser_name = bstack1l1lllll_opy_[bstack11ll11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᚖ")]
    browser_version = bstack1l1lllll_opy_[bstack11ll11_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᚗ")]
    chrome_options = bstack1l1lllll_opy_[bstack11ll11_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪᚘ")]
    try:
        bstack11lll1111l1_opy_ = int(browser_version.split(bstack11ll11_opy_ (u"ࠪ࠲ࠬᚙ"))[0])
    except ValueError as e:
        logger.error(bstack11ll11_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡳࡼࡥࡳࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠣᚚ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11ll11_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ᚛")):
        logger.warning(bstack11ll11_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ᚜"))
        return False
    if bstack11lll1111l1_opy_ < bstack11lll11lll1_opy_.bstack1ll11l1ll11_opy_:
        logger.warning(bstack1lll11ll111_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡸࠦࡃࡩࡴࡲࡱࡪࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡼࡅࡒࡒࡘ࡚ࡁࡏࡖࡖ࠲ࡒࡏࡎࡊࡏࡘࡑࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡖࡒࡓࡓࡗ࡚ࡅࡅࡡࡆࡌࡗࡕࡍࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࢀࠤࡴࡸࠠࡩ࡫ࡪ࡬ࡪࡸ࠮ࠨ᚝"))
        return False
    if chrome_options and any(bstack11ll11_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬ᚞") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11ll11_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦ᚟"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11ll11_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡪࡴࡸࠠ࡭ࡱࡦࡥࡱࠦࡃࡩࡴࡲࡱࡪࡀࠠࠣᚠ") + str(e))
    return False
def bstack11l1l111l_opy_(bstack11l11111l1_opy_, config):
    try:
      bstack1ll111ll1l1_opy_ = bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚡ") in config and config[bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚢ")] == True
      bstack11lll11l1ll_opy_ = bstack11ll11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᚣ") in config and str(config[bstack11ll11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᚤ")]).lower() != bstack11ll11_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᚥ")
      if not (bstack1ll111ll1l1_opy_ and (not bstack1l111lll1l_opy_(config) or bstack11lll11l1ll_opy_)):
        return bstack11l11111l1_opy_
      bstack11lll11ll1l_opy_ = bstack11llll1l1l_opy_.bstack11lll1l1ll1_opy_
      if bstack11lll11ll1l_opy_ is None:
        logger.debug(bstack11ll11_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡫ࠠࡏࡱࡱࡩࠧᚦ"))
        return bstack11l11111l1_opy_
      bstack11lll1111ll_opy_ = int(str(bstack11ll1lll1ll_opy_()).split(bstack11ll11_opy_ (u"ࠪ࠲ࠬᚧ"))[0])
      logger.debug(bstack11ll11_opy_ (u"ࠦࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࠦᚨ") + str(bstack11lll1111ll_opy_) + bstack11ll11_opy_ (u"ࠧࠨᚩ"))
      if bstack11lll1111ll_opy_ == 3 and isinstance(bstack11l11111l1_opy_, dict) and bstack11ll11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚪ") in bstack11l11111l1_opy_ and bstack11lll11ll1l_opy_ is not None:
        if bstack11ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚫ") not in bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚬ")]:
          bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᚭ")][bstack11ll11_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚮ")] = {}
        if bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩᚯ") in bstack11lll11ll1l_opy_:
          if bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪᚰ") not in bstack11l11111l1_opy_[bstack11ll11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚱ")][bstack11ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚲ")]:
            bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚳ")][bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚴ")][bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚵ")] = []
          for arg in bstack11lll11ll1l_opy_[bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩᚶ")]:
            if arg not in bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᚷ")][bstack11ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚸ")][bstack11ll11_opy_ (u"ࠧࡢࡴࡪࡷࠬᚹ")]:
              bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚺ")][bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚻ")][bstack11ll11_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚼ")].append(arg)
        if bstack11ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᚽ") in bstack11lll11ll1l_opy_:
          if bstack11ll11_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᚾ") not in bstack11l11111l1_opy_[bstack11ll11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚿ")][bstack11ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛀ")]:
            bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᛁ")][bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᛂ")][bstack11ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᛃ")] = []
          for ext in bstack11lll11ll1l_opy_[bstack11ll11_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᛄ")]:
            if ext not in bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᛅ")][bstack11ll11_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᛆ")][bstack11ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᛇ")]:
              bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᛈ")][bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᛉ")][bstack11ll11_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᛊ")].append(ext)
        if bstack11ll11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᛋ") in bstack11lll11ll1l_opy_:
          if bstack11ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᛌ") not in bstack11l11111l1_opy_[bstack11ll11_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᛍ")][bstack11ll11_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛎ")]:
            bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᛏ")][bstack11ll11_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᛐ")][bstack11ll11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᛑ")] = {}
          bstack11ll1ll11l1_opy_(bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᛒ")][bstack11ll11_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛓ")][bstack11ll11_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᛔ")],
                    bstack11lll11ll1l_opy_[bstack11ll11_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᛕ")])
        os.environ[bstack11ll11_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᛖ")] = bstack11ll11_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᛗ")
        return bstack11l11111l1_opy_
      else:
        chrome_options = None
        if isinstance(bstack11l11111l1_opy_, ChromeOptions):
          chrome_options = bstack11l11111l1_opy_
        elif isinstance(bstack11l11111l1_opy_, dict):
          for value in bstack11l11111l1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11l11111l1_opy_, dict):
            bstack11l11111l1_opy_[bstack11ll11_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᛘ")] = chrome_options
          else:
            bstack11l11111l1_opy_ = chrome_options
        if bstack11lll11ll1l_opy_ is not None:
          if bstack11ll11_opy_ (u"ࠫࡦࡸࡧࡴࠩᛙ") in bstack11lll11ll1l_opy_:
                bstack11lll1l1l1l_opy_ = chrome_options.arguments or []
                new_args = bstack11lll11ll1l_opy_[bstack11ll11_opy_ (u"ࠬࡧࡲࡨࡵࠪᛚ")]
                for arg in new_args:
                    if arg not in bstack11lll1l1l1l_opy_:
                        chrome_options.add_argument(arg)
          if bstack11ll11_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᛛ") in bstack11lll11ll1l_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11ll11_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᛜ"), [])
                bstack11lll11llll_opy_ = bstack11lll11ll1l_opy_[bstack11ll11_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᛝ")]
                for extension in bstack11lll11llll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11ll11_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᛞ") in bstack11lll11ll1l_opy_:
                bstack11lll111ll1_opy_ = chrome_options.experimental_options.get(bstack11ll11_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᛟ"), {})
                bstack11lll11l1l1_opy_ = bstack11lll11ll1l_opy_[bstack11ll11_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᛠ")]
                bstack11ll1ll11l1_opy_(bstack11lll111ll1_opy_, bstack11lll11l1l1_opy_)
                chrome_options.add_experimental_option(bstack11ll11_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᛡ"), bstack11lll111ll1_opy_)
        os.environ[bstack11ll11_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᛢ")] = bstack11ll11_opy_ (u"ࠧࡵࡴࡸࡩࠬᛣ")
        return bstack11l11111l1_opy_
    except Exception as e:
      logger.error(bstack11ll11_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡥࡦ࡬ࡲ࡬ࠦ࡮ࡰࡰ࠰ࡆࡘࠦࡩ࡯ࡨࡵࡥࠥࡧ࠱࠲ࡻࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠨᛤ") + str(e))
      return bstack11l11111l1_opy_