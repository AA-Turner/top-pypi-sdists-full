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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l11lll1l1_opy_, bstack1l1l1l1ll1_opy_, get_host_info, bstack111l111l1ll_opy_, \
 bstack1l11lll1l_opy_, bstack11ll1lll_opy_, bstack111l11l1l1_opy_, bstack1111llll11l_opy_, bstack1lllllllll_opy_
import bstack_utils.accessibility as bstack11llll1l11_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l1ll111ll_opy_
from bstack_utils.percy import bstack11ll11l111_opy_
from bstack_utils.config import Config
bstack1l1l11l1ll_opy_ = Config.bstack11l1l11l11_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll11l111_opy_()
@bstack111l11l1l1_opy_(class_method=False)
def bstack1lllll1ll1l1_opy_(bs_config, bstack1ll111ll1_opy_):
  try:
    data = {
        bstack11l1111_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ℉"): bstack11l1111_opy_ (u"ࠩ࡭ࡷࡴࡴࠧℊ"),
        bstack11l1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩℋ"): bs_config.get(bstack11l1111_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩℌ"), bstack11l1111_opy_ (u"ࠬ࠭ℍ")),
        bstack11l1111_opy_ (u"࠭࡮ࡢ࡯ࡨࠫℎ"): bs_config.get(bstack11l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪℏ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫℐ"): bs_config.get(bstack11l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫℑ")),
        bstack11l1111_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨℒ"): bs_config.get(bstack11l1111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧℓ"), bstack11l1111_opy_ (u"ࠬ࠭℔")),
        bstack11l1111_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪℕ"): bstack1lllllllll_opy_(),
        bstack11l1111_opy_ (u"ࠧࡵࡣࡪࡷࠬ№"): bstack111l111l1ll_opy_(bs_config),
        bstack11l1111_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ℗"): get_host_info(),
        bstack11l1111_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ℘"): bstack1l1l1l1ll1_opy_(),
        bstack11l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪℙ"): os.environ.get(bstack11l1111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪℚ")),
        bstack11l1111_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪℛ"): os.environ.get(bstack11l1111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫℜ"), False),
        bstack11l1111_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩℝ"): bstack11l11lll1l1_opy_(),
        bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ℞"): bstack1lllll1111ll_opy_(bs_config),
        bstack11l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭℟"): bstack1llll1lllll1_opy_(bstack1ll111ll1_opy_),
        bstack11l1111_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ℠"): bstack1llll1llllll_opy_(bs_config, bstack1ll111ll1_opy_.get(bstack11l1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ℡"), bstack11l1111_opy_ (u"ࠬ࠭™"))),
        bstack11l1111_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ℣"): bstack1l11lll1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣℤ").format(str(error)))
    return None
def bstack1llll1lllll1_opy_(framework):
  return {
    bstack11l1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ℥"): framework.get(bstack11l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪΩ"), bstack11l1111_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ℧")),
    bstack11l1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧℨ"): framework.get(bstack11l1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ℩")),
    bstack11l1111_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪK"): framework.get(bstack11l1111_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬÅ")),
    bstack11l1111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪℬ"): bstack11l1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩℭ"),
    bstack11l1111_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ℮"): framework.get(bstack11l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫℯ"))
  }
def bstack1111l111_opy_(bs_config, framework):
  bstack11lll11l1l_opy_ = False
  bstack1l1l1lll_opy_ = False
  bstack1lllll111lll_opy_ = False
  if bstack11l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩℰ") in bs_config:
    bstack1lllll111lll_opy_ = True
  elif bstack11l1111_opy_ (u"࠭ࡡࡱࡲࠪℱ") in bs_config:
    bstack11lll11l1l_opy_ = True
  else:
    bstack1l1l1lll_opy_ = True
  bstack1l1l111lll_opy_ = {
    bstack11l1111_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧℲ"): bstack1l1ll111ll_opy_.bstack1lllll111111_opy_(bs_config, framework),
    bstack11l1111_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨℳ"): bstack11llll1l11_opy_.bstack11l1111lll_opy_(bs_config),
    bstack11l1111_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨℴ"): bs_config.get(bstack11l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩℵ"), False),
    bstack11l1111_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭ℶ"): bstack1l1l1lll_opy_,
    bstack11l1111_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫℷ"): bstack11lll11l1l_opy_,
    bstack11l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪℸ"): bstack1lllll111lll_opy_
  }
  return bstack1l1l111lll_opy_
@bstack111l11l1l1_opy_(class_method=False)
def bstack1lllll1111ll_opy_(bs_config):
  try:
    bstack1llll1llll1l_opy_ = json.loads(os.getenv(bstack11l1111_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨℹ"), bstack11l1111_opy_ (u"ࠨࡽࢀࠫ℺")))
    bstack1llll1llll1l_opy_ = bstack1lllll111l1l_opy_(bs_config, bstack1llll1llll1l_opy_)
    return {
        bstack11l1111_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ℻"): bstack1llll1llll1l_opy_
    }
  except Exception as error:
    logger.error(bstack11l1111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤℼ").format(str(error)))
    return {}
def bstack1lllll111l1l_opy_(bs_config, bstack1llll1llll1l_opy_):
  if ((bstack11l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨℽ") in bs_config or not bstack1l11lll1l_opy_(bs_config)) and bstack11llll1l11_opy_.bstack11l1111lll_opy_(bs_config)):
    bstack1llll1llll1l_opy_[bstack11l1111_opy_ (u"ࠧ࡯࡮ࡤ࡮ࡸࡨࡪࡋ࡮ࡤࡱࡧࡩࡩࡋࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠣℾ")] = True
  return bstack1llll1llll1l_opy_
def bstack1lllll1l11l1_opy_(array, bstack1lllll111ll1_opy_, bstack1lllll11111l_opy_):
  result = {}
  for o in array:
    key = o[bstack1lllll111ll1_opy_]
    result[key] = o[bstack1lllll11111l_opy_]
  return result
def bstack1lllll11l1ll_opy_(bstack1l1l1l11l_opy_=bstack11l1111_opy_ (u"࠭ࠧℿ")):
  bstack1lllll11l11l_opy_ = bstack11llll1l11_opy_.on()
  bstack1lllll1111l1_opy_ = bstack1l1ll111ll_opy_.on()
  bstack1lllll11l111_opy_ = percy.bstack111ll1l1l_opy_()
  if bstack1lllll11l111_opy_ and not bstack1lllll1111l1_opy_ and not bstack1lllll11l11l_opy_:
    return bstack1l1l1l11l_opy_ not in [bstack11l1111_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⅀"), bstack11l1111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⅁")]
  elif bstack1lllll11l11l_opy_ and not bstack1lllll1111l1_opy_:
    return bstack1l1l1l11l_opy_ not in [bstack11l1111_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⅂"), bstack11l1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⅃"), bstack11l1111_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⅄")]
  return bstack1lllll11l11l_opy_ or bstack1lllll1111l1_opy_ or bstack1lllll11l111_opy_
@bstack111l11l1l1_opy_(class_method=False)
def bstack1llllll111ll_opy_(bstack1l1l1l11l_opy_, test=None):
  bstack1lllll111l11_opy_ = bstack11llll1l11_opy_.on()
  if not bstack1lllll111l11_opy_ or bstack1l1l1l11l_opy_ not in [bstack11l1111_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧⅅ")] or test == None:
    return None
  return {
    bstack11l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ⅆ"): bstack1lllll111l11_opy_ and bstack11ll1lll_opy_(threading.current_thread(), bstack11l1111_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭ⅇ"), None) == True and bstack11llll1l11_opy_.bstack1lll111l1l_opy_(test[bstack11l1111_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭ⅈ")])
  }
def bstack1llll1llllll_opy_(bs_config, framework):
  bstack11lll11l1l_opy_ = False
  bstack1l1l1lll_opy_ = False
  bstack1lllll111lll_opy_ = False
  if bstack11l1111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ⅉ") in bs_config:
    bstack1lllll111lll_opy_ = True
  elif bstack11l1111_opy_ (u"ࠪࡥࡵࡶࠧ⅊") in bs_config:
    bstack11lll11l1l_opy_ = True
  else:
    bstack1l1l1lll_opy_ = True
  bstack1l1l111lll_opy_ = {
    bstack11l1111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⅋"): bstack1l1ll111ll_opy_.bstack1lllll111111_opy_(bs_config, framework),
    bstack11l1111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⅌"): bstack11llll1l11_opy_.bstack1l1ll11111_opy_(bs_config),
    bstack11l1111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⅍"): bs_config.get(bstack11l1111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ⅎ"), False),
    bstack11l1111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⅏"): bstack1l1l1lll_opy_,
    bstack11l1111_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⅐"): bstack11lll11l1l_opy_,
    bstack11l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⅑"): bstack1lllll111lll_opy_
  }
  return bstack1l1l111lll_opy_