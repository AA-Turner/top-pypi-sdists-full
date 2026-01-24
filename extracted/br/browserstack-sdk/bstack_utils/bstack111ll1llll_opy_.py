# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1l11ll1_opy_ = 2048
bstack1l11l11_opy_ = 7
def bstack1l1111_opy_ (bstack11l11ll_opy_):
    global bstack111l1l1_opy_
    bstack111l1ll_opy_ = ord (bstack11l11ll_opy_ [-1])
    bstack1l1l1_opy_ = bstack11l11ll_opy_ [:-1]
    bstack111111_opy_ = bstack111l1ll_opy_ % len (bstack1l1l1_opy_)
    bstack1lllll1l_opy_ = bstack1l1l1_opy_ [:bstack111111_opy_] + bstack1l1l1_opy_ [bstack111111_opy_:]
    if bstack1l111l_opy_:
        bstack1lll1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    else:
        bstack1lll1l_opy_ = str () .join ([chr (ord (char) - bstack1l11ll1_opy_ - (bstack1ll1ll_opy_ + bstack111l1ll_opy_) % bstack1l11l11_opy_) for bstack1ll1ll_opy_, char in enumerate (bstack1lllll1l_opy_)])
    return eval (bstack1lll1l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11l1l11ll1l_opy_, bstack1l11ll1l1_opy_, get_host_info, bstack111l11111l1_opy_, \
 bstack1l111111l1_opy_, bstack111111lll_opy_, error_handler, bstack111ll11l111_opy_, bstack1111l11l1_opy_
import bstack_utils.accessibility as bstack1l11l1l111_opy_
from bstack_utils.bstack111l1111_opy_ import bstack1l1llll1l_opy_
from bstack_utils.bstack1111l1ll11_opy_ import bstack1lll11ll11_opy_
from bstack_utils.percy import bstack1l1l11l1ll_opy_
from bstack_utils.config import Config
bstack1llllll11l_opy_ = Config.bstack111ll1lll1_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1l11l1ll_opy_()
@error_handler(class_method=False)
def bstack1lll1l111l11_opy_(bs_config, bstack11ll111ll_opy_):
  try:
    data = {
        bstack1l1111_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧ⌱"): bstack1l1111_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭⌲"),
        bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨ⌳"): bs_config.get(bstack1l1111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ⌴"), bstack1l1111_opy_ (u"ࠫࠬ⌵")),
        bstack1l1111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ⌶"): bs_config.get(bstack1l1111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ⌷"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⌸"): bs_config.get(bstack1l1111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ⌹")),
        bstack1l1111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ⌺"): bs_config.get(bstack1l1111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭⌻"), bstack1l1111_opy_ (u"ࠫࠬ⌼")),
        bstack1l1111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ⌽"): bstack1111l11l1_opy_(),
        bstack1l1111_opy_ (u"࠭ࡴࡢࡩࡶࠫ⌾"): bstack111l11111l1_opy_(bs_config),
        bstack1l1111_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ⌿"): get_host_info(),
        bstack1l1111_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩ⍀"): bstack1l11ll1l1_opy_(),
        bstack1l1111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ⍁"): os.environ.get(bstack1l1111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ⍂")),
        bstack1l1111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩ⍃"): os.environ.get(bstack1l1111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ⍄"), False),
        bstack1l1111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨ⍅"): bstack11l1l11ll1l_opy_(),
        bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⍆"): bstack1lll11l1l1l1_opy_(bs_config),
        bstack1l1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬ⍇"): bstack1lll11l1ll11_opy_(bstack11ll111ll_opy_),
        bstack1l1111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ⍈"): bstack1lll11l11l1l_opy_(bs_config, bstack11ll111ll_opy_.get(bstack1l1111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ⍉"), bstack1l1111_opy_ (u"ࠫࠬ⍊"))),
        bstack1l1111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⍋"): bstack1l111111l1_opy_(bs_config),
        bstack1l1111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫ⍌"): bstack1lll11l111l1_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1l1111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ⍍").format(str(error)))
    return None
def bstack1lll11l1ll11_opy_(framework):
  return {
    bstack1l1111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ⍎"): framework.get(bstack1l1111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ⍏"), bstack1l1111_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⍐")),
    bstack1l1111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ⍑"): framework.get(bstack1l1111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⍒")),
    bstack1l1111_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ⍓"): framework.get(bstack1l1111_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⍔")),
    bstack1l1111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ⍕"): bstack1l1111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⍖"),
    bstack1l1111_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⍗"): framework.get(bstack1l1111_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⍘"))
  }
def bstack1lll11l111l1_opy_(bs_config):
  bstack1l1111_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡴࡶࡤࡶࡹ࠴ࠊࠡࠢࠥࠦࠧ⍙")
  if not bs_config:
    return {}
  bstack11111111lll_opy_ = bstack1l1llll1l_opy_(bs_config).bstack111111llll1_opy_(bs_config)
  return bstack11111111lll_opy_
def bstack1l11l11lll_opy_(bs_config, framework):
  bstack11ll1l1111_opy_ = False
  bstack1lll1ll1l_opy_ = False
  bstack1lll11l11l11_opy_ = False
  if bstack1l1111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ⍚") in bs_config:
    bstack1lll11l11l11_opy_ = True
  elif bstack1l1111_opy_ (u"ࠧࡢࡲࡳࠫ⍛") in bs_config:
    bstack11ll1l1111_opy_ = True
  else:
    bstack1lll1ll1l_opy_ = True
  bstack1l1111lll_opy_ = {
    bstack1l1111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ⍜"): bstack1lll11ll11_opy_.bstack1lll11l1lll1_opy_(bs_config, framework),
    bstack1l1111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ⍝"): bstack1l11l1l111_opy_.bstack111ll11l1l_opy_(bs_config),
    bstack1l1111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ⍞"): bs_config.get(bstack1l1111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ⍟"), False),
    bstack1l1111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ⍠"): bstack1lll1ll1l_opy_,
    bstack1l1111_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ⍡"): bstack11ll1l1111_opy_,
    bstack1l1111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ⍢"): bstack1lll11l11l11_opy_
  }
  return bstack1l1111lll_opy_
@error_handler(class_method=False)
def bstack1lll11l1l1l1_opy_(bs_config):
  try:
    bstack1lll11l11lll_opy_ = json.loads(os.getenv(bstack1l1111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ⍣"), bstack1l1111_opy_ (u"ࠩࡾࢁࠬ⍤")))
    bstack1lll11l11lll_opy_ = bstack1lll11l1llll_opy_(bs_config, bstack1lll11l11lll_opy_)
    return {
        bstack1l1111_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬ⍥"): bstack1lll11l11lll_opy_
    }
  except Exception as error:
    logger.error(bstack1l1111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ⍦").format(str(error)))
    return {}
def bstack1lll11l1llll_opy_(bs_config, bstack1lll11l11lll_opy_):
  if ((bstack1l1111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⍧") in bs_config or not bstack1l111111l1_opy_(bs_config)) and bstack1l11l1l111_opy_.bstack111ll11l1l_opy_(bs_config)):
    bstack1lll11l11lll_opy_[bstack1l1111_opy_ (u"ࠨࡩ࡯ࡥ࡯ࡹࡩ࡫ࡅ࡯ࡥࡲࡨࡪࡪࡅࡹࡶࡨࡲࡸ࡯࡯࡯ࠤ⍨")] = True
  return bstack1lll11l11lll_opy_
def bstack1lll11llll11_opy_(array, bstack1lll11l1l111_opy_, bstack1lll11l1ll1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1lll11l1l111_opy_]
    result[key] = o[bstack1lll11l1ll1l_opy_]
  return result
def bstack1lll11ll11ll_opy_(bstack1ll11l11ll_opy_=bstack1l1111_opy_ (u"ࠧࠨ⍩")):
  bstack1lll11l1l11l_opy_ = bstack1l11l1l111_opy_.on()
  bstack1lll11l11ll1_opy_ = bstack1lll11ll11_opy_.on()
  bstack1lll11l111ll_opy_ = percy.bstack11l1llllll_opy_()
  if bstack1lll11l111ll_opy_ and not bstack1lll11l11ll1_opy_ and not bstack1lll11l1l11l_opy_:
    return bstack1ll11l11ll_opy_ not in [bstack1l1111_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ⍪"), bstack1l1111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭⍫")]
  elif bstack1lll11l1l11l_opy_ and not bstack1lll11l11ll1_opy_:
    return bstack1ll11l11ll_opy_ not in [bstack1l1111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ⍬"), bstack1l1111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⍭"), bstack1l1111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⍮")]
  return bstack1lll11l1l11l_opy_ or bstack1lll11l11ll1_opy_ or bstack1lll11l111ll_opy_
@error_handler(class_method=False)
def bstack1lll1l111lll_opy_(bstack1ll11l11ll_opy_, test=None):
  bstack1lll11l1l1ll_opy_ = bstack1l11l1l111_opy_.on()
  if not bstack1lll11l1l1ll_opy_ or bstack1ll11l11ll_opy_ not in [bstack1l1111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⍯")] or test == None:
    return None
  return {
    bstack1l1111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⍰"): bstack1lll11l1l1ll_opy_ and bstack111111lll_opy_(threading.current_thread(), bstack1l1111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⍱"), None) == True and bstack1l11l1l111_opy_.bstack1lllll11ll_opy_(test[bstack1l1111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⍲")])
  }
def bstack1lll11l11l1l_opy_(bs_config, framework):
  bstack11ll1l1111_opy_ = False
  bstack1lll1ll1l_opy_ = False
  bstack1lll11l11l11_opy_ = False
  if bstack1l1111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⍳") in bs_config:
    bstack1lll11l11l11_opy_ = True
  elif bstack1l1111_opy_ (u"ࠫࡦࡶࡰࠨ⍴") in bs_config:
    bstack11ll1l1111_opy_ = True
  else:
    bstack1lll1ll1l_opy_ = True
  bstack1l1111lll_opy_ = {
    bstack1l1111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⍵"): bstack1lll11ll11_opy_.bstack1lll11l1lll1_opy_(bs_config, framework),
    bstack1l1111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⍶"): bstack1l11l1l111_opy_.bstack1lll1111ll_opy_(bs_config),
    bstack1l1111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⍷"): bs_config.get(bstack1l1111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⍸"), False),
    bstack1l1111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⍹"): bstack1lll1ll1l_opy_,
    bstack1l1111_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⍺"): bstack11ll1l1111_opy_,
    bstack1l1111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⍻"): bstack1lll11l11l11_opy_
  }
  return bstack1l1111lll_opy_