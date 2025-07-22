# coding: UTF-8
import sys
bstack1llllll1_opy_ = sys.version_info [0] == 2
bstack11l1l1l_opy_ = 2048
bstack1ll111_opy_ = 7
def bstack111l111_opy_ (bstack11ll1_opy_):
    global bstack11111_opy_
    bstack1111l11_opy_ = ord (bstack11ll1_opy_ [-1])
    bstack1ll11l1_opy_ = bstack11ll1_opy_ [:-1]
    bstack1111ll_opy_ = bstack1111l11_opy_ % len (bstack1ll11l1_opy_)
    bstack1lll1_opy_ = bstack1ll11l1_opy_ [:bstack1111ll_opy_] + bstack1ll11l1_opy_ [bstack1111ll_opy_:]
    if bstack1llllll1_opy_:
        bstack1l1ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    else:
        bstack1l1ll11_opy_ = str () .join ([chr (ord (char) - bstack11l1l1l_opy_ - (bstack111111_opy_ + bstack1111l11_opy_) % bstack1ll111_opy_) for bstack111111_opy_, char in enumerate (bstack1lll1_opy_)])
    return eval (bstack1l1ll11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11ll1lllll1_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11ll1l111ll_opy_ as bstack11ll1llllll_opy_, EVENTS
from bstack_utils.bstack111lll1ll_opy_ import bstack111lll1ll_opy_
from bstack_utils.helper import bstack1ll1ll1l1_opy_, bstack111l1ll111_opy_, bstack1lllll1lll_opy_, bstack11ll1lll111_opy_, \
  bstack11ll1l1lll1_opy_, bstack1ll1l11111_opy_, get_host_info, bstack11ll1ll11l1_opy_, bstack1llll111l_opy_, bstack111l1l1l1l_opy_, bstack11ll11lllll_opy_, bstack11ll1lll1ll_opy_, bstack1ll11lllll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l1111ll_opy_ import get_logger
from bstack_utils.bstack1ll11l1lll_opy_ import bstack1llll1111l1_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1ll11l1lll_opy_ = bstack1llll1111l1_opy_()
@bstack111l1l1l1l_opy_(class_method=False)
def _11ll1l1ll1l_opy_(driver, bstack11111l11ll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack111l111_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩᘒ"): caps.get(bstack111l111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᘓ"), None),
        bstack111l111_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᘔ"): bstack11111l11ll_opy_.get(bstack111l111_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᘕ"), None),
        bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᘖ"): caps.get(bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᘗ"), None),
        bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᘘ"): caps.get(bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᘙ"), None)
    }
  except Exception as error:
    logger.debug(bstack111l111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᘚ") + str(error))
  return response
def on():
    if os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᘛ"), None) is None or os.environ[bstack111l111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᘜ")] == bstack111l111_opy_ (u"ࠧࡴࡵ࡭࡮ࠥᘝ"):
        return False
    return True
def bstack1ll1l1l1l_opy_(config):
  return config.get(bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᘞ"), False) or any([p.get(bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘟ"), False) == True for p in config.get(bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘠ"), [])])
def bstack11l111lll_opy_(config, bstack11ll11l111_opy_):
  try:
    bstack11ll1l1l1l1_opy_ = config.get(bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘡ"), False)
    if int(bstack11ll11l111_opy_) < len(config.get(bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᘢ"), [])) and config[bstack111l111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᘣ")][bstack11ll11l111_opy_]:
      bstack11ll11lll1l_opy_ = config[bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᘤ")][bstack11ll11l111_opy_].get(bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᘥ"), None)
    else:
      bstack11ll11lll1l_opy_ = config.get(bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘦ"), None)
    if bstack11ll11lll1l_opy_ != None:
      bstack11ll1l1l1l1_opy_ = bstack11ll11lll1l_opy_
    bstack11ll1l111l1_opy_ = os.getenv(bstack111l111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᘧ")) is not None and len(os.getenv(bstack111l111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᘨ"))) > 0 and os.getenv(bstack111l111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᘩ")) != bstack111l111_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᘪ")
    return bstack11ll1l1l1l1_opy_ and bstack11ll1l111l1_opy_
  except Exception as error:
    logger.debug(bstack111l111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᘫ") + str(error))
  return False
def bstack11ll111lll_opy_(test_tags):
  bstack1ll11ll1l1l_opy_ = os.getenv(bstack111l111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᘬ"))
  if bstack1ll11ll1l1l_opy_ is None:
    return True
  bstack1ll11ll1l1l_opy_ = json.loads(bstack1ll11ll1l1l_opy_)
  try:
    include_tags = bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᘭ")] if bstack111l111_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᘮ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᘯ")], list) else []
    exclude_tags = bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᘰ")] if bstack111l111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᘱ") in bstack1ll11ll1l1l_opy_ and isinstance(bstack1ll11ll1l1l_opy_[bstack111l111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᘲ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack111l111_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᘳ") + str(error))
  return False
def bstack11lll1111ll_opy_(config, bstack11lll111l11_opy_, bstack11ll1l11lll_opy_, bstack11ll1ll111l_opy_):
  bstack11ll1l11111_opy_ = bstack11ll1lll111_opy_(config)
  bstack11ll1l11l1l_opy_ = bstack11ll1l1lll1_opy_(config)
  if bstack11ll1l11111_opy_ is None or bstack11ll1l11l1l_opy_ is None:
    logger.error(bstack111l111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᘴ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᘵ"), bstack111l111_opy_ (u"ࠩࡾࢁࠬᘶ")))
    data = {
        bstack111l111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᘷ"): config[bstack111l111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᘸ")],
        bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᘹ"): config.get(bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᘺ"), os.path.basename(os.getcwd())),
        bstack111l111_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪᘻ"): bstack1ll1ll1l1_opy_(),
        bstack111l111_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᘼ"): config.get(bstack111l111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᘽ"), bstack111l111_opy_ (u"ࠪࠫᘾ")),
        bstack111l111_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫᘿ"): {
            bstack111l111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬᙀ"): bstack11lll111l11_opy_,
            bstack111l111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᙁ"): bstack11ll1l11lll_opy_,
            bstack111l111_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᙂ"): __version__,
            bstack111l111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪᙃ"): bstack111l111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩᙄ"),
            bstack111l111_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪᙅ"): bstack111l111_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭ᙆ"),
            bstack111l111_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᙇ"): bstack11ll1ll111l_opy_
        },
        bstack111l111_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᙈ"): settings,
        bstack111l111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨᙉ"): bstack11ll1ll11l1_opy_(),
        bstack111l111_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨᙊ"): bstack1ll1l11111_opy_(),
        bstack111l111_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫᙋ"): get_host_info(),
        bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᙌ"): bstack1lllll1lll_opy_(config)
    }
    headers = {
        bstack111l111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᙍ"): bstack111l111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᙎ"),
    }
    config = {
        bstack111l111_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᙏ"): (bstack11ll1l11111_opy_, bstack11ll1l11l1l_opy_),
        bstack111l111_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᙐ"): headers
    }
    response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᙑ"), bstack11ll1llllll_opy_ + bstack111l111_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩᙒ"), data, config)
    bstack11ll1llll11_opy_ = response.json()
    if bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᙓ")]:
      parsed = json.loads(os.getenv(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᙔ"), bstack111l111_opy_ (u"ࠬࢁࡽࠨᙕ")))
      parsed[bstack111l111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᙖ")] = bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠧࡥࡣࡷࡥࠬᙗ")][bstack111l111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᙘ")]
      os.environ[bstack111l111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᙙ")] = json.dumps(parsed)
      bstack111lll1ll_opy_.bstack11lll111l_opy_(bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠪࡨࡦࡺࡡࠨᙚ")][bstack111l111_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᙛ")])
      bstack111lll1ll_opy_.bstack11ll11lll11_opy_(bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠬࡪࡡࡵࡣࠪᙜ")][bstack111l111_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨᙝ")])
      bstack111lll1ll_opy_.store()
      return bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠧࡥࡣࡷࡥࠬᙞ")][bstack111l111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭ᙟ")], bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠩࡧࡥࡹࡧࠧᙠ")][bstack111l111_opy_ (u"ࠪ࡭ࡩ࠭ᙡ")]
    else:
      logger.error(bstack111l111_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬᙢ") + bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᙣ")])
      if bstack11ll1llll11_opy_[bstack111l111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᙤ")] == bstack111l111_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩᙥ"):
        for bstack11lll111111_opy_ in bstack11ll1llll11_opy_[bstack111l111_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨᙦ")]:
          logger.error(bstack11lll111111_opy_[bstack111l111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᙧ")])
      return None, None
  except Exception as error:
    logger.error(bstack111l111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦᙨ") +  str(error))
    return None, None
def bstack11ll1ll11ll_opy_():
  if os.getenv(bstack111l111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᙩ")) is None:
    return {
        bstack111l111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᙪ"): bstack111l111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᙫ"),
        bstack111l111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᙬ"): bstack111l111_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧ᙭")
    }
  data = {bstack111l111_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪ᙮"): bstack1ll1ll1l1_opy_()}
  headers = {
      bstack111l111_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪᙯ"): bstack111l111_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬᙰ") + os.getenv(bstack111l111_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥᙱ")),
      bstack111l111_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬᙲ"): bstack111l111_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪᙳ")
  }
  response = bstack1llll111l_opy_(bstack111l111_opy_ (u"ࠨࡒࡘࡘࠬᙴ"), bstack11ll1llllll_opy_ + bstack111l111_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫᙵ"), data, { bstack111l111_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫᙶ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack111l111_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧᙷ") + bstack111l1ll111_opy_().isoformat() + bstack111l111_opy_ (u"ࠬࡠࠧᙸ"))
      return {bstack111l111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᙹ"): bstack111l111_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨᙺ"), bstack111l111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᙻ"): bstack111l111_opy_ (u"ࠩࠪᙼ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack111l111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨᙽ") + str(error))
    return {
        bstack111l111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᙾ"): bstack111l111_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᙿ"),
        bstack111l111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ "): str(error)
    }
def bstack11ll11ll1ll_opy_(bstack11ll1l1llll_opy_):
    return re.match(bstack111l111_opy_ (u"ࡲࠨࡠ࡟ࡨ࠰࠮࡜࠯࡞ࡧ࠯࠮ࡅࠤࠨᚁ"), bstack11ll1l1llll_opy_.strip()) is not None
def bstack1l11llll1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11ll1l11l11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11ll1l11l11_opy_ = desired_capabilities
        else:
          bstack11ll1l11l11_opy_ = {}
        bstack1ll11llll1l_opy_ = (bstack11ll1l11l11_opy_.get(bstack111l111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᚂ"), bstack111l111_opy_ (u"ࠩࠪᚃ")).lower() or caps.get(bstack111l111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᚄ"), bstack111l111_opy_ (u"ࠫࠬᚅ")).lower())
        if bstack1ll11llll1l_opy_ == bstack111l111_opy_ (u"ࠬ࡯࡯ࡴࠩᚆ"):
            return True
        if bstack1ll11llll1l_opy_ == bstack111l111_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧᚇ"):
            bstack1ll111l1l1l_opy_ = str(float(caps.get(bstack111l111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩᚈ")) or bstack11ll1l11l11_opy_.get(bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚉ"), {}).get(bstack111l111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᚊ"),bstack111l111_opy_ (u"ࠪࠫᚋ"))))
            if bstack1ll11llll1l_opy_ == bstack111l111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬᚌ") and int(bstack1ll111l1l1l_opy_.split(bstack111l111_opy_ (u"ࠬ࠴ࠧᚍ"))[0]) < float(bstack11ll1ll1lll_opy_):
                logger.warning(str(bstack11lll1111l1_opy_))
                return False
            return True
        bstack1ll11l1l1ll_opy_ = caps.get(bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚎ"), {}).get(bstack111l111_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫᚏ"), caps.get(bstack111l111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨᚐ"), bstack111l111_opy_ (u"ࠩࠪᚑ")))
        if bstack1ll11l1l1ll_opy_:
            logger.warning(bstack111l111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢᚒ"))
            return False
        browser = caps.get(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᚓ"), bstack111l111_opy_ (u"ࠬ࠭ᚔ")).lower() or bstack11ll1l11l11_opy_.get(bstack111l111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᚕ"), bstack111l111_opy_ (u"ࠧࠨᚖ")).lower()
        if browser != bstack111l111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨᚗ"):
            logger.warning(bstack111l111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᚘ"))
            return False
        browser_version = caps.get(bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚙ")) or caps.get(bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᚚ")) or bstack11ll1l11l11_opy_.get(bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᚛")) or bstack11ll1l11l11_opy_.get(bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᚜"), {}).get(bstack111l111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ᚝")) or bstack11ll1l11l11_opy_.get(bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᚞"), {}).get(bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᚟"))
        bstack1ll1l11l1l1_opy_ = bstack11ll1lllll1_opy_.bstack1ll111l11ll_opy_
        bstack11ll1llll1l_opy_ = False
        if config is not None:
          bstack11ll1llll1l_opy_ = bstack111l111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧᚠ") in config and str(config[bstack111l111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨᚡ")]).lower() != bstack111l111_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫᚢ")
        if os.environ.get(bstack111l111_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᚣ"), bstack111l111_opy_ (u"ࠧࠨᚤ")).lower() == bstack111l111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᚥ") or bstack11ll1llll1l_opy_:
          bstack1ll1l11l1l1_opy_ = bstack11ll1lllll1_opy_.bstack1ll11lll1ll_opy_
        if browser_version and browser_version != bstack111l111_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᚦ") and int(browser_version.split(bstack111l111_opy_ (u"ࠪ࠲ࠬᚧ"))[0]) <= bstack1ll1l11l1l1_opy_:
          logger.warning(bstack1lll11l11ll_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥࢁ࡭ࡪࡰࡢࡥ࠶࠷ࡹࡠࡵࡸࡴࡵࡵࡲࡵࡧࡧࡣࡨ࡮ࡲࡰ࡯ࡨࡣࡻ࡫ࡲࡴ࡫ࡲࡲࢂ࠴ࠧᚨ"))
          return False
        if not options:
          bstack1ll111ll111_opy_ = caps.get(bstack111l111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᚩ")) or bstack11ll1l11l11_opy_.get(bstack111l111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᚪ"), {})
          if bstack111l111_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᚫ") in bstack1ll111ll111_opy_.get(bstack111l111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᚬ"), []):
              logger.warning(bstack111l111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᚭ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack111l111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᚮ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll11l1l1l_opy_ = config.get(bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᚯ"), {})
    bstack1lll11l1l1l_opy_[bstack111l111_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᚰ")] = os.getenv(bstack111l111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᚱ"))
    bstack11ll1l1ll11_opy_ = json.loads(os.getenv(bstack111l111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᚲ"), bstack111l111_opy_ (u"ࠨࡽࢀࠫᚳ"))).get(bstack111l111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᚴ"))
    if not config[bstack111l111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬᚵ")].get(bstack111l111_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥᚶ")):
      if bstack111l111_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᚷ") in caps:
        caps[bstack111l111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᚸ")][bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᚹ")] = bstack1lll11l1l1l_opy_
        caps[bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᚺ")][bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᚻ")][bstack111l111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᚼ")] = bstack11ll1l1ll11_opy_
      else:
        caps[bstack111l111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᚽ")] = bstack1lll11l1l1l_opy_
        caps[bstack111l111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᚾ")][bstack111l111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᚿ")] = bstack11ll1l1ll11_opy_
  except Exception as error:
    logger.debug(bstack111l111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࠣᛀ") +  str(error))
def bstack111l11l1_opy_(driver, bstack11ll1ll1l11_opy_):
  try:
    setattr(driver, bstack111l111_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨᛁ"), True)
    session = driver.session_id
    if session:
      bstack11ll1l11ll1_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11ll1l11ll1_opy_ = False
      bstack11ll1l11ll1_opy_ = url.scheme in [bstack111l111_opy_ (u"ࠤ࡫ࡸࡹࡶࠢᛂ"), bstack111l111_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤᛃ")]
      if bstack11ll1l11ll1_opy_:
        if bstack11ll1ll1l11_opy_:
          logger.info(bstack111l111_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦᛄ"))
      return bstack11ll1ll1l11_opy_
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᛅ") + str(e))
    return False
def bstack1llllll11_opy_(driver, name, path):
  try:
    bstack1ll111ll11l_opy_ = {
        bstack111l111_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭ᛆ"): threading.current_thread().current_test_uuid,
        bstack111l111_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬᛇ"): os.environ.get(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭ᛈ"), bstack111l111_opy_ (u"ࠩࠪᛉ")),
        bstack111l111_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧᛊ"): os.environ.get(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨᛋ"), bstack111l111_opy_ (u"ࠬ࠭ᛌ"))
    }
    bstack1ll11llll11_opy_ = bstack1ll11l1lll_opy_.bstack1ll111llll1_opy_(EVENTS.bstack1l1l1lll1_opy_.value)
    logger.debug(bstack111l111_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩᛍ"))
    try:
      if (bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧᛎ"), None) and bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪᛏ"), None)):
        scripts = {bstack111l111_opy_ (u"ࠩࡶࡧࡦࡴࠧᛐ"): bstack111lll1ll_opy_.perform_scan}
        bstack11ll1lll1l1_opy_ = json.loads(scripts[bstack111l111_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᛑ")].replace(bstack111l111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᛒ"), bstack111l111_opy_ (u"ࠧࠨᛓ")))
        bstack11ll1lll1l1_opy_[bstack111l111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩᛔ")][bstack111l111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧᛕ")] = None
        scripts[bstack111l111_opy_ (u"ࠣࡵࡦࡥࡳࠨᛖ")] = bstack111l111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᛗ") + json.dumps(bstack11ll1lll1l1_opy_)
        bstack111lll1ll_opy_.bstack11lll111l_opy_(scripts)
        bstack111lll1ll_opy_.store()
        logger.debug(driver.execute_script(bstack111lll1ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack111lll1ll_opy_.perform_scan, {bstack111l111_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥᛘ"): name}))
      bstack1ll11l1lll_opy_.end(EVENTS.bstack1l1l1lll1_opy_.value, bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᛙ"), bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥᛚ"), True, None)
    except Exception as error:
      bstack1ll11l1lll_opy_.end(EVENTS.bstack1l1l1lll1_opy_.value, bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᛛ"), bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᛜ"), False, str(error))
    bstack1ll11llll11_opy_ = bstack1ll11l1lll_opy_.bstack11ll1l1l11l_opy_(EVENTS.bstack1ll11ll111l_opy_.value)
    bstack1ll11l1lll_opy_.mark(bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᛝ"))
    try:
      if (bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩᛞ"), None) and bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬᛟ"), None)):
        scripts = {bstack111l111_opy_ (u"ࠫࡸࡩࡡ࡯ࠩᛠ"): bstack111lll1ll_opy_.perform_scan}
        bstack11ll1lll1l1_opy_ = json.loads(scripts[bstack111l111_opy_ (u"ࠧࡹࡣࡢࡰࠥᛡ")].replace(bstack111l111_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤᛢ"), bstack111l111_opy_ (u"ࠢࠣᛣ")))
        bstack11ll1lll1l1_opy_[bstack111l111_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫᛤ")][bstack111l111_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩᛥ")] = None
        scripts[bstack111l111_opy_ (u"ࠥࡷࡨࡧ࡮ࠣᛦ")] = bstack111l111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢᛧ") + json.dumps(bstack11ll1lll1l1_opy_)
        bstack111lll1ll_opy_.bstack11lll111l_opy_(scripts)
        bstack111lll1ll_opy_.store()
        logger.debug(driver.execute_script(bstack111lll1ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack111lll1ll_opy_.bstack11ll1l1111l_opy_, bstack1ll111ll11l_opy_))
      bstack1ll11l1lll_opy_.end(bstack1ll11llll11_opy_, bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᛨ"), bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᛩ"),True, None)
    except Exception as error:
      bstack1ll11l1lll_opy_.end(bstack1ll11llll11_opy_, bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᛪ"), bstack1ll11llll11_opy_ + bstack111l111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᛫"),False, str(error))
    logger.info(bstack111l111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᛬"))
  except Exception as bstack1ll1111ll1l_opy_:
    logger.error(bstack111l111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡶࡪࡹࡵ࡭ࡶࡶࠤࡨࡵࡵ࡭ࡦࠣࡲࡴࡺࠠࡣࡧࠣࡴࡷࡵࡣࡦࡵࡶࡩࡩࠦࡦࡰࡴࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧ࠽ࠤࠧ᛭") + str(path) + bstack111l111_opy_ (u"ࠦࠥࡋࡲࡳࡱࡵࠤ࠿ࠨᛮ") + str(bstack1ll1111ll1l_opy_))
def bstack11ll1ll1111_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack111l111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦᛯ")) and str(caps.get(bstack111l111_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᛰ"))).lower() == bstack111l111_opy_ (u"ࠢࡢࡰࡧࡶࡴ࡯ࡤࠣᛱ"):
        bstack1ll111l1l1l_opy_ = caps.get(bstack111l111_opy_ (u"ࠣࡣࡳࡴ࡮ࡻ࡭࠻ࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥᛲ")) or caps.get(bstack111l111_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᛳ"))
        if bstack1ll111l1l1l_opy_ and int(str(bstack1ll111l1l1l_opy_)) < bstack11ll1ll1lll_opy_:
            return False
    return True
def bstack11l1l1ll_opy_(config):
  if bstack111l111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᛴ") in config:
        return config[bstack111l111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛵ")]
  for platform in config.get(bstack111l111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᛶ"), []):
      if bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᛷ") in platform:
          return platform[bstack111l111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛸ")]
  return None
def bstack1l1llll1_opy_(bstack11l1l1111_opy_):
  try:
    browser_name = bstack11l1l1111_opy_[bstack111l111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡱࡥࡲ࡫ࠧ᛹")]
    browser_version = bstack11l1l1111_opy_[bstack111l111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫ᛺")]
    chrome_options = bstack11l1l1111_opy_[bstack111l111_opy_ (u"ࠪࡧ࡭ࡸ࡯࡮ࡧࡢࡳࡵࡺࡩࡰࡰࡶࠫ᛻")]
    try:
        bstack11ll1ll1l1l_opy_ = int(browser_version.split(bstack111l111_opy_ (u"ࠫ࠳࠭᛼"))[0])
    except ValueError as e:
        logger.error(bstack111l111_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡴࡴࡶࡦࡴࡷ࡭ࡳ࡭ࠠࡣࡴࡲࡻࡸ࡫ࡲࠡࡸࡨࡶࡸ࡯࡯࡯ࠤ᛽") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack111l111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭᛾")):
        logger.warning(bstack111l111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥ᛿"))
        return False
    if bstack11ll1ll1l1l_opy_ < bstack11ll1lllll1_opy_.bstack1ll11lll1ll_opy_:
        logger.warning(bstack1lll11l11ll_opy_ (u"ࠨࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡸࡥࡲࡷ࡬ࡶࡪࡹࠠࡄࡪࡵࡳࡲ࡫ࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡽࡆࡓࡓ࡙ࡔࡂࡐࡗࡗ࠳ࡓࡉࡏࡋࡐ࡙ࡒࡥࡎࡐࡐࡢࡆࡘ࡚ࡁࡄࡍࡢࡍࡓࡌࡒࡂࡡࡄ࠵࠶࡟࡟ࡔࡗࡓࡔࡔࡘࡔࡆࡆࡢࡇࡍࡘࡏࡎࡇࡢ࡚ࡊࡘࡓࡊࡑࡑࢁࠥࡵࡲࠡࡪ࡬࡫࡭࡫ࡲ࠯ࠩᜀ"))
        return False
    if chrome_options and any(bstack111l111_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᜁ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack111l111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧᜂ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack111l111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣ࡭ࡳࠦࡣࡩࡧࡦ࡯࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡷࡺࡶࡰࡰࡴࡷࠤ࡫ࡵࡲࠡ࡮ࡲࡧࡦࡲࠠࡄࡪࡵࡳࡲ࡫࠺ࠡࠤᜃ") + str(e))
    return False
def bstack11l1ll1lll_opy_(bstack1l1lll1l11_opy_, config):
    try:
      bstack1ll11l11lll_opy_ = bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᜄ") in config and config[bstack111l111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᜅ")] == True
      bstack11ll1llll1l_opy_ = bstack111l111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᜆ") in config and str(config[bstack111l111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬᜇ")]).lower() != bstack111l111_opy_ (u"ࠩࡩࡥࡱࡹࡥࠨᜈ")
      if not (bstack1ll11l11lll_opy_ and (not bstack1lllll1lll_opy_(config) or bstack11ll1llll1l_opy_)):
        return bstack1l1lll1l11_opy_
      bstack11ll11ll1l1_opy_ = bstack111lll1ll_opy_.bstack11ll1ll1ll1_opy_
      if bstack11ll11ll1l1_opy_ is None:
        logger.debug(bstack111l111_opy_ (u"ࠥࡋࡴࡵࡧ࡭ࡧࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶࠤࡦࡸࡥࠡࡐࡲࡲࡪࠨᜉ"))
        return bstack1l1lll1l11_opy_
      bstack11ll1l1l1ll_opy_ = int(str(bstack11ll1lll1ll_opy_()).split(bstack111l111_opy_ (u"ࠫ࠳࠭ᜊ"))[0])
      logger.debug(bstack111l111_opy_ (u"࡙ࠧࡥ࡭ࡧࡱ࡭ࡺࡳࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡦࡨࡸࡪࡩࡴࡦࡦ࠽ࠤࠧᜋ") + str(bstack11ll1l1l1ll_opy_) + bstack111l111_opy_ (u"ࠨࠢᜌ"))
      if bstack11ll1l1l1ll_opy_ == 3 and isinstance(bstack1l1lll1l11_opy_, dict) and bstack111l111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜍ") in bstack1l1lll1l11_opy_ and bstack11ll11ll1l1_opy_ is not None:
        if bstack111l111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜎ") not in bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᜏ")]:
          bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᜐ")][bstack111l111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᜑ")] = {}
        if bstack111l111_opy_ (u"ࠬࡧࡲࡨࡵࠪᜒ") in bstack11ll11ll1l1_opy_:
          if bstack111l111_opy_ (u"࠭ࡡࡳࡩࡶࠫᜓ") not in bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ᜔ࠧ")][bstack111l111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ᜕࠭")]:
            bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᜖")][bstack111l111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᜗")][bstack111l111_opy_ (u"ࠫࡦࡸࡧࡴࠩ᜘")] = []
          for arg in bstack11ll11ll1l1_opy_[bstack111l111_opy_ (u"ࠬࡧࡲࡨࡵࠪ᜙")]:
            if arg not in bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭᜚")][bstack111l111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬ᜛")][bstack111l111_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭᜜")]:
              bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩ᜝")][bstack111l111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᜞")][bstack111l111_opy_ (u"ࠫࡦࡸࡧࡴࠩᜟ")].append(arg)
        if bstack111l111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᜠ") in bstack11ll11ll1l1_opy_:
          if bstack111l111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᜡ") not in bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜢ")][bstack111l111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜣ")]:
            bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᜤ")][bstack111l111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᜥ")][bstack111l111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᜦ")] = []
          for ext in bstack11ll11ll1l1_opy_[bstack111l111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᜧ")]:
            if ext not in bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᜨ")][bstack111l111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᜩ")][bstack111l111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᜪ")]:
              bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᜫ")][bstack111l111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᜬ")][bstack111l111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᜭ")].append(ext)
        if bstack111l111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᜮ") in bstack11ll11ll1l1_opy_:
          if bstack111l111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᜯ") not in bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᜰ")][bstack111l111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᜱ")]:
            bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᜲ")][bstack111l111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᜳ")][bstack111l111_opy_ (u"ࠫࡵࡸࡥࡧࡵ᜴ࠪ")] = {}
          bstack11ll11lllll_opy_(bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ᜵")][bstack111l111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ᜶")][bstack111l111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭᜷")],
                    bstack11ll11ll1l1_opy_[bstack111l111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ᜸")])
        os.environ[bstack111l111_opy_ (u"ࠩࡌࡗࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡆࡕࡖࡍࡔࡔࠧ᜹")] = bstack111l111_opy_ (u"ࠪࡸࡷࡻࡥࠨ᜺")
        return bstack1l1lll1l11_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l1lll1l11_opy_, ChromeOptions):
          chrome_options = bstack1l1lll1l11_opy_
        elif isinstance(bstack1l1lll1l11_opy_, dict):
          for value in bstack1l1lll1l11_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l1lll1l11_opy_, dict):
            bstack1l1lll1l11_opy_[bstack111l111_opy_ (u"ࠫࡴࡶࡴࡪࡱࡱࡷࠬ᜻")] = chrome_options
          else:
            bstack1l1lll1l11_opy_ = chrome_options
        if bstack11ll11ll1l1_opy_ is not None:
          if bstack111l111_opy_ (u"ࠬࡧࡲࡨࡵࠪ᜼") in bstack11ll11ll1l1_opy_:
                bstack11lll11111l_opy_ = chrome_options.arguments or []
                new_args = bstack11ll11ll1l1_opy_[bstack111l111_opy_ (u"࠭ࡡࡳࡩࡶࠫ᜽")]
                for arg in new_args:
                    if arg not in bstack11lll11111l_opy_:
                        chrome_options.add_argument(arg)
          if bstack111l111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ᜾") in bstack11ll11ll1l1_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack111l111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬ᜿"), [])
                bstack11ll1lll11l_opy_ = bstack11ll11ll1l1_opy_[bstack111l111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᝀ")]
                for extension in bstack11ll1lll11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack111l111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᝁ") in bstack11ll11ll1l1_opy_:
                bstack11ll11llll1_opy_ = chrome_options.experimental_options.get(bstack111l111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᝂ"), {})
                bstack11ll1l1l111_opy_ = bstack11ll11ll1l1_opy_[bstack111l111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᝃ")]
                bstack11ll11lllll_opy_(bstack11ll11llll1_opy_, bstack11ll1l1l111_opy_)
                chrome_options.add_experimental_option(bstack111l111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᝄ"), bstack11ll11llll1_opy_)
        os.environ[bstack111l111_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᝅ")] = bstack111l111_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᝆ")
        return bstack1l1lll1l11_opy_
    except Exception as e:
      logger.error(bstack111l111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡࡹ࡫࡭ࡱ࡫ࠠࡢࡦࡧ࡭ࡳ࡭ࠠ࡯ࡱࡱ࠱ࡇ࡙ࠠࡪࡰࡩࡶࡦࠦࡡ࠲࠳ࡼࠤࡨ࡮ࡲࡰ࡯ࡨࠤࡴࡶࡴࡪࡱࡱࡷ࠿ࠦࠢᝇ") + str(e))
      return bstack1l1lll1l11_opy_