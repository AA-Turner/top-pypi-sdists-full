# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll1llll1l_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1ll11l1_opy_ as bstack11ll1l1l111_opy_, EVENTS
from bstack_utils.bstack1l11l1l111_opy_ import bstack1l11l1l111_opy_
from bstack_utils.helper import bstack1l1l11lll_opy_, bstack111l1ll11l_opy_, bstack111l1llll_opy_, bstack11ll1lll11l_opy_, \
  bstack11lll111111_opy_, bstack1lllll11l_opy_, get_host_info, bstack11lll11l11l_opy_, bstack1l11l1l1l1_opy_, error_handler, bstack11ll1ll1ll1_opy_, bstack11ll1ll1lll_opy_, bstack1ll11l11ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l1111111_opy_ import get_logger
from bstack_utils.bstack1ll111lll1_opy_ import bstack1ll1ll11111_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1ll111lll1_opy_ = bstack1ll1ll11111_opy_()
@error_handler(class_method=False)
def _11ll1l111ll_opy_(driver, bstack1111l11l1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1_opy_ (u"ࠬࡵࡳࡠࡰࡤࡱࡪ࠭ᘏ"): caps.get(bstack11l1_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬᘐ"), None),
        bstack11l1_opy_ (u"ࠧࡰࡵࡢࡺࡪࡸࡳࡪࡱࡱࠫᘑ"): bstack1111l11l1l_opy_.get(bstack11l1_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᘒ"), None),
        bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡲࡦࡳࡥࠨᘓ"): caps.get(bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᘔ"), None),
        bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᘕ"): caps.get(bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘖ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥ࡬ࡥࡵࡥ࡫࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡧࡩࡹࡧࡩ࡭ࡵࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᘗ") + str(error))
  return response
def on():
    if os.environ.get(bstack11l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᘘ"), None) is None or os.environ[bstack11l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘙ")] == bstack11l1_opy_ (u"ࠤࡱࡹࡱࡲࠢᘚ"):
        return False
    return True
def bstack1l1l1llll_opy_(config):
  return config.get(bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘛ"), False) or any([p.get(bstack11l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘜ"), False) == True for p in config.get(bstack11l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᘝ"), [])])
def bstack11ll1lll1l_opy_(config, bstack111111lll_opy_):
  try:
    bstack11ll1l1111l_opy_ = config.get(bstack11l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᘞ"), False)
    if int(bstack111111lll_opy_) < len(config.get(bstack11l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᘟ"), [])) and config[bstack11l1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘠ")][bstack111111lll_opy_]:
      bstack11ll1l111l1_opy_ = config[bstack11l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᘡ")][bstack111111lll_opy_].get(bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘢ"), None)
    else:
      bstack11ll1l111l1_opy_ = config.get(bstack11l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘣ"), None)
    if bstack11ll1l111l1_opy_ != None:
      bstack11ll1l1111l_opy_ = bstack11ll1l111l1_opy_
    bstack11lll111l11_opy_ = os.getenv(bstack11l1_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᘤ")) is not None and len(os.getenv(bstack11l1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᘥ"))) > 0 and os.getenv(bstack11l1_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᘦ")) != bstack11l1_opy_ (u"ࠨࡰࡸࡰࡱ࠭ᘧ")
    return bstack11ll1l1111l_opy_ and bstack11lll111l11_opy_
  except Exception as error:
    logger.debug(bstack11l1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡸࡨࡶ࡮࡬ࡹࡪࡰࡪࠤࡹ࡮ࡥࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡵࡨࡷࡸ࡯࡯࡯ࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᘨ") + str(error))
  return False
def bstack1ll11ll11_opy_(test_tags):
  bstack1ll1l11l1l1_opy_ = os.getenv(bstack11l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᘩ"))
  if bstack1ll1l11l1l1_opy_ is None:
    return True
  bstack1ll1l11l1l1_opy_ = json.loads(bstack1ll1l11l1l1_opy_)
  try:
    include_tags = bstack1ll1l11l1l1_opy_[bstack11l1_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘪ")] if bstack11l1_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘫ") in bstack1ll1l11l1l1_opy_ and isinstance(bstack1ll1l11l1l1_opy_[bstack11l1_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘬ")], list) else []
    exclude_tags = bstack1ll1l11l1l1_opy_[bstack11l1_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘭ")] if bstack11l1_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘮ") in bstack1ll1l11l1l1_opy_ and isinstance(bstack1ll1l11l1l1_opy_[bstack11l1_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘯ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡸࡤࡰ࡮ࡪࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡨࡲࡶࠥࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡨࡥࡧࡱࡵࡩࠥࡹࡣࡢࡰࡱ࡭ࡳ࡭࠮ࠡࡇࡵࡶࡴࡸࠠ࠻ࠢࠥᘰ") + str(error))
  return False
def bstack11lll111ll1_opy_(config, bstack11ll1ll111l_opy_, bstack11lll11l1l1_opy_, bstack11lll1111ll_opy_):
  bstack11ll1l1l1l1_opy_ = bstack11ll1lll11l_opy_(config)
  bstack11ll1l11lll_opy_ = bstack11lll111111_opy_(config)
  if bstack11ll1l1l1l1_opy_ is None or bstack11ll1l11lll_opy_ is None:
    logger.error(bstack11l1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࡒ࡯ࡳࡴ࡫ࡱ࡫ࠥࡧࡵࡵࡪࡨࡲࡹ࡯ࡣࡢࡶ࡬ࡳࡳࠦࡴࡰ࡭ࡨࡲࠬᘱ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᘲ"), bstack11l1_opy_ (u"࠭ࡻࡾࠩᘳ")))
    data = {
        bstack11l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᘴ"): config[bstack11l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ᘵ")],
        bstack11l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᘶ"): config.get(bstack11l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭ᘷ"), os.path.basename(os.getcwd())),
        bstack11l1_opy_ (u"ࠫࡸࡺࡡࡳࡶࡗ࡭ࡲ࡫ࠧᘸ"): bstack1l1l11lll_opy_(),
        bstack11l1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᘹ"): config.get(bstack11l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᘺ"), bstack11l1_opy_ (u"ࠧࠨᘻ")),
        bstack11l1_opy_ (u"ࠨࡵࡲࡹࡷࡩࡥࠨᘼ"): {
            bstack11l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡓࡧ࡭ࡦࠩᘽ"): bstack11ll1ll111l_opy_,
            bstack11l1_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᘾ"): bstack11lll11l1l1_opy_,
            bstack11l1_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘿ"): __version__,
            bstack11l1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧᙀ"): bstack11l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ᙁ"),
            bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧᙂ"): bstack11l1_opy_ (u"ࠨࡵࡨࡰࡪࡴࡩࡶ࡯ࠪᙃ"),
            bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᙄ"): bstack11lll1111ll_opy_
        },
        bstack11l1_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬᙅ"): settings,
        bstack11l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡈࡵ࡮ࡵࡴࡲࡰࠬᙆ"): bstack11lll11l11l_opy_(),
        bstack11l1_opy_ (u"ࠬࡩࡩࡊࡰࡩࡳࠬᙇ"): bstack1lllll11l_opy_(),
        bstack11l1_opy_ (u"࠭ࡨࡰࡵࡷࡍࡳ࡬࡯ࠨᙈ"): get_host_info(),
        bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩᙉ"): bstack111l1llll_opy_(config)
    }
    headers = {
        bstack11l1_opy_ (u"ࠨࡅࡲࡲࡹ࡫࡮ࡵ࠯ࡗࡽࡵ࡫ࠧᙊ"): bstack11l1_opy_ (u"ࠩࡤࡴࡵࡲࡩࡤࡣࡷ࡭ࡴࡴ࠯࡫ࡵࡲࡲࠬᙋ"),
    }
    config = {
        bstack11l1_opy_ (u"ࠪࡥࡺࡺࡨࠨᙌ"): (bstack11ll1l1l1l1_opy_, bstack11ll1l11lll_opy_),
        bstack11l1_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᙍ"): headers
    }
    response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠬࡖࡏࡔࡖࠪᙎ"), bstack11ll1l1l111_opy_ + bstack11l1_opy_ (u"࠭࠯ࡷ࠴࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠭ᙏ"), data, config)
    bstack11lll11l111_opy_ = response.json()
    if bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᙐ")]:
      parsed = json.loads(os.getenv(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᙑ"), bstack11l1_opy_ (u"ࠩࡾࢁࠬᙒ")))
      parsed[bstack11l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᙓ")] = bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᙔ")][bstack11l1_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᙕ")]
      os.environ[bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᙖ")] = json.dumps(parsed)
      bstack1l11l1l111_opy_.bstack1llll11111_opy_(bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠧࡥࡣࡷࡥࠬᙗ")][bstack11l1_opy_ (u"ࠨࡵࡦࡶ࡮ࡶࡴࡴࠩᙘ")])
      bstack1l11l1l111_opy_.bstack11ll1l11l11_opy_(bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠩࡧࡥࡹࡧࠧᙙ")][bstack11l1_opy_ (u"ࠪࡧࡴࡳ࡭ࡢࡰࡧࡷࠬᙚ")])
      bstack1l11l1l111_opy_.store()
      return bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠫࡩࡧࡴࡢࠩᙛ")][bstack11l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ࡙ࡵ࡫ࡦࡰࠪᙜ")], bstack11lll11l111_opy_[bstack11l1_opy_ (u"࠭ࡤࡢࡶࡤࠫᙝ")][bstack11l1_opy_ (u"ࠧࡪࡦࠪᙞ")]
    else:
      logger.error(bstack11l1_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡶࡺࡴ࡮ࡪࡰࡪࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠩᙟ") + bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙠ")])
      if bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙡ")] == bstack11l1_opy_ (u"ࠫࡎࡴࡶࡢ࡮࡬ࡨࠥࡩ࡯࡯ࡨ࡬࡫ࡺࡸࡡࡵ࡫ࡲࡲࠥࡶࡡࡴࡵࡨࡨ࠳࠭ᙢ"):
        for bstack11ll1l1l11l_opy_ in bstack11lll11l111_opy_[bstack11l1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࡷࠬᙣ")]:
          logger.error(bstack11ll1l1l11l_opy_[bstack11l1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙤ")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠣᙥ") +  str(error))
    return None, None
def bstack11ll1l11ll1_opy_():
  if os.getenv(bstack11l1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᙦ")) is None:
    return {
        bstack11l1_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᙧ"): bstack11l1_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᙨ"),
        bstack11l1_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙩ"): bstack11l1_opy_ (u"ࠬࡈࡵࡪ࡮ࡧࠤࡨࡸࡥࡢࡶ࡬ࡳࡳࠦࡨࡢࡦࠣࡪࡦ࡯࡬ࡦࡦ࠱ࠫᙪ")
    }
  data = {bstack11l1_opy_ (u"࠭ࡥ࡯ࡦࡗ࡭ࡲ࡫ࠧᙫ"): bstack1l1l11lll_opy_()}
  headers = {
      bstack11l1_opy_ (u"ࠧࡂࡷࡷ࡬ࡴࡸࡩࡻࡣࡷ࡭ࡴࡴࠧᙬ"): bstack11l1_opy_ (u"ࠨࡄࡨࡥࡷ࡫ࡲࠡࠩ᙭") + os.getenv(bstack11l1_opy_ (u"ࠤࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠢ᙮")),
      bstack11l1_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᙯ"): bstack11l1_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᙰ")
  }
  response = bstack1l11l1l1l1_opy_(bstack11l1_opy_ (u"ࠬࡖࡕࡕࠩᙱ"), bstack11ll1l1l111_opy_ + bstack11l1_opy_ (u"࠭࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵ࠲ࡷࡹࡵࡰࠨᙲ"), data, { bstack11l1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᙳ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1_opy_ (u"ࠣࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤ࡙࡫ࡳࡵࠢࡕࡹࡳࠦ࡭ࡢࡴ࡮ࡩࡩࠦࡡࡴࠢࡦࡳࡲࡶ࡬ࡦࡶࡨࡨࠥࡧࡴࠡࠤᙴ") + bstack111l1ll11l_opy_().isoformat() + bstack11l1_opy_ (u"ࠩ࡝ࠫᙵ"))
      return {bstack11l1_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᙶ"): bstack11l1_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᙷ"), bstack11l1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙸ"): bstack11l1_opy_ (u"࠭ࠧᙹ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡰࡥࡷࡱࡩ࡯ࡩࠣࡧࡴࡳࡰ࡭ࡧࡷ࡭ࡴࡴࠠࡰࡨࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮࠻ࠢࠥᙺ") + str(error))
    return {
        bstack11l1_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙻ"): bstack11l1_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᙼ"),
        bstack11l1_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙽ"): str(error)
    }
def bstack11lll11111l_opy_(bstack11ll1lll1l1_opy_):
    return re.match(bstack11l1_opy_ (u"ࡶࠬࡤ࡜ࡥ࠭ࠫࡠ࠳ࡢࡤࠬࠫࡂࠨࠬᙾ"), bstack11ll1lll1l1_opy_.strip()) is not None
def bstack1l1l11ll1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11ll1l1ll1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11ll1l1ll1l_opy_ = desired_capabilities
        else:
          bstack11ll1l1ll1l_opy_ = {}
        bstack1ll11ll1l1l_opy_ = (bstack11ll1l1ll1l_opy_.get(bstack11l1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᙿ"), bstack11l1_opy_ (u"࠭ࠧ ")).lower() or caps.get(bstack11l1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᚁ"), bstack11l1_opy_ (u"ࠨࠩᚂ")).lower())
        if bstack1ll11ll1l1l_opy_ == bstack11l1_opy_ (u"ࠩ࡬ࡳࡸ࠭ᚃ"):
            return True
        if bstack1ll11ll1l1l_opy_ == bstack11l1_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᚄ"):
            bstack1ll11llll11_opy_ = str(float(caps.get(bstack11l1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᚅ")) or bstack11ll1l1ll1l_opy_.get(bstack11l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚆ"), {}).get(bstack11l1_opy_ (u"࠭࡯ࡴࡘࡨࡶࡸ࡯࡯࡯ࠩᚇ"),bstack11l1_opy_ (u"ࠧࠨᚈ"))))
            if bstack1ll11ll1l1l_opy_ == bstack11l1_opy_ (u"ࠨࡣࡱࡨࡷࡵࡩࡥࠩᚉ") and int(bstack1ll11llll11_opy_.split(bstack11l1_opy_ (u"ࠩ࠱ࠫᚊ"))[0]) < float(bstack11ll1ll11ll_opy_):
                logger.warning(str(bstack11ll1llllll_opy_))
                return False
            return True
        bstack1ll1l11l1ll_opy_ = caps.get(bstack11l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᚋ"), {}).get(bstack11l1_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࡒࡦࡳࡥࠨᚌ"), caps.get(bstack11l1_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࠬᚍ"), bstack11l1_opy_ (u"࠭ࠧᚎ")))
        if bstack1ll1l11l1ll_opy_:
            logger.warning(bstack11l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡅࡧࡶ࡯ࡹࡵࡰࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᚏ"))
            return False
        browser = caps.get(bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡐࡤࡱࡪ࠭ᚐ"), bstack11l1_opy_ (u"ࠩࠪᚑ")).lower() or bstack11ll1l1ll1l_opy_.get(bstack11l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᚒ"), bstack11l1_opy_ (u"ࠫࠬᚓ")).lower()
        if browser != bstack11l1_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬᚔ"):
            logger.warning(bstack11l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤᚕ"))
            return False
        browser_version = caps.get(bstack11l1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚖ")) or caps.get(bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᚗ")) or bstack11ll1l1ll1l_opy_.get(bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᚘ")) or bstack11ll1l1ll1l_opy_.get(bstack11l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᚙ"), {}).get(bstack11l1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚚ")) or bstack11ll1l1ll1l_opy_.get(bstack11l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭᚛"), {}).get(bstack11l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ᚜"))
        bstack1ll111l1ll1_opy_ = bstack11ll1llll1l_opy_.bstack1ll11ll11l1_opy_
        bstack11lll111lll_opy_ = False
        if config is not None:
          bstack11lll111lll_opy_ = bstack11l1_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᚝") in config and str(config[bstack11l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᚞")]).lower() != bstack11l1_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨ᚟")
        if os.environ.get(bstack11l1_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᚠ"), bstack11l1_opy_ (u"ࠫࠬᚡ")).lower() == bstack11l1_opy_ (u"ࠬࡺࡲࡶࡧࠪᚢ") or bstack11lll111lll_opy_:
          bstack1ll111l1ll1_opy_ = bstack11ll1llll1l_opy_.bstack1ll1l11ll11_opy_
        if browser_version and browser_version != bstack11l1_opy_ (u"࠭࡬ࡢࡶࡨࡷࡹ࠭ᚣ") and int(browser_version.split(bstack11l1_opy_ (u"ࠧ࠯ࠩᚤ"))[0]) <= bstack1ll111l1ll1_opy_:
          logger.warning(bstack1lll1lll111_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࠢࡹࡩࡷࡹࡩࡰࡰࠣ࡫ࡷ࡫ࡡࡵࡧࡵࠤࡹ࡮ࡡ࡯ࠢࡾࡱ࡮ࡴ࡟ࡢ࠳࠴ࡽࡤࡹࡵࡱࡲࡲࡶࡹ࡫ࡤࡠࡥ࡫ࡶࡴࡳࡥࡠࡸࡨࡶࡸ࡯࡯࡯ࡿ࠱ࠫᚥ"))
          return False
        if not options:
          bstack1ll111ll111_opy_ = caps.get(bstack11l1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚦ")) or bstack11ll1l1ll1l_opy_.get(bstack11l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᚧ"), {})
          if bstack11l1_opy_ (u"ࠫ࠲࠳ࡨࡦࡣࡧࡰࡪࡹࡳࠨᚨ") in bstack1ll111ll111_opy_.get(bstack11l1_opy_ (u"ࠬࡧࡲࡨࡵࠪᚩ"), []):
              logger.warning(bstack11l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣᚪ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡶࡢ࡮࡬ࡨࡦࡺࡥࠡࡣ࠴࠵ࡾࠦࡳࡶࡲࡳࡳࡷࡺࠠ࠻ࠤᚫ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1llll11ll11_opy_ = config.get(bstack11l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᚬ"), {})
    bstack1llll11ll11_opy_[bstack11l1_opy_ (u"ࠩࡤࡹࡹ࡮ࡔࡰ࡭ࡨࡲࠬᚭ")] = os.getenv(bstack11l1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᚮ"))
    bstack11ll1l1ll11_opy_ = json.loads(os.getenv(bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᚯ"), bstack11l1_opy_ (u"ࠬࢁࡽࠨᚰ"))).get(bstack11l1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚱ"))
    if not config[bstack11l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡖࡲࡰࡦࡸࡧࡹࡓࡡࡱࠩᚲ")].get(bstack11l1_opy_ (u"ࠣࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠢᚳ")):
      if bstack11l1_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚴ") in caps:
        caps[bstack11l1_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᚵ")][bstack11l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᚶ")] = bstack1llll11ll11_opy_
        caps[bstack11l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚷ")][bstack11l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚸ")][bstack11l1_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚹ")] = bstack11ll1l1ll11_opy_
      else:
        caps[bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᚺ")] = bstack1llll11ll11_opy_
        caps[bstack11l1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᚻ")][bstack11l1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚼ")] = bstack11ll1l1ll11_opy_
  except Exception as error:
    logger.debug(bstack11l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡳࡦࡶࡷ࡭ࡳ࡭ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵ࠱ࠤࡊࡸࡲࡰࡴ࠽ࠤࠧᚽ") +  str(error))
def bstack1ll1lll1ll_opy_(driver, bstack11ll1l11l1l_opy_):
  try:
    setattr(driver, bstack11l1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯ࡆ࠷࠱ࡺࡕ࡫ࡳࡺࡲࡤࡔࡥࡤࡲࠬᚾ"), True)
    session = driver.session_id
    if session:
      bstack11ll1lll1ll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1lll1ll_opy_ = False
      bstack11ll1lll1ll_opy_ = url.scheme in [bstack11l1_opy_ (u"ࠨࡨࡵࡶࡳࠦᚿ"), bstack11l1_opy_ (u"ࠢࡩࡶࡷࡴࡸࠨᛀ")]
      if bstack11ll1lll1ll_opy_:
        if bstack11ll1l11l1l_opy_:
          logger.info(bstack11l1_opy_ (u"ࠣࡕࡨࡸࡺࡶࠠࡧࡱࡵࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡹ࡫ࡳࡵ࡫ࡱ࡫ࠥ࡮ࡡࡴࠢࡶࡸࡦࡸࡴࡦࡦ࠱ࠤࡆࡻࡴࡰ࡯ࡤࡸࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡨࡼࡪࡩࡵࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡦࡪ࡭ࡩ࡯ࠢࡰࡳࡲ࡫࡮ࡵࡣࡵ࡭ࡱࡿ࠮ࠣᛁ"))
      return bstack11ll1l11l1l_opy_
  except Exception as e:
    logger.error(bstack11l1_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡵࡷࡥࡷࡺࡩ࡯ࡩࠣࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡥࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡴࡥࡤࡲࠥ࡬࡯ࡳࠢࡷ࡬࡮ࡹࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧᛂ") + str(e))
    return False
def bstack1ll1l1lll1_opy_(driver, name, path):
  try:
    bstack1ll11l11lll_opy_ = {
        bstack11l1_opy_ (u"ࠪࡸ࡭࡚ࡥࡴࡶࡕࡹࡳ࡛ࡵࡪࡦࠪᛃ"): threading.current_thread().current_test_uuid,
        bstack11l1_opy_ (u"ࠫࡹ࡮ࡂࡶ࡫࡯ࡨ࡚ࡻࡩࡥࠩᛄ"): os.environ.get(bstack11l1_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤ࡛ࡕࡊࡆࠪᛅ"), bstack11l1_opy_ (u"࠭ࠧᛆ")),
        bstack11l1_opy_ (u"ࠧࡵࡪࡍࡻࡹ࡚࡯࡬ࡧࡱࠫᛇ"): os.environ.get(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡌ࡚ࡘࠬᛈ"), bstack11l1_opy_ (u"ࠩࠪᛉ"))
    }
    bstack1ll111llll1_opy_ = bstack1ll111lll1_opy_.bstack1ll11lll11l_opy_(EVENTS.bstack1llll111l_opy_.value)
    logger.debug(bstack11l1_opy_ (u"ࠪࡔࡪࡸࡦࡰࡴࡰ࡭ࡳ࡭ࠠࡴࡥࡤࡲࠥࡨࡥࡧࡱࡵࡩࠥࡹࡡࡷ࡫ࡱ࡫ࠥࡸࡥࡴࡷ࡯ࡸࡸ࠭ᛊ"))
    try:
      if (bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠫ࡮ࡹࡁࡱࡲࡄ࠵࠶ࡿࡔࡦࡵࡷࠫᛋ"), None) and bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠬࡧࡰࡱࡃ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧᛌ"), None)):
        scripts = {bstack11l1_opy_ (u"࠭ࡳࡤࡣࡱࠫᛍ"): bstack1l11l1l111_opy_.perform_scan}
        bstack11ll1ll1l11_opy_ = json.loads(scripts[bstack11l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᛎ")].replace(bstack11l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᛏ"), bstack11l1_opy_ (u"ࠤࠥᛐ")))
        bstack11ll1ll1l11_opy_[bstack11l1_opy_ (u"ࠪࡥࡷ࡭ࡵ࡮ࡧࡱࡸࡸ࠭ᛑ")][bstack11l1_opy_ (u"ࠫࡲ࡫ࡴࡩࡱࡧࠫᛒ")] = None
        scripts[bstack11l1_opy_ (u"ࠧࡹࡣࡢࡰࠥᛓ")] = bstack11l1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᛔ") + json.dumps(bstack11ll1ll1l11_opy_)
        bstack1l11l1l111_opy_.bstack1llll11111_opy_(scripts)
        bstack1l11l1l111_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l1l111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l1l111_opy_.perform_scan, {bstack11l1_opy_ (u"ࠢ࡮ࡧࡷ࡬ࡴࡪࠢᛕ"): name}))
      bstack1ll111lll1_opy_.end(EVENTS.bstack1llll111l_opy_.value, bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᛖ"), bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᛗ"), True, None)
    except Exception as error:
      bstack1ll111lll1_opy_.end(EVENTS.bstack1llll111l_opy_.value, bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᛘ"), bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᛙ"), False, str(error))
    bstack1ll111llll1_opy_ = bstack1ll111lll1_opy_.bstack11ll1l1lll1_opy_(EVENTS.bstack1ll111l1l11_opy_.value)
    bstack1ll111lll1_opy_.mark(bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᛚ"))
    try:
      if (bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"࠭ࡩࡴࡃࡳࡴࡆ࠷࠱ࡺࡖࡨࡷࡹ࠭ᛛ"), None) and bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠧࡢࡲࡳࡅ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩᛜ"), None)):
        scripts = {bstack11l1_opy_ (u"ࠨࡵࡦࡥࡳ࠭ᛝ"): bstack1l11l1l111_opy_.perform_scan}
        bstack11ll1ll1l11_opy_ = json.loads(scripts[bstack11l1_opy_ (u"ࠤࡶࡧࡦࡴࠢᛞ")].replace(bstack11l1_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᛟ"), bstack11l1_opy_ (u"ࠦࠧᛠ")))
        bstack11ll1ll1l11_opy_[bstack11l1_opy_ (u"ࠬࡧࡲࡨࡷࡰࡩࡳࡺࡳࠨᛡ")][bstack11l1_opy_ (u"࠭࡭ࡦࡶ࡫ࡳࡩ࠭ᛢ")] = None
        scripts[bstack11l1_opy_ (u"ࠢࡴࡥࡤࡲࠧᛣ")] = bstack11l1_opy_ (u"ࠣࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࡟ࡦࡺࡨࡧࡺࡺ࡯ࡳ࠼ࠣࠦᛤ") + json.dumps(bstack11ll1ll1l11_opy_)
        bstack1l11l1l111_opy_.bstack1llll11111_opy_(scripts)
        bstack1l11l1l111_opy_.store()
        logger.debug(driver.execute_script(bstack1l11l1l111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l11l1l111_opy_.bstack11ll1ll1111_opy_, bstack1ll11l11lll_opy_))
      bstack1ll111lll1_opy_.end(bstack1ll111llll1_opy_, bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛥ"), bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᛦ"),True, None)
    except Exception as error:
      bstack1ll111lll1_opy_.end(bstack1ll111llll1_opy_, bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᛧ"), bstack1ll111llll1_opy_ + bstack11l1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᛨ"),False, str(error))
    logger.info(bstack11l1_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡴࡦࡵࡷ࡭ࡳ࡭ࠠࡧࡱࡵࠤࡹ࡮ࡩࡴࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡮ࡡࡴࠢࡨࡲࡩ࡫ࡤ࠯ࠤᛩ"))
  except Exception as bstack1ll1l111ll1_opy_:
    logger.error(bstack11l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡳࡧࡶࡹࡱࡺࡳࠡࡥࡲࡹࡱࡪࠠ࡯ࡱࡷࠤࡧ࡫ࠠࡱࡴࡲࡧࡪࡹࡳࡦࡦࠣࡪࡴࡸࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᛪ") + str(path) + bstack11l1_opy_ (u"ࠣࠢࡈࡶࡷࡵࡲࠡ࠼ࠥ᛫") + str(bstack1ll1l111ll1_opy_))
def bstack11ll1l1l1ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11l1_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ᛬")) and str(caps.get(bstack11l1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ᛭"))).lower() == bstack11l1_opy_ (u"ࠦࡦࡴࡤࡳࡱ࡬ࡨࠧᛮ"):
        bstack1ll11llll11_opy_ = caps.get(bstack11l1_opy_ (u"ࠧࡧࡰࡱ࡫ࡸࡱ࠿ࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᛯ")) or caps.get(bstack11l1_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣᛰ"))
        if bstack1ll11llll11_opy_ and int(str(bstack1ll11llll11_opy_)) < bstack11ll1ll11ll_opy_:
            return False
    return True
def bstack11l111111_opy_(config):
  if bstack11l1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛱ") in config:
        return config[bstack11l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᛲ")]
  for platform in config.get(bstack11l1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᛳ"), []):
      if bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᛴ") in platform:
          return platform[bstack11l1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛵ")]
  return None
def bstack11l11l1ll_opy_(bstack11l1111ll_opy_):
  try:
    browser_name = bstack11l1111ll_opy_[bstack11l1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᛶ")]
    browser_version = bstack11l1111ll_opy_[bstack11l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᛷ")]
    chrome_options = bstack11l1111ll_opy_[bstack11l1_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫࡟ࡰࡲࡷ࡭ࡴࡴࡳࠨᛸ")]
    try:
        bstack11lll1111l1_opy_ = int(browser_version.split(bstack11l1_opy_ (u"ࠨ࠰ࠪ᛹"))[0])
    except ValueError as e:
        logger.error(bstack11l1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡱࡱࡺࡪࡸࡴࡪࡰࡪࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠨ᛺") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11l1_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࠪ᛻")):
        logger.warning(bstack11l1_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢ᛼"))
        return False
    if bstack11lll1111l1_opy_ < bstack11ll1llll1l_opy_.bstack1ll1l11ll11_opy_:
        logger.warning(bstack1lll1lll111_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡵࡩࡶࡻࡩࡳࡧࡶࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࢁࡃࡐࡐࡖࡘࡆࡔࡔࡔ࠰ࡐࡍࡓࡏࡍࡖࡏࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘ࡛ࡐࡑࡑࡕࡘࡊࡊ࡟ࡄࡊࡕࡓࡒࡋ࡟ࡗࡇࡕࡗࡎࡕࡎࡾࠢࡲࡶࠥ࡮ࡩࡨࡪࡨࡶ࠳࠭᛽"))
        return False
    if chrome_options and any(bstack11l1_opy_ (u"࠭࠭࠮ࡪࡨࡥࡩࡲࡥࡴࡵࠪ᛾") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11l1_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤ᛿"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11l1_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡪࡰࠣࡧ࡭࡫ࡣ࡬࡫ࡱ࡫ࠥࡶ࡬ࡢࡶࡩࡳࡷࡳࠠࡴࡷࡳࡴࡴࡸࡴࠡࡨࡲࡶࠥࡲ࡯ࡤࡣ࡯ࠤࡈ࡮ࡲࡰ࡯ࡨ࠾ࠥࠨᜀ") + str(e))
    return False
def bstack1ll1l1111l_opy_(bstack1ll1111ll1_opy_, config):
    try:
      bstack1ll11l1l1ll_opy_ = bstack11l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᜁ") in config and config[bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᜂ")] == True
      bstack11lll111lll_opy_ = bstack11l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᜃ") in config and str(config[bstack11l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᜄ")]).lower() != bstack11l1_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬᜅ")
      if not (bstack1ll11l1l1ll_opy_ and (not bstack111l1llll_opy_(config) or bstack11lll111lll_opy_)):
        return bstack1ll1111ll1_opy_
      bstack11ll1l1llll_opy_ = bstack1l11l1l111_opy_.bstack11ll1lll111_opy_
      if bstack11ll1l1llll_opy_ is None:
        logger.debug(bstack11l1_opy_ (u"ࠢࡈࡱࡲ࡫ࡱ࡫ࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳࠡࡣࡵࡩࠥࡔ࡯࡯ࡧࠥᜆ"))
        return bstack1ll1111ll1_opy_
      bstack11ll1l11111_opy_ = int(str(bstack11ll1ll1lll_opy_()).split(bstack11l1_opy_ (u"ࠨ࠰ࠪᜇ"))[0])
      logger.debug(bstack11l1_opy_ (u"ࠤࡖࡩࡱ࡫࡮ࡪࡷࡰࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠥࡪࡥࡵࡧࡦࡸࡪࡪ࠺ࠡࠤᜈ") + str(bstack11ll1l11111_opy_) + bstack11l1_opy_ (u"ࠥࠦᜉ"))
      if bstack11ll1l11111_opy_ == 3 and isinstance(bstack1ll1111ll1_opy_, dict) and bstack11l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᜊ") in bstack1ll1111ll1_opy_ and bstack11ll1l1llll_opy_ is not None:
        if bstack11l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᜋ") not in bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜌ")]:
          bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜍ")][bstack11l1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜎ")] = {}
        if bstack11l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᜏ") in bstack11ll1l1llll_opy_:
          if bstack11l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᜐ") not in bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᜑ")][bstack11l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᜒ")]:
            bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜓ")][bstack11l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷ᜔ࠬ")][bstack11l1_opy_ (u"ࠨࡣࡵ࡫ࡸ᜕࠭")] = []
          for arg in bstack11ll1l1llll_opy_[bstack11l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᜖")]:
            if arg not in bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᜗")][bstack11l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᜘")][bstack11l1_opy_ (u"ࠬࡧࡲࡨࡵࠪ᜙")]:
              bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᜚")][bstack11l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᜛")][bstack11l1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᜜")].append(arg)
        if bstack11l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᜝") in bstack11ll1l1llll_opy_:
          if bstack11l1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᜞") not in bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᜟ")][bstack11l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᜠ")]:
            bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜡ")][bstack11l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᜢ")][bstack11l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᜣ")] = []
          for ext in bstack11ll1l1llll_opy_[bstack11l1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᜤ")]:
            if ext not in bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜥ")][bstack11l1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜦ")][bstack11l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᜧ")]:
              bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜨ")][bstack11l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᜩ")][bstack11l1_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᜪ")].append(ext)
        if bstack11l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᜫ") in bstack11ll1l1llll_opy_:
          if bstack11l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᜬ") not in bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᜭ")][bstack11l1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᜮ")]:
            bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜯ")][bstack11l1_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᜰ")][bstack11l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᜱ")] = {}
          bstack11ll1ll1ll1_opy_(bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᜲ")][bstack11l1_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᜳ")][bstack11l1_opy_ (u"ࠫࡵࡸࡥࡧࡵ᜴ࠪ")],
                    bstack11ll1l1llll_opy_[bstack11l1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ᜵")])
        os.environ[bstack11l1_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫ᜶")] = bstack11l1_opy_ (u"ࠧࡵࡴࡸࡩࠬ᜷")
        return bstack1ll1111ll1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll1111ll1_opy_, ChromeOptions):
          chrome_options = bstack1ll1111ll1_opy_
        elif isinstance(bstack1ll1111ll1_opy_, dict):
          for value in bstack1ll1111ll1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll1111ll1_opy_, dict):
            bstack1ll1111ll1_opy_[bstack11l1_opy_ (u"ࠨࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᜸")] = chrome_options
          else:
            bstack1ll1111ll1_opy_ = chrome_options
        if bstack11ll1l1llll_opy_ is not None:
          if bstack11l1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᜹") in bstack11ll1l1llll_opy_:
                bstack11ll1lllll1_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1l1llll_opy_[bstack11l1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ᜺")]
                for arg in new_args:
                    if arg not in bstack11ll1lllll1_opy_:
                        chrome_options.add_argument(arg)
          if bstack11l1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᜻") in bstack11ll1l1llll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11l1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᜼"), [])
                bstack11ll1ll1l1l_opy_ = bstack11ll1l1llll_opy_[bstack11l1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ᜽")]
                for extension in bstack11ll1ll1l1l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11l1_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᜾") in bstack11ll1l1llll_opy_:
                bstack11ll1llll11_opy_ = chrome_options.experimental_options.get(bstack11l1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᜿"), {})
                bstack11lll111l1l_opy_ = bstack11ll1l1llll_opy_[bstack11l1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᝀ")]
                bstack11ll1ll1ll1_opy_(bstack11ll1llll11_opy_, bstack11lll111l1l_opy_)
                chrome_options.add_experimental_option(bstack11l1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᝁ"), bstack11ll1llll11_opy_)
        os.environ[bstack11l1_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩᝂ")] = bstack11l1_opy_ (u"ࠬࡺࡲࡶࡧࠪᝃ")
        return bstack1ll1111ll1_opy_
    except Exception as e:
      logger.error(bstack11l1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡦࡪࡤࡪࡰࡪࠤࡳࡵ࡮࠮ࡄࡖࠤ࡮ࡴࡦࡳࡣࠣࡥ࠶࠷ࡹࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴ࠼ࠣࠦᝄ") + str(e))
      return bstack1ll1111ll1_opy_