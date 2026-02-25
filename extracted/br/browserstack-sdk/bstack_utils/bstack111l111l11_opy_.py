# coding: UTF-8
import sys
bstack1_opy_ = sys.version_info [0] == 2
bstack11ll1l_opy_ = 2048
bstack1lllllll_opy_ = 7
def bstack11l1l11_opy_ (bstack11lllll_opy_):
    global bstack111l1ll_opy_
    bstack111111l_opy_ = ord (bstack11lllll_opy_ [-1])
    bstack1llllll_opy_ = bstack11lllll_opy_ [:-1]
    bstack11ll1ll_opy_ = bstack111111l_opy_ % len (bstack1llllll_opy_)
    bstack1l11l_opy_ = bstack1llllll_opy_ [:bstack11ll1ll_opy_] + bstack1llllll_opy_ [bstack11ll1ll_opy_:]
    if bstack1_opy_:
        bstack1lll11_opy_ = unicode () .join ([unichr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    else:
        bstack1lll11_opy_ = str () .join ([chr (ord (char) - bstack11ll1l_opy_ - (bstack1lll1_opy_ + bstack111111l_opy_) % bstack1lllllll_opy_) for bstack1lll1_opy_, char in enumerate (bstack1l11l_opy_)])
    return eval (bstack1lll11_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l11ll11ll_opy_, bstack1l111l1lll_opy_, get_host_info, bstack111l1l1ll11_opy_, \
 bstack1lll1l1l_opy_, bstack11llll11l1_opy_, error_handler, bstack111l1l11ll1_opy_, current_time
import bstack_utils.accessibility as bstack1l111ll111_opy_
from bstack_utils.bstack11ll11l1l_opy_ import bstack1l1l11l11l_opy_
from bstack_utils.bstack1111lll11l_opy_ import bstack1l111111_opy_
from bstack_utils.percy import bstack11l1llll1_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack11l1llll1_opy_()
@error_handler(class_method=False)
def bstack1lll1111l1l1_opy_(bs_config, bstack11l1l11l1_opy_):
  try:
    data = {
        bstack11l1l11_opy_ (u"࠭ࡦࡰࡴࡰࡥࡹ࠭␬"): bstack11l1l11_opy_ (u"ࠧ࡫ࡵࡲࡲࠬ␭"),
        bstack11l1l11_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡡࡱࡥࡲ࡫ࠧ␮"): bs_config.get(bstack11l1l11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡑࡥࡲ࡫ࠧ␯"), bstack11l1l11_opy_ (u"ࠪࠫ␰")),
        bstack11l1l11_opy_ (u"ࠫࡳࡧ࡭ࡦࠩ␱"): bs_config.get(bstack11l1l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡒࡦࡳࡥࠨ␲"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l1l11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ␳"): bs_config.get(bstack11l1l11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡏࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ␴")),
        bstack11l1l11_opy_ (u"ࠨࡦࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭␵"): bs_config.get(bstack11l1l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡅࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ␶"), bstack11l1l11_opy_ (u"ࠪࠫ␷")),
        bstack11l1l11_opy_ (u"ࠫࡸࡺࡡࡳࡶࡨࡨࡤࡧࡴࠨ␸"): current_time(),
        bstack11l1l11_opy_ (u"ࠬࡺࡡࡨࡵࠪ␹"): bstack111l1l1ll11_opy_(bs_config),
        bstack11l1l11_opy_ (u"࠭ࡨࡰࡵࡷࡣ࡮ࡴࡦࡰࠩ␺"): get_host_info(),
        bstack11l1l11_opy_ (u"ࠧࡤ࡫ࡢ࡭ࡳ࡬࡯ࠨ␻"): bstack1l111l1lll_opy_(),
        bstack11l1l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡳࡷࡱࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ␼"): os.environ.get(bstack11l1l11_opy_ (u"ࠩࡅࡖࡔ࡝ࡓࡆࡔࡖࡘࡆࡉࡋࡠࡄࡘࡍࡑࡊ࡟ࡓࡗࡑࡣࡎࡊࡅࡏࡖࡌࡊࡎࡋࡒࠨ␽")),
        bstack11l1l11_opy_ (u"ࠪࡪࡦ࡯࡬ࡦࡦࡢࡸࡪࡹࡴࡴࡡࡵࡩࡷࡻ࡮ࠨ␾"): os.environ.get(bstack11l1l11_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡖࡊࡘࡕࡏࠩ␿"), False),
        bstack11l1l11_opy_ (u"ࠬࡼࡥࡳࡵ࡬ࡳࡳࡥࡣࡰࡰࡷࡶࡴࡲࠧ⑀"): bstack11l11ll11ll_opy_(),
        bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⑁"): bstack1ll1lllll1ll_opy_(bs_config),
        bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡨࡪࡺࡡࡪ࡮ࡶࠫ⑂"): bstack1ll1lllllll1_opy_(bstack11l1l11l1_opy_),
        bstack11l1l11_opy_ (u"ࠨࡲࡵࡳࡩࡻࡣࡵࡡࡰࡥࡵ࠭⑃"): bstack1lll11111111_opy_(bs_config, bstack11l1l11l1_opy_.get(bstack11l1l11_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡻࡳࡦࡦࠪ⑄"), bstack11l1l11_opy_ (u"ࠪࠫ⑅"))),
        bstack11l1l11_opy_ (u"ࠫࡧࡸ࡯ࡸࡵࡨࡶࡸࡺࡡࡤ࡭ࡄࡹࡹࡵ࡭ࡢࡶ࡬ࡳࡳ࠭⑆"): bstack1lll1l1l_opy_(bs_config),
        bstack11l1l11_opy_ (u"ࠬࡺࡥࡴࡶࡢࡳࡷࡩࡨࡦࡵࡷࡶࡦࡺࡩࡰࡰࠪ⑇"): bstack1ll1llll11ll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack11l1l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⑈").format(str(error)))
    return None
def bstack1ll1lllllll1_opy_(framework):
  return {
    bstack11l1l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ⑉"): framework.get(bstack11l1l11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ⑊"), bstack11l1l11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⑋")),
    bstack11l1l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⑌"): framework.get(bstack11l1l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⑍")),
    bstack11l1l11_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⑎"): framework.get(bstack11l1l11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⑏")),
    bstack11l1l11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ⑐"): bstack11l1l11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⑑"),
    bstack11l1l11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⑒"): framework.get(bstack11l1l11_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⑓"))
  }
def bstack1ll1llll11ll_opy_(bs_config):
  bstack11l1l11_opy_ (u"ࠦࠧࠨࠊࠡࠢࡕࡩࡹࡻࡲ࡯ࡵࠣࡸ࡭࡫ࠠࡵࡧࡶࡸࠥࡵࡲࡤࡪࡨࡷࡹࡸࡡࡵ࡫ࡲࡲࠥࡪࡡࡵࡣࠣࡪࡴࡸࠠࡣࡷ࡬ࡰࡩࠦࡳࡵࡣࡵࡸ࠳ࠐࠠࠡࠤࠥࠦ⑔")
  if not bs_config:
    return {}
  bstack1lllll1l111l_opy_ = bstack1l1l11l11l_opy_(bs_config).bstack1lllll1ll111_opy_(bs_config)
  return bstack1lllll1l111l_opy_
def bstack1l111l111_opy_(bs_config, framework):
  bstack111lll11l1_opy_ = False
  bstack111111ll_opy_ = False
  bstack1ll1llll1lll_opy_ = False
  if bstack11l1l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⑕") in bs_config:
    bstack1ll1llll1lll_opy_ = True
  elif bstack11l1l11_opy_ (u"࠭ࡡࡱࡲࠪ⑖") in bs_config:
    bstack111lll11l1_opy_ = True
  else:
    bstack111111ll_opy_ = True
  bstack1llll111l_opy_ = {
    bstack11l1l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⑗"): bstack1l111111_opy_.bstack1ll1lllll1l1_opy_(bs_config, framework),
    bstack11l1l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⑘"): bstack1l111ll111_opy_.bstack111l1ll1l_opy_(bs_config),
    bstack11l1l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⑙"): bs_config.get(bstack11l1l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⑚"), False),
    bstack11l1l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⑛"): bstack111111ll_opy_,
    bstack11l1l11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⑜"): bstack111lll11l1_opy_,
    bstack11l1l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⑝"): bstack1ll1llll1lll_opy_
  }
  return bstack1llll111l_opy_
@error_handler(class_method=False)
def bstack1ll1lllll1ll_opy_(bs_config):
  try:
    bstack1ll1llll1l1l_opy_ = json.loads(os.getenv(bstack11l1l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⑞"), bstack11l1l11_opy_ (u"ࠨࡽࢀࠫ⑟")))
    bstack1ll1llll1l1l_opy_ = bstack1ll1llllll1l_opy_(bs_config, bstack1ll1llll1l1l_opy_)
    return {
        bstack11l1l11_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶࠫ①"): bstack1ll1llll1l1l_opy_
    }
  except Exception as error:
    logger.error(bstack11l1l11_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ②").format(str(error)))
    return {}
def bstack1ll1llllll1l_opy_(bs_config, bstack1ll1llll1l1l_opy_):
  if ((bstack11l1l11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ③") in bs_config or not bstack1lll1l1l_opy_(bs_config)) and bstack1l111ll111_opy_.bstack111l1ll1l_opy_(bs_config)):
    bstack1ll1llll1l1l_opy_[bstack11l1l11_opy_ (u"ࠧ࡯࡮ࡤ࡮ࡸࡨࡪࡋ࡮ࡤࡱࡧࡩࡩࡋࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠣ④")] = True
  return bstack1ll1llll1l1l_opy_
def bstack1lll111111l1_opy_(array, bstack1ll1llllllll_opy_, bstack1ll1lllll111_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1llllllll_opy_]
    result[key] = o[bstack1ll1lllll111_opy_]
  return result
def bstack1lll111ll1l1_opy_(bstack1l11l11l_opy_=bstack11l1l11_opy_ (u"࠭ࠧ⑤")):
  bstack1ll1llll1ll1_opy_ = bstack1l111ll111_opy_.on()
  bstack1ll1llll1l11_opy_ = bstack1l111111_opy_.on()
  bstack1ll1llllll11_opy_ = percy.bstack1l1111ll11_opy_()
  if bstack1ll1llllll11_opy_ and not bstack1ll1llll1l11_opy_ and not bstack1ll1llll1ll1_opy_:
    return bstack1l11l11l_opy_ not in [bstack11l1l11_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⑥"), bstack11l1l11_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⑦")]
  elif bstack1ll1llll1ll1_opy_ and not bstack1ll1llll1l11_opy_:
    return bstack1l11l11l_opy_ not in [bstack11l1l11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⑧"), bstack11l1l11_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⑨"), bstack11l1l11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⑩")]
  return bstack1ll1llll1ll1_opy_ or bstack1ll1llll1l11_opy_ or bstack1ll1llllll11_opy_
@error_handler(class_method=False)
def bstack1lll1111l1ll_opy_(bstack1l11l11l_opy_, test=None):
  bstack1ll1lllll11l_opy_ = bstack1l111ll111_opy_.on()
  if not bstack1ll1lllll11l_opy_ or bstack1l11l11l_opy_ not in [bstack11l1l11_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⑪")] or test == None:
    return None
  return {
    bstack11l1l11_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⑫"): bstack1ll1lllll11l_opy_ and bstack11llll11l1_opy_(threading.current_thread(), bstack11l1l11_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ࠭⑬"), None) == True and bstack1l111ll111_opy_.bstack11ll1lll1l_opy_(test[bstack11l1l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭⑭")])
  }
def bstack1lll11111111_opy_(bs_config, framework):
  bstack111lll11l1_opy_ = False
  bstack111111ll_opy_ = False
  bstack1ll1llll1lll_opy_ = False
  if bstack11l1l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⑮") in bs_config:
    bstack1ll1llll1lll_opy_ = True
  elif bstack11l1l11_opy_ (u"ࠪࡥࡵࡶࠧ⑯") in bs_config:
    bstack111lll11l1_opy_ = True
  else:
    bstack111111ll_opy_ = True
  bstack1llll111l_opy_ = {
    bstack11l1l11_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⑰"): bstack1l111111_opy_.bstack1ll1lllll1l1_opy_(bs_config, framework),
    bstack11l1l11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⑱"): bstack1l111ll111_opy_.bstack11l1ll1ll1_opy_(bs_config),
    bstack11l1l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⑲"): bs_config.get(bstack11l1l11_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⑳"), False),
    bstack11l1l11_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⑴"): bstack111111ll_opy_,
    bstack11l1l11_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⑵"): bstack111lll11l1_opy_,
    bstack11l1l11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⑶"): bstack1ll1llll1lll_opy_
  }
  return bstack1llll111l_opy_