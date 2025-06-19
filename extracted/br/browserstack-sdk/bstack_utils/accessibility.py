# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11lll1ll1l1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11lll111l11_opy_ as bstack11lll1l1l1l_opy_, EVENTS
from bstack_utils.bstack11ll1l1ll_opy_ import bstack11ll1l1ll_opy_
from bstack_utils.helper import bstack1llllllll1_opy_, bstack111l1lll11_opy_, bstack1l1l111l1_opy_, bstack11lll111111_opy_, \
  bstack11llll111ll_opy_, bstack1lll111lll_opy_, get_host_info, bstack11lll11l1ll_opy_, bstack1l1ll1l111_opy_, bstack111l1ll1l1_opy_, bstack11lll11111l_opy_, bstack11lll111l1l_opy_, bstack1ll11l1l1l_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1111ll111_opy_ import get_logger
from bstack_utils.bstack1ll1l111ll_opy_ import bstack1llll1l1l11_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1ll1l111ll_opy_ = bstack1llll1l1l11_opy_()
@bstack111l1ll1l1_opy_(class_method=False)
def _11lll1l11l1_opy_(driver, bstack1111l1lll1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111lll_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᖡ"): caps.get(bstack111lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᖢ"), None),
        bstack111lll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᖣ"): bstack1111l1lll1_opy_.get(bstack111lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖤ"), None),
        bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᖥ"): caps.get(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᖦ"), None),
        bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᖧ"): caps.get(bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖨ"), None)
    }
  except Exception as error:
    logger.debug(bstack111lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᖩ") + str(error))
  return response
def on():
    if os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᖪ"), None) is None or os.environ[bstack111lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖫ")] == bstack111lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᖬ"):
        return False
    return True
def bstack1l111lll1l_opy_(config):
  return config.get(bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᖭ"), False) or any([p.get(bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᖮ"), False) == True for p in config.get(bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᖯ"), [])])
def bstack1111111l1_opy_(config, bstack1l11l11l1l_opy_):
  try:
    bstack11lll1ll1ll_opy_ = config.get(bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᖰ"), False)
    if int(bstack1l11l11l1l_opy_) < len(config.get(bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᖱ"), [])) and config[bstack111lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᖲ")][bstack1l11l11l1l_opy_]:
      bstack11lll1ll111_opy_ = config[bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᖳ")][bstack1l11l11l1l_opy_].get(bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᖴ"), None)
    else:
      bstack11lll1ll111_opy_ = config.get(bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᖵ"), None)
    if bstack11lll1ll111_opy_ != None:
      bstack11lll1ll1ll_opy_ = bstack11lll1ll111_opy_
    bstack11lll111lll_opy_ = os.getenv(bstack111lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᖶ")) is not None and len(os.getenv(bstack111lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᖷ"))) > 0 and os.getenv(bstack111lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᖸ")) != bstack111lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᖹ")
    return bstack11lll1ll1ll_opy_ and bstack11lll111lll_opy_
  except Exception as error:
    logger.debug(bstack111lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᖺ") + str(error))
  return False
def bstack11lllllll1_opy_(test_tags):
  bstack1ll11l1l111_opy_ = os.getenv(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᖻ"))
  if bstack1ll11l1l111_opy_ is None:
    return True
  bstack1ll11l1l111_opy_ = json.loads(bstack1ll11l1l111_opy_)
  try:
    include_tags = bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᖼ")] if bstack111lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᖽ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᖾ")], list) else []
    exclude_tags = bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᖿ")] if bstack111lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᗀ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstack111lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᗁ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᗂ") + str(error))
  return False
def bstack11lll1l11ll_opy_(config, bstack11llll11111_opy_, bstack11ll1llllll_opy_, bstack11lll11llll_opy_):
  bstack11lll1l1111_opy_ = bstack11lll111111_opy_(config)
  bstack11llll111l1_opy_ = bstack11llll111ll_opy_(config)
  if bstack11lll1l1111_opy_ is None or bstack11llll111l1_opy_ is None:
    logger.error(bstack111lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᗃ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᗄ"), bstack111lll_opy_ (u"ࠨࡽࢀࠫᗅ")))
    data = {
        bstack111lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᗆ"): config[bstack111lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᗇ")],
        bstack111lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᗈ"): config.get(bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᗉ"), os.path.basename(os.getcwd())),
        bstack111lll_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᗊ"): bstack1llllllll1_opy_(),
        bstack111lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᗋ"): config.get(bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᗌ"), bstack111lll_opy_ (u"ࠩࠪᗍ")),
        bstack111lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᗎ"): {
            bstack111lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᗏ"): bstack11llll11111_opy_,
            bstack111lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗐ"): bstack11ll1llllll_opy_,
            bstack111lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᗑ"): __version__,
            bstack111lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᗒ"): bstack111lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᗓ"),
            bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᗔ"): bstack111lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᗕ"),
            bstack111lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᗖ"): bstack11lll11llll_opy_
        },
        bstack111lll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᗗ"): settings,
        bstack111lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᗘ"): bstack11lll11l1ll_opy_(),
        bstack111lll_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᗙ"): bstack1lll111lll_opy_(),
        bstack111lll_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᗚ"): get_host_info(),
        bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᗛ"): bstack1l1l111l1_opy_(config)
    }
    headers = {
        bstack111lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᗜ"): bstack111lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᗝ"),
    }
    config = {
        bstack111lll_opy_ (u"ࠬࡧࡵࡵࡪࠪᗞ"): (bstack11lll1l1111_opy_, bstack11llll111l1_opy_),
        bstack111lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᗟ"): headers
    }
    response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"ࠧࡑࡑࡖࡘࠬᗠ"), bstack11lll1l1l1l_opy_ + bstack111lll_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᗡ"), data, config)
    bstack11lll11ll1l_opy_ = response.json()
    if bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᗢ")]:
      parsed = json.loads(os.getenv(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᗣ"), bstack111lll_opy_ (u"ࠫࢀࢃࠧᗤ")))
      parsed[bstack111lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗥ")] = bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᗦ")][bstack111lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗧ")]
      os.environ[bstack111lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᗨ")] = json.dumps(parsed)
      bstack11ll1l1ll_opy_.bstack1ll1l11l1_opy_(bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᗩ")][bstack111lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᗪ")])
      bstack11ll1l1ll_opy_.bstack11lll1lll11_opy_(bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"ࠫࡩࡧࡴࡢࠩᗫ")][bstack111lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᗬ")])
      bstack11ll1l1ll_opy_.store()
      return bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᗭ")][bstack111lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᗮ")], bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᗯ")][bstack111lll_opy_ (u"ࠩ࡬ࡨࠬᗰ")]
    else:
      logger.error(bstack111lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᗱ") + bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᗲ")])
      if bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗳ")] == bstack111lll_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᗴ"):
        for bstack11lll1111l1_opy_ in bstack11lll11ll1l_opy_[bstack111lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᗵ")]:
          logger.error(bstack11lll1111l1_opy_[bstack111lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᗶ")])
      return None, None
  except Exception as error:
    logger.error(bstack111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᗷ") +  str(error))
    return None, None
def bstack11lll11ll11_opy_():
  if os.getenv(bstack111lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᗸ")) is None:
    return {
        bstack111lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᗹ"): bstack111lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᗺ"),
        bstack111lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᗻ"): bstack111lll_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᗼ")
    }
  data = {bstack111lll_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᗽ"): bstack1llllllll1_opy_()}
  headers = {
      bstack111lll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᗾ"): bstack111lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᗿ") + os.getenv(bstack111lll_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᘀ")),
      bstack111lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᘁ"): bstack111lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᘂ")
  }
  response = bstack1l1ll1l111_opy_(bstack111lll_opy_ (u"ࠧࡑࡗࡗࠫᘃ"), bstack11lll1l1l1l_opy_ + bstack111lll_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᘄ"), data, { bstack111lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᘅ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᘆ") + bstack111l1lll11_opy_().isoformat() + bstack111lll_opy_ (u"ࠫ࡟࠭ᘇ"))
      return {bstack111lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᘈ"): bstack111lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᘉ"), bstack111lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᘊ"): bstack111lll_opy_ (u"ࠨࠩᘋ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᘌ") + str(error))
    return {
        bstack111lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᘍ"): bstack111lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᘎ"),
        bstack111lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᘏ"): str(error)
    }
def bstack11lll1ll11l_opy_(bstack11llll11l1l_opy_):
    return re.match(bstack111lll_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᘐ"), bstack11llll11l1l_opy_.strip()) is not None
def bstack111l1111l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11llll11l11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llll11l11_opy_ = desired_capabilities
        else:
          bstack11llll11l11_opy_ = {}
        bstack11ll1lll11l_opy_ = (bstack11llll11l11_opy_.get(bstack111lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᘑ"), bstack111lll_opy_ (u"ࠨࠩᘒ")).lower() or caps.get(bstack111lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᘓ"), bstack111lll_opy_ (u"ࠪࠫᘔ")).lower())
        if bstack11ll1lll11l_opy_ == bstack111lll_opy_ (u"ࠫ࡮ࡵࡳࠨᘕ"):
            return True
        if bstack11ll1lll11l_opy_ == bstack111lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᘖ"):
            bstack11lll1lll1l_opy_ = str(float(caps.get(bstack111lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘗ")) or bstack11llll11l11_opy_.get(bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘘ"), {}).get(bstack111lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᘙ"),bstack111lll_opy_ (u"ࠩࠪᘚ"))))
            if bstack11ll1lll11l_opy_ == bstack111lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᘛ") and int(bstack11lll1lll1l_opy_.split(bstack111lll_opy_ (u"ࠫ࠳࠭ᘜ"))[0]) < float(bstack11lll1l111l_opy_):
                logger.warning(str(bstack11lll1l1lll_opy_))
                return False
            return True
        bstack1ll1l11l1ll_opy_ = caps.get(bstack111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘝ"), {}).get(bstack111lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᘞ"), caps.get(bstack111lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᘟ"), bstack111lll_opy_ (u"ࠨࠩᘠ")))
        if bstack1ll1l11l1ll_opy_:
            logger.warning(bstack111lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᘡ"))
            return False
        browser = caps.get(bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᘢ"), bstack111lll_opy_ (u"ࠫࠬᘣ")).lower() or bstack11llll11l11_opy_.get(bstack111lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᘤ"), bstack111lll_opy_ (u"࠭ࠧᘥ")).lower()
        if browser != bstack111lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᘦ"):
            logger.warning(bstack111lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᘧ"))
            return False
        browser_version = caps.get(bstack111lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᘨ")) or caps.get(bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᘩ")) or bstack11llll11l11_opy_.get(bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘪ")) or bstack11llll11l11_opy_.get(bstack111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᘫ"), {}).get(bstack111lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᘬ")) or bstack11llll11l11_opy_.get(bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᘭ"), {}).get(bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᘮ"))
        bstack1ll1l1l111l_opy_ = bstack11lll1ll1l1_opy_.bstack1ll1l1ll111_opy_
        bstack11lll11l1l1_opy_ = False
        if config is not None:
          bstack11lll11l1l1_opy_ = bstack111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ᘯ") in config and str(config[bstack111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᘰ")]).lower() != bstack111lll_opy_ (u"ࠫ࡫ࡧ࡬ࡴࡧࠪᘱ")
        if os.environ.get(bstack111lll_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᘲ"), bstack111lll_opy_ (u"࠭ࠧᘳ")).lower() == bstack111lll_opy_ (u"ࠧࡵࡴࡸࡩࠬᘴ") or bstack11lll11l1l1_opy_:
          bstack1ll1l1l111l_opy_ = bstack11lll1ll1l1_opy_.bstack1ll1l1l1111_opy_
        if browser_version and browser_version != bstack111lll_opy_ (u"ࠨ࡮ࡤࡸࡪࡹࡴࠨᘵ") and int(browser_version.split(bstack111lll_opy_ (u"ࠩ࠱ࠫᘶ"))[0]) <= bstack1ll1l1l111l_opy_:
          logger.warning(bstack1lllll111l1_opy_ (u"ࠪࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥ࡭ࡲࡦࡣࡷࡩࡷࠦࡴࡩࡣࡱࠤࢀࡳࡩ࡯ࡡࡤ࠵࠶ࡿ࡟ࡴࡷࡳࡴࡴࡸࡴࡦࡦࡢࡧ࡭ࡸ࡯࡮ࡧࡢࡺࡪࡸࡳࡪࡱࡱࢁ࠳࠭ᘷ"))
          return False
        if not options:
          bstack1ll1l1ll1ll_opy_ = caps.get(bstack111lll_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᘸ")) or bstack11llll11l11_opy_.get(bstack111lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᘹ"), {})
          if bstack111lll_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪᘺ") in bstack1ll1l1ll1ll_opy_.get(bstack111lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᘻ"), []):
              logger.warning(bstack111lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᘼ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack111lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡤࡰ࡮ࡪࡡࡵࡧࠣࡥ࠶࠷ࡹࠡࡵࡸࡴࡵࡵࡲࡵࠢ࠽ࠦᘽ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll1ll11l1_opy_ = config.get(bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᘾ"), {})
    bstack1lll1ll11l1_opy_[bstack111lll_opy_ (u"ࠫࡦࡻࡴࡩࡖࡲ࡯ࡪࡴࠧᘿ")] = os.getenv(bstack111lll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᙀ"))
    bstack11lll11l111_opy_ = json.loads(os.getenv(bstack111lll_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᙁ"), bstack111lll_opy_ (u"ࠧࡼࡿࠪᙂ"))).get(bstack111lll_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᙃ"))
    if not config[bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡑࡴࡲࡨࡺࡩࡴࡎࡣࡳࠫᙄ")].get(bstack111lll_opy_ (u"ࠥࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠤᙅ")):
      if bstack111lll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᙆ") in caps:
        caps[bstack111lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᙇ")][bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᙈ")] = bstack1lll1ll11l1_opy_
        caps[bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᙉ")][bstack111lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᙊ")][bstack111lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙋ")] = bstack11lll11l111_opy_
      else:
        caps[bstack111lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᙌ")] = bstack1lll1ll11l1_opy_
        caps[bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᙍ")][bstack111lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙎ")] = bstack11lll11l111_opy_
  except Exception as error:
    logger.debug(bstack111lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡵࡨࡸࡹ࡯࡮ࡨࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷ࠳ࠦࡅࡳࡴࡲࡶ࠿ࠦࠢᙏ") +  str(error))
def bstack1ll1l1l1l1_opy_(driver, bstack11lll1l1l11_opy_):
  try:
    setattr(driver, bstack111lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱࡁ࠲࠳ࡼࡗ࡭ࡵࡵ࡭ࡦࡖࡧࡦࡴࠧᙐ"), True)
    session = driver.session_id
    if session:
      bstack11lll1l1ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1l1ll1_opy_ = False
      bstack11lll1l1ll1_opy_ = url.scheme in [bstack111lll_opy_ (u"ࠣࡪࡷࡸࡵࠨᙑ"), bstack111lll_opy_ (u"ࠤ࡫ࡸࡹࡶࡳࠣᙒ")]
      if bstack11lll1l1ll1_opy_:
        if bstack11lll1l1l11_opy_:
          logger.info(bstack111lll_opy_ (u"ࠥࡗࡪࡺࡵࡱࠢࡩࡳࡷࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡩࡣࡶࠤࡸࡺࡡࡳࡶࡨࡨ࠳ࠦࡁࡶࡶࡲࡱࡦࡺࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤࡪࡾࡥࡤࡷࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡨࡥࡨ࡫ࡱࠤࡲࡵ࡭ࡦࡰࡷࡥࡷ࡯࡬ࡺ࠰ࠥᙓ"))
      return bstack11lll1l1l11_opy_
  except Exception as e:
    logger.error(bstack111lll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡷࡹࡧࡲࡵ࡫ࡱ࡫ࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡧࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡶࡧࡦࡴࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩ࠿ࠦࠢᙔ") + str(e))
    return False
def bstack1ll1ll1l11_opy_(driver, name, path):
  try:
    bstack1ll1l1l1lll_opy_ = {
        bstack111lll_opy_ (u"ࠬࡺࡨࡕࡧࡶࡸࡗࡻ࡮ࡖࡷ࡬ࡨࠬᙕ"): threading.current_thread().current_test_uuid,
        bstack111lll_opy_ (u"࠭ࡴࡩࡄࡸ࡭ࡱࡪࡕࡶ࡫ࡧࠫᙖ"): os.environ.get(bstack111lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡖࡗࡌࡈࠬᙗ"), bstack111lll_opy_ (u"ࠨࠩᙘ")),
        bstack111lll_opy_ (u"ࠩࡷ࡬ࡏࡽࡴࡕࡱ࡮ࡩࡳ࠭ᙙ"): os.environ.get(bstack111lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚ࡈࡖࡄࡢࡎ࡜࡚ࠧᙚ"), bstack111lll_opy_ (u"ࠫࠬᙛ"))
    }
    bstack1ll11llll11_opy_ = bstack1ll1l111ll_opy_.bstack1ll1l1l1l1l_opy_(EVENTS.bstack1ll1l1l1_opy_.value)
    logger.debug(bstack111lll_opy_ (u"ࠬࡖࡥࡳࡨࡲࡶࡲ࡯࡮ࡨࠢࡶࡧࡦࡴࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡣࡹ࡭ࡳ࡭ࠠࡳࡧࡶࡹࡱࡺࡳࠨᙜ"))
    try:
      if (bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᙝ"), None) and bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᙞ"), None)):
        scripts = {bstack111lll_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᙟ"): bstack11ll1l1ll_opy_.perform_scan}
        bstack11lll1llll1_opy_ = json.loads(scripts[bstack111lll_opy_ (u"ࠤࡶࡧࡦࡴࠢᙠ")].replace(bstack111lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᙡ"), bstack111lll_opy_ (u"ࠦࠧᙢ")))
        bstack11lll1llll1_opy_[bstack111lll_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᙣ")][bstack111lll_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᙤ")] = None
        scripts[bstack111lll_opy_ (u"ࠢࡴࡥࡤࡲࠧᙥ")] = bstack111lll_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᙦ") + json.dumps(bstack11lll1llll1_opy_)
        bstack11ll1l1ll_opy_.bstack1ll1l11l1_opy_(scripts)
        bstack11ll1l1ll_opy_.store()
        logger.debug(driver.execute_script(bstack11ll1l1ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll1l1ll_opy_.perform_scan, {bstack111lll_opy_ (u"ࠤࡰࡩࡹ࡮࡯ࡥࠤᙧ"): name}))
      bstack1ll1l111ll_opy_.end(EVENTS.bstack1ll1l1l1_opy_.value, bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᙨ"), bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᙩ"), True, None)
    except Exception as error:
      bstack1ll1l111ll_opy_.end(EVENTS.bstack1ll1l1l1_opy_.value, bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᙪ"), bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᙫ"), False, str(error))
    bstack1ll11llll11_opy_ = bstack1ll1l111ll_opy_.bstack11ll1llll11_opy_(EVENTS.bstack1ll11lll111_opy_.value)
    bstack1ll1l111ll_opy_.mark(bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᙬ"))
    try:
      if (bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ᙭"), None) and bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ᙮"), None)):
        scripts = {bstack111lll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᙯ"): bstack11ll1l1ll_opy_.perform_scan}
        bstack11lll1llll1_opy_ = json.loads(scripts[bstack111lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᙰ")].replace(bstack111lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᙱ"), bstack111lll_opy_ (u"ࠨࠢᙲ")))
        bstack11lll1llll1_opy_[bstack111lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᙳ")][bstack111lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᙴ")] = None
        scripts[bstack111lll_opy_ (u"ࠤࡶࡧࡦࡴࠢᙵ")] = bstack111lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᙶ") + json.dumps(bstack11lll1llll1_opy_)
        bstack11ll1l1ll_opy_.bstack1ll1l11l1_opy_(scripts)
        bstack11ll1l1ll_opy_.store()
        logger.debug(driver.execute_script(bstack11ll1l1ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll1l1ll_opy_.bstack11ll1lllll1_opy_, bstack1ll1l1l1lll_opy_))
      bstack1ll1l111ll_opy_.end(bstack1ll11llll11_opy_, bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᙷ"), bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᙸ"),True, None)
    except Exception as error:
      bstack1ll1l111ll_opy_.end(bstack1ll11llll11_opy_, bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᙹ"), bstack1ll11llll11_opy_ + bstack111lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᙺ"),False, str(error))
    logger.info(bstack111lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡩࡣࡶࠤࡪࡴࡤࡦࡦ࠱ࠦᙻ"))
  except Exception as bstack1ll11l1lll1_opy_:
    logger.error(bstack111lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᙼ") + str(path) + bstack111lll_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧᙽ") + str(bstack1ll11l1lll1_opy_))
def bstack11llll1111l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack111lll_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥᙾ")) and str(caps.get(bstack111lll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᙿ"))).lower() == bstack111lll_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢ "):
        bstack11lll1lll1l_opy_ = caps.get(bstack111lll_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤᚁ")) or caps.get(bstack111lll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᚂ"))
        if bstack11lll1lll1l_opy_ and int(str(bstack11lll1lll1l_opy_)) < bstack11lll1l111l_opy_:
            return False
    return True
def bstack11ll1ll11_opy_(config):
  if bstack111lll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᚃ") in config:
        return config[bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᚄ")]
  for platform in config.get(bstack111lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᚅ"), []):
      if bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚆ") in platform:
          return platform[bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᚇ")]
  return None
def bstack1lll11llll_opy_(bstack1lll1lll11_opy_):
  try:
    browser_name = bstack1lll1lll11_opy_[bstack111lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭ᚈ")]
    browser_version = bstack1lll1lll11_opy_[bstack111lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᚉ")]
    chrome_options = bstack1lll1lll11_opy_[bstack111lll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪᚊ")]
    try:
        bstack11ll1lll1l1_opy_ = int(browser_version.split(bstack111lll_opy_ (u"ࠪ࠲ࠬᚋ"))[0])
    except ValueError as e:
        logger.error(bstack111lll_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡳࡼࡥࡳࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠣᚌ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack111lll_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᚍ")):
        logger.warning(bstack111lll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᚎ"))
        return False
    if bstack11ll1lll1l1_opy_ < bstack11lll1ll1l1_opy_.bstack1ll1l1l1111_opy_:
        logger.warning(bstack1lllll111l1_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡸࠦࡃࡩࡴࡲࡱࡪࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡼࡅࡒࡒࡘ࡚ࡁࡏࡖࡖ࠲ࡒࡏࡎࡊࡏࡘࡑࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡖࡒࡓࡓࡗ࡚ࡅࡅࡡࡆࡌࡗࡕࡍࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࢀࠤࡴࡸࠠࡩ࡫ࡪ࡬ࡪࡸ࠮ࠨᚏ"))
        return False
    if chrome_options and any(bstack111lll_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬᚐ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack111lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᚑ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack111lll_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡪࡴࡸࠠ࡭ࡱࡦࡥࡱࠦࡃࡩࡴࡲࡱࡪࡀࠠࠣᚒ") + str(e))
    return False
def bstack1ll11111ll_opy_(bstack11l11l111_opy_, config):
    try:
      bstack1ll11l1l11l_opy_ = bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᚓ") in config and config[bstack111lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᚔ")] == True
      bstack11lll11l1l1_opy_ = bstack111lll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᚕ") in config and str(config[bstack111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᚖ")]).lower() != bstack111lll_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᚗ")
      if not (bstack1ll11l1l11l_opy_ and (not bstack1l1l111l1_opy_(config) or bstack11lll11l1l1_opy_)):
        return bstack11l11l111_opy_
      bstack11lll1lllll_opy_ = bstack11ll1l1ll_opy_.bstack11lll1111ll_opy_
      if bstack11lll1lllll_opy_ is None:
        logger.debug(bstack111lll_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡫ࠠࡏࡱࡱࡩࠧᚘ"))
        return bstack11l11l111_opy_
      bstack11ll1lll1ll_opy_ = int(str(bstack11lll111l1l_opy_()).split(bstack111lll_opy_ (u"ࠪ࠲ࠬᚙ"))[0])
      logger.debug(bstack111lll_opy_ (u"ࠦࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࠦᚚ") + str(bstack11ll1lll1ll_opy_) + bstack111lll_opy_ (u"ࠧࠨ᚛"))
      if bstack11ll1lll1ll_opy_ == 3 and isinstance(bstack11l11l111_opy_, dict) and bstack111lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᚜") in bstack11l11l111_opy_ and bstack11lll1lllll_opy_ is not None:
        if bstack111lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᚝") not in bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨ᚞")]:
          bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᚟")][bstack111lll_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚠ")] = {}
        if bstack111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᚡ") in bstack11lll1lllll_opy_:
          if bstack111lll_opy_ (u"ࠬࡧࡲࡨࡵࠪᚢ") not in bstack11l11l111_opy_[bstack111lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚣ")][bstack111lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚤ")]:
            bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚥ")][bstack111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚦ")][bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚧ")] = []
          for arg in bstack11lll1lllll_opy_[bstack111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᚨ")]:
            if arg not in bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᚩ")][bstack111lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚪ")][bstack111lll_opy_ (u"ࠧࡢࡴࡪࡷࠬᚫ")]:
              bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚬ")][bstack111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚭ")][bstack111lll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᚮ")].append(arg)
        if bstack111lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᚯ") in bstack11lll1lllll_opy_:
          if bstack111lll_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᚰ") not in bstack11l11l111_opy_[bstack111lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚱ")][bstack111lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᚲ")]:
            bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚳ")][bstack111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚴ")][bstack111lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᚵ")] = []
          for ext in bstack11lll1lllll_opy_[bstack111lll_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᚶ")]:
            if ext not in bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᚷ")][bstack111lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚸ")][bstack111lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᚹ")]:
              bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᚺ")][bstack111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚻ")][bstack111lll_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᚼ")].append(ext)
        if bstack111lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᚽ") in bstack11lll1lllll_opy_:
          if bstack111lll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᚾ") not in bstack11l11l111_opy_[bstack111lll_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᚿ")][bstack111lll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᛀ")]:
            bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᛁ")][bstack111lll_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᛂ")][bstack111lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᛃ")] = {}
          bstack11lll11111l_opy_(bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᛄ")][bstack111lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᛅ")][bstack111lll_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᛆ")],
                    bstack11lll1lllll_opy_[bstack111lll_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᛇ")])
        os.environ[bstack111lll_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᛈ")] = bstack111lll_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᛉ")
        return bstack11l11l111_opy_
      else:
        chrome_options = None
        if isinstance(bstack11l11l111_opy_, ChromeOptions):
          chrome_options = bstack11l11l111_opy_
        elif isinstance(bstack11l11l111_opy_, dict):
          for value in bstack11l11l111_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack11l11l111_opy_, dict):
            bstack11l11l111_opy_[bstack111lll_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᛊ")] = chrome_options
          else:
            bstack11l11l111_opy_ = chrome_options
        if bstack11lll1lllll_opy_ is not None:
          if bstack111lll_opy_ (u"ࠫࡦࡸࡧࡴࠩᛋ") in bstack11lll1lllll_opy_:
                bstack11lll11lll1_opy_ = chrome_options.arguments or []
                new_args = bstack11lll1lllll_opy_[bstack111lll_opy_ (u"ࠬࡧࡲࡨࡵࠪᛌ")]
                for arg in new_args:
                    if arg not in bstack11lll11lll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack111lll_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᛍ") in bstack11lll1lllll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack111lll_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᛎ"), [])
                bstack11ll1llll1l_opy_ = bstack11lll1lllll_opy_[bstack111lll_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᛏ")]
                for extension in bstack11ll1llll1l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack111lll_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᛐ") in bstack11lll1lllll_opy_:
                bstack11lll111ll1_opy_ = chrome_options.experimental_options.get(bstack111lll_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᛑ"), {})
                bstack11lll11l11l_opy_ = bstack11lll1lllll_opy_[bstack111lll_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᛒ")]
                bstack11lll11111l_opy_(bstack11lll111ll1_opy_, bstack11lll11l11l_opy_)
                chrome_options.add_experimental_option(bstack111lll_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᛓ"), bstack11lll111ll1_opy_)
        os.environ[bstack111lll_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᛔ")] = bstack111lll_opy_ (u"ࠧࡵࡴࡸࡩࠬᛕ")
        return bstack11l11l111_opy_
    except Exception as e:
      logger.error(bstack111lll_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡥࡦ࡬ࡲ࡬ࠦ࡮ࡰࡰ࠰ࡆࡘࠦࡩ࡯ࡨࡵࡥࠥࡧ࠱࠲ࡻࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠨᛖ") + str(e))
      return bstack11l11l111_opy_