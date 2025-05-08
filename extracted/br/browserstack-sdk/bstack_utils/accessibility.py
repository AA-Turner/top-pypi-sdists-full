# coding: UTF-8
import sys
bstack111l1ll_opy_ = sys.version_info [0] == 2
bstack1lll11l_opy_ = 2048
bstack11111_opy_ = 7
def bstack1l1lll_opy_ (bstack11l_opy_):
    global bstack1l11l11_opy_
    bstack1_opy_ = ord (bstack11l_opy_ [-1])
    bstack1ll111l_opy_ = bstack11l_opy_ [:-1]
    bstack11l1111_opy_ = bstack1_opy_ % len (bstack1ll111l_opy_)
    bstack11l1l_opy_ = bstack1ll111l_opy_ [:bstack11l1111_opy_] + bstack1ll111l_opy_ [bstack11l1111_opy_:]
    if bstack111l1ll_opy_:
        bstack11llll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    else:
        bstack11llll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11l_opy_ - (bstack1lllll_opy_ + bstack1_opy_) % bstack11111_opy_) for bstack1lllll_opy_, char in enumerate (bstack11l1l_opy_)])
    return eval (bstack11llll1_opy_)
import os
import json
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11llll1llll_opy_ as bstack11lllll11l1_opy_, EVENTS
from bstack_utils.bstack11ll11ll11_opy_ import bstack11ll11ll11_opy_
from bstack_utils.helper import bstack1l1ll1ll_opy_, bstack111l1lll1l_opy_, bstack1lll111l1l_opy_, bstack11lllll1lll_opy_, \
  bstack11llll1l1ll_opy_, bstack1l1l1ll1l_opy_, get_host_info, bstack11lll1lllll_opy_, bstack11ll1l111l_opy_, bstack111ll1ll1l_opy_, bstack1l111l11_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1ll1l111l1_opy_ import get_logger
from bstack_utils.bstack1ll11111l1_opy_ import bstack1lll1lll111_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1ll11111l1_opy_ = bstack1lll1lll111_opy_()
@bstack111ll1ll1l_opy_(class_method=False)
def _11llll1l111_opy_(driver, bstack1111lll1l1_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1l1lll_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᕛ"): caps.get(bstack1l1lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᕜ"), None),
        bstack1l1lll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᕝ"): bstack1111lll1l1_opy_.get(bstack1l1lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᕞ"), None),
        bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᕟ"): caps.get(bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᕠ"), None),
        bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕡ"): caps.get(bstack1l1lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕢ"), None)
    }
  except Exception as error:
    logger.debug(bstack1l1lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᕣ") + str(error))
  return response
def on():
    if os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕤ"), None) is None or os.environ[bstack1l1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕥ")] == bstack1l1lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕦ"):
        return False
    return True
def bstack111ll1ll1_opy_(config):
  return config.get(bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕧ"), False) or any([p.get(bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕨ"), False) == True for p in config.get(bstack1l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕩ"), [])])
def bstack1ll1llll1_opy_(config, bstack11l11l1l1l_opy_):
  try:
    if not bstack1lll111l1l_opy_(config):
      return False
    bstack11lllll1l11_opy_ = config.get(bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕪ"), False)
    if int(bstack11l11l1l1l_opy_) < len(config.get(bstack1l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᕫ"), [])) and config[bstack1l1lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᕬ")][bstack11l11l1l1l_opy_]:
      bstack11lllll11ll_opy_ = config[bstack1l1lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕭ")][bstack11l11l1l1l_opy_].get(bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕮ"), None)
    else:
      bstack11lllll11ll_opy_ = config.get(bstack1l1lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕯ"), None)
    if bstack11lllll11ll_opy_ != None:
      bstack11lllll1l11_opy_ = bstack11lllll11ll_opy_
    bstack11lllll1ll1_opy_ = os.getenv(bstack1l1lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᕰ")) is not None and len(os.getenv(bstack1l1lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᕱ"))) > 0 and os.getenv(bstack1l1lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕲ")) != bstack1l1lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᕳ")
    return bstack11lllll1l11_opy_ and bstack11lllll1ll1_opy_
  except Exception as error:
    logger.debug(bstack1l1lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᕴ") + str(error))
  return False
def bstack1ll1llll11_opy_(test_tags):
  bstack1ll1ll1111l_opy_ = os.getenv(bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᕵ"))
  if bstack1ll1ll1111l_opy_ is None:
    return True
  bstack1ll1ll1111l_opy_ = json.loads(bstack1ll1ll1111l_opy_)
  try:
    include_tags = bstack1ll1ll1111l_opy_[bstack1l1lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕶ")] if bstack1l1lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᕷ") in bstack1ll1ll1111l_opy_ and isinstance(bstack1ll1ll1111l_opy_[bstack1l1lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕸ")], list) else []
    exclude_tags = bstack1ll1ll1111l_opy_[bstack1l1lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕹ")] if bstack1l1lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕺ") in bstack1ll1ll1111l_opy_ and isinstance(bstack1ll1ll1111l_opy_[bstack1l1lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕻ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1l1lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᕼ") + str(error))
  return False
def bstack11llll11111_opy_(config, bstack11llllll11l_opy_, bstack11llll11lll_opy_, bstack11lll1lll1l_opy_):
  bstack11llll11l11_opy_ = bstack11lllll1lll_opy_(config)
  bstack11llll1ll1l_opy_ = bstack11llll1l1ll_opy_(config)
  if bstack11llll11l11_opy_ is None or bstack11llll1ll1l_opy_ is None:
    logger.error(bstack1l1lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᕽ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᕾ"), bstack1l1lll_opy_ (u"ࠨࡽࢀࠫᕿ")))
    data = {
        bstack1l1lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᖀ"): config[bstack1l1lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᖁ")],
        bstack1l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᖂ"): config.get(bstack1l1lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᖃ"), os.path.basename(os.getcwd())),
        bstack1l1lll_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᖄ"): bstack1l1ll1ll_opy_(),
        bstack1l1lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᖅ"): config.get(bstack1l1lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᖆ"), bstack1l1lll_opy_ (u"ࠩࠪᖇ")),
        bstack1l1lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᖈ"): {
            bstack1l1lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᖉ"): bstack11llllll11l_opy_,
            bstack1l1lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖊ"): bstack11llll11lll_opy_,
            bstack1l1lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᖋ"): __version__,
            bstack1l1lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᖌ"): bstack1l1lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᖍ"),
            bstack1l1lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᖎ"): bstack1l1lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᖏ"),
            bstack1l1lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᖐ"): bstack11lll1lll1l_opy_
        },
        bstack1l1lll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᖑ"): settings,
        bstack1l1lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᖒ"): bstack11lll1lllll_opy_(),
        bstack1l1lll_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᖓ"): bstack1l1l1ll1l_opy_(),
        bstack1l1lll_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᖔ"): get_host_info(),
        bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᖕ"): bstack1lll111l1l_opy_(config)
    }
    headers = {
        bstack1l1lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᖖ"): bstack1l1lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᖗ"),
    }
    config = {
        bstack1l1lll_opy_ (u"ࠬࡧࡵࡵࡪࠪᖘ"): (bstack11llll11l11_opy_, bstack11llll1ll1l_opy_),
        bstack1l1lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᖙ"): headers
    }
    response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"ࠧࡑࡑࡖࡘࠬᖚ"), bstack11lllll11l1_opy_ + bstack1l1lll_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᖛ"), data, config)
    bstack11llll111l1_opy_ = response.json()
    if bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᖜ")]:
      parsed = json.loads(os.getenv(bstack1l1lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖝ"), bstack1l1lll_opy_ (u"ࠫࢀࢃࠧᖞ")))
      parsed[bstack1l1lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖟ")] = bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖠ")][bstack1l1lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖡ")]
      os.environ[bstack1l1lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᖢ")] = json.dumps(parsed)
      bstack11ll11ll11_opy_.bstack111llll11_opy_(bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᖣ")][bstack1l1lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᖤ")])
      bstack11ll11ll11_opy_.bstack11llll11l1l_opy_(bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"ࠫࡩࡧࡴࡢࠩᖥ")][bstack1l1lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᖦ")])
      bstack11ll11ll11_opy_.store()
      return bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖧ")][bstack1l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᖨ")], bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖩ")][bstack1l1lll_opy_ (u"ࠩ࡬ࡨࠬᖪ")]
    else:
      logger.error(bstack1l1lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᖫ") + bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖬ")])
      if bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖭ")] == bstack1l1lll_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᖮ"):
        for bstack11lll1llll1_opy_ in bstack11llll111l1_opy_[bstack1l1lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᖯ")]:
          logger.error(bstack11lll1llll1_opy_[bstack1l1lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖰ")])
      return None, None
  except Exception as error:
    logger.error(bstack1l1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᖱ") +  str(error))
    return None, None
def bstack11lllll1111_opy_():
  if os.getenv(bstack1l1lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖲ")) is None:
    return {
        bstack1l1lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᖳ"): bstack1l1lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᖴ"),
        bstack1l1lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖵ"): bstack1l1lll_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᖶ")
    }
  data = {bstack1l1lll_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᖷ"): bstack1l1ll1ll_opy_()}
  headers = {
      bstack1l1lll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᖸ"): bstack1l1lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᖹ") + os.getenv(bstack1l1lll_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᖺ")),
      bstack1l1lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖻ"): bstack1l1lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᖼ")
  }
  response = bstack11ll1l111l_opy_(bstack1l1lll_opy_ (u"ࠧࡑࡗࡗࠫᖽ"), bstack11lllll11l1_opy_ + bstack1l1lll_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᖾ"), data, { bstack1l1lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᖿ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1l1lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᗀ") + bstack111l1lll1l_opy_().isoformat() + bstack1l1lll_opy_ (u"ࠫ࡟࠭ᗁ"))
      return {bstack1l1lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᗂ"): bstack1l1lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᗃ"), bstack1l1lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗄ"): bstack1l1lll_opy_ (u"ࠨࠩᗅ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1l1lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᗆ") + str(error))
    return {
        bstack1l1lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᗇ"): bstack1l1lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᗈ"),
        bstack1l1lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗉ"): str(error)
    }
def bstack11llll1111l_opy_(bstack11llll111ll_opy_):
    return re.match(bstack1l1lll_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᗊ"), bstack11llll111ll_opy_.strip()) is not None
def bstack111ll1lll_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11lll1ll11l_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll1ll11l_opy_ = desired_capabilities
        else:
          bstack11lll1ll11l_opy_ = {}
        bstack11lll1ll1l1_opy_ = (bstack11lll1ll11l_opy_.get(bstack1l1lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᗋ"), bstack1l1lll_opy_ (u"ࠨࠩᗌ")).lower() or caps.get(bstack1l1lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᗍ"), bstack1l1lll_opy_ (u"ࠪࠫᗎ")).lower())
        if bstack11lll1ll1l1_opy_ == bstack1l1lll_opy_ (u"ࠫ࡮ࡵࡳࠨᗏ"):
            return True
        if bstack11lll1ll1l1_opy_ == bstack1l1lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᗐ"):
            bstack11lllll111l_opy_ = str(float(caps.get(bstack1l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗑ")) or bstack11lll1ll11l_opy_.get(bstack1l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗒ"), {}).get(bstack1l1lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᗓ"),bstack1l1lll_opy_ (u"ࠩࠪᗔ"))))
            if bstack11lll1ll1l1_opy_ == bstack1l1lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᗕ") and int(bstack11lllll111l_opy_.split(bstack1l1lll_opy_ (u"ࠫ࠳࠭ᗖ"))[0]) < float(bstack11lll1lll11_opy_):
                logger.warning(str(bstack11llll11ll1_opy_))
                return False
            return True
        bstack1ll1l1l1l1l_opy_ = caps.get(bstack1l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗗ"), {}).get(bstack1l1lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᗘ"), caps.get(bstack1l1lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᗙ"), bstack1l1lll_opy_ (u"ࠨࠩᗚ")))
        if bstack1ll1l1l1l1l_opy_:
            logger.warn(bstack1l1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᗛ"))
            return False
        browser = caps.get(bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᗜ"), bstack1l1lll_opy_ (u"ࠫࠬᗝ")).lower() or bstack11lll1ll11l_opy_.get(bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᗞ"), bstack1l1lll_opy_ (u"࠭ࠧᗟ")).lower()
        if browser != bstack1l1lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᗠ"):
            logger.warning(bstack1l1lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᗡ"))
            return False
        browser_version = caps.get(bstack1l1lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗢ")) or caps.get(bstack1l1lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᗣ")) or bstack11lll1ll11l_opy_.get(bstack1l1lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗤ")) or bstack11lll1ll11l_opy_.get(bstack1l1lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗥ"), {}).get(bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗦ")) or bstack11lll1ll11l_opy_.get(bstack1l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗧ"), {}).get(bstack1l1lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᗨ"))
        if browser_version and browser_version != bstack1l1lll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᗩ") and int(browser_version.split(bstack1l1lll_opy_ (u"ࠪ࠲ࠬᗪ"))[0]) <= 98:
            logger.warning(bstack1l1lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠸࠯ࠤᗫ"))
            return False
        if not options:
            bstack1ll1l1l1ll1_opy_ = caps.get(bstack1l1lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᗬ")) or bstack11lll1ll11l_opy_.get(bstack1l1lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᗭ"), {})
            if bstack1l1lll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᗮ") in bstack1ll1l1l1ll1_opy_.get(bstack1l1lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᗯ"), []):
                logger.warn(bstack1l1lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᗰ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack1l1lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᗱ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lll1l11l11_opy_ = config.get(bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗲ"), {})
    bstack1lll1l11l11_opy_[bstack1l1lll_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᗳ")] = os.getenv(bstack1l1lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᗴ"))
    bstack11llll1l11l_opy_ = json.loads(os.getenv(bstack1l1lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᗵ"), bstack1l1lll_opy_ (u"ࠨࡽࢀࠫᗶ"))).get(bstack1l1lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗷ"))
    caps[bstack1l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗸ")] = True
    if not config[bstack1l1lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᗹ")].get(bstack1l1lll_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᗺ")):
      if bstack1l1lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᗻ") in caps:
        caps[bstack1l1lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗼ")][bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᗽ")] = bstack1lll1l11l11_opy_
        caps[bstack1l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗾ")][bstack1l1lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᗿ")][bstack1l1lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘀ")] = bstack11llll1l11l_opy_
      else:
        caps[bstack1l1lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᘁ")] = bstack1lll1l11l11_opy_
        caps[bstack1l1lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᘂ")][bstack1l1lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘃ")] = bstack11llll1l11l_opy_
  except Exception as error:
    logger.debug(bstack1l1lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤᘄ") +  str(error))
def bstack1l1l11111l_opy_(driver, bstack11llll1l1l1_opy_):
  try:
    setattr(driver, bstack1l1lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᘅ"), True)
    session = driver.session_id
    if session:
      bstack11lllll1l1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lllll1l1l_opy_ = False
      bstack11lllll1l1l_opy_ = url.scheme in [bstack1l1lll_opy_ (u"ࠥ࡬ࡹࡺࡰࠣᘆ"), bstack1l1lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᘇ")]
      if bstack11lllll1l1l_opy_:
        if bstack11llll1l1l1_opy_:
          logger.info(bstack1l1lll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧᘈ"))
      return bstack11llll1l1l1_opy_
  except Exception as e:
    logger.error(bstack1l1lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᘉ") + str(e))
    return False
def bstack1111l1111_opy_(driver, name, path):
  try:
    bstack1ll1ll1ll1l_opy_ = {
        bstack1l1lll_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᘊ"): threading.current_thread().current_test_uuid,
        bstack1l1lll_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᘋ"): os.environ.get(bstack1l1lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᘌ"), bstack1l1lll_opy_ (u"ࠪࠫᘍ")),
        bstack1l1lll_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨᘎ"): os.environ.get(bstack1l1lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᘏ"), bstack1l1lll_opy_ (u"࠭ࠧᘐ"))
    }
    bstack1ll1l11lll1_opy_ = bstack1ll11111l1_opy_.bstack1ll1l1ll1l1_opy_(EVENTS.bstack1ll11l1l11_opy_.value)
    logger.debug(bstack1l1lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᘑ"))
    try:
      if (bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᘒ"), None) and bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᘓ"), None)):
        scripts = {bstack1l1lll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᘔ"): bstack11ll11ll11_opy_.perform_scan}
        bstack11llll1ll11_opy_ = json.loads(scripts[bstack1l1lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘕ")].replace(bstack1l1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘖ"), bstack1l1lll_opy_ (u"ࠨࠢᘗ")))
        bstack11llll1ll11_opy_[bstack1l1lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᘘ")][bstack1l1lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᘙ")] = None
        scripts[bstack1l1lll_opy_ (u"ࠤࡶࡧࡦࡴࠢᘚ")] = bstack1l1lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᘛ") + json.dumps(bstack11llll1ll11_opy_)
        bstack11ll11ll11_opy_.bstack111llll11_opy_(scripts)
        bstack11ll11ll11_opy_.store()
        logger.debug(driver.execute_script(bstack11ll11ll11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll11ll11_opy_.perform_scan, {bstack1l1lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᘜ"): name}))
      bstack1ll11111l1_opy_.end(EVENTS.bstack1ll11l1l11_opy_.value, bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘝ"), bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᘞ"), True, None)
    except Exception as error:
      bstack1ll11111l1_opy_.end(EVENTS.bstack1ll11l1l11_opy_.value, bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘟ"), bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘠ"), False, str(error))
    bstack1ll1l11lll1_opy_ = bstack1ll11111l1_opy_.bstack11lll1ll1ll_opy_(EVENTS.bstack1ll1l1ll1ll_opy_.value)
    bstack1ll11111l1_opy_.mark(bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘡ"))
    try:
      if (bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᘢ"), None) and bstack1l111l11_opy_(threading.current_thread(), bstack1l1lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᘣ"), None)):
        scripts = {bstack1l1lll_opy_ (u"ࠬࡹࡣࡢࡰࠪᘤ"): bstack11ll11ll11_opy_.perform_scan}
        bstack11llll1ll11_opy_ = json.loads(scripts[bstack1l1lll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘥ")].replace(bstack1l1lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘦ"), bstack1l1lll_opy_ (u"ࠣࠤᘧ")))
        bstack11llll1ll11_opy_[bstack1l1lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᘨ")][bstack1l1lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᘩ")] = None
        scripts[bstack1l1lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘪ")] = bstack1l1lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘫ") + json.dumps(bstack11llll1ll11_opy_)
        bstack11ll11ll11_opy_.bstack111llll11_opy_(scripts)
        bstack11ll11ll11_opy_.store()
        logger.debug(driver.execute_script(bstack11ll11ll11_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack11ll11ll11_opy_.bstack11llll1lll1_opy_, bstack1ll1ll1ll1l_opy_))
      bstack1ll11111l1_opy_.end(bstack1ll1l11lll1_opy_, bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘬ"), bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᘭ"),True, None)
    except Exception as error:
      bstack1ll11111l1_opy_.end(bstack1ll1l11lll1_opy_, bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘮ"), bstack1ll1l11lll1_opy_ + bstack1l1lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘯ"),False, str(error))
    logger.info(bstack1l1lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᘰ"))
  except Exception as bstack1ll1l1l111l_opy_:
    logger.error(bstack1l1lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᘱ") + str(path) + bstack1l1lll_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᘲ") + str(bstack1ll1l1l111l_opy_))
def bstack11llllll111_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1l1lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᘳ")) and str(caps.get(bstack1l1lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᘴ"))).lower() == bstack1l1lll_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᘵ"):
        bstack11lllll111l_opy_ = caps.get(bstack1l1lll_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᘶ")) or caps.get(bstack1l1lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᘷ"))
        if bstack11lllll111l_opy_ and int(str(bstack11lllll111l_opy_)) < bstack11lll1lll11_opy_:
            return False
    return True
def bstack1ll11ll111_opy_(config):
  if bstack1l1lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘸ") in config:
        return config[bstack1l1lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘹ")]
  for platform in config.get(bstack1l1lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘺ"), []):
      if bstack1l1lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘻ") in platform:
          return platform[bstack1l1lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘼ")]
  return None