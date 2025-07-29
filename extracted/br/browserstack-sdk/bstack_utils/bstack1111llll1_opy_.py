# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1l11lll_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstackl_opy_ (bstack1111111_opy_):
    global bstack1lllll1_opy_
    bstack111l111_opy_ = ord (bstack1111111_opy_ [-1])
    bstack1l11l11_opy_ = bstack1111111_opy_ [:-1]
    bstack1lll1l1_opy_ = bstack111l111_opy_ % len (bstack1l11l11_opy_)
    bstack1llll1_opy_ = bstack1l11l11_opy_ [:bstack1lll1l1_opy_] + bstack1l11l11_opy_ [bstack1lll1l1_opy_:]
    if bstack111ll1_opy_:
        bstack1llll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    else:
        bstack1llll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11lll_opy_ - (bstack1l1l1l_opy_ + bstack111l111_opy_) % bstack111l1ll_opy_) for bstack1l1l1l_opy_, char in enumerate (bstack1llll1_opy_)])
    return eval (bstack1llll1l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll111ll1_opy_, bstack1111l1l1l_opy_, get_host_info, bstack111llll11l1_opy_, \
 bstack1l11l11ll_opy_, bstack11ll1111ll_opy_, bstack111l1lll11_opy_, bstack111lllllll1_opy_, bstack1lll111111_opy_
import bstack_utils.accessibility as bstack11ll1ll11_opy_
from bstack_utils.bstack111lll1111_opy_ import bstack1l11l1l1l1_opy_
from bstack_utils.percy import bstack111l1ll1l_opy_
from bstack_utils.config import Config
bstack1l1llll1l1_opy_ = Config.bstack1l1l11ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack111l1ll1l_opy_()
@bstack111l1lll11_opy_(class_method=False)
def bstack1lllll1lll11_opy_(bs_config, bstack1l11ll1l11_opy_):
  try:
    data = {
        bstackl_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭ℎ"): bstackl_opy_ (u"ࠧ࡫ࡵࡲࡲࠬℏ"),
        bstackl_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧℐ"): bs_config.get(bstackl_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧℑ"), bstackl_opy_ (u"ࠪࠫℒ")),
        bstackl_opy_ (u"ࠫࡳࡧ࡭ࡦࠩℓ"): bs_config.get(bstackl_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ℔"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstackl_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩℕ"): bs_config.get(bstackl_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ№")),
        bstackl_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭℗"): bs_config.get(bstackl_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ℘"), bstackl_opy_ (u"ࠪࠫℙ")),
        bstackl_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨℚ"): bstack1lll111111_opy_(),
        bstackl_opy_ (u"ࠬࡺࡡࡨࡵࠪℛ"): bstack111llll11l1_opy_(bs_config),
        bstackl_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩℜ"): get_host_info(),
        bstackl_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨℝ"): bstack1111l1l1l_opy_(),
        bstackl_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ℞"): os.environ.get(bstackl_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ℟")),
        bstackl_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ℠"): os.environ.get(bstackl_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ℡"), False),
        bstackl_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ™"): bstack11lll111ll1_opy_(),
        bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭℣"): bstack1llll1llll1l_opy_(bs_config),
        bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫℤ"): bstack1llll1lll1l1_opy_(bstack1l11ll1l11_opy_),
        bstackl_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭℥"): bstack1llll1llllll_opy_(bs_config, bstack1l11ll1l11_opy_.get(bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪΩ"), bstackl_opy_ (u"ࠪࠫ℧"))),
        bstackl_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭ℨ"): bstack1l11l11ll_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstackl_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ℩").format(str(error)))
    return None
def bstack1llll1lll1l1_opy_(framework):
  return {
    bstackl_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭K"): framework.get(bstackl_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨÅ"), bstackl_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨℬ")),
    bstackl_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬℭ"): framework.get(bstackl_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ℮")),
    bstackl_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨℯ"): framework.get(bstackl_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪℰ")),
    bstackl_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨℱ"): bstackl_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧℲ"),
    bstackl_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨℳ"): framework.get(bstackl_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩℴ"))
  }
def bstack11ll1l1ll_opy_(bs_config, framework):
  bstack1ll1111ll_opy_ = False
  bstack1ll1ll1l1l_opy_ = False
  bstack1llll1lllll1_opy_ = False
  if bstackl_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧℵ") in bs_config:
    bstack1llll1lllll1_opy_ = True
  elif bstackl_opy_ (u"ࠫࡦࡶࡰࠨℶ") in bs_config:
    bstack1ll1111ll_opy_ = True
  else:
    bstack1ll1ll1l1l_opy_ = True
  bstack1l1l11l1_opy_ = {
    bstackl_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬℷ"): bstack1l11l1l1l1_opy_.bstack1lllll111l1l_opy_(bs_config, framework),
    bstackl_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭ℸ"): bstack11ll1ll11_opy_.bstack1llll111l_opy_(bs_config),
    bstackl_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭ℹ"): bs_config.get(bstackl_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ℺"), False),
    bstackl_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ℻"): bstack1ll1ll1l1l_opy_,
    bstackl_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩℼ"): bstack1ll1111ll_opy_,
    bstackl_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨℽ"): bstack1llll1lllll1_opy_
  }
  return bstack1l1l11l1_opy_
@bstack111l1lll11_opy_(class_method=False)
def bstack1llll1llll1l_opy_(bs_config):
  try:
    bstack1llll1llll11_opy_ = json.loads(os.getenv(bstackl_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭ℾ"), bstackl_opy_ (u"࠭ࡻࡾࠩℿ")))
    bstack1llll1llll11_opy_ = bstack1lllll11111l_opy_(bs_config, bstack1llll1llll11_opy_)
    return {
        bstackl_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ⅀"): bstack1llll1llll11_opy_
    }
  except Exception as error:
    logger.error(bstackl_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⅁").format(str(error)))
    return {}
def bstack1lllll11111l_opy_(bs_config, bstack1llll1llll11_opy_):
  if ((bstackl_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⅂") in bs_config or not bstack1l11l11ll_opy_(bs_config)) and bstack11ll1ll11_opy_.bstack1llll111l_opy_(bs_config)):
    bstack1llll1llll11_opy_[bstackl_opy_ (u"ࠥ࡭ࡳࡩ࡬ࡶࡦࡨࡉࡳࡩ࡯ࡥࡧࡧࡉࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠨ⅃")] = True
  return bstack1llll1llll11_opy_
def bstack1lllll11l1l1_opy_(array, bstack1lllll111111_opy_, bstack1lllll1111l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1lllll111111_opy_]
    result[key] = o[bstack1lllll1111l1_opy_]
  return result
def bstack1lllll1l1111_opy_(bstack1l111ll111_opy_=bstackl_opy_ (u"ࠫࠬ⅄")):
  bstack1lllll111ll1_opy_ = bstack11ll1ll11_opy_.on()
  bstack1llll1lll1ll_opy_ = bstack1l11l1l1l1_opy_.on()
  bstack1lllll111l11_opy_ = percy.bstack1l11lll11_opy_()
  if bstack1lllll111l11_opy_ and not bstack1llll1lll1ll_opy_ and not bstack1lllll111ll1_opy_:
    return bstack1l111ll111_opy_ not in [bstackl_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩⅅ"), bstackl_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪⅆ")]
  elif bstack1lllll111ll1_opy_ and not bstack1llll1lll1ll_opy_:
    return bstack1l111ll111_opy_ not in [bstackl_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨⅇ"), bstackl_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪⅈ"), bstackl_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭ⅉ")]
  return bstack1lllll111ll1_opy_ or bstack1llll1lll1ll_opy_ or bstack1lllll111l11_opy_
@bstack111l1lll11_opy_(class_method=False)
def bstack1lllll1ll1ll_opy_(bstack1l111ll111_opy_, test=None):
  bstack1lllll1111ll_opy_ = bstack11ll1ll11_opy_.on()
  if not bstack1lllll1111ll_opy_ or bstack1l111ll111_opy_ not in [bstackl_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⅊")] or test == None:
    return None
  return {
    bstackl_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⅋"): bstack1lllll1111ll_opy_ and bstack11ll1111ll_opy_(threading.current_thread(), bstackl_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⅌"), None) == True and bstack11ll1ll11_opy_.bstack1l111lll_opy_(test[bstackl_opy_ (u"࠭ࡴࡢࡩࡶࠫ⅍")])
  }
def bstack1llll1llllll_opy_(bs_config, framework):
  bstack1ll1111ll_opy_ = False
  bstack1ll1ll1l1l_opy_ = False
  bstack1llll1lllll1_opy_ = False
  if bstackl_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫⅎ") in bs_config:
    bstack1llll1lllll1_opy_ = True
  elif bstackl_opy_ (u"ࠨࡣࡳࡴࠬ⅏") in bs_config:
    bstack1ll1111ll_opy_ = True
  else:
    bstack1ll1ll1l1l_opy_ = True
  bstack1l1l11l1_opy_ = {
    bstackl_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⅐"): bstack1l11l1l1l1_opy_.bstack1lllll111l1l_opy_(bs_config, framework),
    bstackl_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⅑"): bstack11ll1ll11_opy_.bstack11ll1l1lll_opy_(bs_config),
    bstackl_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⅒"): bs_config.get(bstackl_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⅓"), False),
    bstackl_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ⅔"): bstack1ll1ll1l1l_opy_,
    bstackl_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⅕"): bstack1ll1111ll_opy_,
    bstackl_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ⅖"): bstack1llll1lllll1_opy_
  }
  return bstack1l1l11l1_opy_