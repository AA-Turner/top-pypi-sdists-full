# coding: UTF-8
import sys
bstack1l111l_opy_ = sys.version_info [0] == 2
bstack1ll1111_opy_ = 2048
bstack1ll11_opy_ = 7
def bstack11ll1l1_opy_ (bstack1lll1ll_opy_):
    global bstack1l1l111_opy_
    bstack1l1111l_opy_ = ord (bstack1lll1ll_opy_ [-1])
    bstack1lll11_opy_ = bstack1lll1ll_opy_ [:-1]
    bstack1l1llll_opy_ = bstack1l1111l_opy_ % len (bstack1lll11_opy_)
    bstack11l111l_opy_ = bstack1lll11_opy_ [:bstack1l1llll_opy_] + bstack1lll11_opy_ [bstack1l1llll_opy_:]
    if bstack1l111l_opy_:
        bstack111l1l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    else:
        bstack111l1l_opy_ = str () .join ([chr (ord (char) - bstack1ll1111_opy_ - (bstack11l11l_opy_ + bstack1l1111l_opy_) % bstack1ll11_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l111l_opy_)])
    return eval (bstack111l1l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1l1l11l_opy_, bstack1l1l1l111l_opy_, get_host_info, bstack11l11ll111l_opy_, \
 bstack1ll1l1lll1_opy_, bstack11111ll1l_opy_, bstack111l1llll1_opy_, bstack111llll111l_opy_, bstack1ll1l11l11_opy_
import bstack_utils.accessibility as bstack1lll11l1_opy_
from bstack_utils.bstack111ll1l11l_opy_ import bstack1l1111l1_opy_
from bstack_utils.percy import bstack11ll1l11ll_opy_
from bstack_utils.config import Config
bstack1111ll111_opy_ = Config.bstack1lllll111l_opy_()
logger = logging.getLogger(__name__)
percy = bstack11ll1l11ll_opy_()
@bstack111l1llll1_opy_(class_method=False)
def bstack1llllll11ll1_opy_(bs_config, bstack1lllll111_opy_):
  try:
    data = {
        bstack11ll1l1_opy_ (u"ࠬ࡬࡯ࡳ࡯ࡤࡸࠬ⃇"): bstack11ll1l1_opy_ (u"࠭ࡪࡴࡱࡱࠫ⃈"),
        bstack11ll1l1_opy_ (u"ࠧࡱࡴࡲ࡮ࡪࡩࡴࡠࡰࡤࡱࡪ࠭⃉"): bs_config.get(bstack11ll1l1_opy_ (u"ࠨࡲࡵࡳ࡯࡫ࡣࡵࡐࡤࡱࡪ࠭⃊"), bstack11ll1l1_opy_ (u"ࠩࠪ⃋")),
        bstack11ll1l1_opy_ (u"ࠪࡲࡦࡳࡥࠨ⃌"): bs_config.get(bstack11ll1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡑࡥࡲ࡫ࠧ⃍"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11ll1l1_opy_ (u"ࠬࡨࡵࡪ࡮ࡧࡣ࡮ࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⃎"): bs_config.get(bstack11ll1l1_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡎࡪࡥ࡯ࡶ࡬ࡪ࡮࡫ࡲࠨ⃏")),
        bstack11ll1l1_opy_ (u"ࠧࡥࡧࡶࡧࡷ࡯ࡰࡵ࡫ࡲࡲࠬ⃐"): bs_config.get(bstack11ll1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡄࡦࡵࡦࡶ࡮ࡶࡴࡪࡱࡱࠫ⃑"), bstack11ll1l1_opy_ (u"⃒ࠩࠪ")),
        bstack11ll1l1_opy_ (u"ࠪࡷࡹࡧࡲࡵࡧࡧࡣࡦࡺ⃓ࠧ"): bstack1ll1l11l11_opy_(),
        bstack11ll1l1_opy_ (u"ࠫࡹࡧࡧࡴࠩ⃔"): bstack11l11ll111l_opy_(bs_config),
        bstack11ll1l1_opy_ (u"ࠬ࡮࡯ࡴࡶࡢ࡭ࡳ࡬࡯ࠨ⃕"): get_host_info(),
        bstack11ll1l1_opy_ (u"࠭ࡣࡪࡡ࡬ࡲ࡫ࡵࠧ⃖"): bstack1l1l1l111l_opy_(),
        bstack11ll1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡲࡶࡰࡢ࡭ࡩ࡫࡮ࡵ࡫ࡩ࡭ࡪࡸࠧ⃗"): os.environ.get(bstack11ll1l1_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡃࡗࡌࡐࡉࡥࡒࡖࡐࡢࡍࡉࡋࡎࡕࡋࡉࡍࡊࡘ⃘ࠧ")),
        bstack11ll1l1_opy_ (u"ࠩࡩࡥ࡮ࡲࡥࡥࡡࡷࡩࡸࡺࡳࡠࡴࡨࡶࡺࡴ⃙ࠧ"): os.environ.get(bstack11ll1l1_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡕࡉࡗ࡛ࡎࠨ⃚"), False),
        bstack11ll1l1_opy_ (u"ࠫࡻ࡫ࡲࡴ࡫ࡲࡲࡤࡩ࡯࡯ࡶࡵࡳࡱ࠭⃛"): bstack11ll1l1l11l_opy_(),
        bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃜"): bstack1lllll11l111_opy_(bs_config),
        bstack11ll1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡧࡩࡹࡧࡩ࡭ࡵࠪ⃝"): bstack1lllll11111l_opy_(bstack1lllll111_opy_),
        bstack11ll1l1_opy_ (u"ࠧࡱࡴࡲࡨࡺࡩࡴࡠ࡯ࡤࡴࠬ⃞"): bstack1lllll1111l1_opy_(bs_config, bstack1lllll111_opy_.get(bstack11ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡺࡹࡥࡥࠩ⃟"), bstack11ll1l1_opy_ (u"ࠩࠪ⃠"))),
        bstack11ll1l1_opy_ (u"ࠪࡦࡷࡵࡷࡴࡧࡵࡷࡹࡧࡣ࡬ࡃࡸࡸࡴࡳࡡࡵ࡫ࡲࡲࠬ⃡"): bstack1ll1l1lll1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11ll1l1_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡲࡤࡽࡱࡵࡡࡥࠢࡩࡳࡷࠦࡔࡦࡵࡷࡌࡺࡨ࠺ࠡࠢࡾࢁࠧ⃢").format(str(error)))
    return None
def bstack1lllll11111l_opy_(framework):
  return {
    bstack11ll1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡏࡣࡰࡩࠬ⃣"): framework.get(bstack11ll1l1_opy_ (u"࠭ࡦࡳࡣࡰࡩࡼࡵࡲ࡬ࡡࡱࡥࡲ࡫ࠧ⃤"), bstack11ll1l1_opy_ (u"ࠧࡑࡻࡷࡩࡸࡺ⃥ࠧ")),
    bstack11ll1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮࡚ࡪࡸࡳࡪࡱࡱ⃦ࠫ"): framework.get(bstack11ll1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡼࡥࡳࡵ࡬ࡳࡳ࠭⃧")),
    bstack11ll1l1_opy_ (u"ࠪࡷࡩࡱࡖࡦࡴࡶ࡭ࡴࡴ⃨ࠧ"): framework.get(bstack11ll1l1_opy_ (u"ࠫࡸࡪ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⃩")),
    bstack11ll1l1_opy_ (u"ࠬࡲࡡ࡯ࡩࡸࡥ࡬࡫⃪ࠧ"): bstack11ll1l1_opy_ (u"࠭ࡰࡺࡶ࡫ࡳࡳ⃫࠭"),
    bstack11ll1l1_opy_ (u"ࠧࡵࡧࡶࡸࡋࡸࡡ࡮ࡧࡺࡳࡷࡱ⃬ࠧ"): framework.get(bstack11ll1l1_opy_ (u"ࠨࡶࡨࡷࡹࡌࡲࡢ࡯ࡨࡻࡴࡸ࡫ࠨ⃭"))
  }
def bstack1l11111l1_opy_(bs_config, framework):
  bstack11ll1l11l_opy_ = False
  bstack1ll1ll1l11_opy_ = False
  bstack1lllll111lll_opy_ = False
  if bstack11ll1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ⃮࠭") in bs_config:
    bstack1lllll111lll_opy_ = True
  elif bstack11ll1l1_opy_ (u"ࠪࡥࡵࡶ⃯ࠧ") in bs_config:
    bstack11ll1l11l_opy_ = True
  else:
    bstack1ll1ll1l11_opy_ = True
  bstack1l1l1ll111_opy_ = {
    bstack11ll1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃰"): bstack1l1111l1_opy_.bstack1lllll1111ll_opy_(bs_config, framework),
    bstack11ll1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃱"): bstack1lll11l1_opy_.bstack1l111l1111_opy_(bs_config),
    bstack11ll1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽࠬ⃲"): bs_config.get(bstack11ll1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⃳"), False),
    bstack11ll1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧࠪ⃴"): bstack1ll1ll1l11_opy_,
    bstack11ll1l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⃵"): bstack11ll1l11l_opy_,
    bstack11ll1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫ࠧ⃶"): bstack1lllll111lll_opy_
  }
  return bstack1l1l1ll111_opy_
@bstack111l1llll1_opy_(class_method=False)
def bstack1lllll11l111_opy_(bs_config):
  try:
    bstack1lllll111l11_opy_ = json.loads(os.getenv(bstack11ll1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡘࡊ࡙ࡔࡠࡃࡆࡇࡊ࡙ࡓࡊࡄࡌࡐࡎ࡚࡙ࡠࡅࡒࡒࡋࡏࡇࡖࡔࡄࡘࡎࡕࡎࡠ࡛ࡐࡐࠬ⃷"), bstack11ll1l1_opy_ (u"ࠬࢁࡽࠨ⃸")))
    bstack1lllll111l11_opy_ = bstack1lllll11l11l_opy_(bs_config, bstack1lllll111l11_opy_)
    return {
        bstack11ll1l1_opy_ (u"࠭ࡳࡦࡶࡷ࡭ࡳ࡭ࡳࠨ⃹"): bstack1lllll111l11_opy_
    }
  except Exception as error:
    logger.error(bstack11ll1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤ࡬࡫ࡴࡠࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࡠࡵࡨࡸࡹ࡯࡮ࡨࡵࠣࡪࡴࡸࠠࡕࡧࡶࡸࡍࡻࡢ࠻ࠢࠣࡿࢂࠨ⃺").format(str(error)))
    return {}
def bstack1lllll11l11l_opy_(bs_config, bstack1lllll111l11_opy_):
  if ((bstack11ll1l1_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩࠬ⃻") in bs_config or not bstack1ll1l1lll1_opy_(bs_config)) and bstack1lll11l1_opy_.bstack1l111l1111_opy_(bs_config)):
    bstack1lllll111l11_opy_[bstack11ll1l1_opy_ (u"ࠤ࡬ࡲࡨࡲࡵࡥࡧࡈࡲࡨࡵࡤࡦࡦࡈࡼࡹ࡫࡮ࡴ࡫ࡲࡲࠧ⃼")] = True
  return bstack1lllll111l11_opy_
def bstack1lllll1l11ll_opy_(array, bstack1lllll111l1l_opy_, bstack1lllll11l1l1_opy_):
  result = {}
  for o in array:
    key = o[bstack1lllll111l1l_opy_]
    result[key] = o[bstack1lllll11l1l1_opy_]
  return result
def bstack1lllll1l1ll1_opy_(bstack11111l1l_opy_=bstack11ll1l1_opy_ (u"ࠪࠫ⃽")):
  bstack1lllll11l1ll_opy_ = bstack1lll11l1_opy_.on()
  bstack1lllll11ll11_opy_ = bstack1l1111l1_opy_.on()
  bstack1lllll111111_opy_ = percy.bstack1l1ll1l11_opy_()
  if bstack1lllll111111_opy_ and not bstack1lllll11ll11_opy_ and not bstack1lllll11l1ll_opy_:
    return bstack11111l1l_opy_ not in [bstack11ll1l1_opy_ (u"ࠫࡈࡈࡔࡔࡧࡶࡷ࡮ࡵ࡮ࡄࡴࡨࡥࡹ࡫ࡤࠨ⃾"), bstack11ll1l1_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⃿")]
  elif bstack1lllll11l1ll_opy_ and not bstack1lllll11ll11_opy_:
    return bstack11111l1l_opy_ not in [bstack11ll1l1_opy_ (u"࠭ࡈࡰࡱ࡮ࡖࡺࡴࡓࡵࡣࡵࡸࡪࡪࠧ℀"), bstack11ll1l1_opy_ (u"ࠧࡉࡱࡲ࡯ࡗࡻ࡮ࡇ࡫ࡱ࡭ࡸ࡮ࡥࡥࠩ℁"), bstack11ll1l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬℂ")]
  return bstack1lllll11l1ll_opy_ or bstack1lllll11ll11_opy_ or bstack1lllll111111_opy_
@bstack111l1llll1_opy_(class_method=False)
def bstack1lllll1l1l11_opy_(bstack11111l1l_opy_, test=None):
  bstack1lllll111ll1_opy_ = bstack1lll11l1_opy_.on()
  if not bstack1lllll111ll1_opy_ or bstack11111l1l_opy_ not in [bstack11ll1l1_opy_ (u"ࠩࡗࡩࡸࡺࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ℃")] or test == None:
    return None
  return {
    bstack11ll1l1_opy_ (u"ࠪࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࠪ℄"): bstack1lllll111ll1_opy_ and bstack11111ll1l_opy_(threading.current_thread(), bstack11ll1l1_opy_ (u"ࠫࡦ࠷࠱ࡺࡒ࡯ࡥࡹ࡬࡯ࡳ࡯ࠪ℅"), None) == True and bstack1lll11l1_opy_.bstack1lll11l1l1_opy_(test[bstack11ll1l1_opy_ (u"ࠬࡺࡡࡨࡵࠪ℆")])
  }
def bstack1lllll1111l1_opy_(bs_config, framework):
  bstack11ll1l11l_opy_ = False
  bstack1ll1ll1l11_opy_ = False
  bstack1lllll111lll_opy_ = False
  if bstack11ll1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪℇ") in bs_config:
    bstack1lllll111lll_opy_ = True
  elif bstack11ll1l1_opy_ (u"ࠧࡢࡲࡳࠫ℈") in bs_config:
    bstack11ll1l11l_opy_ = True
  else:
    bstack1ll1ll1l11_opy_ = True
  bstack1l1l1ll111_opy_ = {
    bstack11ll1l1_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ℉"): bstack1l1111l1_opy_.bstack1lllll1111ll_opy_(bs_config, framework),
    bstack11ll1l1_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩℊ"): bstack1lll11l1_opy_.bstack11llll1111_opy_(bs_config),
    bstack11ll1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩℋ"): bs_config.get(bstack11ll1l1_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪℌ"), False),
    bstack11ll1l1_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧℍ"): bstack1ll1ll1l11_opy_,
    bstack11ll1l1_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬℎ"): bstack11ll1l11l_opy_,
    bstack11ll1l1_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫℏ"): bstack1lllll111lll_opy_
  }
  return bstack1l1l1ll111_opy_