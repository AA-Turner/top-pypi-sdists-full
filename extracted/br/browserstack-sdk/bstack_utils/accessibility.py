# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll1ll1ll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1ll11l1_opy_ as bstack11ll1l11l11_opy_, EVENTS
from bstack_utils.bstack1l111l111_opy_ import bstack1l111l111_opy_
from bstack_utils.helper import bstack1lll111111_opy_, bstack111l1111ll_opy_, bstack1l11l11ll_opy_, bstack11ll1l1111l_opy_, \
  bstack11ll1l1l11l_opy_, bstack1111l1l1l_opy_, get_host_info, bstack11lll111ll1_opy_, bstack11llll1l1l_opy_, bstack111l1lll11_opy_, bstack11ll1ll1l11_opy_, bstack11lll1111l1_opy_, bstack11ll1111ll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1ll11l1ll_opy_ import get_logger
from bstack_utils.bstack11l111111_opy_ import bstack1lll11lll1l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack11l111111_opy_ = bstack1lll11lll1l_opy_()
@bstack111l1lll11_opy_(class_method=False)
def _11ll1lll1l1_opy_(driver, bstack1111l1llll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstackl_opy_ (u"ࠫࡴࡹ࡟࡯ࡣࡰࡩࠬᘎ"): caps.get(bstackl_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠫᘏ"), None),
        bstackl_opy_ (u"࠭࡯ࡴࡡࡹࡩࡷࡹࡩࡰࡰࠪᘐ"): bstack1111l1llll_opy_.get(bstackl_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪᘑ"), None),
        bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧᘒ"): caps.get(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᘓ"), None),
        bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᘔ"): caps.get(bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘕ"), None)
    }
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤ࡫࡫ࡴࡤࡪ࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡦࡨࡸࡦ࡯࡬ࡴࠢࡺ࡭ࡹ࡮ࠠࡦࡴࡵࡳࡷࠦ࠺ࠡࠩᘖ") + str(error))
  return response
def on():
    if os.environ.get(bstackl_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᘗ"), None) is None or os.environ[bstackl_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᘘ")] == bstackl_opy_ (u"ࠣࡰࡸࡰࡱࠨᘙ"):
        return False
    return True
def bstack1llll111l_opy_(config):
  return config.get(bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘚ"), False) or any([p.get(bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘛ"), False) == True for p in config.get(bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᘜ"), [])])
def bstack1l1111l1l_opy_(config, bstack1ll11l11l_opy_):
  try:
    bstack11lll111l11_opy_ = config.get(bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘝ"), False)
    if int(bstack1ll11l11l_opy_) < len(config.get(bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘞ"), [])) and config[bstackl_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᘟ")][bstack1ll11l11l_opy_]:
      bstack11ll1l11ll1_opy_ = config[bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘠ")][bstack1ll11l11l_opy_].get(bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘡ"), None)
    else:
      bstack11ll1l11ll1_opy_ = config.get(bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘢ"), None)
    if bstack11ll1l11ll1_opy_ != None:
      bstack11lll111l11_opy_ = bstack11ll1l11ll1_opy_
    bstack11ll11lll1l_opy_ = os.getenv(bstackl_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᘣ")) is not None and len(os.getenv(bstackl_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᘤ"))) > 0 and os.getenv(bstackl_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᘥ")) != bstackl_opy_ (u"ࠧ࡯ࡷ࡯ࡰࠬᘦ")
    return bstack11lll111l11_opy_ and bstack11ll11lll1l_opy_
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡧࡵ࡭࡫ࡿࡩ࡯ࡩࠣࡸ࡭࡫ࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡧࡶࡷ࡮ࡵ࡮ࠡࡹ࡬ࡸ࡭ࠦࡥࡳࡴࡲࡶࠥࡀࠠࠨᘧ") + str(error))
  return False
def bstack1l111lll_opy_(test_tags):
  bstack1ll11l1l111_opy_ = os.getenv(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᘨ"))
  if bstack1ll11l1l111_opy_ is None:
    return True
  bstack1ll11l1l111_opy_ = json.loads(bstack1ll11l1l111_opy_)
  try:
    include_tags = bstack1ll11l1l111_opy_[bstackl_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘩ")] if bstackl_opy_ (u"ࠫ࡮ࡴࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘪ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstackl_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘫ")], list) else []
    exclude_tags = bstack1ll11l1l111_opy_[bstackl_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᘬ")] if bstackl_opy_ (u"ࠧࡦࡺࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘭ") in bstack1ll11l1l111_opy_ and isinstance(bstack1ll11l1l111_opy_[bstackl_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘮ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡷࡣ࡯࡭ࡩࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫ࠠࡧࡱࡵࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡩࡡ࡯ࡰ࡬ࡲ࡬࠴ࠠࡆࡴࡵࡳࡷࠦ࠺ࠡࠤᘯ") + str(error))
  return False
def bstack11ll1ll111l_opy_(config, bstack11ll1l1l1l1_opy_, bstack11ll1l11111_opy_, bstack11ll1llllll_opy_):
  bstack11ll1lllll1_opy_ = bstack11ll1l1111l_opy_(config)
  bstack11ll1llll11_opy_ = bstack11ll1l1l11l_opy_(config)
  if bstack11ll1lllll1_opy_ is None or bstack11ll1llll11_opy_ is None:
    logger.error(bstackl_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࡑ࡮ࡹࡳࡪࡰࡪࠤࡦࡻࡴࡩࡧࡱࡸ࡮ࡩࡡࡵ࡫ࡲࡲࠥࡺ࡯࡬ࡧࡱࠫᘰ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᘱ"), bstackl_opy_ (u"ࠬࢁࡽࠨᘲ")))
    data = {
        bstackl_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫᘳ"): config[bstackl_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡏࡣࡰࡩࠬᘴ")],
        bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫᘵ"): config.get(bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬᘶ"), os.path.basename(os.getcwd())),
        bstackl_opy_ (u"ࠪࡷࡹࡧࡲࡵࡖ࡬ࡱࡪ࠭ᘷ"): bstack1lll111111_opy_(),
        bstackl_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩᘸ"): config.get(bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨᘹ"), bstackl_opy_ (u"࠭ࠧᘺ")),
        bstackl_opy_ (u"ࠧࡴࡱࡸࡶࡨ࡫ࠧᘻ"): {
            bstackl_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨᘼ"): bstack11ll1l1l1l1_opy_,
            bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᘽ"): bstack11ll1l11111_opy_,
            bstackl_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᘾ"): __version__,
            bstackl_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭ᘿ"): bstackl_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬᙀ"),
            bstackl_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭ᙁ"): bstackl_opy_ (u"ࠧࡴࡧ࡯ࡩࡳ࡯ࡵ࡮ࠩᙂ"),
            bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᙃ"): bstack11ll1llllll_opy_
        },
        bstackl_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫᙄ"): settings,
        bstackl_opy_ (u"ࠪࡺࡪࡸࡳࡪࡱࡱࡇࡴࡴࡴࡳࡱ࡯ࠫᙅ"): bstack11lll111ll1_opy_(),
        bstackl_opy_ (u"ࠫࡨ࡯ࡉ࡯ࡨࡲࠫᙆ"): bstack1111l1l1l_opy_(),
        bstackl_opy_ (u"ࠬ࡮࡯ࡴࡶࡌࡲ࡫ࡵࠧᙇ"): get_host_info(),
        bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨᙈ"): bstack1l11l11ll_opy_(config)
    }
    headers = {
        bstackl_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᙉ"): bstackl_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᙊ"),
    }
    config = {
        bstackl_opy_ (u"ࠩࡤࡹࡹ࡮ࠧᙋ"): (bstack11ll1lllll1_opy_, bstack11ll1llll11_opy_),
        bstackl_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᙌ"): headers
    }
    response = bstack11llll1l1l_opy_(bstackl_opy_ (u"ࠫࡕࡕࡓࡕࠩᙍ"), bstack11ll1l11l11_opy_ + bstackl_opy_ (u"ࠬ࠵ࡶ࠳࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷࠬᙎ"), data, config)
    bstack11lll1111ll_opy_ = response.json()
    if bstack11lll1111ll_opy_[bstackl_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᙏ")]:
      parsed = json.loads(os.getenv(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᙐ"), bstackl_opy_ (u"ࠨࡽࢀࠫᙑ")))
      parsed[bstackl_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᙒ")] = bstack11lll1111ll_opy_[bstackl_opy_ (u"ࠪࡨࡦࡺࡡࠨᙓ")][bstackl_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᙔ")]
      os.environ[bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᙕ")] = json.dumps(parsed)
      bstack1l111l111_opy_.bstack111l1ll11_opy_(bstack11lll1111ll_opy_[bstackl_opy_ (u"࠭ࡤࡢࡶࡤࠫᙖ")][bstackl_opy_ (u"ࠧࡴࡥࡵ࡭ࡵࡺࡳࠨᙗ")])
      bstack1l111l111_opy_.bstack11ll1lll111_opy_(bstack11lll1111ll_opy_[bstackl_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᙘ")][bstackl_opy_ (u"ࠩࡦࡳࡲࡳࡡ࡯ࡦࡶࠫᙙ")])
      bstack1l111l111_opy_.store()
      return bstack11lll1111ll_opy_[bstackl_opy_ (u"ࠪࡨࡦࡺࡡࠨᙚ")][bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡘࡴࡱࡥ࡯ࠩᙛ")], bstack11lll1111ll_opy_[bstackl_opy_ (u"ࠬࡪࡡࡵࡣࠪᙜ")][bstackl_opy_ (u"࠭ࡩࡥࠩᙝ")]
    else:
      logger.error(bstackl_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡵࡹࡳࡴࡩ࡯ࡩࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࠨᙞ") + bstack11lll1111ll_opy_[bstackl_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙟ")])
      if bstack11lll1111ll_opy_[bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙠ")] == bstackl_opy_ (u"ࠪࡍࡳࡼࡡ࡭࡫ࡧࠤࡨࡵ࡮ࡧ࡫ࡪࡹࡷࡧࡴࡪࡱࡱࠤࡵࡧࡳࡴࡧࡧ࠲ࠬᙡ"):
        for bstack11ll1l1l111_opy_ in bstack11lll1111ll_opy_[bstackl_opy_ (u"ࠫࡪࡸࡲࡰࡴࡶࠫᙢ")]:
          logger.error(bstack11ll1l1l111_opy_[bstackl_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙣ")])
      return None, None
  except Exception as error:
    logger.error(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࠢᙤ") +  str(error))
    return None, None
def bstack11ll1l1lll1_opy_():
  if os.getenv(bstackl_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᙥ")) is None:
    return {
        bstackl_opy_ (u"ࠨࡵࡷࡥࡹࡻࡳࠨᙦ"): bstackl_opy_ (u"ࠩࡨࡶࡷࡵࡲࠨᙧ"),
        bstackl_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᙨ"): bstackl_opy_ (u"ࠫࡇࡻࡩ࡭ࡦࠣࡧࡷ࡫ࡡࡵ࡫ࡲࡲࠥ࡮ࡡࡥࠢࡩࡥ࡮ࡲࡥࡥ࠰ࠪᙩ")
    }
  data = {bstackl_opy_ (u"ࠬ࡫࡮ࡥࡖ࡬ࡱࡪ࠭ᙪ"): bstack1lll111111_opy_()}
  headers = {
      bstackl_opy_ (u"࠭ࡁࡶࡶ࡫ࡳࡷ࡯ࡺࡢࡶ࡬ࡳࡳ࠭ᙫ"): bstackl_opy_ (u"ࠧࡃࡧࡤࡶࡪࡸࠠࠨᙬ") + os.getenv(bstackl_opy_ (u"ࠣࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙ࠨ᙭")),
      bstackl_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨ᙮"): bstackl_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᙯ")
  }
  response = bstack11llll1l1l_opy_(bstackl_opy_ (u"ࠫࡕ࡛ࡔࠨᙰ"), bstack11ll1l11l11_opy_ + bstackl_opy_ (u"ࠬ࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴ࠱ࡶࡸࡴࡶࠧᙱ"), data, { bstackl_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᙲ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstackl_opy_ (u"ࠢࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲࠥࡳࡡࡳ࡭ࡨࡨࠥࡧࡳࠡࡥࡲࡱࡵࡲࡥࡵࡧࡧࠤࡦࡺࠠࠣᙳ") + bstack111l1111ll_opy_().isoformat() + bstackl_opy_ (u"ࠨ࡜ࠪᙴ"))
      return {bstackl_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᙵ"): bstackl_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᙶ"), bstackl_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᙷ"): bstackl_opy_ (u"ࠬ࠭ᙸ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡ࡯ࡤࡶࡰ࡯࡮ࡨࠢࡦࡳࡲࡶ࡬ࡦࡶ࡬ࡳࡳࠦ࡯ࡧࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴ࠺ࠡࠤᙹ") + str(error))
    return {
        bstackl_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᙺ"): bstackl_opy_ (u"ࠨࡧࡵࡶࡴࡸࠧᙻ"),
        bstackl_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙼ"): str(error)
    }
def bstack11ll1ll11ll_opy_(bstack11ll1l1l1ll_opy_):
    return re.match(bstackl_opy_ (u"ࡵࠫࡣࡢࡤࠬࠪ࡟࠲ࡡࡪࠫࠪࡁࠧࠫᙽ"), bstack11ll1l1l1ll_opy_.strip()) is not None
def bstack1lll1l111l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11ll1l1ll11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11ll1l1ll11_opy_ = desired_capabilities
        else:
          bstack11ll1l1ll11_opy_ = {}
        bstack1ll11llll1l_opy_ = (bstack11ll1l1ll11_opy_.get(bstackl_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᙾ"), bstackl_opy_ (u"ࠬ࠭ᙿ")).lower() or caps.get(bstackl_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ "), bstackl_opy_ (u"ࠧࠨᚁ")).lower())
        if bstack1ll11llll1l_opy_ == bstackl_opy_ (u"ࠨ࡫ࡲࡷࠬᚂ"):
            return True
        if bstack1ll11llll1l_opy_ == bstackl_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᚃ"):
            bstack1ll111l1lll_opy_ = str(float(caps.get(bstackl_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚄ")) or bstack11ll1l1ll11_opy_.get(bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚅ"), {}).get(bstackl_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᚆ"),bstackl_opy_ (u"࠭ࠧᚇ"))))
            if bstack1ll11llll1l_opy_ == bstackl_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᚈ") and int(bstack1ll111l1lll_opy_.split(bstackl_opy_ (u"ࠨ࠰ࠪᚉ"))[0]) < float(bstack11ll1l1llll_opy_):
                logger.warning(str(bstack11ll11lllll_opy_))
                return False
            return True
        bstack1ll111ll11l_opy_ = caps.get(bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚊ"), {}).get(bstackl_opy_ (u"ࠪࡨࡪࡼࡩࡤࡧࡑࡥࡲ࡫ࠧᚋ"), caps.get(bstackl_opy_ (u"ࠫࡩ࡫ࡶࡪࡥࡨࠫᚌ"), bstackl_opy_ (u"ࠬ࠭ᚍ")))
        if bstack1ll111ll11l_opy_:
            logger.warning(bstackl_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡄࡦࡵ࡮ࡸࡴࡶࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᚎ"))
            return False
        browser = caps.get(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᚏ"), bstackl_opy_ (u"ࠨࠩᚐ")).lower() or bstack11ll1l1ll11_opy_.get(bstackl_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᚑ"), bstackl_opy_ (u"ࠪࠫᚒ")).lower()
        if browser != bstackl_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᚓ"):
            logger.warning(bstackl_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᚔ"))
            return False
        browser_version = caps.get(bstackl_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚕ")) or caps.get(bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᚖ")) or bstack11ll1l1ll11_opy_.get(bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᚗ")) or bstack11ll1l1ll11_opy_.get(bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚘ"), {}).get(bstackl_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚙ")) or bstack11ll1l1ll11_opy_.get(bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚚ"), {}).get(bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ᚛"))
        bstack1ll11l11ll1_opy_ = bstack11ll1ll1ll1_opy_.bstack1ll1l111111_opy_
        bstack11lll111l1l_opy_ = False
        if config is not None:
          bstack11lll111l1l_opy_ = bstackl_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ᚜") in config and str(config[bstackl_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ᚝")]).lower() != bstackl_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧ᚞")
        if os.environ.get(bstackl_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧ᚟"), bstackl_opy_ (u"ࠪࠫᚠ")).lower() == bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩᚡ") or bstack11lll111l1l_opy_:
          bstack1ll11l11ll1_opy_ = bstack11ll1ll1ll1_opy_.bstack1ll11l111ll_opy_
        if browser_version and browser_version != bstackl_opy_ (u"ࠬࡲࡡࡵࡧࡶࡸࠬᚢ") and int(browser_version.split(bstackl_opy_ (u"࠭࠮ࠨᚣ"))[0]) <= bstack1ll11l11ll1_opy_:
          logger.warning(bstack1lll11l1l1l_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠢࡪࡶࡪࡧࡴࡦࡴࠣࡸ࡭ࡧ࡮ࠡࡽࡰ࡭ࡳࡥࡡ࠲࠳ࡼࡣࡸࡻࡰࡱࡱࡵࡸࡪࡪ࡟ࡤࡪࡵࡳࡲ࡫࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࡾ࠰ࠪᚤ"))
          return False
        if not options:
          bstack1ll11ll11ll_opy_ = caps.get(bstackl_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚥ")) or bstack11ll1l1ll11_opy_.get(bstackl_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᚦ"), {})
          if bstackl_opy_ (u"ࠪ࠱࠲࡮ࡥࡢࡦ࡯ࡩࡸࡹࠧᚧ") in bstack1ll11ll11ll_opy_.get(bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩᚨ"), []):
              logger.warning(bstackl_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠ࡯ࡱࡷࠤࡷࡻ࡮ࠡࡱࡱࠤࡱ࡫ࡧࡢࡥࡼࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲࡙ࠥࡷࡪࡶࡦ࡬ࠥࡺ࡯ࠡࡰࡨࡻࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩࠥࡵࡲࠡࡣࡹࡳ࡮ࡪࠠࡶࡵ࡬ࡲ࡬ࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠢᚩ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstackl_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡡ࡭࡫ࡧࡥࡹ࡫ࠠࡢ࠳࠴ࡽࠥࡹࡵࡱࡲࡲࡶࡹࠦ࠺ࠣᚪ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1lll1lll_opy_ = config.get(bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᚫ"), {})
    bstack1ll1lll1lll_opy_[bstackl_opy_ (u"ࠨࡣࡸࡸ࡭࡚࡯࡬ࡧࡱࠫᚬ")] = os.getenv(bstackl_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᚭ"))
    bstack11ll11lll11_opy_ = json.loads(os.getenv(bstackl_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᚮ"), bstackl_opy_ (u"ࠫࢀࢃࠧᚯ"))).get(bstackl_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᚰ"))
    if not config[bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᚱ")].get(bstackl_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᚲ")):
      if bstackl_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚳ") in caps:
        caps[bstackl_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᚴ")][bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᚵ")] = bstack1ll1lll1lll_opy_
        caps[bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᚶ")][bstackl_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᚷ")][bstackl_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚸ")] = bstack11ll11lll11_opy_
      else:
        caps[bstackl_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᚹ")] = bstack1ll1lll1lll_opy_
        caps[bstackl_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᚺ")][bstackl_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᚻ")] = bstack11ll11lll11_opy_
  except Exception as error:
    logger.debug(bstackl_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦᚼ") +  str(error))
def bstack1ll1l11111_opy_(driver, bstack11ll1l111l1_opy_):
  try:
    setattr(driver, bstackl_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᚽ"), True)
    session = driver.session_id
    if session:
      bstack11ll1l11l1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1l11l1l_opy_ = False
      bstack11ll1l11l1l_opy_ = url.scheme in [bstackl_opy_ (u"ࠧ࡮ࡴࡵࡲࠥᚾ"), bstackl_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᚿ")]
      if bstack11ll1l11l1l_opy_:
        if bstack11ll1l111l1_opy_:
          logger.info(bstackl_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢᛀ"))
      return bstack11ll1l111l1_opy_
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᛁ") + str(e))
    return False
def bstack11ll11111l_opy_(driver, name, path):
  try:
    bstack1ll1l111lll_opy_ = {
        bstackl_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᛂ"): threading.current_thread().current_test_uuid,
        bstackl_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᛃ"): os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᛄ"), bstackl_opy_ (u"ࠬ࠭ᛅ")),
        bstackl_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪᛆ"): os.environ.get(bstackl_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᛇ"), bstackl_opy_ (u"ࠨࠩᛈ"))
    }
    bstack1ll11lll11l_opy_ = bstack11l111111_opy_.bstack1ll11llllll_opy_(EVENTS.bstack11ll11l11_opy_.value)
    logger.debug(bstackl_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᛉ"))
    try:
      if (bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᛊ"), None) and bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᛋ"), None)):
        scripts = {bstackl_opy_ (u"ࠬࡹࡣࡢࡰࠪᛌ"): bstack1l111l111_opy_.perform_scan}
        bstack11ll1l111ll_opy_ = json.loads(scripts[bstackl_opy_ (u"ࠨࡳࡤࡣࡱࠦᛍ")].replace(bstackl_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᛎ"), bstackl_opy_ (u"ࠣࠤᛏ")))
        bstack11ll1l111ll_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᛐ")][bstackl_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᛑ")] = None
        scripts[bstackl_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᛒ")] = bstackl_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᛓ") + json.dumps(bstack11ll1l111ll_opy_)
        bstack1l111l111_opy_.bstack111l1ll11_opy_(scripts)
        bstack1l111l111_opy_.store()
        logger.debug(driver.execute_script(bstack1l111l111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111l111_opy_.perform_scan, {bstackl_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᛔ"): name}))
      bstack11l111111_opy_.end(EVENTS.bstack11ll11l11_opy_.value, bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᛕ"), bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᛖ"), True, None)
    except Exception as error:
      bstack11l111111_opy_.end(EVENTS.bstack11ll11l11_opy_.value, bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᛗ"), bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᛘ"), False, str(error))
    bstack1ll11lll11l_opy_ = bstack11l111111_opy_.bstack11lll11111l_opy_(EVENTS.bstack1ll11ll1l11_opy_.value)
    bstack11l111111_opy_.mark(bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᛙ"))
    try:
      if (bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᛚ"), None) and bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᛛ"), None)):
        scripts = {bstackl_opy_ (u"ࠧࡴࡥࡤࡲࠬᛜ"): bstack1l111l111_opy_.perform_scan}
        bstack11ll1l111ll_opy_ = json.loads(scripts[bstackl_opy_ (u"ࠣࡵࡦࡥࡳࠨᛝ")].replace(bstackl_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᛞ"), bstackl_opy_ (u"ࠥࠦᛟ")))
        bstack11ll1l111ll_opy_[bstackl_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᛠ")][bstackl_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᛡ")] = None
        scripts[bstackl_opy_ (u"ࠨࡳࡤࡣࡱࠦᛢ")] = bstackl_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᛣ") + json.dumps(bstack11ll1l111ll_opy_)
        bstack1l111l111_opy_.bstack111l1ll11_opy_(scripts)
        bstack1l111l111_opy_.store()
        logger.debug(driver.execute_script(bstack1l111l111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l111l111_opy_.bstack11ll1llll1l_opy_, bstack1ll1l111lll_opy_))
      bstack11l111111_opy_.end(bstack1ll11lll11l_opy_, bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᛤ"), bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᛥ"),True, None)
    except Exception as error:
      bstack11l111111_opy_.end(bstack1ll11lll11l_opy_, bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᛦ"), bstack1ll11lll11l_opy_ + bstackl_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᛧ"),False, str(error))
    logger.info(bstackl_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᛨ"))
  except Exception as bstack1ll1111lll1_opy_:
    logger.error(bstackl_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᛩ") + str(path) + bstackl_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᛪ") + str(bstack1ll1111lll1_opy_))
def bstack11ll1l1ll1l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstackl_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢ᛫")) and str(caps.get(bstackl_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣ᛬"))).lower() == bstackl_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦ᛭"):
        bstack1ll111l1lll_opy_ = caps.get(bstackl_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᛮ")) or caps.get(bstackl_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᛯ"))
        if bstack1ll111l1lll_opy_ and int(str(bstack1ll111l1lll_opy_)) < bstack11ll1l1llll_opy_:
            return False
    return True
def bstack11ll1l1lll_opy_(config):
  if bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᛰ") in config:
        return config[bstackl_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛱ")]
  for platform in config.get(bstackl_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᛲ"), []):
      if bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᛳ") in platform:
          return platform[bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᛴ")]
  return None
def bstack1l11l1ll_opy_(bstack1lll11l111_opy_):
  try:
    browser_name = bstack1lll11l111_opy_[bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᛵ")]
    browser_version = bstack1lll11l111_opy_[bstackl_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᛶ")]
    chrome_options = bstack1lll11l111_opy_[bstackl_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪࡥ࡯ࡱࡶ࡬ࡳࡳࡹࠧᛷ")]
    try:
        bstack11lll111111_opy_ = int(browser_version.split(bstackl_opy_ (u"ࠧ࠯ࠩᛸ"))[0])
    except ValueError as e:
        logger.error(bstackl_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡣࡰࡰࡹࡩࡷࡺࡩ࡯ࡩࠣࡦࡷࡵࡷࡴࡧࡵࠤࡻ࡫ࡲࡴ࡫ࡲࡲࠧ᛹") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstackl_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩ᛺")):
        logger.warning(bstackl_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨ᛻"))
        return False
    if bstack11lll111111_opy_ < bstack11ll1ll1ll1_opy_.bstack1ll11l111ll_opy_:
        logger.warning(bstack1lll11l1l1l_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡴࡨࡵࡺ࡯ࡲࡦࡵࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡺࡪࡸࡳࡪࡱࡱࠤࢀࡉࡏࡏࡕࡗࡅࡓ࡚ࡓ࠯ࡏࡌࡒࡎࡓࡕࡎࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗ࡚ࡖࡐࡐࡔࡗࡉࡉࡥࡃࡉࡔࡒࡑࡊࡥࡖࡆࡔࡖࡍࡔࡔࡽࠡࡱࡵࠤ࡭࡯ࡧࡩࡧࡵ࠲ࠬ᛼"))
        return False
    if chrome_options and any(bstackl_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩ᛽") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstackl_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡰࡲࡸࠥࡸࡵ࡯ࠢࡲࡲࠥࡲࡥࡨࡣࡦࡽࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠦࡓࡸ࡫ࡷࡧ࡭ࠦࡴࡰࠢࡱࡩࡼࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪࠦ࡯ࡳࠢࡤࡺࡴ࡯ࡤࠡࡷࡶ࡭ࡳ࡭ࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠣ᛾"))
        return False
    return True
  except Exception as e:
    logger.error(bstackl_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡩ࡯ࠢࡦ࡬ࡪࡩ࡫ࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡳࡶࡲࡳࡳࡷࡺࠠࡧࡱࡵࠤࡱࡵࡣࡢ࡮ࠣࡇ࡭ࡸ࡯࡮ࡧ࠽ࠤࠧ᛿") + str(e))
    return False
def bstack11llll111_opy_(bstack1l1l11lll1_opy_, config):
    try:
      bstack1ll111l1ll1_opy_ = bstackl_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜀ") in config and config[bstackl_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᜁ")] == True
      bstack11lll111l1l_opy_ = bstackl_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᜂ") in config and str(config[bstackl_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᜃ")]).lower() != bstackl_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᜄ")
      if not (bstack1ll111l1ll1_opy_ and (not bstack1l11l11ll_opy_(config) or bstack11lll111l1l_opy_)):
        return bstack1l1l11lll1_opy_
      bstack11ll1ll1lll_opy_ = bstack1l111l111_opy_.bstack11ll11llll1_opy_
      if bstack11ll1ll1lll_opy_ is None:
        logger.debug(bstackl_opy_ (u"ࠨࡇࡰࡱࡪࡰࡪࠦࡣࡩࡴࡲࡱࡪࠦ࡯ࡱࡶ࡬ࡳࡳࡹࠠࡢࡴࡨࠤࡓࡵ࡮ࡦࠤᜅ"))
        return bstack1l1l11lll1_opy_
      bstack11ll1l11lll_opy_ = int(str(bstack11lll1111l1_opy_()).split(bstackl_opy_ (u"ࠧ࠯ࠩᜆ"))[0])
      logger.debug(bstackl_opy_ (u"ࠣࡕࡨࡰࡪࡴࡩࡶ࡯ࠣࡺࡪࡸࡳࡪࡱࡱࠤࡩ࡫ࡴࡦࡥࡷࡩࡩࡀࠠࠣᜇ") + str(bstack11ll1l11lll_opy_) + bstackl_opy_ (u"ࠤࠥᜈ"))
      if bstack11ll1l11lll_opy_ == 3 and isinstance(bstack1l1l11lll1_opy_, dict) and bstackl_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜉ") in bstack1l1l11lll1_opy_ and bstack11ll1ll1lll_opy_ is not None:
        if bstackl_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜊ") not in bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜋ")]:
          bstack1l1l11lll1_opy_[bstackl_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜌ")][bstackl_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᜍ")] = {}
        if bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᜎ") in bstack11ll1ll1lll_opy_:
          if bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᜏ") not in bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜐ")][bstackl_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜑ")]:
            bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜒ")][bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜓ")][bstackl_opy_ (u"ࠧࡢࡴࡪࡷ᜔ࠬ")] = []
          for arg in bstack11ll1ll1lll_opy_[bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ᜕࠭")]:
            if arg not in bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᜖")][bstackl_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᜗")][bstackl_opy_ (u"ࠫࡦࡸࡧࡴࠩ᜘")]:
              bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᜙")][bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᜚")][bstackl_opy_ (u"ࠧࡢࡴࡪࡷࠬ᜛")].append(arg)
        if bstackl_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᜜") in bstack11ll1ll1lll_opy_:
          if bstackl_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭᜝") not in bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ᜞")][bstackl_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜟ")]:
            bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜠ")][bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜡ")][bstackl_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᜢ")] = []
          for ext in bstack11ll1ll1lll_opy_[bstackl_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᜣ")]:
            if ext not in bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᜤ")][bstackl_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᜥ")][bstackl_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᜦ")]:
              bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜧ")][bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜨ")][bstackl_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᜩ")].append(ext)
        if bstackl_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᜪ") in bstack11ll1ll1lll_opy_:
          if bstackl_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᜫ") not in bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜬ")][bstackl_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜭ")]:
            bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᜮ")][bstackl_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᜯ")][bstackl_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᜰ")] = {}
          bstack11ll1ll1l11_opy_(bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᜱ")][bstackl_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᜲ")][bstackl_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᜳ")],
                    bstack11ll1ll1lll_opy_[bstackl_opy_ (u"ࠫࡵࡸࡥࡧࡵ᜴ࠪ")])
        os.environ[bstackl_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ᜵")] = bstackl_opy_ (u"࠭ࡴࡳࡷࡨࠫ᜶")
        return bstack1l1l11lll1_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l1l11lll1_opy_, ChromeOptions):
          chrome_options = bstack1l1l11lll1_opy_
        elif isinstance(bstack1l1l11lll1_opy_, dict):
          for value in bstack1l1l11lll1_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l1l11lll1_opy_, dict):
            bstack1l1l11lll1_opy_[bstackl_opy_ (u"ࠧࡰࡲࡷ࡭ࡴࡴࡳࠨ᜷")] = chrome_options
          else:
            bstack1l1l11lll1_opy_ = chrome_options
        if bstack11ll1ll1lll_opy_ is not None:
          if bstackl_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᜸") in bstack11ll1ll1lll_opy_:
                bstack11ll1ll1l1l_opy_ = chrome_options.arguments or []
                new_args = bstack11ll1ll1lll_opy_[bstackl_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ᜹")]
                for arg in new_args:
                    if arg not in bstack11ll1ll1l1l_opy_:
                        chrome_options.add_argument(arg)
          if bstackl_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ᜺") in bstack11ll1ll1lll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstackl_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ᜻"), [])
                bstack11ll1lll11l_opy_ = bstack11ll1ll1lll_opy_[bstackl_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ᜼")]
                for extension in bstack11ll1lll11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstackl_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ᜽") in bstack11ll1ll1lll_opy_:
                bstack11ll1lll1ll_opy_ = chrome_options.experimental_options.get(bstackl_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᜾"), {})
                bstack11ll1ll1111_opy_ = bstack11ll1ll1lll_opy_[bstackl_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᜿")]
                bstack11ll1ll1l11_opy_(bstack11ll1lll1ll_opy_, bstack11ll1ll1111_opy_)
                chrome_options.add_experimental_option(bstackl_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᝀ"), bstack11ll1lll1ll_opy_)
        os.environ[bstackl_opy_ (u"ࠪࡍࡘࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡇࡖࡗࡎࡕࡎࠨᝁ")] = bstackl_opy_ (u"ࠫࡹࡸࡵࡦࠩᝂ")
        return bstack1l1l11lll1_opy_
    except Exception as e:
      logger.error(bstackl_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡥࡩࡪࡩ࡯ࡩࠣࡲࡴࡴ࠭ࡃࡕࠣ࡭ࡳ࡬ࡲࡢࠢࡤ࠵࠶ࡿࠠࡤࡪࡵࡳࡲ࡫ࠠࡰࡲࡷ࡭ࡴࡴࡳ࠻ࠢࠥᝃ") + str(e))
      return bstack1l1l11lll1_opy_