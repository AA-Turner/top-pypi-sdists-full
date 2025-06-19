# coding: UTF-8
import sys
bstack111ll1_opy_ = sys.version_info [0] == 2
bstack1llll1_opy_ = 2048
bstack1111l_opy_ = 7
def bstack111lll_opy_ (bstack1lll1l_opy_):
    global bstack1l11lll_opy_
    bstack1ll1l1_opy_ = ord (bstack1lll1l_opy_ [-1])
    bstack1ll1l11_opy_ = bstack1lll1l_opy_ [:-1]
    bstack1l_opy_ = bstack1ll1l1_opy_ % len (bstack1ll1l11_opy_)
    bstack1l11ll_opy_ = bstack1ll1l11_opy_ [:bstack1l_opy_] + bstack1ll1l11_opy_ [bstack1l_opy_:]
    if bstack111ll1_opy_:
        bstack1l1l11l_opy_ = unicode () .join ([unichr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    else:
        bstack1l1l11l_opy_ = str () .join ([chr (ord (char) - bstack1llll1_opy_ - (bstack1111l1l_opy_ + bstack1ll1l1_opy_) % bstack1111l_opy_) for bstack1111l1l_opy_, char in enumerate (bstack1l11ll_opy_)])
    return eval (bstack1l1l11l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll11l1ll_opy_, bstack1lll111lll_opy_, get_host_info, bstack11l11l1ll11_opy_, \
 bstack1l1l111l1_opy_, bstack1ll11l1l1l_opy_, bstack111l1ll1l1_opy_, bstack11l111111ll_opy_, bstack1llllllll1_opy_
import bstack_utils.accessibility as bstack1l11l11ll1_opy_
from bstack_utils.bstack111lll1l1l_opy_ import bstack11l1ll111_opy_
from bstack_utils.percy import bstack11l1ll1l11_opy_
from bstack_utils.config import Config
bstack1ll1l11ll_opy_ = Config.bstack1ll11lll1l_opy_()
logger = logging.getLogger(__name__)
percy = bstack11l1ll1l11_opy_()
@bstack111l1ll1l1_opy_(class_method=False)
def bstack11111l11l11_opy_(bs_config, bstack1ll1l11l1l_opy_):
  try:
    data = {
        bstack111lll_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭‼"): bstack111lll_opy_ (u"ࠧ࡫ࡵࡲࡲࠬ‽"),
        bstack111lll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧ‾"): bs_config.get(bstack111lll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ‿"), bstack111lll_opy_ (u"ࠪࠫ⁀")),
        bstack111lll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ⁁"): bs_config.get(bstack111lll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ⁂"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack111lll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⁃"): bs_config.get(bstack111lll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⁄")),
        bstack111lll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭⁅"): bs_config.get(bstack111lll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⁆"), bstack111lll_opy_ (u"ࠪࠫ⁇")),
        bstack111lll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ⁈"): bstack1llllllll1_opy_(),
        bstack111lll_opy_ (u"ࠬࡺࡡࡨࡵࠪ⁉"): bstack11l11l1ll11_opy_(bs_config),
        bstack111lll_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩ⁊"): get_host_info(),
        bstack111lll_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ⁋"): bstack1lll111lll_opy_(),
        bstack111lll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⁌"): os.environ.get(bstack111lll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ⁍")),
        bstack111lll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ⁎"): os.environ.get(bstack111lll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ⁏"), False),
        bstack111lll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ⁐"): bstack11lll11l1ll_opy_(),
        bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⁑"): bstack111111l111l_opy_(bs_config),
        bstack111lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫ⁒"): bstack1111111l1ll_opy_(bstack1ll1l11l1l_opy_),
        bstack111lll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⁓"): bstack11111111ll1_opy_(bs_config, bstack1ll1l11l1l_opy_.get(bstack111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ⁔"), bstack111lll_opy_ (u"ࠪࠫ⁕"))),
        bstack111lll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⁖"): bstack1l1l111l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack111lll_opy_ (u"ࠧࡋࡸࡤࡧࡳࡸ࡮ࡵ࡮ࠡࡹ࡫࡭ࡱ࡫ࠠࡤࡴࡨࡥࡹ࡯࡮ࡨࠢࡳࡥࡾࡲ࡯ࡢࡦࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⁗").format(str(error)))
    return None
def bstack1111111l1ll_opy_(framework):
  return {
    bstack111lll_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡐࡤࡱࡪ࠭⁘"): framework.get(bstack111lll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡲࡦࡳࡥࠨ⁙"), bstack111lll_opy_ (u"ࠨࡒࡼࡸࡪࡹࡴࠨ⁚")),
    bstack111lll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⁛"): framework.get(bstack111lll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⁜")),
    bstack111lll_opy_ (u"ࠫࡸࡪ࡫ࡗࡧࡵࡷ࡮ࡵ࡮ࠨ⁝"): framework.get(bstack111lll_opy_ (u"ࠬࡹࡤ࡬ࡡࡹࡩࡷࡹࡩࡰࡰࠪ⁞")),
    bstack111lll_opy_ (u"࠭࡬ࡢࡰࡪࡹࡦ࡭ࡥࠨ "): bstack111lll_opy_ (u"ࠧࡱࡻࡷ࡬ࡴࡴࠧ⁠"),
    bstack111lll_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⁡"): framework.get(bstack111lll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⁢"))
  }
def bstack1l1ll1lll1_opy_(bs_config, framework):
  bstack1ll1lllll1_opy_ = False
  bstack11l1llllll_opy_ = False
  bstack1111111l11l_opy_ = False
  if bstack111lll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⁣") in bs_config:
    bstack1111111l11l_opy_ = True
  elif bstack111lll_opy_ (u"ࠫࡦࡶࡰࠨ⁤") in bs_config:
    bstack1ll1lllll1_opy_ = True
  else:
    bstack11l1llllll_opy_ = True
  bstack11ll1ll1ll_opy_ = {
    bstack111lll_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⁥"): bstack11l1ll111_opy_.bstack1111111ll1l_opy_(bs_config, framework),
    bstack111lll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⁦"): bstack1l11l11ll1_opy_.bstack1l111lll1l_opy_(bs_config),
    bstack111lll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⁧"): bs_config.get(bstack111lll_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⁨"), False),
    bstack111lll_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⁩"): bstack11l1llllll_opy_,
    bstack111lll_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⁪"): bstack1ll1lllll1_opy_,
    bstack111lll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⁫"): bstack1111111l11l_opy_
  }
  return bstack11ll1ll1ll_opy_
@bstack111l1ll1l1_opy_(class_method=False)
def bstack111111l111l_opy_(bs_config):
  try:
    bstack1111111ll11_opy_ = json.loads(os.getenv(bstack111lll_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣ࡙ࡋࡓࡕࡡࡄࡇࡈࡋࡓࡔࡋࡅࡍࡑࡏࡔ࡚ࡡࡆࡓࡓࡌࡉࡈࡗࡕࡅ࡙ࡏࡏࡏࡡ࡜ࡑࡑ࠭⁬"), bstack111lll_opy_ (u"࠭ࡻࡾࠩ⁭")))
    bstack1111111ll11_opy_ = bstack1111111l1l1_opy_(bs_config, bstack1111111ll11_opy_)
    return {
        bstack111lll_opy_ (u"ࠧࡴࡧࡷࡸ࡮ࡴࡧࡴࠩ⁮"): bstack1111111ll11_opy_
    }
  except Exception as error:
    logger.error(bstack111lll_opy_ (u"ࠣࡇࡻࡧࡪࡶࡴࡪࡱࡱࠤࡼ࡮ࡩ࡭ࡧࠣࡧࡷ࡫ࡡࡵ࡫ࡱ࡫ࠥ࡭ࡥࡵࡡࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࡡࡶࡩࡹࡺࡩ࡯ࡩࡶࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⁯").format(str(error)))
    return {}
def bstack1111111l1l1_opy_(bs_config, bstack1111111ll11_opy_):
  if ((bstack111lll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⁰") in bs_config or not bstack1l1l111l1_opy_(bs_config)) and bstack1l11l11ll1_opy_.bstack1l111lll1l_opy_(bs_config)):
    bstack1111111ll11_opy_[bstack111lll_opy_ (u"ࠥ࡭ࡳࡩ࡬ࡶࡦࡨࡉࡳࡩ࡯ࡥࡧࡧࡉࡽࡺࡥ࡯ࡵ࡬ࡳࡳࠨⁱ")] = True
  return bstack1111111ll11_opy_
def bstack11111l111l1_opy_(array, bstack11111111lll_opy_, bstack11111111l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack11111111lll_opy_]
    result[key] = o[bstack11111111l1l_opy_]
  return result
def bstack11111l11ll1_opy_(bstack1ll1111l1l_opy_=bstack111lll_opy_ (u"ࠫࠬ⁲")):
  bstack111111l1111_opy_ = bstack1l11l11ll1_opy_.on()
  bstack1111111lll1_opy_ = bstack11l1ll111_opy_.on()
  bstack1111111llll_opy_ = percy.bstack11l1ll11l1_opy_()
  if bstack1111111llll_opy_ and not bstack1111111lll1_opy_ and not bstack111111l1111_opy_:
    return bstack1ll1111l1l_opy_ not in [bstack111lll_opy_ (u"ࠬࡉࡂࡕࡕࡨࡷࡸ࡯࡯࡯ࡅࡵࡩࡦࡺࡥࡥࠩ⁳"), bstack111lll_opy_ (u"࠭ࡌࡰࡩࡆࡶࡪࡧࡴࡦࡦࠪ⁴")]
  elif bstack111111l1111_opy_ and not bstack1111111lll1_opy_:
    return bstack1ll1111l1l_opy_ not in [bstack111lll_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡔࡶࡤࡶࡹ࡫ࡤࠨ⁵"), bstack111lll_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⁶"), bstack111lll_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⁷")]
  return bstack111111l1111_opy_ or bstack1111111lll1_opy_ or bstack1111111llll_opy_
@bstack111l1ll1l1_opy_(class_method=False)
def bstack11111l1l11l_opy_(bstack1ll1111l1l_opy_, test=None):
  bstack1111111l111_opy_ = bstack1l11l11ll1_opy_.on()
  if not bstack1111111l111_opy_ or bstack1ll1111l1l_opy_ not in [bstack111lll_opy_ (u"ࠪࡘࡪࡹࡴࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⁸")] or test == None:
    return None
  return {
    bstack111lll_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⁹"): bstack1111111l111_opy_ and bstack1ll11l1l1l_opy_(threading.current_thread(), bstack111lll_opy_ (u"ࠬࡧ࠱࠲ࡻࡓࡰࡦࡺࡦࡰࡴࡰࠫ⁺"), None) == True and bstack1l11l11ll1_opy_.bstack11lllllll1_opy_(test[bstack111lll_opy_ (u"࠭ࡴࡢࡩࡶࠫ⁻")])
  }
def bstack11111111ll1_opy_(bs_config, framework):
  bstack1ll1lllll1_opy_ = False
  bstack11l1llllll_opy_ = False
  bstack1111111l11l_opy_ = False
  if bstack111lll_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⁼") in bs_config:
    bstack1111111l11l_opy_ = True
  elif bstack111lll_opy_ (u"ࠨࡣࡳࡴࠬ⁽") in bs_config:
    bstack1ll1lllll1_opy_ = True
  else:
    bstack11l1llllll_opy_ = True
  bstack11ll1ll1ll_opy_ = {
    bstack111lll_opy_ (u"ࠩࡲࡦࡸ࡫ࡲࡷࡣࡥ࡭ࡱ࡯ࡴࡺࠩ⁾"): bstack11l1ll111_opy_.bstack1111111ll1l_opy_(bs_config, framework),
    bstack111lll_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪⁿ"): bstack1l11l11ll1_opy_.bstack11ll1ll11_opy_(bs_config),
    bstack111lll_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ₀"): bs_config.get(bstack111lll_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ₁"), False),
    bstack111lll_opy_ (u"࠭ࡡࡶࡶࡲࡱࡦࡺࡥࠨ₂"): bstack11l1llllll_opy_,
    bstack111lll_opy_ (u"ࠧࡢࡲࡳࡣࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭₃"): bstack1ll1lllll1_opy_,
    bstack111lll_opy_ (u"ࠨࡶࡸࡶࡧࡵࡳࡤࡣ࡯ࡩࠬ₄"): bstack1111111l11l_opy_
  }
  return bstack11ll1ll1ll_opy_