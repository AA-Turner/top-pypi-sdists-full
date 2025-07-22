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
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1ll11l1_opy_, bstack1ll1l11111_opy_, get_host_info, bstack111llll1lll_opy_, \
 bstack1lllll1lll_opy_, bstack1ll11lllll_opy_, bstack111l1l1l1l_opy_, bstack11l111l1111_opy_, bstack1ll1ll1l1_opy_
import bstack_utils.accessibility as bstack1l1ll11l1l_opy_
from bstack_utils.bstack111llll1l1_opy_ import bstack11llll1l11_opy_
from bstack_utils.percy import bstack1111l11l1_opy_
from bstack_utils.config import Config
bstack1ll1ll11_opy_ = Config.bstack1ll11ll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1111l11l1_opy_()
@bstack111l1l1l1l_opy_(class_method=False)
def bstack1llllll11111_opy_(bs_config, bstack11l1l1l11l_opy_):
  try:
    data = {
        bstack111l111_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬℍ"): bstack111l111_opy_ (u"࠭ࡪࡴࡱࡱࠫℎ"),
        bstack111l111_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭ℏ"): bs_config.get(bstack111l111_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭ℐ"), bstack111l111_opy_ (u"ࠩࠪℑ")),
        bstack111l111_opy_ (u"ࠪࡲࡦࡳࡥࠨℒ"): bs_config.get(bstack111l111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧℓ"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111l111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ℔"): bs_config.get(bstack111l111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨℕ")),
        bstack111l111_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ№"): bs_config.get(bstack111l111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ℗"), bstack111l111_opy_ (u"ࠩࠪ℘")),
        bstack111l111_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺࠧℙ"): bstack1ll1ll1l1_opy_(),
        bstack111l111_opy_ (u"ࠫࡹࡧࡧࡴࠩℚ"): bstack111llll1lll_opy_(bs_config),
        bstack111l111_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨℛ"): get_host_info(),
        bstack111l111_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧℜ"): bstack1ll1l11111_opy_(),
        bstack111l111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧℝ"): os.environ.get(bstack111l111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘࠧ℞")),
        bstack111l111_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴࠧ℟"): os.environ.get(bstack111l111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ℠"), False),
        bstack111l111_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭℡"): bstack11ll1ll11l1_opy_(),
        bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ™"): bstack1lllll1111ll_opy_(bs_config),
        bstack111l111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ℣"): bstack1llll1llll1l_opy_(bstack11l1l1l11l_opy_),
        bstack111l111_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬℤ"): bstack1llll1lllll1_opy_(bs_config, bstack11l1l1l11l_opy_.get(bstack111l111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ℥"), bstack111l111_opy_ (u"ࠩࠪΩ"))),
        bstack111l111_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ℧"): bstack1lllll1lll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack111l111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧℨ").format(str(error)))
    return None
def bstack1llll1llll1l_opy_(framework):
  return {
    bstack111l111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ℩"): framework.get(bstack111l111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧK"), bstack111l111_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺࠧÅ")),
    bstack111l111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱࠫℬ"): framework.get(bstack111l111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭ℭ")),
    bstack111l111_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ℮"): framework.get(bstack111l111_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩℯ")),
    bstack111l111_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫ࠧℰ"): bstack111l111_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ࠭ℱ"),
    bstack111l111_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧℲ"): framework.get(bstack111l111_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨℳ"))
  }
def bstack11l111ll_opy_(bs_config, framework):
  bstack1l1l1ll11_opy_ = False
  bstack111ll111l_opy_ = False
  bstack1lllll111l1l_opy_ = False
  if bstack111l111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭ℴ") in bs_config:
    bstack1lllll111l1l_opy_ = True
  elif bstack111l111_opy_ (u"ࠪࡥࡵࡶࠧℵ") in bs_config:
    bstack1l1l1ll11_opy_ = True
  else:
    bstack111ll111l_opy_ = True
  bstack1ll11llll1_opy_ = {
    bstack111l111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫℶ"): bstack11llll1l11_opy_.bstack1lllll111ll1_opy_(bs_config, framework),
    bstack111l111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬℷ"): bstack1l1ll11l1l_opy_.bstack1ll1l1l1l_opy_(bs_config),
    bstack111l111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬℸ"): bs_config.get(bstack111l111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ℹ"), False),
    bstack111l111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ℺"): bstack111ll111l_opy_,
    bstack111l111_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ℻"): bstack1l1l1ll11_opy_,
    bstack111l111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧℼ"): bstack1lllll111l1l_opy_
  }
  return bstack1ll11llll1_opy_
@bstack111l1l1l1l_opy_(class_method=False)
def bstack1lllll1111ll_opy_(bs_config):
  try:
    bstack1lllll11111l_opy_ = json.loads(os.getenv(bstack111l111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬℽ"), bstack111l111_opy_ (u"ࠬࢁࡽࠨℾ")))
    bstack1lllll11111l_opy_ = bstack1lllll111lll_opy_(bs_config, bstack1lllll11111l_opy_)
    return {
        bstack111l111_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨℿ"): bstack1lllll11111l_opy_
    }
  except Exception as error:
    logger.error(bstack111l111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⅀").format(str(error)))
    return {}
def bstack1lllll111lll_opy_(bs_config, bstack1lllll11111l_opy_):
  if ((bstack111l111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⅁") in bs_config or not bstack1lllll1lll_opy_(bs_config)) and bstack1l1ll11l1l_opy_.bstack1ll1l1l1l_opy_(bs_config)):
    bstack1lllll11111l_opy_[bstack111l111_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧ⅂")] = True
  return bstack1lllll11111l_opy_
def bstack1lllll11ll1l_opy_(array, bstack1llll1llllll_opy_, bstack1llll1lll1ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1llll1llllll_opy_]
    result[key] = o[bstack1llll1lll1ll_opy_]
  return result
def bstack1lllll1l1l1l_opy_(bstack1l1l11l1ll_opy_=bstack111l111_opy_ (u"ࠪࠫ⅃")):
  bstack1llll1llll11_opy_ = bstack1l1ll11l1l_opy_.on()
  bstack1lllll111l11_opy_ = bstack11llll1l11_opy_.on()
  bstack1lllll111111_opy_ = percy.bstack1l11ll111_opy_()
  if bstack1lllll111111_opy_ and not bstack1lllll111l11_opy_ and not bstack1llll1llll11_opy_:
    return bstack1l1l11l1ll_opy_ not in [bstack111l111_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ⅄"), bstack111l111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩⅅ")]
  elif bstack1llll1llll11_opy_ and not bstack1lllll111l11_opy_:
    return bstack1l1l11l1ll_opy_ not in [bstack111l111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧⅆ"), bstack111l111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩⅇ"), bstack111l111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬⅈ")]
  return bstack1llll1llll11_opy_ or bstack1lllll111l11_opy_ or bstack1lllll111111_opy_
@bstack111l1l1l1l_opy_(class_method=False)
def bstack1lllll1l1l11_opy_(bstack1l1l11l1ll_opy_, test=None):
  bstack1lllll1111l1_opy_ = bstack1l1ll11l1l_opy_.on()
  if not bstack1lllll1111l1_opy_ or bstack1l1l11l1ll_opy_ not in [bstack111l111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫⅉ")] or test == None:
    return None
  return {
    bstack111l111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⅊"): bstack1lllll1111l1_opy_ and bstack1ll11lllll_opy_(threading.current_thread(), bstack111l111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⅋"), None) == True and bstack1l1ll11l1l_opy_.bstack11ll111lll_opy_(test[bstack111l111_opy_ (u"ࠬࡺࡡࡨࡵࠪ⅌")])
  }
def bstack1llll1lllll1_opy_(bs_config, framework):
  bstack1l1l1ll11_opy_ = False
  bstack111ll111l_opy_ = False
  bstack1lllll111l1l_opy_ = False
  if bstack111l111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⅍") in bs_config:
    bstack1lllll111l1l_opy_ = True
  elif bstack111l111_opy_ (u"ࠧࡢࡲࡳࠫⅎ") in bs_config:
    bstack1l1l1ll11_opy_ = True
  else:
    bstack111ll111l_opy_ = True
  bstack1ll11llll1_opy_ = {
    bstack111l111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⅏"): bstack11llll1l11_opy_.bstack1lllll111ll1_opy_(bs_config, framework),
    bstack111l111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⅐"): bstack1l1ll11l1l_opy_.bstack11l1l1ll_opy_(bs_config),
    bstack111l111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⅑"): bs_config.get(bstack111l111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⅒"), False),
    bstack111l111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⅓"): bstack111ll111l_opy_,
    bstack111l111_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⅔"): bstack1l1l1ll11_opy_,
    bstack111l111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⅕"): bstack1lllll111l1l_opy_
  }
  return bstack1ll11llll1_opy_