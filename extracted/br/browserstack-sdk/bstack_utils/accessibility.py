# coding: UTF-8
import sys
bstack11l1l1_opy_ = sys.version_info [0] == 2
bstack111l1l1_opy_ = 2048
bstack11l11ll_opy_ = 7
def bstack1llllll_opy_ (bstack1ll111l_opy_):
    global bstack1l111l_opy_
    bstack1l11l_opy_ = ord (bstack1ll111l_opy_ [-1])
    bstack1111l1l_opy_ = bstack1ll111l_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack1l11l_opy_ % len (bstack1111l1l_opy_)
    bstack1ll1_opy_ = bstack1111l1l_opy_ [:bstack11ll1ll_opy_] + bstack1111l1l_opy_ [bstack11ll1ll_opy_:]
    if bstack11l1l1_opy_:
        bstack1lllll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    else:
        bstack1lllll1l_opy_ = str () .join ([chr (ord (char) - bstack111l1l1_opy_ - (bstack11ll1_opy_ + bstack1l11l_opy_) % bstack11l11ll_opy_) for bstack11ll1_opy_, char in enumerate (bstack1ll1_opy_)])
    return eval (bstack1lllll1l_opy_)
import os
import json
import requests
import logging
import threading
from urllib.parse import urlparse
from bstack_utils.constants import bstack11lllll1111_opy_ as bstack11llll11lll_opy_, EVENTS
from bstack_utils.bstack1l1llll1_opy_ import bstack1l1llll1_opy_
from bstack_utils.helper import bstack1l11l1l11l_opy_, bstack111l1l1l11_opy_, bstack1l1ll1lll_opy_, bstack11llll1l11l_opy_, \
  bstack11llll1ll11_opy_, bstack1l1ll111_opy_, get_host_info, bstack11llll11l1l_opy_, bstack1l1ll1111_opy_, bstack111l1l1111_opy_, bstack1lll11l1_opy_
from browserstack_sdk._version import __version__
from bstack_utils.bstack1llllll1ll_opy_ import get_logger
from bstack_utils.bstack1llll1l1_opy_ import bstack1lll1llll1l_opy_
from bstack_utils.constants import *
logger = get_logger(__name__)
bstack1llll1l1_opy_ = bstack1lll1llll1l_opy_()
@bstack111l1l1111_opy_(class_method=False)
def _11llll11l11_opy_(driver, bstack1111llllll_opy_):
  response = {}
  try:
    caps = driver.capabilities
    response = {
        bstack1llllll_opy_ (u"ࠩࡲࡷࡤࡴࡡ࡮ࡧࠪᕖ"): caps.get(bstack1llllll_opy_ (u"ࠪࡴࡱࡧࡴࡧࡱࡵࡱࡓࡧ࡭ࡦࠩᕗ"), None),
        bstack1llllll_opy_ (u"ࠫࡴࡹ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨᕘ"): bstack1111llllll_opy_.get(bstack1llllll_opy_ (u"ࠬࡵࡳࡗࡧࡵࡷ࡮ࡵ࡮ࠨᕙ"), None),
        bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸ࡟࡯ࡣࡰࡩࠬᕚ"): caps.get(bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᕛ"), None),
        bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡡࡹࡩࡷࡹࡩࡰࡰࠪᕜ"): caps.get(bstack1llllll_opy_ (u"ࠩࡥࡶࡴࡽࡳࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᕝ"), None)
    }
  except Exception as error:
    logger.debug(bstack1llllll_opy_ (u"ࠪࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡩ࡯ࠢࡩࡩࡹࡩࡨࡪࡰࡪࠤࡵࡲࡡࡵࡨࡲࡶࡲࠦࡤࡦࡶࡤ࡭ࡱࡹࠠࡸ࡫ࡷ࡬ࠥ࡫ࡲࡳࡱࡵࠤ࠿ࠦࠧᕞ") + str(error))
  return response
def on():
    if os.environ.get(bstack1llllll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕟ"), None) is None or os.environ[bstack1llllll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᕠ")] == bstack1llllll_opy_ (u"ࠨ࡮ࡶ࡮࡯ࠦᕡ"):
        return False
    return True
def bstack11l11ll111_opy_(config):
  return config.get(bstack1llllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᕢ"), False) or any([p.get(bstack1llllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕣ"), False) == True for p in config.get(bstack1llllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡷࠬᕤ"), [])])
def bstack1lllll11l_opy_(config, bstack1ll111ll11_opy_):
  try:
    if not bstack1l1ll1lll_opy_(config):
      return False
    bstack11lllll111l_opy_ = config.get(bstack1llllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᕥ"), False)
    if int(bstack1ll111ll11_opy_) < len(config.get(bstack1llllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡹࠧᕦ"), [])) and config[bstack1llllll_opy_ (u"ࠬࡶ࡬ࡢࡶࡩࡳࡷࡳࡳࠨᕧ")][bstack1ll111ll11_opy_]:
      bstack11llll111ll_opy_ = config[bstack1llllll_opy_ (u"࠭ࡰ࡭ࡣࡷࡪࡴࡸ࡭ࡴࠩᕨ")][bstack1ll111ll11_opy_].get(bstack1llllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᕩ"), None)
    else:
      bstack11llll111ll_opy_ = config.get(bstack1llllll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨᕪ"), None)
    if bstack11llll111ll_opy_ != None:
      bstack11lllll111l_opy_ = bstack11llll111ll_opy_
    bstack11llllll11l_opy_ = os.getenv(bstack1llllll_opy_ (u"ࠩࡅࡗࡤࡇ࠱࠲࡛ࡢࡎ࡜࡚ࠧᕫ")) is not None and len(os.getenv(bstack1llllll_opy_ (u"ࠪࡆࡘࡥࡁ࠲࠳࡜ࡣࡏ࡝ࡔࠨᕬ"))) > 0 and os.getenv(bstack1llllll_opy_ (u"ࠫࡇ࡙࡟ࡂ࠳࠴࡝ࡤࡐࡗࡕࠩᕭ")) != bstack1llllll_opy_ (u"ࠬࡴࡵ࡭࡮ࠪᕮ")
    return bstack11lllll111l_opy_ and bstack11llllll11l_opy_
  except Exception as error:
    logger.debug(bstack1llllll_opy_ (u"࠭ࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢ࡬ࡲࠥࡼࡥࡳ࡫ࡩࡽ࡮ࡴࡧࠡࡶ࡫ࡩࠥࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡹࡥࡴࡵ࡬ࡳࡳࠦࡷࡪࡶ࡫ࠤࡪࡸࡲࡰࡴࠣ࠾ࠥ࠭ᕯ") + str(error))
  return False
def bstack11l1ll11l_opy_(test_tags):
  bstack1ll1ll1l1ll_opy_ = os.getenv(bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨᕰ"))
  if bstack1ll1ll1l1ll_opy_ is None:
    return True
  bstack1ll1ll1l1ll_opy_ = json.loads(bstack1ll1ll1l1ll_opy_)
  try:
    include_tags = bstack1ll1ll1l1ll_opy_[bstack1llllll_opy_ (u"ࠨ࡫ࡱࡧࡱࡻࡤࡦࡖࡤ࡫ࡸࡏ࡮ࡕࡧࡶࡸ࡮ࡴࡧࡔࡥࡲࡴࡪ࠭ᕱ")] if bstack1llllll_opy_ (u"ࠩ࡬ࡲࡨࡲࡵࡥࡧࡗࡥ࡬ࡹࡉ࡯ࡖࡨࡷࡹ࡯࡮ࡨࡕࡦࡳࡵ࡫ࠧᕲ") in bstack1ll1ll1l1ll_opy_ and isinstance(bstack1ll1ll1l1ll_opy_[bstack1llllll_opy_ (u"ࠪ࡭ࡳࡩ࡬ࡶࡦࡨࡘࡦ࡭ࡳࡊࡰࡗࡩࡸࡺࡩ࡯ࡩࡖࡧࡴࡶࡥࠨᕳ")], list) else []
    exclude_tags = bstack1ll1ll1l1ll_opy_[bstack1llllll_opy_ (u"ࠫࡪࡾࡣ࡭ࡷࡧࡩ࡙ࡧࡧࡴࡋࡱࡘࡪࡹࡴࡪࡰࡪࡗࡨࡵࡰࡦࠩᕴ")] if bstack1llllll_opy_ (u"ࠬ࡫ࡸࡤ࡮ࡸࡨࡪ࡚ࡡࡨࡵࡌࡲ࡙࡫ࡳࡵ࡫ࡱ࡫ࡘࡩ࡯ࡱࡧࠪᕵ") in bstack1ll1ll1l1ll_opy_ and isinstance(bstack1ll1ll1l1ll_opy_[bstack1llllll_opy_ (u"࠭ࡥࡹࡥ࡯ࡹࡩ࡫ࡔࡢࡩࡶࡍࡳ࡚ࡥࡴࡶ࡬ࡲ࡬࡙ࡣࡰࡲࡨࠫᕶ")], list) else []
    excluded = any(tag in exclude_tags for tag in test_tags)
    included = len(include_tags) == 0 or any(tag in include_tags for tag in test_tags)
    return not excluded and included
  except Exception as error:
    logger.debug(bstack1llllll_opy_ (u"ࠢࡆࡴࡵࡳࡷࠦࡷࡩ࡫࡯ࡩࠥࡼࡡ࡭࡫ࡧࡥࡹ࡯࡮ࡨࠢࡷࡩࡸࡺࠠࡤࡣࡶࡩࠥ࡬࡯ࡳࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡥࡩ࡫ࡵࡲࡦࠢࡶࡧࡦࡴ࡮ࡪࡰࡪ࠲ࠥࡋࡲࡳࡱࡵࠤ࠿ࠦࠢᕷ") + str(error))
  return False
def bstack11lllll11ll_opy_(config, bstack11llll1111l_opy_, bstack11llll1llll_opy_, bstack11llll111l1_opy_):
  bstack11llll1l111_opy_ = bstack11llll1l11l_opy_(config)
  bstack11lll1ll11l_opy_ = bstack11llll1ll11_opy_(config)
  if bstack11llll1l111_opy_ is None or bstack11lll1ll11l_opy_ is None:
    logger.error(bstack1llllll_opy_ (u"ࠨࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥࡺࡥࡴࡶࠣࡶࡺࡴࠠࡧࡱࡵࠤࡇࡸ࡯ࡸࡵࡨࡶࡘࡺࡡࡤ࡭ࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴ࠺ࠡࡏ࡬ࡷࡸ࡯࡮ࡨࠢࡤࡹࡹ࡮ࡥ࡯ࡶ࡬ࡧࡦࡺࡩࡰࡰࠣࡸࡴࡱࡥ࡯ࠩᕸ"))
    return [None, None]
  try:
    settings = json.loads(os.getenv(bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᕹ"), bstack1llllll_opy_ (u"ࠪࡿࢂ࠭ᕺ")))
    data = {
        bstack1llllll_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩᕻ"): config[bstack1llllll_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪᕼ")],
        bstack1llllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩᕽ"): config.get(bstack1llllll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪᕾ"), os.path.basename(os.getcwd())),
        bstack1llllll_opy_ (u"ࠨࡵࡷࡥࡷࡺࡔࡪ࡯ࡨࠫᕿ"): bstack1l11l1l11l_opy_(),
        bstack1llllll_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧᖀ"): config.get(bstack1llllll_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭ᖁ"), bstack1llllll_opy_ (u"ࠫࠬᖂ")),
        bstack1llllll_opy_ (u"ࠬࡹ࡯ࡶࡴࡦࡩࠬᖃ"): {
            bstack1llllll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭ᖄ"): bstack11llll1111l_opy_,
            bstack1llllll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪᖅ"): bstack11llll1llll_opy_,
            bstack1llllll_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬᖆ"): __version__,
            bstack1llllll_opy_ (u"ࠩ࡯ࡥࡳ࡭ࡵࡢࡩࡨࠫᖇ"): bstack1llllll_opy_ (u"ࠪࡴࡾࡺࡨࡰࡰࠪᖈ"),
            bstack1llllll_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫᖉ"): bstack1llllll_opy_ (u"ࠬࡹࡥ࡭ࡧࡱ࡭ࡺࡳࠧᖊ"),
            bstack1llllll_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᖋ"): bstack11llll111l1_opy_
        },
        bstack1llllll_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩᖌ"): settings,
        bstack1llllll_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡅࡲࡲࡹࡸ࡯࡭ࠩᖍ"): bstack11llll11l1l_opy_(),
        bstack1llllll_opy_ (u"ࠩࡦ࡭ࡎࡴࡦࡰࠩᖎ"): bstack1l1ll111_opy_(),
        bstack1llllll_opy_ (u"ࠪ࡬ࡴࡹࡴࡊࡰࡩࡳࠬᖏ"): get_host_info(),
        bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ᖐ"): bstack1l1ll1lll_opy_(config)
    }
    headers = {
        bstack1llllll_opy_ (u"ࠬࡉ࡯࡯ࡶࡨࡲࡹ࠳ࡔࡺࡲࡨࠫᖑ"): bstack1llllll_opy_ (u"࠭ࡡࡱࡲ࡯࡭ࡨࡧࡴࡪࡱࡱ࠳࡯ࡹ࡯࡯ࠩᖒ"),
    }
    config = {
        bstack1llllll_opy_ (u"ࠧࡢࡷࡷ࡬ࠬᖓ"): (bstack11llll1l111_opy_, bstack11lll1ll11l_opy_),
        bstack1llllll_opy_ (u"ࠨࡪࡨࡥࡩ࡫ࡲࡴࠩᖔ"): headers
    }
    response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"ࠩࡓࡓࡘ࡚ࠧᖕ"), bstack11llll11lll_opy_ + bstack1llllll_opy_ (u"ࠪ࠳ࡻ࠸࠯ࡵࡧࡶࡸࡤࡸࡵ࡯ࡵࠪᖖ"), data, config)
    bstack11lll1lllll_opy_ = response.json()
    if bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"ࠫࡸࡻࡣࡤࡧࡶࡷࠬᖗ")]:
      parsed = json.loads(os.getenv(bstack1llllll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ᖘ"), bstack1llllll_opy_ (u"࠭ࡻࡾࠩᖙ")))
      parsed[bstack1llllll_opy_ (u"ࠧࡴࡥࡤࡲࡳ࡫ࡲࡗࡧࡵࡷ࡮ࡵ࡮ࠨᖚ")] = bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖛ")][bstack1llllll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᖜ")]
      os.environ[bstack1llllll_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫᖝ")] = json.dumps(parsed)
      bstack1l1llll1_opy_.bstack1l11ll1ll_opy_(bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"ࠫࡩࡧࡴࡢࠩᖞ")][bstack1llllll_opy_ (u"ࠬࡹࡣࡳ࡫ࡳࡸࡸ࠭ᖟ")])
      bstack1l1llll1_opy_.bstack11llll1l1ll_opy_(bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"࠭ࡤࡢࡶࡤࠫᖠ")][bstack1llllll_opy_ (u"ࠧࡤࡱࡰࡱࡦࡴࡤࡴࠩᖡ")])
      bstack1l1llll1_opy_.store()
      return bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"ࠨࡦࡤࡸࡦ࠭ᖢ")][bstack1llllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡖࡲ࡯ࡪࡴࠧᖣ")], bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"ࠪࡨࡦࡺࡡࠨᖤ")][bstack1llllll_opy_ (u"ࠫ࡮ࡪࠧᖥ")]
    else:
      logger.error(bstack1llllll_opy_ (u"ࠬࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡳࡷࡱࡲ࡮ࡴࡧࠡࡄࡵࡳࡼࡹࡥࡳࡕࡷࡥࡨࡱࠠࡂࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠠࡂࡷࡷࡳࡲࡧࡴࡪࡱࡱ࠾ࠥ࠭ᖦ") + bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"࠭࡭ࡦࡵࡶࡥ࡬࡫ࠧᖧ")])
      if bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᖨ")] == bstack1llllll_opy_ (u"ࠨࡋࡱࡺࡦࡲࡩࡥࠢࡦࡳࡳ࡬ࡩࡨࡷࡵࡥࡹ࡯࡯࡯ࠢࡳࡥࡸࡹࡥࡥ࠰ࠪᖩ"):
        for bstack11lllll11l1_opy_ in bstack11lll1lllll_opy_[bstack1llllll_opy_ (u"ࠩࡨࡶࡷࡵࡲࡴࠩᖪ")]:
          logger.error(bstack11lllll11l1_opy_[bstack1llllll_opy_ (u"ࠪࡱࡪࡹࡳࡢࡩࡨࠫᖫ")])
      return None, None
  except Exception as error:
    logger.error(bstack1llllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡶࡨࡷࡹࠦࡲࡶࡰࠣࡪࡴࡸࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰ࠽ࠤࠧᖬ") +  str(error))
    return None, None
def bstack11llllll111_opy_():
  if os.getenv(bstack1llllll_opy_ (u"ࠬࡈࡓࡠࡃ࠴࠵࡞ࡥࡊࡘࡖࠪᖭ")) is None:
    return {
        bstack1llllll_opy_ (u"࠭ࡳࡵࡣࡷࡹࡸ࠭ᖮ"): bstack1llllll_opy_ (u"ࠧࡦࡴࡵࡳࡷ࠭ᖯ"),
        bstack1llllll_opy_ (u"ࠨ࡯ࡨࡷࡸࡧࡧࡦࠩᖰ"): bstack1llllll_opy_ (u"ࠩࡅࡹ࡮ࡲࡤࠡࡥࡵࡩࡦࡺࡩࡰࡰࠣ࡬ࡦࡪࠠࡧࡣ࡬ࡰࡪࡪ࠮ࠨᖱ")
    }
  data = {bstack1llllll_opy_ (u"ࠪࡩࡳࡪࡔࡪ࡯ࡨࠫᖲ"): bstack1l11l1l11l_opy_()}
  headers = {
      bstack1llllll_opy_ (u"ࠫࡆࡻࡴࡩࡱࡵ࡭ࡿࡧࡴࡪࡱࡱࠫᖳ"): bstack1llllll_opy_ (u"ࠬࡈࡥࡢࡴࡨࡶࠥ࠭ᖴ") + os.getenv(bstack1llllll_opy_ (u"ࠨࡂࡔࡡࡄ࠵࠶࡟࡟ࡋ࡙ࡗࠦᖵ")),
      bstack1llllll_opy_ (u"ࠧࡄࡱࡱࡸࡪࡴࡴ࠮ࡖࡼࡴࡪ࠭ᖶ"): bstack1llllll_opy_ (u"ࠨࡣࡳࡴࡱ࡯ࡣࡢࡶ࡬ࡳࡳ࠵ࡪࡴࡱࡱࠫᖷ")
  }
  response = bstack1l1ll1111_opy_(bstack1llllll_opy_ (u"ࠩࡓ࡙࡙࠭ᖸ"), bstack11llll11lll_opy_ + bstack1llllll_opy_ (u"ࠪ࠳ࡹ࡫ࡳࡵࡡࡵࡹࡳࡹ࠯ࡴࡶࡲࡴࠬᖹ"), data, { bstack1llllll_opy_ (u"ࠫ࡭࡫ࡡࡥࡧࡵࡷࠬᖺ"): headers })
  try:
    if response.status_code == 200:
      logger.info(bstack1llllll_opy_ (u"ࠧࡈࡲࡰࡹࡶࡩࡷ࡙ࡴࡢࡥ࡮ࠤࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡖࡨࡷࡹࠦࡒࡶࡰࠣࡱࡦࡸ࡫ࡦࡦࠣࡥࡸࠦࡣࡰ࡯ࡳࡰࡪࡺࡥࡥࠢࡤࡸࠥࠨᖻ") + bstack111l1l1l11_opy_().isoformat() + bstack1llllll_opy_ (u"࡚࠭ࠨᖼ"))
      return {bstack1llllll_opy_ (u"ࠧࡴࡶࡤࡸࡺࡹࠧᖽ"): bstack1llllll_opy_ (u"ࠨࡵࡸࡧࡨ࡫ࡳࡴࠩᖾ"), bstack1llllll_opy_ (u"ࠩࡰࡩࡸࡹࡡࡨࡧࠪᖿ"): bstack1llllll_opy_ (u"ࠪࠫᗀ")}
    else:
      response.raise_for_status()
  except requests.RequestException as error:
    logger.error(bstack1llllll_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦ࡭ࡢࡴ࡮࡭ࡳ࡭ࠠࡤࡱࡰࡴࡱ࡫ࡴࡪࡱࡱࠤࡴ࡬ࠠࡃࡴࡲࡻࡸ࡫ࡲࡔࡶࡤࡧࡰࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡘࡪࡹࡴࠡࡔࡸࡲ࠿ࠦࠢᗁ") + str(error))
    return {
        bstack1llllll_opy_ (u"ࠬࡹࡴࡢࡶࡸࡷࠬᗂ"): bstack1llllll_opy_ (u"࠭ࡥࡳࡴࡲࡶࠬᗃ"),
        bstack1llllll_opy_ (u"ࠧ࡮ࡧࡶࡷࡦ࡭ࡥࠨᗄ"): str(error)
    }
def bstack11lll1llll1_opy_(bstack11lllll1l11_opy_):
    return re.match(bstack1llllll_opy_ (u"ࡳࠩࡡࡠࡩ࠱ࠨ࡝࠰࡟ࡨ࠰࠯࠿ࠥࠩᗅ"), bstack11lllll1l11_opy_.strip()) is not None
def bstack1lll1ll11_opy_(caps, options, desired_capabilities={}):
    try:
        if options:
          bstack11lll1lll11_opy_ = options.to_capabilities()
        elif desired_capabilities:
          bstack11lll1lll11_opy_ = desired_capabilities
        else:
          bstack11lll1lll11_opy_ = {}
        bstack11llll11111_opy_ = (bstack11lll1lll11_opy_.get(bstack1llllll_opy_ (u"ࠩࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠨᗆ"), bstack1llllll_opy_ (u"ࠪࠫᗇ")).lower() or caps.get(bstack1llllll_opy_ (u"ࠫࡵࡲࡡࡵࡨࡲࡶࡲࡔࡡ࡮ࡧࠪᗈ"), bstack1llllll_opy_ (u"ࠬ࠭ᗉ")).lower())
        if bstack11llll11111_opy_ == bstack1llllll_opy_ (u"࠭ࡩࡰࡵࠪᗊ"):
            return True
        if bstack11llll11111_opy_ == bstack1llllll_opy_ (u"ࠧࡢࡰࡧࡶࡴ࡯ࡤࠨᗋ"):
            bstack11lll1ll1l1_opy_ = str(float(caps.get(bstack1llllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯࡙ࡩࡷࡹࡩࡰࡰࠪᗌ")) or bstack11lll1lll11_opy_.get(bstack1llllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗍ"), {}).get(bstack1llllll_opy_ (u"ࠪࡳࡸ࡜ࡥࡳࡵ࡬ࡳࡳ࠭ᗎ"),bstack1llllll_opy_ (u"ࠫࠬᗏ"))))
            if bstack11llll11111_opy_ == bstack1llllll_opy_ (u"ࠬࡧ࡮ࡥࡴࡲ࡭ࡩ࠭ᗐ") and int(bstack11lll1ll1l1_opy_.split(bstack1llllll_opy_ (u"࠭࠮ࠨᗑ"))[0]) < float(bstack11lllll1ll1_opy_):
                logger.warning(str(bstack11llll1lll1_opy_))
                return False
            return True
        bstack1ll1l1lllll_opy_ = caps.get(bstack1llllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗒ"), {}).get(bstack1llllll_opy_ (u"ࠨࡦࡨࡺ࡮ࡩࡥࡏࡣࡰࡩࠬᗓ"), caps.get(bstack1llllll_opy_ (u"ࠩࡧࡩࡻ࡯ࡣࡦࠩᗔ"), bstack1llllll_opy_ (u"ࠪࠫᗕ")))
        if bstack1ll1l1lllll_opy_:
            logger.warn(bstack1llllll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦࡲࡶࡰࠣࡳࡳࡲࡹࠡࡱࡱࠤࡉ࡫ࡳ࡬ࡶࡲࡴࠥࡨࡲࡰࡹࡶࡩࡷࡹ࠮ࠣᗖ"))
            return False
        browser = caps.get(bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡔࡡ࡮ࡧࠪᗗ"), bstack1llllll_opy_ (u"࠭ࠧᗘ")).lower() or bstack11lll1lll11_opy_.get(bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡏࡣࡰࡩࠬᗙ"), bstack1llllll_opy_ (u"ࠨࠩᗚ")).lower()
        if browser != bstack1llllll_opy_ (u"ࠩࡦ࡬ࡷࡵ࡭ࡦࠩᗛ"):
            logger.warning(bstack1llllll_opy_ (u"ࠥࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠠࡸ࡫࡯ࡰࠥࡸࡵ࡯ࠢࡲࡲࡱࡿࠠࡰࡰࠣࡇ࡭ࡸ࡯࡮ࡧࠣࡦࡷࡵࡷࡴࡧࡵࡷ࠳ࠨᗜ"))
            return False
        browser_version = caps.get(bstack1llllll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗝ")) or caps.get(bstack1llllll_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡥࡶࡦࡴࡶ࡭ࡴࡴࠧᗞ")) or bstack11lll1lll11_opy_.get(bstack1llllll_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗟ")) or bstack11lll1lll11_opy_.get(bstack1llllll_opy_ (u"ࠧࡣࡵࡷࡥࡨࡱ࠺ࡰࡲࡷ࡭ࡴࡴࡳࠨᗠ"), {}).get(bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡘࡨࡶࡸ࡯࡯࡯ࠩᗡ")) or bstack11lll1lll11_opy_.get(bstack1llllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗢ"), {}).get(bstack1llllll_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬᗣ"))
        if browser_version and browser_version != bstack1llllll_opy_ (u"ࠫࡱࡧࡴࡦࡵࡷࠫᗤ") and int(browser_version.split(bstack1llllll_opy_ (u"ࠬ࠴ࠧᗥ"))[0]) <= 98:
            logger.warning(bstack1llllll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡻ࡮ࡲ࡬ࠡࡴࡸࡲࠥࡵ࡮࡭ࡻࠣࡳࡳࠦࡃࡩࡴࡲࡱࡪࠦࡢࡳࡱࡺࡷࡪࡸࠠࡷࡧࡵࡷ࡮ࡵ࡮ࠡࡩࡵࡩࡦࡺࡥࡳࠢࡷ࡬ࡦࡴࠠ࠺࠺࠱ࠦᗦ"))
            return False
        if not options:
            bstack1ll1l1l1ll1_opy_ = caps.get(bstack1llllll_opy_ (u"ࠧࡨࡱࡲ࡫࠿ࡩࡨࡳࡱࡰࡩࡔࡶࡴࡪࡱࡱࡷࠬᗧ")) or bstack11lll1lll11_opy_.get(bstack1llllll_opy_ (u"ࠨࡩࡲࡳ࡬ࡀࡣࡩࡴࡲࡱࡪࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗨ"), {})
            if bstack1llllll_opy_ (u"ࠩ࠰࠱࡭࡫ࡡࡥ࡮ࡨࡷࡸ࠭ᗩ") in bstack1ll1l1l1ll1_opy_.get(bstack1llllll_opy_ (u"ࠪࡥࡷ࡭ࡳࠨᗪ"), []):
                logger.warn(bstack1llllll_opy_ (u"ࠦࡆࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠤࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠡࡹ࡬ࡰࡱࠦ࡮ࡰࡶࠣࡶࡺࡴࠠࡰࡰࠣࡰࡪ࡭ࡡࡤࡻࠣ࡬ࡪࡧࡤ࡭ࡧࡶࡷࠥࡳ࡯ࡥࡧ࠱ࠤࡘࡽࡩࡵࡥ࡫ࠤࡹࡵࠠ࡯ࡧࡺࠤ࡭࡫ࡡࡥ࡮ࡨࡷࡸࠦ࡭ࡰࡦࡨࠤࡴࡸࠠࡢࡸࡲ࡭ࡩࠦࡵࡴ࡫ࡱ࡫ࠥ࡮ࡥࡢࡦ࡯ࡩࡸࡹࠠ࡮ࡱࡧࡩ࠳ࠨᗫ"))
                return False
        return True
    except Exception as error:
        logger.debug(bstack1llllll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡ࡫ࡱࠤࡻࡧ࡬ࡪࡦࡤࡸࡪࠦࡡ࠲࠳ࡼࠤࡸࡻࡰࡱࡱࡵࡸࠥࡀࠢᗬ") + str(error))
        return False
def set_capabilities(caps, config):
  try:
    bstack1llllll1l11_opy_ = config.get(bstack1llllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗭ"), {})
    bstack1llllll1l11_opy_[bstack1llllll_opy_ (u"ࠧࡢࡷࡷ࡬࡙ࡵ࡫ࡦࡰࠪᗮ")] = os.getenv(bstack1llllll_opy_ (u"ࠨࡄࡖࡣࡆ࠷࠱࡚ࡡࡍ࡛࡙࠭ᗯ"))
    bstack11llll11ll1_opy_ = json.loads(os.getenv(bstack1llllll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡖࡈࡗ࡙ࡥࡁࡄࡅࡈࡗࡘࡏࡂࡊࡎࡌࡘ࡞ࡥࡃࡐࡐࡉࡍࡌ࡛ࡒࡂࡖࡌࡓࡓࡥ࡙ࡎࡎࠪᗰ"), bstack1llllll_opy_ (u"ࠪࡿࢂ࠭ᗱ"))).get(bstack1llllll_opy_ (u"ࠫࡸࡩࡡ࡯ࡰࡨࡶ࡛࡫ࡲࡴ࡫ࡲࡲࠬᗲ"))
    caps[bstack1llllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬᗳ")] = True
    if not config[bstack1llllll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡕࡸ࡯ࡥࡷࡦࡸࡒࡧࡰࠨᗴ")].get(bstack1llllll_opy_ (u"ࠢࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪࠨᗵ")):
      if bstack1llllll_opy_ (u"ࠨࡤࡶࡸࡦࡩ࡫࠻ࡱࡳࡸ࡮ࡵ࡮ࡴࠩᗶ") in caps:
        caps[bstack1llllll_opy_ (u"ࠩࡥࡷࡹࡧࡣ࡬࠼ࡲࡴࡹ࡯࡯࡯ࡵࠪᗷ")][bstack1llllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡒࡴࡹ࡯࡯࡯ࡵࠪᗸ")] = bstack1llllll1l11_opy_
        caps[bstack1llllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮࠾ࡴࡶࡴࡪࡱࡱࡷࠬᗹ")][bstack1llllll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡔࡶࡴࡪࡱࡱࡷࠬᗺ")][bstack1llllll_opy_ (u"࠭ࡳࡤࡣࡱࡲࡪࡸࡖࡦࡴࡶ࡭ࡴࡴࠧᗻ")] = bstack11llll11ll1_opy_
      else:
        caps[bstack1llllll_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰ࠴ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࡕࡰࡵ࡫ࡲࡲࡸ࠭ᗼ")] = bstack1llllll1l11_opy_
        caps[bstack1llllll_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱ࠮ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࡏࡱࡶ࡬ࡳࡳࡹࠧᗽ")][bstack1llllll_opy_ (u"ࠩࡶࡧࡦࡴ࡮ࡦࡴ࡙ࡩࡷࡹࡩࡰࡰࠪᗾ")] = bstack11llll11ll1_opy_
  except Exception as error:
    logger.debug(bstack1llllll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡹࡥࡵࡶ࡬ࡲ࡬ࠦࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠣࡧࡦࡶࡡࡣ࡫࡯࡭ࡹ࡯ࡥࡴ࠰ࠣࡉࡷࡸ࡯ࡳ࠼ࠣࠦᗿ") +  str(error))
def bstack1l1ll1lll1_opy_(driver, bstack11llll1ll1l_opy_):
  try:
    setattr(driver, bstack1llllll_opy_ (u"ࠫࡧࡹࡴࡢࡥ࡮ࡅ࠶࠷ࡹࡔࡪࡲࡹࡱࡪࡓࡤࡣࡱࠫᘀ"), True)
    session = driver.session_id
    if session:
      bstack11lll1lll1l_opy_ = True
      current_url = driver.current_url
      try:
        url = urlparse(current_url)
      except Exception as e:
        bstack11lll1lll1l_opy_ = False
      bstack11lll1lll1l_opy_ = url.scheme in [bstack1llllll_opy_ (u"ࠧ࡮ࡴࡵࡲࠥᘁ"), bstack1llllll_opy_ (u"ࠨࡨࡵࡶࡳࡷࠧᘂ")]
      if bstack11lll1lll1l_opy_:
        if bstack11llll1ll1l_opy_:
          logger.info(bstack1llllll_opy_ (u"ࠢࡔࡧࡷࡹࡵࠦࡦࡰࡴࠣࡅࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠣࡸࡪࡹࡴࡪࡰࡪࠤ࡭ࡧࡳࠡࡵࡷࡥࡷࡺࡥࡥ࠰ࠣࡅࡺࡺ࡯࡮ࡣࡷࡩࠥࡺࡥࡴࡶࠣࡧࡦࡹࡥࠡࡧࡻࡩࡨࡻࡴࡪࡱࡱࠤࡼ࡯࡬࡭ࠢࡥࡩ࡬࡯࡮ࠡ࡯ࡲࡱࡪࡴࡴࡢࡴ࡬ࡰࡾ࠴ࠢᘃ"))
      return bstack11llll1ll1l_opy_
  except Exception as e:
    logger.error(bstack1llllll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤ࡮ࡴࠠࡴࡶࡤࡶࡹ࡯࡮ࡨࠢࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠢࡤࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳࠦࡳࡤࡣࡱࠤ࡫ࡵࡲࠡࡶ࡫࡭ࡸࠦࡴࡦࡵࡷࠤࡨࡧࡳࡦ࠼ࠣࠦᘄ") + str(e))
    return False
def bstack1l1l1ll111_opy_(driver, name, path):
  try:
    bstack1ll1l1l11ll_opy_ = {
        bstack1llllll_opy_ (u"ࠩࡷ࡬࡙࡫ࡳࡵࡔࡸࡲ࡚ࡻࡩࡥࠩᘅ"): threading.current_thread().current_test_uuid,
        bstack1llllll_opy_ (u"ࠪࡸ࡭ࡈࡵࡪ࡮ࡧ࡙ࡺ࡯ࡤࠨᘆ"): os.environ.get(bstack1llllll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡉࡗࡅࡣ࡚࡛ࡉࡅࠩᘇ"), bstack1llllll_opy_ (u"ࠬ࠭ᘈ")),
        bstack1llllll_opy_ (u"࠭ࡴࡩࡌࡺࡸ࡙ࡵ࡫ࡦࡰࠪᘉ"): os.environ.get(bstack1llllll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡌ࡚ࡈ࡟ࡋ࡙ࡗࠫᘊ"), bstack1llllll_opy_ (u"ࠨࠩᘋ"))
    }
    bstack1ll1ll111l1_opy_ = bstack1llll1l1_opy_.bstack1ll1ll1l11l_opy_(EVENTS.bstack11lll11l11_opy_.value)
    logger.debug(bstack1llllll_opy_ (u"ࠩࡓࡩࡷ࡬࡯ࡳ࡯࡬ࡲ࡬ࠦࡳࡤࡣࡱࠤࡧ࡫ࡦࡰࡴࡨࠤࡸࡧࡶࡪࡰࡪࠤࡷ࡫ࡳࡶ࡮ࡷࡷࠬᘌ"))
    try:
      if (bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠪ࡭ࡸࡇࡰࡱࡃ࠴࠵ࡾ࡚ࡥࡴࡶࠪᘍ"), None) and bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠫࡦࡶࡰࡂ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ᘎ"), None)):
        scripts = {bstack1llllll_opy_ (u"ࠬࡹࡣࡢࡰࠪᘏ"): bstack1l1llll1_opy_.perform_scan}
        bstack11lllll1l1l_opy_ = json.loads(scripts[bstack1llllll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘐ")].replace(bstack1llllll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘑ"), bstack1llllll_opy_ (u"ࠣࠤᘒ")))
        bstack11lllll1l1l_opy_[bstack1llllll_opy_ (u"ࠩࡤࡶ࡬ࡻ࡭ࡦࡰࡷࡷࠬᘓ")][bstack1llllll_opy_ (u"ࠪࡱࡪࡺࡨࡰࡦࠪᘔ")] = None
        scripts[bstack1llllll_opy_ (u"ࠦࡸࡩࡡ࡯ࠤᘕ")] = bstack1llllll_opy_ (u"ࠧࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡣࡪࡾࡥࡤࡷࡷࡳࡷࡀࠠࠣᘖ") + json.dumps(bstack11lllll1l1l_opy_)
        bstack1l1llll1_opy_.bstack1l11ll1ll_opy_(scripts)
        bstack1l1llll1_opy_.store()
        logger.debug(driver.execute_script(bstack1l1llll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1llll1_opy_.perform_scan, {bstack1llllll_opy_ (u"ࠨ࡭ࡦࡶ࡫ࡳࡩࠨᘗ"): name}))
      bstack1llll1l1_opy_.end(EVENTS.bstack11lll11l11_opy_.value, bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠢ࠻ࡵࡷࡥࡷࡺࠢᘘ"), bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠣ࠼ࡨࡲࡩࠨᘙ"), True, None)
    except Exception as error:
      bstack1llll1l1_opy_.end(EVENTS.bstack11lll11l11_opy_.value, bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠤ࠽ࡷࡹࡧࡲࡵࠤᘚ"), bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠥ࠾ࡪࡴࡤࠣᘛ"), False, str(error))
    bstack1ll1ll111l1_opy_ = bstack1llll1l1_opy_.bstack11lllll1lll_opy_(EVENTS.bstack1ll1l1111ll_opy_.value)
    bstack1llll1l1_opy_.mark(bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠦ࠿ࡹࡴࡢࡴࡷࠦᘜ"))
    try:
      if (bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"ࠬ࡯ࡳࡂࡲࡳࡅ࠶࠷ࡹࡕࡧࡶࡸࠬᘝ"), None) and bstack1lll11l1_opy_(threading.current_thread(), bstack1llllll_opy_ (u"࠭ࡡࡱࡲࡄ࠵࠶ࡿࡐ࡭ࡣࡷࡪࡴࡸ࡭ࠨᘞ"), None)):
        scripts = {bstack1llllll_opy_ (u"ࠧࡴࡥࡤࡲࠬᘟ"): bstack1l1llll1_opy_.perform_scan}
        bstack11lllll1l1l_opy_ = json.loads(scripts[bstack1llllll_opy_ (u"ࠣࡵࡦࡥࡳࠨᘠ")].replace(bstack1llllll_opy_ (u"ࠤࡥࡶࡴࡽࡳࡦࡴࡶࡸࡦࡩ࡫ࡠࡧࡻࡩࡨࡻࡴࡰࡴ࠽ࠤࠧᘡ"), bstack1llllll_opy_ (u"ࠥࠦᘢ")))
        bstack11lllll1l1l_opy_[bstack1llllll_opy_ (u"ࠫࡦࡸࡧࡶ࡯ࡨࡲࡹࡹࠧᘣ")][bstack1llllll_opy_ (u"ࠬࡳࡥࡵࡪࡲࡨࠬᘤ")] = None
        scripts[bstack1llllll_opy_ (u"ࠨࡳࡤࡣࡱࠦᘥ")] = bstack1llllll_opy_ (u"ࠢࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡥࡥࡹࡧࡦࡹࡹࡵࡲ࠻ࠢࠥᘦ") + json.dumps(bstack11lllll1l1l_opy_)
        bstack1l1llll1_opy_.bstack1l11ll1ll_opy_(scripts)
        bstack1l1llll1_opy_.store()
        logger.debug(driver.execute_script(bstack1l1llll1_opy_.perform_scan))
      else:
        logger.debug(driver.execute_async_script(bstack1l1llll1_opy_.bstack11llll1l1l1_opy_, bstack1ll1l1l11ll_opy_))
      bstack1llll1l1_opy_.end(bstack1ll1ll111l1_opy_, bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠣ࠼ࡶࡸࡦࡸࡴࠣᘧ"), bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠤ࠽ࡩࡳࡪࠢᘨ"),True, None)
    except Exception as error:
      bstack1llll1l1_opy_.end(bstack1ll1ll111l1_opy_, bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠥ࠾ࡸࡺࡡࡳࡶࠥᘩ"), bstack1ll1ll111l1_opy_ + bstack1llllll_opy_ (u"ࠦ࠿࡫࡮ࡥࠤᘪ"),False, str(error))
    logger.info(bstack1llllll_opy_ (u"ࠧࡇࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠥࡺࡥࡴࡶ࡬ࡲ࡬ࠦࡦࡰࡴࠣࡸ࡭࡯ࡳࠡࡶࡨࡷࡹࠦࡣࡢࡵࡨࠤ࡭ࡧࡳࠡࡧࡱࡨࡪࡪ࠮ࠣᘫ"))
  except Exception as bstack1ll1l11llll_opy_:
    logger.error(bstack1llllll_opy_ (u"ࠨࡁࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾࠦࡲࡦࡵࡸࡰࡹࡹࠠࡤࡱࡸࡰࡩࠦ࡮ࡰࡶࠣࡦࡪࠦࡰࡳࡱࡦࡩࡸࡹࡥࡥࠢࡩࡳࡷࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡥࡤࡷࡪࡀࠠࠣᘬ") + str(path) + bstack1llllll_opy_ (u"ࠢࠡࡇࡵࡶࡴࡸࠠ࠻ࠤᘭ") + str(bstack1ll1l11llll_opy_))
def bstack11lll1ll1ll_opy_(driver):
    caps = driver.capabilities
    if caps.get(bstack1llllll_opy_ (u"ࠣࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡑࡥࡲ࡫ࠢᘮ")) and str(caps.get(bstack1llllll_opy_ (u"ࠤࡳࡰࡦࡺࡦࡰࡴࡰࡒࡦࡳࡥࠣᘯ"))).lower() == bstack1llllll_opy_ (u"ࠥࡥࡳࡪࡲࡰ࡫ࡧࠦᘰ"):
        bstack11lll1ll1l1_opy_ = caps.get(bstack1llllll_opy_ (u"ࠦࡦࡶࡰࡪࡷࡰ࠾ࡵࡲࡡࡵࡨࡲࡶࡲ࡜ࡥࡳࡵ࡬ࡳࡳࠨᘱ")) or caps.get(bstack1llllll_opy_ (u"ࠧࡶ࡬ࡢࡶࡩࡳࡷࡳࡖࡦࡴࡶ࡭ࡴࡴࠢᘲ"))
        if bstack11lll1ll1l1_opy_ and int(str(bstack11lll1ll1l1_opy_)) < bstack11lllll1ll1_opy_:
            return False
    return True
def bstack1l1l1lll11_opy_(config):
  if bstack1llllll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ᘳ") in config:
        return config[bstack1llllll_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧᘴ")]
  for platform in config.get(bstack1llllll_opy_ (u"ࠨࡲ࡯ࡥࡹ࡬࡯ࡳ࡯ࡶࠫᘵ"), []):
      if bstack1llllll_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩᘶ") in platform:
          return platform[bstack1llllll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪᘷ")]
  return None