# coding: UTF-8
import sys
bstack1l1l11l_opy_ = sys.version_info [0] == 2
bstack1ll11l_opy_ = 2048
bstack1l11ll1_opy_ = 7
def bstack1l1ll1_opy_ (bstack111ll1l_opy_):
    global bstack111ll1_opy_
    bstack11ll1ll_opy_ = ord (bstack111ll1l_opy_ [-1])
    bstack1l11ll_opy_ = bstack111ll1l_opy_ [:-1]
    bstack11l1l11_opy_ = bstack11ll1ll_opy_ % len (bstack1l11ll_opy_)
    bstack11ll1_opy_ = bstack1l11ll_opy_ [:bstack11l1l11_opy_] + bstack1l11ll_opy_ [bstack11l1l11_opy_:]
    if bstack1l1l11l_opy_:
        bstack111ll11_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    else:
        bstack111ll11_opy_ = str () .join ([chr (ord (char) - bstack1ll11l_opy_ - (bstack1l1l1ll_opy_ + bstack11ll1ll_opy_) % bstack1l11ll1_opy_) for bstack1l1l1ll_opy_, char in enumerate (bstack11ll1_opy_)])
    return eval (bstack111ll11_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll11l1ll_opy_, bstack11ll11ll1_opy_, get_host_info, bstack111llll1lll_opy_, \
 bstack11ll1ll11_opy_, bstack11l1ll11ll_opy_, bstack111l1111ll_opy_, bstack11l11ll11ll_opy_, bstack1llllll1l_opy_
import bstack_utils.accessibility as bstack1l11ll1lll_opy_
from bstack_utils.bstack111ll1lll1_opy_ import bstack111l1ll1l_opy_
from bstack_utils.percy import bstack11llll1111_opy_
from bstack_utils.config import Config
bstack11lll111ll_opy_ = Config.bstack11ll1l11l_opy_()
logger = logging.getLogger(__name__)
percy = bstack11llll1111_opy_()
@bstack111l1111ll_opy_(class_method=False)
def bstack1lllll1ll1l1_opy_(bs_config, bstack1lll11111l_opy_):
  try:
    data = {
        bstack1l1ll1_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬ⃇"): bstack1l1ll1_opy_ (u"࠭ࡪࡴࡱࡱࠫ⃈"),
        bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭⃉"): bs_config.get(bstack1l1ll1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⃊"), bstack1l1ll1_opy_ (u"ࠩࠪ⃋")),
        bstack1l1ll1_opy_ (u"ࠪࡲࡦࡳࡥࠨ⃌"): bs_config.get(bstack1l1ll1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⃍"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1ll1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⃎"): bs_config.get(bstack1l1ll1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⃏")),
        bstack1l1ll1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⃐"): bs_config.get(bstack1l1ll1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ⃑"), bstack1l1ll1_opy_ (u"⃒ࠩࠪ")),
        bstack1l1ll1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺ⃓ࠧ"): bstack1llllll1l_opy_(),
        bstack1l1ll1_opy_ (u"ࠫࡹࡧࡧࡴࠩ⃔"): bstack111llll1lll_opy_(bs_config),
        bstack1l1ll1_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨ⃕"): get_host_info(),
        bstack1l1ll1_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ⃖"): bstack11ll11ll1_opy_(),
        bstack1l1ll1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⃗"): os.environ.get(bstack1l1ll1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ⃘ࠧ")),
        bstack1l1ll1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴ⃙ࠧ"): os.environ.get(bstack1l1ll1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ⃚"), False),
        bstack1l1ll1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭⃛"): bstack11lll11l1ll_opy_(),
        bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃜"): bstack1lllll11l111_opy_(bs_config),
        bstack1l1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ⃝"): bstack1lllll11ll11_opy_(bstack1lll11111l_opy_),
        bstack1l1ll1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⃞"): bstack1lllll1111ll_opy_(bs_config, bstack1lll11111l_opy_.get(bstack1l1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ⃟"), bstack1l1ll1_opy_ (u"ࠩࠪ⃠"))),
        bstack1l1ll1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⃡"): bstack11ll1ll11_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1ll1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⃢").format(str(error)))
    return None
def bstack1lllll11ll11_opy_(framework):
  return {
    bstack1l1ll1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ⃣"): framework.get(bstack1l1ll1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧ⃤"), bstack1l1ll1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ⃥ࠧ")),
    bstack1l1ll1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱ⃦ࠫ"): framework.get(bstack1l1ll1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⃧")),
    bstack1l1ll1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴ⃨ࠧ"): framework.get(bstack1l1ll1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⃩")),
    bstack1l1ll1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫⃪ࠧ"): bstack1l1ll1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ⃫࠭"),
    bstack1l1ll1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱ⃬ࠧ"): framework.get(bstack1l1ll1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⃭"))
  }
def bstack11l1lllll1_opy_(bs_config, framework):
  bstack1lll111lll_opy_ = False
  bstack111l1l11_opy_ = False
  bstack1lllll11l1l1_opy_ = False
  if bstack1l1ll1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ⃮࠭") in bs_config:
    bstack1lllll11l1l1_opy_ = True
  elif bstack1l1ll1_opy_ (u"ࠪࡥࡵࡶ⃯ࠧ") in bs_config:
    bstack1lll111lll_opy_ = True
  else:
    bstack111l1l11_opy_ = True
  bstack1lll1l1l11_opy_ = {
    bstack1l1ll1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃰"): bstack111l1ll1l_opy_.bstack1lllll11111l_opy_(bs_config, framework),
    bstack1l1ll1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃱"): bstack1l11ll1lll_opy_.bstack111llllll_opy_(bs_config),
    bstack1l1ll1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⃲"): bs_config.get(bstack1l1ll1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⃳"), False),
    bstack1l1ll1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⃴"): bstack111l1l11_opy_,
    bstack1l1ll1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⃵"): bstack1lll111lll_opy_,
    bstack1l1ll1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⃶"): bstack1lllll11l1l1_opy_
  }
  return bstack1lll1l1l11_opy_
@bstack111l1111ll_opy_(class_method=False)
def bstack1lllll11l111_opy_(bs_config):
  try:
    bstack1lllll111ll1_opy_ = json.loads(os.getenv(bstack1l1ll1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⃷"), bstack1l1ll1_opy_ (u"ࠬࢁࡽࠨ⃸")))
    bstack1lllll111ll1_opy_ = bstack1lllll111l11_opy_(bs_config, bstack1lllll111ll1_opy_)
    return {
        bstack1l1ll1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ⃹"): bstack1lllll111ll1_opy_
    }
  except Exception as error:
    logger.error(bstack1l1ll1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⃺").format(str(error)))
    return {}
def bstack1lllll111l11_opy_(bs_config, bstack1lllll111ll1_opy_):
  if ((bstack1l1ll1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⃻") in bs_config or not bstack11ll1ll11_opy_(bs_config)) and bstack1l11ll1lll_opy_.bstack111llllll_opy_(bs_config)):
    bstack1lllll111ll1_opy_[bstack1l1ll1_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧ⃼")] = True
  return bstack1lllll111ll1_opy_
def bstack1lllll1lll11_opy_(array, bstack1lllll111l1l_opy_, bstack1lllll11l11l_opy_):
  result = {}
  for o in array:
    key = o[bstack1lllll111l1l_opy_]
    result[key] = o[bstack1lllll11l11l_opy_]
  return result
def bstack1lllll1l1l11_opy_(bstack1111l1ll1_opy_=bstack1l1ll1_opy_ (u"ࠪࠫ⃽")):
  bstack1lllll111lll_opy_ = bstack1l11ll1lll_opy_.on()
  bstack1lllll1111l1_opy_ = bstack111l1ll1l_opy_.on()
  bstack1lllll11l1ll_opy_ = percy.bstack1ll1111lll_opy_()
  if bstack1lllll11l1ll_opy_ and not bstack1lllll1111l1_opy_ and not bstack1lllll111lll_opy_:
    return bstack1111l1ll1_opy_ not in [bstack1l1ll1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ⃾"), bstack1l1ll1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⃿")]
  elif bstack1lllll111lll_opy_ and not bstack1lllll1111l1_opy_:
    return bstack1111l1ll1_opy_ not in [bstack1l1ll1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ℀"), bstack1l1ll1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ℁"), bstack1l1ll1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬℂ")]
  return bstack1lllll111lll_opy_ or bstack1lllll1111l1_opy_ or bstack1lllll11l1ll_opy_
@bstack111l1111ll_opy_(class_method=False)
def bstack1llllll1111l_opy_(bstack1111l1ll1_opy_, test=None):
  bstack1lllll11ll1l_opy_ = bstack1l11ll1lll_opy_.on()
  if not bstack1lllll11ll1l_opy_ or bstack1111l1ll1_opy_ not in [bstack1l1ll1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ℃")] or test == None:
    return None
  return {
    bstack1l1ll1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ℄"): bstack1lllll11ll1l_opy_ and bstack11l1ll11ll_opy_(threading.current_thread(), bstack1l1ll1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ℅"), None) == True and bstack1l11ll1lll_opy_.bstack11l11l11_opy_(test[bstack1l1ll1_opy_ (u"ࠬࡺࡡࡨࡵࠪ℆")])
  }
def bstack1lllll1111ll_opy_(bs_config, framework):
  bstack1lll111lll_opy_ = False
  bstack111l1l11_opy_ = False
  bstack1lllll11l1l1_opy_ = False
  if bstack1l1ll1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪℇ") in bs_config:
    bstack1lllll11l1l1_opy_ = True
  elif bstack1l1ll1_opy_ (u"ࠧࡢࡲࡳࠫ℈") in bs_config:
    bstack1lll111lll_opy_ = True
  else:
    bstack111l1l11_opy_ = True
  bstack1lll1l1l11_opy_ = {
    bstack1l1ll1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ℉"): bstack111l1ll1l_opy_.bstack1lllll11111l_opy_(bs_config, framework),
    bstack1l1ll1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩℊ"): bstack1l11ll1lll_opy_.bstack1111l1lll_opy_(bs_config),
    bstack1l1ll1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩℋ"): bs_config.get(bstack1l1ll1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪℌ"), False),
    bstack1l1ll1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧℍ"): bstack111l1l11_opy_,
    bstack1l1ll1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬℎ"): bstack1lll111lll_opy_,
    bstack1l1ll1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫℏ"): bstack1lllll11l1l1_opy_
  }
  return bstack1lll1l1l11_opy_