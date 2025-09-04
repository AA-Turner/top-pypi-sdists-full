# coding: UTF-8
import sys
bstack1111ll_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1_opy_ = 7
def bstack1111l1l_opy_ (bstack1l11_opy_):
    global bstack1ll1_opy_
    bstack11l11l1_opy_ = ord (bstack1l11_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1l11_opy_ [:-1]
    bstack111lll_opy_ = bstack11l11l1_opy_ % len (bstack1l1l1l1_opy_)
    bstack11l11ll_opy_ = bstack1l1l1l1_opy_ [:bstack111lll_opy_] + bstack1l1l1l1_opy_ [bstack111lll_opy_:]
    if bstack1111ll_opy_:
        bstack1ll1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    else:
        bstack1ll1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll11ll_opy_ + bstack11l11l1_opy_) % bstack11l1l1_opy_) for bstack1ll11ll_opy_, char in enumerate (bstack11l11ll_opy_)])
    return eval (bstack1ll1lll_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1l1lll1_opy_, bstack1ll111ll_opy_, get_host_info, bstack111llll111l_opy_, \
 bstack111l1l11_opy_, bstack1l11l1lll_opy_, error_handler, bstack11l11l1l1ll_opy_, bstack1ll111ll1l_opy_
import bstack_utils.accessibility as bstack1lll1111l1_opy_
from bstack_utils.bstack11llllll_opy_ import bstack111l1llll_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack1ll11lll1_opy_
from bstack_utils.percy import bstack1llll111l1_opy_
from bstack_utils.config import Config
bstack1l1ll11l1_opy_ = Config.bstack1l11llll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1llll111l1_opy_()
@error_handler(class_method=False)
def bstack1llll1ll1ll1_opy_(bs_config, bstack1l1ll1l1_opy_):
  try:
    data = {
        bstack1111l1l_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧ↛"): bstack1111l1l_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭↜"),
        bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨ↝"): bs_config.get(bstack1111l1l_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ↞"), bstack1111l1l_opy_ (u"ࠫࠬ↟")),
        bstack1111l1l_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ↠"): bs_config.get(bstack1111l1l_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ↡"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1111l1l_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ↢"): bs_config.get(bstack1111l1l_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ↣")),
        bstack1111l1l_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ↤"): bs_config.get(bstack1111l1l_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭↥"), bstack1111l1l_opy_ (u"ࠫࠬ↦")),
        bstack1111l1l_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ↧"): bstack1ll111ll1l_opy_(),
        bstack1111l1l_opy_ (u"࠭ࡴࡢࡩࡶࠫ↨"): bstack111llll111l_opy_(bs_config),
        bstack1111l1l_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ↩"): get_host_info(),
        bstack1111l1l_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩ↪"): bstack1ll111ll_opy_(),
        bstack1111l1l_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ↫"): os.environ.get(bstack1111l1l_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ↬")),
        bstack1111l1l_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩ↭"): os.environ.get(bstack1111l1l_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ↮"), False),
        bstack1111l1l_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨ↯"): bstack11ll1l1lll1_opy_(),
        bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ↰"): bstack1llll11lll11_opy_(bs_config),
        bstack1111l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬ↱"): bstack1llll11ll111_opy_(bstack1l1ll1l1_opy_),
        bstack1111l1l_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ↲"): bstack1llll11l111l_opy_(bs_config, bstack1l1ll1l1_opy_.get(bstack1111l1l_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ↳"), bstack1111l1l_opy_ (u"ࠫࠬ↴"))),
        bstack1111l1l_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ↵"): bstack111l1l11_opy_(bs_config),
        bstack1111l1l_opy_ (u"࠭ࡴࡦࡵࡷࡣࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫ↶"): bstack1llll11ll1ll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1111l1l_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ↷").format(str(error)))
    return None
def bstack1llll11ll111_opy_(framework):
  return {
    bstack1111l1l_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ↸"): framework.get(bstack1111l1l_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ↹"), bstack1111l1l_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ↺")),
    bstack1111l1l_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ↻"): framework.get(bstack1111l1l_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ↼")),
    bstack1111l1l_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ↽"): framework.get(bstack1111l1l_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ↾")),
    bstack1111l1l_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ↿"): bstack1111l1l_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⇀"),
    bstack1111l1l_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⇁"): framework.get(bstack1111l1l_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⇂"))
  }
def bstack1llll11ll1ll_opy_(bs_config):
  bstack1111l1l_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡴࡶࡤࡶࡹ࠴ࠊࠡࠢࠥࠦࠧ⇃")
  if not bs_config:
    return {}
  bstack111l1111l1l_opy_ = bstack111l1llll_opy_(bs_config).bstack1111llllll1_opy_(bs_config)
  return bstack111l1111l1l_opy_
def bstack1l1llll1_opy_(bs_config, framework):
  bstack1l11111l11_opy_ = False
  bstack1l111ll1ll_opy_ = False
  bstack1llll11l1l11_opy_ = False
  if bstack1111l1l_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⇄") in bs_config:
    bstack1llll11l1l11_opy_ = True
  elif bstack1111l1l_opy_ (u"ࠧࡢࡲࡳࠫ⇅") in bs_config:
    bstack1l11111l11_opy_ = True
  else:
    bstack1l111ll1ll_opy_ = True
  bstack1l1lllll_opy_ = {
    bstack1111l1l_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⇆"): bstack1ll11lll1_opy_.bstack1llll11l1111_opy_(bs_config, framework),
    bstack1111l1l_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⇇"): bstack1lll1111l1_opy_.bstack11l1l11ll_opy_(bs_config),
    bstack1111l1l_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⇈"): bs_config.get(bstack1111l1l_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⇉"), False),
    bstack1111l1l_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⇊"): bstack1l111ll1ll_opy_,
    bstack1111l1l_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⇋"): bstack1l11111l11_opy_,
    bstack1111l1l_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⇌"): bstack1llll11l1l11_opy_
  }
  return bstack1l1lllll_opy_
@error_handler(class_method=False)
def bstack1llll11lll11_opy_(bs_config):
  try:
    bstack1llll11l1l1l_opy_ = json.loads(os.getenv(bstack1111l1l_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ⇍"), bstack1111l1l_opy_ (u"ࠩࡾࢁࠬ⇎")))
    bstack1llll11l1l1l_opy_ = bstack1llll11l11ll_opy_(bs_config, bstack1llll11l1l1l_opy_)
    return {
        bstack1111l1l_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬ⇏"): bstack1llll11l1l1l_opy_
    }
  except Exception as error:
    logger.error(bstack1111l1l_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ⇐").format(str(error)))
    return {}
def bstack1llll11l11ll_opy_(bs_config, bstack1llll11l1l1l_opy_):
  if ((bstack1111l1l_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⇑") in bs_config or not bstack111l1l11_opy_(bs_config)) and bstack1lll1111l1_opy_.bstack11l1l11ll_opy_(bs_config)):
    bstack1llll11l1l1l_opy_[bstack1111l1l_opy_ (u"ࠨࡩ࡯ࡥ࡯ࡹࡩ࡫ࡅ࡯ࡥࡲࡨࡪࡪࡅࡹࡶࡨࡲࡸ࡯࡯࡯ࠤ⇒")] = True
  return bstack1llll11l1l1l_opy_
def bstack1llll1ll11ll_opy_(array, bstack1llll11l11l1_opy_, bstack1llll11ll11l_opy_):
  result = {}
  for o in array:
    key = o[bstack1llll11l11l1_opy_]
    result[key] = o[bstack1llll11ll11l_opy_]
  return result
def bstack1llll1l111l1_opy_(bstack1llll1111_opy_=bstack1111l1l_opy_ (u"ࠧࠨ⇓")):
  bstack1llll11l1ll1_opy_ = bstack1lll1111l1_opy_.on()
  bstack1llll11ll1l1_opy_ = bstack1ll11lll1_opy_.on()
  bstack1llll11l1lll_opy_ = percy.bstack11lll1l1l_opy_()
  if bstack1llll11l1lll_opy_ and not bstack1llll11ll1l1_opy_ and not bstack1llll11l1ll1_opy_:
    return bstack1llll1111_opy_ not in [bstack1111l1l_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ⇔"), bstack1111l1l_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⇕")]
  elif bstack1llll11l1ll1_opy_ and not bstack1llll11ll1l1_opy_:
    return bstack1llll1111_opy_ not in [bstack1111l1l_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⇖"), bstack1111l1l_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⇗"), bstack1111l1l_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⇘")]
  return bstack1llll11l1ll1_opy_ or bstack1llll11ll1l1_opy_ or bstack1llll11l1lll_opy_
@error_handler(class_method=False)
def bstack1llll1ll1l11_opy_(bstack1llll1111_opy_, test=None):
  bstack1llll11lll1l_opy_ = bstack1lll1111l1_opy_.on()
  if not bstack1llll11lll1l_opy_ or bstack1llll1111_opy_ not in [bstack1111l1l_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⇙")] or test == None:
    return None
  return {
    bstack1111l1l_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⇚"): bstack1llll11lll1l_opy_ and bstack1l11l1lll_opy_(threading.current_thread(), bstack1111l1l_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⇛"), None) == True and bstack1lll1111l1_opy_.bstack11l111ll_opy_(test[bstack1111l1l_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⇜")])
  }
def bstack1llll11l111l_opy_(bs_config, framework):
  bstack1l11111l11_opy_ = False
  bstack1l111ll1ll_opy_ = False
  bstack1llll11l1l11_opy_ = False
  if bstack1111l1l_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⇝") in bs_config:
    bstack1llll11l1l11_opy_ = True
  elif bstack1111l1l_opy_ (u"ࠫࡦࡶࡰࠨ⇞") in bs_config:
    bstack1l11111l11_opy_ = True
  else:
    bstack1l111ll1ll_opy_ = True
  bstack1l1lllll_opy_ = {
    bstack1111l1l_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⇟"): bstack1ll11lll1_opy_.bstack1llll11l1111_opy_(bs_config, framework),
    bstack1111l1l_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⇠"): bstack1lll1111l1_opy_.bstack1llllllll1_opy_(bs_config),
    bstack1111l1l_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⇡"): bs_config.get(bstack1111l1l_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⇢"), False),
    bstack1111l1l_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⇣"): bstack1l111ll1ll_opy_,
    bstack1111l1l_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⇤"): bstack1l11111l11_opy_,
    bstack1111l1l_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⇥"): bstack1llll11l1l11_opy_
  }
  return bstack1l1lllll_opy_