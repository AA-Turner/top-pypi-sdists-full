# coding: UTF-8
import sys
bstack1lll1l1_opy_ = sys.version_info [0] == 2
bstack1lll11_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll111_opy_ (bstack1l1l1l1_opy_):
    global bstack1l11ll1_opy_
    bstack1l1l11_opy_ = ord (bstack1l1l1l1_opy_ [-1])
    bstack11l11l1_opy_ = bstack1l1l1l1_opy_ [:-1]
    bstack1ll1l1l_opy_ = bstack1l1l11_opy_ % len (bstack11l11l1_opy_)
    bstack1l1ll1l_opy_ = bstack11l11l1_opy_ [:bstack1ll1l1l_opy_] + bstack11l11l1_opy_ [bstack1ll1l1l_opy_:]
    if bstack1lll1l1_opy_:
        bstack11l1ll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    else:
        bstack11l1ll1_opy_ = str () .join ([chr (ord (char) - bstack1lll11_opy_ - (bstack11llll1_opy_ + bstack1l1l11_opy_) % bstack1ll11_opy_) for bstack11llll1_opy_, char in enumerate (bstack1l1ll1l_opy_)])
    return eval (bstack11l1ll1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l11ll1111_opy_, bstack1llll111_opy_, get_host_info, bstack111l1llll1l_opy_, \
 bstack11l1llllll_opy_, bstack1lll11l111_opy_, error_handler, bstack111l111l1ll_opy_, current_time
import bstack_utils.accessibility as bstack11l11l11ll_opy_
from bstack_utils.bstack1lllll111l_opy_ import bstack1111lll11_opy_
from bstack_utils.bstack1111ll1l1l_opy_ import bstack11lll1ll1_opy_
from bstack_utils.percy import bstack1ll1111l_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1ll1111l_opy_()
@error_handler(class_method=False)
def bstack1lll1111ll11_opy_(bs_config, bstack1lllll11ll_opy_):
  try:
    data = {
        bstack11ll111_opy_ (u"ࠪࡪࡴࡸ࡭ࡢࡶࠪ␩"): bstack11ll111_opy_ (u"ࠫ࡯ࡹ࡯࡯ࠩ␪"),
        bstack11ll111_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡥ࡮ࡢ࡯ࡨࠫ␫"): bs_config.get(bstack11ll111_opy_ (u"࠭ࡰࡳࡱ࡭ࡩࡨࡺࡎࡢ࡯ࡨࠫ␬"), bstack11ll111_opy_ (u"ࠧࠨ␭")),
        bstack11ll111_opy_ (u"ࠨࡰࡤࡱࡪ࠭␮"): bs_config.get(bstack11ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡏࡣࡰࡩࠬ␯"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡ࡬ࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭␰"): bs_config.get(bstack11ll111_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡌࡨࡪࡴࡴࡪࡨ࡬ࡩࡷ࠭␱")),
        bstack11ll111_opy_ (u"ࠬࡪࡥࡴࡥࡵ࡭ࡵࡺࡩࡰࡰࠪ␲"): bs_config.get(bstack11ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡉ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ␳"), bstack11ll111_opy_ (u"ࠧࠨ␴")),
        bstack11ll111_opy_ (u"ࠨࡵࡷࡥࡷࡺࡥࡥࡡࡤࡸࠬ␵"): current_time(),
        bstack11ll111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ␶"): bstack111l1llll1l_opy_(bs_config),
        bstack11ll111_opy_ (u"ࠪ࡬ࡴࡹࡴࡠ࡫ࡱࡪࡴ࠭␷"): get_host_info(),
        bstack11ll111_opy_ (u"ࠫࡨ࡯࡟ࡪࡰࡩࡳࠬ␸"): bstack1llll111_opy_(),
        bstack11ll111_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣࡷࡻ࡮ࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ␹"): os.environ.get(bstack11ll111_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡈࡕࡊࡎࡇࡣࡗ࡛ࡎࡠࡋࡇࡉࡓ࡚ࡉࡇࡋࡈࡖࠬ␺")),
        bstack11ll111_opy_ (u"ࠧࡧࡣ࡬ࡰࡪࡪ࡟ࡵࡧࡶࡸࡸࡥࡲࡦࡴࡸࡲࠬ␻"): os.environ.get(bstack11ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡓࡇࡕ࡙ࡓ࠭␼"), False),
        bstack11ll111_opy_ (u"ࠩࡹࡩࡷࡹࡩࡰࡰࡢࡧࡴࡴࡴࡳࡱ࡯ࠫ␽"): bstack11l11ll1111_opy_(),
        bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ␾"): bstack1ll1llll1ll1_opy_(bs_config),
        bstack11ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡥࡧࡷࡥ࡮ࡲࡳࠨ␿"): bstack1ll1llll1l11_opy_(bstack1lllll11ll_opy_),
        bstack11ll111_opy_ (u"ࠬࡶࡲࡰࡦࡸࡧࡹࡥ࡭ࡢࡲࠪ⑀"): bstack1ll1llll11l1_opy_(bs_config, bstack1lllll11ll_opy_.get(bstack11ll111_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡸࡷࡪࡪࠧ⑁"), bstack11ll111_opy_ (u"ࠧࠨ⑂"))),
        bstack11ll111_opy_ (u"ࠨࡤࡵࡳࡼࡹࡥࡳࡵࡷࡥࡨࡱࡁࡶࡶࡲࡱࡦࡺࡩࡰࡰࠪ⑃"): bstack11l1llllll_opy_(bs_config),
        bstack11ll111_opy_ (u"ࠩࡷࡩࡸࡺ࡟ࡰࡴࡦ࡬ࡪࡹࡴࡳࡣࡷ࡭ࡴࡴࠧ⑄"): bstack1ll1llllllll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack11ll111_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡱࡣࡼࡰࡴࡧࡤࠡࡨࡲࡶ࡚ࠥࡥࡴࡶࡋࡹࡧࡀࠠࠡࡽࢀࠦ⑅").format(str(error)))
    return None
def bstack1ll1llll1l11_opy_(framework):
  return {
    bstack11ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡎࡢ࡯ࡨࠫ⑆"): framework.get(bstack11ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡰࡤࡱࡪ࠭⑇"), bstack11ll111_opy_ (u"࠭ࡐࡺࡶࡨࡷࡹ࠭⑈")),
    bstack11ll111_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ⑉"): framework.get(bstack11ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⑊")),
    bstack11ll111_opy_ (u"ࠩࡶࡨࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⑋"): framework.get(bstack11ll111_opy_ (u"ࠪࡷࡩࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⑌")),
    bstack11ll111_opy_ (u"ࠫࡱࡧ࡮ࡨࡷࡤ࡫ࡪ࠭⑍"): bstack11ll111_opy_ (u"ࠬࡶࡹࡵࡪࡲࡲࠬ⑎"),
    bstack11ll111_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⑏"): framework.get(bstack11ll111_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱࠧ⑐"))
  }
def bstack1ll1llllllll_opy_(bs_config):
  bstack11ll111_opy_ (u"ࠣࠤࠥࠎࠥࠦࡒࡦࡶࡸࡶࡳࡹࠠࡵࡪࡨࠤࡹ࡫ࡳࡵࠢࡲࡶࡨ࡮ࡥࡴࡶࡵࡥࡹ࡯࡯࡯ࠢࡧࡥࡹࡧࠠࡧࡱࡵࠤࡧࡻࡩ࡭ࡦࠣࡷࡹࡧࡲࡵ࠰ࠍࠤࠥࠨࠢࠣ⑑")
  if not bs_config:
    return {}
  bstack1llllll1ll1l_opy_ = bstack1111lll11_opy_(bs_config).bstack11111111111_opy_(bs_config)
  return bstack1llllll1ll1l_opy_
def bstack1l1ll1lll_opy_(bs_config, framework):
  bstack11lllll11l_opy_ = False
  bstack1l1l1lllll_opy_ = False
  bstack1ll1llllll11_opy_ = False
  if bstack11ll111_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⑒") in bs_config:
    bstack1ll1llllll11_opy_ = True
  elif bstack11ll111_opy_ (u"ࠪࡥࡵࡶࠧ⑓") in bs_config:
    bstack11lllll11l_opy_ = True
  else:
    bstack1l1l1lllll_opy_ = True
  bstack1l11l1l1ll_opy_ = {
    bstack11ll111_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⑔"): bstack11lll1ll1_opy_.bstack1ll1lllll1l1_opy_(bs_config, framework),
    bstack11ll111_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⑕"): bstack11l11l11ll_opy_.bstack1ll1ll1111_opy_(bs_config),
    bstack11ll111_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⑖"): bs_config.get(bstack11ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⑗"), False),
    bstack11ll111_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⑘"): bstack1l1l1lllll_opy_,
    bstack11ll111_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⑙"): bstack11lllll11l_opy_,
    bstack11ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⑚"): bstack1ll1llllll11_opy_
  }
  return bstack1l11l1l1ll_opy_
@error_handler(class_method=False)
def bstack1ll1llll1ll1_opy_(bs_config):
  try:
    bstack1ll1lllll11l_opy_ = json.loads(os.getenv(bstack11ll111_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⑛"), bstack11ll111_opy_ (u"ࠬࢁࡽࠨ⑜")))
    bstack1ll1lllll11l_opy_ = bstack1ll1llll1lll_opy_(bs_config, bstack1ll1lllll11l_opy_)
    return {
        bstack11ll111_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ⑝"): bstack1ll1lllll11l_opy_
    }
  except Exception as error:
    logger.error(bstack11ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⑞").format(str(error)))
    return {}
def bstack1ll1llll1lll_opy_(bs_config, bstack1ll1lllll11l_opy_):
  if ((bstack11ll111_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⑟") in bs_config or not bstack11l1llllll_opy_(bs_config)) and bstack11l11l11ll_opy_.bstack1ll1ll1111_opy_(bs_config)):
    bstack1ll1lllll11l_opy_[bstack11ll111_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧ①")] = True
  return bstack1ll1lllll11l_opy_
def bstack1lll1111ll1l_opy_(array, bstack1ll1llllll1l_opy_, bstack1ll1llll1l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1llllll1l_opy_]
    result[key] = o[bstack1ll1llll1l1l_opy_]
  return result
def bstack1lll11111111_opy_(bstack11l1l1llll_opy_=bstack11ll111_opy_ (u"ࠪࠫ②")):
  bstack1ll1lllllll1_opy_ = bstack11l11l11ll_opy_.on()
  bstack1ll1lllll111_opy_ = bstack11lll1ll1_opy_.on()
  bstack1ll1llll11ll_opy_ = percy.bstack1lll11ll1l_opy_()
  if bstack1ll1llll11ll_opy_ and not bstack1ll1lllll111_opy_ and not bstack1ll1lllllll1_opy_:
    return bstack11l1l1llll_opy_ not in [bstack11ll111_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ③"), bstack11ll111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ④")]
  elif bstack1ll1lllllll1_opy_ and not bstack1ll1lllll111_opy_:
    return bstack11l1l1llll_opy_ not in [bstack11ll111_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ⑤"), bstack11ll111_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ⑥"), bstack11ll111_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⑦")]
  return bstack1ll1lllllll1_opy_ or bstack1ll1lllll111_opy_ or bstack1ll1llll11ll_opy_
@error_handler(class_method=False)
def bstack1lll1111lll1_opy_(bstack11l1l1llll_opy_, test=None):
  bstack1ll1lllll1ll_opy_ = bstack11l11l11ll_opy_.on()
  if not bstack1ll1lllll1ll_opy_ or bstack11l1l1llll_opy_ not in [bstack11ll111_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⑧")] or test == None:
    return None
  return {
    bstack11ll111_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ⑨"): bstack1ll1lllll1ll_opy_ and bstack1lll11l111_opy_(threading.current_thread(), bstack11ll111_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ⑩"), None) == True and bstack11l11l11ll_opy_.bstack1l11ll1111_opy_(test[bstack11ll111_opy_ (u"ࠬࡺࡡࡨࡵࠪ⑪")])
  }
def bstack1ll1llll11l1_opy_(bs_config, framework):
  bstack11lllll11l_opy_ = False
  bstack1l1l1lllll_opy_ = False
  bstack1ll1llllll11_opy_ = False
  if bstack11ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⑫") in bs_config:
    bstack1ll1llllll11_opy_ = True
  elif bstack11ll111_opy_ (u"ࠧࡢࡲࡳࠫ⑬") in bs_config:
    bstack11lllll11l_opy_ = True
  else:
    bstack1l1l1lllll_opy_ = True
  bstack1l11l1l1ll_opy_ = {
    bstack11ll111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⑭"): bstack11lll1ll1_opy_.bstack1ll1lllll1l1_opy_(bs_config, framework),
    bstack11ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⑮"): bstack11l11l11ll_opy_.bstack1l1lll11_opy_(bs_config),
    bstack11ll111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⑯"): bs_config.get(bstack11ll111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⑰"), False),
    bstack11ll111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⑱"): bstack1l1l1lllll_opy_,
    bstack11ll111_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⑲"): bstack11lllll11l_opy_,
    bstack11ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⑳"): bstack1ll1llllll11_opy_
  }
  return bstack1l11l1l1ll_opy_