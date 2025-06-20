# coding: UTF-8
import sys
bstack1ll1l1l_opy_ = sys.version_info [0] == 2
bstack1ll1ll_opy_ = 2048
bstack1l1l11l_opy_ = 7
def bstack11ll11_opy_ (bstack11l1lll_opy_):
    global bstack1l1l_opy_
    bstack1lll111_opy_ = ord (bstack11l1lll_opy_ [-1])
    bstack1l1lll_opy_ = bstack11l1lll_opy_ [:-1]
    bstack1ll1lll_opy_ = bstack1lll111_opy_ % len (bstack1l1lll_opy_)
    bstack11l1l11_opy_ = bstack1l1lll_opy_ [:bstack1ll1lll_opy_] + bstack1l1lll_opy_ [bstack1ll1lll_opy_:]
    if bstack1ll1l1l_opy_:
        bstack111l_opy_ = unicode () .join ([unichr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    else:
        bstack111l_opy_ = str () .join ([chr (ord (char) - bstack1ll1ll_opy_ - (bstack11l11l_opy_ + bstack1lll111_opy_) % bstack1l1l11l_opy_) for bstack11l11l_opy_, char in enumerate (bstack11l1l11_opy_)])
    return eval (bstack111l_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11ll1ll1111_opy_, bstack11l1l1l1l_opy_, get_host_info, bstack11l11l1lll1_opy_, \
 bstack1l111lll1l_opy_, bstack111ll1lll_opy_, bstack111l1lll11_opy_, bstack11l11ll11l1_opy_, bstack1l11l11ll_opy_
import bstack_utils.accessibility as bstack11l11lll11_opy_
from bstack_utils.bstack111lll111l_opy_ import bstack11l1ll11_opy_
from bstack_utils.percy import bstack1l1111ll1_opy_
from bstack_utils.config import Config
bstack1l1ll1llll_opy_ = Config.bstack1lll11ll_opy_()
logger = logging.getLogger(__name__)
percy = bstack1l1111ll1_opy_()
@bstack111l1lll11_opy_(class_method=False)
def bstack1lllll1llll1_opy_(bs_config, bstack1l1llll11l_opy_):
  try:
    data = {
        bstack11ll11_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧ₦"): bstack11ll11_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭₧"),
        bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨ₨"): bs_config.get(bstack11ll11_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ₩"), bstack11ll11_opy_ (u"ࠫࠬ₪")),
        bstack11ll11_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ₫"): bs_config.get(bstack11ll11_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ€"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack11ll11_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ₭"): bs_config.get(bstack11ll11_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ₮")),
        bstack11ll11_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ₯"): bs_config.get(bstack11ll11_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭₰"), bstack11ll11_opy_ (u"ࠫࠬ₱")),
        bstack11ll11_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₲"): bstack1l11l11ll_opy_(),
        bstack11ll11_opy_ (u"࠭ࡴࡢࡩࡶࠫ₳"): bstack11l11l1lll1_opy_(bs_config),
        bstack11ll11_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪ₴"): get_host_info(),
        bstack11ll11_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩ₵"): bstack11l1l1l1l_opy_(),
        bstack11ll11_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩ₶"): os.environ.get(bstack11ll11_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩ₷")),
        bstack11ll11_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩ₸"): os.environ.get(bstack11ll11_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪ₹"), False),
        bstack11ll11_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨ₺"): bstack11ll1ll1111_opy_(),
        bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ₻"): bstack1lllll1l111l_opy_(bs_config),
        bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬ₼"): bstack1lllll11l1ll_opy_(bstack1l1llll11l_opy_),
        bstack11ll11_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧ₽"): bstack1lllll1l1111_opy_(bs_config, bstack1l1llll11l_opy_.get(bstack11ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫ₾"), bstack11ll11_opy_ (u"ࠫࠬ₿"))),
        bstack11ll11_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ⃀"): bstack1l111lll1l_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack11ll11_opy_ (u"ࠨࡅࡹࡥࡨࡴࡹ࡯࡯࡯ࠢࡺ࡬࡮ࡲࡥࠡࡥࡵࡩࡦࡺࡩ࡯ࡩࠣࡴࡦࡿ࡬ࡰࡣࡧࠤ࡫ࡵࡲࠡࡖࡨࡷࡹࡎࡵࡣ࠼ࠣࠤࢀࢃࠢ⃁").format(str(error)))
    return None
def bstack1lllll11l1ll_opy_(framework):
  return {
    bstack11ll11_opy_ (u"ࠧࡧࡴࡤࡱࡪࡽ࡯ࡳ࡭ࡑࡥࡲ࡫ࠧ⃂"): framework.get(bstack11ll11_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡳࡧ࡭ࡦࠩ⃃"), bstack11ll11_opy_ (u"ࠩࡓࡽࡹ࡫ࡳࡵࠩ⃄")),
    bstack11ll11_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰ࡜ࡥࡳࡵ࡬ࡳࡳ࠭⃅"): framework.get(bstack11ll11_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡷࡧࡵࡷ࡮ࡵ࡮ࠨ⃆")),
    bstack11ll11_opy_ (u"ࠬࡹࡤ࡬ࡘࡨࡶࡸ࡯࡯࡯ࠩ⃇"): framework.get(bstack11ll11_opy_ (u"࠭ࡳࡥ࡭ࡢࡺࡪࡸࡳࡪࡱࡱࠫ⃈")),
    bstack11ll11_opy_ (u"ࠧ࡭ࡣࡱ࡫ࡺࡧࡧࡦࠩ⃉"): bstack11ll11_opy_ (u"ࠨࡲࡼࡸ࡭ࡵ࡮ࠨ⃊"),
    bstack11ll11_opy_ (u"ࠩࡷࡩࡸࡺࡆࡳࡣࡰࡩࡼࡵࡲ࡬ࠩ⃋"): framework.get(bstack11ll11_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⃌"))
  }
def bstack1ll1l1l11l_opy_(bs_config, framework):
  bstack1llllll11_opy_ = False
  bstack1llll1111l_opy_ = False
  bstack1lllll11l111_opy_ = False
  if bstack11ll11_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⃍") in bs_config:
    bstack1lllll11l111_opy_ = True
  elif bstack11ll11_opy_ (u"ࠬࡧࡰࡱࠩ⃎") in bs_config:
    bstack1llllll11_opy_ = True
  else:
    bstack1llll1111l_opy_ = True
  bstack1l11111111_opy_ = {
    bstack11ll11_opy_ (u"࠭࡯ࡣࡵࡨࡶࡻࡧࡢࡪ࡮࡬ࡸࡾ࠭⃏"): bstack11l1ll11_opy_.bstack1lllll111ll1_opy_(bs_config, framework),
    bstack11ll11_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃐"): bstack11l11lll11_opy_.bstack1l11l11l11_opy_(bs_config),
    bstack11ll11_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⃑"): bs_config.get(bstack11ll11_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⃒"), False),
    bstack11ll11_opy_ (u"ࠪࡥࡺࡺ࡯࡮ࡣࡷࡩ⃓ࠬ"): bstack1llll1111l_opy_,
    bstack11ll11_opy_ (u"ࠫࡦࡶࡰࡠࡣࡸࡸࡴࡳࡡࡵࡧࠪ⃔"): bstack1llllll11_opy_,
    bstack11ll11_opy_ (u"ࠬࡺࡵࡳࡤࡲࡷࡨࡧ࡬ࡦࠩ⃕"): bstack1lllll11l111_opy_
  }
  return bstack1l11111111_opy_
@bstack111l1lll11_opy_(class_method=False)
def bstack1lllll1l111l_opy_(bs_config):
  try:
    bstack1lllll11l1l1_opy_ = json.loads(os.getenv(bstack11ll11_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤ࡚ࡅࡔࡖࡢࡅࡈࡉࡅࡔࡕࡌࡆࡎࡒࡉࡕ࡛ࡢࡇࡔࡔࡆࡊࡉࡘࡖࡆ࡚ࡉࡐࡐࡢ࡝ࡒࡒࠧ⃖"), bstack11ll11_opy_ (u"ࠧࡼࡿࠪ⃗")))
    bstack1lllll11l1l1_opy_ = bstack1lllll11ll1l_opy_(bs_config, bstack1lllll11l1l1_opy_)
    return {
        bstack11ll11_opy_ (u"ࠨࡵࡨࡸࡹ࡯࡮ࡨࡵ⃘ࠪ"): bstack1lllll11l1l1_opy_
    }
  except Exception as error:
    logger.error(bstack11ll11_opy_ (u"ࠤࡈࡼࡨ࡫ࡰࡵ࡫ࡲࡲࠥࡽࡨࡪ࡮ࡨࠤࡨࡸࡥࡢࡶ࡬ࡲ࡬ࠦࡧࡦࡶࡢࡥࡨࡩࡥࡴࡵ࡬ࡦ࡮ࡲࡩࡵࡻࡢࡷࡪࡺࡴࡪࡰࡪࡷࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽ⃙ࠣ").format(str(error)))
    return {}
def bstack1lllll11ll1l_opy_(bs_config, bstack1lllll11l1l1_opy_):
  if ((bstack11ll11_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫⃚ࠧ") in bs_config or not bstack1l111lll1l_opy_(bs_config)) and bstack11l11lll11_opy_.bstack1l11l11l11_opy_(bs_config)):
    bstack1lllll11l1l1_opy_[bstack11ll11_opy_ (u"ࠦ࡮ࡴࡣ࡭ࡷࡧࡩࡊࡴࡣࡰࡦࡨࡨࡊࡾࡴࡦࡰࡶ࡭ࡴࡴࠢ⃛")] = True
  return bstack1lllll11l1l1_opy_
def bstack1llllll111l1_opy_(array, bstack1lllll11llll_opy_, bstack1lllll111lll_opy_):
  result = {}
  for o in array:
    key = o[bstack1lllll11llll_opy_]
    result[key] = o[bstack1lllll111lll_opy_]
  return result
def bstack1llllll1l1l1_opy_(bstack1l1ll11l1l_opy_=bstack11ll11_opy_ (u"ࠬ࠭⃜")):
  bstack1lllll11l11l_opy_ = bstack11l11lll11_opy_.on()
  bstack1lllll1l11l1_opy_ = bstack11l1ll11_opy_.on()
  bstack1lllll11ll11_opy_ = percy.bstack11ll1ll1l_opy_()
  if bstack1lllll11ll11_opy_ and not bstack1lllll1l11l1_opy_ and not bstack1lllll11l11l_opy_:
    return bstack1l1ll11l1l_opy_ not in [bstack11ll11_opy_ (u"࠭ࡃࡃࡖࡖࡩࡸࡹࡩࡰࡰࡆࡶࡪࡧࡴࡦࡦࠪ⃝"), bstack11ll11_opy_ (u"ࠧࡍࡱࡪࡇࡷ࡫ࡡࡵࡧࡧࠫ⃞")]
  elif bstack1lllll11l11l_opy_ and not bstack1lllll1l11l1_opy_:
    return bstack1l1ll11l1l_opy_ not in [bstack11ll11_opy_ (u"ࠨࡊࡲࡳࡰࡘࡵ࡯ࡕࡷࡥࡷࡺࡥࡥࠩ⃟"), bstack11ll11_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡉ࡭ࡳ࡯ࡳࡩࡧࡧࠫ⃠"), bstack11ll11_opy_ (u"ࠪࡐࡴ࡭ࡃࡳࡧࡤࡸࡪࡪࠧ⃡")]
  return bstack1lllll11l11l_opy_ or bstack1lllll1l11l1_opy_ or bstack1lllll11ll11_opy_
@bstack111l1lll11_opy_(class_method=False)
def bstack1lllll1ll1l1_opy_(bstack1l1ll11l1l_opy_, test=None):
  bstack1lllll11lll1_opy_ = bstack11l11lll11_opy_.on()
  if not bstack1lllll11lll1_opy_ or bstack1l1ll11l1l_opy_ not in [bstack11ll11_opy_ (u"࡙ࠫ࡫ࡳࡵࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭⃢")] or test == None:
    return None
  return {
    bstack11ll11_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࠬ⃣"): bstack1lllll11lll1_opy_ and bstack111ll1lll_opy_(threading.current_thread(), bstack11ll11_opy_ (u"࠭ࡡ࠲࠳ࡼࡔࡱࡧࡴࡧࡱࡵࡱࠬ⃤"), None) == True and bstack11l11lll11_opy_.bstack1ll1lllll_opy_(test[bstack11ll11_opy_ (u"ࠧࡵࡣࡪࡷ⃥ࠬ")])
  }
def bstack1lllll1l1111_opy_(bs_config, framework):
  bstack1llllll11_opy_ = False
  bstack1llll1111l_opy_ = False
  bstack1lllll11l111_opy_ = False
  if bstack11ll11_opy_ (u"ࠨࡶࡸࡶࡧࡵࡓࡤࡣ࡯ࡩ⃦ࠬ") in bs_config:
    bstack1lllll11l111_opy_ = True
  elif bstack11ll11_opy_ (u"ࠩࡤࡴࡵ࠭⃧") in bs_config:
    bstack1llllll11_opy_ = True
  else:
    bstack1llll1111l_opy_ = True
  bstack1l11111111_opy_ = {
    bstack11ll11_opy_ (u"ࠪࡳࡧࡹࡥࡳࡸࡤࡦ࡮ࡲࡩࡵࡻ⃨ࠪ"): bstack11l1ll11_opy_.bstack1lllll111ll1_opy_(bs_config, framework),
    bstack11ll11_opy_ (u"ࠫࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࠫ⃩"): bstack11l11lll11_opy_.bstack1l1ll111ll_opy_(bs_config),
    bstack11ll11_opy_ (u"ࠬࡶࡥࡳࡥࡼ⃪ࠫ"): bs_config.get(bstack11ll11_opy_ (u"࠭ࡰࡦࡴࡦࡽ⃫ࠬ"), False),
    bstack11ll11_opy_ (u"ࠧࡢࡷࡷࡳࡲࡧࡴࡦ⃬ࠩ"): bstack1llll1111l_opy_,
    bstack11ll11_opy_ (u"ࠨࡣࡳࡴࡤࡧࡵࡵࡱࡰࡥࡹ࡫⃭ࠧ"): bstack1llllll11_opy_,
    bstack11ll11_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡴࡥࡤࡰࡪ⃮࠭"): bstack1lllll11l111_opy_
  }
  return bstack1l11111111_opy_