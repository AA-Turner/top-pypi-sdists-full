# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l1ll1l111_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1l1lll11_opy_ as bstack11l1l1ll111_opy_, EVENTS
from bstack_utils.bstack1l1111l1ll_opy_ import bstack1l1111l1ll_opy_
from bstack_utils.helper import bstack1111l11l1_opy_, bstack11111l1l11_opy_, bstack1l111111l1_opy_, bstack11l1l11l1ll_opy_, \
  bstack11l1l11ll11_opy_, bstack1l11ll1l1_opy_, get_host_info, bstack11l1l11ll1l_opy_, bstack1l1ll11111_opy_, error_handler, bstack11l1lll111l_opy_, bstack11l1l1ll1l1_opy_, bstack111111lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack111llll1ll_opy_ import get_logger
from bstack_utils.bstack11l111111l_opy_ import bstack11ll111lll_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
from bstack_utils import bstack111llll1ll_opy_
logger = get_logger(__name__)
bstack11l1lll11_opy_ = bstack111llll1ll_opy_.bstack1l11ll11l_opy_(__name__)
bstack11l111111l_opy_ = bstack11ll111lll_opy_()
@error_handler(class_method=False)
def _11l1ll11l11_opy_(driver, bstack1llll1lllll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1111_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪᜤ"): caps.get(bstack1l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᜥ"), None),
        bstack1l1111_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᜦ"): bstack1llll1lllll_opy_.get(bstack1l1111_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᜧ"), None),
        bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᜨ"): caps.get(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᜩ"), None),
        bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᜪ"): caps.get(bstack1l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᜫ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᜬ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᜭ"), None) is None or os.environ[bstack1l1111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᜮ")] == bstack1l1111_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᜯ"):
        return False
    return True
def bstack111ll11l1l_opy_(config):
  return config.get(bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᜰ"), False) or any([p.get(bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᜱ"), False) == True for p in config.get(bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᜲ"), [])])
def bstack11l111l1l_opy_(config, bstack11llll11l1_opy_):
  try:
    bstack11l1ll11ll1_opy_ = config.get(bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᜳ"), False)
    if int(bstack11llll11l1_opy_) < len(config.get(bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹ᜴ࠧ"), [])) and config[bstack1l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨ᜵")][bstack11llll11l1_opy_]:
      bstack11l1ll1l1ll_opy_ = config[bstack1l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩ᜶")][bstack11llll11l1_opy_].get(bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ᜷"), None)
    else:
      bstack11l1ll1l1ll_opy_ = config.get(bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ᜸"), None)
    if bstack11l1ll1l1ll_opy_ != None:
      bstack11l1ll11ll1_opy_ = bstack11l1ll1l1ll_opy_
    bstack11l1l1l1111_opy_ = os.getenv(bstack1l1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᜹")) is not None and len(os.getenv(bstack1l1111_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨ᜺"))) > 0 and os.getenv(bstack1l1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩ᜻")) != bstack1l1111_opy_ (u"ࠬࡴࡵ࡭࡮ࠪ᜼")
    return bstack11l1ll11ll1_opy_ and bstack11l1l1l1111_opy_
  except Exception as error:
    logger.debug(bstack1l1111_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭᜽") + str(error))
  return False
def bstack1lllll11ll_opy_(test_tags):
  bstack1l1lllll1l1_opy_ = os.getenv(bstack1l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ᜾"))
  if bstack1l1lllll1l1_opy_ is None:
    return True
  bstack1l1lllll1l1_opy_ = json.loads(bstack1l1lllll1l1_opy_)
  try:
    include_tags = bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭᜿")] if bstack1l1111_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᝀ") in bstack1l1lllll1l1_opy_ and isinstance(bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᝁ")], list) else []
    exclude_tags = bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᝂ")] if bstack1l1111_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᝃ") in bstack1l1lllll1l1_opy_ and isinstance(bstack1l1lllll1l1_opy_[bstack1l1111_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᝄ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᝅ") + str(error))
  return False
def bstack11l1lll1111_opy_(config, bstack11l1l1l1ll1_opy_, bstack11l1l11l11l_opy_, bstack11l1ll1l1l1_opy_):
  bstack11l1l1ll1ll_opy_ = bstack11l1l11l1ll_opy_(config)
  bstack11l1l1l111l_opy_ = bstack11l1l11ll11_opy_(config)
  if bstack11l1l1ll1ll_opy_ is None or bstack11l1l1l111l_opy_ is None:
    logger.error(bstack1l1111_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᝆ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᝇ"), bstack1l1111_opy_ (u"ࠪࡿࢂ࠭ᝈ")))
    data = {
        bstack1l1111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᝉ"): config[bstack1l1111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᝊ")],
        bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᝋ"): config.get(bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᝌ"), os.path.basename(os.getcwd())),
        bstack1l1111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫᝍ"): bstack1111l11l1_opy_(),
        bstack1l1111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᝎ"): config.get(bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᝏ"), bstack1l1111_opy_ (u"ࠫࠬᝐ")),
        bstack1l1111_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᝑ"): {
            bstack1l1111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᝒ"): bstack11l1l1l1ll1_opy_,
            bstack1l1111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᝓ"): bstack11l1l11l11l_opy_,
            bstack1l1111_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ᝔"): __version__,
            bstack1l1111_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫ᝕"): bstack1l1111_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪ᝖"),
            bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ᝗"): bstack1l1111_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧ᝘"),
            bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭᝙"): bstack11l1ll1l1l1_opy_
        },
        bstack1l1111_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ᝚"): settings,
        bstack1l1111_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩ᝛"): bstack11l1l11ll1l_opy_(),
        bstack1l1111_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩ᝜"): bstack1l11ll1l1_opy_(),
        bstack1l1111_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬ᝝"): get_host_info(),
        bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭᝞"): bstack1l111111l1_opy_(config)
    }
    headers = {
        bstack1l1111_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫ᝟"): bstack1l1111_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᝠ"),
    }
    config = {
        bstack1l1111_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᝡ"): (bstack11l1l1ll1ll_opy_, bstack11l1l1l111l_opy_),
        bstack1l1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᝢ"): headers
    }
    response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᝣ"), bstack11l1l1ll111_opy_ + bstack1l1111_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪᝤ"), data, config)
    bstack11l1l1lll1l_opy_ = response.json()
    if bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᝥ")]:
      parsed = json.loads(os.getenv(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᝦ"), bstack1l1111_opy_ (u"࠭ࡻࡾࠩᝧ")))
      parsed[bstack1l1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᝨ")] = bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᝩ")][bstack1l1111_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᝪ")]
      os.environ[bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᝫ")] = json.dumps(parsed)
      bstack1l1111l1ll_opy_.bstack1l1l11lll1_opy_(bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"ࠫࡩࡧࡴࡢࠩᝬ")][bstack1l1111_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭᝭")])
      bstack1l1111l1ll_opy_.bstack11l1ll11lll_opy_(bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"࠭ࡤࡢࡶࡤࠫᝮ")][bstack1l1111_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᝯ")])
      bstack1l1111l1ll_opy_.store()
      return bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᝰ")][bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧ᝱")], bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"ࠪࡨࡦࡺࡡࠨᝲ")][bstack1l1111_opy_ (u"ࠫ࡮ࡪࠧᝳ")]
    else:
      logger.error(bstack1l1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭᝴") + bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧ᝵")])
      if bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᝶")] == bstack1l1111_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪ᝷"):
        for bstack11l1l1l1lll_opy_ in bstack11l1l1lll1l_opy_[bstack1l1111_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩ᝸")]:
          logger.error(bstack11l1l1l1lll_opy_[bstack1l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᝹")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧ᝺") +  str(error))
    return None, None
def bstack11l1l1lllll_opy_():
  if os.getenv(bstack1l1111_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪ᝻")) is None:
    return {
        bstack1l1111_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭᝼"): bstack1l1111_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭᝽"),
        bstack1l1111_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩ᝾"): bstack1l1111_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨ᝿")
    }
  data = {bstack1l1111_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫក"): bstack1111l11l1_opy_()}
  headers = {
      bstack1l1111_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫខ"): bstack1l1111_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭គ") + os.getenv(bstack1l1111_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦឃ")),
      bstack1l1111_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ង"): bstack1l1111_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫច")
  }
  response = bstack1l1ll11111_opy_(bstack1l1111_opy_ (u"ࠩࡓ࡙࡙࠭ឆ"), bstack11l1l1ll111_opy_ + bstack1l1111_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬជ"), data, { bstack1l1111_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬឈ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1111_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨញ") + bstack11111l1l11_opy_().isoformat() + bstack1l1111_opy_ (u"࡚࠭ࠨដ"))
      return {bstack1l1111_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧឋ"): bstack1l1111_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩឌ"), bstack1l1111_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪឍ"): bstack1l1111_opy_ (u"ࠪࠫណ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢត") + str(error))
    return {
        bstack1l1111_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬថ"): bstack1l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬទ"),
        bstack1l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨធ"): str(error)
    }
def bstack11l1l1llll1_opy_(bstack11l1l1l11ll_opy_):
    return re.match(bstack1l1111_opy_ (u"ࡳࠩࡡࡠࡩ࠱ࠨ࡝࠰࡟ࡨ࠰࠯࠿ࠥࠩន"), bstack11l1l1l11ll_opy_.strip()) is not None
def bstack111l11111_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l1l1l1l11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l1l1l1l11_opy_ = desired_capabilities
        else:
          bstack11l1l1l1l11_opy_ = {}
        bstack1l1ll111l11_opy_ = (bstack11l1l1l1l11_opy_.get(bstack1l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨប"), bstack1l1111_opy_ (u"ࠪࠫផ")).lower() or caps.get(bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪព"), bstack1l1111_opy_ (u"ࠬ࠭ភ")).lower())
        if bstack1l1ll111l11_opy_ == bstack1l1111_opy_ (u"࠭ࡩࡰࡵࠪម"):
            return True
        if bstack1l1ll111l11_opy_ == bstack1l1111_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨយ"):
            bstack1l1ll11llll_opy_ = str(float(caps.get(bstack1l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪរ")) or bstack11l1l1l1l11_opy_.get(bstack1l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪល"), {}).get(bstack1l1111_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭វ"),bstack1l1111_opy_ (u"ࠫࠬឝ"))))
            if bstack1l1ll111l11_opy_ == bstack1l1111_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ឞ") and int(bstack1l1ll11llll_opy_.split(bstack1l1111_opy_ (u"࠭࠮ࠨស"))[0]) < float(bstack11l1ll1ll1l_opy_):
                logger.warning(str(bstack11l1l1ll11l_opy_))
                return False
            return True
        bstack1l1llll1lll_opy_ = caps.get(bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨហ"), {}).get(bstack1l1111_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬឡ"), caps.get(bstack1l1111_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩអ"), bstack1l1111_opy_ (u"ࠪࠫឣ")))
        if bstack1l1llll1lll_opy_:
            logger.warning(bstack1l1111_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣឤ"))
            return False
        browser = caps.get(bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪឥ"), bstack1l1111_opy_ (u"࠭ࠧឦ")).lower() or bstack11l1l1l1l11_opy_.get(bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬឧ"), bstack1l1111_opy_ (u"ࠨࠩឨ")).lower()
        if browser != bstack1l1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩឩ"):
            logger.warning(bstack1l1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨឪ"))
            return False
        browser_version = caps.get(bstack1l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬឫ")) or caps.get(bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧឬ")) or bstack11l1l1l1l11_opy_.get(bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧឭ")) or bstack11l1l1l1l11_opy_.get(bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨឮ"), {}).get(bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩឯ")) or bstack11l1l1l1l11_opy_.get(bstack1l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪឰ"), {}).get(bstack1l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬឱ"))
        bstack1l1lllll1ll_opy_ = bstack11l1ll1l111_opy_.bstack1l1llll11l1_opy_
        bstack11l1l1l11l1_opy_ = False
        if config is not None:
          bstack11l1l1l11l1_opy_ = bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨឲ") in config and str(config[bstack1l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩឳ")]).lower() != bstack1l1111_opy_ (u"࠭ࡦࡢ࡮ࡶࡩࠬ឴")
        if os.environ.get(bstack1l1111_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ឵"), bstack1l1111_opy_ (u"ࠨࠩា")).lower() == bstack1l1111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧិ") or bstack11l1l1l11l1_opy_:
          bstack1l1lllll1ll_opy_ = bstack11l1ll1l111_opy_.bstack1l1ll11ll11_opy_
        if browser_version and browser_version != bstack1l1111_opy_ (u"ࠪࡰࡦࡺࡥࡴࡶࠪី") and int(browser_version.split(bstack1l1111_opy_ (u"ࠫ࠳࠭ឹ"))[0]) <= bstack1l1lllll1ll_opy_:
          logger.warning(bstack1ll1ll1l1ll_opy_ (u"ࠬࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡨࡴࡨࡥࡹ࡫ࡲࠡࡶ࡫ࡥࡳࠦࡻ࡮࡫ࡱࡣࡦ࠷࠱ࡺࡡࡶࡹࡵࡶ࡯ࡳࡶࡨࡨࡤࡩࡨࡳࡱࡰࡩࡤࡼࡥࡳࡵ࡬ࡳࡳࢃ࠮ࠨឺ"))
          return False
        if not options:
          bstack1l1ll1111l1_opy_ = caps.get(bstack1l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫុ")) or bstack11l1l1l1l11_opy_.get(bstack1l1111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬូ"), {})
          if bstack1l1111_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬួ") in bstack1l1ll1111l1_opy_.get(bstack1l1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧើ"), []):
              logger.warning(bstack1l1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡴ࡯ࡵࠢࡵࡹࡳࠦ࡯࡯ࠢ࡯ࡩ࡬ࡧࡣࡺࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠣࡗࡼ࡯ࡴࡤࡪࠣࡸࡴࠦ࡮ࡦࡹࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧࠣࡳࡷࠦࡡࡷࡱ࡬ࡨࠥࡻࡳࡪࡰࡪࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨ࠲ࠧឿ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack1l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡦࡲࡩࡥࡣࡷࡩࠥࡧ࠱࠲ࡻࠣࡷࡺࡶࡰࡰࡴࡷࠤ࠿ࠨៀ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1ll11l11l1l_opy_ = config.get(bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬេ"), {})
    bstack1ll11l11l1l_opy_[bstack1l1111_opy_ (u"࠭ࡡࡶࡶ࡫ࡘࡴࡱࡥ࡯ࠩែ")] = os.getenv(bstack1l1111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬៃ"))
    bstack11l1l11lll1_opy_ = json.loads(os.getenv(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩោ"), bstack1l1111_opy_ (u"ࠩࡾࢁࠬៅ"))).get(bstack1l1111_opy_ (u"ࠪࡷࡨࡧ࡮࡯ࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫំ"))
    if not config[bstack1l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ះ")].get(bstack1l1111_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦៈ")):
      if bstack1l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ៉") in caps:
        caps[bstack1l1111_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨ៊")][bstack1l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ់")] = bstack1ll11l11l1l_opy_
        caps[bstack1l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪ៌")][bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪ៍")][bstack1l1111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬ៎")] = bstack11l1l11lll1_opy_
      else:
        caps[bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫ៏")] = bstack1ll11l11l1l_opy_
        caps[bstack1l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ័")][bstack1l1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨ៑")] = bstack11l1l11lll1_opy_
  except Exception as error:
    logger.debug(bstack1l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤ្") +  str(error))
def bstack111l11l1ll_opy_(driver, bstack11l1ll1llll_opy_):
  try:
    setattr(driver, bstack1l1111_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩ៓"), True)
    session = driver.session_id
    if session:
      bstack11l1l11l111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l1l11l111_opy_ = False
      bstack11l1l11l111_opy_ = url.scheme in [bstack1l1111_opy_ (u"ࠥ࡬ࡹࡺࡰࠣ។"), bstack1l1111_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥ៕")]
      if bstack11l1l11l111_opy_:
        if bstack11l1ll1llll_opy_:
          logger.info(bstack1l1111_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧ៖"))
      return bstack11l1ll1llll_opy_
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤៗ") + str(e))
    return False
def bstack111ll1ll1_opy_(driver, name, path):
  try:
    bstack1l1lll11ll1_opy_ = {
        bstack1l1111_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧ៘"): threading.current_thread().current_test_uuid,
        bstack1l1111_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭៙"): os.environ.get(bstack1l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧ៚"), bstack1l1111_opy_ (u"ࠪࠫ៛")),
        bstack1l1111_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨៜ"): os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩ៝"), bstack1l1111_opy_ (u"࠭ࠧ៞"))
    }
    bstack1ll1111lll_opy_ = bstack11l111111l_opy_.bstack111llllll_opy_(EVENTS.bstack11l1l1llll_opy_.value)
    logger.debug(bstack1l1111_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪ៟"))
    try:
      if (bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨ០"), None) and bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ១"), None)):
        scripts = {bstack1l1111_opy_ (u"ࠪࡷࡨࡧ࡮ࠨ២"): bstack1l1111l1ll_opy_.perform_scan}
        bstack11l1ll111l1_opy_ = json.loads(scripts[bstack1l1111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ៣")].replace(bstack1l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣ៤"), bstack1l1111_opy_ (u"ࠨࠢ៥")))
        bstack11l1ll111l1_opy_[bstack1l1111_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪ៦")][bstack1l1111_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨ៧")] = None
        scripts[bstack1l1111_opy_ (u"ࠤࡶࡧࡦࡴࠢ៨")] = bstack1l1111_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨ៩") + json.dumps(bstack11l1ll111l1_opy_)
        bstack1l1111l1ll_opy_.bstack1l1l11lll1_opy_(scripts)
        bstack1l1111l1ll_opy_.store()
        logger.debug(driver.execute_script(bstack1l1111l1ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1111l1ll_opy_.perform_scan, {bstack1l1111_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦ៪"): name}))
      bstack11l111111l_opy_.end(EVENTS.bstack11l1l1llll_opy_.value, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧ៫"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦ៬"), True, None)
    except Exception as error:
      bstack11l111111l_opy_.end(EVENTS.bstack11l1l1llll_opy_.value, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢ៭"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠣ࠼ࡨࡲࡩࠨ៮"), False, str(error))
    bstack1ll1111lll_opy_ = bstack11l111111l_opy_.bstack11l1ll11111_opy_(EVENTS.bstack1l1lllll111_opy_.value)
    bstack11l111111l_opy_.mark(bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤ៯"))
    try:
      if (bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪ៰"), None) and bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭៱"), None)):
        scripts = {bstack1l1111_opy_ (u"ࠬࡹࡣࡢࡰࠪ៲"): bstack1l1111l1ll_opy_.perform_scan}
        bstack11l1ll111l1_opy_ = json.loads(scripts[bstack1l1111_opy_ (u"ࠨࡳࡤࡣࡱࠦ៳")].replace(bstack1l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥ៴"), bstack1l1111_opy_ (u"ࠣࠤ៵")))
        bstack11l1ll111l1_opy_[bstack1l1111_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬ៶")][bstack1l1111_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪ៷")] = None
        scripts[bstack1l1111_opy_ (u"ࠦࡸࡩࡡ࡯ࠤ៸")] = bstack1l1111_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣ៹") + json.dumps(bstack11l1ll111l1_opy_)
        bstack1l1111l1ll_opy_.bstack1l1l11lll1_opy_(scripts)
        bstack1l1111l1ll_opy_.store()
        logger.debug(driver.execute_script(bstack1l1111l1ll_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1111l1ll_opy_.bstack11l1l1l1l1l_opy_, bstack1l1lll11ll1_opy_))
      bstack11l111111l_opy_.end(bstack1ll1111lll_opy_, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨ៺"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠢ࠻ࡧࡱࡨࠧ៻"),True, None)
    except Exception as error:
      bstack11l111111l_opy_.end(bstack1ll1111lll_opy_, bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣ៼"), bstack1ll1111lll_opy_ + bstack1l1111_opy_ (u"ࠤ࠽ࡩࡳࡪࠢ៽"),False, str(error))
    logger.info(bstack1l1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨ៾"))
    try:
      bstack1l1lll1llll_opy_ = {
        bstack1l1111_opy_ (u"ࠦࡷ࡫ࡱࡶࡧࡶࡸࠧ៿"): {
          bstack1l1111_opy_ (u"ࠧࡩ࡯࡮࡯ࡤࡲࡩࠨ᠀"): bstack1l1111_opy_ (u"ࠨࡁ࠲࠳࡜ࡣࡘࡇࡖࡆࡡࡕࡉࡘ࡛ࡌࡕࡕࠥ᠁"),
        },
        bstack1l1111_opy_ (u"ࠢࡳࡧࡶࡴࡴࡴࡳࡦࠤ᠂"): {
          bstack1l1111_opy_ (u"ࠣࡤࡲࡨࡾࠨ᠃"): {
            bstack1l1111_opy_ (u"ࠤࡰࡷ࡬ࠨ᠄"): bstack1l1111_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨ᠅"),
            bstack1l1111_opy_ (u"ࠦࡸࡻࡣࡤࡧࡶࡷࠧ᠆"): True
          }
        }
      }
      bstack11l1lll11_opy_.info(json.dumps(bstack1l1lll1llll_opy_, separators=(bstack1l1111_opy_ (u"ࠬ࠲ࠧ᠇"), bstack1l1111_opy_ (u"࠭࠺ࠨ᠈"))))
    except Exception as bstack1l1l111111_opy_:
      logger.debug(bstack1l1111_opy_ (u"ࠢࡇࡣ࡬ࡰࡪࡪࠠࡵࡱࠣࡰࡴ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡴࡣࡹࡩࠥࡸࡥࡴࡷ࡯ࡸࡸࠦࡤࡢࡶࡤ࠾ࠥࠨ᠉") + str(bstack1l1l111111_opy_) + bstack1l1111_opy_ (u"ࠣࠤ᠊"))
  except Exception as bstack1l1ll1111ll_opy_:
    logger.error(bstack1l1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡵࡩࡸࡻ࡬ࡵࡵࠣࡧࡴࡻ࡬ࡥࠢࡱࡳࡹࠦࡢࡦࠢࡳࡶࡴࡩࡥࡴࡵࡨࡨࠥ࡬࡯ࡳࠢࡷ࡬ࡪࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦ᠋") + str(path) + bstack1l1111_opy_ (u"ࠥࠤࡊࡸࡲࡰࡴࠣ࠾ࠧ᠌") + str(bstack1l1ll1111ll_opy_))
def bstack11l1ll1ll11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥ᠍")) and str(caps.get(bstack1l1111_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡎࡢ࡯ࡨࠦ᠎"))).lower() == bstack1l1111_opy_ (u"ࠨࡡ࡯ࡦࡵࡳ࡮ࡪࠢ᠏"):
        bstack1l1ll11llll_opy_ = caps.get(bstack1l1111_opy_ (u"ࠢࡢࡲࡳ࡭ࡺࡳ࠺ࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤ᠐")) or caps.get(bstack1l1111_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠥ᠑"))
        if bstack1l1ll11llll_opy_ and int(str(bstack1l1ll11llll_opy_)) < bstack11l1ll1ll1l_opy_:
            return False
    return True
def bstack1lll1111ll_opy_(config):
  if bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ᠒") in config:
        return config[bstack1l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ᠓")]
  for platform in config.get(bstack1l1111_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧ᠔"), []):
      if bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ᠕") in platform:
          return platform[bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭᠖")]
  return None
def bstack11lll1l1l_opy_(bstack1ll1111l11_opy_):
  try:
    browser_name = bstack1ll1111l11_opy_[bstack1l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡰࡤࡱࡪ࠭᠗")]
    browser_version = bstack1ll1111l11_opy_[bstack1l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪ᠘")]
    chrome_options = bstack1ll1111l11_opy_[bstack1l1111_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࡡࡲࡴࡹ࡯࡯࡯ࡵࠪ᠙")]
    try:
        bstack11l1ll11l1l_opy_ = int(browser_version.split(bstack1l1111_opy_ (u"ࠪ࠲ࠬ᠚"))[0])
    except ValueError as e:
        logger.error(bstack1l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡦࡳࡳࡼࡥࡳࡶ࡬ࡲ࡬ࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠣ᠛") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack1l1111_opy_ (u"ࠬࡩࡨࡳࡱࡰࡩࠬ᠜")):
        logger.warning(bstack1l1111_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࡳ࠯ࠤ᠝"))
        return False
    if bstack11l1ll11l1l_opy_ < bstack11l1ll1l111_opy_.bstack1l1ll11ll11_opy_:
        logger.warning(bstack1ll1ll1l1ll_opy_ (u"ࠧࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡷ࡫ࡱࡶ࡫ࡵࡩࡸࠦࡃࡩࡴࡲࡱࡪࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡼࡅࡒࡒࡘ࡚ࡁࡏࡖࡖ࠲ࡒࡏࡎࡊࡏࡘࡑࡤࡔࡏࡏࡡࡅࡗ࡙ࡇࡃࡌࡡࡌࡒࡋࡘࡁࡠࡃ࠴࠵࡞ࡥࡓࡖࡒࡓࡓࡗ࡚ࡅࡅࡡࡆࡌࡗࡕࡍࡆࡡ࡙ࡉࡗ࡙ࡉࡐࡐࢀࠤࡴࡸࠠࡩ࡫ࡪ࡬ࡪࡸ࠮ࠨ᠞"))
        return False
    if chrome_options and any(bstack1l1111_opy_ (u"ࠨ࠯࠰࡬ࡪࡧࡤ࡭ࡧࡶࡷࠬ᠟") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack1l1111_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᠠ"))
        return False
    return True
  except Exception as e:
    logger.error(bstack1l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢ࡬ࡲࠥࡩࡨࡦࡥ࡮࡭ࡳ࡭ࠠࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࠢࡶࡹࡵࡶ࡯ࡳࡶࠣࡪࡴࡸࠠ࡭ࡱࡦࡥࡱࠦࡃࡩࡴࡲࡱࡪࡀࠠࠣᠡ") + str(e))
    return False
def bstack1l1l1l11l1_opy_(bstack1111l111l_opy_, config):
    try:
      bstack1l1ll11l111_opy_ = bstack1l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᠢ") in config and config[bstack1l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᠣ")] == True
      bstack11l1l1l11l1_opy_ = bstack1l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪᠤ") in config and str(config[bstack1l1111_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫᠥ")]).lower() != bstack1l1111_opy_ (u"ࠨࡨࡤࡰࡸ࡫ࠧᠦ")
      if not (bstack1l1ll11l111_opy_ and (not bstack1l111111l1_opy_(config) or bstack11l1l1l11l1_opy_)):
        return bstack1111l111l_opy_
      bstack11l1ll111ll_opy_ = bstack1l1111l1ll_opy_.bstack11l1ll1111l_opy_
      if bstack11l1ll111ll_opy_ is None:
        logger.debug(bstack1l1111_opy_ (u"ࠤࡊࡳࡴ࡭࡬ࡦࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵࠣࡥࡷ࡫ࠠࡏࡱࡱࡩࠧᠧ"))
        return bstack1111l111l_opy_
      bstack11l1l11l1l1_opy_ = int(str(bstack11l1l1ll1l1_opy_()).split(bstack1l1111_opy_ (u"ࠪ࠲ࠬᠨ"))[0])
      logger.debug(bstack1l1111_opy_ (u"ࠦࡘ࡫࡬ࡦࡰ࡬ࡹࡲࠦࡶࡦࡴࡶ࡭ࡴࡴࠠࡥࡧࡷࡩࡨࡺࡥࡥ࠼ࠣࠦᠩ") + str(bstack11l1l11l1l1_opy_) + bstack1l1111_opy_ (u"ࠧࠨᠪ"))
      if bstack11l1l11l1l1_opy_ == 3 and isinstance(bstack1111l111l_opy_, dict) and bstack1l1111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᠫ") in bstack1111l111l_opy_ and bstack11l1ll111ll_opy_ is not None:
        if bstack1l1111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᠬ") not in bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᠭ")]:
          bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠩࡧࡩࡸ࡯ࡲࡦࡦࡢࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴࠩᠮ")][bstack1l1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨᠯ")] = {}
        if bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩᠰ") in bstack11l1ll111ll_opy_:
          if bstack1l1111_opy_ (u"ࠬࡧࡲࡨࡵࠪᠱ") not in bstack1111l111l_opy_[bstack1l1111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᠲ")][bstack1l1111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᠳ")]:
            bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᠴ")][bstack1l1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᠵ")][bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᠶ")] = []
          for arg in bstack11l1ll111ll_opy_[bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩᠷ")]:
            if arg not in bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᠸ")][bstack1l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᠹ")][bstack1l1111_opy_ (u"ࠧࡢࡴࡪࡷࠬᠺ")]:
              bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᠻ")][bstack1l1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᠼ")][bstack1l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᠽ")].append(arg)
        if bstack1l1111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᠾ") in bstack11l1ll111ll_opy_:
          if bstack1l1111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩᠿ") not in bstack1111l111l_opy_[bstack1l1111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᡀ")][bstack1l1111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᡁ")]:
            bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᡂ")][bstack1l1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡃ")][bstack1l1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᡄ")] = []
          for ext in bstack11l1ll111ll_opy_[bstack1l1111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨᡅ")]:
            if ext not in bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬᡆ")][bstack1l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᡇ")][bstack1l1111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᡈ")]:
              bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᡉ")][bstack1l1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡊ")][bstack1l1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧᡋ")].append(ext)
        if bstack1l1111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᡌ") in bstack11l1ll111ll_opy_:
          if bstack1l1111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᡍ") not in bstack1111l111l_opy_[bstack1l1111_opy_ (u"࠭ࡤࡦࡵ࡬ࡶࡪࡪ࡟ࡤࡣࡳࡥࡧ࡯࡬ࡪࡶ࡬ࡩࡸ࠭ᡎ")][bstack1l1111_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᡏ")]:
            bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨᡐ")][bstack1l1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧᡑ")][bstack1l1111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᡒ")] = {}
          bstack11l1lll111l_opy_(bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫᡓ")][bstack1l1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᡔ")][bstack1l1111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬᡕ")],
                    bstack11l1ll111ll_opy_[bstack1l1111_opy_ (u"ࠧࡱࡴࡨࡪࡸ࠭ᡖ")])
        os.environ[bstack1l1111_opy_ (u"ࠨࡋࡖࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡅࡔࡕࡌࡓࡓ࠭ᡗ")] = bstack1l1111_opy_ (u"ࠩࡷࡶࡺ࡫ࠧᡘ")
        return bstack1111l111l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1111l111l_opy_, ChromeOptions):
          chrome_options = bstack1111l111l_opy_
        elif isinstance(bstack1111l111l_opy_, dict):
          for value in bstack1111l111l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1111l111l_opy_, dict):
            bstack1111l111l_opy_[bstack1l1111_opy_ (u"ࠪࡳࡵࡺࡩࡰࡰࡶࠫᡙ")] = chrome_options
          else:
            bstack1111l111l_opy_ = chrome_options
        if bstack11l1ll111ll_opy_ is not None:
          if bstack1l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩᡚ") in bstack11l1ll111ll_opy_:
                bstack11l1l111lll_opy_ = chrome_options.arguments or []
                new_args = bstack11l1ll111ll_opy_[bstack1l1111_opy_ (u"ࠬࡧࡲࡨࡵࠪᡛ")]
                for arg in new_args:
                    if arg not in bstack11l1l111lll_opy_:
                        chrome_options.add_argument(arg)
          if bstack1l1111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪᡜ") in bstack11l1ll111ll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack1l1111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫᡝ"), [])
                bstack11l1ll1l11l_opy_ = bstack11l1ll111ll_opy_[bstack1l1111_opy_ (u"ࠨࡧࡻࡸࡪࡴࡳࡪࡱࡱࡷࠬᡞ")]
                for extension in bstack11l1ll1l11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack1l1111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨᡟ") in bstack11l1ll111ll_opy_:
                bstack11l1ll1lll1_opy_ = chrome_options.experimental_options.get(bstack1l1111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩᡠ"), {})
                bstack11l1l11llll_opy_ = bstack11l1ll111ll_opy_[bstack1l1111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪᡡ")]
                bstack11l1lll111l_opy_(bstack11l1ll1lll1_opy_, bstack11l1l11llll_opy_)
                chrome_options.add_experimental_option(bstack1l1111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫᡢ"), bstack11l1ll1lll1_opy_)
        os.environ[bstack1l1111_opy_ (u"࠭ࡉࡔࡡࡑࡓࡓࡥࡂࡔࡖࡄࡇࡐࡥࡉࡏࡈࡕࡅࡤࡇ࠱࠲࡛ࡢࡗࡊ࡙ࡓࡊࡑࡑࠫᡣ")] = bstack1l1111_opy_ (u"ࠧࡵࡴࡸࡩࠬᡤ")
        return bstack1111l111l_opy_
    except Exception as e:
      logger.error(bstack1l1111_opy_ (u"ࠣࡇࡵࡶࡴࡸࠠࡸࡪ࡬ࡰࡪࠦࡡࡥࡦ࡬ࡲ࡬ࠦ࡮ࡰࡰ࠰ࡆࡘࠦࡩ࡯ࡨࡵࡥࠥࡧ࠱࠲ࡻࠣࡧ࡭ࡸ࡯࡮ࡧࠣࡳࡵࡺࡩࡰࡰࡶ࠾ࠥࠨᡥ") + str(e))
      return bstack1111l111l_opy_