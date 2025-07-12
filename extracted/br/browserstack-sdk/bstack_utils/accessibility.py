# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack11_opy_ = 7
def bstack11l1111_opy_ (bstack111l111_opy_):
    global bstack1l1l11_opy_
    bstack1lll11l_opy_ = ord (bstack111l111_opy_ [-1])
    bstack11l11l1_opy_ = bstack111l111_opy_ [:-1]
    bstack1111lll_opy_ = bstack1lll11l_opy_ % len (bstack11l11l1_opy_)
    bstack11lll11_opy_ = bstack11l11l1_opy_ [:bstack1111lll_opy_] + bstack11l11l1_opy_ [bstack1111lll_opy_:]
    if bstack1l111l_opy_:
        bstack111l11_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    else:
        bstack111l11_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l111ll_opy_ + bstack1lll11l_opy_) % bstack11_opy_) for bstack1l111ll_opy_, char in enumerate (bstack11lll11_opy_)])
    return eval (bstack111l11_opy_)
import os
import json
import requests
import logging
import threading
import bstack_utils.constants as bstack11l11l1ll11_opy_
from urllib.parse import urlparse
from bstack_utils.constants import bstack11l1l11l1ll_opy_ as bstack11l11l1lll1_opy_, EVENTS
from bstack_utils.bstack11llll1111_opy_ import bstack11llll1111_opy_
from bstack_utils.helper import bstack1lllllllll_opy_, bstack111l111lll_opy_, bstack1l11lll1l_opy_, bstack11l11l1llll_opy_, \
  bstack11l11ll111l_opy_, bstack1l1l1l1ll1_opy_, get_host_info, bstack11l11lll1l1_opy_, bstack1lllll1111_opy_, bstack111l11l1l1_opy_, bstack11l11lll111_opy_, bstack11l1l11ll11_opy_, bstack11ll1lll_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l11l1l1l_opy_ import get_logger
from bstack_utils.bstack11lllll1l1_opy_ import bstack1lll1l1l11l_opy_
from selenium.webdriver.chrome.options import Options as ChromeOptions
from browserstack_sdk.sdk_cli.cli import cli
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack11lllll1l1_opy_ = bstack1lll1l1l11l_opy_()
@bstack111l11l1l1_opy_(class_method=False)
def _11l11ll1l1l_opy_(driver, bstack1111l1l11l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11l1111_opy_ (u"࠭࡯ࡴࡡࡱࡥࡲ࡫ࠧᛆ"): caps.get(bstack11l1111_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᛇ"), None),
        bstack11l1111_opy_ (u"ࠨࡱࡶࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᛈ"): bstack1111l1l11l_opy_.get(bstack11l1111_opy_ (u"ࠩࡲࡷ࡛࡫ࡲࡴ࡫ࡲࡲࠬᛉ"), None),
        bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡳࡧ࡭ࡦࠩᛊ"): caps.get(bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᛋ"), None),
        bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᛌ"): caps.get(bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᛍ"), None)
    }
  except Exception as error:
    logger.debug(bstack11l1111_opy_ (u"ࠧࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣ࡭ࡳࠦࡦࡦࡶࡦ࡬࡮ࡴࡧࠡࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࠣࡨࡪࡺࡡࡪ࡮ࡶࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᛎ") + str(error))
  return response
def on():
    if os.environ.get(bstack11l1111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᛏ"), None) is None or os.environ[bstack11l1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᛐ")] == bstack11l1111_opy_ (u"ࠥࡲࡺࡲ࡬ࠣᛑ"):
        return False
    return True
def bstack11l1111lll_opy_(config):
  return config.get(bstack11l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛒ"), False) or any([p.get(bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᛓ"), False) == True for p in config.get(bstack11l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᛔ"), [])])
def bstack1l1ll1l1l1_opy_(config, bstack11llllll11_opy_):
  try:
    bstack11l11lllll1_opy_ = config.get(bstack11l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᛕ"), False)
    if int(bstack11llllll11_opy_) < len(config.get(bstack11l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᛖ"), [])) and config[bstack11l1111_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᛗ")][bstack11llllll11_opy_]:
      bstack11l11ll1111_opy_ = config[bstack11l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᛘ")][bstack11llllll11_opy_].get(bstack11l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᛙ"), None)
    else:
      bstack11l11ll1111_opy_ = config.get(bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᛚ"), None)
    if bstack11l11ll1111_opy_ != None:
      bstack11l11lllll1_opy_ = bstack11l11ll1111_opy_
    bstack11l1l111111_opy_ = os.getenv(bstack11l1111_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᛛ")) is not None and len(os.getenv(bstack11l1111_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᛜ"))) > 0 and os.getenv(bstack11l1111_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᛝ")) != bstack11l1111_opy_ (u"ࠩࡱࡹࡱࡲࠧᛞ")
    return bstack11l11lllll1_opy_ and bstack11l1l111111_opy_
  except Exception as error:
    logger.debug(bstack11l1111_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡩࡷ࡯ࡦࡺ࡫ࡱ࡫ࠥࡺࡨࡦࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡶࡩࡸࡹࡩࡰࡰࠣࡻ࡮ࡺࡨࠡࡧࡵࡶࡴࡸࠠ࠻ࠢࠪᛟ") + str(error))
  return False
def bstack1lll111l1l_opy_(test_tags):
  bstack1l1111111ll_opy_ = os.getenv(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬᛠ"))
  if bstack1l1111111ll_opy_ is None:
    return True
  bstack1l1111111ll_opy_ = json.loads(bstack1l1111111ll_opy_)
  try:
    include_tags = bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"ࠬ࡯࡮ࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᛡ")] if bstack11l1111_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᛢ") in bstack1l1111111ll_opy_ and isinstance(bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᛣ")], list) else []
    exclude_tags = bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"ࠨࡧࡻࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᛤ")] if bstack11l1111_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᛥ") in bstack1l1111111ll_opy_ and isinstance(bstack1l1111111ll_opy_[bstack11l1111_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᛦ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11l1111_opy_ (u"ࠦࡊࡸࡲࡰࡴࠣࡻ࡭࡯࡬ࡦࠢࡹࡥࡱ࡯ࡤࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢࡩࡳࡷࠦࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡢࡦࡨࡲࡶࡪࠦࡳࡤࡣࡱࡲ࡮ࡴࡧ࠯ࠢࡈࡶࡷࡵࡲࠡ࠼ࠣࠦᛧ") + str(error))
  return False
def bstack11l11l11ll1_opy_(config, bstack11l1l11111l_opy_, bstack11l11l11lll_opy_, bstack11l11ll1ll1_opy_):
  bstack11l11ll1l11_opy_ = bstack11l11l1llll_opy_(config)
  bstack11l11ll11ll_opy_ = bstack11l11ll111l_opy_(config)
  if bstack11l11ll1l11_opy_ is None or bstack11l11ll11ll_opy_ is None:
    logger.error(bstack11l1111_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡳࡷࡱࠤ࡫ࡵࡲࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥࡓࡩࡴࡵ࡬ࡲ࡬ࠦࡡࡶࡶ࡫ࡩࡳࡺࡩࡤࡣࡷ࡭ࡴࡴࠠࡵࡱ࡮ࡩࡳ࠭ᛨ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧᛩ"), bstack11l1111_opy_ (u"ࠧࡼࡿࠪᛪ")))
    data = {
        bstack11l1111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭᛫"): config[bstack11l1111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ᛬")],
        bstack11l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡐࡤࡱࡪ࠭᛭"): config.get(bstack11l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᛮ"), os.path.basename(os.getcwd())),
        bstack11l1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡘ࡮ࡳࡥࠨᛯ"): bstack1lllllllll_opy_(),
        bstack11l1111_opy_ (u"࠭ࡤࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᛰ"): config.get(bstack11l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡊࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪᛱ"), bstack11l1111_opy_ (u"ࠨࠩᛲ")),
        bstack11l1111_opy_ (u"ࠩࡶࡳࡺࡸࡣࡦࠩᛳ"): {
            bstack11l1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪᛴ"): bstack11l1l11111l_opy_,
            bstack11l1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧᛵ"): bstack11l11l11lll_opy_,
            bstack11l1111_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩᛶ"): __version__,
            bstack11l1111_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨᛷ"): bstack11l1111_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧᛸ"),
            bstack11l1111_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ᛹"): bstack11l1111_opy_ (u"ࠩࡶࡩࡱ࡫࡮ࡪࡷࡰࠫ᛺"),
            bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ᛻"): bstack11l11ll1ll1_opy_
        },
        bstack11l1111_opy_ (u"ࠫࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸ࠭᛼"): settings,
        bstack11l1111_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡉ࡯࡯ࡶࡵࡳࡱ࠭᛽"): bstack11l11lll1l1_opy_(),
        bstack11l1111_opy_ (u"࠭ࡣࡪࡋࡱࡪࡴ࠭᛾"): bstack1l1l1l1ll1_opy_(),
        bstack11l1111_opy_ (u"ࠧࡩࡱࡶࡸࡎࡴࡦࡰࠩ᛿"): get_host_info(),
        bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪᜀ"): bstack1l11lll1l_opy_(config)
    }
    headers = {
        bstack11l1111_opy_ (u"ࠩࡆࡳࡳࡺࡥ࡯ࡶ࠰ࡘࡾࡶࡥࠨᜁ"): bstack11l1111_opy_ (u"ࠪࡥࡵࡶ࡬ࡪࡥࡤࡸ࡮ࡵ࡮࠰࡬ࡶࡳࡳ࠭ᜂ"),
    }
    config = {
        bstack11l1111_opy_ (u"ࠫࡦࡻࡴࡩࠩᜃ"): (bstack11l11ll1l11_opy_, bstack11l11ll11ll_opy_),
        bstack11l1111_opy_ (u"ࠬ࡮ࡥࡢࡦࡨࡶࡸ࠭ᜄ"): headers
    }
    response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"࠭ࡐࡐࡕࡗࠫᜅ"), bstack11l11l1lll1_opy_ + bstack11l1111_opy_ (u"ࠧ࠰ࡸ࠵࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹࠧᜆ"), data, config)
    bstack11l11l11l1l_opy_ = response.json()
    if bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᜇ")]:
      parsed = json.loads(os.getenv(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᜈ"), bstack11l1111_opy_ (u"ࠪࡿࢂ࠭ᜉ")))
      parsed[bstack11l1111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᜊ")] = bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠬࡪࡡࡵࡣࠪᜋ")][bstack11l1111_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᜌ")]
      os.environ[bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᜍ")] = json.dumps(parsed)
      bstack11llll1111_opy_.bstack11l1l1llll_opy_(bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᜎ")][bstack11l1111_opy_ (u"ࠩࡶࡧࡷ࡯ࡰࡵࡵࠪᜏ")])
      bstack11llll1111_opy_.bstack11l11llll1l_opy_(bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠪࡨࡦࡺࡡࠨᜐ")][bstack11l1111_opy_ (u"ࠫࡨࡵ࡭࡮ࡣࡱࡨࡸ࠭ᜑ")])
      bstack11llll1111_opy_.store()
      return bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠬࡪࡡࡵࡣࠪᜒ")][bstack11l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࡚࡯࡬ࡧࡱࠫᜓ")], bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠧࡥࡣࡷࡥ᜔ࠬ")][bstack11l1111_opy_ (u"ࠨ࡫ࡧ᜕ࠫ")]
    else:
      logger.error(bstack11l1111_opy_ (u"ࠩࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡷࡻ࡮࡯࡫ࡱ࡫ࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠪ᜖") + bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫ᜗")])
      if bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬ᜘")] == bstack11l1111_opy_ (u"ࠬࡏ࡮ࡷࡣ࡯࡭ࡩࠦࡣࡰࡰࡩ࡭࡬ࡻࡲࡢࡶ࡬ࡳࡳࠦࡰࡢࡵࡶࡩࡩ࠴ࠧ᜙"):
        for bstack11l1l111l11_opy_ in bstack11l11l11l1l_opy_[bstack11l1111_opy_ (u"࠭ࡥࡳࡴࡲࡶࡸ࠭᜚")]:
          logger.error(bstack11l1l111l11_opy_[bstack11l1111_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨ᜛")])
      return None, None
  except Exception as error:
    logger.error(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࠤ᜜") +  str(error))
    return None, None
def bstack11l1l11l1l1_opy_():
  if os.getenv(bstack11l1111_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧ᜝")) is None:
    return {
        bstack11l1111_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪ᜞"): bstack11l1111_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᜟ"),
        bstack11l1111_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᜠ"): bstack11l1111_opy_ (u"࠭ࡂࡶ࡫࡯ࡨࠥࡩࡲࡦࡣࡷ࡭ࡴࡴࠠࡩࡣࡧࠤ࡫ࡧࡩ࡭ࡧࡧ࠲ࠬᜡ")
    }
  data = {bstack11l1111_opy_ (u"ࠧࡦࡰࡧࡘ࡮ࡳࡥࠨᜢ"): bstack1lllllllll_opy_()}
  headers = {
      bstack11l1111_opy_ (u"ࠨࡃࡸࡸ࡭ࡵࡲࡪࡼࡤࡸ࡮ࡵ࡮ࠨᜣ"): bstack11l1111_opy_ (u"ࠩࡅࡩࡦࡸࡥࡳࠢࠪᜤ") + os.getenv(bstack11l1111_opy_ (u"ࠥࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠣᜥ")),
      bstack11l1111_opy_ (u"ࠫࡈࡵ࡮ࡵࡧࡱࡸ࠲࡚ࡹࡱࡧࠪᜦ"): bstack11l1111_opy_ (u"ࠬࡧࡰࡱ࡮࡬ࡧࡦࡺࡩࡰࡰ࠲࡮ࡸࡵ࡮ࠨᜧ")
  }
  response = bstack1lllll1111_opy_(bstack11l1111_opy_ (u"࠭ࡐࡖࡖࠪᜨ"), bstack11l11l1lll1_opy_ + bstack11l1111_opy_ (u"ࠧ࠰ࡶࡨࡷࡹࡥࡲࡶࡰࡶ࠳ࡸࡺ࡯ࡱࠩᜩ"), data, { bstack11l1111_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᜪ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11l1111_opy_ (u"ࠤࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࡚ࠥࡥࡴࡶࠣࡖࡺࡴࠠ࡮ࡣࡵ࡯ࡪࡪࠠࡢࡵࠣࡧࡴࡳࡰ࡭ࡧࡷࡩࡩࠦࡡࡵࠢࠥᜫ") + bstack111l111lll_opy_().isoformat() + bstack11l1111_opy_ (u"ࠪ࡞ࠬᜬ"))
      return {bstack11l1111_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᜭ"): bstack11l1111_opy_ (u"ࠬࡹࡵࡤࡥࡨࡷࡸ࠭ᜮ"), bstack11l1111_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᜯ"): bstack11l1111_opy_ (u"ࠧࠨᜰ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡱࡦࡸ࡫ࡪࡰࡪࠤࡨࡵ࡭ࡱ࡮ࡨࡸ࡮ࡵ࡮ࠡࡱࡩࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡕࡧࡶࡸࠥࡘࡵ࡯࠼ࠣࠦᜱ") + str(error))
    return {
        bstack11l1111_opy_ (u"ࠩࡶࡸࡦࡺࡵࡴࠩᜲ"): bstack11l1111_opy_ (u"ࠪࡩࡷࡸ࡯ࡳࠩᜳ"),
        bstack11l1111_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩ᜴ࠬ"): str(error)
    }
def bstack11l11ll11l1_opy_(bstack11l11l1l11l_opy_):
    return re.match(bstack11l1111_opy_ (u"ࡷ࠭࡞࡝ࡦ࠮ࠬࡡ࠴࡜ࡥ࠭ࠬࡃࠩ࠭᜵"), bstack11l11l1l11l_opy_.strip()) is not None
def bstack1l11l11l1l_opy_(caps, options, desired_capabilities={}, config=None):
    try:
        if options:
          bstack11l11l1l1ll_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11l11l1l1ll_opy_ = desired_capabilities
        else:
          bstack11l11l1l1ll_opy_ = {}
        bstack11lllll1lll_opy_ = (bstack11l11l1l1ll_opy_.get(bstack11l1111_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠬ᜶"), bstack11l1111_opy_ (u"ࠧࠨ᜷")).lower() or caps.get(bstack11l1111_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧ᜸"), bstack11l1111_opy_ (u"ࠩࠪ᜹")).lower())
        if bstack11lllll1lll_opy_ == bstack11l1111_opy_ (u"ࠪ࡭ࡴࡹࠧ᜺"):
            return True
        if bstack11lllll1lll_opy_ == bstack11l1111_opy_ (u"ࠫࡦࡴࡤࡳࡱ࡬ࡨࠬ᜻"):
            bstack11lllllllll_opy_ = str(float(caps.get(bstack11l1111_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠧ᜼")) or bstack11l11l1l1ll_opy_.get(bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧ᜽"), {}).get(bstack11l1111_opy_ (u"ࠧࡰࡵ࡙ࡩࡷࡹࡩࡰࡰࠪ᜾"),bstack11l1111_opy_ (u"ࠨࠩ᜿"))))
            if bstack11lllll1lll_opy_ == bstack11l1111_opy_ (u"ࠩࡤࡲࡩࡸ࡯ࡪࡦࠪᝀ") and int(bstack11lllllllll_opy_.split(bstack11l1111_opy_ (u"ࠪ࠲ࠬᝁ"))[0]) < float(bstack11l11l11l11_opy_):
                logger.warning(str(bstack11l11l1ll1l_opy_))
                return False
            return True
        bstack11lllll1ll1_opy_ = caps.get(bstack11l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᝂ"), {}).get(bstack11l1111_opy_ (u"ࠬࡪࡥࡷ࡫ࡦࡩࡓࡧ࡭ࡦࠩᝃ"), caps.get(bstack11l1111_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪ࠭ᝄ"), bstack11l1111_opy_ (u"ࠧࠨᝅ")))
        if bstack11lllll1ll1_opy_:
            logger.warning(bstack11l1111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡆࡨࡷࡰࡺ࡯ࡱࠢࡥࡶࡴࡽࡳࡦࡴࡶ࠲ࠧᝆ"))
            return False
        browser = caps.get(bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡑࡥࡲ࡫ࠧᝇ"), bstack11l1111_opy_ (u"ࠪࠫᝈ")).lower() or bstack11l11l1l1ll_opy_.get(bstack11l1111_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡓࡧ࡭ࡦࠩᝉ"), bstack11l1111_opy_ (u"ࠬ࠭ᝊ")).lower()
        if browser != bstack11l1111_opy_ (u"࠭ࡣࡩࡴࡲࡱࡪ࠭ᝋ"):
            logger.warning(bstack11l1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡵࡹࡳࠦ࡯࡯࡮ࡼࠤࡴࡴࠠࡄࡪࡵࡳࡲ࡫ࠠࡣࡴࡲࡻࡸ࡫ࡲࡴ࠰ࠥᝌ"))
            return False
        browser_version = caps.get(bstack11l1111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᝍ")) or caps.get(bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡢࡺࡪࡸࡳࡪࡱࡱࠫᝎ")) or bstack11l11l1l1ll_opy_.get(bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵ࡚ࡪࡸࡳࡪࡱࡱࠫᝏ")) or bstack11l11l1l1ll_opy_.get(bstack11l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᝐ"), {}).get(bstack11l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᝑ")) or bstack11l11l1l1ll_opy_.get(bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᝒ"), {}).get(bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩᝓ"))
        bstack1l11111l1l1_opy_ = bstack11l11l1ll11_opy_.bstack11lllllll1l_opy_
        bstack11l11l111ll_opy_ = False
        if config is not None:
          bstack11l11l111ll_opy_ = bstack11l1111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ᝔") in config and str(config[bstack11l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭᝕")]).lower() != bstack11l1111_opy_ (u"ࠪࡪࡦࡲࡳࡦࠩ᝖")
        if os.environ.get(bstack11l1111_opy_ (u"ࠫࡎ࡙࡟ࡏࡑࡑࡣࡇ࡙ࡔࡂࡅࡎࡣࡎࡔࡆࡓࡃࡢࡅ࠶࠷࡙ࡠࡕࡈࡗࡘࡏࡏࡏࠩ᝗"), bstack11l1111_opy_ (u"ࠬ࠭᝘")).lower() == bstack11l1111_opy_ (u"࠭ࡴࡳࡷࡨࠫ᝙") or bstack11l11l111ll_opy_:
          bstack1l11111l1l1_opy_ = bstack11l11l1ll11_opy_.bstack11llll1lll1_opy_
        if browser_version and browser_version != bstack11l1111_opy_ (u"ࠧ࡭ࡣࡷࡩࡸࡺࠧ᝚") and int(browser_version.split(bstack11l1111_opy_ (u"ࠨ࠰ࠪ᝛"))[0]) <= bstack1l11111l1l1_opy_:
          logger.warning(bstack1lll1111lll_opy_ (u"ࠩࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡆ࡬ࡷࡵ࡭ࡦࠢࡥࡶࡴࡽࡳࡦࡴࠣࡺࡪࡸࡳࡪࡱࡱࠤ࡬ࡸࡥࡢࡶࡨࡶࠥࡺࡨࡢࡰࠣࡿࡲ࡯࡮ࡠࡣ࠴࠵ࡾࡥࡳࡶࡲࡳࡳࡷࡺࡥࡥࡡࡦ࡬ࡷࡵ࡭ࡦࡡࡹࡩࡷࡹࡩࡰࡰࢀ࠲ࠬ᝜"))
          return False
        if not options:
          bstack11llllll1ll_opy_ = caps.get(bstack11l1111_opy_ (u"ࠪ࡫ࡴࡵࡧ࠻ࡥ࡫ࡶࡴࡳࡥࡐࡲࡷ࡭ࡴࡴࡳࠨ᝝")) or bstack11l11l1l1ll_opy_.get(bstack11l1111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ᝞"), {})
          if bstack11l1111_opy_ (u"ࠬ࠳࠭ࡩࡧࡤࡨࡱ࡫ࡳࡴࠩ᝟") in bstack11llllll1ll_opy_.get(bstack11l1111_opy_ (u"࠭ࡡࡳࡩࡶࠫᝠ"), []):
              logger.warning(bstack11l1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡱࡳࡹࠦࡲࡶࡰࠣࡳࡳࠦ࡬ࡦࡩࡤࡧࡾࠦࡨࡦࡣࡧࡰࡪࡹࡳࠡ࡯ࡲࡨࡪ࠴ࠠࡔࡹ࡬ࡸࡨ࡮ࠠࡵࡱࠣࡲࡪࡽࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫ࠠࡰࡴࠣࡥࡻࡵࡩࡥࠢࡸࡷ࡮ࡴࡧࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠤᝡ"))
              return False
        return True
    except Exception as error:
        logger.debug(bstack11l1111_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡷࡣ࡯࡭ࡩࡧࡴࡦࠢࡤ࠵࠶ࡿࠠࡴࡷࡳࡴࡴࡸࡴࠡ࠼ࠥᝢ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1l111lllll1_opy_ = config.get(bstack11l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᝣ"), {})
    bstack1l111lllll1_opy_[bstack11l1111_opy_ (u"ࠪࡥࡺࡺࡨࡕࡱ࡮ࡩࡳ࠭ᝤ")] = os.getenv(bstack11l1111_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᝥ"))
    bstack11l1l111ll1_opy_ = json.loads(os.getenv(bstack11l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᝦ"), bstack11l1111_opy_ (u"࠭ࡻࡾࠩᝧ"))).get(bstack11l1111_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᝨ"))
    if not config[bstack11l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡐࡳࡱࡧࡹࡨࡺࡍࡢࡲࠪᝩ")].get(bstack11l1111_opy_ (u"ࠤࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠣᝪ")):
      if bstack11l1111_opy_ (u"ࠪࡦࡸࡺࡡࡤ࡭࠽ࡳࡵࡺࡩࡰࡰࡶࠫᝫ") in caps:
        caps[bstack11l1111_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᝬ")][bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬ᝭")] = bstack1l111lllll1_opy_
        caps[bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᝮ")][bstack11l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᝯ")][bstack11l1111_opy_ (u"ࠨࡵࡦࡥࡳࡴࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᝰ")] = bstack11l1l111ll1_opy_
      else:
        caps[bstack11l1111_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫࠯ࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨ᝱")] = bstack1l111lllll1_opy_
        caps[bstack11l1111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬࠰ࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡑࡳࡸ࡮ࡵ࡮ࡴࠩᝲ")][bstack11l1111_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᝳ")] = bstack11l1l111ll1_opy_
  except Exception as error:
    logger.debug(bstack11l1111_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡴࡧࡷࡸ࡮ࡴࡧࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶ࠲ࠥࡋࡲࡳࡱࡵ࠾ࠥࠨ᝴") +  str(error))
def bstack11l11llll_opy_(driver, bstack11l1l11ll1l_opy_):
  try:
    setattr(driver, bstack11l1111_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡇ࠱࠲ࡻࡖ࡬ࡴࡻ࡬ࡥࡕࡦࡥࡳ࠭᝵"), True)
    session = driver.session_id
    if session:
      bstack11l11l1l111_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11l11l1l111_opy_ = False
      bstack11l11l1l111_opy_ = url.scheme in [bstack11l1111_opy_ (u"ࠢࡩࡶࡷࡴࠧ᝶"), bstack11l1111_opy_ (u"ࠣࡪࡷࡸࡵࡹࠢ᝷")]
      if bstack11l11l1l111_opy_:
        if bstack11l1l11ll1l_opy_:
          logger.info(bstack11l1111_opy_ (u"ࠤࡖࡩࡹࡻࡰࠡࡨࡲࡶࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡨࡢࡵࠣࡷࡹࡧࡲࡵࡧࡧ࠲ࠥࡇࡵࡵࡱࡰࡥࡹ࡫ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡩࡽ࡫ࡣࡶࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡧ࡫ࡧࡪࡰࠣࡱࡴࡳࡥ࡯ࡶࡤࡶ࡮ࡲࡹ࠯ࠤ᝸"))
      return bstack11l1l11ll1l_opy_
  except Exception as e:
    logger.error(bstack11l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡶࡸࡦࡸࡴࡪࡰࡪࠤࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡦࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡵࡦࡥࡳࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨ᝹") + str(e))
    return False
def bstack1lllll1lll_opy_(driver, name, path):
  try:
    bstack11lllllll11_opy_ = {
        bstack11l1111_opy_ (u"ࠫࡹ࡮ࡔࡦࡵࡷࡖࡺࡴࡕࡶ࡫ࡧࠫ᝺"): threading.current_thread().current_test_uuid,
        bstack11l1111_opy_ (u"ࠬࡺࡨࡃࡷ࡬ࡰࡩ࡛ࡵࡪࡦࠪ᝻"): os.environ.get(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡋ࡙ࡇࡥࡕࡖࡋࡇࠫ᝼"), bstack11l1111_opy_ (u"ࠧࠨ᝽")),
        bstack11l1111_opy_ (u"ࠨࡶ࡫ࡎࡼࡺࡔࡰ࡭ࡨࡲࠬ᝾"): os.environ.get(bstack11l1111_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡍ࡛࡙࠭᝿"), bstack11l1111_opy_ (u"ࠪࠫក"))
    }
    bstack1lll1lll11l_opy_ = bstack11lllll1l1_opy_.bstack1llll1lllll_opy_(EVENTS.bstack11l111111_opy_.value)
    logger.debug(bstack11l1111_opy_ (u"ࠫࡕ࡫ࡲࡧࡱࡵࡱ࡮ࡴࡧࠡࡵࡦࡥࡳࠦࡢࡦࡨࡲࡶࡪࠦࡳࡢࡸ࡬ࡲ࡬ࠦࡲࡦࡵࡸࡰࡹࡹࠧខ"))
    try:
      if (bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬគ"), None) and bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨឃ"), None)):
        scripts = {bstack11l1111_opy_ (u"ࠧࡴࡥࡤࡲࠬង"): bstack11llll1111_opy_.perform_scan}
        bstack11l1l111l1l_opy_ = json.loads(scripts[bstack11l1111_opy_ (u"ࠣࡵࡦࡥࡳࠨច")].replace(bstack11l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧឆ"), bstack11l1111_opy_ (u"ࠥࠦជ")))
        bstack11l1l111l1l_opy_[bstack11l1111_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧឈ")][bstack11l1111_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬញ")] = None
        scripts[bstack11l1111_opy_ (u"ࠨࡳࡤࡣࡱࠦដ")] = bstack11l1111_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥឋ") + json.dumps(bstack11l1l111l1l_opy_)
        bstack11llll1111_opy_.bstack11l1l1llll_opy_(scripts)
        bstack11llll1111_opy_.store()
        logger.debug(driver.execute_script(bstack11llll1111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11llll1111_opy_.perform_scan, {bstack11l1111_opy_ (u"ࠣ࡯ࡨࡸ࡭ࡵࡤࠣឌ"): name}))
      bstack11lllll1l1_opy_.end(EVENTS.bstack11l111111_opy_.value, bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤឍ"), bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠥ࠾ࡪࡴࡤࠣណ"), True, None)
    except Exception as error:
      bstack11lllll1l1_opy_.end(EVENTS.bstack11l111111_opy_.value, bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦត"), bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠧࡀࡥ࡯ࡦࠥថ"), False, str(error))
    bstack1lll1lll11l_opy_ = bstack11lllll1l1_opy_.bstack11l1l1111ll_opy_(EVENTS.bstack11lllll1l1l_opy_.value)
    bstack11lllll1l1_opy_.mark(bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨទ"))
    try:
      if (bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠧࡪࡵࡄࡴࡵࡇ࠱࠲ࡻࡗࡩࡸࡺࠧធ"), None) and bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠨࡣࡳࡴࡆ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪន"), None)):
        scripts = {bstack11l1111_opy_ (u"ࠩࡶࡧࡦࡴࠧប"): bstack11llll1111_opy_.perform_scan}
        bstack11l1l111l1l_opy_ = json.loads(scripts[bstack11l1111_opy_ (u"ࠥࡷࡨࡧ࡮ࠣផ")].replace(bstack11l1111_opy_ (u"ࠦࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡢࡩࡽ࡫ࡣࡶࡶࡲࡶ࠿ࠦࠢព"), bstack11l1111_opy_ (u"ࠧࠨភ")))
        bstack11l1l111l1l_opy_[bstack11l1111_opy_ (u"࠭ࡡࡳࡩࡸࡱࡪࡴࡴࡴࠩម")][bstack11l1111_opy_ (u"ࠧ࡮ࡧࡷ࡬ࡴࡪࠧយ")] = None
        scripts[bstack11l1111_opy_ (u"ࠣࡵࡦࡥࡳࠨរ")] = bstack11l1111_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧល") + json.dumps(bstack11l1l111l1l_opy_)
        bstack11llll1111_opy_.bstack11l1l1llll_opy_(scripts)
        bstack11llll1111_opy_.store()
        logger.debug(driver.execute_script(bstack11llll1111_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11llll1111_opy_.bstack11l11l1l1l1_opy_, bstack11lllllll11_opy_))
      bstack11lllll1l1_opy_.end(bstack1lll1lll11l_opy_, bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥវ"), bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠦ࠿࡫࡮ࡥࠤឝ"),True, None)
    except Exception as error:
      bstack11lllll1l1_opy_.end(bstack1lll1lll11l_opy_, bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧឞ"), bstack1lll1lll11l_opy_ + bstack11l1111_opy_ (u"ࠨ࠺ࡦࡰࡧࠦស"),False, str(error))
    logger.info(bstack11l1111_opy_ (u"ࠢࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡵࡧࡶࡸ࡮ࡴࡧࠡࡨࡲࡶࠥࡺࡨࡪࡵࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡨࡢࡵࠣࡩࡳࡪࡥࡥ࠰ࠥហ"))
  except Exception as bstack1l111111l1l_opy_:
    logger.error(bstack11l1111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡴࡨࡷࡺࡲࡴࡴࠢࡦࡳࡺࡲࡤࠡࡰࡲࡸࠥࡨࡥࠡࡲࡵࡳࡨ࡫ࡳࡴࡧࡧࠤ࡫ࡵࡲࠡࡶ࡫ࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥ࠻ࠢࠥឡ") + str(path) + bstack11l1111_opy_ (u"ࠤࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠦអ") + str(bstack1l111111l1l_opy_))
def bstack11l11llll11_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11l1111_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠤឣ")) and str(caps.get(bstack11l1111_opy_ (u"ࠦࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠥឤ"))).lower() == bstack11l1111_opy_ (u"ࠧࡧ࡮ࡥࡴࡲ࡭ࡩࠨឥ"):
        bstack11lllllllll_opy_ = caps.get(bstack11l1111_opy_ (u"ࠨࡡࡱࡲ࡬ࡹࡲࡀࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠣឦ")) or caps.get(bstack11l1111_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡘࡨࡶࡸ࡯࡯࡯ࠤឧ"))
        if bstack11lllllllll_opy_ and int(str(bstack11lllllllll_opy_)) < bstack11l11l11l11_opy_:
            return False
    return True
def bstack1l1ll11111_opy_(config):
  if bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨឨ") in config:
        return config[bstack11l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩឩ")]
  for platform in config.get(bstack11l1111_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ឪ"), []):
      if bstack11l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫឫ") in platform:
          return platform[bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬឬ")]
  return None
def bstack11ll1l1ll_opy_(bstack1lll1ll1l_opy_):
  try:
    browser_name = bstack1lll1ll1l_opy_[bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬឭ")]
    browser_version = bstack1lll1ll1l_opy_[bstack11l1111_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡠࡸࡨࡶࡸ࡯࡯࡯ࠩឮ")]
    chrome_options = bstack1lll1ll1l_opy_[bstack11l1111_opy_ (u"ࠨࡥ࡫ࡶࡴࡳࡥࡠࡱࡳࡸ࡮ࡵ࡮ࡴࠩឯ")]
    try:
        bstack11l1l1111l1_opy_ = int(browser_version.split(bstack11l1111_opy_ (u"ࠩ࠱ࠫឰ"))[0])
    except ValueError as e:
        logger.error(bstack11l1111_opy_ (u"ࠥࡉࡷࡸ࡯ࡳࠢࡺ࡬࡮ࡲࡥࠡࡥࡲࡲࡻ࡫ࡲࡵ࡫ࡱ࡫ࠥࡨࡲࡰࡹࡶࡩࡷࠦࡶࡦࡴࡶ࡭ࡴࡴࠢឱ") + str(e))
        return False
    if not (browser_name and browser_name.lower() == bstack11l1111_opy_ (u"ࠫࡨ࡮ࡲࡰ࡯ࡨࠫឲ")):
        logger.warning(bstack11l1111_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡳࡷࡱࠤࡴࡴ࡬ࡺࠢࡲࡲࠥࡉࡨࡳࡱࡰࡩࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣឳ"))
        return False
    if bstack11l1l1111l1_opy_ < bstack11l11l1ll11_opy_.bstack11llll1lll1_opy_:
        logger.warning(bstack1lll1111lll_opy_ (u"࠭ࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡶࡪࡷࡵࡪࡴࡨࡷࠥࡉࡨࡳࡱࡰࡩࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡻࡄࡑࡑࡗ࡙ࡇࡎࡕࡕ࠱ࡑࡎࡔࡉࡎࡗࡐࡣࡓࡕࡎࡠࡄࡖࡘࡆࡉࡋࡠࡋࡑࡊࡗࡇ࡟ࡂ࠳࠴࡝ࡤ࡙ࡕࡑࡒࡒࡖ࡙ࡋࡄࡠࡅࡋࡖࡔࡓࡅࡠࡘࡈࡖࡘࡏࡏࡏࡿࠣࡳࡷࠦࡨࡪࡩ࡫ࡩࡷ࠴ࠧ឴"))
        return False
    if chrome_options and any(bstack11l1111_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫ឵") in value for value in chrome_options.values() if isinstance(value, str)):
        logger.warning(bstack11l1111_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡲࡴࡺࠠࡳࡷࡱࠤࡴࡴࠠ࡭ࡧࡪࡥࡨࡿࠠࡩࡧࡤࡨࡱ࡫ࡳࡴࠢࡰࡳࡩ࡫࠮ࠡࡕࡺ࡭ࡹࡩࡨࠡࡶࡲࠤࡳ࡫ࡷࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥࠡࡱࡵࠤࡦࡼ࡯ࡪࡦࠣࡹࡸ࡯࡮ࡨࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦ࠰ࠥា"))
        return False
    return True
  except Exception as e:
    logger.error(bstack11l1111_opy_ (u"ࠤࡈࡶࡷࡵࡲࠡ࡫ࡱࠤࡨ࡮ࡥࡤ࡭࡬ࡲ࡬ࠦࡰ࡭ࡣࡷࡪࡴࡸ࡭ࠡࡵࡸࡴࡵࡵࡲࡵࠢࡩࡳࡷࠦ࡬ࡰࡥࡤࡰࠥࡉࡨࡳࡱࡰࡩ࠿ࠦࠢិ") + str(e))
    return False
def bstack11l11l1l11_opy_(bstack1ll111l1l_opy_, config):
    try:
      bstack1l111111ll1_opy_ = bstack11l1111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪី") in config and config[bstack11l1111_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫឹ")] == True
      bstack11l11l111ll_opy_ = bstack11l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩឺ") in config and str(config[bstack11l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪុ")]).lower() != bstack11l1111_opy_ (u"ࠧࡧࡣ࡯ࡷࡪ࠭ូ")
      if not (bstack1l111111ll1_opy_ and (not bstack1l11lll1l_opy_(config) or bstack11l11l111ll_opy_)):
        return bstack1ll111l1l_opy_
      bstack11l11llllll_opy_ = bstack11llll1111_opy_.bstack11l1l111lll_opy_
      if bstack11l11llllll_opy_ is None:
        logger.debug(bstack11l1111_opy_ (u"ࠣࡉࡲࡳ࡬ࡲࡥࠡࡥ࡫ࡶࡴࡳࡥࠡࡱࡳࡸ࡮ࡵ࡮ࡴࠢࡤࡶࡪࠦࡎࡰࡰࡨࠦួ"))
        return bstack1ll111l1l_opy_
      bstack11l11lll1ll_opy_ = int(str(bstack11l1l11ll11_opy_()).split(bstack11l1111_opy_ (u"ࠩ࠱ࠫើ"))[0])
      logger.debug(bstack11l1111_opy_ (u"ࠥࡗࡪࡲࡥ࡯࡫ࡸࡱࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡤࡦࡶࡨࡧࡹ࡫ࡤ࠻ࠢࠥឿ") + str(bstack11l11lll1ll_opy_) + bstack11l1111_opy_ (u"ࠦࠧៀ"))
      if bstack11l11lll1ll_opy_ == 3 and isinstance(bstack1ll111l1l_opy_, dict) and bstack11l1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬេ") in bstack1ll111l1l_opy_ and bstack11l11llllll_opy_ is not None:
        if bstack11l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫែ") not in bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧៃ")]:
          bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠨࡦࡨࡷ࡮ࡸࡥࡥࡡࡦࡥࡵࡧࡢࡪ࡮࡬ࡸ࡮࡫ࡳࠨោ")][bstack11l1111_opy_ (u"ࠩࡪࡳࡴ࡭࠺ࡤࡪࡵࡳࡲ࡫ࡏࡱࡶ࡬ࡳࡳࡹࠧៅ")] = {}
        if bstack11l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨំ") in bstack11l11llllll_opy_:
          if bstack11l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩះ") not in bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬៈ")][bstack11l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ៉")]:
            bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ៊")][bstack11l1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭់")][bstack11l1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ៌")] = []
          for arg in bstack11l11llllll_opy_[bstack11l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ៍")]:
            if arg not in bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫ៎")][bstack11l1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៏")][bstack11l1111_opy_ (u"࠭ࡡࡳࡩࡶࠫ័")]:
              bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ៑")][bstack11l1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ្࠭")][bstack11l1111_opy_ (u"ࠩࡤࡶ࡬ࡹࠧ៓")].append(arg)
        if bstack11l1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ។") in bstack11l11llllll_opy_:
          if bstack11l1111_opy_ (u"ࠫࡪࡾࡴࡦࡰࡶ࡭ࡴࡴࡳࠨ៕") not in bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ៖")][bstack11l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫៗ")]:
            bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ៘")][bstack11l1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭៙")][bstack11l1111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭៚")] = []
          for ext in bstack11l11llllll_opy_[bstack11l1111_opy_ (u"ࠪࡩࡽࡺࡥ࡯ࡵ࡬ࡳࡳࡹࠧ៛")]:
            if ext not in bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠫࡩ࡫ࡳࡪࡴࡨࡨࡤࡩࡡࡱࡣࡥ࡭ࡱ࡯ࡴࡪࡧࡶࠫៜ")][bstack11l1111_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪ៝")][bstack11l1111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ៞")]:
              bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ៟")][bstack11l1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭០")][bstack11l1111_opy_ (u"ࠩࡨࡼࡹ࡫࡮ࡴ࡫ࡲࡲࡸ࠭១")].append(ext)
        if bstack11l1111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ២") in bstack11l11llllll_opy_:
          if bstack11l1111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ៣") not in bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠬࡪࡥࡴ࡫ࡵࡩࡩࡥࡣࡢࡲࡤࡦ࡮ࡲࡩࡵ࡫ࡨࡷࠬ៤")][bstack11l1111_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫ៥")]:
            bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠧࡥࡧࡶ࡭ࡷ࡫ࡤࡠࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹࠧ៦")][bstack11l1111_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭៧")][bstack11l1111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ៨")] = {}
          bstack11l11lll111_opy_(bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠪࡨࡪࡹࡩࡳࡧࡧࡣࡨࡧࡰࡢࡤ࡬ࡰ࡮ࡺࡩࡦࡵࠪ៩")][bstack11l1111_opy_ (u"ࠫ࡬ࡵ࡯ࡨ࠼ࡦ࡬ࡷࡵ࡭ࡦࡑࡳࡸ࡮ࡵ࡮ࡴࠩ៪")][bstack11l1111_opy_ (u"ࠬࡶࡲࡦࡨࡶࠫ៫")],
                    bstack11l11llllll_opy_[bstack11l1111_opy_ (u"࠭ࡰࡳࡧࡩࡷࠬ៬")])
        os.environ[bstack11l1111_opy_ (u"ࠧࡊࡕࡢࡒࡔࡔ࡟ࡃࡕࡗࡅࡈࡑ࡟ࡊࡐࡉࡖࡆࡥࡁ࠲࠳࡜ࡣࡘࡋࡓࡔࡋࡒࡒࠬ៭")] = bstack11l1111_opy_ (u"ࠨࡶࡵࡹࡪ࠭៮")
        return bstack1ll111l1l_opy_
      else:
        chrome_options = None
        if isinstance(bstack1ll111l1l_opy_, ChromeOptions):
          chrome_options = bstack1ll111l1l_opy_
        elif isinstance(bstack1ll111l1l_opy_, dict):
          for value in bstack1ll111l1l_opy_.values():
            if isinstance(value, ChromeOptions):
              chrome_options = value
              break
        if chrome_options is None:
          chrome_options = ChromeOptions()
          if isinstance(bstack1ll111l1l_opy_, dict):
            bstack1ll111l1l_opy_[bstack11l1111_opy_ (u"ࠩࡲࡴࡹ࡯࡯࡯ࡵࠪ៯")] = chrome_options
          else:
            bstack1ll111l1l_opy_ = chrome_options
        if bstack11l11llllll_opy_ is not None:
          if bstack11l1111_opy_ (u"ࠪࡥࡷ࡭ࡳࠨ៰") in bstack11l11llllll_opy_:
                bstack11l1l11l11l_opy_ = chrome_options.arguments or []
                new_args = bstack11l11llllll_opy_[bstack11l1111_opy_ (u"ࠫࡦࡸࡧࡴࠩ៱")]
                for arg in new_args:
                    if arg not in bstack11l1l11l11l_opy_:
                        chrome_options.add_argument(arg)
          if bstack11l1111_opy_ (u"ࠬ࡫ࡸࡵࡧࡱࡷ࡮ࡵ࡮ࡴࠩ៲") in bstack11l11llllll_opy_:
                existing_extensions = chrome_options.experimental_options.get(bstack11l1111_opy_ (u"࠭ࡥࡹࡶࡨࡲࡸ࡯࡯࡯ࡵࠪ៳"), [])
                bstack11l11lll11l_opy_ = bstack11l11llllll_opy_[bstack11l1111_opy_ (u"ࠧࡦࡺࡷࡩࡳࡹࡩࡰࡰࡶࠫ៴")]
                for extension in bstack11l11lll11l_opy_:
                    if extension not in existing_extensions:
                        chrome_options.add_encoded_extension(extension)
          if bstack11l1111_opy_ (u"ࠨࡲࡵࡩ࡫ࡹࠧ៵") in bstack11l11llllll_opy_:
                bstack11l11ll1lll_opy_ = chrome_options.experimental_options.get(bstack11l1111_opy_ (u"ࠩࡳࡶࡪ࡬ࡳࠨ៶"), {})
                bstack11l1l11l111_opy_ = bstack11l11llllll_opy_[bstack11l1111_opy_ (u"ࠪࡴࡷ࡫ࡦࡴࠩ៷")]
                bstack11l11lll111_opy_(bstack11l11ll1lll_opy_, bstack11l1l11l111_opy_)
                chrome_options.add_experimental_option(bstack11l1111_opy_ (u"ࠫࡵࡸࡥࡧࡵࠪ៸"), bstack11l11ll1lll_opy_)
        os.environ[bstack11l1111_opy_ (u"ࠬࡏࡓࡠࡐࡒࡒࡤࡈࡓࡕࡃࡆࡏࡤࡏࡎࡇࡔࡄࡣࡆ࠷࠱࡚ࡡࡖࡉࡘ࡙ࡉࡐࡐࠪ៹")] = bstack11l1111_opy_ (u"࠭ࡴࡳࡷࡨࠫ៺")
        return bstack1ll111l1l_opy_
    except Exception as e:
      logger.error(bstack11l1111_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡧࡤࡥ࡫ࡱ࡫ࠥࡴ࡯࡯࠯ࡅࡗࠥ࡯࡮ࡧࡴࡤࠤࡦ࠷࠱ࡺࠢࡦ࡬ࡷࡵ࡭ࡦࠢࡲࡴࡹ࡯࡯࡯ࡵ࠽ࠤࠧ៻") + str(e))
      return bstack1ll111l1l_opy_