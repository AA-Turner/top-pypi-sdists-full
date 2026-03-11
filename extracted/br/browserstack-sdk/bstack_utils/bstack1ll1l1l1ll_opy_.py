# coding: UTF-8
import sys
bstack1l1ll11_opy_ = sys.version_info [0] == 2
bstack11111l1_opy_ = 2048
bstack1111lll_opy_ = 7
def bstack1ll111_opy_ (bstack1111l1l_opy_):
    global bstack11l111l_opy_
    bstack11l1ll_opy_ = ord (bstack1111l1l_opy_ [-1])
    bstack11lll1l_opy_ = bstack1111l1l_opy_ [:-1]
    bstack111lll_opy_ = bstack11l1ll_opy_ % len (bstack11lll1l_opy_)
    bstack11llll1_opy_ = bstack11lll1l_opy_ [:bstack111lll_opy_] + bstack11lll1l_opy_ [bstack111lll_opy_:]
    if bstack1l1ll11_opy_:
        bstack11l1111_opy_ = unicode () .join ([unichr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    else:
        bstack11l1111_opy_ = str () .join ([chr (ord (char) - bstack11111l1_opy_ - (bstack111l11_opy_ + bstack11l1ll_opy_) % bstack1111lll_opy_) for bstack111l11_opy_, char in enumerate (bstack11llll1_opy_)])
    return eval (bstack11l1111_opy_)
import os
import json
import logging
import datetime
import threading
from bstack_utils.helper import bstack111l1l1111l_opy_, bstack1ll1lll111_opy_, get_host_info, bstack111l1ll1l1l_opy_, \
 bstack1l111l111_opy_, bstack11llll11l_opy_, error_handler, bstack111l111ll11_opy_, current_time
import bstack_utils.accessibility as bstack1ll11lll11_opy_
from bstack_utils.bstack111ll11l_opy_ import bstack1l1ll111l_opy_
from bstack_utils.bstack11l1llll_opy_ import bstack11l1ll1111_opy_
from bstack_utils.percy import bstack1ll11111l_opy_
from bstack_utils.config import Config
global_config = Config.get_instance()
logger = logging.getLogger(__name__)
percy = bstack1ll11111l_opy_()
@error_handler(class_method=False)
def bstack1lll11ll1l1l_opy_(bs_config, bstack11111l1ll_opy_):
  try:
    data = {
        bstack1ll111_opy_ (u"ࠧࡧࡱࡵࡱࡦࡺࠧ₃"): bstack1ll111_opy_ (u"ࠨ࡬ࡶࡳࡳ࠭₄"),
        bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡰࡥࡤࡶࡢࡲࡦࡳࡥࠨ₅"): bs_config.get(bstack1ll111_opy_ (u"ࠪࡴࡷࡵࡪࡦࡥࡷࡒࡦࡳࡥࠨ₆"), bstack1ll111_opy_ (u"ࠫࠬ₇")),
        bstack1ll111_opy_ (u"ࠬࡴࡡ࡮ࡧࠪ₈"): bs_config.get(bstack1ll111_opy_ (u"࠭ࡢࡶ࡫࡯ࡨࡓࡧ࡭ࡦࠩ₉"), os.path.basename(os.path.abspath(os.getcwd()))),
        bstack1ll111_opy_ (u"ࠧࡣࡷ࡬ࡰࡩࡥࡩࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ₊"): bs_config.get(bstack1ll111_opy_ (u"ࠨࡤࡸ࡭ࡱࡪࡉࡥࡧࡱࡸ࡮࡬ࡩࡦࡴࠪ₋")),
        bstack1ll111_opy_ (u"ࠩࡧࡩࡸࡩࡲࡪࡲࡷ࡭ࡴࡴࠧ₌"): bs_config.get(bstack1ll111_opy_ (u"ࠪࡦࡺ࡯࡬ࡥࡆࡨࡷࡨࡸࡩࡱࡶ࡬ࡳࡳ࠭₍"), bstack1ll111_opy_ (u"ࠫࠬ₎")),
        bstack1ll111_opy_ (u"ࠬࡹࡴࡢࡴࡷࡩࡩࡥࡡࡵࠩ₏"): current_time(),
        bstack1ll111_opy_ (u"࠭ࡴࡢࡩࡶࠫₐ"): bstack111l1ll1l1l_opy_(bs_config),
        bstack1ll111_opy_ (u"ࠧࡩࡱࡶࡸࡤ࡯࡮ࡧࡱࠪₑ"): get_host_info(),
        bstack1ll111_opy_ (u"ࠨࡥ࡬ࡣ࡮ࡴࡦࡰࠩₒ"): bstack1ll1lll111_opy_(),
        bstack1ll111_opy_ (u"ࠩࡥࡹ࡮ࡲࡤࡠࡴࡸࡲࡤ࡯ࡤࡦࡰࡷ࡭࡫࡯ࡥࡳࠩₓ"): os.environ.get(bstack1ll111_opy_ (u"ࠪࡆࡗࡕࡗࡔࡇࡕࡗ࡙ࡇࡃࡌࡡࡅ࡙ࡎࡒࡄࡠࡔࡘࡒࡤࡏࡄࡆࡐࡗࡍࡋࡏࡅࡓࠩₔ")),
        bstack1ll111_opy_ (u"ࠫ࡫ࡧࡩ࡭ࡧࡧࡣࡹ࡫ࡳࡵࡵࡢࡶࡪࡸࡵ࡯ࠩₕ"): os.environ.get(bstack1ll111_opy_ (u"ࠬࡈࡒࡐ࡙ࡖࡉࡗ࡙ࡔࡂࡅࡎࡣࡗࡋࡒࡖࡐࠪₖ"), False),
        bstack1ll111_opy_ (u"࠭ࡶࡦࡴࡶ࡭ࡴࡴ࡟ࡤࡱࡱࡸࡷࡵ࡬ࠨₗ"): bstack111l1l1111l_opy_(),
        bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧₘ"): bstack1lll11l11ll1_opy_(bs_config),
        bstack1ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡣࡩ࡫ࡴࡢ࡫࡯ࡷࠬₙ"): bstack1lll11l11lll_opy_(bstack11111l1ll_opy_),
        bstack1ll111_opy_ (u"ࠩࡳࡶࡴࡪࡵࡤࡶࡢࡱࡦࡶࠧₚ"): bstack1lll11l11l11_opy_(bs_config, bstack11111l1ll_opy_.get(bstack1ll111_opy_ (u"ࠪࡪࡷࡧ࡭ࡦࡹࡲࡶࡰࡥࡵࡴࡧࡧࠫₛ"), bstack1ll111_opy_ (u"ࠫࠬₜ"))),
        bstack1ll111_opy_ (u"ࠬࡨࡲࡰࡹࡶࡩࡷࡹࡴࡢࡥ࡮ࡅࡺࡺ࡯࡮ࡣࡷ࡭ࡴࡴࠧ₝"): bstack1l111l111_opy_(bs_config),
        bstack1ll111_opy_ (u"࠭ࡴࡦࡵࡷࡣࡴࡸࡣࡩࡧࡶࡸࡷࡧࡴࡪࡱࡱࠫ₞"): bstack1lll111lllll_opy_(bs_config)
    }
    return data
  except Exception as error:
    logger.error(bstack1ll111_opy_ (u"ࠢࡆࡺࡦࡩࡵࡺࡩࡰࡰࠣࡻ࡭࡯࡬ࡦࠢࡦࡶࡪࡧࡴࡪࡰࡪࠤࡵࡧࡹ࡭ࡱࡤࡨࠥ࡬࡯ࡳࠢࡗࡩࡸࡺࡈࡶࡤ࠽ࠤࠥࢁࡽࠣ₟").format(str(error)))
    return None
def bstack1lll11l11lll_opy_(framework):
  return {
    bstack1ll111_opy_ (u"ࠨࡨࡵࡥࡲ࡫ࡷࡰࡴ࡮ࡒࡦࡳࡥࠨ₠"): framework.get(bstack1ll111_opy_ (u"ࠩࡩࡶࡦࡳࡥࡸࡱࡵ࡯ࡤࡴࡡ࡮ࡧࠪ₡"), bstack1ll111_opy_ (u"ࠪࡔࡾࡺࡥࡴࡶࠪ₢")),
    bstack1ll111_opy_ (u"ࠫ࡫ࡸࡡ࡮ࡧࡺࡳࡷࡱࡖࡦࡴࡶ࡭ࡴࡴࠧ₣"): framework.get(bstack1ll111_opy_ (u"ࠬ࡬ࡲࡢ࡯ࡨࡻࡴࡸ࡫ࡠࡸࡨࡶࡸ࡯࡯࡯ࠩ₤")),
    bstack1ll111_opy_ (u"࠭ࡳࡥ࡭࡙ࡩࡷࡹࡩࡰࡰࠪ₥"): framework.get(bstack1ll111_opy_ (u"ࠧࡴࡦ࡮ࡣࡻ࡫ࡲࡴ࡫ࡲࡲࠬ₦")),
    bstack1ll111_opy_ (u"ࠨ࡮ࡤࡲ࡬ࡻࡡࡨࡧࠪ₧"): bstack1ll111_opy_ (u"ࠩࡳࡽࡹ࡮࡯࡯ࠩ₨"),
    bstack1ll111_opy_ (u"ࠪࡸࡪࡹࡴࡇࡴࡤࡱࡪࡽ࡯ࡳ࡭ࠪ₩"): framework.get(bstack1ll111_opy_ (u"ࠫࡹ࡫ࡳࡵࡈࡵࡥࡲ࡫ࡷࡰࡴ࡮ࠫ₪"))
  }
def bstack1lll111lllll_opy_(bs_config):
  bstack1ll111_opy_ (u"ࠧࠨࠢࠋࠢࠣࡖࡪࡺࡵࡳࡰࡶࠤࡹ࡮ࡥࠡࡶࡨࡷࡹࠦ࡯ࡳࡥ࡫ࡩࡸࡺࡲࡢࡶ࡬ࡳࡳࠦࡤࡢࡶࡤࠤ࡫ࡵࡲࠡࡤࡸ࡭ࡱࡪࠠࡴࡶࡤࡶࡹ࠴ࠊࠡࠢࠥࠦࠧ₫")
  if not bs_config:
    return {}
  bstack11111llll1l_opy_ = bstack1l1ll111l_opy_(bs_config).bstack11111l11l1l_opy_(bs_config)
  return bstack11111llll1l_opy_
def bstack1111llll11_opy_(bs_config, framework):
  bstack1l1lll1l_opy_ = False
  bstack11ll1l11_opy_ = False
  bstack1lll11l1111l_opy_ = False
  if bstack1ll111_opy_ (u"࠭ࡴࡶࡴࡥࡳࡘࡩࡡ࡭ࡧࠪ€") in bs_config:
    bstack1lll11l1111l_opy_ = True
  elif bstack1ll111_opy_ (u"ࠧࡢࡲࡳࠫ₭") in bs_config:
    bstack1l1lll1l_opy_ = True
  else:
    bstack11ll1l11_opy_ = True
  bstack1ll11l1l11_opy_ = {
    bstack1ll111_opy_ (u"ࠨࡱࡥࡷࡪࡸࡶࡢࡤ࡬ࡰ࡮ࡺࡹࠨ₮"): bstack11l1ll1111_opy_.bstack1lll11l1l1l1_opy_(bs_config, framework),
    bstack1ll111_opy_ (u"ࠩࡤࡧࡨ࡫ࡳࡴ࡫ࡥ࡭ࡱ࡯ࡴࡺࠩ₯"): bstack1ll11lll11_opy_.bstack1l1lll1111_opy_(bs_config),
    bstack1ll111_opy_ (u"ࠪࡴࡪࡸࡣࡺࠩ₰"): bs_config.get(bstack1ll111_opy_ (u"ࠫࡵ࡫ࡲࡤࡻࠪ₱"), False),
    bstack1ll111_opy_ (u"ࠬࡧࡵࡵࡱࡰࡥࡹ࡫ࠧ₲"): bstack11ll1l11_opy_,
    bstack1ll111_opy_ (u"࠭ࡡࡱࡲࡢࡥࡺࡺ࡯࡮ࡣࡷࡩࠬ₳"): bstack1l1lll1l_opy_,
    bstack1ll111_opy_ (u"ࠧࡵࡷࡵࡦࡴࡹࡣࡢ࡮ࡨࠫ₴"): bstack1lll11l1111l_opy_
  }
  return bstack1ll11l1l11_opy_
@error_handler(class_method=False)
def bstack1lll11l11ll1_opy_(bs_config):
  try:
    bstack1lll111lll1l_opy_ = json.loads(os.getenv(bstack1ll111_opy_ (u"ࠨࡄࡕࡓ࡜࡙ࡅࡓࡕࡗࡅࡈࡑ࡟ࡕࡇࡖࡘࡤࡇࡃࡄࡇࡖࡗࡎࡈࡉࡍࡋࡗ࡝ࡤࡉࡏࡏࡈࡌࡋ࡚ࡘࡁࡕࡋࡒࡒࡤ࡟ࡍࡍࠩ₵"), bstack1ll111_opy_ (u"ࠩࡾࢁࠬ₶")))
    bstack1lll111lll1l_opy_ = bstack1lll11l1l11l_opy_(bs_config, bstack1lll111lll1l_opy_)
    return {
        bstack1ll111_opy_ (u"ࠪࡷࡪࡺࡴࡪࡰࡪࡷࠬ₷"): bstack1lll111lll1l_opy_
    }
  except Exception as error:
    logger.error(bstack1ll111_opy_ (u"ࠦࡊࡾࡣࡦࡲࡷ࡭ࡴࡴࠠࡸࡪ࡬ࡰࡪࠦࡣࡳࡧࡤࡸ࡮ࡴࡧࠡࡩࡨࡸࡤࡧࡣࡤࡧࡶࡷ࡮ࡨࡩ࡭࡫ࡷࡽࡤࡹࡥࡵࡶ࡬ࡲ࡬ࡹࠠࡧࡱࡵࠤ࡙࡫ࡳࡵࡊࡸࡦ࠿ࠦࠠࡼࡿࠥ₸").format(str(error)))
    return {}
def bstack1lll11l1l11l_opy_(bs_config, bstack1lll111lll1l_opy_):
  if ((bstack1ll111_opy_ (u"ࠬࡺࡵࡳࡤࡲࡗࡨࡧ࡬ࡦࠩ₹") in bs_config or not bstack1l111l111_opy_(bs_config)) and bstack1ll11lll11_opy_.bstack1l1lll1111_opy_(bs_config)):
    bstack1lll111lll1l_opy_[bstack1ll111_opy_ (u"ࠨࡩ࡯ࡥ࡯ࡹࡩ࡫ࡅ࡯ࡥࡲࡨࡪࡪࡅࡹࡶࡨࡲࡸ࡯࡯࡯ࠤ₺")] = True
  return bstack1lll111lll1l_opy_
def bstack1lll11lllll1_opy_(array, bstack1lll11l11111_opy_, bstack1lll11l11l1l_opy_):
  result = {}
  for o in array:
    key = o[bstack1lll11l11111_opy_]
    result[key] = o[bstack1lll11l11l1l_opy_]
  return result
def bstack1lll11ll1l11_opy_(bstack11l1l1l11l_opy_=bstack1ll111_opy_ (u"ࠧࠨ₻")):
  bstack1lll11l111ll_opy_ = bstack1ll11lll11_opy_.on()
  bstack1lll111llll1_opy_ = bstack11l1ll1111_opy_.on()
  bstack1lll11l1l111_opy_ = percy.bstack1ll1l1l1l_opy_()
  if bstack1lll11l1l111_opy_ and not bstack1lll111llll1_opy_ and not bstack1lll11l111ll_opy_:
    return bstack11l1l1l11l_opy_ not in [bstack1ll111_opy_ (u"ࠨࡅࡅࡘࡘ࡫ࡳࡴ࡫ࡲࡲࡈࡸࡥࡢࡶࡨࡨࠬ₼"), bstack1ll111_opy_ (u"ࠩࡏࡳ࡬ࡉࡲࡦࡣࡷࡩࡩ࠭₽")]
  elif bstack1lll11l111ll_opy_ and not bstack1lll111llll1_opy_:
    return bstack11l1l1l11l_opy_ not in [bstack1ll111_opy_ (u"ࠪࡌࡴࡵ࡫ࡓࡷࡱࡗࡹࡧࡲࡵࡧࡧࠫ₾"), bstack1ll111_opy_ (u"ࠫࡍࡵ࡯࡬ࡔࡸࡲࡋ࡯࡮ࡪࡵ࡫ࡩࡩ࠭₿"), bstack1ll111_opy_ (u"ࠬࡒ࡯ࡨࡅࡵࡩࡦࡺࡥࡥࠩ⃀")]
  return bstack1lll11l111ll_opy_ or bstack1lll111llll1_opy_ or bstack1lll11l1l111_opy_
@error_handler(class_method=False)
def bstack1lll1l111lll_opy_(bstack11l1l1l11l_opy_, test=None):
  bstack1lll11l111l1_opy_ = bstack1ll11lll11_opy_.on()
  if not bstack1lll11l111l1_opy_ or bstack11l1l1l11l_opy_ not in [bstack1ll111_opy_ (u"࠭ࡔࡦࡵࡷࡖࡺࡴࡆࡪࡰ࡬ࡷ࡭࡫ࡤࠨ⃁")] or test == None:
    return None
  return {
    bstack1ll111_opy_ (u"ࠧࡢࡥࡦࡩࡸࡹࡩࡣ࡫࡯࡭ࡹࡿࠧ⃂"): bstack1lll11l111l1_opy_ and bstack11llll11l_opy_(threading.current_thread(), bstack1ll111_opy_ (u"ࠨࡣ࠴࠵ࡾࡖ࡬ࡢࡶࡩࡳࡷࡳࠧ⃃"), None) == True and bstack1ll11lll11_opy_.bstack11l1llll11_opy_(test[bstack1ll111_opy_ (u"ࠩࡷࡥ࡬ࡹࠧ⃄")])
  }
def bstack1lll11l11l11_opy_(bs_config, framework):
  bstack1l1lll1l_opy_ = False
  bstack11ll1l11_opy_ = False
  bstack1lll11l1111l_opy_ = False
  if bstack1ll111_opy_ (u"ࠪࡸࡺࡸࡢࡰࡕࡦࡥࡱ࡫ࠧ⃅") in bs_config:
    bstack1lll11l1111l_opy_ = True
  elif bstack1ll111_opy_ (u"ࠫࡦࡶࡰࠨ⃆") in bs_config:
    bstack1l1lll1l_opy_ = True
  else:
    bstack11ll1l11_opy_ = True
  bstack1ll11l1l11_opy_ = {
    bstack1ll111_opy_ (u"ࠬࡵࡢࡴࡧࡵࡺࡦࡨࡩ࡭࡫ࡷࡽࠬ⃇"): bstack11l1ll1111_opy_.bstack1lll11l1l1l1_opy_(bs_config, framework),
    bstack1ll111_opy_ (u"࠭ࡡࡤࡥࡨࡷࡸ࡯ࡢࡪ࡮࡬ࡸࡾ࠭⃈"): bstack1ll11lll11_opy_.bstack1111llll1_opy_(bs_config),
    bstack1ll111_opy_ (u"ࠧࡱࡧࡵࡧࡾ࠭⃉"): bs_config.get(bstack1ll111_opy_ (u"ࠨࡲࡨࡶࡨࡿࠧ⃊"), False),
    bstack1ll111_opy_ (u"ࠩࡤࡹࡹࡵ࡭ࡢࡶࡨࠫ⃋"): bstack11ll1l11_opy_,
    bstack1ll111_opy_ (u"ࠪࡥࡵࡶ࡟ࡢࡷࡷࡳࡲࡧࡴࡦࠩ⃌"): bstack1l1lll1l_opy_,
    bstack1ll111_opy_ (u"ࠫࡹࡻࡲࡣࡱࡶࡧࡦࡲࡥࠨ⃍"): bstack1lll11l1111l_opy_
  }
  return bstack1ll11l1l11_opy_