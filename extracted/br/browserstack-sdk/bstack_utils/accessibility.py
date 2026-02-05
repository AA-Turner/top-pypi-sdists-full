# coding: UTF-8
import sys
bstack11111l_opy_ = sys.version_info [0] == 2
bstack1111_opy_ = 2048
bstack11l111l_opy_ = 7
def bstack11l1ll1_opy_ (bstack111ll_opy_):
    global bstack11lll11_opy_
    bstack11111l1_opy_ = ord (bstack111ll_opy_ [-1])
    bstack1l11l1l_opy_ = bstack111ll_opy_ [:-1]
    bstack1111l1_opy_ = bstack11111l1_opy_ % len (bstack1l11l1l_opy_)
    bstack111ll1_opy_ = bstack1l11l1l_opy_ [:bstack1111l1_opy_] + bstack1l11l1l_opy_ [bstack1111l1_opy_:]
    if bstack11111l_opy_:
        bstack1llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    else:
        bstack1llll1_opy_ = str () .join ([chr (ord (char) - bstack1111_opy_ - (bstack111l11_opy_ + bstack11111l1_opy_) % bstack11l111l_opy_) for bstack111l11_opy_, char in enumerate (bstack111ll1_opy_)])
    return eval (bstack1llll1_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l1l1lll11_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1l11l111_opy_ as bstack11l1l11llll_opy_, EVENTS
from bstack_utils.bstack1lll1ll11l_opy_ import bstack1lll1ll11l_opy_
from bstack_utils.helper import bstack1ll1llll11_opy_, bstack11111lllll_opy_, bstack1l1l1111l1_opy_, bstack11l1l1l111l_opy_, \
  bstack11l1ll11111_opy_, bstack11l1lll11l_opy_, get_host_info, bstack11l1ll11lll_opy_, bstack111l11l1ll_opy_, error_handler, bstack11l1ll111ll_opy_, bstack11l1l11l11l_opy_, bstack111ll1l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l1111l1l_opy_ import get_logger
from bstack_utils.bstack11ll1ll111_opy_ import bstack1ll1111ll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import bstack1l1111l1l_opy_
logger = get_logger(__name__)
bstack11llll111_opy_ = bstack1l1111l1l_opy_.bstack11l1111l11_opy_(__name__)
bstack11ll1ll111_opy_ = bstack1ll1111ll_opy_()
@error_handler(class_method=False)
def _11l1ll1lll1_opy_(driver, bstack1llll1lll1l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1ll1_opy_ (u"ࠨࡱࡶࡣࡳࡧ࡭ࡦࠩᜪ"): caps.get(bstack11l1ll1_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᜫ"), None),
        bstack11l1ll1_opy_ (u"ࠪࡳࡸࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᜬ"): bstack1llll1lll1l_opy_.get(bstack11l1ll1_opy_ (u"ࠫࡴࡹࡖࡦࡴࡶ࡭ࡴࡴࠧᜭ"), None),
        bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥ࡮ࡢ࡯ࡨࠫᜮ"): caps.get(bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫᜯ"), None),
        bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᜰ"): caps.get(bstack11l1ll1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᜱ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1ll1_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥ࡯࡮ࠡࡨࡨࡸࡨ࡮ࡩ࡯ࡩࠣࡴࡱࡧࡴࡧࡱࡵࡱࠥࡪࡥࡵࡣ࡬ࡰࡸࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᜲ") + str(error))
  return response
def on():
    if os.environ.get(bstack11l1ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᜳ"), None) is None or os.environ[bstack11l1ll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕ᜴ࠩ")] == bstack11l1ll1_opy_ (u"ࠧࡴࡵ࡭࡮ࠥ᜵"):
        return False
    return True
def bstack111l111l1_opy_(config):
  return config.get(bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᜶"), False) or any([p.get(bstack11l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᜷"), False) == True for p in config.get(bstack11l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫ᜸"), [])])
def bstack1l11l11111_opy_(config, bstack11ll11l1ll_opy_):
  try:
    bstack11l1l1ll1l1_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᜹"), False)
    if int(bstack11ll11l1ll_opy_) < len(config.get(bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᜺"), [])) and config[bstack11l1ll1_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᜻")][bstack11ll11l1ll_opy_]:
      bstack11l1l1lll1l_opy_ = config[bstack11l1ll1_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᜼")][bstack11ll11l1ll_opy_].get(bstack11l1ll1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᜽"), None)
    else:
      bstack11l1l1lll1l_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᜾"), None)
    if bstack11l1l1lll1l_opy_ != None:
      bstack11l1l1ll1l1_opy_ = bstack11l1l1lll1l_opy_
    bstack11l1l1l1l1l_opy_ = os.getenv(bstack11l1ll1_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭᜿")) is not None and len(os.getenv(bstack11l1ll1_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᝀ"))) > 0 and os.getenv(bstack11l1ll1_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᝁ")) != bstack11l1ll1_opy_ (u"ࠫࡳࡻ࡬࡭ࠩᝂ")
    return bstack11l1l1ll1l1_opy_ and bstack11l1l1l1l1l_opy_
  except Exception as error:
    logger.debug(bstack11l1ll1_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻ࡫ࡲࡪࡨࡼ࡭ࡳ࡭ࠠࡵࡪࡨࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡸ࡫ࡳࡴ࡫ࡲࡲࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᝃ") + str(error))
  return False
def bstack1lll1l1lll_opy_(test_tags):
  bstack1l1ll1l111l_opy_ = os.getenv(bstack11l1ll1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᝄ"))
  if bstack1l1ll1l111l_opy_ is None:
    return True
  bstack1l1ll1l111l_opy_ = json.loads(bstack1l1ll1l111l_opy_)
  try:
    include_tags = bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᝅ")] if bstack11l1ll1_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᝆ") in bstack1l1ll1l111l_opy_ and isinstance(bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᝇ")], list) else []
    exclude_tags = bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᝈ")] if bstack11l1ll1_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᝉ") in bstack1l1ll1l111l_opy_ and isinstance(bstack1l1ll1l111l_opy_[bstack11l1ll1_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᝊ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1ll1_opy_ (u"ࠨࡅࡳࡴࡲࡶࠥࡽࡨࡪ࡮ࡨࠤࡻࡧ࡬ࡪࡦࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡫ࡵࡲࠡࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡤࡨࡪࡴࡸࡥࠡࡵࡦࡥࡳࡴࡩ࡯ࡩ࠱ࠤࡊࡸࡲࡰࡴࠣ࠾ࠥࠨᝋ") + str(error))
  return False
def bstack11l1ll111l1_opy_(config, bstack11l1l111lll_opy_, bstack11l1l1l1lll_opy_, bstack11l1l11l1ll_opy_):
  bstack11l1ll1ll1l_opy_ = bstack11l1l1l111l_opy_(config)
  bstack11l1l11ll1l_opy_ = bstack11l1ll11111_opy_(config)
  if bstack11l1ll1ll1l_opy_ is None or bstack11l1l11ll1l_opy_ is None:
    logger.error(bstack11l1ll1_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡹ࡫ࡳࡵࠢࡵࡹࡳࠦࡦࡰࡴࠣࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࡀࠠࡎ࡫ࡶࡷ࡮ࡴࡧࠡࡣࡸࡸ࡭࡫࡮ࡵ࡫ࡦࡥࡹ࡯࡯࡯ࠢࡷࡳࡰ࡫࡮ࠨᝌ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᝍ"), bstack11l1ll1_opy_ (u"ࠩࡾࢁࠬᝎ")))
    data = {
        bstack11l1ll1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᝏ"): config[bstack11l1ll1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᝐ")],
        bstack11l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᝑ"): config.get(bstack11l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᝒ"), os.path.basename(os.getcwd())),
        bstack11l1ll1_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡚ࡩ࡮ࡧࠪᝓ"): bstack1ll1llll11_opy_(),
        bstack11l1ll1_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭᝔"): config.get(bstack11l1ll1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ᝕"), bstack11l1ll1_opy_ (u"ࠪࠫ᝖")),
        bstack11l1ll1_opy_ (u"ࠫࡸࡵࡵࡳࡥࡨࠫ᝗"): {
            bstack11l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ᝘"): bstack11l1l111lll_opy_,
            bstack11l1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ᝙"): bstack11l1l1l1lll_opy_,
            bstack11l1ll1_opy_ (u"ࠧࡴࡦ࡮࡚ࡪࡸࡳࡪࡱࡱࠫ᝚"): __version__,
            bstack11l1ll1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ᝛"): bstack11l1ll1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ᝜"),
            bstack11l1ll1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ᝝"): bstack11l1ll1_opy_ (u"ࠫࡸ࡫࡬ࡦࡰ࡬ࡹࡲ࠭᝞"),
            bstack11l1ll1_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ᝟"): bstack11l1l11l1ll_opy_
        },
        bstack11l1ll1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨᝠ"): settings,
        bstack11l1ll1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡄࡱࡱࡸࡷࡵ࡬ࠨᝡ"): bstack11l1ll11lll_opy_(),
        bstack11l1ll1_opy_ (u"ࠨࡥ࡬ࡍࡳ࡬࡯ࠨᝢ"): bstack11l1lll11l_opy_(),
        bstack11l1ll1_opy_ (u"ࠩ࡫ࡳࡸࡺࡉ࡯ࡨࡲࠫᝣ"): get_host_info(),
        bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬᝤ"): bstack1l1l1111l1_opy_(config)
    }
    headers = {
        bstack11l1ll1_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᝥ"): bstack11l1ll1_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᝦ"),
    }
    config = {
        bstack11l1ll1_opy_ (u"࠭ࡡࡶࡶ࡫ࠫᝧ"): (bstack11l1ll1ll1l_opy_, bstack11l1l11ll1l_opy_),
        bstack11l1ll1_opy_ (u"ࠧࡩࡧࡤࡨࡪࡸࡳࠨᝨ"): headers
    }
    response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"ࠨࡒࡒࡗ࡙࠭ᝩ"), bstack11l1l11llll_opy_ + bstack11l1ll1_opy_ (u"ࠩ࠲ࡺ࠷࠵ࡴࡦࡵࡷࡣࡷࡻ࡮ࡴࠩᝪ"), data, config)
    bstack11l1ll1ll11_opy_ = response.json()
    if bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠪࡷࡺࡩࡣࡦࡵࡶࠫᝫ")]:
      parsed = json.loads(os.getenv(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᝬ"), bstack11l1ll1_opy_ (u"ࠬࢁࡽࠨ᝭")))
      parsed[bstack11l1ll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᝮ")] = bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬᝯ")][bstack11l1ll1_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᝰ")]
      os.environ[bstack11l1ll1_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪ᝱")] = json.dumps(parsed)
      bstack1lll1ll11l_opy_.bstack11ll11l11l_opy_(bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠪࡨࡦࡺࡡࠨᝲ")][bstack11l1ll1_opy_ (u"ࠫࡸࡩࡲࡪࡲࡷࡷࠬᝳ")])
      bstack1lll1ll11l_opy_.bstack11l1l111ll1_opy_(bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠬࡪࡡࡵࡣࠪ᝴")][bstack11l1ll1_opy_ (u"࠭ࡣࡰ࡯ࡰࡥࡳࡪࡳࠨ᝵")])
      bstack1lll1ll11l_opy_.store()
      return bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡣࡷࡥࠬ᝶")][bstack11l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡕࡱ࡮ࡩࡳ࠭᝷")], bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠩࡧࡥࡹࡧࠧ᝸")][bstack11l1ll1_opy_ (u"ࠪ࡭ࡩ࠭᝹")]
    else:
      logger.error(bstack11l1ll1_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡲࡶࡰࡱ࡭ࡳ࡭ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠬ᝺") + bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭᝻")])
      if bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᝼")] == bstack11l1ll1_opy_ (u"ࠧࡊࡰࡹࡥࡱ࡯ࡤࠡࡥࡲࡲ࡫࡯ࡧࡶࡴࡤࡸ࡮ࡵ࡮ࠡࡲࡤࡷࡸ࡫ࡤ࠯ࠩ᝽"):
        for bstack11l1l11lll1_opy_ in bstack11l1ll1ll11_opy_[bstack11l1ll1_opy_ (u"ࠨࡧࡵࡶࡴࡸࡳࠨ᝾")]:
          logger.error(bstack11l1l11lll1_opy_[bstack11l1ll1_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪ᝿")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡸࡵ࡯ࠢࡩࡳࡷࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠦក") +  str(error))
    return None, None
def bstack11l1l1l1ll1_opy_():
  if os.getenv(bstack11l1ll1_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩខ")) is None:
    return {
        bstack11l1ll1_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬគ"): bstack11l1ll1_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬឃ"),
        bstack11l1ll1_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨង"): bstack11l1ll1_opy_ (u"ࠨࡄࡸ࡭ࡱࡪࠠࡤࡴࡨࡥࡹ࡯࡯࡯ࠢ࡫ࡥࡩࠦࡦࡢ࡫࡯ࡩࡩ࠴ࠧច")
    }
  data = {bstack11l1ll1_opy_ (u"ࠩࡨࡲࡩ࡚ࡩ࡮ࡧࠪឆ"): bstack1ll1llll11_opy_()}
  headers = {
      bstack11l1ll1_opy_ (u"ࠪࡅࡺࡺࡨࡰࡴ࡬ࡾࡦࡺࡩࡰࡰࠪជ"): bstack11l1ll1_opy_ (u"ࠫࡇ࡫ࡡࡳࡧࡵࠤࠬឈ") + os.getenv(bstack11l1ll1_opy_ (u"ࠧࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠥញ")),
      bstack11l1ll1_opy_ (u"࠭ࡃࡰࡰࡷࡩࡳࡺ࠭ࡕࡻࡳࡩࠬដ"): bstack11l1ll1_opy_ (u"ࠧࡢࡲࡳࡰ࡮ࡩࡡࡵ࡫ࡲࡲ࠴ࡰࡳࡰࡰࠪឋ")
  }
  response = bstack111l11l1ll_opy_(bstack11l1ll1_opy_ (u"ࠨࡒࡘࡘࠬឌ"), bstack11l1l11llll_opy_ + bstack11l1ll1_opy_ (u"ࠩ࠲ࡸࡪࡹࡴࡠࡴࡸࡲࡸ࠵ࡳࡵࡱࡳࠫឍ"), data, { bstack11l1ll1_opy_ (u"ࠪ࡬ࡪࡧࡤࡦࡴࡶࠫណ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1ll1_opy_ (u"ࠦࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯ࠢࡰࡥࡷࡱࡥࡥࠢࡤࡷࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡫ࡤࠡࡣࡷࠤࠧត") + bstack11111lllll_opy_().isoformat() + bstack11l1ll1_opy_ (u"ࠬࡠࠧថ"))
      return {bstack11l1ll1_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ទ"): bstack11l1ll1_opy_ (u"ࠧࡴࡷࡦࡧࡪࡹࡳࠨធ"), bstack11l1ll1_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩន"): bstack11l1ll1_opy_ (u"ࠩࠪប")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡳࡡࡳ࡭࡬ࡲ࡬ࠦࡣࡰ࡯ࡳࡰࡪࡺࡩࡰࡰࠣࡳ࡫ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡗࡩࡸࡺࠠࡓࡷࡱ࠾ࠥࠨផ") + str(error))
    return {
        bstack11l1ll1_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫព"): bstack11l1ll1_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫភ"),
        bstack11l1ll1_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧម"): str(error)
    }
def bstack11l1l1l11ll_opy_(bstack11l1ll1l1l1_opy_):
    return re.match(bstack11l1ll1_opy_ (u"ࡲࠨࡠ࡟ࡨ࠰࠮࡜࠯࡞ࡧ࠯࠮ࡅࠤࠨយ"), bstack11l1ll1l1l1_opy_.strip()) is not None
def bstack1lll1lll1_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l1ll11l1l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l1ll11l1l_opy_ = desired_capabilities
        else:
          bstack11l1ll11l1l_opy_ = {}
        bstack1l1ll1lllll_opy_ = (bstack11l1ll11l1l_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧរ"), bstack11l1ll1_opy_ (u"ࠩࠪល")).lower() or caps.get(bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩវ"), bstack11l1ll1_opy_ (u"ࠫࠬឝ")).lower())
        if bstack1l1ll1lllll_opy_ == bstack11l1ll1_opy_ (u"ࠬ࡯࡯ࡴࠩឞ"):
            return True
        if bstack1l1ll1lllll_opy_ == bstack11l1ll1_opy_ (u"࠭ࡡ࡯ࡦࡵࡳ࡮ࡪࠧស"):
            bstack1l1llll1111_opy_ = str(float(caps.get(bstack11l1ll1_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠩហ")) or bstack11l1ll11l1l_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩឡ"), {}).get(bstack11l1ll1_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬអ"),bstack11l1ll1_opy_ (u"ࠪࠫឣ"))))
            if bstack1l1ll1lllll_opy_ == bstack11l1ll1_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬឤ") and int(bstack1l1llll1111_opy_.split(bstack11l1ll1_opy_ (u"ࠬ࠴ࠧឥ"))[0]) < float(bstack11l1ll1111l_opy_):
                logger.warning(str(bstack11l1ll11ll1_opy_))
                return False
            return True
        bstack1l1llllll1l_opy_ = caps.get(bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧឦ"), {}).get(bstack11l1ll1_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࡎࡢ࡯ࡨࠫឧ"), caps.get(bstack11l1ll1_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࠨឨ"), bstack11l1ll1_opy_ (u"ࠩࠪឩ")))
        if bstack1l1llllll1l_opy_:
            logger.warning(bstack11l1ll1_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡈࡪࡹ࡫ࡵࡱࡳࠤࡧࡸ࡯ࡸࡵࡨࡶࡸ࠴ࠢឪ"))
            return False
        browser = caps.get(bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩឫ"), bstack11l1ll1_opy_ (u"ࠬ࠭ឬ")).lower() or bstack11l1ll11l1l_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡎࡢ࡯ࡨࠫឭ"), bstack11l1ll1_opy_ (u"ࠧࠨឮ")).lower()
        if browser != bstack11l1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࠨឯ"):
            logger.warning(bstack11l1ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧឰ"))
            return False
        browser_version = caps.get(bstack11l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫឱ")) or caps.get(bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ឲ")) or bstack11l1ll11l1l_opy_.get(bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ឳ")) or bstack11l1ll11l1l_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ឴"), {}).get(bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ឵")) or bstack11l1ll11l1l_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩា"), {}).get(bstack11l1ll1_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫិ"))
        bstack1l1lll1111l_opy_ = bstack11l1l1lll11_opy_.bstack1l1lllll111_opy_
        bstack11l1l1l1111_opy_ = False
        if config is not None:
          bstack11l1l1l1111_opy_ = bstack11l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧី") in config and str(config[bstack11l1ll1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨឹ")]).lower() != bstack11l1ll1_opy_ (u"ࠬ࡬ࡡ࡭ࡵࡨࠫឺ")
        if os.environ.get(bstack11l1ll1_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫុ"), bstack11l1ll1_opy_ (u"ࠧࠨូ")).lower() == bstack11l1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ួ") or bstack11l1l1l1111_opy_:
          bstack1l1lll1111l_opy_ = bstack11l1l1lll11_opy_.bstack1l1ll1l1lll_opy_
        if browser_version and browser_version != bstack11l1ll1_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩើ") and int(browser_version.split(bstack11l1ll1_opy_ (u"ࠪ࠲ࠬឿ"))[0]) <= bstack1l1lll1111l_opy_:
          logger.warning(bstack1ll1ll11l1l_opy_ (u"ࠫࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥࢁ࡭ࡪࡰࡢࡥ࠶࠷ࡹࡠࡵࡸࡴࡵࡵࡲࡵࡧࡧࡣࡨ࡮ࡲࡰ࡯ࡨࡣࡻ࡫ࡲࡴ࡫ࡲࡲࢂ࠴ࠧៀ"))
          return False
        if not options:
          bstack1l1ll111l1l_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪេ")) or bstack11l1ll11l1l_opy_.get(bstack11l1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫែ"), {})
          if bstack11l1ll1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫៃ") in bstack1l1ll111l1l_opy_.get(bstack11l1ll1_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ោ"), []):
              logger.warning(bstack11l1ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦៅ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11l1ll1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧំ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll1l11llll_opy_ = config.get(bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫះ"), {})
    bstack1ll1l11llll_opy_[bstack11l1ll1_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨៈ")] = os.getenv(bstack11l1ll1_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫ៉"))
    bstack11l1l111l11_opy_ = json.loads(os.getenv(bstack11l1ll1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ៊"), bstack11l1ll1_opy_ (u"ࠨࡽࢀࠫ់"))).get(bstack11l1ll1_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪ៌"))
    if not config[bstack11l1ll1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡒࡵࡳࡩࡻࡣࡵࡏࡤࡴࠬ៍")].get(bstack11l1ll1_opy_ (u"ࠦࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠥ៎")):
      if bstack11l1ll1_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭៏") in caps:
        caps[bstack11l1ll1_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ័")][bstack11l1ll1_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧ៑")] = bstack1ll1l11llll_opy_
        caps[bstack11l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴ្ࠩ")][bstack11l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៓")][bstack11l1ll1_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫ។")] = bstack11l1l111l11_opy_
      else:
        caps[bstack11l1ll1_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭࠱ࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ៕")] = bstack1ll1l11llll_opy_
        caps[bstack11l1ll1_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ៖")][bstack11l1ll1_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧៗ")] = bstack11l1l111l11_opy_
  except Exception as error:
    logger.debug(bstack11l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡶࡩࡹࡺࡩ࡯ࡩࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠴ࠠࡆࡴࡵࡳࡷࡀࠠࠣ៘") +  str(error))
def bstack1ll1l1ll1l_opy_(driver, bstack11l1ll11l11_opy_):
  try:
    setattr(driver, bstack11l1ll1_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫ࡂ࠳࠴ࡽࡘ࡮࡯ࡶ࡮ࡧࡗࡨࡧ࡮ࠨ៙"), True)
    session = driver.session_id
    if session:
      bstack11l1ll1l11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1ll1l11l_opy_ = False
      bstack11l1ll1l11l_opy_ = url.scheme in [bstack11l1ll1_opy_ (u"ࠤ࡫ࡸࡹࡶࠢ៚"), bstack11l1ll1_opy_ (u"ࠥ࡬ࡹࡺࡰࡴࠤ៛")]
      if bstack11l1ll1l11l_opy_:
        if bstack11l1ll11l11_opy_:
          logger.info(bstack11l1ll1_opy_ (u"ࠦࡘ࡫ࡴࡶࡲࠣࡪࡴࡸࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡪࡤࡷࠥࡹࡴࡢࡴࡷࡩࡩ࠴ࠠࡂࡷࡷࡳࡲࡧࡴࡦࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡫ࡸࡦࡥࡸࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡢࡦࡩ࡬ࡲࠥࡳ࡯࡮ࡧࡱࡸࡦࡸࡩ࡭ࡻ࠱ࠦៜ"))
      return bstack11l1ll11l11_opy_
  except Exception as e:
    logger.error(bstack11l1ll1_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡸࡺࡡࡳࡶ࡬ࡲ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡡࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡷࡨࡧ࡮ࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣ៝") + str(e))
    return False
def bstack11ll1l111_opy_(driver, name, path):
  try:
    bstack1l1lll11111_opy_ = {
        bstack11l1ll1_opy_ (u"࠭ࡴࡩࡖࡨࡷࡹࡘࡵ࡯ࡗࡸ࡭ࡩ࠭៞"): threading.current_thread().current_test_uuid,
        bstack11l1ll1_opy_ (u"ࠧࡵࡪࡅࡹ࡮ࡲࡤࡖࡷ࡬ࡨࠬ៟"): os.environ.get(bstack11l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡍ࡛ࡂࡠࡗࡘࡍࡉ࠭០"), bstack11l1ll1_opy_ (u"ࠩࠪ១")),
        bstack11l1ll1_opy_ (u"ࠪࡸ࡭ࡐࡷࡵࡖࡲ࡯ࡪࡴࠧ២"): os.environ.get(bstack11l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣࡏ࡝ࡔࠨ៣"), bstack11l1ll1_opy_ (u"ࠬ࠭៤"))
    }
    bstack1lll1llll1_opy_ = bstack11ll1ll111_opy_.bstack11l11l1l_opy_(EVENTS.bstack1l1l11llll_opy_.value)
    logger.debug(bstack11l1ll1_opy_ (u"࠭ࡐࡦࡴࡩࡳࡷࡳࡩ࡯ࡩࠣࡷࡨࡧ࡮ࠡࡤࡨࡪࡴࡸࡥࠡࡵࡤࡺ࡮ࡴࡧࠡࡴࡨࡷࡺࡲࡴࡴࠩ៥"))
    try:
      if (bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧ៦"), None) and bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ៧"), None)):
        scripts = {bstack11l1ll1_opy_ (u"ࠩࡶࡧࡦࡴࠧ៨"): bstack1lll1ll11l_opy_.perform_scan}
        bstack11l1l111l1l_opy_ = json.loads(scripts[bstack11l1ll1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ៩")].replace(bstack11l1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢ៪"), bstack11l1ll1_opy_ (u"ࠧࠨ៫")))
        bstack11l1l111l1l_opy_[bstack11l1ll1_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩ៬")][bstack11l1ll1_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧ៭")] = None
        scripts[bstack11l1ll1_opy_ (u"ࠣࡵࡦࡥࡳࠨ៮")] = bstack11l1ll1_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧ៯") + json.dumps(bstack11l1l111l1l_opy_)
        bstack1lll1ll11l_opy_.bstack11ll11l11l_opy_(scripts)
        bstack1lll1ll11l_opy_.store()
        logger.debug(driver.execute_script(bstack1lll1ll11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1lll1ll11l_opy_.perform_scan, {bstack11l1ll1_opy_ (u"ࠥࡱࡪࡺࡨࡰࡦࠥ៰"): name}))
      bstack11ll1ll111_opy_.end(EVENTS.bstack1l1l11llll_opy_.value, bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦ៱"), bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠧࡀࡥ࡯ࡦࠥ៲"), True, None)
    except Exception as error:
      bstack11ll1ll111_opy_.end(EVENTS.bstack1l1l11llll_opy_.value, bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ៳"), bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ៴"), False, str(error))
    bstack1lll1llll1_opy_ = bstack11ll1ll111_opy_.bstack11l1l11ll11_opy_(EVENTS.bstack1l1ll1llll1_opy_.value)
    bstack11ll1ll111_opy_.mark(bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ៵"))
    try:
      if (bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠩ࡬ࡷࡆࡶࡰࡂ࠳࠴ࡽ࡙࡫ࡳࡵࠩ៶"), None) and bstack111ll1l1_opy_(threading.current_thread(), bstack11l1ll1_opy_ (u"ࠪࡥࡵࡶࡁ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ៷"), None)):
        scripts = {bstack11l1ll1_opy_ (u"ࠫࡸࡩࡡ࡯ࠩ៸"): bstack1lll1ll11l_opy_.perform_scan}
        bstack11l1l111l1l_opy_ = json.loads(scripts[bstack11l1ll1_opy_ (u"ࠧࡹࡣࡢࡰࠥ៹")].replace(bstack11l1ll1_opy_ (u"ࠨࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡤ࡫ࡸࡦࡥࡸࡸࡴࡸ࠺ࠡࠤ៺"), bstack11l1ll1_opy_ (u"ࠢࠣ៻")))
        bstack11l1l111l1l_opy_[bstack11l1ll1_opy_ (u"ࠨࡣࡵ࡫ࡺࡳࡥ࡯ࡶࡶࠫ៼")][bstack11l1ll1_opy_ (u"ࠩࡰࡩࡹ࡮࡯ࡥࠩ៽")] = None
        scripts[bstack11l1ll1_opy_ (u"ࠥࡷࡨࡧ࡮ࠣ៾")] = bstack11l1ll1_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢ៿") + json.dumps(bstack11l1l111l1l_opy_)
        bstack1lll1ll11l_opy_.bstack11ll11l11l_opy_(scripts)
        bstack1lll1ll11l_opy_.store()
        logger.debug(driver.execute_script(bstack1lll1ll11l_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1lll1ll11l_opy_.bstack11l1l1ll11l_opy_, bstack1l1lll11111_opy_))
      bstack11ll1ll111_opy_.end(bstack1lll1llll1_opy_, bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ᠀"), bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ᠁"),True, None)
    except Exception as error:
      bstack11ll1ll111_opy_.end(bstack1lll1llll1_opy_, bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ᠂"), bstack1lll1llll1_opy_ + bstack11l1ll1_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ᠃"),False, str(error))
    logger.info(bstack11l1ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᠄"))
    try:
      bstack1l1l1llll11_opy_ = {
        bstack11l1ll1_opy_ (u"ࠥࡶࡪࡷࡵࡦࡵࡷࠦ᠅"): {
          bstack11l1ll1_opy_ (u"ࠦࡨࡵ࡭࡮ࡣࡱࡨࠧ᠆"): bstack11l1ll1_opy_ (u"ࠧࡇ࠱࠲࡛ࡢࡗࡆ࡜ࡅࡠࡔࡈࡗ࡚ࡒࡔࡔࠤ᠇"),
        },
        bstack11l1ll1_opy_ (u"ࠨࡲࡦࡵࡳࡳࡳࡹࡥࠣ᠈"): {
          bstack11l1ll1_opy_ (u"ࠢࡣࡱࡧࡽࠧ᠉"): {
            bstack11l1ll1_opy_ (u"ࠣ࡯ࡶ࡫ࠧ᠊"): bstack11l1ll1_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡷࡩࡸࡺࡩ࡯ࡩࠣࡪࡴࡸࠠࡵࡪ࡬ࡷࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡪࡤࡷࠥ࡫࡮ࡥࡧࡧ࠲ࠧ᠋"),
            bstack11l1ll1_opy_ (u"ࠥࡷࡺࡩࡣࡦࡵࡶࠦ᠌"): True
          }
        }
      }
      bstack11llll111_opy_.info(json.dumps(bstack1l1l1llll11_opy_, separators=(bstack11l1ll1_opy_ (u"ࠫ࠱࠭᠍"), bstack11l1ll1_opy_ (u"ࠬࡀࠧ᠎"))))
    except Exception as bstack11lll11l_opy_:
      logger.debug(bstack11l1ll1_opy_ (u"ࠨࡆࡢ࡫࡯ࡩࡩࠦࡴࡰࠢ࡯ࡳ࡬ࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡳࡢࡸࡨࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡪࡡࡵࡣ࠽ࠤࠧ᠏") + str(bstack11lll11l_opy_) + bstack11l1ll1_opy_ (u"ࠢࠣ᠐"))
  except Exception as bstack1l1ll1lll11_opy_:
    logger.error(bstack11l1ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥ᠑") + str(path) + bstack11l1ll1_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦ᠒") + str(bstack1l1ll1lll11_opy_))
def bstack11l1l1llll1_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11l1ll1_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤ᠓")) and str(caps.get(bstack11l1ll1_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ᠔"))).lower() == bstack11l1ll1_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨ᠕"):
        bstack1l1llll1111_opy_ = caps.get(bstack11l1ll1_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣ᠖")) or caps.get(bstack11l1ll1_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ᠗"))
        if bstack1l1llll1111_opy_ and int(str(bstack1l1llll1111_opy_)) < bstack11l1ll1111l_opy_:
            return False
    return True
def bstack1lllll111_opy_(config):
  if bstack11l1ll1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᠘") in config:
        return config[bstack11l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᠙")]
  for platform in config.get(bstack11l1ll1_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭᠚"), []):
      if bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ᠛") in platform:
          return platform[bstack11l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᠜")]
  return None
def bstack1llll1l1ll_opy_(bstack1llll1l11_opy_):
  try:
    browser_name = bstack1llll1l11_opy_[bstack11l1ll1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬ᠝")]
    browser_version = bstack1llll1l11_opy_[bstack11l1ll1_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ᠞")]
    chrome_options = bstack1llll1l11_opy_[bstack11l1ll1_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩ᠟")]
    try:
        bstack11l1l1l11l1_opy_ = int(browser_version.split(bstack11l1ll1_opy_ (u"ࠩ࠱ࠫᠠ"))[0])
    except ValueError as e:
        logger.error(bstack11l1ll1_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡲࡻ࡫ࡲࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠢᠡ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11l1ll1_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫᠢ")):
        logger.warning(bstack11l1ll1_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᠣ"))
        return False
    if bstack11l1l1l11l1_opy_ < bstack11l1l1lll11_opy_.bstack1l1ll1l1lll_opy_:
        logger.warning(bstack1ll1ll11l1l_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡪࡴࡨࡷࠥࡉࡨࡳࡱࡰࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡻࡄࡑࡑࡗ࡙ࡇࡎࡕࡕ࠱ࡑࡎࡔࡉࡎࡗࡐࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡕࡑࡒࡒࡖ࡙ࡋࡄࡠࡅࡋࡖࡔࡓࡅࡠࡘࡈࡖࡘࡏࡏࡏࡿࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠧᠤ"))
        return False
    if chrome_options and any(bstack11l1ll1_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᠥ") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11l1ll1_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥᠦ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11l1ll1_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡩࡳࡷࠦ࡬ࡰࡥࡤࡰࠥࡉࡨࡳࡱࡰࡩ࠿ࠦࠢᠧ") + str(e))
    return False
def bstack11lllll1l1_opy_(bstack1l11ll11_opy_, config):
    try:
      bstack1l1llll1lll_opy_ = bstack11l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᠨ") in config and config[bstack11l1ll1_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᠩ")] == True
      bstack11l1l1l1111_opy_ = bstack11l1ll1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩᠪ") in config and str(config[bstack11l1ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᠫ")]).lower() != bstack11l1ll1_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ᠬ")
      if not (bstack1l1llll1lll_opy_ and (not bstack1l1l1111l1_opy_(config) or bstack11l1l1l1111_opy_)):
        return bstack1l11ll11_opy_
      bstack11l1l1l1l11_opy_ = bstack1lll1ll11l_opy_.bstack11l1ll1l111_opy_
      if bstack11l1l1l1l11_opy_ is None:
        logger.debug(bstack11l1ll1_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶࡪࠦࡎࡰࡰࡨࠦᠭ"))
        return bstack1l11ll11_opy_
      bstack11l1l1ll111_opy_ = int(str(bstack11l1l11l11l_opy_()).split(bstack11l1ll1_opy_ (u"ࠩ࠱ࠫᠮ"))[0])
      logger.debug(bstack11l1ll1_opy_ (u"ࠥࡗࡪࡲࡥ࡯࡫ࡸࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࠥᠯ") + str(bstack11l1l1ll111_opy_) + bstack11l1ll1_opy_ (u"ࠦࠧᠰ"))
      if bstack11l1l1ll111_opy_ == 3 and isinstance(bstack1l11ll11_opy_, dict) and bstack11l1ll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᠱ") in bstack1l11ll11_opy_ and bstack11l1l1l1l11_opy_ is not None:
        if bstack11l1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᠲ") not in bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᠳ")]:
          bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᠴ")][bstack11l1ll1_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᠵ")] = {}
        if bstack11l1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᠶ") in bstack11l1l1l1l11_opy_:
          if bstack11l1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩᠷ") not in bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᠸ")][bstack11l1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᠹ")]:
            bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᠺ")][bstack11l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᠻ")][bstack11l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᠼ")] = []
          for arg in bstack11l1l1l1l11_opy_[bstack11l1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᠽ")]:
            if arg not in bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᠾ")][bstack11l1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᠿ")][bstack11l1ll1_opy_ (u"࠭ࡡࡳࡩࡶࠫᡀ")]:
              bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᡁ")][bstack11l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᡂ")][bstack11l1ll1_opy_ (u"ࠩࡤࡶ࡬ࡹࠧᡃ")].append(arg)
        if bstack11l1ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᡄ") in bstack11l1l1l1l11_opy_:
          if bstack11l1ll1_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᡅ") not in bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᡆ")][bstack11l1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᡇ")]:
            bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᡈ")][bstack11l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᡉ")][bstack11l1ll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᡊ")] = []
          for ext in bstack11l1l1l1l11_opy_[bstack11l1ll1_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᡋ")]:
            if ext not in bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡌ")][bstack11l1ll1_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᡍ")][bstack11l1ll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᡎ")]:
              bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᡏ")][bstack11l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᡐ")][bstack11l1ll1_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭ᡑ")].append(ext)
        if bstack11l1ll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᡒ") in bstack11l1l1l1l11_opy_:
          if bstack11l1ll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᡓ") not in bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᡔ")][bstack11l1ll1_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᡕ")]:
            bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧᡖ")][bstack11l1ll1_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᡗ")][bstack11l1ll1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᡘ")] = {}
          bstack11l1ll111ll_opy_(bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪᡙ")][bstack11l1ll1_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩᡚ")][bstack11l1ll1_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᡛ")],
                    bstack11l1l1l1l11_opy_[bstack11l1ll1_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᡜ")])
        os.environ[bstack11l1ll1_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬᡝ")] = bstack11l1ll1_opy_ (u"ࠨࡶࡵࡹࡪ࠭ᡞ")
        return bstack1l11ll11_opy_
      else:
        chrome_options = None
        if isinstance(bstack1l11ll11_opy_, ChromeOptions):
          chrome_options = bstack1l11ll11_opy_
        elif isinstance(bstack1l11ll11_opy_, dict):
          for value in bstack1l11ll11_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1l11ll11_opy_, dict):
            bstack1l11ll11_opy_[bstack11l1ll1_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪᡟ")] = chrome_options
          else:
            bstack1l11ll11_opy_ = chrome_options
        if bstack11l1l1l1l11_opy_ is not None:
          if bstack11l1ll1_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᡠ") in bstack11l1l1l1l11_opy_:
                bstack11l1l11l1l1_opy_ = chrome_options.arguments or []
                new_args = bstack11l1l1l1l11_opy_[bstack11l1ll1_opy_ (u"ࠫࡦࡸࡧࡴࠩᡡ")]
                for arg in new_args:
                    if arg not in bstack11l1l11l1l1_opy_:
                        chrome_options.add_argument(arg)
          if bstack11l1ll1_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᡢ") in bstack11l1l1l1l11_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11l1ll1_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᡣ"), [])
                bstack11l1l1ll1ll_opy_ = bstack11l1l1l1l11_opy_[bstack11l1ll1_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᡤ")]
                for extension in bstack11l1l1ll1ll_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11l1ll1_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧᡥ") in bstack11l1l1l1l11_opy_:
                bstack11l1ll1l1ll_opy_ = chrome_options.experimental_options.get(bstack11l1ll1_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᡦ"), {})
                bstack11l1l1lllll_opy_ = bstack11l1l1l1l11_opy_[bstack11l1ll1_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᡧ")]
                bstack11l1ll111ll_opy_(bstack11l1ll1l1ll_opy_, bstack11l1l1lllll_opy_)
                chrome_options.add_experimental_option(bstack11l1ll1_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᡨ"), bstack11l1ll1l1ll_opy_)
        os.environ[bstack11l1ll1_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪᡩ")] = bstack11l1ll1_opy_ (u"࠭ࡴࡳࡷࡨࠫᡪ")
        return bstack1l11ll11_opy_
    except Exception as e:
      logger.error(bstack11l1ll1_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡴ࡯࡯࠯ࡅࡗࠥ࡯࡮ࡧࡴࡤࠤࡦ࠷࠱ࡺࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧᡫ") + str(e))
      return bstack1l11ll11_opy_