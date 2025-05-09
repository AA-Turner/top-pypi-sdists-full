# coding: UTF-8
import sys
bstack111l1l1_opy_ = sys.version_info [0] == 2
bstack1ll1l1l_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack11lll_opy_ (bstack111ll1l_opy_):
    global bstack1l111l_opy_
    bstack1lllll1l_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack11111ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11ll1l1_opy_ = bstack1lllll1l_opy_ % len (bstack11111ll_opy_)
    bstack1lll1l1_opy_ = bstack11111ll_opy_ [:bstack11ll1l1_opy_] + bstack11111ll_opy_ [bstack11ll1l1_opy_:]
    if bstack111l1l1_opy_:
        bstack1ll1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    else:
        bstack1ll1ll1_opy_ = str () .join ([chr (ord (char) - bstack1ll1l1l_opy_ - (bstack11l11l_opy_ + bstack1lllll1l_opy_) % bstack1l11l11_opy_) for bstack11l11l_opy_, char in enumerate (bstack1lll1l1_opy_)])
    return eval (bstack1ll1ll1_opy_)
import os
import json
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11llll1llll_opy_ as bstack11llll111l1_opy_, EVENTS
from bstack_utils.bstack1l1111l1_opy_ import bstack1l1111l1_opy_
from bstack_utils.helper import bstack11ll11l1ll_opy_, bstack111l1l1ll1_opy_, bstack1l111l1ll1_opy_, bstack11lll1ll111_opy_, \
  bstack11llll11ll1_opy_, bstack11lllll11_opy_, get_host_info, bstack11lll1l1lll_opy_, bstack1lll1ll11l_opy_, bstack111l11l1ll_opy_, bstack1llll11ll1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1l11lll1_opy_ import get_logger
from bstack_utils.bstack1lll1ll1l1_opy_ import bstack1ll1llllll1_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1lll1ll1l1_opy_ = bstack1ll1llllll1_opy_()
@bstack111l11l1ll_opy_(class_method=False)
def _11llll1l1ll_opy_(driver, bstack1111lll11l_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack11lll_opy_ (u"ࠧࡰࡵࡢࡲࡦࡳࡥࠨᕛ"): caps.get(bstack11lll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠧᕜ"), None),
        bstack11lll_opy_ (u"ࠩࡲࡷࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ᕝ"): bstack1111lll11l_opy_.get(bstack11lll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᕞ"), None),
        bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡤࡴࡡ࡮ࡧࠪᕟ"): caps.get(bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᕠ"), None),
        bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕡ"): caps.get(bstack11lll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕢ"), None)
    }
  except Exception as error:
    logger.debug(bstack11lll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡧࡧࡷࡧ࡭࡯࡮ࡨࠢࡳࡰࡦࡺࡦࡰࡴࡰࠤࡩ࡫ࡴࡢ࡫࡯ࡷࠥࡽࡩࡵࡪࠣࡩࡷࡸ࡯ࡳࠢ࠽ࠤࠬᕣ") + str(error))
  return response
def on():
    if os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕤ"), None) is None or os.environ[bstack11lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕥ")] == bstack11lll_opy_ (u"ࠦࡳࡻ࡬࡭ࠤᕦ"):
        return False
    return True
def bstack11ll111l1l_opy_(config):
  return config.get(bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕧ"), False) or any([p.get(bstack11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕨ"), False) == True for p in config.get(bstack11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡵࠪᕩ"), [])])
def bstack11l1ll111_opy_(config, bstack1111l111l_opy_):
  try:
    if not bstack1l111l1ll1_opy_(config):
      return False
    bstack11llll1lll1_opy_ = config.get(bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕪ"), False)
    if int(bstack1111l111l_opy_) < len(config.get(bstack11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᕫ"), [])) and config[bstack11lll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡸ࠭ᕬ")][bstack1111l111l_opy_]:
      bstack11llll111ll_opy_ = config[bstack11lll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕭ")][bstack1111l111l_opy_].get(bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᕮ"), None)
    else:
      bstack11llll111ll_opy_ = config.get(bstack11lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᕯ"), None)
    if bstack11llll111ll_opy_ != None:
      bstack11llll1lll1_opy_ = bstack11llll111ll_opy_
    bstack11llll1l111_opy_ = os.getenv(bstack11lll_opy_ (u"ࠧࡃࡕࡢࡅ࠶࠷࡙ࡠࡌ࡚ࡘࠬᕰ")) is not None and len(os.getenv(bstack11lll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᕱ"))) > 0 and os.getenv(bstack11lll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕲ")) != bstack11lll_opy_ (u"ࠪࡲࡺࡲ࡬ࠨᕳ")
    return bstack11llll1lll1_opy_ and bstack11llll1l111_opy_
  except Exception as error:
    logger.debug(bstack11lll_opy_ (u"ࠫࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡪࡰࠣࡺࡪࡸࡩࡧࡻ࡬ࡲ࡬ࠦࡴࡩࡧࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡷࡪࡹࡳࡪࡱࡱࠤࡼ࡯ࡴࡩࠢࡨࡶࡷࡵࡲࠡ࠼ࠣࠫᕴ") + str(error))
  return False
def bstack1l11l111l_opy_(test_tags):
  bstack1ll1l1ll111_opy_ = os.getenv(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᕵ"))
  if bstack1ll1l1ll111_opy_ is None:
    return True
  bstack1ll1l1ll111_opy_ = json.loads(bstack1ll1l1ll111_opy_)
  try:
    include_tags = bstack1ll1l1ll111_opy_[bstack11lll_opy_ (u"࠭ࡩ࡯ࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕶ")] if bstack11lll_opy_ (u"ࠧࡪࡰࡦࡰࡺࡪࡥࡕࡣࡪࡷࡎࡴࡔࡦࡵࡷ࡭ࡳ࡭ࡓࡤࡱࡳࡩࠬᕷ") in bstack1ll1l1ll111_opy_ and isinstance(bstack1ll1l1ll111_opy_[bstack11lll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕸ")], list) else []
    exclude_tags = bstack1ll1l1ll111_opy_[bstack11lll_opy_ (u"ࠩࡨࡼࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕹ")] if bstack11lll_opy_ (u"ࠪࡩࡽࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕺ") in bstack1ll1l1ll111_opy_ and isinstance(bstack1ll1l1ll111_opy_[bstack11lll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕻ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack11lll_opy_ (u"ࠧࡋࡲࡳࡱࡵࠤࡼ࡮ࡩ࡭ࡧࠣࡺࡦࡲࡩࡥࡣࡷ࡭ࡳ࡭ࠠࡵࡧࡶࡸࠥࡩࡡࡴࡧࠣࡪࡴࡸࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡣࡧࡩࡳࡷ࡫ࠠࡴࡥࡤࡲࡳ࡯࡮ࡨ࠰ࠣࡉࡷࡸ࡯ࡳࠢ࠽ࠤࠧᕼ") + str(error))
  return False
def bstack11lll1lll1l_opy_(config, bstack11llll1111l_opy_, bstack11lll1ll1l1_opy_, bstack11lll1lll11_opy_):
  bstack11lllll1l11_opy_ = bstack11lll1ll111_opy_(config)
  bstack11llll1ll11_opy_ = bstack11llll11ll1_opy_(config)
  if bstack11lllll1l11_opy_ is None or bstack11llll1ll11_opy_ is None:
    logger.error(bstack11lll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡸࡪࡹࡴࠡࡴࡸࡲࠥ࡬࡯ࡳࠢࡅࡶࡴࡽࡳࡦࡴࡖࡸࡦࡩ࡫ࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲ࠿ࠦࡍࡪࡵࡶ࡭ࡳ࡭ࠠࡢࡷࡷ࡬ࡪࡴࡴࡪࡥࡤࡸ࡮ࡵ࡮ࠡࡶࡲ࡯ࡪࡴࠧᕽ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᕾ"), bstack11lll_opy_ (u"ࠨࡽࢀࠫᕿ")))
    data = {
        bstack11lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧᖀ"): config[bstack11lll_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨᖁ")],
        bstack11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧᖂ"): config.get(bstack11lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨᖃ"), os.path.basename(os.getcwd())),
        bstack11lll_opy_ (u"࠭ࡳࡵࡣࡵࡸ࡙࡯࡭ࡦࠩᖄ"): bstack11ll11l1ll_opy_(),
        bstack11lll_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬᖅ"): config.get(bstack11lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫᖆ"), bstack11lll_opy_ (u"ࠩࠪᖇ")),
        bstack11lll_opy_ (u"ࠪࡷࡴࡻࡲࡤࡧࠪᖈ"): {
            bstack11lll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫᖉ"): bstack11llll1111l_opy_,
            bstack11lll_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖊ"): bstack11lll1ll1l1_opy_,
            bstack11lll_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᖋ"): __version__,
            bstack11lll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩᖌ"): bstack11lll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨᖍ"),
            bstack11lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩᖎ"): bstack11lll_opy_ (u"ࠪࡷࡪࡲࡥ࡯࡫ࡸࡱࠬᖏ"),
            bstack11lll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫᖐ"): bstack11lll1lll11_opy_
        },
        bstack11lll_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧᖑ"): settings,
        bstack11lll_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴࡃࡰࡰࡷࡶࡴࡲࠧᖒ"): bstack11lll1l1lll_opy_(),
        bstack11lll_opy_ (u"ࠧࡤ࡫ࡌࡲ࡫ࡵࠧᖓ"): bstack11lllll11_opy_(),
        bstack11lll_opy_ (u"ࠨࡪࡲࡷࡹࡏ࡮ࡧࡱࠪᖔ"): get_host_info(),
        bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱࠫᖕ"): bstack1l111l1ll1_opy_(config)
    }
    headers = {
        bstack11lll_opy_ (u"ࠪࡇࡴࡴࡴࡦࡰࡷ࠱࡙ࡿࡰࡦࠩᖖ"): bstack11lll_opy_ (u"ࠫࡦࡶࡰ࡭࡫ࡦࡥࡹ࡯࡯࡯࠱࡭ࡷࡴࡴࠧᖗ"),
    }
    config = {
        bstack11lll_opy_ (u"ࠬࡧࡵࡵࡪࠪᖘ"): (bstack11lllll1l11_opy_, bstack11llll1ll11_opy_),
        bstack11lll_opy_ (u"࠭ࡨࡦࡣࡧࡩࡷࡹࠧᖙ"): headers
    }
    response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠧࡑࡑࡖࡘࠬᖚ"), bstack11llll111l1_opy_ + bstack11lll_opy_ (u"ࠨ࠱ࡹ࠶࠴ࡺࡥࡴࡶࡢࡶࡺࡴࡳࠨᖛ"), data, config)
    bstack11lll1llll1_opy_ = response.json()
    if bstack11lll1llll1_opy_[bstack11lll_opy_ (u"ࠩࡶࡹࡨࡩࡥࡴࡵࠪᖜ")]:
      parsed = json.loads(os.getenv(bstack11lll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖝ"), bstack11lll_opy_ (u"ࠫࢀࢃࠧᖞ")))
      parsed[bstack11lll_opy_ (u"ࠬࡹࡣࡢࡰࡱࡩࡷ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖟ")] = bstack11lll1llll1_opy_[bstack11lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖠ")][bstack11lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖡ")]
      os.environ[bstack11lll_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩᖢ")] = json.dumps(parsed)
      bstack1l1111l1_opy_.bstack11ll11llll_opy_(bstack11lll1llll1_opy_[bstack11lll_opy_ (u"ࠩࡧࡥࡹࡧࠧᖣ")][bstack11lll_opy_ (u"ࠪࡷࡨࡸࡩࡱࡶࡶࠫᖤ")])
      bstack1l1111l1_opy_.bstack11llll1ll1l_opy_(bstack11lll1llll1_opy_[bstack11lll_opy_ (u"ࠫࡩࡧࡴࡢࠩᖥ")][bstack11lll_opy_ (u"ࠬࡩ࡯࡮࡯ࡤࡲࡩࡹࠧᖦ")])
      bstack1l1111l1_opy_.store()
      return bstack11lll1llll1_opy_[bstack11lll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖧ")][bstack11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡔࡰ࡭ࡨࡲࠬᖨ")], bstack11lll1llll1_opy_[bstack11lll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖩ")][bstack11lll_opy_ (u"ࠩ࡬ࡨࠬᖪ")]
    else:
      logger.error(bstack11lll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡸࡵ࡯ࡰ࡬ࡲ࡬ࠦࡂࡳࡱࡺࡷࡪࡸࡓࡵࡣࡦ࡯ࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯࠼ࠣࠫᖫ") + bstack11lll1llll1_opy_[bstack11lll_opy_ (u"ࠫࡲ࡫ࡳࡴࡣࡪࡩࠬᖬ")])
      if bstack11lll1llll1_opy_[bstack11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᖭ")] == bstack11lll_opy_ (u"࠭ࡉ࡯ࡸࡤࡰ࡮ࡪࠠࡤࡱࡱࡪ࡮࡭ࡵࡳࡣࡷ࡭ࡴࡴࠠࡱࡣࡶࡷࡪࡪ࠮ࠨᖮ"):
        for bstack11llll11l1l_opy_ in bstack11lll1llll1_opy_[bstack11lll_opy_ (u"ࠧࡦࡴࡵࡳࡷࡹࠧᖯ")]:
          logger.error(bstack11llll11l1l_opy_[bstack11lll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖰ")])
      return None, None
  except Exception as error:
    logger.error(bstack11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡴࡦࡵࡷࠤࡷࡻ࡮ࠡࡨࡲࡶࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮࠻ࠢࠥᖱ") +  str(error))
    return None, None
def bstack11lllll1l1l_opy_():
  if os.getenv(bstack11lll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᖲ")) is None:
    return {
        bstack11lll_opy_ (u"ࠫࡸࡺࡡࡵࡷࡶࠫᖳ"): bstack11lll_opy_ (u"ࠬ࡫ࡲࡳࡱࡵࠫᖴ"),
        bstack11lll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖵ"): bstack11lll_opy_ (u"ࠧࡃࡷ࡬ࡰࡩࠦࡣࡳࡧࡤࡸ࡮ࡵ࡮ࠡࡪࡤࡨࠥ࡬ࡡࡪ࡮ࡨࡨ࠳࠭ᖶ")
    }
  data = {bstack11lll_opy_ (u"ࠨࡧࡱࡨ࡙࡯࡭ࡦࠩᖷ"): bstack11ll11l1ll_opy_()}
  headers = {
      bstack11lll_opy_ (u"ࠩࡄࡹࡹ࡮࡯ࡳ࡫ࡽࡥࡹ࡯࡯࡯ࠩᖸ"): bstack11lll_opy_ (u"ࠪࡆࡪࡧࡲࡦࡴࠣࠫᖹ") + os.getenv(bstack11lll_opy_ (u"ࠦࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠤᖺ")),
      bstack11lll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖻ"): bstack11lll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᖼ")
  }
  response = bstack1lll1ll11l_opy_(bstack11lll_opy_ (u"ࠧࡑࡗࡗࠫᖽ"), bstack11llll111l1_opy_ + bstack11lll_opy_ (u"ࠨ࠱ࡷࡩࡸࡺ࡟ࡳࡷࡱࡷ࠴ࡹࡴࡰࡲࠪᖾ"), data, { bstack11lll_opy_ (u"ࠩ࡫ࡩࡦࡪࡥࡳࡵࠪᖿ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack11lll_opy_ (u"ࠥࡆࡷࡵࡷࡴࡧࡵࡗࡹࡧࡣ࡬ࠢࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡔࡦࡵࡷࠤࡗࡻ࡮ࠡ࡯ࡤࡶࡰ࡫ࡤࠡࡣࡶࠤࡨࡵ࡭ࡱ࡮ࡨࡸࡪࡪࠠࡢࡶࠣࠦᗀ") + bstack111l1l1ll1_opy_().isoformat() + bstack11lll_opy_ (u"ࠫ࡟࠭ᗁ"))
      return {bstack11lll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᗂ"): bstack11lll_opy_ (u"࠭ࡳࡶࡥࡦࡩࡸࡹࠧᗃ"), bstack11lll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗄ"): bstack11lll_opy_ (u"ࠨࠩᗅ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack11lll_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡲࡧࡲ࡬࡫ࡱ࡫ࠥࡩ࡯࡮ࡲ࡯ࡩࡹ࡯࡯࡯ࠢࡲࡪࠥࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰ࠽ࠤࠧᗆ") + str(error))
    return {
        bstack11lll_opy_ (u"ࠪࡷࡹࡧࡴࡶࡵࠪᗇ"): bstack11lll_opy_ (u"ࠫࡪࡸࡲࡰࡴࠪᗈ"),
        bstack11lll_opy_ (u"ࠬࡳࡥࡴࡵࡤ࡫ࡪ࠭ᗉ"): str(error)
    }
def bstack11llll11lll_opy_(bstack11lllll1lll_opy_):
    return re.match(bstack11lll_opy_ (u"ࡸࠧ࡟࡞ࡧ࠯࠭ࡢ࠮࡝ࡦ࠮࠭ࡄࠪࠧᗊ"), bstack11lllll1lll_opy_.strip()) is not None
def bstack1l1ll1l1l_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11llll1l1l1_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11llll1l1l1_opy_ = desired_capabilities
        else:
          bstack11llll1l1l1_opy_ = {}
        bstack11lllll111l_opy_ = (bstack11llll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠧࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪ࠭ᗋ"), bstack11lll_opy_ (u"ࠨࠩᗌ")).lower() or caps.get(bstack11lll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᗍ"), bstack11lll_opy_ (u"ࠪࠫᗎ")).lower())
        if bstack11lllll111l_opy_ == bstack11lll_opy_ (u"ࠫ࡮ࡵࡳࠨᗏ"):
            return True
        if bstack11lllll111l_opy_ == bstack11lll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᗐ"):
            bstack11lllll1111_opy_ = str(float(caps.get(bstack11lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡗࡧࡵࡷ࡮ࡵ࡮ࠨᗑ")) or bstack11llll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗒ"), {}).get(bstack11lll_opy_ (u"ࠨࡱࡶ࡚ࡪࡸࡳࡪࡱࡱࠫᗓ"),bstack11lll_opy_ (u"ࠩࠪᗔ"))))
            if bstack11lllll111l_opy_ == bstack11lll_opy_ (u"ࠪࡥࡳࡪࡲࡰ࡫ࡧࠫᗕ") and int(bstack11lllll1111_opy_.split(bstack11lll_opy_ (u"ࠫ࠳࠭ᗖ"))[0]) < float(bstack11lllll11l1_opy_):
                logger.warning(str(bstack11lll1lllll_opy_))
                return False
            return True
        bstack1ll1l11lll1_opy_ = caps.get(bstack11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗗ"), {}).get(bstack11lll_opy_ (u"࠭ࡤࡦࡸ࡬ࡧࡪࡔࡡ࡮ࡧࠪᗘ"), caps.get(bstack11lll_opy_ (u"ࠧࡥࡧࡹ࡭ࡨ࡫ࠧᗙ"), bstack11lll_opy_ (u"ࠨࠩᗚ")))
        if bstack1ll1l11lll1_opy_:
            logger.warn(bstack11lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡷࡻ࡮ࠡࡱࡱࡰࡾࠦ࡯࡯ࠢࡇࡩࡸࡱࡴࡰࡲࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᗛ"))
            return False
        browser = caps.get(bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡒࡦࡳࡥࠨᗜ"), bstack11lll_opy_ (u"ࠫࠬᗝ")).lower() or bstack11llll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᗞ"), bstack11lll_opy_ (u"࠭ࠧᗟ")).lower()
        if browser != bstack11lll_opy_ (u"ࠧࡤࡪࡵࡳࡲ࡫ࠧᗠ"):
            logger.warning(bstack11lll_opy_ (u"ࠣࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠥࡽࡩ࡭࡮ࠣࡶࡺࡴࠠࡰࡰ࡯ࡽࠥࡵ࡮ࠡࡅ࡫ࡶࡴࡳࡥࠡࡤࡵࡳࡼࡹࡥࡳࡵ࠱ࠦᗡ"))
            return False
        browser_version = caps.get(bstack11lll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗢ")) or caps.get(bstack11lll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᗣ")) or bstack11llll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗤ")) or bstack11llll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠬࡨࡳࡵࡣࡦ࡯࠿ࡵࡰࡵ࡫ࡲࡲࡸ࠭ᗥ"), {}).get(bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗦ")) or bstack11llll1l1l1_opy_.get(bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗧ"), {}).get(bstack11lll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᗨ"))
        if browser_version and browser_version != bstack11lll_opy_ (u"ࠩ࡯ࡥࡹ࡫ࡳࡵࠩᗩ") and int(browser_version.split(bstack11lll_opy_ (u"ࠪ࠲ࠬᗪ"))[0]) <= 98:
            logger.warning(bstack11lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡈ࡮ࡲࡰ࡯ࡨࠤࡧࡸ࡯ࡸࡵࡨࡶࠥࡼࡥࡳࡵ࡬ࡳࡳࠦࡧࡳࡧࡤࡸࡪࡸࠠࡵࡪࡤࡲࠥ࠿࠸࠯ࠤᗫ"))
            return False
        if not options:
            bstack1ll1l111lll_opy_ = caps.get(bstack11lll_opy_ (u"ࠬ࡭࡯ࡰࡩ࠽ࡧ࡭ࡸ࡯࡮ࡧࡒࡴࡹ࡯࡯࡯ࡵࠪᗬ")) or bstack11llll1l1l1_opy_.get(bstack11lll_opy_ (u"࠭ࡧࡰࡱࡪ࠾ࡨ࡮ࡲࡰ࡯ࡨࡓࡵࡺࡩࡰࡰࡶࠫᗭ"), {})
            if bstack11lll_opy_ (u"ࠧ࠮࠯࡫ࡩࡦࡪ࡬ࡦࡵࡶࠫᗮ") in bstack1ll1l111lll_opy_.get(bstack11lll_opy_ (u"ࠨࡣࡵ࡫ࡸ࠭ᗯ"), []):
                logger.warn(bstack11lll_opy_ (u"ࠤࡄࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡷࡪ࡮࡯ࠤࡳࡵࡴࠡࡴࡸࡲࠥࡵ࡮ࠡ࡮ࡨ࡫ࡦࡩࡹࠡࡪࡨࡥࡩࡲࡥࡴࡵࠣࡱࡴࡪࡥ࠯ࠢࡖࡻ࡮ࡺࡣࡩࠢࡷࡳࠥࡴࡥࡸࠢ࡫ࡩࡦࡪ࡬ࡦࡵࡶࠤࡲࡵࡤࡦࠢࡲࡶࠥࡧࡶࡰ࡫ࡧࠤࡺࡹࡩ࡯ࡩࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠦᗰ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack11lll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡹࡥࡱ࡯ࡤࡢࡶࡨࠤࡦ࠷࠱ࡺࠢࡶࡹࡵࡶ࡯ࡳࡶࠣ࠾ࠧᗱ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1lllll11111_opy_ = config.get(bstack11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᗲ"), {})
    bstack1lllll11111_opy_[bstack11lll_opy_ (u"ࠬࡧࡵࡵࡪࡗࡳࡰ࡫࡮ࠨᗳ")] = os.getenv(bstack11lll_opy_ (u"࠭ࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠫᗴ"))
    bstack11llll11l11_opy_ = json.loads(os.getenv(bstack11lll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᗵ"), bstack11lll_opy_ (u"ࠨࡽࢀࠫᗶ"))).get(bstack11lll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗷ"))
    caps[bstack11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᗸ")] = True
    if not config[bstack11lll_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡓࡶࡴࡪࡵࡤࡶࡐࡥࡵ࠭ᗹ")].get(bstack11lll_opy_ (u"ࠧࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠦᗺ")):
      if bstack11lll_opy_ (u"࠭ࡢࡴࡶࡤࡧࡰࡀ࡯ࡱࡶ࡬ࡳࡳࡹࠧᗻ") in caps:
        caps[bstack11lll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗼ")][bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡐࡲࡷ࡭ࡴࡴࡳࠨᗽ")] = bstack1lllll11111_opy_
        caps[bstack11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗾ")][bstack11lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᗿ")][bstack11lll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᘀ")] = bstack11llll11l11_opy_
      else:
        caps[bstack11lll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮࠲ࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡓࡵࡺࡩࡰࡰࡶࠫᘁ")] = bstack1lllll11111_opy_
        caps[bstack11lll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯࠳ࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᘂ")][bstack11lll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᘃ")] = bstack11llll11l11_opy_
  except Exception as error:
    logger.debug(bstack11lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡷࡪࡺࡴࡪࡰࡪࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡥࡤࡴࡦࡨࡩ࡭࡫ࡷ࡭ࡪࡹ࠮ࠡࡇࡵࡶࡴࡸ࠺ࠡࠤᘄ") +  str(error))
def bstack1ll1lll11l_opy_(driver, bstack11lllll1ll1_opy_):
  try:
    setattr(driver, bstack11lll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬ࡃ࠴࠵ࡾ࡙ࡨࡰࡷ࡯ࡨࡘࡩࡡ࡯ࠩᘅ"), True)
    session = driver.session_id
    if session:
      bstack11lll1ll11l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1ll11l_opy_ = False
      bstack11lll1ll11l_opy_ = url.scheme in [bstack11lll_opy_ (u"ࠥ࡬ࡹࡺࡰࠣᘆ"), bstack11lll_opy_ (u"ࠦ࡭ࡺࡴࡱࡵࠥᘇ")]
      if bstack11lll1ll11l_opy_:
        if bstack11lllll1ll1_opy_:
          logger.info(bstack11lll_opy_ (u"࡙ࠧࡥࡵࡷࡳࠤ࡫ࡵࡲࠡࡃࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠡࡶࡨࡷࡹ࡯࡮ࡨࠢ࡫ࡥࡸࠦࡳࡵࡣࡵࡸࡪࡪ࠮ࠡࡃࡸࡸࡴࡳࡡࡵࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࠦࡥࡹࡧࡦࡹࡹ࡯࡯࡯ࠢࡺ࡭ࡱࡲࠠࡣࡧࡪ࡭ࡳࠦ࡭ࡰ࡯ࡨࡲࡹࡧࡲࡪ࡮ࡼ࠲ࠧᘈ"))
      return bstack11lllll1ll1_opy_
  except Exception as e:
    logger.error(bstack11lll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡹࡴࡢࡴࡷ࡭ࡳ࡭ࠠࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡢࡷࡷࡳࡲࡧࡴࡪࡱࡱࠤࡸࡩࡡ࡯ࠢࡩࡳࡷࠦࡴࡩ࡫ࡶࠤࡹ࡫ࡳࡵࠢࡦࡥࡸ࡫࠺ࠡࠤᘉ") + str(e))
    return False
def bstack1lll1l1l1_opy_(driver, name, path):
  try:
    bstack1ll11lllll1_opy_ = {
        bstack11lll_opy_ (u"ࠧࡵࡪࡗࡩࡸࡺࡒࡶࡰࡘࡹ࡮ࡪࠧᘊ"): threading.current_thread().current_test_uuid,
        bstack11lll_opy_ (u"ࠨࡶ࡫ࡆࡺ࡯࡬ࡥࡗࡸ࡭ࡩ࠭ᘋ"): os.environ.get(bstack11lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡎࡕࡃࡡࡘ࡙ࡎࡊࠧᘌ"), bstack11lll_opy_ (u"ࠪࠫᘍ")),
        bstack11lll_opy_ (u"ࠫࡹ࡮ࡊࡸࡶࡗࡳࡰ࡫࡮ࠨᘎ"): os.environ.get(bstack11lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡊࡘࡆࡤࡐࡗࡕࠩᘏ"), bstack11lll_opy_ (u"࠭ࠧᘐ"))
    }
    bstack1ll11lll1l1_opy_ = bstack1lll1ll1l1_opy_.bstack1ll1ll111ll_opy_(EVENTS.bstack11lll1ll11_opy_.value)
    logger.debug(bstack11lll_opy_ (u"ࠧࡑࡧࡵࡪࡴࡸ࡭ࡪࡰࡪࠤࡸࡩࡡ࡯ࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡥࡻ࡯࡮ࡨࠢࡵࡩࡸࡻ࡬ࡵࡵࠪᘑ"))
    try:
      if (bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠨ࡫ࡶࡅࡵࡶࡁ࠲࠳ࡼࡘࡪࡹࡴࠨᘒ"), None) and bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠩࡤࡴࡵࡇ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫᘓ"), None)):
        scripts = {bstack11lll_opy_ (u"ࠪࡷࡨࡧ࡮ࠨᘔ"): bstack1l1111l1_opy_.perform_scan}
        bstack11llll11111_opy_ = json.loads(scripts[bstack11lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘕ")].replace(bstack11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘖ"), bstack11lll_opy_ (u"ࠨࠢᘗ")))
        bstack11llll11111_opy_[bstack11lll_opy_ (u"ࠧࡢࡴࡪࡹࡲ࡫࡮ࡵࡵࠪᘘ")][bstack11lll_opy_ (u"ࠨ࡯ࡨࡸ࡭ࡵࡤࠨᘙ")] = None
        scripts[bstack11lll_opy_ (u"ࠤࡶࡧࡦࡴࠢᘚ")] = bstack11lll_opy_ (u"ࠥࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡡࡨࡼࡪࡩࡵࡵࡱࡵ࠾ࠥࠨᘛ") + json.dumps(bstack11llll11111_opy_)
        bstack1l1111l1_opy_.bstack11ll11llll_opy_(scripts)
        bstack1l1111l1_opy_.store()
        logger.debug(driver.execute_script(bstack1l1111l1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1111l1_opy_.perform_scan, {bstack11lll_opy_ (u"ࠦࡲ࡫ࡴࡩࡱࡧࠦᘜ"): name}))
      bstack1lll1ll1l1_opy_.end(EVENTS.bstack11lll1ll11_opy_.value, bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠧࡀࡳࡵࡣࡵࡸࠧᘝ"), bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠨ࠺ࡦࡰࡧࠦᘞ"), True, None)
    except Exception as error:
      bstack1lll1ll1l1_opy_.end(EVENTS.bstack11lll1ll11_opy_.value, bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘟ"), bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘠ"), False, str(error))
    bstack1ll11lll1l1_opy_ = bstack1lll1ll1l1_opy_.bstack11lllll11ll_opy_(EVENTS.bstack1ll1l1l1111_opy_.value)
    bstack1lll1ll1l1_opy_.mark(bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘡ"))
    try:
      if (bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᘢ"), None) and bstack1llll11ll1_opy_(threading.current_thread(), bstack11lll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᘣ"), None)):
        scripts = {bstack11lll_opy_ (u"ࠬࡹࡣࡢࡰࠪᘤ"): bstack1l1111l1_opy_.perform_scan}
        bstack11llll11111_opy_ = json.loads(scripts[bstack11lll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘥ")].replace(bstack11lll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘦ"), bstack11lll_opy_ (u"ࠣࠤᘧ")))
        bstack11llll11111_opy_[bstack11lll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᘨ")][bstack11lll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᘩ")] = None
        scripts[bstack11lll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘪ")] = bstack11lll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘫ") + json.dumps(bstack11llll11111_opy_)
        bstack1l1111l1_opy_.bstack11ll11llll_opy_(scripts)
        bstack1l1111l1_opy_.store()
        logger.debug(driver.execute_script(bstack1l1111l1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1111l1_opy_.bstack11lll1ll1ll_opy_, bstack1ll11lllll1_opy_))
      bstack1lll1ll1l1_opy_.end(bstack1ll11lll1l1_opy_, bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠨ࠺ࡴࡶࡤࡶࡹࠨᘬ"), bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠢ࠻ࡧࡱࡨࠧᘭ"),True, None)
    except Exception as error:
      bstack1lll1ll1l1_opy_.end(bstack1ll11lll1l1_opy_, bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘮ"), bstack1ll11lll1l1_opy_ + bstack11lll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘯ"),False, str(error))
    logger.info(bstack11lll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦࠢ࡫ࡥࡸࠦࡥ࡯ࡦࡨࡨ࠳ࠨᘰ"))
  except Exception as bstack1ll1l1l1l1l_opy_:
    logger.error(bstack11lll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠥࡩ࡯ࡶ࡮ࡧࠤࡳࡵࡴࠡࡤࡨࠤࡵࡸ࡯ࡤࡧࡶࡷࡪࡪࠠࡧࡱࡵࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨ࠾ࠥࠨᘱ") + str(path) + bstack11lll_opy_ (u"ࠧࠦࡅࡳࡴࡲࡶࠥࡀࠢᘲ") + str(bstack1ll1l1l1l1l_opy_))
def bstack11llll1l11l_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack11lll_opy_ (u"ࠨࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡏࡣࡰࡩࠧᘳ")) and str(caps.get(bstack11lll_opy_ (u"ࠢࡱ࡮ࡤࡸ࡫ࡵࡲ࡮ࡐࡤࡱࡪࠨᘴ"))).lower() == bstack11lll_opy_ (u"ࠣࡣࡱࡨࡷࡵࡩࡥࠤᘵ"):
        bstack11lllll1111_opy_ = caps.get(bstack11lll_opy_ (u"ࠤࡤࡴࡵ࡯ࡵ࡮࠼ࡳࡰࡦࡺࡦࡰࡴࡰ࡚ࡪࡸࡳࡪࡱࡱࠦᘶ")) or caps.get(bstack11lll_opy_ (u"ࠥࡴࡱࡧࡴࡧࡱࡵࡱ࡛࡫ࡲࡴ࡫ࡲࡲࠧᘷ"))
        if bstack11lllll1111_opy_ and int(str(bstack11lllll1111_opy_)) < bstack11lllll11l1_opy_:
            return False
    return True
def bstack11ll1l1111_opy_(config):
  if bstack11lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫᘸ") in config:
        return config[bstack11lll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᘹ")]
  for platform in config.get(bstack11lll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᘺ"), []):
      if bstack11lll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘻ") in platform:
          return platform[bstack11lll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᘼ")]
  return None