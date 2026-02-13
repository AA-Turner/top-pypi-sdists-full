# coding: UTF-8
import sys
bstack111ll11_opy_ = sys.version_info [0] == 2
bstack1l1l1l_opy_ = 2048
bstack1111ll1_opy_ = 7
def bstack11l11_opy_ (bstack1lll1ll_opy_):
    global bstack11l11l_opy_
    bstack11111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1l11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack11111l1_opy_ = bstack11111l_opy_ % len (bstack1l11_opy_)
    bstack1lll1l_opy_ = bstack1l11_opy_ [:bstack11111l1_opy_] + bstack1l11_opy_ [bstack11111l1_opy_:]
    if bstack111ll11_opy_:
        bstack1l1l1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    else:
        bstack1l1l1_opy_ = str () .join ([chr (ord (char) - bstack1l1l1l_opy_ - (bstack1l1111l_opy_ + bstack11111l_opy_) % bstack1111ll1_opy_) for bstack1l1111l_opy_, char in enumerate (bstack1lll1l_opy_)])
    return eval (bstack1l1l1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l111ll1ll_opy_, bstack11l1lllll1_opy_, get_host_info, bstack111l1111ll1_opy_, \
 bstack1ll111l11_opy_, bstack11ll11l11_opy_, error_handler, bstack1111l111lll_opy_, bstack11l1lll11_opy_
import bstack_utils.accessibility as bstack1lllll111l_opy_
from bstack_utils.bstack1l11ll1l_opy_ import bstack1l11l1l1ll_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack11l1ll111l_opy_
from bstack_utils.percy import bstack11l11ll11_opy_
from bstack_utils.config import Config
bstack11l1l1111_opy_ = Config.bstack111l1lll_opy_()
logger = logging.getLogger(__name__)
percy = bstack11l11ll11_opy_()
@error_handler(class_method=False)
def bstack1lll1111111l_opy_(bs_config, bstack1l1l1l1l1l_opy_):
  try:
    data = {
        bstack11l11_opy_ (u"ࠩࡩࡳࡷࡳࡡࡵࠩ␡"): bstack11l11_opy_ (u"ࠪ࡮ࡸࡵ࡮ࠨ␢"),
        bstack11l11_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡤࡴࡡ࡮ࡧࠪ␣"): bs_config.get(bstack11l11_opy_ (u"ࠬࡶࡲࡰ࡬ࡨࡧࡹࡔࡡ࡮ࡧࠪ␤"), bstack11l11_opy_ (u"࠭ࠧ␥")),
        bstack11l11_opy_ (u"ࠧ࡯ࡣࡰࡩࠬ␦"): bs_config.get(bstack11l11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡎࡢ࡯ࡨࠫ␧"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11l11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠ࡫ࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ␨"): bs_config.get(bstack11l11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡋࡧࡩࡳࡺࡩࡧ࡫ࡨࡶࠬ␩")),
        bstack11l11_opy_ (u"ࠫࡩ࡫ࡳࡤࡴ࡬ࡴࡹ࡯࡯࡯ࠩ␪"): bs_config.get(bstack11l11_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡈࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ␫"), bstack11l11_opy_ (u"࠭ࠧ␬")),
        bstack11l11_opy_ (u"ࠧࡴࡶࡤࡶࡹ࡫ࡤࡠࡣࡷࠫ␭"): bstack11l1lll11_opy_(),
        bstack11l11_opy_ (u"ࠨࡶࡤ࡫ࡸ࠭␮"): bstack111l1111ll1_opy_(bs_config),
        bstack11l11_opy_ (u"ࠩ࡫ࡳࡸࡺ࡟ࡪࡰࡩࡳࠬ␯"): get_host_info(),
        bstack11l11_opy_ (u"ࠪࡧ࡮ࡥࡩ࡯ࡨࡲࠫ␰"): bstack11l1lllll1_opy_(),
        bstack11l11_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡢࡶࡺࡴ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ␱"): os.environ.get(bstack11l11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡇ࡛ࡉࡍࡆࡢࡖ࡚ࡔ࡟ࡊࡆࡈࡒ࡙ࡏࡆࡊࡇࡕࠫ␲")),
        bstack11l11_opy_ (u"࠭ࡦࡢ࡫࡯ࡩࡩࡥࡴࡦࡵࡷࡷࡤࡸࡥࡳࡷࡱࠫ␳"): os.environ.get(bstack11l11_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡒࡆࡔࡘࡒࠬ␴"), False),
        bstack11l11_opy_ (u"ࠨࡸࡨࡶࡸ࡯࡯࡯ࡡࡦࡳࡳࡺࡲࡰ࡮ࠪ␵"): bstack11l111ll1ll_opy_(),
        bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ␶"): bstack1ll1lll11lll_opy_(bs_config),
        bstack11l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡤࡦࡶࡤ࡭ࡱࡹࠧ␷"): bstack1ll1lll1ll1l_opy_(bstack1l1l1l1l1l_opy_),
        bstack11l11_opy_ (u"ࠫࡵࡸ࡯ࡥࡷࡦࡸࡤࡳࡡࡱࠩ␸"): bstack1ll1lll11ll1_opy_(bs_config, bstack1l1l1l1l1l_opy_.get(bstack11l11_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡷࡶࡩࡩ࠭␹"), bstack11l11_opy_ (u"࠭ࠧ␺"))),
        bstack11l11_opy_ (u"ࠧࡣࡴࡲࡻࡸ࡫ࡲࡴࡶࡤࡧࡰࡇࡵࡵࡱࡰࡥࡹ࡯࡯࡯ࠩ␻"): bstack1ll111l11_opy_(bs_config),
        bstack11l11_opy_ (u"ࠨࡶࡨࡷࡹࡥ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳ࠭␼"): bstack1ll1lll11l11_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack11l11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡰࡢࡻ࡯ࡳࡦࡪࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ␽").format(str(error)))
    return None
def bstack1ll1lll1ll1l_opy_(framework):
  return {
    bstack11l11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡔࡡ࡮ࡧࠪ␾"): framework.get(bstack11l11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟࡯ࡣࡰࡩࠬ␿"), bstack11l11_opy_ (u"ࠬࡖࡹࡵࡧࡶࡸࠬ⑀")),
    bstack11l11_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⑁"): framework.get(bstack11l11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⑂")),
    bstack11l11_opy_ (u"ࠨࡵࡧ࡯࡛࡫ࡲࡴ࡫ࡲࡲࠬ⑃"): framework.get(bstack11l11_opy_ (u"ࠩࡶࡨࡰࡥࡶࡦࡴࡶ࡭ࡴࡴࠧ⑄")),
    bstack11l11_opy_ (u"ࠪࡰࡦࡴࡧࡶࡣࡪࡩࠬ⑅"): bstack11l11_opy_ (u"ࠫࡵࡿࡴࡩࡱࡱࠫ⑆"),
    bstack11l11_opy_ (u"ࠬࡺࡥࡴࡶࡉࡶࡦࡳࡥࡸࡱࡵ࡯ࠬ⑇"): framework.get(bstack11l11_opy_ (u"࠭ࡴࡦࡵࡷࡊࡷࡧ࡭ࡦࡹࡲࡶࡰ࠭⑈"))
  }
def bstack1ll1lll11l11_opy_(bs_config):
  bstack11l11_opy_ (u"ࠢࠣࠤࠍࠤࠥࡘࡥࡵࡷࡵࡲࡸࠦࡴࡩࡧࠣࡸࡪࡹࡴࠡࡱࡵࡧ࡭࡫ࡳࡵࡴࡤࡸ࡮ࡵ࡮ࠡࡦࡤࡸࡦࠦࡦࡰࡴࠣࡦࡺ࡯࡬ࡥࠢࡶࡸࡦࡸࡴ࠯ࠌࠣࠤࠧࠨࠢ⑉")
  if not bs_config:
    return {}
  bstack1lllll1ll111_opy_ = bstack1l11l1l1ll_opy_(bs_config).bstack1llllll111ll_opy_(bs_config)
  return bstack1lllll1ll111_opy_
def bstack11l1ll11l_opy_(bs_config, framework):
  bstack11lll11l11_opy_ = False
  bstack1l1ll1l1l1_opy_ = False
  bstack1ll1lll1l11l_opy_ = False
  if bstack11l11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⑊") in bs_config:
    bstack1ll1lll1l11l_opy_ = True
  elif bstack11l11_opy_ (u"ࠩࡤࡴࡵ࠭⑋") in bs_config:
    bstack11lll11l11_opy_ = True
  else:
    bstack1l1ll1l1l1_opy_ = True
  bstack111ll1ll1l_opy_ = {
    bstack11l11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻࠪ⑌"): bstack11l1ll111l_opy_.bstack1ll1lll1llll_opy_(bs_config, framework),
    bstack11l11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⑍"): bstack1lllll111l_opy_.bstack1lll1l1l1_opy_(bs_config),
    bstack11l11_opy_ (u"ࠬࡶࡥࡳࡥࡼࠫ⑎"): bs_config.get(bstack11l11_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⑏"), False),
    bstack11l11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦࠩ⑐"): bstack1l1ll1l1l1_opy_,
    bstack11l11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⑑"): bstack11lll11l11_opy_,
    bstack11l11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ࠭⑒"): bstack1ll1lll1l11l_opy_
  }
  return bstack111ll1ll1l_opy_
@error_handler(class_method=False)
def bstack1ll1lll11lll_opy_(bs_config):
  try:
    bstack1ll1lll1l1l1_opy_ = json.loads(os.getenv(bstack11l11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡗࡉࡘ࡚࡟ࡂࡅࡆࡉࡘ࡙ࡉࡃࡋࡏࡍ࡙࡟࡟ࡄࡑࡑࡊࡎࡍࡕࡓࡃࡗࡍࡔࡔ࡟࡚ࡏࡏࠫ⑓"), bstack11l11_opy_ (u"ࠫࢀࢃࠧ⑔")))
    bstack1ll1lll1l1l1_opy_ = bstack1ll1lll1ll11_opy_(bs_config, bstack1ll1lll1l1l1_opy_)
    return {
        bstack11l11_opy_ (u"ࠬࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠧ⑕"): bstack1ll1lll1l1l1_opy_
    }
  except Exception as error:
    logger.error(bstack11l11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣ࡫ࡪࡺ࡟ࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿ࡟ࡴࡧࡷࡸ࡮ࡴࡧࡴࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⑖").format(str(error)))
    return {}
def bstack1ll1lll1ll11_opy_(bs_config, bstack1ll1lll1l1l1_opy_):
  if ((bstack11l11_opy_ (u"ࠧࡵࡷࡵࡦࡴ࡙ࡣࡢ࡮ࡨࠫ⑗") in bs_config or not bstack1ll111l11_opy_(bs_config)) and bstack1lllll111l_opy_.bstack1lll1l1l1_opy_(bs_config)):
    bstack1ll1lll1l1l1_opy_[bstack11l11_opy_ (u"ࠣ࡫ࡱࡧࡱࡻࡤࡦࡇࡱࡧࡴࡪࡥࡥࡇࡻࡸࡪࡴࡳࡪࡱࡱࠦ⑘")] = True
  return bstack1ll1lll1l1l1_opy_
def bstack1lll11111l1l_opy_(array, bstack1ll1lll111l1_opy_, bstack1ll1lll1l111_opy_):
  result = {}
  for o in array:
    key = o[bstack1ll1lll111l1_opy_]
    result[key] = o[bstack1ll1lll1l111_opy_]
  return result
def bstack1ll1llll111l_opy_(bstack1l1ll11111_opy_=bstack11l11_opy_ (u"ࠩࠪ⑙")):
  bstack1ll1lll1lll1_opy_ = bstack1lllll111l_opy_.on()
  bstack1ll1lll1l1ll_opy_ = bstack11l1ll111l_opy_.on()
  bstack1ll1lll111ll_opy_ = percy.bstack1l1l1l1111_opy_()
  if bstack1ll1lll111ll_opy_ and not bstack1ll1lll1l1ll_opy_ and not bstack1ll1lll1lll1_opy_:
    return bstack1l1ll11111_opy_ not in [bstack11l11_opy_ (u"ࠪࡇࡇ࡚ࡓࡦࡵࡶ࡭ࡴࡴࡃࡳࡧࡤࡸࡪࡪࠧ⑚"), bstack11l11_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⑛")]
  elif bstack1ll1lll1lll1_opy_ and not bstack1ll1lll1l1ll_opy_:
    return bstack1l1ll11111_opy_ not in [bstack11l11_opy_ (u"ࠬࡎ࡯ࡰ࡭ࡕࡹࡳ࡙ࡴࡢࡴࡷࡩࡩ࠭⑜"), bstack11l11_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⑝"), bstack11l11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⑞")]
  return bstack1ll1lll1lll1_opy_ or bstack1ll1lll1l1ll_opy_ or bstack1ll1lll111ll_opy_
@error_handler(class_method=False)
def bstack1ll1llll1ll1_opy_(bstack1l1ll11111_opy_, test=None):
  bstack1ll1lll11l1l_opy_ = bstack1lllll111l_opy_.on()
  if not bstack1ll1lll11l1l_opy_ or bstack1l1ll11111_opy_ not in [bstack11l11_opy_ (u"ࠨࡖࡨࡷࡹࡘࡵ࡯ࡈ࡬ࡲ࡮ࡹࡨࡦࡦࠪ⑟")] or test == None:
    return None
  return {
    bstack11l11_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ①"): bstack1ll1lll11l1l_opy_ and bstack11ll11l11_opy_(threading.current_thread(), bstack11l11_opy_ (u"ࠪࡥ࠶࠷ࡹࡑ࡮ࡤࡸ࡫ࡵࡲ࡮ࠩ②"), None) == True and bstack1lllll111l_opy_.bstack11l11l1lll_opy_(test[bstack11l11_opy_ (u"ࠫࡹࡧࡧࡴࠩ③")])
  }
def bstack1ll1lll11ll1_opy_(bs_config, framework):
  bstack11lll11l11_opy_ = False
  bstack1l1ll1l1l1_opy_ = False
  bstack1ll1lll1l11l_opy_ = False
  if bstack11l11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ④") in bs_config:
    bstack1ll1lll1l11l_opy_ = True
  elif bstack11l11_opy_ (u"࠭ࡡࡱࡲࠪ⑤") in bs_config:
    bstack11lll11l11_opy_ = True
  else:
    bstack1l1ll1l1l1_opy_ = True
  bstack111ll1ll1l_opy_ = {
    bstack11l11_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⑥"): bstack11l1ll111l_opy_.bstack1ll1lll1llll_opy_(bs_config, framework),
    bstack11l11_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⑦"): bstack1lllll111l_opy_.bstack1ll11l1l1l_opy_(bs_config),
    bstack11l11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⑧"): bs_config.get(bstack11l11_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⑨"), False),
    bstack11l11_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⑩"): bstack1l1ll1l1l1_opy_,
    bstack11l11_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⑪"): bstack11lll11l11_opy_,
    bstack11l11_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⑫"): bstack1ll1lll1l11l_opy_
  }
  return bstack111ll1ll1l_opy_