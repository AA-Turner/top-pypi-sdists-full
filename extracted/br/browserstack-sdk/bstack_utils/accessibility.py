# coding: UTF-8
import sys
bstack1ll11_opy_ = sys.version_info [0] == 2
bstack1111l1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l11lll_opy_ (bstack1l1ll1l_opy_):
    global bstack1l1l111_opy_
    bstack1l1l11l_opy_ = ord (bstack1l1ll1l_opy_ [-1])
    bstack11llll_opy_ = bstack1l1ll1l_opy_ [:-1]
    bstack1l1lll1_opy_ = bstack1l1l11l_opy_ % len (bstack11llll_opy_)
    bstack11l1ll1_opy_ = bstack11llll_opy_ [:bstack1l1lll1_opy_] + bstack11llll_opy_ [bstack1l1lll1_opy_:]
    if bstack1ll11_opy_:
        bstack111l111_opy_ = unicode () .join ([unichr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    else:
        bstack111l111_opy_ = str () .join ([chr (ord (char) - bstack1111l1_opy_ - (bstack111l1ll_opy_ + bstack1l1l11l_opy_) % bstack1l11l11_opy_) for bstack111l1ll_opy_, char in enumerate (bstack11l1ll1_opy_)])
    return eval (bstack111l111_opy_)
import os
import json
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11llll11l1l_opy_ as bstack11llllll11l_opy_, EVENTS
from bstack_utils.bstack11l111l11_opy_ import bstack11l111l11_opy_
from bstack_utils.helper import bstack11lll111l1_opy_, bstack111l1lll1l_opy_, bstack1l11l1l1l_opy_, bstack11lll1ll1l1_opy_, \
  bstack11lllll1111_opy_, bstack1lll1ll1ll_opy_, get_host_info, bstack11llll1l1ll_opy_, bstack1l1lll11l_opy_, bstack111l1ll1ll_opy_, bstack11l11l1ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack11111llll_opy_ import get_logger
from bstack_utils.bstack1l111lll_opy_ import bstack1ll1llll111_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1l111lll_opy_ = bstack1ll1llll111_opy_()
@bstack111l1ll1ll_opy_(class_method=False)
def _11lllll11l1_opy_(driver, bstack1111lll11l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l11lll_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᕔ"): caps.get(bstack1l11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᕕ"), None),
        bstack1l11lll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᕖ"): bstack1111lll11l_opy_.get(bstack1l11lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᕗ"), None),
        bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᕘ"): caps.get(bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᕙ"), None),
        bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕚ"): caps.get(bstack1l11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕛ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l11lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᕜ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕝ"), None) is None or os.environ[bstack1l11lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕞ")] == bstack1l11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕟ"):
        return False
    return True
def bstack1lll1ll1l_opy_(config):
  return config.get(bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕠ"), False) or any([p.get(bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕡ"), False) == True for p in config.get(bstack1l11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕢ"), [])])
def bstack111llll11_opy_(config, bstack111l111l_opy_):
  try:
    if not bstack1l11l1l1l_opy_(config):
      return False
    bstack11llll1ll1l_opy_ = config.get(bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕣ"), False)
    if int(bstack111l111l_opy_) < len(config.get(bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᕤ"), [])) and config[bstack1l11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᕥ")][bstack111l111l_opy_]:
      bstack11lll1ll11l_opy_ = config[bstack1l11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕦ")][bstack111l111l_opy_].get(bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕧ"), None)
    else:
      bstack11lll1ll11l_opy_ = config.get(bstack1l11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕨ"), None)
    if bstack11lll1ll11l_opy_ != None:
      bstack11llll1ll1l_opy_ = bstack11lll1ll11l_opy_
    bstack11llll11ll1_opy_ = os.getenv(bstack1l11lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᕩ")) is not None and len(os.getenv(bstack1l11lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᕪ"))) > 0 and os.getenv(bstack1l11lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕫ")) != bstack1l11lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᕬ")
    return bstack11llll1ll1l_opy_ and bstack11llll11ll1_opy_
  except Exception as error:
    logger.debug(bstack1l11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᕭ") + str(error))
  return False
def bstack111ll1l1l_opy_(test_tags):
  bstack1ll11lll1ll_opy_ = os.getenv(bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᕮ"))
  if bstack1ll11lll1ll_opy_ is None:
    return True
  bstack1ll11lll1ll_opy_ = json.loads(bstack1ll11lll1ll_opy_)
  try:
    include_tags = bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕯ")] if bstack1l11lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᕰ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕱ")], list) else []
    exclude_tags = bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕲ")] if bstack1l11lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕳ") in bstack1ll11lll1ll_opy_ and isinstance(bstack1ll11lll1ll_opy_[bstack1l11lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕴ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᕵ") + str(error))
  return False
def bstack11llll1111l_opy_(config, bstack11llll1l1l1_opy_, bstack11lllll11ll_opy_, bstack11lllll1lll_opy_):
  bstack11llll1lll1_opy_ = bstack11lll1ll1l1_opy_(config)
  bstack11lllll111l_opy_ = bstack11lllll1111_opy_(config)
  if bstack11llll1lll1_opy_ is None or bstack11lllll111l_opy_ is None:
    logger.error(bstack1l11lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᕶ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᕷ"), bstack1l11lll_opy_ (u"ࠨࡽࢀࠫᕸ")))
    data = {
        bstack1l11lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᕹ"): config[bstack1l11lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᕺ")],
        bstack1l11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᕻ"): config.get(bstack1l11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᕼ"), os.path.basename(os.getcwd())),
        bstack1l11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᕽ"): bstack11lll111l1_opy_(),
        bstack1l11lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᕾ"): config.get(bstack1l11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᕿ"), bstack1l11lll_opy_ (u"ࠩࠪᖀ")),
        bstack1l11lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᖁ"): {
            bstack1l11lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᖂ"): bstack11llll1l1l1_opy_,
            bstack1l11lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖃ"): bstack11lllll11ll_opy_,
            bstack1l11lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᖄ"): __version__,
            bstack1l11lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᖅ"): bstack1l11lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᖆ"),
            bstack1l11lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᖇ"): bstack1l11lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᖈ"),
            bstack1l11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᖉ"): bstack11lllll1lll_opy_
        },
        bstack1l11lll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᖊ"): settings,
        bstack1l11lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᖋ"): bstack11llll1l1ll_opy_(),
        bstack1l11lll_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᖌ"): bstack1lll1ll1ll_opy_(),
        bstack1l11lll_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᖍ"): get_host_info(),
        bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᖎ"): bstack1l11l1l1l_opy_(config)
    }
    headers = {
        bstack1l11lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᖏ"): bstack1l11lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᖐ"),
    }
    config = {
        bstack1l11lll_opy_ (u"ࠬࡧࡵࡵࡪࠪᖑ"): (bstack11llll1lll1_opy_, bstack11lllll111l_opy_),
        bstack1l11lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᖒ"): headers
    }
    response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"ࠧࡑࡑࡖࡘࠬᖓ"), bstack11llllll11l_opy_ + bstack1l11lll_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᖔ"), data, config)
    bstack11llll1llll_opy_ = response.json()
    if bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᖕ")]:
      parsed = json.loads(os.getenv(bstack1l11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖖ"), bstack1l11lll_opy_ (u"ࠫࢀࢃࠧᖗ")))
      parsed[bstack1l11lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖘ")] = bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖙ")][bstack1l11lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖚ")]
      os.environ[bstack1l11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᖛ")] = json.dumps(parsed)
      bstack11l111l11_opy_.bstack1l11lll11l_opy_(bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᖜ")][bstack1l11lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᖝ")])
      bstack11l111l11_opy_.bstack11lllll1ll1_opy_(bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"ࠫࡩࡧࡴࡢࠩᖞ")][bstack1l11lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᖟ")])
      bstack11l111l11_opy_.store()
      return bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖠ")][bstack1l11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᖡ")], bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖢ")][bstack1l11lll_opy_ (u"ࠩ࡬ࡨࠬᖣ")]
    else:
      logger.error(bstack1l11lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᖤ") + bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖥ")])
      if bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖦ")] == bstack1l11lll_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᖧ"):
        for bstack11lll1ll1ll_opy_ in bstack11llll1llll_opy_[bstack1l11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᖨ")]:
          logger.error(bstack11lll1ll1ll_opy_[bstack1l11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖩ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᖪ") +  str(error))
    return None, None
def bstack11lll1lll11_opy_():
  if os.getenv(bstack1l11lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖫ")) is None:
    return {
        bstack1l11lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᖬ"): bstack1l11lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᖭ"),
        bstack1l11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖮ"): bstack1l11lll_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᖯ")
    }
  data = {bstack1l11lll_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᖰ"): bstack11lll111l1_opy_()}
  headers = {
      bstack1l11lll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᖱ"): bstack1l11lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᖲ") + os.getenv(bstack1l11lll_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᖳ")),
      bstack1l11lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖴ"): bstack1l11lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᖵ")
  }
  response = bstack1l1lll11l_opy_(bstack1l11lll_opy_ (u"ࠧࡑࡗࡗࠫᖶ"), bstack11llllll11l_opy_ + bstack1l11lll_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᖷ"), data, { bstack1l11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᖸ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l11lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᖹ") + bstack111l1lll1l_opy_().isoformat() + bstack1l11lll_opy_ (u"ࠫ࡟࠭ᖺ"))
      return {bstack1l11lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᖻ"): bstack1l11lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᖼ"), bstack1l11lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖽ"): bstack1l11lll_opy_ (u"ࠨࠩᖾ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᖿ") + str(error))
    return {
        bstack1l11lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᗀ"): bstack1l11lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᗁ"),
        bstack1l11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗂ"): str(error)
    }
def bstack11lllll1l1l_opy_(bstack11lllll1l11_opy_):
    return re.match(bstack1l11lll_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᗃ"), bstack11lllll1l11_opy_.strip()) is not None
def bstack11l1ll1l1l_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11llll11111_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llll11111_opy_ = desired_capabilities
        else:
          bstack11llll11111_opy_ = {}
        bstack11llll111ll_opy_ = (bstack11llll11111_opy_.get(bstack1l11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᗄ"), bstack1l11lll_opy_ (u"ࠨࠩᗅ")).lower() or caps.get(bstack1l11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᗆ"), bstack1l11lll_opy_ (u"ࠪࠫᗇ")).lower())
        if bstack11llll111ll_opy_ == bstack1l11lll_opy_ (u"ࠫ࡮ࡵࡳࠨᗈ"):
            return True
        if bstack11llll111ll_opy_ == bstack1l11lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᗉ"):
            bstack11lll1llll1_opy_ = str(float(caps.get(bstack1l11lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗊ")) or bstack11llll11111_opy_.get(bstack1l11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗋ"), {}).get(bstack1l11lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᗌ"),bstack1l11lll_opy_ (u"ࠩࠪᗍ"))))
            if bstack11llll111ll_opy_ == bstack1l11lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᗎ") and int(bstack11lll1llll1_opy_.split(bstack1l11lll_opy_ (u"ࠫ࠳࠭ᗏ"))[0]) < float(bstack11llllll111_opy_):
                logger.warning(str(bstack11llll11lll_opy_))
                return False
            return True
        bstack1ll1ll11l11_opy_ = caps.get(bstack1l11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗐ"), {}).get(bstack1l11lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᗑ"), caps.get(bstack1l11lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᗒ"), bstack1l11lll_opy_ (u"ࠨࠩᗓ")))
        if bstack1ll1ll11l11_opy_:
            logger.warn(bstack1l11lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᗔ"))
            return False
        browser = caps.get(bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᗕ"), bstack1l11lll_opy_ (u"ࠫࠬᗖ")).lower() or bstack11llll11111_opy_.get(bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᗗ"), bstack1l11lll_opy_ (u"࠭ࠧᗘ")).lower()
        if browser != bstack1l11lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᗙ"):
            logger.warning(bstack1l11lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᗚ"))
            return False
        browser_version = caps.get(bstack1l11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗛ")) or caps.get(bstack1l11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᗜ")) or bstack11llll11111_opy_.get(bstack1l11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗝ")) or bstack11llll11111_opy_.get(bstack1l11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗞ"), {}).get(bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗟ")) or bstack11llll11111_opy_.get(bstack1l11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗠ"), {}).get(bstack1l11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᗡ"))
        if browser_version and browser_version != bstack1l11lll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᗢ") and int(browser_version.split(bstack1l11lll_opy_ (u"ࠪ࠲ࠬᗣ"))[0]) <= 98:
            logger.warning(bstack1l11lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠸࠯ࠤᗤ"))
            return False
        if not options:
            bstack1ll1l11llll_opy_ = caps.get(bstack1l11lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᗥ")) or bstack11llll11111_opy_.get(bstack1l11lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᗦ"), {})
            if bstack1l11lll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᗧ") in bstack1ll1l11llll_opy_.get(bstack1l11lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᗨ"), []):
                logger.warn(bstack1l11lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᗩ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack1l11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᗪ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll1111111_opy_ = config.get(bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗫ"), {})
    bstack1lll1111111_opy_[bstack1l11lll_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᗬ")] = os.getenv(bstack1l11lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᗭ"))
    bstack11llll1l11l_opy_ = json.loads(os.getenv(bstack1l11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᗮ"), bstack1l11lll_opy_ (u"ࠨࡽࢀࠫᗯ"))).get(bstack1l11lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗰ"))
    caps[bstack1l11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗱ")] = True
    if not config[bstack1l11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᗲ")].get(bstack1l11lll_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᗳ")):
      if bstack1l11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᗴ") in caps:
        caps[bstack1l11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗵ")][bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᗶ")] = bstack1lll1111111_opy_
        caps[bstack1l11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗷ")][bstack1l11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᗸ")][bstack1l11lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗹ")] = bstack11llll1l11l_opy_
      else:
        caps[bstack1l11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗺ")] = bstack1lll1111111_opy_
        caps[bstack1l11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᗻ")][bstack1l11lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗼ")] = bstack11llll1l11l_opy_
  except Exception as error:
    logger.debug(bstack1l11lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤᗽ") +  str(error))
def bstack1lll1l11l1_opy_(driver, bstack11lll1lll1l_opy_):
  try:
    setattr(driver, bstack1l11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᗾ"), True)
    session = driver.session_id
    if session:
      bstack11lll1lllll_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1lllll_opy_ = False
      bstack11lll1lllll_opy_ = url.scheme in [bstack1l11lll_opy_ (u"ࠥ࡬ࡹࡺࡰࠣᗿ"), bstack1l11lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᘀ")]
      if bstack11lll1lllll_opy_:
        if bstack11lll1lll1l_opy_:
          logger.info(bstack1l11lll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧᘁ"))
      return bstack11lll1lll1l_opy_
  except Exception as e:
    logger.error(bstack1l11lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᘂ") + str(e))
    return False
def bstack1l111l11l1_opy_(driver, name, path):
  try:
    bstack1ll11llll1l_opy_ = {
        bstack1l11lll_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᘃ"): threading.current_thread().current_test_uuid,
        bstack1l11lll_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᘄ"): os.environ.get(bstack1l11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᘅ"), bstack1l11lll_opy_ (u"ࠪࠫᘆ")),
        bstack1l11lll_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨᘇ"): os.environ.get(bstack1l11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᘈ"), bstack1l11lll_opy_ (u"࠭ࠧᘉ"))
    }
    bstack1ll1ll1l111_opy_ = bstack1l111lll_opy_.bstack1ll1l1l1111_opy_(EVENTS.bstack1111l11ll_opy_.value)
    logger.debug(bstack1l11lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᘊ"))
    try:
      if (bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᘋ"), None) and bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᘌ"), None)):
        scripts = {bstack1l11lll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᘍ"): bstack11l111l11_opy_.perform_scan}
        bstack11llll11l11_opy_ = json.loads(scripts[bstack1l11lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘎ")].replace(bstack1l11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘏ"), bstack1l11lll_opy_ (u"ࠨࠢᘐ")))
        bstack11llll11l11_opy_[bstack1l11lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᘑ")][bstack1l11lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᘒ")] = None
        scripts[bstack1l11lll_opy_ (u"ࠤࡶࡧࡦࡴࠢᘓ")] = bstack1l11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᘔ") + json.dumps(bstack11llll11l11_opy_)
        bstack11l111l11_opy_.bstack1l11lll11l_opy_(scripts)
        bstack11l111l11_opy_.store()
        logger.debug(driver.execute_script(bstack11l111l11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11l111l11_opy_.perform_scan, {bstack1l11lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᘕ"): name}))
      bstack1l111lll_opy_.end(EVENTS.bstack1111l11ll_opy_.value, bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘖ"), bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᘗ"), True, None)
    except Exception as error:
      bstack1l111lll_opy_.end(EVENTS.bstack1111l11ll_opy_.value, bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘘ"), bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘙ"), False, str(error))
    bstack1ll1ll1l111_opy_ = bstack1l111lll_opy_.bstack11llll111l1_opy_(EVENTS.bstack1ll1l1l1ll1_opy_.value)
    bstack1l111lll_opy_.mark(bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘚ"))
    try:
      if (bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᘛ"), None) and bstack11l11l1ll1_opy_(threading.current_thread(), bstack1l11lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᘜ"), None)):
        scripts = {bstack1l11lll_opy_ (u"ࠬࡹࡣࡢࡰࠪᘝ"): bstack11l111l11_opy_.perform_scan}
        bstack11llll11l11_opy_ = json.loads(scripts[bstack1l11lll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘞ")].replace(bstack1l11lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘟ"), bstack1l11lll_opy_ (u"ࠣࠤᘠ")))
        bstack11llll11l11_opy_[bstack1l11lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᘡ")][bstack1l11lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᘢ")] = None
        scripts[bstack1l11lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘣ")] = bstack1l11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘤ") + json.dumps(bstack11llll11l11_opy_)
        bstack11l111l11_opy_.bstack1l11lll11l_opy_(scripts)
        bstack11l111l11_opy_.store()
        logger.debug(driver.execute_script(bstack11l111l11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11l111l11_opy_.bstack11llll1ll11_opy_, bstack1ll11llll1l_opy_))
      bstack1l111lll_opy_.end(bstack1ll1ll1l111_opy_, bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘥ"), bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᘦ"),True, None)
    except Exception as error:
      bstack1l111lll_opy_.end(bstack1ll1ll1l111_opy_, bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘧ"), bstack1ll1ll1l111_opy_ + bstack1l11lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘨ"),False, str(error))
    logger.info(bstack1l11lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᘩ"))
  except Exception as bstack1ll1l111ll1_opy_:
    logger.error(bstack1l11lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᘪ") + str(path) + bstack1l11lll_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᘫ") + str(bstack1ll1l111ll1_opy_))
def bstack11llll1l111_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l11lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᘬ")) and str(caps.get(bstack1l11lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᘭ"))).lower() == bstack1l11lll_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᘮ"):
        bstack11lll1llll1_opy_ = caps.get(bstack1l11lll_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᘯ")) or caps.get(bstack1l11lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᘰ"))
        if bstack11lll1llll1_opy_ and int(str(bstack11lll1llll1_opy_)) < bstack11llllll111_opy_:
            return False
    return True
def bstack11lll11l1l_opy_(config):
  if bstack1l11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘱ") in config:
        return config[bstack1l11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘲ")]
  for platform in config.get(bstack1l11lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘳ"), []):
      if bstack1l11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘴ") in platform:
          return platform[bstack1l11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘵ")]
  return None