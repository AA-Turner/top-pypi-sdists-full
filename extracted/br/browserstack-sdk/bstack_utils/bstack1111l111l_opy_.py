# coding: UTF-8
import sys
bstack1ll11l_opy_ = sys.version_info [0] == 2
bstack111111l_opy_ = 2048
bstack111l1ll_opy_ = 7
def bstack11l1_opy_ (bstack1llllll1_opy_):
    global bstack1l11ll_opy_
    bstack1ll111l_opy_ = ord (bstack1llllll1_opy_ [-1])
    bstack1l1l1l1_opy_ = bstack1llllll1_opy_ [:-1]
    bstack1l111_opy_ = bstack1ll111l_opy_ % len (bstack1l1l1l1_opy_)
    bstack11ll1ll_opy_ = bstack1l1l1l1_opy_ [:bstack1l111_opy_] + bstack1l1l1l1_opy_ [bstack1l111_opy_:]
    if bstack1ll11l_opy_:
        bstack11l1ll_opy_ = unicode () .join ([unichr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    else:
        bstack11l1ll_opy_ = str () .join ([chr (ord (char) - bstack111111l_opy_ - (bstack11111ll_opy_ + bstack1ll111l_opy_) % bstack111l1ll_opy_) for bstack11111ll_opy_, char in enumerate (bstack11ll1ll_opy_)])
    return eval (bstack11l1ll_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll11l11l_opy_, bstack1lllll11l_opy_, get_host_info, bstack11l11ll1l11_opy_, \
 bstack111l1llll_opy_, bstack1ll11l11ll_opy_, error_handler, bstack111llll1l11_opy_, bstack1l1l11lll_opy_
import bstack_utils.accessibility as bstack1ll1ll1111_opy_
from bstack_utils.bstack111l11l1_opy_ import bstack1l111ll11l_opy_
from bstack_utils.bstack111ll1ll11_opy_ import bstack11l1l1111_opy_
from bstack_utils.percy import bstack11111111_opy_
from bstack_utils.config import Config
bstack1l1llll1l_opy_ = Config.bstack1l1lll11l_opy_()
logger = logging.getLogger(__name__)
percy = bstack11111111_opy_()
@error_handler(class_method=False)
def bstack1llll1lll11l_opy_(bs_config, bstack111ll1ll_opy_):
  try:
    data = {
        bstack11l1_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪ↗"): bstack11l1_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩ↘"),
        bstack11l1_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫ↙"): bs_config.get(bstack11l1_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ↚"), bstack11l1_opy_ (u"ࠧࠨ↛")),
        bstack11l1_opy_ (u"ࠨࡰࡤࡱࡪ࠭↜"): bs_config.get(bstack11l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ↝"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭↞"): bs_config.get(bstack11l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭↟")),
        bstack11l1_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ↠"): bs_config.get(bstack11l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ↡"), bstack11l1_opy_ (u"ࠧࠨ↢")),
        bstack11l1_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ↣"): bstack1l1l11lll_opy_(),
        bstack11l1_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ↤"): bstack11l11ll1l11_opy_(bs_config),
        bstack11l1_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭↥"): get_host_info(),
        bstack11l1_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬ↦"): bstack1lllll11l_opy_(),
        bstack11l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ↧"): os.environ.get(bstack11l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ↨")),
        bstack11l1_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬ↩"): os.environ.get(bstack11l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭↪"), False),
        bstack11l1_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫ↫"): bstack11lll11l11l_opy_(),
        bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ↬"): bstack1llll1l1l1l1_opy_(bs_config),
        bstack11l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨ↭"): bstack1llll1l11ll1_opy_(bstack111ll1ll_opy_),
        bstack11l1_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ↮"): bstack1llll1l11lll_opy_(bs_config, bstack111ll1ll_opy_.get(bstack11l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ↯"), bstack11l1_opy_ (u"ࠧࠨ↰"))),
        bstack11l1_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ↱"): bstack111l1llll_opy_(bs_config),
        bstack11l1_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠧ↲"): bstack1llll1l1ll1l_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack11l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ↳").format(str(error)))
    return None
def bstack1llll1l11ll1_opy_(framework):
  return {
    bstack11l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫ↴"): framework.get(bstack11l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭↵"), bstack11l1_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭↶")),
    bstack11l1_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ↷"): framework.get(bstack11l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ↸")),
    bstack11l1_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭↹"): framework.get(bstack11l1_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ↺")),
    bstack11l1_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭↻"): bstack11l1_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ↼"),
    bstack11l1_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭↽"): framework.get(bstack11l1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ↾"))
  }
def bstack1llll1l1ll1l_opy_(bs_config):
  bstack11l1_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦࠣࡷࡹࡧࡲࡵ࠰ࠍࠤࠥࠨࠢࠣ↿")
  if not bs_config:
    return {}
  bstack111l11l111l_opy_ = bstack1l111ll11l_opy_(bs_config).bstack1111lll1l11_opy_(bs_config)
  return bstack111l11l111l_opy_
def bstack11111lll1_opy_(bs_config, framework):
  bstack1lll11l111_opy_ = False
  bstack1l1lll1lll_opy_ = False
  bstack1llll1l1l1ll_opy_ = False
  if bstack11l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⇀") in bs_config:
    bstack1llll1l1l1ll_opy_ = True
  elif bstack11l1_opy_ (u"ࠪࡥࡵࡶࠧ⇁") in bs_config:
    bstack1lll11l111_opy_ = True
  else:
    bstack1l1lll1lll_opy_ = True
  bstack1llll1111l_opy_ = {
    bstack11l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⇂"): bstack11l1l1111_opy_.bstack1llll1l11l11_opy_(bs_config, framework),
    bstack11l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⇃"): bstack1ll1ll1111_opy_.bstack1l1l1llll_opy_(bs_config),
    bstack11l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⇄"): bs_config.get(bstack11l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⇅"), False),
    bstack11l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⇆"): bstack1l1lll1lll_opy_,
    bstack11l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⇇"): bstack1lll11l111_opy_,
    bstack11l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⇈"): bstack1llll1l1l1ll_opy_
  }
  return bstack1llll1111l_opy_
@error_handler(class_method=False)
def bstack1llll1l1l1l1_opy_(bs_config):
  try:
    bstack1llll1l1ll11_opy_ = json.loads(os.getenv(bstack11l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⇉"), bstack11l1_opy_ (u"ࠬࢁࡽࠨ⇊")))
    bstack1llll1l1ll11_opy_ = bstack1llll1l1l11l_opy_(bs_config, bstack1llll1l1ll11_opy_)
    return {
        bstack11l1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ⇋"): bstack1llll1l1ll11_opy_
    }
  except Exception as error:
    logger.error(bstack11l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⇌").format(str(error)))
    return {}
def bstack1llll1l1l11l_opy_(bs_config, bstack1llll1l1ll11_opy_):
  if ((bstack11l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⇍") in bs_config or not bstack111l1llll_opy_(bs_config)) and bstack1ll1ll1111_opy_.bstack1l1l1llll_opy_(bs_config)):
    bstack1llll1l1ll11_opy_[bstack11l1_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧ⇎")] = True
  return bstack1llll1l1ll11_opy_
def bstack1lllll11l11l_opy_(array, bstack1llll1l1l111_opy_, bstack1llll1l111ll_opy_):
  result = {}
  for o in array:
    key = o[bstack1llll1l1l111_opy_]
    result[key] = o[bstack1llll1l111ll_opy_]
  return result
def bstack1lllll111111_opy_(bstack1l1111ll1_opy_=bstack11l1_opy_ (u"ࠪࠫ⇏")):
  bstack1llll1l1llll_opy_ = bstack1ll1ll1111_opy_.on()
  bstack1llll1l111l1_opy_ = bstack11l1l1111_opy_.on()
  bstack1llll1l11l1l_opy_ = percy.bstack11lll1l11_opy_()
  if bstack1llll1l11l1l_opy_ and not bstack1llll1l111l1_opy_ and not bstack1llll1l1llll_opy_:
    return bstack1l1111ll1_opy_ not in [bstack11l1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ⇐"), bstack11l1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⇑")]
  elif bstack1llll1l1llll_opy_ and not bstack1llll1l111l1_opy_:
    return bstack1l1111ll1_opy_ not in [bstack11l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⇒"), bstack11l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⇓"), bstack11l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⇔")]
  return bstack1llll1l1llll_opy_ or bstack1llll1l111l1_opy_ or bstack1llll1l11l1l_opy_
@error_handler(class_method=False)
def bstack1lllll11111l_opy_(bstack1l1111ll1_opy_, test=None):
  bstack1llll1l1lll1_opy_ = bstack1ll1ll1111_opy_.on()
  if not bstack1llll1l1lll1_opy_ or bstack1l1111ll1_opy_ not in [bstack11l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⇕")] or test == None:
    return None
  return {
    bstack11l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⇖"): bstack1llll1l1lll1_opy_ and bstack1ll11l11ll_opy_(threading.current_thread(), bstack11l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⇗"), None) == True and bstack1ll1ll1111_opy_.bstack1ll11ll11_opy_(test[bstack11l1_opy_ (u"ࠬࡺࡡࡨࡵࠪ⇘")])
  }
def bstack1llll1l11lll_opy_(bs_config, framework):
  bstack1lll11l111_opy_ = False
  bstack1l1lll1lll_opy_ = False
  bstack1llll1l1l1ll_opy_ = False
  if bstack11l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⇙") in bs_config:
    bstack1llll1l1l1ll_opy_ = True
  elif bstack11l1_opy_ (u"ࠧࡢࡲࡳࠫ⇚") in bs_config:
    bstack1lll11l111_opy_ = True
  else:
    bstack1l1lll1lll_opy_ = True
  bstack1llll1111l_opy_ = {
    bstack11l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⇛"): bstack11l1l1111_opy_.bstack1llll1l11l11_opy_(bs_config, framework),
    bstack11l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⇜"): bstack1ll1ll1111_opy_.bstack11l111111_opy_(bs_config),
    bstack11l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⇝"): bs_config.get(bstack11l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⇞"), False),
    bstack11l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⇟"): bstack1l1lll1lll_opy_,
    bstack11l1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⇠"): bstack1lll11l111_opy_,
    bstack11l1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⇡"): bstack1llll1l1l1ll_opy_
  }
  return bstack1llll1111l_opy_