# coding: UTF-8
import sys
bstack1llll1l_opy_ = sys.version_info [0] == 2
bstack1lll111_opy_ = 2048
bstack11l1l1l_opy_ = 7
def bstack1ll11ll_opy_ (bstack1ll1lll_opy_):
    global bstack1ll1l1l_opy_
    bstack1ll11l_opy_ = ord (bstack1ll1lll_opy_ [-1])
    bstack1l11_opy_ = bstack1ll1lll_opy_ [:-1]
    bstack1l1l1ll_opy_ = bstack1ll11l_opy_ % len (bstack1l11_opy_)
    bstack111111_opy_ = bstack1l11_opy_ [:bstack1l1l1ll_opy_] + bstack1l11_opy_ [bstack1l1l1ll_opy_:]
    if bstack1llll1l_opy_:
        bstack1lll_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    else:
        bstack1lll_opy_ = str () .join ([chr (ord (char) - bstack1lll111_opy_ - (bstack1ll1l1_opy_ + bstack1ll11l_opy_) % bstack11l1l1l_opy_) for bstack1ll1l1_opy_, char in enumerate (bstack111111_opy_)])
    return eval (bstack1lll_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1ll1l1l_opy_, bstack1l1llll111_opy_, get_host_info, bstack11l111l1l11_opy_, \
 bstack11l1lll1ll_opy_, bstack1111l1l11_opy_, error_handler, bstack111llll111l_opy_, bstack11l1l1l1l1_opy_
import bstack_utils.accessibility as bstack1l1l11l1l1_opy_
from bstack_utils.bstack11l1l11l11_opy_ import bstack1ll1l111_opy_
from bstack_utils.bstack111ll11111_opy_ import bstack11lllllll1_opy_
from bstack_utils.percy import bstack11ll1l1111_opy_
from bstack_utils.config import Config
bstack1l111111l1_opy_ = Config.bstack11l11lllll_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll1l1111_opy_()
@error_handler(class_method=False)
def bstack1llll1l11l11_opy_(bs_config, bstack1111l1l1l_opy_):
  try:
    data = {
        bstack1ll11ll_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭↚"): bstack1ll11ll_opy_ (u"ࠧ࡫ࡵࡲࡲࠬ↛"),
        bstack1ll11ll_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧ↜"): bs_config.get(bstack1ll11ll_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ↝"), bstack1ll11ll_opy_ (u"ࠪࠫ↞")),
        bstack1ll11ll_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ↟"): bs_config.get(bstack1ll11ll_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ↠"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll11ll_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ↡"): bs_config.get(bstack1ll11ll_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ↢")),
        bstack1ll11ll_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭↣"): bs_config.get(bstack1ll11ll_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ↤"), bstack1ll11ll_opy_ (u"ࠪࠫ↥")),
        bstack1ll11ll_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ↦"): bstack11l1l1l1l1_opy_(),
        bstack1ll11ll_opy_ (u"ࠬࡺࡡࡨࡵࠪ↧"): bstack11l111l1l11_opy_(bs_config),
        bstack1ll11ll_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩ↨"): get_host_info(),
        bstack1ll11ll_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ↩"): bstack1l1llll111_opy_(),
        bstack1ll11ll_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ↪"): os.environ.get(bstack1ll11ll_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ↫")),
        bstack1ll11ll_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ↬"): os.environ.get(bstack1ll11ll_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ↭"), False),
        bstack1ll11ll_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ↮"): bstack11ll1ll1l1l_opy_(),
        bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭↯"): bstack1llll11lll11_opy_(bs_config),
        bstack1ll11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫ↰"): bstack1llll11l1l1l_opy_(bstack1111l1l1l_opy_),
        bstack1ll11ll_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭↱"): bstack1llll11ll111_opy_(bs_config, bstack1111l1l1l_opy_.get(bstack1ll11ll_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ↲"), bstack1ll11ll_opy_ (u"ࠪࠫ↳"))),
        bstack1ll11ll_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭↴"): bstack11l1lll1ll_opy_(bs_config),
        bstack1ll11ll_opy_ (u"ࠬࡺࡥࡴࡶࡢࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪ↵"): bstack1llll111llll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll11ll_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ↶").format(str(error)))
    return None
def bstack1llll11l1l1l_opy_(framework):
  return {
    bstack1ll11ll_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ↷"): framework.get(bstack1ll11ll_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ↸"), bstack1ll11ll_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ↹")),
    bstack1ll11ll_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭↺"): framework.get(bstack1ll11ll_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ↻")),
    bstack1ll11ll_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ↼"): framework.get(bstack1ll11ll_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ↽")),
    bstack1ll11ll_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ↾"): bstack1ll11ll_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ↿"),
    bstack1ll11ll_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⇀"): framework.get(bstack1ll11ll_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⇁"))
  }
def bstack1llll111llll_opy_(bs_config):
  bstack1ll11ll_opy_ (u"ࠦࠧࠨࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡳࡵࡣࡵࡸ࠳ࠐࠠࠡࠤࠥࠦ⇂")
  if not bs_config:
    return {}
  bstack1111l1ll1l1_opy_ = bstack1ll1l111_opy_(bs_config).bstack1111lll11l1_opy_(bs_config)
  return bstack1111l1ll1l1_opy_
def bstack111lll11l_opy_(bs_config, framework):
  bstack1111l1ll_opy_ = False
  bstack111l11ll_opy_ = False
  bstack1llll11ll1ll_opy_ = False
  if bstack1ll11ll_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⇃") in bs_config:
    bstack1llll11ll1ll_opy_ = True
  elif bstack1ll11ll_opy_ (u"࠭ࡡࡱࡲࠪ⇄") in bs_config:
    bstack1111l1ll_opy_ = True
  else:
    bstack111l11ll_opy_ = True
  bstack1l1l1111l_opy_ = {
    bstack1ll11ll_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⇅"): bstack11lllllll1_opy_.bstack1llll11ll11l_opy_(bs_config, framework),
    bstack1ll11ll_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⇆"): bstack1l1l11l1l1_opy_.bstack1ll1l11lll_opy_(bs_config),
    bstack1ll11ll_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⇇"): bs_config.get(bstack1ll11ll_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⇈"), False),
    bstack1ll11ll_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⇉"): bstack111l11ll_opy_,
    bstack1ll11ll_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⇊"): bstack1111l1ll_opy_,
    bstack1ll11ll_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⇋"): bstack1llll11ll1ll_opy_
  }
  return bstack1l1l1111l_opy_
@error_handler(class_method=False)
def bstack1llll11lll11_opy_(bs_config):
  try:
    bstack1llll11l1111_opy_ = json.loads(os.getenv(bstack1ll11ll_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⇌"), bstack1ll11ll_opy_ (u"ࠨࡽࢀࠫ⇍")))
    bstack1llll11l1111_opy_ = bstack1llll11l111l_opy_(bs_config, bstack1llll11l1111_opy_)
    return {
        bstack1ll11ll_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ⇎"): bstack1llll11l1111_opy_
    }
  except Exception as error:
    logger.error(bstack1ll11ll_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⇏").format(str(error)))
    return {}
def bstack1llll11l111l_opy_(bs_config, bstack1llll11l1111_opy_):
  if ((bstack1ll11ll_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⇐") in bs_config or not bstack11l1lll1ll_opy_(bs_config)) and bstack1l1l11l1l1_opy_.bstack1ll1l11lll_opy_(bs_config)):
    bstack1llll11l1111_opy_[bstack1ll11ll_opy_ (u"ࠧ࡯࡮ࡤ࡮ࡸࡨࡪࡋ࡮ࡤࡱࡧࡩࡩࡋࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠣ⇑")] = True
  return bstack1llll11l1111_opy_
def bstack1llll1ll1l1l_opy_(array, bstack1llll11l11l1_opy_, bstack1llll11l1ll1_opy_):
  result = {}
  for o in array:
    key = o[bstack1llll11l11l1_opy_]
    result[key] = o[bstack1llll11l1ll1_opy_]
  return result
def bstack1llll1l11lll_opy_(bstack1ll1l11ll1_opy_=bstack1ll11ll_opy_ (u"࠭ࠧ⇒")):
  bstack1llll11l1lll_opy_ = bstack1l1l11l1l1_opy_.on()
  bstack1llll11l11ll_opy_ = bstack11lllllll1_opy_.on()
  bstack1llll11ll1l1_opy_ = percy.bstack11ll1ll1l_opy_()
  if bstack1llll11ll1l1_opy_ and not bstack1llll11l11ll_opy_ and not bstack1llll11l1lll_opy_:
    return bstack1ll1l11ll1_opy_ not in [bstack1ll11ll_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⇓"), bstack1ll11ll_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⇔")]
  elif bstack1llll11l1lll_opy_ and not bstack1llll11l11ll_opy_:
    return bstack1ll1l11ll1_opy_ not in [bstack1ll11ll_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⇕"), bstack1ll11ll_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⇖"), bstack1ll11ll_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⇗")]
  return bstack1llll11l1lll_opy_ or bstack1llll11l11ll_opy_ or bstack1llll11ll1l1_opy_
@error_handler(class_method=False)
def bstack1llll1l1111l_opy_(bstack1ll1l11ll1_opy_, test=None):
  bstack1llll11l1l11_opy_ = bstack1l1l11l1l1_opy_.on()
  if not bstack1llll11l1l11_opy_ or bstack1ll1l11ll1_opy_ not in [bstack1ll11ll_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⇘")] or test == None:
    return None
  return {
    bstack1ll11ll_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⇙"): bstack1llll11l1l11_opy_ and bstack1111l1l11_opy_(threading.current_thread(), bstack1ll11ll_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⇚"), None) == True and bstack1l1l11l1l1_opy_.bstack1l1l1l11ll_opy_(test[bstack1ll11ll_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⇛")])
  }
def bstack1llll11ll111_opy_(bs_config, framework):
  bstack1111l1ll_opy_ = False
  bstack111l11ll_opy_ = False
  bstack1llll11ll1ll_opy_ = False
  if bstack1ll11ll_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⇜") in bs_config:
    bstack1llll11ll1ll_opy_ = True
  elif bstack1ll11ll_opy_ (u"ࠪࡥࡵࡶࠧ⇝") in bs_config:
    bstack1111l1ll_opy_ = True
  else:
    bstack111l11ll_opy_ = True
  bstack1l1l1111l_opy_ = {
    bstack1ll11ll_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⇞"): bstack11lllllll1_opy_.bstack1llll11ll11l_opy_(bs_config, framework),
    bstack1ll11ll_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⇟"): bstack1l1l11l1l1_opy_.bstack1llllll1ll_opy_(bs_config),
    bstack1ll11ll_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⇠"): bs_config.get(bstack1ll11ll_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⇡"), False),
    bstack1ll11ll_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⇢"): bstack111l11ll_opy_,
    bstack1ll11ll_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⇣"): bstack1111l1ll_opy_,
    bstack1ll11ll_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⇤"): bstack1llll11ll1ll_opy_
  }
  return bstack1l1l1111l_opy_