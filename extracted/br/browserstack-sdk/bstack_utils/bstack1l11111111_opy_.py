# coding: UTF-8
import sys
bstack11llll_opy_ = sys.version_info [0] == 2
bstack1l1lll1_opy_ = 2048
bstack11ll1_opy_ = 7
def bstack1l1l1l1_opy_ (bstack1111l11_opy_):
    global bstack11l111_opy_
    bstack11ll1l_opy_ = ord (bstack1111l11_opy_ [-1])
    bstack1l111_opy_ = bstack1111l11_opy_ [:-1]
    bstack1l11l_opy_ = bstack11ll1l_opy_ % len (bstack1l111_opy_)
    bstack1ll11l_opy_ = bstack1l111_opy_ [:bstack1l11l_opy_] + bstack1l111_opy_ [bstack1l11l_opy_:]
    if bstack11llll_opy_:
        bstack1lll1_opy_ = unicode () .join ([unichr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    else:
        bstack1lll1_opy_ = str () .join ([chr (ord (char) - bstack1l1lll1_opy_ - (bstack1ll1l1l_opy_ + bstack11ll1l_opy_) % bstack11ll1_opy_) for bstack1ll1l1l_opy_, char in enumerate (bstack1ll11l_opy_)])
    return eval (bstack1lll1_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack11lll1l111l_opy_, bstack1l1l1ll11_opy_, get_host_info, bstack11l11l1l111_opy_, \
 bstack11l1l1l1_opy_, bstack111l1ll1l_opy_, bstack111ll11111_opy_, bstack11l1l11l1ll_opy_, bstack1lllll1l1l_opy_
import bstack_utils.accessibility as bstack1ll1l11ll_opy_
from bstack_utils.bstack111ll1l1ll_opy_ import bstack11l1l1l1ll_opy_
from bstack_utils.percy import bstack11lllll1_opy_
from bstack_utils.config import Config
bstack11lll11111_opy_ = Config.bstack1ll11lll_opy_()
logger = logging.getLogger(__name__)
percy = bstack11lllll1_opy_()
@bstack111ll11111_opy_(class_method=False)
def bstack1lllll1llll1_opy_(bs_config, bstack11l1111l11_opy_):
  try:
    data = {
        bstack1l1l1l1_opy_ (u"ࠨࡨࡲࡶࡲࡧࡴࠨ₧"): bstack1l1l1l1_opy_ (u"ࠩ࡭ࡷࡴࡴࠧ₨"),
        bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡣࡳࡧ࡭ࡦࠩ₩"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠫࡵࡸ࡯࡫ࡧࡦࡸࡓࡧ࡭ࡦࠩ₪"), bstack1l1l1l1_opy_ (u"ࠬ࠭₫")),
        bstack1l1l1l1_opy_ (u"࠭࡮ࡢ࡯ࡨࠫ€"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡔࡡ࡮ࡧࠪ₭"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1l1l1l1_opy_ (u"ࠨࡤࡸ࡭ࡱࡪ࡟ࡪࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ₮"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡊࡦࡨࡲࡹ࡯ࡦࡪࡧࡵࠫ₯")),
        bstack1l1l1l1_opy_ (u"ࠪࡨࡪࡹࡣࡳ࡫ࡳࡸ࡮ࡵ࡮ࠨ₰"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠫࡧࡻࡩ࡭ࡦࡇࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ₱"), bstack1l1l1l1_opy_ (u"ࠬ࠭₲")),
        bstack1l1l1l1_opy_ (u"࠭ࡳࡵࡣࡵࡸࡪࡪ࡟ࡢࡶࠪ₳"): bstack1lllll1l1l_opy_(),
        bstack1l1l1l1_opy_ (u"ࠧࡵࡣࡪࡷࠬ₴"): bstack11l11l1l111_opy_(bs_config),
        bstack1l1l1l1_opy_ (u"ࠨࡪࡲࡷࡹࡥࡩ࡯ࡨࡲࠫ₵"): get_host_info(),
        bstack1l1l1l1_opy_ (u"ࠩࡦ࡭ࡤ࡯࡮ࡧࡱࠪ₶"): bstack1l1l1ll11_opy_(),
        bstack1l1l1l1_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡡࡵࡹࡳࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ₷"): os.environ.get(bstack1l1l1l1_opy_ (u"ࠫࡇࡘࡏࡘࡕࡈࡖࡘ࡚ࡁࡄࡍࡢࡆ࡚ࡏࡌࡅࡡࡕ࡙ࡓࡥࡉࡅࡇࡑࡘࡎࡌࡉࡆࡔࠪ₸")),
        bstack1l1l1l1_opy_ (u"ࠬ࡬ࡡࡪ࡮ࡨࡨࡤࡺࡥࡴࡶࡶࡣࡷ࡫ࡲࡶࡰࠪ₹"): os.environ.get(bstack1l1l1l1_opy_ (u"࠭ࡂࡓࡑ࡚ࡗࡊࡘࡓࡕࡃࡆࡏࡤࡘࡅࡓࡗࡑࠫ₺"), False),
        bstack1l1l1l1_opy_ (u"ࠧࡷࡧࡵࡷ࡮ࡵ࡮ࡠࡥࡲࡲࡹࡸ࡯࡭ࠩ₻"): bstack11lll1l111l_opy_(),
        bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ₼"): bstack1lllll11l11l_opy_(bs_config),
        bstack1l1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡪࡥࡵࡣ࡬ࡰࡸ࠭₽"): bstack1lllll11ll1l_opy_(bstack11l1111l11_opy_),
        bstack1l1l1l1_opy_ (u"ࠪࡴࡷࡵࡤࡶࡥࡷࡣࡲࡧࡰࠨ₾"): bstack1lllll11l1ll_opy_(bs_config, bstack11l1111l11_opy_.get(bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱ࡟ࡶࡵࡨࡨࠬ₿"), bstack1l1l1l1_opy_ (u"ࠬ࠭⃀"))),
        bstack1l1l1l1_opy_ (u"࠭ࡢࡳࡱࡺࡷࡪࡸࡳࡵࡣࡦ࡯ࡆࡻࡴࡰ࡯ࡤࡸ࡮ࡵ࡮ࠨ⃁"): bstack11l1l1l1_opy_(bs_config),
    }
    return data
  except Exception as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ⃂").format(str(error)))
    return None
def bstack1lllll11ll1l_opy_(framework):
  return {
    bstack1l1l1l1_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ⃃"): framework.get(bstack1l1l1l1_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ⃄"), bstack1l1l1l1_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ⃅")),
    bstack1l1l1l1_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ⃆"): framework.get(bstack1l1l1l1_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ⃇")),
    bstack1l1l1l1_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ⃈"): framework.get(bstack1l1l1l1_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ⃉")),
    bstack1l1l1l1_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ⃊"): bstack1l1l1l1_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ⃋"),
    bstack1l1l1l1_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ⃌"): framework.get(bstack1l1l1l1_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ⃍"))
  }
def bstack111ll1ll1_opy_(bs_config, framework):
  bstack11ll11lll1_opy_ = False
  bstack1l11llll11_opy_ = False
  bstack1lllll111lll_opy_ = False
  if bstack1l1l1l1_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ⃎") in bs_config:
    bstack1lllll111lll_opy_ = True
  elif bstack1l1l1l1_opy_ (u"࠭ࡡࡱࡲࠪ⃏") in bs_config:
    bstack11ll11lll1_opy_ = True
  else:
    bstack1l11llll11_opy_ = True
  bstack11l111l1_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠧࡰࡤࡶࡩࡷࡼࡡࡣ࡫࡯࡭ࡹࡿࠧ⃐"): bstack11l1l1l1ll_opy_.bstack1lllll11l1l1_opy_(bs_config, framework),
    bstack1l1l1l1_opy_ (u"ࠨࡣࡦࡧࡪࡹࡳࡪࡤ࡬ࡰ࡮ࡺࡹࠨ⃑"): bstack1ll1l11ll_opy_.bstack111lll11_opy_(bs_config),
    bstack1l1l1l1_opy_ (u"ࠩࡳࡩࡷࡩࡹࠨ⃒"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠪࡴࡪࡸࡣࡺ⃓ࠩ"), False),
    bstack1l1l1l1_opy_ (u"ࠫࡦࡻࡴࡰ࡯ࡤࡸࡪ࠭⃔"): bstack1l11llll11_opy_,
    bstack1l1l1l1_opy_ (u"ࠬࡧࡰࡱࡡࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⃕"): bstack11ll11lll1_opy_,
    bstack1l1l1l1_opy_ (u"࠭ࡴࡶࡴࡥࡳࡸࡩࡡ࡭ࡧࠪ⃖"): bstack1lllll111lll_opy_
  }
  return bstack11l111l1_opy_
@bstack111ll11111_opy_(class_method=False)
def bstack1lllll11l11l_opy_(bs_config):
  try:
    bstack1lllll11l111_opy_ = json.loads(os.getenv(bstack1l1l1l1_opy_ (u"ࠧࡃࡔࡒ࡛ࡘࡋࡒࡔࡖࡄࡇࡐࡥࡔࡆࡕࡗࡣࡆࡉࡃࡆࡕࡖࡍࡇࡏࡌࡊࡖ࡜ࡣࡈࡕࡎࡇࡋࡊ࡙ࡗࡇࡔࡊࡑࡑࡣ࡞ࡓࡌࠨ⃗"), bstack1l1l1l1_opy_ (u"ࠨࡽࢀ⃘ࠫ")))
    bstack1lllll11l111_opy_ = bstack1lllll1l1111_opy_(bs_config, bstack1lllll11l111_opy_)
    return {
        bstack1l1l1l1_opy_ (u"ࠩࡶࡩࡹࡺࡩ࡯ࡩࡶ⃙ࠫ"): bstack1lllll11l111_opy_
    }
  except Exception as error:
    logger.error(bstack1l1l1l1_opy_ (u"ࠥࡉࡽࡩࡥࡱࡶ࡬ࡳࡳࠦࡷࡩ࡫࡯ࡩࠥࡩࡲࡦࡣࡷ࡭ࡳ࡭ࠠࡨࡧࡷࡣࡦࡩࡣࡦࡵࡶ࡭ࡧ࡯࡬ࡪࡶࡼࡣࡸ࡫ࡴࡵ࡫ࡱ࡫ࡸࠦࡦࡰࡴࠣࡘࡪࡹࡴࡉࡷࡥ࠾ࠥࠦࡻࡾࠤ⃚").format(str(error)))
    return {}
def bstack1lllll1l1111_opy_(bs_config, bstack1lllll11l111_opy_):
  if ((bstack1l1l1l1_opy_ (u"ࠫࡹࡻࡲࡣࡱࡖࡧࡦࡲࡥࠨ⃛") in bs_config or not bstack11l1l1l1_opy_(bs_config)) and bstack1ll1l11ll_opy_.bstack111lll11_opy_(bs_config)):
    bstack1lllll11l111_opy_[bstack1l1l1l1_opy_ (u"ࠧ࡯࡮ࡤ࡮ࡸࡨࡪࡋ࡮ࡤࡱࡧࡩࡩࡋࡸࡵࡧࡱࡷ࡮ࡵ࡮ࠣ⃜")] = True
  return bstack1lllll11l111_opy_
def bstack1llllll1111l_opy_(array, bstack1lllll11ll11_opy_, bstack1lllll11llll_opy_):
  result = {}
  for o in array:
    key = o[bstack1lllll11ll11_opy_]
    result[key] = o[bstack1lllll11llll_opy_]
  return result
def bstack1llllll1l1ll_opy_(bstack11lll1ll11_opy_=bstack1l1l1l1_opy_ (u"࠭ࠧ⃝")):
  bstack1lllll1l11l1_opy_ = bstack1ll1l11ll_opy_.on()
  bstack1lllll111ll1_opy_ = bstack11l1l1l1ll_opy_.on()
  bstack1lllll11lll1_opy_ = percy.bstack1l111l11_opy_()
  if bstack1lllll11lll1_opy_ and not bstack1lllll111ll1_opy_ and not bstack1lllll1l11l1_opy_:
    return bstack11lll1ll11_opy_ not in [bstack1l1l1l1_opy_ (u"ࠧࡄࡄࡗࡗࡪࡹࡳࡪࡱࡱࡇࡷ࡫ࡡࡵࡧࡧࠫ⃞"), bstack1l1l1l1_opy_ (u"ࠨࡎࡲ࡫ࡈࡸࡥࡢࡶࡨࡨࠬ⃟")]
  elif bstack1lllll1l11l1_opy_ and not bstack1lllll111ll1_opy_:
    return bstack11lll1ll11_opy_ not in [bstack1l1l1l1_opy_ (u"ࠩࡋࡳࡴࡱࡒࡶࡰࡖࡸࡦࡸࡴࡦࡦࠪ⃠"), bstack1l1l1l1_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡊ࡮ࡴࡩࡴࡪࡨࡨࠬ⃡"), bstack1l1l1l1_opy_ (u"ࠫࡑࡵࡧࡄࡴࡨࡥࡹ࡫ࡤࠨ⃢")]
  return bstack1lllll1l11l1_opy_ or bstack1lllll111ll1_opy_ or bstack1lllll11lll1_opy_
@bstack111ll11111_opy_(class_method=False)
def bstack1lllll1l1l1l_opy_(bstack11lll1ll11_opy_, test=None):
  bstack1lllll1l111l_opy_ = bstack1ll1l11ll_opy_.on()
  if not bstack1lllll1l111l_opy_ or bstack11lll1ll11_opy_ not in [bstack1l1l1l1_opy_ (u"࡚ࠬࡥࡴࡶࡕࡹࡳࡌࡩ࡯࡫ࡶ࡬ࡪࡪࠧ⃣")] or test == None:
    return None
  return {
    bstack1l1l1l1_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃤"): bstack1lllll1l111l_opy_ and bstack111l1ll1l_opy_(threading.current_thread(), bstack1l1l1l1_opy_ (u"ࠧࡢ࠳࠴ࡽࡕࡲࡡࡵࡨࡲࡶࡲ⃥࠭"), None) == True and bstack1ll1l11ll_opy_.bstack11lll1llll_opy_(test[bstack1l1l1l1_opy_ (u"ࠨࡶࡤ࡫ࡸ⃦࠭")])
  }
def bstack1lllll11l1ll_opy_(bs_config, framework):
  bstack11ll11lll1_opy_ = False
  bstack1l11llll11_opy_ = False
  bstack1lllll111lll_opy_ = False
  if bstack1l1l1l1_opy_ (u"ࠩࡷࡹࡷࡨ࡯ࡔࡥࡤࡰࡪ࠭⃧") in bs_config:
    bstack1lllll111lll_opy_ = True
  elif bstack1l1l1l1_opy_ (u"ࠪࡥࡵࡶ⃨ࠧ") in bs_config:
    bstack11ll11lll1_opy_ = True
  else:
    bstack1l11llll11_opy_ = True
  bstack11l111l1_opy_ = {
    bstack1l1l1l1_opy_ (u"ࠫࡴࡨࡳࡦࡴࡹࡥࡧ࡯࡬ࡪࡶࡼࠫ⃩"): bstack11l1l1l1ll_opy_.bstack1lllll11l1l1_opy_(bs_config, framework),
    bstack1l1l1l1_opy_ (u"ࠬࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽ⃪ࠬ"): bstack1ll1l11ll_opy_.bstack111llll1_opy_(bs_config),
    bstack1l1l1l1_opy_ (u"࠭ࡰࡦࡴࡦࡽ⃫ࠬ"): bs_config.get(bstack1l1l1l1_opy_ (u"ࠧࡱࡧࡵࡧࡾ⃬࠭"), False),
    bstack1l1l1l1_opy_ (u"ࠨࡣࡸࡸࡴࡳࡡࡵࡧ⃭ࠪ"): bstack1l11llll11_opy_,
    bstack1l1l1l1_opy_ (u"ࠩࡤࡴࡵࡥࡡࡶࡶࡲࡱࡦࡺࡥࠨ⃮"): bstack11ll11lll1_opy_,
    bstack1l1l1l1_opy_ (u"ࠪࡸࡺࡸࡢࡰࡵࡦࡥࡱ࡫⃯ࠧ"): bstack1lllll111lll_opy_
  }
  return bstack11l111l1_opy_